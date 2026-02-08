# 🏗️ Architecture Documentation

## Overview

The 211 Chat Widget is deployed as a serverless application on AWS using Infrastructure as Code (IaC) with AWS CDK.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         AWS Cloud                                │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │           CloudFormation Stack (Main)                       │ │
│  │           Name: ChatWidget-{Environment}                    │ │
│  │                                                              │ │
│  │  ┌───────────────────────────────────────────────────────┐ │ │
│  │  │     Nested Stack: ChatWidgetNestedStack               │ │ │
│  │  │                                                         │ │ │
│  │  │  ┌──────────────────────────────────────────────────┐ │ │ │
│  │  │  │  Lambda Function                                  │ │ │ │
│  │  │  │  Name: chat-widget-{env}                         │ │ │ │
│  │  │  │  Runtime: Python 3.11                            │ │ │ │
│  │  │  │  Handler: lambda_function.lambda_handler         │ │ │ │
│  │  │  │  Memory: 512MB - 1024MB (env-specific)           │ │ │ │
│  │  │  │  Timeout: 30s                                     │ │ │ │
│  │  │  │                                                    │ │ │ │
│  │  │  │  Environment Variables:                           │ │ │ │
│  │  │  │  • VIEW_MODE                                      │ │ │ │
│  │  │  │  • COMPANY_NAME                                   │ │ │ │
│  │  │  │  • CONNECT_URL                                    │ │ │ │
│  │  │  │  • WIDGET_ID                                      │ │ │ │
│  │  │  │  • SNIPPET_ID                                     │ │ │ │
│  │  │  │  • Colors, text, etc.                             │ │ │ │
│  │  │  └──────────────────────────────────────────────────┘ │ │ │
│  │  │                         │                              │ │ │
│  │  │                         │ Logs                         │ │ │
│  │  │                         ▼                              │ │ │
│  │  │  ┌──────────────────────────────────────────────────┐ │ │ │
│  │  │  │  CloudWatch Logs                                  │ │ │ │
│  │  │  │  Group: /aws/lambda/chat-widget-{env}           │ │ │ │
│  │  │  │  Retention: 7-30 days (env-specific)            │ │ │ │
│  │  │  └──────────────────────────────────────────────────┘ │ │ │
│  │  │                                                         │ │ │
│  │  │  ┌──────────────────────────────────────────────────┐ │ │ │
│  │  │  │  Lambda Function URL                              │ │ │ │
│  │  │  │  https://{id}.lambda-url.{region}.on.aws/        │ │ │ │
│  │  │  │  Auth: NONE (Public)                             │ │ │ │
│  │  │  │  CORS: Enabled                                    │ │ │ │
│  │  │  └──────────────────────────────────────────────────┘ │ │ │
│  │  │                         │                              │ │ │
│  │  └─────────────────────────┼──────────────────────────────┘ │ │
│  │                            │                                │ │
│  └────────────────────────────┼────────────────────────────────┘ │
│                               │                                  │
└───────────────────────────────┼──────────────────────────────────┘
                                │
                                │ HTTPS
                                ▼
                    ┌────────────────────────┐
                    │   End Users/Browsers   │
                    │   • Desktop            │
                    │   • Mobile             │
                    │   • Kiosk Terminals    │
                    └────────────────────────┘
                                │
                                │ WebSocket
                                ▼
                    ┌────────────────────────┐
                    │   Amazon Connect       │
                    │   Chat Interface       │
                    └────────────────────────┘
