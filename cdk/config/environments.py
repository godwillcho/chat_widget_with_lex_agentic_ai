"""
Environment-specific configurations for multi-account/multi-environment deployments.
Add new environments as needed for different AWS accounts or regions.

═══════════════════════════════════════════════════════════════════════════════
HOW TO GET AMAZON CONNECT CREDENTIALS
═══════════════════════════════════════════════════════════════════════════════

To configure your chat widget, you need three values from Amazon Connect:
1. CONNECT_URL    - Your Connect instance URL
2. WIDGET_ID      - Widget identifier (UUID format)
3. SNIPPET_ID     - Encrypted snippet ID (long base64 string)

STEP-BY-STEP INSTRUCTIONS:
──────────────────────────────────────────────────────────────────────────────

1. Log into AWS Console
   → Navigate to Amazon Connect service
   → Select your Connect instance

2. Go to Chat Widgets
   → In left sidebar: Channels → Chat widgets
   → Click on your widget (or create a new one)

3. Get Widget Code
   → Click "Show security key" button
   → Copy the entire widget code snippet

4. Extract Values from Widget Code

   The snippet looks like this:

   <script type="text/javascript">
       (function(w, d, x, id){
           s=d.createElement('script');
           s.src='https://YOUR-INSTANCE.my.connect.aws/connectwidget/...';
           ...
       })(window, document, 'amazon_connect', 'WIDGET-ID-HERE');
       amazon_connect('snippetId', 'SNIPPET-ID-HERE');
   </script>

   Extract:

   ✓ CONNECT_URL (from s.src line):
     Example: "https://yourinstance.my.connect.aws"
     Format:  https://{instance-name}.my.connect.aws

   ✓ WIDGET_ID (from the function call, 4th parameter):
     Example: "abc12345-1234-5678-90ab-cdef12345678"
     Format:  UUID (8-4-4-4-12 hex digits)

   ✓ SNIPPET_ID (from amazon_connect('snippetId', ...) call):
     Example: "QVFJREFIaEdEc0hWQU9TcWFkUjZBZVY0bDJ6..."
     Format:  Very long base64-encoded string (200+ characters)

5. Update This File
   → Replace the placeholder values below with your actual credentials
   → Save the file
   → Redeploy: cdk deploy -c environment=dev --require-approval never

SECURITY NOTES:
──────────────────────────────────────────────────────────────────────────────
• SNIPPET_ID contains encrypted Amazon Connect credentials - keep it secure
• This file is committed to git - ensure your repository is private
• For production, consider using AWS Secrets Manager (see docs/CONNECT_CONFIGURATION.md)
• Never share SNIPPET_ID publicly

MULTI-ORGANIZATION SUPPORT:
──────────────────────────────────────────────────────────────────────────────
To deploy for multiple organizations, add new environment entries:

ENVIRONMENTS = {
    "dev": { ... },           # Your development environment
    "prod": { ... },          # Your production environment
    "org2-prod": { ... },     # Another organization's production
}

Then deploy: cdk deploy -c environment=org2-prod

═══════════════════════════════════════════════════════════════════════════════
"""

