# Amazon Connect Widget Allowed Origins - Quick Guide

After deploying your chat widget, you need to configure allowed origins in Amazon Connect to specify which domains can use your widget.

---

## 🎯 Why This is Needed

Amazon Connect widgets have security restrictions that only allow specific domains to embed and use the widget. This prevents unauthorized websites from using your widget.

**Two CORS configurations needed:**
1. **Lambda Function URL CORS** ← Automated by CDK ✅
2. **Amazon Connect Widget Origins** ← Manual step required ⚠️

---

## 🚀 Automated Process

After running `./deploy.sh dev deploy`, the post-deployment hook automatically:

✅ Updates Lambda Function URL CORS settings
✅ Displays current allowed origins from your config
⚠️  Provides instructions for updating Connect widget (manual step)

---

## 📋 Manual Steps (Required)

### Step 1: Open Amazon Connect Console

1. Log into [AWS Console](https://console.aws.amazon.com)
2. Navigate to **Amazon Connect** service
3. Select your Connect instance

### Step 2: Go to Communication Widgets

1. In left sidebar: Click **Channels**
2. Click **Communication widgets**
3. Find and click your widget

   You can find your Widget ID in `config/environments.py`:
   ```python
   "WIDGET_ID": "abc12345-1234-5678-90ab-cdef12345678"  # This one
   ```

### Step 3: Update Allowed Origins

1. Click **Domain & security** tab
2. Under "Add the required domains for the communication widget":
   - For **Development**: Add `*` (allows all domains)
   - For **Production**: Add specific domains

3. Click **+ Add domain** and enter each origin:

   **Example for Dev**:
   ```
   https://wxd2gcfo7vjv63ni2nwuvce3ma0zcpxc.lambda-url.us-east-1.on.aws
   ```

   **Example for Production**:
   ```
   https://www.yourcompany.com
   https://yourcompany.com
   ```

4. Click **Save**

---

## 📊 Environment-Specific Origins

### Development Environment

**In `config/environments.py`**:
```python
"dev": {
    "cors_allowed_origins": ["*"],  # Allow all origins
}
```

**In Amazon Connect Console**:
- Add your Lambda Function URL
- Or use `*` to allow all origins (for testing only!)

### Production Environment

**In `config/environments.py`**:
```python
"prod": {
    "cors_allowed_origins": [
        "https://www.yourcompany.com",
        "https://yourcompany.com"
    ],
}
```

**In Amazon Connect Console**:
- Add each specific domain
- Match exactly what's in `cors_allowed_origins`
- Include both `www` and non-`www` if needed

---

## 🔍 Finding Your Lambda Function URL

The post-deployment script displays your Function URL after each deployment:

```
Function URL:
https://wxd2gcfo7vjv63ni2nwuvce3ma0zcpxc.lambda-url.us-east-1.on.aws/
```

Or retrieve it manually:

```bash
aws cloudformation describe-stacks \
    --stack-name Project-Dev \
    --query "Stacks[0].Outputs[?OutputKey=='WebAppUrl'].OutputValue" \
    --output text
```

---

## ⚙️ Using the Automation Script

### Run After Deployment

```bash
# Update domains for dev environment
python scripts/update_widget_domains.py --environment dev
```

### Dry Run (Preview Changes)

```bash
# See what would be updated without making changes
python scripts/update_widget_domains.py --environment prod --dry-run
```

### Script Output

The script will:
1. ✅ Display current configuration
2. ✅ Show which origins should be added
3. ⚠️  Provide manual instructions for Connect Console
4. ✅ Update Lambda Function URL CORS (if needed)

---

## 🔒 Security Best Practices

### Development

✅ **OK to use**: `*` (wildcard) for allowed origins
⚠️  **Warning**: Only in dev/testing environments

### Staging/Production

❌ **Never use**: `*` (wildcard) in production
✅ **Always use**: Specific domain names

**Example**:
```python
"cors_allowed_origins": [
    "https://www.yourcompany.com",  # Production website
    "https://yourcompany.com",      # Without www
    "https://app.yourcompany.com",  # If embedding in app
]
```

---

## 🆘 Common Issues

### Issue: Widget shows "Something went wrong"

**Cause**: Domain not in allowed origins

**Solution**:
1. Check browser console for CORS errors
2. Verify domain is added in Connect Console
3. Ensure domain matches exactly (including `https://`)

### Issue: "Failed to load widget script"

**Cause**: Connect URL or Widget ID incorrect

**Solution**:
1. Verify `CONNECT_URL` in `config/environments.py`
2. Verify `WIDGET_ID` matches your Connect widget
3. Redeploy after fixing configuration

### Issue: CORS error in browser console

**Example error**:
```
Access to fetch at 'https://instance.my.connect.aws/...' has been blocked by CORS policy
```

**Solution**:
1. Add your domain to Connect widget allowed origins
2. Wait a few minutes for changes to propagate
3. Clear browser cache and reload

---

## 📝 Checklist After Each Deployment

- [ ] Deployment completed successfully
- [ ] Post-deployment script ran
- [ ] Note the Function URL displayed
- [ ] Open Amazon Connect Console
- [ ] Go to your widget's "Domain & security" tab
- [ ] Add/verify all required origins
- [ ] Save changes
- [ ] Test the widget in browser
- [ ] Check for CORS errors in browser console

---

## 🔄 Future Automation

**Note**: Currently, Amazon Connect doesn't provide a full API to programmatically update widget allowed origins. The manual step is required.

If AWS releases an API for this in the future, we'll update the automation script to handle it fully.

---

## 📚 Related Documentation

- [config/environments.py](../config/environments.py) - Configure allowed origins here
- [scripts/README.md](../scripts/README.md) - Automation scripts documentation
- [QUICK_FIX_GUIDE.md](QUICK_FIX_GUIDE.md) - Fix widget errors
- [CONNECT_CONFIGURATION.md](CONNECT_CONFIGURATION.md) - Complete Connect setup

---

## 💡 Quick Reference

| Environment | Allowed Origins | Where to Add |
|-------------|----------------|--------------|
| **Dev** | `*` or Function URL | Connect Console → Widget → Domain & security |
| **Staging** | Specific staging domain | Connect Console → Widget → Domain & security |
| **Production** | Specific production domains | Connect Console → Widget → Domain & security |

**Remember**: Changes in `config/environments.py` only update Lambda CORS. You must manually update Connect widget origins in the AWS Console.
