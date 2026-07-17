# Group messages webhook reference | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/group_

---

# Group messages webhook reference

Updated: Nov 10, 2025

This reference describes trigger events and payload contents for the WhatsApp Business Account **messages** webhook for messages that are sent to a group, or received from a group.

## Triggers

- A WhatsApp user or a business sends a message to a group.
- A WhatsApp user or a business receives a message within a group.

## Syntax

```html
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "<WHATSAPP_BUSINESS_ACCOUNT_ID>",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "<BUSINESS_DISPLAY_PHONE_NUMBER>",
              "phone_number_id": "<BUSINESS_PHONE_NUMBER_ID>"
            },
            "contacts": [
              {
                "profile": {
                  "name": "<WHATSAPP_USER_PROFILE_NAME>"
                },
                "wa_id": "<WHATSAPP_USER_ID>",
                "identity_key_hash": "<IDENTITY_KEY_HASH>" <!-- only included if identity change check enabled -->
              }
            ],
            "messages": [
              {
                "from": "<WHATSAPP_USER_PHONE_NUMBER>",
                "group_id": "<GROUP_ID>",
                "id": "<WHATSAPP_MESSAGE_ID>",
                "timestamp": "<WEBHOOK_TRIGGER_TIMESTAMP>",
                "text": {
                  "body": "<MESSAGE_TEXT_BODY>"
                },
                "type": "<MESSAGE_TYPE>"
              }
            ],
          },
          "field": "messages"
        }
      ]
    }
  ]
}
```

## Parameters

| Placeholder | Description | Example value |
| --- | --- | --- |
| `<BUSINESS_DISPLAY_PHONE_NUMBER>`<br>*String* | Business display phone number. | `15550783881` |
| `<BUSINESS_PHONE_NUMBER_ID>`<br>*String* | Business phone number ID. | `106540352242922` |
| `<GROUP_ID>`<br>*String* | The string identifier of a group made using the Groups API.<br>This field shows when messages are sent, received, or read from a group.<br>[Learn more about the Groups API](https://developers.facebook.com/documentation/business-messaging/whatsapp/groups) | `"Y2FwaV9ncm91cDoxNzA1NTU1MDEzOToxMjAzNjM0MDQ2OTQyMzM4MjAZD"` |
| `<IDENTITY_KEY_HASH>`<br>*String* | Identity key hash. Only included if you have enabled the [identity change check](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers) feature. | `DF2lS5v2W6x=` |
| `<MESSAGE_TEXT_BODY>`<br>*String* | Text body of the message. | `What do you all think about this?` |
| `<MESSAGE_TYPE>`<br>*String* | The type of message being sent. Will change depending on the message sent to the group.<br>Currently, the Groups API supports:<br>TextMediaText-based templatesMedia-based templates | `text` |
| `<WHATSAPP_BUSINESS_ACCOUNT_ID>`<br>*String* | WhatsApp Business Account ID. | `102290129340398` |
| `<WHATSAPP_MESSAGE_ID>`<br>*String* | WhatsApp message ID. | `wamid.HBgLMTY1MDM4Nzk0MzkVAgASGBQzQUFERjg0NDEzNDdFODU3MUMxMAA=` |
| `<WEBHOOK_TRIGGER_TIMESTAMP>`<br>*String* | Unix timestamp indicating when the webhook was triggered. | `1739321024` |
| `<WHATSAPP_USER_PHONE_NUMBER>`<br>*String* | WhatsApp user phone number. This is the same value returned by the API as the `input` value when sending a message to a WhatsApp user. Note that a WhatsApp user’s phone number and ID may not always match. | `+16505551234` |
| `<WHATSAPP_USER_PROFILE_NAME>`<br>*String* | WhatsApp user’s name as it appears in their profile in the WhatsApp client. | `Sheena Nelson` |
| `<WHATSAPP_USER_ID>`<br>*String* | WhatsApp user ID. Note that a WhatsApp user’s ID and phone number may not always match. | `16505551234` |

## Example

```json
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "102290129340398",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "15550783881",
              "phone_number_id": "106540352242922"
            },
            "contacts": [
              {
                "profile": {
                  "name": "Tiago Mingo"
                },
                "wa_id": "16505551234"
              }
            ],
            "messages": [
              {
                "from": "16505551234",
                "group_id": "HBgLMTY1MDM4Nzk0MzkVAgASGBQzQTRBNjU5OUFFRTAzODEwMTQ0RgA",
                "id": "wamid.HASDI128HJOPUERIH82ahdasd09ASDHi5>",
                "timestamp": "1744344496",
                "text": {
                  "body": "What does everyone think about this?"
                },
                "type": "text"
              }
            ]
          },
          "field": "messages"
        }
      ]
    }
  ]
}
```
