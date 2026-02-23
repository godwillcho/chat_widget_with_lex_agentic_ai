"""
widget.py — Orchestrates the Amazon Connect widget with enhancements
────────────────────────────────────────────────────────────────────────────
Loads:
  1. Amazon Connect widget snippet from widget_scripts/connect_snippet.js
  2. Injects customDisplayNames (bot name from config)
  3. Custom enhancements (widget_enhancements.py)

To update the widget snippet:
  1. Copy the new snippet from Amazon Connect admin console
  2. Paste it into widget_scripts/connect_snippet.js (replace entire file)
  3. Deploy with: python deploy.py

View modes:
  standard → floating widget (bottom-right)
  kiosk    → large centered widget, auto-open, auto-reset on close
"""

import os
from config import WIDGET_BOT_NAME
from widget_enhancements import get_enhancements

_DIR = os.path.dirname(os.path.abspath(__file__))
_SNIPPET_FILE = os.path.join(_DIR, "widget_scripts", "connect_snippet.js")


def _js_esc(s: str) -> str:
    """Escape strings for safe use in JavaScript."""
    return s.replace("\\", "\\\\").replace("'", "\\'")


def _load_base_snippet() -> str:
    """Load the Amazon Connect widget snippet from file."""
    with open(_SNIPPET_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()


def _display_names_script() -> str:
    """Generate customDisplayNames script (bot name from config)."""
    return f"""<script type="text/javascript">
  amazon_connect('customDisplayNames', {{
    transcript: {{
      botMessageDisplayName: '{_js_esc(WIDGET_BOT_NAME)}',
      systemMessageDisplayName: '{_js_esc(WIDGET_BOT_NAME)}'
    }}
  }});
</script>"""


def render_widget_script() -> str:
    """
    Render complete widget script: snippet file + display names + enhancements.

    Returns:
        Complete HTML/JS string for widget injection.
    """
    parts = [
        _load_base_snippet(),
        "\n",
        _display_names_script(),
        "\n",
    ]
    parts.extend(get_enhancements())
    return "".join(parts)
