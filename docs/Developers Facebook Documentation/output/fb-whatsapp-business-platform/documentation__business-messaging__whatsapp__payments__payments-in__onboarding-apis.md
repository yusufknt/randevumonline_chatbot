# Onboarding APIs | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/onboarding-apis_

---

# Onboarding APIs

Updated: Nov 14, 2025

To receive payments on WhatsApp, you must have a payment configuration linked to the corresponding WhatsApp Business Account. Each payment configuration is associated with a unique name. As part of the order_details message, you can specify the payment configuration to use for a specific checkout.

Onboarding APIs allows you to programatically perform certain operations:

- Get all payment configurations linked to a WhatsApp Business Account.
- Get a specific payment configuration linked to a WhatsApp Business Account.
- Create a payment configuration.
- Regenerate payment gateway OAuth link to link payment configuration to a payment gateway.
- Remove a payment configuration.

## Get All Payment Configurations

Get a list of payment configurations linked to the WhatsApp Business Account.

### Request Syntax

```html
GET /<WHATSAPP_BUSINESS_ACCOUNT_ID>/payment_configurations
```

### Sample Request

```curl
curl 'https://graph.facebook.com/v16.0/102290129340398/payment_configurations' \
-H 'Authorization: Bearer EAAJB...'
```

### Sample Response

```json
{
  "data": [
    {
      "payment_configurations": [
    {
      "configuration_name": "test-payment-configuration",
      "merchant_category_code": {
        "code": "0000",
            "description": "Test MCC Code"
       },
           "purpose_code": {
         "code": "00",
         "description": "Test Purpose Code"
        },
        "status": "Active",
         "provider_mid": "test-payment-gateway-mid",
        "provider_name": "RazorPay",
        "created_timestamp": 1720203204,
        "updated_timestamp": 1721088316
    },
          ....
  ]
     }
  ]
}
```

| Field | Description |
| --- | --- |
| `configuration_name`<br>string | **Required.**<br>The name of the payment configuration to be used in the Order Details message. |
| `merchant_category_code`<br>object | **Required.**<br>Merchant Category Code:<br>`code` string<br>**Required.** Will be a valid MCC code.<br>`description` string<br>**Required.** MCC code description. |
| `purpose_code`<br>object | **Required.**<br>Purpose Code:<br>`code` string<br>**Required.** Will be a valid purpose code.<br>`description` string<br>**Required.** Purpose code description. |
| `status`<br>string | **Required.**<br>Status of the payment configuration. Must be one of [“Active”, “Needs_Connecting”, “Needs_Testing”]. |
| `provider_mid`<br>string | **Optional.**<br>Payment Gateway Merchant Identification Number (MID). |
| `provider_name`<br>string | **Optional.**<br>Payment Gateway Name. Must be one of [“razorpay”, “payu”, “zaakpay”]. |
| `merchant_vpa`<br>string | **Optional.**<br>Merchant UPI handle. |
| `created_timestamp`<br>integer | **Optional.**<br>Time when payment configuration was created. |
| `updated_timestamp`<br>integer | **Optional.**<br>Time when payment configuration was last updated. |

## Get a specific Payment Configuration

Get a specific payment configuration linked to the WhatsApp Business Account.

### Request Syntax

```html
GET /<WHATSAPP_BUSINESS_ACCOUNT_ID>/payment_configuration/<CONFIGURATION_NAME>
```

### Sample Request

```curl
curl 'https://graph.facebook.com/v16.0/102290129340398/payment_configuration/test-payment-configuration' \
-H 'Authorization: Bearer EAAJB...'
```

### Sample Response

```json
{
  "data": [
    {
      "configuration_name": "test-payment-configuration",
      "merchant_category_code": {
        "code": "0000",
        "description": "Test MCC Code"
      },
      "purpose_code": {
        "code": "00",
        "description": "Test Purpose Code"
      },
      "status": "Active",
      "provider_mid": "test-payment-gateway-mid",
      "provider_name": "RazorPay",
      "created_timestamp": 1720203204,
      "updated_timestamp": 1721088316
     }
  ]
}
```

