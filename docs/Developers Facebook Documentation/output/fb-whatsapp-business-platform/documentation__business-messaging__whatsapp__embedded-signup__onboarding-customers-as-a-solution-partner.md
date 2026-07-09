# Onboarding business customers as a Solution Partner

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-customers-as-a-solution-partner_

---

# Onboarding business customers as a Solution Partner

Updated: Nov 14, 2025

This document describes the steps Solution Partners must perform to onboard new business customers who have completed the Embedded Signup flow.

If you are a Solution Partner, any business customer who completes your implementation of the Embedded Signup flow will not be able to use your app to access their WhatsApp assets or send and receive messages until you complete these steps.

## What you will need

- the business customer’s WABA ID (returned via [session logging](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/implementation#session-logging-message-event-listener) or [API request](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/manage-accounts#get-shared-waba-id-with-access-token) )
- the business customer’s business phone number ID (returned via [session logging](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/implementation#session-logging-message-event-listener) or [API request](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/manage-phone-numbers#getting-phone-numbers) )
- your app ID (displayed at the top of the **App Dashboard** )
- your app secret (displayed in the **App Dashboard** > **App settings** > **Basic** panel)
- your credit line ID (displayed in **Business Manager** > **Business Settings** > **Business Info** or returned via [API request](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/share-and-revoke-credit-lines#get-your-credit-line-id) )
- your [system user access token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens) (“system token”)

Also, if you wish to test messaging capabilities using the customer’s business phone number, you will need a WhatsApp phone number that can already send and receive messages from other WhatsApp numbers.

Perform all of the requests described below using server-to-server requests. Do not use client-side requests.

## Step 1: Exchange the token code for a business token

Use the **Access Token API** to exchange the token code [returned](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/implementation#response-callback) by Embedded Signup for a business integration system user access token (“business token”).

### Request

```html
curl --get 'https://graph.facebook.com/v21.0/oauth/access_token' \
-d 'client_id=<APP_ID>' \
-d 'client_secret=<APP_SECRET>' \
-d 'code=<CODE>'
```

### Request parameters

| Placeholder | Description | Example value |
| --- | --- | --- |
| `<APP_ID>` | **Required.**<br>Your app ID. This is displayed at the top of the **App Dashboard**. | `236484624622562` |
| `<APP_SECRET>` | **Required.**<br>Your app secret. You can get this from the **App Dashboard** > **App Secret** > **Basic** panel. | `614fc2afde15eee07a26b2fe3eaee9b9` |
| `<CODE>` | **Required.**<br>The code [returned by Embedded Signup](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/implementation#response-callback) when the customer successfully completed the flow. | `AQBhlXsctMxJYbwbrpybxlo9tLPGy-QAmjBJA03jxLos43wxlBlrYozY5C33BXJULd133cOJf_5y6EkJZYMrAmW-EMj3Wdap9-NUM2nS4s8tC-ES7slBhh6QpCFM7-SzpI-iqsjqTGyxbUUW3AeaEyLkeZFIkBgcQ_SOxo9HShm20SDR5_n7AT9ZJ5dcgpqBQykNT-pQ8V7Ne9-sr6RLAWtJMF7-Zx6ABudRcWIN53tUTtquDVNuq3lrco4BlVQAv-54tR83Ae0ODN9Uet6j-BVLuetXhQCM3sz9RdgedlbxkidMbkztvYX1j7baOrJxyLyYGWYgbnUrKRQKCtWTsO5ekIGFgtbpS8UPJNqV6j8E5XKPJ8QA7ZFqzkB0s2O__J5FrjHzc_rDo1EuRbw98ihHDzQnvuXeHapEyfhLDJct0A` |

### Response

Upon success:

```html
<BUSINESS_TOKEN>
```

### Response parameters

| Placeholder | Description | Example value |
| --- | --- | --- |
| `<BUSINESS_TOKEN>` | The customer’s [business token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens). | `EAAAN6tcBzAUBOwtDtTfmZCJ9n3FHpSDcDTH86ekf89XnnMZAtaitMUysPDE7LES3CXkA4MmbKCghdQeU1boHr0QZA05SShiILcoUy7ZAb2GE7hrUEpYHKLDuP2sYZCURkZCHGEvEGjScGLHzC4KDm8tq2slt4BsOQE1HHX8DzHahdT51MRDqBw0YaeZByrVFZkVAoVTxXUtuKgDDdrmJQXMnI4jqJYetsZCP1efj5ygGscZBm4OvvuCYB039ZAFlyNn` |

## Step 2: Subscribe to webhooks on the customer’s WABA

Use the [POST /<WABA_ID>/subscribed_apps](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/subscribed-apps-api#post-version-waba-id-subscribed-apps) endpoint to subscribe your app to webhooks on the business customer’s WABA. If you want the customer’s webhooks to be sent to a different callback URL than the one set on your app, you have multiple [webhook override](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/override) options.

### Request

```html
curl -X POST 'https://graph.facebook.com/<API_VERSION>/<WABA_ID>/subscribed_apps' \
-H 'Authorization: Bearer <ACCESS_TOKEN>'
```

### Request parameters

| Placeholder | Description | Example value |
| --- | --- | --- |
| `<BUSINESS_TOKEN>` | **Required.**<br>The customer’s [business token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens). | `EAAAN6tcBzAUBOwtDtTfmZCJ9n3FHpSDcDTH86ekf89XnnMZAtaitMUysPDE7LES3CXkA4MmbKCghdQeU1boHr0QZA05SShiILcoUy7ZAb2GE7hrUEpYHKLDuP2sYZCURkZCHGEvEGjScGLHzC4KDm8tq2slt4BsOQE1HHX8DzHahdT51MRDqBw0YaeZByrVFZkVAoVTxXUtuKgDDdrmJQXMnI4jqJYetsZCP1efj5ygGscZBm4OvvuCYB039ZAFlyNn` |
| `<WABA_ID>` | **Required.**<br>The customer’s WABA ID. | `102290129340398` |

### Response

Upon success:

```json
{
  "success": true
}
```

## Step 3: Share your credit line with the customer

We are currently testing new steps for sharing your credit line with onboarded business customers. These steps will eventually replace this step, so if you wish to implement these steps now, see [Alternate method for sharing your credit line](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/share-and-revoke-credit-lines#alternate-method-for-sharing-your-credit-line).

**Note**: If you are using the below API i.e. `whatsapp_credit_sharing_and_attach`, you would need to add your System User to the shared WhatsApp Business Accounts as a pre-requisite. Please refer to [this doc for steps](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/manage-system-users).

Once you have added the System user to the WhatsApp Business Account, use the [Credit Sharing API](https://developers.facebook.com/docs/marketing-api/reference/extended-credit/whatsapp_credit_sharing_and_attach#Creating) to share your credit line with an onboarded business customer.

### Request

```html
curl -X POST 'https://graph.facebook.com/<API_VERSION>/<EXTENDED_CREDIT_LINE_ID>/whatsapp_credit_sharing_and_attach?waba_currency=<CUSTOMER_BUSINESS_CURRENCY>&waba_id=<CUSTOMER_WABA_ID>' \
-H 'Authorization: Bearer <SYSTEM_TOKEN>'
```

### Request parameters

| Placeholder | Description | Example value |
| --- | --- | --- |
| `<CUSTOMER_BUSINESS_CURRENCY>` | **Required.**<br>The business’s currency, as a three-letter currency code. Support values are:<br>`AUD``EUR``GBP``IDR``INR``USD`<br>This currency is used for invoicing and corresponds to [pricing](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing) rates. | `USD` |
| `<CUSTOMER_WABA_ID>` | **Required.**<br>The customer’s WABA ID. | `102290129340398` |
| `<EXTENDED_CREDIT_LINE_ID>` | **Required.**<br>Your extended credit line ID. | `1972385232742146` |
| `<SYSTEM_TOKEN>` | **Required.**<br>Your system token. | `EAAAN6tcBzAUBOZC82CW7iR2LiaZBwUHS4Y7FDtQxRUPy1PHZClDGZBZCgWdrTisgMjpFKiZAi1FBBQNO2IqZBAzdZAA16lmUs0XgRcCf6z1LLxQCgLXDEpg80d41UZBt1FKJZCqJFcTYXJvSMeHLvOdZwFyZBrV9ZPHZASSqxDZBUZASyFdzjiy2A1sippEsF4DVV5W2IlkOSr2LrMLuYoNMYBy8xQczzOKDOMccqHEZD` |

### Response

Upon success:

```html
{
  "allocation_config_id": "<ALLOCATION_CONFIGURATION_ID>",
  "waba_id": "<CUSTOMER_WABA_ID>"
}
```

### Response parameters

| Placeholder | Description | Example value |
| --- | --- | --- |
| `<ALLOCATION_CONFIGURATION_ID>` | The extended credit line’s allocation configuration ID.<br>Save this ID if you want to [verify](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/share-and-revoke-credit-lines#verifying-shared-status) that your credit line has been shared with the customer. | `58501441721238` |
| `<CUSTOMER_WABA_ID>` | The customer’s WABA ID. | `102290129340398` |

## Step 4: Register the customer’s phone number

Use the [Register API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/register-api#post-version-phone-number-id-register) to register the customer’s business phone number for use with Cloud API.

### Request

```html
curl 'https://graph.facebook.com/v21.0/<BUSINESS_PHONE_NUMBER_ID>/register' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <BUSINESS_TOKEN>' \
-d '
{
  "messaging_product": "whatsapp",
  "pin": "<DESIRED_PIN>"
}'
```

### Request parameters

| Placeholder | Description | Example value |
| --- | --- | --- |
| `<BUSINESS_PHONE_NUMBER_ID>` | **Required.**<br>The customer’s business phone number ID returned. | `106540352242922` |
| `<BUSINESS_TOKEN>` | **Required.**<br>The customer’s business token. | `EAAAN6tcBzAUBOwtDtTfmZCJ9n3FHpSDcDTH86ekf89XnnMZAtaitMUysPDE7LES3CXkA4MmbKCghdQeU1boHr0QZA05SShiILcoUy7ZAb2GE7hrUEpYHKLDuP2sYZCURkZCHGEvEGjScGLHzC4KDm8tq2slt4BsOQE1HHX8DzHahdT51MRDqBw0YaeZByrVFZkVAoVTxXUtuKgDDdrmJQXMnI4jqJYetsZCP1efj5ygGscZBm4OvvuCYB039ZAFlyNn` |
| `<DESIRED_PIN>` | **Required.**<br>Set this value to a 6-digit number. This will be the business phone number’s two-step verification PIN. | `581063` |

### Response

Upon success:

```html
{
  "success": true
}
```

## Step 5: Send a test message

*This step is optional.*

If you wish to test the messaging capabilities of your business customer’s business phone number, send a message to the customer’s number from your own WhatsApp number (this will open a [customer service window](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages#customer-service-windows), allowing you to respond with any type of message).

Next, use the [Messages API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api#post-version-phone-number-id-messages) to send a text message in response.

### Request

```html
curl 'https://graph.facebook.com/v21.0/<BUSINESS_PHONE_NUMBER_ID>/messages' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <BUSINESS_TOKEN>' \
-d '
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "<WHATSAPP_USER_NUMBER>",
  "type": "text",
  "text": {
    "body": "<BODY_TEXT>"
  }
}'
```

### Request parameters

| Placeholder | Description | Example value |
| --- | --- | --- |
| `<BODY_TEXT>` | **Required.**<br>Message body text. Supports URLs.<br>Maximum 4096 characters. | `Message received, loud and clear!` |
| `<BUSINESS_PHONE_NUMBER_ID>` | **Required.**<br>The customer’s business phone number ID. | `106540352242922` |
| `<BUSINESS_TOKEN>` | **Required.**<br>The customer’s business token. | `EAAAN6tcBzAUBOwtDtTfmZCJ9n3FHpSDcDTH86ekf89XnnMZAtaitMUysPDE7LES3CXkA4MmbKCghdQeU1boHr0QZA05SShiILcoUy7ZAb2GE7hrUEpYHKLDuP2sYZCURkZCHGEvEGjScGLHzC4KDm8tq2slt4BsOQE1HHX8DzHahdT51MRDqBw0YaeZByrVFZkVAoVTxXUtuKgDDdrmJQXMnI4jqJYetsZCP1efj5ygGscZBm4OvvuCYB039ZAFlyNn` |
| `<WHATSAPP_USER_NUMBER>` | **Required.**<br>Your WhatsApp phone number that can send and receive messages from other WhatsApp numbers.<br>Note that this cannot be a business phone number already registered for use with Cloud API. | `+16505551234` |

### Response

Upon success:

```html
{
  "messaging_product": "whatsapp",
  "contacts": [
    {
      "input": "<WHATSAPP_USER_NUMBER>",
      "wa_id": "<WHATSAPP_USER_ID>"
    }
  ],
  "messages": [
    {
      "id": "<WHATSAPP_MESSAGE_ID>"
    }
  ]
}
```

### Response parameters

| Placeholder | Description | Example value |
| --- | --- | --- |
| `<WHATSAPP_MESSAGE_ID>` | WhatsApp message ID. | `wamid.HBgLMTY0NjcwNDM1OTUVAgARGBI1RjQyNUE3NEYxMzAzMzQ5MkEA` |
| `<WHATSAPP_USER_ID>` | Your WhatsApp user ID. | `16505551234` |
| `<WHATSAPP_USER_NUMBER>` | Your WhatsApp phone number that the message was sent to. | `+16505551234` |

If you were able to successfully send and receive messages using the customer’s business phone number, and if **messages** webhooks were triggered [describing the initial message that you sent](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages), as well as the [delivery statuses](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/status) of the message you sent in response, the customer’s business phone number is working properly.
