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


def get_enhancements() -> list:
    """
    Get all enhancements for the current view mode.

    Returns:
        List of enhancement strings (scripts and styles) to inject.
    """
    enhancements = [custom_styles_script()]

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
