# Two-Step Verification | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/two-step-verification_

---

# Two-Step Verification

Updated: Nov 5, 2025

Set up two-step verification for your phone number to add an extra layer of security to your business accounts. Use the [WhatsApp Business Phone Number API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/whatsapp-business-account-phone-number-api#post-version-phone-number-id) to set it up with the parameters below. There is no endpoint to disable two-step verification.

| Endpoint | Authentication |
| --- | --- |
| `/PHONE_NUMBER_ID`<br>(See [Get Phone Number ID](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers#get-all-phone-numbers)) | Solution Partners must authenticate themselves with an access token with the `whatsapp_business_management` and `whatsapp_business_messaging` permissions. |

### Parameters

| Name | Description |
| --- | --- |
| `pin` | **Required.**<br>A 6-digit PIN you wish to use for two-step verification. |

### Example

Sample request:

```curl
curl -X  POST \
 'https://graph.facebook.com/v25.0/FROM_PHONE_NUMBER_ID' \
 -H 'Authorization: Bearer ACCESS_TOKEN' \
 -H 'Content-Type: application/json' \
 -d '{"pin" : "6_DIGIT_PIN"}'
```

Sample response:

```json
{
  "success": true
}
```

All API calls require authentication with access tokens.

Developers can authenticate their API calls with the access token generated in the App Dashboard > WhatsApp > API Setup.

Solution Partners must authenticate themselves with an access token with the `whatsapp_business_messaging` and `whatsapp_business_management` permissions. See [System User Access Tokens](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens) for information.

## Reset your PIN

If you forget or misplace your PIN, you can update it by following these steps in WhatsApp Manager:

1. Go to [settings](https://business.facebook.com/settings/) and log into your Facebook Business. Click the business you use to manage your WABA (WhatsApp Business Account).
2. In the settings screen, click **WhatsApp Accounts** . Find the WABA you want to update. Click the WABA. A panel with its info displays.
3. In the WABA info panel, click **Settings** .
4. In the new tab, click **WhatsApp Manager** .
5. In WhatsApp Manager, find your phone number and click **Settings** .
6. Click **Two-step verification** .
7. In the Two-step verification tab, click **Change PIN** .
8. Enter a new PIN and confirm it to complete the update.
