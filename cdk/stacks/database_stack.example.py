"""
Example Nested Stack: Database Layer
This is an EXAMPLE template showing how to add another nested stack.
Rename to database_stack.py and uncomment in main_stack.py to use.
"""
from aws_cdk import (
    NestedStack,
    Duration,
    CfnOutput,
    RemovalPolicy,
)
from aws_cdk import aws_rds as rds
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_ec2 as ec2
from constructs import Construct


class DatabaseStack(NestedStack):
    """
    Database Nested Stack - Example implementation.

    This shows how to add a new nested stack to the project.
    You can create RDS instances, DynamoDB tables, or both.

    Creates (examples):
    - DynamoDB table for session storage
    - RDS PostgreSQL database for user data
    - VPC security groups
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        environment_name: str,
        database_config: dict,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Example: Create DynamoDB table
        if database_config.get("create_dynamodb", False):
            self.sessions_table = dynamodb.Table(
                self,
                "SessionsTable",
                table_name=f"chat-sessions-{environment_name}",
                partition_key=dynamodb.Attribute(
                    name="session_id",
                    type=dynamodb.AttributeType.STRING
                ),
                billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
                removal_policy=RemovalPolicy.DESTROY if environment_name == "dev" else RemovalPolicy.RETAIN,
                point_in_time_recovery=environment_name == "prod",
            )

            CfnOutput(
                self,
                "SessionsTableName",
                value=self.sessions_table.table_name,
                description="DynamoDB table for chat sessions",
            )

            CfnOutput(
                self,
                "SessionsTableArn",
                value=self.sessions_table.table_arn,
                description="DynamoDB table ARN",
            )

        # Example: Create RDS PostgreSQL database (commented out for template)
        # if database_config.get("create_rds", False):
        #     # Create VPC
        #     vpc = ec2.Vpc(self, "DatabaseVpc",
        #         max_azs=2,
        #         nat_gateways=1 if environment_name != "dev" else 0,
        #     )
        #
        #     # Create RDS instance
        #     self.database = rds.DatabaseInstance(
        #         self,
        #         "ChatDatabase",
        #         engine=rds.DatabaseInstanceEngine.postgres(
        #             version=rds.PostgresEngineVersion.VER_15_3
        #         ),
        #         instance_type=ec2.InstanceType.of(
        #             ec2.InstanceClass.BURSTABLE3,
        #             ec2.InstanceSize.MICRO if environment_name == "dev" else ec2.InstanceSize.SMALL
        #         ),
        #         vpc=vpc,
        #         allocated_storage=20,
        #         database_name=f"chatdb_{environment_name}",
        #         backup_retention=Duration.days(7 if environment_name == "prod" else 0),
        #         removal_policy=RemovalPolicy.SNAPSHOT if environment_name == "prod" else RemovalPolicy.DESTROY,
        #     )
        #
        #     self.endpoint = self.database.db_instance_endpoint_address
        #
        #     CfnOutput(
        #         self,
        #         "DatabaseEndpoint",
        #         value=self.endpoint,
        #         description="RDS database endpoint",
        #     )
