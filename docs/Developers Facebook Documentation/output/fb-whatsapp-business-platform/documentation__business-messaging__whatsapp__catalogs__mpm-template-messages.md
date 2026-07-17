# Multi-product message templates | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/catalogs/mpm-template-messages_

---

# Multi-product message templates

Updated: Mar 3, 2026

This document describes multi-product message (“MPM”) templates, their uses, and how to use them.

MPM templates are marketing templates that allow you to showcase up to 30 products from your ecommerce catalog, organized in up to 10 sections, in a single message.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/345336924_1476472873159435_9050004394387774321_n.png?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=TwzPu0nWHC8Q7kNvwHNcCEC&_nc_oc=AdoFudCkxjn3VzNudjvVCdVywWwCGStRzX-YlsJ5NRafZ1AoivjdqaUBB7j03W-JVQU&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=CSuhdPqY5wU8E_i75Znc8g&_nc_ss=7b20f&oh=00_Af6sqmN3ZxTZUJ4aZUxTqT46Fr2xXn6dCle4jtQxPoVw_w&oe=6A1BFF9C)

Customers can browse products and sections within the message, view details for each product, add and remove products from their cart, and submit their cart to place an order. Orders are then sent to you via a webhook.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/345301814_777009393786308_8675106872073624223_n.png?_nc_cat=101&ccb=1-7&_nc_sid=e280be&_nc_ohc=EYvuOncDptQQ7kNvwHdDCzq&_nc_oc=AdoJaCP-RzGwUGDZ5TjSDLn6qQO8AXAU5_gqMDKafU7e81xjMC2WvFrj-bXEHtVgM_s&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=CSuhdPqY5wU8E_i75Znc8g&_nc_ss=7b20f&oh=00_Af5gY4Qi-TTa3ZyiRBF_EjZNZoOf0hmINBg_iAWI_uBy_Q&oe=6A1C1EA9)

