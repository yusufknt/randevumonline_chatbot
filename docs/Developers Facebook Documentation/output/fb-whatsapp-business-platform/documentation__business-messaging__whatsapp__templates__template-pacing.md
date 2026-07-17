# Template pacing | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-pacing_

---

# Template pacing

Updated: Dec 8, 2025

Template pacing is a mechanism that allows time for customers to provide early feedback on templates. This identifies and [pauses templates](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-pausing) that have received poor feedback or engagement, giving you enough time to adjust their contents before they are sent to too many customers, thereby reducing the likelihood of negative feedback impacting your business.

Template pacing is valid for marketing and utility templates. Newly created templates, paused templates that are unpaused, and templates that may have been created previously but don’t have a `GREEN` quality rating are potentially subject to pacing. Template quality history — for example, low quality resulting in a template pause — is one of the primary reasons for template pacing and you may see other templates get paced.
When a template is paced, messages will be sent normally until an unspecified threshold is reached. Once this threshold is reached, subsequent messages using that template will be held to allow enough time for customer feedback. Once we receive a good quality signal, subsequent messages using that template will be scaled to the entire target audience. If we receive a bad quality signal, subsequent messages using that template will be dropped, giving you the opportunity to adjust content, targeting, etc.

## Utility template pacing

Utility templates are subject to pacing only if you have had a utility template paused. Once a utility template has been paused, newly created templates, paused templates that are unpaused, and templates that may have been created previously but don’t have GREEN quality rating are potentially subject to pacing for the next 7 days.

## API Behavior

The immediate response from the messages endpoint will indicate if the message was sent or held with the new `message_status` property in the `messages` object. This response will be available on all versions of the API.

- Cloud API will always include a `message_status` property that will have a value of `accepted` for messages that are processed, and `held_for_quality_assessment` for messages that are held. Messages that are accepted will trigger the `sent` and `delivered` webhooks when they are actually sent (this is the same behavior that existed before pacing). A full example response can be found in the Cloud API docs.

If the feedback is positive and changes the template’s quality rating to high quality, the held messages will be released and sent normally. The `message_template_quality_update` will send the quality update and the `messages` webhook will send the sent and delivered updates.

If the feedback is negative and changes the template’s quality to low quality:

- The template’s `status` will be set to `PAUSED`
- A `message_template_status_update` will be sent with an event value of `paused`
- Each held message will be dropped and trigger a `messages` webhook with `"status":"failed"` and `"code":"132015"` (Cloud API users).
- A `message_template_quality_update` webhook will be triggered with the quality change
- Admins of the WhatsApp Business Account owning business will be informed of the dropped messages by Meta Business Suite notification, WhatsApp Manager banner, and email

See [Template Pausing](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-pausing) to learn how to unpause a template that has been paused due to pacing.

Note that we have internal guardrails in place to ensure that we evaluate and make a pacing decision within a reasonable time to avoid impact on time sensitive campaigns. Our goal is that even if paced, campaign messages with highest throughput still get delivered within an hour (99 percentile).

Thus, if our internal guardrails are reached before a template has received enough feedback to change its quality to high or low, the held messages will be released normally along with any appropriate messages webhooks.
