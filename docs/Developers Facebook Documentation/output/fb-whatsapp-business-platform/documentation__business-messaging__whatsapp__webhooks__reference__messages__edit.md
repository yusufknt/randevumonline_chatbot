# Edit messages webhook reference | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/edit_

---

# Edit messages webhook reference

Updated: Dec 3, 2025

The edit webhook is only available to WhatsApp Business app users (aka “Coexistence”)

This reference describes edit events and payload contents for the WhatsApp Business Account **messages** webhook for replies to messages.

## Triggers

- A WhatsApp user edits a previously sent message (text, media with caption).
- A WhatsApp user edits a previous sent message within 15 minutes after being sent.

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
               "type": "edit",
               "edit": {
                 "original_message_id": "<ORIGINAL_WHATSAPP_MESSAGE_ID>",
                 "message": {
                   "context": {
                     "id": "<CONTEXT_ID>"
                   },
                   "type": "image",
                   "image": {
                     "caption": "<MEDIA_ASSET_CAPTION>",
                     "mime_type": "<MEDIA_ASSET_MIME_TYPE>",
                     "sha256": "<MEDIA_ASSET_SHA256_HASH>",
                     "id": "<MEDIA_ASSET_ID>",
                     "url": "<MEDIA_ASSET_URL>"
                   }
                 }
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
| `<WHATSAPP_MESSAGE_ID>` | WhatsApp message ID for the edit event. | wamid.HBgLMTY1MDM4Nzk0MzkV... |
| `<WEBHOOK_TRIGGER_TIMESTAMP>` | Unix timestamp when the webhook was triggered. | 1739321024 |
| `<ORIGINAL_WHATSAPP_MESSAGE_ID>` | ID of the original message being edited. | wamid.HBgLMTQxMjU1NTA4MjkV... |
| `<CONTEXT_ID>` | Contextual message ID (if applicable). | M0 |
| `<MEDIA_ASSET_CAPTION>` | Caption for the media asset. | Updated image caption |
| `<MEDIA_ASSET_MIME_TYPE>` | MIME type of the media asset. | image/jpeg |
| `<MEDIA_ASSET_SHA256_HASH>` | SHA256 hash of the media asset. | a1b2c3d4e5f6... |
| `<MEDIA_ASSET_ID>` | Media asset ID. | 1234567890 |
| `<MEDIA_ASSET_URL>` | URL to the media asset. | https://media.example.com/... |

## Example

This example webhook describes an edit made by a user in a message.

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
               "type": "edit",
               "edit": {
                 "original_message_id": "wamid.HBgLMTQxMjU1NTA4MjkVAgASGBQzQUNCNjk5RDUwNUZGMUZEM0VBRAA=",
                 "message": {
                   "context": {
                     "id": "M0"
                   },
                   "type": "image",
                   "image": {
                     "caption": "Updated image caption",
                     "mime_type": "image/jpeg",
                     "sha256": "a1b2c3d4e5f6...",
                     "id": "1234567890",
                     "url": "https://media.example.com/updated-image.jpg"
                   }
                 }
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
