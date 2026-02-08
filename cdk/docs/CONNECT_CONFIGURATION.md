# Amazon Connect Configuration Guide

## The Issue

The "Something went wrong" error occurs because the Amazon Connect widget needs to be configured with **your specific Amazon Connect instance credentials**.

The current deployment is using **placeholder credentials** that need to be replaced with your actual Amazon Connect instance details.

---

## Quick Fix: Configure Your Connect Instance

### Step 1: Get Your Amazon Connect Widget Details

1. **Log into AWS Console**
2. Go to **Amazon Connect**
3. Select your Connect instance
4. Go to **Channels** → **Chat widgets**
5. Create or select a chat widget
6. Click **Show security key**
7. Copy the widget code snippet

### Step 2: Extract Required Values

From the widget snippet, you need:

1. **CONNECT_URL**: The Connect instance URL
   ```
   Example: https://your-instance.my.connect.aws
   ```

2. **WIDGET_ID**: The widget ID (UUID format)
   ```
   Example: abc12345-1234-5678-90ab-cdef12345678
   ```

3. **SNIPPET_ID**: The encrypted snippet ID (long base64 string)
   ```
   Example: QVFJREF...base64...string
   ```

### Step 3: Update Configuration

Edit **`cdk/config/environments.py`** and update your environment:

```python
"dev": {
    # ... other config ...
    "widget_config": {
        "COMPANY_NAME": "Your Organization Name",
        "CONNECT_URL": "https://your-instance.my.connect.aws",  # ← Change this
        "WIDGET_ID": "your-widget-id-here",                      # ← Change this
        "SNIPPET_ID": "your-snippet-id-here",                    # ← Change this
        # ... rest of config ...
    },
}
```

### Step 4: Redeploy

```bash
cd cdk
export PATH="/c/Program Files/nodejs:/c/Users/godwi/AppData/Roaming/npm:$PATH"
cdk deploy -c environment=dev --require-approval never
```

---

## Alternative: Use Environment Variables (Recommended for Multiple Deployments)

Instead of hardcoding in `environments.py`, you can use environment variables:

### 1. Create a `.env` file

```bash
# cdk/.env.dev
COMPANY_NAME="Your Organization Name"
CONNECT_URL="https://your-instance.my.connect.aws"
WIDGET_ID="your-widget-id-here"
SNIPPET_ID="your-snippet-id-here"
COLOR_NAVY="#10264a"
COLOR_GOLD="#f5a623"
```

### 2. Load environment variables before deployment

```bash
cd cdk

# Load environment variables
export $(cat .env.dev | xargs)

# Deploy
cdk deploy -c environment=dev --require-approval never
```

---

## For Multiple Deployments/Organizations

### Scenario: Different Organizations Using Same Codebase

Create separate environment files:

```
cdk/
├── .env.org1-dev
├── .env.org1-prod
├── .env.org2-dev
├── .env.org2-prod
└── config/
    └── environments.py
```

**Example `.env.org1-dev`:**
```bash
COMPANY_NAME="Organization 1"
CONNECT_URL="https://org1-instance.my.connect.aws"
WIDGET_ID="org1-widget-id"
SNIPPET_ID="org1-snippet-id"
```

**Example `.env.org2-dev`:**
```bash
COMPANY_NAME="Organization 2"
CONNECT_URL="https://org2-instance.my.connect.aws"
WIDGET_ID="org2-widget-id"
SNIPPET_ID="org2-snippet-id"
```

**Deploy to different organizations:**

```bash
# Deploy for Organization 1
export $(cat .env.org1-dev | xargs)
cdk deploy -c environment=dev

# Deploy for Organization 2
export $(cat .env.org2-dev | xargs)
cdk deploy -c environment=dev
```

---

## Creating Your Amazon Connect Instance (If You Don't Have One)

### 1. Create Connect Instance

1. Go to AWS Console → Amazon Connect
2. Click **Create instance**
3. Choose **Store users within Amazon Connect**
4. Enter instance name (e.g., `my-211-helpline`)
5. Create admin user
6. Complete setup

### 2. Set Up Chat Widget

1. In Connect instance, go to **Channels** → **Chat widgets**
2. Click **Add a new chat widget**
3. Configure:
   - **Widget name**: "211 Helpline Chat"
   - **Welcome message**: "Welcome to 211! How can we help you today?"
4. Click **Create**
5. Copy the widget code snippet

### 3. Create Contact Flow

1. Go to **Routing** → **Contact flows**
2. Click **Create contact flow**
3. Add blocks:
   - **Entry point** → **Set working queue**
   - **Set working queue** → **Transfer to queue**