See our help center article [About Multi-product message templates on WhatsApp](https://www.facebook.com/business/help/978451836847222) for common use cases and tips on how to make the most of MPM templates.

## Requirements

In order to create and use MPM templates you must have an ecommerce product catalog, with inventory, connected to your WhatsApp Business Account. See the Cloud API [Commerce](https://developers.facebook.com/documentation/business-messaging/whatsapp/catalogs/catalogs-overview) guide.

## Limitations

- Customers must be using WhatsApp v2.22.24 or greater.
- MPM templates cannot be forwarded to other customers.

## Creating MPM templates

You can create MPM templates using the [Message Templates API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/template-api#post-version-waba-id-message-templates) or the [**WhatsApp Manager**](https://business.facebook.com/wa/manage/home/) > **Account tools** > **Message templates** panel. Once your template is approved, you can use the [Messages API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api#post-version-phone-number-id-messages) to send it in a template message.

### Request syntax

```json
curl -X POST "https://graph.facebook.com/v23.0/<WHATSAPP_BUSINESS_ACCOUNT_ID>/message_templates" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "<NAME>",
    "category": "<CATEGORY>",
    "language": "<LANGUAGE>",
    "components": [<COMPONENTS>]
  }'
```

### Request parameters

| Placeholder | Description | Sample Value |
| --- | --- | --- |
| `<CATEGORY>` | **Required.**<br>Template category. Set this to `MARKETING`. | `MARKETING` |
| `<COMPONENTS>` | **Required.**<br>Array of objects that describe the components that make up the template. See [Components](https://developers.facebook.com/documentation/business-messaging/whatsapp/catalogs/mpm-template-messages#components) below. | See [Components](https://developers.facebook.com/documentation/business-messaging/whatsapp/catalogs/mpm-template-messages#components) below. |
| `<LANGUAGE>` | **Required.**<br>Template [language and locale code](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/supported-languages). | `en_US` |
| `<NAME>` | **Required.**<br>Template name.<br>Maximum 512 characters. | `abandoned_cart` |

### Components

The `components` value must be an array of objects that describes each component that makes up the template. MPM templates must have the following components:

- a single header component
- a single body component
- a single footer component (optional)
- a single MPM button component

```json
[
  {
    "type": "HEADER",
    "format": "TEXT",
    "text": "<HEADER_TEXT>",

    /* Example required if header uses a variable */
    "example": {
      "header_text": [
        "<HEADER_EXAMPLE_TEXT>"
      ]
    }
  },
  {
    "type": "BODY",
    "text": "<BODY_TEXT>",

    /* Example required if body uses variables */
​​    "example": {
      "body_text": [
        [
          "<BODY_EXAMPLE_TEXT>"
        ]
      ]
    }
  },
  {
    "type": "FOOTER",
    "text": "<FOOTER_TEXT>"
  },
  {
    "type":"BUTTONS",
    "buttons": [
      {
        "type": "MPM",
        "text": "View items"
      }
    ]
  }
]
```

### Request parameters

| Placeholder | Description | Sample Value |
| --- | --- | --- |
| `<BODY_EXAMPLE_TEXT>` | String or array of strings. Example body variable value(s). | `10OFF` |
| `<BODY_TEXT>` | Template body text. Supports multiple variables.<br>If the string contains variables, you must include the example property and sample variable values.<br>1024 characters maximum. | `Forget something, {{1}}?` |
| `<FOOTER_TEXT>` | Template footer text.<br>60 characters maximum. | `Lucky Shrub, 1 Hacker Way, Menlo Park, CA 94025` |
| `<HEADER_EXAMPLE_TEXT>` | Example header variable value. | `Pablo` |
| `<HEADER_TEXT>` | Template header text. Supports 1 variable.<br>If the string contains a variable, you must include the example property and a sample variable value.<br>60 characters maximum. | `Looks like you left these items in your cart, still interested? Use code {{1}} to get 10% off!` |

### Response

Upon success, the API will respond with:

```json
{
  "id": "<ID>",
  "status": "<STATUS>",
  "category": "MARKETING"
}
```

### Response parameters

| Placeholder | Description | Sample Value |
| --- | --- | --- |
| `<ID>` | Template ID. | `546151681022936` |
| `<STATUS>` | Template status. Only templates with an `APPROVED` status can be sent in a template message. | `PENDING` |

### Example request

```curl
curl 'https://graph.facebook.com/v25.0/102290129340398/message_templates' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "name": "abandoned_cart",
  "language": "en_US",
  "category": "MARKETING",
  "components": [
    {
      "type": "HEADER",
      "format": "TEXT",
      "text": "Forget something, {{1}}?",
      "example": {
        "header_text": [
          "Pablo"
        ]
      }
    },
    {
      "type": "BODY",
      "text": "Looks like you left these items in your cart, still interested? Use code {{1}} to get 10% off!",
      "example": {
        "body_text": [
          [
            "10OFF"
          ]
        ]
      }
    },
    {
      "type":"BUTTONS",
      "buttons": [
        {
          "type": "MPM",
          "text": "View items"
        }
      ]
    }
  ]
}'
```

### Sample response

```json
{
  "id": "546151681022936",
  "status": "PENDING",
  "category": "MARKETING"
}
```

## Webhooks

When a customer adds one or more products to their cart and submits an order, a webhook describing the order is sent to you.

### Webhook syntax

```json
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "<ENTRY.ID>",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "<DISPLAY_PHONE_NUMBER>",
              "phone_number_id": "<PHONE_NUMBER_ID>"
            },
            "contacts": [
              {
                "profile": {
                  "name": "<NAME>"
                },
                "wa_id": "<WA_ID>"
              }
            ],
            "messages": [
              {
                "from": "<FROM>",
                "id": "<MESSAGES.ID>",
                "timestamp": "<TIMESTAMP>",
                "type": "order",
                "order": {
                  "catalog_id": "<CATALOG_ID>",
                  "product_items": [
                    {
                      "product_retailer_id": "<PRODUCT_RETAILER_ID>",
                      "quantity": <QUANTITY>,
                      "item_price": <ITEM_PRICE>,
                      "currency": "<CURRENCY>"
                    }
                  ]
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

### Webhook contents

| Placeholder | Description | Sample Value |
| --- | --- | --- |
| `<CATALOG_ID>` | Ecommerce product catalog ID. | `1537566713439863` |
| `<CURRENCY>` | Item currency. | `USD` |
| `<DISPLAY_PHONE_NUMBER>` | Business phone number display number. | `15550051310` |
| `<ENTRY.ID>` | WhatsApp Business Account ID. | `102290129340398` |
| `<ITEM_PRICE>` | Item price. | `99.99` |
| `<MESSAGES.ID>` | WhatsApp message ID. | `wamid.HBgLMTY1MDM4Nzk0MzkVAgARGBJDOEI3ODgxNzQzMjJBQTdEQTcA` |
| `<NAME>` | Customer’s name. | `Pablo Morales` |
| `<PHONE_NUMBER_ID>` | Business phone number ID. | `106540352242922` |
| `<PRODUCT_RETAILER_ID>` | The item SKU number. Labeled as **Content ID** in the Commerce Manager. | `2lc20305pt` |
| `<QUANTITY>` | Number of items ordered (for this particular item). | `1` |
| `<TIMESTAMP>` | UNIX timestamp indicating when the webhook was sent. | `1677522117` |
| `<WA_ID>` | Customer’s WhatsApp phone number. | `16505551234` |

### Sample webhook

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
              "display_phone_number": "15550051310",
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
                "from": "16505551234",
                "id": "wamid.HBgLMTY1MDM4Nzk0MzkVAgASGBQzQTMxNzA1QzNENEI4ODY0OTY2MAA=",
                "timestamp": "1683223069",
                "type": "order",
                "order": {
                  "catalog_id": "1537566713439863",
                  "product_items": [
                    {
                      "product_retailer_id": "n6k6x0y7oe",
                      "quantity": 1,
                      "item_price": 99.99,
                      "currency": "USD"
                    }
                  ]
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

## Sending MPM template messages

You can send [multi-product message (MPM) templates](https://developers.facebook.com/documentation/business-messaging/whatsapp/catalogs/mpm-template-messages) in template messages.

### Components

MPM template messages must have:

- a **header** component (only required if template uses a header variable)
- a **body** component (only required if template uses a body variable)
- a single **MPM button** component

Use the MPM button component to define sections and their titles that will appear when the customer taps the **View items** button, and to designate which products appear in each of those sections.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/345454978_257502929976881_8980265032321705247_n.png?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=isgmS_4NQy8Q7kNvwGZDIKL&_nc_oc=AdpyeIVwTHatgJUjyzpMYPTPp8ppWLnRffLlPhViXCOY0tI_TdVXy2RaQsuYLrdOtS0&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=CSuhdPqY5wU8E_i75Znc8g&_nc_ss=7b20f&oh=00_Af5xy1iRcXVvuOQUqtrxhYAzdPMEMxInLWPg_OGliKJPXg&oe=6A1C0B8B)

To send an approved MPM template in a template message, use the [Messages API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api#post-version-phone-number-id-messages). Use the POST body to define the contents of the message and to describe any variables to inject into the template itself.

### Request syntax

```json
curl -X POST "https://graph.facebook.com/v23.0/<BUSINESS_PHONE_NUMBER_ID>/messages" \
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
          "type": "header",
          "parameters": [
            {
              "type": "text",
              "text": "<HEADER_TEXT>"
            }
          ]
        },
        {
          "type": "body",
          "parameters": [
            {
              "type": "text",
              "text": "<BODY_TEXT>"
            }
          ]
        },
        {
          "type": "button",
          "sub_type": "mpm",
          "index": 0,
          "parameters": [
            {
              "type": "action",
              "action": {
                "thumbnail_product_retailer_id": "<THUMBNAIL_PRODUCT_RETAILER_ID>",
                "sections": [
                  {
                    "title": "<TITLE>",
                    "product_items": [
                      {
                        "product_retailer_id": "<PRODUCT_RETAILER_ID_1>"
                      },
                      {
                        "product_retailer_id": "<PRODUCT_RETAILER_ID_2>"
                      }
                      // ... Add up to 30 product items per section
                    ]
                  }
                  // ... Add up to 10 section objects as needed
                ]
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
| `<BODY_TEXT>` | **Required if template uses variables.**<br>String or array of strings. Text to replace body variable(s) defined in the template. | `10OFF` |
| `<CODE>` | Template [language and locale code](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/supported-languages). | `en_US` |
| `<HEADER_TEXT>` | **Required if template uses a variable.**<br>Text to replace header variable defined in the template. | `Pablo` |
| `<NAME>` | Template name. | `abandoned_cart` |
| `<PRODUCT_RETAILER_ID>` | SKU number of the item you want to appear in the section.<br>SKU numbers are labeled as **Content ID** in the Commerce Manager.<br>Supports up to 30 products total, across all sections. | `2lc20305pt` |
| `<THUMBNAIL_PRODUCT_RETAILER_ID>` | Item SKU number. Labeled as **Content ID** in the Commerce Manager.<br>The thumbnail of this item will be used as the template message’s header image. | `2lc20305pt` |
| `<TITLE>` | Section title text.<br>You can define up to 10 sections.<br>Maximum 24 characters. Markdown is not supported. | `Popular Bundles` |
| `<TO>` | Customer phone number. | `16505551234` |

### Response

Upon success, the API will respond with:

```json
{
  "messaging_product": "whatsapp",
  "contacts": [
    {
      "input": "<INPUT>",
      "wa_id": "<WA_ID>"
    }
  ],
  "messages": [
    {
      "id": "<ID>"
    }
  ]
}
```

### Response parameters

| Placeholder | Description | Sample Value |
| --- | --- | --- |
| `<ID>` | WhatsApp message ID. | `wamid.HBgLMTY1MDM4Nzk0MzkVAgARGBJDOEI3ODgxNzQzMjJBQTdEQTcA` |
| `<INPUT>` | Customer WhatsApp phone number. | `16505551234` |
| `<WA_ID>` | Customer WhatsApp ID. | `16505551234` |

### Example request

This example sends an approved template named “abandoned_cart” and injects a variable (the customer’s first name) into the template header and a discount code into the template body. It also defines two sections (“Popular Bundles” and “Premium Packages”) and identifies the products (a total of 3) that should be injected into those sections.

```curl
curl 'https://graph.facebook.com/v25.0/106540352242922/messages' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "16505551234",
  "type": "template",
  "template": {
    "name": "abandoned_cart",
    "language": {
      "code": "en_US"
    },
    "components": [
      {
        "type": "header",
        "parameters": [
          {
            "type": "text",
            "text": "Pablo"
          }
        ]
      },
      {
        "type": "body",
        "parameters": [
          {
            "type": "text",
            "text": "10OFF"
          }
        ]
      },
      {
        "type": "button",
        "sub_type": "mpm",
        "index": 0,
        "parameters": [
          {
            "type": "action",
            "action": {
              "thumbnail_product_retailer_id": "2lc20305pt",
              "sections": [
                {
                  "title": "Popular Bundles",
                  "product_items": [
                    {
                      "product_retailer_id": "2lc20305pt"
                    },
                    {
                      "product_retailer_id": "nseiw1x3ch"
                    }
                  ]
                },
                {
                  "title": "Premium Packages",
                  "product_items": [
                    {
                      "product_retailer_id": "n6k6x0y7oe"
                    }
                  ]
                }
              ]
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
      "input": "16505551234",
      "wa_id": "16505551234"
    }
  ],
  "messages": [
    {
      "id": "wamid.HBgLMTY1MDM4Nzk0MzkVAgARGBJDOEI3ODgxNzQzMjJBQTdEQTcA"
    }
  ]
}
```
