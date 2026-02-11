#!/usr/bin/env python3
"""
Post-deployment setup script for Lex Bot.
Builds the bot locale and associates it with Connect.
"""
import sys
import time
import boto3

# Configuration
REGION = "us-west-2"
ENVIRONMENT = "dev"
BOT_NAME = f"YesNoBot-{ENVIRONMENT}"
CONNECT_INSTANCE_ID = "e75a053a-60c7-45f3-83f7-a24df6d3b52d"

lex = boto3.client('lexv2-models', region_name=REGION)
connect = boto3.client('connect', region_name=REGION)


def get_bot_id(bot_name):
    """Get bot ID from bot name."""
    response = lex.list_bots()
    for bot in response['botSummaries']:
        if bot['botName'] == bot_name:
            return bot['botId']
    raise Exception(f"Bot '{bot_name}' not found")


def get_bot_alias_id(bot_id):
    """Get bot alias ID."""
    response = lex.list_bot_aliases(botId=bot_id)
    for alias in response['botAliasSummaries']:
        if alias['botAliasName'] == 'prod':
            return alias['botAliasId']
    raise Exception(f"Bot alias 'prod' not found for bot {bot_id}")


def build_bot_locale(bot_id, locale_id='en_US'):
    """Build bot locale."""
    print(f"\n1. Building bot locale {locale_id}...")

    try:
        lex.build_bot_locale(
            botId=bot_id,
            botVersion='DRAFT',
            localeId=locale_id
        )
        print("   Build initiated")
    except Exception as e:
        print(f"   Error: {e}")
        return False

    # Wait for build to complete
    print("   Waiting for build to complete...", end='', flush=True)
    max_wait = 300  # 5 minutes
    start_time = time.time()

    while (time.time() - start_time) < max_wait:
        response = lex.describe_bot_locale(
            botId=bot_id,
            botVersion='DRAFT',
            localeId=locale_id
        )

        status = response['botLocaleStatus']

        if status == 'Built':
            print(" Done!")
            return True
        elif status in ['Failed', 'Deleting']:
            print(f" Failed with status: {status}")
            return False

        print(".", end='', flush=True)
        time.sleep(5)

    print(" Timed out!")
    return False


def associate_with_connect(bot_id, bot_alias_id):
    """Associate bot with Connect instance."""
    print(f"\n2. Associating bot with Connect instance {CONNECT_INSTANCE_ID}...")

    bot_alias_arn = f"arn:aws:lex:{REGION}:{boto3.client('sts').get_caller_identity()['Account']}:bot-alias/{bot_id}/{bot_alias_id}"

    try:
        connect.associate_bot(
            InstanceId=CONNECT_INSTANCE_ID,
            LexV2Bot={'AliasArn': bot_alias_arn}
        )
        print("   Successfully associated!")
        return True
    except Exception as e:
        if 'ResourceConflictException' in str(e):
            print("   Already associated")
            return True
        print(f"   Error: {e}")
        return False


def grant_connect_permission(bot_id):
    """Grant Connect permission to invoke fulfillment Lambda."""
    print(f"\n3. Granting Connect permission to invoke Lambda...")

    lambda_client = boto3.client('lambda', region_name=REGION)
    function_name = f"lex-yesno-fulfillment-{ENVIRONMENT}"

    try:
        lambda_client.add_permission(
            FunctionName=function_name,
            StatementId='AllowConnectInvoke',
            Action='lambda:InvokeFunction',
            Principal='connect.amazonaws.com',
            SourceArn=f"arn:aws:connect:{REGION}:{boto3.client('sts').get_caller_identity()['Account']}:instance/{CONNECT_INSTANCE_ID}"
        )
        print("   Permission granted!")
        return True
    except Exception as e:
        if 'ResourceConflictException' in str(e):
            print("   Permission already exists")
            return True
        print(f"   Error: {e}")
        return False


def main():
    print("=" * 60)
    print("Lex Bot Post-Deployment Setup")
    print("=" * 60)

    try:
        # Get bot ID
        print(f"\nFinding bot '{BOT_NAME}'...")
        bot_id = get_bot_id(BOT_NAME)
        print(f"   Bot ID: {bot_id}")

        # Build bot locale
        if not build_bot_locale(bot_id):
            print("\n❌ Bot build failed!")
            sys.exit(1)

        # Get bot alias ID
        print(f"\nFinding bot alias 'prod'...")
        bot_alias_id = get_bot_alias_id(bot_id)
        print(f"   Alias ID: {bot_alias_id}")

        # Associate with Connect
        if not associate_with_connect(bot_id, bot_alias_id):
            print("\n❌ Connect association failed!")
            sys.exit(1)

        # Grant Lambda permission
        if not grant_connect_permission(bot_id):
            print("\n⚠️  Lambda permission grant failed (may already exist)")

        print("\n" + "=" * 60)
        print("✅ Setup complete!")
        print("=" * 60)
        print(f"\nYour bot is now ready to use in Amazon Connect flows:")
        print(f"  Bot Name: {BOT_NAME}")
        print(f"  Bot ID: {bot_id}")
        print(f"  Alias: prod ({bot_alias_id})")
        print(f"  Connect Instance: {CONNECT_INSTANCE_ID}")
        print("\nAdd the bot to your Connect flow using the 'Get customer input' block.")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
