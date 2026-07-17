# Limited-time offer templates | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/marketing-templates/limited-time-offer-templates_

---

# Limited-time offer templates

Updated: May 6, 2026

This document describes limited-time offer templates and how to use them.

Limited-time offer templates allow you to display expiration dates and running countdown timers for offer codes in template messages, making it easy for you to communicate time-bound offers and drive customer engagement.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/385485492_1044097420371007_6435130166952753459_n.png?_nc_cat=110&ccb=1-7&_nc_sid=e280be&_nc_ohc=0wqL3qGCSKUQ7kNvwEcZRu7&_nc_oc=AdriHm7cQWfw7mzPiUp5gHZ7nZGlhXddWHLOoVe_zcFTryYwPKnZHQpxM4EyK62-KVc&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=naipy4Pu8IpHpzOuyZ6rWw&_nc_ss=7b20f&oh=00_Af7em9qkytS0TmjvcP6a2VoVT3G4cjzKnelOqfBrFjdJUg&oe=6A1C0E3F)

## Limitations

- Only templates categorized as `MARKETING` are supported.
- Footer components are not supported.
- Users who view a limited-time offer template message using that WhatsApp web app or desktop app will not see the offer, but will instead see a message indicating that they have received a message but that it’s not supported in the client they are using.

## Creating limited-time offer templates

Use the [Message Templates API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/template-api#post-version-waba-id-message-templates) to create a limited-time offer template.

### Request syntax

```json
curl -X POST "https://graph.facebook.com/v23.0/<WHATSAPP_BUSINESS_ACCOUNT_ID>/message_templates" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '
{
    "name": "<TEMPLATE_NAME>",
    "language": "<TEMPLATE_LANGUAGE>",
    "category": "marketing",
    "components": [
      {
        "type": "header",
        "format": "<HEADER_FORMAT>",
        "example": {
          "header_handle": [
            "<HEADER_ASSET_HANDLE>"
          ]
        }
      },
      {
        "type": "limited_time_offer",
        "limited_time_offer": {
          "text": "<LIMITED_TIME_OFFER_TEXT>",
          "has_expiration": <HAS_EXPIRATION>
        }
      },
      {
        "type": "body",
        "text": "<BODY_TEXT>",
        "example": {
          "body_text": [<BODY_TEXT_VARIABLE_EXAMPLES>]
        }
      },
      {
        "type": "buttons",
        "buttons": [
          {
            "type": "copy_code",
            "example": "<OFFER_CODE_EXAMPLE>"
          },
          {
            "type": "url",
            "text": "<URL_BUTTON_TEXT>",
            "url": "<URL_BUTTON_URL>",
            "example": [
              "<URL_EXAMPLE_WITH_VARIABLE_EXAMPLE>"
            ]
          }
        ]
      }
    ]
  }'
```

### Request parameters

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<BODY_TEXT>`<br>*String* | **Required.**<br>Body component text. Supports variables.<br>Maximum 600 characters. | `Good news, {{1}}! Use code {{2}} to get 25% off all Caribbean Destination packages!` |
| `<BODY_TEXT_VARIABLE_EXAMPLES>`<br>*Array of strings* | **Required if body component text uses variables.**<br>Array of example variable strings.<br>Must supply examples for all placeholders in `<BODY_TEXT>` string.<br>No maximum, but counts against `<BODY_TEXT>` maximum. | `["Pablo","CARIBE25"]` |
| `<HAS_EXPIRATION>`<br>*Boolean* | **Optional.**<br>Set to `true` to have the [offer expiration details](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/marketing-templates/limited-time-offer-templates#offer-expiration-details) appear in the delivered message. | `true` |
| `<HEADER_ASSET_HANDLE>`<br>*Media asset handle* | **Required if using an image or video header.**<br>Uploaded media asset handle. Use the [Resumable Upload API](https://developers.facebook.com/docs/graph-api/guides/upload) to generate an asset handle. | `4::aW...` |
| `<HEADER_FORMAT>`<br>*Enum* | **Required if using a header.**<br>Can be `IMAGE`, or `VIDEO`. | `IMAGE` |
| `<LIMITED_TIME_OFFER_TEXT>`<br>*String* | **Required.**<br>Offer details text.<br>Maximum 16 characters. | `Expiring offer!` |
| `<OFFER_CODE_EXAMPLE>`<br>*String* | **Required.**<br>Example offer code.<br>Maximum 15 characters. | `CARIBE25` |
| `<TEMPLATE_LANGUAGE>`<br>*Enum* | **Required.**<br>Template [language and locale code](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/supported-languages). | `en_US` |
| `<TEMPLATE_NAME>`<br>*String* | **Required.**<br>Template name.<br>Maximum 512 characters. | `limited_time_offer_caribbean_pkg_2023` |
| `<URL_BUTTON_TEXT>`<br>*String* | **Required.**<br>[URL button](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/components#url-buttons) label text. Supports 1 variable.<br>25 characters maximum. | `Book now!` |
| `<URL_BUTTON_URL>`<br>*String* | **Required.**<br>URL of website that loads in the device’s default mobile web browser when the [URL button](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/components#url-buttons) is tapped by the WhatsApp user.<br>Supports 1 variable appended to the end of the URL string.<br>Maximum 2000 characters. | `https://awesomedestinations.com/offers?code={{1}}` |
| `<URL_EXAMPLE_WITH_VARIABLE_EXAMPLE>`<br>*String* | **Required if URL uses a variable.**<br>Example URL with example variable appended to the end.<br>No maximum, but value counts against `<URL_BUTTON_URL>` maximum. | `https://awesomedestinations.com/offers?ref=n3mtql` |

### Offer expiration details

The delivered message can display an offer expiration details section with a heading, an optional expiration timer, and the offer code itself.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/384988489_703197894993408_6289249753669812858_n.png?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=wtXocxvVNlwQ7kNvwHavTWv&_nc_oc=Adp35vcl7GzfDIpuU2nAFXJJYVjq7MzcqqOB0Rl2s2fKM8KT5crh2jTnlgTopGSMXcQ&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=naipy4Pu8IpHpzOuyZ6rWw&_nc_ss=7b20f&oh=00_Af5zzN_Xgd_hoJPTkTT44RvOy94rIgUHmLAQ_EO3ZDZEdQ&oe=6A1C1AE1)

