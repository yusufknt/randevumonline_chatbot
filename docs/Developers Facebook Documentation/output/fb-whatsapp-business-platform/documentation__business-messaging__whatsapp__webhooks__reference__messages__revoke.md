# Revoke messages webhook reference | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/revoke_

---

# Revoke messages webhook reference

Updated: Dec 3, 2025

The revoke webhook is only available to WhatsApp Business app users (aka “Coexistence”)

This reference describes revoke events and payload contents for the WhatsApp Business Account messages webhook for replies to messages.

## Triggers

- A WhatsApp user revokes (deletes) a previously sent message.
- A WhatsApp user revokes a previous sent message within two days after being sent.

## Syntax

```html
{
 "object": "whatsapp_business_account",
 "entry": [
   {
     "id": "<WHATSAPP_BUSINESS_ACCOUNT_ID>",
     "changes": [
       {
         "value": {
           "messaging_product": "whatsapp",
           "metadata": {
             "display_phone_number": "<BUSINESS_DISPLAY_PHONE_NUMBER>",
             "phone_number_id": "<BUSINESS_PHONE_NUMBER_ID>"
           },
           "contacts": [
             {
               "profile": {
                 "name": "<WHATSAPP_USER_PROFILE_NAME>"
               },
               "wa_id": "<WHATSAPP_USER_ID>"
             }
           ],
           "messages": [
             {
               "from": "<WHATSAPP_USER_PHONE_NUMBER>",
               "id": "<WHATSAPP_MESSAGE_ID>",
               "timestamp": "<WEBHOOK_TRIGGER_TIMESTAMP>",
               "type": "revoke",
               "revoke": {
                 "original_message_id": "<ORIGINAL_WHATSAPP_MESSAGE_ID>"
               }
             }
           ]
         },
         "field": "messages"
       }
     ]
   }
 ]
}
```

## Parameters

| Placeholder | Description | Example value |
| --- | --- | --- |
| `<BUSINESS_DISPLAY_PHONE_NUMBER>` | Business display phone number. | 15550783881 |
| `<BUSINESS_PHONE_NUMBER_ID>` | Business phone number ID. | 106540352242922 |
| `<WHATSAPP_USER_PROFILE_NAME>` | WhatsApp user’s profile name. | Sheena Nelson |
| `<WHATSAPP_USER_ID>` | WhatsApp user ID. | 16505551234 |
| `<WHATSAPP_USER_PHONE_NUMBER>` | WhatsApp user phone number. | 16505551234 |
| `<WHATSAPP_MESSAGE_ID>` | WhatsApp message ID for the revoke event. | wamid.HBgLMTY1MDM4Nzk0MzkV... |
| `<WEBHOOK_TRIGGER_TIMESTAMP>` | Unix timestamp when the webhook was triggered. | 1739321024 |
| `<ORIGINAL_WHATSAPP_MESSAGE_ID>` | ID of the original message being revoked (deleted). | wamid.HBgLMTQxMjU1NTA4MjkV... |

## Example

This example webhook describes a delete made by a user in a message.

```json
{
 "object": "whatsapp_business_account",
 "entry": [
   {
     "id": "102290129340398",
     "changes": [
       {
         "value": {
           "messaging_product": "whatsapp",
           "metadata": {
             "display_phone_number": "15550783881",
             "phone_number_id": "106540352242922"
           },
           "contacts": [
             {
               "profile": {
                 "name": "Sheena Nelson"
               },
               "wa_id": "16505551234"
             }
           ],
           "messages": [
             {
               "from": "16505551234",
               "id": "wamid.HBgLMTY1MDM4Nzk0MzkVAgASGBQzQUFERjg0NDEzNDdFODU3MUMxMAA=",
               "timestamp": "1749854575",
               "type": "revoke",
               "revoke": {
                 "original_message_id": "wamid.HBgLMTQxMjU1NTA4MjkVAgASGBQzQUNCNjk5RDUwNUZGMUZEM0VBRAA="
               }
             }
           ]
         },
         "field": "messages"
       }
     ]
   }
 ]
}
```
