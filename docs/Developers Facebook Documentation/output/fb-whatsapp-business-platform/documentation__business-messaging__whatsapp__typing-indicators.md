# Typing indicators | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/typing-indicators_

---

# Typing indicators

Updated: Oct 21, 2025

When you get a **messages** webhook indicating a [received message](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages), you can use the `message.id` value to mark the message as read and display a typing indicator so the WhatsApp user knows you are preparing a response. This is good practice if it will take you a few seconds to respond.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/488360772_654124507349470_2240843625651955811_n.png?_nc_cat=110&ccb=1-7&_nc_sid=e280be&_nc_ohc=HglXs-ME1DsQ7kNvwGXuqUZ&_nc_oc=AdqZSFu8HwDXebycSx_Rjm2a2Wl5Al1wcmRYpe0LVwBSc-aNbtz7ztKESq2jk6hV1DQ&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=4DERkl3JBvpMiEr4ih2X4Q&_nc_ss=7b20f&oh=00_Af6ULbZkThHMajbI5HMItXkipKk2Rc_QIJklb3QdeuCtfw&oe=6A1C145C)

The typing indicator will be dismissed once you respond, or after 25 seconds, whichever comes first. To prevent a poor user experience, only display a typing indicator if you are going to respond.

## Request syntax

```html
curl -X POST \
'https://graph.facebook.com/<API_VERSION>/<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>/messages'
-H 'Authorization: Bearer <ACCESS_TOKEN>' \
-H 'Content-Type: application/json' \
-d '
{
  "messaging_product": "whatsapp",
  "status": "read",
  "message_id": "<WHATSAPP_MESSAGE_ID>",
  "typing_indicator": {
    "type": "text"
  }
}'
```

## Request parameters

| Placeholder | Description | Example value |
| --- | --- | --- |
| `<ACCESS_TOKEN>`<br>*String* | **Required.**<br>[System token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens) or [business token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens). | `EAAA...` |
| `<API_VERSION>`<br>*String* | **Optional.**<br>Graph API version. | v25.0 |
| `<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>`<br>*String* | **Required.**<br>WhatsApp business phone number ID. | `106540352242922` |
| `<WHATSAPP_MESSAGE_ID>`<br>*String* | **Required.**<br>WhatsApp message ID. This ID is assigned to the `messages.id` property in **received message** [messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages) webhooks. | `wamid.HBgLMTY1MDM4Nzk0MzkVAgARGBJDQjZCMzlEQUE4OTJBMTE4RTUA` |

## Response

Upon success:

```json
{
  "success": true
}
```

## Example request

```curl
curl 'https://graph.facebook.com/v25.0/106540352242922/messages' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "messaging_product": "whatsapp",
  "status": "read",
  "message_id": "wamid.HBgLMTY1MDM4Nzk0MzkVAgARGBJDQjZCMzlEQUE4OTJBMTE4RTUA",
  "typing_indicator": {
    "type": "text"
  }
}'
```

## Response

Upon success:

```json
{
  "success": true
}
```
