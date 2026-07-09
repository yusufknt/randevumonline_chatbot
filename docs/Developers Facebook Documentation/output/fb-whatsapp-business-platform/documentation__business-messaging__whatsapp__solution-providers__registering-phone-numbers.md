# Registering business phone numbers | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/registering-phone-numbers_

---

# Registering business phone numbers

Updated: Nov 14, 2025

This document describes the steps to programmatically register business phone numbers on WhatsApp Business Accounts (WABA).

Note that **Embedded Signup performs steps 1-3 automatically** (unless you are [bypassing the phone number addition screen](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/bypass-phone-addition)) so you only need to perform step 4 when a business customer completes the flow. If you have disabled phone number selection, however, you must perform all 4 steps.

Registering business phone numbers is a four step process:

1. Create the number on a WABA.
2. Get a verification code for that number.
3. Use the code to verify the number.
4. Register the verified number for API use.

These steps are described below.

You can also perform all 4 steps repeatedly to register business phone numbers in bulk.

## Limitations

Business phone numbers must meet our [phone number requirements](https://developers.facebook.com/docs/whatsapp/phone-numbers#requirements).

## Step 1: Create the phone number

Use the [Phone Numbers API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/phone-number-management-api#post-version-waba-id-phone-numbers) to create a business phone number on a WABA.

### Request syntax

```https
POST /<WHATSAPP_BUSINESS_ACCOUNT_ID>/phone_numbers
```

### Post body

```json
{
  "cc": "<CC>",
  "phone_number": "<PHONE_NUMBER>",
  "verified_name": "<VERIFIED_NAME>"
}
```

### Body properties

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<CC>`<br>*String* | **Required**.<br>The phone number’s country calling code. | `1` |
| `<PHONE_NUMBER>`<br>*String* | **Required.**<br>The phone number, with or without the country calling code. | `15551234` |
| `<VERIFIED_NAME>`<br>*String* | **Required.**<br>The phone number’s [display name](https://www.facebook.com/business/help/338047025165344). | `Lucky Shrub` |

### Response

Upon success, the API returns a business phone number ID. Capture this ID for use in the next step.

```json
{
  "id": "<ID>"
}
```

### Response properties

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<ID>` | An unverified [WhatsApp Business Phone Number](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/whatsapp-business-account-phone-number-api) ID. | `106540352242922` |

### Example request

```curl
curl 'https://graph.facebook.com/v25.0/102290129340398/phone_numbers' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAH7...' \
-d '{
    "cc": "1",
    "phone_number": "14195551518",
    "verified_name": "Lucky Shrub"
}'
```

### Example Response

```json
{
  "id": "110200345501442"
}
```

## Step 2: Request a verification code

Use the [Request Code API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-pre-verified-phone-number/request-verification-code-api#post-version-pre-verified-phone-number-id-request-code) to have a verification code sent to the business phone number.

### Request syntax

```https
POST /<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>/request_code
  ?code_method=<CODE_METHOD>
  &language=<LANGUAGE>
```

### Query string parameters

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<CODE_METHOD>` | **Required.**<br>Indicates how you want the verification code delivered to the business phone number. Values can be `SMS` or `VOICE`. | `SMS` |
| `<LANGUAGE>` | **Required.**<br>Indicates language used in delivered verification code. | `en_US` |

### Response

```json
{
  "success": <SUCCESS>
}
```

### Response properties

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<SUCCESS>` | Boolean indicating success or failure.<br>Upon success, the API will respond with `true` and a verification code will be sent to the business phone number using the method specified in your request. | `true` |

### Example request

```curl
curl -X POST 'https://graph.facebook.com/v25.0/110200345501442/request_code?code_method=SMS&language=en_US' \
-H 'Authorization: Bearer EAAJB...'
```

### Example response

```json
{
  "success": true
}
```

### Example SMS delivery

Example of an SMS message in English containing a verification code, delivered to a business phone number:

```json
WhatsApp code 123-830
```

## Step 3: Verify the number

Use the [Verify Code API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/verify-code-api#post-version-phone-number-id-verify-code) to verify the business phone number, using the verification code contained in the SMS or voice message delivered to the number.

### Request syntax

```https
POST /<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>/verify_code
  ?code=<CODE>
```

### Query string parameters

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<CODE>`<br>*String* | **Required.**<br>Verification code, without the hyphen. | `123830` |

### Response

```json
{
  "success": <SUCCESS>
}
```

### Response properties

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<SUCCESS>` | Boolean indicating success or failure.<br>Upon success, the API will respond with `true`, indicating that the business phone number has been verified. | `true` |

### Example request

```curl
curl -X POST 'https://graph.facebook.com/v25.0/110200345501442/verify_code?code=123830' \
-H 'Authorization: Bearer EAAJB...'
```

### Example response

```json
{
  "success": true
}
```

## Step 4: Register the number

Use the [Register API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/register-api#post-version-phone-number-id-register) to register the business phone number for use with the API.

### Request syntax

```https
POST /<BUSINESS_PHONE_NUMBER_ID>/register
```

### Post body

```json
{
  "messaging_product": "whatsapp",
  "pin": "<PIN>"
}
```

### Body properties

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<PIN>`<br>*String* | **Required.**<br>If the verified business phone number already has two-step verification enabled, set this value to the number’s 6-digit two-step verification PIN. If you do not recall the PIN, you can [update](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/two-step-verification#updating-verification-code) it.<br>If the verified business phone number does not have two-step verification enabled, set this value to a 6-digit number. This will be the business phone number’s two-step verification PIN. | `123456` |

### Response

Upon success, the API will respond with `true`, indicating successful registration.

```json
{
  "success": <SUCCESS>
}
```

### Response properties

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<SUCCESS>` | Boolean indicating success or failure.<br>Upon success, the API will respond with `true`, indicating successful registration. | `true` |

### Example request

```curl
curl 'https://graph.facebook.com/v25.0/110200345501442/register' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "messaging_product": "whatsapp",
  "pin": "123456"
}'
```

### Example response

```json
{
  "success": true
}
```
