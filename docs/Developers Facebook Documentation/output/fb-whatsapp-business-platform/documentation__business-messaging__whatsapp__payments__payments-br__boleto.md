# Boleto | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/boleto_

---

# Boleto

Updated: Nov 14, 2025

Payments API also enables businesses to collect payments from their customers via WhatsApp using Boleto.

When using this integration, WhatsApp only facilitates the communication between merchants and buyers. Merchants are responsible for integrating with a PSP from which they can generate Boleto codes, and confirm their payment.

## Before you start

1. Familiarize yourself with the [Orders API](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/orders) . Orders are the entrypoint for collecting payments in WhatsApp.
2. You will need an existing integration with a PSP to generate Boleto codes and do automatic reconciliation when a payment is made.
3. You must update the order status as soon as a payment is made.

## Integration steps

The following sequence diagram shows the typical integration with Boleto.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/561622607_1339318274593490_8768265383653853535_n.jpg?_nc_cat=110&ccb=1-7&_nc_sid=e280be&_nc_ohc=bIRHs3mvyU4Q7kNvwG_1Bow&_nc_oc=AdoYei2bjaeGqdNK1Z3w7ebs6aSL-L0KfjCg31XXOngUBOrJB9O8xJg7x0vyZsRyRHI&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=hcD9fFb87m84s9zXaUG_hg&_nc_ss=7b20f&oh=00_Af5PpeW702aVUQFmi5KsZ5yy5bpGiPz1jRxLC2cL25xvNg&oe=6A1C17C5)

### 1. Send an Order Details message

Follow the full integration guide in the [Orders API page](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/orders).

If Boleto payment is available on this order, you will need to provide a `boleto` object in the `payment_settings` attribute. You can optionally include an `order` object with itemized products, fees, and discounts, or send a simplified message with just the total amount and payment settings.

The following images show how the order details message with Boleto appears in WhatsApp, in both full and simplified versions.

![Full order details message with Boleto showing itemized products and Copy Boleto code button](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/672096263_1482949426897040_3119189760917924652_n.png?_nc_cat=110&ccb=1-7&_nc_sid=e280be&_nc_ohc=GmM62Z7TGKkQ7kNvwHOfnBD&_nc_oc=AdpgLamSYHhC6oYffLHvwLCtA379t0AHOAqYqq33dYBjyrGFpjEXnn9WTlYyCGOEefo&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=hcD9fFb87m84s9zXaUG_hg&_nc_ss=7b20f&oh=00_Af5PLVNyVz3vI4MLSi0tBlDskbOwQSkC9Lm3UeRFciu3zQ&oe=6A1C1DF5)![Simplified order details message with Boleto showing total amount and Copy Boleto code button](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/672037282_1482949446897038_7515930059113700177_n.png?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=HRazDZO1BykQ7kNvwGZn44W&_nc_oc=AdpKB5V_mVfYXiox2UyROOMgnKwGLrcUtbikkIlnZGhyjNxahDMtSAwLaM8ScB6A5Fg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=hcD9fFb87m84s9zXaUG_hg&_nc_ss=7b20f&oh=00_Af72uaOYL_DLTZ82qcun-KAYWCbaBNNF_RgrCtWrtWg2ig&oe=6A1C03A5)

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
            "type": "boleto",
            "boleto": {
              "digitable_line": "03399026944140000002628346101018898510000008848"
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
            "type": "boleto",
            "boleto": {
              "digitable_line": "03399026944140000002628346101018898510000008848"
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
| `payment_settings` | Optional | [Payment Settings Object](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/boleto#paymentsettingsobject) | List of payment related configuration objects. |

Payment settings

| Field Name | Optional? | Type | Description |
| --- | --- | --- | --- |
| `type` | Required | String | Must be `boleto`. |
| `boleto` | Required | [Boleto Object](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/boleto#boletoobject) | Boleto object that will be used to render the option to buyers during the checkout flow. |

Boleto object

| Field Name | Optional? | Type | Description |
| --- | --- | --- | --- |
| `digitable_line` | Required | String | The Boleto digital line / code which will be copied to the clipboard, when user taps on the Boleto CTA button. |

### 2. Send an order status update

Once the payment is confirmed, you must send an order status update. Follow the integration guide in the [Orders API page](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/orders).
