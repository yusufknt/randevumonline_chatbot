# Welcome message flows | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/ads/ads-welcome-message-flows_

---

# Welcome message flows

Updated: Mar 15, 2026

When creating ads that Click to Messenger or Click to Instagram Direct, you can connect a message flow from a messaging partner app. A message flow can include text, images, emoji, buttons, and other message types supported by the [Messenger Send API](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/send-api) or [Instagram Messaging API](https://developers.facebook.com/docs/messenger-platform/instagram).

This guide explains how to manage welcome message flows via the API endpoint.

## Requirements

You will need:

- A [Page access token](https://developers.facebook.com/docs/pages/overview#tokens) requested by a person who can perform the [`MESSAGING` task](https://developers.facebook.com/docs/pages/overview#tasks) on the Page
- The [`pages_messaging` permission](https://developers.facebook.com/docs/permissions/reference/pages_messaging)

If setting `eligible_platforms` to include `instagram`, your app will also need:

- The [`instagram_basic` permission](https://developers.facebook.com/docs/permissions/reference/instagram_basic)
- The [`instagram_manage_messages` permission](https://developers.facebook.com/docs/permissions/reference/instagram_manage_messages)

## Create a new flow

To create a new welcome message flow, send a `POST` request to the `graph.facebook.com/v25.0/PAGE_ID/welcome_message_flows` endpoint.

### Sample request

```curl
curl -X POST \
-F 'welcome_message_flow=[
   {"message":
      {
       "text":"This is a welcome message authored in a 3P tool",
       "quick_replies":[
           {
             "content_type":"text",
             "title":"Quick reply 1",
             "payload":"Payload 1"
           },
           {
             "content_type":"text",
             "title":"Quick reply 2",
             "payload":"Payload 2"
           },
           {
             "content_type":"text",
             "title":"Quick reply 3",
             "payload":"Payload 3"
           }
        ]
      }
    }
  ]' \
-F 'eligible_platforms=["messenger"]' \
-F 'name="Driver sign up"' \
"https://graph.facebook.com/v25.0/<PAGE_ID>/welcome_message_flows?access_token=<ACCESS-TOKEN>"
```

In response, your app will receive a flow ID.

```json
{"flow_id":"123456789"}
```

### Parameters

| Parameter | Type | Required? | Description |
| --- | --- | --- | --- |
| `name` | string | yes | Name of the flow |
| `welcome_message_flow` | JSON | yes | The welcome message JSON that will be sent upon clicking the ad |
| `eligible_platforms` | Array of strings | yes | The platforms that the welcome message can be shown on (`["instagram", "messenger"]`)<br>Note: Each Welcome Message will be validated against the platform(s) specified and will only be accepted if the message type in the welcome message is supported on the specified platform(s). |

## Update an existing flow

To update an existing flow, send a `POST` request to the `graph.facebook.com/v14.0/PAGE_ID/welcome_message_flows` endpoint with:

- the `flow_id` parameter set to the ID of the flow being updated
- optionally, the other parameters ( `name` , `welcome_message` , `platforms` ) that need to be updated

A flow that is currently connected to an advertisement cannot be updated. Check the `is_used_in_ad` field to determine whether a flow is connected to an advertisement.

### Sample request

```curl
curl -X POST\
-F 'flow_id="123456789"'\
-F 'eligible_platforms=["messenger", "instagram"]' \
-F 'name="Driver sign up - updated"' \
"https://graph.facebook.com/v14.0/{PAGE-ID}/welcome_message_flows?access_token={ACCESS-TOKEN}"
```

In response, your app will receive a success message or the appropriate error message.

```json
{"success":true}
```

### Parameters

| Parameter | Type | Required? | Description |
| --- | --- | --- | --- |
| `flow_id` | string | yes | The identifier of the flow to update |
| `name` | string | no | Name of the flow |
| `welcome_message_flow` | JSON | no | The welcome message that will be sent upon clicking the ad |
| `eligible_platforms` | Array of strings | no | The platforms that the flow can be applied to (`["instagram", "messenger"]`) |

To make an update, at least one of the three optional parameters must be provided.

## Read

### Get a list of flows

To get a list of flows for the page, send a `GET` request to `graph.facebook.com/v14.0/PAGE-ID/welcome_message_flows`

Sample request

```curl
curl -X GET \
"https://graph.facebook.com/v14.0/{PAGE-ID}/welcome_message_flows?access_token={ACCESS-TOKEN}"
```

On success, your app will receive a list of flows created for that particular app.

```json
[
  {
    "id":"123456789",
    "name":"Driver Sign up",
    "welcome_message":"<JSON String>",
    "eligible_platforms": ["instagram", "messenger"],
    "last_update_time":"2023-09-01T05:20:38+0000",
    "is_used_in_ad": false // indicates whether or not a flow is used in an ad
  },
  {
    "id":"4362",
    "name":"Basic Triage",
    "welcome_message":"<JSON String>",
    "eligible_platforms": ["instagram"],
    "last_update_time":"2023-08-25T08:21:48+0000",
    "is_used_in_ad": true
  },
  {
    "id":"234564",
    "name":"Appointment Schedule",
    "welcome_message":"<JSON String>",
    "eligible_platforms": ["messenger"],
    "last_update_time":"2023-08-20T07:43:00+0000",
    "is_used_in_ad": true
  }
  ...
  ...
  ...,
  {
    "id":"6987565",
    "name":"Car Leads",
    "welcome_message":"<JSON String>",
    "eligible_platforms": ["instagram", "messenger"],
    "last_update_time":"2023-07-21T05:21:48+0000",
    "is_used_in_ad": false
  },
]
```

### Get a specific flow

To get a specific flow, send a `GET` request to `graph.facebook.com/v14.0/PAGE-ID/welcome_message_flows` with the `flow_id` parameter set to the `flow_id` being queried.

Sample request

```curl
curl -X GET \
-F 'flow_id="123456789"'
"https://graph.facebook.com/v14.0/{PAGE-ID}/welcome_message_flows?access_token={ACCESS-TOKEN}"
```

On success, your app will receive the flow in JSON format.

```json
[
  {
    "id":"123456789",
    "name":"Driver Sign up",
    "welcome_message":"<JSON String>",
    "eligible_platforms": ["instagram", "messenger"],
    "last_update_time":"2023-09-01T05:20:38+0000",
    "is_used_in_ad": false
  },
]
```

Parameters

| Parameter | Type | Required? | Description |
| --- | --- | --- | --- |
| `flow_id` | string | no | The identifier of the flow to fetch |
| `limit` | int | no | Maximum number of flows to fetch |

## Delete

To delete a flow, send a `DELETE` request to `graph.facebook.com/v14.0/PAGE-ID/welcome_message_flows` with the `flow_id` parameter set to the ID of the flow that is being deleted.

A flow that is currently connected to an advertisement cannot be deleted. Check the `is_used_in_ad` field to determine whether a flow is connected to an advertisement.

### Sample request

```curl
curl -X DELETE \
-F 'flow_id="1234567890"'
"https://graph.facebook.com/v14.0/{PAGE-ID}/welcome_message_flows?access_token={ACCESS-TOKEN}"
```

In response, your app will receive a success message or the appropriate error message.

```json
{"success":true}
```

### Parameters

| Parameter | Type | Required? | Description |
| --- | --- | --- | --- |
| `flow_id` | string | yes | The identifier of the flow to delete |

## Ads Manager experience

Once welcome message flows have been successfully submitted over the API, they will show up in Ads Manager for messaging destinations within the Engagement and Sales objectives. The flows will show up in the Partner App option within the Message Template section of the Ad Creative.

### Example use

In the Message Template section of the Ad Creative, select Partner App.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/642810699_1445181620673821_9064167414171522750_n.png?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=kmKZUGIXhvgQ7kNvwGzqNkD&_nc_oc=AdqtOANoQQbWGZeNL76XXHyLhgCXHkpA36IhasPheu8N2urodq9RMD9fBUxHLQtzLHg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=W8iB2i3aNdUKEn_gdPfeXw&_nc_ss=7b20f&oh=00_Af7FT5H1RHg3bAAnSRu-gCJX85ctrcNOm9CV5SZzBhi-yw&oe=6A1C3AF2)

Select the appropriate messaging Partner App.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/643365635_1445181374007179_3373605531625520350_n.png?_nc_cat=106&ccb=1-7&_nc_sid=e280be&_nc_ohc=lgAx35CF5V8Q7kNvwEdusj3&_nc_oc=AdqHwUt8Bt5IrhpzcekRNlpZlbIrI8YA-QdM6z1m1z9HsoXz373r_tv0uokLmH-u6Vo&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=W8iB2i3aNdUKEn_gdPfeXw&_nc_ss=7b20f&oh=00_Af4nYYT6xLmpd2NubSpWpJc2Ks3ebw5aaldLcOgLh4Clrg&oe=6A1C1367)

Select the Welcome Message Flow that you submitted via the API.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/642787941_1445181677340482_4974191698556784172_n.png?_nc_cat=110&ccb=1-7&_nc_sid=e280be&_nc_ohc=2kyChUAVLDcQ7kNvwGFpfCg&_nc_oc=Adru6nIP4Y38bADIIoalDXTyQWqGIP50IpqmjbeKm9DwLRT5cDP4jfEATuxXw4FalLA&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=W8iB2i3aNdUKEn_gdPfeXw&_nc_ss=7b20f&oh=00_Af4bNQCPUK_TsBmjz3hlbGX4_KkpN2Jm-wT6PkrWDDig-Q&oe=6A1C10BB)

Preview your message flow.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/641496932_1445181597340490_1653095472374780192_n.png?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=MW0FeSHJ-5sQ7kNvwH6Wiwm&_nc_oc=AdqEwgCQX8UPJX6hMDdPJGQm6geWrQIWfyyA9LTvtIHwBeN7-gN97tczR8g7w4HZjCY&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=W8iB2i3aNdUKEn_gdPfeXw&_nc_ss=7b20f&oh=00_Af5PXgDYB8hZUvP-fsscINSp_8MiIk219yeIbG_XsJsDBQ&oe=6A1C46EB)

## Marketing API Experience

Once welcome message flows have been successfully submitted over the API, the flow ID can be used to configure ads through the marketing API.

In the ad creative, the flow ID can be set as follows:

```json
{
  "name": "creative",
  "object_story_spec": {...},
  "asset_feed_spec": {
    "additional_data": {
      "partner_app_welcome_message_flow_id": "<FLOW_ID_RETURNED_FROM_POST_REQUEST>"
    }
  }
}
```

For more information about messaging ads, please refer to [Messaging Ads](https://developers.facebook.com/documentation/ads-commerce/marketing-api/ad-creative/messaging-ads) in the Marketing API documentation.
