# 211 Chat Widget - AWS CDK Deployment

This directory contains AWS CDK infrastructure code for deploying the 211 Chat Widget across multiple AWS accounts and environments.

## 🏗️ Architecture

```
Main Stack (ChatWidget-{Environment})
└── Nested Stack (ChatWidgetNestedStack)
    ├── Lambda Function (chat-widget-{environment})
    ├── Lambda Function URL (Public HTTPS endpoint)
    ├── CloudWatch Logs (Configurable retention)
    └── IAM Role (Lambda execution permissions)
```

### Why Nested Stacks?

- **Reusability**: Deploy the same Lambda infrastructure across multiple environments
- **Modularity**: Separate concerns between main orchestration and Lambda resources
- **Resource Limits**: Stay within CloudFormation resource limits for complex stacks
- **Team Collaboration**: Different teams can own different nested stacks

## 📋 Prerequisites

### Required Software

1. **Python 3.11+**
   ```bash
   python --version  # Should be 3.11 or higher
   ```

2. **Node.js 18+ and npm** (for AWS CDK CLI)
   - Download from: https://nodejs.org/
   ```bash
   node --version  # Should be 18 or higher
   npm --version
   ```

3. **AWS CDK CLI**
   ```bash
   npm install -g aws-cdk
   cdk --version  # Should be 2.170.0 or higher
   ```

4. **AWS CLI** (configured with credentials)
   ```bash
   aws --version
   aws configure  # Set up your credentials
   ```

### AWS Credentials

Configure your AWS credentials using one of these methods:

**Option 1: AWS CLI Configuration**
```bash
aws configure
# Enter: Access Key ID, Secret Access Key, Region, Output format
```

**Option 2: Environment Variables**
```bash
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="us-west-2"
```

**Option 3: AWS Profile**
```bash
aws configure --profile myprofile
export AWS_PROFILE=myprofile
```

### Required IAM Permissions

Your AWS user/role needs these permissions:
- `cloudformation:*` - Create/update/delete stacks
- `lambda:*` - Create/manage Lambda functions
- `iam:*` - Create Lambda execution roles
- `logs:*` - Create CloudWatch log groups
- `s3:*` - Upload CDK assets to bootstrap bucket

## 🚀 Quick Start

### 1. Install Dependencies

**On Windows:**
```powershell
cd cdk
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**On Linux/Mac:**
```bash
cd cdk
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Bootstrap CDK (First Time Only)

This creates an S3 bucket and other resources needed by CDK in your AWS account.

**Windows:**
```powershell
.\deploy.ps1 -Action bootstrap
```

**Linux/Mac:**
```bash
chmod +x deploy.sh
./deploy.sh dev bootstrap
```

### 3. Deploy to an Environment

**Windows:**
```powershell
# Deploy to dev
.\deploy.ps1 -Environment dev -Action deploy

# Deploy to staging
.\deploy.ps1 -Environment staging -Action deploy

# Deploy to production
.\deploy.ps1 -Environment prod -Action deploy
```

**Linux/Mac:**
```bash
# Deploy to dev
./deploy.sh dev deploy

# Deploy to staging
./deploy.sh staging deploy

# Deploy to production
./deploy.sh prod deploy
```

The script will output the Lambda Function URL at the end.

## 📁 Project Structure

```
cdk/
├── app.py                      # CDK app entry point
├── cdk.json                    # CDK configuration
├── requirements.txt            # Python dependencies
├── deploy.sh                   # Unix/Linux deployment script
├── deploy.ps1                  # Windows PowerShell deployment script
├── README.md                   # This file
│
├── config/                     # Environment configurations
│   ├── __init__.py
│   └── environments.py         # Multi-environment settings
│
├── stacks/                     # CDK stack definitions
│   ├── __init__.py
│   ├── main_stack.py          # Main orchestration stack
│   └── chat_widget_stack.py   # Nested Lambda stack
│
└── lambda/                     # Lambda function code
    ├── lambda_function.py      # Lambda handler
    ├── config.py               # Configuration
    ├── view_config.py          # Amazon Connect view
    ├── widget.py               # Widget rendering
    ├── styles.py               # CSS styles
    ├── page.py                 # HTML page generation
    └── widget_snippet.js       # Amazon Connect snippet
```

## 🌍 Environments

Three pre-configured environments are available:

| Environment | Stack Suffix | Memory | Timeout | Log Retention | Concurrency |
|-------------|--------------|--------|---------|---------------|-------------|
| **dev**     | Dev          | 512 MB | 30s     | 7 days        | None        |
| **staging** | Staging      | 1024 MB| 30s     | 14 days       | 10          |
| **prod**    | Prod         | 1024 MB| 30s     | 30 days       | 50          |

### Customizing Environments

Edit [config/environments.py](config/environments.py) to:
- Add new environments (e.g., `qa`, `uat`)
- Change Lambda configuration (memory, timeout, etc.)
- Update widget settings (company name, colors, Connect credentials)
- Configure CORS origins

