# Coupon code templates | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/marketing-templates/coupon-templates_

---

# Coupon code templates

Updated: Dec 3, 2025

Coupon code templates are marketing templates that display a single copy code button. When tapped, the code is copied to the customer’s clipboard.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/365756533_1756280054770140_7287687181799037425_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=zJuheUvb3aMQ7kNvwHjJJew&_nc_oc=Adq6KGRUFUYB2QVl4jAXeoUVYzDVRTvX5zOOpG-2QzTDGVPcR9nTSn5EJLZU01yYNWI&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=OVl5pof9JAAyxxjzUjghJQ&_nc_ss=7b20f&oh=00_Af6yk6QsWUvBg-qz1dIGSrcZ1TEfIp9ONaqgSBjWy9TiuQ&oe=6A1BFBE5)

## Limitations

- Coupon code templates are currently not supported by the WhatsApp web client.
- Copy code button text cannot be customized.
- Templates are limited to one copy code button.

## Creating coupon code templates

Use the [Message Templates API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/template-api#post-version-waba-id-message-templates) to create coupon code templates.

### Request syntax

```html
curl 'https://graph.facebook.com/<API_VERSION>/<WHATSAPP_BUSINESS_ACCOUNT_ID>/message_templates' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <ACCESS_TOKEN>' \
-d '
{
  "name": "<TEMPLATE_NAME>",
  "language": "<TEMPLATE_LANGUAGE>",
  "category": "marketing",
  "components": [

    <!-- Only if using a header component -->
    {
      "type": "header",
      "format": "text",
      "text": "<HEADER_TEXT>"
    },

    {
      "type": "body",
      "text": "<BODY_TEXT>",

      <!-- Only include if body text includes one or more parameters -->
      "example": {
        "body_text": [
          [
            "<BODY_PARAMETER_EXAMPLE_VALUE>"
            <!-- Additional examples values would follow, if using multiple body parameters -->
          ]
        ]
      }
    },
    {
      "type": "buttons",
      "buttons": [

        <!-- Only if using a quick-reply button -->
        {
          "type": "quick_reply",
          "text": "<QUICK_REPLY_BUTTON_LABEL_TEXT>"
        },

        {
          "type": "copy_code",
          "example": "<COPY_CODE_BUTTON_EXAMPLE_CODE>"
        }
      ]
    }
  ]
}'
```

### Request parameters

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<ACCESS_TOKEN>`<br>*String* | **Required.**<br>Access token. | `EAAAN...` |
| `<API_VERSION>`<br>*String* | **Optional.**<br>API version. If omitted, defaults to the newest API version available to your app. | `v23.0` |
| `<BODY_PARAMETER_EXAMPLE_VALUE>`<br>*String* | **Required if using a body component string that includes one or more parameters.**<br>Example parameter value. You must supply an example for each parameter defined in your body component string. | `0itCfer5xDB14SHWLACB` |
| `<BODY_TEXT>`<br>*String* | **Required.**<br>Template body text. Variables are supported.<br>Maximum 1024 characters. | `Shop now through the end of December and use the one-time use code {{1}} to get {{2}} off of your entire order!` |
| `<COPY_CODE_BUTTON_EXAMPLE_CODE>`<br>*String* | **Required.**<br>Code to be copied to device clipboard when tapped.<br>Maximum 20 characters. | `fLBponPDsqF0KQThzkrf` |
| `<HEADER_TEXT>`<br>*String* | **Required if using a text header component.**<br>Header text.<br>Maximum 60 characters. | `Our Winter Sale is on!` |
| `<QUICK_REPLY_BUTTON_LABEL_TEXT>` | **Required if using a quick-reply button.**<br>Button label text. Maximum 25 characters. Alphanumeric characters only. | `Unsubscribe` |
| `<TEMPLATE_LANGUAGE>`<br>*String* | **Required.**<br>Template [language code](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/supported-languages). | `en_US` |
| `<TEMPLATE_NAME>`<br>*String* | **Required.**<br>Template name. Must be unique, unless existing templates with the same name have a different template language.<br>Maximum 512 characters. Lowercase, alphanumeric characters and underscores only. | `coupon_code_onetime_winter_2025` |
| `<WHATSAPP_BUSINESS_ACCOUNT_ID>`<br>*String* | **Required.**<br>WhatsApp Business Account ID. | `102290129340398` |

### Response syntax

Upon success:

```html
{
  "id": "<TEMPLATE_ID>",
  "status": "<TEMPLATE_STATUS>",
  "category": "<TEMPLATE_CATEGORY>"
}
```

### Response parameters

| Placeholder | Description | Example value |
| --- | --- | --- |
| `<TEMPLATE_CATEGORY>` | [Template category](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-categorization). | `MARKETING` |
| `<TEMPLATE_ID>` | Template ID. | `1627019861106475` |
| `<TEMPLATE_STATUS>` | [Template status](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview#template-status). | `PENDING` |

### Example request

```curl
curl 'https://graph.facebook.com/v25.0/102290129340398/message_templates' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "name": "coupon_code_onetime_winter_2025",
  "language": "en_US",
  "category": "marketing",
  "components": [
    {
      "type": "header",
      "format": "text",
      "text": "Our Winter Sale is on!"
    },
    {
      "type": "BODY",
      "text": "Shop now through the end of December and use the one-time use code {{1}} to get {{2}} off of your entire order!",
      "example": {
        "body_text": [
          [
            "fLBponPDsqF0KQThzkrf",
            "30%"
          ]
        ]
      }
    },
    {
      "type": "BUTTONS",
      "buttons": [
        {
          "type": "QUICK_REPLY",
          "text": "Unsubscribe"
        },
        {
          "type": "COPY_CODE",
          "example": "fLBponPDsqF0KQThzkrf"
        }
      ]
    }
  ]
}'
```

### Example response

```json
{
  "category" : "MARKETING",
  "id" : "1924084211297547",
  "status" : "PENDING"
}
```

## Sending coupon code templates

### Request syntax

Use the [Messages API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api#post-version-phone-number-id-messages) to send an approved coupon template in a template message.

```html
curl -X POST "https://graph.facebook.com/<API_VERSION>/<BUSINESS_PHONE_NUMBER_ID>/messages" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '
{
    "messaging_product": "whatsapp",
    "to": "<USER_PHONE_NUMBER>",
    "type": "template",
    "template": {
      "name": "<TEMPLATE_NAME>",
      "language": {
        "code": "<TEMPLATE_LANGUAGE>"
      },
      "components": [
        {
          "type": "button",
          "sub_type": "copy_code",
          "index": <BUTTON_INDEX>,
          "parameters": [
            {
              "type": "coupon_code",
              "coupon_code": "<COUPON_CODE>"
            }
          ]
        }
        <!-- Additional components would follow, if templates requires them -->
      ]
    }
  }'
