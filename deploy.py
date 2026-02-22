"""
deploy.py - Deploy the Trident United Way Stability360 widget to AWS.

Usage:
    python deploy.py

Creates/updates the CloudFormation stack, then pushes Lambda code.
"""
import os
import sys
import io
import zipfile
import time
import boto3
from botocore.exceptions import ClientError

# Import config
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config.environments import get_environment_config

ENV_NAME = "dev"
STACK_NAME = "ChatWidget-Dev"
TEMPLATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "template.yaml")
LAMBDA_CODE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lambda_functions", "chat_widget")


def load_template():
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        return f.read()


def build_parameters(config):
    """Map environments.py config to CloudFormation parameter keys."""
    wc = config["widget_config"]
    lc = config["lambda_config"]
    return [
        {"ParameterKey": "Environment", "ParameterValue": wc["ENVIRONMENT"]},
        {"ParameterKey": "ViewMode", "ParameterValue": wc["VIEW_MODE"]},
        {"ParameterKey": "CompanyName", "ParameterValue": wc["COMPANY_NAME"]},
        {"ParameterKey": "ConnectUrl", "ParameterValue": wc["CONNECT_URL"]},
        {"ParameterKey": "ConnectInstanceId", "ParameterValue": wc["CONNECT_INSTANCE_ID"]},
        {"ParameterKey": "ContactFlowId", "ParameterValue": wc["CONTACT_FLOW_ID"]},
        {"ParameterKey": "WidgetId", "ParameterValue": wc["WIDGET_ID"]},
        {"ParameterKey": "SnippetId", "ParameterValue": wc["SNIPPET_ID"]},
        {"ParameterKey": "SecurityKey", "ParameterValue": wc["SECURITY_KEY"]},
        {"ParameterKey": "ColorNavy", "ParameterValue": wc["COLOR_NAVY"]},
        {"ParameterKey": "ColorBlue", "ParameterValue": wc["COLOR_BLUE"]},
        {"ParameterKey": "ColorGold", "ParameterValue": wc["COLOR_GOLD"]},
        {"ParameterKey": "ColorGoldLight", "ParameterValue": wc["COLOR_GOLD_LIGHT"]},
        {"ParameterKey": "WidgetHeader", "ParameterValue": wc["WIDGET_HEADER"]},
        {"ParameterKey": "WidgetBotName", "ParameterValue": wc["WIDGET_BOT_NAME"]},
        {"ParameterKey": "ServiceName", "ParameterValue": wc["SERVICE_NAME"]},
        {"ParameterKey": "ServiceTagline", "ParameterValue": wc["SERVICE_TAGLINE"]},
        {"ParameterKey": "CompanyTagline", "ParameterValue": wc["COMPANY_TAGLINE"]},
        {"ParameterKey": "FooterTagline", "ParameterValue": wc["FOOTER_TAGLINE"]},
        {"ParameterKey": "LambdaMemory", "ParameterValue": str(lc["memory_size"])},
        {"ParameterKey": "LambdaTimeout", "ParameterValue": str(lc["timeout"])},
    ]


def zip_lambda_code(code_dir):
    """Zip the Lambda code directory into a bytes buffer."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(code_dir):
            # Skip __pycache__
            dirs[:] = [d for d in dirs if d != "__pycache__"]
            for fname in files:
                if fname.endswith(".pyc"):
                    continue
                full_path = os.path.join(root, fname)
                arc_name = os.path.relpath(full_path, code_dir)
                zf.write(full_path, arc_name)
    buf.seek(0)
    return buf.read()


def deploy_stack(cfn, template_body, parameters):
    """Create or update the CloudFormation stack."""
    try:
        cfn.describe_stacks(StackName=STACK_NAME)
        stack_exists = True
    except ClientError:
        stack_exists = False

    if stack_exists:
        print(f"Updating stack: {STACK_NAME}")
        try:
            cfn.update_stack(
                StackName=STACK_NAME,
                TemplateBody=template_body,
                Parameters=parameters,
                Capabilities=["CAPABILITY_NAMED_IAM"],
            )
            waiter = cfn.get_waiter("stack_update_complete")
        except ClientError as e:
            if "No updates are to be performed" in str(e):
                print("Stack is already up to date.")
                return
            raise
    else:
        print(f"Creating stack: {STACK_NAME}")
        cfn.create_stack(
            StackName=STACK_NAME,
            TemplateBody=template_body,
            Parameters=parameters,
            Capabilities=["CAPABILITY_NAMED_IAM"],
        )
        waiter = cfn.get_waiter("stack_create_complete")

    print("Waiting for stack operation to complete...")
    waiter.wait(StackName=STACK_NAME, WaiterConfig={"Delay": 10, "MaxAttempts": 60})
    print("Stack operation complete.")


def get_stack_outputs(cfn):
    """Get stack outputs as a dict."""
    resp = cfn.describe_stacks(StackName=STACK_NAME)
    outputs = resp["Stacks"][0].get("Outputs", [])
    return {o["OutputKey"]: o["OutputValue"] for o in outputs}


def update_lambda_code(lambda_client, function_name, zip_bytes):
    """Push zipped code to the Lambda function."""
    print(f"Updating Lambda code: {function_name}")
    lambda_client.update_function_code(
        FunctionName=function_name,
        ZipFile=zip_bytes,
    )
    # Wait for update to complete
    waiter = lambda_client.get_waiter("function_updated_v2")
    waiter.wait(FunctionName=function_name)
    print("Lambda code updated.")


def main():
    config = get_environment_config(ENV_NAME)
    region = config["aws_region"]

    print(f"Deploying Stability360 ({ENV_NAME}) to {region}")
    print("-" * 50)

    cfn = boto3.client("cloudformation", region_name=region)
    lambda_client = boto3.client("lambda", region_name=region)

    # Step 1: Deploy CloudFormation stack
    template_body = load_template()
    parameters = build_parameters(config)
    deploy_stack(cfn, template_body, parameters)

    # Step 2: Get outputs
    outputs = get_stack_outputs(cfn)
    function_name = outputs.get("FunctionName")
    function_url = outputs.get("FunctionUrl")

    if not function_name:
        print("ERROR: Could not get FunctionName from stack outputs.")
        sys.exit(1)

    # Step 3: Package and push Lambda code
    print(f"Packaging Lambda code from: {LAMBDA_CODE_DIR}")
    zip_bytes = zip_lambda_code(LAMBDA_CODE_DIR)
    print(f"Zip size: {len(zip_bytes):,} bytes")
    update_lambda_code(lambda_client, function_name, zip_bytes)

    # Done
    print()
    print("=" * 50)
    print("Deployment complete!")
    print(f"Function URL: {function_url}")
    print(f"Kiosk mode:   {function_url}?mode=kiosk")
    print("=" * 50)


if __name__ == "__main__":
    main()
