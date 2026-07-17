# smb_app_state_sync webhook reference | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/smb_app_state_sync_

---

# smb_app_state_sync webhook reference

Updated: Oct 22, 2025

This reference describes trigger events and payload contents for the WhatsApp Business Account **smb_app_state_sync** webhook.

The **smb_app_state_sync** webhook is used for synchronizing contacts of [WhatsApp Business app users who have been onboarded](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users) via a solution provider.

## Triggers

- A solution provider [synchronizes the WhatsApp Business app contacts](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users#step-1--initiate-contacts-synchronization) of a business customer with a WhatsApp Business app phone number who the provider has [onboarded](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users) .
- A business customer with a WhatsApp Business app phone number who has been [onboarded](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users) by a solution provider adds a contact to their WhatsApp Business app [contacts](https://faq.whatsapp.com/1270784217226727/) .
- A business customer with a WhatsApp Business app phone number who has been [onboarded](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users) by a solution provider removes a contact from their WhatsApp Business app [contacts](https://faq.whatsapp.com/1270784217226727/) .
- A business customer with a WhatsApp Business app phone number who has been [onboarded](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users) by a solution provider edits a contact in their WhatsApp Business app [contacts](https://faq.whatsapp.com/1270784217226727/) .

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
            "state_sync": [
              {
                "type": "contact",
                "contact": {
                  "full_name": "<CONTACT_FULL_NAME>",
                  "first_name": "<CONTACT_FIRST_NAME>",
                  "phone_number": "<CONTACT_PHONE_NUMBER>"
                },
                "action": "<ACTION>",
                "metadata": {
                  "timestamp": "<WEBHOOK_TRIGGER_TIMESTAMP>"
                }
              },
              <!-- Additional contacts would follow, if any -->
            ]
          },
          "field": "smb_app_state_sync"
        }
      ]
    }
  ]
}
```

## Parameters

| Placeholder | Description | Example value |
| --- | --- | --- |
| `<ACTION>`<br>*String* | Indicates if the business customer added, edited, or deleted a contact from their WhatsApp Business app phone address book.<br>Values can be:<br>`add` — Indicates the WhatsApp Business app user added or edited a contact.<br>`remove` — Indicates the WhatsApp Business app user removed a contact. | `add` |
| `<BUSINESS_DISPLAY_PHONE_NUMBER>`<br>*String* | Business display phone number. | `15550783881` |
| `<BUSINESS_PHONE_NUMBER_ID>`<br>*String* | Business phone number ID. | `106540352242922` |
| `<CONTACT_FIRST_NAME>`<br>*String* | The contact’s first name, as it appears in the business customer’s WhatsApp Business app phone address book.<br>Not included when the business customer removes a contact from their WhatsApp Business app phone address book. | `Pablo` |
| `<CONTACT_FULL_NAME>`<br>*String* | The contact’s full name, as it appears in the business customer’s WhatsApp Business app phone address book.<br>Not included when the business customer removes a contact from their WhatsApp Business app phone address book. | `Pablo Morales` |
| `<CONTACT_PHONE_NUMBER>`*String* | The contact’s WhatsApp phone number. | `16505551234` |
| `<WEBHOOK_TRIGGER_TIMESTAMP>`<br>*Integer* | Unix timestamp indicating when the webhook was triggered. | `1739321024` |
| `<WHATSAPP_BUSINESS_ACCOUNT_ID>`<br>*String* | WhatsApp Business Account ID. | `102290129340398` |

## Example

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
            "state_sync": [
              {
                "type": "contact",
                "contact": {
                  "full_name": "Pablo Morales",
                  "first_name": "Pablo",
                  "phone_number": "16505551234"
                },
                "action": "add",
                "metadata": {
                  "timestamp": "1739321024"
                }
              }
            ]
          },
          "field": "smb_app_state_sync"
        }
      ]
    }
  ]
}
```
