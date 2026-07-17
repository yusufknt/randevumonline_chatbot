# Template groups | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-groups_

---

# Template groups

Updated: Feb 27, 2026

This document describes how to create, manage, and measure template groups.

Template groups allow you to associate a set of templates so it’s easier to track their performance as a set when querying template metrics.

## Limitations

- a template can only be a part of a single template group at a time
- template group names must be unique
- removing a template from a template group does not remove any template metrics it may have contributed to the group

## Create a template group

Use the [Template Groups API](https://developers.facebook.com/docs/graph-api/reference/whats-app-business-account/template_groups#Creating) to create a template group.

### Request

```html
curl 'https://graph.facebook.com/<API_VERSION>/<WABA_ID>/template_groups' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <ACCESS_TOKEN>' \
-d '
{
  "name": "<TEMPLATE_GROUP_NAME>",
  "description": "<TEMPLATE_GROUP_DESCRIPTION>",
  "whatsapp_business_templates": [
    <TEMPLATE_IDS>
  ]
}'
```

### Request parameters

| Placeholder | Description | Example value |
| --- | --- | --- |
| `<API_VERSION>`<br>*String* | **Optional.**<br>Graph API version. | v25.0 |
| `<WABA_ID>`*String* | **Required.**<br>WhatsApp Business Account ID. | `102290129340398` |
| `<ACCESS_TOKEN>`<br>*String* | **Required.**<br>[System token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens) or [business token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens). | `EAAA...` |
| `<TEMPLATE_GROUP_NAME>`*String* | **Required.**<br>Template group name. Must be unique.<br>Maximum 256 characters. | `Black Friday 2024` |
| `<TEMPLATE_GROUP_DESCRIPTION>`*String* | **Optional.**<br>Template group description.<br>Maximum 512 characters. | `US-based Black Friday sale 2024 templates.` |
| `<TEMPLATE_IDS>`*Array of integers* | **Required.**<br>Array of template IDs to add to the group. | `278077987957091,1945418102598215,1035843174854974` |

### Response

Upon success:

```html
{
  "id": "<TEMPLATE_GROUP_ID>"
}
```

### Response parameters

| Placeholder | Description | Example value |
| --- | --- | --- |
| `<TEMPLATE_GROUP_ID>` | Template group ID. | `9020555671393375` |

### Example request

```curl
curl 'https://graph.facebook.com/v25.0/102290129340398/template_groups' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "name": "Black Friday 2024",
  "description": "US-based Black Friday sale 2024 templates.",
  "whatsapp_business_templates": [278077987957091,1945418102598215,1035843174854974]
}'
```

### Example response

```json
{
  "id": "9020555671393375"
}
```

## Get a template group

Use the [Template Group API](https://developers.facebook.com/docs/graph-api/reference/business-messaging-template-group#Reading) to get data on a template group, as well as template data for each template within the group.

### Request

```html
curl 'https://graph.facebook.com/<API_VERSION>/<TEMPLATE_GROUP_ID>' \
-H 'Authorization: Bearer <ACCESS_TOKEN>'
```

### Request parameters

| Placeholder | Description | Example value |
| --- | --- | --- |
| `<ACCESS_TOKEN>`<br>*String* | **Required.**<br>[System token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens) or [business token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens). | `EAAA...` |
| `<API_VERSION>`<br>*String* | **Optional.**<br>Graph API version. | v25.0 |
| `<TEMPLATE_GROUP_ID>`<br>String | **Required.**<br>Template group ID. | `9020555671393375` |

### Response

Upon success:

```html
{
  "name": "<TEMPLATE_GROUP_NAME>",
  "description": "<TEMPLATE_GROUP_DESCRIPTION>",
  "creation_time": "<TEMPLATE_GROUP_CREATION_TIMESTAMP>",
  "update_time": "<TEMPLATE_GROUP_LAST_UPDATE_TIMESTAMP>",
  "whatsapp_business_account": {
    <WABA_DETAILS>
  },
  "whatsapp_business_templates": {
    "data": [
      <TEMPLATE_DETAILS>
    ],
    "paging": {
      <PAGING_CURSORS>
    }
  },
  "id": "<TEMPLATE_GROUP_ID>"
}
```

### Response parameters

| Placeholder | Description | Example value |
| --- | --- | --- |
| `<TEMPLATE_GROUP_NAME>` | Template group name. | `Black Friday 2024` |
| `<TEMPLATE_GROUP_DESCRIPTION>` | Template group description. | `US-based Black Friday sale 2024 templates.` |
| `<TEMPLATE_GROUP_CREATION_TIMESTAMP>` | ISO 8601 timestamp indicating when the template group was created. | `2025-01-06T23:05:12+0000` |
| `<TEMPLATE_GROUP_LAST_UPDATE_TIMESTAMP>` | ISO 8601 timestamp indicating when the template group was last updated. | `2025-01-06T23:05:12+0000` |
| `<WABA_DETAILS>` | Object describing the WhatsApp Business Account that owns the template group. | See [example response](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-groups#example-response-2) below. |
| `<TEMPLATE_DETAILS>` | Array of objects. Each object describes a template, and its components, within the template group. | See [example response](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-groups#example-response-2) below. |
| `<PAGING_CURSORS>` | An object with before-and-after [paging cursors](https://developers.facebook.com/docs/graph-api/results) that can be used to get the next (after) or previous (before) set of objects in the result set. | See [example response](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-groups#example-response-2) below. |
| `<TEMPLATE_GROUP_ID>` | Template group ID. | `9020555671393375` |

### Example request

```curl
curl 'https://graph.facebook.com/v25.0/9020555671393375' \
-H 'Authorization: Bearer EAAJB...'
```

### Example response

Response results are truncated with ellipses (...) in the example below for brevity.

```json
{
  "name": "Black Friday 2024",
  "description": "US-based Black Friday sale 2024 templates.",
  "creation_time": "2025-01-06T23:05:12+0000",
  "update_time": "2025-01-06T23:05:12+0000",
  "whatsapp_business_account": {
    "id": "102290129340398",
    "name": "Lucky Shrub",
    "currency": "USD",
    "timezone_id": "1",
    "message_template_namespace": "ba30dd89_2ebd_41e4_b805_f2c05ae04cc9"
  },
  "whatsapp_business_templates": {
    "data": [
      {
        "name": "black_friday_2024_carousel_media_header_cards",
        "parameter_format": "POSITIONAL",
        "components": [
          {
            "type": "BODY",
            "text": "Rare black succulents for sale! {{1}}, add...",
            "example": {
              "body_text": [
                [
                  "Pablo"
                ]
              ]
            }
          },
          {
            "type": "CAROUSEL",
            "cards": [
              {
                "components": [
                  {
                    "type": "HEADER",
                    "format": "IMAGE",
                    "example": {
                      "header_handle": [
                        "https://scontent.whatsapp.net/v/t61.29..."
                      ]
                    }
                  },
                  {
                    "type": "BODY",
                    "text": "Add a touch of..."
                  },
                  {
                    "type": "BUTTONS",
                    "buttons": [
                      {
                        "type": "QUICK_REPLY",
                        "text": "Send me more like this!"
                      },
                      {
                        "type": "URL",
                        "text": "Shop",
                        "url": "https://www.luckyshrub.com/rare-succulents/{{1}}",
                        "example": [
                          "BLUE_ELF"
                        ]
                      }
                    ]
                  }
                ]
              }
              ...
            ]
          }
        ],
        "language": "en_US",
        "status": "APPROVED",
        "category": "MARKETING",
        "id": "1945418102598215"
      }
      ...
    ],
    "paging": {
      "cursors": {
        "before": "QVFIU...",
        "after": "QVFIU..."
      }
    }
  },
  "id": "9020555671393375"
}
```

## Update a template group

Use the [Template Group API](https://developers.facebook.com/docs/graph-api/reference/business-messaging-template-group#Updating) to update a template group’s name or description, or to add or remove templates to and from the group.

Note that removing a template from a group does not delete any metric-related data that the removed template may have already contributed to the group’s overall template group metrics.

### Request

```html
curl 'https://graph.facebook.com/<API_VERSION>/<TEMPLATE_GROUP_ID>' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <ACCESS_TOKEN>' \
-d '
{
  "name": "<TEMPLATE_GROUP_NAME>",
  "description": "<TEMPLATE_GROUP_DESCRIPTION>",
  "add_templates": [
    <TEMPLATE_IDS>
  ],
  "remove_templates": [
    <TEMPLATE_IDS>
  ]
}'
```

### Request parameters

| Placeholder | Description | Example value |
| --- | --- | --- |
| `<API_VERSION>`<br>*String* | **Optional.**<br>Graph API version. | v25.0 |
| `<TEMPLATE_GROUP_ID>`*String* | **Required.**<br>Template group ID. | `102290129340398` |
| `<ACCESS_TOKEN>`<br>*String* | **Required.**<br>[System token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens) or [business token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens). | `EAAA...` |
| `<TEMPLATE_GROUP_NAME>`*String* | **Optional.**<br>Template group name. Must be unique.<br>Maximum 256 characters. | `Black Friday 2024` |
| `<TEMPLATE_GROUP_DESCRIPTION>`*String* | **Optional.**<br>Template group description.<br>Maximum 512 characters. | `US-based Black Friday sale 2024 templates.` |
| `<TEMPLATE_IDS>`*Array of integers* | **Optional.**<br>Array of template IDs to add to the group. | `278077987957091,1945418102598215,1035843174854974` |

### Response

Upon success:

```html
{
  "success": <SUCCESS>
}
```

### Response parameters

| Placeholder | Description | Example value |
| --- | --- | --- |
| `<SUCCESS>` | Value set to `true` if the update template group request is successful, otherwise it will be set to `false`. | `true` |

### Example request

This example adds two templates to a template group while removing a third template from the group.

```curl
curl 'https://graph.facebook.com/v25.0/9020555671393375' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "add_templates": [844006344365270,1188657612184382],
  "remove_templates": [1035843174854974]
}'
```

### Example response

```json
{
  "success": true
}
```

## Delete a template group

Use the [Template Group API](https://developers.facebook.com/docs/graph-api/reference/business-messaging-template-group#Deleting) to delete a template group. Deleting a template group does not delete its associated templates.

### Request

```html
curl -X DELETE 'https://graph.facebook.com/<API_VERSION>/<TEMPLATE_GROUP_ID>' \
-H 'Authorization: Bearer <ACCESS_TOKEN>'
```

### Request parameters

| Placeholder | Description | Example value |
| --- | --- | --- |
| `<API_VERSION>`<br>*String* | **Optional.**<br>Graph API version. | v25.0 |
| `<TEMPLATE_GROUP_ID>`*String* | **Required.**<br>Template group ID. | `102290129340398` |
| `<ACCESS_TOKEN>`<br>*String* | **Required.**<br>[System token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens) or [business token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens). | `EAAA...` |

### Response

Upon success:

```html
{
  "success": <SUCCESS>
}
```

### Response parameters

| Placeholder | Description | Example value |
| --- | --- | --- |
| `<SUCCESS>` | Value set to `true` if the deletion successful, otherwise it will set to `false`. | `true` |

### Example request

```curl
curl -X DELETE 'https://graph.facebook.com/v25.0/9020555671393375' \
-H 'Authorization: Bearer EAAJB...'
```

### Example response

```json
{
  "success": true
}
```

## Template group analytics

See the [Template group analytics](https://developers.facebook.com/documentation/business-messaging/whatsapp/analytics#template-group-analytics) document.
