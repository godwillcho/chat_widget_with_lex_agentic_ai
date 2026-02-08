#!/usr/bin/env python3
"""
CDK App Entry Point
Multi-environment deployment for the entire project with nested stacks.

This app creates a main stack that orchestrates multiple nested stacks:
- Web App Stack (Chat Widget Lambda)
- [Future] Database Stack
- [Future] API Stack
- [Future] Monitoring Stack
"""
import os
from aws_cdk import App, Environment, Tags
from stacks.main_stack import ProjectMainStack
from config.environments import get_environment_config

app = App()

# Get environment from context or default to 'dev'
env_name = app.node.try_get_context("environment") or os.environ.get("CDK_ENVIRONMENT", "dev")
config = get_environment_config(env_name)

# Create AWS environment (use config region, not CDK_DEFAULT_REGION)
aws_env = Environment(
    account=os.environ.get("CDK_DEFAULT_ACCOUNT"),
    region=config["aws_region"]  # Always use configured region from environments.py
)

# Deploy main stack (orchestrates all nested stacks)
main_stack = ProjectMainStack(
    app,
    f"Project-{config['stack_name_suffix']}",
    env=aws_env,
    environment_name=env_name,
    config=config,
    description=f"Main Project Infrastructure - {env_name.upper()} environment (orchestrates nested stacks)"
)

# Add project-level tags for resource management
Tags.of(app).add("Project", "211ChatWidget")
Tags.of(app).add("Environment", env_name)
Tags.of(app).add("ManagedBy", "CDK")
Tags.of(app).add("CostCenter", config.get("cost_center", "211Helpline"))
Tags.of(app).add("Owner", config.get("owner", "Infrastructure Team"))

app.synth()
