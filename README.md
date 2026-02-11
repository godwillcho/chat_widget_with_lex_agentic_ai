# 211 Chat Widget with Lex Agentic AI

An AWS CDK-based infrastructure project that deploys an **Amazon Connect** chat widget integrated with **Amazon Lex V2** conversational AI. Built for **Trident United Way's 211 Helpline**, providing a production-ready, serverless chat interface with multi-environment support.

## Architecture

```
Project-{Environment} (Main Stack)
├── WebAppStack
│   ├── Lambda Function (chat-widget-{env}) — serves HTML with embedded Connect widget
│   └── Lambda Function URL — public HTTPS endpoint
│
├── LexBotStack
│   ├── Lex V2 Bot (YesNoBot-{env}) — consent question handling
│   ├── Fulfillment Lambda — Yes/No card generation and response routing
│   ├── Bot Builder Lambda — custom resource for automated bot creation
│   └── Post-Deploy Lambda — bot association and final setup
│
└── [Future] Database, API, Monitoring, Storage stacks
```

## Features

- **3 View Modes** — Standard (floating widget), Kiosk (full-screen), Mobile (phone-optimized)
- **Dynamic Mode Resolution** — URL params (`?mode=kiosk`), environment variables, User-Agent auto-detection
- **Multi-Environment Deployment** — dev, staging, prod with distinct configs
- **Multi-Organization Support** — add new orgs with custom branding and Connect credentials
- **Amazon Lex V2 Integration** — conversational AI with interactive Yes/No cards
- **Theme Customization** — configurable colors, fonts, and branding per environment
- **Infrastructure as Code** — fully reproducible deployments via AWS CDK

## Prerequisites

- **Python 3.11+**
- **AWS CLI** configured with valid credentials
- **AWS CDK CLI** (`npm install -g aws-cdk`)
- **Amazon Connect** instance with a chat widget configured

## Quick Start

### 1. Clone and set up

```bash
git clone https://github.com/godwillcho/chat_widget_with_lex_agentic_ai.git
cd chat_widget_with_lex_agentic_ai/cdk
python -m venv venv
```

Activate the virtual environment:

```powershell
# Windows
.\venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 2. Configure your environment

Edit `cdk/config/environments.py` and update the Amazon Connect credentials for your target environment:

| Field | Description | Where to find it |
|-------|-------------|------------------|
| `CONNECT_URL` | Connect instance URL | AWS Console > Amazon Connect > Instance |
| `CONNECT_INSTANCE_ID` | Connect instance ID | AWS Console > Amazon Connect > Instance |
| `CONTACT_FLOW_ID` | Contact flow for chat routing | Connect Console > Flows |
| `WIDGET_ID` | Widget identifier (UUID) | Connect Console > Channels > Chat widgets |
| `SECURITY_KEY` | JWT authentication key | Connect Console > Chat widgets > Show security key |

### 3. Bootstrap CDK (first time only)

```powershell
# Windows
.\deploy.ps1 -Environment dev -Action bootstrap

# Linux/Mac
./deploy.sh dev bootstrap
```

### 4. Deploy

```powershell
# Windows
.\deploy.ps1 -Environment dev -Action deploy

# Linux/Mac
./deploy.sh dev deploy
```

The deployment outputs a public **Lambda Function URL** — that's your chat widget endpoint.

## Deployment Commands

| Action | PowerShell (Windows) | Bash (Linux/Mac) |
|--------|----------------------|-------------------|
| **Deploy** | `.\deploy.ps1 -Environment dev -Action deploy` | `./deploy.sh dev deploy` |
| **Preview changes** | `.\deploy.ps1 -Environment dev -Action diff` | `./deploy.sh dev diff` |
| **Generate template** | `.\deploy.ps1 -Environment dev -Action synth` | `./deploy.sh dev synth` |
| **Destroy** | `.\deploy.ps1 -Environment dev -Action destroy` | `./deploy.sh dev destroy` |

Replace `dev` with `staging` or `prod` as needed.

## Project Structure

```
cdk/
├── app.py                          # CDK entry point
├── cdk.json                        # CDK runtime configuration
├── deploy.sh / deploy.ps1          # Deployment scripts
├── requirements.txt                # Python dependencies
│
├── config/
│   └── environments.py             # Multi-environment configs and credentials
│
├── stacks/
│   ├── main_stack.py               # Main orchestration stack
│   ├── web_app_stack.py            # Lambda + Function URL stack
│   └── lex_bot_stack.py            # Lex bot stack
│
├── lambda_functions/
│   ├── chat_widget/                # Main widget Lambda
│   │   ├── lambda_function.py      # Request handler with mode resolution
│   │   ├── config.py               # Environment config loading
│   │   ├── widget.py               # Amazon Connect snippet orchestration
│   │   ├── widget_enhancements.py  # Custom interactivity and styling
│   │   ├── styles.py               # CSS generation
│   │   ├── page.py                 # HTML template generation
│   │   ├── view_configs.py         # View-specific configs (standard/kiosk/mobile)
│   │   └── widget_scripts/         # Connect snippets per environment
│   ├── lex_bot_builder/            # Custom resource for bot creation
│   ├── lex_fulfillment/            # Lex code hook (Yes/No cards)
│   └── lex_post_deploy/            # Post-deployment tasks
│
├── scripts/                        # Utility scripts
└── docs/                           # Documentation
```

## Environment Configuration

Three environments are pre-configured in `config/environments.py`:

| Environment | Region | Lambda Memory | Log Retention | Concurrency |
|-------------|--------|---------------|---------------|-------------|
| **dev** | us-west-2 | 512 MB | 7 days | Unreserved |
| **staging** | us-west-2 | 1024 MB | 14 days | 10 |
| **prod** | us-west-2 | 1024 MB | 30 days | 50 |

### Adding a new organization

Add a new entry in `config/environments.py`:

```python
"org2-prod": {
    "stack_name_suffix": "Org2-Prod",
    "aws_region": "us-east-1",
    "widget_config": {
        "CONNECT_URL": "https://org2-instance.my.connect.aws",
        "WIDGET_ID": "your-widget-id",
        # ... other config
    },
}
```

Then deploy: `.\deploy.ps1 -Environment org2-prod -Action deploy`

## View Modes

| Mode | Layout | Use Case |
|------|--------|----------|
| **standard** | Floating widget, bottom-right corner (420x640px) | Website embedding |
| **kiosk** | Full-screen, centered (780x920px), auto-open | Public kiosks, lobbies |
| **mobile** | Full-width, anchored below header, auto-open | Phone browsers |

Override at runtime via URL: `https://your-function-url/?mode=kiosk`

## Tech Stack

- **AWS CDK v2** (Python) — Infrastructure as Code
- **AWS Lambda** (Python 3.11) — Serverless compute
- **Lambda Function URLs** — Public HTTPS endpoints
- **Amazon Connect** — Contact center and chat routing
- **Amazon Lex V2** — Conversational AI
- **CloudWatch** — Logging and monitoring

## License

Private — Trident United Way
