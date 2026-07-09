# Business-Initiated Calls | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/business-initiated-calls_

---

# Business-Initiated Calls

Updated: Nov 13, 2025

## Overview

The Calling API supports making calls to WhatsApp users from your business.

The user dictates when calls can be received by [granting call permissions to the business phone number](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/user-call-permissions).

### Call sequence diagram

![Business-initiated call sequence diagram showing flow between business, Cloud API, and WhatsApp user](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/561795972_1339317917926859_882777793042649890_n.jpg?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=Wg0d6fC6HoAQ7kNvwG_heKp&_nc_oc=AdpiBTCgOf7k8qwU6dJYo28z9OLbNHA9mHfkQ_i1Dxip7lRQCJLkpAt-7VgvjZ0DCJI&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=4bCUQcOwhEm-59shOzr0eg&_nc_ss=7b20f&oh=00_Af7OaYxnSS41oOxPhGuMspwTIWGm_P6sZwz9UM2c0H_0Mg&oe=6A1C2E0D)

*Note: The `ACCEPTED` call status webhook will typically arrive after the call has been established. The Cloud API primarily sends it for call event auditing.*

## Prerequisites

Before you get started with business-initiated calling, ensure that:

- [Subscribe](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/create-webhook-endpoint#configure-webhooks) to the “calls” webhook field
- [Calling APIs are enabled on your business phone number](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/call-settings)

Lastly, **before you can call a WhatsApp user, you must obtain their permission to do so.**

[Learn how to obtain WhatsApp user calling permissions here](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/user-call-permissions)

## Business-initiated calling flow

### Part 1: Obtain permission to call the WhatsApp user

You can obtain call permissions from the WhatsApp user in one of the following ways:

Send a call permission request message

You can request call permissions by sending the WhatsApp user a permission request. Send it as a free form message during an open customer service window, or use a template message.

- [Learn how to send a **free form** call permission request](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/user-call-permissions#how-to-send-a-free-form-call-permission-request-message)
- [Learn how to send a **template** call permission request](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/user-call-permissions#how-to-create-and-send-call-permission-request-template-messages)

Enable

callback_permission_status

in call settings

When `callback_permission_status` is enabled, the user automatically provides call permission to your business when they place a call to you.

[Learn how to enable `callback_permission_status`](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/call-settings#configure-update-business-phone-number-calling-settings)

WhatsApp user grants permanent permissions

The user can also grant permanent permissions to the business at any time through their business profile.

### Part 2: Your business initiates a new call to the WhatsApp user

Now that you have user permission, you can initiate a new call to the WhatsApp user in question.

Use the [Calls API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/calling-api) with the following request body to initiate a new call:

```https
POST <PHONE_NUMBER_ID>/calls
{
  "messaging_product": "whatsapp",
  "to":"12185552828", // The WhatsApp user's phone number (callee)
  "action":"connect",
  "session" : {
      "sdp_type" : "offer",
      "sdp" : "<<RFC 8866 SDP>>"
  }
}
```

If there are no errors, you will receive a successful response:

```https
{
  "messaging_product": "whatsapp",
  "calls" : [
    { "id" : "wacid.HBgLMTIxODU1NTI4MjgVAgARGCAyODRQIAFRoA" } // The WhatsApp call ID
   ]
}
```

*Note: Response with error code `138006` indicates a lack of a call request permission for this business number from the WhatsApp user.*

### Part 3: You establish the call connection using webhook signaling

After you successfully initiate a new call, you receive a Call Connect webhook response containing an `SDP Answer` from Cloud API. Your business will then apply the `SDP Answer` from this webhook to your WebRTC stack to initiate the media connection.

```https
{
    "entry": [
        {
            "changes": [
                {
                    "field": "calls",
                    "value": {
                        "calls": [
                            {
                                "biz_opaque_callback_data": "TRx334DUDFTI4Mj", // Arbitrary string passed by business for tracking purposes
                                "session": {
                                    "sdp_type": "answer",
                                    "sdp": "<RFC 8866 SDP>"
                                },
                                "from": "13175551399", // The business phone number placing the call (caller)
                                "connection": {
                                    "webrtc": {
                                        "sdp": "<RFC 8866 SDP>"
                                    }
                                },
                                "id": "wacid.HBgLMTIxODU1NTI4MjgVAgARGCAyODRQIAFRoA", // The WhatsApp call ID
                                "to": "12185552828", // The WhatsApp user's phone number (callee)
                                "event": "connect",
                                "timestamp": "1749196895",
                                "direction": "BUSINESS_INITIATED"
                            }
                        ],
                        "metadata": { // ID and display number for the business phone number placing the call (caller)
                            "phone_number_id": "436666719526789",
                            "display_phone_number": "13175551399"
                        },
                        "messaging_product": "whatsapp"
                    }
                }
            ],
            "id": "366634483210360" // WhatsApp Business Account ID associated with the business phone number
        }
    ],
    "object": "whatsapp_business_account"
},
```

You then receive an appropriate status webhook, indicating that the call is `RINGING`, `ACCEPTED`, or `REJECTED`:

```https
{
  "entry": [
    {
      "changes": [
        {
          "field": "calls",
          "value": {
            "statuses": [
              {
                "id": "wacid.HBgLMTIxODU1NTI4MjgVAgARGCAyODRQIAFRoA", // The WhatsApp call ID
                "type": "call",
                "status": "[RINGING|ACCEPTED|REJECTED]", // The current call status
                "timestamp": "1749197000",
                "recipient_id": "12185552828" // The WhatsApp user's phone number (callee)
              }
            ],
            "metadata": { // ID and display number for the business phone number placing the call (caller)
              "phone_number_id": "436666719526789",
              "display_phone_number": "13175551399"
            },
            "messaging_product": "whatsapp"
          }
        }
      ],
      "id": "366634483210360" // WhatsApp Business Account ID associated with the business phone number
    }
  ],
  "object": "whatsapp_business_account"
}
```

### Part 4: Your business or the WhatsApp user terminates the call

Either you or the WhatsApp user can terminate the call at any time.

Use the [Calls API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/calling-api) with the following request body to terminate the call:

```curl
POST <PHONE_NUMBER_ID>/calls
{
  "messaging_product": "whatsapp",
  "call_id": "wacid.HBgLMTIxODU1NTI4MjgVAgARGCAyODRQIAFRoA", // The WhatsApp call ID
  "action" : "terminate"
}
```

If there are no errors, you will receive a success response:

```https
{
  "success" : true
}
```

When either the business or the WhatsApp user terminates the call, you receive a Call Terminate webhook:

```https
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "366634483210360", // WhatsApp Business Account ID associated with the business phone number
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": { // ID and display number for the business phone number placing the call (caller)
              "phone_number_id": "436666719526789",
              "display_phone_number": "13175551399",

            },
            "calls": [
              {
                "id": "wacid.HBgLMTIxODU1NTI4MjgVAgARGCAyODRQIAFRoA",
                "to": "12185552828", // The WhatsApp user's phone number (callee)
                "from": "13175551399", // The business phone number placing the call (caller)
                "event": "terminate",
                "direction": "BUSINESS_INITIATED",
                "timestamp": "1749197480",
                "status": ["Failed", "Completed"],
                "start_time": "1671644824", // Call start UNIX timestamp
                "end_time": "1671644944", // Call end UNIX timestamp
                "duration": 480 // Call duration in seconds
              }
            ]
          },
          "field": "calls"
        }
      ]
    }
  ]
}
```

## Endpoints for business-initiated calling

### Initiate call

Use this endpoint to initiate a call to a WhatsApp user by providing a phone number and a WebRTC call offer. There is a rate limit of 10000 per 24 hours for initiating new calls per business phone number.

Request syntax

```https
POST <PHONE_NUMBER_ID>/calls
```

| Placeholder | Description | Sample Value |
| --- | --- | --- |
| `<PHONE_NUMBER_ID>`<br>*Integer* | **Required**<br>ID of the business phone number from which you are initiating the new call. | `106540352242922` |

Request body

```https
{
  "messaging_product": "whatsapp",
  "to": "14085551234",
  "action": "connect",
  "session": {
    "sdp_type": "offer",
    "sdp": "<<RFC 8866 SDP>>"
  },
  "biz_opaque_callback_data": "0fS5cePMok"
}
```

Body parameters

| Parameter | Description | Sample Value |
| --- | --- | --- |
| `to`<br>*Integer* | **Required**<br>The number being called (callee)<br>[Learn more about formatting phone numbers in Cloud API](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers) | `“17863476655”` |
| `action`<br>*String* | **Required**<br>The action being taken on the given call ID.<br>Values can be `connect` \| `pre_accept` \| `accept` \| `reject` \| `terminate` | `“connect”` |
| `session`<br>*JSON object* | **Optional**<br>Contains the session description protocol (SDP) type and description language.<br>Requires two values:<br>`sdp_type` — (*String*) **Required**<br>“offer”, to indicate SDP offer<br>`sdp` — (*String*) **Required**<br>The SDP info of the device on the other end of the call. The SDP must be compliant with [RFC 8866](https://datatracker.ietf.org/doc/html/rfc8866).<br>[Learn more about Session Description Protocol (SDP)](https://www.rfc-editor.org/rfc/rfc8866.html)<br>[View example SDP structures](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/reference#sdp-overview-and-sample-sdp-structures) | `"session" :<br>{<br>"sdp_type" : "offer",<br>"sdp" : "<<RFC 8866 SDP>>"<br>}` |
| `biz_opaque_callback_data`<br>*String* | **Optional**<br>An arbitrary string you can pass in that is useful for tracking and logging purposes.<br>Any app subscribed to the “calls” webhook field on your WhatsApp Business Account can receive this string, as it is included in the `calls` object within the subsequent [Call Terminate Webhook](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/business-initiated-calls#call-terminate-webhook) payload.<br>Cloud API does not process this field.<br>Maximum 512 characters | `“0fS5cePMok”` |

Success response

```https
{
  "messaging_product": "whatsapp",
  "calls" : [{
     "id" : "wacid.ABGGFjFVU2AfAgo6V",
   }]
}
```

Error response

Possible errors that can occur:

- Invalid `phone-number-id`
- Permissions/Authorization errors
- Request format validation errors, for example connection info, sdp, ice
- SDP validation errors
- Calling restriction errors

[View Calling API Error Codes and Troubleshooting for more information](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/troubleshooting)

[View general Cloud API Error Codes here](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/error-codes)

### Terminate call

Use this endpoint to terminate an active call.

This must be done even if there is an `RTCP BYE` packet in the media path. Ending the call this way also ensures pricing is more accurate.

When the WhatsApp user terminates the call, you do not have to call this endpoint. Once the call is successfully terminated, you will receive a [Call Terminate Webhook](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/business-initiated-calls#call-terminate-webhook).

Request syntax

```https
POST <PHONE_NUMBER_ID>/calls
```

| Parameter | Description | Sample Value |
| --- | --- | --- |
| `<PHONE_NUMBER_ID>`<br>*Integer* | **Required**<br>The business phone number which you are terminating a call from.<br>[Learn more about formatting phone numbers in Cloud API](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers) | `18274459827` |

Request body

```https
{
  "messaging_product": "whatsapp",
  "call_id": "wacid.ABGGFjFVU2AfAgo6V-Hc5eCgK5Gh",
  "action": "terminate"
}
```

Body parameters

| Parameter | Description | Sample Value |
| --- | --- | --- |
| `call_id`<br>*String* | **Required**<br>The ID of the phone call.<br>For inbound calls, you receive a call ID from the [Call Connect webhook](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/business-initiated-calls#call-connect-webhook) when a WhatsApp user initiates the call. | `“wacid.ABGGFjFVU2AfAgo6V-Hc5eCgK5Gh”` |
| `action`<br>*String* | **Required**<br>The action being taken on the given call ID.<br>Values can be `connect` \| `pre_accept` \| `accept` \| `reject` \| `terminate` | `“terminate”` |

Success response

```https
{
  "messaging_product": "whatsapp",
  "success" : true
}
```

Error response

Possible errors that can occur:

- Invalid `call id`
- Invalid `phone-number-id`
- The WhatsApp user has already terminated the call
- Reject call is already in progress
- Permissions/Authorization errors

[View Calling API Error Codes and Troubleshooting for more information](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/troubleshooting)

[View general Cloud API Error Codes here](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/error-codes)

## Webhooks for business-initiated calling

With all Calling API webhooks, there is a `”calls”` object inside the `”value”` object of the webhook response. The `”calls”` object contains metadata about the call that is used to action on each call placed or received by your business.

To receive Calling API webhooks, subscribe to the “calls” webhook field.

[Learn more about Cloud API webhooks here](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/status)

### Call connect webhook

You receive a webhook notification in near real-time when a call initiated by your business is ready to connect to the WhatsApp user (an `SDP Answer`).

Critically, the webhook contains information required to establish a call connection via WebRTC.

Once you receive the Call Connect webhook, you can apply the `SDP Answer` received in the webhook to your WebRTC stack to initiate the media connection.

```https
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "<WHATSAPP_BUSINESS_ACCOUNT_ID>",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "16315553601",
              "phone_number_id": "<PHONE_NUMBER_ID>"
            },
            "contacts": [
              {
                "wa_id": "16315553602"
              }
            ],
            "calls": [
              {
                "id": "wacid.ABGGFjFVU2AfAgo6V-Hc5eCgK5Gh",
                "to": "16315553601",
                "from": "16315553602",
                "event": "connect",
                "timestamp": "1671644824",
                "direction": "BUSINESS_INITIATED",
                "session": {
                  "sdp_type": "answer",
                  "sdp": "<<RFC 8866 SDP>>"
                }
              }
            ]
          },
          "field": "calls"
        }
      ]
    }
  ]
}
```

Webhook values for

"calls"

| Placeholder | Description |
| --- | --- |
| `id`<br>*String* | A unique ID for the call |
| `to`<br>*Integer* | The number being called (callee) |
| `from`<br>*Integer* | The number of the caller |
| `event`<br>*Integer* | The calling event that this webhook is notifying the subscriber of |
| `timestamp`<br>*Integer* | The UNIX timestamp of the webhook event |
| `direction`<br>*String* | The direction of the call being made.<br>Can contain either:<br>`BUSINESS_INITIATED`, for calls initiated by your business.<br>`USER_INITIATED`, for calls initiated by a WhatsApp user. |
| `session`<br>*JSON object* | **Optional**<br>Contains the session description protocol (SDP) type and description language.<br>Requires two values:<br>`sdp_type` — (*String*) **Required**<br>“offer”, to indicate SDP offer<br>`sdp` — (*String*) **Required**<br>The SDP info of the device on the other end of the call. The SDP must be compliant with [RFC 8866](https://datatracker.ietf.org/doc/html/rfc8866).<br>[Learn more about Session Description Protocol (SDP)](https://www.rfc-editor.org/rfc/rfc8866.html)<br>[View example SDP structures](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/reference#sdp-overview-and-sample-sdp-structures) |
| `contacts`<br>*JSON object* | `wa_id` — The WhatsApp ID of the callee. |

### Call status webhook

This webhook is sent during the following calling events:

1. Ringing: When the WhatsApp user’s client device begins ringing
2. Accepted: When the WhatsApp user accepts the call
3. Rejected: When the WhatsApp user rejects the call. You also receive the call terminate webhook in this case

The webhook structure here is similar to the Status webhooks used for the Cloud API messages.

```https
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "<WHATSAPP_BUSINESS_ACCOUNT_ID>",
      "changes": [
        {
          "value": {
              "messaging_product": "whatsapp",
              "metadata": {
                   "display_phone_number": "16315553601",
                   "phone_number_id": "<PHONE_NUMBER_ID>",
              },
              "statuses": [{
                    "id": "wacid.ABGGFjFVU2AfAgo6V",
                    "timestamp": "1671644824",
                    "type": "call"
                    "status": "[RINGING|ACCEPTED|REJECTED]",
                    "recipient_id": "163155536021",
                    "biz_opaque_callback_data": "random_string",
               }]
          },
          "field": "calls"
        }
      ]
    }
  ]
}
```

[*Learn more about Cloud API status webhooks*](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/status)

Webhook values for

"statuses"

| Placeholder | Description |
| --- | --- |
| `id`<br>*String* | A unique ID for the call |
| `timestamp`<br>*Integer* | The UNIX timestamp of the webhook event |
| `recipient_id`<br>*Integer* | The phone number of the WhatsApp user receiving the call |
| `status`<br>*Integer* | The current call status.<br>Possible values:<br>`RINGING`: Business initiated call is ringing the user<br>`ACCEPTED`: Business initiated call is accepted by the user<br>`REJECTED`: Business initiated call is rejected by the user |
| `biz_opaque_callback_data`<br>*String* | Arbitrary string your business passes into the call for tracking and logging purposes.<br>Will only be returned if provided through [Initiate New Call API requests](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/business-initiated-calls#initiate-a-new-call) |

### Call terminate webhook

A webhook notification is sent whenever the call has been terminated for any reason, such as when the WhatsApp user hangs up, or when the business uses the [Calls API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/calling-api) with an action of `terminate` or `reject`.

```https
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "<WHATSAPP_BUSINESS_ACCOUNT_ID>",
      "changes": [
        {
          "value": {
              "messaging_product": "whatsapp",
              "metadata": {
                   "display_phone_number": "16505553602",
                   "phone_number_id": "<PHONE_NUMBER_ID>",
              },
               "calls": [
                {
                    "id": "wacid.ABGGFjFVU2AfAgo6V-Hc5eCgK5Gh",
                    "to": "16315553601",
                    "from": "16315553602",
                    "event": "terminate"
                    "direction": "BUSINESS_INITIATED",
                    "biz_opaque_callback_data": "random_string",
                    "timestamp": "1671644824",
                    "status" : [FAILED | COMPLETED],
                    "start_time" : "1671644824",
                    "end_time" : "1671644944",
                    "duration" : 120
                }
              ],
              "errors": [
                {
                    "code": INT_CODE,
                    "message": "ERROR_TITLE",
                    "href": "ERROR_HREF",
                    "error_data": {
                        "details": "ERROR_DETAILS"
                    }
                }
              ]
          },
          "field": "calls"
        }
      ]
    }
  ]
}
```

Webhook values for

"calls"

| Placeholder | Description |
| --- | --- |
| `id`<br>*String* | A unique ID for the call |
| `to`<br>*Integer* | The number being called (callee) |
| `from`<br>*Integer* | The number of the caller |
| `event`<br>*Integer* | The calling event that this webhook is notifying the subscriber of |
| `timestamp`<br>*Integer* | The UNIX timestamp of the webhook event |
| `direction`<br>*String* | The direction of the call being made.<br>Can contain either:<br>`BUSINESS_INITIATED`, for calls initiated by your business.<br>`USER_INITIATED`, for calls initiated by a WhatsApp user. |
| `start_time`<br>*Integer* | The UNIX timestamp of when the call started.<br>Only present when the call was picked up by the other party. |
| `end_time`<br>*Integer* | The UNIX timestamp of when the call ended.<br>Only present when the call was picked up by the other party. |
| `duration`<br>*Integer* | Duration of the call in seconds.<br>Only present when the call was picked up by the other party. |
| `biz_opaque_callback_data`<br>*String* | Arbitrary string your business passes into the call for tracking and logging purposes.<br>Will only be returned if provided through an [Initiate Call API request](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/business-initiated-calls#initiate-call) or [Accept Call request](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/reference#accept-call) |
| `errors.code`<br>*Integer* | The `errors` object is present only for failed calls when there is error information available. Code is one of the [calling error codes](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/troubleshooting#calling-error-codes) |

## SDP overview and sample structures

Session Description Protocol (SDP) is a text-based format used to describe the characteristics of multimedia sessions, such as voice and video calls, in real-time communication applications. SDP provides a standardized way to describe the session’s media streams. This includes media type, codecs, protocols, and parameters for establishing and managing the session.

In the context of WebRTC, SDP is used to negotiate the media parameters between the sender and receiver, enabling them to agree on the specifics of the media exchange.

[View SDP sample structures for business-initiated calls](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/reference#sdp-overview-and-sample-sdp-structures)
