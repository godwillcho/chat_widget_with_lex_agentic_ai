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
    VIEW_MODE, IS_KIOSK, IS_STD,
    COLOR_NAVY,
    WIDGET_WIDTH, WIDGET_HEIGHT, WIDGET_FONT_SIZE,
    COMPANY_NAME_JS,
    WIDGET_HEADER_HTML,
)


def custom_styles_script() -> str:
    """Generate custom styles for the Amazon Connect widget."""
    fh = "90px" if IS_KIOSK else "70px"
    hh = "80px" if IS_KIOSK else "64px"
    lh = "48px" if IS_KIOSK else "40px"

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
            agentMessageTextColor: '#1f2937', systemMessageTextColor: '#4b5563',
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


</script>
<style>
/* Bold text throughout the widget */
#amazon-connect-widget-frame {{
    font-weight: 600 !important;
}}

/* Bold message text */
#amazon-connect-widget-frame [class*="Message"],
#amazon-connect-widget-frame [class*="message"],
#amazon-connect-widget-frame [class*="ChatMessage"],
#amazon-connect-widget-frame .message-content,
#amazon-connect-widget-frame [class*="transcript"] {{
    font-weight: 600 !important;
}}

/* Bold participant names */
#amazon-connect-widget-frame [class*="participant"],
#amazon-connect-widget-frame [class*="ParticipantName"],
#amazon-connect-widget-frame [class*="displayName"] {{
    font-weight: 700 !important;
}}

/* Bold header */
#amazon-connect-widget-frame [class*="Header"],
#amazon-connect-widget-frame header {{
    font-weight: 700 !important;
}}

/* Bold buttons */
#amazon-connect-widget-frame button {{
    font-weight: 600 !important;
}}

/* Red color for consent question and important messages */
#amazon-connect-widget-frame [class*="InteractiveMessage"] [class*="title"],
#amazon-connect-widget-frame [class*="interactive"] [class*="title"],
#amazon-connect-widget-frame [class*="QuickReply"] [class*="title"],
#amazon-connect-widget-frame [data-testid*="interactive"] [class*="title"] {{
    color: #dc2626 !important;
}}
</style>"""


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


def kiosk_landing_page() -> str:
    """Landing page HTML and CSS for kiosk mode."""
    return """
