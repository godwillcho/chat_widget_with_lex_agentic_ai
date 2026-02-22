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
            # ─── Amazon Connect Credentials ───────────────────────
            "CONNECT_URL": "https://nextgencxsolutions.my.connect.aws",
            "CONNECT_INSTANCE_ID": "e75a053a-60c7-45f3-83f7-a24df6d3b52d",
            "CONTACT_FLOW_ID": "b1cc0b5a-09d5-4c50-ad1f-5b9b55f75336",
            "WIDGET_ID": "497c0ff9-3611-45dc-a56d-21aa65f76969",
            "SNIPPET_ID": "QVFJREFIaEdEc0hWQU9TcWFkUjZBZVY0bDJ6cnBCUVdIZ0EyUC9OWkxRSmRQWGEzY0FGMjJzcWp0L045Qk5ZNmFQYXQweXpHQUFBQWJqQnNCZ2txaGtpRzl3MEJCd2FnWHpCZEFnRUFNRmdHQ1NxR1NJYjNEUUVIQVRBZUJnbGdoa2dCWlFNRUFTNHdFUVFNQUZkTHdhcERSK3MrcVZYYUFnRVFnQ3Y3dUdLYjc4K0RERnc2Nzl5RHVHN1Znc3dybVpwUDIzUkdIVGI3bDNSZEpHS2NDZThyaUpnWGE2Vmw6OlZyU3UrQmFJdFZ5REhNeUplVEJUK1JZd2dwTmV2UkFQVHJGSXU1SkRDSUtpTjF1UkNERVd0K1A5L25zNTh6Q0lYcVpvN3Jib2lqWU5BOWRGVThiUE8reDBVK0V0SmlGRERSVEllRjEzTGlKb3lBQ24wd1pKVnoxQWxFQlJETWJHOUN1U1FhS05sdWNNaFdDemJQN3dZNzA2eGI4ZmEzbz0=",
            "SECURITY_KEY": "Z+I+2RtFRc0fj0Nx9CgRBQiPSChzRQnFQ4wBL2N3WXg=",
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
