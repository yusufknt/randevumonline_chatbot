# Catalog templates | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/catalogs/catalog-template-messages_

---

# Catalog templates

Updated: Mar 3, 2026

This document explains how to create catalog templates. See [Sell Products & Services](https://developers.facebook.com/documentation/business-messaging/whatsapp/catalogs/catalogs-overview) to learn more about product catalogs and ways to showcase your products.

Catalog templates are marketing templates that allow you to showcase your product catalog entirely within WhatsApp. Catalog templates display a product thumbnail header image of your choice and custom body text, along with a fixed text header and fixed text sub-header.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/354047426_125269187252102_7173148343631613735_n.png?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=14131RCcGscQ7kNvwGiVexH&_nc_oc=AdripxlbU0d3LosQgw5nQsmznDp9yKY5fF8MyoHD4fNmygSFZfoScWUgWT_E-RmqdXw&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=IQtwjvwGuYEG9a4QD4y3Cg&_nc_ss=7b20f&oh=00_Af5u0MlLYCsSmyxM82GyEQ4cCC27Xg9YBURS9m2Hfyk5VQ&oe=6A1C1426)

When a customer taps the **View catalog** button in a catalog template message, your product catalog appears within WhatsApp.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/353808079_9331603410246288_3629219693038191737_n.png?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=Tjzfo9GLP9wQ7kNvwEnnrmm&_nc_oc=AdoVfEhnDqlVglEUtaWEpE3kAJaHyZsSMGoufXHVv9VYMv-KXFdCVurknFg71-A90_I&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=IQtwjvwGuYEG9a4QD4y3Cg&_nc_ss=7b20f&oh=00_Af7DsBgezIbzhNYDDGJbMwdj8Hal1u1h-jVgN77F_a-hrA&oe=6A1C19E8)

## Creating catalog templates

### Requirements

