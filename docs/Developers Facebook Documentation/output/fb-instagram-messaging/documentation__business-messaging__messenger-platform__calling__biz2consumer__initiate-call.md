# Initiate and end a call | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/biz2consumer/initiate-call_

---

# Initiate and end a call

Updated: Mar 23, 2026

After the consumer has granted call permission, use the new call API to initiate a call by providing an SDP offer.

## Before you begin

- Complete the setup described in the [Calling overview](https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling)
- Verify the consumer has granted [call permission](https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/biz2consumer/check-permissions)

## Initiate a call

Use this API to start a call by providing the consumer’s PSID and an SDP offer. A successful response includes an SDP answer that you apply to your local peer connection.

### Request syntax

```curl
POST /{page-id}/calls
{
  "platform": "messenger",
  "to": "{psid}",
  "action": "connect",
  "session": {
      "sdp_type": "offer",
      "sdp": "<<RFC 4566 SDP>>"
   }
}
```

### Request parameters

| Property | Description |
| --- | --- |
| `to` string | The Page-scoped ID of the consumer to call |
| `action` string | Set to `connect` to initiate a call |
| `session` JSON | Connection information containing:<br>`sdp`: SDP offer compliant with [RFC 4566](https://datatracker.ietf.org/doc/html/rfc4566)`sdp_type`: Set to `offer` |

### Example response

```json
{
  "success": true,
  "id": "c_M5YPhGE5jm0L_PMQdScLlYJlR7tU_f0rgXinCqnTQ",
  "session": {
    "sdp_response": {
      "sdp_type": "answer",
      "sdp": "<<RFC 4566 SDP>>"
    }
  }
}
```

### Response fields

| Property | Description |
| --- | --- |
| `success` boolean | Whether the operation was successful |
| `id` string | Unique ID for this call. Use this ID for subsequent API calls and to correlate webhooks. |
| `session` JSON | Contains `sdp_response` with the SDP answer. Apply this answer to your local peer connection. |

### Error response

The following errors can occur:

- Invalid Page ID
- Permissions or authorization errors
- Consumer has not given permission to call
- Request format validation errors (for example, connection info, SDP, or ICE)

For more details, see the [Messenger Platform error codes reference](https://developers.facebook.com/documentation/business-messaging/messenger-platform/error-codes).

## Terminate a call

Use this API to end an active call.

### Request syntax

```curl
POST /{page-id}/calls
{
  "platform": "messenger",
  "call_id": "{call-id}",
  "action" : "terminate"
}
```

### Request parameters

| Property | Description |
| --- | --- |
| `platform` Optional string | Only `Messenger` is supported |
| `call_id` string | ID of the call from the webhook or the new call API response |
| `action` string | Set to `terminate` |

### Example response

```json
{
  "success" : true
}
```

### Error response

The following errors can occur:

- Invalid call ID or Page ID
- Call already terminated
- Cannot terminate a failed or completed call
- Permissions or authorization errors

For more details, see the [Messenger Platform error codes reference](https://developers.facebook.com/documentation/business-messaging/messenger-platform/error-codes).

## Next steps

- Handle [calling webhooks](https://developers.facebook.com/docs/messenger-platform/calling/biz2consumer/webhooks) for call status, media updates, and termination events
- See the [end-to-end call flow](https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/biz2consumer/call-flow) for a complete walkthrough
www/flib/intern/public-developer-docs/social/mdsourcedc/business-messaging/messenger-platform/_staging/calling/biz2consumer/webhooks.md
