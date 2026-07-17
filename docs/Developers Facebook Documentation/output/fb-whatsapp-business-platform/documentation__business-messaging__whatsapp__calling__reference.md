# API and Webhook Reference | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/reference_

---

# API and Webhook Reference

Updated: Nov 25, 2025

## Calling API endpoints

### Configure or update calling settings

Use the [Settings API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/settings-api#post-version-phone-number-id-settings) and pass in Calling API parameters to configure settings on a business phone number you designate in the request syntax.

Request syntax

```https
POST /<PHONE_NUMBER_ID>/settings
```

Endpoint parameters

| Placeholder | Description | Sample Value |
| --- | --- | --- |
| `<PHONE_NUMBER_ID>`<br>*Integer* | **Required**<br>The business phone number for which you are updating Calling API settings. | `+12784358810` |

Request body

```curl
{
  "calling": {
    "status": "ENABLED",
    "call_icon_visibility": "DEFAULT",
    "call_hours": {
      "status": "ENABLED",
      "timezone_id": "America/Manaus",
      "weekly_operating_hours": [
        {
          "day_of_week": "MONDAY",
          "open_time": "0400",
          "close_time": "1020"
        },
        {
          "day_of_week": "TUESDAY",
          "open_time": "0108",
          "close_time": "1020"
        }
      ],
      "holiday_schedule": [
        {
          "date": "2026-01-01",
          "start_time": "0000",
          "end_time": "2359"
        }
      ]
    },
    "callback_permission_status": "ENABLED",
    "sip": {
      "status": "ENABLED | DISABLED (default)",
      "servers": [
        {
          "hostname": SIP_SERVER_HOSTNAME,
          "port": SIP_SERVER_PORT,
          "request_uri_user_params": {
            "KEY1": "VALUE1",
            "KEY2": "VALUE2"
          }
        }
      ]
    }
  }
}
```

Body parameters

| Parameter | Description | Sample Value |
| --- | --- | --- |
| `status`<br>*String* | **Optional**<br>Enable or disable the Calling API for the given business phone number. | `“ENABLED”`<br>`“DISABLED”` |
| `call_icon_visibility`<br>*String* | **Optional**<br>Configure whether the WhatsApp call button icon displays for users when chatting with the business.<br>[View call icon visibility behavior details in the Parameter details section](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/reference#configure-call-settings-parameter-details) | [View call icon visibility behavior details below](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/reference#configure-call-settings-parameter-details) |
| `call_hours`<br>*JSON object* | **Optional**<br>Allows you to specify and trigger call settings for incoming calls based on your timezone, business operating hours, and holiday schedules.<br>Any previously configured values in `call_hours` will be replaced with the values passed in the request body of this API call.<br>[View call hours behavior details in the Parameter details section](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/reference#configure-call-settings-parameter-details) | [View call hours behavior details below](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/reference#configure-call-settings-parameter-details) |
| `callback_permission_status`<br>*String* | **Optional**<br>Configure whether a WhatsApp user is prompted with a call permission request after calling your business.<br>Note: The call permission request is triggered from either a missed or connected call.<br>[View callback permission status behavior details in the Parameter details section](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/reference#configure-call-settings-parameter-details) | `“ENABLED”`<br>`“DISABLED”` |
| `sip`<br>*JSON object* | **Optional**<br>Configure call signaling via signal initiation protocol (SIP).<br>**Note: When SIP is enabled, you cannot use calling related endpoints and will not receive calling related webhooks.**<br>[Learn how to configure and use SIP call signaling](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/sip) | `"sip": {<br> "status": "ENABLED \| DISABLED (default)",<br> "servers": [// one server per app]<br> {<br> "hostname": SIP_SERVER_HOSTNAME<br> "port": SIP_SERVER_PORT,<br> "request_uri_user_params": {<br> "KEY1": "VALUE1", // for cases like TGRP<br> "KEY2": "VALUE2",<br> }<br> }<br> ]<br> }` |

Parameter details: Calling status

When the `status` parameter is set to `“ENABLED”`, calling features are enabled for the business phone number. WhatsApp client applications will render the call button icon in both the business chat and business chat profile.

When the `status` parameter is set to `“DISABLED”`, calling features are **disabled**, and both the business chat and business chat profile **do not display the call button icon.**

Updates to `status` will update the call button icon in existing business chats in near real-time when the business phone number is in the WhatsApp user’s contacts.

Otherwise, updates are real-time for a limited number of users in conversation with the business, and are eventually updated for the rest of conversations.

Parameter details: Call button icon visibility

When Calling API features are enabled for a business number, you can still choose whether to show the call button icon or not by using the `call_icon_visibility` parameter. Note: Disabling call button icon visibility **does not** disable a WhatsApp user’s ability to make unsolicited calls to your business.

The behavior for supported options is as follows:

`DEFAULT`

The Call button icon will be displayed in the chat menu bar and the business info page, allowing for unsolicited calls to the business by WhatsApp users.

![Screenshot showing the call button icon displayed in the WhatsApp chat menu bar and business info page](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/560917504_1339317971260187_5308835930412534329_n.jpg?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=xQyVLeUpUhgQ7kNvwGebcB8&_nc_oc=AdqoJ5pkgjtGQ6hr2jzFMVh041R0m9eZuf6eS4VRu5PbDG9WUL-iMkSEMe26o2uw-80&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=iKkkXx8GH48I78kJEtGexg&_nc_ss=7b20f&oh=00_Af7l-mxTmisblylE2DhKUiduZokFGJMYE2gzx5HrwmYJ_g&oe=6A1C1A41)

`DISABLE ALL`

The call button icon is hidden in the chat menu bar and the business info page, and all other entry points external to the chat are also disabled. Consumers cannot make unsolicited calls to the business.

Your business can still [send interactive messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/call-button-messages-deep-links#send-interactive-message-with-a-whatsapp-call-button) or [template messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/call-button-messages-deep-links#create-and-send-whatsapp-call-button-template-message) with a Calling API CTA button.

![Screenshot showing the WhatsApp chat interface with the call button icon hidden](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/560585020_1339317941260190_3863205212606668279_n.jpg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=hvH2L81YjrsQ7kNvwGPX8q6&_nc_oc=Adqgfm6pg05CpxSlDnhJqxB33Pe3Tb-gdZF0GlOrBG8oVf3_hbs9K2rmkNZ6kljurEk&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=iKkkXx8GH48I78kJEtGexg&_nc_ss=7b20f&oh=00_Af6u-RdEx1taejhTkXAcwjB9jZDFZ5nzi3J7IbtNfdIRCA&oe=6A1C27C4)

Callback permissions

Calling a WhatsApp user requires explicit permission from the user. One way to obtain calling permissions is to request permission when a WhatsApp user calls your business.

You can configure the call permission UI to automatically show in the WhatsApp user’s client app when they call your business number. The user may change their permission selection at any time.

![Screenshot showing the WhatsApp call permission request dialog](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/602352272_1389874706204513_7741631937402058550_n.jpg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=Z5ttGfRVSJAQ7kNvwHYG-cS&_nc_oc=Adq1PhODbrFd1jFwCb4kwsX-701VpcTgexV5V0f_2gQ5hpMUeTr6i2pXA_-niOU4MR8&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=iKkkXx8GH48I78kJEtGexg&_nc_ss=7b20f&oh=00_Af78TAABpYpJ5llIvLRWaaJcV2ZVnmad-CdBN7iAJjB2GA&oe=6A1C261A)

Call hours

With the `call_hours` setting, you can specify the timezone, business operating hours, and holiday schedules that will be enforced for all user-initiated calls.

Configuring this setting restricts calls only to available weekly hours you configure. User-initiated calls are unavailable outside of the weekly hours and holiday schedules you set.

The WhatsApp client app will show users an option to chat with the business, or request a callback, if `callback_permission_status` is `ENABLED`. The user will also be shown the next available calling slot on the option screen.

![Screenshot showing WhatsApp call hours unavailable screen with callback option](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/561822470_1339317924593525_4183355843280485487_n.jpg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=I0UhGIogB-QQ7kNvwEiCONt&_nc_oc=AdoYC6f6XQUAvytLvo3QDAwpLZmXJ5llnpRWW43WdanQwdhbUckKnlBV5qscgYI3HjQ&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=iKkkXx8GH48I78kJEtGexg&_nc_ss=7b20f&oh=00_Af4SWYoVXAbmI5S-PbpLcIdMxEf50ox5upGIvBdlLpEEtw&oe=6A1BFC27)

```curl
"call_hours": {
  "status": "ENABLED",
  "timezone_id": "America/Manaus",
  "weekly_operating_hours": [
    {
      "day_of_week": "MONDAY",
      "open_time": "04:00",
      "close_time": "10:20"
    },
    {
      "day_of_week": "TUESDAY",
      "open_time": "01:08",
      "close_time": "10:20"
    }
  ],
  "holiday_schedule": [
    {
      "date": "2026-01-01",
      "start_time": "00:00",
      "end_time": "23:59"
    }
  ]
}
```

| Parameter | Description | Sample Values |
| --- | --- | --- |
| `status`<br>*String* | **Required**<br>Enable or disable the call hours for the business.<br>If call hours are disabled, the business is considered open all 24 hours of the day, 7 days a week. | `“ENABLED”`<br>`“DISABLED”` |
| `timezone_id`<br>*String* | **Required**<br>The timezone that the business is operating within.<br>[Learn more about supported values for `timezone_id`](https://developers.facebook.com/docs/facebook-business-extension/fbe/reference#time-zones) | `“America/Menominee”`<br>`“Asia/Singapore”` |
| `weekly_operating_hours`<br>*List of JSON object* | **Required**<br>The operating hours schedule for each day of the week.<br>Each entry is an JSON object with 3 key/value pairs:<br>`day_of_week` — (*Enum*) **[Required]**<br>The day of the week.<br>Can take one of seven values: `"MONDAY"`, `“TUESDAY”`, `“WEDNESDAY”`, `“THURSDAY”`, `“FRIDAY”`, `“SATURDAY”`, `“SUNDAY”`<br>`open_time``close_time` — (*Integer*) **[Required]**<br>Opening and closing times represented in 24 hour format, for example `"1130"` = 11:30AM<br>Maximum of 2 entries allowed per day of week`open_time` must be before `close_time`Overlapping entries not allowed | `{<br>"day_of_week": "MONDAY",<br>"open_time": "0400",<br>"close_time": "1020"<br>},<br>{<br>"day_of_week":"TUESDAY",<br>"open_time": "0108",<br>"close_time": "1020"<br>}<br>...` |
| `holiday_schedule`<br>*String* | **Optional**<br>An optional override to the weekly schedule.<br>Up to 20 overrides can be specified.<br>Note: If `holiday_schedule` is not passed in the request, then the existing `holiday_schedule` will be deleted and replaced with an empty schedule.<br>`date` — (*String*) **[Required]**<br>Date for which you want to specify the override.<br>YYYY-MM-DD format.<br>`open_time``close_time` — (*Integer*) **[Required]**<br>Opening and closing times represented in 24 hour format, for example, `”1130”` = 11:30AM<br>Maximum of 2 entries allowed per day of week`open_time` must be before `close_time`Overlapping entries not allowed | `{<br>"date": "2026-01-01",<br>"start_time": "0000",<br>"end_time": "2359",<br>}<br>...` |

Success response

```curl
{
  "success": true
}
```

Error response

Possible errors that can occur:

- Permissions/Authorization errors
- Invalid status
- Invalid schedule for `call_hours`
- Holiday given in `call_hours` is a past date
- Timezone is invalid in `call_hours`
- `weekly_operating_hours` in `call_hours` cannot be empty
- Date format in `holiday_schedule` for call_hours is invalid
- More than 2 entries not allowed in `weekly_operating_hours` schedule in `call_hours`
- Overlapping schedule in `call_hours` is not allowed

[View Calling API Error Codes and Troubleshooting for more information](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/troubleshooting).

[View general Cloud API Error Codes here](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/error-codes).

### Get phone number calling settings

Use the [Settings API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/settings-api#get-version-phone-number-id-settings) to retrieve Calling API settings on an individual business phone number you designate in the request syntax.

This endpoint can return information for other Cloud API feature settings.

Request syntax

```https
POST /<PHONE_NUMBER_ID>/settings
```

Endpoint parameters

| Parameter | Description | Sample Value |
| --- | --- | --- |
| `<PHONE_NUMBER_ID>`<br>*Integer* | **Required**<br>The business phone number for which you are getting Calling API settings.<br>[Learn more about formatting phone numbers in Cloud API](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers) | `+12784358810` |

App permission required

`whatsapp_business_management`: Advanced access is required to use the API for end business clients

Response body

```curl
{
  "calling": {
    "status": "ENABLED",
    "call_icon_visibility": "DEFAULT",
    "call_hours": {
      "status": "ENABLED",
      "timezone_id": "America/Manaus",
      "weekly_operating_hours": [
        {
          "day_of_week": "MONDAY",
          "open_time": "0400",
          "close_time": "1020"
        },
        {
          "day_of_week": "TUESDAY",
          "open_time": "0108",
          "close_time": "1020"
        }
      ],
      "holiday_schedule": [
        {
          "date": "2026-01-01",
          "start_time": "0000",
          "end_time": "2359"
        }
      ]
    },
    "callback_permission_status": "ENABLED",
    "sip": {
      "status": "ENABLED | DISABLED (default)",
      "servers": [
        {
          "hostname": SIP_SERVER_HOSTNAME,
          "port": SIP_SERVER_PORT,
          "request_uri_user_params": {
            "KEY1": "VALUE1",
            "KEY2": "VALUE2"
          }
        }
      ]
    }
  }
}
```

Include SIP user password

Optionally, you can include SIP user credentials in your response body by adding the SIP credentials query parameter in the POST request:

```https
POST /<PHONE_NUMBER_ID>/settings?include_sip_credentials=true
```

Where the response will look like this:

```curl
{
  "calling": {
    ... // other calling api settings
    "sip": {
      "status": "ENABLED",
      "servers": [
        {
          "hostname": "sip.example.com",
          "sip_user_password": "{SIP_USER_PASSWORD}"
        }
      ]
    }
  }
}
```

Response details

The `GET /<PHONE_NUMBER_ID>/settings` endpoint returns Calling API settings, along with other configuration information for your WhatsApp business phone number.

[Learn more about Calling API settings and their values](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/call-settings#body-parameters)

Error response

Possible errors that can occur:

- Permissions/Authorization errors

[View Calling API Error Codes and Troubleshooting for more information](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/troubleshooting)

[View general Cloud API Error Codes here](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/error-codes)

### Pre-accept call

When you pre-accept an inbound call, you allow the calling media connection to be established before attempting to send call media through the connection.

When you then call the accept call endpoint, media begins flowing immediately since the connection has already been established.

Pre-accepting calls is recommended because it facilitates faster connection times and avoids [audio clipping issues](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/troubleshooting#audio-clipping-issue-and-solution).

There is about 30 to 60 seconds after the [Call Connect webhook](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/reference#call-connect-webhook) is sent for the business to accept the phone call. If the business does not respond, the call is terminated on the WhatsApp user side with a “Not Answered” notification and a [Terminate Webhook](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/reference#call-terminate-webhook) is delivered back to you.

**Note:** Since the WebRTC connection is established before calling the [Accept Call endpoint](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/reference#accept-call), make sure to flow the call media only after you receive a 200 OK response back.

If call media flows too early, the caller will miss the first few words of the call. If call media flows too late, callers will hear silence.

Request syntax

```https
POST <PHONE_NUMBER_ID>/calls
```

| Placeholder | Description | Sample Value |
| --- | --- | --- |
| `<PHONE_NUMBER_ID>`<br>*Integer* | **Required**<br>The business phone number which you are using Calling API features from.<br>[Learn more about formatting phone numbers in Cloud API](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers) | `+12784358810` |

Request body

```https
{
  "messaging_product": "whatsapp",
  "call_id": "wacid.ABGGFjFVU2AfAgo6V-Hc5eCgK5Gh",
  "action": "pre_accept",
  "session" : {
      "sdp_type" : "answer",
      "sdp" : "<<RFC 8866 SDP>>"
   }
}
```

Body parameters

| Parameter | Description | Sample Value |
| --- | --- | --- |
| `call_id`<br>*String* | **Required**<br>The ID of the phone call.<br>For inbound calls, you receive a call ID from the [Call Connect webhook](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/reference#call-connect-webhook) when a WhatsApp user initiates the call. | `“wacid.ABGGFjFVU2AfAgo6V-Hc5eCgK5Gh”` |
| `action`<br>*String* | **Optional**<br>The action being taken on the given call ID.<br>Values can be `connect` \| `pre_accept` \| `accept` \| `reject` \| `terminate` | `“pre_accept”` |
| `session`<br>*JSON object* | **Optional**<br>Contains the session description protocol (SDP) type and description language.<br>Requires two values:<br>`sdp_type` — (*String*) **Required**<br>“offer”, to indicate SDP offer<br>`sdp` — (*String*) **Required**<br>The SDP info of the device on the other end of the call. The SDP must be compliant with [RFC 8866](https://datatracker.ietf.org/doc/html/rfc8866).<br>[Learn more about Session Description Protocol (SDP)](https://www.rfc-editor.org/rfc/rfc8866.html)<br>[View example SDP structures](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/reference#sdp-overview-and-sample-sdp-structures) | `"session" :<br>{<br>"sdp_type" : "offer",<br>"sdp" : "<<RFC 8866 SDP>>"<br>}` |

Success response

```https
{
  "messaging_product": "whatsapp",
  "success" : true
}
```

Error response

Possible errors that can occur:

- Invalid `call-id`
- Invalid `phone-number-id`
- Error related to your payment method
- Invalid Connection info, for example, sdp, ice
- Accept/Reject an already In Progress/Completed/Failed call
- Permissions/Authorization errors

[View Calling API Error Codes and Troubleshooting for more information](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/troubleshooting).

[View general Cloud API Error Codes here](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/error-codes).

### Accept call

Use this endpoint to connect to a call by providing a call agent’s SDP.

You have about 30 to 60 seconds after the [Call Connect Webhook](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/reference#call-connect-webhook) is sent to accept the phone call. If your business does not respond, the call is terminated on the WhatsApp user side with a “Not Answered” notification and a [Terminate Webhook](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/reference#call-terminate-webhook) is delivered back to you.

Request syntax

```https
POST <PHONE_NUMBER_ID>/calls
```

| Placeholder | Description | Sample Value |
| --- | --- | --- |
| `<PHONE_NUMBER_ID>`<br>*Integer* | **Required**<br>The business phone number which you are using Calling API features from.<br>[Learn more about formatting phone numbers in Cloud API](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers) | `+12784358810` |

Request body

```https
{
  "messaging_product": "whatsapp",
  "call_id": "wacid.ABGGFjFVU2AfAgo6V-Hc5eCgK5Gh",
  "action": "accept",
  "session" : {
      "sdp_type" : "answer",
      "sdp" : "<<RFC 8866 SDP>>"
   },
   "biz_opaque_callback_data": "random_string"
}
```

Body parameters

| Parameter | Description | Sample Value |
| --- | --- | --- |
| `call_id`<br>*String* | **Required**<br>The ID of the phone call.<br>For inbound calls, you receive a call ID from the [Call Connect webhook](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/reference#call-connect-webhook) when a WhatsApp user initiates the call. | `“wacid.ABGGFjFVU2AfAgo6V-Hc5eCgK5Gh”` |
| `action`<br>*String* | **Optional**<br>The action being taken on the given call ID.<br>Values can be `connect` \| `pre_accept` \| `accept` \| `reject` \| `terminate` | `“accept”` |
| `session`<br>*JSON object* | **Optional**<br>Contains the session description protocol (SDP) type and description language.<br>Requires two values:<br>`sdp_type` — (*String*) **Required**<br>“offer”, to indicate SDP offer<br>`sdp` — (*String*) **Required**<br>The SDP info of the device on the other end of the call. The SDP must be compliant with [RFC 8866](https://datatracker.ietf.org/doc/html/rfc8866).<br>[Learn more about Session Description Protocol (SDP)](https://www.rfc-editor.org/rfc/rfc8866.html)<br>[View example SDP structures](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/reference#sdp-overview-and-sample-sdp-structures) | `"session" :<br>{<br>"sdp_type" : "offer",<br>"sdp" : "<<RFC 8866 SDP>>"<br>}` |
| `biz_opaque_callback_data`<br>*String* | **Optional**<br>An arbitrary string you can pass in that is useful for tracking and logging purposes.<br>Any app subscribed to the “calls” webhook field on your WhatsApp Business Account can receive this string, as it is included in the `calls` object within the subsequent [Terminate webhook](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/reference#call-terminate-webhook) payload.<br>Cloud API does not process this field, it just returns it as part of the [Terminate webhook](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/reference#call-terminate-webhook).<br>Maximum 512 characters | `“8huas8d80nn”` |

Success response

```https
{
  "messaging_product": "whatsapp",
  "success" : true
}
```

Error response

Possible errors that can occur:

- Invalid `call-id`
- Invalid `phone-number-id`
- Error related to your payment method
- Invalid Connection info, for example, sdp, ice, or other connection parameters
- Accept/Reject an already In Progress/Completed/Failed call
- Permissions/Authorization errors
- SDP answer provided in accept does not match the SDP answer given in the [Pre-Accept endpoint](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/reference#pre-accept-call) for the same `call-id`

[View Calling API Error Codes and Troubleshooting for more information](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/troubleshooting).

[View general Cloud API Error Codes here](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/error-codes).

### Reject call

Use this endpoint to reject a call.

You have about 30 to 60 seconds after the [Call Connect webhook](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/reference#call-connect-webhook) is sent to accept the phone call. If the business does not respond, the call is terminated on the WhatsApp user side with a “Not Answered” notification and a [Terminate Webhook](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/reference#call-terminate-webhook) is delivered back to you.

Request syntax

```https
POST <PHONE_NUMBER_ID>/calls
```

| Placeholder | Description | Sample Value |
| --- | --- | --- |
| `<PHONE_NUMBER_ID>`<br>*Integer* | **Required**<br>The business phone number which you are using Calling API features from.<br>[Learn more about formatting phone numbers in Cloud API](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers) | `+12784358810` |

Request body

```https
{
  "messaging_product": "whatsapp",
  "call_id": "wacid.ABGGFjFVU2AfAgo6V-Hc5eCgK5Gh",
  "action": "reject"
}
```

Body parameters

| Parameter | Description | Sample Value |
| --- | --- | --- |
| `call_id`<br>*String* | **Required**<br>The ID of the phone call.<br>For inbound calls, you receive a call ID from the [Call Connect webhook](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/reference#call-connect-webhook) when a WhatsApp user initiates the call. | `“wacid.ABGGFjFVU2AfAgo6V-Hc5eCgK5Gh”` |
| `action`<br>*String* | **Optional**<br>The action being taken on the given call ID.<br>Values can be `connect` \| `pre_accept` \| `accept` \| `reject` \| `terminate` | `“reject”` |

Success response

```https
{
  "messaging_product": "whatsapp",
  "success" : true
}
```

Error response

Possible errors that can occur:

- Invalid `call-id`
- Invalid `phone-number-id`
- Accept/Reject an already In Progress/Completed/Failed call
- Permissions/Authorization errors

[View Calling API Error Codes and Troubleshooting for more information](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/troubleshooting).

[View general Cloud API Error Codes here](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/error-codes).

### Initiate call

Use this endpoint to initiate a call to a WhatsApp user by providing a phone number and a WebRTC call offer.

Request syntax

```https
POST <PHONE_NUMBER_ID>/calls
```

| Placeholder | Description | Sample Value |
| --- | --- | --- |
| `<PHONE_NUMBER_ID>`<br>*Integer* | **Required**<br>The business phone number from which you are initiating a new call.<br>[Learn more about formatting phone numbers in Cloud API](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers) | `+12784358810` |

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
| `to`<br>*Integer* | **Required**<br>The number being called (callee) | `“17863476655”` |
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

[View Calling API Error Codes and Troubleshooting for more information](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/troubleshooting).

[View general Cloud API Error Codes here](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/error-codes).

### Terminate call

Use this endpoint to terminate an active call.

This must be done even if there is an `RTCP BYE` packet in the media path. Ending the call this way also ensures pricing is more accurate.

When the WhatsApp user terminates the call, you do not have to call this endpoint. Once the call is successfully terminated, a [Call Terminate Webhook](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/business-initiated-calls#call-terminate-webhook) will be sent to you.

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

[View Calling API Error Codes and Troubleshooting for more information](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/troubleshooting).

[View general Cloud API Error Codes here](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/error-codes).

### Get current call permission state

Use this endpoint to get the call permission state for a business phone number with a single WhatsApp user phone number.

Request syntax

```https
GET /<PHONE_NUMBER_ID>/call_permissions?user_wa_id=<CONSUMER_WHATSAPP_ID>
```

Request parameters

| Parameter | Description | Sample Value |
| --- | --- | --- |
| `<PHONE_NUMBER_ID>`<br>*String* | **Required**<br>The business phone number you are fetching permissions against.<br>[Learn more about formatting phone numbers in Cloud API](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers) | `+18762639988` |
| `<CONSUMER_WHATSAPP_ID>`<br>*Integer* | **Required**<br>The phone number of the WhatsApp user who you are requesting call permissions from.<br>[Learn more about formatting phone numbers in Cloud API](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers) | `+13057765456` |

Response body

```https
{
  "messaging_product": "whatsapp",
  "permission": {
    "status": "temporary",
    "expiration_time": 1745343479
  },
  "actions": [
    {
      "action_name": "send_call_permission_request",
      "can_perform_action": true,
      "limits": [
        {
          "time_period": "PT24H",
          "max_allowed": 1,
          "current_usage": 0,
        },
        {
          "time_period": "P7D",
          "max_allowed": 2,
          "current_usage": 1,
        }
      ]
    },
    {
      "action_name": "start_call",
      "can_perform_action": false,
      "limits": [
        {
          "time_period": "PT24H",
          "max_allowed": 5,
          "current_usage": 5,
          "limit_expiration_time": 1745622600,
        }
      ]
    }
  ]
}
```

Response parameters

| Parameter | Description |
| --- | --- |
| `permission`<br>*JSON Object* | The permission object contains two values:<br>`status` *(String)* — The current status of the permission.<br>Can be either:<br>`“no_permission”``"temporary"`<br>`expiration` *(Integer)* — The Unix time at which the permission will expire in UTC timezone. |
| `actions`<br>*JSON Object* | A list of actions a business phone number may undertake to facilitate a call permission or a business initiated call.<br>Current actions are:<br>`send_call_permission_request`: Represents the action of sending new call permissions request messages to the WhatsApp user.<br>`start_call`: Represents the action of establishing a new call with the WhatsApp user. Establishing a new call means that the call was successfully picked up by the consumer.<br>For example, `send_call_permission_request` having a `can_perform_action` of `true` means that your business can send a call permission request to the WhatsApp user in question<br>`can_perform_action` (*Boolean*) —<br>A flag indicating whether the action can be performed now, taking into account all limits. |
| `limits`<br>*JSON Object* | A list of time-bound restrictions for the given `action_name`.<br>Each `action_name` has 1 or more restrictions depending on the timeframe.<br>For example, a business can only send 2 permission requests in a 24-hour period.<br>`limits` contains the following fields:<br>`time_period` (*String*) — The span of time in which the limit applies, represented in the ISO 8601 format.<br>`max_allowed` (*Integer*) — The maximum number of actions allowed within the specified time period.<br>`current_usage` (*Integer*) — The current number of actions the business has taken within the specified time period.<br>`limit_expiration_time` (*Integer*) — The Unix time at which the limit will expire in UTC timezone.<br>If `current_usage` is under the max allowed for the limit, this field won’t be present. |

Error response

Possible errors that can occur:

- Invalid `phone-number-id`
- If the consumer phone number is uncallable, the api response will be `no_permission` .
- Permissions/Authorization errors.
- Rate limit reached. A maximum of 5 requests in a 1 second window can be made to the API.
- Calling is not enabled for the business phone number.

[View Calling API Error Codes and Troubleshooting for more information](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/troubleshooting)

[View general Cloud API Error Codes here](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/error-codes)

## Calling API Webhooks

### Call Connect webhook

A webhook notification is sent in near real-time when a call initiated by your business is ready to be connected to the WhatsApp user (an `SDP Answer`).

Critically, the webhook contains information required to establish a call connection via WebRTC.

Once you receive the Call Connect webhook, you can apply the `SDP Answer` received in the webhook to your WebRTC stack in order to initiate the media connection.

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
                "profile": {
                  "name": "<CALLEE_NAME>"
                },
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
| `contacts`<br>*JSON object* | Profile information of the callee.<br>Contains two values:<br>`name` — The WhatsApp profile name of the callee.<br>`wa_id` — The WhatsApp ID of the callee. |

### Call status webhook

This webhook is sent during the following calling events:

1. Ringing: When the WhatsApp user’s client device begins ringing
2. Accepted: When the WhatsApp user accepts the call
3. Rejected: When the call is rejected by the WhatsApp user

The Webhook structure here is similar to the Status webhooks used for the Cloud API messages.

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

A webhook notification is sent whenever the call has been terminated for any reason, such as when the WhatsApp user hangs up, or when the business calls the `POST /<PHONE_NUMBER_ID>/calls` endpoint with an action of `terminate` or `reject`.

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
| `biz_opaque_callback_data`<br>*String* | Arbitrary string your business passes into the call for tracking and logging purposes.<br>Will only be returned if provided through [New Call API requests](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/reference#initiate-call) or [Accept Call requests](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/reference#accept-call) |

### User calling permission request webhook

This webhook is sent back after requesting user calling permissions.

The webhook changes depending on if the user:

- accepts or rejects the request
- gives permission by responding to a request or by calling the business

Webhook sample

```https
{
. . .

"messages": [{
    "from": "{customer_phone_number}",
    "id": "wamid.sH0kFlaCGg0xcvZbgmg90lHrg2dL",
    "timestamp": "{timestamp}",
    "context": {
          "from": "{customer_phone_number}",
          "id": "wacid.gBGGFlaCmZ9plHrf2Mh-o"
    },
    "interactive": {
       "type":  "call_permission_reply",
        "call_permission_reply": {
            "response":"accept",
            "is_permanent":false,
            "expiration_timestamp": "{timestamp}",
            "response_source": "[user_action|automatic]"
       }
    }
 ],
. . .
}
```

Webhook sample (with permanent permissions)

```https
"messages": [{
    "from": "{customer_phone_number}",
    "id": "wamid.sH0kFlaCGg0xcvZbgmg90lHrg2dL",
    "timestamp": "{timestamp}",
    "context": {
          "from": "{customer_phone_number}",
          "id": "wacid.gBGGFlaCmZ9plHrf2Mh-o"
    },
    "interactive": {
       "type":  "call_permission_reply",
        "call_permission_reply": {
            "response":"accept",
            "is_permanent":false,
            "expiration_timestamp": "{timestamp}",
            "response_source": "[user_action|automatic]"
       }
    }
 ],
. . .
}
```

Webhook values

| Placeholder | Description |
| --- | --- |
| `customer_phone_number`<br>*String* | The phone number of the customer |
| `context.id`<br>*String* | Can be either of two values<br>Message ID of the permission request message sent by the business to the customer number. Shows when a permission decision is made by the user in response to a call permission request.Call ID of the missed call placed by the business to the customer number. Shows when callback permission is enabled in settings and the user calls the business. |
| `response`<br>*String* | The WhatsApp users response to the call permission request message<br>Can be `accept` or `reject` |
| `expiration_timestamp`<br>*Integer* | Time in seconds when this call permission expires if the WhatsApp user approved it |
| `response_source`<br>*String* | The source of this permission<br>Possible values for accepted call permissions are:<br>`user_action`: User approved or rejected the permission`automatic`: An automatic permission approval due to the WhatsApp user initiating the call |

## SDP overview and sample SDP structures

Session Description Protocol (SDP) is a text-based format that describes multimedia session characteristics, such as voice and video calls, in real-time communication applications. SDP provides a standardized way to convey information about the session’s media streams, including the type of media, codecs, protocols, and other parameters necessary for establishing and managing the session.

In the context of WebRTC, SDP is used to negotiate the media parameters between the sender and receiver, enabling them to agree on the specifics of the media exchange.

### Business-initiated sample SDP structures

Sample SDP offer structure

```https
v=0
o=- 3626166318745852955 2 IN IP4 127.0.0.1
s=-
t=0 0
a=group:BUNDLE 0
a=extmap-allow-mixed
a=msid-semantic: WMS d8b26053-4474-4eb7-b3c3-c93d6c8c9b2e
m=audio 9 UDP/TLS/RTP/SAVPF 111 63 9 0 8 110 126
c=IN IP4 0.0.0.0
a=rtcp:9 IN IP4 0.0.0.0
a=ice-ufrag:4g1c
a=ice-pwd:qY/Bb+jQzg5ICn6X4fhJQetk
a=ice-options:trickle
a=fingerprint:sha-256 35:47:24:24:9F:93:C4:3E:DB:37:7F:BB:ED:F8:20:B5:AD:AC:DC:35:C2:7D:67:EE:6C:35:54:DF:A6:00:5C:4A
a=setup:actpass
a=mid:0
a=extmap:1 urn:ietf:params:rtp-hdrext:ssrc-audio-level
a=extmap:2 http://www.webrtc.org/experiments/rtp-hdrext/abs-send-time
a=extmap:3 http://www.ietf.org/id/draft-holmer-rmcat-transport-wide-cc-extensions-01
a=extmap:4 urn:ietf:params:rtp-hdrext:sdes:mid
a=sendrecv
a=msid:d8b26053-4474-4eb7-b3c3-c93d6c8c9b2e 5b4d3d96-ea9b-44a8-87e6-11a1ad21a3bc
a=rtcp-mux
a=rtpmap:111 opus/48000/2
a=rtcp-fb:111 transport-cc
a=fmtp:111 minptime=10;useinbandfec=1
a=rtpmap:63 red/48000/2
a=fmtp:63 111/111
a=rtpmap:9 G722/8000
a=rtpmap:0 PCMU/8000
a=rtpmap:8 PCMA/8000
a=rtpmap:110 telephone-event/48000
a=rtpmap:126 telephone-event/8000
a=ssrc:2220762577 cname:w/zwpg3jXNiTFTdZ
a=ssrc:2220762577 msid:d8b26053-4474-4eb7-b3c3-c93d6c8c9b2e 5b4d3d96-ea9b-44a8-87e6-11a1ad21a3bc
```

Sample SDP answer structure

```https
v=0
o=- 741807839102053725 2 IN IP4 127.0.0.1
s=-
t=0 0
a=group:BUNDLE 0
a=extmap-allow-mixed
a=msid-semantic: WMS 798a9670-c0d6-47a8-925e-5f082ef4d8a0
a=ice-lite
m=audio 3482 UDP/TLS/RTP/SAVPF 111 9 0 8 110 126
c=IN IP4 31.13.65.130
a=rtcp:9 IN IP4 0.0.0.0
a=candidate:2754936280 1 udp 2113937151 31.13.65.130 3482 typ host generation 0 network-cost 50 ufrag JHqAXFH4HcAY/8
a=candidate:1581496399 1 udp 2113939711 2a03:2880:f211:d1:face:b00c:0:699c 3482 typ host generation 0 network-cost 50 ufrag JHqAXFH4HcAY/8
a=ice-ufrag:JHqAXFH4HcAY/8
a=ice-pwd:dNNMmR8wUcGezvfBZOO0Qgcwl2m86GP/
a=ice-options:trickle
a=fingerprint:sha-256 9C:97:5C:4C:A9:BE:9E:2F:06:94:F5:BB:38:2C:A1:29:B5:69:B8:FA:94:10:56:1D:0B:5D:80:28:C1:FD:F0:F6
a=setup:active
a=mid:0
a=extmap:1 urn:ietf:params:rtp-hdrext:ssrc-audio-level
a=extmap:2 http://www.webrtc.org/experiments/rtp-hdrext/abs-send-time
a=extmap:3 http://www.ietf.org/id/draft-holmer-rmcat-transport-wide-cc-extensions-01
a=sendrecv
a=rtcp-mux
a=rtpmap:111 opus/48000/2
a=rtcp-fb:111 transport-cc
a=fmtp:111 minptime=10;useinbandfec=1
a=rtpmap:9 G722/8000
a=rtpmap:0 PCMU/8000
a=rtpmap:8 PCMA/8000
a=rtpmap:110 telephone-event/48000
a=rtpmap:126 telephone-event/8000
a=ssrc:3407645770 cname:bg8KQDoIk2UJa6sf
a=ssrc:3407645770 msid:798a9670-c0d6-47a8-925e-5f082ef4d8a0 audio#nuxVMf9EAJX
a=ssrc:3407645770 mslabel:798a9670-c0d6-47a8-925e-5f082ef4d8a0
a=ssrc:3407645770 label:audio#nuxVMf9EAJX
```

### User-initiated sample SDP structures

Sample SDP offer structure

```https
v=0
o=- 7602563789789945080 2 IN IP4 127.0.0.1
s=-
t=0 0
a=group:BUNDLE audio
a=msid-semantic: WMS 6932bc1c-db1a-4abe-b437-0c4168be8a13
a=ice-lite
m=audio 40012 UDP/TLS/RTP/SAVPF 111 126
c=IN IP4 31.13.65.60
a=rtcp:9 IN IP4 0.0.0.0
a=candidate:1972637320 1 udp 2113937151 31.13.65.60 40012 typ host generation 0 network-cost 50 ufrag 6k2qP1R6kBfI/2
a=candidate:1652262791 1 udp 2113939711 2a03:2880:f211:cf:face:b00c:0:6443 40012 typ host generation 0 network-cost 50 ufrag 6k2qP1R6kBfI/2
a=ice-ufrag:6k2qP1R6kBfI/2
a=ice-pwd:UApvJw3NcwFRDvIMKdM0vWCdlXah25E9
a=fingerprint:sha-256 1B:B6:6B:40:A5:0B:8C:75:0D:8C:CB:90:2F:99:74:1E:26:45:AE:AF:45:C1:51:60:8F:73:C9:2D:10:6D:8A:88
a=setup:actpass
a=mid:audio
a=extmap:1 urn:ietf:params:rtp-hdrext:ssrc-audio-level
a=extmap:2 http://www.webrtc.org/experiments/rtp-hdrext/abs-send-time
a=extmap:3 http://www.ietf.org/id/draft-holmer-rmcat-transport-wide-cc-extensions-01
a=sendrecv
a=rtcp-mux
a=rtpmap:111 opus/48000/2
a=rtcp-fb:111 transport-cc
a=fmtp:111 minptime=10;useinbandfec=1
a=rtpmap:126 telephone-event/8000
a=ssrc:4208138518 cname:gAXq2V9TKltrnapv
a=ssrc:4208138518 msid:6932bc1c-db1a-4abe-b437-0c4168be8a13 audio#R5wfXFcdmT6
a=ssrc:4208138518 mslabel:6932bc1c-db1a-4abe-b437-0c4168be8a13
a=ssrc:4208138518 label:audio#R5wfXFcdmT6
```

Sample SDP answer structure

```https
v=0
o=- 2822644248144643933 2 IN IP4 127.0.0.1
s=-
t=0 0
a=group:BUNDLE audio
a=msid-semantic: WMS eb909cf0-87f0-4358-a4c9-7861680d9431
m=audio 9 UDP/TLS/RTP/SAVPF 111 126
c=IN IP4 0.0.0.0
a=rtcp:9 IN IP4 0.0.0.0
a=ice-ufrag:X1ho
a=ice-pwd:7fJSbV2N5qWiA5QiDKwK3vuh
a=fingerprint:sha-256 2E:35:9F:21:9E:63:72:E5:42:74:76:2D:B3:70:F7:CB:24:14:9B:14:52:71:05:48:DA:4D:67:31:09:58:2A:ED
a=setup:active
a=mid:audio
a=extmap:1 urn:ietf:params:rtp-hdrext:ssrc-audio-level
a=extmap:2 http://www.webrtc.org/experiments/rtp-hdrext/abs-send-time
a=extmap:3 http://www.ietf.org/id/draft-holmer-rmcat-transport-wide-cc-extensions-01
a=sendrecv
a=rtcp-mux
a=rtpmap:111 opus/48000/2
a=rtcp-fb:111 transport-cc
a=fmtp:111 minptime=10;useinbandfec=1
a=rtpmap:126 telephone-event/8000
a=ssrc:330833028 cname:EDc1JutBl8rwHQc2
a=ssrc:330833028 msid:eb909cf0-87f0-4358-a4c9-7861680d9431 ea478c16-d9f7-493c-8cec-19bfac750a36
```

## Sample cURL requests

New call

```https
curl -i -X POST 'https://graph.facebook.com/v14.0/1234567890/calls' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAADUMAze4GIBO1B7B.....<REPLACE_WITH_YOUR_TOKEN>' \
-d '{
   "messaging_product": "whatsapp",
   "to": "14085550000",
   "session": {
       "sdp": "v=0\r\no=- 7669997803033704573 2 IN IP4 127.0.0.1\r\ns=-\r\nt=0 0\r\na=group:BUNDLE 0\r\na=extmap-allow-mixed\r\na=msid-semantic: WMS 3c28addc-03b7-4170-b5cd-535bfe767e75\r\nm=audio 9 UDP/TLS/RTP/SAVPF 111 63 9 0 8 110 126\r\nc=IN IP4 0.0.0.0\r\na=rtcp:9 IN IP4 0.0.0.0\r\na=ice-ufrag:6O0H\r\na=ice-pwd:TYCbtfOrBMPpfxFRgSbYnuTI\r\na=ice-options:trickle\r\na=fingerprint:sha-256 9F:45:2C:A8:C3:C0:CC:9B:59:4F:D1:02:56:52:FA:36:00:BE:C0:79:87:B3:D9:9C:3E:BF:60:98:25:B4:26:FC\r\na=setup:active\r\na=mid:0\r\na=extmap:1 urn:ietf:params:rtp-hdrext:ssrc-audio-level\r\na=extmap:2 http://www.webrtc.org/experiments/rtp-hdrext/abs-send-time\r\na=extmap:3 http://www.ietf.org/id/draft-holmer-rmcat-transport-wide-cc-extensions-01\r\na=extmap:4 urn:ietf:params:rtp-hdrext:sdes:mid\r\na=sendrecv\r\na=msid:3c28addc-03b7-4170-b5cd-535bfe767e75 38c455bc-3727-4129-b336-8cd2c6a68486\r\na=rtcp-mux\r\na=rtcp-rsize\r\na=rtpmap:111 opus/48000/2\r\na=rtcp-fb:111 transport-cc\r\na=fmtp:111 minptime=10;useinbandfec=1\r\na=rtpmap:63 red/48000/2\r\na=fmtp:63 111/111\r\na=rtpmap:9 G722/8000\r\na=rtpmap:0 PCMU/8000\r\na=rtpmap:8 PCMA/8000\r\na=rtpmap:110 telephone-event/48000\r\na=rtpmap:126 telephone-event/8000\r\na=ssrc:2430753100 cname:MPddPt/R2ioP4vCm\r\na=ssrc:2430753100 msid:3c28addc-03b7-4170-b5cd-535bfe767e75 38c455bc-3727-4129-b336-8cd2c6a68486\r\n",
       "sdp_type": "answer"
   }
}'
```

Terminate call

```https
curl -i -X POST 'https://graph.facebook.com/v14.0/1234567890/calls' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAADUMAze4GIBO1B7B.....<REPLACE_WITH_YOUR_TOKEN>' \
-d '{
   "messaging_product": "whatsapp",
   "action": "terminate",
   "call_id": "wacid.HBgLMTY1MDMxMzM5NzQVAgARGCBFRjNEODRBM0Q3NDZDM0Q0QzI4MzAwQjZBRkZGODM3NhwYCzEyMjQ1NTU0NDg5FQIAAA"
}'
```

Accept call

```https
curl -i -X POST 'https://graph.facebook.com/v14.0/1234567890/calls' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAADUMAze4GIBO1B7B.....<REPLACE_WITH_YOUR_TOKEN>' \
-d '{
 "messaging_product": "whatsapp",
 "to": "14085550000",
 "action": "accept",
 "call_id": "wacid.HBgLMTY1MDMxMzM5NzQVAgASGCA5ODkyMDk2RkM2NUM1QTYwRkM4NjFDQzk0NkQwNDBCRRwYCzEyMjQ1NTU0NDg5FQIAAA==",
 "session": {
     "sdp": "v=0\r\no=- 7669997803033704573 2 IN IP4 127.0.0.1\r\ns=-\r\nt=0 0\r\na=group:BUNDLE 0\r\na=extmap-allow-mixed\r\na=msid-semantic: WMS 3c28addc-03b7-4170-b5cd-535bfe767e75\r\nm=audio 9 UDP/TLS/RTP/SAVPF 111 63 9 0 8 110 126\r\nc=IN IP4 0.0.0.0\r\na=rtcp:9 IN IP4 0.0.0.0\r\na=ice-ufrag:6O0H\r\na=ice-pwd:TYCbtfOrBMPpfxFRgSbYnuTI\r\na=ice-options:trickle\r\na=fingerprint:sha-256 9F:45:2C:A8:C3:C0:CC:9B:59:4F:D1:02:56:52:FA:36:00:BE:C0:79:87:B3:D9:9C:3E:BF:60:98:25:B4:26:FC\r\na=setup:active\r\na=mid:0\r\na=extmap:1 urn:ietf:params:rtp-hdrext:ssrc-audio-level\r\na=extmap:2 http://www.webrtc.org/experiments/rtp-hdrext/abs-send-time\r\na=extmap:3 http://www.ietf.org/id/draft-holmer-rmcat-transport-wide-cc-extensions-01\r\na=extmap:4 urn:ietf:params:rtp-hdrext:sdes:mid\r\na=sendrecv\r\na=msid:3c28addc-03b7-4170-b5cd-535bfe767e75 38c455bc-3727-4129-b336-8cd2c6a68486\r\na=rtcp-mux\r\na=rtcp-rsize\r\na=rtpmap:111 opus/48000/2\r\na=rtcp-fb:111 transport-cc\r\na=fmtp:111 minptime=10;useinbandfec=1\r\na=rtpmap:63 red/48000/2\r\na=fmtp:63 111/111\r\na=rtpmap:9 G722/8000\r\na=rtpmap:0 PCMU/8000\r\na=rtpmap:8 PCMA/8000\r\na=rtpmap:110 telephone-event/48000\r\na=rtpmap:126 telephone-event/8000\r\na=ssrc:2430753100 cname:MPddPt/R2ioP4vCm\r\na=ssrc:2430753100 msid:3c28addc-03b7-4170-b5cd-535bfe767e75 38c455bc-3727-4129-b336-8cd2c6a68486\r\n",
     "sdp_type": "answer"
 }
}'
```

New call (using legacy connection param)

```https
curl -i -X POST 'https://graph.facebook.com/v14.0/123456789/calls' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAADUMAze4GIBO1B7B.....<REPLACE_WITH_YOUR_TOKEN>' \
-d '{
   "messaging_product": "whatsapp",
   "to": "14085550000",
   "connection": {
       "webrtc": {
           "sdp": "{\"sdp\":\"v=0\\r\\no=- 6314352886888624490 2 IN IP4 127.0.0.1\\r\\ns=-\\r\\nt=0 0\\r\\na=group:BUNDLE 0\\r\\na=extmap-allow-mixed\\r\\na=msid-semantic: WMS ccd3f422-8d7d-49c9-936c-a152979ee4fa\\r\\nm=audio 9 UDP/TLS/RTP/SAVPF 111 63 9 0 8 110 126\\r\\nc=IN IP4 0.0.0.0\\r\\na=rtcp:9 IN IP4 0.0.0.0\\r\\na=ice-ufrag:/PSS\\r\\na=ice-pwd:buBIz+JlbmakiCT7JdJIq/j0\\r\\na=ice-options:trickle\\r\\na=fingerprint:sha-256 43:08:34:16:67:E3:D9:A2:F5:AA:6A:AE:03:97:C8:D5:B8:F2:4B:40:79:C8:1A:44:53:69:4B:9C:89:88:D7:22\\r\\na=setup:active\\r\\na=mid:0\\r\\na=extmap:1 urn:ietf:params:rtp-hdrext:ssrc-audio-level\\r\\na=extmap:2 http://www.webrtc.org/experiments/rtp-hdrext/abs-send-time\\r\\na=extmap:3 http://www.ietf.org/id/draft-holmer-rmcat-transport-wide-cc-extensions-01\\r\\na=extmap:4 urn:ietf:params:rtp-hdrext:sdes:mid\\r\\na=sendrecv\\r\\na=msid:ccd3f422-8d7d-49c9-936c-a152979ee4fa 4e58b2a9-c864-4752-8f4f-23f9ced35971\\r\\na=rtcp-mux\\r\\na=rtcp-rsize\\r\\na=rtpmap:111 opus/48000/2\\r\\na=rtcp-fb:111 transport-cc\\r\\na=fmtp:111 minptime=10;useinbandfec=1\\r\\na=rtpmap:63 red/48000/2\\r\\na=fmtp:63 111/111\\r\\na=rtpmap:9 G722/8000\\r\\na=rtpmap:0 PCMU/8000\\r\\na=rtpmap:8 PCMA/8000\\r\\na=rtpmap:110 telephone-event/48000\\r\\na=rtpmap:126 telephone-event/8000\\r\\na=ssrc:3354317731 cname:zgqSj/r4rlErlW23\\r\\na=ssrc:3354317731 msid:ccd3f422-8d7d-49c9-936c-a152979ee4fa 4e58b2a9-c864-4752-8f4f-23f9ced35971\\r\\n\",\"type\":\"offer\"}"
       }
   }
}'
```

## Sample call connect webhook

Call connect webhook

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
                               "session": {
                                   "sdp_type": "answer",
                                   "sdp": "v=0\r\no=- 8076734947255960322 2 IN IP4 127.0.0.1\r\ns=-\r\nt=0 0\r\na=group:BUNDLE 0\r\na=extmap-allow-mixed\r\na=msid-semantic: WMS 68a296ba-41cc-41db-8edb-3ddf4dbbb483\r\na=ice-lite\r\nm=audio 3482 UDP/TLS/RTP/SAVPF 111 9 0 8 110 126\r\nc=IN IP4 31.13.65.130\r\na=rtcp:9 IN IP4 0.0.0.0\r\na=candidate:2754936280 1 udp 2113937151 31.13.65.130 3482 typ host generation 0 network-cost 50 ufrag kv6Jn8vBmEds/8\r\na=candidate:1581496399 1 udp 2113939711 2a03:2880:f211:d1:face:b00c:0:699c 3482 typ host generation 0 network-cost 50 ufrag kv6Jn8vBmEds/8\r\na=ice-ufrag:kv6Jn8vBmEds/8\r\na=ice-pwd:OhY8sT7v6PJe3bbs0Yx2TC/oPb5oatnK\r\na=ice-options:trickle\r\na=fingerprint:sha-256 46:14:2B:31:B1:9D:AF:15:81:E2:EF:45:B1:2B:96:3D:64:0E:63:F1:CC:9A:BD:88:D6:32:8F:E9:2A:13:3A:38\r\na=setup:active\r\na=mid:0\r\na=extmap:1 urn:ietf:params:rtp-hdrext:ssrc-audio-level\r\na=extmap:2 http://www.webrtc.org/experiments/rtp-hdrext/abs-send-time\r\na=extmap:3 http://www.ietf.org/id/draft-holmer-rmcat-transport-wide-cc-extensions-01\r\na=sendrecv\r\na=rtcp-mux\r\na=rtpmap:111 opus/48000/2\r\na=rtcp-fb:111 transport-cc\r\na=fmtp:111 minptime=10;useinbandfec=1\r\na=rtpmap:9 G722/8000\r\na=rtpmap:0 PCMU/8000\r\na=rtpmap:8 PCMA/8000\r\na=rtpmap:110 telephone-event/48000\r\na=rtpmap:126 telephone-event/8000\r\na=ssrc:433528572 cname:VBDcSNi/cg1Wg6D3\r\na=ssrc:433528572 msid:68a296ba-41cc-41db-8edb-3ddf4dbbb483 audio#wx3mq6BITjB\r\na=ssrc:433528572 mslabel:68a296ba-41cc-41db-8edb-3ddf4dbbb483\r\na=ssrc:433528572 label:audio#wx3mq6BITjB\r\n"
                               },
                               "from": "15551112222",
                               "connection": {
                                   "webrtc": {
                                       "sdp": "{\"sdp\":\"v=0\\r\\no=- 8076734947255960322 2 IN IP4 127.0.0.1\\r\\ns=-\\r\\nt=0 0\\r\\na=group:BUNDLE 0\\r\\na=extmap-allow-mixed\\r\\na=msid-semantic: WMS 68a296ba-41cc-41db-8edb-3ddf4dbbb483\\r\\na=ice-lite\\r\\nm=audio 3482 UDP/TLS/RTP/SAVPF 111 9 0 8 110 126\\r\\nc=IN IP4 31.13.65.130\\r\\na=rtcp:9 IN IP4 0.0.0.0\\r\\na=candidate:2754936280 1 udp 2113937151 31.13.65.130 3482 typ host generation 0 network-cost 50 ufrag kv6Jn8vBmEds/8\\r\\na=candidate:1581496399 1 udp 2113939711 2a03:2880:f211:d1:face:b00c:0:699c 3482 typ host generation 0 network-cost 50 ufrag kv6Jn8vBmEds/8\\r\\na=ice-ufrag:kv6Jn8vBmEds/8\\r\\na=ice-pwd:OhY8sT7v6PJe3bbs0Yx2TC/oPb5oatnK\\r\\na=ice-options:trickle\\r\\na=fingerprint:sha-256 46:14:2B:31:B1:9D:AF:15:81:E2:EF:45:B1:2B:96:3D:64:0E:63:F1:CC:9A:BD:88:D6:32:8F:E9:2A:13:3A:38\\r\\na=setup:active\\r\\na=mid:0\\r\\na=extmap:1 urn:ietf:params:rtp-hdrext:ssrc-audio-level\\r\\na=extmap:2 http://www.webrtc.org/experiments/rtp-hdrext/abs-send-time\\r\\na=extmap:3 http://www.ietf.org/id/draft-holmer-rmcat-transport-wide-cc-extensions-01\\r\\na=sendrecv\\r\\na=rtcp-mux\\r\\na=rtpmap:111 opus/48000/2\\r\\na=rtcp-fb:111 transport-cc\\r\\na=fmtp:111 minptime=10;useinbandfec=1\\r\\na=rtpmap:9 G722/8000\\r\\na=rtpmap:0 PCMU/8000\\r\\na=rtpmap:8 PCMA/8000\\r\\na=rtpmap:110 telephone-event/48000\\r\\na=rtpmap:126 telephone-event/8000\\r\\na=ssrc:433528572 cname:VBDcSNi/cg1Wg6D3\\r\\na=ssrc:433528572 msid:68a296ba-41cc-41db-8edb-3ddf4dbbb483 audio#wx3mq6BITjB\\r\\na=ssrc:433528572 mslabel:68a296ba-41cc-41db-8edb-3ddf4dbbb483\\r\\na=ssrc:433528572 label:audio#wx3mq6BITjB\\r\\n\",\"type\":\"answer\"}"
                                   }
                               },
                               "id": "wacid.HBgLMTY1MDMxMzM5NzQVAgARGCAwQTJCRDYwNkEzQUNCQUVCMEFGMzYzRTYxNjMxMDdFMxwYCzE0MDg1NTUyODk5FQIAAA==",
                               "to": "16501230000",
                               "event": "connect",
                               "timestamp": "1724467313",
                               "direction": "BUSINESS_INITIATED"
                           }
                       ],
                       "metadata": {
                           "phone_number_id": "105615555715855",
                           "display_phone_number": "15551112222"
                       },
                       "messaging_product": "whatsapp"
                   }
               }
           ],
           "id": "112735964992110"
       }
   ],
   "object": "whatsapp_business_account"
}
```
