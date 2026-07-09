# Interactive Call-to-Action URL Button Messages | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/interactive-cta-url-messages_

---

# Interactive Call-to-Action URL Button Messages

Updated: Nov 3, 2025

WhatsApp users may be hesitant to tap raw URLs containing lengthy or obscure strings in text messages. In these situations, you may wish to send an interactive call-to-action (CTA) URL button message instead. CTA URL button messages allow you to map any URL to a button so you don’t have to include the raw URL in the message body.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/498114174_2231456237292792_1964702441845433307_n.png?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=SwecilS9R18Q7kNvwFULiPs&_nc_oc=AdqtkND78BWdk87b4EYC1CpZXHH_5JqprIrOqeIm0KNReMtQB6OAijgB2dVHWALoOCo&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=-FGizziJS3V3Kc3GsAoMOg&_nc_ss=7b20f&oh=00_Af5fOnlnk-Im88g-yDNr2aW0lTUA3tlFF8kJPO2Xuq_TyA&oe=6A1BFF51)

## Request syntax

Use the [Messages API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api#post-version-phone-number-id-messages) to send an interactive CTA URL message.

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
    "type": "cta_url",

    <!-- If using document header, otherwise omit -->
    "header": {
      "type": "document",
      "document": {
        "link": "<ASSET_URL>"
      }
    },

    <!-- If using image header, otherwise omit -->
    "header": {
      "type": "image",
      "image": {
        "link": "<ASSET_URL>"
      }
    },

    <!-- If using text header, otherwise omit -->
    "header": {
      "type": "text",
      "text": "<HEADER_TEXT>"
      }
    },

    <!-- If using video header, otherwise omit -->
    "header": {
      "type": "video",
      "video": {
        "link": "<ASSET_URL>"
      }
    },

    "body": {
      "text": "<BODY_TEXT>"
    },
    "action": {
      "name": "cta_url",
      "parameters": {
        "display_text": "<BUTTON_LABEL_TEXT>",
        "url": "<BUTTON_URL>"
      }
    },

    <!-- If using footer text, otherwise omit -->
    "footer": {
      "text": "<FOOTER_TEXT>"
    }
  }
}'
```

## Request parameters

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<ACCESS_TOKEN>`<br>*String* | **Required.**<br>[System token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens) or [business token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens). | `EAAA...` |
| `<API_VERSION>`<br>*String* | **Optional.**<br>Graph API version. | v25.0 |
| `<ASSET_URL>`<br>*String* | **Required if using a header with a media asset.**<br>Asset URL on a public server. | `https://www.luckyshrub.com/assets/lucky-shrub-banner-logo-v1.png` |
| `<BODY_TEXT>`<br>*String* | **Required.**<br>Body text. URLs are automatically hyperlinked.<br>Maximum 1024 characters. | `Tap the button below to see available dates.` |
| `<BUTTON_LABEL_TEXT>`<br>*String* | **Required.**<br>Button label text. Must be unique if using multiple buttons.<br>Maximum 20 characters. | `See Dates` |
| `<BUTTON_URL>` | **Required.**<br>URL to load in the device’s default web browser when tapped by the WhatsApp user. | `https://www.luckyshrub.com?clickID=kqDGWd24Q5TRwoEQTICY7W1JKoXvaZOXWAS7h1P76s0R7Paec4` |
| `<FOOTER_TEXT>`<br>*String* | **Required if using a footer.**<br>Footer text. URLs are automatically hyperlinked.<br>Maximum 60 characters. | `Dates subject to change.` |
| `<HEADER_TEXT>`<br>*String* | **Required if using a text header.**<br>Header text.<br>Maximum 60 characters. | `New workshop dates announced!` |
| `<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>`<br>*String* | **Required.**<br>WhatsApp business phone number ID. | `106540352242922` |
| `<WHATSAPP_USER_PHONE_NUMBER>`<br>*String* | **Required.**<br>WhatsApp user phone number. | `+16505551234` |

## Example request

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
    "type": "cta_url",
    "header": {
      "type": "image",
      "image": {
        "link": "https://www.luckyshrub.com/assets/lucky-shrub-banner-logo-v1.png"
      }
    },
    "body": {
      "text": "Tap the button below to see available dates."
    },
    "action": {
      "name": "cta_url",
      "parameters": {
        "display_text": "See Dates",
        "url": "https://www.luckyshrub.com?clickID=kqDGWd24Q5TRwoEQTICY7W1JKoXvaZOXWAS7h1P76s0R7Paec4"
      }
    },
    "footer": {
      "text": "Dates subject to change."
    }
  }
}'
```

## Example Response

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
