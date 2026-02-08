"""
widget_enhancements.py — Custom enhancements for Amazon Connect widget
────────────────────────────────────────────────────────────────────────────
All customizations, styling, and behavior modifications for the widget.
This file contains all enhancements separate from the base Amazon Connect snippet.

Enhancements included:
  - Custom styles (colors, fonts, sizing)
  - Custom display names (header, bot name, placeholders)
  - Auto-open functionality (kiosk, mobile)
  - Auto-reset on chat end (kiosk only)
  - View-specific CSS (kiosk, mobile positioning)
"""

from config import (
    VIEW_MODE, IS_KIOSK, IS_MOBILE, IS_STD,
    COLOR_NAVY,
    WIDGET_WIDTH, WIDGET_HEIGHT, WIDGET_FONT_SIZE,
    WIDGET_HEADER, WIDGET_BOT_NAME, COMPANY_NAME_JS,
)


def _js_esc(s: str) -> str:
    """Escape strings for safe use in JavaScript."""
    return s.replace("\\", "\\\\").replace("'", "\\'")


def custom_styles_script() -> str:
    """Generate custom styles for the Amazon Connect widget."""
    fh = "90px" if IS_KIOSK else ("70px" if IS_MOBILE else "70px")
    hh = "80px" if IS_KIOSK else ("56px" if IS_MOBILE else "64px")
    lh = "48px" if IS_KIOSK else ("36px" if IS_MOBILE else "40px")

    return f"""<script type="text/javascript">
    amazon_connect('customStyles', {{
        global: {{
            frameWidth: '{WIDGET_WIDTH}', frameHeight: '{WIDGET_HEIGHT}',
            textColor: '#1f2937', fontSize: '{WIDGET_FONT_SIZE}',
            footerHeight: '{fh}', headerHeight: '{hh}',
            typeface: "'Open Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
            customTypefaceStylesheetUrl:
                'https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;500;600;700&display=swap',
        }},
        header: {{ headerTextColor: '#ffffff', headerBackgroundColor: '{COLOR_NAVY}' }},
        transcript: {{
            messageFontSize: '{WIDGET_FONT_SIZE}',
            messageTextColor: '#374151', widgetBackgroundColor: '#f9fafb',
            agentMessageTextColor: '#1f2937', systemMessageTextColor: '#6b7280',
            customerMessageTextColor: '#ffffff',
            agentChatBubbleColor: '#ffffff', systemChatBubbleColor: '#e5e7eb',
            customerChatBubbleColor: '{COLOR_NAVY}',
        }},
        footer: {{
            buttonFontSize: '{WIDGET_FONT_SIZE}', buttonTextColor: '#ffffff',
            buttonBorderColor: '{COLOR_NAVY}', buttonBackgroundColor: '{COLOR_NAVY}',
            footerBackgroundColor: '#ffffff',
        }},
        logo: {{ logoMaxHeight: '{lh}', logoMaxWidth: '80%' }},
        composer: {{ fontSize: '{WIDGET_FONT_SIZE}' }},
    }});

    amazon_connect('customDisplayNames', {{
        header: {{ headerMessage: '{_js_esc(WIDGET_HEADER)}' }},
        transcript: {{
            systemMessageDisplayName: '{COMPANY_NAME_JS}',
            botMessageDisplayName: '{_js_esc(WIDGET_BOT_NAME)}',
        }},
        footer: {{
            textInputPlaceholder: 'Describe what you need help with\\u2026',
            endChatButtonText: 'End Chat',
            closeChatButtonText: 'Close',
        }},
    }});
</script>"""


def auto_open_script() -> str:
    """Auto-open the widget on page load (used by kiosk and mobile modes)."""
    return """
<script>
(function() {
    function tryOpen() {
        var btn = document.getElementById('amazon-connect-open-widget-button');
        if (btn) { btn.click(); }
        else { setTimeout(tryOpen, 400); }
    }
    setTimeout(tryOpen, 1200);
})();
</script>"""


def auto_reset_script() -> str:
    """Auto-reload on chat end or widget close (kiosk mode only)."""
    return """
<script>
(function() {
    var cbRegistered = false;
    var cbInterval = setInterval(function() {
        if (cbRegistered) return;
        if (window.amazon_connect && typeof window.amazon_connect === 'function') {
            try {
                amazon_connect('registerCallback', {
                    'CHAT_ENDED': function() {
                        setTimeout(function() { window.location.reload(); }, 2500);
                    }
                });
                cbRegistered = true;
                clearInterval(cbInterval);
            } catch(e) {}
        }
    }, 800);

    var wasShowing = false;
    setInterval(function() {
        var frame = document.getElementById('amazon-connect-widget-frame');
        if (!frame) return;
        var isShowing = frame.classList.contains('show');
        if (wasShowing && !isShowing) {
            setTimeout(function() { window.location.reload(); }, 1000);
        }
        wasShowing = isShowing;
    }, 500);
})();
</script>"""


