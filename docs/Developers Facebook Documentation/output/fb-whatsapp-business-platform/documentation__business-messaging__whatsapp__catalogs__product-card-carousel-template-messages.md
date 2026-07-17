# Product card carousel templates | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/catalogs/product-card-carousel-template-messages_

---

# Product card carousel templates

Updated: Mar 3, 2026

Product card carousel templates allow you to send a single text message accompanied by a set of up to 10 product cards in a horizontally scrollable view:

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/456451243_832660229062364_6760679807399209749_n.png?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=LwFujrSuIt4Q7kNvwGxHicB&_nc_oc=Adot0BYhev0_FqwO4hgnu1JmITnQStqtDhquNAibgSn1RseOMDdwK9lawWPE6N8bWwk&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=GiQdArvNwHdZwK-X-UqsSg&_nc_ss=7b20f&oh=00_Af6PylC_f6aJI9Mn9aSXetw89cWZvBw7N2J4dBkbA49UqA&oe=6A1C1C23)

When a WhatsApp user taps the **View** button, they can view more information about the product, add the product to a shopping cart, and place an order, all without leaving the WhatsApp client experience. If instead you prefer to send the user to your website when they click the button, see [Media Card Carousel Templates](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/marketing-templates/media-card-carousel-templates).

## Product cards

Carousel templates support up to 10 product cards, composed of message body text, a product image, product title, product price, and a single View button or URL button. All cards defined on a template must have the same components.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/456183425_819329683713319_8287896812760303277_n.png?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=EmksIxSaI5wQ7kNvwHjR8nT&_nc_oc=Adoy5qDnwMldFk1jR8RGi2DiWQShG9LM2Qm-JiVQJcHeQBd4qkRGh97NxkI3OH6kcFA&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=GiQdArvNwHdZwK-X-UqsSg&_nc_ss=7b20f&oh=00_Af6GSrApn2vpsXpHWhlR3jXwTU8pv-689B2y-zYTQ81w5g&oe=6A1C267A)

## View buttons

When a WhatsApp user taps the button, the product details view appears, displaying product information pulled from your product catalog.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/456536571_1403706086934453_4366317090049712342_n.png?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=AWJhoL5W5FYQ7kNvwFZX2cZ&_nc_oc=Ado-iUnUXrPX9Qe9ZftjR25TtRVbwLQeWrFZ-IAC19oLL0YoLs5xt7Iu5UrZHkqhiyY&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=GiQdArvNwHdZwK-X-UqsSg&_nc_ss=7b20f&oh=00_Af6qrRIDLBHkD2gVB-40SbBUkW5ah1wzCXVu9FCx_v9cow&oe=6A1C2CFA)

Users can then add the product to a cart and place an order.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/456294794_1915042982315160_3191620650033958999_n.png?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=8DlgM4v4A38Q7kNvwHRQ7zK&_nc_oc=AdobKA5LBmIJfe03ibWvvxYaW8UvozJua2mRxSS1ODRWFMFCQTirVgM39_2wMKHs6xE&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=GiQdArvNwHdZwK-X-UqsSg&_nc_ss=7b20f&oh=00_Af7XseZHXBBNIOLX-bttPC2L9OPwQ6WM_EUw_jcibHCnYg&oe=6A1C252E)

When a user submits the cart, a [webhook](https://developers.facebook.com/documentation/business-messaging/whatsapp/catalogs/product-card-carousel-template-messages#webhooks) will be triggered describing the order, and an order confirmation message will appear in the message thread.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/456482022_473045605708419_6165153125141611284_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=CwpiqJwo0-QQ7kNvwF-ymLg&_nc_oc=Ado7gbfAJC_9Ea0FKpvIyb2GXZ8jT3k6DOkSQo3Ix2jjw6J3RAL3z7o3J_dYaW6krrM&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=GiQdArvNwHdZwK-X-UqsSg&_nc_ss=7b20f&oh=00_Af4o5NbGzqghWpvwVdIJYU_A00EZnlBkW1rfuEgPoxgNBw&oe=6A1C02E1)

Users who have placed an order can see the contents of the order by tapping the **View details** button.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/456576172_505851605146576_6951890413402171834_n.png?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=F_MuQAxTPrMQ7kNvwFa2dPH&_nc_oc=Adr9Dj7qdoNRrgZkeen--mZZ70zzXVgjTd96VZntblBIWrROwjrc5mU6Fz808oBYXAg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=GiQdArvNwHdZwK-X-UqsSg&_nc_ss=7b20f&oh=00_Af6ruRr7P0GWpU5L3bUhdKcSP7Z7bOysT0e0XySdbXkedw&oe=6A1C1001)

