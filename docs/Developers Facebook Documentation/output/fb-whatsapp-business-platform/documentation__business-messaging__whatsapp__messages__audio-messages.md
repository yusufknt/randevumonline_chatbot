# Audio messages | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/audio-messages_

---

# Audio messages

Updated: Feb 17, 2026

On March 17th, 2026, voice messages will start receiving a [“played” status webhook](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/status) the first time a WhatsApp user plays a voice message shared by the business.

You can use Cloud API to send voice messages and basic audio messages.

## Voice messages

A voice message (sometimes referred to as a voice note, voice memo, or audio) is a recording of one or more persons speaking, and can include background sounds like music. Voice messages include features like automatic download, profile picture, and voice icon. These features are not available with basic audio messages. If the user sets voice message transcripts to **Automatic**, the message includes a text transcription.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/562379210_2249057198900177_5743647093897895635_n.png?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=yjYRaW9CcvoQ7kNvwEApKyw&_nc_oc=Ado2e698ltzIQr4aGCyDdPWGrTBhbdHo6Iv2YTc-nz_DhpheTXGP5syhP4XRuipUjVc&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=_6nIV7G959xM1DF7dFpL1A&_nc_ss=7b20f&oh=00_Af5R28S3xXrbTNEaXijRIF4PcJDnCHLTs8MFCrvvbcW9KQ&oe=6A1C208C)

- Voice messages require .ogg files encoded with the **OPUS** codec. If you send a different file type or a file encoded with a different codec, voice message transcription will fail.
- The play icon will only appear if the file is 512KB or smaller, otherwise it will be replaced with a download icon (a downward facing arrow).
- The message displays your business’s profile image with a microphone icon.
- The text transcription appears if the user has enabled **Automatic** [voice message transcripts](https://faq.whatsapp.com/241617298315321/) . If the user has set this to **Manual** , the text “Transcribe” will appear instead, which will display the transcribed text once tapped. If the user has set voice message transcripts to **Never** , no text will appear.

## Basic audio messages

Basic audio messages display a download icon and a music icon. When the WhatsApp user taps the play icon, the user manually download the audio message for the WhatsApp client to load and then play the audio file.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/561815849_2827972817396551_127160148973074084_n.png?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=NF1BexgEEbgQ7kNvwFulJ05&_nc_oc=AdoBT_5Y6ANzMQKj8nTGZkMZ_vzZgC6ta3QYXSOs_WGrKUhG4qqJltjlsqA5ekMt1bo&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=_6nIV7G959xM1DF7dFpL1A&_nc_ss=7b20f&oh=00_Af5I5NAh1TgTcH0DvQXwv5RKwHKJ2t1REGMDvS6EIr_0DQ&oe=6A1C25E0)

- The download icon will be replaced with a play icon if the WhatsApp user has enabled [auto-download](https://faq.whatsapp.com/366146522333492/) for audio media and conditions for auto-download are met (e.g. connected to wi-fi).
- If you send a .ogg file encoded with the OPUS code as a basic audio message, the music icon will be replaced with a microphone icon. In addition, if the user has enabled **Automatic** or **Manual** [voice message transcripts](https://faq.whatsapp.com/241617298315321/) , a text transcription or the text “Transcribe” will accompany the message.

## Request syntax

Use the [Messages API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api#post-version-phone-number-id-messages) to send an audio message to a WhatsApp user.

```html
curl 'https://graph.facebook.com/<API_VERSION>/<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>/messages' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <ACCESS_TOKEN>' \
-d '
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "<WHATSAPP_USER_PHONE_NUMBER>",
  "type": "audio",
  "audio": {
    "id": "<MEDIA_ID>", <!-- Only if using uploaded media -->
    "link": "<MEDIA_URL>", <!-- Only if using hosted media (not recommended) -->
    "voice": <IS_VOICE?> <!-- Only include if sending voice message -->
  }
}'
```

## Request parameters

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<ACCESS_TOKEN>`<br>*String* | **Required.**<br>[System token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens) or [business token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens). | `EAAA...` |
| `<API_VERSION>`<br>*String* | **Optional.**<br>Graph API version. | v25.0 |
| `<IS_VOICE?>`<br>*Boolean* | **Optional.**<br>Set to `true` if sending a [voice message](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/audio-messages#voice-messages). Voice messages must be Ogg files encoded with the **OPUS** codec.<br>To send a [basic audio message](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/audio-messages#basic-audio-messages), set to `false` or omit entirely. | `true` |
| `<MEDIA_ID>`<br>*String* | **Required if using uploaded media, otherwise omit.**<br>ID of the [uploaded media asset](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/media#upload-media). | `1013859600285441` |
| `<MEDIA_URL>`<br>*String* | **Required if using hosted media, otherwise omit.**<br>URL of the media asset hosted on your public server. For better performance, we recommend using `id` and an [uploaded media asset ID](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/media#upload-media) instead. | `https://www.luckyshrub.com/media/ringtones/wind-chime.mp3` |
| `<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>`<br>*String* | **Required.**<br>WhatsApp business phone number ID. | `106540352242922` |
| `<WHATSAPP_USER_PHONE_NUMBER>`<br>*String* | **Required.**<br>WhatsApp user phone number. | `+16505551234` |

## Supported audio formats

| Audio Type | Extension | MIME Type | Max Size |
| --- | --- | --- | --- |
| AAC | .aac | audio/aac | 16 MB |
| AMR | .amr | audio/amr | 16 MB |
| MP3 | .mp3 | audio/mpeg | 16 MB |
| MP4 Audio | .m4a | audio/mp4 | 16 MB |
| OGG Audio | .ogg | audio/ogg (OPUS codecs only; base audio/ogg not supported; mono input only) | 16 MB |

The most common errors associated with audio files are mismatched MIME types (MIME type doesn’t match the file type indicated by the file name) and invalid encoding for Ogg files (OPUS codec only). If you encounter an error when sending a media file, verify that your audio file’s MIME type matches its extension and is a supported type. For Ogg files, use the OPUS codec for encoding.

## Example request

Example request to send an image message using an uploaded media ID and a caption.

```curl
curl 'https://graph.facebook.com/v25.0/106540352242922/messages' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "+16505551234",
  "type": "audio",
  "audio": {
    "id" : "1013859600285441",
    "voice": true
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
