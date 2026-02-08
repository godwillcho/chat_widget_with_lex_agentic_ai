"""
page.py — HTML page template, three modes: standard / kiosk / mobile.
─────────────────────────────────────────────────────────────────────
  standard → full 211 website with floating widget
  kiosk    → two-panel (branding left, centered widget right)
  mobile   → compact header bar + full-screen widget below
"""

from config import VIEW_MODE, IS_KIOSK, IS_MOBILE, IS_STD, COMPANY_NAME_HTML


# ═══════════════════════════════════════════════════════
#  SHARED
# ═══════════════════════════════════════════════════════

def _head(styles_css: str) -> str:
    scalable = ", user-scalable=no" if not IS_STD else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0{scalable}">
    <title>211 Helpline | {COMPANY_NAME_HTML}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Open+Sans:wght@400;500;600;700;800&family=Merriweather:wght@700;900&display=swap" rel="stylesheet">
    {styles_css}
</head>
<body>"""


def _closing() -> str:
    return "\n</body>\n</html>"


# ── Mode toggle ────────────────────────────────────────

_ICONS = {
    # monitor — switch to standard website
    "standard": (
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
        '<rect x="2" y="3" width="20" height="14" rx="2" ry="2"/>'
        '<line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>'
    ),
    # expand — switch to kiosk
    "kiosk": (
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
        '<polyline points="15 3 21 3 21 9"/><polyline points="9 21 3 21 3 15"/>'
        '<line x1="21" y1="3" x2="14" y2="10"/><line x1="3" y1="21" x2="10" y2="14"/></svg>'
    ),
    # phone — switch to mobile
    "mobile": (
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
        '<rect x="5" y="2" width="14" height="20" rx="2" ry="2"/>'
        '<line x1="12" y1="18" x2="12.01" y2="18"/></svg>'
    ),
}

_LABELS = {"standard": "Website", "kiosk": "Kiosk", "mobile": "Mobile"}


def _mode_toggle() -> str:
    """Floating pill with buttons to switch between all three modes."""
    dark_bg = not IS_STD  # kiosk + mobile have dark backgrounds

    buttons_html = ""
    for mode in ("standard", "kiosk", "mobile"):
        is_active = (mode == VIEW_MODE)
        buttons_html += f"""
            <a href="?mode={mode}" class="mt-btn {'mt-active' if is_active else ''}"
               aria-label="Switch to {_LABELS[mode]} view">
                {_ICONS[mode]}
                <span class="mt-label">{_LABELS[mode]}</span>
            </a>"""

    return f"""
    <style>
        .mode-switcher {{
            position: fixed;
            top: {'auto' if IS_MOBILE else '14px'};
            {'bottom: 8px;' if IS_MOBILE else ''}
            right: {'50%' if IS_MOBILE else '14px'};
            {'transform: translateX(50%);' if IS_MOBILE else ''}
            z-index: 9999;
            display: flex;
            gap: 2px;
            padding: 4px;
            border-radius: 50px;
            background: {'rgba(255,255,255,0.08)' if dark_bg else 'rgba(16,38,74,0.06)'};
            border: 1.5px solid {'rgba(245,166,35,0.3)' if dark_bg else 'rgba(16,38,74,0.12)'};
            backdrop-filter: blur(12px);
            box-shadow: 0 4px 20px {'rgba(0,0,0,0.3)' if dark_bg else 'rgba(0,0,0,0.08)'};
        }}
        .mt-btn {{
            display: flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.4rem 0.75rem;
            border-radius: 50px;
            text-decoration: none;
            font-family: 'Open Sans', sans-serif;
            font-size: 0.68rem;
            font-weight: 700;
            letter-spacing: 0.02em;
            color: {'rgba(255,255,255,0.5)' if dark_bg else 'rgba(16,38,74,0.45)'};
            transition: all 0.2s ease;
            white-space: nowrap;
        }}
        .mt-btn:hover {{
            color: {'#f5a623' if dark_bg else '#10264a'};
            background: {'rgba(245,166,35,0.1)' if dark_bg else 'rgba(16,38,74,0.06)'};
        }}
        .mt-btn.mt-active {{
            background: {'rgba(245,166,35,0.2)' if dark_bg else '#f5a623'};
            color: {'#f5a623' if dark_bg else '#10264a'};
            pointer-events: none;
        }}
        .mt-btn svg {{
            flex-shrink: 0;
            width: 16px; height: 16px;
        }}
        .mt-label {{
            line-height: 1;
        }}
    </style>
    <div class="mode-switcher">{buttons_html}
    </div>"""


# ═══════════════════════════════════════════════════════
#  MOBILE PAGE
# ═══════════════════════════════════════════════════════

def _mobile_page(styles_css: str, widget_script: str) -> str:
    cn = COMPANY_NAME_HTML
    return "".join([
        _head(styles_css),
        f"""
    <div class="mobile-header">
        <div class="mobile-brand">
            <div class="mobile-211">211</div>
            <div class="mobile-brand-text">
                <div class="mobile-org">{cn}</div>
                <div class="mobile-tagline">Free &bull; Confidential &bull; 24/7</div>
            </div>
        </div>
        <div class="mobile-tags">
            <span class="mobile-tag">180+ Languages</span>
        </div>
    </div>
    <div class="mobile-body"></div>""",
        _mode_toggle(),
        widget_script,
        _closing(),
    ])


# ═══════════════════════════════════════════════════════
#  KIOSK PAGE
# ═══════════════════════════════════════════════════════

def _kiosk_page(styles_css: str, widget_script: str) -> str:
    cn = COMPANY_NAME_HTML
    return "".join([
        _head(styles_css),
        f"""
    <div class="kiosk-wrapper">
        <div class="brand-panel">
            <div class="brand-top">
                <div class="brand-org">{cn}</div>
                <div class="brand-tagline">Serving Berkeley, Charleston &amp; Dorchester Counties</div>
                <div class="brand-211">2-1-1</div>
                <div class="brand-subtitle">Your connection to care</div>
                <div class="brand-desc">
                    Free, confidential support connecting you to essential
                    resources &mdash; housing, food, utilities, healthcare,
                    employment and more.
                </div>
                <div class="brand-tags">
                    <span class="brand-tag">Free</span>
                    <span class="brand-tag">Confidential</span>
                    <span class="brand-tag">24 / 7 / 365</span>
                    <span class="brand-tag">180+ Languages</span>
                </div>
                <div class="reach-section">
                    <div class="reach-label">Ways to Reach 211</div>
                    <div class="reach-item">
                        <div class="reach-num">1</div>
                        <div class="reach-text"><strong>Chat</strong><span>Use the form on this screen</span></div>
                    </div>
                    <div class="reach-item">
                        <div class="reach-num">2</div>
                        <div class="reach-text"><strong>Call 2-1-1</strong><span>Toll-free: 1-866-892-9211</span></div>
                    </div>
                    <div class="reach-item">
                        <div class="reach-num">3</div>
                        <div class="reach-text"><strong>Text &ldquo;Help&rdquo; to 211-211</strong><span>Get connected via text message</span></div>
                    </div>
                </div>
            </div>
            <div class="brand-bottom">
                <div class="brand-address">
                    <strong>{cn}</strong><br>6296 Rivers Ave, Ste 200<br>North Charleston, SC 29406<br>843.740.9000
                </div>
            </div>
        </div>
        <div class="widget-area"><div class="widget-glow"></div></div>
    </div>
    <div class="widget-hint">
        <div class="hint-text">Fill out the form above to start your chat session</div>
    </div>""",
        _mode_toggle(),
        widget_script,
        _closing(),
    ])


# ═══════════════════════════════════════════════════════
#  STANDARD (WEBSITE) PAGE
# ═══════════════════════════════════════════════════════

_CHECK = (
    '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor"'
    ' stroke-width="3" stroke-linecap="round" stroke-linejoin="round">'
    '<polyline points="20 6 9 17 4 12"/></svg>'
)
_ARROW = (
    '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"'
    ' stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
    '<line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>'
)


def _standard_page(styles_css: str, widget_script: str) -> str:
    cn = COMPANY_NAME_HTML
    return "".join([
        _head(styles_css),
        f"""
    <div class="util-bar">
        <span>Serving Berkeley, Charleston &amp; Dorchester Counties</span>
        <a href="#">Stay Connected</a><span>|</span><a href="tel:211">Call 2-1-1 Now</a>
    </div>
    <nav>
        <a href="#" class="nav-brand"><div class="nav-logo-text">
            <span class="org-name">{cn}</span>
            <span class="org-tag">Uniting the Tri-County to uplift families</span>
        </div></a>
        <div class="nav-links">
            <a href="#">Ways to Help</a><a href="#">Our Impact</a>
            <a href="#">About Us</a><a href="#" class="active">Get Help</a>
            <a href="#">Events</a><a href="#" class="btn-donate">Donate</a>
        </div>
    </nav>
    <div class="breadcrumb">
        <a href="#">Home</a> &rsaquo; <a href="#">Get Help</a> &rsaquo; <strong>211 Helpline</strong>
    </div>
    <section class="hero-banner"><div class="hero-inner">
        <div>
            <h1>Get connected to help.<br><span>Start here.</span></h1>
            <p class="subtitle">{cn}&rsquo;s 211 Helpline is a free, confidential, 24/7
                service that connects you to essential resources across Berkeley,
                Charleston and Dorchester counties.</p>
        </div>
        <div class="hero-right"><div class="hero-211">
            <div class="big-211">2-1-1</div>
            <div style="font-size:0.95rem;opacity:0.9;margin-bottom:0.25rem;">Your connection to care</div>
            <div class="hero-tags">
                <span class="hero-tag">Free</span><span class="hero-tag">Confidential</span>
                <span class="hero-tag">24/7/365</span><span class="hero-tag">180+ Languages</span>
            </div>
        </div></div>
    </div></section>

    <section class="content">
        <div class="chat-callout">
            <div class="chat-callout-icon">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
            </div>
            <div class="chat-callout-body">
                <h3>Chat with us &mdash; right from this page</h3>
                <p>Click the <strong>chat icon</strong> in the bottom-right corner to start a conversation with a Community Resource Specialist.</p>
                <ul>
                    <li>{_ARROW} <strong>Create a case</strong> so our team can follow up</li>
                    <li>{_ARROW} <strong>Get information about your needs</strong> &mdash; housing, food, utilities, healthcare</li>
                    <li>{_ARROW} <strong>Receive vetted referrals</strong> to local agencies</li>
                </ul>
                <p class="chat-note">Your information is confidential.</p>
            </div>
        </div>

        <h2>Three ways to reach 211:</h2>
        <div class="ways-grid">
            <div class="way-card"><div class="way-num">1</div><h3>Call</h3><div class="way-action">Dial 2-1-1</div><p>Talk to a specialist 24/7. Toll-free: 1-866-892-9211.</p></div>
            <div class="way-card"><div class="way-num">2</div><h3>Chat</h3><div class="way-action">Click the chat icon</div><p>Start a case right from this page.</p></div>
            <div class="way-card"><div class="way-num">3</div><h3>Text</h3><div class="way-action">&ldquo;Help&rdquo; to 211-211</div><p>Text anytime to get connected.</p></div>
        </div>

        <div class="know-section"><h3>What to expect</h3>
            <ul class="know-list">
                <li><span class="check">{_CHECK}</span><span>A trained Specialist will listen and identify resources.</span></li>
                <li><span class="check">{_CHECK}</span><span>Chat creates a <strong>case</strong> for follow-up.</span></li>
                <li><span class="check">{_CHECK}</span><span>Vetted agency referrals with details.</span></li>
                <li><span class="check">{_CHECK}</span><span><strong>Free and confidential</strong>. 180+ languages.</span></li>
            </ul>
        </div>

        <div class="alice-section">
            <div class="alice-badge">ALICE&reg;</div>
            <div class="alice-body">
                <h3>Are you an ALICE&reg; family?</h3>
                <p><strong>38%</strong> of Tri-County households are ALICE &mdash; <em>Asset Limited, Income Constrained, Employed</em>.</p>
                <p>{cn}&rsquo;s goal: uplift <strong>15,000 families</strong> by 2035. <strong>Start a chat</strong> to create a case.</p>
            </div>
        </div>

        <div class="centers-section"><h3>Resource Connection Centers</h3>
            <p>Last year: <strong>6,038 households</strong> served (<strong>12,251 individuals</strong>).</p>
            <div class="centers-grid">
                <div class="center-card"><strong>Berkeley County</strong><span>Grace Impact Development Center</span></div>
                <div class="center-card"><strong>Charleston County</strong><span>Coming soon</span></div>
                <div class="center-card"><strong>Dorchester County</strong><span>133 E 1st North St, Summerville</span></div>
            </div>
        </div>

        <div class="cta-banner"><div><h3>Ready to get connected?</h3><p>Use chat or call 2-1-1 anytime.</p></div><a href="tel:211" class="cta-btn">Call 2-1-1</a></div>
    </section>

    <footer><div class="footer-inner">
        <div>
            <div class="footer-brand">{cn}</div>
            <div class="footer-tagline">Uniting the Tri-County to uplift families out of poverty.</div>
            <div class="footer-addr">6296 Rivers Ave, Ste 200<br>North Charleston, SC 29406<br>843.740.9000</div>
        </div>
        <div><h4>Get Help</h4><ul><li><a href="#">211 Helpline</a></li><li><a href="#">Berkeley County</a></li><li><a href="#">Charleston County</a></li><li><a href="#">Dorchester County</a></li></ul></div>
        <div><h4>About Us</h4><ul><li><a href="#">Our Team</a></li><li><a href="#">ALICE&reg; Report</a></li><li><a href="#">Impact Report</a></li><li><a href="#">Contact Us</a></li></ul></div>
    </div><div class="footer-bottom">&copy; 2025 {cn}. All Rights Reserved.</div></footer>""",
        _mode_toggle(),
        widget_script,
        _closing(),
    ])


# ═══════════════════════════════════════════════════════
#  PUBLIC API
# ═══════════════════════════════════════════════════════

def render_page(styles_css: str, widget_script: str) -> str:
    return {
        "standard": _standard_page,
        "kiosk": _kiosk_page,
        "mobile": _mobile_page,
    }[VIEW_MODE](styles_css, widget_script)
