# Generic Template | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/api-reference/generic_

---

# Generic Template

Updated: Feb 12, 2026

The generic template allows you to send a structured message that includes an image, text and buttons. A generic template with multiple templates described in the `elements` array will send a horizontally scrollable carousel of items, each composed of an image, text and buttons. For complete implementation details, see Generic Template.

**Personalization**: You may also add personalization macros to the `title` and `subtitle` fields for all formats. You can add `{{first_name}}`, `{{last_name}}`, and `{{full_name}}` into your `title` and `subtitle` strings to enable personalized marketing messages. For example, the `title` field may read as `"New sale for you, {{first_name}}!"`. For a user named John Doe, the rendered message title will be `"New sale for you, John!"`.

- For carousel, personalization macros may be applied to the `title` and `subtitle` field of each element in the `elements` field.
- Personalization is not enabled for buttons.

## Request with image

You can send a template with an image if you have a link to your image, you must also set `media_type` to image (this is the default if not set). These links need to lead to an image file and don’t have to facebook URLs.

✅ Use the correct aspect ratio for your image. Photos that aren’t 1:1 will be scaled or cropped.

```json
{
  "message_id": "<MESSAGE_ID>",
  "messenger_delivery_data": {
    "subscription_token": "<SUBSCRIPTION_TOKEN>"
  },
  "message":{
    "attachment":{
      "type":"template",
      "payload":{
        "template_type":"generic",
        "elements":[
           {
            "title":"Welcome!",
            "image_url":"<IMAGE_URL>",
            "subtitle":"We have the right hat for everyone.",
            "buttons":[
              {
                "type":"web_url",
                "url":"<BUTTON_URL>",
                "title":"View Website"
              },{
                "type":"postback",
                "title":"Start Chatting",
                "payload":"<PAYLOAD_WEBHOOK>"
              }
            ]
          }
        ]
      }
    }
  }
}
```

## Request with App Destinations

You can send a template with app destination , you can specify the button type as `app` and provide deeplink url for ios and android apps.

```json
{
  "message_id": "<MESSAGE_ID>",
  "messenger_delivery_data": {
    "subscription_token": "<SUBSCRIPTION_TOKEN>"
  },
  "message":{
    "attachment":{
      "type":"template",
      "payload":{
        "template_type":"generic",
        "elements":[
           {
            "title":"Welcome!",
            "image_url":"<IMAGE_URL>",
            "subtitle":"We have the right hat for everyone.",
            "buttons":[
              {
                "type":"web_url",
                "url":"<BUTTON_URL>",
                "title":"View Website"
              },{
                "type":"app",
                "android_url":"<ANDROID_APP_DEEPLINK_URL>",
                "ios_url":"<IOS_APP_DEEPLINK_URL>"
              }
            ]
          }
        ]
      }
    }
  }
}
```

## Request with video

You can send videos in your generic template by passing in a `video_id` field and setting `media_type` to video. This video id can be retrieved from the URI when clicking on a video on facebook.

**Note**: For video, the video_id needs to be obtained from the [Ad Videos](https://developers.facebook.com/documentation/ads-commerce/marketing-api/reference/ad-account/advideos) API

```json
{
  "message_id": "<MESSAGE_ID>",
  "messenger_delivery_data": {
    "subscription_token": "<SUBSCRIPTION_TOKEN>"
  },
  "message":{
    "attachment":{
      "type":"template",
      "payload":{
        "template_type":"generic",
        "elements":[
           {
            "title":"Welcome!",
            "media_type": "video",
            "video_id":"<VIDEO_ID>",
            "subtitle":"We have the right hat for everyone.",
            "buttons":[
              {
                "type":"web_url",
                "url":"<BUTTON_URL>",
                "title":"View Website"
              }
            ]
          }
        ]
      }
    }
  }
}
```

**Note**: Currently, we do not support postback buttons in video payloads. We are actively working to add this support.

## Request with multiple images

You can send a template with multiple images to showcase in a grid. You can also define one of these images as “hero” to highlight it in the grid. These links need to lead to an image files and don’t have to be facebook URLs.

```json
{
  "message_id": "<MESSAGE_ID>",
  "messenger_delivery_data": {
    "subscription_token": "<SUBSCRIPTION_TOKEN>"
  },
  "message":{
    "attachment":{
      "type":"template",
      "payload":{
        "template_type":"generic",
        "elements":[
           {
            "title":"Welcome!",
            "image_urls":[
              {
                "url":"<IMAGE_URL>",
                "is_hero_image":"true"
              },
              {
                "url":"<IMAGE_URL>",
              },
            ],
            "subtitle":"We have the right hat for everyone.",
            "buttons":[
              {
                "type":"web_url",
                "url":"<BUTTON_URL>",
                "title":"View Website"
              },{
                "type":"postback",
                "title":"Start Chatting",
                "payload":"<PAYLOAD_WEBHOOK>"
              }
            ]
          }
        ]
      }
    }
  }
}
```

- Supports upto 6 images
- Use only one of `image_url` or `image_urls`
- Only one url can be designated as the hero image using `"is_hero_image":"true"`

## Carousel - Multiple elements

If you are trying to send a carousel, you can do so by adding multiple elements (max 10) to the payload as shown here:

```json
"payload": {
  "template_type":"generic",
  "elements":[
    <GENERIC_TEMPLATE>,
    <GENERIC_TEMPLATE>,
    ...
  ]
}
```

## Additional Messages

### Greeting

MAPI-D supports sending a **greeting pre-message** before the main marketing template in freeform messages. This allows businesses to create a more conversational experience by greeting users before showing promotional content.

How to Add a Greeting

To include a greeting in your freeform message, add the `text` field to your `generic` template payload:

```json
{
  "message": {
    "attachment": {
      "type": "template",
      "payload": {
        "template_type": "generic",
"text": "Hello! Welcome to our store.",        "elements": [...]
      }
    }
  }
}
```

**Personalize your greetings**: Include `{{first_name}}`, `{{last_name}}`, and `{{full_name}}` macros into your `text` string to enable personalized greetings for users.

## Error codes

Certain errors may occur if the payload is malformed, the below table references possible error codes that may occur.

| Namespace | Name | Code | Description |
| --- | --- | --- | --- |
| MARKETING_MESSAGES_DIRECT | VIDEO_MEDIA_TYPE_MISSING_VIDEO_ID | 2300021 | When media_type is ‘video’, a video_id must be provided. |
| MARKETING_MESSAGES_DIRECT | IMAGE_MEDIA_TYPE_MISSING_IMAGE_URL | 2300022 | When media_type is ‘image’, an image_url must be provided. |
| MARKETING_MESSAGES_DIRECT | INVALID_BUTTON_TYPE | 2300023 | The button type is invalid. Valid button types are: web_url. |
| MARKETING_MESSAGES_DIRECT | EMPTY_BUTTON_URL | 2300024 | Button URL cannot be empty when provided. |
| MARKETING_MESSAGES_DIRECT | EMPTY_BUTTON_TITLE | 2300025 | Button title cannot be empty. |
| MARKETING_MESSAGES_DIRECT | TOO_MANY_BUTTONS | 2300026 | Too many buttons provided. Maximum of 3 buttons are allowed per message. |
