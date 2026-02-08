"""
widget.py — Orchestrates the Amazon Connect widget with enhancements
────────────────────────────────────────────────────────────────────────────
Generates:
  1. Base Amazon Connect widget snippet (from widget_scripts/*.js files)
  2. Custom enhancements (widget_enhancements.py)

View modes:
  standard → floating widget (bottom-right)
  kiosk    → large centered widget, auto-open, auto-reset on close
  mobile   → full-width widget anchored below header, auto-open
"""

import os
from widget_enhancements import get_enhancements


def _generate_base_snippet() -> str:
    """Load the base Amazon Connect snippet from file."""
    # Get environment name from environment variable
    environment = os.environ.get('ENVIRONMENT', 'dev')

    # Build path to the widget script file
    script_path = os.path.join(
        os.path.dirname(__file__),
        'widget_scripts',
        f'connect_snippet_{environment}.js'
    )

    # Read and return the raw Amazon Connect script
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        error_msg = f"Widget script not found: {script_path}"
        print(f"ERROR: {error_msg}")
        return f"<!-- ERROR: {error_msg} -->"
    except Exception as e:
        error_msg = f"Failed to read widget script: {e}"
        print(f"ERROR: {error_msg}")
        return f"<!-- ERROR: {error_msg} -->"


def render_widget_script() -> str:
    """
    Render complete widget script with base snippet + enhancements.

    Returns:
        Complete HTML/JS string for widget injection.
    """
    parts = [_generate_base_snippet(), "\n"]
    parts.extend(get_enhancements())
    return "".join(parts)
