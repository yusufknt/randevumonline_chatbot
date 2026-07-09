# WhatsApp Cloud API - Phone Number API

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/phone-number-api/v23.0.md_

---

```
## Base URL

| URL | Description |
|-----|-------------|
| https://graph.facebook.com |  |

## APIs

| Method | Endpoint |
|--------|----------|
| GET | [/{Version}/{Phone-Number-ID}/whatsapp_commerce_settings](#get-version-phone-number-id-whatsapp-commerce-settings) |
| POST | [/{Version}/{Phone-Number-ID}/whatsapp_commerce_settings](#post-version-phone-number-id-whatsapp-commerce-settings) |

<jumplink id="get-version-phone-number-id-whatsapp-commerce-settings"></jumplink>
## GET /{Version}/{Phone-Number-ID}/whatsapp_commerce_settings

Get commerce settings

- Guide: [Sell Products & Services](https://developers.facebook.com/docs/whatsapp/cloud-api/guides/sell-products-and-services) (Cloud API)
- Guide: [Sell Products & Services](https://developers.facebook.com/docs/whatsapp/on-premises/guides/commerce-guides) (On-Premises API)
- Endpoint reference: [WhatsApp Business Phone Number &gt; WhatsApp Commerce Settings](https://developers.facebook.com/docs/graph-api/reference/whats-app-business-account-to-number-current-status/whatsapp_commerce_settings)

### Responses

**200**

Example response

**Content Type**: `application/json`

**Schema**: object

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| data | array of [Data](#object-data-1) |  |  |

<jumplink id="post-version-phone-number-id-whatsapp-commerce-settings"></jumplink>
## POST /{Version}/{Phone-Number-ID}/whatsapp_commerce_settings

Set or update commerce settings

- Guide: [Sell Products & Services](https://developers.facebook.com/docs/whatsapp/cloud-api/guides/sell-products-and-services) (Cloud API)
- Guide: [Sell Products & Services](https://developers.facebook.com/docs/whatsapp/on-premises/guides/commerce-guides) (On-Premises API)
- Endpoint reference: [WhatsApp Business Phone Number &gt; WhatsApp Commerce Settings](https://developers.facebook.com/docs/graph-api/reference/whats-app-business-account-to-number-current-status/whatsapp_commerce_settings)

### Header Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| User-Agent | string |  | The user agent string identifying the client software making the request. |
| Authorization | string | ✓ | Bearer token for API authentication. This should be a valid access token obtained through the appropriate OAuth flow or system user token. |

### Query Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| is_cart_enabled | string |  |  |
| is_catalog_visible | string |  |  |

### Responses

**200**

Example response

**Content Type**: `application/json`

**Schema**: object

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| success | boolean |  |  |

# Components

## Inline Object Definitions

<jumplink id="object-data-1"></jumplink>
### Data

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| id | string |  |  |
| is_cart_enabled | boolean |  |  |
| is_catalog_visible | boolean |  |  |
```
