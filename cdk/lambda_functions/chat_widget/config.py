"""
config.py — Centralized configuration from environment variables.
──────────────────────────────────────────────────────────────────
VIEW_MODE controls the layout:
  standard → full 211 website with floating chat widget (default)
  kiosk    → full-screen kiosk, large centered widget, auto-open/reset
  mobile   → phone-optimized, compact header, full-width widget, auto-open
"""

import os
import html as html_mod


def _env(key: str, default: str = "") -> str:
    return os.environ.get(key, default)


# ── Mode ──
_legacy = _env("KIOSK_MODE", "false").lower() in ("true", "1", "yes")
VIEW_MODE = _env("VIEW_MODE", "kiosk" if _legacy else "standard").lower()
if VIEW_MODE not in ("standard", "kiosk", "mobile"):
    VIEW_MODE = "standard"

# ── Branding ──
COMPANY_NAME      = _env("COMPANY_NAME", "Trident United Way")
COMPANY_NAME_HTML = html_mod.escape(COMPANY_NAME)
COMPANY_NAME_JS   = COMPANY_NAME.replace("\\", "\\\\").replace("'", "\\'")

# ── Amazon Connect ──
CONNECT_URL  = _env("CONNECT_URL", "https://nextgencxsolutions.my.connect.aws")
WIDGET_ID    = _env("WIDGET_ID", "cba73f0d-a749-4cb2-9e0e-2510043f48ac")
SNIPPET_ID   = _env("SNIPPET_ID",
    "QVFJREFIaEdEc0hWQU9TcWFkUjZBZVY0bDJ6cnBCUVdIZ0EyUC9OWkxRSmRQWGEzY0FG"
    "ekVPL3Bac1lxWXJPT3lPUUdUYXdMQUFBQWJqQnNCZ2txaGtpRzl3MEJCd2FnWHpCZEFn"
    "RUFNRmdHQ1NxR1NJYjNEUUVIQVRBZUJnbGdoa2dCWlFNRUFTNHdFUVFNZVduTjdBV3Zn"
    "WElFYTRkNkFnRVFnQ3Z2MXNwdEt6YjBTNXRRVEFiU2QyWmFvZ2VQb0Z4TzhPQXI4UkxB"
    "MWpQUG83V3ZQTXg1ZHhxKzk1WjU6OkM1WVI2U01URGIrdzhHMTYyOG1HVlVZUitobGx3"
    "S1FYZnh6STVzNGtadkYrcXJXNDhjTmJQUFJtZWhTSy8wQjk1bHZPSFVKNkg0cTFOdVM2"
    "bUFxWmUwa3hWZ21FOC9iS1pIZmt2RzVyRlVCRmJzaVd1NXF6b2xXdFFJQU5xMEM1WDV6"
    "TSsrTzhCdU9xaEVVbnZ4MXl0ekNnUmMwSkU2ST0="
)

# ── Theme colors ──
COLOR_NAVY      = _env("COLOR_NAVY", "#10264a")
COLOR_BLUE      = _env("COLOR_BLUE", "#1a3a6b")
COLOR_GOLD      = _env("COLOR_GOLD", "#f5a623")
COLOR_GOLD_LT   = _env("COLOR_GOLD_LIGHT", "#fbbf24")

# ── Widget display — sizes adapt to mode ──
WIDGET_HEADER    = _env("WIDGET_HEADER", "211 Helpline")
WIDGET_BOT_NAME  = _env("WIDGET_BOT_NAME", "211 Specialist")

_DEFAULTS = {
    "standard": {"w": "420px", "h": "640px", "font": "14px"},
    "kiosk":    {"w": "780px", "h": "920px", "font": "18px"},
    "mobile":   {"w": "100vw", "h": "calc(100vh - 72px)", "font": "16px"},
}
_d = _DEFAULTS[VIEW_MODE]

WIDGET_WIDTH     = _env("WIDGET_WIDTH",  _d["w"])
WIDGET_HEIGHT    = _env("WIDGET_HEIGHT", _d["h"])
WIDGET_FONT_SIZE = _d["font"]

IS_KIOSK  = VIEW_MODE == "kiosk"
IS_MOBILE = VIEW_MODE == "mobile"
IS_STD    = VIEW_MODE == "standard"
