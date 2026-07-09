# Receipt Template | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/api-reference/receipt_

---

# Receipt Template

Updated: Oct 23, 2025

The receipt template allows you to send an order confirmation as a structured message. The template may include an order summary, payment details, and shipping information.

```json
{
  "message_id": "<MESSAGE_ID>",
  "messenger_delivery_data": {
    "subscription_token": "<SUBSCRIPTION_TOKEN>"
  },
  "message":{
    "attachment":{
      "type":"template",
      "payload":{
        "template_type":"receipt",
        "recipient_name":"<RECIPIENT_FULL_NAME>",
        "order_number":"<ORDER_NUMBER>",
        "currency":"USD",
        "payment_method":"<PAYMENT_METHOD>",
        "order_url":"<ORDER_URL>",
        "timestamp":"1428444852",
        "address":{
          "street_1":"<ADDRESS_LINE_1>",
          "street_2":"<ADDRESS_LINE_2>",
          "city":"<CITY>",
          "postal_code":"<POSTAL_CODE>",
          "state":"<STATE>",
          "country":"US"
        },
        "summary":{
          "subtotal":75.00,
          "shipping_cost":4.95,
          "total_tax":6.19,
          "total_cost":56.14
        },
        "adjustments":[
          {
            "name":"New Customer Discount",
            "amount":20
          },
          {
            "name":"$10 Off Coupon",
            "amount":10
          }
        ],
        "elements":[
          {
            "title":"Classic White T-Shirt",
            "subtitle":"100% Soft and Luxurious Cotton",
            "quantity":2,
            "price":50,
            "currency":"USD",
            "image_url":"<IMAGE_URL>"
          },
          {
            "title":"Classic Gray T-Shirt",
            "subtitle":"100% Soft and Luxurious Cotton",
            "quantity":1,
            "price":25,
            "currency":"USD",
            "image_url":"<IMAGE_URL>"
          }
        ]
      }
    }
  }
}
```
