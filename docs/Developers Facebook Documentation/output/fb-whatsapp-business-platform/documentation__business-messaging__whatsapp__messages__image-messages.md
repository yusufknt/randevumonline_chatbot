# Image messages | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/image-messages_

---

# Image messages

Updated: Nov 3, 2025

Image messages are messages that display a single image and an optional caption.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/440788911_1344094656981591_356280964045551612_n.png?_nc_cat=110&ccb=1-7&_nc_sid=e280be&_nc_ohc=x-pLCSSg8RsQ7kNvwFHYWzQ&_nc_oc=Adq0dz-G7cwnZnTFEhcNJyC5qbRV7sq-YgPlVHuK1JNMJMozdLEUIJ18LnX_nCpvxN4&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=ZvaM0kEntRRgOub7viCLbw&_nc_ss=7b20f&oh=00_Af5ckPGtNKgu7LZG7RcSh9N5Y1CpTGYWt7KQFzxcX-0NIA&oe=6A1C1E09)

## Request syntax

Use the [Messages API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api#post-version-phone-number-id-messages) to send an image message to a WhatsApp user.

```html
curl 'https://graph.facebook.com/<API_VERSION>/<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>/messages' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <ACCESS_TOKEN>' \
-d '
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "<WHATSAPP_USER_PHONE_NUMBER>",
  "type": "image",
  "image": {
    "id": "<MEDIA_ID>", <!-- Only if using uploaded media -->
    "link": "<MEDIA_URL>", <!-- Only if using hosted media (not recommended) -->
    "caption": "<MEDIA_CAPTION_TEXT>"
  }
}'
```

## Request parameters

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<ACCESS_TOKEN>`<br>*String* | **Required.**<br>[System token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens) or [business token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens). | `EAAA...` |
| `<API_VERSION>`<br>*String* | **Optional.**<br>Graph API version. | v25.0 |
| `<MEDIA_CAPTION_TEXT>`<br>*String* | **Optional.**<br>Media asset caption text.<br>Maximum 1024 characters. | `The best succulent ever?` |
| `<MEDIA_ID>`<br>*String* | **Required if using uploaded media, otherwise omit.**<br>ID of the [uploaded media asset](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/media#upload-media). | `1013859600285441` |
| `<MEDIA_URL>`<br>*String* | **Required if using hosted media, otherwise omit.**<br>URL of the media asset hosted on your public server. For better performance, we recommend using `id` and an [uploaded media asset ID](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/media#upload-media) instead. | `https://www.luckyshrub.com/assets/succulents/aloe.png` |
| `<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>`<br>*String* | **Required.**<br>WhatsApp business phone number ID. | `106540352242922` |
| `<WHATSAPP_USER_PHONE_NUMBER>`<br>*String* | **Required.**<br>WhatsApp user phone number. | `+16505551234` |

## Supported image formats

Images must be 8-bit, RGB or RGBA.

| Image Type | Extension | MIME Type | Max Size |
| --- | --- | --- | --- |
| JPEG | .jpeg | image/jpeg | 5 MB |
| PNG | .png | image/png | 5 MB |

## Example request

Example request to send an image message with a caption to a WhatsApp user.

```curl
curl 'https://graph.facebook.com/v25.0/106540352242922/messages' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "+16505551234",
  "type": "image",
  "image": {
    "id" : "1479537139650973",
    "caption": "The best succulent ever?"
  }
}'
```

## Example response

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
