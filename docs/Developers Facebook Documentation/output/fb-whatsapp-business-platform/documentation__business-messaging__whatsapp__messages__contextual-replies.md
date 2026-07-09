# Contextual replies | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/contextual-replies_

---

# Contextual replies

Updated: Oct 21, 2025

Contextual replies are a special way of responding to a WhatsApp user message. Sending a message as a contextual reply makes it clearer to the user which message you are replying to by quoting the previous message in a contextual bubble:

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/441349069_1363509007609494_6528221959622289637_n.png?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Cbh6OS-UtgQQ7kNvwEFeGr_&_nc_oc=AdqnvELwYGGJ_gFdVHV0TfzGUVGNtyA6_9z6ACwDOZG94XlxzuWSivaf6ey2rZi0dmw&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=z44M62hjhitfbVI2l4DilQ&_nc_ss=7b20f&oh=00_Af5yaH-Cl0gFaH8qdRD7_7OSspfB8Vlu6CrgGfY8Nv1u1A&oe=6A1C2A6B)

## Limitations

- You cannot send a [reaction message](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/reaction-messages) as a contextual reply.

The contextual bubble will not appear at the top of the delivered message if:

- The previous message has been deleted or moved to long term storage (messages are typically moved to long term storage after 30 days, unless you have enabled [local storage](https://developers.facebook.com/documentation/business-messaging/whatsapp/local-storage) ).
- You reply with an [audio](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/audio-messages) , [image](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/image-messages) , or [video message](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/video-messages) and the WhatsApp user is running KaiOS.
- You use the WhatsApp client to reply with a [push-to-talk](https://faq.whatsapp.com/657157755756612/?cms_platform=web) message and the WhatsApp user is running KaiOS.
- You reply with a [template message](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview) .

## Request Syntax

```https
POST /<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>/messages
```

### Post Body

```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "<WHATSAPP_USER_PHONE_NUMBER>",
  "context": {
    "message_id": "WAMID_TO_REPLY_TO"
  },

  /* Message type and type contents goes here */

}
```

### Post Body Parameters

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<WAMID_TO_REPLY_TO>`<br>*String* | **Required.**<br>WhatsApp message ID (wamid) of the previous message you want to reply to. | `wamid.HBgLMTY0NjcwNDM1OTUVAgASGBQzQTdCNTg5RjY1MEMyRjlGMjRGNgA=` |
| `<WHATSAPP_USER_PHONE_NUMBER>`<br>*String* | **Required.**<br>WhatsApp user phone number. | `+16505551234` |

## Example Request

Example of a text message sent as a reply to a previous message.

```curl
curl 'https://graph.facebook.com/v19.0/106540352242922/messages' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "+16505551234",
  "context": {
    "message_id": "wamid.HBgLMTY0NjcwNDM1OTUVAgASGBQzQTdCNTg5RjY1MEMyRjlGMjRGNgA="
  },
  "type": "text",
  "text": {
    "body": "You'\''re welcome, Pablo!"
  }
}'
```
