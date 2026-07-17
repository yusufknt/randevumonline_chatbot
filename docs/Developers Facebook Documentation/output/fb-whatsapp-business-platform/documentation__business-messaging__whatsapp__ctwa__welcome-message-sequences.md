# Welcome Message Sequences - API Guide | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/ctwa/welcome-message-sequences_

---

# Welcome Message Sequences - API Guide

Updated: Nov 17, 2025

When creating Click-to-WhatsApp ads, you can connect a Welcome Message Sequence from your messaging app. A sequence can include text, prefilled message, and FAQs.

This guide explains how to manage Welcome Message Sequences via the API endpoint.

## Requirements

Your app must be granted the **whatsapp_business_management** permission.

## Endpoints

```html
// Create a new sequence / Change an existing sequence
POST /<WHATSAPP_BUSINESS_ACCOUNT_ID>/welcome_message_sequences
```

```html
// Get a list of sequences / Get a specific sequence
GET /<WHATSAPP_BUSINESS_ACCOUNT_ID>/welcome_message_sequences
```

```html
// Delete a sequence
DELETE /<WHATSAPP_BUSINESS_ACCOUNT_ID>/welcome_message_sequences
```

## Create a sequence

To upload a new welcome message sequence, send a `POST` request to the `WHATSAPP_BUSINESS_ACCOUNT_ID/welcome_message_sequences` endpoint.

### Endpoint

```html
// Create a new sequence
POST /<WHATSAPP_BUSINESS_ACCOUNT_ID>/welcome_message_sequences
```

### Sample request

```curl
curl -X POST\
-F 'welcome_message_sequence=
      {
       "text":"This is a welcome message authored in a 3P tool",
"autofill_message": {"content": "Hello! Can I get more info on this!"},
"ice_breakers":[
    {"title":"Quick reply 1"},
           {"title":"Quick reply 2"},
           {"title":"Quick reply 3"}
        ]
      }' \
-F 'name="Driver sign-up"' \
"https://graph.facebook.com/v14.0/WhatsappBusinessAccount/welcome_message_sequences"
-H 'Authorization: Bearer <ACCESS_TOKEN>'
```

### Sample response

The response includes a welcome message sequence ID.

```json
{"sequence_id":"186473890"}
```

### Parameters

| Parameter | Description | Sample Value |
| --- | --- | --- |
| `sequence_id`<br>*String* | **Required**<br>Identifier of the sequence. | `186473890` |
| `name`<br>*String* | **Required**<br>Name of the sequence. | `Driver sign-up` |
| `welcome_message_sequence`<br>*JSON Object* | **Required**<br>The welcome message JSON that will be sent upon clicking the ad. | `{<br> "text":"This is a welcome message authored in a 3P tool",<br> "autofill_message": {"content": "Hello! Can I get more info on this!"},<br> "ice_breakers":[<br> {"title":"Quick reply 1"},<br> {"title":"Quick reply 2"},<br> {"title":"Quick reply 3"}<br> ]<br>}` |

## Change an existing sequence

A sequence linked to an active ad cannot be deleted.

To update an existing sequence, send a `POST` request to the `WHATSAPP_BUSINESS_ACCOUNT_ID/welcome_message_sequences` endpoint with:

- The `sequence_id` parameter set to the ID of the sequence being updated
- Other parameters, like `name` or `welcome_message_sequence` , that need to be updated.

### Endpoint

```html
// Change an existing sequence
POST /<WHATSAPP_BUSINESS_ACCOUNT_ID>/welcome_message_sequences
```

### Sample request

```curl
curl -X POST\
-F 'sequence_id="186473890"'\
-F 'name="Driver sign-up updated name"' \
"https://graph.facebook.com/v14.0/395394933592466/welcome_message_sequences"
-H 'Authorization: Bearer BEAiil...'
```

### Sample response

The response includes a success or error message.

```json
{"success": true}
```

### Parameters

| Placeholder | Description | Sample Value |
| --- | --- | --- |
| `sequence_id`<br>*String* | **Required**<br>Identifier of the sequence. | `186473890` |
| `name`<br>*String* | **Optional**<br>Name of the sequence. | `Driver sign-up` |
| `welcome_message_sequence`<br>*JSON Object* | **Optional**<br>The welcome message JSON that will be sent upon clicking the ad. | `{<br> "text":"This is a welcome message authored in a 3P tool",<br> "autofill_message": {"content": "Hello! Can I get more info on this!"},<br> "ice_breakers":[<br> {"title":"Quick reply 1"},<br> {"title":"Quick reply 2"},<br> {"title":"Quick reply 3"}<br> ]<br>}` |

## Get a list of sequences

