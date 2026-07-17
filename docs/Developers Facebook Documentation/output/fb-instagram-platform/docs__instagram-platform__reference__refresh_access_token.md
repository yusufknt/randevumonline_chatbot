# Refresh Access Token - Instagram Platform

_Source: https://developers.facebook.com/docs/instagram-platform/reference/refresh_access_token_

---

# Refresh Access Token

This endpoint allows you to refresh long-lived Instagram User Access Tokens.

## Creating

This operation is not supported.

## Reading

**`GET /refresh_access_token`**

Refresh a long-lived accesstoken that is at least 24 hours old but has not expired. Refreshed tokens are valid for 60 days from the date at which they are refreshed.

### Requirements

| Type | Requirement |
| --- | --- |
| Access tokens | Instagram User (long-lived) |
| Permissions | `instagram_business_basic` |

### Request Syntax

```
GET https://graph.instagram.com/refresh_access_token
  ?grant_type=ig_refresh_token
  &access_token=<LONG_LIVED_ACCESS_TOKENS>
```

### Query String Parameters

Include the following query string parameters to augment the request.

| Key | Value |
| --- | --- |
| `grant_type`  **Required**  *String* | Set this to `ig_refresh_token`. |
| `access_token`  **Required**  *String* | The valid (unexpired) long-lived Instagram User Access Token that you want to refresh. |

### Response

A JSON-formatted object containing the following properties and values.

```
{
  "access_token": "<ACCESS_TOKEN>",
  "token_type": "<TOKEN_TYPE>",
  "expires_in": <EXPIRES_IN>
}
```

**Response Contents**

| Value Placeholder | Value |
| --- | --- |
| `<ACCESS_TOKEN>`  *Numeric string* | A long-lived Instagram User Access Token. |
| `<TOKEN_TYPE>`  *String* | `bearer` |
| `<EXPIRES_IN>`  *Integer* | The number of seconds until the long-lived token expires. |

### cURL Example

#### Request

```
curl -X GET \
  'https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token=F4RVB...'
```

#### Response

```
{
  "access_token": "c3oxd...",
  "token_type": "bearer",
  "expires_in": 5183944
}
```

## Updating

This operation is not supported.

## Deleting

This operation is not supported.
