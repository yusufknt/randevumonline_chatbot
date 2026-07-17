# Call button | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/buttons/call_

---

# Call button

Updated: Apr 22, 2026

The call button dials a phone number when tapped. The phone number must be in the format `+<COUNTRY_CODE><PHONE_NUMBER>`, for example `+15105559999`.

## Supported usage

The call button is supported for use with the following:

- Generic template
- List template
- Button template
- Media template

## Properties

| Property | Type | Description |
| --- | --- | --- |
| `type` | String | Type of button. Must be<br>`phone_number`<br>. |
| `title` | String | Button title. 20 character limit. |
| `payload` | String | Phone number to dial. Format must have<br>`+`<br>prefix followed by the country code, area code, and local number. For example,<br>`+16505551234`<br>. |

## Sample request

```curl
curl -X POST -H "Content-Type: application/json" -d '{
  "recipient":{
    "id":"<PSID>"
  },
  "message":{
    "attachment":{
      "type":"template",
      "payload":{
        "template_type":"button",
        "text":"Need further assistance? Talk to a representative",
        "buttons":[
          {
            "type":"phone_number",
            "title":"Call Representative",
            "payload":"+15105551234"
          }
        ]
      }
    }
  }
}' "https://graph.facebook.com/me/messages?access_token=<PAGE_ACCESS_TOKEN>"
```

## Sample response

```js
{
  "recipient_id": "1254477777772919",
  "message_id": "AG5Hz2Uq7tuwNEhXfYYKj8mJEM_QPpz5jdCK48PnKAjSdjfipqxqMvK8ma6AC8fplwlqLP_5cgXIbu7I3rBN0P"
}
```