The expiration timer is a text string that is not customizable, but it will change to red text if the message is viewed and the offer code is expiring within the next hour. (You include the actual offer code and its expiration timestamp when you send the template in a template message.)

### Example request

This is an example request to create a limited-time offer template that uses:

- an image header component
- body text component with variables
- the limited time offer component
- a copy code button
- a button URL with a variable

```curl
curl 'https://graph.facebook.com/v17.0/102290129340398/message_templates' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "name": "limited_time_offer_caribbean_pkg_2023",
  "language": "en_US",
  "category": "marketing",
  "components": [
    {
      "type": "header",
      "format": "image",
      "example": {
        "header_handle": [
          "4::aW..."
        ]
      }
    },
    {
      "type": "limited_time_offer",
      "limited_time_offer": {
        "text": "Expiring offer!",
        "has_expiration": true
      }
    },
    {
      "type": "body",
      "text": "Good news, {{1}}! Use code {{2}} to get 25% off all Caribbean Destination packages!",
      "example": {
        "body_text": [
          [
            "Pablo",
            "CARIBE25"
          ]
        ]
      }
    },
    {
      "type": "buttons",
      "buttons": [
        {
          "type": "copy_code",
          "example": "CARIBE25"
        },
        {
          "type": "url",
          "text": "Book now!",
          "url": "https://awesomedestinations.com/offers?code={{1}}",
          "example": [
            "https://awesomedestinations.com/offers?ref=n3mtql"
          ]
        }
      ]
    }
  ]
}'
```

### Example response

```json
{
  "id": "546151681022936",
  "status": "PENDING",
  "category": "MARKETING"
}
```

## Sending limited-time offer templates

