"""
Custom Resource Lambda - Build Lex Bot and Wait for Completion
Handles building the bot locale and waiting for it to complete.
"""
import json
import logging
import time
import boto3
import urllib3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

lex_client = boto3.client('lexv2-models')
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


def wait_for_bot_build(bot_id, locale_id, max_wait_time=300):
    """
    Wait for bot locale to finish building.

    Args:
        bot_id: The bot ID
        locale_id: The locale ID (e.g., en_US)
        max_wait_time: Maximum time to wait in seconds (default 5 minutes)

    Returns:
        True if build succeeded, False otherwise
    """
    start_time = time.time()

    while (time.time() - start_time) < max_wait_time:
        try:
            response = lex_client.describe_bot_locale(
                botId=bot_id,
                botVersion='DRAFT',
                localeId=locale_id
            )

            bot_locale_status = response['botLocaleStatus']
            logger.info(f"Bot locale status: {bot_locale_status}")

            if bot_locale_status == 'Built':
                logger.info("Bot locale build completed successfully")
                return True
            elif bot_locale_status in ['Failed', 'Deleting']:
                logger.error(f"Bot locale build failed with status: {bot_locale_status}")
                return False
            elif bot_locale_status in ['Creating', 'Building', 'ReadyExpressTesting']:
                logger.info(f"Bot is still building (status: {bot_locale_status}), waiting...")
                time.sleep(10)  # Wait 10 seconds before checking again
            else:
                logger.warning(f"Unknown bot locale status: {bot_locale_status}")
                time.sleep(10)

        except Exception as e:
            logger.error(f"Error checking bot status: {str(e)}")
            time.sleep(10)

    logger.error(f"Bot build did not complete within {max_wait_time} seconds")
    return False


def lambda_handler(event, context):
    """
    Handle CloudFormation custom resource requests.
    """
    logger.info(f"Received event: {json.dumps(event)}")

    request_type = event['RequestType']
    bot_id = event['ResourceProperties'].get('BotId')
    locale_id = event['ResourceProperties'].get('LocaleId', 'en_US')
    physical_resource_id = f"bot-build-{bot_id}-{locale_id}"

    try:
        if request_type == 'Create' or request_type == 'Update':
            # Build the bot locale
            logger.info(f"Building bot {bot_id} locale {locale_id}")

            lex_client.build_bot_locale(
                botId=bot_id,
                botVersion='DRAFT',
                localeId=locale_id
            )

            logger.info("Build initiated, waiting for completion...")

            # Wait for build to complete
            if wait_for_bot_build(bot_id, locale_id):
                send_response(
                    event,
                    context,
                    'SUCCESS',
                    {'Status': 'Bot locale built successfully'},
                    physical_resource_id,
                    'Bot build completed'
                )
            else:
                send_response(
                    event,
                    context,
                    'FAILED',
                    {},
                    physical_resource_id,
                    'Bot build failed or timed out'
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
