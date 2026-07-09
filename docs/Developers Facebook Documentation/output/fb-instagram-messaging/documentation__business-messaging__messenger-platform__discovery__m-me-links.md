# m.me Links | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/discovery/m-me-links_

---

# m.me Links

Updated: Mar 23, 2026

This document shows you how to create m.me links for your Messenger experience.

`m.me` is a URL service provided by Meta that redirects people to a person, page, or conversation in Messenger. You can use them on your website, email newsletters, and more.

## How It Works

The format for an `m.me` link is as follows where `PAGE-NAME` is the Facebook Page linked to your messaging app.

```
http://m.me/PAGE-NAME
```

When a person click an `m.me` link, they will be redirected to either a new conversation with your business or an exist conversation if the person has messaged your business in the past. A default message will appear in the conversation stating: “You have entered this conversation by following a link. We’ve let PAGE-NAME know you’re here.”

You can add the `text` parameter to include a customized message as well.

```
http://m.me/PAGE-NAME?text=Hello%20and%20Welcome
```

Businesses can share links that redirect to websites or other threads, some of which may include prefilled text.

When a person clicks the Get Started button to **start a conversation** with your business, a `messaging_postbacks` webhook notification will be sent to your webhooks server. As part of this webhook notification the `postback` object will contain a `referral` object with the `ref` parameter.

When a person clicks an `m.me` link and a conversation already exists between your business and the person, the link will take them to the existing conversation. This action will reset the 24-hour standard messaging window, allowing your messaging app to reply to the person and a `messaging_referrals` webhook notification will be sent to your webhooks server. As part of this webhook notification a `ref` parameter from the `m.me` link will be included.

### Referral Parameters

**Limitation on referral parameters**

Referrals on m.me links might not work for some Messenger for Android customers or [Pages with georestriction](https://www.facebook.com/help/778445532225441/). We do not make guarantees that referrals will always work, and they may be restricted in some instances. However, the m.me link still works to direct customers to send messages. We recommend that you do not use this feature if these limitations impact your business.

An m.me link can contain a `ref` parameter that, when a person clicks on the link, provides your business with more context about the conversation such as a link on your website versus a link in a store. These types of links can also direct the person to specific content or features available within your Messenger experience.

```
http://m.me/PAGE-NAME?ref=REF-PARAMETER-INFORMATION
```

### QR Codes

`m.me` links with `ref` parameters can be embedded into QR Codes. QR compatible codes can be scanned with a phone’s native camera. When scanned they will open the Messenger app and the message conversation with your business.

QR Code Example

The example QR code has `http://m.me/OriginalCoastClothing?ref=summer_coupon` encoded that will trigger an example flow about a discount coupon on Messenger.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/653706618_1459945579197425_3575307037685461133_n.png?_nc_cat=101&ccb=1-7&_nc_sid=e280be&_nc_ohc=VlOY1x0x6_EQ7kNvwE5G-0X&_nc_oc=AdoFNHSctyQqYu3dVSdWbiJh08LAev25-9kyV8WEOKux7WBgg6EWc1otgutFh5InUZw&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=1ZmnBVGmUhG2NMHMrZM-hg&_nc_ss=7b20f&oh=00_Af7hyb7_wM0LMoxxNJNvXYltMf_NxoGoCVX4jSU_yuP5Xg&oe=6A1C22B1)

### Webhook Notification

When you receive a webhook notification it will contain information from a person who is starting a conversation with your business or from a person who has an existing conversation with your business.

Start a Conversation

When a person clicks the Get Started button to start a conversation with your business, we will deliver the `ref` param as part of the `messaging_postbacks` webhook notification.

```http
{
  "sender":{
    "id":"PSID"
  },
  "recipient":{
    "id":"PAGE-ID"
  },
  "timestamp":1458692752478,
  "postback":{
    "payload":"POSTBACK-PAYLOAD-YOU-CONFIGURED",
    "referral": {
      "ref": "REF-PARAMETER-INFORMATION",
      "source": "SHORTLINK",
      "type": "OPEN_THREAD",
    }
  }
}
```

Continue in an Existing Conversation

If a conversation already exists between your business and the person who clicked the m.me link, the link the `messaging_referrals` webhook notification will be sent.

```http
{
  "sender":{
    "id":"PSID"
  },
  "recipient":{
    "id":"PAGE-ID"
  },
  "timestamp":1458692752478,
  "referral": {
    "ref": "REF-PARAMETER-INFORMATION",
    "source": "SHORTLINK",
    "type": "OPEN_THREAD",
  }
}
```

## Before You Start

