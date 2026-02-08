"""
Nested Stack: Web Application (Chat Widget Lambda)
This is ONE of potentially many nested stacks in the project.
Handles the public-facing web application with chat widget.
"""
from aws_cdk import (
    NestedStack,
    Duration,
    CfnOutput,
    RemovalPolicy,
)
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_logs as logs
from aws_cdk import aws_iam as iam
from constructs import Construct
import os


class WebAppStack(NestedStack):
    """
    Web Application Nested Stack - 211 Chat Widget.

    This nested stack is ONE component of the larger project.
    Other nested stacks can be added for:
    - Database layer (RDS, DynamoDB)
    - API layer (API Gateway, additional Lambdas)
    - Storage layer (S3, CloudFront)
    - Monitoring layer (CloudWatch Dashboards, Alarms)
    - Authentication layer (Cognito, IAM)

    Creates:
    - Lambda function with Python 3.11 runtime
    - Lambda Function URL with CORS support
    - CloudWatch Logs with configurable retention
    - IAM role with necessary permissions
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        environment_name: str,
        lambda_config: dict,
        widget_config: dict,
        enable_cors: bool = True,
        cors_allowed_origins: list = None,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Lambda code directory (relative to CDK root)
        lambda_code_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "lambda_functions",
            "chat_widget"
        )

        # Create Lambda function
        self.chat_widget_function = lambda_.Function(
            self,
            "ChatWidgetFunction",
            function_name=f"chat-widget-{environment_name}",
            runtime=lambda_.Runtime.PYTHON_3_11,
            handler="lambda_function.lambda_handler",
            code=lambda_.Code.from_asset(lambda_code_path),
            memory_size=lambda_config.get("memory_size", 512),
            timeout=Duration.seconds(lambda_config.get("timeout", 30)),
            environment=widget_config,
            description=f"211 Chat Widget Lambda - {environment_name}",
            reserved_concurrent_executions=lambda_config.get("reserved_concurrent_executions"),
            log_retention=self._get_log_retention(lambda_config.get("log_retention_days", 7)),
        )

        # Grant permissions for CloudWatch Logs
        self.chat_widget_function.add_to_role_policy(
            iam.PolicyStatement(
                actions=[
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents"
                ],
                resources=["*"],
            )
        )

        # Create Function URL with CORS
        cors_config = None
        if enable_cors:
            allowed_origins = cors_allowed_origins or ["*"]
            cors_config = lambda_.FunctionUrlCorsOptions(
                allowed_origins=allowed_origins,
                allowed_methods=[lambda_.HttpMethod.GET, lambda_.HttpMethod.POST],
                allowed_headers=["*"],
                max_age=Duration.seconds(300),
            )

        function_url = self.chat_widget_function.add_function_url(
            auth_type=lambda_.FunctionUrlAuthType.NONE,
            cors=cors_config,
        )

        # Outputs
        CfnOutput(
            self,
            "FunctionName",
            value=self.chat_widget_function.function_name,
            description="Lambda function name",
            export_name=f"ChatWidget-{environment_name}-FunctionName",
        )

        CfnOutput(
            self,
            "FunctionArn",
            value=self.chat_widget_function.function_arn,
            description="Lambda function ARN",
            export_name=f"ChatWidget-{environment_name}-FunctionArn",
        )

        CfnOutput(
            self,
            "FunctionUrl",
            value=function_url.url,
            description="Lambda Function URL (publicly accessible)",
            export_name=f"ChatWidget-{environment_name}-FunctionUrl",
        )

        CfnOutput(
            self,
            "Environment",
            value=environment_name,
            description="Deployment environment",
        )

        # Store function URL for parent stack
        self.function_url = function_url.url

    def _get_log_retention(self, days: int) -> logs.RetentionDays:
        """Convert days to RetentionDays enum."""
        retention_map = {
            1: logs.RetentionDays.ONE_DAY,
            3: logs.RetentionDays.THREE_DAYS,
            5: logs.RetentionDays.FIVE_DAYS,
            7: logs.RetentionDays.ONE_WEEK,
            14: logs.RetentionDays.TWO_WEEKS,
            30: logs.RetentionDays.ONE_MONTH,
            60: logs.RetentionDays.TWO_MONTHS,
            90: logs.RetentionDays.THREE_MONTHS,
            120: logs.RetentionDays.FOUR_MONTHS,
            180: logs.RetentionDays.FIVE_MONTHS,
            365: logs.RetentionDays.ONE_YEAR,
        }
        return retention_map.get(days, logs.RetentionDays.ONE_WEEK)
