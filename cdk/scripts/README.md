# Deployment Scripts

Automation scripts for managing widget deployments and Amazon Connect configuration.

## 📁 Scripts

### `update_widget_domains.py`
**Purpose**: Update Amazon Connect widget allowed origins after deployment

**Usage**:
```bash
# Update domains for dev environment
python scripts/update_widget_domains.py --environment dev

# Dry run (show what would change without making changes)
python scripts/update_widget_domains.py --environment prod --dry-run
```

**What it does**:
1. Reads allowed origins from `config/environments.py`
2. Attempts to update Amazon Connect widget's allowed origins
3. Updates Lambda Function URL CORS settings
4. Provides manual instructions if automatic update isn't possible

**Requirements**:
- AWS credentials configured
- Permissions to access Amazon Connect and Lambda

---

### `post_deploy.sh`
**Purpose**: Post-deployment hook that runs automatically after CDK deployment

**Auto-execution**: This script runs automatically when you use `./deploy.sh dev deploy`

**Manual usage**:
```bash
./scripts/post_deploy.sh dev
```

**What it does**:
- Calls `update_widget_domains.py` with the deployed environment
- Updates widget allowed origins to match configuration

---

## 🔄 Automated Workflow

When you deploy using `./deploy.sh dev deploy`:

```
1. CDK Deploy
   ↓
2. Stack Update Complete
   ↓
3. Post-Deploy Hook (automatic)
   ↓
4. Update Widget Domains
   ↓
5. Update Lambda CORS
   ↓
6. Deployment Complete
```

---

## ⚠️ Important Notes

### Amazon Connect Widget Origins

**Current Limitation**: AWS Connect API doesn't fully support programmatic updates to widget allowed origins. The script will:

✅ **Automatically update**: Lambda Function URL CORS
⚠️  **Requires manual step**: Amazon Connect widget allowed origins

**Manual Steps Required**:

After deployment, if the script indicates manual update is needed:

1. Open [AWS Console → Amazon Connect](https://console.aws.amazon.com/connect/)
2. Select your Connect instance
3. Go to **Channels** → **Communication widgets**
4. Select your widget
5. Click **Domain & security** tab
6. Add the allowed origins from your `config/environments.py`:
   - For dev: Usually `*` (all origins)
   - For staging/prod: Specific domains (e.g., `https://staging.example.com`)

---

## 🔧 Configuration

Allowed origins are configured in `config/environments.py`:

```python
"dev": {
    # ...
    "cors_allowed_origins": ["*"],  # Allow all origins in dev
}

"prod": {
    # ...
    "cors_allowed_origins": [
        "https://www.yourcompany.com",
        "https://yourcompany.com"
    ],  # Specific domains in production
}
```

---

## 💡 Tips

### Add Custom Post-Deployment Actions

Edit `scripts/post_deploy.sh` to add more automation:

```bash
# Example: Send deployment notification
scripts/post_deploy.sh "$ENVIRONMENT"

# Add your custom commands here
# notify_slack.sh "$ENVIRONMENT"
# run_smoke_tests.sh "$ENVIRONMENT"
```

### Skip Post-Deployment Hook

If you want to deploy without running the post-deployment hook:

```bash
# Use CDK directly instead of deploy.sh
cdk deploy -c environment=dev --require-approval never
```

---

## 🐛 Troubleshooting

### Script fails with AWS credentials error

**Problem**: `Error initializing AWS clients`

**Solution**:
```bash
# Configure AWS credentials
aws configure

# Or use environment variables
export AWS_ACCESS_KEY_ID=your-key
export AWS_SECRET_ACCESS_KEY=your-secret
export AWS_DEFAULT_REGION=us-west-2
```

### Can't find Connect instance

**Problem**: `Could not find Connect instance with alias`

**Solution**:
1. Verify `CONNECT_URL` in `config/environments.py` is correct
2. Ensure your AWS credentials have access to Amazon Connect
3. Check that the instance exists in the configured region

### Lambda Function URL CORS not updating

**Problem**: CORS settings aren't applied

**Solution**: This is expected - CORS for Lambda Function URL is managed by CDK during deployment. The script is informational only.

---

## 📚 Related Documentation

- [config/environments.py](../config/environments.py) - Environment configuration
- [docs/CONNECT_CONFIGURATION.md](../docs/CONNECT_CONFIGURATION.md) - Connect setup guide
- [deploy.sh](../deploy.sh) - Main deployment script
