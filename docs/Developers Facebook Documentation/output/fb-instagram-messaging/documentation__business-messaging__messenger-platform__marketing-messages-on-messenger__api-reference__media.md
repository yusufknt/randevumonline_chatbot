# Media Template | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/api-reference/media_

---

# Media Template

Updated: Oct 23, 2025

The media template allows you to send images, GIFs, and video as a structured message with an optional button. Videos and animated GIFs sent with the media template are playable in the conversation.

For media templates you must either:

- Use an `attachment`
- Get a Facebook URL for an image or video

## Sending a media template with an attachment

To send a message with an attachment you must first upload your image/video using the [`attachment upload api`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/attachment-upload-api). After successfully uploading an attachment that contains your image/video you should receive an attachment_id, record that and use in the payload below.

```json
{
  "message_id": "<MESSAGE_ID>",
  "messenger_delivery_data": {
    "subscription_token": "<SUBSCRIPTION_TOKEN>"
  },
  "message":{
    "attachment": {
      "type": "template",
      "payload": {
         "template_type": "media",
         "elements": [
            {
               "media_type": "image",
               "attachment_id": "<ATTACHMENT_ID>"
            }
         ]
      }
    }
  }
}
```

## Sending a media template with a URL

To get the Facebook URL for an image or video, do the following:

- Click the image or video thumbnail to open the full-size view.
- Copy the URL from your browser’s address bar. Facebook URLs should be in the following base format:

| Media Type | Media Source | URL Format |
| --- | --- | --- |
| Video | Facebook Page | `https://business.facebook.com/PAGE_NAME/videos/NUMERIC_ID` |
| Video | Facebook Account | `https://www.facebook.com/USERNAME/videos/NUMERIC_ID` |
| Image | Facebook Page | `https://business.facebook.com/PAGE_NAME/photos/NUMERIC_ID` |
| Image | Facebook Account | `https://www.facebook.com/photo.php?fbid=NUMERIC_ID` |

After retrieving a valid facebook URL you can use it in the below payload.

```json
{
  "message_id": "<MESSAGE_ID>",
  "messenger_delivery_data": {
    "subscription_token": "<SUBSCRIPTION_TOKEN>"
  },
  "message":{
    "attachment": {
      "type": "template",
      "payload": {
         "template_type": "media",
         "elements": [
            {
               "media_type": "image",
               "url": "<FACEBOOK_URL>"
            }
         ]
      }
    }
  }
}
```

## Adding a button

Optionally, buttons may also be attached to the media template. You can add up to 3 buttons to a media template message, similar to generic template.

```json
    "elements": [
   {
      "media_type": "image",
      "url": "<MEDIA_URL>",
      "buttons": [
         {
            "type": "web_url",
            "url": "<WEB_URL>",
            "title": "View Website",
         }
      ]
   }
]
```