## URL buttons

Instead of **View** buttons you may wish to use **URL** buttons. When a WhatsApp user taps a URL button to buy a product, the URL mapped to the button is loaded in the device’s default web browser, which takes the user out of the WhatsApp client experience. This can be useful if, for example, you wish to load the product in your mobile checkout page where users can add promo codes and find related products.

With URL button flows, since order placement happens outside of the WhatsApp client, webhooks describing the order are not triggered.

## Catalogs

To use product card carousel templates, you must have an ecommerce product catalog, with inventory, connected to your WhatsApp Business Account. See the Cloud API [Commerce](https://developers.facebook.com/documentation/business-messaging/whatsapp/catalogs/catalogs-overview) guide to learn more about connecting a catalog to your account.

## Webhooks

If you send a carousel template composed of product cards that use a **View** button, when a customer adds one or more products to their cart and submits an order, an [order messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/order) webhook is triggered, describing the order.

## Creating product card carousel templates

Use the [**Message Templates API**](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/template-api#post-version-waba-id-message-templates) to create a product card carousel template.

### Request syntax

It is only necessary to define two product cards upon template creation. An approved template with two product cards can be used to send up to 10 cards in a template message.

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
        "type": "body",
        "text": "<MESSAGE_BODY_TEXT>",
        "example": {
          "body_text": [
            [
              "<MESSAGE_BODY_TEXT_VARIABLE_EXAMPLE_1>",
              "<MESSAGE_BODY_TEXT_VARIABLE_EXAMPLE_2>"
            ]
          ]
        }
      },
      {
        "type": "carousel",
        "cards": [
          {
            "components": [
              {
                "type": "header",
                "format": "product"
              },
              {
                "type": "buttons",
                "buttons": [
                  {
                    "type": "spm",
                    "text": "View"
                  }
                  // OR, for a URL button, use the following instead:
                  // {
                  //   "type": "url",
                  //   "text": "<URL_BUTTON_LABEL_TEXT>",
                  //   "url": "<URL_BUTTON_URL>",
                  //   "example": [
                  //     "<URL_BUTTON_URL_VARIABLE_EXAMPLE>"
                  //   ]
                  // }
                ]
              }
            ]
          }
          // Add a second product card here, following the same structure as above
        ]
      }
    ]
  }'
```

### Request parameters

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<MESSAGE_BODY_TEXT>`<br>*String* | **Required.**<br>Message body text. Supports variables.<br>Maximum 1024 characters. | `Rare succulents for sale! {{1}}, add these unique plants to your collection.` |
| `<MESSAGE_BODY_TEXT_VARIABLE_EXAMPLE>`<br>*String* | **Required if message body text string uses variables.**<br>Message body text example variable string(s). Number of strings must match the number of variable placeholders in the message body text string.<br>If message body text uses a single variable, `body_text` value can be a string, otherwise it must be an array containing an array of strings. | `Pablo` |
| `<TEMPLATE_LANGUAGE>`<br>*String* | **Required.**<br>Template [language and locale code](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/supported-languages). | `en_US` |
| `<TEMPLATE_NAME>`<br>*String* | **Required.**<br>Template name.<br>Maximum 512 characters. | `carousel_template_product_cards_v1` |
| `<URL_BUTTON_LABEL_TEXT>`<br>*String* | **Required if using a URL button.**<br>URL button label text.<br>25 characters maximum. | `Buy now` |
| `<URL_BUTTON_URL>`<br>*String* | **Required if using a URL button.**<br>URL to be loaded in the device’s default web browser when the WhatsApp user taps the button.<br>Supports 1 variable. Variable placeholder must be appended to the end of the URL string.<br>Maximum 2000 characters. | `https://www.luckyshrub.com/rare-succulents/{{1}}` |
| `<URL_BUTTON_URL_VARIABLE_EXAMPLE>`<br>*String* | **Required if URL button URL uses a variable.**<br>URL button URL example variable string.<br>Maximum 2000 characters. | `BUDDHA` |

### Example request

This example request creates a product card carousel template with a message body that uses a single variable and two product cards. Once approved, it can be used to send up to 10 product cards in a template message.

