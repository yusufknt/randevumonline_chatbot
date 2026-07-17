# Consumer to Business Calling | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/consumer2biz_

---

# Consumer to Business Calling

Updated: Apr 19, 2026

Consumer to business calling lets your app handle inbound VoIP calls from consumers on Messenger. When a consumer calls your Page, you receive a connect webhook and have 60 seconds to accept the call.

## Before you begin

- Complete the setup described in the [Calling overview](https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling)
- Subscribe to the `calls` webhook field

## How it works

1. **Receive a connect webhook** — A consumer initiates a call from the Messenger app
2. **Accept, reject, or let it ring** — You have 60 seconds to respond with the accept API and an SDP offer
3. **Establish the WebRTC connection** — Apply the SDP answer from the API response to your local peer connection
4. **Handle call events** — Receive terminate webhooks when the call ends

### Call sequence

![Consumer to business calling sequence diagram showing call initiation and acceptance flow](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/652875991_1459945685864081_8440652347787608727_n.png?_nc_cat=111&ccb=1-7&_nc_sid=e280be&_nc_ohc=NXcYWL3gVCwQ7kNvwEiHwRb&_nc_oc=Ado5gKLwhtpe1B3yGx1V-gpeYODXOfHcJYOHn-l00UUtOBwX0C-xzjpfvjqMZ7KokCc&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=T6Vt_yLh0gev9AAR_PX4pg&_nc_ss=7b20f&oh=00_Af5FLyt4guCH7AuDm1xS3_z02aepHgVS4Qpt2ptR6CW5gA&oe=6A1C36AD)![Consumer to business calling sequence diagram showing media exchange](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/651681289_1459945632530753_5719949635892387730_n.png?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=YaeBAkmwXOEQ7kNvwHxVu_p&_nc_oc=AdrKRTu-DRhXkYgB-Gr0e0F-8jytOdlplKcwwgs-bzzZnfcsnSjf6Y00pX5hGGTBW28&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=T6Vt_yLh0gev9AAR_PX4pg&_nc_ss=7b20f&oh=00_Af6hCxlOjSrYn-rMF0kOLH8kydNH9z7uzuPnaUR6KpdxeQ&oe=6A1C3422)![Consumer to business calling sequence diagram showing call termination](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/653707877_1459945539197429_3525969672189555151_n.png?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=vRHn2TUqUacQ7kNvwHUinl5&_nc_oc=AdobOjBAHWKbvE1BdmGnACaV6z9hHtcE3u2f_JE0YOYmd5pwgZEYzvFG-46pj33r1Mc&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=T6Vt_yLh0gev9AAR_PX4pg&_nc_ss=7b20f&oh=00_Af5jKeA-CatVN5-q0GcoEmim-1VMt69iLHpg7wd6ly3Bmg&oe=6A1C1BAF)

## Guides

| Guide | Description |
| --- | --- |
| [Calling webhooks](https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/webhooks) | Handle call status, media update, and terminate webhook events |
| [Accept a call](https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/consumer2biz/accept-c2b-call) | Accept an incoming call by providing an SDP offer and establishing the WebRTC connection |
| [Reject or end a call](https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/consumer2biz/reject-end-call) | Reject an incoming call or terminate an active call |
| [End-to-end call flow](https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/consumer2biz/call-flow) | Complete walkthrough of a consumer-initiated call from ring to termination |
