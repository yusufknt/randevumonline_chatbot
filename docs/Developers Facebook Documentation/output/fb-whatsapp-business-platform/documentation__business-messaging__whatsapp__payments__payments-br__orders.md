# Orders | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/orders_

---

# Orders

Updated: Mar 25, 2026

Payments API introduces two new types of [interactive messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages#interactive-messages): `order_details` and `order_status`. They are the entrypoint to collect payment in WhatsApp.

1. `order_details` messages are sent to create an order in the buyer’s WhatsApp client app. This message includes the payment settings used to collect payment and can optionally include an `order` object with itemized products, fees, and discounts. Without the `order` object, you can send a simplified order details message with just the total amount and payment settings. The payment settings will vary depending on the integration type ( [Pix](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/offsite-pix) , [payment links](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/payment-links) , [Boleto](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/boleto) , [One Click Payments](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/one-click-payments) ).
2. `order_status` messages are sent when businesses update the order status either based on the WhatsApp payment status change notification or based on their internal processes. You can also send a simplified status update without the `order` object.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/565718019_1339318281260156_7557207642198018127_n.jpg?_nc_cat=106&ccb=1-7&_nc_sid=e280be&_nc_ohc=1pZz-o3B8NwQ7kNvwG2aweu&_nc_oc=AdqVbk6o8orGuBX6xlB5Y5MUIDc9mxSFLD7cxJnotxwiGmZy62oqfsHNf_arKiLJM_E&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=ED3mjhpELTtHqQzb8qeaqg&_nc_ss=7b20f&oh=00_Af7kQTiyzExdu_h8iOpNbMlE3QyIa7NBHNh6aDTk69Q1qQ&oe=6A1C1975)

When attached to an order details message, orders start in `pending` status. When the merchant has fully fulfilled the order and the buyer should not expect any further updates, it must be marked as `completed`.

## Sending order messages

Both message types contain the same 4 main components of an interactive message: *header*, *body*, *footer*, and *action*. The parameters in the *action* component will vary based on the message type. In addition, both `order_details` and `order_status` messages can optionally include an `order` object containing a list of items, fees, and other details about the order.

