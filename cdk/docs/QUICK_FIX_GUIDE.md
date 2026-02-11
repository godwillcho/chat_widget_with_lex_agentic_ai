# Quick Fix: Configure Your Amazon Connect Credentials

## 🚨 The Problem

Your widget shows **"Something went wrong"** because it's using placeholder Amazon Connect credentials.

---

## ✅ The Solution (2 Steps)

### Step 1: Get Your Amazon Connect Widget Script

**From AWS Console:**

1. Go to **Amazon Connect** in AWS Console
2. Select your Connect instance
3. Click **Channels** → **Chat widgets**
4. Create or select a widget
5. Click **Show security key**
6. **Copy the entire `<script>...</script>` block**

---

### Step 2: Update Widget Script File

Paste the widget script into the appropriate environment file:

**For Development:**
Edit **`cdk/lambda_functions/chat_widget/widget_scripts/connect_snippet_dev.js`**

**For Staging:**
Edit **`cdk/lambda_functions/chat_widget/widget_scripts/connect_snippet_staging.js`**

**For Production:**
Edit **`cdk/lambda_functions/chat_widget/widget_scripts/connect_snippet_prod.js`**

**Replace the entire file content** with the script you copied from Amazon Connect.

Example content:
```javascript
<script type="text/javascript">
  (function(w, d, x, id){
    s=d.createElement('script');
    s.src='https://YOUR-INSTANCE.my.connect.aws/connectwidget/static/amazon-connect-chat-interface-client.js';
    s.async=1;
    s.id=id;
    d.getElementsByTagName('head')[0].appendChild(s);
    w[x] =  w[x] || function() { (w[x].ac = w[x].ac || []).push(arguments) };
  })(window, document, 'amazon_connect', 'YOUR-WIDGET-ID');

  amazon_connect('styles', {
    iconType: 'CHAT',
    openChat: { color: '#ffffff', backgroundColor: '#123456' },
    closeChat: { color: '#ffffff', backgroundColor: '#123456'}
  });

  amazon_connect('snippetId', 'YOUR-LONG-SNIPPET-ID');

  amazon_connect('supportedMessagingContentTypes', [
    'text/plain',
    'text/markdown',
    'application/vnd.amazonaws.connect.message.interactive',
    'application/vnd.amazonaws.connect.message.interactive.response'
  ]);
</script>
```

---

### Step 3: Redeploy

```bash
cd cdk
export PATH="/c/Program Files/nodejs:/c/Users/godwi/AppData/Roaming/npm:$PATH"
cdk deploy -c environment=dev --require-approval never
```

**That's it!** Your widget will work. ✅

---

## 🔍 Don't Have Amazon Connect Yet?

### Create Amazon Connect Instance

1. **AWS Console** → **Amazon Connect**
2. Click **Create instance**
3. Identity management: **Store users within Amazon Connect**
4. Instance name: `my-helpline-instance`
5. Create administrator
6. Complete setup wizard

### Create Chat Widget

1. In your Connect instance → **Channels** → **Chat widgets**
2. Click **Add a new chat widget**
3. Widget name: `My Help Chat`
4. Welcome message: `Welcome! How can we help you today?`
5. Click **Create**
6. **Show security key** → Copy the code

### Create Contact Flow

1. **Routing** → **Contact flows**
2. **Create contact flow**
3. Add blocks:
   - Entry point → Set working queue
   - Set working queue → Transfer to queue
4. **Save** and **Publish**
5. Copy Contact Flow ID

### Link Widget to Contact Flow

1. Go back to your widget
2. Settings → Contact Flow
3. Select the contact flow you created
4. Save

**Now get your widget credentials and follow Steps 1-3 above!**

---

## 📝 Optional Branding Configuration

You can customize branding and colors in **`cdk/config/environments.py`**:

```python
"dev": {
    "widget_config": {
        "COMPANY_NAME": "Your Organization"          # Company name displayed
        "COLOR_NAVY": "#10264a"                      # Primary color
        "COLOR_BLUE": "#1a3a6b"                      # Secondary color
        "COLOR_GOLD": "#f5a623"                      # Accent color
        "WIDGET_HEADER": "Chat with Us"              # Widget header text
        "WIDGET_BOT_NAME": "Support Specialist"      # Agent display name
        # ... other settings
    }
}
```

**Note:** Widget credentials (URLs, IDs, snippetId) are now in the widget script files, not in environments.py.

---

## 🌍 Multiple Organizations?

Each environment has its own widget script file. To support multiple organizations:

1. **Create environment-specific widget files** in `cdk/lambda_functions/chat_widget/widget_scripts/`:
   - `connect_snippet_org1prod.js`
   - `connect_snippet_org2prod.js`

2. **Add environments** in `config/environments.py`:
   ```python
   ENVIRONMENTS = {
       "dev": {
           # Dev environment config
           "widget_config": {
               "COMPANY_NAME": "Dev Test",
               # ...
           }
       },

       "org1-prod": {  # ← New environment for Organization 1
           "stack_name_suffix": "Org1Prod",
           "aws_region": "us-west-2",
           "widget_config": {
               "COMPANY_NAME": "Organization 1",
               # ...
           }
       },

       "org2-prod": {  # ← New environment for Organization 2
           "stack_name_suffix": "Org2Prod",
           "aws_region": "us-east-1",
           "widget_config": {
               "COMPANY_NAME": "Organization 2",
               # ...
           }
       },
   }
   ```

3. **Paste widget scripts** from each organization's Amazon Connect into their respective files

4. **Deploy to each:**
   ```bash
   # Organization 1
   cdk deploy -c environment=org1-prod --require-approval never

   # Organization 2
   cdk deploy -c environment=org2-prod --require-approval never
   ```

---

## ❓ Common Issues

### Issue: Widget still shows error after redeployment
**Solution**: Wait 1-2 minutes for Lambda to update, then hard refresh browser (Ctrl+Shift+R)

### Issue: Widget loads but can't start chat
**Solution**: Ensure you created and published a Contact Flow, and linked it to your widget

### Issue: "Invalid widget configuration" error
**Solution**: Make sure you copied the complete widget script from Amazon Connect without modifications

### Issue: CORS errors in browser console
**Solution**: In Connect Console → Application integration → Add your domain to approved origins

---

## 📖 Need More Help?

See complete guide: **[cdk/docs/CONNECT_CONFIGURATION.md](cdk/docs/CONNECT_CONFIGURATION.md)**

---

**Time to fix**: ~5 minutes ⚡

**After fixing, your widget will work perfectly!** 🎉
