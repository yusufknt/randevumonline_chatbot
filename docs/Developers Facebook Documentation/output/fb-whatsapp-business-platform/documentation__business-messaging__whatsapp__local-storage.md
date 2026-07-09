# Local Storage | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/local-storage_

---

# Local Storage

Updated: Mar 31, 2026

Local storage offers an additional layer of data management control, by giving you the option to specify where your message data is stored at rest. If your company is in a regulated industry such as finance, government, or healthcare, you may prefer to have your message data stored in a specific country when at rest because of regulatory or company policies.

## How local storage works

Local storage is controlled by a setting enabled or disabled at a WhatsApp business phone number level. Both Cloud API and Marketing Messages API for WhatsApp support local storage, and the setting will apply to any messages sent via either API if enabled.

When Local storage is enabled, the following constraints are applied to message content for a business phone number:

- **Data-in-use:** When message content is sent or received by Cloud API or Marketing Messages API for WhatsApp, message content may be stored on Meta data centers internationally while being processed. The data-in-use period differs between Cloud API and Marketing Messages API for WhatsApp: When using Local Storage for Cloud API, the data-in-use period is up to 60 minutes.When using Local Storage for Marketing Messages API for WhatsApp, the data-in-use period is up to 90 minutes.
- **Data-at-rest:** After the data-in-use period, message content is deleted from Meta data centers outside of the specified local storage region, and persisted only in data centers within the local storage region selected.