| Field | Description |
| --- | --- |
| `configuration_name`<br>string | **Required.**<br>The name of the payment configuration to be used in the Order Details message. |
| `merchant_category_code`<br>object | **Required.**<br>Merchant Category Code:<br>`code` string<br>**Required.** Will be a valid MCC code.<br>`description` string<br>**Required.** MCC code description. |
| `purpose_code`<br>object | **Required.**<br>Purpose Code:<br>`code` string<br>**Required.** Will be a valid purpose code.<br>`description` string<br>**Required.** Purpose code description. |
| `status`<br>string | **Required.**<br>Status of the payment configuration. Must be one of [“Active”, “Needs_Connecting”, “Needs_Testing”]. |
| `provider_mid`<br>string | **Optional.**<br>Payment Gateway Merchant Identification Number (MID). |
| `provider_name`<br>string | **Optional.**<br>Payment Gateway Name. Must be one of [“razorpay”, “payu”, “zaakpay”]. |
| `merchant_vpa`<br>string | **Optional.**<br>Merchant UPI handle. |
| `created_timestamp`<br>integer | **Optional.**<br>Time when payment configuration was created. |
| `updated_timestamp`<br>integer | **Optional.**<br>Time when payment configuration was last updated. |

## Create a Payment Configuration

Create a payment configuration.

### Request Syntax

```html
POST /<WHATSAPP_BUSINESS_ACCOUNT_ID>/payment_configuration
```

### Sample Request

Payment Gateway type configuration

```curl
curl -X  POST \
'https://graph.facebook.com/v15.0/102290129340398/payment_configuration' \
-H 'Authorization: Bearer EAAJB...' \
-H 'Content-Type: application/json' \
-d '{
       "configuration_name": "test-payment-configuration",
       "purpose_code": "00",
       "merchant_category_code": "0000",
       "provider_name": "razorpay",
       "redirect_url": "https://test-redirect-url.com"
    }'
```

UPI Vpa type configuration

```curl
curl -X  POST \
'https://graph.facebook.com/v15.0/102290129340398/payment_configuration' \
-H 'Authorization: Bearer EAAJB...' \
-H 'Content-Type: application/json' \
-d '{
       "configuration_name": "test-payment-configuration",
       "purpose_code": "00",
       "merchant_category_code": "0000",
       "provider_name": "upi_vpa",
       "merchant_vpa": "test-upi-merchant-vpa@test"
    }'
```

| Field | Description |
| --- | --- |
| `configuration_name`<br>string | **Required.**<br>The name of the payment configuration to be used in the Order Details message. |
| `merchant_category_code`<br>string | **Optional.**<br>Merchant Category Code. |
| `purpose_code`<br>object | **Optional.**<br>Purpose Code. |
| `provider_name`<br>string | **Required.**<br>Provider name of the payment configuration. Must be one of [“upi_vpa”, “razorpay”, “payu”, “zaakpay”]. |
| `merchant_vpa`<br>string | **Optional.**<br>Merchant UPI handle. |
| `redirect_url`<br>URI | **Optional.**<br>The url which merchant will be redirected to after successfully linking a payment configuration. |

### Sample Response

Payment Gateway type configuration

```json
{
  "oauth_url": "https://www.facebook.com/payment/onboarding/init/",
  "expiration": 1721687287,
  "success": true
}
```

UPI Vpa type configuration

```json
{
  "success": true
}
```

| Field | Description |
| --- | --- |
| `oauth_url`<br>string | **Optional.**<br>OAuth url to be used to link payment configuration to the payment gateway |
| `expiration`<br>integer | **Optional.**<br>Expiration time of the OAuth url. |
| `success`<br>boolean | **Required.**<br>Boolean flag to denote if payment configuration creation was successful or not. |

## Link or Update Data Endpoint

