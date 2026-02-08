# Creating a New Nested Stack

This guide shows how to add a new nested stack to the project.

## Steps to Add a New Nested Stack

### 1. Create Your Stack File

Create a new file in `cdk/stacks/` directory:

```bash
cd cdk/stacks
touch my_new_stack.py
```

### 2. Use This Template

```python
"""
Nested Stack: [Your Component Name]
Brief description of what this stack creates.
"""
from aws_cdk import (
    NestedStack,
    CfnOutput,
)
# Import AWS services you need
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_dynamodb as dynamodb
# ... other imports

from constructs import Construct


class MyNewStack(NestedStack):
    """
    [Component Name] Nested Stack.

    Creates:
    - Resource 1
    - Resource 2
    - Resource 3
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        environment_name: str,
        my_config: dict,
        # Add any dependencies from other stacks
        # database_endpoint: str = None,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create your resources here
        # Example: S3 bucket
        self.my_bucket = s3.Bucket(
            self,
            "MyBucket",
            bucket_name=f"my-bucket-{environment_name}",
        )

        # Example: Lambda function
        self.my_function = lambda_.Function(
            self,
            "MyFunction",
            function_name=f"my-function-{environment_name}",
            runtime=lambda_.Runtime.PYTHON_3_11,
            handler="index.handler",
            code=lambda_.Code.from_asset("lambda/my_function"),
        )

        # Outputs (accessible from main stack and other nested stacks)
        CfnOutput(
            self,
            "BucketName",
            value=self.my_bucket.bucket_name,
            description="S3 bucket name",
            export_name=f"MyStack-{environment_name}-BucketName",
        )

        CfnOutput(
            self,
            "FunctionArn",
            value=self.my_function.function_arn,
            description="Lambda function ARN",
            export_name=f"MyStack-{environment_name}-FunctionArn",
        )

        # Store important values for parent stack
        self.bucket_name = self.my_bucket.bucket_name
        self.function_arn = self.my_function.function_arn
```

### 3. Add Configuration to `config/environments.py`

```python
ENVIRONMENTS = {
    "dev": {
        # ... existing config ...

        # Add your new stack's config
        "my_stack_config": {
            "enable_feature_x": True,
            "timeout": 300,
            # ... other settings
        },
    },
    "staging": {
        # ... add config for staging ...
        "my_stack_config": { ... },
    },
    "prod": {
        # ... add config for production ...
        "my_stack_config": { ... },
    },
}
```

### 4. Import in `stacks/__init__.py`

```python
"""CDK Stacks module."""
from .main_stack import ProjectMainStack
from .web_app_stack import WebAppStack
from .my_new_stack import MyNewStack  # Add this

__all__ = ["ProjectMainStack", "WebAppStack", "MyNewStack"]  # Add to exports
```

### 5. Add to Main Stack

Edit `stacks/main_stack.py`:

```python
# At the top, import your new stack
from .my_new_stack import MyNewStack

class ProjectMainStack(Stack):
    def __init__(...):
        # ... existing code ...

        # Add your nested stack
        self.my_new_stack = MyNewStack(
            self,
            "MyNewStack",
            environment_name=environment_name,
            my_config=config.get("my_stack_config", {}),
            # Pass outputs from other stacks if needed
            # database_endpoint=self.database_stack.endpoint,
            description=f"My New Component - {environment_name}",
        )

        # Add outputs to main stack
        CfnOutput(
            self,
            "MyNewStackBucket",
            value=self.my_new_stack.bucket_name,
            description="Bucket name from my new stack",
        )
```

### 6. Deploy

```bash
# Preview changes
./deploy.sh dev diff

# Deploy
./deploy.sh dev deploy
```

## Examples of Nested Stacks You Can Add

### Database Stack
- RDS PostgreSQL/MySQL
- DynamoDB tables
- ElastiCache Redis
- Database security groups

### API Stack
- API Gateway REST/HTTP API
- API Lambda functions
- Authorizers (Cognito, Lambda)
- Usage plans and API keys

