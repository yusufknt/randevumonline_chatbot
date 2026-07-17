# Payment links | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/payment-links_

---

# Payment links

Updated: Nov 14, 2025

Payments API also enables businesses to collect payments from their customers via WhatsApp using Payment Links.

When using this integration, WhatsApp only facilitates the communication between merchants and buyers. Merchants are responsible for integrating with a PSP from which they can generate Payment Links, and confirm their payment.

## Before You Start

1. Familiarize yourself with the [Orders API](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/orders) . Orders are the entrypoint for collecting payments in WhatsApp.
2. You will need an existing integration with a PSP to generate Payment Links and do automatic reconciliation when a payment is made.
3. You must update the order status as soon as a payment is made.

## Integration steps

The following sequence diagram shows the typical integration with Payment Links.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/560047558_1339318174593500_8182680878959019679_n.jpg?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=DhaHfHA1-PkQ7kNvwG11qRP&_nc_oc=Adr0Qpn0zU2C7yYEzkWBMECHDBBOol4WmmDbEMIi_aTBzr8OvBnMmYMXviVtvLPh2_A&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=N24j6vEM4QA5pFN8rGtgSQ&_nc_ss=7b20f&oh=00_Af7h6kIWTFPVrhHCpx6cAuI9WqgK5lOIzRIctByCsCKlEQ&oe=6A1C31F2)

### 1. Send an order details message

Follow the full integration guide in the [Orders API page](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/orders).

If Payment Link payment is available on this order, you will need to provide a `payment_link` to the `payment_settings` attribute. You can optionally include an `order` object with itemized products, fees, and discounts, or send a simplified message with just the total amount and payment settings.

The following images show how the order details message with Payment Links appears in WhatsApp, in both full and simplified versions.

![Full order details message with Payment Link showing itemized products and Open payment link button](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/672159259_1482949483563701_4921268168995059725_n.png?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=doWY5aNN_CUQ7kNvwHmLwWV&_nc_oc=AdoM6pITgJSkGzZFOFLKlLW6Bno2cOOc2ZdPtzCEwoQCScnFNbFZXXj72qXBYfulFxM&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=N24j6vEM4QA5pFN8rGtgSQ&_nc_ss=7b20f&oh=00_Af5O0sT61oDms0c-moXXFLpRacLIzMwsduuler-LoG5awQ&oe=6A1C22F2)![Simplified order details message with Payment Link showing total amount and Open payment link button](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/671847286_1482949486897034_2098909345778483921_n.png?_nc_cat=106&ccb=1-7&_nc_sid=e280be&_nc_ohc=1di0cDnWMhQQ7kNvwEPThzw&_nc_oc=AdpG75onjsA6oRBIo0vaZUuEHI9IvwC8ovq6isgNwNTUyD9BBXlZgQDMwfa6nXqCns4&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=N24j6vEM4QA5pFN8rGtgSQ&_nc_ss=7b20f&oh=00_Af5_xO5SEO1vP5Tb0HWnVJGpUOGISrbb1bNzSJJM7Rt_uA&oe=6A1C2B51)

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

Parameters object

| Field Name | Optional? | Type | Description |
| --- | --- | --- | --- |
| `payment_settings` | Optional | [Payment Settings Object](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/payment-links#paymentsettingsobject) | List of payment related configuration objects. |

Payment settings

| Field Name | Optional? | Type | Description |
| --- | --- | --- | --- |
| `type` | Required | String | Must be `payment_link`. |
| `payment_link` | Required | [Payment Link Object](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/payment-links#paymentlinkobject) | Payment Link object that will be used to render the option to buyers during the checkout flow. |

Payment link object

| Field Name | Optional? | Type | Description |
| --- | --- | --- | --- |
| `uri` | Required | String | The Payment Link’s uri which will be opened in the web browser, when user taps on the Payment Link CTA button. |

### 2. Send an order status update

Once the payment is confirmed, you must send an order status update. Follow the integration guide in the [Orders API page](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/orders).