```

### Request parameters

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<ACCESS_TOKEN>`<br>*String* | **Required.**<br>Access token. | `EAAAN...` |
| `<API_VERSION>`<br>*String* | **Optional.**<br>API version. If omitted, defaults to the newest API version available to your app. | `v23.0` |
| `<BUSINESS_PHONE_NUMBER_ID>`<br>*String* | **Required.**<br>WhatsApp business phone number ID. | `106540352242922` |
| `<BUTTON_INDEX>`<br>*Integer* | **Required.**<br>Indicates order in which button should appear, if the template uses multiple buttons.<br>Buttons are zero-indexed, so setting value to `0` will cause the button to appear first, and another button with an index of `1` will appear next, etc. | `0` |
| `<COUPON_CODE>`<br>*String* | **Required.**<br>The coupon code to be copied when the customer taps the button. Only accepting alphanumeric characters.<br>Maximum 20 characters. | `25OFF` |
| `<TEMPLATE_NAME>`<br>*String* | **Required.**<br>Name of the template to be sent. | `coupon_code_fall2023_25off` |
| `<TEMPLATE_LANGUAGE>`<br>*String* | **Required.**<br>The template’s language and locale code. | `en_US` |
| `<USER_PHONE_NUMBER>`<br>*String* | **Required.**<br>The WhatsApp ID or phone number of the customer to send the message to. See [Phone Number Formats](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api). | `+16505551234` |

### Response syntax

Upon success the API will respond with:

```html
{
  "messaging_product": "whatsapp",
  "contacts": [
    {
      "input": "<WHATSAPP_USER_PHONE_NUMBER>",
      "wa_id": "<WHATSAPP_USER_ID>"
    }
  ],
  "messages": [
    {
      "id": "<WHATSAPP_MESSAGE_ID>",
      "group_id": "<GROUP_ID>", <!-- Only included if messaging a group -->
      "message_status": "<PACING_STATUS>" <!-- Only included if sending a template -->
    }
  ]
}
```

### Response parameters

| Placeholder | Description | Sample Value |
| --- | --- | --- |
| `<GROUP_ID>`<br>*String* | The string identifier of a group made using the Groups API.<br>This field shows when messages are sent, received, or read from a group.<br>[Learn more about the Groups API](https://developers.facebook.com/documentation/business-messaging/whatsapp/groups) | `Y2FwaV9ncm91cDoxNzA1NTU1MDEzOToxMjAzNjM0MDQ2OTQyMzM4MjAZD` |
| `<PACING_STATUS>`<br>*String* | Indicates [template pacing](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-pacing) status. The `message_status` property is only included in responses when sending a [template message](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview) that uses a template that is being paced. | `wamid.HBgLMTY0NjcwNDM1OTUVAgARGBI4MjZGRDA0OUE2OTQ3RkEyMzcA` |
| `<WHATSAPP_USER_PHONE_NUMBER>`<br>*String* | WhatsApp user’s WhatsApp phone number. May not match `wa_id` value. | `+16505551234` |
| `<WHATSAPP_USER_ID>`<br>*String* | WhatsApp user’s WhatsApp ID. May not match `input` value. | `16505551234` |
| `<WHATSAPP_MESSAGE_ID>`<br>*String* | WhatsApp Message ID. This ID appears in associated **messages** webhooks, such as sent, read, and delivered webhooks. | `wamid.HBgLMTY0NjcwNDM1OTUVAgARGBI4MjZGRDA0OUE2OTQ3RkEyMzcA` |

### Example Request

```curl
curl 'https://graph.facebook.com/v25.0/106540352242922/messages' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "messaging_product": "whatsapp",
  "to": "16505551234",
  "type": "template",
  "template": {
    "name": "coupon_code_fall2023_25off",
    "language": {
      "code": "en_US"
    },
    "components": [
      {
        "type": "body",
        "parameters": [
          {
            "type": "text",
            "text": "25OFF"
          },
          {
            "type": "text",
            "text": "25%"
          }
        ]
      },
      {
        "type": "button",
        "sub_type": "COPY_CODE",
        "index": 1,
        "parameters": [
          {
            "type": "coupon_code",
            "coupon_code": "25OFF"
          }
        ]
      }
    ]
  }
}'
```

### Example Response

```json
{
  "messaging_product": "whatsapp",
  "contacts": [
    {
      "input": "16505551234",
      "wa_id": "16505551234"
    }
  ],
  "messages": [
    {
      "id": "wamid.HBgLMTY1MDM4Nzk0MzkVAgARGBIxRjk1REYzMDBERDE3RUI0RDYA"
    }
  ]
}
```
