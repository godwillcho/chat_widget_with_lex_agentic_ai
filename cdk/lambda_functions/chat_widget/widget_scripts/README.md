# Amazon Connect Widget Scripts

This folder contains the raw Amazon Connect widget scripts for each environment.

## How to Update

### 1. Get the Widget Script from Amazon Connect

1. Log into **AWS Console** → **Amazon Connect**
2. Go to **Channels** → **Chat widgets**
3. Click on your widget
4. Click **"Show security key"** button
5. **Copy the entire `<script>...</script>` block**

### 2. Update the Appropriate File

- **Development**: `connect_snippet_dev.js`
- **Staging**: `connect_snippet_staging.js`
- **Production**: `connect_snippet_prod.js`

Replace the entire content of the file with the script from Amazon Connect.

### 3. Redeploy

```bash
cd cdk
cdk deploy -c environment=dev --require-approval never
```

## File Structure

```
widget_scripts/
├── README.md                      # This file
├── connect_snippet_dev.js         # Dev environment widget script
├── connect_snippet_staging.js     # Staging environment widget script
└── connect_snippet_prod.js        # Prod environment widget script
```

## Important Notes

- **Use the exact script** from Amazon Connect - don't modify it
- The script includes:
  - Widget initialization code
  - Widget ID and Snippet ID (credentials)
  - ViewConfig (pre-chat form configuration)
  - Styles and settings
- Our code will automatically add custom enhancements on top of this base script
- Each environment can have different widget configurations

## What Gets Added Automatically

After loading the base Amazon Connect script, the system automatically adds:

1. **Custom styles** (from `widget_enhancements.py`)
   - Branded colors (navy, gold)
   - Custom sizing (standard, kiosk, mobile modes)
   - Typography and spacing

2. **Custom behaviors** (from `widget_enhancements.py`)
   - Auto-open for kiosk/mobile modes
   - Auto-reset on close
   - Custom display names

You don't need to include these in the Amazon Connect script - they're added programmatically.

## Troubleshooting

### Widget shows "Something went wrong"

1. **Check credentials**: Make sure WIDGET_ID and SNIPPET_ID in the script are correct
2. **Check approved origins**: Add your Lambda Function URL to Amazon Connect's approved origins
   - Go to: Amazon Connect → Channels → Chat widgets → Your widget → Domain & Security
   - Add: `https://YOUR-FUNCTION-URL.lambda-url.REGION.on.aws`

### Pre-chat form not showing

1. Make sure the script includes `amazon_connect('viewConfig', '...')` line
2. Verify the viewConfig has `inputSchema` with field definitions
3. Check browser console for specific errors

### How to test

1. Open the Lambda Function URL in your browser
2. Click the chat widget (bottom-right corner)
3. The pre-chat form should appear if configured
4. Fill out the form and click submit to start chat
