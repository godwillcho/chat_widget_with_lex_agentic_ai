#!/usr/bin/env python3
"""
Setup Verification Script
Checks if all prerequisites are installed and configured correctly.
"""
import sys
import subprocess
import shutil
from typing import Tuple


def check_command(command: str, min_version: str = None) -> Tuple[bool, str]:
    """Check if a command is available and optionally verify version."""
    if not shutil.which(command):
        return False, f"❌ {command} not found"

    try:
        result = subprocess.run(
            [command, "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        version_output = result.stdout + result.stderr
        return True, f"✓ {command} installed: {version_output.split()[0] if version_output else 'version unknown'}"
    except Exception as e:
        return False, f"❌ Error checking {command}: {str(e)}"


def check_aws_credentials() -> Tuple[bool, str]:
    """Check if AWS credentials are configured."""
    try:
        result = subprocess.run(
            ["aws", "sts", "get-caller-identity"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            import json
            identity = json.loads(result.stdout)
            return True, f"✓ AWS credentials valid (Account: {identity.get('Account', 'unknown')})"
        else:
            return False, f"❌ AWS credentials not configured or invalid"
    except Exception as e:
        return False, f"❌ Error checking AWS credentials: {str(e)}"


def main():
    print("=" * 60)
    print("  211 Chat Widget CDK - Setup Verification")
    print("=" * 60)
    print()

    checks = []
    all_passed = True

    # Check Python
    print("Checking Python...")
    success, message = check_command("python")
    if not success:
        success, message = check_command("python3")
    checks.append((success, message))
    print(f"  {message}")

    # Check pip
    print("\nChecking pip...")
    success, message = check_command("pip")
    checks.append((success, message))
    print(f"  {message}")

    # Check Node.js
    print("\nChecking Node.js...")
    success, message = check_command("node")
    checks.append((success, message))
    print(f"  {message}")
    if not success:
        print("  ℹ️  Download from: https://nodejs.org/")

    # Check npm
    print("\nChecking npm...")
    success, message = check_command("npm")
    checks.append((success, message))
    print(f"  {message}")

    # Check AWS CDK
    print("\nChecking AWS CDK...")
    success, message = check_command("cdk")
    checks.append((success, message))
    print(f"  {message}")
    if not success:
        print("  ℹ️  Install with: npm install -g aws-cdk")

    # Check AWS CLI
    print("\nChecking AWS CLI...")
    success, message = check_command("aws")
    checks.append((success, message))
    print(f"  {message}")

    # Check AWS Credentials
    if any(c[0] and "aws" in c[1].lower() for c in checks):
        print("\nChecking AWS Credentials...")
        success, message = check_aws_credentials()
        checks.append((success, message))
        print(f"  {message}")
        if not success:
            print("  ℹ️  Configure with: aws configure")

    # Check Python packages
    print("\nChecking Python packages...")
    try:
        import aws_cdk
        checks.append((True, f"✓ aws-cdk-lib installed ({aws_cdk.__version__})"))
        print(f"  ✓ aws-cdk-lib installed ({aws_cdk.__version__})")
    except ImportError:
        checks.append((False, "❌ aws-cdk-lib not installed"))
        print("  ❌ aws-cdk-lib not installed")
        print("  ℹ️  Run: pip install -r requirements.txt")

    # Summary
    print("\n" + "=" * 60)
    print("  Summary")
    print("=" * 60)

    passed = sum(1 for c in checks if c[0])
    total = len(checks)

    print(f"\nChecks passed: {passed}/{total}")

    if passed == total:
        print("\n✅ All checks passed! You're ready to deploy.")
        print("\nNext steps:")
        print("  1. Review config/environments.py")
        print("  2. Bootstrap CDK (first time): ./deploy.sh dev bootstrap")
        print("  3. Deploy: ./deploy.sh dev deploy")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please install missing dependencies.")
        print("\nFor detailed instructions, see: README.md")
        return 1


if __name__ == "__main__":
    sys.exit(main())