<style>
    /* Kiosk Landing Page */
    #kiosk-landing {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        z-index: 99999;
        display: flex;
        opacity: 1;
        transition: opacity 0.5s ease;
    }

    #kiosk-landing.hidden {
        opacity: 0;
        pointer-events: none;
    }

    /* Left Side - Animated Visual Area */
    .kiosk-visual-area {
        flex: 1;
        position: relative;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* Animated Service Cards */
    .service-card {
        position: absolute;
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        padding: 30px;
        color: white;
        text-align: center;
        animation: float 12s infinite ease-in-out;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.3s ease, background 0.3s ease;
    }

    .service-card:hover {
        background: rgba(255, 255, 255, 0.25);
        transform: scale(1.05) !important;
    }

    .service-icon {
        font-size: 3rem;
        margin-bottom: 15px;
        display: block;
    }

    .service-title {
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .service-desc {
        font-size: 0.85rem;
        opacity: 0.9;
        line-height: 1.4;
    }

    .card-1 {
        width: 280px;
        top: 8%;
        left: 8%;
        animation-delay: 0s;
    }

    .card-2 {
        width: 260px;
        top: 55%;
        left: 12%;
        animation-delay: 4s;
    }

    .card-3 {
        width: 240px;
        top: 28%;
        left: 58%;
        animation-delay: 2s;
    }

    .card-4 {
        width: 270px;
        top: 68%;
        left: 52%;
        animation-delay: 6s;
    }

    @keyframes float {
        0%, 100% {
            transform: translate(0, 0) scale(1);
        }
        25% {
            transform: translate(30px, -30px) scale(1.1);
        }
        50% {
            transform: translate(-20px, 20px) scale(0.9);
        }
        75% {
            transform: translate(20px, 30px) scale(1.05);
        }
    }

    /* Decorative Animated Bubbles */
    .bubble {
        position: absolute;
        border-radius: 50%;
        opacity: 0.6;
        animation: bubbleFloat 8s infinite ease-in-out;
        pointer-events: none;
    }

    @keyframes bubbleFloat {
        0%, 100% {
            transform: translateY(0) translateX(0) scale(1);
            opacity: 0.6;
        }
        33% {
            transform: translateY(-40px) translateX(25px) scale(1.15);
            opacity: 0.8;
        }
        66% {
            transform: translateY(30px) translateX(-20px) scale(0.9);
            opacity: 0.5;
        }
    }

    /* Individual bubble styles with different colors */
    .bubble-1 {
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #ff6b6b, #ee5a6f);
        top: 15%;
        left: 25%;
        animation-delay: 0s;
        animation-duration: 7s;
    }

    .bubble-2 {
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, #4ecdc4, #44a08d);
        top: 45%;
        left: 35%;
        animation-delay: 2s;
        animation-duration: 9s;
    }

    .bubble-3 {
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, #f7b731, #f79f1f);
        top: 75%;
        left: 15%;
        animation-delay: 4s;
        animation-duration: 8s;
    }

    .bubble-4 {
        width: 70px;
        height: 70px;
        background: linear-gradient(135deg, #5f27cd, #341f97);
        top: 25%;
        left: 70%;
        animation-delay: 1s;
        animation-duration: 7.5s;
    }

    .bubble-5 {
        width: 55px;
        height: 55px;
        background: linear-gradient(135deg, #00d2ff, #3a7bd5);
        top: 60%;
        left: 75%;
        animation-delay: 3s;
        animation-duration: 8.5s;
    }

    .bubble-6 {
        width: 65px;
        height: 65px;
        background: linear-gradient(135deg, #ff9ff3, #feca57);
        top: 85%;
        left: 65%;
        animation-delay: 5s;
        animation-duration: 9.5s;
    }

    .bubble-7 {
        width: 45px;
        height: 45px;
        background: linear-gradient(135deg, #54a0ff, #5f27cd);
        top: 10%;
        left: 45%;
        animation-delay: 2.5s;
        animation-duration: 6.5s;
    }

    .bubble-8 {
        width: 75px;
        height: 75px;
        background: linear-gradient(135deg, #48dbfb, #0abde3);
        top: 40%;
        left: 8%;
        animation-delay: 4.5s;
        animation-duration: 10s;
    }

    .bubble-9 {
        width: 58px;
        height: 58px;
        background: linear-gradient(135deg, #ff6348, #ff4757);
        top: 50%;
        left: 85%;
        animation-delay: 1.5s;
        animation-duration: 7.5s;
    }

    .bubble-10 {
        width: 52px;
        height: 52px;
        background: linear-gradient(135deg, #1dd1a1, #10ac84);
        top: 90%;
        left: 40%;
        animation-delay: 3.5s;
        animation-duration: 8s;
    }

    /* Logo/Branding Area */
    .kiosk-branding {
        position: relative;
        z-index: 2;
        text-align: center;
        color: white;
        padding: 40px;
    }

    .kiosk-logo {
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 20px;
        text-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        font-family: 'Open Sans', -apple-system, sans-serif;
        line-height: 1.2;
    }

    .kiosk-tagline {
        font-size: 1.5rem;
        opacity: 0.9;
        font-weight: 300;
        letter-spacing: 1px;
    }

    /* Right Side - Button Area */
    .kiosk-button-area {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #10264a 0%, #1a3a6b 100%);
        position: relative;
    }

    /* Decorative Elements */
    .kiosk-button-area::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle at 50% 50%, rgba(255, 255, 255, 0.05) 0%, transparent 70%);
        pointer-events: none;
    }

    /* Start Button Container */
    .kiosk-start-container {
        position: relative;
        z-index: 2;
        text-align: center;
    }

    .kiosk-start-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 20px;
        font-family: 'Open Sans', sans-serif;
    }

    .kiosk-start-subtitle {
        color: rgba(255, 255, 255, 0.8);
        font-size: 1.2rem;
        margin-bottom: 50px;
        font-weight: 300;
    }

    /* Start Chat Button */
    #kiosk-start-button {
        background: linear-gradient(135deg, #f5a623 0%, #fbbf24 100%);
        color: #10264a;
        font-size: 1.5rem;
        font-weight: 700;
        padding: 30px 60px;
        border: none;
        border-radius: 60px;
        cursor: pointer;
        box-shadow: 0 10px 40px rgba(245, 166, 35, 0.4);
        transition: all 0.3s ease;
        font-family: 'Open Sans', sans-serif;
        text-transform: uppercase;
        letter-spacing: 2px;
        position: relative;
        overflow: hidden;
    }

    #kiosk-start-button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }

    #kiosk-start-button:hover::before {
        width: 300px;
        height: 300px;
    }

    #kiosk-start-button:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 50px rgba(245, 166, 35, 0.6);
    }

    #kiosk-start-button:active {
        transform: translateY(-2px);
    }

    .button-text {
        position: relative;
        z-index: 1;
    }

    /* Pulse animation for button */
    @keyframes pulse {
        0%, 100% {
            box-shadow: 0 10px 40px rgba(245, 166, 35, 0.4);
        }
        50% {
            box-shadow: 0 10px 40px rgba(245, 166, 35, 0.7);
        }
    }

    #kiosk-start-button {
        animation: pulse 2s infinite;
    }

    /* Helper text */
    .kiosk-help-text {
        margin-top: 40px;
        color: rgba(255, 255, 255, 0.6);
        font-size: 1rem;
        font-style: italic;
    }
</style>

<div id="kiosk-landing">
    <!-- Left Side - Animated Visual Area -->
    <div class="kiosk-visual-area">
        <!-- Decorative Animated Bubbles -->
        <div class="bubble bubble-1"></div>
        <div class="bubble bubble-2"></div>
        <div class="bubble bubble-3"></div>
        <div class="bubble bubble-4"></div>
        <div class="bubble bubble-5"></div>
        <div class="bubble bubble-6"></div>
        <div class="bubble bubble-7"></div>
        <div class="bubble bubble-8"></div>
        <div class="bubble bubble-9"></div>
        <div class="bubble bubble-10"></div>

        <!-- Service Card 1 - Food Assistance -->
        <div class="service-card card-1">
            <span class="service-icon">🍎</span>
            <div class="service-title">Food Assistance</div>
            <div class="service-desc">Find food banks, meal programs, and nutrition support</div>
        </div>

        <!-- Service Card 2 - Housing Support -->
        <div class="service-card card-2">
            <span class="service-icon">🏠</span>
            <div class="service-title">Housing Help</div>
            <div class="service-desc">Rental assistance, shelters, and housing resources</div>
        </div>

        <!-- Service Card 3 - Healthcare -->
        <div class="service-card card-3">
            <span class="service-icon">⚕️</span>
            <div class="service-title">Healthcare</div>
            <div class="service-desc">Medical clinics, mental health, and insurance help</div>
        </div>

        <!-- Service Card 4 - Utility Assistance -->
        <div class="service-card card-4">
            <span class="service-icon">💡</span>
            <div class="service-title">Utility Bills</div>
            <div class="service-desc">Help with electricity, water, and heating bills</div>
        </div>

        <div class="kiosk-branding">
            <div class="kiosk-logo">""" + WIDGET_HEADER_HTML + """</div>
            <div class="kiosk-tagline">We're here to help you</div>
        </div>
    </div>

    <!-- Right Side - Button Area -->
    <div class="kiosk-button-area">
        <div class="kiosk-start-container">
            <h1 class="kiosk-start-title">Welcome</h1>
            <p class="kiosk-start-subtitle">Get connected with our support team</p>
            <button id="kiosk-start-button">
                <span class="button-text">Start Chat</span>
            </button>
            <p class="kiosk-help-text">Touch the button above to begin</p>
        </div>
    </div>
</div>"""


def kiosk_start_button_script() -> str:
    """Script to handle kiosk start button click."""
    return """
<script>
(function() {
    var landing = document.getElementById('kiosk-landing');
    var startBtn = document.getElementById('kiosk-start-button');

    if (startBtn) {
        startBtn.addEventListener('click', function() {
            // Hide the landing page
            landing.classList.add('hidden');

            // Wait for animation, then open the widget
            setTimeout(function() {
                var openBtn = document.getElementById('amazon-connect-open-widget-button');
                if (openBtn) {
                    openBtn.click();
                } else {
                    // Retry if button not ready
                    function tryOpen() {
                        var btn = document.getElementById('amazon-connect-open-widget-button');
                        if (btn) {
                            btn.click();
                        } else {
                            setTimeout(tryOpen, 200);
                        }
                    }
                    tryOpen();
                }
            }, 500);
        });
    }
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


def form_styling_css() -> str:
    """Placeholder for form styling - currently disabled."""
    return ""


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
            kiosk_landing_page(),
            kiosk_css(),
            kiosk_start_button_script(),
            auto_reset_script()
        ])

    return enhancements
