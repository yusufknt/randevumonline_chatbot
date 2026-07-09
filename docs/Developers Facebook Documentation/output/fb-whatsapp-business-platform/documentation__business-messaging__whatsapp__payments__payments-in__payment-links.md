# Accept Payments via Payment Links | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/payment-links_

---

# Accept Payments via Payment Links

Updated: Nov 14, 2025

This feature is not publicly available yet. Please reach out to whatsappindia-bizpayments-support@meta.com to know more.

Your businesses can enable customers to pay for their orders by bringing in all the payment methods supported on your platform to WhatsApp. Businesses can send customers invoice(`order_details`) messages, then get notified about payment status updates via webhook notifications from Payment Gateway.

## Overview

Currently, customers browse business catalogs, add products to cart, and send orders in with our set of commerce messaging solutions, which includes [Single Product Message, Multi Product Message, and Product Detail Page](https://developers.facebook.com/documentation/business-messaging/whatsapp/catalogs/share-products).

With the WhatsApp Messaging API, businesses can send customers a bill to complete the order with one of the supported payment instrument.

## How It Works

The business must send an `order_details` message for the consumer to initiate payment. This type of message is a new type of interactive message, which always contains the same 4 main components: **header**, **body**, **footer**, and **action**. Inside the **action** component, the business includes all the information needed for the customer to complete their payment.

Each `order_details` message contains a unique `reference_id` provided by the business, and that unique number is used throughout the flow to track the order. This `reference_id` is used to generate the payment link from Payment Gateway.

Once the message is sent, the business waits for a payment or transaction status updates directly from Payment Gateway. Upon receiving payment signal for an order, business should relay this payment signal to consumer client through interactive order status(`order_status`) message.

Updating user about the payment signal is important as this message updates the order details message and order details view for the consumer reflecting the order confirmation from merchant. This is shown with an example in subsequent sections.

## Purchase Flow in App

In the WhatsApp customer app, the purchase flow has the following steps:

1. Customer sends an order with selected products to the business or business identifies the products that the customer has shown interest to purchase.
2. After receiving the order or identifying the product, if a business accepts payment methods other than UPI, such as credit cards and payment wallets, etc. then business will send a message to the user to get their preferred payment method for the order. ![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/565092551_1339318041260180_6100091283875651354_n.jpg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=yVflNtXrJcIQ7kNvwHEYOKa&_nc_oc=AdqNg9rj5z4camac5mXgCFNWqwFP3xjwi4Am6OyIIxlShSQp2f1UDCvkw1AISVKjbQw&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=xWk0OhVNfDMVNMXgsE9UdQ&_nc_ss=7b20f&oh=00_Af73T2Xt5VY9MBmiE11KI9cVUIiZ8g2MO-A5vzdH1IR3KQ&oe=6A1C263E)
3. When consumers want to pay using other payment method option, the business should generate the payment link by calling Payment Gateway by providing the unique “reference-id” and other information like amount, validity etc, then business can use the generated payment link to construct the order details message and send to the consumer. ![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/560743135_1339318431260141_4647602383513770880_n.jpg?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=bRSq9YNB6ggQ7kNvwH6T-b-&_nc_oc=AdoBNIomfJ0eoAeoGM1V3-w9AVGqlUTRQnaw4StdsfLayPDp1waDH7s71GamObFTvxI&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=xWk0OhVNfDMVNMXgsE9UdQ&_nc_ss=7b20f&oh=00_Af6LdMsXCW5cTdUuoFqnJohAvzoUKhEJwabVvObk8cploA&oe=6A1C18A2)![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/565660275_1339317854593532_4612206710255341597_n.jpg?_nc_cat=111&ccb=1-7&_nc_sid=e280be&_nc_ohc=MLSo5sHoDqwQ7kNvwEcN0VR&_nc_oc=AdpWr_dVBZxupWteZX8DGlz2VPKjYDZZcy-FeiTrckRNVTRmI77E6qf_cWmId8s_4-s&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=xWk0OhVNfDMVNMXgsE9UdQ&_nc_ss=7b20f&oh=00_Af7Q-vB5eC9bXANhpNce_CU9IsVeq14z2fcRbiNBaZP_NA&oe=6A1C33A2)
4. When the consumer taps the Pay now/continue button, consumer will be redirected to the payment link within specially designed In-App browser to present with the list of supported payment options such as credit card, debit card, wallet or UPI apps. Consumers can choose any one of the payment option to pay for the order. The following is a sample payment link redirect within In-App Browser accepting various payment methods like credit, debit, wallet and UPI apps.![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/564160491_1339318417926809_8923443632387956339_n.jpg?_nc_cat=102&ccb=1-7&_nc_sid=e280be&_nc_ohc=ZNZaaVGd4QYQ7kNvwFdrlYg&_nc_oc=Adompf_GR25D8vNYMje-6BIo0vO8EBHYvRygFcqTMwI-nf_7BxDsrY534691ZkrFZeU&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=xWk0OhVNfDMVNMXgsE9UdQ&_nc_ss=7b20f&oh=00_Af6G8mPHATZYigdakY-G_rYJVyMybMsojnBlAP4QcoBA6g&oe=6A1C1A9C)![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/561772090_1339318161260168_2471127466153480453_n.jpg?_nc_cat=110&ccb=1-7&_nc_sid=e280be&_nc_ohc=zCVLpF3UMecQ7kNvwHmbyW-&_nc_oc=Adql6nhQrJGKu9Yz7Qx58tGf2m0-V08WC2ZcFijhkh0XGBbAPbJx0Q65ThPABQKT-7w&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=xWk0OhVNfDMVNMXgsE9UdQ&_nc_ss=7b20f&oh=00_Af7nZAWymgCa39AdCWxfcZ-IzeCAH7y5lS_luRnlImjQjg&oe=6A1C322C)
5. Once the payment is complete, the business will receive a notification from Payment Gateway and the business needs to send order status updates to the consumer client notifying consumers about the progress on their order, this will update the order details message CTAs, Order details screen and Order status. The order status should contain the matching “reference-id” of order details. ![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/561528290_1339318227926828_5203165586545314384_n.jpg?_nc_cat=102&ccb=1-7&_nc_sid=e280be&_nc_ohc=4bYlxKUFNyMQ7kNvwELqoKy&_nc_oc=AdoTtkx7F2loqABF2GP8ehs7jxFZAqKJPQY-Hl4IWa5ayY9BeVawjSrnF2-gAW8CnP8&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=xWk0OhVNfDMVNMXgsE9UdQ&_nc_ss=7b20f&oh=00_Af5NIOksmyalR_DaG_9cGX4mPQVitnVpD9_RpQrw8UYOYQ&oe=6A1C1B48)![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/564584803_1339318121260172_4660237707662893676_n.jpg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=H40nRWLs-xEQ7kNvwEtGgSD&_nc_oc=AdqjJqGv5Qm0ob6X1rdSyGI3Spn5db5AH3dl8moMj2bEylFjzxujmHAhmIOfH6dDdHI&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=xWk0OhVNfDMVNMXgsE9UdQ&_nc_ss=7b20f&oh=00_Af7DFMJvWymnL2jhD03omFIIU6QR7o5VwhM8RFdmrDUZEg&oe=6A1C15F4)

## Integration Steps

The steps outlined below assume that the business is about to send order details message to consumer client.

The following sequence diagram demonstrates the typical integration flow for WA Payments API:
![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/564616717_1339318061260178_2911403093938616620_n.jpg?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=48NCVJntwNkQ7kNvwG58WnU&_nc_oc=Ado6CgwZ0lz6lnZKRh3XxeUMymmBX9s3M4ETOex8LINZKdoRsGDQDXBKSYpDPlDTlIc&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=xWk0OhVNfDMVNMXgsE9UdQ&_nc_ss=7b20f&oh=00_Af7bSOHDmhdq5pTWhYXh6BjSmWXVdXa4NUZD03xQ__jFIw&oe=6A1C0BC9)

### Step 1: Get Payment Link from Payment Gateway

Once the consumer has expressed their interest to purchase an item using payment link. Business needs to call payment gateway with necessary information like reference-id, amount and validity to generate the payment link. Following is a sample payment link:

```html
https://rzp.io/i/rNiAagU8y
```

Business needs to use the same reference-id, amount and expiration in invoice(`order_details`) interactive message.

### Step 2: Assemble the Interactive Object

To send an `order_details` message, businesses must assemble an [interactive object](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api) of type `order_details` with the following components:

| Object | Description |
| --- | --- |
| `type`<br>object | **Required.**<br>Must be “order_details”. |
| `header`<br>object | **Optional.**<br>Header content displayed on top of a message. If a header is not provided, the API uses an image of the first available product as the header |
| `body`<br>object | **Required.**<br>An object with the body of the message. The object contains the following field:<br>`text` string<br>**Required** if `body` is present. The content of the message. Emojis and markdown are supported. Maximum length is 1024 characters |
| `footer`<br>object | **Optional.**<br>An object with the footer of the message. The object contains the following fields:<br>`text` string<br>**Required** if `footer` is present. The footer content. Emojis, markdown, and links are supported. Maximum length is 60 characters |
| `action`<br>object | **Required.**<br>An action object you want the user to perform after reading the message. This action object contains the following fields:<br>`name` string<br>**Required**. Must be “review_and_pay”<br>`parameters` object<br>See [Parameters Object](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/payment-links#paramobject) for information |

Parameters Object

| Object | Description |
| --- | --- |
| `reference_id`<br>string | **Required.**<br>Unique identifier for the order or invoice provided by the business. It is case sensitive and cannot be an empty string and can only contain English letters, numbers, underscores, dashes, or dots, and should not exceed 35 characters.<br>The `reference_id` must be unique for each `order_details` message for the same business. If the partner would like to send multiple order_details messages for the same order, invoice, etc. it is recommended to include a sequence number in the `reference_id` (for example, <order-or-invoice-id>-<sequence-number>) to ensure `reference_id` uniqueness. |
| `type`<br>object | **Required.**<br>The type of goods being paid for in this order. Current supported options are `digital-goods` and `physical-goods` |
| `beneficiaries`<br>array | **Required for shipped physical-goods.**<br>An array of beneficiaries for this order. A beneficiary is an intended recipient for shipping the physical goods in the order. It contains the following fields:<br>Beneficiary information isn’t shown to users but is needed for legal and compliance reasons.<br>`name` string<br>**Required.** Name of the individual or business receiving the physical goods. Cannot exceed 200 characters<br>`address_line1` string<br>**Required.** Shipping address (Door/Tower Number, Street Name etc.). Cannot exceed 100 characters<br>`address_line2` string<br>**Optional.** Shipping address (Landmark, Area, etc.). Cannot exceed 100 characters<br>`city` string<br>**Required.** Name of the city.<br>`state` string<br>**Required.** Name of the state.<br>`country` string<br>**Required.** Must be “India”.<br>`postal_code` string<br>**Required.** 6-digit zipcode of shipping address. |
| `payment_type` | **Required.**<br>Must be “upi”. |
| `payment_settings` | **Required.**<br>See [Payment Settings Object](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/payment-links#payment_settings) for more details. |
| `currency` | **Required.**<br>The currency for this order. Currently the only supported value is `INR`. |
| `total_amount`<br>object | **Required.**<br>The `total_amount` object contains the following fields:<br>`offset` integer<br>**Required.** Must be `100` for `INR`.<br>`value` integer<br>**Required.** Positive integer representing the amount value multiplied by offset. For example, ₹12.34 has value 1234.<br>`total_amount.value` must be equal to `order.subtotal.value` + `order.tax.value` + `order.shipping.value` - `order.discount.value`. |
| `order`<br>object | **Required.**<br>See [order object](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/payment-links#ordobject) for more information. |

Payment Setting Object

| Object | Description |
| --- | --- |
| `type`<br>string | **Required.**<br>Must be `payment_link`. |
| `payment_link`<br>object | **Required.**<br>Refer [Payment Link Object](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/payment-links#payment_link) for more information. |

Payment Link Object

| Object | Description |
| --- | --- |
| `uri`<br>string | **Required.**<br>A valid payment link generated through payment gateway.<br>Generated payment links domains needs to be enabled to accept payments. Please reach out to whatsappindia-bizpayments-support@meta.com to know more. |
| `success_url`<br>string | **Optional.**<br>The flow terminated with success status, when success_url is hit. |
| `cancel_url`<br>string | **Optional.**<br>The flow ends with failure, when the cancel_url is triggered. |

Order Object

| Object | Description |
| --- | --- |
| `status`<br>string | **Required.**<br>Only supported value in the `order_details` message is `pending`.<br>In an `order_status` message, `status` can be: `pending`, `captured`, or `failed`. |
| `type`<br>string | **Optional.**<br>Only supported value is `quick_pay`. When this field is passed in we hide the “Review and Pay” button and only show the “Pay Now” button in the order details bubble. |
| `items`<br>object | **Required.**<br>An object with the list of items for this order, containing the following fields:<br>`retailer_id` string<br>**Optional.** Content ID for an item in the order from your catalog.<br>`name` string<br>**Required.** The item’s name to be displayed to the user. Cannot exceed 60 characters<br>`image` object<br>**Optional.** Custom image for the item to be displayed to the user. See [item image object](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/payment-links#item_image_object) for information<br>Using this image field will limit the items array to a maximum of 10 items and this cannot be used with `retailer_id` or `catalog_id`.<br>`amount` amount object with value and offset -- refer total amount field above<br>**Required.** The price per item<br>`sale_amount` amount object<br>**Optional.** The discounted price per item. This should be less than the original amount. If included, this field is used to calculate the subtotal amount<br>`quantity` integer<br>**Required.** The number of items in this order, this field cannot be decimal has to be integer.<br>`country_of_origin` string<br>**Required** if `catalog_id` is not present. The country of origin of the product<br>`importer_name` string<br>**Required** if `catalog_id` is not present. Name of the importer company<br>`importer_adress` string<br>**Required** if `catalog_id` is not present. Address of importer company |
| `subtotal`<br>object | **Required.**<br>The value **must be equal** to sum of `order.amount.value` * `order.amount.quantity`. Refer to `total_amount` description for explanation of `offset` and `value` fields<br>The following fields are part of the `subtotal` object:<br>`offset` integer<br>**Required.** Must be `100` for `INR`<br>`value` integer<br>**Required.** Positive integer representing the amount value multiplied by offset. For example, ₹12.34 has value 1234 |
| `tax`<br>object | **Required.**<br>The tax information for this order which contains the following fields:<br>`offset` integer<br>**Required.** Must be `100` for `INR`<br>`value` integer<br>**Required.** Positive integer representing the amount value multiplied by offset. For example, ₹12.34 has value 1234<br>`description` string<br>**Optional.** Max character limit is 60 characters |
| `shipping`<br>object | **Optional.**<br>The shipping cost of the order. The object contains the following fields:<br>`offset` integer<br>**Required.** Must be `100` for `INR`<br>`value` integer<br>**Required.** Positive integer representing the amount value multiplied by offset. For example, ₹12.34 has value 1234<br>`description` string<br>**Optional.** Max character limit is 60 characters |
| `discount`<br>object | **Optional.**<br>The discount for the order. The object contains the following fields:<br>`offset` integer<br>**Required.** Must be `100` for `INR`<br>`value` integer<br>**Required.** Positive integer representing the amount value multiplied by offset. For example, ₹12.34 has value 1234<br>`description` string<br>**Optional.** Max character limit is 60 characters<br>`discount_program_name` string<br>**Optional.** Text used for defining incentivised orders. If order is incentivised, the merchant needs to define this information. Max character limit is 60 characters |
| `catalog_id`<br>object | **Optional.**<br>Unique identifier of the Facebook catalog being used by the business.<br>If you do not provide this field, you must provide the following fields inside the items object: `country_of_origin`, `importer_name`, and `importer_address` |
| `expiration`<br>object | **Optional.**<br>Expiration for that order. Business must define the following fields inside this object:<br>`timestamp` string – UTC timestamp in seconds of time when order should expire. Minimum threshold is 300 seconds<br>`description` string – Text explanation for expiration. Max character limit is 120 characters |

Item Image Object

| Object | Description |
| --- | --- |
| `link`<br>string | **Required.**<br>A link to the image that will be shown to the user. Must be an `image/jpeg` or `image/png` and 8-bit, RGB or RGBA. Follows same requirements as image in [media](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/media#supported-media-types) |

The `parameters` value is a stringified JSON object.

By the end, the interactive object should look something like this for a catalog-based integration:

```json
{
  "interactive": {
    "type": "order_details",
    "header": {
      "type": "image",
      "image": {
        "link": "http(s)://the-url",
        "provider": {
          "name": "provider-name"
        }
      }
    },
    "body": {
      "text": "your-text-body-content"
    },
    "footer": {
      "text": "your-text-footer-content"
    },
    "action": {
      "name": "review_and_pay",
      "parameters": {
        "reference_id": "reference-id-value",
        "type": "digital-goods",
        "payment_type": "upi",
        "payment_settings": [
          {
            "type": "payment_link",
            "payment_link": {
              "uri": "https://the-payment-link"
            }
          }
        ],
        "currency": "INR",
        "total_amount": {
          "value": 21000,
          "offset": 100
        },
        "order": {
          "status": "pending",
          "catalog_id": "the-catalog_id",
          "expiration": {
            "timestamp": "utc_timestamp_in_seconds",
            "description": "cancellation-explanation"
          },
          "items": [
            {
              "retailer_id": "1234567",
              "name": "Product name, for example bread",
              "amount": {
                "value": 10000,
                "offset": 100
              },
              "quantity": 1,
              "sale_amount": {
                "value": 100,
                "offset": 100
              }
            }
          ],
          "subtotal": {
            "value": 20000,
            "offset": 100
          },
          "tax": {
            "value": 1000,
            "offset": 100,
            "description": "optional_text"
          },
          "shipping": {
            "value": 1000,
            "offset": 100,
            "description": "optional_text"
          },
          "discount": {
            "value": 1000,
            "offset": 100,
            "description": "optional_text",
            "discount_program_name": "optional_text"
          }
        }
      }
    }
  }
}
```

The `parameters` value is a stringified JSON object.

For a non-catalog based integration i.e. when catalog-id is not present, an example payload looks as follows:

```json
{
  "interactive": {
    "type": "order_details",
    "header": {
      "type": "image",
      "image": {
        "id": "your-media-id"
      }
    },
    "body": {
      "text": "your-text-body-content"
    },
    "footer": {
      "text": "your-text-footer-content"
    },
    "action": {
      "name": "review_and_pay",
      "parameters": {
        "reference_id": "reference-id-value",
        "type": "digital-goods",
        "payment_type": "upi",
        "payment_settings": [
          {
            "type": "payment_link",
            "payment_link": {
              "uri": "https://the-payment-link"
            }
          }
        ],
        "currency": "INR",
        "total_amount": {
          "value": 21000,
          "offset": 100
        },
        "order": {
          "status": "pending",
          "expiration": {
            "timestamp": "utc_timestamp_in_seconds",
            "description": "cancellation-explanation"
          },
          "items": [
            {
              "name": "Product name, for example bread",
              "amount": {
                "value": 10000,
                "offset": 100
              },
              "quantity": 1,
              "sale_amount": {
                "value": 100,
                "offset": 100
              },
              "country_of_origin": "country-of-origin",
              "importer_name": "name-of-importer-business",
              "importer_address": {
                "address_line1": "B8/733 nand nagri",
                "address_line2": "police station",
                "city": "East Delhi",
                "zone_code": "DL",
                "postal_code": "110093",
                "country_code": "IN"
              }
            },
            {
              "name": "Product name, for example bread",
              "amount": {
                "value": 10000,
                "offset": 100
              },
              "quantity": 1,
              "sale_amount": {
                "value": 100,
                "offset": 100
              },
              "country_of_origin": "country-of-origin",
              "importer_name": "name-of-importer-business",
              "importer_address": {
                "address_line1": "B8/733 nand nagri",
                "address_line2": "police station",
                "city": "East Delhi",
                "zone_code": "DL",
                "postal_code": "110093",
                "country_code": "IN"
              }
            }
          ],
          "subtotal": {
            "value": 20000,
            "offset": 100
          },
          "tax": {
            "value": 1000,
            "offset": 100,
            "description": "optional_text"
          },
          "shipping": {
            "value": 1000,
            "offset": 100,
            "description": "optional_text"
          },
          "discount": {
            "value": 1000,
            "offset": 100,
            "description": "optional_text",
            "discount_program_name": "optional_text"
          }
        }
      }
    }
  }
}
```

### Step 3: Add Common Message Parameters

Once the interactive object is complete, append the other parameters that make a message: `recipient_type`, `to`, and `type`. Remember to set the `type` to `interactive`.

```json
{
   "messaging_product": "whatsapp",
   "recipient_type": "individual",
   "to": "PHONE_NUMBER",
   "type": "interactive",
   "interactive": {
     // interactive object here
   }
 }
```

These are [parameters common to all message types](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages#requests).

### Step 4:Make a POST Call to Messages Endpoint

Make a POST call to the [`/[PHONE_NUMBER_ID]/messages`](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api) endpoint with the `JSON` object you have assembled. If your message is sent successfully, you get the following response:

```json
{
  "messaging_product": "whatsapp",
  "contacts": [ {
      "input": "[PHONE_NUMBER_ID]",
      "wa_id": "[PHONE-NUMBER_ID]"
  } ],
  "messages": [ {
      "id": "wamid.HBgLMTY1MDUwNzY1MjAVAgARGBI5QTNDQTVCM0Q0Q0Q2RTY3RTcA"
  } ]
}
```

Errors

WhatsApp Payments Terms of Service Acceptance Pending

If you see the following error, accept the WhatsApp Payments terms of service using the link provided in the error message before trying again.

```json
{
  "error": {
    "message": "(#134011) WhatsApp Payments terms of service has not been accepted",
    "type": "OAuthException",
    "code": 134011,
    "error_data": {
      "messaging_product": "whatsapp",
      "details": "WhatsApp Payments Terms of Service acceptance pending for this WhatsApp Business Account.
Please use the following link to accept terms of service before using Business APIs: https://fb.me/12345"
    }
  }
}
```

For all other errors that can be returned and guidance on how to handle them, see [WhatsApp Cloud API, Error Codes](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/error-codes).

### Step 5: Consumer Pays for the Order

Consumers can pay using WhatsApp payment method or using any UPI supported app that is installed on the device.

### Step 6: Get Notified About Transaction Status Updates from payment gateway

Businesses receive updates to the invoice via payment gateway webhooks, when the status of the user-initiated transaction changes. The unique identifier reference-id passed in `order_details` message can be used to map the transaction to the consumer invoice or interactive order details message.

### Step 7: Update order status

Upon receiving transaction signals from payment gateway through webhook, the business must update the order status to keep the user up to date. Currently we support the following order status values:

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/565718019_1339318281260156_7557207642198018127_n.jpg?_nc_cat=106&ccb=1-7&_nc_sid=e280be&_nc_ohc=1pZz-o3B8NwQ7kNvwG2aweu&_nc_oc=AdqVbk6o8orGuBX6xlB5Y5MUIDc9mxSFLD7cxJnotxwiGmZy62oqfsHNf_arKiLJM_E&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=xWk0OhVNfDMVNMXgsE9UdQ&_nc_ss=7b20f&oh=00_Af7rzvtZJg8J6QpXiqA355x5yaBudvlV72c7UW1RKYnRdg&oe=6A1C1975)

| Value | Description |
| --- | --- |
| `pending` | User has not successfully paid yet |
| `processing` | User payment authorized, merchant/partner is fulfilling the order, performing service, etc. |
| `partially-shipped` | A portion of the products in the order have been shipped by the merchant |
| `shipped` | All the products in the order have been shipped by the merchant |
| `completed` | The order is completed and no further action is expected from the user or the partner/merchant |
| `canceled` | The partner/merchant would like to cancel the `order_details` message for the order/invoice. The status update will fail if there is already a `successful` or `pending` payment for this `order_details` message |

Typically businesses update the `order_status` using either the WhatsApp payment status change notifications or their own internal processes. To update `order_status`, the partner sends an `order_status` message to the user.

```json
{
  "recipient_type": "individual",
  "to": "whatsapp-id",
  "type": "interactive",
  "interactive": {
    "type": "order_status",
    "body": {
      "text": "your-text-body-content"
    },
    "action": {
      "name": "review_order",
      "parameters": {
        "reference_id": "reference-id-value",
        "order": {
          "status": "processing | partially_shipped | shipped | completed | canceled",
          "description": "optional-text"
        }
      }
    }
  }
}
```

The following table describes the returned values:

| Value | Description |
| --- | --- |
| `reference_id` | The ID provided by the partner in the `order_details` message |
| `status` | The new order `status` |
| `description` | Optional text for sharing status related information in `order_details`. Could be useful while sending cancellation. Max character limit is 120 characters |

Merchant should always post this order-status message to consumer after receiving transaction updates for an order. As the order_details message and order details screen experience is tied to to the order status updates.

### Step 8: Reconcile Payments

Businesses should use their bank statements to reconcile the payments using the `reference_id` provided in the `order_details` messages.

## Checklist for Integrated Merchants

- Ensure that `order_status` message is send to consumer informing them about updates to an order after receiving transaction updates for an order.
- Ensure the merchant is verified and WABA contact is marked with a verified check.
- Verify the WABA is mapped to appropriate merchant initiated messaging tier(1k, 10k and 100k per day)
- Merchant should list the customer support information in the profile screen incase consumer wants to report any issues.
