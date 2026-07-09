# Coupon Template | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/template/coupon_

---

# Coupon Template

Updated: Mar 17, 2026

This document describes how to create and send a coupon to a person in a Messenger conversation.

### How It Works

A coupon template message has some preset elements and a number of optional properties. The title for the message recipient is required and gives the recipient details about the coupon. The disclaimer, **Terms may apply.**, is a preset element but can be configured. The **Reveal code** button is a preset element that can not be changed. You can add a second button, with default text **Shop now**, that is configurable with your own text and a URL to redirect a person to your store.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/324107382_1265661220962475_6992602145917470034_n.png?_nc_cat=110&ccb=1-7&_nc_sid=e280be&_nc_ohc=ZWzR5o9whKAQ7kNvwEr7qXC&_nc_oc=AdpU7_iLuePQIbfdBHhXMb687jgUYDWGH_NhnnzFqvrFHBGr3AskJh3CILqmME2zE5M&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=J8GDLRTFWN7geCQBKIixhQ&_nc_ss=7b20f&oh=00_Af4kkvo3vLfdwOMmiYIXiyce8Wmpw3iUpQHg4wyoZwpP3A&oe=6A1C29D6)

When a person clicks the **Reveal code** button, the coupon code is displayed in the conversation and a webhook notification is sent to your server.

## Before You Start

This guide assumes you have read the [Messenger Platform Overview](https://developers.facebook.com/documentation/business-messaging/messenger-platform/overview) and implemented the needed components for sending and receiving messages and notifications.

You need the following:

- The Page ID for the Facebook Page sending the message
- A Page access token representing the Facebook Page sending the message
- The `pages_show_list` and `pages_messaging` permissions
- Your app subscribed to the `messages` webhook
- The ID for the person receiving the coupon message. Can be one of the following: Page-scoped ID (PSID)Post or Comment IDNotification Message TokenUser Ref

## Send a Basic Coupon

In the following example, we are sending a basic coupon message that contains a coupon code.

To send a coupon message, send a `POST` request to the `/PAGE-ID/messages` endpoint with a JSON object with the attachment type set to `template` and payload set with the `template_type` set to `coupon`, `title` set to coupon text, and the `coupon_code` set to the coupon code to send to the person.

In the following code example we have set `title` to “10% off everything” and `coupon_code` to “10PERCENT”.

The subtitle text, **Terms may apply.**, and **Reveal code** button text are the default text for these coupon message properties.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/327764634_1628843484215623_5292291581993679431_n.png?_nc_cat=101&ccb=1-7&_nc_sid=e280be&_nc_ohc=vtod7T1yoHoQ7kNvwGZE25H&_nc_oc=Adpzx5fx_k8XiecWHDAXd7AEulbAOMaigG7t2PxBm7Hzrydgbw-3F7FAQAb-p_oC4T8&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=J8GDLRTFWN7geCQBKIixhQ&_nc_ss=7b20f&oh=00_Af5FWIubYcQ48P2-rkocSbwVL0GleuHknt59bUPq5ecl3Q&oe=6A1C1478)

```curl
curl -X POST -H "Content-Type: application/json" -d '{
  "recipient":{
    "id":"PSID"
  },
  "message":{
    "attachment": {
      "type": "template",
      "payload": {
          "template_type": "coupon",
          "title":"10% off everything",
          "coupon_code":"10PERCENT",
      },
    }
  }
}' "https://graph.facebook.com/LATEST-API-VERSION/PAGE-ID/messages?access_token=PAGE-ACCESS-TOKEN"
```

On success, your app receives the following JSON response with the PSID for the recipient and the ID for the message:

```json
{
  "recipient_id": "PSID",
  "message_id": "MESSAGE-ID"
}
```

## Send a Complex Coupon

In the following example, we are sending a more complex coupon message that contains all the properties you can send in the coupon template payload.

