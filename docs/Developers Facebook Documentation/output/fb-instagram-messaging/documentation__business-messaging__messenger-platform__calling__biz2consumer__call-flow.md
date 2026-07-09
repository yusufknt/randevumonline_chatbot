# Business-initiated call flow | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/biz2consumer/call-flow_

---

# Business-initiated call flow

Updated: Apr 2, 2026

This walkthrough shows a complete business-initiated call flow, from requesting permission to ending the call.

## Before you begin

- Complete the setup described in the [Calling overview](https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling)
- Subscribe to the `calls` and `call_permission_reply` webhook fields

## Send a call permission request

Send the consumer a call permission request:

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

You receive a confirmation response:

```html
{
  "recipient": {
    "id": "{psid}"
  },
  "message_id": "{mid}"
}
```

## Receive the permission reply webhook

When the consumer approves or rejects the request, you receive a `call_permission_reply` webhook:

```html
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

## Initiate the call

Generate an SDP offer and call the `/calls` API:

```html
const offer = await pc.createOffer();
await pc.setLocalDescription(offer);
```

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

## Receive call status webhooks

You receive webhooks as the call progresses:

```html
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

## Handle the media update webhook

After the consumer accepts, you receive a `media_update` webhook with an SDP renegotiation offer:

```html
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

Generate an SDP answer and apply it to your peer connection:

```html
onMediaUpdate = async (mediaUpdateSDP) => {
  pc.setRemoteDescription(new RTCSessionDescription({
    sdp: mediaUpdateSDP.sdp, type: mediaUpdateSDP.sdp_type
  })).then(
    () => {
      pc.createAnswer().then(answer => {
        pc.setLocalDescription(answer);
      });
    }
  )
}
```

The call is now connected. You can hang up at any time, or receive a terminate webhook when the consumer ends the call.
