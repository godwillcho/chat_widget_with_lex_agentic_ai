"""
view_configs.py — Static view configurations for each environment
────────────────────────────────────────────────────────────────────────────
Pre-chat form configurations loaded at deployment time (not runtime).

IMPORTANT: Use lowercase keys (inputSchema, template, actions) and objects (not strings)!

HOW TO UPDATE:
1. Get the widget script from Amazon Connect Console
2. Extract the viewConfig from the amazon_connect('viewConfig', '...') line
3. Parse the JSON and update below
4. Add field definitions to inputSchema.properties
5. Redeploy: cdk deploy -c environment=dev --require-approval never
"""

# ═══════════════════════════════════════════════════════════════════════════
# DEVELOPMENT ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════
VIEW_CONFIG_DEV = {
    "arn": "arn:aws:connect:us-west-2:551642657889:instance/e75a053a-60c7-45f3-83f7-a24df6d3b52d/view/0b286577-6474-4a95-abc9-6fef67e1521c:$LATEST",
    "id": "0b286577-6474-4a95-abc9-6fef67e1521c",
    "content": {
        "actions": [
            "ActionSelected"
        ],
        "inputSchema": {
            "type": "object",
            "properties": {
                "first-name": {
                    "type": "string",
                    "title": "First Name"
                },
                "middle-name": {
                    "type": "string",
                    "title": "Middle Initial"
                },
                "last-name": {
                    "type": "string",
                    "title": "Last Name"
                },
                "phone-number": {
                    "type": "string",
                    "title": "Phone Number"
                },
                "email": {
                    "type": "string",
                    "title": "Email",
                    "format": "email"
                }
            },
            "required": [
                "first-name",
                "last-name",
                "email"
            ],
            "$defs": {
                "ViewCondition": {
                    "$id": "/view/condition",
                    "type": "object",
                    "patternProperties": {
                        "^(MoreThan|LessThan|NotEquals|Equals|Includes)$": {
                            "type": "object",
                            "properties": {
                                "ElementByKey": {
                                    "type": "string"
                                },
                                "ElementByValue": {
                                    "anyOf": [
                                        {
                                            "type": "number"
                                        },
                                        {
                                            "type": "string"
                                        },
                                        {
                                            "type": "boolean"
                                        },
                                        {
                                            "type": "array"
                                        },
                                        {
                                            "type": "object"
                                        }
                                    ]
                                }
                            },
                            "additionalProperties": False
                        },
                        "^(AndConditions|OrConditions)$": {
                            "type": "array",
                            "items": {
                                "$ref": "/view/condition"
                            }
                        }
                    },
                    "additionalProperties": False
                }
            }
        },
        "template": {
            "Head": {
                "Configuration": {
                    "Layout": {
                        "Columns": [
                            12
                        ]
                    }
                },
                "Integrations": [],
                "Title": "CONSENT_AND_IDENTIFICATION"
            },
            "Body": [
                {
                    "_id": "StyleBlock_Professional",
                    "Type": "TextContent",
                    "Props": {},
                    "Content": [
                        "<style>* {font-family: 'Open Sans', -apple-system, sans-serif;} form {background: #fff; padding: 24px; border-radius: 12px;} h2 {color: #10264a; font-weight: 700; font-size: 1.5rem; margin-bottom: 8px;} p {color: #6b7280; font-size: 0.9rem; line-height: 1.5; margin-bottom: 20px;} label {display: block; color: #374151; font-size: 0.9rem; font-weight: 600; margin-bottom: 6px;} input[type=\"text\"], input[type=\"email\"], input[type=\"tel\"] {width: 100%; padding: 11px 14px; font-size: 0.95rem; color: #1f2937; background: #fff; border: 2px solid #d1d5db; border-radius: 8px; transition: all 0.2s ease; box-sizing: border-box; margin-bottom: 18px;} input:focus {outline: none; border-color: #10264a; box-shadow: 0 0 0 3px rgba(16,38,74,0.1);} input:hover {border-color: #9ca3af;} button {width: 100%; padding: 14px 24px; font-size: 1rem; font-weight: 600; color: #fff; background: linear-gradient(135deg, #10264a 0%, #1a3a6b 100%); border: none; border-radius: 10px; cursor: pointer; transition: all 0.3s ease; box-shadow: 0 4px 12px rgba(16,38,74,0.25); margin-top: 8px;} button:hover {background: linear-gradient(135deg, #1a3a6b 0%, #10264a 100%); box-shadow: 0 6px 16px rgba(16,38,74,0.35); transform: translateY(-2px);} button:active {transform: translateY(0); box-shadow: 0 2px 8px rgba(16,38,74,0.3);}</style>"
                    ]
                },
                {
                    "_id": "Address_1770339674464",
                    "Type": "Container",
                    "Props": {},
                    "Content": [
                        {
                            "_id": "Form_1770339805953",
                            "Type": "Form",
                            "Props": {
                                "HideBorder": False
                            },
                            "Content": [
                                {
                                    "_id": "Header_1770340308206",
                                    "Type": "Header",
                                    "Props": {
                                        "variant": "h2",
                                        "description": "By submitting this form you consent to the use of your data for identification purposes and to research resources based on your needs. All information is kept confidential."
                                    },
                                    "Content": [
                                        "Data Consent & Identification"
                                    ]
                                },
                                {
                                    "_id": "FirstName_1770340124686",
                                    "Type": "FormInput",
                                    "Props": {
                                        "Label": "First Name",
                                        "Name": "first-name",
                                        "InputType": "text"
                                    },
                                    "Content": []
                                },
                                {
                                    "_id": "FirstName_1770339805953",
                                    "Type": "FormInput",
                                    "Props": {
                                        "Label": "Middle Initial",
                                        "Name": "middle-name",
                                        "InputType": "text",
                                        "Required": False
                                    },
                                    "Content": []
                                },
                                {
                                    "_id": "LastName_1770339805953",
                                    "Type": "FormInput",
                                    "Props": {
                                        "Label": "Last Name",
                                        "Name": "last-name",
                                        "InputType": "text"
                                    },
                                    "Content": []
                                },
                                {
                                    "_id": "StreetAddress_1770339674464",
                                    "Type": "FormInput",
                                    "Props": {
                                        "Label": "Phone Number",
                                        "Name": "phone-number",
                                        "InputType": "tel",
                                        "Required": False
                                    },
                                    "Content": []
                                },
                                {
                                    "_id": "FirstName_1770340552258",
                                    "Type": "FormInput",
                                    "Props": {
                                        "Label": "Email",
                                        "Name": "email",
                                        "InputType": "email"
                                    },
                                    "Content": []
                                },
                                {
                                    "_id": "ConnectAction_1770351336556",
                                    "Type": "ConnectAction",
                                    "Props": {
                                        "ConnectActionType": "StartChatContact",
                                        "Label": "I Consent & Start Chat",
                                        "StartTaskContactProps": {
                                            "ContactFlowId": "",
                                            "TaskFields": {
                                                "Name": "",
                                                "References": {}
                                            },
                                            "Attributes": [
                                                {
                                                    "Key": "",
                                                    "Value": ""
                                                }
                                            ]
                                        },
                                        "StartEmailContactProps": {
                                            "DestinationEmailAddress": "",
                                            "ContactFlowId": "",
                                            "EmailFields": {
                                                "CustomerDisplayName": "",
                                                "CustomerEmailAddress": "",
                                                "Subject": "",
                                                "Body": ""
                                            },
                                            "Attributes": [
                                                {
                                                    "Key": "",
                                                    "Value": ""
                                                }
                                            ]
                                        },
                                        "StartChatContactProps": {
                                            "ContactFlowId": "",
                                            "ChatFields": {
                                                "CustomerDisplayName": "",
                                                "InitialMessage": ""
                                            },
                                            "Attributes": [
                                                {
                                                    "Key": "",
                                                    "Value": ""
                                                }
                                            ]
                                        }
                                    },
                                    "Content": [
                                        "Connect Action Button"
                                    ]
                                }
                            ]
                        }
                    ],
                    "Configuration": {
                        "Layout": {
                            "Columns": "12"
                        }
                    }
                }
            ]
        }
    },
    "name": "CONSENT_AND_IDENTIFICATION",
    "status": "PUBLISHED",
    "type": "CUSTOMER_MANAGED",
    "viewContentSha256": "c9f91c9e6989be67db93067367383e8749d1799dc1857a514fa27a40fee030d2"
}

