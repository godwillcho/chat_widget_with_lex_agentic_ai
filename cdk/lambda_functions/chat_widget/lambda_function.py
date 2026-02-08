"""
lambda_function.py — AWS Lambda entry point.
─────────────────────────────────────────────
Mode priority:
  1. ?mode=standard|kiosk|mobile  (URL query string — explicit choice)
  2. VIEW_MODE env var at deploy   (standard|kiosk|mobile)
  3. Legacy KIOSK_MODE=true env    (maps to kiosk)
  4. Auto-detect mobile via User-Agent header
  5. Defaults to standard

Logs every request's resolved view mode + source to CloudWatch.
"""

import json
import logging
import os
import re
import sys

logger = logging.getLogger()
logger.setLevel(logging.INFO)

_MOBILE_RE = re.compile(
    r"Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini|Mobile|Tablet",
    re.IGNORECASE,
)

# Snapshot the ORIGINAL deploy-time env vars once at cold start.
# This prevents previous invocations' os.environ writes from polluting
# the next invocation's mode resolution.
_DEPLOY_VIEW_MODE = os.environ.get("VIEW_MODE", "").lower().strip()
_DEPLOY_KIOSK     = os.environ.get("KIOSK_MODE", "").lower().strip() in ("true", "1", "yes")


def _resolve_mode(event: dict) -> tuple:
    """Return (mode, source) for this request without side-effects."""

    # 1. Explicit query string — always wins
    qs = event.get("queryStringParameters") or {}
    qm = qs.get("mode", "").lower()
    if qm in ("standard", "kiosk", "mobile"):
        return qm, "query_string"

    # 2. Deploy-time VIEW_MODE env
    if _DEPLOY_VIEW_MODE in ("standard", "kiosk", "mobile"):
        return _DEPLOY_VIEW_MODE, "env_VIEW_MODE"

    # 3. Legacy KIOSK_MODE env
    if _DEPLOY_KIOSK:
        return "kiosk", "env_KIOSK_MODE"

    # 4. Auto-detect from User-Agent
    headers = event.get("headers") or {}
    ua = headers.get("user-agent") or headers.get("User-Agent") or ""
    if _MOBILE_RE.search(ua):
        return "mobile", "auto_detect_mobile"

    # 5. Default
    return "standard", "default"


def lambda_handler(event, context):
    mode, source = _resolve_mode(event)

    # Set env so config.py reads it on import, then clear after render
    os.environ["VIEW_MODE"] = mode
    os.environ.pop("KIOSK_MODE", None)

    # Force reimport with fresh mode
    for mod in ("config", "styles", "widget", "widget_enhancements", "page"):
        sys.modules.pop(mod, None)

    from styles import render_styles
    from widget import render_widget_script
    from page import render_page

    html = render_page(
        styles_css=render_styles(),
        widget_script=render_widget_script(),
    )

    # Reset VIEW_MODE to deploy-time value so next invocation's
    # _resolve_mode snapshot check isn't polluted
    if _DEPLOY_VIEW_MODE:
        os.environ["VIEW_MODE"] = _DEPLOY_VIEW_MODE
    else:
        os.environ.pop("VIEW_MODE", None)

    # ── CloudWatch structured log ──
    headers = event.get("headers") or {}
    ua = headers.get("user-agent") or headers.get("User-Agent") or ""
    source_ip = (event.get("requestContext", {})
                      .get("http", {})
                      .get("sourceIp", ""))

    logger.info(json.dumps({
        "event":       "page_render",
        "view_mode":   mode,
        "mode_source": source,
        "user_agent":  ua[:300],
        "source_ip":   source_ip or None,
        "query_mode":  (event.get("queryStringParameters") or {}).get("mode"),
    }))

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html; charset=utf-8"},
        "body": html,
    }