Once the interactive message object is assembled, make a POST call to the [messages endpoint](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api#messages). Remember to set the type to `interactive`.

### Order details example

The following images show how the full and simplified `order_details` messages appear in WhatsApp. The full version includes itemized products, while the simplified version displays only the total amount.

![Full order details message showing itemized products, payment methods, and total amount in a WhatsApp conversation](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/672671792_1482949470230369_3595354703933395831_n.png?_nc_cat=102&ccb=1-7&_nc_sid=e280be&_nc_ohc=8Navqm8B8LYQ7kNvwFI9oJz&_nc_oc=AdofSZd_buD67FLwiXohL0dwyXC1vJSY2hVgnO7huR8JcuOdZnFQLWXEJzydt18RyMg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=ED3mjhpELTtHqQzb8qeaqg&_nc_ss=7b20f&oh=00_Af7gB99VvmzKDCJlQwtm2MGtroj6q2fdsEAK_vPfcq47kw&oe=6A1C18BD)![Simplified order details message showing only the total amount and payment methods in a WhatsApp conversation](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/672671469_1482949480230368_4856741402553535910_n.png?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=eKah72JJ_7sQ7kNvwEpexwZ&_nc_oc=Adr0ALJ0zC5kpsUBAaMjUiNvTm5hu0F1eXCdXQ0whHrYal-0Qj_eT1ToWesxKmU2CsY&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=ED3mjhpELTtHqQzb8qeaqg&_nc_ss=7b20f&oh=00_Af74jmtku4iuVMggRaVrTvSz0HPeNrVMgerGZ9AChuxxbw&oe=6A1C2B1F)

Endpoint

```bash
POST /{PHONE_NUMBER_ID}/messages
```

Request body

```json
{
  "recipient_type": "individual",
  "to": "<PHONE_NUMBER>",
  "type": "interactive",
  "interactive": {
    "type": "order_details",
    "body": {
      "text": "Your message content"
    },
    "action": {
      "name": "review_and_pay",
      "parameters": {
        "reference_id": "unique-reference-id",
        "type": "digital-goods",
        "payment_type": "br",
        "payment_settings": [
          {
            "type": "payment_link",
            "payment_link": {
              "uri": "https://my-payment-link-url"
            }
          }
        ],
        "currency": "BRL",
        "total_amount": {
          "value": 50000,
          "offset": 100
        },
        "order": {
          "status": "pending",
          "tax": {
            "value": 0,
            "offset": 100,
            "description": "optional text"
          },
          "items": [
            {
              "retailer_id": "1234567",
              "name": "Cake",
              "amount": {
                "value": 50000,
                "offset": 100
              },
              "quantity": 1
            }
          ],
          "subtotal": {
            "value": 50000,
            "offset": 100
          }
        }
      }
    }
  }
}
```

### Simplified order details message

You can send a simplified order details message without the `order` object. This is useful when you don’t need to send itemized product details and only need to collect the total payment amount.

Simplified order details messages do not support an image header. Instead of the thumbnail image, the total payment amount is displayed prominently at the top of the message. If an image is a required part of your use case, consider using the [Payment Request CTA Templates](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/payment-request-cta) solution instead.

Endpoint

```bash
POST /{PHONE_NUMBER_ID}/messages
```

Request body

```json
{
  "recipient_type": "individual",
  "to": "<PHONE_NUMBER>",
  "type": "interactive",
  "interactive": {
    "type": "order_details",
    "body": {
      "text": "Your message content"
    },
    "action": {
      "name": "review_and_pay",
      "parameters": {
        "reference_id": "unique-reference-id",
        "type": "digital-goods",
        "payment_type": "br",
        "payment_settings": [
          {
            "type": "payment_link",
            "payment_link": {
              "uri": "https://my-payment-link-url"
            }
          }
        ],
        "currency": "BRL",
        "total_amount": {
          "value": 50000,
          "offset": 100
        }
      }
    }
  }
}
```

### Order status example

The following images show how the `order_status` message appears in WhatsApp after the payment is confirmed, for both the full and simplified versions.

![Full order details message with paid status in a WhatsApp conversation](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/671831234_1482949466897036_4859858914316070498_n.png?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=7vh1jNZh0McQ7kNvwEqoaWp&_nc_oc=AdqOrFFsXhJaIMnurQrSob8Tq0fKEI06Vf-cdTicIttqp8H-nuwgtW0U6kgmRARqf3E&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=ED3mjhpELTtHqQzb8qeaqg&_nc_ss=7b20f&oh=00_Af7tCqhrI7Z5jWSy_wBL4n3gRA-q6my5uyiRgImj3673jA&oe=6A1C1642)![Simplified order details message with paid status in a WhatsApp conversation](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/672031825_1482949476897035_4475141346611238505_n.png?_nc_cat=101&ccb=1-7&_nc_sid=e280be&_nc_ohc=OKcy64BCSz8Q7kNvwFhYlfr&_nc_oc=AdqR7y0R-osAVUQje9iroDMXKa8rK6vscxZNLR3FJyo3rwRWeDbPXyQcxX63PpGuzP4&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=ED3mjhpELTtHqQzb8qeaqg&_nc_ss=7b20f&oh=00_Af5Y7wEt1SjJCJpsWyBw_Bvvi4WRGckkDwfETwMFijZQXw&oe=6A1C0E24)

Endpoint

```bash
POST /{PHONE_NUMBER_ID}/messages
```

Request body

```json
{
  "recipient_type": "individual",
  "to": "<PHONE_NUMBER>",
  "type": "interactive",
  "interactive": {
    "type": "order_status",
    "body": {
      "text": "your-mandatory-text-body-content"
    },
    "footer": {
      "text": "your-optional-text-footer-content"
    },
    "action": {
      "name": "review_order",
      "parameters": {
        "reference_id": "unique-reference-id",
        "order": {
          "status": "processing"
        },
        "payment": {
          "status": "captured",
          "timestamp": 1722445231
        }
      }
    }
  }
}
```

### Simplified order status example

Endpoint

```bash
POST /{PHONE_NUMBER_ID}/messages
```

Request body

```json
{
  "recipient_type": "individual",
  "to": "<PHONE_NUMBER>",
  "type": "interactive",
  "interactive": {
    "type": "order_status",
    "body": {
      "text": "your-mandatory-text-body-content"
    },
    "footer": {
      "text": "your-optional-text-footer-content"
    },
    "action": {
      "name": "review_order",
      "parameters": {
        "reference_id": "unique-reference-id",
        "payment": {
          "status": "captured",
          "timestamp": 1722445231
        }
      }
    }
  }
}
```

### Message response

For either type, if your message is sent successfully, you will get the following response:

```json
{
  "messaging_product": "whatsapp",
  "contacts": [
    {
      "input": "[PHONE_NUMBER_ID]",
      "wa_id": "[PHONE-NUMBER_ID]"
    }
  ],
  "messages": [
    {
      "id": "wamid.HBgLMTY1MDUwNzY1MjAVAgARGBI5QTNDQTVCM0Q0Q0Q2RTY3RTcA"
    }
  ]
}
```

For all errors that can be returned and guidance on how to handle them, see [Cloud API Errors Codes](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/error-codes).

## Full API Reference

### Order Details

To send an order_details message, businesses must assemble an interactive object of type order_details with the following components:

Interactive Object

| Field Name | Optional? | Type | Description |
| --- | --- | --- | --- |
| type | Required | String | Must be `order_details`. |
| header | Optional | Object | Thumbnail image for order details message. It has the following fields:<br>`type`: Must be `image`.`image`: See [Image Object](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/orders#imageobject).<br>If the header is not present, the API finds the first product with an image and uses that for the thumbnail image. |
| body | Required | Object | An object with the body of the message. The object contains the following field:<br>`text` string: The content of the message. Emojis and markdown are supported. Maximum length is 1024 characters. |
| footer | Optional | Object | An object with the footer of the message. The object contains the following field:<br>`text` string: **Required** if footer is present. The footer content. Emojis, markdown, and links are supported. Maximum length is 60 characters. |
| action | Required | Action Object | See [Action Object](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/orders#actionobject) below. |

Image Object

| Field Name | Optional? | Type | Description |
| --- | --- | --- | --- |
| link | Required | String | Url of the image. |

Action Object

| Field Name | Optional? | Type | Description |
| --- | --- | --- | --- |
| name | Required | String | Must be `review_and_pay`. |
| parameters | Required | Parameters Object | See [Parameters Object](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/orders#paramsobject). |

Parameters Object

| Field Name | Optional? | Type | Description |
| --- | --- | --- | --- |
| reference_id | Required | String | Unique identifier for the order or invoice provided by the business. This cannot be an empty string and can only contain English letters, numbers, underscores, dashes, or dots, and should not exceed 60 characters.<br>The reference_id must be unique for each order_details message for the same business. If the partner would like to send multiple order_details messages for the same order, invoice, etc. it is recommended to include a sequence number in the reference_id to ensure reference_id uniqueness. |
| type | Required | String | Must be one of `digital-goods` or `physical-goods`. |
| payment_type | Required | String | Must be `br`. |
| payment_settings | Optional | [Payment Settings Object](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/orders#paymentsettingsobject) | List of payment related configuration objects. |
| currency | Required | String | ISO 4217 currency code for the order. Must be `BRL` (Brazilian Real). |
| total_amount | Required | Amount Object | See [Amount Object](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/orders#amountobject).<br>`total_amount.value` must be equal to `order.subtotal.value` + `order.tax.value` + `order.shipping.value` - `order.discount.value` |
| order | Optional | Order Object | See [Order Object](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/orders#orderobject). |

Payment Settings

| Field Name | Optional? | Type | Description |
| --- | --- | --- | --- |
| `type` | Required | String | One of `pix_dynamic_code`, `payment_link`, `boleto`. |
| One of the following objects: `pix_dynamic_code`, `payment_link`, `boleto`. | Required | Object | Payment instructions which will be displayed to buyers during the checkout process. |

Order Object

| Field Name | Optional? | Type | Description |
| --- | --- | --- | --- |
| status | Required | String | Status of the order. Only supported value here is `pending`. |
| catalog_id | Optional | String | Unique identifier of the Facebook catalog being used by the business. |
| expiration | Optional | Expiration Object | Expiration for that order. The CTA for payment will be disabled after expiry on the user end. See [Expiration Object](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/orders#expirationobject). |
| items | Required | List of Item Objects | List must have at least one item. See [Item Object](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/orders#itemobject). |
| subtotal | Required | Amount Object | See [Amount Object](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/orders#amountobject).<br>The value **must be equal** to sum of (`item.amount.value` or `item.sale_amount.value`) * `item.quantity`.<br>The following fields are part of the `subtotal` object:<br>`offset` string<br>**Required.** Must be `100` for `BRL`.<br>`value` string<br>**Required.** Positive integer representing the amount value multiplied by offset. For example, S$12.34. has value 1234 |
| tax | Required | Amount With Description Object | The tax information for this order. Even though the object is required, the amount can be zero. When zero is used, the tax line is not rendered in the client. See [Amount With Description Object](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/orders#amountdescriptionobject). |
| shipping | Optional | Amount With Description Object | See [Amount Object](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/orders#amountdescriptionobject). |
| discount | Optional | Discount Object | The discount for the order. See [Discount object](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/orders#discountobject). |

Expiration Object

| Field Name | Optional? | Type | Description |
| --- | --- | --- | --- |
| timestamp | Required | String | UTC time in seconds. Minimum threshold is 300 seconds. |
| description | Required | String | Text explanation for when the order will expire. Max character limit is 120 characters. |

Item Object

| Field Name | Optional? | Type | Description |
| --- | --- | --- | --- |
| retailer_id | Required | String | Content ID for an item in the order from your catalog. |
| name | Required | String | The item’s name to be displayed to the user. Cannot exceed 60 characters. |
| amount | Required | Amount Object | The price per item. See [Amount Object](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/orders#amountobject). |
| quantity | Required | Integer | Number of items in this order. |
| sale_amount | Optional | Amount Object | The discounted price per item. This should be less than the original amount. If included, this field is used to calculate the subtotal amount. See [Amount Object](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/orders#amountobject). |

Discount Object

| Field Name | Optional? | Type | Description |
| --- | --- | --- | --- |
| value | Required | Integer | Positive integer representing the amount value multiplied by offset. For example, 12.34 BRL has value 1234. |
| offset | Required | Integer | Must be `100` for `BRL`. |
| description | Optional | String | Max character limit is 60 characters. |
| discount_program_name | Optional | String | Text used for defining incentivised orders. If order is incentivised, the merchant needs to define this information. Max character limit is 60 characters. |

Amount Object

| Field Name | Optional? | Type | Description |
| --- | --- | --- | --- |
| value | Required | Integer | Positive integer representing the amount value multiplied by offset. For example, 12.34 BRL has value 1234. |
| offset | Required | Integer | Must be `100` for `BRL`. |

Amount Object (With Description)

| Field Name | Optional? | Type | Description |
| --- | --- | --- | --- |
| value | Required | Integer | Positive integer representing the amount value multiplied by offset. For example, 12.34 BRL has value 1234. |
| offset | Required | Integer | Must be `100` for `BRL`. |
| description | Optional | String | Max character limit is 60 characters. |

### Order Status

To send an order_status message, businesses must assemble an interactive object of type order_status with the following components:

Interactive Object

| Field Name | Optional? | Type | Description |
| --- | --- | --- | --- |
| type | Required | String | Must be `order_status`. |
| header | Optional | Object | Optional object for the message’s header for the message. |
| body | Required | Object | An object with the body of the message. The object contains the following field:<br>`text` string: The content of the message. Emojis and markdown are supported. Maximum length is 1024 characters. |
| footer | Optional | Object | An object with the footer of the message. The object contains the following field:<br>`text` string: **Required** if footer is present. The footer content. Emojis, markdown, and links are supported. Maximum length is 60 characters. |
| action | Required | Action Object | See [Action Object](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/orders#statusactionobject) below. |

Action Object

| Field Name | Optional? | Type | Description |
| --- | --- | --- | --- |
| name | Required | String | Must be `review_order`. |
| parameters | Required | Parameters Object | See [Parameters Object](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/orders#statusparamsobject). |

Parameters Object

| Field Name | Optional? | Type | Description |
| --- | --- | --- | --- |
| reference_id | Required | String | The unique ID provided in the `order_details` message. |
| order | Optional | Order Object | See [Order Object](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/orders#statusorderobject). |
| payment | Optional | Payment Object | See [Payment Object](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/orders#statuspaymentobject). |

Order Object

| Field Name | Optional? | Type | Description |
| --- | --- | --- | --- |
| status | Required | String | The new order status. [See supported order status](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/orders#orderstatussupported). |
| description | Optional | String | Optional text for sharing status related information in order-details page. Could be useful while sending cancellation. Length should not exceed 120 characters. |

Payment Object

| Field Name | Optional? | Type | Description |
| --- | --- | --- | --- |
| status | Required | String | The new payment status. [See supported payment status](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/orders#paymentstatussupported). |
| timestamp | Optional | Integer | Optional epoch timestamp in seconds |

Supported Order Status

Currently we support the following order status values:

| Value | Description |
| --- | --- |
| `pending` | Order is pending / not processed yet. |
| `processing` | Merchant/partner is fulfilling the order, performing service, etc. |
| `partially_shipped` | Part of the products in order have been shipped by the merchant. |
| `shipped` | All the products in order have been shipped by the merchant. |
| `completed` | The order is completed and no further action is expected from the user or the partner/merchant. |
| `canceled` | The partner/merchant would like to cancel the order_details message for the order/invoice. The status update will fail if there is already a successful or pending payment for this order_details message. |

Supported Payment Status

Currently we support the following payment status values:

| Value | Description |
| --- | --- |
| `pending` | Payment is pending. |
| `captured` | Payment was successfully captured. Receiving this payment status will update the order bubble to include the “paid” label (with green checkmark). |
| `failed` | Payment failed. |

## Errors and Statuses

These are the relevant errors for the WhatsApp Payments API:

| Error Code | Description |
| --- | --- |
| `2040 - Message is not supported` | The message you are trying to send cannot be received by this user |
| `2046 - Order status invalid transition` | The order status cannot be updated from the existing value to the new one |
| `2047 - Order cancellation failure` | The order could not be cancelled |

For a comprehensive list with detailed descriptions of error codes and HTTP status codes, please refer to our [Error Codes](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/error-codes) document.
