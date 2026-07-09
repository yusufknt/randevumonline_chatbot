# Calling | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling_

---

# Calling

Updated: Apr 20, 2026

The Messenger Business Calling API enables VoIP communication between consumers and businesses on Messenger. Consumers use the Messenger app to place and receive calls. Your app interfaces with Messenger through the Graph API and webhooks for call signaling and connection.

## How it works

When a call is initiated, your app exchanges SDP (Session Description Protocol) offers and answers with Meta through the Graph API to establish a WebRTC connection. Once connected, audio and video streams flow directly over the WebRTC peer connection.

Your app handles call lifecycle events — accepting, rejecting, and terminating calls — through API calls and receives status updates through webhooks.

## Features

| Feature | Description |
| --- | --- |
| [Consumer to business calling](https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/consumer2biz) | Accept, reject, or terminate calls initiated by consumers |
| [Business to consumer calling](https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/biz2consumer) | Initiate outbound calls to consumers, manage permissions |
| [Video calling](https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/videocalling) | Enable video during calls, with codec selection and media updates |
| [Call settings](https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/callsettings) | Configure call icon visibility, business hours, and inbound call routing |
| [Call audio CTA](https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/callaudiocta) | Add audio call buttons to generic and button templates |
| [DTMF](https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling#dtmf) | Support touch-tone input for IVR-based systems |
| [Metrics](https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/metrics) | Submit call quality metrics to Meta after each call |
| [JS integration](https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/jsintegration) | JavaScript code samples for WebRTC peer connection handling |
| [Appendix](https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/appendix) | Sample SDP offer and answer structures |

## DTMF

The Messenger Calling API supports DTMF tones, enabling you to support IVR-based systems for participating businesses.

Consumers can press buttons on the client app, and the DTMF tones are injected into the WebRTC RTP stream established as part of the VoIP connection. The WebRTC stream conforms to [RFC 4733](https://datatracker.ietf.org/doc/html/rfc4733) for the transfer of DTMF digits via RTP payload. Note: there is **no webhook** for conveying DTMF digits.

### Sending DTMF digits on consumer Messenger client

The Messenger client applications include a dialpad for calls with Messenger businesses. Consumers can press buttons on the client app dialpad to send DTMF tones.

### Delivering DTMF digits on WebRTC connection

When a consumer presses a digit in the dialpad on the client, the equivalent DTMF is injected into the WebRTC connection. [Tone values](https://datatracker.ietf.org/doc/html/rfc4733#autoid-41) include digits 0 to 9, #, and *. Duration is **500ms** and inter-tone gap is **100ms** for all tones.

## Check Page eligibility

Before making calls, verify that your Facebook Page has access to the Calling API by sending a `POST` request to `/<PAGE_ID>/business_messaging_feature_status` with the feature `messenger_api_calling`. A status of `ENABLED` confirms the Page has access.

```html
POST /{page-id}/business_messaging_feature_status
{
  "features": [
    {
      "feature": "messenger_api_calling"
    }
  ]
}
```

You receive the status in the response:

```html
{
  "data": [
    {
      "feature": "messenger_api_calling",
      "status": "enabled"
    }
  ]
}
```

For more details on errors, see the [Messenger Platform error codes reference](https://developers.facebook.com/documentation/business-messaging/messenger-platform/error-codes).

## Available countries

The Messenger Calling API is currently available for Pages in the following countries:

- Angola
- Argentina
- Armenia
- Australia
- Bosnia and Herzegovina
- Congo (DRC)
- Dominican Republic
- Ecuador
- Honduras
- Hong Kong
- Indonesia
- Israel
- Ivory Coast
- Jordan
- Kenya
- Laos
- Macau
- Malaysia
- Moldova
- Mongolia
- Morocco
- Mozambique
- Nepal
- Nicaragua
- Nigeria
- Oman
- Pakistan
- Panama
- Philippines
- Qatar
- Russia
- Saudi Arabia
- Serbia
- South Africa
- Taiwan
- Turkey
- Ukraine
- Uruguay
- Uzbekistan
- Vietnam
- Zambia

## Next steps

- Learn how [a consumer can call a business](https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/consumer2biz) .
- Learn how [a business can call a consumer](https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/biz2consumer) .
- Learn how to [make a video call](https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/videocalling) .
