# Block users | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/block-users_

---

# Block users

Updated: Apr 21, 2026

You can block and unblock WhatsApp users and retrieve a list of blocked users using the [Block Users API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/block-api).

## Before you start

When you block a WhatsApp user:

- The user cannot contact your business or see that you are online.
- Your business cannot message the user. Attempts to message a blocked user return an error.

Errors are returned per-number, since blocks might succeed on some numbers and fail on others. The Block Users API is synchronous.

## Limitations

- You can only block users that have messaged your business in the last 24 hours.
- You cannot block another WhatsApp Business account.
- Each request can include a maximum of 1,000 users.
- The blocklist has a 64,000 user limit.

## Block a user

Use the [Block Users API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/block-api#post-version-phone-number-id-block-users) to [block a list of WhatsApp users](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/block-api#post-version-phone-number-id-block-users).

### Request syntax

```html
curl 'https://graph.facebook.com/<API_VERSION>/<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>/block_users' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <ACCESS_TOKEN>' \
-d '
{
  "messaging_product": "whatsapp",
  "block_users": [
    {
      "user": "<WHATSAPP_USER_PHONE_NUMBER>"
    }
  ]
}'
```

### Request parameters

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<ACCESS_TOKEN>`<br>*String* | **Required.**<br>[System token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens) or [business token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens). | `EAAA...` |
| `<API_VERSION>`<br>*String* | **Optional.**<br>Graph API version. | v25.0 |
| `<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>`<br>*String* | **Required.**<br>WhatsApp business phone number ID. | `106540352242922` |
| `<WHATSAPP_USER_PHONE_NUMBER>`<br>*String* | **Required.**<br>WhatsApp user phone number. This is the same value returned by the API as the `input` value when sending a message to a WhatsApp user. Note that a WhatsApp user’s phone number and ID may not always match. | `+16505551234` |

### Response syntax

```json
{
  "messaging_product": "whatsapp",
  "block_users": {
    "added_users": [
      {
        "input": "<WHATSAPP_USER_PHONE_NUMBER>",
        "wa_id": "<WHATSAPP_USER_ID>"
      }
    ],
    "failed_users": [
      {
        "input": "<WHATSAPP_USER_PHONE_NUMBER>",
        "wa_id": "<WHATSAPP_USER_ID>",
        "errors": [
          {
            "message": "<MESSAGE>",
            "code": "<CODE>",
            "error_data": {
              "details": "<DETAILS>"
            }
          }
        ]
      }
    ]
  }
}
```

### Response parameters

| Field | Description | Example Value |
| --- | --- | --- |
| `<CODE>`<br>*Integer* | Error code. See [Error codes](https://developers.facebook.com/documentation/business-messaging/whatsapp/block-users#error-codes) below. Only present in `failed_users`. | `131047` |
| `<DETAILS>`<br>*String* | Additional detail about the error. Only present in `failed_users`. | `User has not messaged in the last 24 hours` |
| `<MESSAGE>`<br>*String* | Error message describing why the block failed. Only present in `failed_users`. | `Re-engagement required` |
| `<WHATSAPP_USER_ID>`<br>*String* | WhatsApp user ID. Note that a WhatsApp user’s ID and phone number may not always match.<br>Returned as `wa_id`. May not be present in `failed_users` if the number is invalid. | `16505551234` |
| `<WHATSAPP_USER_PHONE_NUMBER>`<br>*String* | WhatsApp user phone number. This is the same value returned by the API as the `input` value when sending a message to a WhatsApp user. Note that a WhatsApp user’s phone number and ID may not always match.<br>Returned as `input` in both `added_users` and `failed_users` arrays. | `+16505551234` |

### Example request

This example blocks two WhatsApp users.

```curl
curl 'https://graph.facebook.com/v25.0/106540352242922/block_users' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "messaging_product": "whatsapp",
  "block_users": [
    {
      "user": "+16505551234"
    },
    {
      "user": "+14155559876"
    }
  ]
}'
```

### Example response

Successful response when all users are blocked:

```json
{
  "messaging_product": "whatsapp",
  "block_users": {
    "added_users": [
      {
        "input": "+16505551234",
        "wa_id": "16505551234"
      },
      {
        "input": "+14155559876",
        "wa_id": "14155559876"
      }
    ]
  }
}
```

Mixed success/failure response when some users cannot be blocked:

```json
{
  "messaging_product": "whatsapp",
  "block_users": {
    "added_users": [
      {
        "input": "+16505551234",
        "wa_id": "16505551234"
      }
    ],
    "failed_users": [
      {
        "input": "+14155559876",
        "wa_id": "14155559876",
        "errors": [
          {
            "message": "Re-engagement required",
            "code": 131047,
            "error_data": {
              "details": "User has not messaged in the last 24 hours"
            }
          }
        ]
      }
    ]
  },
  "error": {
    "message": "(#139100) Failed to block/unblock users",
    "type": "OAuthException",
    "code": 139100,
    "error_data": {
      "details": "Failed to block some users, see the block_users response list for details"
    },
    "fbtrace_id": "<FBTRACE_ID>"
  }
}
```

## Unblock a user

Use the [Block Users API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/block-api#delete-version-phone-number-id-block-users) to [unblock a list of WhatsApp users](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/block-api#delete-version-phone-number-id-block-users).

### Request syntax

```html
curl -X DELETE 'https://graph.facebook.com/<API_VERSION>/<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>/block_users' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <ACCESS_TOKEN>' \
-d '
{
  "messaging_product": "whatsapp",
  "block_users": [
    {
      "user": "<WHATSAPP_USER_PHONE_NUMBER>"
    }
  ]
}'
```

### Request parameters

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<ACCESS_TOKEN>`<br>*String* | **Required.**<br>[System token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens) or [business token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens). | `EAAA...` |
| `<API_VERSION>`<br>*String* | **Optional.**<br>Graph API version. | v25.0 |
| `<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>`<br>*String* | **Required.**<br>WhatsApp business phone number ID. | `106540352242922` |
| `<WHATSAPP_USER_PHONE_NUMBER>`<br>*String* | **Required.**<br>WhatsApp user phone number. This is the same value returned by the API as the `input` value when sending a message to a WhatsApp user. Note that a WhatsApp user’s phone number and ID may not always match. | `+16505551234` |