You must have [inventory uploaded to Meta](https://developers.facebook.com/documentation/business-messaging/whatsapp/catalogs/upload-inventory) in an e-commerce catalog [connected to your WhatsApp Business Account](https://www.facebook.com/business/help/158662536425974).

### Request syntax

Use the [Message Templates API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/template-api#post-version-waba-id-message-templates) to create a catalog template. Once your template is approved, you can use the [Messages API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api#post-version-phone-number-id-messages) to send it in a template message.

```json
curl -X POST "https://graph.facebook.com/<API_VERSION>/<WHATSAPP_BUSINESS_ACCOUNT_ID>/message_templates" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '
{
    "name": "<NAME>",
    "language": "<LANGUAGE>",
    "category": "MARKETING",
    "components": [
      {
        "type": "BODY",
        "text": "<BODY_TEXT>",
        "example": {
          "body_text": [
            [
              "<EXAMPLE_BODY_TEXT>"
            ]
          ]
        }
      },
      {
        "type": "FOOTER",
        "text": "<FOOTER_TEXT>"
      },
      {
        "type": "BUTTONS",
        "buttons": [
          {
            "type": "CATALOG",
            "text": "View catalog"
          }
        ]
      }
    ]
  }'
```

### Request parameters

| Placeholder | Description | Sample Value |
| --- | --- | --- |
| `<BODY_TEXT>`<br>*String* | **Required.**<br>Template body text. Variables are supported.<br>Maximum 1024 characters. | `Now shop for your favorite products right here on WhatsApp! Get Rs {{1}} off on all orders above {{2}}Rs! Valid for your first {{3}} orders placed on WhatsApp!` |
| `<EXAMPLE_BODY_TEXT>`<br>*String (of an array of strings)* | **Required if body text uses variables.**<br>Sample strings to replace variable placeholders in `<BODY_TEXT>` string.<br>Maximum 1024 characters. | `100` |
| `<FOOTER_TEXT>`<br>*String* | **Optional.**<br>Template footer text. Variables are supported.<br>Maximum 60 characters. | `Best grocery deals on WhatsApp!` |
| `<LANGUAGE>`<br>*String* | **Required.**<br>Template [language and locale code](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/supported-languages). | `en_US` |
| `<NAME>`<br>*String* | **Required.**<br>Template name.<br>Maximum 512 characters. | `intro_catalog_offer` |

### Example request

```curl
curl 'https://graph.facebook.com/v17.0/102290129340398/message_templates' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "name": "intro_catalog_offer",
  "language": "en_US",
  "category": "MARKETING",
  "components": [
    {
      "type": "BODY",
      "text": "Now shop for your favorite products right here on WhatsApp! Get Rs {{1}} off on all orders above {{2}}Rs! Valid for your first {{3}} orders placed on WhatsApp!",
      "example": {
        "body_text": [
          [
            "100",
            "400",
            "3"
          ]
        ]
      }
    },
    {
      "type": "FOOTER",
      "text": "Best grocery deals on WhatsApp!"
    },
    {
      "type": "BUTTONS",
      "buttons": [
        {
          "type": "CATALOG",
          "text": "View catalog"
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

## Sending catalog template messages

You can send approved [catalog templates](https://developers.facebook.com/documentation/business-messaging/whatsapp/catalogs/catalog-template-messages) in a template message. See [Sell Products & Services](https://developers.facebook.com/documentation/business-messaging/whatsapp/catalogs/catalogs-overview) to learn more about product catalogs and ways to showcase your products.

### Requirements

You must have [inventory uploaded to Meta](https://developers.facebook.com/documentation/business-messaging/whatsapp/catalogs/upload-inventory) in an e-commerce catalog [connected to your WhatsApp Business Account](https://www.facebook.com/business/help/158662536425974).

### Request syntax

Use the [Messages API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api#post-version-phone-number-id-messages) to send a catalog template message using a catalog template with an `APPROVED` status.

```json
curl -X POST "https://graph.facebook.com/v19.0/<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>/messages" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '
{
    "messaging_product": "whatsapp",
    "recipient_type": "individual",
    "to": "<TO>",
    "type": "template",
    "template": {
      "name": "<NAME>",
      "language": {
        "code": "<CODE>"
      },
      "components": [
        {
          "type": "body",
          "parameters": [
            {
              "type": "<TYPE>",
              "text": "<TEXT>"
            }
          ]
        },
        {
          "type": "button",
          "sub_type": "CATALOG",
          "index": 0,
          "parameters": [
            {
              "type": "action",
              "action": {
                "thumbnail_product_retailer_id": "<THUMBNAIL_PRODUCT_RETAILER_ID>"
              }
            }
          ]
        }
      ]
    }
  }'
```

### Request parameters

| Placeholder | Description | Sample Value |
| --- | --- | --- |
| `<CODE>`<br>*String* | **Required.**<br>Template [language and locale code](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/supported-languages). | `en_US` |
| `<NAME>`<br>*String* | **Required.**<br>Template name. | `intro_catalog_offer` |
| `<THUMBNAIL_PRODUCT_RETAILER_ID>`<br>*String* | **Optional.**<br>Item SKU number. Labeled as Content ID in the Commerce Manager.<br>The thumbnail of this item will be used as the message’s header image.<br>If the `parameters` object is omitted, the product image of the first item in your catalog will be used. | `2lc20305pt` |
| `<TEXT>`<br>*String* | **Required if template uses variables.**<br>Template variable. | `100` |
| `<TO>`<br>*String* | **Required.**<br>Customer phone number. | `+16505551234` |
| `<TYPE>`<br>*String* | **Required if template uses variables.**<br>Template variable type. | `text` |

### Example request

```curl
curl 'https://graph.facebook.com/v17.0/106540352242922/messages' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "+16505551234",
  "type": "template",
  "template": {
    "name": "intro_catalog_offer",
    "language": {
      "code": "en_US"
    },
    "components": [
      {
        "type": "body",
        "parameters": [
          {
            "type": "text",
            "text": "100"
          },
          {
            "type": "text",
            "text": "400"
          },
          {
            "type": "text",
            "text": "3"
          }
        ]
      },
      {
        "type": "button",
        "sub_type": "CATALOG",
        "index": 0,
        "parameters": [
          {
            "type": "action",
            "action": {
              "thumbnail_product_retailer_id": "2lc20305pt"
            }
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
      "input": "+16505551234",
      "wa_id": "16505551234"
    }
  ],
  "messages": [
    {
      "id": "wamid.HBgLMTY1MDM4Nzk0MzkVAgARGBI5RkEwM0EyODFEQzQ2NDYzQTMA"
    }
  ]
}
```

## See also

- [Sell Products & Services](https://developers.facebook.com/documentation/business-messaging/whatsapp/catalogs/catalogs-overview)
- [Catalog Messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/catalogs/share-products#catalog-messages)