The following section explains how to link, update and delete data endpoint to enable coupons, shipping address and real-time inventory offered by [Checkout Button Templates](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/checkout-button-templates#enabling_coupons_inventory).

### Request Syntax

```html
POST /<WHATSAPP_BUSINESS_ACCOUNT_ID>/payment_configuration/<CONFIGURATION_NAME>
```

### Sample Request

Payment Gateway type configuration

```curl
curl -X  POST \
'https://graph.facebook.com/v15.0/102290129340398/payment_configuration/test-payment-configuration' \
-H 'Authorization: Bearer EAAJB...' \
-H 'Content-Type: application/json' \
-d '{
       "data_endpoint_url": "https://test-data-endpoint-url.com"
    }'
```

| Field | Description |
| --- | --- |
| `data-endpoint-url`<br>URI | **Optional.**<br>The URL endpoint that the WhatsApp client sends a secure HTTPS request to for data exchange purposes in [Checkout Button Templates](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/checkout-button-templates#enabling_coupons_inventory) offering. |

## Regenerate Payment Configuration OAuth link

Regenerate OAuth link of payment gateway type payment configuration.

### Request Syntax

```html
POST /<WHATSAPP_BUSINESS_ACCOUNT_ID>/generate_payment_configuration_oauth_link
```

### Sample Request

```curl
curl -X  POST \
'https://graph.facebook.com/v15.0/102290129340398/generate_payment_configuration_oauth_link' \
-H 'Authorization: Bearer EAAJB...' \
-H 'Content-Type: application/json' \
-d '{
       "configuration_name": "test-payment-configuration",
       "redirect_url": "https://test-redirect-url.com"
    }'
```

| Field | Description |
| --- | --- |
| `configuration_name`<br>string | **Required.**<br>The name of the payment configuration to be used in the Order Details message. |
| `redirect_url`<br>URI | **Optional.**<br>The url which merchant will be redirected to after successfully linking a payment configuration. |

### Sample Response

```json
{
  "oauth_url": "https://www.facebook.com/payment/onboarding/init/",
  "expiration": 1721687287
}
```

| Field | Description |
| --- | --- |
| `oauth_url`<br>string | **Optional.**<br>OAuth url to be used to link payment configuration to the payment gateway |
| `expiration`<br>integer | **Optional.**<br>Expiration time of the OAuth url. |

## Remove a Payment Configuration

Remove a payment configuration.

### Request Syntax

```html
DELETE /<WHATSAPP_BUSINESS_ACCOUNT_ID>/payment_configuration
```

| Field | Description |
| --- | --- |
| `configuration_name`<br>string | **Required.**<br>The name of the payment configuration to be used in the Order Details message. |

### Sample Request

```curl
curl -X  DELETE \
'https://graph.facebook.com/v15.0/102290129340398/payment_configuration' \
-H 'Authorization: Bearer EAAJB...' \
-H 'Content-Type: application/json' \
-d '{
       "configuration_name": "test-payment-configuration"
    }'
```

### Sample Response

```json
{
  "success": true
}
```

| Field | Description |
| --- | --- |
| `success`<br>boolean | **Required.**<br>Boolean flag to denote if payment configuration removal was successful or not. |

## Payment Configuration Webhook

Businesses receive updates via WhatsApp webhooks when the status of the payment configuration changes.

To receive webhook, Businesses must subscribe to “payment_configuration_update” event for their respective application.

Webhook contains the following fields:

| Field | Description |
| --- | --- |
| `configuration_name`<br>string | **Required.**<br>The name of the payment configuration to be used in the Order Details message. |
| `provider_name`<br>string | **Required.**<br>Provider name of the payment configuration. Must be one of [“razorpay”, “payu”, “zaakpay”]. |
| `provider_mid`<br>string | **Required.**<br>Payment gateway account merchant ID. |
| `status`<br>string | **Required.**<br>Status of the payment configuration. Must be one of [“Active”, “Needs_Connecting”, “Needs_Testing”]. |
| `created_timestamp`<br>integer | **Required.**<br>Time when payment configuration was created. |
| `updated_timestamp`<br>integer | **Required.**<br>Time when payment configuration was last updated. |

### Sample Payment Configuration Webhook

```json
{
  "entry": [
    {
      "id": "0",
      "time": 1725499886,
      "changes": [
        {
          "field": "payment_configuration_update",
          "value": {
            "configuration_name": "test-payment-configuration",
            "provider_name": "razorpay",
            "provider_mid": "test-provider-mid",
            "status": "Needs Testing",
            "created_timestamp": 123457678,
            "updated_timestamp": 123457678
          }
        }
      ]
    }
  ],
  "object": "whatsapp_business_account"
}
```

### Errors

WhatsApp Payments Terms of Service Acceptance Pending

If you see the following error, accept the WhatsApp Payments terms of service using the link provided in the error message before trying again.

```json
{
  "error": {
    "message": "(#131005) Access denied",
    "type": "OAuthException",
    "code": 131005,
    "error_data": {
      "messaging_product": "whatsapp",
      "details": "WhatsApp Payments Terms of Service acceptance pending for this WhatsApp Business Account.
Please use the following link to accept terms of service before using Business APIs: https://fb.me/12345"
    }
  }
}
```

For all other errors that can be returned and guidance on how to handle them, see [WhatsApp Cloud API, Error Codes](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/error-codes).
