# Developer Platform

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/consumer2biz/call-flow_

---

# Consumer-initiated call flow

Updated: Mar 23, 2026

This walkthrough shows a complete consumer-initiated call flow, from receiving the incoming call to ending it.

## Before you begin

- Complete the setup described in the [Calling overview](https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling)
- Subscribe to the `calls` webhook field

## Receive the connect webhook

When a consumer calls your Page from the Messenger app, you receive a connect webhook:

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
          "call_direction": "user_initiated"
        }
      ]
    }
  ]
}
```

## Accept the call

Respond within 60 seconds by calling the `/calls` API with an SDP offer:

```curl
POST /{page-id}/calls
{
  "call_id": "c_M5YPhGE5jm0L_PMQdScLlYJlR7tU_f0rgXinCqnTQ",
  "action": "accept",
  "session" : {
     "sdp" : "<<RFC 4566 SDP>>",
     "sdp_type" : "offer"
  }
}
```

You receive an SDP answer in the response:

```json
{
  "success" : true,
  "session" : {
    "sdp_response" : "<<RFC 4566 SDP>>",
    "sdp_renegotiation" : "<<RFC 4566 SDP>>"
  }
}
```

## Establish the WebRTC connection

Apply the response and renegotiation offer to your local peer connection:

```js
fetch(url, data).then(response => {
  response.json().then(data => {
    pc.setRemoteDescription(new RTCSessionDescription({
      sdp: data.session.sdp_response.sdp, type: 'answer'
    }));
    pc.setRemoteDescription(new RTCSessionDescription({
      sdp: data.session.sdp_renegotiation.sdp, type: 'offer'
    }));
    pc.createAnswer().then(answer => {
      pc.setLocalDescription(answer);
    });
  })
});
```

The call is now connected.

## Terminate the call

To end the call, send a terminate request:

```curl
POST /{page-id}/calls
{
  "call_id": "c_M5YPhGE5jm0L_PMQdScLlYJlR7tU_f0rgXinCqnTQ",
  "action" : "terminate"
}
```

You receive a confirmation:

```json
{
  "success" : true
}
```

## Receive the terminate webhook

After the call ends (whether you terminated it or the consumer hung up), you receive a terminate webhook:

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
          "status" : "Completed",
          "start_time" : 1671644824,
          "end_time" : 1671644944,
          "duration" : 120
        }
      ]
    }
  ]
}
```
