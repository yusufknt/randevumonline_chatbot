# Configure Call Settings

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/call-settings_

---

# Configure Call Settings

Updated: Mar 23, 2026

## Overview

Calling is not enabled by default on a business phone number. To enable calling, your business must have a [messaging limit](https://developers.facebook.com/documentation/business-messaging/whatsapp/messaging-limits) of 2000 or above.

Use these endpoints to view and configure call settings for the Calling API.

You can also [configure session initiation protocol (SIP)](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/sip) for call signaling instead of using Graph API endpoint calls and webhooks.

## Configure/Update business phone number calling settings

Use this endpoint to update call settings configuration for an individual business phone number.

### WhatsApp clients reflecting latest calling config**

After you update call configuration, WhatsApp users may take up to 7 days to reflect those changes. Most users refresh much sooner. You can force an immediate refresh in WhatsApp by entering the chat window with business and open the chat info page. Regardless of WhatsApp client behavior, the semantics of settings are still honored on the server side.

### Request syntax

```https
POST /<PHONE_NUMBER_ID>/settings
```

### Endpoint parameters

| Placeholder | Description | Sample Value |
| --- | --- | --- |
| `<PHONE_NUMBER_ID>`<br>*Integer* | **Required**<br>ID of the business phone number for which you are updating Calling API settings. | `106540352242922` |

### Request body

`{
 "calling": {
 "status": "ENABLED",
 "call_icon_visibility": "DEFAULT",
 "call_icons": {
 "restrict_to_user_countries": [
 "US",
 "BR"
 ]
 },
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
 },
 "audio": {
 "additional_codecs": ["PCMA", "PCMU"]
 }
 }
}`

### Body parameters

| Parameter | Description | Sample Value |
| --- | --- | --- |
| `status`<br>*String* | **Optional**<br>Enable or disable the Calling API for the given business phone number. | `“ENABLED”`<br>`“DISABLED”` |
| `call_icon_visibility`<br>*String* | **Optional**<br>Configure whether the WhatsApp call button icon displays for users when chatting with the business.<br>[View call icon visibility behavior details below](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/call-settings#call-icons) | [View call icon visibility behavior details below](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/call-settings#call-icons) |
| `call_icons`<br>*String* | **Optional**<br>Configure whether WhatsApp call button icon displays for users when chatting with the business.<br>[View call icons visibility behavior details below](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/call-settings#call-icons) | [View call icons behavior details below](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/call-settings#call-icons) |
| `call_hours`<br>*JSON object* | **Optional**<br>Allows you to specify and trigger call settings for incoming calls based on your timezone, business operating hours, and holiday schedules.<br>Any previously configured values in `call_hours` will be replaced with the values passed in the request body of this API call.<br>[View call hours behavior details below](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/call-settings#call-hours) | [View call hours behavior details below](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/call-settings#call-hours) |
| `callback_permission_status`<br>*String* | **Optional**<br>Configure whether a WhatsApp user is prompted with a call permission request after calling your business.<br>Note: The call permission request is triggered from either a missed or connected call.<br>[View callback permission status behavior details below](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/call-settings#callback-permissions) | `“ENABLED”`<br>`“DISABLED”` |
| `sip`<br>*JSON object* | **Optional**<br>Configure call signaling via signal initiation protocol (SIP).<br>**Note: When SIP is enabled, you cannot use calling related endpoints and will not receive calling related webhooks.**<br>[Learn how to configure and use SIP call signaling](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/sip) | View [Configure SIP settings on business phone number](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/sip#configure-or-update-sip-settings-on-business-phone-number) |
| `audio`<br>*JSON object* | **Optional**<br>Configure call audio codec settings. Opus is the default codec and is always present.<br>[View audio codec details below](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/call-settings#audio-codec) | `"audio": {<br> "additional_codecs": [<br> "PCMA", "PCMU"<br> ]<br>}` |

### Calling status

When the `status` parameter is set to `“ENABLED”`, calling features are enabled for the business phone number. WhatsApp client applications will render the call button icon in both the business chat and business chat profile.

When the `status` parameter is set to `“DISABLED”`, calling features are **disabled**, and both the business chat and business chat profile **do not display the call button icon.**

Updates to `status` will update the call button icon in existing business chats in near real-time when the business phone number is in the WhatsApp user’s contacts.

Otherwise, updates are real-time for a limited number of users in conversation with the business, and are eventual for the rest of the conversations.

Call button icon visibility

When Calling API features are enabled for a business number, you can still choose whether to show the call button icon or not by using the `call_icon_visibility` parameter. Note: Disabling call button icon visibility **does not** disable a WhatsApp user’s ability to make unsolicited calls to your business.

The behavior for supported options is as follows:

`DEFAULT`

The Call button icon will be displayed in the chat menu bar and the business info page, allowing for unsolicited calls to the business by WhatsApp users.

![Screenshot showing call button icon displayed in WhatsApp chat](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/560917504_1339317971260187_5308835930412534329_n.jpg?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=xQyVLeUpUhgQ7kNvwGebcB8&_nc_oc=AdqoJ5pkgjtGQ6hr2jzFMVh041R0m9eZuf6eS4VRu5PbDG9WUL-iMkSEMe26o2uw-80&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=eL7TNZfgvdpgD3iJ7wzm7g&_nc_ss=7b20f&oh=00_Af4CETOC8PxYxHbSrRNI9gfUA-Xog0ccC5UBS8BhoSdwRg&oe=6A1C1A41)

`DISABLE_ALL`

The call button icon is hidden in the chat menu bar and the business info page, and all other entry points external to the chat are also disabled. Consumers cannot make unsolicited calls to the business.

Your business can still [send interactive messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/call-button-messages-deep-links#send-interactive-message-with-a-whatsapp-call-button) or [template messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/call-button-messages-deep-links#create-and-send-whatsapp-call-button-template-message) with a Calling API CTA button.

![Screenshot showing hidden call button icon in WhatsApp chat](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/560585020_1339317941260190_3863205212606668279_n.jpg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=hvH2L81YjrsQ7kNvwGPX8q6&_nc_oc=Adqgfm6pg05CpxSlDnhJqxB33Pe3Tb-gdZF0GlOrBG8oVf3_hbs9K2rmkNZ6kljurEk&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=eL7TNZfgvdpgD3iJ7wzm7g&_nc_ss=7b20f&oh=00_Af6N9bIDrP3EUfDjZ0RNrWBVkcxvGhKEE4kYWWEVMxtDwQ&oe=6A1C27C4)

### Callback permissions

Calling a WhatsApp user requires explicit permission from the user. One way to obtain calling permissions is to request permission when a WhatsApp user calls your business.

You can configure the call permission UI to automatically show in the WhatsApp user’s client app when they call your business number. The user may change their permission selection at any time.

![Diagram showing callback permissions flow in WhatsApp](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/602352272_1389874706204513_7741631937402058550_n.jpg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=Z5ttGfRVSJAQ7kNvwHYG-cS&_nc_oc=Adq1PhODbrFd1jFwCb4kwsX-701VpcTgexV5V0f_2gQ5hpMUeTr6i2pXA_-niOU4MR8&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=eL7TNZfgvdpgD3iJ7wzm7g&_nc_ss=7b20f&oh=00_Af76V89aotJEGd-jxCLKCaRDqaJvTORtxhD6w01P66RPpw&oe=6A1C261A)

### Call icons

With the `call_icons` setting, you can specify the countries where these icons should show up.

```curl
"call_icons": {
  "restrict_to_user_countries": [
    "US",
    "BR"
  ]
}
```

| Parameter | Description | Sample Values |
| --- | --- | --- |
| `restrict_to_user_countries`<br>*List of Strings* | **Optional**<br>Restrict the visibility of call icons to these countries.<br>*NOTE: For example if you restrict it to “US,” then it will apply to all the people who have a US registered phone number. These people could be physically located inside or outside of the USA.* | Restrict to US and Brazil:<br>`"restrict_to_user_countries": [<br> "US",<br> "BR"<br>]`<br>No restriction:<br>`"restrict_to_user_countries": []` |

### Call hours

With the `call_hours` setting, you can specify the timezone, business operating hours, and holiday schedules that will be enforced for all user-initiated calls.

Configuring this setting restricts calls only to available weekly hours you configure. User-initiated calls are unavailable outside of the weekly hours and holiday schedules you set.

The WhatsApp client app will show users an option to chat with the business, or request a callback, if `callback_permission_status` is `ENABLED`. The user will also be shown the next available calling slot on the option screen.

![Screenshot showing call hours unavailable message in WhatsApp](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/561822470_1339317924593525_4183355843280485487_n.jpg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=I0UhGIogB-QQ7kNvwEiCONt&_nc_oc=AdoYC6f6XQUAvytLvo3QDAwpLZmXJ5llnpRWW43WdanQwdhbUckKnlBV5qscgYI3HjQ&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=eL7TNZfgvdpgD3iJ7wzm7g&_nc_ss=7b20f&oh=00_Af4iXZeOq_wiDkpxCaCDx69PffwoZwYASWSQYxz7ns52dA&oe=6A1BFC27)

```curl
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
}
```

| Parameter | Description | Sample Values |
| --- | --- | --- |
| `status`<br>*String* | **Required**<br>Enable or disable the call hours for the business.<br>If call hours are disabled, the business is considered open all 24 hours of the day, 7 days a week. | `“ENABLED”`<br>`“DISABLED”` |
| `timezone_id`<br>*String* | **Required**<br>The timezone that the business is operating within.<br>[Learn more about supported values for `timezone_id`](https://developers.facebook.com/docs/facebook-business-extension/fbe/reference#time-zones) | `“America/Menominee”`<br>`“Asia/Singapore”` |
| `weekly_operating_hours`<br>*List of JSON object* | **Required**<br>The operating hours schedule for each day of the week.<br>Each entry is a JSON object with 3 key/value pairs:<br>`day_of_week` — (*Enum*) **[Required]**<br>The day of the week.<br>Can take one of seven values: `"MONDAY"`, `“TUESDAY”`, `“WEDNESDAY”`, `“THURSDAY”`, `“FRIDAY”`, `“SATURDAY”`, `“SUNDAY”`<br>`open_time``close_time` — (*Integer*) **[Required]**<br>Opening and closing times represented in 24 hour format, for example `"1130"` = 11:30AM<br>Maximum of 2 entries allowed per day of week`open_time` must be before `close_time`Overlapping entries not allowed | `{<br>"day_of_week": "MONDAY",<br>"open_time": "0400",<br>"close_time": "1020"<br>},<br>{<br>"day_of_week":"TUESDAY",<br>"open_time": "0108",<br>"close_time": "1020"<br>}<br>...` |
| `holiday_schedule`<br>*String* | **Optional**<br>An optional override to the weekly schedule.<br>Up to 20 overrides can be specified.<br>Note: If `holiday_schedule` is not passed in the request, then the existing `holiday_schedule` will be deleted and replaced with an empty schedule.<br>`date` — (*String*) **[Required]**<br>Date for which you want to specify the override.<br>YYYY-MM-DD format.<br>`open_time``close_time` — (*Integer*) **[Required]**<br>Opening and closing times represented in 24 hour format, for example, `”1130”` = 11:30AM<br>Maximum of 2 entries allowed per day of week`open_time` must be before `close_time`Overlapping entries not allowed | `{<br>"date": "2026-01-01",<br>"start_time": "0000",<br>"end_time": "2359",<br>}<br>...` |

Audio codecOpus is the default audio codec for all WhatsApp calls. You can enable G.711 (PCMA/PCMU) codecs for interoperability with legacy telephony systems or PSTN gateways.Guidelines and considerations**Opus is the recommended codec.** Opus delivers higher audio quality with lower bandwidth usage and is the default for all WhatsApp calls. Use Opus unless you have a specific requirement for G.711.**G.711 requires transcoding.** When a G.711 codec is negotiated, audio is transcoded between Opus (on the WhatsApp user side) and G.711 (on the business side), which can add latency to the call.**G.711 has lower audio quality.** G.711 encodes audio at a fixed 64 kbps without advanced compression, resulting in lower fidelity compared to Opus.**G.711 uses more bandwidth.** G.711 requires approximately 64 kbps per direction, while Opus achieves comparable or better quality at significantly lower bitrates.**Use G.711 only when necessary.** The primary use case is interoperability with legacy telephony infrastructure and PSTN gateways that do not support Opus.`"audio": {
 "additional_codecs": ["PCMA", "PCMU"]
}`

| Parameter | Description | Sample Values |
| --- | --- | --- |
| `additional_codecs`<br>*List of Strings* | **Optional**<br>Enable additional audio codecs. Supported values: `"PCMA"` (G.711 A-law), `"PCMU"` (G.711 µ-law). Opus is always enabled by default and cannot be removed. After enabling additional codecs, they can be selected during SDP codec negotiation according to RFC 3264. | `"additional_codecs": [<br> "PCMA",<br> "PCMU"<br>]`<br>No additional codecs:<br>`"additional_codecs": []` |

### Success response

```curl
{
  "success": true
}
```

### Error response

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

[View Calling API Error Codes and Troubleshooting for more information](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/troubleshooting)

[View general Cloud API Error Codes here](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/error-codes)

## Get phone number calling settings

Use this endpoint to check the configuration of your Calling API feature settings.

This endpoint can return information for other Cloud API feature settings.

### Request syntax

```https
GET /<PHONE_NUMBER_ID>/settings
```

### Endpoint parameters

| Parameter | Description | Sample Value |
| --- | --- | --- |
| `<PHONE_NUMBER_ID>`<br>*Integer* | **Required**<br>ID of the business phone number for which you are getting Calling API settings. | `106540352242922` |

### App permission required

`whatsapp_business_management`: Advanced access is required to use the API for end business clients

### Response body

`{
 "calling": {
 "status": "ENABLED",
 "call_icon_visibility": "DEFAULT",
 "callback_permission_status": "ENABLED",
 "call_hours": {
 "status": "ENABLED",
 "timezone_id": "[REDACTED]",
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
 "sip": {
 "status": "ENABLED",
 "servers": [
 {
 "hostname": "[REDACTED]",
 "sip_user_password": "[REDACTED]"
 }
 ]
 },
 "audio": {
 "additional_codecs": ["PCMA", "PCMU"]
 }
 },
 <Other non-calling feature configuration...>
}`

### Include SIP user password in response

Optionally, you can include SIP user credentials in your response body by adding the SIP credentials query parameter in the POST request:

```https
GET /<PHONE_NUMBER_ID>/settings?include_sip_credentials=true
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

### Response details

The [Settings API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/settings-api#get-version-phone-number-id-settings) returns Calling API settings, along with other configuration information for your WhatsApp business phone number.

[Learn more about Calling API settings and their values](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/call-settings#body-parameters)

Response with calling restrictions

If your business has restrictions enforced, the response body contains information about the restriction along with other calling API settings.

```curl
 {
   "calling": {
     ... // other calling api settings
     "restrictions": {
       "restrictions_list": [
         {
           "type": "[RESTRICTED_BUSINESS_INITIATED_CALLING|RESTRICTED_USER_INITIATED_CALLING]",
           "reason": "Business|User initiated calling capability has been temporarily disabled for this phone number due to high negative feedback from users.",
           "expiration": 1754072386
         }
       ]
     }
   }
}
```

| Parameter | Description |
| --- | --- |
| `<restrictions>`<br>*JSON Object* | The restrictions object contains the following values:<br>`restriction_list` *(JSON Object)*: list of currently imposed restrictions with the following values<br>`type` *(string)* - for calling restriction, this would have the value of `RESTRICTED_BUSINESS_INITIATED_CALLING` or `RESTRICTED_USER_INITIATED_CALLING`<br>`reason` *(string)* - description of restriction<br>`expiration` *(Integer)* - The UNIX time at which the restriction will expire in UTC timezone |

### Error response

Possible errors that can occur:

- Permissions/Authorization errors

[View Calling API Error Codes and Troubleshooting for more information](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/troubleshooting)

[View general Cloud API Error Codes here](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/error-codes)

## Call settings in WhatsApp Manager

You can also control your call settings via [WhatsApp Manager](https://business.facebook.com/latest/whatsapp_manager/).

To access calling controls in WhatsApp Manager:

1. Click on **Account tools** > **Phone numbers** panel
2. Click the gear icon next to the phone number you are using for calling
3. Click the **Calls** tab

![Screenshot of WhatsApp Manager call settings interface](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/560806366_1339318237926827_2957205066303057693_n.jpg?_nc_cat=106&ccb=1-7&_nc_sid=e280be&_nc_ohc=tXPHKW_uNmsQ7kNvwGQ_-mA&_nc_oc=AdqjTnzixVjBilDtjUDymitPV1NamjplOlt-fz6zjzCk-VNcFDyAfaTAbBMtFjZzsVI&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=eL7TNZfgvdpgD3iJ7wzm7g&_nc_ss=7b20f&oh=00_Af7DMACjMjpOUxyKniOlS-OpV-3diI-PghjNeW0ZAU5bCQ&oe=6A1C0A3A)

## Configure and use call signaling via session initiation protocol (SIP)

Session Initiation Protocol (SIP) is a signaling protocol used for initiating, maintaining, modifying, and terminating real-time communication sessions between two or more endpoints. You can send and receive call signals using SIP instead of Graph API endpoints.

[Learn more about how to use and configure SIP](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/sip)

## Settings update webhooks

You can subscribe to a new webhook subscription field `account_settings_update` to get notified on updates to phone number settings.

- You’ll be notified even for your own updates
- Currently, only changes to calling settings are supported. Under the calling object, only changes to these fields are observed: status, call_icon_visibility, callback_permission_status, sip.status, and srtp_key_exchange_protocol.

### Steps to get started

- [Set up your webhook subscription](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/create-webhook-endpoint#configure-webhooks) and subscribe to the `account_settings_update` field.
- The same app should also be subscribed to the WhatsApp Business Account of your business phone number.
- Your app should have `whatsapp_business_management` permission to receive the webhooks. Using access token for the same app, if you’re able to [get settings](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/call-settings#get-phone-number-calling-settings) successfully, your app is good to receive the webhooks too.

### Webhook payload

```https
{
    "object": "whatsapp_business_account",
    "entry": [
        {
            "id": "whatsapp-business-account-id",
            "changes": [
                {
                    "value": {
                        "messaging_product": "whatsapp",
                        "timestamp": "1671644824",
                        "type": "[phone_number_settings]",
                        "phone_number_settings": {
                            "phone_number_id": "phone-number-id",
                            "calling": {
                                "status": "ENABLED",
                                "call_icon_visibility": "DEFAULT",
                                "callback_permission_status": "ENABLED",
                                "call_hours": {
                                    "status": "ENABLED",
                                    "timezone_id": "[REDACTED]",
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
                                "sip": {
                                    "status": "ENABLED",
                                    "servers": [
                                        {
                                            "hostname": "[REDACTED]",
                                            "port": SIP_SERVER_PORT
                                        }
                                    ]
                                }
                            }
                        }
                    },
                    "field": "account_settings_update"
                }
            ]
        }
    ]
}
```

### Webhook values

| Placeholder | Description |
| --- | --- |
| `messaging_product`<br>*String* | Always `whatsapp` for now |
| `timestamp`<br>*Integer* | Time when the settings got updated |
| `type`<br>*String* | Type of the change. Currently only `PHONE_NUMBER_SETTINGS` |
| `phone_number_settings`<br>*Object* | This field is present if the type is `PHONE_NUMBER_SETTINGS`. Currently only `calling` sub-field under this is supported. |
| `phone_number_settings.phone_number_id`<br>*String* | The phone number id, whose settings got updated |
| `phone_number_settings.calling`<br>*Object* | This is present only if fields related to `calling` are updated. It’s null otherwise. When present, the payload is same as [Get settings API](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/call-settings#get-phone-number-calling-settings) |

## Calling restrictions for user feedback

If your calls receive a high negative user feedback, such as blocks and reports, business initiated calling, user initiated calling, or both functionalities on your phone number can be restricted.

### Early warning

You will be notified when the business phone number is close to being paused as an early warning. The early warning notifications will be communicated via below channels

Email

Enforcement emails are sent to the email addresses of all users and admins associated with the business.
If you did not receive an email, confirm which email you have designated as the contact email for your app and make sure that it is active, can receive new email, and does not flag the email as junk or spam mail.

Webhook

A webhook will be sent on the `account_update` field:

```curl
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "0",
      "time": 1623862418,
      "changes": [
        {
          "field": "account_update",
          "value": {
            "phone_number": "PN",
            "event": "ACCOUNT_VIOLATION",
            "violation_info": {
               "violation_type": "[LOW_BUSINESS_INITIATED_CALLING_QUALITY|LOW_USER_INITIATED_CALLING_QUALITY]",
            }
          }
        }
      ]
    }
  ]
}
```

If either business or user initiated calling are close to being paused, you will receive a webhook for the respective violation type. Refer [account_update](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/account_update) for information about the webhook.

### Pause in calling functionality

Once the negative user feedback reaches a threshold, Cloud API will automatically restrict calling functionality on your phone number for a period of 7 days. While paused the calling phone number will be unable to

- *Make business initiated calls to users*
- *Send call permissions requests*

Once your phone number has been paused, notifications will be communicated via below channels.

Note: Any call permissions approved or declined by the users while paused, will still be valid.

Email

Enforcement emails are sent to the email addresses of all users and admins associated with the business.
If you did not receive an email, confirm which email you have designated as the contact email for your app and make sure that it is active, can receive new email, and does not flag the email as junk or spam mail.

Webhook

A webhook will be sent on the `account_update` field:

```curl
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "0",
      "time": 1641848059,
      "changes": [
        {
          "field": "account_update",
          "value": {
            "phone_number": "PN",
            "event": "ACCOUNT_RESTRICTION",
            "restriction_info": [
              {
                "restriction_type": "RESTRICTED_BUSINESS_INITIATED_CALLING",
                "expiration": 1641848057
              }
            ]
          }
        }
      ]
    }
  ]
}
```

Refer [account_update](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/account_update) for information about the webhook.

### Pause in user initiated calling functionality

Once the negative user feedback reaches a threshold, Cloud API will automatically restrict user initiated calling functionality on your phone number for a period of 7 days. While paused the calling phone number will be unable to

- *Receive calls from users*
- *Have call icon visible*

Once your phone number has been paused, notifications will be communicated via below channels.

Email

Enforcement emails are sent to the email addresses of all users and admins associated with the business.
If you did not receive an email, confirm which email you have designated as the contact email for your app and make sure that it is active, can receive new email, and does not flag the email as junk or spam mail.

Webhook

A webhook will be sent on the `account_update` field:

```curl
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "0",
      "time": 1641848059,
      "changes": [
        {
          "field": "account_update",
          "value": {
            "phone_number": "PN",
            "event": "ACCOUNT_RESTRICTION",
            "restriction_info": [
              {
                "restriction_type": "RESTRICTED_USER_INITIATED_CALLING",
                "expiration": 1641848057
              }
            ]
          }
        }
      ]
    }
  ]
}
```

Refer [account_update](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/account_update) for information about the webhook.

## Calling restrictions for low call pickup rates

When calling is enabled on your business phone number, you are expected to pick up calls that users place to you.

If a significant number of calls placed to your calling-enabled business phone number are not picked up, you will be notified and expected to make a change.

### What happens if you do not pick up calls

1. **Warning via Email:** You receive an email notification with options to change how you handle incoming calls.
2. **Calling becomes restricted on the business phone number:** The calling button will be hidden from users.

### How to mitigate the situation

If you receive a warning

- **Continue allowing users to call:** Please identify and address the cause of calls not being picked up and make sure you are properly resourced to handle expected call volumes.
- **Hide call buttons for user-initiated calls:** You can do so either by working with your partner or going to [WhatsApp Manager](https://business.facebook.com/latest/whatsapp_manager/overview/) > Account tools > Phone numbers > select Phone number [WA phone number] > Calls > toggle off Display call buttons.
- **Turn off calling altogether:** You can do so either by working with your partner or going to [WhatsApp Manager](https://business.facebook.com/latest/whatsapp_manager/overview/) > Account tools > Phone numbers > select Phone number [WA phone number] > Calls > toggle off Allow voice calls.

If the call button is hidden for the business phone number

- **Re-display calling buttons:** Please identify and address the cause of calls not being picked up and make sure you are properly resourced to handle expected call volumes.Next, display the calling buttons by either working with your partner or going to [WhatsApp Manager](https://business.facebook.com/latest/whatsapp_manager/overview/) > Account tools > Phone numbers > select Phone number [WA phone number] > Calls > toggle on Display call buttons.
- **Turn off calling altogether:** You can do so either by working with your partner or going to [WhatsApp Manager](https://business.facebook.com/latest/whatsapp_manager/overview/) > Account tools > Phone numbers > select Phone number [WA phone number] > Calls > toggle off Allow voice calls.

### Webhooks

Warning webhook

```curl
[
  {
    "object": "whatsapp_business_account",
    "entry": [
      {
        "id": "0",
        "time": 1641848059,
        "changes": [
          {
            "field": "account_update",
            "value": {
              "phone_number": "16505552771",
              "event": "ACCOUNT_VIOLATION",
              "violation_info": {
                "violation_type": "USER_INITIATED_CALLS_LOW_PICKUP_RATE",
                "remediation": "Please identify and address the cause of user-initiated calls not being picked up and make sure the business is properly resourced to handle expected call volumes."
              }
            }
          }
        ]
      }
    ]
  }
]
```

Enforcement webhook

```curl
[
  {
    "object": "whatsapp_business_account",
    "entry": [
      {
        "id": "0",
        "time": 1641848059,
        "changes": [
          {
            "field": "account_update",
            "value": {
              "phone_number": "16505552771",
              "event": "ACCOUNT_RESTRICTION",
              "restriction_info": [
                {
                  "restriction_type": "RESTRICTED_USER_INITIATED_CALLING_CALL_BUTTON_HIDDEN",
                  "remediation": "The call button has been hidden due to low pickup rates. Please identify and address the cause of user-initiated calls not being picked up.  Next, display the calling buttons by either working with your partner or going to WhatsApp Manager > Account tools > Phone numbers > select Phone number > Calls > toggle on Display call buttons"
                }
              ]
            }
          }
        ]
      }
    ]
  }
]
```
