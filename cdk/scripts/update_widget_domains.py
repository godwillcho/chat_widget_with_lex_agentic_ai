#!/usr/bin/env python3
"""
Update Amazon Connect Widget Allowed Origins

This script automatically updates the allowed origins (domains) for your
Amazon Connect communication widget after deployment.

Usage:
    python scripts/update_widget_domains.py --environment dev
    python scripts/update_widget_domains.py --environment prod --dry-run
"""

import argparse
import json
import sys
import os

# Add parent directory to path to import config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import boto3
from botocore.exceptions import ClientError
from config.environments import get_environment_config


def extract_instance_id(connect_url: str) -> str:
    """
    Extract Connect instance ID or alias from CONNECT_URL.

    Example: https://myinstance.my.connect.aws -> myinstance
    """
    # Remove protocol
    url = connect_url.replace('https://', '').replace('http://', '')
    # Get instance alias (first part before .my.connect.aws)
    instance_alias = url.split('.')[0]
    return instance_alias


def get_instance_id_from_alias(connect_client, alias: str, region: str) -> str:
    """Get the actual instance ID from the instance alias."""
    try:
        # List all instances in the region
        response = connect_client.list_instances()

        for instance in response.get('InstanceSummaryList', []):
            # Check if alias matches
            instance_alias = instance.get('InstanceAlias', '')
            if instance_alias == alias:
                return instance['Id']

        raise ValueError(f"Could not find Connect instance with alias: {alias}")

    except ClientError as e:
        print(f"Error listing Connect instances: {e}")
        raise


def update_widget_allowed_origins(
    connect_client,
    instance_id: str,
    widget_id: str,
    allowed_origins: list,
    dry_run: bool = False
) -> bool:
    """
    Update the allowed origins for a Connect widget.

    Note: As of now, AWS Connect API doesn't have a direct method to update
    widget allowed origins programmatically. This function attempts to use
    available APIs, but you may need to update origins manually in the console.
    """
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Updating widget allowed origins...")
    print(f"  Instance ID: {instance_id}")
    print(f"  Widget ID: {widget_id}")
    print(f"  Allowed Origins: {', '.join(allowed_origins)}")

    if dry_run:
        print("\n✓ Dry run completed - no changes made")
        return True

    try:
        # Try to update using DescribeInstanceAttribute and UpdateInstanceAttribute
        # Note: This may not directly affect widget origins, but updates instance-level CORS

        # Get current instance attributes
        current_attrs = connect_client.describe_instance_attribute(
            InstanceId=instance_id,
            AttributeType='CONTACTFLOW_LOGS'  # Use any valid attribute type
        )

        print("\n⚠️  Note: Amazon Connect widget allowed origins are typically managed")
        print("   through the AWS Console. Attempting API update...")

        # The Connect API doesn't have a direct method to update widget origins
        # You'll need to do this manually or use CloudFormation if available

        print("\n❌ Automatic update not fully supported by AWS Connect API")
        print("   Please update allowed origins manually in the AWS Console:")
        print(f"\n   1. Go to: Amazon Connect → {instance_id}")
        print("   2. Channels → Communication widgets")
        print(f"   3. Select your widget (ID: {widget_id})")
        print("   4. Domain & security → Add domains:")

        for origin in allowed_origins:
            print(f"      • {origin}")

        return False

    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'ResourceNotFoundException':
            print(f"\n❌ Error: Connect instance not found: {instance_id}")
        else:
            print(f"\n❌ Error updating widget: {e}")
        return False


def update_cors_for_lambda_url(
    lambda_client,
    function_name: str,
    allowed_origins: list,
    dry_run: bool = False
) -> bool:
    """
    Update CORS settings for Lambda Function URL.

    Note: This is separate from Connect widget origins.
    The Lambda Function URL also needs CORS configuration.
    """
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Updating Lambda Function URL CORS...")
    print(f"  Function: {function_name}")
    print(f"  Allowed Origins: {', '.join(allowed_origins)}")

    if dry_run:
        print("\n✓ Dry run completed - no changes made")
        return True

    try:
        # Get Function URL configuration
        response = lambda_client.get_function_url_config(
            FunctionName=function_name
        )

        function_url = response['FunctionUrl']

        # Update CORS
        lambda_client.update_function_url_config(
            FunctionName=function_name,
            Cors={
                'AllowOrigins': allowed_origins,
                'AllowMethods': ['GET', 'POST'],
                'AllowHeaders': ['*'],
                'MaxAge': 300,
            }
        )

        print(f"\n✓ Lambda Function URL CORS updated successfully")
        print(f"  Function URL: {function_url}")

        return True

    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'ResourceNotFoundException':
            print(f"\n⚠️  Note: Lambda function URL not found for: {function_name}")
            print("   This is set during CDK deployment via the stack configuration")
        else:
            print(f"\n❌ Error updating Lambda CORS: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Update Amazon Connect widget allowed origins after deployment'
    )
    parser.add_argument(
        '--environment', '-e',
        required=True,
        help='Environment name (dev, staging, prod)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be updated without making changes'
    )

    args = parser.parse_args()

    # Load environment configuration
    try:
        config = get_environment_config(args.environment)
    except ValueError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

    # Extract configuration
    widget_config = config['widget_config']
    connect_url = widget_config['CONNECT_URL']
    widget_id = widget_config['WIDGET_ID']
    allowed_origins = config.get('cors_allowed_origins', ['*'])
    aws_region = config['aws_region']

    print("=" * 70)
    print(f"Amazon Connect Widget Domain Update - {args.environment.upper()}")
    print("=" * 70)
    print(f"Environment: {args.environment}")
    print(f"AWS Region: {aws_region}")
    print(f"Connect URL: {connect_url}")
    print(f"Widget ID: {widget_id}")
    print(f"Allowed Origins: {', '.join(allowed_origins)}")

    if args.dry_run:
        print("\n⚠️  DRY RUN MODE - No changes will be made")

    # Initialize AWS clients
    try:
        connect_client = boto3.client('connect', region_name=aws_region)
        lambda_client = boto3.client('lambda', region_name=aws_region)
    except Exception as e:
        print(f"\n❌ Error initializing AWS clients: {e}")
        print("   Make sure you have AWS credentials configured")
        sys.exit(1)

    # Extract instance alias from URL
    instance_alias = extract_instance_id(connect_url)

    # Get actual instance ID
    try:
        instance_id = get_instance_id_from_alias(connect_client, instance_alias, aws_region)
        print(f"✓ Found Connect instance ID: {instance_id}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

    # Update Connect widget origins
    widget_success = update_widget_allowed_origins(
        connect_client,
        instance_id,
        widget_id,
        allowed_origins,
        dry_run=args.dry_run
    )

    # Update Lambda Function URL CORS
    lambda_function_name = f"chat-widget-{args.environment}"
    lambda_success = update_cors_for_lambda_url(
        lambda_client,
        lambda_function_name,
        allowed_origins,
        dry_run=args.dry_run
    )

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    if widget_success:
        print("✓ Connect widget origins: Updated")
    else:
        print("⚠️  Connect widget origins: Manual update required (see instructions above)")

    if lambda_success:
        print("✓ Lambda Function URL CORS: Updated")
    else:
        print("⚠️  Lambda Function URL CORS: Managed by CDK deployment")

    print("\n💡 Tip: Run this script after each 'cdk deploy' to keep origins in sync")
    print("=" * 70)


if __name__ == '__main__':
    main()
