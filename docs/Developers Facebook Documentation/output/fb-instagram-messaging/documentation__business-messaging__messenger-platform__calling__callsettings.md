# Call Settings | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/callsettings_

---

# Call Settings

Updated: Mar 30, 2026

## Call icon visibility controls

You can hide the call icon in a Messenger thread by setting `icon_enabled` to false using the Messenger Call Settings API. By default, the call icon visibility is set to `true` for all Pages. When `icon_enabled` is set to `false`, the call icon won’t display in any threads for that Page.

Additionally, users can’t initiate calls from Missed Call or Completed Call messages when icon visibility is turned off. You can send a Call Prompt message to allow the user to call your business.

Use this API to enable or disable the call icon for the Page.

| Property | Description |
| --- | --- |
| `icon_enabled` boolean | Set to `true` to make call icon visible in Messenger threads, or `false` to hide the call icon in Messenger threads |

```curl
POST /<PAGE_ID>/messenger_call_settings
{
    "icon_enabled" : <boolean_value>
}
```

### Example response

| Property | Description |
| --- | --- |
| `result` string | `success` if the icon visibility was successfully set<br>`failure` if the icon visibility could not be set |

```json
{
  "result": "success/failure"
}
```

### Error response

The following errors can happen:

- Incorrect permissions for the API request

