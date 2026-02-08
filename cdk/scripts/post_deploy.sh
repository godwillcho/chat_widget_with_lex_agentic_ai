#!/bin/bash
#
# Post-Deployment Hook
# Runs automatically after successful CDK deployment
#
# This script updates the Amazon Connect widget's allowed origins
# to match the environment configuration.

set -e

ENVIRONMENT=$1

if [ -z "$ENVIRONMENT" ]; then
    echo "Usage: $0 <environment>"
    exit 1
fi

echo ""
echo "=========================================================================="
echo "POST-DEPLOYMENT: Updating widget allowed origins"
echo "=========================================================================="
echo ""

# Run the Python script to update domains
python scripts/update_widget_domains.py --environment "$ENVIRONMENT"

echo ""
echo "=========================================================================="
echo "POST-DEPLOYMENT COMPLETE"
echo "=========================================================================="
echo ""
