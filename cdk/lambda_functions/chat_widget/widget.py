"""
widget.py — Orchestrates the Amazon Connect widget with enhancements
────────────────────────────────────────────────────────────────────────────
Generates:
  1. Static Amazon Connect widget snippet with snippetId (from widget_scripts/*.js files)
  2. Custom enhancements (widget_enhancements.py)

View modes:
  standard → floating widget (bottom-right)
  kiosk    → large centered widget, auto-open, auto-reset on close
  mobile   → full-width widget anchored below header, auto-open
"""

import os
from widget_enhancements import get_enhancements


def _generate_base_snippet() -> str:
    """
    Load the base Amazon Connect snippet from environment-specific file.

    Loads: connect_snippet_{environment}.js (e.g., connect_snippet_dev.js)
    """
    environment = os.environ.get('ENVIRONMENT', 'dev')
    script_path = os.path.join(
        os.path.dirname(__file__),
        'widget_scripts',
        f'connect_snippet_{environment}.js'
    )

    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            print(f"INFO: Loading static widget snippet for {environment}")
            return f.read()
    except Exception as e:
        error_msg = f"Failed to read widget script {script_path}: {e}"
        print(f"ERROR: {error_msg}")
        return f"<!-- ERROR: {error_msg} -->"


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
