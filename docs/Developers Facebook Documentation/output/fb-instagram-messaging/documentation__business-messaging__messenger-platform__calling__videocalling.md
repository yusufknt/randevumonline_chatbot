# Video Calling | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/videocalling_

---

# Video Calling

Updated: Mar 16, 2026

Video calling enables a richer user experience as well as new business cases such as screen sharing and visual information presentation.

## Video calling sequences

### Consumer turns on or off video during a call

If the call starts with audio only and the consumer turns on their video during the call, a `media_update` webhook is sent. Like business-initiated calling, when you receive this webhook, you must generate an SDP answer using the SDP information and apply that answer to your local peer connection. See the appendix for an example media update webhook containing video track data.

At this time only the Opus codec is supported. For video codecs, the following are supported:

- VP8
- VP9
- H264
- H265
- AV1

If the consumer switches from the front camera to the back camera, the system reuses the same video stream. You don’t need to process any media update for this case.

Video codec trade-offs involve processing power, device support, video quality, and network bandwidth. The following table helps guide your decision. You can specify multiple codecs supported in your SDP offer along with a priority configuration. Additionally, the WebRTC standard requires all browsers to support both H264 and VP8.

REMB and TWCC are supported for bandwidth estimation (BWE).

| Codec | Processing Power | Device Support | Video Quality | Network Bandwidth | Use Case |
| --- | --- | --- | --- | --- | --- |
| VP8 | Low-Medium | Wide (WebRTC native) | Medium | Medium-High | Wide support and minimum network bandwidth |
| VP9 | Medium-High | Wide (WebRTC native) | High | Low-Medium | Higher quality than VP8 and less network bandwidth but not supported on as many devices |
| H264 | Medium | Very Wide (hardware accelerated) | High | Medium-High | Most broad support and high quality |
| H265 | High | Limited (hardware accelerated on newer devices) | Very High | Low | Higher quality than H264 and less network bandwidth but not supported on as many devices |
| AV1 | High | Increasing (WebRTC native, but limited hardware acceleration) | Very High | Low | Highest quality and least network bandwidth but only supports modern devices |

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/653714501_1459945555864094_6097340399940926871_n.png?_nc_cat=111&ccb=1-7&_nc_sid=e280be&_nc_ohc=Bie0VT7wWNYQ7kNvwEKAbA1&_nc_oc=Adq_K_JRDPMuKHMnu-Fha-K4fRDWRVJOh2aQZuikJ00IQYr5VUdRU27U-ekb_i6KlTk&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=-g7KDVUWlZMY7tiIPxBf1A&_nc_ss=7b20f&oh=00_Af5Y8B5tjPR3WQy3yg6tJYCgx-M_0WOGLkbmkFBl6-R5hg&oe=6A1C203F)

### Business turns on or off video during a call

To turn video on or off during a call, send an API request to `/<page-id>/calls` with `action=media_update` and an SDP offer containing your updated media tracks. See the appendix for example SDP offer and answer.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/653880407_1459945445864105_5572676567888886251_n.png?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=4R1Tfwk8BFgQ7kNvwFUqFLg&_nc_oc=AdqlqnJ8x-MCDzdnDg2YKZc4twGnNZKN2Oc7Qx33C--q94lfYkQVjx0FuCbGlLTs4GU&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=-g7KDVUWlZMY7tiIPxBf1A&_nc_ss=7b20f&oh=00_Af6iyB-tL-SfsbCZBOwVfK88KyYE8O6SaWNvbM3C-zVwqQ&oe=6A1C4013)

### Consumer and business turn on or off video at the same time

If both the consumer and the business turn their video on or off at the same time during a call, a request collision state occurs. This is handled by the `from_version` and `to_version` in the API request. The API caller receives a `200 OK` with no SDP offer or an error about conflicting media status. In either case, the client should process the version updates and retry the request.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/652226921_1459945449197438_3447051051210416102_n.png?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=K3dj5H6EZSYQ7kNvwG8RZil&_nc_oc=AdoDe3kZ7M7M0b2l-Zfs35_oYyTnAhAHvt-FsRh8MXFZSLT63O7cLbiLJv3VdjniHCM&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=-g7KDVUWlZMY7tiIPxBf1A&_nc_ss=7b20f&oh=00_Af4tJYaSDOD95RQYRNc6BMa3MRqw4uIklmVODhvV8cPKCA&oe=6A1C3DE5)

