# Mark messages as read | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/mark-message-as-read_

---

# Mark messages as read

Updated: Nov 3, 2025

When you get a **messages** webhook indicating an [incoming message](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api), you can use the `message.id` value to mark the message as read.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/491643461_603380552708521_8284248965365504291_n.png?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=_mrSzwZxTVsQ7kNvwHy65A7&_nc_oc=Adq-GkfjMIFueLzUK5bOlh36eZ0JzlOb-s8Z1EukafM3nHtdP5hPibFbLjZitzQ7bk4&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=XWk_xH5eKi0IrshRT-84-A&_nc_ss=7b20f&oh=00_Af4T_PPfqksSwxc_4s5l98LMFDs4Yw2yjAultg1dux5SIw&oe=6A1C2670)

It’s good practice to mark an incoming messages as read within 30 days of receipt. Marking a message as read will also mark earlier messages in the thread as read.

## Request syntax

Use the [Messages API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api#post-version-phone-number-id-messages) to mark a message as read.

```html
curl -X POST \
'https://graph.facebook.com/<API_VERSION>/<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>/messages'
-H 'Authorization: Bearer <ACCESS_TOKEN>' \
-H 'Content-Type: application/json' \
-d '
{
  "messaging_product": "whatsapp",
  "status": "read",
  "message_id": "<WHATSAPP_MESSAGE_ID>"
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
  "message_id": "wamid.HBgLMTY1MDM4Nzk0MzkVAgARGBJDQjZCMzlEQUE4OTJBMTE4RTUA"
}'
```

## Example response

```json
{
  "success": true
}
```
