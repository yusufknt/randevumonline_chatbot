# Conversations API for Messenger Platform | Developer Documentation

_Source: https://developers.facebook.com/docs/messenger-platform/instagram/features/conversation_

---

# Conversations API for Messenger Platform

Updated: Feb 11, 2026

This document explains how to get information about your Messenger and Instagram Messaging conversations. You can get:

- A list of conversations for your Facebook Page or your Instagram Professional account
- A list of messages within each conversation
- Details about each message including when the message was sent and from who

## Before You Start

This tutorial assumes you have read the [Messenger Platform Overview](https://developers.facebook.com/docs/messenger-platform/instagram/features/docs/messenger-platform/overview) and the [Instagram Messaging Overview](https://developers.facebook.com/docs/messenger-platform/instagram/overview) and implemented the needed components.

You will need:

- The ID for your Facebook Page for your business or the Facebook Page that is linked to your Instagram Professional account
- A Page access token requested from a person who can perform the `MESSAGING` or `MODERATE` task on the Page
- Advanced Access is required to access conversations between your business and people who do not have a role on your messaging app, your Instagram Professional account, your Facebook Page, or your business

For Messenger conversations between people and your Page, your app will need:

- Page access token requested by a person who can perform the [`MESSAGING` or `MODERATE` task](https://developers.facebook.com/docs/pages/overview#tasks) on the Page
- The [`pages_manage_metadata`, `pages_read_engagement`, and `pages_messaging` permissions](https://developers.facebook.com/docs/pages/overview#permissions)

For Instagram Messaging conversations between people and your Instagram Professional account, your app will need:

- A Page access token requested by a person who can perform the [`MESSAGING` task](https://developers.facebook.com/docs/pages/overview#tasks) on the Page linked to your Instagram Business account
- The [`instagram_basic`, `instagram_manage_messages`, and `pages_manage_metadata` permissions](https://developers.facebook.com/docs/pages/overview#permissions)
- Your app must be owned by a verified business

### Limitations

- Only the image or video URL for a share will be included in the data returned in a call to the API or in the webhooks notification.
- If your accounts are linked using private keys, such as an email or phone number, you will not be able to retrieve conversations between these accounts. Only conversations between one Facebook User and one Instagram account will be available. This issue will be resolved when your app has been approved for Advanced Access. If you have multiple accounts linked in the Account Center on the Instagram app, you will be able to retrieve conversations between all linked accounts.
- Conversations that are within the Requests folder that have not been active for 30 days will not be returned in API calls.

You can leverage this API to do inbox syncing on past conversations when an Instagram business account is newly connected to your app.

## Get a List of Conversations

To get a list of conversations, send a `GET` request to the `/PAGE-ID/conversations` endpoint and include the `platform` parameter set to `instagram` or `messenger`.

Sample Request

Formatted for readability

```curl
curl -i -X GET "https://graph.facebook.com/LATEST-API-VERSION/PAGE-ID/conversations
    ?platform=PLATFORM
    &access_token=PAGE-ACCESS-TOKEN"
```

On success, your app will receive a JSON object with a list of IDs for the conversations between you and a person and the most recent time a message was sent.

```json
{
  "data":
    {
      "id": "CONVERSATION-ID-1",
      "updated_time": "UNIX-TIMESTAMP"
    },
    {
      "id": "CONVERSATION-ID-2",
      "updated_time": "UNIX-TIMESTAMP"
    }
    ...
  ]
}
```

### Find a Conversation with a Specific User

To get a conversation between your Instagram Professional account or Facebook Page and a specific person, send a `GET` request to the `/PAGE-ID/conversations` endpoint with `platform` parameter and the `user_id` parameters set to the Instagram-scoped ID or Page-scoped ID for the person.

Sample Request

Formatted for readability

```curl
curl -i -X GET "https://graph.facebook.com/LATEST-API-VERSION/PAGE-ID/conversations
    ?platform=PLATFORM
    &user_id=INSTAGRAM-OR-PAGE-SCOPED-ID
    &access_token=PAGE-ACCESS-TOKEN"
```

On success, your app will receive the ID for the conversation.

```
{
  "data": [
      {
        "id": "CONVERSATION-ID"
      },
  ]
}
```

## Get a List of Messages in a Conversation

To get a list of messages in a conversations, send a `GET` request to the `/CONVERSATION-ID` endpoint and include the `messages` field.

```curl
curl -i -X GET "https://graph.facebook.com/LATEST-API-VERSION/CONVERSATION-ID
    ?fields=messages
    &access_token=PAGE-ACCESS-TOKEN"
```

On success, your app will receive a list of message IDs and the time each message was created.

```
{
  "messages": {
    "data": [
      {
        "id": "Message ID-1",
        "created_time": "UNIX-TIMESTAMP-MOST-RECENT-MESSAGE"
      },
      {
        "id": "Message ID-2",
        "created_time": "UNIX-TIMESTAMP"
      },
      {
        "id": "Message ID-3",
        "created_time": "UNIX-TIMESTAMP"
      },
...
    ]
  },
  "id": "Conversation ID",
}
```

### Get Information about a Message

To get information about a message, such as the sender, receiver, and message content, send a `GET` request to the `/MESSAGE-ID` endpoint with the fields you are interested.

The `reply_to` field is present only when a message is a reply to another message in the thread; the `is_self_reply` flag indicates if the reply is to the sender’s own message.

Default fields are `id` and `created_time`.

**Note:** Queries to the `/CONVERSATION-ID` endpoint will return all message IDs in a conversation. However, you can only get details about the 20 most recent messages in the conversation. If you query a message that is older than the last 20, you will see [an error that the message has been deleted.](https://developers.facebook.com/documentation/business-messaging/messenger-platform/error-codes)

```curl
curl -i -X GET "https://graph.facebook.com/LATEST-API-VERSION/MESSAGE-ID
    ?fields=id,created_time,from,to,message,reply_to
    &access_token=PAGE-ACCESS-TOKEN"
```

On success, your app will receive the following JSON response. In this example a customer sent a plain text message to your Instagram Professional account.

```json
{
  "id": "aWdGGiblWZ...",
  "created_time": "2022-07-12T19:11:07+0000",
  "to": {
    "data": [
      {
        "username": "INSTAGRAM-PROFESSIONAL-ACCOUNT-USERNAME",
        "id": "INSTAGRAM-PROFESSIONAL-ACCOUNT-ID"
      }
    ]
  },
  "from": {
    "username": "INSTAGRAM-USERNAME",
    "id": "INSTAGRAM-SCOPED-ID"
  },
  "message": "Hi Kitty!",
  "reply_to": {
    "mid":"zEspJ9wmRG9…",
    "is_self_reply":true
  }
}
```

## Conversation Ownership Filtering

The Conversations API now supports the `is_owner` field, allowing your app to determine if it is responsible for responding to a conversation thread.

**Why use `is_owner`?**

- Efficiently filter and act only on conversations your app owns.
- Avoid unnecessary ticket creation and reduce operational overhead.
- No need for extra logic to determine thread ownership.

**How to use:**

1. Ensure your app uses [Conversation Routing](https://developers.facebook.com/documentation/business-messaging/messenger-platform/conversation-routing) .
2. Explicitly request the `is_owner` field in your API call.
3. Filter and respond only to threads where `is_owner` is `true` .

**Sample Request:**

```curl
curl -i -X GET "https://graph.facebook.com/LATEST-API-VERSION/conversations?fields=messages,is_owner&access_token=PAGE-ACCESS-TOKEN"
```

**Sample Response:**

```json
{
  "data": [
    {
      "messages": {
        "data": [
          { "id": "Message ID-1", "created_time": "UNIX-TIMESTAMP" },
          { "id": "Message ID-2", "created_time": "UNIX-TIMESTAMP" }
        ]
      },
      "is_owner": true,
      "id": "Conversation ID-1"
    },
    {
      "messages": {
        "data": [
          { "id": "Message ID-3", "created_time": "UNIX-TIMESTAMP" }
        ]
      },
      "is_owner": false,
      "id": "Conversation ID-2"
    }
  ]
}
```

## Learn more

Visit our reference for:

- [The Conversations endpoint](https://developers.facebook.com/docs/graph-api/reference/page/conversations)
- [The Conversation endpoint](https://developers.facebook.com/docs/graph-api/reference/conversation)
- [The Message endpoint](https://developers.facebook.com/docs/graph-api/reference/message)

### Developer Support

- Use the [Meta Status tool](https://metastatus.com) to check for the status and outages of Meta business products.
- Use the [Meta Developer Support tool](https://developers.facebook.com/support) to report bugs and view reported bugs, get help with Ads or Business Manager, and more.