```

## Components

### 1. Main Stack (`ChatWidgetMainStack`)
- **Purpose**: Orchestrates all infrastructure resources
- **Type**: CloudFormation Stack
- **Naming**: `ChatWidget-{Dev|Staging|Prod}`
- **Responsibilities**:
  - Creates nested stacks
  - Manages environment-specific configurations
  - Provides aggregated outputs

### 2. Nested Stack (`ChatWidgetStack`)
- **Purpose**: Encapsulates Lambda function and related resources
- **Type**: CloudFormation Nested Stack
- **Benefits**:
  - Reusable across environments
  - Independent lifecycle management
  - Cleaner resource organization
- **Resources**:
  - Lambda Function
  - Lambda Function URL
  - CloudWatch Log Group
  - IAM Execution Role

### 3. Lambda Function
- **Runtime**: Python 3.11
- **Handler**: `lambda_function.lambda_handler`
- **Trigger**: Function URL (HTTPS endpoint)
- **Code Structure**:
  ```
  lambda_function.py  → Entry point, mode resolution
  config.py           → Configuration management
  view_config.py      → Amazon Connect View JSON
  widget.py           → Widget rendering logic
  styles.py           → CSS generation
  page.py             → HTML page templates
  widget_snippet.js   → Amazon Connect snippet
  ```

### 4. Lambda Function URL
- **Type**: Public HTTPS endpoint
- **Authentication**: None (public access)
- **CORS**: Enabled with configurable origins
- **Format**: `https://{id}.lambda-url.{region}.on.aws/`
- **Features**:
  - No API Gateway needed (simpler, cheaper)
  - Built-in HTTPS
  - Low latency
  - Automatic scaling

### 5. CloudWatch Logs
- **Log Group**: `/aws/lambda/chat-widget-{environment}`
- **Retention**: Environment-specific (7-90 days)
- **Contains**:
  - Lambda execution logs
  - Request/response details
  - View mode resolution logs
  - Error traces

## Data Flow

### Request Flow
```
1. User opens URL in browser
   ↓
2. Browser sends GET request to Lambda Function URL
   ↓
3. API Gateway (built into Function URL) invokes Lambda
   ↓
4. Lambda handler executes:
   a. Resolves view mode (query string → env vars → auto-detect)
   b. Dynamically imports Python modules
   c. Generates HTML with widget
   d. Returns HTTP response
   ↓
5. Browser receives HTML page
   ↓
6. Browser loads Amazon Connect widget JavaScript
   ↓
7. Widget connects to Amazon Connect service
   ↓
8. User interacts with chat interface
```

### View Mode Resolution (Priority Order)
```
1. URL Query String: ?mode=standard|kiosk|mobile
   ↓ (if not present)
2. VIEW_MODE environment variable
   ↓ (if not set)
3. Legacy KIOSK_MODE environment variable
   ↓ (if not set)
4. User-Agent header detection
   ↓ (if not mobile)
5. Default: standard
```

## Multi-Environment Strategy

### Environment Isolation

Each environment is deployed as a separate CloudFormation stack:

| Environment | Stack Name         | Function Name       | Purpose                |
|-------------|-------------------|---------------------|------------------------|
| **dev**     | ChatWidget-Dev    | chat-widget-dev     | Development & testing  |
| **staging** | ChatWidget-Staging| chat-widget-staging | Pre-production testing |
| **prod**    | ChatWidget-Prod   | chat-widget-prod    | Production serving     |

### Configuration Management

Configurations are managed in `config/environments.py`:

```python
ENVIRONMENTS = {
    "dev": {
        "lambda_config": { ... },
        "widget_config": { ... },
        "cors_allowed_origins": ["*"],
    },
    "staging": { ... },
    "prod": { ... }
}
```

### Multi-Account Deployment

The CDK app supports deployment to different AWS accounts:

```bash
# Deploy to dev account
AWS_PROFILE=dev-account ./deploy.sh dev deploy

# Deploy to prod account
AWS_PROFILE=prod-account ./deploy.sh prod deploy
```

## Security Architecture

### IAM Permissions

