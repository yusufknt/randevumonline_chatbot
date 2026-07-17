# Video Messages | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/video-messages_

---

# Video Messages

Updated: Nov 3, 2025

Video messages display a thumbnail preview of a video image with an optional caption. When the WhatsApp user taps the preview, it loads the video and displays it to the user.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/440793312_1179905419842171_7706273386179077435_n.png?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=0ZqjO3Dme88Q7kNvwH0GwDp&_nc_oc=Adq1XC3i-SQHpOtid1oYaZefDTydUFMHB9LwNHXdRRuLGy70zEdnrjJV1kiubvaPKgY&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=QUXjO1BJ21QfQAWdGGuUGg&_nc_ss=7b20f&oh=00_Af5qoUfJh0omVUBYqL33jUiOKlDc-1AaKhP15IawNsvMTw&oe=6A1C2C13)

## Sending Video Messages

Use the [Messages API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api#post-version-phone-number-id-messages) to send a video message to a WhatsApp user.

### Request Syntax

```https
POST /<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>/messages
```

### Post Body

```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "{{wa-user-phone-number}}",
  "type": "video",
  "video": {
    "id" : "<MEDIA_ID>", /* Only if using uploaded media */
    "link": "<MEDIA_URL>", /* Only if linking to your media */
    "caption": "<VIDEO_CAPTION_TEXT>"
  }
}
```

### Post Body Parameters

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<VIDEO_CAPTION_TEXT>`<br>*String* | **Optional.**<br>Video caption text.<br>Maximum 1024 characters. | `A succulent eclipse!` |
| `<MEDIA_ID>`<br>*String* | **Required if using an uploaded media asset (recommended)**.<br>[Uploaded media](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/media#upload-media) asset ID. | `1166846181421424` |
| `<MEDIA_URL>`<br>*String* | **Required if linking to your media asset (not recommended)**<br>URL of video asset on your public server. For better performance, we recommend that you [upload your media asset](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/media#upload-media) instead. | `https://www.luckyshrub.com/assets/lucky-shrub-eclipse-viewing.mp4` |
| `<WHATSAPP_USER_PHONE_NUMBER>`<br>*String* | **Required.**<br>WhatsApp user phone number. | `+16505551234` |

## Supported Video Formats

Only H.264 video codec and AAC audio codec supported. Single audio stream or no audio stream only.

Note that videos encoded with the H.264 “High” profile and B-frames are not supported by Android WhatsApp clients. We recommend that you use H.264 “Main” profile without B-frames, or the H.264 “Baseline” profile when encoding (or re-encoding with a tool like ffmpeg), and place moov boxes before mdat boxes, for broader compatibility. If you are using ffmpeg, you can use the -movflags faststart flag to place moov boxes before mdata boxes.

| Video Type | Extension | MIME Type | Max Size |
| --- | --- | --- | --- |
| 3GPP | .3gp | video/3gpp | 16 MB |
| MP4 Video | .mp4 | video/mp4 | 16 MB |

## Example Request

Example request to send a video message with a caption to a WhatsApp user.

```curl
curl 'https://graph.facebook.com/v25.0/106540352242922/messages' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "+16505551234",
  "type": "video",
  "video": {
    "id" : "1166846181421424",
    "caption": "A succulent eclipse!"
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
