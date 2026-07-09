# System messages webhook reference | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/system_

---

# System messages webhook reference

Updated: Oct 22, 2025

This reference describes trigger events and payload contents for the WhatsApp Business Account **messages** webhook for system messages.

Note that unlike other incoming messages webhooks, system **messages** webhooks don’t include a `contacts` array.

## Triggers

- A WhatsApp user changes their WhatsApp phone number.

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
            "messages": [
              {
                "from": "<WHATSAPP_USER_PHONE_NUMBER>",
                "id": "<WHATSAPP_MESSAGE_ID>",
                "timestamp": "<WEBHOOK_TRIGGER_TIMESTAMP>",
                "type": "system",
                "system": {
                  "body": "User <WHATSAPP_USER_PROFILE_NAME> changed from <WHATSAPP_USER_PHONE_NUMBER> to <NEW_WHATSAPP_USER_PHONE_NUMBER>",
                  "wa_id": "<NEW_WHATSAPP_USER_ID>",
                  "type": "user_changed_number"
                }
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

## Parameters

| Placeholder | Description | Example value |
| --- | --- | --- |
| `<BUSINESS_DISPLAY_PHONE_NUMBER>`<br>*String* | Business display phone number. | `15550783881` |
| `<BUSINESS_PHONE_NUMBER_ID>`<br>*String* | Business phone number ID. | `106540352242922` |
| `<NEW_WHATSAPP_USER_ID>`<br>*String* | New WhatsApp user ID. Note that a WhatsApp user’s ID and phone number may not always match. | `12195555358` |
| `<NEW_WHATSAPP_USER_PHONE_NUMBER>`<br>*String* | New WhatsApp user phone number. Note that a WhatsApp user’s phone number and ID may not always match. | `12195555358` |
| `<WEBHOOK_TRIGGER_TIMESTAMP>`<br>*String* | Unix timestamp indicating when the webhook was triggered. | `1739321024` |
| `<WHATSAPP_BUSINESS_ACCOUNT_ID>`<br>*String* | WhatsApp Business Account ID. | `102290129340398` |
| `<WHATSAPP_MESSAGE_ID>`<br>*String* | WhatsApp message ID. | `wamid.HBgLMTY1MDM4Nzk0MzkVAgASGBQzQUFERjg0NDEzNDdFODU3MUMxMAA=` |
| `<WHATSAPP_USER_PHONE_NUMBER>` *String* | WhatsApp user phone number. Note that a WhatsApp user’s phone number and ID may not always match. | `16505551234` |
| `<WHATSAPP_USER_PROFILE_NAME>` *String* | WhatsApp user’s name as it appears in their profile in the WhatsApp client. | `Sheena Nelson` |

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
            "messages": [
              {
                "from": "16505551234",
                "id": "wamid.HBgLMTk4MzU1NTE5NzQVAgASGAoxMTgyMDg2MjY3AA==",
                "timestamp": "1750269342",
                "system": {
                  "body": "User Sheena Nelson changed from 16505551234 to 12195555358",
                  "wa_id": "12195555358",
                  "type": "user_changed_number"
                },
                "type": "system"
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
