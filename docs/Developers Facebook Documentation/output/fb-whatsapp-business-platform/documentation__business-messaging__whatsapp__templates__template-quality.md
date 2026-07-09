# Template quality rating | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-quality_

---

# Template quality rating

Updated: Oct 29, 2025

Every template has a quality rating based on usage, customer feedback, and engagement. Templates can have the following ratings, as reported by the API:

- `GREEN` — Indicates high quality. The template has received little to no negative feedback from WhatsApp users. The template can be sent.
- `YELLOW` — Indicates medium quality. The template has received negative feedback from multiple WhatsApp users, or low read-rates, and may soon become paused or disabled. Message templates with this status can still be sent.
- `RED` — Indicates low quality. The template has received negative feedback from multiple WhatsApp users, or low read-rates. The template can be sent, but is in danger of being paused or disabled soon. We recommend that you address the issues that users are reporting.
- `UNKNOWN` — Indicates a quality score is still pending, because it has yet to receive WhatsApp user feedback or read-rate data. The template can be sent.

Newly created templates have a quality score of `UNKNOWN`, but their rating will change automatically as usage, feedback, and engagement signal is collected over time.

Quality ratings factor into [template pacing](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-pacing) and [template pausing](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-pausing), which can affect template delivery. If a template continuously receives negative feedback or low engagement, it can eventually affect the template’s status. If the status changes to anything other than `APPROVED`, the template cannot be sent in template messages unless its `APPROVED` status is restored.

## Get template quality rating via API

Use the [Template API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/template-api#get-version-template-id) and request the `quality_score` field to get a template’s quality score.

### Example request

```curl
curl 'https://graph.facebook.com/v25.0/1105258428396250?fields=quality_score' \
-H 'Authorization: Bearer EAAJB...'
```

### Example response

```curl
{
  "quality_score": {
    "score": "GREEN",
    "date": 1758754645
  },
  "id": "1387372356726668"
}
```

## Get template quality rating via WhatsApp Manager

The [Manage templates](https://business.facebook.com/latest/whatsapp_manager/message_templates) panel in WhatsApp Manager also displays template quality ratings for templates that have an approved status:

- Active - **Quality pending** (equates to an `UNKNOWN` quality score)
- Active - **High quality** (equates to a `GREEN` quality score)
- Active - **Medium quality** (equates to a `YELLOW` quality score)
- Active - **Low quality** (equates to a `RED` quality score)

## See also

- [About your WhatsApp Business message template’s quality rating](https://www.facebook.com/business/help/766346674749731)
