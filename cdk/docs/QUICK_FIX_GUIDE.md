# Quick Fix: Configure Your Amazon Connect Credentials

## 🚨 The Problem

Your widget shows **"Something went wrong"** because it's using placeholder Amazon Connect credentials.

---

## ✅ The Solution (2 Steps)

### Step 1: Get Your Amazon Connect Credentials

**From AWS Console:**

1. Go to **Amazon Connect** in AWS Console
2. Select your Connect instance
3. Click **Channels** → **Chat widgets**
4. Create or select a widget
5. Click **Show security key**
6. Copy the widget code snippet

**Extract these 3 values from the code:**

```javascript
// You'll see something like this in the widget code:
amazon_connect('snippetId', 'YOUR_SNIPPET_ID_HERE');  // ← Copy this
s.src='https://YOUR-INSTANCE.my.connect.aws/...';      // ← Copy this
s.id='YOUR-WIDGET-ID';                                  // ← Copy this
```

You need:
- **CONNECT_URL**: `https://YOUR-INSTANCE.my.connect.aws`
- **WIDGET_ID**: UUID format (e.g., `abc12345-1234-5678-90ab-cdef12345678`)
- **SNIPPET_ID**: Long base64 string (e.g., `QVFJREF...`)

---

### Step 2: Update Configuration File

Edit **`cdk/config/environments.py`** (around line 25-40):

**Find this section:**
```python
"dev": {
    # ... other config ...
    "widget_config": {
        "VIEW_MODE": "standard",
        "COMPANY_NAME": "Trident United Way - DEV",
        "CONNECT_URL": "https://nextgencxsolutions.my.connect.aws",  # ← CHANGE THIS
        "WIDGET_ID": "cba73f0d-a749-4cb2-9e0e-2510043f48ac",         # ← CHANGE THIS
        "SNIPPET_ID": "QVFJREFIaEdEc0hWQU9TcWFkUjZBZVY0...",          # ← CHANGE THIS
        # ... rest of config ...
    },
}
```

**Replace with your values:**
```python
"dev": {
    # ... other config ...
    "widget_config": {
        "VIEW_MODE": "standard",
        "COMPANY_NAME": "Your Organization Name",                     # ← Change
        "CONNECT_URL": "https://YOUR-INSTANCE.my.connect.aws",       # ← Change
        "WIDGET_ID": "your-widget-id-here",                          # ← Change
        "SNIPPET_ID": "your-snippet-id-here",                        # ← Change
        "COLOR_NAVY": "#10264a",                                     # ← Optional
        "COLOR_GOLD": "#f5a623",                                     # ← Optional
        "WIDGET_HEADER": "Your Helpline",                            # ← Optional
        "WIDGET_BOT_NAME": "Support Specialist",                     # ← Optional
    },
}
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

## 📝 Configuration Options

### Required Fields
```python
"CONNECT_URL": "https://your-instance.my.connect.aws"  # Required
"WIDGET_ID": "your-widget-id"                          # Required
"SNIPPET_ID": "your-snippet-id"                        # Required
```

### Optional Branding
```python
"COMPANY_NAME": "Your Organization"          # Company name displayed
"COLOR_NAVY": "#10264a"                      # Primary color
"COLOR_BLUE": "#1a3a6b"                      # Secondary color
"COLOR_GOLD": "#f5a623"                      # Accent color
"WIDGET_HEADER": "Chat with Us"              # Widget header text
"WIDGET_BOT_NAME": "Support Specialist"      # Agent display name
```

---

## 🌍 Multiple Organizations?

To deploy to different organizations, create separate environment entries in `config/environments.py`:

```python
ENVIRONMENTS = {
    "dev": {
        # Dev environment config
        "widget_config": {
            "COMPANY_NAME": "Dev Test",
            "CONNECT_URL": "https://dev-instance.my.connect.aws",
            # ...
        }
    },

    "org1-prod": {  # ← New environment for Organization 1
        "stack_name_suffix": "Org1Prod",
        "aws_region": "us-west-2",
        "widget_config": {
            "COMPANY_NAME": "Organization 1",
            "CONNECT_URL": "https://org1-instance.my.connect.aws",
            "WIDGET_ID": "org1-widget-id",
            "SNIPPET_ID": "org1-snippet-id",
            # ...
        }
    },

    "org2-prod": {  # ← New environment for Organization 2
        "stack_name_suffix": "Org2Prod",
        "aws_region": "us-east-1",
        "widget_config": {
            "COMPANY_NAME": "Organization 2",
            "CONNECT_URL": "https://org2-instance.my.connect.aws",
            "WIDGET_ID": "org2-widget-id",
            "SNIPPET_ID": "org2-snippet-id",
            # ...
        }
    },
}
```

**Deploy to each:**
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
**Solution**: Double-check all 3 credentials (URL, Widget ID, Snippet ID) are from the same Connect instance

### Issue: CORS errors in browser console
**Solution**: In Connect Console → Application integration → Add your domain to approved origins

---

## 📖 Need More Help?

See complete guide: **[cdk/docs/CONNECT_CONFIGURATION.md](cdk/docs/CONNECT_CONFIGURATION.md)**

---

**Time to fix**: ~5 minutes ⚡

**After fixing, your widget will work perfectly!** 🎉
