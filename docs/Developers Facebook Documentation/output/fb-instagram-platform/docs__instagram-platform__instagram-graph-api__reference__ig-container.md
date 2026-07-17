# IG Container - Instagram Platform

_Source: https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-container_

---

# Instagram (IG) Container

Represents a media container for publishing an Instagram media object.

### Requirements

|  | Instagram API with Instagram Login | Instagram API with Facebook Login |
| --- | --- | --- |
| **Access Tokens** | - Instagram User user access token | - [Facebook User access token](https://developers.facebook.com/docs/facebook-login/access-tokens/#usertokens) |
| **Host URL** | `graph.instagram.com` | `graph.facebook.com` |
| **Login Type** | Business Login for Instagram | Facebook Login for Business |
| [**Permissions**](https://developers.facebook.com/docs/permissions/reference#i) | - `instagram_business_basic` - `instagram_business_content_publish` | - `instagram_basic` - `instagram_content_publish` - `pages_read_engagement`   If the app user was granted a role via the Business Manager on the [Page](https://developers.facebook.com/docs/instagram-api/overview#pages) connected to the targeted IG User, you will also need one of:   - `ads_management` - `ads_read` |

## Creating

This operation is not supported.

## Reading

**`GET <HOST_URL>/<IG_CONTAINER_ID>`**

Get [fields](#fields) and [edges](#edges) on an IG Container.

### Request Syntax

```
GET <HOST_URL>/<API_VERSION>/<IG_CONTAINER_ID>
  ?fields=<LIST_OF_FIELDS>
  &access_token=<ACCESS_TOKEN>
```

### Query String Parameters

| Parameter | Value |
| --- | --- |
| `access_token`  **Required**  *String* | The app user's [User](https://developers.facebook.com/docs/facebook-login/access-tokens/#usertokens) access token. |
| `fields`  *Comma-separated list* | A comma-separated list of [fields](#fields) and [edges](#edges) you want returned. If omitted, default fields will be returned. |

### Fields

| Field Name | Description |
| --- | --- |
| `copyright_check_status` | Used to determine if an uploaded video is violating copyright. Key-values pairs return include:   - `matches_found` set to one of the following:   - `true` – the video is violating copyright   - `false` – the video is not violating copyright - `status` set to one of the following:   - `completed` – the detection process has finished   - `error` – an error occurred during the detection process   - `in_progress` – the detection process is ongoing   - `not_started` – the detection process has not started |
| `id` | Instagram Container ID, represented in code examples as `<IG_CONTAINER_ID>` |
| `status` | Publishing status. If `status_code` is `ERROR`, this value will be an [error subcode](https://developers.facebook.com/docs/instagram-api/reference/error-codes). |
| `status_code` | The container's publishing status. Possible values:    - `EXPIRED` — The container was not published within 24 hours and has expired. - `ERROR` — The container failed to complete the publishing process. - `FINISHED` — The container and its media object are ready to be published. - `IN_PROGRESS` — The container is still in the publishing process. - `PUBLISHED` — The container's media object has been published. |

### Edges

There are no edges on this node.

### Response

A JSON-formatted object containing default and requested [fields](#fields).

```
{
  "<FIELD>":"<VALUE>",
  ...
}
```

### Example Request

```
curl -X GET \
  'https://graph.instagram.com/17889615691921648?fields=status_code&access_token=IGQVJ...'
```

### Sample Response

```
{
  "status_code": "FINISHED",
  "id": "17889615691921648"
}
```

## Updating

This operation is not supported.

## Deleting

This operation is not supported.
