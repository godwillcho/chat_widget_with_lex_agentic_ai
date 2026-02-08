# CDK Resource Organization

## Directory Structure

```
cdk/
├── app.py                          # CDK app entry point
├── cdk.json                        # CDK configuration
├── requirements.txt                # Python dependencies
│
├── config/                         # Configuration
│   ├── __init__.py
│   └── environments.py             # Environment-specific configs
│
├── stacks/                         # CDK Stack Definitions
│   ├── __init__.py
│   ├── main_stack.py              # Main orchestration stack
│   ├── web_app_stack.py           # Web app nested stack
│   └── [future_stack.py]          # Add new stacks here
│
├── lambda_functions/               # All Lambda Functions
│   ├── chat_widget/               # Chat widget Lambda
│   │   ├── lambda_function.py     # Handler
│   │   ├── config.py              # Configuration
│   │   ├── view_config.py         # Connect View
│   │   ├── widget.py              # Widget logic
│   │   ├── styles.py              # CSS generation
│   │   ├── page.py                # HTML templates
│   │   └── widget_snippet.js      # Connect snippet
│   │
│   └── [future_lambda/]           # Add new Lambdas here
│
├── resources/                      # Other AWS Resources
│   ├── README.md                  # Resource organization guide
│   └── future_resources/          # Placeholder for future resources
│
└── docs/                          # Documentation
    ├── INDEX.md
    ├── README.md
    ├── QUICKSTART.md
    ├── ARCHITECTURE.md
    ├── DEPLOYMENT_CHECKLIST.md
    ├── NESTED_STACK_TEMPLATE.md
    └── CONNECT_CONFIGURATION.md
```

---

## Resource Organization Guidelines

### Lambda Functions (`lambda_functions/`)

**Purpose**: Store all Lambda function code

**Structure**:
```
lambda_functions/
├── function_name_1/
│   ├── lambda_function.py    # Required: Handler file
│   ├── requirements.txt      # Optional: Function-specific dependencies
│   └── [other modules]       # Supporting code
│
└── function_name_2/
    └── ...
```

**When to create**:
- One directory per Lambda function
- Name directory after the function's purpose (e.g., `chat_widget`, `api_handler`, `data_processor`)

**Example - Adding a new Lambda**:
```bash
mkdir -p lambda_functions/api_handler
touch lambda_functions/api_handler/lambda_function.py
touch lambda_functions/api_handler/requirements.txt
```

---

### Stacks (`stacks/`)

**Purpose**: CDK stack definitions (Infrastructure as Code)

**Structure**:
```
stacks/
├── __init__.py
├── main_stack.py             # Main orchestration stack
├── web_app_stack.py          # Nested stack #1
├── database_stack.py         # Nested stack #2
├── api_stack.py              # Nested stack #3
└── monitoring_stack.py       # Nested stack #4
```

**When to create**:
- One file per nested stack
- Each stack encapsulates a logical component (web app, database, API, etc.)

**Example - Adding a database stack**:
```bash
touch stacks/database_stack.py
# Then import in main_stack.py
```

---

### Resources (`resources/`)

**Purpose**: Store configurations for other AWS resources

**What goes here**:
- CloudFormation templates
- Lambda layers
- Custom resource handlers
- Step Functions definitions
- EventBridge rule configurations
- Any non-Lambda resource definitions

**Structure** (example):
```
resources/
├── README.md
├── lambda_layers/
│   └── common_layer/
│       └── python/
│           └── lib/
├── step_functions/
│   └── workflow_definition.json
├── eventbridge/
│   └── rules/
└── cloudformation/
    └── custom_templates/
```

**When to create**:
- When adding Lambda layers
- When defining Step Functions
- When configuring EventBridge rules
- Any other AWS resource that needs configuration files

---

### Configuration (`config/`)

**Purpose**: Environment-specific configurations

**Structure**:
```
config/
├── __init__.py
└── environments.py    # Dev, Staging, Prod configs
```

**What goes here**:
- Environment definitions (dev, staging, prod)
- Lambda configurations (memory, timeout, etc.)
- Widget configurations (Connect credentials, branding)
- CORS policies
- Any environment-specific settings

---

### Documentation (`docs/`)

**Purpose**: All project documentation

**Files**:
- `INDEX.md` - Documentation navigation
- `README.md` - Complete deployment guide
- `QUICKSTART.md` - Quick start guide
- `ARCHITECTURE.md` - Architecture documentation
- `DEPLOYMENT_CHECKLIST.md` - Deployment checklist
- `NESTED_STACK_TEMPLATE.md` - Adding nested stacks
- `CONNECT_CONFIGURATION.md` - Connect configuration

**When to add**:
- New deployment guides
- Architecture changes
- Troubleshooting guides
- Best practices

---

## Adding New Resources

### Adding a New Lambda Function

**1. Create Lambda directory**:
```bash
mkdir -p lambda_functions/my_new_function
```

**2. Create handler**:
```python
# lambda_functions/my_new_function/lambda_function.py
def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': 'Hello from new function'
    }
```

**3. Create/update nested stack**:
```python
# stacks/my_new_stack.py
class MyNewStack(NestedStack):
    def __init__(self, ...):
        lambda_code_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "lambda_functions",
            "my_new_function"  # ← Your function directory
        )

        self.my_function = lambda_.Function(
            self,
            "MyNewFunction",
            code=lambda_.Code.from_asset(lambda_code_path),
            handler="lambda_function.lambda_handler",
            # ... other config
        )
```

**4. Import in main stack**:
```python
# stacks/main_stack.py
from .my_new_stack import MyNewStack

# In __init__:
self.my_new_stack = MyNewStack(...)
```

---

### Adding Other Resources

**Lambda Layer**:
```bash
mkdir -p resources/lambda_layers/common_layer/python/lib
# Add packages to python/lib directory
```

**Step Functions**:
```bash
mkdir -p resources/step_functions
# Create workflow JSON files
```

**EventBridge Rules**:
```bash
mkdir -p resources/eventbridge/rules
# Create rule configuration files
```

---

## Why This Organization?

### Benefits

✅ **Clear Separation**: Each resource type has its own directory
✅ **Scalable**: Easy to add new Lambdas, stacks, or resources
✅ **Maintainable**: Find code quickly by resource type
✅ **Team-Friendly**: Multiple developers can work without conflicts
✅ **CDK Best Practice**: Aligns with AWS CDK recommended structure

### Consistency

All resources follow the same pattern:
- Lambda functions → `lambda_functions/`
- Stack definitions → `stacks/`
- Other resources → `resources/`
- Configuration → `config/`
- Documentation → `docs/`

---

## Current Resources

### Lambda Functions
1. **chat_widget** - 211 Chat Widget web application
   - Location: `lambda_functions/chat_widget/`
   - Handler: `lambda_function.lambda_handler`
   - Stack: `web_app_stack.py`

### Stacks
1. **ProjectMainStack** - Main orchestration stack
2. **WebAppStack** - Chat widget nested stack

### Configuration
- **environments.py** - Dev, Staging, Prod configurations

---

## Future Additions

When adding new components:

1. **Database** → Create `stacks/database_stack.py`
2. **API** → Create `lambda_functions/api_handler/` + `stacks/api_stack.py`
3. **Lambda Layer** → Create `resources/lambda_layers/common/`
4. **Step Function** → Create `resources/step_functions/workflow.json` + stack code
5. **Monitoring** → Create `stacks/monitoring_stack.py`

---

**This organization makes your project scalable and maintainable!** 🏗️
