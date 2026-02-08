"""
Main Stack: Project Infrastructure
Orchestrates multiple nested stacks and shared resources for the entire project.
"""
from aws_cdk import (
    Stack,
    CfnOutput,
    Tags,
)
from constructs import Construct
from .web_app_stack import WebAppStack
# Import other nested stacks here as you add them
# from .database_stack import DatabaseStack
# from .api_stack import ApiStack
# from .monitoring_stack import MonitoringStack


class ProjectMainStack(Stack):
    """
    Main orchestration stack for the entire project.

    This stack creates and coordinates multiple nested stacks:
    - Web App Stack (Chat Widget Lambda + Function URL)
    - [Future] Database Stack (RDS, DynamoDB, etc.)
    - [Future] API Stack (API Gateway, additional Lambdas)
    - [Future] Monitoring Stack (CloudWatch Dashboards, Alarms)
    - [Future] Storage Stack (S3 buckets, CloudFront)

    Each nested stack is independently manageable while sharing
    common resources and configurations defined in the main stack.
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        environment_name: str,
        config: dict,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Add project-level tags
        Tags.of(self).add("StackType", "Main")
        Tags.of(self).add("Project", "211ChatWidget")
        Tags.of(self).add("ManagedBy", "CDK")

        # ═══════════════════════════════════════════════════════════
        # NESTED STACK 1: Web Application (Chat Widget)
        # ═══════════════════════════════════════════════════════════
        self.web_app_stack = WebAppStack(
            self,
            "WebAppStack",
            environment_name=environment_name,
            lambda_config=config["lambda_config"],
            widget_config=config["widget_config"],
            enable_cors=config.get("enable_cors", True),
            cors_allowed_origins=config.get("cors_allowed_origins", ["*"]),
            description=f"Web App: 211 Chat Widget Lambda - {environment_name}",
        )

        # ═══════════════════════════════════════════════════════════
        # NESTED STACK 2: Database (Example - Uncomment to add)
        # ═══════════════════════════════════════════════════════════
        # self.database_stack = DatabaseStack(
        #     self,
        #     "DatabaseStack",
        #     environment_name=environment_name,
        #     database_config=config.get("database_config", {}),
        #     description=f"Database: RDS/DynamoDB - {environment_name}",
        # )

        # ═══════════════════════════════════════════════════════════
        # NESTED STACK 3: API Layer (Example - Uncomment to add)
        # ═══════════════════════════════════════════════════════════
        # self.api_stack = ApiStack(
        #     self,
        #     "ApiStack",
        #     environment_name=environment_name,
        #     api_config=config.get("api_config", {}),
        #     # Pass outputs from other stacks if needed
        #     database_endpoint=self.database_stack.endpoint,
        #     description=f"API: REST/GraphQL - {environment_name}",
        # )

        # ═══════════════════════════════════════════════════════════
        # NESTED STACK 4: Monitoring (Example - Uncomment to add)
        # ═══════════════════════════════════════════════════════════
        # self.monitoring_stack = MonitoringStack(
        #     self,
        #     "MonitoringStack",
        #     environment_name=environment_name,
        #     # Pass resources to monitor
        #     lambda_functions=[self.web_app_stack.chat_widget_function],
        #     description=f"Monitoring: CloudWatch - {environment_name}",
        # )

        # ═══════════════════════════════════════════════════════════
        # MAIN STACK OUTPUTS
        # ═══════════════════════════════════════════════════════════

        CfnOutput(
            self,
            "DeploymentEnvironment",
            value=environment_name,
            description="Deployment environment name",
        )

        CfnOutput(
            self,
            "StackName",
            value=self.stack_name,
            description="CloudFormation main stack name",
        )

        CfnOutput(
            self,
            "Region",
            value=self.region,
            description="AWS region",
        )

        # Web App outputs
        CfnOutput(
            self,
            "WebAppUrl",
            value=self.web_app_stack.function_url,
            description="Public URL for the chat widget web application",
        )

        CfnOutput(
            self,
            "WebAppFunctionName",
            value=self.web_app_stack.chat_widget_function.function_name,
            description="Lambda function name for the web app",
        )

        # Add outputs from other nested stacks as you create them
        # CfnOutput(
        #     self,
        #     "DatabaseEndpoint",
        #     value=self.database_stack.endpoint,
        #     description="Database connection endpoint",
        # )
