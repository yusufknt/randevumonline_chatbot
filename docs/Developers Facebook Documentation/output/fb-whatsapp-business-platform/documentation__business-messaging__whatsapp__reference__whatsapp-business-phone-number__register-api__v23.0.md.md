# WhatsApp Cloud API - Register API

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/register-api/v23.0.md_

---

```
## Base URL

| URL | Description |
|-----|-------------|
| https://graph.facebook.com |  |

## APIs

| Method | Endpoint |
|--------|----------|
| POST | [/{Version}/{Phone-Number-ID}/deregister](#post-version-phone-number-id-deregister) |
| POST | [/{Version}/{Phone-Number-ID}/register](#post-version-phone-number-id-register) |

<jumplink id="post-version-phone-number-id-deregister"></jumplink>
## POST /{Version}/{Phone-Number-ID}/deregister

Deregister Phone

To deregister your phone, make a **POST** call to **`{{Phone-Number-ID}}/deregister`**. **Deregister Phone** removes a previously registered phone. You can always re-register your phone using by repeating the registration process.

#### Response

A successful response returns:

``` json
{
    "success": true
}

```

### Request Body (Optional)

**Content Type**: `text/plain`

### Responses

**200**

Successfully deregistered the specified phone number.

<jumplink id="post-version-phone-number-id-register"></jumplink>
## POST /{Version}/{Phone-Number-ID}/register

Register Phone Number

With your phone number’s ID in hand, you can register it. In the registration API call, you perform two actions at the same time:\n\n1.  Register the phone.\n2.  Enable [two-step verification](https://faq.whatsapp.com/general/verification/about-two-step-verification) by setting a 6-digit registration code — you must set this code on your end. Save and memorize this code as it can be requested later. **Setting up two-factor authentication is a requirement to use the Cloud API.**\n    \n\n**Embedded Signup Users**\n\nA phone number **must** be registered within 14 days after going through the Embedded Signup flow. If the phone number is not registered during that window, the phone number must go through the Embedded Signup flow again prior to registration.

### Request Body (Optional)

**Content Type**: `application/json`

**Schema**: object

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| backup | [Backup](#object-backup-1) |  |  |
| messaging_product | string |  |  |
| pin | string |  |  |

### Responses

**200**

Register Phone Number / Register Phone / Migrate Account

**Content Type**: `application/json`

**Schema**: object

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| success | Must be any of: string, boolean, string |  |  |

# Components

## Inline Object Definitions

<jumplink id="object-backup-1"></jumplink>
### Backup

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| data | string |  |  |
| password | string |  |  |
```
