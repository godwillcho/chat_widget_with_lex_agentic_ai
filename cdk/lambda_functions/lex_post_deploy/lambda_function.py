"""
Post-Deployment Lambda for Lex Bot
Automatically builds bot locale and associates with Connect after deployment.
"""
import json
import logging
import time
import boto3
import urllib3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

lex = boto3.client('lexv2-models')
connect = boto3.client('connect')
lambda_client = boto3.client('lambda')
http = urllib3.PoolManager()


def send_response(event, context, response_status, response_data, physical_resource_id=None, reason=None):
    """Send response to CloudFormation"""
    response_url = event['ResponseURL']

    response_body = {
        'Status': response_status,
        'Reason': reason or f'See CloudWatch Log Stream: {context.log_stream_name}',
        'PhysicalResourceId': physical_resource_id or context.log_stream_name,
        'StackId': event['StackId'],
        'RequestId': event['RequestId'],
        'LogicalResourceId': event['LogicalResourceId'],
        'Data': response_data
    }

    json_response_body = json.dumps(response_body)

    headers = {
        'content-type': '',
        'content-length': str(len(json_response_body))
    }

    try:
        response = http.request(
            'PUT',
            response_url,
            body=json_response_body.encode('utf-8'),
            headers=headers
        )
        logger.info(f"CloudFormation response status code: {response.status}")
    except Exception as e:
        logger.error(f"Failed to send response to CloudFormation: {str(e)}")


def build_bot_locale(bot_id, locale_id='en_US', max_wait=300):
    """Build bot locale and wait for completion"""
    logger.info(f"Building bot locale {locale_id}...")

    try:
        lex.build_bot_locale(
            botId=bot_id,
            botVersion='DRAFT',
            localeId=locale_id
        )
        logger.info("Build initiated")
    except Exception as e:
        logger.error(f"Failed to initiate build: {e}")
        return False

    # Wait for build to complete
    start_time = time.time()
    while (time.time() - start_time) < max_wait:
        try:
            response = lex.describe_bot_locale(
                botId=bot_id,
                botVersion='DRAFT',
                localeId=locale_id
            )

            status = response['botLocaleStatus']
            logger.info(f"Bot locale status: {status}")

            if status == 'Built':
                logger.info("Bot locale built successfully")
                return True
            elif status in ['Failed', 'Deleting']:
                logger.error(f"Bot build failed with status: {status}")
                if 'failureReasons' in response:
                    logger.error(f"Failure reasons: {response['failureReasons']}")
                return False

            time.sleep(5)
        except Exception as e:
            logger.error(f"Error checking bot status: {e}")
            time.sleep(5)

    logger.error(f"Bot build timed out after {max_wait} seconds")
    return False


def associate_with_connect(bot_id, bot_alias_id, connect_instance_id, region, account_id):
    """Associate bot with Connect instance"""
    logger.info(f"Associating bot with Connect instance {connect_instance_id}...")

    bot_alias_arn = f"arn:aws:lex:{region}:{account_id}:bot-alias/{bot_id}/{bot_alias_id}"

    try:
        connect.associate_bot(
            InstanceId=connect_instance_id,
            LexV2Bot={'AliasArn': bot_alias_arn}
        )
        logger.info("Successfully associated bot with Connect")
        return True
    except Exception as e:
        if 'ResourceConflictException' in str(e):
            logger.info("Bot already associated with Connect")
            return True
        logger.error(f"Failed to associate bot: {e}")
        return False


def grant_connect_permission(fulfillment_function_name, connect_instance_id, region, account_id):
    """Grant Connect permission to invoke fulfillment Lambda"""
    logger.info("Granting Connect permission to invoke fulfillment Lambda...")

    try:
        lambda_client.add_permission(
            FunctionName=fulfillment_function_name,
            StatementId='AllowConnectInvoke',
            Action='lambda:InvokeFunction',
            Principal='connect.amazonaws.com',
            SourceArn=f"arn:aws:connect:{region}:{account_id}:instance/{connect_instance_id}"
        )
        logger.info("Permission granted")
        return True
    except Exception as e:
        if 'ResourceConflictException' in str(e):
            logger.info("Permission already exists")
            return True
        logger.error(f"Failed to grant permission: {e}")
        return False


def lambda_handler(event, context):
    """Handle CloudFormation custom resource requests"""
    logger.info(f"Received event: {json.dumps(event)}")

    request_type = event['RequestType']
    props = event['ResourceProperties']

    bot_id = props.get('BotId')
    bot_alias_id = props.get('BotAliasId')
    connect_instance_id = props.get('ConnectInstanceId')
    fulfillment_function_name = props.get('FulfillmentFunctionName')
    region = props.get('Region')
    account_id = props.get('AccountId')

    physical_resource_id = f"lex-post-deploy-{bot_id}"

    try:
        if request_type == 'Create' or request_type == 'Update':
            # Step 1: Build bot locale
            if not build_bot_locale(bot_id):
                send_response(
                    event,
                    context,
                    'FAILED',
                    {},
                    physical_resource_id,
                    'Bot build failed'
                )
                return

            # Step 2: Associate with Connect (if instance ID provided)
            if connect_instance_id:
                if not associate_with_connect(bot_id, bot_alias_id, connect_instance_id, region, account_id):
                    send_response(
                        event,
                        context,
                        'FAILED',
                        {},
                        physical_resource_id,
                        'Connect association failed'
                    )
                    return

                # Step 3: Grant Lambda permission
                if not grant_connect_permission(fulfillment_function_name, connect_instance_id, region, account_id):
                    logger.warning("Failed to grant Lambda permission (may already exist)")

            # Success
            send_response(
                event,
                context,
                'SUCCESS',
                {
                    'BotId': bot_id,
                    'Status': 'Bot built and associated with Connect'
                },
                physical_resource_id,
                'Post-deployment tasks completed successfully'
            )

        elif request_type == 'Delete':
            # Nothing to do on delete
            logger.info("Delete request - no action needed")
            send_response(
                event,
                context,
                'SUCCESS',
                {},
                physical_resource_id,
                'Delete completed'
            )

        else:
            logger.error(f"Unknown request type: {request_type}")
            send_response(
                event,
                context,
                'FAILED',
                {},
                physical_resource_id,
                f'Unknown request type: {request_type}'
            )

    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        send_response(
            event,
            context,
            'FAILED',
            {},
            physical_resource_id,
            str(e)
        )
