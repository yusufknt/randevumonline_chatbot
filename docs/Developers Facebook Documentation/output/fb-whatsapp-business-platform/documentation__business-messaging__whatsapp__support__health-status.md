# Messaging and Calling Health Status | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/support/health-status_

---

# Messaging and Calling Health Status

Updated: Oct 22, 2025

This document describes how to determine whether or not you can do messaging and calling successfully using a given API resource.

The following nodes have a `health_status` field:

- [WhatsApp Business Account](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/whatsapp-business-account-api)
- [WhatsApp Business Phone Number](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/whatsapp-business-account-phone-number-api)
- [WhatsApp Message Template](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/template-api)

If you request the `health_status` field on any of these nodes, the API will return a summary of the messaging and calling health of all the nodes involved in messaging/calling requests if using the targeted node. This summary indicates if you will be able to use the API for messaging and calling successfully, or if you will have limited success due to some limitation on one or more nodes, or if you will be prevented from messaging and calling entirely.

## Request Syntax

```https
GET /<NODE_ID>?fields=health_status
```

## Response

```json
{
  "health_status": {
    "can_send_message": "<OVERALL_MESSAGING_STATUS>",
    "entities": [

      /* Only included if targeting a business phone number */
      {
        "entity_type": "PHONE_NUMBER",
        "id": "<BUSINESS_PHONE_NUMBER_ID>",
        "can_send_message": "<BUSINESS_PHONE_NUMBER_MESSAGING_STATUS>",
        "can_receive_call_sip": "<BUSINESS_PHONE_NUMBER_RECEIVE_CALL_SIP_STATUS>"
      },

      /* Only included if targeting a template */
      {
        "entity_type": "MESSAGE_TEMPLATE",
        "id": "<TEMPLATE_ID>",
        "can_send_message": "<TEMPLATE_MESSAGING_STATUS>"
      },

      /* WABA, business, and app always included */
      {
        "entity_type": "WABA",
        "id": "<WABA_ID>",
        "can_send_message": "<WABA_MESSAGING_STATUS>"
      },
      {
        "entity_type": "BUSINESS",
        "id": "<BUSINESS_PORTFOLIO_ID>",
        "can_send_message": "<BUSINESS_PORTFOLIO_MESSAGING_STATUS>"
      },
      {
        "entity_type": "APP",
        "id": "<APP_ID>",
        "can_send_message": "<APP_MESSAGING_STATUS>",
        "can_receive_call_sip": "<APP_RECEIVE_CALL_SIP_STATUS>"
      }
    ]
  },
  "id": "<NODE_ID>"
}
```

