# Template management | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-management_

---

# Template management

Updated: Apr 13, 2026

Learn about common endpoints used to manage templates, including getting, editing, deleting, archiving, and unarchiving templates.

## Get templates

Use the [Message Templates API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/template-api#get-version-waba-id-message-templates) to get a list of templates in a WhatsApp Business Account.

### Get all templates

Example request to get all templates (default fields):

```curl
curl 'https://graph.facebook.com/v23.0/102290129340398/message_templates' \
-H 'Authorization: Bearer EAAJB...'
```

Example response, truncated (`...`) for brevity:

```json
{
  "data": [
    {
      "name": "reservation_confirmation",
      "parameter_format": "NAMED",
      "components": [
        {
          "type": "HEADER",
          "format": "IMAGE",
          "example": {
            "header_handle": [
              "https://scontent.whatsapp.net/v/t61..."
            ]
          }
        },
        {
          "type": "BODY",
          "text": "*You're all set!*\n\nYour reservation for {{number_of_guests}} at Lucky Shrub Eatery on {{day}}, {{date}}, at {{time}}, is confirmed. See you then!",
          "example": {
            "body_text_named_params": [
              {
                "param_name": "number_of_guests",
                "example": "4"
              },
              {
                "param_name": "day",
                "example": "Saturday"
              },
              {
                "param_name": "date",
                "example": "August 30th, 2025"
              },
              {
                "param_name": "time",
                "example": "7:30 pm"
              }
            ]
          }
        },
        {
          "type": "FOOTER",
          "text": "Lucky Shrub Eatery: The Luckiest Eatery in Town!"
        },
        {
          "type": "BUTTONS",
          "buttons": [
            {
              "type": "URL",
              "text": "Change reservation",
              "url": "https://www.luckyshrubeater.com/reservations"
            },
            {
              "type": "PHONE_NUMBER",
              "text": "Call us",
              "phone_number": "+16467043595"
            },
            {
              "type": "QUICK_REPLY",
              "text": "Cancel reservation"
            }
          ]
        }
      ],
      "language": "en_US",
      "status": "APPROVED",
      "category": "UTILITY",
      "id": "1387372356726668"
    },
    {
      "name": "coupon_expiration_reminder_number_vars",
      "parameter_format": "POSITIONAL",
      "components": [
        {
          "type": "HEADER",
          "format": "TEXT",
          "text": "Act fast, {{1}}!",
          "example": {
            "header_text": [
              "Pablo"
            ]
          }
        },
        {
          "type": "BODY",
          "text": "Just a quick reminder—your exclusive coupon code, {{1}}, *expires in only {{2}} days!* Don't miss out on our special deals. Use your code at checkout before it's too late.\n\nHappy shopping! 😃",
          "example": {
            "body_text": [
              [
                "SUMMER20",
                "10"
              ]
            ]
          }
        },
        {
          "type": "FOOTER",
          "text": "Lucky Shrub Succulents"
        },
        {
          "type": "BUTTONS",
          "buttons": [
            {
              "type": "URL",
              "text": "See deals",
              "url": "https://www.luckyshrub.com/deals"
            },
            {
              "type": "QUICK_REPLY",
              "text": "Unsubscribe"
            }
          ]
        }
      ],
      "language": "en",
      "status": "APPROVED",
      "category": "MARKETING",
      "sub_category": "CUSTOM",
      "id": "1304694804498707"
    }

    ...

  ],
  "paging": {
    "cursors": {
      "before": "QVFIU...",
      "after": "QVFIU..."
    },
    "next": "https://graph.facebook.com/v23.0/10229..."
  }
}
```

### Get all templates and specific fields

Example request to get the name, category, and status of all templates in a WhatsApp Business Account, limiting the response to 5 templates per result set:

```curl
curl 'https://graph.facebook.com/v23.0/102290129340398/message_templates?fields=name,category,status&limit=5' \
-H 'Authorization: Bearer EAAJB...'
```

Example response:

```json
{
  "data": [
    {
      "name": "reservation_confirmation",
      "category": "UTILITY",
      "status": "APPROVED",
      "id": "1387372356726668"
    },
    {
      "name": "coupon_expiration_reminder_number_vars",
      "category": "MARKETING",
      "status": "APPROVED",
      "id": "1304694804498707"
    },
    {
      "name": "coupon_expiration_reminder_named_vars",
      "category": "MARKETING",
      "status": "APPROVED",
      "id": "1625063511800527"
    },
    {
      "name": "address_update",
      "category": "UTILITY",
      "status": "PENDING",
      "id": "1137051647947973"
    },
    {
      "name": "reservation_confirmation_short_banner",
      "category": "UTILITY",
      "status": "REJECTED",
      "id": "1166414785519855"
    }
  ],
  "paging": {
    "cursors": {
      "before": "QVFIU...",
      "after": "QVFIU..."
    },
    "next": "https://graph.facebook.com/v23.0/10229..."
  }
}
```

### Get all approved and rejected templates

Example request to get all approved templates and their name, category, and status (swap `status=approved` with `status=rejected` to get rejected templates instead):

```json
curl 'https://graph.facebook.com/v23.0/102290129340398/message_templates?fields=name,category,status&status=approved' \
-H 'Authorization: Bearer EAAJB...'
```

Example response:

```json
{
  "data": [
    {
      "name": "reservation_confirmation",
      "category": "UTILITY",
      "status": "APPROVED",
      "id": "1387372356726668"
    },
    {
      "name": "coupon_expiration_reminder_number_vars",
      "category": "MARKETING",
      "status": "APPROVED",
      "id": "1304694804498707"
    },
    {
      "name": "coupon_expiration_reminder_named_vars",
      "category": "MARKETING",
      "status": "APPROVED",
      "id": "1625063511800527"
    },
    {
      "name": "calling_permission_request",
      "category": "MARKETING",
      "status": "APPROVED",
      "id": "1092999222892024"
    },
    {
      "name": "location_request_v1",
      "category": "MARKETING",
      "status": "APPROVED",
      "id": "3373761659571648"
    },
    {
      "name": "order_confirmation",
      "category": "UTILITY",
      "status": "APPROVED",
      "id": "1667696820637468"
    }
  ],
  "paging": {
    "cursors": {
      "before": "QVFIU...",
      "after": "QVFIU..."
    },
    "next": "https://graph.facebook.com/v23.0/10229..."
  }
}
```

## Edit templates

Use the [Template API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/template-api#post-version-template-id) to edit a template. You can also use the [Message templates](https://business.facebook.com/latest/whatsapp_manager/message_templates) panel in WhatsApp Manager to edit templates.

### Limitations

- Only templates with an `APPROVED` , `REJECTED` , or `PAUSED` status can be edited.
- You can only edit a template’s category, components, or time-to-live.
- You cannot edit individual template components; all components will be replaced with the components in the edit request payload.
- You cannot edit the category of an approved template.
- Approved templates can be edited up to 10 times in a 30 day window, or 1 time in a 24 hour window. Rejected or paused templates can be edited an unlimited number of times.
- After editing an approved or paused template, it will automatically be approved unless it fails template review.

### Edit template category

Example request:

```curl
curl 'https://graph.facebook.com/v23.0/1252715608684590' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "category": "MARKETING"
}'
```

Example response:

```json
{
  "success": true
}
```

### Edit template components

Example request to overwrite a template’s existing components with new components.

```curl
curl 'https://graph.facebook.com/v23.0/564750795574598' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "components": [
    {
      "type": "HEADER",
      "format": "TEXT",
      "text": "Our {{1}} is on!",
      "example": {
        "header_text": [
          "Spring Sale"
        ]
      }
    },
    {
      "type": "BODY",
      "text": "Shop now through {{1}} and use code {{2}} to get {{3}} off of all merchandise.",
      "example": {
        "body_text": [
          [
            "the end of April",
            "25OFF",
            "25%"
          ]
        ]
      }
    },
    {
      "type": "FOOTER",
      "text": "Use the buttons below to manage your marketing subscriptions"
    },
    {
      "type": "BUTTONS",
      "buttons": [
        {
          "type": "QUICK_REPLY",
          "text": "Unsubscribe from Promos"
        },
        {
          "type": "QUICK_REPLY",
          "text": "Unsubscribe from All"
        }
      ]
    }
  ]
}'
```

## Delete templates

Use the [Message Templates API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/template-api#delete-version-waba-id-message-templates) to delete a template by name or ID.

### Limitations

- If you delete a template that has been sent in a template message but has yet to be delivered (e.g. because the customer’s phone is turned off), the template’s status will be set to `PENDING_DELETION` and we will attempt to deliver the message for 30 days.
- If you delete an approved template, you cannot create a new template with the same name for 30 days.
- Templates that are in a disabled status cannot be deleted.

### Delete template by name

Deleting a template by name deletes all templates that match that name (meaning templates with the same name but different languages will also be deleted).

Example request:

```curl
curl -X DELETE 'https://graph.facebook.com/v23.0/102290129340398/message_templates?name=order_confirmation' \
-H 'Authorization: Bearer EAAJB...'
```

Example response:

```curl
{
  "success": true
}
```

### Delete template by ID

To delete a template by ID, include the template’s ID along with its name in your request; only the template with the matching template ID will be deleted.

Example request:

```curl
curl -X DELETE 'https://graph.facebook.com/v23.0/102290129340398/message_templates?hsm_id=1407680676729941&name=order_confirmation' \
-H 'Authorization: Bearer EAAJB...'
```

### Example response

```json
{
  "success": true
}
```

## Archive and unarchive templates

Templates that have been inactive for 12 months or more are automatically archived and scheduled for deletion after 28 days. You can also manually archive or unarchive templates in bulk using the API.

See [template archival](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-archival) for more information about auto-archival, the archive and unarchive endpoints, and notifications.
