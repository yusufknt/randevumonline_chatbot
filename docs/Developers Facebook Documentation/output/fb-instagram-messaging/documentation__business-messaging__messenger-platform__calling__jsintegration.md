# JS Integration | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/jsintegration_

---

# JS Integration

Updated: Mar 16, 2026

This page provides JavaScript code samples for using the Messenger Calling API.

### Accept an incoming call

```js
// 'pc' is the browser peer connection object

// create sdp offer
let offerDescription = await pc.createOffer();
await pc.setLocalDescription(offerDescription);

// create request to messenger calling api accept endpoint with sdp offer
let data = {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    'host': host,
    'access_token': accessToken,
    'call_id': callID,
    'sdp': offerDescription.sdp,
    'sdp_type': offerDescription.type,
  }),
};
let url = `https://graph.facebook.com/page-id/calls`

fetch(url, data).then(response => {
  response.json().then(data => {
    if (data.success) {
      pc.setRemoteDescription(new RTCSessionDescription({sdp: data.session.sdp_response.sdp, type: 'answer'}));
      pc.setRemoteDescription(new RTCSessionDescription({sdp: data.session.sdp_renegotiation.sdp, type: 'offer'}));
      pc.createAnswer().then(answer => {
        pc.setLocalDescription(answer);
      });
    } else {
      // handle api error response
    }
  })
}).catch(error => {
  // handle error
});
```

### Apply the SDP answer from a new call API response

```js
const offer = await pc.createOffer();
await pc.setLocalDescription(offer);
let data = {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    'host': host,
    'access_token': accessToken,
    'sdp': offer.sdp,
    'sdp_type': offer.type,
    'to': psid,
  }),
};
let url = `https://graph.facebook.com/page-id/calls`
fetch(url, data).then(response => {
  response.json().then(data => {
    if (data.success) {
      pc.setRemoteDescription(new RTCSessionDescription({
        sdp: data.session.sdp_response.sdp,
        type: 'answer'
      }));
    } else {
      // handle api error response
    }
  })
}).catch(error => {
  // handle error
});
```

### Generate the SDP answer from a SDP renegotiation offer from a media_update_webhook

```js
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

### Turn on business video

```js
// assuming our pc is already connected with an audio call
let stream = await navigator.mediaDevices.getUserMedia({
  video: true,
  audio: true,
});
let webcamVideo = stream.getVideoTracks()[0];
let webcamAudio = stream.getAudioTracks()[0];
pc.addTransceiver(webcamVideo, stream);
let tracks = [
  {
    msid: webcamVideo.id,
    label: 'DEFAULT_VIDEO',
    status: 'enabled',
  },
  {
    msid: webcamAudio.id,
    label: 'DEFAULT_AUDIO',
    status: 'enabled',
  }
];
let fromVersion = this.state.version; // track call version
let toVersion = fromVersion+1;
let offer = await pc.createOffer();
await pc.setLocalDescription(offer);

// create request to messenger calling api media_update endpoint with sdp offer
let data = {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    'host': host,
    'access_token': accessToken,
    'call_id': callID,
     tracks: tracks,
    'from_version': fromVersion,
    'to_version': toVersion,
    'sdp': offer.sdp,
  }),
};
let url = `https://graph.facebook.com/page-id/calls`
fetch(url, data).then(response => {
  response.json().then(data => {
    if (data.success) {
      pc.setRemoteDescription(new RTCSessionDescription({sdp: data.session.sdp_response.sdp, type: 'answer'}));
      // increment version
      if (data.session.sdp_renegotiation) {
        pc.setRemoteDescription(new RTCSessionDescription({sdp: data.session.sdp_renegotiation.sdp, type: 'offer'}));
        // increment version
        pc.createAnswer().then(answer => {
          pc.setLocalDescription(answer);
        });
      }
      else {
      // handle api error response
     }
  })
}).catch(error => {
  // handle error
});
```
