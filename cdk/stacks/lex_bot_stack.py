"""
Nested Stack: Amazon Lex Bot
Creates a Lex bot that shows Yes/No cards for configured questions.
"""
from aws_cdk import (
    NestedStack,
    Duration,
    CfnOutput,
    RemovalPolicy,
)
from aws_cdk import aws_lex as lex
from aws_cdk import aws_iam as iam
from aws_cdk import aws_logs as logs
from aws_cdk import aws_lambda as lambda_
from constructs import Construct
import os


class LexBotStack(NestedStack):
    """
    Amazon Lex Bot Nested Stack - Yes/No Question Bot.

    Creates:
    - Lex V2 Bot with Yes/No question capability
    - Bot locale configuration (en_US)
    - Intent for handling Yes/No responses
    - IAM role for Lex bot
    - CloudWatch Logs for bot conversations
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        environment_name: str,
        lex_config: dict,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Extract configuration
        question_text = lex_config.get("question_text", "Would you like to continue?")
        bot_name = f"YesNoBot-{environment_name}"
        idle_session_timeout = lex_config.get("idle_session_timeout", 300)

        # ═══════════════════════════════════════════════════════════
        # LAMBDA FUNCTION FOR LEX FULFILLMENT (CODE HOOK)
        # ═══════════════════════════════════════════════════════════
        lambda_code_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "lambda_functions",
            "lex_fulfillment"
        )

        self.fulfillment_function = lambda_.Function(
            self,
            "LexFulfillmentFunction",
            function_name=f"lex-yesno-fulfillment-{environment_name}",
            runtime=lambda_.Runtime.PYTHON_3_11,
            handler="lambda_function.lambda_handler",
            code=lambda_.Code.from_asset(lambda_code_path),
            memory_size=256,
            timeout=Duration.seconds(30),
            environment={
                'QUESTION_TEXT': question_text,
            },
            description=f"Lex bot fulfillment for Yes/No responses - {environment_name}",
            log_retention=logs.RetentionDays.ONE_WEEK,
        )

        # ═══════════════════════════════════════════════════════════
        # GRANT LEX PERMISSION TO INVOKE LAMBDA
        # ═══════════════════════════════════════════════════════════
        self.fulfillment_function.grant_invoke(iam.ServicePrincipal("lexv2.amazonaws.com"))

        # Add resource-based policy to allow Lex to invoke Lambda
        self.fulfillment_function.add_permission(
            "AllowLexInvoke",
            principal=iam.ServicePrincipal("lexv2.amazonaws.com"),
            action="lambda:InvokeFunction",
        )

        # ═══════════════════════════════════════════════════════════
        # IAM ROLE FOR LEX BOT
        # ═══════════════════════════════════════════════════════════
        bot_role = iam.Role(
            self,
            "LexBotRole",
            assumed_by=iam.ServicePrincipal("lexv2.amazonaws.com"),
            description=f"Service role for Lex bot - {environment_name}",
        )

        # Add CloudWatch Logs permissions
        bot_role.add_to_policy(
            iam.PolicyStatement(
                actions=[
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents",
                ],
                resources=["*"],
            )
        )

        # ═══════════════════════════════════════════════════════════
        # LEX BOT
        # ═══════════════════════════════════════════════════════════
        self.bot = lex.CfnBot(
            self,
            "YesNoBot",
            name=bot_name,
            role_arn=bot_role.role_arn,
            data_privacy={"ChildDirected": False},
            idle_session_ttl_in_seconds=idle_session_timeout,
            description=f"Yes/No question bot for {environment_name} environment",
            bot_locales=[
                lex.CfnBot.BotLocaleProperty(
                    locale_id="en_US",
                    nlu_confidence_threshold=0.4,
                    description="English (US) locale for Yes/No bot",
                    voice_settings=lex.CfnBot.VoiceSettingsProperty(
                        voice_id="Joanna"  # AWS Polly voice
                    ),
                    # Define Yes/No intent
                    intents=[
                        # Fallback intent (required)
                        lex.CfnBot.IntentProperty(
                            name="FallbackIntent",
                            description="Default fallback intent",
                            parent_intent_signature="AMAZON.FallbackIntent",
                            intent_closing_setting=lex.CfnBot.IntentClosingSettingProperty(
                                closing_response=lex.CfnBot.ResponseSpecificationProperty(
                                    message_groups_list=[
                                        lex.CfnBot.MessageGroupProperty(
                                            message=lex.CfnBot.MessageProperty(
                                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                    value="I didn't understand that. Please answer Yes or No."
                                                )
                                            )
                                        )
                                    ]
                                )
                            ),
                        ),
                        # Yes/No Question Intent
                        lex.CfnBot.IntentProperty(
                            name="YesNoQuestionIntent",
                            description="Intent to handle Yes/No responses",
                            sample_utterances=[
                                lex.CfnBot.SampleUtteranceProperty(utterance="Yes"),
                                lex.CfnBot.SampleUtteranceProperty(utterance="No"),
                                lex.CfnBot.SampleUtteranceProperty(utterance="Yeah"),
                                lex.CfnBot.SampleUtteranceProperty(utterance="Nope"),
                                lex.CfnBot.SampleUtteranceProperty(utterance="Sure"),
                                lex.CfnBot.SampleUtteranceProperty(utterance="Okay"),
                                lex.CfnBot.SampleUtteranceProperty(utterance="Not really"),
                                lex.CfnBot.SampleUtteranceProperty(utterance="I agree"),
                                lex.CfnBot.SampleUtteranceProperty(utterance="I don't agree"),
                            ],
                            # Slot for capturing Yes/No response
                            slots=[
                                lex.CfnBot.SlotProperty(
                                    name="YesNoResponse",
                                    description="Captures Yes or No response",
                                    slot_type_name="AMAZON.AlphaNumeric",
                                    value_elicitation_setting=lex.CfnBot.SlotValueElicitationSettingProperty(
                                        slot_constraint="Required",
                                        # Cards are generated by Lambda code hook, not here
                                        prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                                            max_retries=2,
                                            message_groups_list=[
                                                lex.CfnBot.MessageGroupProperty(
                                                    message=lex.CfnBot.MessageProperty(
                                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                            value="Please answer Yes or No."
                                                        )
                                                    )
                                                )
                                            ]
                                        )
                                    )
                                )
                            ],
                            # Intent confirmation (optional)
                            intent_confirmation_setting=lex.CfnBot.IntentConfirmationSettingProperty(
                                prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                                    max_retries=2,
                                    message_groups_list=[
                                        lex.CfnBot.MessageGroupProperty(
                                            message=lex.CfnBot.MessageProperty(
                                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                    value="You selected {YesNoResponse}. Is that correct?"
                                                )
                                            )
                                        )
                                    ]
                                ),
                                declination_response=lex.CfnBot.ResponseSpecificationProperty(
                                    message_groups_list=[
                                        lex.CfnBot.MessageGroupProperty(
                                            message=lex.CfnBot.MessageProperty(
                                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                    value="Okay, let me ask again."
                                                )
                                            )
                                        )
                                    ]
                                ),
                            ) if lex_config.get("enable_confirmation", False) else None,
                            # Dialog Code Hook (Lambda - generates cards during conversation)
                            dialog_code_hook=lex.CfnBot.DialogCodeHookSettingProperty(
                                enabled=True
                            ),
                            # Fulfillment Code Hook (Lambda - processes final response)
                            fulfillment_code_hook=lex.CfnBot.FulfillmentCodeHookSettingProperty(
                                enabled=True,
                            ),
                            # Closing response (used when code hook is not enabled or after fulfillment)
                            intent_closing_setting=lex.CfnBot.IntentClosingSettingProperty(
                                closing_response=lex.CfnBot.ResponseSpecificationProperty(
                                    message_groups_list=[
                                        lex.CfnBot.MessageGroupProperty(
                                            message=lex.CfnBot.MessageProperty(
                                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                                    value="Thank you for your response!"
                                                )
                                            )
                                        )
                                    ]
                                ),
                                is_active=False  # Don't use closing response when code hook is active
                            ),
                        ),
                    ],
                    # Slot types (if custom slots are needed)
                    slot_types=[],
                )
            ],
        )

        # ═══════════════════════════════════════════════════════════
        # BOT VERSION
        # ═══════════════════════════════════════════════════════════
        bot_version = lex.CfnBotVersion(
            self,
            "BotVersion",
            bot_id=self.bot.ref,
            bot_version_locale_specification=[
                lex.CfnBotVersion.BotVersionLocaleSpecificationProperty(
                    bot_version_locale_details=lex.CfnBotVersion.BotVersionLocaleDetailsProperty(
                        source_bot_version="DRAFT"
                    ),
                    locale_id="en_US"
                )
            ],
            description=f"Version 1 - {environment_name}",
        )

        # ═══════════════════════════════════════════════════════════
        # BOT ALIAS
        # ═══════════════════════════════════════════════════════════
        self.bot_alias = lex.CfnBotAlias(
            self,
            "BotAlias",
            bot_alias_name=lex_config.get("alias_name", "prod"),
            bot_id=self.bot.ref,
            bot_version=bot_version.attr_bot_version,
            description=f"Production alias for {environment_name}",
            bot_alias_locale_settings=[
                lex.CfnBotAlias.BotAliasLocaleSettingsItemProperty(
                    bot_alias_locale_setting=lex.CfnBotAlias.BotAliasLocaleSettingsProperty(
                        enabled=True,
                        # Configure Lambda for code hooks
                        code_hook_specification=lex.CfnBotAlias.CodeHookSpecificationProperty(
                            lambda_code_hook=lex.CfnBotAlias.LambdaCodeHookProperty(
                                lambda_arn=self.fulfillment_function.function_arn,
                                code_hook_interface_version="1.0"
                            )
                        )
                    ),
                    locale_id="en_US"
                )
            ],
            # Conversation logs (optional)
            conversation_log_settings=lex.CfnBotAlias.ConversationLogSettingsProperty(
                text_log_settings=[
                    lex.CfnBotAlias.TextLogSettingProperty(
                        enabled=lex_config.get("enable_conversation_logs", True),
                        destination=lex.CfnBotAlias.TextLogDestinationProperty(
                            cloud_watch=lex.CfnBotAlias.CloudWatchLogGroupLogDestinationProperty(
                                cloud_watch_log_group_arn=f"arn:aws:logs:{self.region}:{self.account}:log-group:/aws/lex/{bot_name}:*",
                                log_prefix="conversation"
                            )
                        )
                    )
                ]
            ) if lex_config.get("enable_conversation_logs", True) else None,
        )

        # ═══════════════════════════════════════════════════════════
        # OUTPUTS
        # ═══════════════════════════════════════════════════════════
        CfnOutput(
            self,
            "BotId",
            value=self.bot.ref,
            description="Lex Bot ID",
            export_name=f"LexBot-{environment_name}-BotId",
        )

        CfnOutput(
            self,
            "BotAliasId",
            value=self.bot_alias.attr_bot_alias_id,
            description="Lex Bot Alias ID",
            export_name=f"LexBot-{environment_name}-AliasId",
        )

        CfnOutput(
            self,
            "BotName",
            value=bot_name,
            description="Lex Bot Name",
        )

        CfnOutput(
            self,
            "BotLocale",
            value="en_US",
            description="Bot locale",
        )

        CfnOutput(
            self,
            "FulfillmentFunctionArn",
            value=self.fulfillment_function.function_arn,
            description="Fulfillment Lambda function ARN",
            export_name=f"LexBot-{environment_name}-FulfillmentArn",
        )

        CfnOutput(
            self,
            "FulfillmentFunctionName",
            value=self.fulfillment_function.function_name,
            description="Fulfillment Lambda function name",
        )

        # Store values for parent stack
        self.bot_id = self.bot.ref
        self.bot_alias_id = self.bot_alias.attr_bot_alias_id
        self.bot_name = bot_name
        self.fulfillment_function_arn = self.fulfillment_function.function_arn
