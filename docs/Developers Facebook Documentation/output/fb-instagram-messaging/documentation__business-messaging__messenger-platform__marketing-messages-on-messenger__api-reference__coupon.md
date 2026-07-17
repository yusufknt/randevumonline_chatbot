# Coupon and LTO Template | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/api-reference/coupon_

---

# Coupon and LTO Template

Updated: Apr 6, 2026

This document describes how to create coupon code format with optional running timer (LTO).

## How It Works

A coupon template message has some preset elements and a number of optional properties. The **Copy code** button is a preset element that cannot be changed. You need to add a **coupon code** and second button, with default text **Shop now**, that is configurable with your own text and a URL to redirect a person to your store.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/571352926_1471875067217954_7175114048941057158_n.png?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=FAdJ_2qY8MEQ7kNvwEMgifZ&_nc_oc=Adp4rbbTBUpoAwAQmRD4q5hT43CEznX_pLWrYkPWQrIcrXxNgiYHiz05ggDsI7GepfY&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=X-324lnjdNyJW4BF4ZR1ZA&_nc_ss=7b20f&oh=00_Af63C0IjWkjmGStyFC35Q1yATXiKdby60oVHjdINGp0bJw&oe=6A1C2542)

When a person clicks the **Copy code** button, the coupon code is copied and the bottom sheet shows up with the confirmation and second button to redirect to your store.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/571330549_1953236172124865_4953695866972802221_n.png?_nc_cat=101&ccb=1-7&_nc_sid=e280be&_nc_ohc=XLcWSlgHzegQ7kNvwG8DBNX&_nc_oc=AdrYOAMUCQc0DylP9msLwmNlxJJc_CCf-jlTUgGElHi8JFlf_OaeB-bffKqKlQqdW6k&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=X-324lnjdNyJW4BF4ZR1ZA&_nc_ss=7b20f&oh=00_Af4Kj_FZNRlCmG1wsIyDX_NDhM6D9fhORVZZB2PxwZc0GA&oe=6A1C2507)

## Send a Basic Coupon

In the following example, we are sending a basic coupon message that contains a coupon code.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/570086872_1527196338524384_4222852112258958896_n.png?_nc_cat=110&ccb=1-7&_nc_sid=e280be&_nc_ohc=wwFUXVSy7AEQ7kNvwFbAO7E&_nc_oc=AdowKiJF2KIYmCdAlEbDtVjzHbs_nLpL0vmFOM1hIxSAuelMf2s-_OSg_funZm37aJE&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=X-324lnjdNyJW4BF4ZR1ZA&_nc_ss=7b20f&oh=00_Af4-v70mCZiipxeYufWjBQpF9NbibshECXjrHGBxqUk8zQ&oe=6A1C24CB)

To send a coupon message, send a `POST` request to the `/PAGE-ID/messages` endpoint with a JSON object with the attachment type set to `template` and payload set with the `template_type` set to `coupon`, `title` set to coupon text, and the `coupon_code` set to the coupon code to send to the person.

In the following code example we have set `title` to “10% off summer sale” , `subtitle` to “Copy code 10offsummer and use at checkout.” , `coupon_code` to “10offsummer” and `coupon_url` to “https://www.myshop.com/”.

The subtitle text, **Terms may apply.**, and **Reveal code** button text are the default text for these coupon message properties.

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
          "title":"10% off summer sale",
          "subtitle": "Copy code 10offsummer and use at checkout."
          "coupon_code":"10offsummer",
          "coupon_url":"https://www.myshop.com/",
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

In the following example, we are sending a more complex coupon message that contains image,title, subtitle, shop now button ,coupon code button and greeting params.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/571352926_1471875067217954_7175114048941057158_n.png?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=FAdJ_2qY8MEQ7kNvwEMgifZ&_nc_oc=Adp4rbbTBUpoAwAQmRD4q5hT43CEznX_pLWrYkPWQrIcrXxNgiYHiz05ggDsI7GepfY&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=X-324lnjdNyJW4BF4ZR1ZA&_nc_ss=7b20f&oh=00_Af63C0IjWkjmGStyFC35Q1yATXiKdby60oVHjdINGp0bJw&oe=6A1C2542)

In the following code example we have configured a greeting using the `coupon_pre_message`, `title`, `subtitle`, the disclaimer that applies to this coupon, the second button with my store’s URL and “Shop now” text, an image from my store, and additional information to be sent in the webhook notification when a person clicks the **Copy code** button.

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
          "title":"10% off summer sale 🎁",
          "subtitle":"Use code 10offsummer at checkout.",
          "coupon_code":"10offsummer",
          "coupon_url":"https://www.myshop.com/",
          "coupon_url_button_title":"Shop now",
          "coupon_pre_message":"We have a new summer sale coming up",
          "image_url": "https://www.myshop.com/sale-image.png",
          "payload":"The coupon for 10% off everything that expires 2022-10-1",
      },
    }
  }
}' "https://graph.facebook.com/LATEST-API-VERSION/PAGE-ID/messages?access_token=PAGE-ACCESS-TOKEN"
```

## Send a Coupon Code With LTO

In the following example, we are sending a coupon code with LTO format by passing expire time in the API params.

In the following code example we have configured LTO format by passing `expire_time` in the API spec.

When expire_time is passed we show running timer to the user

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/574338968_815364864570432_2959479086333167233_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=aR8xsN4UclcQ7kNvwFTePmu&_nc_oc=AdoGfnBT-n8kqA0Ow01ridsfGnETk9BAMpKQGVQLTvlB2EgPjsZJTMCHswGHGdkk-kM&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=X-324lnjdNyJW4BF4ZR1ZA&_nc_ss=7b20f&oh=00_Af7Ym-hhFT3xIpb7cgAFspkkEzboI0YbprtMRjJCF0RWwQ&oe=6A1C13B4)

### Request example

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
          "title":"10% off summer sale 🎁",
          "subtitle":"Use code 10offsummer at checkout.",
          "coupon_code":"10offsummer",
          "coupon_url":"https://www.myshop.com/",
          "coupon_url_button_title":"Shop now",
          "expire_time" :"2025-10-25 16:00:00",
          "coupon_pre_message":"We have a new summer sale coming up",
          "image_url": "https://www.myshop.com/sale-image.png",
          "payload":"The coupon for 10% off everything that expires 2022-10-1",
      },
    }
  }
}' "https://graph.facebook.com/LATEST-API-VERSION/PAGE-ID/messages?access_token=PAGE-ACCESS-TOKEN"
```

## Expired Coupon Code

When a coupon code is sent with an `expire_time`, we display the expired state format once the coupon code has expired.

In the expired state we don’t show coupon code CTA and only show URL CTA (if added) to redirect a person to your store with default title and body.

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
| `coupon_code`string | **Required**. Coupon Code for person to copy and apply. |
| `expire_time`string | **optional** Expire time to show Limited Time Offer (Timer) to the user. |
| `coupon_pre_message`string | The message sent before the coupon message |
| `coupon_url`string | **Required**. The coupon URL that allows person to redirect to the website to apply the coupon. |
| `coupon_url_button_title`string | The text for the button that allows a person to click to the coupon URL |
| `image_url`string | The URL for the image displayed in the coupon message |
| `payload`string | Additional information to be included in the webhook notification |
