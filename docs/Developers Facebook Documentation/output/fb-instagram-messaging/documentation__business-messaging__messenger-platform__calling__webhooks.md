# Calling webhooks | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/webhooks_

---

# Calling webhooks

Updated: Mar 23, 2026

When a call is initiated or received, Meta sends webhook events on the `calls` field to notify you of call lifecycle changes. The webhook structure follows the same pattern as [Messenger Platform webhooks](https://developers.facebook.com/documentation/business-messaging/messenger-platform/webhooks).

Subscribe to the `calls` webhook field to receive these events. For business-initiated calls, also subscribe to the `call_permission_reply` field.

## Connect

**Applies to:** consumer-initiated and business-initiated calls

This webhook notifies you in near real-time when a call is initiated. For consumer-initiated calls, respond by calling `/{page-id}/calls` with `action=accept` to establish the WebRTC connection.

```json
{
  "object": "page",
  "entry": [
    {
      "id": "{page-id}",
      "time": 1671644824,
      "calls": [
        {
          "id": "c_M5YPhGE5jm0L_PMQdScLlYJlR7tU_f0rgXiTQ",
          "to": "106378625516323",
          "from": "5275811702471834",
          "event": "connect",
          "timestamp": 1671644824,
          "call_direction": "[business_initiated|user_initiated]"
        }
      ]
    }
  ]
}
```

| Property | Description |
| --- | --- |
| `id` string | Unique ID for the call. Use this in your accept, reject, or terminate API calls. |
| `to` string | Callee of the call (Page ID) |
| `from` string | Caller of the call (PSID) |
| `event` string | `connect` or `terminate` |
| `timestamp` Unix timestamp | Start time of the call from the caller’s perspective |
| `call_direction` string | `business_initiated` or `user_initiated` |

## Call status

**Applies to:** business-initiated calls only

This webhook notifies you when a business-initiated call begins ringing or is accepted by the consumer.

```json
{
  "object": "page",
  "entry": [
    {
      "id": "{page-id}",
      "time": 1671644824,
      "calls": [
        {
          "id": "c_M5YPhGE5jm0L_PMQdScLlYJlR7tU_f0rgXiTQ",
          "event": "call_status",
          "timestamp": 1671644824,
          "recipient_id": "{psid}",
          "call_status": "[ringing | accepted]"
        }
      ]
    }
  ]
}
```

| Property | Description |
| --- | --- |
| `id` string | Unique ID for the call |
| `event` string | `call_status` |
| `recipient_id` string | PSID of the consumer |
| `call_status` string | `ringing`: The outgoing call is ringing the consumer’s device`accepted`: The consumer accepted the call |

## Media update

**Applies to:** business-initiated calls only

This webhook notifies you when a consumer-side media event occurs, providing new SDP information that you must apply to your local peer connection. Triggers include:

- Consumer picks up the business-initiated call
- Consumer mutes or unmutes

When you receive this webhook, generate an SDP answer from the offer and apply it to your local peer connection to establish or update the WebRTC connection.

```json
{
  "object": "page",
  "entry": [
    {
      "id": "{page-id}",
      "time": 1671644824,
      "calls": [
        {
          "id": "c_M5YPhGE5jm0L_PMQdScLlYJlR7tU_f0rgXiTQ",
          "event": "media_update",
          "timestamp": 1671644824,
          "session": {
              "version": 1,
              "sdp_renegotiation": {
                  "sdp_type": "offer",
                  "sdp": "<<RFC 4566 SDP>>"
              }
          }
        }
      ]
    }
  ]
}
```

| Property | Description |
| --- | --- |
| `event` string | `media_update` |
| `session.version` integer | Incremented each time Meta provides new SDP. If you receive multiple `media_update` webhooks, apply the one with the highest version number. |
| `session.sdp_renegotiation` JSON | Contains the SDP offer from Meta. Generate an answer from this offer and apply it to your local peer connection.<br>`sdp`: SDP data compliant with [RFC 4566](https://datatracker.ietf.org/doc/html/rfc4566)`sdp_type`: `offer` |

## Terminate

**Applies to:** consumer-initiated and business-initiated calls

This webhook notifies you when the call ends for any reason. This occurs when:

- The consumer hangs up
- Your app calls `/{page-id}/calls` with `action=terminate`
- Your app calls `/{page-id}/calls` with `action=reject` (consumer-initiated calls only)

```json
{
  "object": "page",
  "entry": [
    {
      "id": "{page-id}",
      "time": 1671644824,
      "calls": [
        {
          "id": "c_M5YPhGE5jm0L_PMQdScLlYJlR7tU_f0rgXiTQ",
          "event": "terminate",
          "timestamp": 1671644824,
          "status" : "[Failed | Completed]",
          "start_time" : 1671644824,
          "end_time" : 1671644944,
          "duration" : 120
        }
      ]
    }
  ]
}
```

| Property | Description |
| --- | --- |
| `status` string | Final status of the call:<br>`Completed`: Call finished normally (includes calls rejected by the consumer or business)`Failed`: Call failed mid-connection |
| `start_time` Unix timestamp | When the call started |
| `end_time` Unix timestamp | When the call ended |
| `duration` integer | Call duration in seconds, counted from when the business connects. Empty if the business did not successfully connect. |
