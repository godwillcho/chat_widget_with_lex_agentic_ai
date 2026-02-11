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

### 1. **widget.py** - Base Widget Loader
- **Purpose**: Loads environment-specific Amazon Connect widget snippet from files
- **Environment-based**: Automatically loads correct file based on ENVIRONMENT variable
- **Static widget files**: Widget scripts stored in `widget_scripts/` directory
  - `connect_snippet_dev.js` - Development environment
  - `connect_snippet_staging.js` - Staging environment
  - `connect_snippet_prod.js` - Production environment

**Key Function:**
```python
def _generate_base_snippet() -> str:
    """Load environment-specific Amazon Connect snippet from file."""
    # Loads connect_snippet_{environment}.js
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

### Environment-Specific Widget Files

Widget credentials are managed in environment-specific files in `widget_scripts/`:

**Widget Script Files:**
- `connect_snippet_dev.js` - Development environment widget
- `connect_snippet_staging.js` - Staging environment widget
- `connect_snippet_prod.js` - Production environment widget

**Environment Variables (Lambda Configuration):**
Set during CDK deployment from [../../config/environments.py](../../config/environments.py):

**Optional Branding:**
- `COMPANY_NAME` - Organization name (default: "Trident United Way")
- `COLOR_NAVY` - Primary color (default: "#10264a")
- `COLOR_GOLD` - Secondary color (default: "#f5a623")
- `VIEW_MODE` - Default view mode: standard, kiosk, or mobile
- `WIDGET_HEADER` - Widget header text (default: "211 Helpline")
- `WIDGET_BOT_NAME` - Bot display name (default: "211 Specialist")

### Updating Widget Code

**Method: Update widget script files directly**

1. **Get widget script from Amazon Connect:**
   - AWS Console → Amazon Connect → Channels → Chat widgets
   - Select your widget → **Show security key**
   - Copy the entire `<script>...</script>` block

2. **Update the appropriate file:**
   - Development: `widget_scripts/connect_snippet_dev.js`
   - Staging: `widget_scripts/connect_snippet_staging.js`
   - Production: `widget_scripts/connect_snippet_prod.js`

3. **Redeploy:**
   ```bash
   cd ../../
   export PATH="/c/Program Files/nodejs:/c/Users/godwi/AppData/Roaming/npm:$PATH"
   cdk deploy -c environment=dev --require-approval never
   ```

See [widget_scripts/README.md](widget_scripts/README.md) for detailed instructions.

## 🚀 Deployment

This Lambda function is deployed via AWS CDK:

```bash
cd ../../
./deploy.sh dev deploy
```

See [../../README.md](../../README.md) for deployment instructions.

## 🏗️ Architecture Benefits

### ✅ Environment-Specific Configuration
- Separate widget files for dev, staging, prod
- Easy to manage multiple environments and organizations
- Simple file-based approach - just paste widget snippet from Amazon Connect

### ✅ Modular Widget Structure
- Base Amazon Connect snippet loaded from environment-specific files
- Custom enhancements isolated in widget_enhancements.py
- Easy to update widget when Amazon Connect releases updates
- Clear separation between base widget and customizations

### ✅ Flexible Enhancements
- Custom styles (colors, fonts, sizing)
- Custom behaviors (auto-open, auto-reset)
- View-specific CSS (kiosk, mobile positioning)
- Easy to modify without touching Amazon Connect code

### ✅ View Mode Flexibility
- Switch modes via URL parameter
- Default mode via environment variable
- Auto-detect mobile devices
- Seamless mode switching with buttons

## 🔍 Troubleshooting

### Widget shows "Something went wrong"
**Cause**: Invalid Amazon Connect credentials in widget script file
**Fix**: Update the environment-specific widget script file (connect_snippet_dev.js, etc.) with fresh snippet from Amazon Connect console and redeploy

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
