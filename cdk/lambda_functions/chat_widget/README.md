# Chat Widget Lambda Function

Modular Amazon Connect chat widget with environment-based configuration.

## 📁 File Structure

```
chat_widget/
├── lambda_function.py        # Lambda handler (entry point)
├── config.py                 # Configuration from environment variables
├── view_config.py            # View mode detection (deprecated - use config.py)
├── widget.py                 # 🔧 Generates base snippet + enhancements
├── widget_enhancements.py    # 🎨 Custom enhancements
├── styles.py                 # Page-level CSS
├── page.py                   # HTML templates
└── README.md                 # This file
```

## 🔧 Architecture

### 1. **widget.py** - Base Widget Generator
- **Purpose**: Generates Amazon Connect widget snippet using environment variables
- **Dynamic Generation**: Snippet is created at runtime using config values
- **No static files**: All credentials come from Lambda environment variables

**Key Function:**
```python
def _generate_base_snippet() -> str:
    """Generate base Amazon Connect snippet from env vars."""
    # Uses CONNECT_URL, WIDGET_ID, SNIPPET_ID from config.py
```

### 2. **widget_enhancements.py** - Custom Enhancements
- **Purpose**: All customizations and behavior modifications
- **Includes**:
  - Custom styles (colors, fonts, sizing)
  - Custom display names (header, bot name, placeholders)
  - Auto-open functionality (kiosk, mobile)
  - Auto-reset on chat end (kiosk)
  - View-specific CSS (kiosk, mobile positioning)

**Key Functions:**
- `custom_styles_script()` - Inject custom colors, fonts, sizing
- `auto_open_script()` - Auto-open widget on page load
- `auto_reset_script()` - Auto-reload after chat ends (kiosk)
- `kiosk_css()` - CSS for kiosk mode (centered, large)
- `mobile_css()` - CSS for mobile mode (full-width)
- `get_enhancements()` - Returns all enhancements for current view mode

### 3. **config.py** - Environment Configuration
- **Purpose**: Centralized configuration from Lambda environment variables
- **Credentials**: CONNECT_URL, WIDGET_ID, SNIPPET_ID
- **Branding**: COMPANY_NAME, colors
- **View Mode**: Determines widget layout and behavior

## 🎯 View Modes

The widget supports three view modes (configured via `?mode=` parameter or environment variable):

### Standard (default)
- Floating widget in bottom-right corner
- Full 211 website layout
- No auto-open

### Kiosk (`?mode=kiosk`)
- Large centered widget
- Auto-opens on page load
- Auto-resets when chat ends or widget closes
- Dark background with branding panel
- Optimized for touch screens

### Mobile (`?mode=mobile`)
- Full-width widget below header
- Auto-opens on page load
- Compact mobile header
- Optimized for phone/tablet

**View Mode Switching:**
- Buttons appear in top-right corner (Website, Kiosk, Mobile)
- Click to instantly switch between modes
- URL updates with `?mode=` parameter

## 🔄 Configuration Management

### Environment Variables (Lambda Configuration)

All credentials and settings are managed through Lambda environment variables, which are set during CDK deployment from [../../config/environments.py](../../config/environments.py):

**Required:**
- `CONNECT_URL` - Amazon Connect instance URL
- `WIDGET_ID` - Widget ID (UUID)
- `SNIPPET_ID` - Encrypted snippet ID (base64 string)

**Optional:**
- `COMPANY_NAME` - Organization name (default: "Trident United Way")
- `COLOR_NAVY` - Primary color (default: "#10264a")
- `COLOR_GOLD` - Secondary color (default: "#f5a623")
- `VIEW_MODE` - Default view mode: standard, kiosk, or mobile
- `WIDGET_HEADER` - Widget header text (default: "211 Helpline")
- `WIDGET_BOT_NAME` - Bot display name (default: "211 Specialist")

### Updating Credentials

**Method: Edit config/environments.py**

1. **Edit configuration file:**
   ```bash
   # Open config/environments.py
   # Update the environment you want to deploy
   ```

2. **Update credentials:**
   ```python
   "dev": {
       "widget_config": {
           "COMPANY_NAME": "Your Organization",
           "CONNECT_URL": "https://your-instance.my.connect.aws",
           "WIDGET_ID": "your-widget-id-uuid",
           "SNIPPET_ID": "your-base64-snippet-id",
           # ... other settings
       }
   }
   ```

3. **Redeploy:**
   ```bash
   cd ../../
   export PATH="/c/Program Files/nodejs:/c/Users/godwi/AppData/Roaming/npm:$PATH"
   cdk deploy -c environment=dev --require-approval never
   ```

### Getting Amazon Connect Credentials

1. **AWS Console** → **Amazon Connect** → Your Instance
2. Click **Channels** → **Chat widgets**
3. Select your widget → **Show security key**
4. Copy widget code snippet
5. Extract values:
   - **CONNECT_URL**: From `s.src='https://YOUR-INSTANCE.my.connect.aws/...'`
   - **WIDGET_ID**: From `'amazon_connect', 'WIDGET-ID-HERE'`
   - **SNIPPET_ID**: From `amazon_connect('snippetId', 'LONG-BASE64-STRING')`

## 🚀 Deployment

This Lambda function is deployed via AWS CDK:

```bash
cd ../../
./deploy.sh dev deploy
```

See [../../README.md](../../README.md) for deployment instructions.

## 🏗️ Architecture Benefits

### ✅ Centralized Configuration
- All credentials in one place (config/environments.py)
- Easy to manage multiple environments
- No hardcoded credentials in code

### ✅ Dynamic Snippet Generation
- Snippet generated at runtime from environment variables
- No static files to maintain
- Credentials stay in CDK configuration

### ✅ Modular Enhancements
- Custom styles isolated in widget_enhancements.py
- Easy to modify appearance and behavior
- Clear separation between base widget and customizations

### ✅ View Mode Flexibility
- Switch modes via URL parameter
- Default mode via environment variable
- Auto-detect mobile devices
- Seamless mode switching with buttons

## 🔍 Troubleshooting

### Widget shows "Something went wrong"
**Cause**: Invalid Amazon Connect credentials
**Fix**: Update CONNECT_URL, WIDGET_ID, SNIPPET_ID in config/environments.py and redeploy

### View mode buttons don't work
**Cause**: Module caching issue
**Fix**: Ensure widget_enhancements is in reimport list (already fixed)

### Widget doesn't auto-open in kiosk/mobile mode
**Cause**: Enhancements not loading
**Fix**: Check CloudWatch logs, verify view mode is correct

### Credentials showing in logs
**Warning**: Never log SNIPPET_ID - it contains encrypted credentials
**Check**: Review CloudWatch logs to ensure no sensitive data is logged

## 📊 Monitoring

View Lambda logs:
```bash
aws logs tail /aws/lambda/chat-widget-dev --follow
```

Each request logs:
- View mode used
- Mode source (query string, env var, auto-detect, default)
- User agent
- Source IP

## 🔐 Security Notes

- Credentials are passed as Lambda environment variables (encrypted at rest)
- Never commit credentials to git
- SNIPPET_ID contains encrypted Connect credentials
- All requests logged to CloudWatch for audit trail
