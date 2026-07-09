# Configure message time-to-live | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/time-to-live_

---

# Configure message time-to-live

Updated: Apr 30, 2026

If a message cannot be delivered to a WhatsApp user, delivery is retried for a period of time known as *time-to-live* (“TTL”), or the message validity period.

You can customize the default TTL for authentication and utility templates sent via Cloud API, and for marketing templates sent via Marketing Messages API for WhatsApp.

Set a TTL for all authentication templates, preferably equal to or less than your code expiration time, to ensure your customers only get a message when a code is still usable.

## Defaults, min/max values, and compatibility table

|  | Authentication | Utility | Marketing |
| --- | --- | --- | --- |
| **Default TTL** | 10 minutes<br>30 days for authentication templates created before October 23, 2024 | 30 days | 30 days |
| **Compatibility** | Cloud API | Cloud API only | Marketing Messages API for WhatsApp |
| **Customizable range** | 30 seconds to 15 minutes | 30 seconds to 12 hours | 12 hours to 30 days |

## Customize the TTL

To set a custom TTL on an authentication, utility, or marketing template, include the `message_send_ttl_seconds` property in the `POST /<PHONE_NUMBER_ID>/message_templates` call.

You can change the TTL on a previously configured template using this method, as well.

TTL can be customized in 1 second increments.

### Valid `message_send_ttl_seconds` property values

- Authentication templates: `30` to `900` seconds (30 seconds to 15 minutes)
- Utility templates: `30` to `43200` seconds (30 seconds to 12 hours)
- Marketing templates: `43200` to `2592000` (12 hours to 30 days)

For authentication and utility templates, you can set the `message_send_ttl_seconds` property value to `-1`, which will set a custom TTL of 30 days.

### Example request

```curl
curl 'https://graph.facebook.com/v21.0/102290129340398/message_templates' \
      -H 'Authorization: Bearer EAAJB...' \
      -H 'Content-Type: application/json' \
      -d '
      {
        "name": "test_template",
        "language": "en_US",
        "category": "MARKETING",
        "message_send_ttl_seconds": 120,
        "components": [
          {
            "type": "BODY",
            "text": "Shop now through {{1}} and use code {{2}} to get {{3}} off of all merchandise.",
            "example": {
              "body_text": [
                [
                  "the end of August","25OFF","25%"
                ]
              ]
            }
          },
          {
            "type": "FOOTER",
            "text": "Use the buttons below to manage your marketing subscriptions"
          },
        ]
      }'
```

### Sample response

```json
{
  "id": "572279198452421",
  "status": "PENDING",
  "category": "MARKETING"
}
```

### When TTL is exceeded

The system drops messages that cannot be delivered within the default or customized TTL.

If you do not receive a [delivered message webhook](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/status) before the TTL is exceeded, assume the message was dropped.

If you send a message that [fails to deliver](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/status), there could be a minor delay before you receive the webhook, so you may wish to build in a small buffer before assuming the message was dropped.

### TTL reset on automatic category updates

If a template is reclassified by an [automatic category update](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-categorization/#automatic-category-updates), the TTL value is cleared by setting it to a *null value*.
You can reset the TTL to any value within the customizable range for the new template category, as listed in the [Defaults, min/max values, and compatibility table](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/time-to-live#defaults-minmax-values-and-compatibility-table).

For example, if a utility template with a custom TTL of 12 hours is reclassified as a marketing template, the custom TTL is cleared (`message_send_ttl_seconds` = `null`).
At this point, you can set the TTL to any value between 12 hours and 30 days, which is the customizable range for marketing templates, as listed in the table above.

See [Template categorization](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-categorization/) for more details about WABA message template categories and associated workflows.
