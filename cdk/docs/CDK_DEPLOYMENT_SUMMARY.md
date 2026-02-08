# ✅ CDK Deployment Package - Complete

## 🎯 Overview

Your 211 Chat Widget is now ready for AWS deployment using AWS CDK (Infrastructure as Code). This package provides a production-ready, multi-environment deployment solution that can be easily used across different AWS accounts.

## 📦 What's Included

### Complete CDK Infrastructure
✅ **Nested Stack Architecture** - Modular, reusable infrastructure
✅ **Multi-Environment Support** - Dev, Staging, Production configs
✅ **Lambda Function** with Function URL (no API Gateway needed)
✅ **CloudWatch Logging** with configurable retention
✅ **CORS Configuration** per environment
✅ **IAM Roles** with least privilege
✅ **Automated Deployment Scripts** for Windows & Unix/Linux/Mac

## 📂 Project Structure

```
CHAT_WIDGET/
├── cdk/                                    # ← AWS CDK Infrastructure
│   ├── app.py                             # CDK app entry point
│   ├── cdk.json                           # CDK configuration
│   ├── requirements.txt                   # Python dependencies
│   │
│   ├── 📜 Documentation
│   ├── README.md                          # Complete deployment guide
│   ├── QUICKSTART.md                      # 10-minute quick start
│   ├── ARCHITECTURE.md                    # Architecture deep-dive
│   ├── DEPLOYMENT_CHECKLIST.md            # Pre/post deployment checklist
│   │
│   ├── 🚀 Deployment Scripts
│   ├── deploy.sh                          # Unix/Linux/Mac deployment
│   ├── deploy.ps1                         # Windows PowerShell deployment
│   ├── verify-setup.py                    # Prerequisites checker
│   │
│   ├── config/                            # Environment configurations
│   │   ├── __init__.py
│   │   └── environments.py                # Multi-environment settings
│   │
│   ├── stacks/                            # CDK stack definitions
│   │   ├── __init__.py
│   │   ├── main_stack.py                 # Main orchestration stack
│   │   └── chat_widget_stack.py          # Nested Lambda stack
│   │
│   └── lambda/                            # Lambda function code
│       ├── lambda_function.py             # Entry point
│       ├── config.py                      # Configuration
│       ├── view_config.py                 # Amazon Connect View
│       ├── widget.py                      # Widget rendering
│       ├── styles.py                      # CSS generation
│       ├── page.py                        # HTML templates
│       └── widget_snippet.js              # Amazon Connect snippet
│
├── Original Files (for reference)
├── lambda_function.py
├── config.py
├── view_config.py
├── widget.py
├── styles.py
├── page.py
├── widget_snippet.js
└── deployment.zip
```

## 🚀 Quick Deployment

### Prerequisites Check
```bash
cd cdk
python verify-setup.py
```

### Deploy to Development
```bash
# Windows
.\deploy.ps1 -Environment dev -Action deploy

# Linux/Mac
./deploy.sh dev deploy
```

### Deploy to Other Environments
```bash
# Staging
./deploy.sh staging deploy

# Production
./deploy.sh prod deploy
```

## 🌍 Multi-Environment Features

### Three Pre-Configured Environments

| Feature              | Dev          | Staging      | Production   |
|---------------------|--------------|--------------|--------------|
| Stack Name          | ChatWidget-Dev | ChatWidget-Staging | ChatWidget-Prod |
| Lambda Memory       | 512 MB       | 1024 MB      | 1024 MB      |
| Log Retention       | 7 days       | 14 days      | 30 days      |
| Reserved Concurrency| Unlimited    | 10           | 50           |
| CORS Origins        | * (all)      | Staging URL  | Production URLs only |

### Easy Customization

Edit **`cdk/config/environments.py`** to:
- Add new environments (QA, UAT, etc.)
- Change AWS regions
- Update Lambda settings
- Configure Amazon Connect credentials
- Customize branding and colors
- Set CORS policies

### Multi-Account Deployment

Deploy to different AWS accounts using profiles:

```bash
# Bootstrap dev account
AWS_PROFILE=dev-account ./deploy.sh dev bootstrap

# Deploy to dev account
AWS_PROFILE=dev-account ./deploy.sh dev deploy

# Bootstrap prod account
AWS_PROFILE=prod-account ./deploy.sh prod bootstrap

# Deploy to prod account
AWS_PROFILE=prod-account ./deploy.sh prod deploy
```

## 🏗️ Architecture Highlights

### Nested Stack Design
```
Main Stack (ChatWidget-Dev/Staging/Prod)
└── Nested Stack (ChatWidgetNestedStack)
    ├── Lambda Function
    ├── Function URL (HTTPS endpoint)
    ├── CloudWatch Logs
    └── IAM Execution Role
```

**Benefits:**
- ✅ Reusable across environments
- ✅ Independent lifecycle management
- ✅ Cleaner resource organization
- ✅ Easier to maintain and update

### Serverless & Cost-Effective
- **No servers to manage** - Lambda scales automatically
- **Pay per use** - Only charged for actual requests
- **Highly available** - Multi-AZ by default
- **Low cost** - ~$0.62/month for 10K requests

## 📚 Documentation

| Document | Purpose | Use When |
|----------|---------|----------|
| **[README.md](cdk/README.md)** | Complete deployment guide | First time setup, detailed reference |
| **[QUICKSTART.md](cdk/QUICKSTART.md)** | 10-minute quick start | Need to deploy fast |
| **[ARCHITECTURE.md](cdk/ARCHITECTURE.md)** | Architecture deep-dive | Understanding infrastructure |
| **[DEPLOYMENT_CHECKLIST.md](cdk/DEPLOYMENT_CHECKLIST.md)** | Pre/post deployment checklist | Production deployments |

