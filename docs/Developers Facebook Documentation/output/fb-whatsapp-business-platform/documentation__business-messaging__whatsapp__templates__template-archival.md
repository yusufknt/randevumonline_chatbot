# Template archival | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-archival_

---

# Template archival

Updated: Apr 17, 2026

Templates that have been inactive for 12 months or more are automatically archived. Archived templates cannot be sent in template messages and are scheduled for deletion after 28 days. You can unarchive a template within the 28-day window to restore it to its previous status.

## Auto-archival

All WhatsApp Business Accounts have auto-archival enabled. You cannot opt out of auto-archival.

A template is eligible for auto-archival when all of the following are true:

- The template status is not `PENDING_DELETION` , `DELETED` , or `ARCHIVED` .
- The template has been inactive for longer than 12 months.

Template activity includes creating, editing, sending, appealing, or unarchiving a template.

## Post-archival deletion

WhatsApp automatically deletes archived templates 28 days after archival. Once deleted, the template cannot be recovered. If you unarchive a template before the 28-day window expires, the scheduled deletion is cancelled.

## Notifications

When templates are archived, you are notified through the following channels:

- **Webhook** — A [message_template_status_update](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/message_template_status_update) webhook is sent for each template that is archived or unarchived.
- **Email** — An email is sent when templates are archived, listing the affected templates with a link to view and unarchive them in WhatsApp Manager.
- **WhatsApp Manager banner** — A one-time banner is displayed before the first auto-archival cycle, informing you that templates inactive for 12 months or more will be automatically archived.
