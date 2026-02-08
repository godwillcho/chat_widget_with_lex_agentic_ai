# PowerShell deployment script for Windows
# Usage: .\deploy.ps1 -Environment dev -Action deploy
# Example: .\deploy.ps1 -Environment prod -Action synth

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet('dev', 'staging', 'prod')]
    [string]$Environment = 'dev',

    [Parameter(Mandatory=$false)]
    [ValidateSet('synth', 'diff', 'deploy', 'destroy', 'bootstrap')]
    [string]$Action = 'deploy'
)

Write-Host "=====================================" -ForegroundColor Blue
Write-Host "  211 Chat Widget CDK Deployment" -ForegroundColor Blue
Write-Host "=====================================" -ForegroundColor Blue
Write-Host "Environment: $Environment" -ForegroundColor Green
Write-Host "Action: $Action" -ForegroundColor Green
Write-Host ""

# Check if Python is installed
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Python is not installed" -ForegroundColor Red
    exit 1
}

# Check if AWS CLI is configured
try {
    $null = aws sts get-caller-identity 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "AWS CLI not configured"
    }
} catch {
    Write-Host "Error: AWS CLI is not configured or credentials are invalid" -ForegroundColor Red
    exit 1
}

Write-Host "✓ AWS credentials valid" -ForegroundColor Green
$AccountId = (aws sts get-caller-identity --query Account --output text)
$Region = (aws configure get region)
if (-not $Region) { $Region = "us-west-2" }
Write-Host "Account: $AccountId" -ForegroundColor Yellow
Write-Host "Region: $Region" -ForegroundColor Yellow
Write-Host ""

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "Creating Python virtual environment..." -ForegroundColor Blue
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Blue
& ".\venv\Scripts\Activate.ps1"

# Install/upgrade dependencies
Write-Host "Installing dependencies..." -ForegroundColor Blue
python -m pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

# Bootstrap CDK (if needed)
if ($Action -eq "bootstrap") {
    Write-Host "Bootstrapping CDK in ${Region}..." -ForegroundColor Blue
    cdk bootstrap "aws://${AccountId}/${Region}"
    Write-Host "✓ Bootstrap complete" -ForegroundColor Green
    exit 0
}

# Set environment variables
$env:CDK_DEFAULT_ACCOUNT = $AccountId
$env:CDK_DEFAULT_REGION = $Region
$env:CDK_ENVIRONMENT = $Environment

# Execute CDK command
switch ($Action) {
    "synth" {
        Write-Host "Synthesizing CloudFormation template..." -ForegroundColor Blue
        cdk synth -c environment=$Environment
    }
    "diff" {
        Write-Host "Comparing deployed stack with current configuration..." -ForegroundColor Blue
        cdk diff -c environment=$Environment
    }
    "deploy" {
        Write-Host "Deploying stack..." -ForegroundColor Blue
        cdk deploy -c environment=$Environment --require-approval never
        Write-Host "✓ Deployment complete!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Function URL:" -ForegroundColor Yellow
        $StackName = "ChatWidget-$($Environment.Substring(0,1).ToUpper() + $Environment.Substring(1))"
        aws cloudformation describe-stacks `
            --stack-name $StackName `
            --query "Stacks[0].Outputs[?OutputKey=='WidgetUrl'].OutputValue" `
            --output text
    }
    "destroy" {
        Write-Host "WARNING: This will destroy all resources in $Environment" -ForegroundColor Red
        $confirmation = Read-Host "Are you sure? Type 'yes' to confirm"
        if ($confirmation -eq "yes") {
            cdk destroy -c environment=$Environment --force
            Write-Host "✓ Resources destroyed" -ForegroundColor Green
        } else {
            Write-Host "Cancelled" -ForegroundColor Yellow
        }
    }
}

deactivate
Write-Host "✓ Done!" -ForegroundColor Green
