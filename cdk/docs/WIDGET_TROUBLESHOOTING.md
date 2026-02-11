# Widget Troubleshooting Guide

## Lambda Layer Implementation ✅

A Lambda Layer has been successfully created and deployed with boto3 dependencies, following AWS Connect documentation best practices.

**Layer Details:**
- Name: `chat-widget-dependencies-dev`
- Size: ~17MB
- Contains: boto3, botocore, and all dependencies
- ARN: `arn:aws:lambda:us-west-2:551642657889:layer:chat-widget-dependencies-dev:1`

## Current Configuration

**Lambda Function URL:**
```
https://kfe6wjm4tyqrwszjh7jhugjima0riwot.lambda-url.us-west-2.on.aws/
```

**Amazon Connect Configuration:**
- Instance ID: `e75a053a-60c7-45f3-83f7-a24df6d3b52d`
- Contact Flow ID: `b1cc0b5a-09d5-4c50-ad1f-5b9b55f75336`
- Widget ID: `497c0ff9-3611-45dc-a56d-21aa65f76969`
- Region: `us-west-2`

## Troubleshooting Steps

### Step 1: Open the Widget Page

1. Open the Lambda Function URL in your browser:
   ```
   https://kfe6wjm4tyqrwszjh7jhugjima0riwot.lambda-url.us-west-2.on.aws/
   ```

2. Open Browser Developer Tools (F12)
   - Chrome/Edge: F12 or Right-click → Inspect
   - Firefox: F12 or Right-click → Inspect Element

### Step 2: Check Browser Console

Look for JavaScript errors in the Console tab:

**Common Issues:**

1. **Widget Script Not Loading**
   ```
   Failed to load resource: net::ERR_FAILED
   https://nextgencxsolutions.my.connect.aws/connectwidget/static/amazon-connect-chat-interface-client.js
   ```
   **Cause:** Amazon Connect CDN script cannot be loaded
   **Fix:** Verify the Connect URL is correct and accessible

2. **Authentication Error**
   ```
   Error fetching authentication token
   ```
   **Cause:** `/token` endpoint is failing
   **Check:** Network tab for POST to `/token` - should return 200 with credentials

3. **CORS Error**
   ```
   Access to fetch at '...' has been blocked by CORS policy
   ```
   **Cause:** CORS configuration issue
   **Fix:** Already configured with `Access-Control-Allow-Origin: *`

### Step 3: Check Network Tab

1. Switch to Network tab in Developer Tools
2. Reload the page
3. Look for these requests:

**Expected Requests:**

| Request | Status | Response |
|---------|--------|----------|
| GET `/` | 200 | HTML page with widget scripts |
| GET `amazon-connect-chat-interface-client.js` | 200 | Widget JavaScript from Amazon Connect |
| POST `/token` | 200 | JSON with session credentials |

**Check POST /token Response:**
```json
{
  "data": {
    "contactFlowId": "b1cc0b5a-09d5-4c50-ad1f-5b9b55f75336",
    "instanceId": "e75a053a-60c7-45f3-83f7-a24df6d3b52d",
    "participantToken": "...",
    "contactId": "...",
    "participantId": "..."
  }
}
```

### Step 4: Verify Amazon Connect Configuration

1. **Check Contact Flow is Published:**
   - Go to Amazon Connect Console
   - Navigate to Routing → Contact Flows
   - Find "CUSTOMERS-INBOUND-FLOW"
   - Verify it's Published (not Draft)

2. **Check Widget Configuration:**
   - Go to Amazon Connect Console
   - Navigate to Channels → Chat widgets
   - Verify widget ID matches: `497c0ff9-3611-45dc-a56d-21aa65f76969`

3. **Check IAM Permissions:**
   - Lambda function has `connect:StartChatContact` permission ✅
   - Lambda function has `connect:DescribeContactFlow` permission ✅

### Step 5: Test Token Generation

Open a new terminal and test the token endpoint directly:

