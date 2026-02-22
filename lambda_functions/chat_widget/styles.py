"""
styles.py — CSS stylesheet, switches between standard / kiosk / mobile.
Colors are pulled from config.py so they can be changed in environments.py.
"""

from config import VIEW_MODE, COLOR_NAVY, COLOR_BLUE, COLOR_GOLD, COLOR_GOLD_LT


def render_styles() -> str:
    return {"standard": _standard, "kiosk": _kiosk}[VIEW_MODE]()


# ═══════════════════════════════════════════════════════
#  KIOSK STYLES
# ═══════════════════════════════════════════════════════

def _kiosk() -> str:
    root = f"""<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Open+Sans:wght@400;600;700;800&display=swap');

    :root {{
        --navy: {COLOR_NAVY}; --navy-deep: #0a1a35; --blue: {COLOR_BLUE};
        --gold: {COLOR_GOLD}; --gold-light: {COLOR_GOLD_LT};
    }}"""

    body = """

    *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

    html, body {
        height: 100%; overflow: hidden;
        font-family: 'Open Sans', -apple-system, sans-serif;
        background: var(--navy-deep); color: #fff;
    }

    .kiosk-wrapper {
        display: grid; grid-template-columns: 380px 1fr;
        height: 100vh; overflow: hidden;
    }

    .brand-panel {
        background: linear-gradient(195deg, var(--navy) 0%, var(--navy-deep) 100%);
        padding: 2.5rem 2rem;
        display: flex; flex-direction: column; justify-content: space-between;
        position: relative; overflow: hidden;
    }
    .brand-panel::before {
        content: ''; position: absolute; top: -100px; right: -100px;
        width: 350px; height: 350px;
        background: radial-gradient(circle, rgba(245,166,35,0.08) 0%, transparent 70%);
        border-radius: 50%;
    }
    .brand-panel::after {
        content: ''; position: absolute; bottom: -60px; left: -60px;
        width: 200px; height: 200px;
        background: radial-gradient(circle, rgba(26,58,107,0.4) 0%, transparent 70%);
        border-radius: 50%;
    }

    .brand-top { position: relative; z-index: 2; }
    .brand-org {
        font-family: 'DM Serif Display', serif;
        font-size: 1.6rem; color: #fff; line-height: 1.25; margin-bottom: 0.35rem;
    }
    .brand-tagline {
        font-size: 0.72rem; color: rgba(255,255,255,0.5);
        text-transform: uppercase; letter-spacing: 0.12em; font-weight: 700;
        margin-bottom: 2.5rem;
    }
    .brand-211 {
        font-family: 'DM Serif Display', serif;
        font-size: 2.8rem; color: var(--gold); line-height: 1; margin-bottom: 0.4rem;
    }
    .brand-subtitle { font-size: 1.15rem; font-weight: 700; color: rgba(255,255,255,0.9); margin-bottom: 0.3rem; }
    .brand-desc { font-size: 0.88rem; line-height: 1.7; color: rgba(255,255,255,0.55); margin-bottom: 2rem; }

    .brand-tags { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 2rem; }
    .brand-tag {
        background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);
        padding: 0.4rem 0.9rem; border-radius: 100px;
        font-size: 0.7rem; font-weight: 700; text-transform: uppercase;
        letter-spacing: 0.06em; color: rgba(255,255,255,0.7);
    }

    .reach-section { position: relative; z-index: 2; margin-bottom: 1.5rem; }
    .reach-label {
        font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.14em;
        color: var(--gold); font-weight: 800; margin-bottom: 0.75rem;
    }
    .reach-item {
        display: flex; align-items: center; gap: 0.85rem;
        padding: 0.7rem 0; border-top: 1px solid rgba(255,255,255,0.06);
    }
    .reach-item:last-child { border-bottom: 1px solid rgba(255,255,255,0.06); }
    .reach-num {
        width: 32px; height: 32px; background: rgba(245,166,35,0.12); color: var(--gold);
        border-radius: 8px; font-size: 0.75rem; font-weight: 800;
        display: flex; align-items: center; justify-content: center; flex-shrink: 0;
    }
    .reach-text strong { display: block; font-size: 0.85rem; color: #fff; font-weight: 700; }
    .reach-text span { font-size: 0.75rem; color: rgba(255,255,255,0.45); }

    .brand-bottom { position: relative; z-index: 2; }
    .brand-address {
        font-size: 0.72rem; line-height: 1.7; color: rgba(255,255,255,0.3);
        border-top: 1px solid rgba(255,255,255,0.06); padding-top: 1rem;
    }
    .brand-address strong { color: rgba(255,255,255,0.5); font-weight: 700; }

    .widget-area {
        position: relative; display: flex; align-items: center; justify-content: center;
        background: linear-gradient(180deg, hsl(218,30%,14%) 0%, hsl(218,35%,10%) 100%);
        overflow: hidden;
    }
    .widget-area::before {
        content: ''; position: absolute; inset: 0;
        background:
            radial-gradient(ellipse at 30% 20%, rgba(245,166,35,0.04) 0%, transparent 60%),
            radial-gradient(ellipse at 70% 80%, rgba(26,58,107,0.15) 0%, transparent 60%);
    }
    .widget-glow {
        position: absolute; width: 700px; height: 700px; border-radius: 50%;
        background: radial-gradient(circle, rgba(245,166,35,0.06) 0%, transparent 70%);
        animation: pulse-glow 6s ease-in-out infinite alternate;
    }
    @keyframes pulse-glow {
        0%   { transform: scale(0.9); opacity: 0.5; }
        100% { transform: scale(1.1); opacity: 1; }
    }

    .widget-hint {
        position: fixed; bottom: 18px; left: 50%; transform: translateX(-30%); z-index: 200;
    }
    .hint-text {
        font-size: 0.8rem; color: rgba(255,255,255,0.35); font-weight: 600; letter-spacing: 0.04em;
    }

    @media (max-width: 900px) {
        .kiosk-wrapper { grid-template-columns: 1fr; grid-template-rows: auto 1fr; }
        .brand-panel { padding: 1.25rem 1.5rem; flex-direction: row; align-items: center; gap: 1.5rem; }
        .brand-211 { font-size: 2rem; }
        .brand-desc, .reach-section, .brand-bottom { display: none; }
        .brand-tags { margin-bottom: 0; }
        #amazon-connect-widget-frame { width: min(700px, 94vw) !important; height: calc(100vh - 120px) !important; }
    }
    @media (max-width: 600px) {
        .brand-tags { display: none; }
        .brand-org { font-size: 1.2rem; }
        .brand-211 { font-size: 1.8rem; margin-bottom: 0; }
        #amazon-connect-widget-frame { width: 98vw !important; height: calc(100vh - 90px) !important; border-radius: 12px !important; }
    }
</style>"""

    return root + body


