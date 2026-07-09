# Tracking click events | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/track-click-events_

---

# Tracking click events

Updated: Feb 10, 2026

*Available using Marketing Messages API for WhatsApp (MM API for WhatsApp) and Ads Manager only*

We deliver a webhook payload when users click on the body or call-to-action of your marketing message. You can subscribe to this webhook to capture this data and use it to inform your campaign decisions.

## Limitations

- At the moment, this feature is not available for all users
- Click events are only available for messages sent in the last 7 days

## Webhooks

To receive this webhook, subscribe to the `whatsapp_business_account` webhook topic. The webhook payload is on the `messages` field and is delivered as below:

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
            "user_actions": [
              {
                "action_type": "marketing_messages_link_click",
                "timestamp": "<time_of_click>",
                "marketing_messages_link_click_data": {
                  "click_component": "cta" | "body",
                  "product_id": "sku_id",
                  "click_id": "click_id",
                  "tracking_token": "example_token"
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

| Field Name | Field Type | Field Description |
| --- | --- | --- |
| `action_type` | **Required**<br>String | Name of the action |
| `timestamp` | **Required**<br>Unix timestamp | Timestamp of when the event happened |
| `click_component` | **Optional**<br>Enum | The click action<br>Can either be `cta` or `body` |
| `click_id` | **Optional**<br>String | The unique identifier for the click. Is also appended to the original url when the user visits the url. |
| `tracking_token` | **Optional**<br>String | Internal Meta token for processing and tracking |
| `product_id` | **Optional**<br>String | ID of the product, if it was assigned in Ads Manager or Marketing API. |
