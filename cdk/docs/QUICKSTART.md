# 🚀 Quick Start Guide

Get the 211 Chat Widget deployed in under 10 minutes!

## Prerequisites Installation

### 1. Install Python (if not already installed)
- Download from: https://www.python.org/downloads/
- Minimum version: 3.11
- Verify: `python --version`

### 2. Install Node.js (if not already installed)
- Download from: https://nodejs.org/
- Minimum version: 18
- Verify: `node --version`

### 3. Install AWS CDK CLI
```bash
npm install -g aws-cdk
```
Verify: `cdk --version`

### 4. Install AWS CLI
- Windows: https://aws.amazon.com/cli/
- Mac: `brew install awscli`
- Linux: `apt-get install awscli` or `yum install awscli`

Verify: `aws --version`

### 5. Configure AWS Credentials
```bash
aws configure
```
Enter your:
- AWS Access Key ID
- AWS Secret Access Key
- Default region (e.g., `us-west-2`)
- Output format (e.g., `json`)

## Deployment (3 Steps)

### Step 1: Verify Setup

**Windows:**
```powershell
cd cdk
python verify-setup.py
```

**Linux/Mac:**
```bash
cd cdk
python3 verify-setup.py
```

✅ All checks should pass before proceeding.

### Step 2: Bootstrap CDK (First Time Only)

This creates required resources in your AWS account.

**Windows:**
```powershell
.\deploy.ps1 -Action bootstrap
```

**Linux/Mac:**
```bash
chmod +x deploy.sh  # Make script executable
./deploy.sh dev bootstrap
```

⏱️ Takes ~1-2 minutes

### Step 3: Deploy

**Windows:**
```powershell
.\deploy.ps1 -Environment dev -Action deploy
```

**Linux/Mac:**
```bash
./deploy.sh dev deploy
```

⏱️ Takes ~3-5 minutes

## 🎉 Success!

After deployment, you'll see output like:

```
✨  Deployment time: 234.56s

Outputs:
ChatWidget-Dev.DeploymentEnvironment = dev
ChatWidget-Dev.WidgetUrl = https://abcd1234.lambda-url.us-west-2.on.aws/
```

**Copy the Function URL** - this is your chat widget endpoint!

## Test Your Deployment

1. **Open the URL in a browser**: Paste the Function URL
2. **You should see**: The 211 Helpline website with chat widget
3. **Test the widget**: Click the chat icon (bottom-right)
4. **Test mode switching**: Use the buttons at top-right to switch between Standard/Kiosk/Mobile views

### Quick Tests

**Standard Mode:**
```
https://your-function-url.on.aws/
```

**Kiosk Mode:**
```
https://your-function-url.on.aws/?mode=kiosk
```

**Mobile Mode:**
```
https://your-function-url.on.aws/?mode=mobile
```

## Deploy to Other Environments

### Staging
```bash
# Windows
.\deploy.ps1 -Environment staging -Action deploy

# Linux/Mac
./deploy.sh staging deploy
```

### Production
```bash
# Windows
.\deploy.ps1 -Environment prod -Action deploy

# Linux/Mac
./deploy.sh prod deploy
```

**⚠️ Important:** Update Amazon Connect credentials in `config/environments.py` before deploying to production!

## Customize Configuration

Edit `config/environments.py` to customize:

```python
"widget_config": {
    "COMPANY_NAME": "Your Organization Name",
    "WIDGET_ID": "your-widget-id",
    "SNIPPET_ID": "your-snippet-id",
    "COLOR_NAVY": "#10264a",     # Your brand color
    "COLOR_GOLD": "#f5a623",     # Your accent color
    "WIDGET_HEADER": "Help Chat",
    # ... more options
}
```

Then redeploy:
```bash
./deploy.sh dev deploy
```

## View Logs

```bash
aws logs tail /aws/lambda/chat-widget-dev --follow
```

Press `Ctrl+C` to stop.

## Update Deployment

After making changes to Lambda code or configuration:

```bash
# View what will change
./deploy.sh dev diff

# Deploy changes
./deploy.sh dev deploy
```

## Troubleshooting

### "Command not found: cdk"
**Solution:** Install CDK CLI: `npm install -g aws-cdk`

### "Unable to resolve AWS account"
**Solution:** Configure AWS credentials: `aws configure`

### "Module 'aws_cdk' not found"
**Solution:**
```bash
cd cdk
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
```

### Widget not loading
**Solution:** Check CloudWatch logs:
```bash
aws logs tail /aws/lambda/chat-widget-dev --follow
```

### CORS errors in browser
**Solution:** Add your domain to `cors_allowed_origins` in `config/environments.py`

## Destroy Resources (⚠️ Careful!)

To delete all deployed resources:

```bash
# Windows
.\deploy.ps1 -Environment dev -Action destroy

# Linux/Mac
./deploy.sh dev destroy
```

Type `yes` to confirm.

## Next Steps

1. ✅ **Customize branding** in `config/environments.py`
2. ✅ **Set up staging** environment: `./deploy.sh staging deploy`
3. ✅ **Configure production** Amazon Connect credentials
4. ✅ **Deploy to production**: `./deploy.sh prod deploy`
5. ✅ **Set up monitoring** in CloudWatch
6. ✅ **Review security** settings (CORS, IAM)

## Need Help?

- 📖 Full documentation: [README.md](README.md)
- ✅ Deployment checklist: [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)
- 🔧 Verify setup: `python verify-setup.py`

## Common Commands Cheat Sheet

```bash
# Verify prerequisites
python verify-setup.py

# Bootstrap (first time)
./deploy.sh dev bootstrap

# Deploy
./deploy.sh dev deploy

# View changes before deploying
./deploy.sh dev diff

# Generate CloudFormation template
./deploy.sh dev synth

# View logs
aws logs tail /aws/lambda/chat-widget-dev --follow

# Get Function URL
aws cloudformation describe-stacks \
  --stack-name ChatWidget-Dev \
  --query "Stacks[0].Outputs[?OutputKey=='WidgetUrl'].OutputValue" \
  --output text

# Destroy stack
./deploy.sh dev destroy
```

---

**Time to first deployment: ~10 minutes** ⚡

Happy deploying! 🚀