def kiosk_css() -> str:
    """CSS styling for kiosk mode (centered, large widget)."""
    return """
<style>
    #amazon-connect-open-widget-button,
    #amazon-connect-close-widget-button { display: none !important; }

    #amazon-connect-widget-frame {
        position: fixed !important;
        bottom: auto !important; right: auto !important;
        top: 50% !important; left: 50% !important;
        transform: translate(-50%, -50%) !important;
        width: min(780px, 92vw) !important;
        height: min(920px, calc(100vh - 60px)) !important;
        max-width: 780px !important;
        border-radius: 20px !important;
        box-shadow: 0 25px 80px rgba(16,38,74,0.35), 0 8px 24px rgba(0,0,0,0.15) !important;
        z-index: 100 !important;
    }
    #amazon-connect-widget-frame:not(.show) {
        display: block !important; opacity: 0; pointer-events: none;
    }
    #amazon-connect-widget-frame.show {
        display: block !important; opacity: 1; pointer-events: auto;
    }
</style>"""


def mobile_css() -> str:
    """CSS styling for mobile mode (full-width, below header)."""
    return """
<style>
    #amazon-connect-open-widget-button,
    #amazon-connect-close-widget-button { display: none !important; }

    #amazon-connect-widget-frame {
        position: fixed !important;
        top: 72px !important;
        left: 0 !important;
        right: 0 !important;
        bottom: 0 !important;
        width: 100vw !important;
        height: calc(100vh - 72px) !important;
        max-width: 100vw !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        z-index: 100 !important;
    }
    #amazon-connect-widget-frame:not(.show) {
        display: block !important; opacity: 0; pointer-events: none;
    }
    #amazon-connect-widget-frame.show {
        display: block !important; opacity: 1; pointer-events: auto;
    }
</style>"""


