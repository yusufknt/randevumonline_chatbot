# business_capability_update webhook reference | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/business_capability_update_

---

# business_capability_update webhook reference

Updated: Nov 14, 2025

This reference describes trigger events and payload contents for the WhatsApp Business Account **business_capability_update** webhook.

The **business_capability_update** webhook notifies you of WhatsApp Business Account or business portfolio capability changes ([messaging limits](https://developers.facebook.com/documentation/business-messaging/whatsapp/messaging-limits#increasing-your-limit), [phone number limits](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers#registered-number-cap), etc.).

## Triggers

- A WhatsApp Business Account is created.
- A WhatsApp Business Account or business portfolio business capability (e.g. [messaging limits](https://developers.facebook.com/documentation/business-messaging/whatsapp/messaging-limits#increasing-your-limit) , [phone number limits](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers#registered-number-limits) ) is increased or decreased.

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
            "max_daily_conversation_per_phone": <MAX_DAILY_CONVERSATIONS_PER_PHONE>,
            "max_daily_conversations_per_business": <MAX_DAILY_CONVERSATIONS_PER_BUSINESS>,
            "max_phone_numbers_per_business": <MAX_PHONES_PER_BUSINESS_PORTFOLIO>,
            "max_phone_numbers_per_waba": <MAX_PHONES_PER_WHATSAPP_BUSINESS_ACCOUNT>
          },
          "field": "business_capability_update"
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
| `<MAX_DAILY_CONVERSATIONS_PER_PHONE>`<br>*Integer* | **This parameter will be removed in February, 2026. Use `max_daily_conversations_per_business` instead.**<br>Business portfolio’s [messaging limit](https://developers.facebook.com/documentation/business-messaging/whatsapp/messaging-limits). Values can be:<br>`250``2000``10000``100000``-1`<br>A value of `-1` indicates unlimited messaging. | `2000` |
| `<MAX_DAILY_CONVERSATIONS_PER_BUSINESS>`<br>*Integer* | Business portfolio’s [messaging limit](https://developers.facebook.com/documentation/business-messaging/whatsapp/messaging-limits).<br>Value can be:<br>`TIER_250``TIER_2K``TIER_10K``TIER_100K``TIER_UNLIMITED` | `TIER_UNLIMITED` |
| `<MAX_PHONES_PER_BUSINESS_PORTFOLIO>`<br>*Integer* | Maximum number of business phone numbers the business portfolio can have.<br>This property is only included if `max_daily_conversation_per_phone` is set to `250`. | `2` |
| `<MAX_PHONES_PER_WHATSAPP_BUSINESS_ACCOUNT>`<br>*Integer* | Maximum number of business phone numbers allowed per WABA.<br>This property is only included if `max_daily_conversation_per_phone` is **not** set to `250`. | `25` |
| `<WEBHOOK_TRIGGER_TIMESTAMP>`<br>*Integer* | Unix timestamp indicating when the webhook was triggered. | `1739321024` |
| `<WHATSAPP_BUSINESS_ACCOUNT_ID>`<br>*String* | WhatsApp Business Account ID. | `102290129340398` |

## Payload example

```json
{
  "entry": [
    {
      "id": "524126980791429",
      "time": 1739321024,
      "changes": [
        {
          "value": {
            "max_daily_conversations_per_business": 2000,
            "max_phone_numbers_per_waba": 25
          },
          "field": "business_capability_update"
        }
      ]
    }
  ],
  "object": "whatsapp_business_account"
}
```
