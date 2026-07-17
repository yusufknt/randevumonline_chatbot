# Register a Business Phone Number | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/registration_

---

# Register a Business Phone Number

Updated: Mar 31, 2026

To use your business phone number with Cloud API you must register it. Registration can only be done via API — you cannot register a number through [WhatsApp Manager](https://business.facebook.com) (WAM) or the App Dashboard.

To get your number ready for Cloud API, complete the following steps:

1. **Add** your business phone number to your WhatsApp Business account using [WhatsApp Manager](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers#add) .
2. **Verify** ownership of the number using [WhatsApp Manager](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers#verify) .
3. **Register** your business phone number by making an API call to the [registration endpoint](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/registration#register) below.

Register your business phone number in the following scenarios:

- **Account creation** — When you implement this API, register the business phone number you want to use. Meta enforces two-step verification during account creation to add an extra layer of security to your accounts.
- **Name change** — If your phone is already registered and you want to change its display name, you can update it via [WhatsApp Manager](https://www.facebook.com/business/help/378834799515077) or [via API](https://developers.facebook.com/documentation/business-messaging/whatsapp/display-names#updating-display-name-via-api) . Once the name change is approved (confirmed via the [phone_number_name_update](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/phone_number_name_update) webhook), re-register your phone number using the endpoint below. Wait for approval before re-registering, as re-registering before approval has no effect. See [Display names](https://developers.facebook.com/documentation/business-messaging/whatsapp/display-names#re-registering-after-display-name-approval) for the complete workflow.

### Migration exception

If you are migrating a phone number from the On-Premises API to the Cloud API, there are extra steps you need to perform before registering a phone number with the Cloud API. See [Migrate From On-Premises API to Cloud API](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/migrating-from-onprem-to-cloud) for the full process.

## Register a business phone number

To register your verified business phone number, make a `POST` call to `PHONE_NUMBER_ID/register`. Include the parameters listed below.

| Endpoint | Authentication |
| --- | --- |
| `PHONE_NUMBER_ID/register`<br>(See [Get Phone Number ID](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers#get-all-phone-numbers)) | Solution Partners must authenticate themselves with an access token with the `whatsapp_business_management` and `whatsapp_business_messaging` permissions. |

### Limitations

Requests to the registration endpoint are limited to 10 requests per business number in a 72-hour moving window.

When you make a registration request, the API checks how many registration requests you have made to register that number in the last 72 hours. If you have already made 10 requests, the API will return error code `133016`, and the number will be prevented from being registered for the next 72 hours.

### Parameters

| Name | Description |
| --- | --- |
| `messaging_product` | **Required.**<br>Messaging service used. Set this to `"whatsapp"`. |
| `pin` | **Required.**<br>If your verified business phone number already has two-step verification enabled, set this value to your number’s 6-digit two-step verification PIN. If you cannot recall your PIN, you can change it. See [Two-step verification](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers#two-step-verification).<br>If your verified business phone number does not have two-step verification enabled, set this value to a 6-digit number. This will be the newly verified business phone number’s two-step verification PIN. |
| `data_localization_region` | **Optional.**<br>If included, enables [local storage](https://developers.facebook.com/documentation/business-messaging/whatsapp/local-storage) on the business phone number. Value must be a 2-letter ISO 3166 country code (for example, `IN`) indicating the country where you want data-at-rest to be stored.<br>Supported values:<br>**APAC**<br>Australia: `AU`Indonesia: `ID`India: `IN`Japan: `JP`Singapore: `SG`South Korea: `KR`<br>**Europe**<br>EU (Germany): `DE`Switzerland: `CH`United Kingdom: `GB`<br>**LATAM**<br>Brazil: `BR`<br>**MEA**<br>Bahrain: `BH`South Africa: `ZA`United Arab Emirates: `AE`<br>**NORAM**<br>Canada: `CA`<br>Once you enable local storage, you cannot disable or change it directly. Instead, you must [deregister](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/registration#deregister) the number and register it again without this parameter (to disable), or include the parameter with the new country code (to change).<br>If the number is already registered, deregister it, then register it again with this parameter to enable local storage. |

### Example request without local storage

```curl
curl 'https://graph.facebook.com/v25.0/106540352242922/register ' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "messaging_product": "whatsapp",
  "pin": "212834"
}
```

### Example request with local storage

```curl
curl 'https://graph.facebook.com/v25.0/106540352242922/register ' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "messaging_product": "whatsapp",
  "pin": "212834",
  "data_localization_region": "CH"
}
```

All API calls require authentication with access tokens.

Developers can authenticate their API calls with the access token generated in the App Dashboard > WhatsApp > API Setup.

Solution Partners must authenticate themselves with an access token with the `whatsapp_business_messaging` and `whatsapp_business_management` permissions. See [System User Access Tokens](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens) for information.

## Deregister a business phone number

Deregistering a business phone number makes it unusable with Cloud API and disables [local storage](https://developers.facebook.com/documentation/business-messaging/whatsapp/local-storage) on the number, if it had been enabled. To use the number again, you must re-register it.

To deregister a business phone number, make a `POST` call to `PHONE_NUMBER_ID/deregister`:

| Endpoint | Authentication |
| --- | --- |
| `PHONE_NUMBER_ID/deregister`<br>(See [Get Phone Number ID](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers#get-all-phone-numbers)) | Solution Partners must authenticate themselves with an access token with the `whatsapp_business_management` and `whatsapp_business_messaging` permissions. |

### Limitations

- This endpoint cannot be used to deregister a business phone number that is in use with [both Cloud API and the WhatsApp Business app](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users) .
- Deregistration does not delete a number or its message history. To delete a number and its history, see [Delete Phone Number from a WABA](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers#deleting-business-phone-numbers) .
- Requests to the deregistration endpoint are limited to 10 requests per business number in a 72-hour moving window. If you exceed this amount, the API will return error code `133016` , and the business phone number will be prevented from being deregistered for the next 72 hours.

### Example

Sample Request:

```curl
curl -X POST \
 'https://graph.facebook.com/v25.0/FROM_PHONE_NUMBER_ID/deregister' \
 -H 'Authorization: Bearer ACCESS_TOKEN'
```

A successful response looks like:

```json
{
  "success": true
}
```

## See also

- [Resetting your PIN](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers#changing-your-pin-via-whatsapp-manager)
- [Cloud API Local Storage](https://developers.facebook.com/documentation/business-messaging/whatsapp/local-storage)
