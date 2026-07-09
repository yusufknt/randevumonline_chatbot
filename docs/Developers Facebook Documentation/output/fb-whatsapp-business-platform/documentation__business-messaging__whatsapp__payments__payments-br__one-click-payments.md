# One-Click Payments | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/one-click-payments_

---

# One-Click Payments

Updated: Nov 14, 2025

This feature is not publicly available yet and is only available for businesses based in Brazil and their Brazilian customers. To enable payments for your businesses, please contact your Solution Partner.

Payments API also enables businesses to collect payments from their customers via WhatsApp using One-Click Payments.

When using this integration, WhatsApp facilitates communication between merchants and buyers. Merchants are responsible for storing payment credentials and integrating with a payment service provider (PSP) to submit these credentials, completing and confirming their payments.

## Before you start

1. Familiarize yourself with the [Orders API](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/orders) . Orders are the entrypoint for collecting payments in WhatsApp.
2. You will need an existing integration with a PSP and do automatic reconciliation when a payment is made.
3. You must update the order status as soon as a payment is made.

## Integration steps

The following sequence diagram shows the typical integration with One-Click Payments.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/560189002_1339318344593483_6488145365318201089_n.jpg?_nc_cat=102&ccb=1-7&_nc_sid=e280be&_nc_ohc=9nOR7KthQRcQ7kNvwHTnPMg&_nc_oc=AdrymUV3DRHuABoWOG4j4Yc8iFrUMcF_7C5BNQpLH0wZs4rmGLDrFuNvjhgQGHcIkl8&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=hr8aofqzIkXiaudDjjsJTQ&_nc_ss=7b20f&oh=00_Af4UST1GV7E_soMYTRT1QUhQFZANliTcOsnPJNWZ0xEnzw&oe=6A1C0268)

### 1. Send an Order Details message

Follow the full integration guide in the [Orders API page](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/orders).

If One-Click Payments is available on this order, you will need to provide a `offsite_card_pay` object in the `payment_settings` attribute. You can optionally include an `order` object with itemized products, fees, and discounts, or send a simplified message with just the total amount and payment settings.

The following images show how the order details message with One-Click Payments appears in WhatsApp, in both full and simplified versions.

![Full order details message with One-Click Payments showing itemized products, card ending in 1234, and Review payment button](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/673815587_1482949453563704_2192854088357669533_n.png?_nc_cat=110&ccb=1-7&_nc_sid=e280be&_nc_ohc=mekhoczXAN0Q7kNvwGONx-W&_nc_oc=Adrc5Gm6F6aDN1DA0FAwoV7Cj6q2nYEdPOlUhYI3o8M9kmBYTqLnwvftN0MPoqsBctY&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=hr8aofqzIkXiaudDjjsJTQ&_nc_ss=7b20f&oh=00_Af5MW1v-k3QabReZGeYTK4Hwiz-09EQcKIHJbYyuQhVXwg&oe=6A1C0A06)![Simplified order details message with One-Click Payments showing total amount, card ending in 1234, and Review payment button](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/672338884_1482949460230370_3565215131767087588_n.png?_nc_cat=111&ccb=1-7&_nc_sid=e280be&_nc_ohc=T_ZU_E4Aw-MQ7kNvwHnKyB5&_nc_oc=AdpkF1_XtZjMOsWZEx0DwEDVL5fif6TwGRr0_VAiMhhBOY3gPGk1CNdzdq1OM8a31bI&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=hr8aofqzIkXiaudDjjsJTQ&_nc_ss=7b20f&oh=00_Af5o28OCLJKa5R4iOQKb1D99JLjSn5leWAYIU-WtyX7X6Q&oe=6A1C297A)

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
        "reference_id": "<UNIQUE_REFERENCE_ID>",
        "type": "digital-goods",
        "payment_type": "br",
        "payment_settings": [
          {
            "type": "offsite_card_pay",
            "offsite_card_pay": {
              "last_four_digits": "5235",
              "credential_id": "1234567"
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
        "reference_id": "<UNIQUE_REFERENCE_ID>",
        "type": "digital-goods",
        "payment_type": "br",
        "payment_settings": [
          {
            "type": "offsite_card_pay",
            "offsite_card_pay": {
              "last_four_digits": "5235",
              "credential_id": "1234567"
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
| `payment_settings` | Optional | [Payment Settings Object](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/one-click-payments#paymentsettingsobject) | List of payment related configuration objects. |

Payment settings

| Field Name | Optional? | Type | Description |
| --- | --- | --- | --- |
| `type` | Required | String | Must be `offsite_card_pay`. |
| `offsite_card_pay` | Required | [Offsite Card Pay Object](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/one-click-payments#offsitecardpayobject) | Offsite Card Pay object that will be used to render the option to buyers during the checkout flow. |

Offsite card pay object

| Field Name | Optional? | Type | Description |
| --- | --- | --- | --- |
| `last_four_digits` | Required | String | The last four digits of the card, which will be displayed to the user for confirmation before they accept the payment (by tapping the “Send payment” CTA button). |
| `credential_id` | Required | String | The ID of the credential associated with the card. After the user taps the “Send Payment” CTA button, the merchant will receive a webhook from Meta notifying that confirmation from the user. The payload of that webhook will contain this credential_id, which the merchant will use to determine the card or credential for payments. |

### 2. Receive the webhook notification

After the WhatsApp user taps “Review payment”, they see the payment confirmation screen shown below.

![One-Click Payments confirmation screen showing card details, total amount, and Send payment button](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/672132965_1482949450230371_6445601384729249309_n.png?_nc_cat=106&ccb=1-7&_nc_sid=e280be&_nc_ohc=bDtvOuFX1u0Q7kNvwFsCxeO&_nc_oc=AdrypzTDLHHrzlLHmzyWGSY9-rTD4o6eGH2V-z8_69UyRuFgJAxJv81nIXq5_jZ21bg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=hr8aofqzIkXiaudDjjsJTQ&_nc_ss=7b20f&oh=00_Af4pW1gXP0HzAY5UrJBdx1FKsI_2YlRCtesIntiH6iq1kw&oe=6A1C0DFA)

This webhook confirms the buyer’s intention to make a payment and includes the ID of the credential to use.

Webhook notification payload example

```json
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "<WHATSAPP_BUSINESS_ACCOUNT_ID>",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "<BUSINESS_DISPLAY_PHONE_NUMBER>",
              "phone_number_id": "<BUSINESS_PHONE_NUMBER_ID>"
            },
            "contacts": [
              {
                "profile": {
                  "name": "<WHATSAPP_USER_NAME>"
                },
                "wa_id": "<WHATSAPP_USER_ID>"
              }
            ],
            "messages": [
              {
                "from": "<WHATSAPP_USER_PHONE_NUMBER>",
                "id": "<WHATSAPP_MESSAGE_ID>",
                "timestamp": "<WEBHOOK_SENT_TIMESTAMP>",
                "from_logical_id": "64244926160970",
                "type": "interactive",
                "interactive": {
                  "type": "payment_method",
                  "payment_method": {
                    "payment_method": "offsite_card_pay",
                    "payment_timestamp": 1726170122,
                    "reference_id": "pix_test_webhook",
                    "last_four_digits": "5235",
                    "credential_id": "1234567"
                  }
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

### 3. Send an order status update

Once the payment is confirmed, you must send an order status update. Follow the integration guide in the [Orders API page](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/orders).