```json
curl 'https://graph.facebook.com/v25.0/161311403722088/message_templates' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "name": "carousel_template_product_cards_v1",
  "language": "en_US",
  "category": "marketing",
  "components": [
    {
      "type": "body",
      "text": "Rare succulents for sale! {{1}}, add these unique plants to your collection. All three of these rare succulents are available for purchase on our website, and they come with a 100% satisfaction guarantee. Whether you're a seasoned succulent enthusiast or just starting your plant collection, these rare succulents are sure to impress. Shop now and add some unique and beautiful plants to your collection!",
      "example": {
        "body_text": "Pablo"
      }
    },
    {
      "type": "carousel",
      "cards": [
        {
          "components": [
            {
              "type": "header",
              "format": "product"
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
        },
        {
          "components": [
            {
              "type": "header",
              "format": "product"
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
        }
      ]
    }
  ]
}'
```

## Sending product card carousel templates

### Request syntax

Use the [**Messages API**](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api#post-version-phone-number-id-messages) to send an approved product card carousel template to a WhatsApp user.

```json
curl -X POST "https://graph.facebook.com/v23.0/<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>/messages" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
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
          "type": "body",
          "parameters": [
            { "type": "text", "text": "<MESSAGE_BODY_TEXT_VARIABLE_1>" },
            { "type": "text", "text": "<MESSAGE_BODY_TEXT_VARIABLE_2>" }
          ]
        },
        {
          "type": "carousel",
          "cards": [
            {
              "card_index": 0,
              "components": [
                {
                  "type": "header",
                  "parameters": [
                    {
                      "type": "product",
                      "product": {
                        "product_retailer_id": "<PRODUCT_ID_1>",
                        "catalog_id": "<CATALOG_ID>"
                      }
                    }
                  ]
                }
                // Add additional components (e.g., buttons) here if your template defines them
              ]
            }
            // Add additional cards here, incrementing card_index for each
          ]
        }
      ]
    }
  }'
```

### Request parameters

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<CARD_INDEX>`<br>*Integer* | **Required.**<br>Zero-indexed order in which card should appear within the card carousel. `0` indicates first card, `1` indicates second card, etc. | `0` |
| `<CATALOG_ID>`<br>*String* | **Required.**<br>ID of [connected ecommerce catalog](https://www.facebook.com/business/help/158662536425974) containing the product. | `194836987003835` |
| `<MESSAGE_BODY_TEXT_VARIABLE>`<br>*Object* | **Required if template message body text uses variables, otherwise omit.**<br>Object describing a message variable. If the template uses multiple variables, you must define an object for each variable.<br>Supports `text`, `currency`, and `date_time` types. See [Messages Parameters](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api#parameter-object).<br>There is no maximum character limit on this value, but it does count against the message body text limit of 1024 characters. | `{<br>"type":"text",<br>"text": "Pablo"<br>}` |
| `<PRODUCT_ID>`<br>*String* | **Required.**<br>Product ID. | `vrpj01fvwp` |
| `<TEMPLATE_LANGUAGE>`<br>*String* | **Required.**<br>Template [language and locale code](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/supported-languages). | `en_US` |
| `<TEMPLATE_NAME>`<br>*String* | **Required.**<br>Template name.<br>Maximum 512 characters. | `carousel_template_media_cards_v1` |
| `<WHATSAPP_USER_PHONE_NUMBER>`<br>*String* | **Required.**<br>WhatsApp user phone number. | `+16505551234` |

### Example request

This example request sends an approved template named “carousel_template_product_cards_v1”. It supplies a single body text variable value (which the template requires) and three product cards. Each card identifies where it should appear in the carousel (card_index), as well as the product ID and catalog ID where the card’s product details (title, description, price, etc.) can be found.

```curl
curl 'https://graph.facebook.com/v25.0/179776755229976/messages' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "+16505551234",
  "type": "template",
  "template": {
    "name": "carousel_template_product_cards_v1",
    "language": {
      "code": "en_US"
    },
    "components": [
      {
        "type": "body",
        "parameters": [
          {
            "type": "text",
            "text": "Pablo"
          }
        ]
      },
      {
        "type": "carousel",
        "cards": [
          {
            "card_index": 0,
            "components": [
              {
                "type": "header",
                "parameters": [
                  {
                    "type": "product",
                    "product": {
                      "product_retailer_id": "vrpj01fvwp",
                      "catalog_id": "194836987003835"
                    }
                  }
                ]
              }
            ]
          },
          {
            "card_index": 1,
            "components": [
              {
                "type": "header",
                "parameters": [
                  {
                    "type": "product",
                    "product": {
                      "product_retailer_id": "va2l5ioeat",
                      "catalog_id": "194836987003835"
                    }
                  }
                ]
              }
            ]
          },
          {
            "card_index": 2,
            "components": [
              {
                "type": "header",
                "parameters": [
                  {
                    "type": "product",
                    "product": {
                      "product_retailer_id": "sqpjv0mgde",
                      "catalog_id": "194836987003835"
                    }
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  }
}'
```
