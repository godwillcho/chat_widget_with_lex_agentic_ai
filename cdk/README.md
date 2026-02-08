# 211 Chat Widget - AWS CDK Deployment

Production-ready AWS infrastructure with organized resource structure and nested stack architecture.

## 🚀 Quick Start

```bash
cd cdk
python verify-setup.py
./deploy.sh dev deploy
```

⚠️ **Widget showing an error?** See: **[docs/QUICK_FIX_GUIDE.md](docs/QUICK_FIX_GUIDE.md)**

---

## 📁 Organized Project Structure

```
cdk/
├── app.py                          # CDK app entry point
├── cdk.json                        # CDK configuration
├── requirements.txt                # Python dependencies
│
├── config/                         # 📋 Configuration
│   └── environments.py             # Dev, Staging, Prod configs
│
├── stacks/                         # 🏗️ CDK Stack Definitions
│   ├── main_stack.py              # Main orchestration
│   └── web_app_stack.py           # Web app nested stack
│
├── lambda_functions/               # ⚡ All Lambda Functions
│   └── chat_widget/               # Chat widget Lambda
│       ├── lambda_function.py     # Handler
│       ├── config.py              # Config logic
│       ├── widget.py              # Widget rendering
│       ├── styles.py              # CSS generation
│       ├── page.py                # HTML templates
│       └── widget_snippet.js      # Connect snippet
│
├── resources/                      # 📦 Other AWS Resources
│   └── future_resources/          # For Lambda layers, etc.
│
└── docs/                          # 📚 Documentation
    ├── INDEX.md                   # Documentation index
    ├── QUICKSTART.md              # 10-min quick start
    ├── ARCHITECTURE.md            # Architecture details
    └── CONNECT_CONFIGURATION.md   # Connect setup guide
```

**See**: [docs/RESOURCE_ORGANIZATION.md](docs/RESOURCE_ORGANIZATION.md) for detailed structure guidelines

---

## 🎯 Documentation

| Document | Purpose |
|----------|---------|
| **[docs/QUICK_FIX_GUIDE.md](docs/QUICK_FIX_GUIDE.md)** | ⚡ Fix widget error (5 min) |
| **[docs/RESOURCE_ORGANIZATION.md](docs/RESOURCE_ORGANIZATION.md)** | 📁 Project structure guide |
| **[docs/INDEX.md](docs/INDEX.md)** | 📚 All documentation |
| **[docs/QUICKSTART.md](docs/QUICKSTART.md)** | 🚀 Quick deployment guide |
| **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** | 🏗️ Architecture deep-dive |
| **[docs/CONNECT_CONFIGURATION.md](docs/CONNECT_CONFIGURATION.md)** | 🔧 Connect setup guide |

---

## 🏗️ Architecture

**Nested Stack Design:**
```
Main Stack (Project-{Environment})
├── Web App Stack (Chat Widget Lambda)
├── [Future] Database Stack
├── [Future] API Stack
└── [Future] Monitoring Stack
```

All resources are **organized by type**:
- Lambda functions → `lambda_functions/`
- Stacks → `stacks/`
- Resources → `resources/`
- Config → `config/`

---

## 🌍 Multi-Environment & Multi-Organization

Deploy to multiple environments and organizations by editing `config/environments.py`:

```python
ENVIRONMENTS = {
    "dev": { ... },
    "staging": { ... },
    "prod": { ... },
    "org2-prod": { ... },  # ← Add more organizations
}
```

Deploy to each:
```bash
./deploy.sh dev deploy      # Development
./deploy.sh staging deploy  # Staging
./deploy.sh prod deploy     # Production
./deploy.sh org2-prod deploy  # Organization 2
```

---

## 🔧 Common Commands

```bash
# Deploy to dev
./deploy.sh dev deploy

# View changes before deploying
./deploy.sh dev diff

# Preview CloudFormation template
./deploy.sh dev synth

# View logs
aws logs tail /aws/lambda/chat-widget-dev --follow

# Destroy (careful!)
./deploy.sh dev destroy
```

---

## ⚠️ Widget Showing an Error?

**Quick Fix**: Update Amazon Connect credentials in `config/environments.py` and redeploy.

**See**: [docs/QUICK_FIX_GUIDE.md](docs/QUICK_FIX_GUIDE.md) for step-by-step instructions.

---

## 📦 What Gets Deployed

- **Main Stack**: `Project-{Environment}`
- **Nested Stack**: `WebAppStack`
  - Lambda Function: `chat-widget-{environment}`
  - Function URL: Public HTTPS endpoint
  - CloudWatch Logs: Automatic logging
  - IAM Role: Secure permissions

**Current deployment:**
- Stack: `Project-Dev`
- Lambda: `chat-widget-dev`
- URL: https://wxd2gcfo7vjv63ni2nwuvce3ma0zcpxc.lambda-url.us-east-1.on.aws/

---

## ➕ Adding New Resources

### Adding a Lambda Function

```bash
# Create directory
mkdir -p lambda_functions/my_function

# Create handler
touch lambda_functions/my_function/lambda_function.py

# Create/update stack
touch stacks/my_function_stack.py

# Deploy
./deploy.sh dev deploy
```

### Adding Other Resources

See **[docs/RESOURCE_ORGANIZATION.md](docs/RESOURCE_ORGANIZATION.md)** for:
- Lambda Layers
- Step Functions
- EventBridge Rules
- Other AWS resources

---

## 💡 Key Features

✅ **Organized Structure** - Resources organized by type
✅ **Nested Stacks** - Modular, scalable architecture
✅ **Multi-Environment** - Dev, Staging, Production
✅ **Multi-Organization** - Deploy to multiple orgs easily
✅ **Infrastructure as Code** - Everything versioned in Git
✅ **Production-Ready** - Best practices built-in

---

**Time to first deployment**: ~10 minutes ⚡

**Start here**: [docs/QUICK_FIX_GUIDE.md](docs/QUICK_FIX_GUIDE.md) or [docs/QUICKSTART.md](docs/QUICKSTART.md)
