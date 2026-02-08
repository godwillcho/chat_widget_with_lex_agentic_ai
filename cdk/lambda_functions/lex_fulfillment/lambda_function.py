"""
Lex Bot Fulfillment Lambda - Yes/No Card Generator
Creates dynamic Yes/No cards and handles responses.
"""
import json
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def create_yes_no_cards(question_text=None):
    """
    Create Yes/No response cards for Lex.

    Returns:
        dict: ImageResponseCard with Yes/No buttons
    """
    if not question_text:
        question_text = os.environ.get('QUESTION_TEXT', 'Would you like to continue?')

    return {
        'contentType': 'ImageResponseCard',
        'imageResponseCard': {
            'title': question_text,
            'subtitle': 'Please select an option',
            'buttons': [
                {
                    'text': 'Yes',
                    'value': 'yes'
                },
                {
                    'text': 'No',
                    'value': 'no'
                }
            ]
        }
    }


def lambda_handler(event, context):
    """
    Handle Lex bot code hook requests.

    Invocation types:
    - DialogCodeHook: Called during conversation (elicit slot)
    - FulfillmentCodeHook: Called when ready to fulfill intent
    """
    logger.info(f"Received event: {json.dumps(event)}")

    # Extract key information
    invocation_source = event.get('invocationSource')
    session_state = event.get('sessionState', {})
    intent = session_state.get('intent', {})
    intent_name = intent.get('name', '')
    slots = intent.get('slots', {})
    session_attributes = session_state.get('sessionAttributes', {})

    # Get Yes/No slot value
    yes_no_slot = slots.get('YesNoResponse', {})
    yes_no_value = None

    if yes_no_slot and yes_no_slot.get('value'):
        yes_no_value = yes_no_slot['value'].get('interpretedValue', '').lower()

    logger.info(f"Invocation: {invocation_source}, Intent: {intent_name}, Response: {yes_no_value}")

    # ═══════════════════════════════════════════════════════════
    # DIALOG CODE HOOK - Show Yes/No Cards
    # ═══════════════════════════════════════════════════════════
    if invocation_source == 'DialogCodeHook':
        # If slot is not filled, show the cards
        if not yes_no_value:
            return {
                'sessionState': {
                    'dialogAction': {
                        'type': 'ElicitSlot',
                        'slotToElicit': 'YesNoResponse'
                    },
                    'intent': intent,
                    'sessionAttributes': session_attributes
                },
                'messages': [
                    create_yes_no_cards()
                ]
            }

        # Slot is filled, delegate to Lex to continue
        return {
            'sessionState': {
                'dialogAction': {
                    'type': 'Delegate'
                },
                'intent': intent,
                'sessionAttributes': session_attributes
            }
        }

    # ═══════════════════════════════════════════════════════════
    # FULFILLMENT CODE HOOK - Process Response
    # ═══════════════════════════════════════════════════════════
    if invocation_source == 'FulfillmentCodeHook':
        # Process the Yes/No response
        if yes_no_value in ['yes', 'yeah', 'sure', 'okay', 'yep', 'y']:
            response_message = "Great! I'll help you with your request."
            # Add your custom logic here for YES response
            # Example: Update database, trigger workflow, etc.
            session_attributes['user_response'] = 'yes'
            session_attributes['action'] = 'proceed'

        elif yes_no_value in ['no', 'nope', 'not really', 'nah', 'n']:
            response_message = "Understood. Is there anything else I can help you with?"
            # Add your custom logic here for NO response
            session_attributes['user_response'] = 'no'
            session_attributes['action'] = 'cancel'

        else:
            # Unrecognized response - ask again with cards
            return {
                'sessionState': {
                    'dialogAction': {
                        'type': 'ElicitSlot',
                        'slotToElicit': 'YesNoResponse'
                    },
                    'intent': intent,
                    'sessionAttributes': session_attributes
                },
                'messages': [
                    {
                        'contentType': 'PlainText',
                        'content': "I didn't understand that. Please select Yes or No."
                    },
                    create_yes_no_cards()
                ]
            }

        # Mark intent as fulfilled
        intent['state'] = 'Fulfilled'

        return {
            'sessionState': {
                'dialogAction': {
                    'type': 'Close'
                },
                'intent': intent,
                'sessionAttributes': session_attributes
            },
            'messages': [
                {
                    'contentType': 'PlainText',
                    'content': response_message
                }
            ]
        }

    # Default response
    return {
        'sessionState': {
            'dialogAction': {
                'type': 'Close'
            },
            'intent': intent,
            'sessionAttributes': session_attributes
        },
        'messages': [
            {
                'contentType': 'PlainText',
                'content': 'Something went wrong. Please try again.'
            }
        ]
    }
