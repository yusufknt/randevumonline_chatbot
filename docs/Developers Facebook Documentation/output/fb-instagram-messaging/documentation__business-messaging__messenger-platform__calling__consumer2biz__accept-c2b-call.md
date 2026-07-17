# Accept a call | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/consumer2biz/accept-c2b-call_

---

# Accept a call

Updated: Mar 23, 2026

When a consumer calls your Page, you receive a [connect webhook](https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/webhooks#connect). You have **60 seconds** to accept the call. If you don’t respond, the call terminates on the consumer side with “Not Answered” and you receive a terminate webhook.

## Before you begin

- Complete the setup described in the [Calling overview](https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling)
- Subscribe to the `calls` webhook field

## Accept a consumer-initiated call

### Request syntax

```curl
POST /{page-id}/calls
{
  "platform": "messenger",
  "call_id": "{call-id}",
  "action": "accept",
  "session" : {
     "sdp_type" : "offer",
     "sdp" : "<<RFC 4566 SDP>>"
  }
}
```

### Request parameters

| Property | Description |
| --- | --- |
| `platform` Optional string | Only `Messenger` is supported |
| `call_id` string | ID of the call from the connect webhook |
| `action` string | Set to `accept` |
| `session` JSON | Connection information containing:<br>`sdp`: SDP offer compliant with [RFC 4566](https://datatracker.ietf.org/doc/html/rfc4566). See the [appendix](https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/appendix) for example SDP structures.`sdp_type`: Set to `offer` |

### Example response

```json
{
  "success" : true,
  "session" : {
     "sdp_response" : "<<RFC 4566 SDP>>",
     "sdp_renegotiation" : "<<RFC 4566 SDP>>"
  }
}
```

The response may include both `sdp_response` and `sdp_renegotiation`. If both are present, first apply the answer, then the renegotiation offer to the peer connection and regenerate the local answer.

### Error response

The following errors can occur:

- Invalid call ID or Page ID
- Invalid connection info (for example, SDP or ICE)
- Permissions or authorization errors
- Call already accepted
- Cannot accept a failed or terminated call
- Calling app is not call owner

For more details, see the [Messenger Platform error codes reference](https://developers.facebook.com/documentation/business-messaging/messenger-platform/error-codes).

## Next steps

- Learn how to [reject or end a call](https://developers.facebook.com/docs/messenger-platform/calling/consumer2biz/reject-terminate)
- See the [end-to-end call flow](https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/consumer2biz/call-flow) for a complete walkthrough
