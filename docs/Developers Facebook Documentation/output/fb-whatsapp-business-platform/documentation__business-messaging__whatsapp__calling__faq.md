# FAQs | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/faq_

---

# FAQs

Updated: Nov 13, 2025

## Product FAQ

Will calls show up in the insights page on Meta WhatsApp Manager UI?

Call insights will be available in both WhatsApp Manager and the [analytics API](https://developers.facebook.com/documentation/business-messaging/whatsapp/analytics).

Are International calls supported like WhatsApp consumer to consumer calls?

Yes.

What are the countries supported for calling?

See [Calling Availability](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling#availability) for more info.

Can I use toll-free numbers for calling?

Yes, as long as the country code for the toll-free number is in the list of supported countries. See [1-800 and toll free numbers](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers#1-800-and-toll-free-numbers) for details on how to register toll-free numbers on Cloud API.

What is the max number of concurrent calls that a single Cloud API account phone number can receive?

Max concurrent calls is 1000. When the rate limit is exceeded, the caller (the WhatsApp user) will get a generic message saying call cannot be placed. No message is played and there is no webhook. This limit is expected to increase and hence chances of this happening are low. Note that the rate limits for messaging API and template creation/update API are separate and unrelated to calling limits.

What is the role of BSP vs. end business in overall call flow?

- The BSP offers value-added services (for example contact center, voice recording, transcription, and so on) on top of the raw audio stream provided by Cloud API Calling.
- The webhook is sent to apps subscribed for the new `calls` subscription field. In typical cases, a BSP uses their own app and receives the call webhook followed by call establishment.
- How the end-business participates in the call is determined by the BSP.

Is the voice infrastructure/API for WhatsApp the same for Facebook Messenger?

WhatsApp Calling API is the first public voice API by Meta. Meta may reuse the same API and integration model for other Meta products when and if they offer voice solutions.

What is the maximum call duration supported?

There is no call duration limit.

Is SIP supported?

Yes, see [“Configure and use call signalling via session initiation protocol (SIP)”](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/sip)

Can I send/receive text/media messages while a call is in progress?

Yes. The [Messages API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api) can be used while a call is in progress.

Does Meta offer services such as voice recording, transcript, voice-mail?

No.

Can I add metadata (for example context) as part of accepting the call?

Yes. See [biz_opaque_callback_data field in the main API spec](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/reference#initiate-call). Also the existing conversation state provides important context to the business human agent. The call routing subsystem should directly connect the call from WhatsApp consumer to the right agent on the business side. This gives the best customer experience and avoids going through standard IVR

How can I raise awareness of the calling feature to WhatsApp users?

- Send messages with voice call buttons. See [send interactive message](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/call-button-messages-deep-links#send-interactive-message-with-a-whatsapp-call-button) and [send template message](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/call-button-messages-deep-links#create-and-send-whatsapp-call-button-template-message) sections for details
- Send a message with a voice call button automatically when a WhatsApp consumer opens a chat with the business account for the first time. See [welcome message](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/conversational-components#welcome-messages) for more details.
- [Link to a WhatsApp call from a website using deeplinks.](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/call-button-messages-deep-links#calling-deep-links)

Is it possible for an AI (for example voicebot) to have a conversation with a customer directly via a WhatsApp call?

Yes. Meta only provides the raw media stream and how it is processed is entirely flexible. Many businesses use automated voicebots including AI bots to answer calls from WhatsApp users. Many AI products in the market offer RTC / Speech APIs and some even have native WebRTC support. The integration approach is similar to integrating WhatsApp Business Calling with call centers for IVR or human agents.

See [WhatsApp Business Solution Terms](https://www.whatsapp.com/legal/business-solution-terms) for restrictions in AI use cases.

Why is

pre-accepting

user initiated call starting the timer on WhatsApp user side?

Likely because media is being sent before the call is [accepted](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/user-initiated-calls#accept-call). WhatsApp clients treat a call as accepted by peer if they receive a media packet or an accept signal whichever comes first.

If the timing of media start cannot be controlled, directly [accept](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/user-initiated-calls#accept-call) the call and do not use [pre-accept](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/user-initiated-calls#pre-accept-call). The pre-accept is meant to frontload media connection establishment but it does require controlling the timing of media transmission.

Is there a status page to track overall health of Calling APIs and view any outages or service incidents?

Yes. See [Cloud API Calling on Meta status page](https://metastatus.com/whatsapp-business-api#cloud-api-calling) and [incident history](https://metastatus.com/whatsapp-business-api/history)

## Getting Started FAQ

What is the minimum Graph API version for the Calling API?

It is v17.0. [See here for general version history](https://developers.facebook.com/docs/graph-api/changelog)

Can I use the same user access token for messaging, for calling?

Yes. Whatever works for messaging should work for calling in general.

Does the WABA need to have an attached credit line for using Calling APIs?

Yes, a credit line attached to the WABA is required in order to use the Calling API.

Does the WABA need to be a verified business for calling?

No. [Business verification](https://www.facebook.com/business/help/2058515294227817?**id=180505742745347) is not a requirement for calling, nor is it required for messaging

How does usage of Calling APIs affect my rate limits?

Calling API usage does not count towards messaging rate limits at the moment. The only limit enforced for calling right now is the 1000 concurrent calls limit, but this may change in near future.

Is it possible for a WhatsApp Business account be connected to Provider A for Chat and to Provider B for Voice (i.e., two different apps subscribed to the same WhatsApp business Webhook account/phone)?

Yes, it is possible for two partners to operate a single WhatsApp Business API phone number with two separate solutions, like chat and calling.

[See Multi-Solution Conversations for more details](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/multi-solution-conversations).

Another option is for the voice provider used by another BSP. In this case a Meta app or being a tech provider on Meta is not needed. This architecture is depicted in detail in the section [“Integrating using a third party voice provider”](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/integration-patterns#integrating-using-a-third-party-voice-provider-detailed-design).

## Graph API Call Signaling FAQ

Does Meta provide any stun/turn servers or WebRTC infra for use by BSP?

No.

Meta uses [ICE-lite](https://datatracker.ietf.org/doc/html/rfc8445#autoid-21) and the Meta SDP offer always has a single ipv4 and ipv6 address per data stream component. The SDP answer should follow the same format.

As such it is not mandatory to use STUN/TURN to determine the ICE candidates

Does Meta recommend any stun/turn servers or WebRTC infra for use by BSP?

Meta doesn’t have recommendations. Here are a few ideas just as food for thought in case they are helpful.

- Check for any existing VoIP related technology and if so, consult that team. WebRTC relies on SRTP/SRTCP for actual media which is the VoIP media standard.
- Using STUN/TURN works well in an end user setup with a browser from a personal device. If the integration with the Meta voice APIs involves terminating the media directly on an end user device, the STUN/TURN, and so on, happen directly on that user device. But often, the media does terminate in a partner’s own infra so services like IVR can be offered. In such cases, the BSP infra may have its own ways to allocate an IP and port for VoIP connections, for example using VIP behind a load-balancer, and so on.

What ICE role should the ICE agent on the business side take?

Always take the CONTROLLING role as the Meta side ICE agent uses ICE-lite ([RFC 8445](https://datatracker.ietf.org/doc/html/rfc8445#autoid-21)). Starting with the CONTROLLED role may cause the ICE process to stall and timeout. Even if it does work, it will take more time due to multiple round-trips needed to resolve role conflicts.

Can more ICE candidates be added as part of signaling in offer + answer (for example using ICE Trickle)?

Short answer is yes. Cloud API uses [ICE-lite (RFC 8445)](https://datatracker.ietf.org/doc/html/rfc8445#autoid-21) and always assumes the controlled [role](https://datatracker.ietf.org/doc/html/rfc8445#autoid-26) in ICE. Hence there is no need to send updated candidates to Meta. The ICE Agent can initiate connectivity checks from addresses not included in the SDP and the Meta ICE agent will consider unknown address as a valid candidate, as long as STUN message integrity passes.

What is the recommendation on how to determine the ICE candidate?

Meta has global infra presence and Meta will choose the media relay on Meta infra that is closest to the WhatsApp user involved in the call.

On the BSP side, the media server/host (aka targeting) can be chosen based on many parameters including the IP Meta chooses, the country of consumer phone number, and the business phone number. The selection of media server location is an important factor in optimizing the media latency between BSP IP and Meta IP which in turn contributes to higher call quality. At the minimum, the BSP call/media hosting location should be close to the country of the WhatsApp user as determined from the country code of the user’s phone number.

Any targeting implementation on the BSP side should optimize for the candidates IPs on the Meta SDPs and not on the source of signaling endpoints.

Is there an API to send a provisional response equivalent to SIP 180 Ringing?

If not, when does the caller’s device start ringing?

Caller (the WhatsApp Consumer app) would already be ringing by the time the webhook is received. There is no need for provisional responses

How are the calls secured?

Cloud API uses SRTP for the encryption of media streams [(RTP/SAVPF)](https://datatracker.ietf.org/doc/html/rfc5124) and the actual SRTP key exchange is initially performed end-to-end with [DTLS-SRTP](https://datatracker.ietf.org/doc/html/rfc5764).

Can Meta send the call webhooks to a different endpoint based on the caller’s geographical location or other factors such as network latency?

The webhook URL is configurable. HTTPS is used, so standard load balancing and targeting techniques can be applied to reroute accordingly. A different (aka override or alternate) webhook URL can also be configured per [WhatsApp Business Account](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/manage-webhooks#overriding-the-callback-url) and per [business phone number](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/override#set-phone-number-alternate-callback). The webhook is only used for signaling and Meta servers calling the webhook server are located in US. Select the location of the media endpoint based on the country code of the WhatsApp consumer (available on the webhooks) or the ice candidate IPs on SDP sent by Meta. See the above FAQ questions **“What is the recommendation on how to determine the ICE candidate?**” and **“How to reduce media latency of the calls?”** .

What are the Meta IP addresses that will call the Webhook or SIP or Media servers in order to allowlist them in a firewall?

Refer to [the WhatsApp Webhooks documentation](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/overview#ip-addresses) on this topic. When collapsing the list of IPv4 addresses the result is around 23 prefixes. See below for an example command and output that was run as of December 11, 2024.

```
$ src % whois -h whois.radb.net — '-i origin AS32934' | grep ^route | awk '{print $2}' | grep -iv ':' | cidrmerge
31.13.24.0/21
31.13.64.0/18
45.64.40.0/22
57.141.0.0/21
57.141.8.0/22
57.141.12.0/23
57.144.0.0/14
66.220.144.0/20
69.63.176.0/20
69.171.224.0/19
74.119.76.0/22
102.132.96.0/20
103.4.96.0/22
129.134.0.0/16
147.75.208.0/20
157.240.0.0/16
163.70.128.0/17
163.77.128.0/17
173.252.64.0/18
179.60.192.0/22
185.60.216.0/22
185.89.216.0/22
204.15.20.0/22
```

Is it possible to reduce the Meta IP addresses that will call webhook servers at-least for dev-test purposes?

No. But see the above FAQ which deduced about 23 IPv4 prefixes to completely cover all Meta address space for v4.

What is the retry policy for calling related webhooks?

Do not assume anything in this regard. The webhook server should determine stale webhooks based on timestamp value and avoid calling Graph APIs to further process them. Existing messaging related [webhooks are retried for up to 7 days](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/overview#webhook-delivery-failure).

Calling related webhooks will likely have a shorter retry policy but stale webhooks may still be delivered as that may be useful information to a business to know that some consumers tried to reach them.

Does Meta guarantee exactly one delivery for webhooks?

No. Be prepared to handle duplicate webhooks.

Due to the distributed nature of Meta’s architecture, exactly-once delivery cannot be guaranteed for any webhooks including even messaging related webhooks. Following are some known scenarios where duplicates can occur today.

1. The Meta HTTPS request to the webhook server timed out after ~20s. In this case, the server thinks it successfully handled a webhook request but from Meta’s side, it failed due to timeout. Meta retries sending this webhook, which then appears as a duplicate.
2. If the phone number has more than 1 app subscribed to the calls field and Meta dispatches webhooks to app1 and app2 in that order. If app2 fails, Meta will retry the whole dispatch so app1 will receive a duplicate webhook. Meta is in the process of fixing this.
3. Failure recovery on Meta queueing infrastructure may result in duplicate webhook sends.
4. There could be other reasons that are currently unknown.

Do you guarantee ordering of webhooks for a given call?

No. Ordering is not guaranteed due to the distributed nature of Meta’s architecture and retries.

For example the terminate webhook can arrive before the connect webhook if the WhatsApp user hangs up the call immediately after initiating it. Following are other known examples.

The connect webhook is attempted which fails with timeout after ~20s. The ‘terminate webhook’ is sent next. The retry of connect webhook happens after the ‘terminate webhook’. In case of timeout, the webhook server thinks there is no failure but this is seen as failure that warrants a retry.

Can I configure multiple webhook servers for calling and have a notion of primary and secondary for high availability?

Similar to messaging, multiple subscriptions with distinct apps associated with distinct callback URLs can be configured. Meta will dispatch all calling webhooks to all configured callback URLs. All URLs are treated as equal and there is no notion of primary/secondary

Can I configure different URLs for messaging and calling related webhooks?

Yes, this can be done by having 2 different Meta apps - one for messaging and one for calling.

Subscribe the messaging app only to message related webhook subscription fields and the calling app to the calling related subscription fields. The callback URL can be overridden for each of these apps at WABA or phone number level to have different URL override for messages and calls.

However a single app can also subscribe to both `messages` and `calls` Webhook subscription fields. In this setup, the callback URI is same for both messages and calls related webhooks but the webhook payload can be used to distinguish between the two categories of webhooks.

In general, using a single app is recommended.

Can you share sample curl request for interacting with APIs?

Please view the [Sample CURL request section](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/reference#sample-curl-requests) in the API reference.

How should the SDP params be serialized with carriage returns and a new line?

The session param requires the SDP to be set as a string per the [RFC-8866](https://datatracker.ietf.org/doc/html/rfc8866) specification which requires CRLF to be used to end a record. Sdp param itself is a string so it should not be further serialized. The legacy connection param however required the [RFC-8866](https://datatracker.ietf.org/doc/html/rfc8866) compliant SDP string to be within a JSON structure and hence required further serialization.

In short, use “\r\n” for session->SDP param. **Do not use the legacy connection->WebRTC->SDP param.**

How do I fix error ‘No fingerprint found in SDP’?

The SDP should have an `a=fingerprint` line when using [DTLS](https://datatracker.ietf.org/doc/html/rfc6347) as the [SRTP](https://datatracker.ietf.org/doc/html/rfc3711) key exchange protocol. Make sure to add that line or [configure the business phone number to use SDES](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/sip#configure-sdes-for-srtp-key-exchange-protocol) instead. See all the possible [Signaling and media possible configurations](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/sip#signaling-and-media-possible-configurations).

## WebRTC and media FAQ

Is the peer to peer connection from Meta to BSP or end business?

Typically it is the BSP but depending on the product offering and architecture it could be end business.

If it is the end business, the BSP would need to programmatically interact with them to obtain the ICE candidates included in the Graph API call to accept the incoming call.

What happens if the media stops flowing from one end due to connection issues?

A simple example would be if the [terminate call endpoint fails](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/reference#terminate-call) but the business side stops sending media.

This will lead to lack of RTCP packets which helps detect inactive WebRTC agent and the call will disconnect followed by a [terminate webhook](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/reference#call-terminate-webhook).

Is the codec always opus/48000?

We also support G.711 (PCMA and PCMU). For opus, the RTP clock rate is set at 48000 in SDP as per [RFC 7587](https://datatracker.ietf.org/doc/html/rfc7587#autoid-17). WhatsApp mobile apps only support opus natively, so Meta media infra transcodes opus to other codecs if needed.

What else is supported in terms of codecs?

Audio codecs supported: OPUS, PCMA, PCMU (aka G.711)

Is DTMF supported?

Yes. See the [DTMF section for details](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/user-initiated-calls#dual-tone-multi-frequency--dtmf--support). Most SIP implementations should support processing DTMF coming through the RTP data stream ([reference](https://voipnuggets.com/2023/06/12/different-types-of-dtmf-in-sip-and-why-dtmf-via-rfc2833-is-more-reliable/)).

How many streams are supported in the SDP?

Only one stream is supported in the Offer/Answer SDP.

How many tracks are supported in each SDP stream?

Only one audio track is supported in the SDP stream.

For a consumer to business call, can WhatsApp consumer apps work with an SDP offer generated by a business agent’s browser?

In this case, the WebRTC agent within the browser should generate an SDP answer, not an offer.

This SDP answer should be supplied back to Meta using the [accept call endpoint](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/reference#accept-call). Meta cannot work with any other SDP offer than the one it generated and supplied on the webhook.

What certificate algorithm is recommended for DTLS?

ECDSA certificates are recommended as they lead to faster cert generation and shorter DTLS handshakes due to [lack of fragmentation](https://datatracker.ietf.org/doc/html/rfc6347#autoid-26).

Who would initiate the calls after accepting the user-initiated call - The BSP or Meta?

The BSP should initiate the ICE connectivity checks as soon as the BSP decides to accept the call.

This can be done even before calling the accept API but the ICE process will only converge after Meta processes the SDP answer, due to the need for DTLS certificate fingerprint.

What are the port numbers used by ICE candidates on Meta’s SDP for allowlisting on firewalls?

Port numbers can be any one from `40012`, `3482`, `3484`, `3478`, `3480`. These are subject to change.

How can I generate the WebRTC Accept SDP?

Consult the documentation of the WebRTC library or tool planned for use.

Processing an SDP offer to generate an SDP answer is the primary functionality of any VoIP technology stack.

How to reduce media latency of the calls?

Meta’s targeting algorithms will choose the Meta relay that receives media from BSP close to the WhatsApp consumer’s location. This media relay is the ice candidate Meta will share in the SDP. Any BSP side targeting should place the BSP media servers in the same region as the consumer. This obviously minimizes latency for calls within the same region, but it will minimize the media packet routes on public internet for international calls.

Is there a process of reconnection if there is a temporary network drop on either end of the media leg?

WhatsApp consumer apps will attempt a reconnect and automatically recover that leg of the call once network connectivity is restored.

For the business leg, relatively more stable network conditions are expected. At this time there is no support to re-handshake or re-negotiate SDPs. In any case, the call can terminate after a certain duration of inactivity, after which a terminate webhook is sent.

How much bandwidth would be required for the call center to support a given number of concurrent calls?

Per call, roughly 40kbps is needed for codec + 20 kbps overhead

The Opus codec has the ability to dynamically change bandwidth consumed based on network conditions. In general it can offer better audio quality with lower bandwidth consumption, compared to G711 codec.

G711 codec in comparison needs 64 kbps for codec + 20 kbps overhead = 84 kbps per call.

Multiply the above numbers with the expected number of concurrent calls to calculate the cumulative bandwidth required. Example: A 1mbps bandwidth can roughly handle 15 concurrent calls on opus (1000/64) vs. 12 concurrent calls on G711 (1000/84).

To calculate the total data usage, multiply the bandwidth with call duration in seconds. For Opus, it’s a bit more tricky because it has variable bandwidth depending on many factors including available bandwidth estimated using bandwidth estimation, whether local party is talking or silent, and so on. But roughly, a 1 min call on Opus consumes 3.75MB of data vs. the same on G711 takes 4.9MB of data

Is it possible to handover / transfer a call from one agent to another during an active call session? In essence, a customer is speaking with Agent A and needs to be transferred to Agent B?

Meta doesn’t have any native support.

Meta is unaware of different agents on the business / partner side, so this is an operation that is doable solely on the partner side. For example, the media flow can be Meta media server to Partner media server to Agent A. When transfer happens, the flow becomes Meta media server to Partner media server to Agent B. So in the both cases, the leg from Meta media server to Partner media server remains constant.

## WhatsApp Consumer Client FAQ

When is the call icon in the chat title bar visible on WhatsApp Consumer apps?

It is visible when **all the following conditions are met:**

- The business phone number has the calling status set to `ENABLED` in the [Call Settings API](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/call-settings) .
- Business phone number `call_icon_visibility` is not `HIDE_IN_CHAT` and not `DISABLE_ALL`
- The call icon visibility feature is supported in WhatsApp mobile versions 2.24.10.8 and above on Android and iOS.
- Consumer’s WhatsApp version 2.23.14 or above. All consumers are expected to be on this version or above.

[View the Call Settings API to learn more](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/call-settings)

Why is the call icon in the WhatsApp Consumer app not reflecting the current call settings?

After call configuration is updated, WhatsApp users may take up to 7 days to reflect that configuration although most users refresh much sooner. An immediate refresh in WhatsApp can be forced by entering the chat window with the business and opening the chat info page. Regardless of WhatsApp client behavior, the semantics of settings are still honored on the server side.

Troubleshoot the call icon not showing using the following steps:

- Navigate to the chat window for the business and click on the business name or number in the chat title bar. This opens the Business Info screen and forces the app to refresh calling state for the business.
- Navigate out of the chat window for the business and re-enter.
- If the expected state is still not visible, kill the WhatsApp app and restart it.
- Make sure to [get call settings](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/call-settings) to double confirm expected call settings.

How long does it take for WhatsApp clients to reflect changes to calling configuration?

It can take up to 7 days although most WhatsApp users should reflect the changes much sooner.

One WhatsApp Business can have chats with any number of 3B+ WhatsApp users. Updates to calling settings sends change notifications to all users that have a chat with this business visible in their WhatsApp Inbox. However notification delivery is best effort so not all users may receive it.

All WhatsApp clients refresh the business information (including calling configuration) every 7 days regardless of getting any change notifications.

In either case (notification driven or 7d refresh), once the local state in WhatsApp client is refreshed, it is reflected in UI only on next enter of the chat screen or chat info screen.

Must I create an allowlist of consumer numbers for calling to work?

No.

Is it possible to limit calling access to specific or individual WhatsApp users instead of all WhatsApp users?

Example: a lead that’s qualified or a customer who is in premium tier

No. There is no way to control visibility or access of calling on an individual WhatsApp user basis. However the [Call Settings API](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/call-settings) can be used to set `call_icon_visibility` to `DISABLE_ALL` which will hide call icons to all WhatsApp users. For qualified WhatsApp users, a message with the call CTA button can be sent so only they can call the business by tapping on the button in the message

Providing this type of feature would require Meta to store configuration per WhatsApp user which has higher privacy risk. It will also incur higher operational overhead to maintain large lists of allowlisted WhatsApp users on an ongoing basis.

When the call icon is hidden using Call Settings API, is it still possible for consumers to call the business?

Yes.

A user can still call the business from other entry points which are unaffected by the [Call Settings API](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/call-settings) such as:

- Save the business number as a contact and use new call
- Call logs from Calls tab > Recent
- Call CTA in messages sent from the business
- Call bubble in the chat window that appears following any call between user and business

Hence the recommendation is to treat `DISABLE_ALL` only as a broad first level filter and ensure webhooks do any additional filtering based on specific business logic.

How will WhatsApp consumers type digits for DTMF?

WhatsApp consumer apps are extended to support a new keypad for business calls.

[Learn more about DTMF support in Calling API](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/user-initiated-calls#dual-tone-multi-frequency--dtmf--support)

What is the min version of WhatsApp mobile apps that support the voice call button?

- Min app version for Android is 2.24.1

What is the experience on the WhatsApp consumer side at various points in the call setup flow?

When a WhatsApp consumer calls a business, the local ringback tone starts immediately if the WhatsApp consumer device has internet connectivity.

The call UI shows ‘Calling BUSINESS_NAME’. When Cloud API receives the consumer call request and pre-accepts the call, the call UI changes to ‘Ringing BUSINESS_NAME’. After the accept Graph API call is made, the call UI changes to an active call window showing live timer for the call duration.

Is calling supported for end users from WhatsApp Web or WhatsApp Desktop apps?

No. WhatsApp Web does not support consumer-v-consumer or business calls. Desktop apps support only consumer-v-consumer calls at this point.

## Business Initiated Calling FAQ

What WhatsApp versions and client platforms support the business initiated calling feature?

WhatsApp Client versions 2.24.14.x and later support the call permission requests and business initiated calling feature.

Both WhatsApp Android and iOS platforms support the feature.

How to avoid 138011 in Business Initiated and user initiated conversation while dev/integration/testing?

User Initiated conversation:

- Send a message to the Cloud API number from the WhatsApp consumer account
- Send any message apart from the call permission message to the user
- Send a call permission request to the user
- Accept the call permission requests on the user’s device

Business Initiated conversation:

- Send a template message to the user from the business
- Send the call permission request to the user
- Accept the call permission requests on the user’s device

Is there a way to reset the call permission request limits?

A connected call will reset the call permission limits.

What happens if the WhatsApp user has set up Silence Unknown Callers settings?

Business initiated calls bypass ‘Silence Unknown Callers’ settings since the call can only happen after explicit permission provided by the user.

Why is my Call Permission Request message rendered differently?

WhatsApp’s renders messages on unsupported client app versions differently than supported ones.

After the WhatsApp user updates their client app, it will be rendered correctly.

I received error 138001 after sending a Call Permission Request, what do I do?

[Please view error codes in the troubleshooting page](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/troubleshooting)

Does the permission expire after 24 hour connected calls limit is reached? I am seeing error

138012

.

Limit on connected calls in 24 hours is a time window based running limit. Reaching that limit does not revoke the permission, permission remains open until the full 7 days for temporary allowed permissions or permanently for always allowed permissions. [Call Permissions API](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/user-call-permissions#get-current-call-permission-state) provides the exact timestamp when this limit is expires and next call can be made.

Think of this as a rate limit for business initiated calls.

## Session Initiation Protocol (SIP) FAQ

See [SIP Errors](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/troubleshooting#sip-errors) for SIP specific errors and possible solutions.

Why is user initiated call getting disconnected immediately after enabling SIP?

Most likely reason for this is certificate validation error: See [How to test if you have a valid TLS certificate](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/sip#how-to-test-if-you-have-a-valid-tls-certificate)

Why am I not getting SIP requests (INVITE, BYE, etc.) when expected?

If you are not getting SIP INVITE following a user initiated call or a SIP BYE following a user initiated call termination, possible reasons include

- TLS certificate validation error: See [How to test if you have a valid TLS certificate](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/sip#how-to-test-if-you-have-a-valid-tls-certificate)
- SIP is not configured. [Fetch calling configuration](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/sip#get-phone-number-calling-settings--sip-) to make sure SIP is enabled
- The app that configured the SIP server does not have `whatsapp_business_messaging` permission on the business phone number. Try to [send a message](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api) using the same business phone number as a way to verify the right permissions are in place.
- Network connectivity issue: Your SIP server may not be reachable from Meta on the port you configured for SIP. You can verify basic TCP connectivity to your SIP server by running the following command:

```bash
nc -zvw2 -G 2 <your-sip-server> <your-sip-port>
```

Replace `<your-sip-server>` with your SIP server hostname and `<your-sip-port>` with the port configured on your SIP server.

**Example: Failure (connection timed out)**

```bash
$ nc -zvw2 -G 2 your-sip-server.example.com 5061
nc: connectx to your-sip-server.example.com port 5061 (tcp) failed: Operation timed out
```

**Example: Success (port is reachable)**

```bash
$ nc -zvw2 -G 2 your-sip-server.example.com 5061
Connection to your-sip-server.example.com port 5061 [tcp/sip-tls] succeeded!
```

If the connection times out or is refused, check your firewall rules and ensure that the configured port is open and your SIP server is listening on it. Also verify that [Meta’s IP addresses](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/sip#ip-addresses) are allowlisted in your firewall.

Why is our SIP TERMINATE to Meta is not hanging up on WhatsApp user side?

Common reason is TLS handshake failure when the SIP server is trying to establish a TLS session with Meta SIP server. Do a network packet capture of SIP traffic or check the SIP server logs to confirm successful TLS handshake

Why is my SIP server continuously responding with 401 Unauthorized for user initiated calls?

Meta supports SIP digest auth for [user initiated calls](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/sip#user-initiated-calls). When the SIP server responds with 401 Unauthorized (see [example flow](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/sip#user-initiated-calls-with-digest-auth--with-sdes-media-)), Meta SIP server will resend the INVITE with proper Authorization header. Make sure the SIP server is configured with username as the business phone number and password as the Meta generated password for the business phone number.

Alternatively, digest auth can be disabled on the SIP server, although this is NOT recommended from a security best practices point of view.

Why is my SIP server responding with 488 Not Acceptable Here?

Consult the SIP server documentation or vendor. The likely reason is the SIP server does not support WebRTC ICE (Interactive Connectivity Establishment) protocol. To fix this, [configure the business phone number to use SDES](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/sip#configure-sdes-for-srtp-key-exchange-protocol) instead.

Is it required to SIP REGISTER business phone number to Meta SIP server?

No. Do not send REGISTER requests to Meta’s SIP server. Doing so is unnecessary resource consumption on both sides. REGISTER requests will fail with 403 Forbidden error. As such Meta’s SIP server owns only meta.vc domain and the only SIP users in that domain are regular WhatsApp consumer users. The WhatsApp Business Numbers belong to the SIP domain configured using the [settings API](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/sip#configure-update-sip-settings-on-business-phone-number).

Does Meta support SIP re-INVITEs?

No. Re-INVITES are not supported today. A 500 Internal Server Error is returned from Meta SIP server.

Is SIP calling as good as the Cloud Graph API/webhook option? Any reason to pick one over the other?

Yes, there is functional parity between the two options. The best way to identify the best option is to complete a thorough assessment and select based on needs.

If SIP is used for calling, are webhooks still needed?

SIP for calling only covers call specific events. For messaging or any non-call specific events, webhooks still need to be used.

Does Meta have a specific, approved list of vendors or SBCs for SIP?

No. Any compatible SIP server.