ENVIRONMENTS = {
    "dev": {
        "stack_name_suffix": "Dev",
        "aws_region": "us-west-2",  # ALL resources deploy here (Lambda, Connect instance, etc.)
        "cost_center": "211Helpline-Dev",
        "lambda_config": {
            "memory_size": 512,
            "timeout": 30,
            "log_retention_days": 7,
            "reserved_concurrent_executions": None,
        },
        "widget_config": {
            # ─── Environment ────────────────────────────────────────────
            "ENVIRONMENT": "dev",  # Used to select view config from view_configs.py

            # ─── View Mode ──────────────────────────────────────────────
            "VIEW_MODE": "standard",  # Options: "standard", "kiosk", "mobile"
                                      # Can be overridden via URL: ?mode=kiosk

            # ─── Branding ───────────────────────────────────────────────
            "COMPANY_NAME": "Trident United Way - DEV",  # Your organization name

            # ─── Amazon Connect Credentials (REQUIRED) ──────────────────
            # NOTE: Connect instance MUST be in the same region as aws_region above
            # See instructions at top of file for how to get these values
            "CONNECT_URL": "https://nextgencxsolutions.my.connect.aws",  # ← UPDATE: Your Connect instance URL
            "WIDGET_ID": "cba73f0d-a749-4cb2-9e0e-2510043f48ac",         # ← UPDATE: Widget ID (UUID)
            "SNIPPET_ID": "QVFJREFIaEdEc0hWQU9TcWFkUjZBZVY0bDJ6cnBCUVdIZ0EyUC9OWkxRSmRQWGEzY0FGekVPL3Bac1lxWXJPT3lPUUdUYXdMQUFBQWJqQnNCZ2txaGtpRzl3MEJCd2FnWHpCZEFnRUFNRmdHQ1NxR1NJYjNEUUVIQVRBZUJnbGdoa2dCWlFNRUFTNHdFUVFNZVduTjdBV3ZnWElFYTRkNkFnRVFnQ3Z2MXNwdEt6YjBTNXRRVEFiU2QyWmFvZ2VQb0Z4TzhPQXI4UkxBMWpQUG83V3ZQTXg1ZHhxKzk1WjU6OkM1WVI2U01URGIrdzhHMTYyOG1HVlVZUitobGx3S1FYZnh6STVzNGtadkYrcXJXNDhjTmJQUFJtZWhTSy8wQjk1bHZPSFVKNkg0cTFOdVM2bUFxWmUwa3hWZ21FOC9iS1pIZmt2RzVyRlVCRmJzaVd1NXF6b2xXdFFJQU5xMEM1WDV6TSsrTzhCdU9xaEVVbnZ4MXl0ekNnUmMwSkU2ST0=",  # ← UPDATE: Encrypted snippet ID (base64)

            # ─── Pre-Chat Form Configuration ────────────────────────────
            # Pre-chat form is configured in lambda_functions/chat_widget/view_configs.py
            # Update VIEW_CONFIG_DEV in that file, then redeploy

            # ─── Theme Colors ───────────────────────────────────────────
            "COLOR_NAVY": "#10264a",        # Primary color (header, buttons)
            "COLOR_BLUE": "#1a3a6b",        # Secondary blue shade
            "COLOR_GOLD": "#f5a623",        # Accent color (highlights, CTAs)
            "COLOR_GOLD_LIGHT": "#fbbf24",  # Light accent shade

            # ─── Widget Display Text ────────────────────────────────────
            "WIDGET_HEADER": "211 Helpline",     # Widget header text
            "WIDGET_BOT_NAME": "211 Specialist", # Bot/agent display name
        },
        "enable_cors": True,
        "cors_allowed_origins": ["*"],
    },
    "staging": {
        "stack_name_suffix": "Staging",
        "aws_region": "us-west-2",  # ALL resources deploy here (Lambda, Connect instance, etc.)
        "cost_center": "211Helpline-Staging",
        "lambda_config": {
            "memory_size": 1024,
            "timeout": 30,
            "log_retention_days": 14,
            "reserved_concurrent_executions": 10,
        },
        "widget_config": {
            "ENVIRONMENT": "staging",
            "VIEW_MODE": "standard",
            "COMPANY_NAME": "Trident United Way - STAGING",
            # Amazon Connect credentials - update with your staging widget values
            "CONNECT_URL": "https://nextgencxsolutions.my.connect.aws",  # ← UPDATE
            "WIDGET_ID": "cba73f0d-a749-4cb2-9e0e-2510043f48ac",         # ← UPDATE
            "SNIPPET_ID": "QVFJREFIaEdEc0hWQU9TcWFkUjZBZVY0bDJ6cnBCUVdIZ0EyUC9OWkxRSmRQWGEzY0FGekVPL3Bac1lxWXJPT3lPUUdUYXdMQUFBQWJqQnNCZ2txaGtpRzl3MEJCd2FnWHpCZEFnRUFNRmdHQ1NxR1NJYjNEUUVIQVRBZUJnbGdoa2dCWlFNRUFTNHdFUVFNZVduTjdBV3ZnWElFYTRkNkFnRVFnQ3Z2MXNwdEt6YjBTNXRRVEFiU2QyWmFvZ2VQb0Z4TzhPQXI4UkxBMWpQUG83V3ZQTXg1ZHhxKzk1WjU6OkM1WVI2U01URGIrdzhHMTYyOG1HVlVZUitobGx3S1FYZnh6STVzNGtadkYrcXJXNDhjTmJQUFJtZWhTSy8wQjk1bHZPSFVKNkg0cTFOdVM2bUFxWmUwa3hWZ21FOC9iS1pIZmt2RzVyRlVCRmJzaVd1NXF6b2xXdFFJQU5xMEM1WDV6TSsrTzhCdU9xaEVVbnZ4MXl0ekNnUmMwSkU2ST0=",  # ← UPDATE
            # Pre-chat form: Update VIEW_CONFIG_STAGING in view_configs.py
            "COLOR_NAVY": "#10264a",
            "COLOR_BLUE": "#1a3a6b",
            "COLOR_GOLD": "#f5a623",
            "COLOR_GOLD_LIGHT": "#fbbf24",
            "WIDGET_HEADER": "211 Helpline",
            "WIDGET_BOT_NAME": "211 Specialist",
        },
        "enable_cors": True,
        "cors_allowed_origins": ["https://staging.example.com"],
    },
    "prod": {
        "stack_name_suffix": "Prod",
        "aws_region": "us-west-2",  # ALL resources deploy here (Lambda, Connect instance, etc.)
        "cost_center": "211Helpline-Production",
        "lambda_config": {
            "memory_size": 1024,
            "timeout": 30,
            "log_retention_days": 30,
            "reserved_concurrent_executions": 50,
        },
        "widget_config": {
            "ENVIRONMENT": "prod",
            "VIEW_MODE": "standard",
            "COMPANY_NAME": "Trident United Way",
            # Amazon Connect credentials - PRODUCTION values (test in dev/staging first!)
            "CONNECT_URL": "https://nextgencxsolutions.my.connect.aws",  # ← UPDATE
            "WIDGET_ID": "cba73f0d-a749-4cb2-9e0e-2510043f48ac",         # ← UPDATE
            "SNIPPET_ID": "QVFJREFIaEdEc0hWQU9TcWFkUjZBZVY0bDJ6cnBCUVdIZ0EyUC9OWkxRSmRQWGEzY0FGekVPL3Bac1lxWXJPT3lPUUdUYXdMQUFBQWJqQnNCZ2txaGtpRzl3MEJCd2FnWHpCZEFnRUFNRmdHQ1NxR1NJYjNEUUVIQVRBZUJnbGdoa2dCWlFNRUFTNHdFUVFNZVduTjdBV3ZnWElFYTRkNkFnRVFnQ3Z2MXNwdEt6YjBTNXRRVEFiU2QyWmFvZ2VQb0Z4TzhPQXI4UkxBMWpQUG83V3ZQTXg1ZHhxKzk1WjU6OkM1WVI2U01URGIrdzhHMTYyOG1HVlVZUitobGx3S1FYZnh6STVzNGtadkYrcXJXNDhjTmJQUFJtZWhTSy8wQjk1bHZPSFVKNkg0cTFOdVM2bUFxWmUwa3hWZ21FOC9iS1pIZmt2RzVyRlVCRmJzaVd1NXF6b2xXdFFJQU5xMEM1WDV6TSsrTzhCdU9xaEVVbnZ4MXl0ekNnUmMwSkU2ST0=",  # ← UPDATE
            # Pre-chat form: Update VIEW_CONFIG_PROD in view_configs.py
            "COLOR_NAVY": "#10264a",
            "COLOR_BLUE": "#1a3a6b",
            "COLOR_GOLD": "#f5a623",
            "COLOR_GOLD_LIGHT": "#fbbf24",
            "WIDGET_HEADER": "211 Helpline",
            "WIDGET_BOT_NAME": "211 Specialist",
        },
        "enable_cors": True,
        "cors_allowed_origins": ["https://www.tridentunitedway.org", "https://tridentunitedway.org"],
    },

    # ═══════════════════════════════════════════════════════════════════════
    # EXAMPLE: Add another organization
    # ═══════════════════════════════════════════════════════════════════════
    # Uncomment and customize the example below to deploy for another organization
    #
    # "org2-prod": {
    #     "stack_name_suffix": "Org2-Prod",
    #     "aws_region": "us-east-1",  # Can use different region
    #     "cost_center": "Organization2-Production",
    #     "lambda_config": {
    #         "memory_size": 1024,
    #         "timeout": 30,
    #         "log_retention_days": 30,
    #         "reserved_concurrent_executions": 25,
    #     },
    #     "widget_config": {
    #         "VIEW_MODE": "kiosk",  # This org uses kiosk mode by default
    #         "COMPANY_NAME": "Organization 2 Name",
    #         # Get these values from Organization 2's Amazon Connect instance
    #         "CONNECT_URL": "https://org2-instance.my.connect.aws",
    #         "WIDGET_ID": "org2-widget-id-here",
    #         "SNIPPET_ID": "org2-snippet-id-here",
    #         # Customize colors for this organization
    #         "COLOR_NAVY": "#003366",
    #         "COLOR_BLUE": "#0066cc",
    #         "COLOR_GOLD": "#ff9900",
    #         "COLOR_GOLD_LIGHT": "#ffcc66",
    #         "WIDGET_HEADER": "Organization 2 Helpline",
    #         "WIDGET_BOT_NAME": "Support Specialist",
    #     },
    #     "enable_cors": True,
    #     "cors_allowed_origins": ["https://www.org2.com"],
    # },
    #
    # Then deploy with: cdk deploy -c environment=org2-prod
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