def form_styling_css() -> str:
    """Professional CSS styling for Amazon Connect forms passed from Show view block."""
    return """
<style>
/* ═══════════════════════════════════════════════════════════════════
   PROFESSIONAL FORM STYLING FOR AMAZON CONNECT VIEWS
   ══════════════════════════════════════════════════════════════════ */

/* Form Container */
.connect-view-form,
[class*="Form_"],
[data-testid*="form"] {
    background: #ffffff !important;
    border-radius: 12px !important;
    padding: 24px !important;
    margin: 16px 0 !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06) !important;
}

/* Form Headers */
.connect-view-form h1,
.connect-view-form h2,
.connect-view-form h3,
[class*="Header_"] h1,
[class*="Header_"] h2,
[class*="Header_"] h3 {
    color: #10264a !important;
    font-family: 'Open Sans', -apple-system, sans-serif !important;
    font-weight: 700 !important;
    margin-bottom: 8px !important;
    line-height: 1.3 !important;
}

.connect-view-form h2,
[class*="Header_"] h2 {
    font-size: 1.5rem !important;
}

/* Form Header Descriptions */
.connect-view-form [class*="description"],
[class*="Header_"] [class*="description"],
[class*="Header_"] p {
    color: #6b7280 !important;
    font-size: 0.9rem !important;
    line-height: 1.5 !important;
    margin-bottom: 20px !important;
    font-family: 'Open Sans', sans-serif !important;
}

/* Form Input Groups */
.connect-view-form [class*="FormInput"],
.connect-view-form .form-group,
[class*="FormInput_"] {
    margin-bottom: 18px !important;
}

/* Form Labels */
.connect-view-form label,
[class*="FormInput_"] label,
[class*="Label_"] {
    display: block !important;
    color: #374151 !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    margin-bottom: 6px !important;
    font-family: 'Open Sans', sans-serif !important;
}

/* Required Field Indicator */
.connect-view-form label[required]::after,
[class*="FormInput_"][class*="required"] label::after {
    content: " *" !important;
    color: #dc2626 !important;
}

/* Input Fields */
.connect-view-form input[type="text"],
.connect-view-form input[type="email"],
.connect-view-form input[type="tel"],
.connect-view-form input[type="number"],
.connect-view-form textarea,
.connect-view-form select,
[class*="FormInput_"] input,
[class*="FormInput_"] textarea,
[class*="FormInput_"] select {
    width: 100% !important;
    padding: 11px 14px !important;
    font-size: 0.95rem !important;
    font-family: 'Open Sans', sans-serif !important;
    color: #1f2937 !important;
    background: #ffffff !important;
    border: 2px solid #d1d5db !important;
    border-radius: 8px !important;
    transition: all 0.2s ease !important;
    box-sizing: border-box !important;
}

/* Input Focus State */
.connect-view-form input:focus,
.connect-view-form textarea:focus,
.connect-view-form select:focus,
[class*="FormInput_"] input:focus,
[class*="FormInput_"] textarea:focus,
[class*="FormInput_"] select:focus {
    outline: none !important;
    border-color: #10264a !important;
    box-shadow: 0 0 0 3px rgba(16, 38, 74, 0.1) !important;
}

/* Input Hover State */
.connect-view-form input:hover,
.connect-view-form textarea:hover,
.connect-view-form select:hover,
[class*="FormInput_"] input:hover,
[class*="FormInput_"] textarea:hover,
[class*="FormInput_"] select:hover {
    border-color: #9ca3af !important;
}

/* Input Error State */
.connect-view-form input[aria-invalid="true"],
.connect-view-form textarea[aria-invalid="true"],
.connect-view-form select[aria-invalid="true"],
[class*="error"] input,
[class*="invalid"] input {
    border-color: #dc2626 !important;
    background: #fef2f2 !important;
}

/* Error Messages */
.connect-view-form .error-message,
.connect-view-form [class*="error"],
[class*="ErrorMessage_"],
[role="alert"] {
    color: #dc2626 !important;
    font-size: 0.85rem !important;
    margin-top: 4px !important;
    font-family: 'Open Sans', sans-serif !important;
}

/* Submit/Action Buttons */
.connect-view-form button[type="submit"],
.connect-view-form [class*="ConnectAction"],
[class*="ConnectAction_"] button,
[class*="SubmitButton_"] {
    width: 100% !important;
    padding: 14px 24px !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    font-family: 'Open Sans', sans-serif !important;
    color: #ffffff !important;
    background: linear-gradient(135deg, #10264a 0%, #1a3a6b 100%) !important;
    border: none !important;
    border-radius: 10px !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 12px rgba(16, 38, 74, 0.25) !important;
    margin-top: 8px !important;
}

/* Button Hover State */
.connect-view-form button[type="submit"]:hover,
[class*="ConnectAction_"] button:hover {
    background: linear-gradient(135deg, #1a3a6b 0%, #10264a 100%) !important;
    box-shadow: 0 6px 16px rgba(16, 38, 74, 0.35) !important;
    transform: translateY(-2px) !important;
}

/* Button Active/Pressed State */
.connect-view-form button[type="submit"]:active,
[class*="ConnectAction_"] button:active {
    transform: translateY(0) !important;
    box-shadow: 0 2px 8px rgba(16, 38, 74, 0.3) !important;
}

/* Button Disabled State */
.connect-view-form button[type="submit"]:disabled,
[class*="ConnectAction_"] button:disabled {
    background: #9ca3af !important;
    cursor: not-allowed !important;
    box-shadow: none !important;
    opacity: 0.6 !important;
}

/* Checkbox and Radio Inputs */
.connect-view-form input[type="checkbox"],
.connect-view-form input[type="radio"],
[class*="FormInput_"] input[type="checkbox"],
[class*="FormInput_"] input[type="radio"] {
    width: auto !important;
    margin-right: 8px !important;
    cursor: pointer !important;
}

/* Help Text / Field Hints */
.connect-view-form .help-text,
.connect-view-form [class*="hint"],
[class*="HelpText_"] {
    color: #6b7280 !important;
    font-size: 0.85rem !important;
    margin-top: 4px !important;
    font-style: italic !important;
}

/* Form Sections/Fieldsets */
.connect-view-form fieldset,
[class*="FormSection_"] {
    border: none !important;
    padding: 0 !important;
    margin: 20px 0 !important;
}

.connect-view-form legend {
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    color: #10264a !important;
    margin-bottom: 12px !important;
}

/* Placeholder Text */
.connect-view-form input::placeholder,
.connect-view-form textarea::placeholder {
    color: #9ca3af !important;
    opacity: 1 !important;
}

/* Mobile Responsiveness */
@media (max-width: 640px) {
    .connect-view-form,
    [class*="Form_"] {
        padding: 18px !important;
    }

    .connect-view-form h2,
    [class*="Header_"] h2 {
        font-size: 1.3rem !important;
    }

    .connect-view-form button[type="submit"],
    [class*="ConnectAction_"] button {
        padding: 12px 20px !important;
        font-size: 0.95rem !important;
    }
}

/* Loading State */
.connect-view-form.loading,
[class*="Form_"][class*="loading"] {
    opacity: 0.6 !important;
    pointer-events: none !important;
}

/* Success State */
.connect-view-form.success,
[class*="Form_"][class*="success"] {
    border: 2px solid #10b981 !important;
    background: #f0fdf4 !important;
}

/* Professional spacing and alignment */
.connect-view-form > * + * {
    margin-top: 16px !important;
}
</style>"""


def get_enhancements() -> list:
    """
    Get all enhancements for the current view mode.

    Returns:
        List of enhancement strings (scripts and styles) to inject.
    """
    enhancements = [
        custom_styles_script(),
        form_styling_css()  # Add professional form styling
    ]

    if IS_KIOSK:
        enhancements.extend([
            kiosk_css(),
            auto_open_script(),
            auto_reset_script()
        ])
    elif IS_MOBILE:
        enhancements.extend([
            mobile_css(),
            auto_open_script()
        ])

    return enhancements
