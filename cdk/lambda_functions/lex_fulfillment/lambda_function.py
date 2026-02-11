"""
Lex Bot Fulfillment Lambda - Yes/No Card Generator
Creates dynamic Yes/No cards and handles responses.
"""
import json
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def create_menu_panel():
    """
    Create initial menu Panel for Amazon Connect.

    Panel template with self-service and talk-to-agent options.

    Returns:
        dict: Amazon Connect Panel interactive message
    """
    interactive_message = {
        "templateType": "Panel",
        "version": "1.0",
        "data": {
            "content": {
                "title": "Welcome to 211 Helpline. How may I assist you today?",
                "subtitle": "Please select an option below",
                "elements": [
                    {
                        "title": "Check self-service options"
                    },
                    {
                        "title": "Talk to an agent"
                    }
                ]
            }
        }
    }

    return {
        'contentType': 'CustomPayload',
        'content': json.dumps(interactive_message)
    }


def create_yes_no_cards(question_text=None):
    """
    Create Yes/No interactive message for Amazon Connect.

    Uses Amazon Connect's QuickReply interactive message format,
    which is compatible with the Amazon Connect chat widget.
    Lex ImageResponseCard is NOT supported in Connect chat widget.

    Args:
        question_text: Custom question text. If None, uses default consent question.

    Returns:
        dict: Amazon Connect interactive message with Yes/No buttons
    """
    if not question_text:
        question_text = os.environ.get(
            'QUESTION_TEXT',
            'Do you consent to the use of your Data for identification purposes and research of resources based on your Needs?'
        )

    # Amazon Connect Interactive Message format (QuickReply template)
    # Must use CustomPayload contentType for Lex Lambda responses
    interactive_message = {
        "templateType": "QuickReply",
        "version": "1.0",
        "data": {
            "content": {
                "title": question_text,
                "elements": [
                    {
                        "title": "Yes"
                    },
                    {
                        "title": "No"
                    }
                ]
            }
        }
    }

    return {
        'contentType': 'CustomPayload',
        'content': json.dumps(interactive_message)
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

    # Get custom question text from session attributes (if provided)
    question_text = session_attributes.get('question_text', None)

    # Get start option from session attributes
    # Options: 'menu' (default) or 'yes_no' (skip menu, go directly to consent cards)
    start_option = session_attributes.get('start_option', 'menu')

    # Get Yes/No slot value
    yes_no_slot = slots.get('YesNoResponse', {})
    yes_no_value = None

    if yes_no_slot and yes_no_slot.get('value'):
        yes_no_value = yes_no_slot['value'].get('interpretedValue', '').lower()

    logger.info(f"Invocation: {invocation_source}, Intent: {intent_name}, Response: {yes_no_value}")

    # ═══════════════════════════════════════════════════════════
    # DIALOG CODE HOOK - Show Menu Panel or Yes/No Cards
    # ═══════════════════════════════════════════════════════════
    if invocation_source == 'DialogCodeHook':
        # Check menu selection status
        menu_selection = session_attributes.get('menu_selection', None)
        input_transcript = event.get('inputTranscript', '').lower().strip()

        # ──────────────────────────────────────────────────────────
        # STAGE 1: Initial entry - Check start_option to determine flow
        # ──────────────────────────────────────────────────────────
        if not menu_selection:
            logger.info(f"No menu selection - start_option: {start_option}, input: {input_transcript}")

            # Option 1: Start directly with Yes/No cards (skip menu)
            if start_option == 'yes_no':
                logger.info("start_option=yes_no - showing Yes/No cards directly")
                session_attributes['menu_selection'] = 'self-service'
                session_attributes['cards_shown'] = 'false'
                # Return with Yes/No cards immediately
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
                        create_yes_no_cards(question_text)
                    ]
                }

            # Option 2: Start with menu panel (default)
            # Check if user clicked a Panel button or typed a menu option
            # Panel button sends the exact title text
            if input_transcript == 'check self-service options' or ('self' in input_transcript and 'service' in input_transcript):
                logger.info("User selected self-service option - showing Yes/No cards")
                session_attributes['menu_selection'] = 'self-service'
                session_attributes['cards_shown'] = 'false'
                # Return with Yes/No cards immediately
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
                        create_yes_no_cards(question_text)
                    ]
                }
            elif input_transcript == 'talk to an agent' or 'agent' in input_transcript or 'talk' in input_transcript:
                logger.info("User selected talk to agent - fulfilling immediately")
                session_attributes['menu_selection'] = 'talk-to-agent'
                # Fill slot and delegate to fulfillment
                slots['YesNoResponse'] = {
                    'shape': 'Scalar',
                    'value': {
                        'originalValue': 'agent',
                        'interpretedValue': 'agent',
                        'resolvedValues': ['agent']
                    }
                }
                intent['slots'] = slots
                intent['state'] = 'ReadyForFulfillment'
                return {
                    'sessionState': {
                        'dialogAction': {
                            'type': 'Delegate'
                        },
                        'intent': intent,
                        'sessionAttributes': session_attributes
                    }
                }
            else:
                # First invocation or unrecognized input - show Panel menu (default flow)
                logger.info("start_option=menu (default) - showing Panel menu")
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
                        create_menu_panel()
                    ]
                }

        # ──────────────────────────────────────────────────────────
        # STAGE 2: User selected "Talk to an agent" - skip to fulfillment
        # ──────────────────────────────────────────────────────────
        if menu_selection == 'talk-to-agent':
            logger.info("Menu selection: talk-to-agent - fulfilling immediately")
            # Fill slot with placeholder and delegate to fulfillment
            slots['YesNoResponse'] = {
                'shape': 'Scalar',
                'value': {
                    'originalValue': 'agent',
                    'interpretedValue': 'agent',
                    'resolvedValues': ['agent']
                }
            }
            intent['slots'] = slots
            intent['state'] = 'ReadyForFulfillment'
            return {
                'sessionState': {
                    'dialogAction': {
                        'type': 'Delegate'
                    },
                    'intent': intent,
                    'sessionAttributes': session_attributes
                }
            }

        # ──────────────────────────────────────────────────────────
        # STAGE 3: User selected "Self-service" - process Yes/No response
        # ──────────────────────────────────────────────────────────
        if menu_selection == 'self-service':
            logger.info(f"Menu selection: self-service - processing response: {input_transcript}")

            # If slot is not filled, check if user typed a yes/no response
            if not yes_no_value:
                # Cards already shown - check if user typed yes or no (or clicked card)
                if input_transcript in ['yes', 'yeah', 'sure', 'okay', 'yep', 'y', 'ye']:
                    logger.info(f"User selected YES via input: {input_transcript}")
                    # Manually fill the slot with 'yes'
                    slots['YesNoResponse'] = {
                        'shape': 'Scalar',
                        'value': {
                            'originalValue': input_transcript,
                            'interpretedValue': 'yes',
                            'resolvedValues': ['yes']
                        }
                    }
                    intent['slots'] = slots
                    intent['state'] = 'ReadyForFulfillment'

                    # Clear the cards_shown flag for next time
                    session_attributes['cards_shown'] = 'false'

                    # Delegate to fulfillment
                    return {
                        'sessionState': {
                            'dialogAction': {
                                'type': 'Delegate'
                            },
                            'intent': intent,
                            'sessionAttributes': session_attributes
                        }
                    }

                elif input_transcript in ['no', 'nope', 'not really', 'nah', 'n', 'nop']:
                    logger.info(f"User selected NO via input: {input_transcript}")
                    # Manually fill the slot with 'no'
                    slots['YesNoResponse'] = {
                        'shape': 'Scalar',
                        'value': {
                            'originalValue': input_transcript,
                            'interpretedValue': 'no',
                            'resolvedValues': ['no']
                        }
                    }
                    intent['slots'] = slots
                    intent['state'] = 'ReadyForFulfillment'

                    # Clear the cards_shown flag for next time
                    session_attributes['cards_shown'] = 'false'

                    # Delegate to fulfillment
                    return {
                        'sessionState': {
                            'dialogAction': {
                                'type': 'Delegate'
                            },
                            'intent': intent,
                            'sessionAttributes': session_attributes
                        }
                    }

                # User didn't type yes/no after cards were shown - ask again
                logger.info("No yes/no detected after cards shown, showing cards again")
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
                        create_yes_no_cards(question_text)
                    ]
                }

            # Slot is filled, delegate to Lex to continue
            logger.info(f"Slot already filled with: {yes_no_value}, delegating")
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
        # Check if user selected "Talk to an agent" from menu
        if yes_no_value == 'agent':
            logger.info("User selected 'Talk to an agent' - fulfilling to route to agent")
            session_attributes['user_response'] = 'agent'
            session_attributes['action'] = 'talk-to-agent'

            # Mark intent as fulfilled
            intent['state'] = 'Fulfilled'

            # Return with NO message - Amazon Connect routes to agent
            return {
                'sessionState': {
                    'dialogAction': {
                        'type': 'Close'
                    },
                    'intent': intent,
                    'sessionAttributes': session_attributes
                }
            }

        # Process the Yes/No consent response (from self-service path)
        if yes_no_value in ['yes', 'yeah', 'sure', 'okay', 'yep', 'y']:
            # User consented - store response and fulfill intent
            session_attributes['user_response'] = 'yes'
            session_attributes['action'] = 'proceed'

            # Mark intent as fulfilled
            intent['state'] = 'Fulfilled'

            # Return with NO message - Amazon Connect takes control
            return {
                'sessionState': {
                    'dialogAction': {
                        'type': 'Close'
                    },
                    'intent': intent,
                    'sessionAttributes': session_attributes
                }
            }

        elif yes_no_value in ['no', 'nope', 'not really', 'nah', 'n']:
            # User declined - store response and fulfill intent
            session_attributes['user_response'] = 'no'
            session_attributes['action'] = 'cancel'

            # Mark intent as fulfilled
            intent['state'] = 'Fulfilled'

            # Return with NO message - Amazon Connect takes control
            return {
                'sessionState': {
                    'dialogAction': {
                        'type': 'Close'
                    },
                    'intent': intent,
                    'sessionAttributes': session_attributes
                }
            }

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
                    create_yes_no_cards(question_text)
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