### Response syntax

```json
{
  "messaging_product": "whatsapp",
  "block_users": {
    "removed_users": [
      {
        "input": "<WHATSAPP_USER_PHONE_NUMBER>",
        "wa_id": "<WHATSAPP_USER_ID>"
      }
    ],
    "failed_users": [
      {
        "input": "<WHATSAPP_USER_PHONE_NUMBER>",
        "wa_id": "<WHATSAPP_USER_ID>",
        "errors": [
          {
            "message": "<MESSAGE>",
            "code": "<CODE>",
            "error_data": {
              "details": "<DETAILS>"
            }
          }
        ]
      }
    ]
  }
}
```

### Response parameters

| Field | Description | Example Value |
| --- | --- | --- |
| `<WHATSAPP_USER_PHONE_NUMBER>`<br>*String* | WhatsApp user phone number. This is the same value returned by the API as the `input` value when sending a message to a WhatsApp user. Note that a WhatsApp user’s phone number and ID may not always match.<br>Returned as `input` in both `removed_users` and `failed_users` arrays. | `+16505551234` |
| `<WHATSAPP_USER_ID>`<br>*String* | WhatsApp user ID. Note that a WhatsApp user’s ID and phone number may not always match.<br>Returned as `wa_id`. May not be present in `failed_users` if the number is invalid. | `16505551234` |
| `<MESSAGE>`<br>*String* | Error message describing why the unblock failed. Only present in `failed_users`. | `Re-engagement required` |
| `<CODE>`<br>*Integer* | Error code. See [Error codes](https://developers.facebook.com/documentation/business-messaging/whatsapp/block-users#error-codes) below. Only present in `failed_users`. | `131047` |
| `<DETAILS>`<br>*String* | Additional detail about the error. Only present in `failed_users`. | `User has not messaged in the last 24 hours` |

### Example request

This example unblocks two previously blocked WhatsApp users.

```curl
curl -X DELETE 'https://graph.facebook.com/v25.0/106540352242922/block_users' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "messaging_product": "whatsapp",
  "block_users": [
    {
      "user": "+16505551234"
    },
    {
      "user": "+14155559876"
    }
  ]
}'
```

### Example response

Successful response when all users are unblocked:

```json
{
  "messaging_product": "whatsapp",
  "block_users": {
    "removed_users": [
      {
        "input": "+16505551234",
        "wa_id": "16505551234"
      },
      {
        "input": "+14155559876",
        "wa_id": "14155559876"
      }
    ]
  }
}
```

Mixed success/failure response when some users cannot be unblocked:

```json
{
  "messaging_product": "whatsapp",
  "block_users": {
    "removed_users": [
      {
        "input": "+16505551234",
        "wa_id": "16505551234"
      }
    ],
    "failed_users": [
      {
        "input": "+14155559876",
        "wa_id": "14155559876",
        "errors": [
          {
            "message": "Re-engagement required",
            "code": 131047,
            "error_data": {
              "details": "User has not messaged in the last 24 hours"
            }
          }
        ]
      }
    ]
  },
  "error": {
    "message": "(#139100) Failed to block/unblock users",
    "type": "OAuthException",
    "code": 139100,
    "error_data": {
      "details": "Failed to unblock some users, see the block_users response list for details"
    },
    "fbtrace_id": "<FBTRACE_ID>"
  }
}
```

## Get blocked users

Use the [Block Users API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/block-api#get-version-phone-number-id-block-users) to [get a list of blocked users](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/block-api#get-version-phone-number-id-block-users) on your WhatsApp business phone number.

### Request syntax

```html
curl 'https://graph.facebook.com/<API_VERSION>/<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>/block_users?limit=<LIMIT>&after=<AFTER_CURSOR>&before=<BEFORE_CURSOR>' \
-H 'Authorization: Bearer <ACCESS_TOKEN>'
```

### Request parameters

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<ACCESS_TOKEN>`<br>*String* | **Required.**<br>[System token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens) or [business token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens). | `EAAA...` |
| `<API_VERSION>`<br>*String* | **Optional.**<br>Graph API version. | v25.0 |
| `<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>`<br>*String* | **Required.**<br>WhatsApp business phone number ID. | `106540352242922` |
| `<LIMIT>`<br>*Integer* | **Optional.**<br>Maximum number of blocked users to return per request. | `10` |
| `<AFTER_CURSOR>`<br>*String* | **Optional.**<br>Cursor for forward pagination. Learn more about [paginated results in Graph API](https://developers.facebook.com/docs/graph-api/results). | `eyJvZAmZAzZAXQ...` |
| `<BEFORE_CURSOR>`<br>*String* | **Optional.**<br>Cursor for backward pagination. Learn more about [paginated results in Graph API](https://developers.facebook.com/docs/graph-api/results). | `eyJvZAmZAzZAXQ...` |

### Response syntax

```json
{
  "data": [
    {
      "messaging_product": "whatsapp",
      "wa_id": "<WHATSAPP_USER_ID>"
    }
  ],
  "paging": {
    "cursors": {
      "after": "<AFTER_CURSOR>",
      "before": "<BEFORE_CURSOR>"
    }
  }
}
```

### Response parameters

| Field | Description | Example Value |
| --- | --- | --- |
| `<WHATSAPP_USER_ID>`<br>*String* | WhatsApp user ID. Note that a WhatsApp user’s ID and phone number may not always match.<br>Returned as `wa_id` in each object in the `data` array. | `16505551234` |
| `<AFTER_CURSOR>`<br>*String* | Cursor for forward pagination. Learn more about [paginated results in Graph API](https://developers.facebook.com/docs/graph-api/results). | `eyJvZAmZAzZAXQ...` |
| `<BEFORE_CURSOR>`<br>*String* | Cursor for backward pagination. Learn more about [paginated results in Graph API](https://developers.facebook.com/docs/graph-api/results). | `eyJvZAmZAzZAXQ...` |

### Example request

This example retrieves up to 10 blocked users.

```curl
curl 'https://graph.facebook.com/v25.0/106540352242922/block_users?limit=10' \
-H 'Authorization: Bearer EAAJB...'
```

### Example response

```json
{
  "data": [
    {
      "messaging_product": "whatsapp",
      "wa_id": "16505551234"
    },
    {
      "messaging_product": "whatsapp",
      "wa_id": "14155559876"
    }
  ],
  "paging": {
    "cursors": {
      "after": "eyJvZAmZAzZAXQiOjAsInZAlcnNpb25JZACI6IjE3Mzc2Nzk2ODgzODM1ODQifQZDZD",
      "before": "eyJvZAmZAzZAXQiOjAsInZAlcnNpb25JZACI6IjE3Mzc2Nzk2ODgzODM1ODQifQZDZD"
    }
  }
}
```

## Error codes

| Code | Description |
| --- | --- |
| `139100`<br>Failed to block/unblock some users | Bulk blocking failed to block some or all of the users. |
| `139101`<br>Blocklist limit reached | The blocklist has reached its 64,000 user limit. |
| `139102`<br>Blocklist concurrent update | Occurs when the blocklist is updated while performing a pagination request and `version_id` does not match. |
| `139103`<br>Internal error | Internal error. Try the request again. |
| `130429`<br>Rate limit hit | Occurs when either too many numbers are in the request or too many requests are made over a short period of time. |
| `131021`<br>Self block | Cannot block your own phone number. |
| `131047`<br>Re-engagement required | The WhatsApp user has not messaged your business in the last 24 hours. This error also occurs if the number is an invalid WhatsApp user. |