## Messenger calling APIs

### Update Media Tracks

Use this API to update your media tracks during a call, such as adding or removing a video or audio track.

**To or from version**

Your client should maintain its version state. It starts at 0 at the beginning of the call. Every time your client makes a new SDP offer, increment the version. Additionally, every time your client receives a `media_update` webhook from Meta, increment the version. This prevents race conditions where your client calls the media update API between Meta sending a `media_update` webhook.

If the versions do not match what the API expects, an error or empty SDP response is returned and you can retry the `media_update` request with the correct version. Please note this is not the same as the version number in the o= line in the SDP.

**Tracks**

You can use this parameter to enable or disable media tracks that Meta is already aware of on the call. For example, if you have a call with audio track 123 and already enabled video with track ID 456, you can turn your video off by sending an API request to this endpoint specifying enabled_tracks: [“123”] without renegotiating SDP. The API currently supports 2 tracks: one for audio and one for video.

Bundle is supported and required in the SDP offer. This means the same network IP and port is used for all tracks (audio, video, and so on) in the call.

| Property | Description |
| --- | --- |
| `platform`<br>Optional string | Only `messenger` is supported at this time |
| `call_id`<br>string | ID of the call from the webhook you previously received for this call |
| `action`<br>string | `media_update` |
| `from_version`<br>string | The current media version of your local client |
| `to_version`<br>string | The new media version that your client is moving to |
| `tracks`<br>Array of objects | Metadata about the media tracks you want to add/update<br>1) `tracks[i].msid`: string that matches the msid line in the sdp offer<br>2) `tracks[i].label`: enum value<br>`DEFAULT_AUDIO`: the default audio track (typically a microphone)`DEFAULT_VIDEO`: the default video track (typically a webcam)<br>3) `tracks[i].status`: enum value<br>`ENABLED`: the track is enabled`DISABLED`: the track is disabled |
| `session`<br>JSON | JSON serialized string with following 2 keys:<br>1) `sdp`: SDP offer of the device on the other end of the call. See the appendix for example structure.<br>2) `sdp_type`: “offer” to indicate an SDP offer |

```curl
POST /<PAGE_ID>/calls
{
  "platform": "messenger",
  "call_id": "c_M5YPhGE5jm0L_PMQdScLlYJlR7tU_f0rgXinCqnTQ",
  "action": "media_update",
  "from_version": "0",
  "to_version": "1",
  "tracks": [
     {
       "msid", "123-abc",
       "label": "default_audio",
       "status": "enabled"
     },
     {
       "msid", "456-def",
       "label": "default_video",
       "status": "enabled"
     }
  ],
  "session" : {
     "sdp_type" : "offer",
     "sdp" : "<<RFC 4566 SDP>>"
  }
}
```

### Example Response

| Property | Description |
| --- | --- |
| `success`<br>boolean | Whether the operation is successful |
| `session`<br>JSON | SDP data. The API response includes an SDP response that should be applied to the business peer connection. |

```json
{
  "success" : true
  "session" : {
     "sdp_response" : {
       "sdp_type": "answer",
       "sdp": "<<RFC 4566 SDP>>"
     },
     "sdp_renegotiation": {
       "sdp_type": "offer",
       "sdp": "<<RFC 4566 SDP>>"
     }
  }
}
```

### Error Response

The following errors can happen:

- Invalid call id
- Invalid page-id
- Invalid connection info (for example, SDP, ICE, and so on).
- Permissions/Authorization errors
- Cannot update a terminated call
- Invalid track msid param
- Calling app is not call owner

For more details on these errors, see the [Messenger Platform Error Code reference](https://developers.facebook.com/documentation/business-messaging/messenger-platform/error-codes).