To get an existing sequence, send a `GET` request to the `WHATSAPP_BUSINESS_ACCOUNT_ID/welcome_message_sequences` endpoint.

### Endpoint

```html
// Get a list of sequences
GET /<WHATSAPP_BUSINESS_ACCOUNT_ID>/welcome_message_sequences
```

### Sample request

```curl
curl -X GET "https://graph.facebook.com/v14.0/395394933592466/welcome_message_sequences"
     -H 'Authorization: Bearer BEAiil...'
```

### Sample response

On success, the API returns a list of sequences for that app.

```json
[
  {
    "sequence_id":"8716291",
    "name":"Driver Sign up",
    "welcome_message_sequence":"<JSON_OBJECT>",
    "is_used_in_ad": true
  },
  {
    "sequence_id":"4362",
    "name":"Basic Triage",
    "welcome_message_sequence":"<JSON_OBJECT>",
    "is_used_in_ad": false
  },
  {
    "sequence_id":"0139138",
    "name":"Appointment Schedule",
    "welcome_message_sequence":"<JSON_OBJECT>",
    "is_used_in_ad": true
  }
  ...
  ...
  ...,
  {
    "sequence_id":"6987565",
    "name":"Car Leads",
    "welcome_message_sequence":"<JSON_OBJECT>",
    "is_used_in_ad": false
  }
]
```

## Get a specific sequence

To get a specific sequence, send a `GET` request to `WHATSAPP_BUSINESS_ACCOUNT_ID/welcome_message_sequences` with the `sequence_id` parameter set to the ID of the sequence you want to query.

### Endpoint

```html
// Get a specific sequence
GET /<WHATSAPP_BUSINESS_ACCOUNT_ID>/welcome_message_sequences
```

### Sample request

```curl
curl -X GET \
-F 'sequence_id="6987565"'
"https://graph.facebook.com/v14.0/395394933592466/welcome_message_sequences"
-H 'Authorization: Bearer BEAiil...'
```

### Sample response

On success, the API returns the requested sequence.

```json
[
  {
    "sequence_id":"6987565",
    "name":"Driver Sign up",
    "welcome_message_sequence":"<JSON_OBJECT>",
    "is_used_in_ad": false
  }
]
```

| Placeholder | Description | Sample Value |
| --- | --- | --- |
| `sequence_id`<br>*String* | **Optional**<br>Identifier of the sequence. | `186473890` |
| `limit`<br>*int* | **Optional**<br>Number of sequences to fetch. | `5` |

## Delete a sequence

A sequence linked to an active ad cannot be deleted.

To delete a sequence, send a `DELETE` request to `WHATSAPP_BUSINESS_ACCOUNT_ID/welcome_message_sequences` with the `sequence_id` parameter set to the ID of the sequence you want to delete.

### Endpoint

```html
// Delete a sequence
DELETE /<WHATSAPP_BUSINESS_ACCOUNT_ID>/welcome_message_sequences
```

### Sample request

```curl
curl -X DELETE \
-F 'sequence_id="1234567890"'
"https://graph.facebook.com/v14.0/395394933592466/welcome_message_sequences"
-H 'Authorization: Bearer BEAiil...'
```

### Sample response

On success, the API returns a success confirmation.

```curl
{"success":true}
```

| Placeholder | Description | Sample Value |
| --- | --- | --- |
| `sequence_id`<br>*String* | **Optional**<br>Identifier of the sequence. | `186473890` |

## Webhook

The following webhook is triggered when a conversation is started after a user clicks an ad with a Click to WhatsApp’s call-to-action.

```json
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "ID",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "PHONE_NUMBER",
              "phone_number_id": "PHONE_NUMBER_ID"
            },
            "contacts": [
              {
                "profile": {
                  "name": "NAME"
                },
                "wa_id": "ID"
              }
            ],
            "messages": [
              {
                "referral": {
                  "source_url": "AD_OR_POST_FB_URL",
                  "source_id": "ADID",
                  "source_type": "ad or post",
                  "headline": "AD_TITLE",
                  "body": "AD_DESCRIPTION",
                  "media_type": "image or video",
                  "image_url": "RAW_IMAGE_URL",
                  "video_url": "RAW_VIDEO_URL",
                  "thumbnail_url": "RAW_THUMBNAIL_URL",
                  "ctwa_clid": "CTWA_CLID",
                  "ref": "REF_ID",  // New field in referral

                },
                "from": "SENDER_PHONE_NUMBERID",
                "id": "wamid.ID",
                "timestamp": "TIMESTAMP",
                "type": "text",
                "text": {
                  "body": "BODY"
                }
              }
            ]
          },
          "field": "messages"
        }
      ]
    }
  ]
}
```

## Marketing API experience

