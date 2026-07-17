# phone_number_quality_update webhook reference | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/phone_number_quality_update_

---

# phone_number_quality_update webhook reference

Updated: Nov 14, 2025

This reference describes trigger events and payload contents for the WhatsApp Business Account **phone_number_quality_update** webhook.

The **phone_number_quality_update** webhook notifies you of changes to a business phone number’s [throughput level](https://developers.facebook.com/documentation/business-messaging/whatsapp/throughput).

## Triggers

- A business phone number’s throughput level changes.

## Syntax

```html
{
    "entry": [
      {
        "id": "<WHATSAPP_BUSINESS_ACCOUNT_ID>",
        "time": <WEBHOOK_TRIGGER_TIMESTAMP>,
        "changes": [
          {
            "value": {
              "display_phone_number": "<BUSINESS_DISPLAY_PHONE_NUMBER>",
              "event": "<EVENT>",
              "old_limit": "<OLD_LIMIT>", <!-- only included for messaging limit changes -->
              "current_limit": "<CURRENT_LIMIT>",
              "max_daily_conversations_per_business": "<MAX_DAILY_MESSAGES_LIMIT>"
            },
            "field": "phone_number_quality_update"
          }
        ]
      }
    ],
    "object": "whatsapp_business_account"
  }
```

## Parameters

| Placeholder | Description | Example value |
| --- | --- | --- |
| `<BUSINESS_DISPLAY_PHONE_NUMBER>`<br>*String* | Business display phone number. | `15550783881` |
| `<CURRENT_LIMIT>`<br>*String* | **This field will be removed in February, 2026. Use `max_daily_conversations_per_business` instead.**<br>Indicates current [messaging limit](https://developers.facebook.com/documentation/business-messaging/whatsapp/messaging-limits) or [throughput](https://developers.facebook.com/documentation/business-messaging/whatsapp/throughput) level.<br>Values can be:<br>`TIER_50` — Indicates a messaging limit of 50.<br>`TIER_250` — Indicates a messaging limit of 250.<br>`TIER_2K` — Indicates a messaging limit of 2,000.<br>`TIER_10K` — Indicates a messaging limit of 10,000.<br>`TIER_100K` — Indicates a messaging limit of 100,000.<br>`TIER_NOT_SET` — Indicates the business phone number has not been used to send a message yet.<br>`TIER_UNLIMITED` — Indicates the business phone number has higher throughput. | `TIER_UNLIMITED` |
| `<EVENT>`<br>*String* | [Messaging limit](https://developers.facebook.com/documentation/business-messaging/whatsapp/messaging-limits) change or [throughput](https://developers.facebook.com/documentation/business-messaging/whatsapp/throughput) change event.<br>Values can be:<br>`ONBOARDING` — Indicates the business phone number is still being registered.<br>`THROUGHPUT_UPGRADE` — Indicates the business phone number’s throughput level has increased to higher throughput. | `THROUGHPUT_UPGRADE` |
| `<MAX_DAILY_MESSAGES_LIMIT>`<br>*String* | Indicates a change to the owning business portfolio’s [messaging limit](https://developers.facebook.com/documentation/business-messaging/whatsapp/messaging-limits) or [throughput](https://developers.facebook.com/documentation/business-messaging/whatsapp/throughput) change.<br>Values can be:<br>`TIER_50` — Indicates a messaging limit of 50.<br>`TIER_250` — Indicates a messaging limit of 250.<br>`TIER_2K` — Indicates a messaging limit of 2,000.<br>`TIER_10K` — Indicates a messaging limit of 10,000.<br>`TIER_100K` — Indicates a messaging limit of 100,000.<br>`TIER_NOT_SET` — Indicates the business phone number has not been used to send a message yet.<br>`TIER_UNLIMITED` — Indicates the business phone number has higher throughput. | `TIER_2K` |
| `<OLD_LIMIT>`<br>*String* | **This parameter will be removed in February, 2026. Use `max_daily_conversations_per_business` instead.**<br>Indicates old [messaging limit](https://developers.facebook.com/documentation/business-messaging/whatsapp/messaging-limits).<br>Values can be:<br>`TIER_50` — Indicates a messaging limit of 50.<br>`TIER_250` — Indicates a messaging limit of 250.<br>`TIER_2K` — Indicates a messaging limit of 2,000.<br>`TIER_10K` — Indicates a messaging limit of 10,000.<br>`TIER_100K` — Indicates a messaging limit of 100,000.<br>`TIER_NOT_SET` — Indicates the business phone number has not been used to send a message yet. | `TIER_UNLIMITED` |
| `<WEBHOOK_TRIGGER_TIMESTAMP>`<br>*Integer* | Unix timestamp indicating when the webhook was triggered. | `1739321024` |
| `<WHATSAPP_BUSINESS_ACCOUNT_ID>`<br>*String* | WhatsApp Business Account ID. | `102290129340398` |

## Example

```json
{
  "entry": [
    {
      "id": "102290129340398",
      "time": 1748454394,
      "changes": [
        {
          "value": {
            "display_phone_number": "15550783881",
            "event": "THROUGHPUT_UPGRADE",
            "current_limit": "TIER_UNLIMITED"
          },
          "field": "phone_number_quality_update"
        }
      ]
    }
  ],
  "object": "whatsapp_business_account"
}
```
