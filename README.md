# Stability360 Chat Widget

An AWS Lambda-based chat widget powered by **Amazon Connect** and **Amazon Lex V2** conversational AI. Deployed via CloudFormation with a simple Python deploy script.

## Architecture

```
CloudFormation Stack (ChatWidget-{Environment})
├── Lambda Function (chat-widget-{env}) — serves HTML with embedded Connect widget
├── Lambda Function URL — public HTTPS endpoint
├── IAM Role + Policy
└── CloudWatch Log Group
```

## Features

- **2 View Modes** — Standard (floating widget), Kiosk (full-screen centered)
- **Dynamic Mode Resolution** — URL params (`?mode=kiosk`) or environment variable
- **Configurable Branding** — colors, text, bot name, all from one config file
- **Amazon Connect Widget** — latest snippet API with customStyles and customDisplayNames
- **Amazon Lex V2 Integration** — conversational AI with interactive cards

## Prerequisites

- **Python 3.11+**
- **AWS CLI** configured with valid credentials
- **Amazon Connect** instance with a communications widget configured

## Quick Start

### 1. Clone and set up

```bash
git clone https://github.com/godwillcho/chat_widget_with_lex_agentic_ai.git
cd chat_widget_with_lex_agentic_ai
pip install -r requirements.txt
```

### 2. Configure your environment

Edit `config/environments.py` and update the Amazon Connect credentials:

| Field | Description | Where to find it |
|-------|-------------|------------------|
| `CONNECT_URL` | Connect instance URL | AWS Console > Amazon Connect > Instance |
| `WIDGET_ID` | Widget identifier (UUID) | Connect snippet: 4th arg in IIFE |
| `SNIPPET_ID` | Encrypted snippet token | Connect snippet: `amazon_connect('snippetId', '...')` |
| `CONNECT_INSTANCE_ID` | Connect instance ID | AWS Console > Amazon Connect |
| `CONTACT_FLOW_ID` | Contact flow for chat | Connect Console > Flows |

### 3. Deploy

```bash
python deploy.py
```

The deployment outputs a public **Lambda Function URL** — that's your chat widget endpoint.

## Project Structure

```
├── deploy.py                           # Deployment script (boto3)
├── template.yaml                       # CloudFormation template
├── requirements.txt                    # Python dependencies
│
├── config/
│   └── environments.py                 # All configuration (credentials, colors, text)
│
└── lambda_functions/
    └── chat_widget/
        ├── lambda_function.py          # Request handler with mode resolution
        ├── config.py                   # Environment variable loading
        ├── widget.py                   # Amazon Connect snippet generation
        ├── widget_enhancements.py      # Custom styles, kiosk landing page
        ├── styles.py                   # CSS generation
        └── page.py                     # HTML template generation
```

## Configuration

All configuration lives in `config/environments.py`. Edit values and run `python deploy.py`.

### Key settings

| Setting | Description |
|---------|-------------|
| `WIDGET_BOT_NAME` | Display name above bot messages (max 26 chars) |
| `WIDGET_HEADER` | Widget header text |
| `SERVICE_NAME` | Service name on the page |
| `COLOR_NAVY` | Primary theme color |
| `COLOR_GOLD` | Accent color |
| `VIEW_MODE` | Default mode: `standard` or `kiosk` |

## View Modes

| Mode | Layout | Use Case |
|------|--------|----------|
| **standard** | Floating widget, bottom-right (420x640px) | Website embedding |
| **kiosk** | Full-screen centered (780x920px), auto-open | Public kiosks, lobbies |

Override at runtime via URL: `https://your-function-url/?mode=kiosk`

## Tech Stack

- **AWS CloudFormation** — Infrastructure as Code
- **AWS Lambda** (Python 3.11) — Serverless compute
- **Lambda Function URLs** — Public HTTPS endpoints
- **Amazon Connect** — Contact center and chat widget
- **Amazon Lex V2** — Conversational AI

## License

Private
