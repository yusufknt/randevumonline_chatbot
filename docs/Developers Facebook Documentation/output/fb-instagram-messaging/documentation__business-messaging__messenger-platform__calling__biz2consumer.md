# Business to Consumer Calling | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/biz2consumer_

---

# Business to Consumer Calling

Updated: Mar 23, 2026

Business to consumer calling lets your app initiate outbound VoIP calls to consumers on Messenger. Before placing a call, you must obtain the consumer’s permission.

## Before you begin

- Complete the setup described in the [Calling overview](https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling)
- [Subscribe to the `calls` and `call_permission_reply` webhook fields](https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/webhooks)

## How it works

1. **Check permissions** — Query the consumer’s current call permission status
2. **Obtain permission** — If the consumer hasn’t granted permission, send a call permission request
3. **Initiate the call** — Provide an SDP offer to start the call; receive an SDP answer to establish the WebRTC connection
4. **Handle webhooks** — Receive call status updates (ringing, accepted), media updates, and termination events
5. **End the call** — Terminate the call when finished

### Call sequence

![Business to consumer calling sequence diagram showing permission request, call initiation, and termination flow](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/652905953_1459945702530746_7013550775337240075_n.png?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=0J8KOtYLhoIQ7kNvwFCjOR9&_nc_oc=AdrfWWo_NicFHyKIbBm0f9xqt7euVev_1hbXOjdfhyXBcE6YQ-i6ko3YH2gbWlmhtNI&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=U-qG2QWB2BS-YzmnX9ziXA&_nc_ss=7b20f&oh=00_Af4uHn6F9upkbJEmXR0Kj_gOpkqXqPUmfx6L4WmjQyYmfQ&oe=6A1C382B)

## Guides

| Guide | Description |
| --- | --- |
| [Check and obtain call permissions](https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/biz2consumer/check-permissions) | Query permission status, send permission requests, and handle permission reply webhooks |
| [Calling webhooks](https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/webhooks) | Handle call status, media update, and terminate webhook events |
| [Initiate and end a call](https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/biz2consumer/initiate-call) | Start a new call with an SDP offer and terminate active calls |
| [End-to-end call flow](https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/biz2consumer/call-flow) | Complete walkthrough of a business-initiated call from permission request to termination |
