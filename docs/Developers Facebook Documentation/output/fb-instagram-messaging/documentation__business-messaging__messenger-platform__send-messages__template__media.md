# Media template | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/template/media_

---

# Media template

Updated: Apr 22, 2026

The media template allows you to send images, GIFs, and video as a structured message with an optional [button](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/buttons). Videos and animated GIFs sent with the media template are playable in the conversation.

The media template can be sent via the Send API and from the Messenger webview with the Messenger Extension SDK’s `beginShareFlow()` function.

### Limitations

- **Images and video only** — The media template only supports sending images and video. Audio is not supported.
- **Re-using media from Facebook URLs** — Attachment IDs are not supported for media from Facebook URLs. These files are already cached, and should be attached to the media template with their Facebook URL.
- **Facebook URLs only** — The media template does not allow any external URL, only those on Facebook. To send an image or video with an external URL, upload it using the [Attachment Upload API](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/attachment-upload-api) and get an `attachment_id` .

## Request URI

```curl
https://graph.facebook.com/v25.0/me/messages?access_token={PAGE_ACCESS_TOKEN}
```

## Payload properties

| Property | Type | Description |
| --- | --- | --- |
| `template_type` | String | Must be<br>`media`<br>. |
| `elements` | Array | An array containing 1<br>`element`<br>object that describes the media in the message. Maximum of 1 element. |
| `sharable` | Boolean | *Optional.*<br>Set to<br>`true`<br>to enable the native share button in Messenger for the template message. Defaults to<br>`false`<br>. |

### `element` properties

| Property | Type | Description |
| --- | --- | --- |
| `media_type` | String | The type of media being sent.<br>`image`<br>or<br>`video`<br>is supported. |
| `attachment_id` | String | The attachment ID of the image or video. Cannot be used if<br>`url`<br>is set. |
| `url` | String | The URL of the image. Cannot be used if<br>`attachment_id`<br>is set. |
| `buttons` | Array | *Optional.*<br>An array of<br>[buttons](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/buttons)<br>to append to the template. Maximum of 3 buttons. |

## Send media by attachment ID

To send an image, send a `POST` request to the Send API with the `attachment_id` property, where `attachment_id` is an ID generated from the [Attachment Upload API](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/attachment-upload-api). Images and videos are supported.

```
curl -X POST -H "Content-Type: application/json" -d '{
  "recipient":{
    "id":"<PSID>"
  },
  "message":{
    "attachment": {
      "type": "template",
      "payload": {
         "template_type": "media",
         "elements": [
            {
               "media_type": "<image|video>",
               "attachment_id": "<ATTACHMENT_ID>"
            }
         ]
      }
    }
  }
}' "https://graph.facebook.com/v25.0/me/messages?access_token=<PAGE_ACCESS_TOKEN>"
```

## Send media by Facebook URL

To send videos and photos uploaded to Facebook, send a `POST` request to the `/<PAGE_ID>/messages` endpoint with the Facebook URL in the `url` property of the request.

```curl
curl -X POST -H "Content-Type: application/json" -d '{
  "recipient":{
    "id":"<PSID>"
  },
  "message":{
    "attachment": {
      "type": "template",
      "payload": {
         "template_type": "media",
         "elements": [
            {
               "media_type": "<image|video>",
               "url": "<FACEBOOK_URL>"
            }
         ]
      }
    }
  }
}' "https://graph.facebook.com/v25.0/me/messages?access_token=<PAGE_ACCESS_TOKEN>"
```

### Get the Facebook URL

To get the Facebook URL for an image or video:

1. Click the image or video thumbnail to open the full-size view.
2. Copy the URL from your browser’s address bar.

Facebook URLs should be in the following base format:

| Media type | Media source | URL format |
| --- | --- | --- |
| Video | Facebook Page | `https://business.facebook.com/<PAGE_NAME>/videos/<NUMERIC_ID>` |
| Video | Facebook Account | `https://www.facebook.com/<USERNAME>/videos/<NUMERIC_ID>/` |
| Image | Facebook Page | `https://business.facebook.com/<PAGE_NAME>/photos/<NUMERIC_ID>` |
| Image | Facebook Account | `https://www.facebook.com/photo.php?fbid=<NUMERIC_ID>` |

## Add a button

Optionally, buttons may be attached to the media template. The number and types of supported buttons varies depending on whether you are using the media template with the Messenger Extensions SDK’s `beginShareFlow()`, or sending it with the Send API:

- **Send API** : Up to 3 buttons of any type may be attached.
- **`beginShareFlow()`** : Only 1 button of type URL may be attached.

To add a button, add a `buttons` array to the template definition in the body of your request. For more on available buttons, see [Buttons](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/buttons).

## Sample response

```js
{
  "recipient_id": "1254477777772919",
  "message_id": "AG5Hz2Uq7tuwNEhXfYYKj8mJEM_QPpz5jdCK48PnKAjSdjfipqxqMvK8ma6AC8fplwlqLP_5cgXIbu7I3rBN0P"
}
```

## Error codes

| Error code | Description |
| --- | --- |
| 2018173 | Failed to generate preview URL |
| 2018175 | Media preview failed |
| 2018182 | Media type not valid |
| 2018183 | Attachment ID is missing |
| 2018184 | Media template Facebook media URL is not supported |
| 2018185 | Non-Facebook URL in URL parameter |
| 2018186 | Unable to get photo or video from Facebook URL |
| 2018187 | Either URL or attachment ID is required |
| 2018188 | External URL is not supported |