4. Save and publish
5. Note the Contact Flow ID

### 4. Configure Pre-Chat Form (Optional)

The current deployment includes a pre-chat form that collects:
- First Name
- Middle Initial
- Last Name
- Phone Number
- Email

If you want to use a different form:
1. Create a custom View in Amazon Connect
2. Copy the View configuration JSON
3. Update `cdk/lambda/view_config.py`

---

## Common Issues and Solutions

### Issue 1: "Something went wrong" Error

**Cause**: Invalid or missing Connect credentials

**Solution**:
1. Verify CONNECT_URL, WIDGET_ID, and SNIPPET_ID are correct
2. Ensure they're from the same Amazon Connect instance
3. Check that the Connect instance is accessible
4. Redeploy after updating configuration

### Issue 2: Widget Loads But Can't Start Chat

**Cause**: Contact flow not configured or wrong Contact Flow ID

**Solution**:
1. Create a contact flow in Amazon Connect
2. Assign it to your chat widget
3. Update the widget configuration

### Issue 3: CORS Errors in Browser Console

**Cause**: CORS not properly configured

**Solution**:
1. In Connect Console, go to **Application integration**
2. Add your domain to approved origins
3. For testing, approved origins can be `*`

### Issue 4: Widget Shows but Form Doesn't Display

**Cause**: View configuration mismatch

**Solution**:
1. Ensure the View ID in `view_config.py` matches your Connect instance
2. Recreate the View in Amazon Connect console
3. Update `view_config.py` with new View JSON

---

## Testing Your Configuration

### 1. Test Widget Loading

```bash
# Test in browser
curl -v https://your-lambda-url/
```

Should return HTML with no errors.

### 2. Test Different Modes

- Standard: `https://your-lambda-url/`
- Kiosk: `https://your-lambda-url/?mode=kiosk`
- Mobile: `https://your-lambda-url/?mode=mobile`

### 3. Check Browser Console

Open browser DevTools (F12) and check:
- No CORS errors
- Connect widget loads successfully
- No 404 errors for Connect resources

### 4. Test Chat Flow

1. Open widget
2. Fill out pre-chat form
3. Click "I Consent & Start Chat"
4. Should connect to agent or queue

---

## Multi-Organization Deployment Strategy

### Strategy 1: Separate Stacks Per Organization

```bash
# Organization 1
export $(cat .env.org1 | xargs)
cdk deploy --stack-name Project-Org1-Dev

# Organization 2
export $(cat .env.org2 | xargs)
cdk deploy --stack-name Project-Org2-Dev
```

### Strategy 2: Single Stack, Multiple Configurations

Use environment variables to switch between organizations without redeploying.

### Strategy 3: Separate AWS Accounts

Deploy to different AWS accounts using AWS profiles:

```bash
# Org 1 (Account A)
AWS_PROFILE=org1-account
export $(cat .env.org1 | xargs)
cdk deploy

# Org 2 (Account B)
AWS_PROFILE=org2-account
export $(cat .env.org2 | xargs)
cdk deploy
```

---

## Security Best Practices

### 1. Never Commit Credentials

Add to `.gitignore`:
```
.env*
*.env
.env.local
```

### 2. Use AWS Secrets Manager (Production)

For production, store Connect credentials in AWS Secrets Manager:

```python
# In config/environments.py
import boto3

def get_connect_credentials(environment):
    client = boto3.client('secretsmanager')
    secret = client.get_secret_value(SecretId=f'connect-{environment}')
    return json.loads(secret['SecretString'])
```

### 3. Restrict CORS Origins

In production, set specific domains:

```python
"prod": {
    "cors_allowed_origins": [
        "https://www.yoursite.com",
        "https://yoursite.com"
    ],
}
```

---

## Quick Start Checklist

- [ ] Amazon Connect instance created
- [ ] Chat widget created in Connect
- [ ] Contact flow created and published
- [ ] Widget credentials copied (URL, Widget ID, Snippet ID)
- [ ] `config/environments.py` updated with credentials
- [ ] CDK stack deployed
- [ ] Widget tested in browser
- [ ] Chat flow tested end-to-end
- [ ] Production CORS configured
- [ ] Credentials secured (not in git)

---

## Need Help?

### AWS Support
- Amazon Connect Documentation: https://docs.aws.amazon.com/connect/
- AWS Support Center

### Common Resources
- Amazon Connect Chat Widgets: https://docs.aws.amazon.com/connect/latest/adminguide/add-chat-to-website.html
- Contact Flows: https://docs.aws.amazon.com/connect/latest/adminguide/connect-contact-flows.html

---

**After configuring your Connect credentials and redeploying, your widget will work!** 🚀