# ═══════════════════════════════════════════════════════════════════════════
# STAGING ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════
VIEW_CONFIG_STAGING = {
    # TODO: Update with your staging view configuration
    # Extract from Amazon Connect widget script
    "arn": "",
    "id": "",
    "content": {
        "actions": [],
        "inputSchema": {},
        "template": {}
    },
    "name": "",
    "status": "PUBLISHED",
    "type": "CUSTOMER_MANAGED",
    "viewContentSha256": ""
}

# ═══════════════════════════════════════════════════════════════════════════
# PRODUCTION ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════
VIEW_CONFIG_PROD = {
    # TODO: Update with your production view configuration
    # Extract from Amazon Connect widget script
    "arn": "",
    "id": "",
    "content": {
        "actions": [],
        "inputSchema": {},
        "template": {}
    },
    "name": "",
    "status": "PUBLISHED",
    "type": "CUSTOMER_MANAGED",
    "viewContentSha256": ""
}

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURATION SELECTOR
# ═══════════════════════════════════════════════════════════════════════════
VIEW_CONFIGS = {
    "dev": VIEW_CONFIG_DEV,
    "staging": VIEW_CONFIG_STAGING,
    "prod": VIEW_CONFIG_PROD,
}


def get_view_config(environment: str) -> dict:
    """
    Get the view configuration for the specified environment.

    Args:
        environment: Environment name (dev, staging, prod)

    Returns:
        View configuration dictionary

    Raises:
        ValueError: If environment is not found
    """
    if environment not in VIEW_CONFIGS:
        raise ValueError(
            f"Unknown environment: {environment}. "
            f"Available: {', '.join(VIEW_CONFIGS.keys())}"
        )

    config = VIEW_CONFIGS[environment]

    # Check if config is populated
    if not config.get("id"):
        raise ValueError(
            f"View config for environment '{environment}' is not populated. "
            f"Please update VIEW_CONFIG_{environment.upper()} in view_configs.py"
        )

    return config