## 🔧 Key Commands

```bash
# Verify prerequisites
python verify-setup.py

# Bootstrap CDK (first time only per account)
./deploy.sh dev bootstrap

# Preview changes
./deploy.sh dev diff

# Deploy
./deploy.sh dev deploy

# View CloudFormation template
./deploy.sh dev synth

# View logs
aws logs tail /aws/lambda/chat-widget-dev --follow

# Get Function URL
aws cloudformation describe-stacks \
  --stack-name ChatWidget-Dev \
  --query "Stacks[0].Outputs[?OutputKey=='WidgetUrl'].OutputValue" \
  --output text

# Destroy (careful!)
./deploy.sh dev destroy
```

## ✨ Key Features

### 🎨 View Modes
- **Standard** - Full website with floating chat widget
- **Kiosk** - Full-screen centered widget, auto-open/reset
- **Mobile** - Phone-optimized, full-width widget

### 🔄 Dynamic Mode Resolution
1. URL query string: `?mode=kiosk`
2. Environment variable: `VIEW_MODE`
3. Auto-detect mobile devices
4. Default: standard

### 🎯 Environment-Specific Configuration
- Lambda memory and timeout
- Log retention periods
- CORS policies
- Amazon Connect credentials
- Branding and colors
- Reserved concurrency

### 📊 Built-in Monitoring
- CloudWatch Logs with structured JSON
- Lambda metrics (invocations, duration, errors)
- Configurable log retention
- Ready for CloudWatch Alarms

## 🔐 Security Features

- ✅ IAM roles with least privilege
- ✅ HTTPS-only Function URLs
- ✅ Environment-specific CORS policies
- ✅ No hardcoded credentials
- ✅ CloudWatch logging for auditing
- ✅ VPC-ready (optional)

## 💰 Cost Estimate

### Development Environment
- **10,000 requests/month**: ~$0.62/month
- **Lambda + CloudWatch Logs**

### Production Environment
- **100,000 requests/month**: ~$6-8/month
- **Includes 30-day log retention**

**Note**: Actual costs depend on usage patterns.

## 🎓 What You Can Do Now

### 1️⃣ Deploy to Development (5 minutes)
```bash
cd cdk
python verify-setup.py
./deploy.sh dev deploy
```

### 2️⃣ Customize Configuration
Edit `cdk/config/environments.py`:
- Company name
- Amazon Connect credentials
- Brand colors
- Widget text

### 3️⃣ Deploy to Staging
```bash
./deploy.sh staging deploy
```

### 4️⃣ Test Thoroughly
- Standard mode: `https://your-url/`
- Kiosk mode: `https://your-url/?mode=kiosk`
- Mobile mode: `https://your-url/?mode=mobile`

### 5️⃣ Deploy to Production
```bash
# Review configuration
cat cdk/config/environments.py

# Use deployment checklist
cat cdk/DEPLOYMENT_CHECKLIST.md

# Deploy
./deploy.sh prod deploy
```

## 🆘 Need Help?

### Quick Troubleshooting
1. **"Command not found: cdk"**
   - Install: `npm install -g aws-cdk`

2. **"Unable to resolve AWS account"**
   - Configure: `aws configure`

3. **"Module 'aws_cdk' not found"**
   ```bash
   cd cdk
   python -m venv venv
   source venv/bin/activate  # or .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

### Resources
- 📖 [Full README](cdk/README.md) - Complete documentation
- 🚀 [Quick Start](cdk/QUICKSTART.md) - 10-minute deployment
- 🏗️ [Architecture](cdk/ARCHITECTURE.md) - Deep dive
- ✅ [Checklist](cdk/DEPLOYMENT_CHECKLIST.md) - Deployment guide

## ✅ What's Different from Original?

### Before (Original deployment.zip)
- ❌ Manual Lambda creation via AWS Console
- ❌ Manual IAM role setup
- ❌ Manual Function URL configuration
- ❌ Hard to replicate across environments
- ❌ Configuration in multiple places
- ❌ No version control for infrastructure

### After (CDK Deployment)
- ✅ **Infrastructure as Code** - Everything defined in Python
- ✅ **One-Command Deployment** - `./deploy.sh dev deploy`
- ✅ **Multi-Environment** - Dev, Staging, Prod configs
- ✅ **Version Controlled** - Git-friendly infrastructure
- ✅ **Repeatable** - Deploy to any AWS account
- ✅ **Documented** - Comprehensive guides
- ✅ **Automated** - Scripts for Windows & Unix
- ✅ **Production-Ready** - Best practices built-in

## 🎉 Summary

You now have a **production-ready AWS CDK deployment package** that:

1. ✅ Deploys the entire 211 Chat Widget infrastructure with one command
2. ✅ Supports multiple environments (dev, staging, production)
3. ✅ Works across different AWS accounts
4. ✅ Includes comprehensive documentation
5. ✅ Has automated deployment scripts for Windows & Unix/Linux/Mac
6. ✅ Uses nested stacks for modularity and reusability
7. ✅ Follows AWS best practices
8. ✅ Is fully customizable via configuration files

**Time to first deployment**: ~10 minutes ⚡

**Next step**: `cd cdk && python verify-setup.py`

---

**Package Version**: 1.0
**Created**: 2025-02-07
**Status**: ✅ Ready for Deployment
**License**: Proprietary - Trident United Way
