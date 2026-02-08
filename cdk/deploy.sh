#!/bin/bash
# Deployment script for Unix/Linux/Mac
# Usage: ./deploy.sh [environment] [action]
# Example: ./deploy.sh dev deploy
# Example: ./deploy.sh prod synth

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
ENVIRONMENT=${1:-dev}
ACTION=${2:-deploy}

echo -e "${BLUE}=====================================${NC}"
echo -e "${BLUE}  211 Chat Widget CDK Deployment${NC}"
echo -e "${BLUE}=====================================${NC}"
echo -e "Environment: ${GREEN}${ENVIRONMENT}${NC}"
echo -e "Action: ${GREEN}${ACTION}${NC}"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi

# Check if AWS CLI is configured
if ! aws sts get-caller-identity &> /dev/null; then
    echo -e "${RED}Error: AWS CLI is not configured or credentials are invalid${NC}"
    exit 1
fi

echo -e "${GREEN}✓ AWS credentials valid${NC}"
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REGION=$(aws configure get region || echo "us-west-2")
echo -e "Account: ${YELLOW}${ACCOUNT_ID}${NC}"
echo -e "Region: ${YELLOW}${REGION}${NC}"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${BLUE}Creating Python virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

# Install/upgrade dependencies
echo -e "${BLUE}Installing dependencies...${NC}"
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Bootstrap CDK (if needed)
if [ "$ACTION" = "bootstrap" ]; then
    echo -e "${BLUE}Bootstrapping CDK in ${REGION}...${NC}"
    cdk bootstrap aws://${ACCOUNT_ID}/${REGION}
    echo -e "${GREEN}✓ Bootstrap complete${NC}"
    exit 0
fi

# Set environment variables
export CDK_DEFAULT_ACCOUNT=${ACCOUNT_ID}
export CDK_DEFAULT_REGION=${REGION}
export CDK_ENVIRONMENT=${ENVIRONMENT}

# Execute CDK command
case $ACTION in
    synth)
        echo -e "${BLUE}Synthesizing CloudFormation template...${NC}"
        cdk synth -c environment=${ENVIRONMENT}
        ;;
    diff)
        echo -e "${BLUE}Comparing deployed stack with current configuration...${NC}"
        cdk diff -c environment=${ENVIRONMENT}
        ;;
    deploy)
        echo -e "${BLUE}Deploying stack...${NC}"
        cdk deploy -c environment=${ENVIRONMENT} --require-approval never
        DEPLOY_STATUS=$?

        if [ $DEPLOY_STATUS -eq 0 ]; then
            echo -e "${GREEN}✓ Deployment complete!${NC}"
            echo ""
            echo -e "${YELLOW}Function URL:${NC}"
            aws cloudformation describe-stacks \
                --stack-name Project-$(echo ${ENVIRONMENT} | sed 's/.*/\u&/') \
                --query "Stacks[0].Outputs[?OutputKey=='WebAppUrl'].OutputValue" \
                --output text

            # Run post-deployment hook
            echo ""
            if [ -f "scripts/post_deploy.sh" ]; then
                chmod +x scripts/post_deploy.sh
                scripts/post_deploy.sh ${ENVIRONMENT}
            fi
        else
            echo -e "${RED}✗ Deployment failed!${NC}"
            exit $DEPLOY_STATUS
        fi
        ;;
    destroy)
        echo -e "${RED}WARNING: This will destroy all resources in ${ENVIRONMENT}${NC}"
        read -p "Are you sure? Type 'yes' to confirm: " -r
        if [[ $REPLY = "yes" ]]; then
            cdk destroy -c environment=${ENVIRONMENT} --force
            echo -e "${GREEN}✓ Resources destroyed${NC}"
        else
            echo -e "${YELLOW}Cancelled${NC}"
        fi
        ;;
    *)
        echo -e "${RED}Unknown action: ${ACTION}${NC}"
        echo "Valid actions: synth, diff, deploy, destroy, bootstrap"
        exit 1
        ;;
esac

deactivate
echo -e "${GREEN}✓ Done!${NC}"
