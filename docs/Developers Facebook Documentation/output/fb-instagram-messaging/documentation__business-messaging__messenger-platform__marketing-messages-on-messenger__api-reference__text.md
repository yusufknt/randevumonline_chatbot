# Text Template | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/api-reference/text_

---

# Text Template

Updated: Oct 23, 2025

Text templates represent a plain text message that can be sent to the user, the message can be up to 640 characters in length. This template generally can be utilized to promote a coming discount or event.

```json
{
  "message_id": "<MESSAGE_ID>",
  "messenger_delivery_data": {
    "subscription_token": "<SUBSCRIPTION_TOKEN>"
  },
  "message": {
    "text": "Add text message here."
  }
}
```
