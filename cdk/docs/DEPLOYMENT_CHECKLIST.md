# Deployment Checklist

Use this checklist for each environment deployment to ensure nothing is missed.

## Pre-Deployment

### Prerequisites
- [ ] Python 3.11+ installed and verified (`python --version`)
- [ ] Node.js 18+ installed (`node --version`)
- [ ] AWS CDK CLI installed (`cdk --version`)
- [ ] AWS CLI installed and configured (`aws sts get-caller-identity`)
- [ ] Access to target AWS account verified
- [ ] IAM permissions validated (CloudFormation, Lambda, IAM, Logs, S3)

### Configuration Review
- [ ] Environment config reviewed in `config/environments.py`
- [ ] Amazon Connect credentials updated (WIDGET_ID, SNIPPET_ID, CONNECT_URL)
- [ ] Company name and branding correct
- [ ] Lambda memory and timeout appropriate for environment
- [ ] CORS origins configured correctly
- [ ] Log retention days set appropriately
- [ ] Concurrent execution limits set (if needed)

### Code Review
- [ ] Lambda code tested locally
- [ ] All Python dependencies compatible with Lambda runtime (Python 3.11)
- [ ] No hardcoded secrets or credentials in code
- [ ] Error handling in place
- [ ] Logging configured properly

## Deployment Steps

### First-Time Deployment (Per Account)
- [ ] CDK bootstrapped in target account/region:
  ```bash
  ./deploy.sh {env} bootstrap
  ```
- [ ] Bootstrap bucket created successfully
- [ ] CDK toolkit stack deployed

### Standard Deployment
- [ ] Virtual environment activated
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Synthesized template reviewed:
  ```bash
  ./deploy.sh {env} synth
  ```
- [ ] No errors in synthesis
- [ ] Diff reviewed (if updating existing stack):
  ```bash
  ./deploy.sh {env} diff
  ```
- [ ] Deployment executed:
  ```bash
  ./deploy.sh {env} deploy
  ```
- [ ] Deployment completed successfully
- [ ] Function URL captured from output

## Post-Deployment Validation

### Functional Testing
- [ ] Function URL accessible in browser
- [ ] Widget loads without errors
- [ ] Correct view mode displayed (standard/kiosk/mobile)
- [ ] Mode switcher works (if enabled)
- [ ] Widget opens and displays chat interface
- [ ] Amazon Connect pre-chat form displays
- [ ] Form submission works
- [ ] Chat session starts successfully
- [ ] Mobile detection working (test with mobile user agent)
- [ ] Query string mode override works: `?mode=kiosk`

### Technical Validation
- [ ] CloudWatch logs created: `/aws/lambda/chat-widget-{env}`
- [ ] Log entries visible in CloudWatch
- [ ] No errors in Lambda execution logs
- [ ] IAM role attached correctly
- [ ] Function URL CORS headers correct
- [ ] Response time acceptable (< 2 seconds for initial load)
- [ ] CloudFormation stack status: `CREATE_COMPLETE` or `UPDATE_COMPLETE`
- [ ] All stack outputs present

### Monitoring Setup
- [ ] CloudWatch dashboard created (if needed)
- [ ] Alarms configured for errors/throttles (production only)
- [ ] Log retention policy applied
- [ ] X-Ray tracing enabled (if needed)

### Security Review
- [ ] CORS origins restricted (not `*` in production)
- [ ] Function URL auth type confirmed: NONE (public access intended)
- [ ] No sensitive data exposed in logs
- [ ] IAM role follows least privilege
- [ ] Environment variables don't contain secrets

## Environment-Specific Checks

### Development Environment
- [ ] `dev` environment configured
- [ ] Test data/credentials used
- [ ] Unrestricted CORS acceptable
- [ ] Lower resource limits acceptable

### Staging Environment
- [ ] `staging` environment configured
- [ ] Production-like configuration
- [ ] CORS restricted to staging domains
- [ ] Appropriate resource limits

### Production Environment
- [ ] `prod` environment configured
- [ ] Production Amazon Connect instance
- [ ] Production branding and company name
- [ ] CORS restricted to production domains only
- [ ] Reserved concurrency configured
- [ ] Extended log retention (30+ days)
- [ ] Alarms configured
- [ ] Runbook documented

## Rollback Plan

If issues occur:
- [ ] Rollback procedure documented
- [ ] Previous CloudFormation stack version noted
- [ ] Rollback command ready:
  ```bash
  ./deploy.sh {env} destroy  # Then redeploy previous version
  ```
- [ ] Stakeholders notified of rollback

## Documentation

- [ ] Function URL documented
- [ ] Stack name recorded: `ChatWidget-{Environment}`
- [ ] Deployment date/time noted
- [ ] Deployer name recorded
- [ ] Change log updated
- [ ] Runbook updated (if changes)

## Sign-Off

**Environment**: _____________

**Deployed By**: _____________

**Date**: _____________

**Function URL**: _____________

**Stack ARN**: _____________

**Validation Completed**: [ ] Yes [ ] No

**Issues Found**: [ ] None [ ] See notes below

**Production Ready**: [ ] Yes [ ] No

**Notes**:
```
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
```

---

## Quick Command Reference

```bash
# Synthesize
./deploy.sh {env} synth

# View diff
./deploy.sh {env} diff

# Deploy
./deploy.sh {env} deploy

# View logs
aws logs tail /aws/lambda/chat-widget-{env} --follow

# Get Function URL
aws cloudformation describe-stacks \
  --stack-name ChatWidget-{Env} \
  --query "Stacks[0].Outputs[?OutputKey=='WidgetUrl'].OutputValue" \
  --output text

# Test Function
curl -v {function-url}

# Destroy (BE CAREFUL!)
./deploy.sh {env} destroy
```

Replace `{env}` with: `dev`, `staging`, or `prod`
Replace `{Env}` with: `Dev`, `Staging`, or `Prod` (capitalized)
