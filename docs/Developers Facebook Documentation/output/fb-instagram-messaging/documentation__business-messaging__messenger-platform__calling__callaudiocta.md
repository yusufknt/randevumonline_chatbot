# Call Audio CTA | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/callaudiocta_

---

# Call Audio CTA

Updated: Mar 16, 2026

## Call audio CTA for generic and button template

You can use the Call-To-Action (CTA) button type `audio_call` in the Messenger API. This button type provides a new entry point for users to initiate calls with businesses by clicking the `audio_call` button directly from a button in the generic and button templates.
This `audio_call` CTA button offers enhanced customization compared to the existing call prompt template.

### Generic template

You can send this `audio_call` button using a generic template.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/652116943_1459945622530754_7316797061330323292_n.png?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=eep__rMxN4oQ7kNvwHzmzWZ&_nc_oc=AdqNGFD2GLE_cL__bmnLkLB8cLh_wLsOGzgpC40r4GL9T8Zxrodyq6anTweBw6MYtCY&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=pdimiup_cpegxBKweX20vg&_nc_ss=7b20f&oh=00_Af4ukRtV3lCxAvJOEG-OTyiel4m3QIiRjCGQFGCNITH28Q&oe=6A1C2769)

| Property | Description |
| --- | --- |
| `Page-ID`<br>string | This is the Page ID connected to the app |
| `recipient`<br>string | The Page-scoped ID of the consumer to whom the message template is requested |
| `message`<br>JSON | The body of the message |
| `attachment`<br>JSON | The XMA attachment as part of the message |
| `type`<br>string | The type of the attachment; in this case `template` |
| `payload`<br>JSON | The payload of the attachment |
| `template_type`<br>string | The type of the template, in this case `generic` |
| `elements`<br>JSON | The elements that will be used in the template |
| `buttons`<br>JSON | The buttons CTA that will be used in the template.<br>**type**: the type of the button CTA, in this case “audio_call”<br>**title (required)**: the title of the button CTA<br>**expires_in_days (default 7)**: [how long the button is clickable](https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/callsettings). The default value is 7 and cannot exceed 7 days. |

```curl
POST /<PAGE_ID>/messages
{
  "recipient": {
    "id": "<PSID>"
  },
  "message": {
    "attachment": {
      "type": "template",
      "payload": {
        "template_type": "generic",
        "elements": [
          {
            "title": "Contact Support!",
            "buttons": [
              {
                "type": "audio_call",
                "title": "Call Now",
                "expires_in_days": 5
              }
            ]
          }
        ]
      }
    }
  }
}
```

### Example response

| Property | Description |
| --- | --- |
| `id`<br>string | The Page-scoped ID of the user to whom the opt-in is requested |
| `message_id`<br>string | The external-facing message ID (mid) of the message sent |

```json
{
  "recipient": {
    "id": <PSID>,
    "message_id": <mid>,
  }
}
```

### Error response

The following errors can happen:

- Invalid page-id or psid
- The business Page hasn’t enabled the audio calling
- Permissions/Authorization errors
- The `expires_in_days` is set above 7
- Message is sent outside of allowed window

For more details on these errors, see the [Messenger Platform error codes reference](https://developers.facebook.com/documentation/business-messaging/messenger-platform/error-codes).

### Button template

You can send this `audio_call` button using a button template.

| Property | Description |
| --- | --- |
| `Page-ID`<br>string | This is the Page ID connected to the app |
| `recipient`<br>string | The Page-scoped ID of the consumer to whom the message template is requested |
| `message`<br>JSON | The body of the message |
| `attachment`<br>JSON | The XMA attachment as part of the message |
| `type`<br>string | The type of the attachment; in this case `template` |
| `payload`<br>JSON | The payload of the attachment |
| `template_type`<br>string | The type of the template, in this case `button` |
| `elements`<br>JSON | The elements that will be used in the template |
| `buttons`<br>JSON | The buttons CTA that will be used in the template.<br>**type**: the type of the button CTA, in this case “audio_call”<br>**title (required)**: the title of the button CTA<br>**expires_in_days (default 7)**: [how long the button is clickable](https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/callsettings). The default value is 7 and cannot exceed 7 days. |

```curl
POST /<PAGE_ID>/messages
{
  "recipient": {
    "id": "<PSID>"
  },
  "message": {
    "attachment": {
      "type": "template",
      "payload": {
        "template_type": "button",
        "text": "Contact Support!",
        "buttons": [
          {
            "type": "audio_call",
            "title": "Call Now",
            "expires_in_days": 5
          }
        ]
      }
    }
  }
}
```

### Example response

| Property | Description |
| --- | --- |
| `id`<br>string | The Page-scoped ID of the user to whom the opt-in is requested |
| `message_id`<br>string | The external-facing message ID (mid) of the message sent |

### Error response

The following errors can happen:

- Invalid page-id or psid
- The business Page hasn’t enabled the audio calling
- Permissions/Authorization errors
- The `expires_in_days` is set above 7
- Message is sent outside of allowed window

For more details on these errors, see the [Messenger Platform error codes reference](https://developers.facebook.com/documentation/business-messaging/messenger-platform/error-codes).
