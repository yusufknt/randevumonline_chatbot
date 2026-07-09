# Single-product message templates | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/catalogs/spm-template-messages_

---

# Single-product message templates

Updated: Mar 3, 2026

This document describes single-product message (SPM) templates, their uses, and how to use them.

SPM templates are marketing templates that allow you to present a single product from your ecommerce catalog, accompanied by a product image, product title, and product price (all pulled from your product within your catalog), along with customizable body text, optional footer text, and an interactive **View** button.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/456611074_369667709517740_8197750041061962345_n.png?_nc_cat=111&ccb=1-7&_nc_sid=e280be&_nc_ohc=j-uEnO57uhgQ7kNvwEIu2Ub&_nc_oc=AdqU7S2muoi8WlMZglVxiJpYjWWxyzYCt_B5yKBuUh6zmoTrrAdRDbf1D-QB8KYpoHU&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=DKL64_EonFmaBL6ze2JtHg&_nc_ss=7b20f&oh=00_Af7BQyqlra3W73XoftyamL6g63b9DCmfDZHWEVuaf-A4iA&oe=6A1C0D8A)

WhatsApp users can tap the button to see details about the product, and can add or remove the product from the WhatsApp shopping cart:

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/455731119_491422670275236_7231575948344280249_n.png?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=AaYWpdBOoa0Q7kNvwFbxAT7&_nc_oc=Adr4jwIsZfcK38d-QWLK3pcySsCvJ6zYl-UicAdN06X_c_aFg3hYPULMJb-8MWWGuTY&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=DKL64_EonFmaBL6ze2JtHg&_nc_ss=7b20f&oh=00_Af6vfVC8MOeSxX1tL7Qpw1fZBjOJfcYu50uXihYcDge4gg&oe=6A1C293F)

If the WhatsApp user adds the product to the cart and submits an order, you will be notified via webhook and the user will see that an order has been placed:

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/455346606_8499522813412387_6714135406583255031_n.png?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=iLS_bNe0XBsQ7kNvwEOMlNz&_nc_oc=AdrHddninD68CPXfMkdQTz-JhoKzfNbiqv0vkI4lHGJm7JqQcjYuDA51YkRk3KGeje8&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=DKL64_EonFmaBL6ze2JtHg&_nc_ss=7b20f&oh=00_Af4Ur-IdWpoSZtEcTYStzQGplgPkUGkx5Z94CF_OqgpM8w&oe=6A1C1885)

Users who place an order are also able to use the View details button to see information about the order:

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/455798578_1140213730376391_4808743486596066303_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=emKedz78Qu4Q7kNvwHrJSNx&_nc_oc=AdrVFLvwY471kfrrwKHrpIF-uLRP3DgLBTpr9zwittfLiXv2MxhNkOggZvo8XYtIMdo&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=DKL64_EonFmaBL6ze2JtHg&_nc_ss=7b20f&oh=00_Af6cG0idAqivtWvJ1UfbkcxW4iD9uDq5_49TxgVDviUzvQ&oe=6A1C06FF)

## Limitations

- Customers must be using WhatsApp v2.22.24 or greater.
- Message forwarding is disabled for SPM templates.

## Catalogs

