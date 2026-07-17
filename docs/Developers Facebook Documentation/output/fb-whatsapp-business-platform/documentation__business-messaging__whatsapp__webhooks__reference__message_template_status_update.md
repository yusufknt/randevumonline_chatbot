# message_template_status_update webhook reference | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/message_template_status_update_

---

# message_template_status_update webhook reference

Updated: Apr 13, 2026

This reference describes trigger events and payload contents for the WhatsApp Business Account `message_template_status_update` webhook.

The **message_template_status_update** webhook notifies you of changes to the status of an existing template.

## Triggers

- A template is approved.
- A template is rejected.
- A template is disabled.
- A template is archived.
- A template is unarchived.

## Syntax

```html
{
  "entry": [
    {
      "id": "<WHATSAPP_BUSINESS_ACCOUNT_ID>",
      "time": <WEBHOOK_TRIGGER_TIMESTAMP>,
      "changes": [
        {
          "value": {
            "event": "<EVENT>",
            "message_template_id": <TEMPLATE_ID>,
            "message_template_name": "<TEMPLATE_NAME>",
            "message_template_language": "<TEMPLATE_LANGUAGE_AND_LOCALE_CODE>",
            "reason": "<REASON>",
            "message_template_category": "<TEMPLATE_CATEGORY>",

            <!-- only included if template disabled -->
            "disable_info": {
              "disable_date": "<DISABLE_TIMESTAMP>"
            },

            <!-- only included if template locked or unlocked -->
            "other_info": {
              "title": "<TITLE>",
              "description": "<DESCRIPTION>"
            },

            <!-- only included if template rejected with INVALID_FORMAT reason -->
            "rejection_info": {
              "reason": "<REASON_INFO>",
              "recommendation": "<RECOMMENDATION_INFO>"
            }
          },
          "field": "message_template_status_update"
        }
      ]
    }
  ],
  "object": "whatsapp_business_account"
}
```

## Parameters

