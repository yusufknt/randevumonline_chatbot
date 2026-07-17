# Interactive list messages

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/interactive-list-messages_

---

# Interactive list messages

Updated: Nov 3, 2025

Interactive list messages allow you to present WhatsApp users with a list of options to choose from (options are defined as rows in the request payload):

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/439906651_815131396632137_2393939757123941379_n.png?_nc_cat=106&ccb=1-7&_nc_sid=e280be&_nc_ohc=rfsg-PC4XjwQ7kNvwGS6CIf&_nc_oc=AdrcEkKEY_19jsqmV56DPUVSfH0YRhGs00Y1e33SBxNyPyUUQjqplHj16Ufr1-x2nRw&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=W8uyUPuHeVzImBfkzOXlGw&_nc_ss=7b20f&oh=00_Af70DqveYH6P9S5bHNs9lZrCMnKKsuRY0bQ9gPFxF081Ow&oe=6A1C0AD1)

When a user taps the button in the message, it displays a modal that lists the options available:

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/440772174_1215031642793437_4263879536705453309_n.png?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=VjTzRh2tqPMQ7kNvwGNGiRB&_nc_oc=AdqJTAl8f9uIW5Wl1eeijmaZ-7Uowkr3FLB4YsAb02pa89UPrbIyjWE3hLTjzhRLPZ8&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=W8uyUPuHeVzImBfkzOXlGw&_nc_ss=7b20f&oh=00_Af53HtPBjinE_nh506AhCKMskIovQIkVzvQyvzCaI9mFuA&oe=6A1C2C43)

Users can then choose one option and their selection will be sent as a reply:

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/440751989_956441365805448_2344471884869029846_n.png?_nc_cat=106&ccb=1-7&_nc_sid=e280be&_nc_ohc=SwmvldzoXFQQ7kNvwFrA4R4&_nc_oc=AdrI-RW6CkY9wBEXFMBL0QTiuD4JgJnZMuMKoAkJ1naK4t5NFVw8AxN-DkdSqp9Kadc&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=W8uyUPuHeVzImBfkzOXlGw&_nc_ss=7b20f&oh=00_Af4zfUoG3X52PBDl8Et54yAsBMeZRI49uyqKvHUp_s8Ysw&oe=6A1C0CD3)

This triggers a webhook, which identifies the option selected by the user.

Interactive list messages support up to 10 sections, with up to 10 rows for all sections combined, and can include an optional header and footer.

## Request Syntax

Use the [Messages API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api#post-version-phone-number-id-messages) to send an interactive list message to a WhatsApp user.

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
    "type": "list",
    "header": {
      "type": "text",
      "text": "<MESSAGE_HEADER_TEXT>"
    },
    "body": {
      "text": "<MESSAGE_BODY_TEXT>"
    },
    "footer": {
      "text": "<MESSAGE_FOOTER_TEXT>"
    },
    "action": {
      "button": "<BUTTON_TEXT>",
      "sections": [
        {
          "title": "<SECTION_TITLE_TEXT>",
          "rows": [
            {
              "id": "<ROW_ID>",
              "title": "<ROW_TITLE_TEXT>",
              "description": "<ROW_DESCRIPTION_TEXT>"
            }
            <!-- Additional rows would go here -->
          ]
        }
        <!-- Additional sections would go here -->
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
| `<BUTTON_TEXT>`<br>*String* | **Required.**<br>Button label text. When tapped, reveals rows (options the WhatsApp user can tap). Supports a single button.<br>Maximum 20 characters. | `Shipping Options` |
| `<MESSAGE_BODY_TEXT>`<br>*String* | **Required.**<br>Message body text. Supports URLs.<br>Maximum 4096 characters. | `Which shipping option do you prefer?` |
| `<MESSAGE_FOOTER_TEXT>`<br>*String* | **Optional.**<br>Message footer text.<br>Maximum 60 characters. | `Lucky Shrub: Your gateway to succulents™` |
| `<MESSAGE_HEADER_TEXT>`<br>*String* | **Optional.**<br>The `header` object is optional. Supports `text` header type only.<br>Maximum 60 characters. | `Choose Shipping Option` |
| `<ROW_DESCRIPTION_TEXT>`<br>*String* | **Optional.**<br>Row description.<br>Maximum 72 characters. | `Next Day to 2 Days` |
| `<ROW_ID>`<br>*String* | **Required.**<br>Arbitrary string identifying the row. This ID will be included in the webhook payload if the user submits the selection.<br>At least one row is required. Supports up to 10 rows.<br>Maximum 200 characters. | `priority_express` |
| `<ROW_TITLE_TEXT>`<br>*String* | **Required.**<br>Row title. At least 1 row is required. Supports up to 10 rows.<br>Maximum 24 characters. | `Priority Mail Express` |
| `<SECTION_TITLE_TEXT>`<br>*String* | **Required.**<br>Section title text. At least 1 section is required. Supports up to 10 sections.<br>Maximum 24 characters. | `I want it ASAP!` |
| `<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>`<br>*String* | **Required.**<br>WhatsApp business phone number ID. | `106540352242922` |
| `<WHATSAPP_USER_PHONE_NUMBER>`<br>*String* | **Required.**<br>WhatsApp user phone number. | `+16505551234` |

## Example request

Example request to send an interactive list message with a header, body, footer, and two sections containing two rows each.

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
    "type": "list",
    "header": {
      "type": "text",
      "text": "Choose Shipping Option"
    },
    "body": {
      "text": "Which shipping option do you prefer?"
    },
    "footer": {
      "text": "Lucky Shrub: Your gateway to succulents™"
    },
    "action": {
      "button": "Shipping Options",
      "sections": [
        {
          "title": "I want it ASAP!",
          "rows": [
            {
              "id": "priority_express",
              "title": "Priority Mail Express",
              "description": "Next Day to 2 Days"
            },
            {
              "id": "priority_mail",
              "title": "Priority Mail",
              "description": "1–3 Days"
            }
          ]
        },
        {
          "title": "I can wait a bit",
          "rows": [
            {
              "id": "usps_ground_advantage",
              "title": "USPS Ground Advantage",
              "description": "2–5 Days"
            },
            {
              "id": "media_mail",
              "title": "Media Mail",
              "description": "2–8 Days"
            }
          ]
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

When a WhatsApp user selects an option and sends their message, a **messages** webhook is triggered identifying the ID (`id`) of the option they chose.

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
                  "id": "wamid.HBgLMTY0NjcwNDM1OTUVAgARGBIwMjg0RkMxOEMyMkNEQUFFRDgA"
                },
                "from": "16505551234",
                "id": "wamid.HBgLMTY0NjcwNDM1OTUVAgASGBQzQTZDMzFGRUFBQjlDMzIzMzlEQwA=",
                "timestamp": "1712595443",
                "type": "interactive",
                "interactive": {
                  "type": "list_reply",
                  "list_reply": {
                    "id": "priority_express",
                    "title": "Priority Mail Express",
                    "description": "Next Day to 2 Days"
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
