# smb_message_echoes webhook reference | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/smb_message_echoes_

---

# smb_message_echoes webhook reference

Updated: Apr 28, 2026

This reference describes trigger events and payload contents for the WhatsApp Business Account **smb_message_echoes** webhook.

The **smb_message_echoes** webhook notifies you of messages sent via the WhatsApp Business app or a [companion (“linked”) device](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users#linked-devices) by a business customer who has been [onboarded to Cloud API](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users) via a solution provider.

## Triggers

- A business customer with a WhatsApp Business app phone number, who has been [onboarded by a solution provider](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users) , sends a message using the WhatsApp Business app or a [companion device](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users#linked-devices) to a WhatsApp user or another business.
- A business customer revokes (deletes) a previously sent message using the WhatsApp Business app.
- A business customer edits a previously sent message using the WhatsApp Business app.

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
            "message_echoes": [
              {
                "from": "<BUSINESS_DISPLAY_PHONE_NUMBER>",
                "to": "<WHATSAPP_USER_PHONE_NUMBER>",
                "id": "<WHATSAPP_MESSAGE_ID>",
                "timestamp": "<WEBHOOK_TRIGGER_TIMESTAMP>",
                "type": "<MESSAGE_TYPE>",
                "<MESSAGE_TYPE>": {
                  <MESSAGE_CONTENTS>
                }
              }
            ]
          },
          "field": "smb_message_echoes"
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
| `<MESSAGE_CONTENTS>`<br>*Object* | An object describing the message’s contents.<br>This value will vary based on the message `type`, as well as the contents of the message.<br>For example, if a business sends an `image` message without a caption, the object would not include the `caption` property.<br>See [Sending messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages) for examples of payloads for each message type. | `{"body":"Here's the info you requested! https://www.meta.com/quest/quest-3/"}` |
| `<MESSAGE_TYPE>`<br>*String* | [Message type](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages). This placeholder appears twice in the syntax above because it serves as both the `type` property value and its matching property name. Supported values include `text`, `image`, `video`, `document`, `revoke`, and `edit`. | `text` |
| `<WEBHOOK_TRIGGER_TIMESTAMP>`<br>*Integer* | Unix timestamp indicating when the webhook was triggered. | `1739321024` |
| `<WHATSAPP_BUSINESS_ACCOUNT_ID>`<br>*String* | The business customer’s WhatsApp Business Account ID. | `102290129340398` |
| `<WHATSAPP_MESSAGE_ID>`<br>*String* | WhatsApp message ID. | `wamid.HBgLMTY1MDM4Nzk0MzkVAgASGBQzQUFERjg0NDEzNDdFODU3MUMxMAA=` |
| `<WHATSAPP_USER_PHONE_NUMBER>`<br>*String* | WhatsApp user phone number. This is the same value returned by the API as the `input` value when sending a message to a WhatsApp user. Note that a WhatsApp user’s phone number and ID may not always match. | `+16505551234` |

## Examples

### Text message

This example payload describes a text message sent to a WhatsApp user by a business customer using the WhatsApp Business app.

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
            "message_echoes": [
              {
                "from": "15550783881",
                "to": "16505551234",
                "id": "wamid.HBgLMTY0NjcwNDM1OTUVAgARGBIyNDlBOEI5QUQ4NDc0N0FCNjMA",
                "timestamp": "1739321024",
                "type": "text",
                "text": {
                  "body": "Here's the info you requested! https://www.meta.com/quest/quest-3/"
                }
              }
            ]
          },
          "field": "smb_message_echoes"
        }
      ]
    }
  ]
}
```

### Revoke message

This example payload describes a business customer revoking (deleting) a previously sent message using the WhatsApp Business app. The `revoke` object contains the `original_message_id` of the message being deleted.

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
            "message_echoes": [
              {
                "from": "15550783881",
                "to": "16505551234",
                "id": "wamid.HBgLMTY1MDM4Nzk0MzkVAgASGBQzQUFERjg0NDEzNDdFODU3MUMxMAA=",
                "timestamp": "1749854575",
                "type": "revoke",
                "revoke": {
                  "original_message_id": "wamid.HBgLMTQxMjU1NTA4MjkVAgASGBQzQUNCNjk5RDUwNUZGMUZEM0VBRAA="
                }
              }
            ]
          },
          "field": "smb_message_echoes"
        }
      ]
    }
  ]
}
```

### Edit message

This example payload describes a business customer editing the caption of a previously sent image message using the WhatsApp Business app. The `edit` object contains the `original_message_id` of the message being edited and a `message` object with the updated content.

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
            "message_echoes": [
              {
                "from": "15550783881",
                "to": "16505551234",
                "id": "wamid.HBgLMTY1MDM4Nzk0MzkVAgASGBQzQkJERjg0NDEzNDdFODU3MUMxMAA=",
                "timestamp": "1749854620",
                "type": "edit",
                "edit": {
                  "original_message_id": "wamid.HBgLMTQxMjU1NTA4MjkVAgASGBQzQUNCNjk5RDUwNUZGMUZEM0VBRAA=",
                  "message": {
                    "context": {
                      "id": "M0"
                    },
                    "type": "image",
                    "image": {
                      "caption": "Updated image caption",
                      "mime_type": "image/jpeg",
                      "sha256": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2",
                      "id": "1234567890",
                      "url": "https://lookaside.fbsbx.com/whatsapp_business/attachments/?mid=133..."
                    }
                  }
                }
              }
            ]
          },
          "field": "smb_message_echoes"
        }
      ]
    }
  ]
}
```