# ═══════════════════════════════════════════════════════
#  STANDARD STYLES
# ═══════════════════════════════════════════════════════

def _standard() -> str:
    root = f"""<style>
    :root {{
        --uw-navy: {COLOR_NAVY}; --uw-blue: {COLOR_BLUE}; --uw-blue-light: #2563eb;
        --uw-gold: {COLOR_GOLD}; --uw-gold-light: {COLOR_GOLD_LT};
        --uw-red: #d32f2f; --uw-green: #16a34a;
        --warm-white: #fafaf8;
        --gray-50: #f9fafb; --gray-100: #f3f4f6; --gray-200: #e5e7eb;
        --gray-300: #d1d5db; --gray-500: #6b7280; --gray-600: #4b5563;
        --gray-700: #374151; --gray-800: #1f2937;
    }}"""

    body = """
    *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
        font-family: 'Open Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        background: var(--warm-white); color: var(--gray-700); min-height: 100vh;
        line-height: 1.6;
    }

    /* ── Utility bar ── */
    .util-bar {
        background: var(--uw-navy); color: rgba(255,255,255,0.7);
        font-size: 0.75rem; padding: 0.4rem 2rem;
        display: flex; justify-content: flex-end; gap: 1.5rem; align-items: center;
    }
    .util-bar a { color: rgba(255,255,255,0.85); text-decoration: none; font-weight: 600; transition: color 0.25s; }
    .util-bar a:hover { color: var(--uw-gold); }

    /* ── Navigation ── */
    nav {
        background: rgba(255,255,255,0.97); padding: 0.75rem 2rem;
        display: flex; align-items: center; justify-content: space-between;
        border-bottom: 3px solid var(--uw-gold);
        box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 16px rgba(0,0,0,0.04);
        position: sticky; top: 0; z-index: 50;
        backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
    }
    .nav-brand { display: flex; align-items: center; gap: 0.85rem; text-decoration: none; }
    .nav-logo-text { display: flex; flex-direction: column; }
    .nav-logo-text .org-name { font-family: 'Merriweather', serif; font-size: 1.2rem; font-weight: 900; color: var(--uw-navy); letter-spacing: -0.02em; line-height: 1.2; }
    .nav-logo-text .org-tag { font-size: 0.65rem; color: var(--gray-500); font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; }
    .nav-links { display: flex; gap: 1.5rem; align-items: center; }
    .nav-links a { color: var(--gray-700); text-decoration: none; font-size: 0.85rem; font-weight: 600; padding: 0.4rem 0; transition: all 0.25s ease; border-bottom: 2px solid transparent; }
    .nav-links a:hover { color: var(--uw-navy); border-bottom-color: var(--uw-gold); }
    .nav-links .active { color: var(--uw-navy); border-bottom-color: var(--uw-gold); }
    .btn-donate { background: var(--uw-gold); color: var(--uw-navy) !important; padding: 0.5rem 1.25rem; border-radius: 8px; font-weight: 700; font-size: 0.85rem; border-bottom: none !important; transition: all 0.25s ease; }
    .btn-donate:hover { background: var(--uw-gold-light); transform: translateY(-1px); box-shadow: 0 4px 12px rgba(245,166,35,0.3); }

    /* ── Breadcrumb ── */
    .breadcrumb { max-width: 1140px; margin: 0 auto; padding: 1rem 2rem 0; font-size: 0.8rem; color: var(--gray-500); }
    .breadcrumb a { color: var(--uw-blue-light); text-decoration: none; transition: color 0.2s; }
    .breadcrumb a:hover { color: var(--uw-navy); }

    /* ── Hero banner ── */
    .hero-banner { position: relative; background: linear-gradient(145deg, var(--uw-navy) 0%, var(--uw-blue) 55%, #234b82 100%); color: #fff; overflow: hidden; }
    .hero-banner::before { content: ''; position: absolute; left: -120px; bottom: -120px; width: 350px; height: 350px; background: radial-gradient(circle, rgba(245,166,35,0.08) 0%, transparent 70%); border-radius: 50%; }
    .hero-banner::after { content: ''; position: absolute; right: -80px; top: -80px; width: 400px; height: 400px; background: radial-gradient(circle, rgba(245,166,35,0.12) 0%, transparent 70%); border-radius: 50%; }
    .hero-inner { max-width: 1140px; margin: 0 auto; padding: 4rem 2rem; position: relative; z-index: 2; display: grid; grid-template-columns: 1fr 1fr; gap: 3rem; align-items: center; }
    .hero-banner h1 { font-family: 'Merriweather', serif; font-size: 2.5rem; font-weight: 900; line-height: 1.2; margin-bottom: 1rem; }
    .hero-banner h1 span { color: var(--uw-gold); }
    .hero-banner .subtitle { font-size: 1.15rem; line-height: 1.7; opacity: 0.9; max-width: 500px; }
    .hero-right { display: flex; justify-content: center; }
    .hero-211 { background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.12); border-radius: 24px; padding: 2.5rem; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); text-align: center; min-width: 280px; box-shadow: 0 8px 32px rgba(0,0,0,0.15); }
    .hero-211 .big-211 { font-family: 'Merriweather', serif; font-size: 2.5rem; font-weight: 900; color: var(--uw-gold); line-height: 1; margin-bottom: 0.5rem; }
    .hero-211 .hero-tags { display: flex; gap: 0.5rem; justify-content: center; flex-wrap: wrap; margin-top: 1rem; }
    .hero-tag { background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.18); padding: 0.3rem 0.85rem; border-radius: 100px; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; }

    /* ── Content area ── */
    .content { max-width: 1140px; margin: 0 auto; padding: 3rem 2rem; }
    .content h2 { font-family: 'Merriweather', serif; font-size: 1.75rem; font-weight: 900; color: var(--uw-navy); margin-bottom: 1.25rem; }

    /* ── Ways cards ── */
    .ways-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.25rem; margin-bottom: 3rem; }
    .way-card { background: #fff; border: 1px solid rgba(0,0,0,0.06); border-radius: 16px; padding: 2rem; text-align: center; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); box-shadow: 0 1px 3px rgba(0,0,0,0.03), 0 4px 12px rgba(0,0,0,0.04); }
    .way-card:hover { box-shadow: 0 12px 32px rgba(16,38,74,0.1); transform: translateY(-4px); border-color: var(--uw-gold); }
    .way-num { width: 48px; height: 48px; background: var(--uw-navy); color: var(--uw-gold); border-radius: 50%; font-weight: 800; font-size: 1.1rem; display: inline-flex; align-items: center; justify-content: center; margin-bottom: 1rem; }
    .way-card h3 { font-size: 1rem; font-weight: 700; color: var(--uw-navy); margin-bottom: 0.35rem; }
    .way-card .way-action { font-size: 1.35rem; font-weight: 800; color: var(--uw-blue-light); margin-bottom: 0.35rem; }
    .way-card p { font-size: 0.85rem; color: var(--gray-500); line-height: 1.5; }

    /* ── About section ── */
    .about-section { background: linear-gradient(135deg, #f8faff, #f0fdf4); border: 1px solid rgba(0,0,0,0.04); border-left: 4px solid var(--uw-navy); border-radius: 16px; padding: 2rem 2.5rem; margin-bottom: 2.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.02), 0 4px 12px rgba(0,0,0,0.03); }
    .about-section h2 { margin-bottom: 0.75rem; }
    .about-section p { font-size: 1rem; line-height: 1.8; color: var(--gray-600); }

    /* ── Way icon (service categories) ── */
    .way-icon { font-size: 2.5rem; margin-bottom: 0.75rem; display: block; }

    /* ── How it works ── */
    .know-section { background: #fff; border: none; border-radius: 16px; padding: 2rem 2.5rem; margin-bottom: 2.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.03), 0 4px 12px rgba(0,0,0,0.04); }
    .know-section h3 { font-family: 'Merriweather', serif; font-size: 1.2rem; font-weight: 700; color: var(--uw-navy); margin-bottom: 1rem; }
    .know-list { list-style: none; display: flex; flex-direction: column; gap: 0.85rem; }
    .know-list li { display: flex; align-items: flex-start; gap: 0.75rem; font-size: 0.95rem; line-height: 1.65; color: var(--gray-600); }
    .know-list .check { flex-shrink: 0; width: 22px; height: 22px; background: rgba(22,163,74,0.1); color: var(--uw-green); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-top: 2px; }

    /* ── ALICE section ── */
    .alice-section { background: #fffbeb; border: 1px solid #fde68a; border-radius: 16px; padding: 2rem 2.5rem; margin-bottom: 2.5rem; display: flex; gap: 1.5rem; align-items: flex-start; box-shadow: 0 1px 3px rgba(0,0,0,0.02), 0 2px 8px rgba(0,0,0,0.03); }
    .alice-badge { flex-shrink: 0; background: var(--uw-gold); color: var(--uw-navy); font-weight: 800; font-size: 0.85rem; padding: 0.6rem 1rem; border-radius: 8px; box-shadow: 0 2px 6px rgba(245,166,35,0.3); }
    .alice-body h3 { font-family: 'Merriweather', serif; font-size: 1.15rem; font-weight: 700; color: var(--uw-navy); margin-bottom: 0.5rem; }
    .alice-body p { font-size: 0.95rem; line-height: 1.7; color: var(--gray-600); margin-bottom: 0.6rem; }
    .alice-body p:last-child { margin-bottom: 0; }

    /* ── Resource centers ── */
    .centers-section { background: #fff; border: none; border-radius: 16px; padding: 2rem 2.5rem; margin-bottom: 2.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.03), 0 4px 12px rgba(0,0,0,0.04); }
    .centers-section h3 { font-family: 'Merriweather', serif; font-size: 1.2rem; font-weight: 700; color: var(--uw-navy); margin-bottom: 0.6rem; }
    .centers-section > p { font-size: 0.95rem; line-height: 1.7; color: var(--gray-600); margin-bottom: 1.25rem; }
    .centers-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }
    .center-card { background: var(--gray-50); border: 1px solid rgba(0,0,0,0.04); border-radius: 12px; padding: 1.25rem; text-align: center; transition: all 0.25s ease; }
    .center-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.06); transform: translateY(-2px); }
    .center-card strong { display: block; font-size: 0.9rem; color: var(--uw-navy); margin-bottom: 0.25rem; }
    .center-card span { font-size: 0.8rem; color: var(--gray-500); }

    /* ── CTA banner ── */
    .cta-banner { background: linear-gradient(135deg, var(--uw-gold), #f7c948); border-radius: 16px; padding: 2rem 2.5rem; display: flex; align-items: center; justify-content: space-between; gap: 2rem; margin-bottom: 2rem; box-shadow: 0 4px 24px rgba(245,166,35,0.2); }
    .cta-banner h3 { font-family: 'Merriweather', serif; font-size: 1.25rem; font-weight: 900; color: var(--uw-navy); margin-bottom: 0.25rem; }
    .cta-banner p { color: var(--uw-blue); font-size: 0.9rem; font-weight: 500; }
    .cta-btn { background: var(--uw-navy); color: #fff; padding: 0.75rem 2rem; border-radius: 10px; text-decoration: none; font-weight: 700; font-size: 0.95rem; white-space: nowrap; transition: all 0.25s ease; box-shadow: 0 2px 8px rgba(16,38,74,0.2); }
    .cta-btn:hover { background: #0d1f3d; transform: translateY(-1px); box-shadow: 0 4px 16px rgba(16,38,74,0.3); }

    /* ── Footer ── */
    footer { background: var(--uw-navy); color: rgba(255,255,255,0.6); padding: 3rem 2rem 2rem; }
    .footer-inner { max-width: 1140px; margin: 0 auto; display: grid; grid-template-columns: 1.5fr 1fr 1fr; gap: 2rem; }
    .footer-brand { font-family: 'Merriweather', serif; font-size: 1.1rem; font-weight: 700; color: #fff; margin-bottom: 0.5rem; }
    .footer-tagline { font-size: 0.85rem; line-height: 1.6; margin-bottom: 1rem; }
    .footer-addr { font-size: 0.8rem; line-height: 1.7; }
    footer h4 { color: var(--uw-gold); font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.75rem; }
    footer ul { list-style: none; }
    footer ul li { margin-bottom: 0.4rem; }
    footer ul a { color: rgba(255,255,255,0.7); text-decoration: none; font-size: 0.85rem; transition: color 0.25s; }
    footer ul a:hover { color: var(--uw-gold); }
    .footer-bottom { max-width: 1140px; margin: 1.5rem auto 0; padding-top: 1.5rem; border-top: 1px solid rgba(255,255,255,0.1); font-size: 0.75rem; text-align: center; }

    /* ── Responsive ── */
    @media (max-width: 900px) {
        .hero-inner { grid-template-columns: 1fr; text-align: center; }
        .hero-banner .subtitle { margin: 0 auto; }
        .ways-grid { grid-template-columns: repeat(2, 1fr); }
        .cta-banner { flex-direction: column; text-align: center; }
        .footer-inner { grid-template-columns: 1fr; text-align: center; }
        .nav-links { display: none; }
        .hero-banner h1 { font-size: 2rem; }
        .chat-callout { flex-direction: column; }
        .alice-section { flex-direction: column; }
        .centers-grid { grid-template-columns: 1fr; }
    }
</style>"""

    return root + body
