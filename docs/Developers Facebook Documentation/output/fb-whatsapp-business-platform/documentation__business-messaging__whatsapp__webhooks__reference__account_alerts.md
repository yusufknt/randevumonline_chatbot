# account_alerts webhook reference

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/account_alerts_

---

# account_alerts webhook reference

Updated: Nov 25, 2025

This reference describes trigger events and payload contents for the WhatsApp Business Account `account_alerts` webhook.

The **account_alerts** webhook notifies you of changes to a business phone number’s [messaging limit](https://developers.facebook.com/documentation/business-messaging/whatsapp/messaging-limits), [business profile](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers#business-profiles), and [Official Business Account](https://developers.facebook.com/documentation/business-messaging/whatsapp/whatsapp-business-accounts#official-business-account) status.

## Triggers

- An increase to the messaging limit of all of a business portfolio’s phone numbers is denied, a decision on the increase has been deferred, or more information is needed before a decision can be made.
- A business phone number Official Business Account status is approved or denied.
- A business phone number’s business profile photo is deleted.

## Syntax

```html
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "<WHATSAPP_BUSINESS_ACCOUNT_ID>",
      "time": <WEBHOOK_TRIGGER_TIMESTAMP>,
      "changes": [
        {
          "field": "account_alerts",
          "value": {
            "entity_type": "<ENTITY_TYPE>",
            "entity_id": "<ENTITY_ID>",
            "alert_info": {
              "alert_severity": "<ALERT_SEVERITY>",
              "alert_status": "<ALERT_STATUS>",
              "alert_type": "<ALERT_TYPE>",
              "alert_description": "<ALERT_DESCRIPTION>"
            }
          }
        }
      ]
    }
  ]
}
```

## Parameters

| Placeholder | Description | Example value |
| --- | --- | --- |
| `<ALERT_DESCRIPTION>`<br>*String* | Alert description.<br>Values can be:<br>`Additional verification is required for your business {NAME}. Go to Security Center in Meta for Business to complete identity verification. To continue without completing additional verification, your business can use WhatsApp Business platform actively for several days and follow our messaging policies.``Based on your activity, limits cannot be increased for your business. Contact support for more information.``Limits cannot be increased for your business <BUSINESS_PORTFOLIO_NAME>. Use WhatsApp Business platform actively for several days and follow our messaging policies.``Limits cannot be increased at this time for your business <BUSINESS_PORTFOLIO_NAME>. Limits cannot be increased as your identity verification submission was rejected. To continue without additional verification, use WhatsApp Business platform actively for several days and follow our messaging policies.``Please reupload your profile picture``This phone number now has a green badge next to its name showing that it's an authentic and notable business account. Add more details to your business profile to increase customer trust.``We do not grant official business accounts to individuals. Your display name must be directly associated with your business. Edit the display name and submit a new request.``Your messaging quality was too low to unlock more capabilities at this time. Alternatively, your business can unlock more capabilities by submitting business documents to verify your business.` | `Limits cannot be increased for your business <BUSINESS_PORTFOLIO_NAME>. Use WhatsApp Business platform actively for several days and follow our messaging policies.` |
| `<ALERT_SEVERITY>`<br>*String* | Alert severity. Values can be:<br>`CRITICAL` — Indicates a rejection or denial. The `alert_description` value may describe actions that can be taken to resolve the underlying reason for the rejection or denial.<br>`INFORMATIONAL` — Indicates webhook contain only informational data and no action is needed.<br>`WARNING` — Indicates action may be needed. The `alert_description` value describes possible actions that can be taken. | `WARNING` |
| `<ALERT_STATUS>` | Alert status.<br>Values can be:<br>`ACTIVE``NONE` | `ACTIVE` |
| `<ALERT_TYPE>`<br>*String* | Alert type.<br>Values can be:<br>`INCREASED_CAPABILITIES_ELIGIBILITY_DEFERRED` — Indicates we don’t have enough message signal to make a determination, identity verification was rejected, or your message quality is too low. Possible solutions are to increase your [messaging limit](https://developers.facebook.com/documentation/business-messaging/whatsapp/messaging-limits) or get your [business verified](https://www.facebook.com/business/help/2058515294227817).<br>`INCREASED_CAPABILITIES_ELIGIBILITY_FAILED` — Indicates messaging limits cannot be increased due to past messaging activity. Possible solutions are to [request an increase](https://developers.facebook.com/documentation/business-messaging/whatsapp/messaging-limits#request-an-increase) or get your [business verified](https://www.facebook.com/business/help/2058515294227817).<br>`INCREASED_CAPABILITIES_ELIGIBILITY_NEED_MORE_INFO` — Indicates messaging limits cannot be increased due to past messaging activity. Possible solutions are to [verify your identity](https://www.facebook.com/business/help/587323819101032) or increase your [messaging limit](https://developers.facebook.com/documentation/business-messaging/whatsapp/messaging-limits).<br>`OBA_APPROVED` — Indicates Official Business Account status approved.<br>`OBA_REJECTED` — Indicates Official Business Account (“OBA”) status denied. Review OBA [criteria](https://developers.facebook.com/documentation/business-messaging/whatsapp/whatsapp-business-accounts#criteria) and edit your [display name](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers#display-names) after reviewing our display name guidelines.<br>`PROFILE_PICTURE_LOST` — Indicates the business phone number’s business profile photo has been deleted. Upload a new photo using [WhatsApp Manager](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers#viewing-or-updating-your-profile-via-whatsapp-manager) or the [API](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers#updating-your-profile-via-api). | `INCREASED_CAPABILITIES_ELIGIBILITY_DEFERRED` |
| `<ENTITY_ID>`<br>*String* | Entity ID. Value can be a business portfolio ID or business phone number ID. | `506914307656634` |
| `<ENTITY_TYPE>`<br>*String* | Entity type. Values can be:<br>`BUSINESS` — Indicates a change associated with a business portfolio.<br>`PHONE_NUMBER` — Indicates a change associated with a business phone number.<br>`CURRENT_STATUS_ID` — Indicates a change associated with a business phone number’s [business profile](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers#business-profiles). | `BUSINESS` |
| `<WEBHOOK_TRIGGER_TIMESTAMP>`<br>*Integer* | Unix timestamp indicating when the webhook was triggered. | `1739321024` |
| `<WHATSAPP_BUSINESS_ACCOUNT_ID>`<br>*String* | WhatsApp Business Account ID. | `102290129340398` |

## Example

```json
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "102290129340398",
      "time": 1745612159,
      "changes": [
        {
          "field": "account_alerts",
          "value": {
            "entity_type": "BUSINESS",
            "entity_id": "506914307656634",
            "alert_info": {
              "alert_severity": "WARNING",
              "alert_status": "ACTIVE",
              "alert_type": "INCREASED_CAPABILITIES_ELIGIBILITY_DEFERRED",
              "alert_description": "Limits cannot be increased for your business <BUSINESS_PORTFOLIO_NAME>. Use WhatsApp Business platform actively for several days and follow our messaging policies."
            }
          }
        }
      ]
    }
  ]
}
```
