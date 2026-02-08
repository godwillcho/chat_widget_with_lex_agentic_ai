"""
connect_api.py — Runtime Amazon Connect API integration
────────────────────────────────────────────────────────────────────────────
Fetches view configurations from Amazon Connect at runtime with caching.
"""

import os
import json
import time
import boto3
from typing import Optional

# Cache for view config with timestamp
_view_cache = {}
_cache_ttl = 300  # 5 minutes TTL


def get_view_config() -> Optional[str]:
    """
    Fetch view configuration from Amazon Connect with caching.

    Returns:
        JSON string of view configuration or None if disabled
    """
    # Get instance ID and view ID from environment
    connect_instance_id = os.environ.get('CONNECT_INSTANCE_ID', '')
    view_id = os.environ.get('CONNECT_VIEW_ID', '')

    # If not configured, return None (no pre-chat form)
    if not connect_instance_id or not view_id:
        return None

    # Use the same region as the Lambda function (set by AWS automatically)
    # This ensures Lambda and Connect are in the same region
    lambda_region = os.environ.get('AWS_REGION', 'us-west-2')

    # Check cache
    cache_key = f"{connect_instance_id}:{view_id}"
    now = time.time()

    if cache_key in _view_cache:
        cached_data, cached_time = _view_cache[cache_key]
        if now - cached_time < _cache_ttl:
            return cached_data

    # Fetch from Connect API (using same region as Lambda)
    try:
        connect = boto3.client('connect', region_name=lambda_region)
        response = connect.describe_view(
            InstanceId=connect_instance_id,
            ViewId=view_id
        )

        # Extract the view data
        view = response.get('View', {})

        # Parse Content (returned as JSON string from API)
        content_str = view.get('Content', '{}')
        content = json.loads(content_str) if isinstance(content_str, str) else content_str

        # Build viewConfig object matching Amazon Connect format
        view_config = {
            "arn": view.get('Arn', ''),
            "id": view.get('Id', ''),
            "content": content,  # Parsed content object
            "name": view.get('Name', ''),
            "status": view.get('Status', ''),
            "type": view.get('Type', ''),
            "viewContentSha256": view.get('ViewContentSha256', '')
        }

        # Convert to JSON string
        view_config_json = json.dumps(view_config, separators=(',', ':'))

        # Cache it
        _view_cache[cache_key] = (view_config_json, now)

        return view_config_json

    except Exception as e:
        # Log error but don't fail - widget can still work without pre-chat form
        print(f"Error fetching view config from Connect: {e}")
        return None
