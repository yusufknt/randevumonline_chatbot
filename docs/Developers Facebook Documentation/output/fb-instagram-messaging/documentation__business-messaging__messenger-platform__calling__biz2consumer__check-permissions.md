# Check and obtain call permissions | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/biz2consumer/check-permissions_

---

# Check and obtain call permissions

Updated: Apr 6, 2026

Before placing a call to a consumer, you must verify that the consumer has granted call permission. Use the call permissions check API to query the current status, and send a permission request if needed.

## Before you begin

- Complete the setup described in the [Calling overview](https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling)
- Subscribe to the `call_permission_reply` webhook field

## Check call permission status

Use this API to check a consumer’s real-time call permission status and decide whether to request permission or start a call directly.

### Request syntax

```curl
GET /{page-id}/messenger_call_permissions?psid={psid}
```

### Request parameters

| Property | Description |
| --- | --- |
| `page-id` string | The delegate ID of the business Facebook Page |
| `psid` string | Unique PSID for the consumer on this Page |

### Example response

```json
{
   "permission": {
    "status": "has_permission",
    "expiration_time": 1745343479
  },
  "actions": [
    {
      "action_name": "send_call_permission_request",
      "can_perform_action": false,
      "limits": [
        {
          "time_period": "PT24H",
          "max_allowed_per_user": 2,
          "current_usage": 1
        }
      ]
    },
    {
      "action_name": "start_call",
      "can_perform_action": true
    }
  ]
}
```

### Response fields

| Property | Description |
| --- | --- |
| `permission` JSON | The current permission status:<br>`no_permission`: No permission found for this consumer`has_permission`: Consumer granted a permanent permission<br>`expiration_time` (included only when status is `has_permission`): Unix timestamp (in seconds, UTC) when the permission expires. Default expiration is 7 days after the consumer grants permission. |
| `actions` JSON | List of actions you can take:<br>`send_call_permission_request`: Send a new call permission request to the consumer`start_call`: Establish a new call with the consumer (requires existing permission and connected call quota within limits)<br>Each action includes `can_perform_action` (boolean) and optional `limits` with `time_period`, `max_allowed_per_user`, and `current_usage`. |

### Error response

The following errors can occur:

- Invalid Page ID or PSID
- Permissions or authorization errors
- Not allowed for business-initiated calling
- Audio calling is not enabled

For more details, see the [Messenger Platform error codes reference](https://developers.facebook.com/documentation/business-messaging/messenger-platform/error-codes).

## Send a call permission request

To place a call to a consumer, you must first receive their permission. You can obtain permission in the following ways:

1. Send a call permission request that the consumer approves
2. The consumer provides implicit callback permission after: A fully connected call with the businessThe consumer calls the business but the business does not pick up

Each calling permission expires after **7 days**. You can send at most **2 call permission requests per thread per day**.

### Request syntax

```curl
POST /{page-id}/messages
{
  "recipient": {
   "id": "{psid}"
  },
  "message": {
    "attachment" : {
      "type":"template",
      "payload":{
         "template_type":"calling_optin"
      }
    }
  }
}
```

### Request parameters

| Property | Description |
| --- | --- |
| `recipient` string | The Page-scoped ID of the consumer to whom the opt-in is requested |
| `template_type` string | Must be `calling_optin` |

The consumer receives a message with **Accept** and **Decline** buttons.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/662981823_1476699224188727_7178588206044227035_n.png?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=GJfTiZbvHIQQ7kNvwFFGOgs&_nc_oc=Adp6RWPtZuUU3JINdSYOPMFldRA4V1oiwQo7rnRtVpvqmLyxzclTPssI8VRpETvv8go&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=5zFgFNMWZEi040GtLonmzw&_nc_ss=7b20f&oh=00_Af4pB-xecd9_dJxOXmJOrRCRHOqkKAqUAawKKC1GHWyalA&oe=6A1C2738)

### Example response

```json
{
  "recipient": {
    "id": "{psid}"
  },
  "message_id": "{mid}"
}
```

### Error response

The following errors can occur:

- Send API errors such as insufficient permission or messaging outside of 24-hour window
- Rate limit reached (2 permission requests per thread per day)

For more details, see the [Messenger Platform error codes reference](https://developers.facebook.com/documentation/business-messaging/messenger-platform/error-codes).

## Call permission reply webhook

When the consumer clicks **Accept** or **Decline**, you receive a postback webhook with the `call_permission_reply` field.

```json
{
  "object": "page",
  "entry": [
    {
      "sender": {
        "id": "{psid}"
      },
      "recipient": {
        "id": "{page-id}"
      },
      "timestamp": 1671644824,
      "call_permission_reply": {
        "response": "[approve|reject]",
        "expiration_timestamp": "{timestamp}"
      }
    }
  ]
}
```

| Property | Description |
| --- | --- |
| `response` string | The consumer’s response: `approve` or `reject` |
| `expiration_timestamp` Unix timestamp | When the permission expires. Only included if the consumer approved the request. |

## Next steps

Once the consumer has granted permission, [initiate a call](https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/biz2consumer/initiate-call).
