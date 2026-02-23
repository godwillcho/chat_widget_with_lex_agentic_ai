"""
Environment configuration for deployment.
Deploy: cdk deploy -c environment=dev --require-approval never
"""

ENVIRONMENTS = {
    "dev": {
        "stack_name_suffix": "Dev",
        "aws_region": "us-west-2",
        "cost_center": "Stability360-Dev",
        "lambda_config": {
            "memory_size": 512,
            "timeout": 30,
            "log_retention_days": 7,
            "reserved_concurrent_executions": None,
        },
        "widget_config": {
            "ENVIRONMENT": "dev",
            "VIEW_MODE": "standard",  # Options: "standard", "kiosk" (override via URL: ?mode=kiosk)
            "COMPANY_NAME": "Trident United Way",
            # ─── Theme Colors ─────────────────────────────────────
            "COLOR_NAVY": "#10264a",
            "COLOR_BLUE": "#1a3a6b",
            "COLOR_GOLD": "#f5a623",
            "COLOR_GOLD_LIGHT": "#fbbf24",
            # ─── Widget Display Text ──────────────────────────────
            "WIDGET_HEADER": "Trident United Way Stability360",
            "WIDGET_BOT_NAME": "Stability360",
            # ─── Page Display Text ───────────────────────────────
            "SERVICE_NAME": "Stability360",
            "SERVICE_TAGLINE": "Your connection to care",
            "COMPANY_TAGLINE": "Serving Berkeley, Charleston & Dorchester Counties",
            "FOOTER_TAGLINE": "Uniting the Tri-County to uplift families out of poverty.",
        },
        "enable_cors": True,
        "cors_allowed_origins": ["*"],
        "lex_bot_config": {
            "question_text": "***Do you consent to the use of your Data for identification purposes and research of resources based on your Needs?***",
            "alias_name": "prod",
            "idle_session_timeout": 300,
            "enable_confirmation": False,
            "enable_conversation_logs": True,
            "connect_instance_id": "e75a053a-60c7-45f3-83f7-a24df6d3b52d",
        },
    },
}


def get_environment_config(env_name: str) -> dict:
    """
    Get configuration for the specified environment.

    Args:
        env_name: Environment name (dev, staging, prod)

    Returns:
        Configuration dictionary for the environment

    Raises:
        ValueError: If environment name is not found
    """
    if env_name not in ENVIRONMENTS:
        raise ValueError(
            f"Unknown environment: {env_name}. "
            f"Available environments: {', '.join(ENVIRONMENTS.keys())}"
        )
    return ENVIRONMENTS[env_name]


def list_environments() -> list:
    """Return list of available environment names."""
    return list(ENVIRONMENTS.keys())