### Storage Stack
- S3 buckets for uploads
- CloudFront distribution
- S3 bucket policies

### Authentication Stack
- Cognito User Pool
- Identity Pool
- User Pool Client
- Custom authentication flows

### Monitoring Stack
- CloudWatch Dashboards
- CloudWatch Alarms
- SNS topics for alerts
- Log insights queries

### Networking Stack (if using VPC)
- VPC with subnets
- NAT Gateways
- Security Groups
- VPC Endpoints

### Queue/Event Stack
- SQS queues
- SNS topics
- EventBridge rules
- Step Functions

## Best Practices

### 1. Keep Stacks Focused
Each nested stack should handle ONE concern:
- ✅ Good: "DatabaseStack" with RDS + DynamoDB
- ❌ Bad: "EverythingStack" with DB, API, storage, etc.

### 2. Use Clear Naming
- Stack files: `component_stack.py` (e.g., `database_stack.py`)
- Class names: `ComponentStack` (e.g., `DatabaseStack`)
- Construct IDs: `"ComponentStack"` in main_stack.py

### 3. Export Important Values
Use `CfnOutput` with `export_name` for values other stacks might need:
```python
CfnOutput(
    self,
    "DatabaseEndpoint",
    value=self.database.endpoint,
    export_name=f"Database-{environment_name}-Endpoint",
)
```

### 4. Handle Dependencies
If Stack B needs resources from Stack A:
```python
# In main_stack.py
self.database_stack = DatabaseStack(...)
self.api_stack = ApiStack(
    ...
    database_endpoint=self.database_stack.endpoint,  # Pass dependency
)
```

### 5. Environment-Specific Config
Different environments should have different settings:
```python
"dev": {"database_size": "micro", "backup_days": 0},
"prod": {"database_size": "large", "backup_days": 30},
```

### 6. Use Removal Policies Wisely
```python
removal_policy=RemovalPolicy.DESTROY if environment_name == "dev" else RemovalPolicy.RETAIN
```
- Dev: DESTROY (easy cleanup)
- Prod: RETAIN (safety)

## Common Patterns

### Pattern 1: Cross-Stack References
```python
# In database_stack.py
self.table_name = my_table.table_name

# In main_stack.py
self.api_stack = ApiStack(
    ...
    table_name=self.database_stack.table_name,
)
```

### Pattern 2: Granting Permissions
```python
# In database_stack.py
def grant_read_access(self, lambda_function):
    self.my_table.grant_read_data(lambda_function)

# In main_stack.py
self.database_stack.grant_read_access(self.web_app_stack.chat_widget_function)
```

### Pattern 3: Conditional Resources
```python
if environment_name == "prod":
    # Only create in production
    self.replica = create_read_replica()
```

## Testing Your Stack

```bash
# 1. Synthesize (verify no errors)
./deploy.sh dev synth

# 2. View what will be created
./deploy.sh dev diff

# 3. Deploy to dev
./deploy.sh dev deploy

# 4. Verify outputs
aws cloudformation describe-stacks \
  --stack-name Project-Dev \
  --query "Stacks[0].Outputs"

# 5. Test functionality
# ... your tests ...

# 6. Deploy to production
./deploy.sh prod deploy
```

## Troubleshooting

### "Circular dependency detected"
**Problem**: Stack A depends on Stack B, and Stack B depends on Stack A.
**Solution**: Redesign dependency flow or use CloudFormation exports.

### "Resource limit exceeded"
**Problem**: Too many resources in one nested stack.
**Solution**: Split into multiple nested stacks.

### "Import error"
**Problem**: Import in main_stack.py fails.
**Solution**: Ensure class name matches in `stacks/__init__.py`.

## Need Help?

Check these examples:
- `stacks/web_app_stack.py` - Working example
- `stacks/database_stack.example.py` - Template example
- [AWS CDK API Reference](https://docs.aws.amazon.com/cdk/api/v2/python/)

---

**Happy stacking!** 🏗️