```bash
curl -X POST https://kfe6wjm4tyqrwszjh7jhugjima0riwot.lambda-url.us-west-2.on.aws/token \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Expected Response:**
```json
{
  "data": {
    "contactFlowId": "b1cc0b5a-09d5-4c50-ad1f-5b9b55f75336",
    "instanceId": "e75a053a-60c7-45f3-83f7-a24df6d3b52d",
    "participantToken": "...",
    "contactId": "...",
    "participantId": "..."
  }
}
```

If you get an error, check CloudWatch logs:
```bash
aws logs tail /aws/lambda/chat-widget-dev --region us-west-2 --follow
```

### Step 6: Check CloudWatch Logs

1. Go to AWS Console → CloudWatch → Log Groups
2. Find log group: `/aws/lambda/chat-widget-dev`
3. Look for recent log streams
4. Check for errors:
   - `CONNECT_INSTANCE_ID not configured` → Update config/environments.py
   - `CONTACT_FLOW_ID not configured` → Update config/environments.py
   - `Error generating JWT token` → Check IAM permissions
   - `AccessDeniedException` → Lambda role needs `connect:StartChatContact` permission

## Common Widget Issues

### Widget Doesn't Appear

**Possible Causes:**
1. Widget script failed to load from Amazon Connect CDN
2. JavaScript error preventing initialization
3. Widget ID doesn't match Amazon Connect configuration
4. Contact flow is not published
5. Amazon Connect instance is not active

**Debug Steps:**
1. Check browser console for JavaScript errors
2. Verify widget script loads in Network tab
3. Verify contact flow is published in Connect console
4. Test token generation endpoint directly

### Widget Shows "Something Went Wrong"

**Possible Causes:**
1. Authentication credentials are invalid
2. Contact flow doesn't exist or is not published
3. Instance ID is incorrect
4. StartChatContact API call failed

**Debug Steps:**
1. Check POST /token response in Network tab
2. Verify credentials contain all required fields
3. Check CloudWatch logs for StartChatContact errors
4. Verify contact flow ID in Amazon Connect console

### Widget Loads But Can't Start Chat

**Possible Causes:**
1. Contact flow has errors
2. Contact flow is not associated with the widget
3. Hours of operation restrict chat availability
4. Chat concurrency limits reached

**Debug Steps:**
1. Test contact flow in Amazon Connect console
2. Check contact flow associations in widget settings
3. Verify hours of operation allow chat
4. Check Amazon Connect service quotas

## Next Steps

If the widget still doesn't show after checking all the above:

1. **Verify the widget script is loading:**
   - Check if `amazon_connect` function is defined in browser console
   - Type `window.amazon_connect` in console - should not be `undefined`

2. **Verify the authenticate callback is working:**
   - Add console.log in connect_authenticate.js to debug
   - Check if POST /token is being called when widget initializes

3. **Check Amazon Connect approved origins:**
   - Go to Amazon Connect Console → Application Integration
   - Add Lambda Function URL to approved origins if needed:
     ```
     https://kfe6wjm4tyqrwszjh7jhugjima0riwot.lambda-url.us-west-2.on.aws
     ```

4. **Test with a simple static widget:**
   - Get a fresh widget snippet from Amazon Connect console
   - Copy it into a basic HTML file
   - Test if it works standalone
   - Compare with current implementation

## Files Modified

### Lambda Layer Files
- `cdk/layers/python_dependencies/requirements.txt` - Dependencies specification
- `cdk/layers/python_dependencies/python/` - Installed packages (boto3, etc.)
- `cdk/layers/python_dependencies/build_layer.sh` - Build script

### CDK Stack Updates
- `cdk/stacks/web_app_stack.py` - Added Lambda Layer creation and attachment

### Deployment
- Lambda Layer: `arn:aws:lambda:us-west-2:551642657889:layer:chat-widget-dependencies-dev:1`
- Function updated with layer attachment
- All dependencies now available via layer (17MB)
