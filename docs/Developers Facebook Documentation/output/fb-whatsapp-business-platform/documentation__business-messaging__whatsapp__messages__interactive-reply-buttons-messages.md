# Interactive reply buttons messages | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/interactive-reply-buttons-messages_

---

# Interactive reply buttons messages

Updated: Apr 21, 2026

Interactive reply buttons messages allow you to send up to three predefined replies for users to choose from.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/440749535_402938502645501_9105062754221017983_n.png?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=IKw3e61TxckQ7kNvwG5epMC&_nc_oc=Adqz8CZzI2081PIhkctz7lEv40-Kl7Yy1A6lVwJi_EXto6AE4AL-Aw4syu_pIAuM4w4&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=TrInvt2RyBNLUtpgTbdiZQ&_nc_ss=7b20f&oh=00_Af4HMy8TaO6Rlg5KRqRhGLok5lNnStL4H_bdBF7T32p9wQ&oe=6A1C00F1)

Users can respond to a message by selecting one of the predefined buttons, which triggers a messages webhook describing their selection.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/440803070_1108181003739406_7014741695346688945_n.png?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=Fz4fwUCUHp4Q7kNvwHSNhbr&_nc_oc=Adqna5JBE2yF26TII-wbdCoNFDcR6mgYMqmWRRscZUEPDzeXFPlFjYk6CsscfL4swLk&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=TrInvt2RyBNLUtpgTbdiZQ&_nc_ss=7b20f&oh=00_Af7gbrJqxy23az8OgQheWA_BytWn7udUmH2OljqdkOOz7g&oe=6A1C0A86)

## Request syntax

Use the [Messages API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api#post-version-phone-number-id-messages) to send an interactive reply buttons message to a WhatsApp user.

```html
curl 'https://graph.facebook.com/<API_VERSION>/<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>/messages' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <ACCESS_TOKEN>' \
-d '
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "<WHATSAPP_USER_PHONE_NUMBER>",
  "type": "interactive",
  "interactive": {
    "type": "button",
    "header": {<MESSAGE_HEADER>},
    "body": {
      "text": "<BODY_TEXT>"
    },
    "footer": {
      "text": "<FOOTER_TEXT>"
    },
    "action": {
      "buttons": [
        {
          "type": "reply",
          "reply": {
            "id": "<BUTTON_ID>",
            "title": "<BUTTON_LABEL_TEXT>"
          }
        }
        <!-- Additional buttons would go here (maximum 3) -->
      ]
    }
  }
}'
```

## Request parameters

| Placeholder | Description | Sample Value |
| --- | --- | --- |
| `<ACCESS_TOKEN>`<br>*String* | **Required.**<br>[System token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens) or [business token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens). | `EAAA...` |
| `<API_VERSION>`<br>*String* | **Optional.**<br>Graph API version. | v25.0 |
| `<BODY_TEXT>`<br>*String* | **Required.**<br>Body text. URLs are automatically hyperlinked.<br>Maximum 1024 characters. | `Hi Pablo! Your gardening workshop is scheduled for 9am tomorrow. Use the buttons if you need to reschedule. Thank you!` |
| `<BUTTON_ID>`<br>*String* | **Required.**<br>A unique identifier for each button. Supports up to 3 buttons.<br>Maximum 256 characters. | `change-button` |
| `<BUTTON_LABEL_TEXT>`<br>*String* | **Required.**<br>Button label text. Must be unique if using multiple buttons.<br>Maximum 20 characters. | `Change` |
| `<FOOTER_TEXT>`<br>*String* | **Required if using a footer.**<br>Footer text. URLs are automatically hyperlinked.<br>Maximum 60 characters. | `Lucky Shrub: Your gateway to succulents!™` |
| `<MESSAGE_HEADER>`<br>*JSON Object* | **Optional.**<br>Header content. Supports the following types:<br>`document``image``text``video`<br>Media assets can be sent using their [uploaded media](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/media#upload-media) `id` or URL `link` (not recommended). | Image header example using uploaded media ID (same basic structure for all media types):<br>`{<br>"type": "image",<br>"image": {<br>"id": "2762702990552401"<br>}`<br>Image header example using hosted media:<br>`{<br>"type": "image",<br>"image": {<br>"link": "https://www.luckyshrub.com/media/workshop-banner.png"<br>}`<br>Text header example:<br>`{<br>"type":"text",<br>"text": "Workshop Details"<br>}` |
| `<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>`<br>*String* | **Required.**<br>WhatsApp business phone number ID. | `106540352242922` |
| `<WHATSAPP_USER_PHONE_NUMBER>`<br>*String* | **Required.**<br>WhatsApp user phone number. | `+16505551234` |

## Example request

Example request to send an interactive reply buttons message with an image header, body text, footer text, and two quick-reply buttons.

```curl
curl 'https://graph.facebook.com/v25.0/106540352242922/messages' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "+16505551234",
  "type": "interactive",
  "interactive": {
    "type": "button",
    "header": {
      "type": "image",
      "image": {
        "id": "2762702990552401"
      }
    },
    "body": {
      "text": "Hi Pablo! Your gardening workshop is scheduled for 9am tomorrow. Use the buttons if you need to reschedule. Thank you!"
    },
    "footer": {
      "text": "Lucky Shrub: Your gateway to succulents!™"
    },
    "action": {
      "buttons": [
        {
          "type": "reply",
          "reply": {
            "id": "change-button",
            "title": "Change"
          }
        },
        {
          "type": "reply",
          "reply": {
            "id": "cancel-button",
            "title": "Cancel"
          }
        }
      ]
    }
  }
}'
```

## Example response

```json
{
  "messaging_product": "whatsapp",
  "contacts": [
    {
      "input": "+16505551234",
      "wa_id": "16505551234"
    }
  ],
  "messages": [
    {
      "id": "wamid.HBgLMTY0NjcwNDM1OTUVAgARGBI1RjQyNUE3NEYxMzAzMzQ5MkEA"
    }
  ]
}
```

## Webhooks

When a WhatsApp user taps on a reply button, a **messages** webhook is triggered that describes their selection in a `button_reply` object:

```json
"button_reply": {
  "id": "<BUTTON_ID>",
  "title": "<BUTTON_LABEL_TEXT>"
}
```

- `<BUTTON_ID>` — The button ID of the button tapped by the user.
- `<BUTTON_LABEL_TEXT>` — The button label text of the button tapped by the user.

### Example webhook

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
                  "name": "Pablo Morales"
                },
                "wa_id": "16505551234"
              }
            ],
            "messages": [
              {
                "context": {
                  "from": "15550783881",
                  "id": "wamid.HBgLMTY0NjcwNDM1OTUVAgARGBJBM0Y4RUU0RUNFQkFDMjYzQUMA"
                },
                "from": "16505551234",
                "id": "wamid.HBgLMTY0NjcwNDM1OTUVAgASGBQzQThBREYwNzc2RDc2QjA1QTIwMgA=",
                "timestamp": "1714510003",
                "type": "interactive",
                "interactive": {
                  "type": "button_reply",
                  "button_reply": {
                    "id": "change-button",
                    "title": "Change"
                  }
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
