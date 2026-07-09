# Offsite Pix payments | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/offsite-pix_

---

# Offsite Pix payments

Updated: Apr 6, 2026

Payments API also enables businesses to collect payments from their customers via WhatsApp using dynamic Pix codes.

When using this integration, WhatsApp only facilitates the communication between merchants and buyers. Merchants are responsible for integrating with a bank or PSP in order to generate dynamic Pix codes, and confirm their payment.

## Before you start

1. Familiarize yourself with the [Orders API](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/orders) . Orders are the entrypoint for collecting payments in WhatsApp.
2. You will need an existing integration with a bank or PSP to generate dynamic Pix codes and do automatic reconciliation when a payment is made. You must be able to update the order status as soon as a payment is made.

## Integration steps

The following sequence diagram shows the typical integration with Pix.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/559928787_1339318127926838_2798974158408097525_n.jpg?_nc_cat=101&ccb=1-7&_nc_sid=e280be&_nc_ohc=Nf1CJryKtkAQ7kNvwH05aQN&_nc_oc=AdqAcDih2sDlzlWCuneBEvaijwBWsP0v4ewOl48tVUEbaDvsFkZ3cX_BM42y7QhCv7A&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=p0Ze8NzYLKJ4oHj8Y6fKKw&_nc_ss=7b20f&oh=00_Af551vv-4XlO5WCGLPtJgD4AXS_0woxYm4eXIRvoW-XwMw&oe=6A1C07ED)

### 1. Send an Order Details message

Follow the full integration guide in the [Orders API page](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/orders).

If Pix is available on this order, you will need to provide a `pix_dynamic_code` to the `payment_settings` attribute. You can optionally include an `order` object with itemized products, fees, and discounts, or send a simplified message with just the total amount and payment settings.

The following images show how the order details message with Pix appears in WhatsApp, in both full and simplified versions.

![Full order details message with Pix payment showing itemized products and Copy Pix code button](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/672383950_1482949490230367_8421252382529780742_n.png?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=BfGs5Ab1MxcQ7kNvwFHuSfU&_nc_oc=AdqE1Dkr6zweJtp9pw3wUQBU3rWPMFL7hSkiMCeHmYFf-ZdaecSWXiBwb3cIqLUv9q0&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=p0Ze8NzYLKJ4oHj8Y6fKKw&_nc_ss=7b20f&oh=00_Af4P38Tdg2G7ycrJg3meocxwVoQsA3reDQI0RAfxhWZUwQ&oe=6A1C20B1)![Simplified order details message with Pix payment showing total amount and Copy Pix code button](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/672670425_1482949493563700_8054150270835736863_n.png?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=Ni3AkyTNK1sQ7kNvwEGM0i8&_nc_oc=AdpPRMQrHTnrVhk4yLRdg-pNL3aYd_ADV3i2vYiOKzou-JnWrjBAU65BByyuwcIi2Ng&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=p0Ze8NzYLKJ4oHj8Y6fKKw&_nc_ss=7b20f&oh=00_Af4qY75ZKLsdgnQaDcJ2g-B2ba6jsFv3I7Y64slZ68MGJw&oe=6A1C16C5)

Endpoint

```bash
POST /{PHONE_NUMBER_ID}/messages
```

Payload example

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
            "type": "pix_dynamic_code",
            "pix_dynamic_code": {
              "code": "00020101021226700014br.gov.bcb.pix2548pix.example.com...",
              "merchant_name": "Account holder name",
              "key": "39580525000189",
              "key_type": "CNPJ"
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

Simplified payload example

You can send a simplified order details message without the `order` object. This is useful when you don’t need to send itemized product details and only need to collect the total payment amount.

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
            "type": "pix_dynamic_code",
            "pix_dynamic_code": {
              "code": "00020101021226700014br.gov.bcb.pix2548pix.example.com...",
              "merchant_name": "Account holder name",
              "key": "39580525000189",
              "key_type": "CNPJ"
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

Parameters object

| Field Name | Optional? | Type | Description |
| --- | --- | --- | --- |
| `payment_settings` | Optional | [Payment Settings Object](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/offsite-pix#paymentsettingsobject) | List of payment related configuration objects. |

Payment settings

| Field Name | Optional? | Type | Description |
| --- | --- | --- | --- |
| `type` | Required | String | Must be `pix_dynamic_code`. |
| `pix_dynamic_code` | Required | [Dynamic Pix Object](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/offsite-pix#dynamicpixobject) | Dynamic Pix Code object that will be used to render the option to buyers during the checkout flow. |

Dynamic Pix code object

| Field Name | Optional? | Type | Description |
| --- | --- | --- | --- |
| `code` | Required | String | The dynamic Pix code which will be copied by the buyer. |
| `merchant_name` | Required | String | Account holder name. Displayed in-app for the buyer for informational purposes. |
| `key` | Required | String | Pix key. Displayed in-app for the buyer for informational purposes. |
| `key_type` | Required | String | Pix key type. One of `CPF`, `CNPJ`, `EMAIL`, `PHONE` or `EVP`. |

### 2. Send an order status update

Once the payment is confirmed, you must send an order status update. Follow the integration guide in the [Orders API page](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/orders).
