# Pre-Chat Form Update Guide

## Overview

The pre-chat form configuration is now stored as **static files** in the codebase that are deployed with your Lambda function. This approach is simpler and more reliable than runtime API fetching.

## File Locations

- **Configuration File**: [`lambda_functions/chat_widget/view_configs.py`](../lambda_functions/chat_widget/view_configs.py)
- **Environment Settings**: [`config/environments.py`](../config/environments.py)

## How It Works

1. View configurations are stored in `view_configs.py` with separate configs for each environment (dev, staging, prod)
2. The `ENVIRONMENT` variable in `environments.py` determines which view config to use
3. The view config is embedded in the widget code at deployment time
4. No runtime API calls to Amazon Connect are needed

## Updating the Pre-Chat Form

### Method 1: Using AWS CLI (Recommended)

1. **Fetch the latest view configuration from Amazon Connect**:

```bash
aws connect describe-view \
    --instance-id e75a053a-60c7-45f3-83f7-a24df6d3b52d \
    --view-id 0b286577-6474-4a95-abc9-6fef67e1521c \
    --region us-west-2 \
    --output json
```

2. **Copy the `View` object from the response**

3. **Update the appropriate environment** in [`view_configs.py`](../lambda_functions/chat_widget/view_configs.py):
   - For dev: Update `VIEW_CONFIG_DEV`
   - For staging: Update `VIEW_CONFIG_STAGING`
   - For prod: Update `VIEW_CONFIG_PROD`

4. **Redeploy**:

```bash
cd cdk
cdk deploy -c environment=dev --require-approval never
```

### Method 2: Using Python Script

Create a script to fetch and format the view config:

```python
import boto3
import json

# Configure your Connect instance
INSTANCE_ID = 'e75a053a-60c7-45f3-83f7-a24df6d3b52d'
VIEW_ID = '0b286577-6474-4a95-abc9-6fef67e1521c'
REGION = 'us-west-2'

# Fetch view from Connect
connect = boto3.client('connect', region_name=REGION)
response = connect.describe_view(
    InstanceId=INSTANCE_ID,
    ViewId=VIEW_ID
)

# Get the View object
view = response['View']

# Parse the Content field (it's returned as a JSON string)
import json
content_str = view['Content']
content = json.loads(content_str)

# Build the config
view_config = {
    "arn": view['Arn'],
    "id": view['Id'],
    "content": content,  # This is now a Python dict
    "name": view['Name'],
    "status": view['Status'],
    "type": view['Type'],
    "viewContentSha256": view.get('ViewContentSha256', '')
}

# Print formatted Python code
print("Copy this to view_configs.py:\n")
print(f"VIEW_CONFIG_DEV = {json.dumps(view_config, indent=4)}")
```

Save this as `fetch_view_config.py` and run:

```bash
python fetch_view_config.py
```

Then copy the output into `view_configs.py`.

### Method 3: Manual Copy from AWS Console

1. **Go to Amazon Connect Console** → Your instance → **Channels** → **Chat widgets**
2. Click on your widget → **Pre-chat form** tab
3. Note the View ID
4. Use the AWS CLI method above to fetch the configuration

## File Structure

### view_configs.py

```python
VIEW_CONFIGS = {
    "dev": VIEW_CONFIG_DEV,
    "staging": VIEW_CONFIG_STAGING,
    "prod": VIEW_CONFIG_PROD,
}

VIEW_CONFIG_DEV = {
    "arn": "arn:aws:connect:...",
    "id": "view-id-here",
    "content": {
        "InputSchema": { ... },  # Form validation schema
        "Template": { ... },     # Form UI definition
        "Actions": [ ... ]       # Available actions
    },
    "name": "CONSENT_AND_IDENTIFICATION",
    "status": "PUBLISHED",
    "type": "CUSTOMER_MANAGED",
    "viewContentSha256": "hash-here"
}
```

### environments.py

```python
"widget_config": {
    "ENVIRONMENT": "dev",  # Selects VIEW_CONFIG_DEV
    ...
}
```

## Important Notes

### ✅ Benefits of This Approach

- **No runtime API calls** - Faster, no Connect API permissions needed
- **Version controlled** - View configs are in git
- **Predictable** - Same config every time, no caching issues
- **Simple** - Easy to update and deploy

### ⚠️ Things to Remember

1. **Content Field**: When fetching from AWS API, the `Content` field is a JSON string. You need to parse it before putting it in `view_configs.py`:
   ```python
   content = json.loads(view['Content'])
   ```

2. **Separate Configs**: Each environment can have its own view configuration
   - Dev might have test fields
   - Prod has the real form

3. **Redeploy Required**: After updating `view_configs.py`, you must redeploy for changes to take effect

4. **Python Syntax**: Make sure the config is valid Python dict syntax:
   - Use `True`/`False` (not `true`/`false`)
   - Use proper quotes
   - Check indentation

## Troubleshooting

### "View config for environment 'dev' is not populated"

**Cause**: The `VIEW_CONFIG_DEV` (or staging/prod) has empty values.

**Fix**: Update the config in `view_configs.py` with your actual view data.

### Pre-chat form not showing

**Possible causes**:
1. View config not properly formatted in `view_configs.py`
2. Wrong environment selected in `environments.py`
3. Need to add Function URL to Amazon Connect allowed origins

**Debug**:
```bash
# Check what's deployed
curl https://YOUR-FUNCTION-URL/ | grep viewConfig

# Check CloudWatch logs
aws logs tail /aws/lambda/chat-widget-dev --region us-west-2 --since 10m
```

### Python syntax errors when deploying

**Cause**: Invalid Python syntax in `view_configs.py`

**Fix**:
- Use a Python IDE to validate syntax
- Ensure all brackets/braces are closed
- Use proper Python boolean values (`True`/`False`)
- Escape quotes properly

## Multiple Organizations

Each environment can have its own view config. For example:

```python
VIEW_CONFIGS = {
    "dev": VIEW_CONFIG_DEV,
    "staging": VIEW_CONFIG_STAGING,
    "prod": VIEW_CONFIG_PROD,
    "org2-prod": VIEW_CONFIG_ORG2_PROD,  # Different org
}
```

Then deploy:
```bash
cdk deploy -c environment=org2-prod
```

## Migration from Runtime API Approach

If you're coming from the previous runtime API fetching approach:

**Removed**:
- `connect_api.py` file (no longer used)
- `CONNECT_INSTANCE_ID` environment variable
- `CONNECT_VIEW_ID` environment variable
- IAM permission `connect:DescribeView`

**Added**:
- `view_configs.py` file with static configs
- `ENVIRONMENT` environment variable

**Same**:
- Everything else works the same way
- Same widget functionality
- Same Amazon Connect credentials needed