You must have an ecommerce product catalog, with inventory, connected to your WhatsApp Business Account. See the Cloud API [Commerce](https://developers.facebook.com/documentation/business-messaging/whatsapp/catalogs/catalogs-overview) guide to learn more about connecting a catalog to your account.

## Webhooks

When a customer adds one or more products to their cart and submits an order, an [order messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/order) webhook is triggered, describing the order.

## Creating SPM templates

Use the [Message Templates API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/template-api#post-version-waba-id-message-templates) to create an SPM template.

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
  "parameter_format": "<PARAMETER_FORMAT>",
  "components": [
    {
      "type": "header",
      "format": "product"
    },
    {
      "type": "body",
      "text": "<CARD_BODY_TEXT>",

      <!-- Example parameter values required, if body text contains parameters -->
      "example": {
        "body_text_named_params": [
          {
            "param_name": "<PARAMETER_NAME>",
            "example": "<PARAMETER_EXAMPLE>"
          },
          <!-- Additional parameters would follow -->
        ]
      }

    },
    {
      "type": "footer",
      "text": "<CARD_FOOTER_TEXT>"
    },
    {
      "type": "buttons",
      "buttons": [
        {
          "type": "spm",
          "text": "View"
        }
      ]
    }
  ]
}'
```

### Request parameters

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<ACCESS_TOKEN>`<br>*String* | **Required.**<br>Access token. | `EAAAN6tcBzAUBOZC82CW7iR2LiaZBwUHS4Y7FDtQxRUPy1PHZClDGZBZCgWdrTisgMjpFKiZAi1FBBQNO2IqZBAzdZAA16lmUs0XgRcCf6z1LLxQCgLXDEpg80d41UZBt1FKJZCqJFcTYXJvSMeHLvOdZwFyZBrV9ZPHZASSqxDZBUZASyFdzjiy2A1sippEsF4DVV5W2IlkOSr2LrMLuYoNMYBy8xQczzOKDOMccqHEZD` |
| `<API_VERSION>`<br>*String* | **Optional.**<br>API version. If omitted, defaults to the newest API version available to your app. | `v23.0` |
| `<CARD_BODY_TEXT>`<br>*String* | **Required.**<br>Card body text. Supports variables.<br>Maximum 160 characters. | `Use code {{1}} to get {{2}} off our newest succulent!` |
| `<CARD_FOOTER_TEXT>`<br>*String* | **Optional.**<br>Footer text.<br>Maximum 60 characters. | `September 30, 2024` |
| `<PARAMETER_NAME>`<br>*String* | **Required if body text uses parameters.**<br>Example parameter value string(s). You must include a parameter example for each parameter in your body text. | `25OFF` |
| `<PARAMETER_FORMAT>`<br>*String* | **Optional.**<br>[Parameter format](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview#parameter-formats). Value can be:<br>`named``positional`<br>If the `parameter_format` property is omitted, the template will use positional formatting. | `Lucky Shrub: Your gateway to succulents!` |
| `<TEMPLATE_LANGUAGE>`<br>*String* | **Required.**<br>Template [language and locale code](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/supported-languages). | `en_US` |
| `<TEMPLATE_NAME>`<br>*String* | **Required.**<br>Template name.<br>Maximum 512 characters. | `abandoned_cart_offer` |
| `<WHATSAPP_BUSINESS_ACCOUNT_ID>`<br>*String* | **Required.**<br>WhatsApp Business Account ID. | `546151681022936` |

### Example request

```curl
curl 'https://graph.facebook.com/v25.0/161311403722088/message_templates' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "name": "spm_template_named_params",
  "language": "en_US",
  "category": "marketing",
  "parameter_format": "named",
  "components": [
    {
      "type": "header",
      "format": "product"
    },
    {
      "type": "body",
      "text": "Use code {{code}} to get {{percent}} off our newest succulent!",
      "example": {
        "body_text_named_params": [
          {
            "param_name": "code",
            "example": "15OFF"
          },
          {
            "param_name": "percent",
            "example": "15%"
          }
        ]
      }
    },
    {
      "type": "footer",
      "text": "Offer ends September 22, 2024"
    },
    {
      "type": "buttons",
      "buttons": [
        {
          "type": "spm",
          "text": "View"
        }
      ]
    }
  ]
}'
```

## Sending single-product template messages

### Request syntax

Use the [Messages API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api#post-version-phone-number-id-messages) to send an SPM template message.

```html
curl 'https://graph.facebook.com/<API_VERSION>/<BUSINESS_PHONE_NUMBER_ID>/messages' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <ACCESS_TOKEN>' \
-d '
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "<WHATSAPP_USER_PHONE_NUMBER>",
  "type": "template",
  "template": {
    "name": "<TEMPLATE_NAME>",
    "language": {
      "code": "<TEMPLATE_LANGUAGE>"
    },
    "components": [
      {
        "type": "header",
        "parameters": [
          {
            "type": "product",
            "product": {
              "product_retailer_id": "<PRODUCT_ID>",
              "catalog_id": "<CATALOG_ID>"
            }
          }
        ]
      },
      {
        "type": "body",
        "parameters": [
          {
            "type": "text",
            "parameter_name": "<PARAMETER_NAME>",
            "text": "<PARAMETER_VALUE>"
          },
          <!-- Additional parameter values would follow, if required by template -->
        ]
      }
    ]
  }
}'
```

### Request parameters

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<ACCESS_TOKEN>`<br>*String* | **Required.**<br>Access token | `EAAAN...` |
| `<API_VERSION>`<br>*String* | **Optional.**<br>API version. If omitted, defaults to the newest API version available to your app. | `v23.0` |
| `<BUSINESS_PHONE_NUMBER_ID>`<br>*String* | **Required.**<br>WhatsApp business phone number ID. | `106540352242922` |
| `<CATALOG_ID>`<br>*String* | **Required.**<br>ID of [connected ecommerce catalog](https://www.facebook.com/business/help/158662536425974) containing the product. | `194836987003835` |
| `<PARAMETER_NAME>`<br>*String* | **Required if template uses one or more named parameters.**<br>Name of [named parameter](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview#named-parameters). | `code` |
| `<PARAMETER_VALUE>`<br>*String* | **Required if template uses one or more named parameters.**<br>[Named parameter](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview#named-parameters) value. | `10OFF` |
| `<PRODUCT_ID>`<br>*String* | **Required.**<br>Product ID. | `nqryix03ez` |
| `<TEMPLATE_LANGUAGE>`<br>*String* | **Required.**<br>Template [language and locale code](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/supported-languages). | `en_US` |
| `<TEMPLATE_NAME>`<br>*String* | **Required.**<br>Template name.<br>Maximum 512 characters. | `spm_template_named_params` |
| `<WHATSAPP_USER_PHONE_NUMBER>`<br>*String* | **Required.**<br>WhatsApp user phone number. | `+16505551234` |

### Example request

This example sends an approved template named “spm_template_named_params” which injects parameters (a discount code and the percentage discounted) into the template body, and which includes a footer. The product image is pulled from the catalog and displayed in the message header.

```curl
curl 'https://graph.facebook.com/v25.0/179776755229976/messages' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "16505551234",
  "type": "template",
  "template": {
    "name": "spm_template_named_params",
    "language": {
      "code": "en_US"
    },
    "components": [
      {
        "type": "header",
        "parameters": [
          {
            "type": "product",
            "product": {
              "product_retailer_id": "nqryix03ez",
              "catalog_id": "194836987003835"
            }
          }
        ]
      },
      {
        "type": "body",
        "parameters": [
          {
            "type": "text",
            "parameter_name": "code",
            "text": "25OFF"
          },
          {
            "type": "text",
            "parameter_name": "percent",
            "text": "25%"
          }
        ]
      }
    ]
  }
}'
```
