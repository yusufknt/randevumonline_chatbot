# Instant Form Template | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/templates/instant-form-template_

---

# Instant Form Template

Updated: Jul 26, 2023

Instant Form templates help you generate and qualify leads by asking people to fill out a form without leaving the conversation.

This functionality is in development. Meta can change or remove this functionality at any time.

This guide explains how to send an instant form for a Messenger conversation.

## Before You Start

This guide assumes you have read the [Messenger Platform Overview](https://developers.facebook.com/documentation/business-messaging/messenger-platform/overview) and implemented the needed components for sending and receiving messages and notifications.

You will need:

- An eligible form ID [Create a form](https://developers.facebook.com/documentation/ads-commerce/marketing-api/guides/lead-ads/create)[Get the ID for an existing form](https://developers.facebook.com/documentation/ads-commerce/marketing-api/guides/lead-ads/create#get-a-list-of-eligible-forms-for-messenger)

### Form Eligibility Requirements

For a form to be eligible, it must contain the following elements:

- Questions in the form can only be one of the following types: `CUSTOM``EMAIL``FIRST_NAME``FULL_NAME``LAST_NAME``PHONE`If a form has a `questions.type` that is set to any other value than those listed, the form will be ineligible.
- During form creation, the `block_display_for_non_targeted_viewer` parameter must be set to `false` . This marks the form as Open Sharing.

Visit the
[Marketing API - Lead Ads Forms documentation](https://developers.facebook.com/documentation/ads-commerce/marketing-api/guides/lead-ads/create)
for more information.

## Step 2. Send

Use the instant form template to send the form to a potential customer.

To send an instant form message, send a `POST` request to the `/`***`page_id`***`/messages` endpoint where ***page_id** is the Page sending the message with the following required parameters:

- a `recipient_id` set to the person’s Page-scoped ID
- `message.attachment` object with: `type` set to `template``payload` object with:
 `template_type` set to `instant_form``form_id` set to the ID for your form

Example Request

Formatted for readability. Replace bold, italics values, such as ad_account_id, with your values.

```curl
curl -X POST "https://graph.facebook.com/v25.0/YOUR_PAGE_ID/messages" \
     -H "Content-Type: application/json" \
     -d '{
           "access_token":"YOUR_PAGE_ACCESS_TOKEN",
           "recipient": { "id": "PAGE_SCOPED_ID" },
           "message": {
             "attachment": {
               "type": "template",
               "payload": {
                 "template_type": "instant_form",
                 "form_id": "YOUR_INSTANT_FORM_ID",
  }'
```

On success your app receives the following JSON response with the ID for the recipient and the ID for the message.

```json
{
  "recipient_id": "RECIPIENT_ID",
  "message_id": "MESSAGE_ID"
}
```

Error Codes

The most common error response your app will receive is `2018382` where in the form ID is incorrect or the form is ineligible.

```json
{
  "error": {
    "message": "(#1) The given \"FORM_ID\" field is incorrect, or the form is not inthread eligible.",
    "type": "OAuthException",
    "code": 1,
    "error_subcode": 2018382,
    "fbtrace_id": "..."
  }
}
```

## Webhook Notifications

When a person has submitted an instant form message, the `messaging_in_thread_lead_form_submit` webhook is triggered and your app will receive a notification with information about the form submission.

### Example Notification

```json
{
  "object": "page",
  "entry": [
    {
      "time": UNIX_TIME_STAMP,
      "id":  PAGE_ID,
      "messaging:": [
        {
          "sender": {
            "id":  SENDER_ID},
"recipient": {
  "id":  RECIPIENT_ID    }
"timestamp":  UNIX_TIME_STAMP,
          "form": {
            "id":  FORM_ID          }
        }
      ]
    }
  ]
}
```