Example:
```python
"prod": {
    "stack_name_suffix": "Prod",
    "aws_region": "us-east-1",  # Change region
    "lambda_config": {
        "memory_size": 2048,     # Increase memory
        "timeout": 60,           # Increase timeout
        "log_retention_days": 90,
    },
    "widget_config": {
        "COMPANY_NAME": "Your Organization",
        "WIDGET_ID": "your-widget-id",
        # ... other settings
    },
}
```

## 🛠️ CDK Commands

### Synthesize CloudFormation Template

Preview the CloudFormation template without deploying:

```bash
# Windows
.\deploy.ps1 -Environment dev -Action synth

# Linux/Mac
./deploy.sh dev synth
```

### View Differences

Compare your current configuration with what's deployed:

```bash
# Windows
.\deploy.ps1 -Environment dev -Action diff

# Linux/Mac
./deploy.sh dev diff
```

### Deploy Stack

```bash
# Windows
.\deploy.ps1 -Environment dev -Action deploy

# Linux/Mac
./deploy.sh dev deploy
```

### Destroy Stack

**⚠️ WARNING: This will delete all resources!**

```bash
# Windows
.\deploy.ps1 -Environment dev -Action destroy

# Linux/Mac
./deploy.sh dev destroy
```

## 🔄 Multi-Account Deployment

To deploy to different AWS accounts:

### 1. Create AWS Profiles

Edit `~/.aws/config`:
```ini
[profile dev-account]
region = us-west-2
output = json

[profile prod-account]
region = us-west-2
output = json
```

Edit `~/.aws/credentials`:
```ini
[dev-account]
aws_access_key_id = YOUR_DEV_KEY
aws_secret_access_key = YOUR_DEV_SECRET

[prod-account]
aws_access_key_id = YOUR_PROD_KEY
aws_secret_access_key = YOUR_PROD_SECRET
```

### 2. Deploy with Profile

```bash
# Deploy to dev account
AWS_PROFILE=dev-account ./deploy.sh dev deploy

# Deploy to prod account
AWS_PROFILE=prod-account ./deploy.sh prod deploy
```

### 3. Bootstrap Each Account

```bash
# Bootstrap dev account
AWS_PROFILE=dev-account ./deploy.sh dev bootstrap

# Bootstrap prod account
AWS_PROFILE=prod-account ./deploy.sh prod bootstrap
```

## 📊 Monitoring & Logs

### CloudWatch Logs

View Lambda logs:
```bash
aws logs tail /aws/lambda/chat-widget-dev --follow
```

### CloudWatch Insights Queries

Example query to analyze widget usage:
```
fields @timestamp, view_mode, mode_source, source_ip
| filter event = "page_render"
| stats count() by view_mode
```

### Function URL Metrics

Monitor in AWS Console:
- Lambda → Functions → chat-widget-{env} → Monitor tab
- Metrics: Invocations, Duration, Errors, Throttles

## 🔧 Troubleshooting

### CDK Bootstrap Failed

**Error**: `Unable to resolve AWS account to use`

**Solution**: Ensure AWS credentials are configured:
```bash
aws sts get-caller-identity  # Should return your account info
```

### Import Error: aws_cdk

**Error**: `ModuleNotFoundError: No module named 'aws_cdk'`

**Solution**: Activate virtual environment and install dependencies:
```bash
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
```

### Lambda Deployment Failed

**Error**: `Resource handler returned message: "The role defined for the function cannot be assumed by Lambda"`

**Solution**: Wait 10-15 seconds and deploy again. IAM role creation can take time to propagate.

### Function URL CORS Issues

If CORS errors occur, check [config/environments.py](config/environments.py):
```python
"cors_allowed_origins": ["https://yourdomain.com"],
```

Change to `["*"]` for testing (not recommended for production).

## 🔐 Security Best Practices

1. **Restrict CORS Origins**: Don't use `["*"]` in production
2. **Use Least Privilege IAM**: Lambda only has necessary permissions
3. **Enable VPC**: For sensitive deployments, deploy Lambda in VPC
4. **Secrets Management**: Use AWS Secrets Manager for Connect credentials
5. **Enable CloudTrail**: Track all API calls for compliance

## 📦 CI/CD Integration

### GitHub Actions Example

```yaml
name: Deploy CDK
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install CDK
        run: npm install -g aws-cdk
      - name: Deploy
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        run: |
          cd cdk
          pip install -r requirements.txt
          cdk deploy -c environment=prod --require-approval never
```

## 📚 Additional Resources

- [AWS CDK Documentation](https://docs.aws.amazon.com/cdk/)
- [AWS Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [Amazon Connect Chat Widget](https://docs.aws.amazon.com/connect/latest/adminguide/add-chat-to-website.html)

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review CloudWatch logs for errors
3. Contact your AWS administrator
4. Open an issue in the project repository

## 📝 License

Copyright © 2025 Trident United Way. All rights reserved.