**Lambda Execution Role** (Auto-created by CDK):
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
```

### Network Security

- **No VPC**: Lambda runs in AWS-managed VPC (default)
- **Public Access**: Function URL is publicly accessible
- **HTTPS Only**: All traffic encrypted in transit
- **CORS**: Configurable per environment

### Data Security

- **No Data Storage**: Lambda is stateless
- **No Secrets**: Connect credentials in environment variables (consider AWS Secrets Manager for production)
- **Logs**: May contain PII, review retention policies

## Scalability & Performance

### Concurrency

| Environment | Reserved Concurrency | Max Concurrent Users |
|-------------|---------------------|----------------------|
| dev         | None (unlimited*)   | ~1,000              |
| staging     | 10                  | ~100                |
| prod        | 50                  | ~500                |

*Subject to account limits

### Cold Start Optimization

- **Runtime**: Python 3.11 (faster cold starts than 3.9)
- **Memory**: 512MB-1024MB (more memory = faster CPU)
- **Code Size**: ~70KB (minimal dependencies)
- **Expected Cold Start**: < 1 second

### Auto-Scaling

Lambda automatically scales based on incoming requests:
- Creates new instances as needed
- Maximum determined by reserved concurrency setting
- Scales down to zero when idle (cost-effective)

## Cost Estimate

### Monthly Cost (Rough Estimate)

Assumptions:
- 10,000 requests/month
- 500ms average duration
- 512MB memory
- us-west-2 region

| Service           | Cost           |
|-------------------|----------------|
| Lambda Requests   | $0.02          |
| Lambda Duration   | $0.10          |
| CloudWatch Logs   | $0.50          |
| **Total**         | **~$0.62/mo**  |

**Production** (100,000 requests/month): ~$6-8/month

### Cost Optimization Tips

1. Reduce memory if response time acceptable
2. Lower log retention (7 days for dev)
3. Use reserved concurrency to limit max spend
4. Monitor unused environments and delete

## Monitoring & Observability

### CloudWatch Metrics (Auto-created)

- **Invocations**: Total number of requests
- **Duration**: Execution time per request
- **Errors**: Failed invocations
- **Throttles**: Requests rejected due to concurrency limits
- **Concurrent Executions**: Current running instances

### Custom Logs

Lambda logs structured JSON for each request:
```json
{
  "event": "page_render",
  "view_mode": "standard",
  "mode_source": "query_string",
  "user_agent": "Mozilla/5.0...",
  "source_ip": "1.2.3.4",
  "query_mode": "standard"
}
```

### Alerting (Optional)

Set up CloudWatch Alarms for:
- Error rate > 1%
- Duration > 5 seconds
- Throttles > 0

## Disaster Recovery

### Backup Strategy

- **IaC**: All infrastructure defined in code (this CDK app)
- **Lambda Code**: Versioned in repository
- **Configuration**: Version controlled in Git

### Recovery Steps

If stack is accidentally deleted:
1. Check out correct Git commit
2. Review `config/environments.py`
3. Run: `./deploy.sh {env} deploy`
4. Recovery time: ~5 minutes

### Rollback

If deployment causes issues:
```bash
# Option 1: Redeploy previous version
git checkout <previous-commit>
./deploy.sh prod deploy

# Option 2: Destroy and recreate
./deploy.sh prod destroy
git checkout <previous-commit>
./deploy.sh prod deploy
```

## Future Enhancements

### Potential Improvements

1. **Custom Domain**: Use Route53 and CloudFront for branded URL
2. **WAF Integration**: Add Web Application Firewall for security
3. **API Gateway**: Add for advanced features (rate limiting, API keys)
4. **VPC Deployment**: For private resources access
5. **Secrets Manager**: Store Connect credentials securely
6. **X-Ray Tracing**: Enable for detailed performance analysis
7. **CI/CD Pipeline**: Automate deployments via GitHub Actions
8. **Multi-Region**: Deploy to multiple regions for HA

### Architecture Evolution

```
Current (v1.0):
  Browser → Function URL → Lambda → HTML Response

Future (v2.0):
  Browser → CloudFront → API Gateway → Lambda → S3 (static assets)
                                      ↓
                                 Secrets Manager
                                      ↓
                                 Amazon Connect
```

## References

- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [Lambda Function URLs](https://docs.aws.amazon.com/lambda/latest/dg/lambda-urls.html)
- [AWS CDK Python Reference](https://docs.aws.amazon.com/cdk/api/v2/python/)
- [Amazon Connect Chat](https://docs.aws.amazon.com/connect/latest/adminguide/chat.html)
- [CloudFormation Nested Stacks](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-nested-stacks.html)

---

**Document Version**: 1.0
**Last Updated**: 2025-02-07
**Author**: CDK Infrastructure Team
