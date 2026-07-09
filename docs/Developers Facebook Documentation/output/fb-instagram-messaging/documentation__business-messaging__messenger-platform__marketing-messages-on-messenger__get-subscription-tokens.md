# Get subscription tokens with Marketing Message API for Messenger | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/get-subscription-tokens_

---

# Get subscription tokens with Marketing Message API for Messenger

Updated: Mar 31, 2026

This guide shows how a business using your app can get a list of their existing subscription tokens and increase their number of subscribers. A subscription token represents a person who has subscribed, opted in to receiving marketing messages from a business’ Facebook Page.

## Get existing tokens

If a business already has subscribers there are a number of ways to get a list of subscription tokens. If your business does not have subscribers or you would like to increase the number, learn how to [grow your marketing messages audience](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/grow-marketing-messages-audience).

### Get subscription tokens for a business’ Facebook Page

Send a `GET` request to the `/<PAGE_ID>/notification_message_tokens` endpoint, where `<PAGE_ID>` represents the business’ Facebook Page, to get a list of all the subscription tokens for that Facebook Page.

```html
curl -i -X GET "https://graph.facebook.com/<API_VERSION>/<PAGE_ID>/notification_message_tokens" \
        -H "Authorization: Bearer <PAGE_ACCESS_TOKEN>"
```

| Parameter | Type | Required | Description | Example |
| --- | --- | --- | --- | --- |
| `limit` | Number | false | The maximum number of tokens to return in a single request.Default: 100Maximum: 1000 | `limit=100` |
| `do_not_return_duplicates` | Boolean | false | If true, prevents returning multiple tokens for the same recipient.Use to avoid sending multiple Marketing Messages to the same recipient. | `do_not_return_duplicates=true` |
| `custom_audience_ids` | Array | false | Filters subscription tokens for one or more custom audience IDs.To safeguard user privacy, the endpoint will only return subscription tokens for a Custom Audience if there are 100 or more matched users in the upload. If fewer than 100 users match, tokens for that Custom Audience will be excluded from the response. | `custom_audience_ids=123456789,9876543211` |

On success, your app receives a JSON response consisting of tokens with the following fields:

- The customer’s subscription token
- The customer’s Page-scoped ID (PSID)
- The time the token was created
- The message’s title
- Time at which your app can send the next marketing message to that recipient
- Time at which the token expires
- Token status
- Re-opt-in status
- The customer’s timezone

For tokens that were created during Custom Audience upload, the response fields are limited to the following:

- The customer’s subscription token
- The message’s title
- Re-opt-in status
- Custom audience IDs that the token has matched in

```html
{
  "data":[
    {
      "notification_messages_token":"<SUBSCRIPTION_TOKEN_ID_1>",
      "recipient_id":"<PSID_1>",
      "notification_messages_reoptin":"<RE_OPT_IN_STATUS>",
      "creation_timestamp":<TIMESTAMP>,
      "token_expiry_timestamp":<UNIX_TIMESTAMP_EXPIRATION_DATE>,
      "user_token_status":"<TOKEN_STATUS>",
      "topic_title":"<NOTIFICATION_TITLE>",
      "notification_messages_timezone":"<TIMEZONE_ID>",
      "next_eligible_time": <TIMESTAMP>
    },
...
    {
      "notification_messages_token":"<SUBSCRIPTION_TOKEN_ID_1>",
      "topic_title":"<NOTIFICATION_TITLE>",
      "notification_messages_reoptin":"<RE_OPT_IN_STATUS>",
      "custom_audience_ids": [
        "<CUSTOM_AUDIENCE_ID>",
        "<CUSTOM_AUDIENCE_ID>",
        "<CUSTOM_AUDIENCE_ID>"
      ]
    },
  ],
  "paging":{"cursors":{"before":"QVFIU...","after":"QVFIU..."},"next":"https:\/\/graph.facebook.com\/<API_VERSION>\/<PAGE_ID>\/notification_message_tokens?access_token=<pPAGE_ACCESS_TOKEN>"}
```

## Get token information

If you already have the subscription token, you can send a `GET` request to the `/notification_messages_<NOTIFICATION_MESSAGES_TOKEN>` endpoint to get information about the token.

```html
curl -i -X GET "https://graph.facebook.com/<API_VERSION>/notification_messages_<SUBSCRIPTION_TOKEN_ID>" \
        -H "Authorization: Bearer <PAGE_ACCESS_TOKEN>"
```

On success, your app receives the following JSON response which includes the following:

- The customer’s subscription token
- The customer’s Page-scoped ID
- The time the token was created
- The message’s title
- Time at which your app can send the next marketing message to that recipient
- Time at which the token expires
- Token status
- Re-opt-in status
- The customer’s timezone

```html
{
  "notification_messages_token": "<SUBSCRIPTION_TOKEN_ID>",
  "recipient_id": "<PSID>",
  "creation_timestamp": "<TIMESTAMP>",
  "token_expiry_timestamp": "<TIMESTAMP>",
  "user_token_status": "REFRESHED",
  "notification_messages_reoptin": "ENABLED",
  "notification_messages_timezone": "<TIMEZONE_ID>"
  "next_eligible_time": <TIMESTAMP>
}
```

For tokens that were created during Custom Audience upload, the response fields are limited to the following:

- The customer’s subscription token
- The message’s title
- Re-opt-in status
- Custom audience IDs that the token has matched in

```html
{
  "notification_messages_token":"<SUBSCRIPTION_TOKEN_ID_1>",
  "topic_title":"<NOTIFICATION_TITLE>",
  "notification_messages_reoptin":"<RE_OPT_IN_STATUS>",
  "custom_audience_ids": [
    "<CUSTOM_AUDIENCE_ID>",
    "<CUSTOM_AUDIENCE_ID>",
    "<CUSTOM_AUDIENCE_ID>"
  ]
},
```

## Next steps

Now that you have subscription tokens, start [sending marketing messages](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/send-messages).
