# ice_breakers Reference | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/messenger-profile-api/ice-breakers_

---

# ice_breakers Reference

Updated: Jun 26, 2024

Ice Breakers provide a way for users to start a conversation with a business with a list of frequently asked questions. A maximum of 4 questions can be set via the Ice Breaker API.

Starting April 19th, 2022, Ice Breakers supports localization allowing businesses to set custom questions based on the user locale. The API will have a new format and we encourage developers to leverage the new format to set and retrieve Ice Breakers information. The list of supported locales can be found [here](https://developers.facebook.com/documentation/business-messaging/messenger-platform/messenger-profile/supported-locales).

## Page Profile Priority

Some profile elements, like Ice Breakers and the Get Started button, are incompatible with each other. When both are set, one will take precedence over the other. This is the order of precendence for the profile elements:

1. [API Ice Breakers](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/messenger-profile-api/ice-breakers)
2. [Get Started button](https://developers.facebook.com/documentation/business-messaging/messenger-platform/discovery/welcome-screen)
3. Custom Questions set via the Page Inbox UI Editing Custom Questions from the Page Inbox UI is disabled when Ice Breakers are set via API. This is to prevent breaking the experience set by the installed app.

## POST request

To set an Ice Breaker configuration, there are two formats for the POST request, existing and new.

One POST request can have the existing format **OR** the new format but not both.

### New format (recommended)

```
curl -X POST -H "Content-Type: application/json" -d '{

     "ice_breakers":[
       {
          "call_to_actions":[
             {
                "question":"<QUESTION>",
                "payload":"<PAYLOAD>"
             },
             {
                "question":"<QUESTION>",
                "payload":"<PAYLOAD>"
             }
          ],
          "locale":"default" // default locale is REQUIRED
       },
       {
          "call_to_actions":[
             {
                "question":"<QUESTION>",
                "payload":"<PAYLOAD>"
             },
             {
                "question":"<QUESTION>",
                "payload":"<PAYLOAD>"
             }
          ],
          "locale":"en_GB"
       }
    ]
}' "https://graph.facebook.com/v25.0/me/messenger_profile?access_token=<PAGE_ACCESS_TOKEN>"
```

### Existing format

```
curl -X POST -H "Content-Type: application/json" -d '{

  "ice_breakers":[
     {
        "question": "<QUESTION>",
        "payload": "<PAYLOAD>"
     },
     {
        "question": "<QUESTION>",
        "payload": "<PAYLOAD>"
     },
     ...

  ]
}' "https://graph.facebook.com/v25.0/me/messenger_profile?access_token=<PAGE_ACCESS_TOKEN>"
```

## GET request

Depending on how the Ice Breaker is setup, GET request will return a different format:

- If the Ice Breaker is setup using the existing format, GET request will return the existing format response.
- If the Ice Breaker is setup using the new format, GET request will return the new format response.

Developers should migrate to the new format as we will be deprecating the old format.

```
curl -X GET "https://graph.facebook.com/v25.0/me/messenger_profile?fields=ice_breakers&access_token=<PAGE_ACCESS_TOKEN>"
```

### New Format Response

```curl
{
   "data": [
        {
          "call_to_actions" : [
               {
                "question": "<QUESTION>",
                "payload": "<PAYLOAD>",

               },
               {
                "question": "<QUESTION>",
                "payload": "<PAYLOAD>",

               },
          ],
          "locale": "<LOCALE>",
      },
      {
          "call_to_actions" : [
               {
                "question": "<QUESTION>",
                "payload": "<PAYLOAD>",

               },
               {
                "question": "<QUESTION>",
                "payload": "<PAYLOAD>",

               },
          ],
          "locale": "<LOCALE>",
        ...
      }
   ]
}
```

### Existing Format Response

```
{
   "data": [
        {
          "ice_breakers": [
            {
                "question": "<QUESTION>",
                "payload": "<PAYLOAD>"
            },
            {
                "question": "<QUESTION>",
                "payload": "<PAYLOAD>"
            },
            ...
        ]
      }
   ]
}
```

## DELETE Request

This will delete ALL the ice breakers. Deletion of locale specific Ice Breakers will be enabled in the future.

```
curl -X DELETE -H "Content-Type: application/json" -d '{
  "fields": [
    "ice_breakers",
  ]
}' "https://graph.facebook.com/v25.0/me/messenger_profile?access_token=<PAGE_ACCESS_TOKEN>"
```

Response

```
{
   "success": "true"
}
```

## Properties

| Property | Type | Description |
| --- | --- | --- |
| `question` | String | Text that will be posted on the thread as the user asking the question. |
| `payload` | String | Payload the will be returned as a [postback webhook event](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/webhook-events/messaging_postbacks) |

## Example API Call

API POST call to set up Ice Breakers in the New format

```
curl -X POST -H "Content-Type: application/json" -d '{
"ice_breakers":[
       {
          "call_to_actions":[
             {
                "question":"Where are you located?",
                "payload":"LOCATION_POSTBACK_PAYLOAD"
             },
             {
                "question":"What are your hours?",
                "payload":"HOURS_POSTBACK_PAYLOAD"
             }
          ],
          "locale":"default"
       },
       {
          "call_to_actions":[
             {
                "question":"What are your hours?",
                "payload": "HOURS_POSTBACK_PAYLOAD"
             },
             {
                "question":"Can you tell me more about your business?",
                "payload": "MORE_POSTBACK_PAYLOAD"
             },
             {
                "question":"What services do you offer?",
                "payload": "SERVICES_POSTBACK_PAYLOAD"
             }

          ],
          "locale":"en_GB"
       }
    ]
}' "https://graph.facebook.com/v25.0/me/messenger_profile?access_token=<PAGE_ACCESS_TOKEN>"
```

## Rate Limit

Calls to the Messenger Profile API are limited to 10 API calls per 10 minute interval. This rate limit is enforced per Page.