After you submit welcome message sequences through the API, use the sequence ID to configure ads through the Marketing API.

In the ad creative, the sequence ID can be set as follows:

```json
{
  "name": "creative",
  "object_story_spec": {...},
  "asset_feed_spec": {
    "additional_data": {
      "partner_app_welcome_message_flow_id": "<SEQUENCE_ID_RETURNED_FROM_POST_REQUEST>"
    }
  }
}
```

For more information about messaging ads, refer to [Messaging Ads](https://developers.facebook.com/documentation/ads-commerce/marketing-api/ad-creative/messaging-ads) in the Marketing API documentation.

## Ads Manager experience walk-through

1: In the **Message Template** section of the Ad Creative, select **Partner App**

![Message Template section showing Partner App option](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/561087025_1339318031260181_8367304189521626982_n.jpg?_nc_cat=106&ccb=1-7&_nc_sid=e280be&_nc_ohc=HwNjsfm9wWcQ7kNvwE1_3Hs&_nc_oc=AdqAnH2PteMxrSXO_QfzJcydn4-11Pqh2JqPZ6exYNIqD7868hddQGh4-0nhD_s9a6E&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=SJxzrHgvGPwo0zrqSux1-g&_nc_ss=7b20f&oh=00_Af67q-DgRBnz3SKaQKa7AdjylbCSpS4Cy94p81S6zVNsng&oe=6A1C015B)

1. Click the **Partner app** dropdown and select the appropriate messaging partner app.

![Partner app dropdown menu selection](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/560623753_1339318387926812_2606718298067002828_n.jpg?_nc_cat=101&ccb=1-7&_nc_sid=e280be&_nc_ohc=0qrLr1tmDBgQ7kNvwF1vmOo&_nc_oc=AdptwWhjPYFH7XsZ16SnSZtGQ65KNnpOO5F80XFOfm1z_Td9F8GI8UcxqbuBR8L2g1Q&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=SJxzrHgvGPwo0zrqSux1-g&_nc_ss=7b20f&oh=00_Af4ym_q_5ZbACoeGNvxTq_fUurCAY4VLdNEvhihuySfIgA&oe=6A1C247C)

3: Under **Message sequence**, select the Welcome Message Sequence that you submitted via the API.

![Message sequence selection dropdown](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/561309659_1339318247926826_482558811705806996_n.jpg?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=U1wB8sepZ7kQ7kNvwF2L5jr&_nc_oc=AdoOX-W3kRh8EEEZjHVATPtICBXsyj9uRc5qCAwVQD-taGW4sJ992k5RoJ49As09pj0&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=SJxzrHgvGPwo0zrqSux1-g&_nc_ss=7b20f&oh=00_Af7FPxCjRRiyNAMUSpBV0oSrBwhZqQ7R35c8Dm1hudMNhg&oe=6A1C023C)

1. Preview your message sequence and click **Save** .

![Message sequence preview with Save button](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/561695479_1339317887926862_4327881879631440625_n.jpg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=CYIQFRjaiFwQ7kNvwHhm5Ss&_nc_oc=AdqgZjluoxmncS4kglH4PuDrPUyB5Be_olxvTSMpeV4zclbXnKxfC3uzmRjhWo62uu4&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=SJxzrHgvGPwo0zrqSux1-g&_nc_ss=7b20f&oh=00_Af4GepOdramoveT_gAi1bg_96ZpLAooQqN9mwS8lSXsIAg&oe=6A1C1F4A)

## Error codes

| Code | Description | Possible Solutions |
| --- | --- | --- |
| `4027001`<br>Invalid input data | Some or all of the input data is not of the required format. | Check all the fields and parameters passed into the request are of the correct type and format, and that all required parameters are present. |
| `4027005`<br>Unable to create a welcome message sequence | An error occurred while trying to create a new welcome message sequence. | Check that the access token has all the required permissions for the WhatsApp business account. |
| `4027006`<br>Unable to update a welcome message sequence | Unable to update the welcome message sequence. | Check all fields and the sequence ID for correctness. Check that the access token has the necessary permissions for the WhatsApp business account. |
| `4027007`<br>API unavailable | The API being accessed is not available for use yet. | Wait a day or two for the API to become available and try again. |
| `4027010`<br>Missing parameter | One or more required parameters is missing. | Check all the documentation and ensure the required parameters are present. |
| `4027012`<br>Sequence used in an ad | The welcome message sequence is linked to an active ad and cannot be updated or deleted. | Disconnect the sequence from the ad and try again. |
| `4027017`<br>Could not load the sequence | Could not load the sequence being updated or deleted. | The welcome message sequence either does not exist, or you do not have permission to access it. Please check the access token and make sure you have the required permissions. |
