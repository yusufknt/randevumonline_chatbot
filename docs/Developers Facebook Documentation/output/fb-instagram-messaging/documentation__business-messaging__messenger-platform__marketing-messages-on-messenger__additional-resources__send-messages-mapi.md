# Send Messages with the Marketing API | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/additional-resources/send-messages-mapi_

---

# Send Messages with the Marketing API

Updated: Mar 31, 2026

Instead of using the Marketing Message API for Messenger to create and send marketing messages, you can use the [Marketing API](https://developers.facebook.com/documentation/ads-commerce/marketing-api/get-started/basic-ad-creation).

## Create an ad creative

When creating the [ad creative](https://developers.facebook.com/documentation/ads-commerce/marketing-api/get-started/basic-ad-creation/create-an-ad-creative) you’ll use the `marketing_message_structured_spec` in addition to the `object_story_spec` parameter.

- `language` in `marketing_message_structured_spec` is a mandatory field and must be set

**Personalization**: You may also add personalization macros to the `name`, `message`, and `greeting` fields for all formats. Specifically, you can add `{{first_name}}`, `{{last_name}}`, and `{{full_name}}` into your `name`, `message`, and `greeting` strings to enable personalized marketing messages. For example, you may enter the `greeting` field as `"New sale for you, {{first_name}}!"`. For a user with full name “John Doe”, the rendered message title will be `"New sale for you, John!"`.

- For carousel messages, you may add personalization macros to the `description` of each element in the `child_attachments` and in the `message` .
- Buttons do not have personalization enabled.

Example image request

```html
curl -X POST "https://graph.facebook.com/<API_VERSION>/act_<AD_ACCOUNT_ID>/adcreatives" \
     -F 'access_token=<SYSTEM_USER_ACCESS_TOKEN>' \
     -F 'name=<MARKETING_MESSAGES_AD_CREATIVE>' \
     -F 'object_story_spec={
          "page_id": "<PAGE_ID>",
          "link_data": {
            "image_hash": <IMAGE_HASH>,
            "link": "<URL>",
            "name": "<NAME>",
            "message": "<MESSAGE_BODY>"
          }
        }'
     -F 'marketing_message_structured_spec={
          "buttons": [
            {
              "text": "<BUTTON_TEXT>",
              "type": "URL",
              "url": "<URL>",
            }
          ],
          "language": "<LOCALE>",
          "greeting": "<GREETING_TEXT>"
        }'
```

On success your app receives a JSON object with the creative ID.

```html
{ "id": "<CREATIVE_ID>" }
```

Example video request

```html
curl -X POST "https://graph.facebook.com/<API_VERSION>/act_<AD_ACCOUNT_ID>/adcreatives" \
     -F 'access_token=<SYSTEM_USER_ACCESS_TOKEN>' \
     -F 'name=<MARKETING_MESSAGES_AD_CREATIVE>' \
     -F 'object_story_spec={
          "page_id": "<PAGE_ID>",
          "video_data": {
            "video_id": <VIDEO_ID>,
            "image_url": "<THUMBNAIL_URL>",
            "message": "<MESSAGE_BODY>"
          }
        }'
     -F 'marketing_message_structured_spec={
          "buttons": [
            {
              "text": "<BUTTON_TEXT>",
              "type": "URL",
              "url": "<URL>",
            }
          ],
          "language": "<LOCALE>",
          "greeting": "<GREETING_TEXT>"
        }'
```

On success your app receives a JSON object with the creative ID.

```html
{ "id": "<CREATIVE_ID>" }
```

Preview creative example request

```html
curl -GET "https://graph.facebook.com/<API_VERSION>/<AD_CREATIVE_ID>/previews \
  ?ad_format=MESSENGER_MARKETING_MESSAGES_MEDIA \
  &access_token=<SYSTEM_USER_ACCESS_TOKEN>"
```

## Create a Direct Campaign

For marketing messages campaigns, you create a Direct Campaign. Direct Campaigns allow you to send marketing messages to specific subscribers based on a business’ own targeting and segmentation data, as well as build complex flows for different use cases.

To create a direct campaign, send a `POST` request to the `/act_<AD_ACCOUNT_ID>/campaigns` endpoint with the following parameters:

- `name` – set to the campaign’s name
- `objective` – set to `OUTCOME_TRAFFIC` `status` – set to `PAUSED`
- `special_ad_categories` – set to an empty array `is_message_campaign` – set to `true``is_direct_send_campaign` – set to `true`

Example request

```html
curl -X POST  "https://graph.facebook.com/<API_VERSION>/act_<AD_ACCOUNT_ID>/campaigns?access_token=<SYSTEM_USER_ACCESS_TOKEN>"
     -F 'name=<CAMPAIGN_NAME>' \
     -F 'objective=OUTCOME_TRAFFIC' \
     -F 'status=PAUSED' \
     -F 'special_ad_categories=[]' \
     -F 'is_message_campaign=true' \
     -F ‘is_direct_send_campaign=true'
```

On success your app receives a JSON object with the marketing messages direct campaign ID. This ID is needed to create a message set (adset specific for a marketing messages campaign).

```html
{ "id": "<CAMPAIGN_ID>" }
```

## Create a message set

Build message sets with one of the following options:

- Evergreen - message sets that require a daily budget
- Lifetime – time-bound message sets that require a lifetime budget

To create a message set, send a `POST` request to the `/act_<AD_ACCOUNT_ID>/adsets` endpoint with the following parameters:

- `billing_event` – set to `IMPRESSIONS`
- `campaign_id` – set to the campaign ID
- `name` – set to the message set’s name
- `optimization_goal` – set to `REACH`
- `pacing_type` – set to an array with `"no_pacing"`
- `status` - set to `PAUSED`
- `targeting` – set to an object with the following properties: `publisher_platforms` – set to an array with `"messenger"``messenger_positions` – set to an array with `"marketing_messages"`

For a Lifetime message set include the following parameters:

- `lifetime_budget` – set to the budget for the lifetime of the campaign, in cents
- `end_time` – set to the time the campaign ends
- `start_time` – set to the time the campaign starts

For an Evergreen message set include the following parameters:

- `daily_budget` – set to the daily budget, in cents

Example request

```html
curl -X POST  "https://graph.facebook.com/<API_VERSION>/act_<AD_ACCOUNT_ID>/adsets?access_token=<SYSTEM_USER_ACCESS_TOKEN>"
     -F 'name=<SET_NAME>'  \
     -F 'optimization_goal=REACH' \
     -F 'billing_event=IMPRESSIONS' \
     -F 'lifetime_budget=100' \
     -F "campaign_id=${CAMPAIGN_ID}" \
     -F 'start_time="2023-11-02T04:45:17+0000"' \
     -F 'end_time="2023-12-02T04:45:17+0000"' \
     -F 'targeting: {
          "publisher_platforms": ["messenger"],
          "messenger_positions": ["marketing_messages"]
        }' \
     -F 'status=PAUSED' \
     -F 'pacing_type: ["no_pacing"]'
```

On success your app receives a JSON object with the message set ID. This ID is needed to create a marketing message.

```html
{ "id": "<CAMPAIGN_ID>" }
```

Guidance for minimum `lifetime budget`:

- Minimum budget per day for currency can be obtained from `minimum_budgets` call `min_daily_budget_imp` value . In order to get a minimum lifetime budget, multiply `min_daily_budget_imp` value with lifetime(End date - start date) of message set. For example if `min_daily_budget_imp` for USD is 100 cents and you plan to run message campaign for 30 days, `minimum lifetime_budget` should be $30

**NOTE:** Amount denomination - ad account currencies minimum denomination level, such as cents for USD.

## Create a marketing message

To create a marketing message (the ad), send a `POST` request to the `/act_<AD_ACCOUNT_ID>/ads` endpoint with the following parameters:

- `adset_id` – set to the message set ID
- `creative` – set to an object with `creative_id` set to the ad creative ID
- `name` – set to the message’s name
- `status` - set to `PAUSED`

Example request

```html
curl -X POST  "https://graph.facebook.com/<API_VERSION>/act_<AD_ACCOUNT_ID>/ads?access_token=<SYSTEM_USER_ACCESS_TOKEN>"
     -F 'name=<MESSAGE_NAME>'  \
     -F 'adset_id=<MESSAGE_SET_ID>' \
     -F 'creative={creative_id: <CREATIVE_ID>}' \
     -F 'status=PAUSED'
```

On success your app receives a JSON object with the message set ID. This ID is needed to create a marketing message.

```html
{ "message_id": "<MESSAGE_ID>" }
```

## Publish the campaign

When you are ready to start sending messages, update the status of the campaign, message set, and message to `ACTIVE`.

Send `POST` requests to the `/<CAMPAIGN_ID>`, `/<MESSAGE_SET_ID>`, and `/<MESSAGE_ID>` endpoints with `status` set to `ACTIVE`.

Example request

```html
curl -X POST  "https://graph.facebook.com/<API_VERSION>/<ID>?access_token=<SYSTEM_USER_ACCESS_TOKEN>"
     -F 'status=ACTIVE'
```

## Send marketing messages

Once your Direct Campaign is active, you can send marketing messages from a business’ Facebook Page to specific users using the user’s `subscription_token`.

In order to use the Direct Send API, the message set, and the message must be created under a direct campaign. This API will not work if the top level campaign is not a direct campaign.

Visit our [Get Subscription Tokens guide](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/get-subscription-tokens) to learn how to get a business’ subscription tokens.

Limitations

- You can only send one message every 12 hours, per `subscription_token` . If you are sending multiple messages be sure to delay subsequent messages by 12 hours or you will receive an error.
- Within 90 days of each campaign, you can only send one message to the same `subscription_token` .

To send a message to a subscriber, send a `POST` request to the `/act_<AD_ACCOUNT_ID>/messages` endpoint with the following parameters:

- `message_id` – set to message ID
- `messenger_delivery_data` – set to an object with `subscription_token` set to the subscriber’s token
- `message` – set to the content of the message

Example request

```html
curl -X POST  "https://graph.facebook.com/<API_VERSION>/act_<AD_ACCOUNT_ID>/messages?access_token=<SYSTEM_USER_ACCESS_TOKEN>"
     -F 'messenger_delivery_data = {subscription_token: <SUBSCRIPTION_TOKEN>}'
     -F 'message_id = <MESSAGE_ID>' \
     -F 'message = <MESSAGE_CONTENT>'
```

On success your app receives a JSON object with `success` set to `true`.

```html
{ "success": true }
```

## Delivery estimation

Use the Delivery Estimation API to provide an estimate of the number send message API calls for a given budget. This estimate is based on factors such as budget and number of available subscribers. This is an estimate and true numbers may vary.

To get a delivery estimation, send a `GET` request to the `/act_<AD_ACCOUNT_ID>/message_delivery_estimate` endpoint with the following parameters:

- `daily_budget` – set to daily spend, in cents, **or** `lifetime_budget` – set to lifetime spend, in cents
- `fields` – set to a comma separated list with `estimate_delivery_upper_bound` and `estimate_delivery_lower_bound`
- `is_direct_send_campaign` – set to `true`
- `promoted_object` – set to an object with `page_id` set to the business’ Facebook Page ID
- `targeting_spec` – set to an object with the following properties: `publisher_platforms` – set to an array with `"messenger"``messenger_positions` – set to an array with `"marketing_messages"`

Example request

```html
curl -X GET  "https://graph.facebook.com/<API_VERSION>/act_<AD_ACCOUNT_ID>/message_delivery_estimate"
     -H "Authorization: Bearer <SYSTEM_USER_ACCESS_TOKEN>" \
     -d 'fields=estimate_delivery_upper_bound,estimate_delivery_lower_bound' \
     -d 'targeting_spec={messenger_positions: ["marketing_messages"], publisher_platforms:["messenger"]}' \
     -d 'promoted_object={page_id: <PAGE_ID>}' \
     -d 'daily_budget=<BUDGET_IN_CENTS>' \
     -d ‘is_direct_send_campaign=true'
```

On success your app receives a JSON object with the estimated upper and lower bound, the estimated most and least number of API calls for the budget.

```html
{
  "data": [
    {
      "estimate_delivery_upper_bound": <UPPER_BOUND_ESTIMATED_NUMBER_API_CALLS>,
      "estimate_delivery_lower_bound": <LOWER_BOUND_ESTIMATED_NUMBER_API_CALLS>,
    }
  ]
}
```

## Next steps

You’ve sent messages, now it’s time to [measure their performance](http://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/measure-performance).