The local storage feature supplements other [WhatsApp Business Platform privacy and security controls](https://l.facebook.com/l.php?u=https%3A%2F%2Fbusiness.whatsapp.com%2Ftrust-and-safety%3Ffbclid%3DIwZXh0bgNhZW0CMTEAYnJpZBExNkRZWTlJbDFSMDBUVlRLZwEe2Qq3X5Y-XnlgB832KjRawCRQOBQGgvzV0IgHxrk5kplGc2LAfA7cvutA9ms_aem_HXrl5zwbIRR1MUiy5tf6Cw&h=AT3UHqLwYU7Bb-85xI2Dn-oTHoESdchy9on_IJHUZQ0uMM-cfAnEQKDGbd1L_ao2QGEk9P27-17YpYYjERTwECJ8QSWxw6DeaOIWhJyblTChWN1teIo2QqHpzUZFtuBrlFEGu5gz5J4), and allows customers to ensure a higher level of compliance with local data protection regulations.

## Data in scope

Local storage applies to message content (text and media) sent and/or received via Cloud API and Marketing Messages API for WhatsApp. The following message content are in scope of the local storage feature:

- Text messages: text payload (message body)
- Media messages: media payload (audio, document, image or video)
- Template messages (static template + parameters passed at message send time): components with text / media payload

In addition, a limited set of metadata attributes is included with the locally stored message content, in order to correctly associate the encrypted message payload with the originally processed message, and to audit the fact of localization. The stored metadata is protected with tokenization and encryption.

## Phone number storage via contact information requests

If your business has enabled the contact book feature and a WhatsApp user shares their contact information by tapping the share contact information button, Meta extracts the user’s phone number from the shared contact card (vCard) and stores it in your contact book. The contact book is hosted on Meta data centers, regardless of your Local Storage configuration. Only the phone number is extracted and stored; no other vCard data is retained on Meta data centers beyond the standard data-in-use period. [Contact book retention policies](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-scoped-user-ids#contact-book) apply to this data and you can [turn off this feature](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-scoped-user-ids#contact-book).

## Available Regions

To see what regions are supported by local storage, see the `data_localization_region` parameter in the [documentation on phone number registration](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/registration#register).

## Limitations

- Media files uploaded by a business phone number with local storage enabled are only accessible to that specific phone number, and cannot be shared with other phone numbers associated with the business.
- If your business has the contact book feature enabled, phone numbers shared via the share contact information button are extracted from the vCard and stored in your contact book on Meta data centers, regardless of your Local Storage configuration. See [Phone number storage via contact information requests](https://developers.facebook.com/documentation/business-messaging/whatsapp/local-storage#phone-number-storage-via-contact-information-requests) for details.

## Enabling Local Storage

Follow the steps below to enable local storage for an unregistered business phone number using API version 21.0 or newer. If you are using an older API version, see [Enabling Local Storage (v20 and older)](https://developers.facebook.com/documentation/business-messaging/whatsapp/local-storage#enabling-local-storage--v20-and-older-).

### Step 1: Enable local storage on the number

Local storage can only be enabled or disabled on WhatsApp business phone numbers when they are in an unregistered state. If a phone number is currently registered, it must be unregistered and re-registered with local storage enabled.

Use the [**Settings API**](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/settings-api#post-version-phone-number-id-settings) to enable local storage on the unregistered business phone number:

Request Syntax

```https
POST /<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>/settings

{
  "storage_configuration": {
    "status": "IN_COUNTRY_STORAGE_ENABLED",
    "data_localization_region": "<COUNTRY_CODE>"
  }
}
```

Set `<COUNTRY_CODE>` to the [country code](https://developers.facebook.com/documentation/business-messaging/whatsapp/local-storage#available-regions) of the country where data-at-rest should be stored.

Response Syntax

```json
{
  "success": <SUCCESS>
}
```

Upon success, `<SUCCESS>` will be set to `true`.

Example Request

```curl
curl 'https://graph.facebook.com/v25.0/106540352242922/settings' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "storage_configuration": {
    "status": "IN_COUNTRY_STORAGE_ENABLED",
    "data_localization_region": "BR"
  }
}'
```

Example Response

```json
{
  "success": true
}
```

### Step 2: Register the number

Use the [**Register API**](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/register-api#post-version-phone-number-id-register) to register the business phone number.

Request Syntax

```https
POST /<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>/register

{
  "messaging_product": "whatsapp",
  "pin": "<TWO_STEP_PIN>"
}
```

Set `<TWO_STEP_PIN>` to the desired two-step verification PIN for the business phone number.

Response Syntax

```json
{
  "success": <SUCCESS>
}
```

Upon success, `<SUCCESS>` will be set to `true`.

Example Request

```curl
curl 'https://graph.facebook.com/v25.0/register' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "messaging_product": "whatsapp",
  "pin": "123456"
}'
```

Example Response

```json
{
  "success": true
}
```

## Getting Local Storage Settings

Use the [**Settings API**](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/settings-api#get-version-phone-number-id-settings) to get local storage settings on a WhatsApp business phone number. For example:

```curl
curl 'https://graph.facebook.com/v25.0/179776755229976/settings' \
-H 'Authorization: Bearer EAAJB...'
```

This returns a [node that represents the local storage settings](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/settings-api) on the business phone number. For example:

```json
{
  "storage_configuration": {
    "status": "IN_COUNTRY_STORAGE_ENABLED",
    "data_localization_region": "BR"
  }
}
```

## Disabling Local Storage

Use the [**Settings API**](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/settings-api#post-version-phone-number-id-settings) to disable local storage on an unregistered business phone number using API version 21.0 or newer. If you are using an older API version, see [Disabling Local Storage (v20 and older)](https://developers.facebook.com/documentation/business-messaging/whatsapp/local-storage#disabling-local-storage-using-v20-and-older).

Request Syntax

```https
POST /<WHATSAPP_BUSINESS_PHONE_NUMBER_ID/>settings

{
  "storage_configuration": {
    "status": "IN_COUNTRY_STORAGE_DISABLED"
  }
}
```

Set `<COUNTRY_CODE>` to the [country code](https://developers.facebook.com/documentation/business-messaging/whatsapp/local-storage#available-regions) of the country where data-at-rest should be stored.

Response Syntax

```json
{
  "success": <SUCCESS>
}
```

Upon success, `<SUCCESS>` will be set to `true`.

Example Request

```curl
curl 'https://graph.facebook.com/v25.0/106540352242922/settings' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "storage_configuration": {
    "status": "IN_COUNTRY_STORAGE_DISABLED"
  }
}'
```

Example Response

```json
{
  "success": true
}
```

## Enabling Local Storage using v20 and older

To enable local storage for an unregistered business phone number using API version 20.0 or older:

### Step 1: Check verification status

Use the [**WhatsApp Business Phone Number API**](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/whatsapp-business-account-phone-number-api#get-version-phone-number-id) and request the `code_verification_status` field. If the code verification status is `VERIFIED`, skip to step 4. Otherwise, proceed to step 2.

### Step 2: Request a verification code

Use the [**Request Verification Code API**](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-pre-verified-phone-number/request-verification-code-api#post-version-pre-verified-phone-number-id-request-code) to request a verification code. Upon success, the API will respond with `true` and a verification code will be sent to the business phone number via the method specified in the `code_method` parameter.

For example, this query requests a verification code to be sent via SMS in the English language (US locale).

```curl
curl -X POST 'https://graph.facebook.com/v20.0/110200345501442/request_code?code_method=SMS&language=en_US' \
-H 'Authorization: Bearer EAAJB...'
```

Use the code in the delivered message in the next step.

### Step 3: Verify the business phone number

Use the [**Verify Code API**](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/verify-code-api#post-version-phone-number-id-verify-code) to verify the business phone number using the verification code included in the message you received from the previous step.

For example:

```curl
curl -X POST 'https://graph.facebook.com/v20.0/110200345501442/verify_code?code=123830' \
-H 'Authorization: Bearer EAAJB...'
```

### Step 4: Reregister the business phone number

Use the [**Register API**](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/register-api#post-version-phone-number-id-register) to register the business phone number. Indicate the country where data-at-rest should be stored using the `data_localization_region` parameter.

For example, this request enables local storage on a business phone number, and sets the country where data should be stored to India:

```curl
curl 'https://graph.facebook.com/v20.0/110200345501442/register' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "messaging_product": "whatsapp",
  "pin": "123456",
  "data_localization_region": "IN"
}'
```

## Disabling local storage using v20 and older

Use the [**Deregister API**](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/phone-number-deregister-api#post-version-phone-number-id-deregister) to disable local storage on a business phone number using API version 20.0 or older.

For example:

```curl
curl -X POST 'https://graph.facebook.com/v25.0/110200345501442/deregister' \
-H 'Authorization: Bearer EAAJB...'
```

Note that this deregisters the business phone number so it cannot be used with WhatsApp Cloud API. If you want to continue using it with Cloud API but without local storage enabled, you must reregister it without including the `data_localization_region` parameter.

## FAQs

**Q. What are the migration paths for moving a phone number to the Cloud API version with Local Storage?**

We support all migration paths to Cloud API version with Local Storage, this includes:

- Existing Cloud API number migrating to Cloud API version with Local Storage
- New Cloud API number enabling Local Storage

In all these scenarios, use the [Register API](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/registration#register) to register the selected phone number, specifying the target country for data localization in the `data_localization_region` parameter.

**Q. Are there any migration risks? Any downtime associated with this?**

No migration risks. Downtime is typically less than 5 minutes and no re-verification of the business phone number is required.

**Q. Is there any downtime associated with enabling local storage for a business phone number?**

If a business phone number is already registered, you will need to de-register and re-register the phone number with local storage enabled. This process typically takes less than 5 minutes. No re-verification of the business phone number is required during this process.