For more details on these errors, see the [Messenger Platform error codes reference](https://developers.facebook.com/documentation/business-messaging/messenger-platform/error-codes).

### Send a call prompt message using Messenger Send API

You can send a new template `call_prompt`. This template contains a button that lets the consumer initiate a call with your business. The consumer can initiate the call for the number of days you specify when sending the message. Use `ttl_days` to specify how many days the calling button remains active for the consumer. If you don’t specify `ttl_days`, the calling button is active for **7 days** by default.

Call the Messenger Send API with the following payload to send a Call CTA to the consumer.

| Property | Description |
| --- | --- |
| `recipient.id` string | Consumer’s PSID that the message will be sent to |
| `message`<br>JSON | The text/attachment that will be sent to the consumer |
| `message.attachment.type` string | Type of the attachment; for a Call CTA, it will always be `template` |
| `message.attachment.payload.template_type` string | Type of template being sent |
| `message.attachment.payload.ttl_days` int | Number of days the user will be able to initiate a new call by clicking on the template |

### Example response

| Property | Description |
| --- | --- |
| `recipient.id` string | Consumer’s PSID that the message will be sent to |
| `message_id`<br>string | `id` representing the successfully sent message |

```json
{
  "recipient_id": "<PSID>"
  "message_id": "<Message-id>"
}
```

### Error response

The following errors can happen:

- The Page does not have calling enabled
- The Page does not have the correct permissions to send messages
- The Page is sending the message outside of the allowed messaging window

For more details on these errors, see the [Messenger Platform error codes reference](https://developers.facebook.com/documentation/business-messaging/messenger-platform/error-codes).

### Call hours

Use this API to update the settings. This updates the same setting on Meta Business Suite and the Messenger app.
To set the call hours for a Page, make an API request to the `messenger_call_settings` endpoint and set `call_hours`.
Updates in existing chats are near real-time.
When you set hours, any previous settings are erased. Any days you don’t set default to closed.

| Property | Description |
| --- | --- |
| `timezone_id` ISO 8601 timezone string | Timezone |
| `weekly_operating_hours` array | Operating hours schedule for each day of the week. Can be an empty array |
| `day_of_week` string | `MONDAY\|TUESDAY\|WEDNESDAY\|THURSDAY\|FRIDAY\|SATURDAY\|SUNDAY` |
| `day_of_week` string | `MONDAY\|TUESDAY\|WEDNESDAY\|THURSDAY\|FRIDAY\|SATURDAY\|SUNDAY` |
| `open_time` string | Open time expressed in the format hhmm. Example: 0000 = 12AM, 0900 = 9AM, 1200 = 12PM, 1830 = 6:30PM |
| `close_time` string | Close time expressed in the format hhmm. Example: 0000 = 12AM, 0900 = 9AM, 1200 = 12PM, 1830 = 6:30PM |

```curl
POST /<PAGE_ID>/messenger_call_settings
{
    "call_hours": {
      "timezone_id": "America/Los_Angeles",
      "weekly_operating_hours": [
        {
          "day_of_week": "MONDAY",
          "open_time": "0900",
          "close_time": "1700"
        },
        {
          "day_of_week": "TUESDAY",
          "open_time": "0930",
          "close_time": "1830"
        }
      ]
    }
}
```

### Example response

| Property | Description |
| --- | --- |
| `success` boolean | Whether the operation was successful. |

```json
{
  "success": true
}
```

### Error response

The following errors can happen:

- Invalid page-id
- Invalid time for weekly call hours
- Close time cannot be before open time
- Duplicate day in request

For more details on these errors, see the [Messenger Platform error codes reference](https://developers.facebook.com/documentation/business-messaging/messenger-platform/error-codes).

### Get call hours

To retrieve the current call hours for a Page, send a GET request to the `messenger_call_settings` endpoint.

| Property | Description |
| --- | --- |
| `Page-Id` string | The delegate Page ID |

```curl
GET /<PAGE_ID>/messenger_call_settings?fields=call_hours
```

### Example response

| Property | Description |
| --- | --- |
| `call_hours` array | Call hours for each day of the week |

```json
{
    "call_hours": {
      "timezone_id": "America/Los_Angeles",
      "weekly_operating_hours": [
        {
          "day_of_week": "MONDAY",
          "open_time": "0900",
          "close_time": "1700"
        },
        {
          "day_of_week": "TUESDAY",
          "open_time": "0930",
          "close_time": "1830"
        }
      ]
    }
}
```

### Error response

The following errors can happen:

- Invalid page-id

For more details on these errors, see the [Messenger Platform error codes reference](https://developers.facebook.com/documentation/business-messaging/messenger-platform/error-codes).

### Call settings update webhook

You can subscribe to the `call_settings_update` webhook to receive notifications whenever your call settings change. For example, if you disable calling via Messenger or update your call hours, this information is sent as a webhook to the subscribed applications.

| Property | Description |
| --- | --- |
| `id` string | Page ID connected to the app |
| `time`<br>Unix timestamp | Time at which Meta processes the call settings update and sends the webhook |
| `audio_enabled` boolean | Whether the business Page has enabled or disabled audio calling |
| `icon_enabled` boolean | Whether the call icon is visible or hidden in Messenger threads |
| `recipient_id` string | ID of the callee that generated this status (PSID of the user). |
| `call_routing` enum | **META**: Incoming calls will only ring meta-owned platforms such as Business Inbox in Messenger and Meta Business Suite)**PARTNERS**: Incoming calls will only ring third party applications |
| `call_hours` array | Call hours for each day of the week |

```json
{
  "object": "page",
  "entry": [
    {
      "id": <PAGE_ID>,
      "time": 1671644824,
      "call_settings": {
          "audio_enabled": true,
          "icon_enabled": true,
          "call_routing": "PARTNERS",
          "call_hours": {
              "timezone_id": "timezone_id",
              "weekly_operating_hours": [
                 {
                   "day_of_week": "MONDAY",
                   "open_time": "0400",
                   "close_time": "1020"
                 },
                 {
                    "day_of_week": "TUESDAY",
                    "open_time": "0108",
                    "close_time": "1020"
                 }
              ],
          },
      }
    }
  ]
}
```

### Inbound call routing

You can select whether incoming calls ring Meta apps such as Business Inbox in Messenger or third-party apps integrated with the Messenger Calling API.
To configure where incoming calls are routed, make an API request to the `messenger_call_settings` endpoint and set `call_routing`.

Use this API to update the settings. This setting only affects consumer-initiated calls. For business-initiated calls, the Page can always place calls using both Meta-owned platforms and third-party applications.

**Call Platform**: Determines where the business will receive incoming call rings.

**Prerequisites**: App must be subscribed to calls webhook to set `ring_target` to `PARTNERS`.

| Property | Description |
| --- | --- |
| `Page-id` string | The delegate Page ID |
| `call_routing`<br>JSON | `ring_target`: Enum value<br>**META**:<br>Incoming calls will only ring meta-owned platforms such as Business Inbox in Messenger and Meta Business Suite**PARTNERS**:<br>Incoming calls will only ring third party applications |

```curl
POST /<PAGE_ID>/messenger_call_settings
{
    "call_routing": {
        "ring_target": <RING_TARGET>
    }
}
```

### Example response

| Property | Description |
| --- | --- |
| `success` boolean | Whether the operation was successful |

```json
{
  "success": true
}
```

### Error response

The following errors can happen:

- Invalid page-id
- Invalid call routing value
- Page not yet eligible

For more details on these errors, see the [Messenger Platform error codes reference](https://developers.facebook.com/documentation/business-messaging/messenger-platform/error-codes).

### Get call routing

To retrieve the current call routing for a Page, send a GET request to the `messenger_call_settings` endpoint.

| Property | Description |
| --- | --- |
| `Page-Id` string | The delegate Page ID |

```curl
GET /<PAGE_ID>/messenger_call_settings?fields=call_routing
```

### Example response

| Property | Description |
| --- | --- |
| `call_routing` JSON | object with value `ring_target` having enum value |

```json
{
  "call_routing": {
    "ring_target": "PARTNERS"
  }
}
```

### Error response

The following errors can happen:

- Invalid page-id

For more details on these errors, see the [Messenger Platform error codes reference](https://developers.facebook.com/documentation/business-messaging/messenger-platform/error-codes).