Use the [Messages API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api#post-version-phone-number-id-messages) to send an approved limited-time offer template in a template message.

### Request syntax

```json
curl -X POST "https://graph.facebook.com/v23.0/<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>/messages" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '
{
    "messaging_product": "whatsapp",
    "recipient_type": "individual",
    "to": "<CUSTOMER_PHONE_NUMBER>",
    "type": "template",
    "template": {
      "name": "<TEMPLATE_NAME>",
      "language": {
        "code": "<TEMPLATE_LANGUAGE_CODE>"
      },
      "components": [
        {
          "type": "header",
          "parameters": [
            {
              "type": "<HEADER_TYPE>",
              "<HEADER_TYPE>": {
                "id": "<HEADER_ASSET_ID>"
              }
            }
          ]
        },
        {
          "type": "body",
          "parameters": [
            <BODY_VARIABLES>
          ]
        },
        {
          "type": "limited_time_offer",
          "parameters": [
            {
              "type": "limited_time_offer",
              "limited_time_offer": {
                "expiration_time_ms": <EXPIRATION_TIME>
              }
            }
          ]
        },
        {
          "type": "button",
          "sub_type": "copy_code",
          "index": 0,
          "parameters": [
            {
              "type": "coupon_code",
              "coupon_code": "<OFFER_CODE>"
            }
          ]
        },
        {
          "type": "button",
          "sub_type": "url",
          "index": <URL_BUTTON_INDEX>,
          "parameters": [
            {
              "type": "text",
              "text": "<URL_VARIABLE>"
            }
          ]
        }
      ]
    }
  }'
```

### Request parameters

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<BODY_VARIABLES>`<br>*Array of objects* | **Required if template body text uses variables.**<br>Body text variable values. Define each variable as an individual object. | `{"type":"text","text":"Pablo"},{"type":"text","text":"CARIBE25"}` |
| `<CUSTOMER_PHONE_NUMBER>`<br>*String* | **Required.**<br>Phone number of customer who the template message should be sent to. | `+16505555555` |
| `<EXPIRATION_TIME>`<br>*Unix timestamp* | **Required.**<br>Offer code expiration time as a UNIX timestamp in milliseconds. | `1698562800000` |
| `<HEADER_ASSET_ID>`<br>*Media asset ID* | **Required.**<br>Uploaded media asset ID. Use the [/PHONE_NUMBER_ID/media](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api) endpoint to generate an ID. | `1602186516975000` |
| `<HEADER_TYPE>`<br>*String* | **Required.**<br>Header type used by the template. Values can be `image` or `video`. | `image` |
| `<OFFER_CODE>`<br>*String* | **Required if template uses a copy code button.**<br>Offer code.<br>Maximum 15 characters. | `CARIBE25` |
| `<TEMPLATE_LANGUAGE_CODE>`<br>*Enum* | **Required.**<br>The template’s [language and locale code](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/supported-languages). | `en_US` |
| `<TEMPLATE_NAME>`<br>*String* | **Required.**<br>The template’s name. | `limited_time_offer_caribbean_pkg_2023` |
| `<URL_BUTTON_INDEX>`<br>*Integer* | **Required.**<br>URL button index. If the template uses a copy code button, value must be `1`.<br>If the template does not use a copy code button, the value must be `0`. | `1` |
| `<URL_VARIABLE>`<br>*String* | **Required if URL uses a variable.**<br>URL variable value.<br>No maximum but value counts against URL string maximum of 2000 characters. | `n3mtql` |

### Example request

Example request to send a limited-time offer template that uses:

- an image header
- body text variables
- the offer expiration details
- a copy code button
- a URL button with a variable

```curl
curl 'https://graph.facebook.com/v17.0/106540352242922/messages' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "16505555555",
  "type": "template",
  "template": {
    "name": "limited_time_offer_caribbean_pkg_2023",
    "language": {
      "code": "en_US"
    },
    "components": [
      {
        "type": "header",
        "parameters": [
          {
            "type": "image",
            "image": {
              "id": "1602186516975000"
            }
          }
        ]
      },
      {
        "type": "body",
        "parameters": [
          {
            "type": "text",
            "text": "Pablo"
          },
          {
            "type": "text",
            "text": "CARIBE25"
          }
        ]
      },
      {
        "type": "limited_time_offer",
        "parameters": [
          {
            "type": "limited_time_offer",
            "limited_time_offer": {
              "expiration_time_ms": 1209600000
            }
          }
        ]
      },
      {
        "type": "button",
        "sub_type": "copy_code",
        "index": 0,
        "parameters": [
          {
            "type": "coupon_code",
            "coupon_code": "CARIBE25"
          }
        ]
      },
      {
        "type": "button",
        "sub_type": "url",
        "index": 1,
        "parameters": [
          {
            "type": "text",
            "text": "n3mtql"
          }
        ]
      }
    ]
  }
}'
```

### Example response

```json
{
  "messaging_product": "whatsapp",
  "contacts": [
    {
      "input": "16505555555",
      "wa_id": "16505555555"
    }
  ],
  "messages": [
    {
      "id": "wamid.HBgLMTY1MDUwNzY1MjAVAgARGBI5QTNDQTVCM0Q0Q0Q2RTY3RTcA"
    }
  ]
}
```

## Combining with payment request buttons

This feature is only available for businesses based in Brazil using payment request CTA buttons with Pix, Boleto, or Payment Link.

You can combine limited-time offer templates with payment request CTA buttons to send time-sensitive payment requests that display a countdown timer alongside payment options. This is useful for scenarios such as flash sales or promotional discounts with a deadline where the payment method should be readily accessible within the message.

For template creation payloads, supported payment methods, button configuration, and expiration management details, see [Payment Request CTA Templates (Brazil)](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/payment-request-cta).
