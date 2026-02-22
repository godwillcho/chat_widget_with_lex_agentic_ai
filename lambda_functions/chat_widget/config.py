"""
config.py — Centralized configuration from environment variables.
──────────────────────────────────────────────────────────────────
VIEW_MODE controls the layout:
  standard → full website with floating chat widget (default)
  kiosk    → full-screen kiosk, large centered widget, auto-open/reset
"""

import os
import html as html_mod


def _env(key: str, default: str = "") -> str:
    return os.environ.get(key, default)


# ── Mode ──
_legacy = _env("KIOSK_MODE", "false").lower() in ("true", "1", "yes")
VIEW_MODE = _env("VIEW_MODE", "kiosk" if _legacy else "standard").lower()
if VIEW_MODE not in ("standard", "kiosk"):
    VIEW_MODE = "standard"

# ── Branding ──
COMPANY_NAME      = _env("COMPANY_NAME", "Trident United Way")
COMPANY_NAME_HTML = html_mod.escape(COMPANY_NAME)
COMPANY_NAME_JS   = COMPANY_NAME.replace("\\", "\\\\").replace("'", "\\'")

# ── Amazon Connect ──
CONNECT_URL  = _env("CONNECT_URL", "https://nextgencxsolutions.my.connect.aws")
WIDGET_ID    = _env("WIDGET_ID", "497c0ff9-3611-45dc-a56d-21aa65f76969")
SNIPPET_ID   = _env("SNIPPET_ID", "")

# ── Theme colors ──
COLOR_NAVY      = _env("COLOR_NAVY", "#10264a")
COLOR_BLUE      = _env("COLOR_BLUE", "#1a3a6b")
COLOR_GOLD      = _env("COLOR_GOLD", "#f5a623")
COLOR_GOLD_LT   = _env("COLOR_GOLD_LIGHT", "#fbbf24")

# ── Widget display — sizes adapt to mode ──
WIDGET_HEADER    = _env("WIDGET_HEADER", "Trident United Way Stability360")
WIDGET_BOT_NAME  = _env("WIDGET_BOT_NAME", "Stability360")

# ── Page display text ──
SERVICE_NAME       = _env("SERVICE_NAME", "Stability360")
SERVICE_TAGLINE    = _env("SERVICE_TAGLINE", "Your connection to care")
COMPANY_TAGLINE    = _env("COMPANY_TAGLINE", "Serving Berkeley, Charleston & Dorchester Counties")
FOOTER_TAGLINE     = _env("FOOTER_TAGLINE", "Uniting the Tri-County to uplift families out of poverty.")

# HTML-safe versions
WIDGET_HEADER_HTML   = html_mod.escape(WIDGET_HEADER)
SERVICE_NAME_HTML    = html_mod.escape(SERVICE_NAME)
SERVICE_TAGLINE_HTML = html_mod.escape(SERVICE_TAGLINE)
COMPANY_TAGLINE_HTML = html_mod.escape(COMPANY_TAGLINE)
FOOTER_TAGLINE_HTML  = html_mod.escape(FOOTER_TAGLINE)

_DEFAULTS = {
    "standard": {"w": "420px", "h": "640px", "font": "14px"},
    "kiosk":    {"w": "780px", "h": "920px", "font": "18px"},
}
_d = _DEFAULTS[VIEW_MODE]

WIDGET_WIDTH     = _env("WIDGET_WIDTH",  _d["w"])
WIDGET_HEIGHT    = _env("WIDGET_HEIGHT", _d["h"])
WIDGET_FONT_SIZE = _d["font"]

IS_KIOSK  = VIEW_MODE == "kiosk"
IS_STD    = VIEW_MODE == "standard"
