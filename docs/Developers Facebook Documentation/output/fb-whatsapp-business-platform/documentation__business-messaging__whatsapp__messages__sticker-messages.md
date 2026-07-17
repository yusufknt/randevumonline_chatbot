# Sticker messages | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/sticker-messages_

---

# Sticker messages

Updated: Nov 3, 2025

Sticker messages display animated or static sticker images in a WhatsApp message.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/441292863_1203428507688350_9164958282076997505_n.png?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=BPcs42RS55YQ7kNvwG0xv7t&_nc_oc=Adq53nBoBhk9cMNI9UPqOHCzQs2Ig2yGef9kImY6g4k-GXy35bWkzoCQhtSaa8c2Zrg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=Yyheqvrqb-0cA6BMsXQGDg&_nc_ss=7b20f&oh=00_Af7M5tVQE7J8-63JCOhTmt3OGVg_KGqLMJDQqYNKio-bcg&oe=6A1C0F7C)

## Request syntax

Use the [Messages API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api#post-version-phone-number-id-messages) to send a sticker message to a WhatsApp user.

```html
curl 'https://graph.facebook.com/<API_VERSION>/<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>/messages' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <ACCESS_TOKEN>' \
-d '
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "<WHATSAPP_USER_PHONE_NUMBER>",
  "type": "sticker",
  "sticker": {
    "id": "<MEDIA_ID>", <!-- Only if using uploaded media -->
    "link": "<MEDIA_URL>", <!-- Only if using hosted media (not recommended) -->
  }
}'
```

### Post Body Parameters

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<ACCESS_TOKEN>`<br>*String* | **Required.**<br>[System token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens) or [business token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens). | `EAAA...` |
| `<API_VERSION>`<br>*String* | **Optional.**<br>Graph API version. | v25.0 |
| `<MEDIA_ID>`<br>*String* | **Required if using uploaded media, otherwise omit.**<br>ID of the [uploaded media asset](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/media#upload-media). | `1013859600285441` |
| `<MEDIA_URL>`<br>*String* | **Required if using hosted media, otherwise omit.**<br>URL of the media asset hosted on your public server. For better performance, we recommend using `id` and an [uploaded media asset ID](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/media#upload-media) instead. | `https://www.luckyshrub.com/assets/animated-smiling-plant.webp` |
| `<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>`<br>*String* | **Required.**<br>WhatsApp business phone number ID. | `106540352242922` |
| `<WHATSAPP_USER_PHONE_NUMBER>`<br>*String* | **Required.**<br>WhatsApp user phone number. | `+16505551234` |

## Supported Sticker Formats

| Sticker Type | Extension | MIME Type | Max Size |
| --- | --- | --- | --- |
| Animated sticker | .webp | image/webp | 500 KB |
| Static sticker | .webp | image/webp | 100 KB |

## Example Request

Example request to send an animated sticker image to a WhatsApp user.

```curl
curl 'https://graph.facebook.com/v25.0/106540352242922/messages' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "+16505551234",
  "type": "sticker",
  "sticker": {
    "id" : "798882015472548"
  }
}'
```

## Example Response

```json
{
  "messaging_product": "whatsapp",
  "contacts": [
    {
      "input": "+16505551234",
      "wa_id": "16505551234"
    }
  ],
  "messages": [
    {
      "id": "wamid.HBgLMTY0NjcwNDM1OTUVAgARGBI1RjQyNUE3NEYxMzAzMzQ5MkEA"
    }
  ]
}
```