In the following code example we have configured a greeting using the `coupon_pre_message`, `title`, `subtitle`, the disclaimer that applies to this coupon, the second button with my store’s URL and “Shop now” text, an image from my store, and additional information to be sent in the webhook notification when a person clicks the **Reveal code** button.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/313869006_1101125734105247_6408134586873650465_n.png?_nc_cat=101&ccb=1-7&_nc_sid=e280be&_nc_ohc=ZQMQQtMvkD4Q7kNvwEvuNnI&_nc_oc=AdozPijjlsiZQpCFaWuNu_mIXCQk7d7oNiFifmGX_6ao1QQzEGKD7keAe3Q-4HrDLXE&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=J8GDLRTFWN7geCQBKIixhQ&_nc_ss=7b20f&oh=00_Af6sLKLJp7bgy51UXvly7yuZPUpR4pxaO_h1C1_DdGIhvA&oe=6A1C1BB2)

```curl
curl -X POST -H "Content-Type: application/json" -d '{
  "recipient":{
    "id":"PSID"
  },
  "message":{
    "attachment": {
      "type": "template",
      "payload": {
          "template_type": "coupon",
          "title":"10% off everything",
          "subtitle":"10% off. Limit 1 per customer. Expires on October 1st, 2022",
          "coupon_code":"10PERCENT",
          "coupon_url":"https://www.myshop.com/",
          "coupon_url_button_title":"Shop now",
          "coupon_pre_message":"Here'\''s a deal just for you!",
          "image_url": "https://www.myshop.com/sale-image.png",
          "payload":"The coupon for 10% off everything that expires 2022-10-1",
      },
    }
  }
}' "https://graph.facebook.com/LATEST-API-VERSION/PAGE-ID/messages?access_token=PAGE-ACCESS-TOKEN"
```

On success, your app receives the following JSON response with the PSID for the recipient and the ID for the message:

```json
{
  "recipient_id": "PSID",
  "message_id": "MESSAGE-ID"
}
```

## Webhook Notification

When a person clicks on the coupon message, a `messages` webhook notification is sent to your server. The notification will contain the PSID for the person who clicked the coupon message, the ID for the Page that sent the message, and payload information about the coupon.

```json
{
  "sender": {
    "id": "PSID",
  },
  "recipient": {
    "id": "PAGE-ID",
  },
  "timestamp": UNIX-TIMESTAMP,
  "template": {
    "type" : "coupon",
    "payload" : "ADDITIONAL-INFORMATION",
    "coupon_code":"COUPON-CODE",
  }
}
```

## Reference

| Property | Description |
| --- | --- |
| `recipient` object | **Required.** Object containing information about the person receiving the coupon message |
| `id`string | The Page-scoped ID (PSID) for the person receiving the coupon message |
| `comment_id`string | Send a Private Reply that contains a coupon template to a person who commented on a post on the Facebook Page |
| `notification_message_token`string | Send Marketing Messages that contain a coupon template to a person |
| `post_id`string | Send a Private Reply that contains a coupon template to a person who published a visitor post on the Facebook Page |
| `user_ref`string | Send a Checkbox plugin that contains a coupon template |
| `message`object | **Required.** Contains the attachment object |
| `attachment`object | **Required.** Contains the type of message and payload. |
| `type`enum {`template`} | **Required.** Message type, set to `coupon` |
| `payload`object | **Required.** Contains the message coupon details |
| `template_type`enum {`coupon`} | **Required.** Set to `coupon` |
| `title`string | **Required.** Title to display in the message. 80 character limit. |
| `subtitle`string | Subtitle to display in the message. 80 character limit. |
| `coupon_code`string | **Required** unless `coupon_url` is set. The coupon code to send to a person. Can not have spaces. |
| `coupon_pre_message`string | The message sent before the coupon message |
| `coupon_url`string | **Required** unless `coupon_code` is set. The coupon URL that allows a person to use the coupon. |
| `coupon_url_button_title`string | The text for the button that allows a person to click to the coupon URL |
| `image_url`string | The URL for the image displayed in the coupon message |
| `payload`string | Additional information to be included in the webhook notification |
