# Conversation Routing | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/conversation-routing_

---

# Conversation Routing

Updated: Sep 24, 2025

Meta no longer supports Handover Protocol for Messenger and all the businesses are migrated to Conversation Routing. Conversation Routing is backwards compatible with most of the Handover Protocol API and functionalities and expected to function without any interruptions.

Conversation Routing allows Meta to route conversations between your business and customers, or prospective customers, to the app that you have specified to respond in the conversation. This routing allows your business to create rich conversations with people and to minimize API calls to Meta’s servers.

This document shows you how to configure your apps for Conversation Routing.

## Overview

Conversation Routing enables businesses to utilize multiple connected applications to respond to user messages in a coordinated manner, designating which application should take responsibility for responding. This allows both businesses and users to have a rich conversation experience without having to manage complex business logic within each individual application when responding to user queries.

Businesses can connect different types of applications to support their customers through messaging.

1. Marketing
2. Sales
3. Customer care

In some cases a single application can have multiple roles when responding to their customers.

When you have multiple messaging applications connected to your Facebook page and you want Meta to route messages to each application based on how your customers messaged you on Messenger, we recommend to use Conversation Routing.

There are a limited number of message routing features available even without Conversation Routing enabled, like default messaging behavior.

### Default Behavior

Default behavior, or zero config behavior, allows the applications to use some conversation controls even without setting a Conversation Routing default application, with certain limitations.
If only one application is connected to your business and is solely responsible for receiving and responding to messages, use default behavior. Coordination of responses from both the application and page inbox is necessary to ensure no duplicate responses to the same message.

### Changes from Conversation Routing

1. All connected applications receive messaging webhooks.
2. All applications can respond to the same user message without restrictions.
3. The Take Thread Control API is blocked unless a default application is set.
4. The Pass Thread Control API is enabled, allowing any application to pass thread control when it is idle.
5. The Request Thread Control API is enabled for any application but must be invoked to gain control.
6. Only campaign routing is available as an entry point thread routing option. Link routing and social routing are not available.

## Before You Start