This guide assumes you have read the [Messenger Platform Overview](https://developers.facebook.com/documentation/business-messaging/messenger-platform/overview) and implemented the needed components for sending and receiving messages and notifications.

You will need:

- Advanced Access for the app that is linked to your business’ Facebook Page
- A [Get Started Button](https://developers.facebook.com/documentation/business-messaging/messenger-platform/discovery/welcome-screen) for your Messenger experience for new conversations
- The app linked to your business’ Facebook Page must be subscribed to the `messaging_postbacks` and `messaging_referrals` webhooks fields

### Limitations

- Apps with Standard Access can only get information from people who have a developer, tester, or admin role on your messaging app

## Marketing Messages Opt In Requests

The `m.me/rn` URL allows you to create a recurring notification opt in request with an `m.me` link. The format for an `m.me/rn` link must include the topic for the recurring notification. You can set the cadence for the recurring notification otherwise it will default to daily.

```
http://m.me/rn/PAGE-NAME?topic=TOPIC&cadence=MESSAGE-FREQUENCY
```

Limitations

- iOS version 383 is required for `m.me/rn` links to work properly. The person who clicked on your link will be redirect to your base `m.me` URL, `http://m.me/PAGE-NAME` URL

Marketing Messages Example Link

```
https://m.me/rn/OriginalCoastClothing?topic=weekly%20deals&cadence=weekly
```

### Register Your Topic

Before you can use your `m.me/rn` URL with a new topic, you must first register the new topic.

If you are using a topic you have used in a previous `m.me/rn` URL and people have opted in to receive recurring notifications, you do not need to register the topic again.

You can register a new topic by following these steps:

**Step 1.** Send yourself a recurring notification opt in request with the topic to a person who has a role on your app. We recommend adding the payload to indicate this is to register your topic.

```curl
curl -X POST -H "Content-Type: application/json" -d '{
  "recipient":{
    "id":"PSID"
  },
  "message":{
    "attachment":{
      "type":"template",
      "payload":{
         "template_type":"notification_messages",
          "title":"TITLE",
          "payload": "Registering a new topic: TOPIC-NAME",
          "notification_messages_frequency": MESSAGE-FREQUENCY,
      }
    }
  }
}' "https://graph.facebook.com/LATEST-API-VERSION/PAGE-ID/messages?access_token=PAGE-ACCESS-TOKEN"
```

On success, your app receives the following JSON response:

```json
{
        "recipient": {
          "id":"PSID",
          "message_id":"MESSAGE-ID",
}
```

**Step 2.** Make sure to click the opt in button in the conversation. We will send you an optin webhook notification. Your topic is now registered and ready for public use.

A person who clicks on an `m.me/rn` link with a topic that has not been registered will be redirected to your base recurring notification URL, `http://m.me/rn/PAGE-NAME` URL.

When registering a topic, if you send yourself an optin request but do not click the opt in button, your topic will not be registered.

Sample Request

Formatted for readability.

```curl
curl -X POST "https://graph.facebook.com/LATEST-API-VERSION/PAGE-ID/notification_messages_dev_support
    ?recipient={
        "notification_messages_token": "NOTIFICATION-MESSAGES-TOKEN"
    }
    &developer_action=ENABLE_FOLLOWUP_MESSAGE
    &access_token=PAGE-ACCESS-TOKEN"
```

On success, your app will receive the following JSON response:

```json
{ "success": true }
```

### `messaging_optins` Webhook Notification

When you receive a webhook notification it will contain information from a person who is starting a conversation with your business or from a person who has an existing conversation with your business.

```json
{
  "sender": {
    "id": "PSID",
  },
  "recipient": {
    "id": "PAGE-ID",
  },
  "timestamp": "TIMESTAMP",
  "optin": {
    "type": "notification_messages",
    "title": "TITLE-FOR-NOTIFICATION-MESSAGE",
    "ref": "REF-PARAMETER-INFORMATION",
    "payload": "",
    "source":"SHORTLINK"
    "notification_messages_token": "NOTIFICATION-MESSAGES-TOKEN",
    "notification_messages_topic": "RECURRING-NOTIFICATION-TOPIC",
    "notification_messages_frequency": "MESSAGE-FREQUENCY",
    "notification_messages_timezone": "TIMEZONE-ID",
    "token_expiry_timestamp": "TIMESTAMP",
    "user_token_status": "TOKEN-STATUS"
    }
}
```

## `m.me` Reference

| Parameter Name | Descripion |
| --- | --- |
| `cadence`*enum { `daily`, `monthly`, `weekly` }* | The message frequency for the `m.me/rn` link opt-in request. Defaults to `daily`. |
| `ref` string | Context about the conversation, such as a link on your website versus a link in a store, that is delivered in a `messaging_referrals` webhook notification. This parameter must be URL-encoded when used on m.me links. Length for this value can not exceeed 2,083 characters |
| `text`string | The customized message sent by you when a person clicks your `m.me` link to enter a conversation. |
| `topic`string | Required. The topic for the `m.me/rn` link opt in request, such as weekly promotions or upcoming releases. This parameter must be URL-encoded when used on m.me links. Alphanumeric, no special characters, URL encoded. |

## Next Steps

- [Send a Reply](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages)
- [Send a Recurring Notification](https://developers.facebook.com/docs/messenger-platform/send-messages/recurring-notifications)

## See Also

- See the [Referral Parameters page](https://www.originalcoastclothing.com/referral-parameters) on [Original Coast Clothing Sample Guide](https://developers.facebook.com/docs/messenger-platform/getting-started/sample-apps/original-coast-clothing)
- Visit the [`messaging_optins` reference](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/webhook-events/messaging_optins)
- Visit the [`messaging_postbacks` reference](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/webhook-events/messaging_postbacks) for more information about this webhook’s fields
- Visit the [`messaging_referrals` reference](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/webhook-events/messaging_referrals) for more information about this webhook’s fields
