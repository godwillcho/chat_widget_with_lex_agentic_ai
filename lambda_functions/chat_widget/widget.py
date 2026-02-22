"""
widget.py — Orchestrates the Amazon Connect widget with enhancements
────────────────────────────────────────────────────────────────────────────
Generates:
  1. Amazon Connect widget snippet (built from config values)
  2. Custom enhancements (widget_enhancements.py)

View modes:
  standard → floating widget (bottom-right)
  kiosk    → large centered widget, auto-open, auto-reset on close
"""

from config import CONNECT_URL, WIDGET_ID, SNIPPET_ID, COLOR_NAVY, WIDGET_HEADER, WIDGET_BOT_NAME
from widget_enhancements import get_enhancements


def _js_esc(s: str) -> str:
    """Escape strings for safe use in JavaScript."""
    return s.replace("\\", "\\\\").replace("'", "\\'")


def _generate_base_snippet() -> str:
    """
    Generate the Amazon Connect hosted widget snippet from config values.

    Uses the latest AWS-supported snippet format with all current content types.
    """
    return f"""<script type="text/javascript">
  (function(w, d, x, id){{
    s=d.createElement('script');
    s.src='{CONNECT_URL}/connectwidget/static/amazon-connect-chat-interface-client.js';
    s.async=1;
    s.id=id;
    d.getElementsByTagName('head')[0].appendChild(s);
    w[x] = w[x] || function() {{ (w[x].ac = w[x].ac || []).push(arguments) }};
  }})(window, document, 'amazon_connect', '{WIDGET_ID}');

  amazon_connect('styles', {{
    iconType: 'CHAT',
    openChat: {{ color: '#ffffff', backgroundColor: '{COLOR_NAVY}' }},
    closeChat: {{ color: '#ffffff', backgroundColor: '{COLOR_NAVY}' }}
  }});

  amazon_connect('snippetId', '{SNIPPET_ID}');

  amazon_connect('supportedMessagingContentTypes', [
    'text/plain',
    'text/markdown',
    'application/vnd.amazonaws.connect.message.interactive',
    'application/vnd.amazonaws.connect.message.interactive.response'
  ]);

  amazon_connect('customDisplayNames', {{
    transcript: {{
      botMessageDisplayName: '{_js_esc(WIDGET_BOT_NAME)}',
      systemMessageDisplayName: '{_js_esc(WIDGET_BOT_NAME)}'
    }}
  }});
</script>"""


def render_widget_script() -> str:
    """
    Render complete widget script with base snippet + enhancements.

    Returns:
        Complete HTML/JS string for widget injection.
    """
    parts = [
        _generate_base_snippet(),
        "\n"
    ]
    parts.extend(get_enhancements())
    return "".join(parts)
