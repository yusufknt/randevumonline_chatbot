# Messenger Profile API | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/messenger-profile-api_

---

# Messenger Profile API

Updated: Mar 18, 2026

The Messenger Profile for your Page is where you set properties that define various aspects of the following Messenger Platform features. For more information, see the [Messenger Profile Properties](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/messenger-profile-api#profile_properties) table below.

- [Get Started Button](https://developers.facebook.com/documentation/business-messaging/messenger-platform/discovery/welcome-screen)
- [Welcome Page](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/messenger-profile-api/greeting)
- [Ice Breakers](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/messenger-profile-api/ice-breakers)
- [Persistent Menu](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/messenger-profile-api/persistent-menu)
- [Domain allowlist](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/messenger-profile-api/domain-whitelisting)
- [Account Linking](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/messenger-profile-api/account-linking-url)
- [Commands](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/messenger-profile-api/commands)

The Messenger Profile API allows you to set, update, retrieve, and delete properties from the Page Messenger Profile.

## Permissions

A page access token with `pages_messaging` permission is required to interact with this endpoint.

Apps in Development Mode, the Messenger Profile settings will only be visible to people with role on the app.

## Request URI

```
https://graph.facebook.com/v25.0/me/messenger_profile?access_token=<PAGE_ACCESS_TOKEN>
```

## Messenger Profile Properties

The following properties may be included in the Messenger profile for your Page. See descriptions in the table below for the type and purpose of each property.

| Property | Type | Description |
| --- | --- | --- |
| `get_started` | Object | The payload that will be sent as a `messaging_postbacks` event when someone taps the ‘get started’ button on your Page Messenger welcome screen.<br><br>For more, see [Get Started Button Reference](https://developers.facebook.com/documentation/business-messaging/messenger-platform/discovery/welcome-screen). |
| `greeting` | Array<Object> | An array of locale-specific greeting messages to display on your Page Messenger welcome screen.<br><br>For more, see [Greeting Text Reference](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/messenger-profile-api/greeting). |
| `ice_breakers` | Array<Object> | An array with an ice breaker object.<br><br>For more, see [Ice Breakers Reference](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/messenger-profile-api/ice-breakers). |
| `persistent_menu` | Array<Object> | An array of call-to-action buttons to include in the persistent menu.<br><br>For more, see [Persistent Menu Reference](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/messenger-profile-api/persistent-menu). |
| `whitelisted_domains` | Array<String> | A list of allowlisted domains. Required for Pages that use the [Messenger Extensions SDK](https://developers.facebook.com/documentation/business-messaging/messenger-platform/webview/extensions) and the [checkbox plugin](https://developers.facebook.com/documentation/business-messaging/messenger-platform/discovery).<br><br>For more, see [Domain Allowlist Reference](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/messenger-profile-api/domain-whitelisting). |
| `account_linking_url` | String | Authentication callback URL. Must use https protocol.<br><br>For more, see [Account Linking URL Reference](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/messenger-profile-api/account-linking-url). |
| `commands` | Array<Object> | Optional argument. If provided, it cannot be null.<br><br>For more, see [Commands Reference](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/messenger-profile-api/commands). |
| `subject_to_new_eu_privacy_rules` | Boolean | A boolean flag that determines whether the page is impacted by the [Messenger API Updates for Europe](https://developers.facebook.com/documentation/business-messaging/messenger-platform/europe-japan-updates). This property is only available for `GET` request. |

## Retrieve Properties

Retrieves the current value of one or more [Messenger Profile properties](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/messenger-profile-api#profile_properties) by name.

### Request Parameters

The following parameters are included in the query string of the request:

| Parameter | Description |
| --- | --- |
| fields | A comma-separated list of [Messenger Profile properties](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/messenger-profile-api#profile_properties) to retrieve. |

### Example Request

```
curl -X GET "https://graph.facebook.com/v25.0/me/messenger_profile?fields=whitelisted_domains,greeting&access_token=<PAGE_ACCESS_TOKEN>"
```

### Example Response

The current value of the requested properties will be returned in the `data` array:

```curl
{
   "data": [
        {
          "whitelisted_domains": [
            "https://facebook.com/"
          ],
          "greeting": [
            {
               "locale": "default",
               "text": "Hello!"
            },
            {
               "locale": "en_US",
               "text": "Timeless apparel for the masses."
            }
         ]
      }
   ]
}
```

## Set/Update Properties

Sets the values of one or more [Messenger Profile properties](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/messenger-profile-api#profile_properties). Only properties set in the request body will be overwritten.

### Example Request

```curl
curl -X POST -H "Content-Type: application/json" -d '{
  "<PROPERTY_NAME>": "<NEW_PROPERTY_VALUE>",
  "<PROPERTY_NAME>": "<NEW_PROPERTY_VALUE>",
  ...
}' "https://graph.facebook.com/v25.0/me/messenger_profile?access_token=<PAGE_ACCESS_TOKEN>"
```

### Example Response

```json
{
    "result": "success"
}
```

## Delete Properties

Deletes one or more [Messenger Profile properties](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/messenger-profile-api#profile_properties). Only properties specified in the `fields` array will be deleted.

### Example Request

```
curl -X DELETE -H "Content-Type: application/json" -d '{
  "fields": [
    "<PROPERTY_NAME>",
    "<PROPERTY_NAME>",
    "<PROPERTY_NAME>",
    ...
  ]
}' "https://graph.facebook.com/v25.0/me/messenger_profile?access_token=<PAGE_ACCESS_TOKEN>"
```

### Example Response

```json
{
    "result": "success"
}
```

## Rate Limit

Calls to the Messenger Profile API are limited to 10 API calls per 10 minute interval. This rate limit is enforced per Page.
