# Upcoming Events - Instagram Platform

_Source: https://developers.facebook.com/docs/instagram-platform/instagram-api-with-facebook-login/upcoming-events_

---

# Instagram Upcoming Events

This document explains how to manage Instagram events using the Instagram API with Facebook Login, covering creation, modification and retrieval of existing events.

In this document we use "Instagram User" and "Instagram Account" interchangeable; both represent your app user's Instagram professional account.

## Before You Start

You'll need the following:

- The `instagram_basic` permission
- The `instagram_manage_upcoming_events` permission
- The ID of the app user's Instagram professional account linked to a Business

### Limitations

- Only supports Instagram Professional accounts linked to a Business
- Currently only supports retrieval of events created via Ads Manager or this API
- Intended to facilitate the creation of reminder ads

## Create a New Event

To create a new event, send a `POST` request to the `/<IG_USER_ID>/upcoming_events` endpoint, where `<IG_USER_ID>` is the ID for your app user's Instagram professional account, including the following parameters:

- `title`
- `start_time`
- `notification_subtypes` (optional)
- `end_time` (optional)
- `notification_target_time` (optional)

### Request

*Formatted for readability. Make sure to replace placeholders with your own values.*

```
curl -X POST "https://graph.facebook.com/v25.0/<IG_USER_ID>/upcoming_events" \
  -F 'title="Season Premiere"' \
  -F 'start_time="2024-06-30T19:00:00+0000"' \
  -F 'notification_subtypes=["BEFORE_EVENT_1DAY", "BEFORE_EVENT_15MIN", "EVENT_START"]' \
  -F 'access_token=<ACCESS_TOKEN>'
```

On success, your app receives a JSON response containing the new event's ID.

```
{
  "id": "<EVENT_ID>"
}
```

### Parameters

| Name | Description |
| --- | --- |
| `end_time`  ISO string | Optional. The event's end time.  **Note:** Must not be set when setting `notification_target_time` to `"EVENT_END"`. |
| `notification_target_time`  string | Optional. A string value specifying the part of the event relative to which notifications will be sent. Supported values are `"EVENT_START"` or `"EVENT_END"`.  If not set in the request, defaults to `"EVENT_START"`. When set to `"EVENT_END"`, the `notification_subtypes` field must include the following three values in any order: `[“BEFORE_EVENT_2DAY”, “BEFORE_EVENT_1DAY”, “BEFORE_EVENT_1HOUR”]`.  Additionally, when set to `"EVENT_END"`, the event `end_date` must not be specified. |
| `notification_subtypes`  array of strings | Optional. A comma-separated list of three values that describe when notifications will be sent to event subscribers relative to the event’s `start_time`. If not set in the request, defaults to `"BEFORE_EVENT_1DAY"`, `"BEFORE_EVENT_15MIN"`, and `"EVENT_START"`.  If set without specifying `notification_target_time` or with `notification_target_time` set to `"EVENT_START"`, `"EVENT_START"` and `"BEFORE_EVENT_1DAY"` are required with one additional value. Possible additional values include:   |  |  | | --- | --- | | - `"AFTER_EVENT_1DAY"` - `"AFTER_EVENT_2DAY"` - `"AFTER_EVENT_3DAY"` - `"AFTER_EVENT_4DAY"` | - `"AFTER_EVENT_5DAY"` - `"AFTER_EVENT_6DAY"` - `"AFTER_EVENT_7DAY"` - `"BEFORE_EVENT_15MIN"` |   Order does not matter.  If `notification_target_time` is set to `"EVENT_END"`, the specified values here must be: `[“BEFORE_EVENT_2DAY”, “BEFORE_EVENT_1DAY”, “BEFORE_EVENT_1HOUR”]` |
| `start_time`  ISO string | **Required.** The event's start time. |
| `title`  string | **Required.** The event's title. |

## Retrieve an event

To retrieve details of an existing event, send a `GET` request to the `/<EVENT_ID>` endpoint.

### Request

*Formatted for readability. Make sure to replace placeholders with your own values.*

```
curl -X GET "https://graph.facebook.com/v25.0/<EVENT_ID>?access_token=<ACCESS_TOKEN>"
```

On success, your app receives a JSON response containing the ID, title , and start time for the event.

```
{
  "id": "<EVENT_ID>"
  "title":"Updated Season Premier",
  "start_time":"2024-05-11T16:00:00+0000"
}
```

## Update an Existing Event

To update the details of an existing event, send a `POST` request to the `/<EVENT_ID>` and include one or more of the following parameters that you want to update:

- `title`
- `start_time`
- `notification_subtypes` (optional)
- `end_time` (optional)

### Example Request

*Formatted for readability. Make sure to replace placeholders with your own values.*

```
curl -X POST "https://graph.facebook.com/v25.0/<EVENT_ID>" \
     -F 'title="Season Premiere"' \
     -F 'start_time="2024-06-30T19:00:00+0000"' \
     -F 'notification_subtypes=["BEFORE_EVENT_1DAY", "BEFORE_EVENT_15MIN", "EVENT_START"]' \
     -F 'access_token=<ACCESS_TOKEN>'
```

On success, your app receives a JSON response containing the ID for the event.

```
{
  "id": "<EVENT_ID>"
}
```

## Retrieve all Upcoming Events

To retrieve a list of all upcoming events, send a `GET` request to the `/<IG_USER_ID>/upcoming_events`.

### Request

*Formatted for readability. Make sure to replace placeholders with your own values.*

```
curl -X GET "https://graph.facebook.com/v25.0/<IG_USER_ID>/upcoming_events?access_token=<ACCESS_TOKEN>"
```

On success, your app receives a JSON response containing a list of all upcoming events with the ID, title, and start time for each.

```
{
  "data": [
    {
      "id": "<EVENT_ID_1>,"
      "title":"<EVENT_TITLE_1>",
      "start_time":"2024-04-11T16:00:00+0000"
    },
    {
      "id": "<EVENT_ID_2>,"
      "title":"<EVENT_TITLE_2>",
      "start_time":"2024-04-18T16:00:00+0000"
    },
    {
      "id": "<EVENT_ID_3>,"
      "title":"<EVENT_TITLE_3>",
      "start_time":"2024-04-25T16:00:00+0000"
    },
  ]
}
```

## Next Steps

- Learn how to create
  [Instagram Reminder Ads
  ![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/310307727_3347317042262105_1088877051262827250_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=5SvUa0KxdZkQ7kNvwHcqah0&_nc_oc=AdpNPlkM5xCl8ncqAEi0DvJzLsMMV09WvXL6Z1STXmvsbKMnBfs-2mixKR1O9x9_AAg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=FvvqIvVoO9lsllcrSZ_ZKg&_nc_ss=7b289&oh=00_Af4njIInYj0CqoJhHEq0hJsBdhvwwFJoPbigvw4kvhV55w&oe=6A1BE7E2)](https://developers.facebook.com/docs/instagram/marketing-api/guides/reminder-ads)
  using Meta's Marketing API.