## Response Contents

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<APP_ID>` | App ID. | `634974688087057` |
| `<APP_MESSAGING_STATUS>` | The app’s messaging health status. See [Messaging Health Status](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/health-status#health-status-field). | `AVAILABLE` |
| `<APP_RECEIVE_CALL_SIP_STATUS>` | The app’s ability to receiving a call over [SIP](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/sip). See [Health Status](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/health-status#health-status-field). Other calling related fields are planned for future. | `AVAILABLE` |
| `<BUSINESS_PORTFOLIO_ID>` | Business portfolio ID. | `506914307656634` |
| `<BUSINESS_PORTFOLIO_MESSAGING_STATUS>` | The business portfolio’s messaging health status. See [Messaging Health Status](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/health-status#health-status-field). | `AVAILABLE` |
| `<BUSINESS_PHONE_NUMBER_ID>` | Business phone number ID. | `106540352242922` |
| `<BUSINESS_PHONE_NUMBER_MESSAGING_STATUS>` | The business phone number’s messaging health status. See [Messaging Health Status](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/health-status#health-status-field). | `AVAILABLE` |
| `<BUSINESS_PHONE_NUMBER_RECEIVE_CALL_SIP_STATUS>` | The business phone number’s ability to receive a call over [SIP](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/sip). See [Health Status](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/health-status#health-status-field). Other calling related fields are planned for future. | `AVAILABLE` |
| `<NODE_ID>` | The targeted node’s ID. | `161311403722088` |
| `<OVERALL_MESSAGING_STATUS>` | The overall messaging health status, given all of the nodes involved in a messaging request, if using the targeted node. See [Messaging Health Status](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/health-status#health-status-field). | `AVAILABLE` |
| `<TEMPLATE_ID>` | Template ID. | `1421988012088524` |
| `<TEMPLATE_MESSAGING_STATUS>` | The template’s messaging health status. See [Messaging Health Status](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/health-status#health-status-field). | `AVAILABLE` |
| `<WABA_ID>` | WABA ID. | `102290129340398` |
| `<WABA_MESSAGING_STATUS>` | The WABA’s messaging health status. See [Messaging Health Status](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/health-status#health-status-field). | `AVAILABLE` |

## Health Status field

When you attempt to do messaging or calling, multiple nodes are involved, including the app, the business portfolio that owns or has claimed it, a WABA, a business phone number, and a template (if sending a template message).

Each of these nodes can have one of the following health statuses assigned to the `can_send_message` or `can_receive_call_sip` property:

- `AVAILABLE` : Indicates that the node meets all messaging or calling requirements.
- `LIMITED` : Indicates that the node meets messaging or calling requirements, but has some limitations. If a given node has this value, [additional info](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/health-status#additional-info-property) will be included.
- `BLOCKED` : Indicates that the node does not meet one or more messaging or calling requirements. If a given node has this value, the [errors property](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/health-status#errors-property) will be included which describes the error and a possible solution.

### Overall Status

The overall health status property (`health_status.can_send_message`) will be set as follows:

- If one or more nodes is blocked, it will be set to `BLOCKED` .
- If no nodes are blocked, but one or more nodes is limited, it will be set to `LIMITED` .
- If all nodes are available, it will be set to `AVAILABLE` .

Note: This aggregate status is not available for `can_receive_call_sip`

## Example Request

```curl
curl 'https://graph.facebook.com/v25.0/106540352242922?fields=health_status' \
-H 'Authorization: Bearer EAAJB'
```

## Example Response

```json
{
  "health_status": {
    "can_send_message": "AVAILABLE",
    "entities": [
      {
        "entity_type": "PHONE_NUMBER",
        "id": "106540352242922",
        "can_send_message": "AVAILABLE",
        "can_receive_call_sip":"AVAILABLE"
      },
      {
        "entity_type": "WABA",
        "id": "102290129340398",
        "can_send_message": "AVAILABLE"
      },
      {
        "entity_type": "BUSINESS",
        "id": "506914307656634",
        "can_send_message": "AVAILABLE"
      },
      {
        "entity_type": "APP",
        "id": "634974688087057",
        "can_send_message": "AVAILABLE",
        "can_receive_call_sip":"AVAILABLE"
      }
    ]
  },
  "id": "106540352242922"
}
```

## Additional Info Property

If a given node’s `can_send_message` or `can_receive_call_sip` property is set to `LIMITED`, the `additional_info` property will be included, which provides additional context for the limitation.

### Example Limited Response

This is an example response to a request on a business phone number that can be used to send messages, but has a limit on the number it can send because its display name has not been approved.

```json
{
  "health_status": {
    "can_send_message": "LIMITED",
    "entities": [
      {
        "entity_type": "PHONE_NUMBER",
        "id": "106540352242922",
        "can_send_message": "LIMITED",
        "can_receive_call_sip":"AVAILABLE",
        "additional_info": [
          "Your display name has not been approved yet. Your message limit will increase after the display name is approved."
        ]
      },
      {
        "entity_type": "WABA",
        "id": "102290129340398",
        "can_send_message": "AVAILABLE"
      },
      {
        "entity_type": "BUSINESS",
        "id": "506914307656634",
        "can_send_message": "AVAILABLE"
      },
      {
        "entity_type": "APP",
        "id": "634974688087057",
        "can_send_message": "AVAILABLE",
        "can_receive_call_sip":"AVAILABLE"
      }
    ]
  },
  "id": "105154286024403"
}
```

## Errors Property

If a given node’s `can_send_message` or `can_receive_call_sip` property is set to `BLOCKED`, the `errors` property will be included, which describes the reason for the status and a possible solution.

### Example Blocked Response

This is an example response to a request on a template that can’t be sent in a template message because it is still in a pending state.

```json
{
  "health_status": {
    "can_send_message": "BLOCKED",
    "entities": [
      {
        "entity_type": "MESSAGE_TEMPLATE",
        "id": "2632273056924580",
        "can_send_message": "BLOCKED",
        "can_receive_call_sip":"AVAILABLE",
        "errors": [
          {
            "error_code": 141002,
            "error_description": "Message templates can only be sent out if they are approved.",
            "possible_solution": "Edit or appeal the message template review decision."
          }
        ]
      },
      {
        "entity_type": "WABA",
        "id": "102290129340398",
        "can_send_message": "AVAILABLE"
      },
      {
        "entity_type": "BUSINESS",
        "id": "506914307656634",
        "can_send_message": "AVAILABLE"
      },
      {
        "entity_type": "APP",
        "id": "634974688087057",
        "can_send_message": "AVAILABLE",
        "can_receive_call_sip":"AVAILABLE"
      }
    ]
  },
  "id": "2632273056924580"
}
```

### Example Blocked Response for receiving calls over SIP

This is an example response to a request on a phone number that has not configured [SIP](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/sip).

```json
{
  "health_status": {
    "can_send_message": "BLOCKED",
    "entities": [
      {
        "entity_type": "PHONE_NUMBER",
        "id": "597727103418254",
        "can_send_message": "AVAILABLE",
        "can_receive_call_sip": "BLOCKED",
        "errors": [
          {
            "error_code": 138024,
            "error_description": "WhatsApp Business calling cannot use SIP because it is not enabled",
            "possible_solution": "Configure SIP using {PHONE_NUMBER_ID}/settings API"
          }
        ]
      },
      {
        "entity_type": "WABA",
        "id": "102290129340398",
        "can_send_message": "AVAILABLE"
      },
      {
        "entity_type": "BUSINESS",
        "id": "506914307656634",
        "can_send_message": "AVAILABLE"
      },
      {
        "entity_type": "APP",
        "id": "634974688087057",
        "can_send_message": "AVAILABLE",
        "can_receive_call_sip": "BLOCKED",
        "errors": [
          {
            "error_code": 138025,
            "error_description": "This app cannot use SIP for WhatsApp Business calling because it has not configured a SIP server for this business phone number",
            "possible_solution": "Configure SIP server using {PHONE_NUMBER_ID}/settings API"
          }
        ]
      }
    ]
  },
  "id": "105154286024403"
}
```