| Placeholder | Description | Example value |
| --- | --- | --- |
| `<DESCRIPTION>`<br>*String* | String describing why the template was locked or unlocked. | Your WhatsApp message template has been unpaused. |
| `<DISABLE_TIMESTAMP>`<br>*Integer* | Unix timestamp indicating when the template was disabled. | `1751234563` |
| `<EVENT>`<br>*String* | Template status event. Values can be:<br>`APPROVED` — Indicates the template has been approved and can now be sent in template messages.<br>`ARCHIVED` — Indicates the template has been [archived](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-archival) due to inactivity. Archived templates are scheduled for deletion after 28 days unless unarchived.<br>`UNARCHIVED` — Indicates the template has been [unarchived](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-archival) and restored to its previous status.<br>`DELETED` — Indicates the template has been deleted.<br>`DISABLED` — Indicates the template has been disabled due to user [feedback](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-quality).<br>`FLAGGED` — Indicates the template has received negative feedback and is at risk of being disabled.<br>`IN_APPEAL` — Indicates the template is in the [appeal](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-review#appeals) process.<br>`LIMIT_EXCEEDED` — Indicates the WhatsApp Business Account template is at its [template limit](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview).<br>`LOCKED` — Indicates the template has been locked and cannot be edited.<br>`PAUSED` — Indicates the template has been [paused](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-pausing).<br>`PENDING` — Indicates the template is undergoing template review.<br>`REINSTATED` — Indicates the template is no longer flagged or disabled and can be sent in template messages again.<br>`PENDING_DELETION` — Indicates template has been deleted via WhatsApp Manager.<br>`REJECTED` — Indicates the template has been rejected. You can [edit the template](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview) to have it undergo template review again or [appeal](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-review#appeals) the rejection. | `APPROVED` |
| `<TEMPLATE_ID>`<br>*Integer* | Template ID. | `1689556908129832` |
| `<TEMPLATE_NAME>`<br>*String* | Template name. | `order_confirmation` |
| `<TEMPLATE_LANGUAGE_AND_LOCALE_CODE>`<br>*String* | Template [language and locale](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/supported-languages) code. | `en-US` |
| `<REASON>`<br>*String* | Template rejection reason, if rejected.<br>If the template is scheduled for deletion, the value will be `null` instead of a string. Otherwise, values can be:<br>`ABUSIVE_CONTENT` — Indicates template contains content that violates our policies.<br>`CATEGORY_NOT_AVAILABLE` — (Deprecated) Indicates an authentication templates for an unsupported region.<br>`INCORRECT_CATEGORY` — Indicates the template’s content doesn’t match the category designated at the time of template creation.<br>`INVALID_FORMAT` — Indicates template has an invalid format.<br>`NONE`: Indicates template was paused.<br>`PROMOTIONAL` — Indicates template contains content that violates our policies.<br>`SCAM` — Indicates template contains content that violates our policies.<br>`TAG_CONTENT_MISMATCH` — Indicates the template’s content doesn’t match the category designated at the time of template creation. | `INVALID_FORMAT` |
| `<TITLE>`<br>*String* | Title of template pause or unpause event.<br>Values can be:<br>`FIRST_PAUSE` — Indicates template has been paused for the first time.<br>`SECOND_PAUSE` — Indicates the template has been paused a second time.<br>`RATE_LIMITING_PAUSE` — Indicates template has been paused due to rate limiting.<br>`UNPAUSE` — Indicates template has been unpaused.<br>`DISABLED` — Indicates template has been disabled. | `FIRST_PAUSE` |
| `<WEBHOOK_TRIGGER_TIMESTAMP>`<br>*Integer* | Unix timestamp indicating when the webhook was triggered. | `1739321024` |
| `<WHATSAPP_BUSINESS_ACCOUNT_ID>`<br>*String* | WhatsApp Business Account ID. | `102290129340398` |
| `<MESSAGE_TEMPLATE_CATEGORY>`<br>*String* | The template category.<br>Values can be:<br>`MARKETING` — Indicates template is categorized as MARKETING.<br>`UTILITY` — Indicates the template is categorized as UTILITY.<br>`AUTHENTICATION` — Indicates template is categorized as AUTHENTICATION. | `MARKETING` |
| `<REASON_INFO>`<br>*String* | Provides a detailed explanation for why the template was rejected. This field describes the specific issue detected in the template content. | `Your template has parameters placed next to each other (like {{1}}{{2}}) without text or punctuation between them.` |
| `<RECOMMENDATION_INFO>`<br>*String* | Offers actionable guidance on how to modify the template to resolve the rejection reason. This field suggests best practices for editing the template content. | `Separate parameters with descriptive text and ensure each parameter is clearly contextualized.` |

## Example

This example webhook describes a template that has been approved.

```json
{
  "entry": [
    {
      "id": "102290129340398",
      "time": 1751247548,
      "changes": [
        {
          "value": {
            "event": "APPROVED",
            "message_template_id": 1689556908129832,
            "message_template_name": "order_confirmation",
            "message_template_language": "en-US",
            "reason": "NONE",
            "message_template_category": "UTILITY"
          },
          "field": "message_template_status_update"
        }
      ]
    }
  ],
  "object": "whatsapp_business_account"
}
```

This example webhook describes a template that has been rejected with INVALID_FORMAT.

```json
{
  "entry": [
    {
      "id": "102290129340398",
      "time": 1751247548,
      "changes": [
        {
          "value": {
            "event": "REJECTED",
            "message_template_id": 1689556908129835,
            "message_template_name": "abandoned_cart",
            "message_template_language": "en",
            "reason": "INVALID_FORMAT",
            "message_template_category": "MARKETING",
            "rejection_info": {
              "reason": "Your template has parameters placed next to each other (like {{1}}{{2}}) without text or punctuation between them.",
              "recommendation": "Separate parameters with descriptive text and ensure each parameter is clearly contextualized."
            }
          },
          "field": "message_template_status_update"
        }
      ]
    }
  ],
  "object": "whatsapp_business_account"
}
```