This guide assumes you have read the [Messenger Platform Overview](https://developers.facebook.com/documentation/business-messaging/messenger-platform/overview) and implemented the needed components for sending and receiving messages and notifications.

Before you can pass conversations between apps, you need the following:

- A Meta Ad Account
- The Meta app ID for your default app
- The Meta app ID for your marketing app
- Connect all apps to your business’ Facebook Page
- The person requesting the Page access token must have Admin access or be able to perform the `MANAGE` task on a Classic Facebook Page, Facebook access (New Pages Experience) for the Facebook Page, or Full control via the Business Settings
- A server to receive Meta Webhooks notifications. We recommend setting up a separate endpoint on your server for each app.
- Subscribe all apps to the following webhooks topics: `messages``messaging_referral``messaging_handover``messaging_postbacks``standby`

**Note:** Your default app may need to subscribe to other messaging webhooks depending on other conversation entry points you use.

## Enable Conversation Routing

Businesses can enable conversation routing by setting up the default application on the page settings.

### Default Application

The default application is the primary app allowed to respond to a conversation when no other app is configured or responding.

Assigning Default Application

You can assign a default app in your [Facebook Page settings](https://www.facebook.com/settings?tab=msgr_conversation_routing). Log in as the Page.

## Conversation Control and Thread Owner

The application responsible for responding to a specific user-business conversation has **Conversation Control** or is the **Thread Owner.**

### Thread Owner States

1. **Idle:** When there is no active conversation between user and business (no user to business message within last 24 hours) or state after current thread owning application invokes release thread control control flow.
Only default application can send a message when the thread is in idle state, and conversation should be within the messaging window in order for the application to message user.
2. **Active:** When there is an active conversation between user and business application and when the thread owner status is active.

## Entry Point Routing

Entry point routing enables you to route conversations to specific apps based on a user’s entry point. You can configure these routes on the Conversation Routing tab of your Facebook Page’s settings.

| Entry Point | How to Configure |
| --- | --- |
| Social Entry | Click on the **Message** button on the page and open up **Messenger** |
| Link Routing | Click on a message link [m.me](http://m.me) on a third party site and open up **Messenger** |
| Campaign Routing | Click on a CTM advertisement and open up MessengerCheck [Messenger Lead Generation Ads with target app](https://developers.facebook.com/docs/messenger-platform/handover-protocol/messenger-lead-ads-hop) for follow ups document for more details |

There are two types of entry points routing available: Link Routing and Social/organic routing.

### Link Routing

Link routing enables you to configure multiple m.me links, and assign a routing app to each link.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/652173673_1459945689197414_4593032583373417710_n.png?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=nIqQkA572wwQ7kNvwHRP87x&_nc_oc=AdoF5L0TVbNwcQgswmKRfjrV7ulAnGNXNiKCQ_buvC-0IZhzBSbSXLZS0sJ3oZsaLsE&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=WGkqRHQGRUApCn40pEN26g&_nc_ss=7b20f&oh=00_Af4XhbTDUC-CDbYSP7O18TKpAi2JFlZ3kmZ_fKhOeQNqIw&oe=6A1C32D0)

### Social Routing

Social (organic) routing enables you to configure one app that will get thread control when a user enters an idle thread (no user messages in the last 24 hours) or clicks a Get Started button.
![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/653702967_1459945575864092_2772249672585142082_n.png?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=FBF3IFtBP9IQ7kNvwG1jAtI&_nc_oc=AdrYfQPekzNkt94KBm8Wpq4pWxtE9_u3I8Tz80n_k319nU-MX77KiuBIfl1-csca5AA&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=WGkqRHQGRUApCn40pEN26g&_nc_ss=7b20f&oh=00_Af5O-C1EMbTzY_YlZJoMwDOzdDnitmtGiqJo3fDt0FQuTQ&oe=6A1C3ECD)

## Conversation Control Flows

Routing control flow allows the applications to change the routing of the messages for the subsequent messages sent by the customers. There are 4 types of control flows

### Meta Business Suite Inbox Support

Conversation routing allows your business to use Meta Business Suite Inbox as another application connected to your page, which can be used to continue conversations with your users. An inbox can also be assigned as a default application. Additionally, if you move a message to the Main folder or respond to a message in a conversation not controlled by the inbox, the inbox takes control of the conversation.

### Pass Thread Control

Current thread owning application passing thread control to another application, assigning a new thread owner.

For example, a marketing application passes thread control to Sales application to complete AI support agent application, which then passes thread control to customer care agent application, which allows user to interact with a customer care agent.

### Release Thread Control

Current thread owning application releases thread control to set thread control state to idle.

For example,
when a marketing application answers all the customer queries successfully and does not expect any further marketing queries from the customer, it releases the thread control to allow the default application to answer any future queries.
Another example is if the current thread owner application cannot respond to the user for the current messages because of technical issues or unrelated queries, release the thread control to allow the default application to respond.

### Take Thread Control

Applications which are allowed to take control of conversations by the business can invoke take thread control control flow, which allows applications to set it as the thread owner.
Applications with Human Agent feature are not allowed to take thread control while using the Send API (with HA tag) if the businesses are not allowing this.

For example, if the user agent on the customer care application sees there is an issue with the marketing bot application, such as it is sending some invalid responses, the customer care application can use take thread control to continue the conversation.

### Extend Thread Control

Thread control will expire after 24 hours of inactivity, but in some cases businesses might not have enough time to respond to the user, and be required to extend the thread control for that application before its thread control status becomes idle.

For example, in a non-default customer sales application, customer sales agents answering the customer queries require more time to find the product details requested by the users, so they invoke extend thread control.

## Conversation Control

We show you how to:

- Pass control to another app
- Release thread control from the current app
- Take thread control from another app
- Request control of a conversation from another app
- Determine which app currently controls a conversation

### Send API: Message send with thread controls

Pass Thread Control

You can pass thread control to a specific app by setting `app_id` and `control_type` fields in `thread_control`.

```html
curl -X POST -H "Content-Type: application/json" -d '{
  "messaging_type": "RESPONSE",
  "thread_control": {
  "app_id": "<APPLICATION_ID>",
  "control_type": "pass"
  },
  "recipient": {
  "id": "<PSID>"
  },
  "message": {
  "text" : "Let me transfer you to our live agent"
  }
}' "https://graph.facebook.com/v12.0/me/messages?access_token=<ACCESS_TOKEN>"
```

On success, your app receives the following JSON object with the recipient ID and the message ID.

```html
{
  "recipient_id":"<PSID>",
  "message_id":"MESSAGE-ID"
}
```

Release Thread Control

You can release thread control to the default application by setting up `control_type` fields in `thread_control`.

```html
curl -X POST -H "Content-Type: application/json" -d '{
  "messaging_type": "RESPONSE",
  "thread_control": {
  "control_type": "release"
  },
  "recipient": {
  "id": "<PSID>"
  },
  "message": {
  "text" : "Let me transfer you to our live agent"
  }
}' "https://graph.facebook.com/v12.0/me/messages?access_token=<ACCESS_TOKEN>"
```

On success, your app receives the following JSON object with the recipient ID and the message ID.

```html
{
  "recipient_id":"<PSID>",
  "message_id":"MESSAGE-ID"
}
```

| Parameter | Description |
| --- | --- |
| `thread_control` | Specify which Conversation Routing control flow needs to be invoked after sending the message. |
| `control_type` | Specify whether to pass or release thread control. If not set, control is released by default. Supports two possible values:<br>`pass`: Passes thread control to the default app and sends a webhook to the configured app. The webhook tells the default app to continue the conversation.`release`: Releases thread control to the default app. No webhook is sent. Should be used when the app in control determines that no further action is needed on the conversation. |
| `app_id` (optional) | Used in pass thread control control flow which defines the application ID that should be set as the thread owner going forward.<br>As an optional parameter if app_id is not defined in the request thread control will be passed to the default application. |

### Thread Control APIs

Pass Thread Control

When your app requires hand over the conversation to another application, to better assist the customer, send a `POST` request to `/PAGE_ID/pass_thread_control` with the recipient parameter set to the `PSID` for the customer who sent the message, `target_app_id` set to the ID for the app that is getting control, and the metadata parameter (optional) set to information about the conversation that should be passed to other apps.

Note: To pass control to an Inbox, set `target_app_id` to **263902037430900** for the Page Inbox and **1217981644879628** for the Instagram Inbox.

```html
curl -X POST "https://graph.facebook.com/LATEST-API-VERSION/PAGE-ID/pass_thread_control
  ?recipient={id:PSID}
  &target_app_id=APP-GETTING-CONTROL
  &metadata=Information about the conversation
  &access_token=PAGE-ACCESS-TOKEN"
```

On success, your app will receive the following response:

```html
{
  "success" : true
}
```

Control of the conversation has been passed to application specified in the request.

Example Webhooks Notification

```html
{
  "sender":{
     "id":"PSID"   // The Page-scoped ID for the person who sent the message to the Page
  },
  "recipient":{
     "id":"PAGE-ID"
  },
  "timestamp":UNIX-TIMESTAMP,
  "pass_thread_control":{
     "previous_owner_app_id":"APP-RELEASING-CONTROL",
      "new_owner_app_id": APP-GETTING-CONTROL,
      "metadata":"Information about the conversation"
  }
}
```

Release Thread Control

We recommend releasing control of the conversation, returning it to idle, as soon as the app is finished with its flow instead of waiting for the response time to expire.

To release control of a conversation, send a `POST` request to `/PAGE-ID/release_thread_control` with the recipient parameter set to the `PSID` for the customer who sent the message and any pertinent information using the metadata parameter.

Sample API Request

```html
curl -X POST "https://graph.facebook.com/LATEST-API-VERSION/PAGE-ID/release_thread_control
  ?recipient={id:PSID}
  &metadata=Information about the conversation
  &access_token=PAGE-ACCESS-TOKEN"
```

Example API Response

On success, your app will receive the following response

```html
{
  "success" : true
}
```

Control of the conversation status will change to idle after successful invocation of the request.

Take Thread Control

If a conversation is idle, or your app is the Primary Receiver, you can send a `POST` request to `/PAGE-ID/take_thread_control` with the recipient parameter set to the ID for the person who sent the message and the metadata parameter (optional) set to information about the conversation that should be passed to other apps.

Sample API Request

```html
curl -X POST -H "https://graph.facebook.com/LATEST-API-VERSION/PAGE-ID/take_thread_control
  ?recipient={id:ID}
  &metadata=Information about the conversation
  &access_token=PAGE_ACCESS_TOKEN"
```

Example API Response

On success, your app will receive the following response

```html
{
  "success" : true
}
```

Example Webhooks Notification

Any apps subscribed to the `messaging_handover` webhook field will receive a notification with the ID for the person who sent the message, the ID for the Facebook Page or Instagram Professional account that received the message, the ID for the previous app that controlled the conversation, the ID for the app that now controls the conversation, and any metadata about the conversation that was sent in the API request that triggered the webhook.

```html
{
  "sender":{
  "id":"ID"
  },
  "recipient":{
  "id":"ID"
  },
  "timestamp":UNIX-TIMESTAMP,
  "take_thread_control":{
  "previous_owner_app_id":"PREVIOUS-OWNER-APP-ID",
  "new_owner_app_id": "NEW-OWNER-APP-ID",
  "metadata":"Information about the conversation"
  }
}
```

Request Thread Control

To request control of a conversation from another app, send a `POST` request to `/PAGE-ID/request_thread_control` with the recipient parameter set to the `PSID` for the customer who sent the message and the metadata parameter (optional) set to information about the conversation that should be passed to other apps. Request thread control is only supported in default.

Sample API Request

```html
curl -X POST "https://graph.facebook.com/LATEST-API-VERSION/PAGE-ID/request_thread_control
  ?recipient={id:PSID}
  &metadata=Information about the conversation
  &access_token=PAGE-ACCESS-TOKEN"
```

Example API Response

On success, your app will receive the following response

```html
{
  "success" : true
}
```

Extend Thread Control

To give your app more time to respond to a message, you can extend control past the 24-hour response time frame. You can extend the time up to 7 days.

To extend control of the conversation, send a `POST` request to `/PAGE-ID/extend_thread_control` with the recipient parameter set to the `PSID` for the customer who sent the message and the duration parameter set to the length of time in seconds.

Sample API Request

```html
curl -X POST "https://graph.facebook.com/LATEST-API-VERSION/PAGE-ID/extend_thread_control
  ?recipient={id:PSID}
  &duration=86400   //Length of time, in seconds
  &access_token=PAGE-ACCESS-TOKEN"
```

Example API Response

On success, your app will receive the following response

```html
{
  "success" : true
}
```

Find the App Control

You can find the app that currently controls the conversation by sending a `GET` request to `/PAGE-ID/thread_owner`, with the recipient parameter set to the Page-scoped ID for the person who sent the message to the Page.

Sample API Request

```html
curl -X GET "https://graph.facebook.com/LATEST-API-VERSION/PAGE-ID/thread_owner
  ?recipient=PSID
  &access_token=PAGE-ACCESS-TOKEN"
```

Example API Response

- If your app is the current thread owner, or if your app is the default app of the page, you will receive the `app_id` and the expiration timestamp in the API response
- If the thread is not idle, you will receive the expiration timestamp in the API response, otherwise, you will receive an empty API response

```html
{
  "data": [
  {
    "thread_owner": {
      "app_id": APP-ID,
      "expiration": UNIX-TIMESTAMP
    }
  }
  ]
}
```

Messaging Feature Status API

You can use the Messaging Feature Status API to check the Conversation Routing status of a Facebook Page for Messenger or a business ID for Instagram Direct (IGD) messaging.

Sample API Request

```html
curl -X GET "https://graph.facebook.com/v12.0/me?fields=messaging_feature_status&access_token=<ACCESS_TOKEN>"
```

Example API Response

```html
{
  "messaging_feature_status": {
  "hop_v2": false,
  "msgr_multi_app": true,
  "ig_multi_app": false
  },
  "id": "<page_id>"
}
```

## See Also

Learn more about the concepts and components of the Messenger Platform for Instagram Messaging.

- [Conversations API](https://www.facebook.com/business/tools/ads-manager/get-started) – Get more information about a conversation
- [Create an ad campaign](https://www.facebook.com/business/tools/ads-manager/get-started)
- [Facebook Page Tasks](https://developers.facebook.com/documentation/business-messaging/messenger-platform/overview#page-tasks) – Learn more about tasks you can perform on a Facebook Page
- [Handover Protocol](https://developers.facebook.com/docs/messenger-platform/handover-protocol) – For routing conversations between 3 or more apps
- [Instagram Messaging from Messenger Platform](https://developers.facebook.com/docs/messenger-platform/instagram)
- [Marketing Messages](https://developers.facebook.com/documentation/business-messaging/instagram-messaging/features/recurring-notifications/ways-to-get-opt-ins) – Learn how to get optins and to send recurring marketing messages
- [Messaging Insights API](https://developers.facebook.com/documentation/business-messaging/messenger-platform/analytics/messaging-insights) – Learn how to get insights into your conversations
- [Policies for using Messenger Platform](https://developers.facebook.com/documentation/business-messaging/messenger-platform/policy) – Learn more about the policies enforced for Messenger Platform
- [Standard Messaging Window](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages#standard-messaging-window) – Learn more about the 24 hour standard messaging window
- [Meta Webhooks for Messenger Platform](https://developers.facebook.com/documentation/business-messaging/messenger-platform/webhooks) – Learn more about setting up a webhooks server to receive Meta Webhooks Notifications
- [Meta Webhooks Topic Reference for Messenger Platform](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/webhook-events) – See examples of webhooks notifications
