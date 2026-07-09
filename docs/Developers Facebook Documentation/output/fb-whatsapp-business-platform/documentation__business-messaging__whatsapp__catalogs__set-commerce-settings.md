# Set commerce settings | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/catalogs/set-commerce-settings_

---

# Set commerce settings

Updated: Mar 3, 2026

You can enable or disable the shopping cart and the product catalog on a per-business phone number basis. By default, the shopping cart is enabled and the storefront icon is hidden for all business phone numbers associated with a WhatsApp Business Account.

## Get business phone numbers

Use the [Phone Numbers API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/phone-number-management-api) to get a list of all business phone numbers associated with a WhatsApp Business Account.

## Enable or disable cart

Use the [Commerce Settings API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/phone-number-api) to enable or disable the shopping cart for a specific business phone number.

When enabled, cart-related buttons appear in the chat, catalog, and product details views:

![Three WhatsApp messenger screenshots with callout of various cart UI components displayed](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/513870481_1426428692034436_5288360534924361904_n.png?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=aUtYaYw4SvEQ7kNvwHD6dSh&_nc_oc=AdqhYPK0fsbeCVq-DdhHvuDghk6bsKQGBzxFuRduV8F5x_DsLAF8-qU4Id7CGWws9-U&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=wWzK8cslhlsSN1gNZod7_g&_nc_ss=7b20f&oh=00_Af4yJiS2Q_myTAnZmczBGsSFl8twl3aDz-t_3Q7Dc0_JOw&oe=6A1C1C56)

When the cart is disabled, customers can see products and their details, but cart-related buttons do not appear in any view.

### Request syntax

```http
POST /<BUSINESS_PHONE_NUMBER_ID>/whatsapp_commerce_settings
  ?is_cart_enabled=<IS_CART_ENABLED>
```

### Parameters

| Placeholder | Sample Value | Description |
| --- | --- | --- |
| `<BUSINESS_PHONE_NUMBER_ID>` | `106850078877666` | Business phone number ID. |
| `<IS_CART_ENABLED>` | `true` | Boolean. Set to `true` to enable cart or `false` to disable it. Default value is `true`. |

### Sample request

```curl
curl -X POST 'https://graph.facebook.com/v25.0/106850078877666/whatsapp_commerce_settings?is_cart_enabled=true' \
-H 'Authorization: Bearer EAAJB...'
```

### Sample response

```json
{
  "success": true
}
```

## Enable or disable catalog

Use the [Commerce Settings API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/phone-number-api) to enable or disable the product catalog for a specific business phone number.

When enabled, the catalog storefront icon and catalog-related buttons appear in chat views and business profile views:

![Two WhatsApp messenger screenshots with callout of various catalog UI components displayed](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/513359223_1234792844894756_6573923522221485884_n.png?_nc_cat=102&ccb=1-7&_nc_sid=e280be&_nc_ohc=lO6TzhdGdF0Q7kNvwH24FHU&_nc_oc=AdpQbU-CO-1svj6As9AtNdghj_c4n_mY4ONbdQlGT1DF-FMl992cJJ5mykPq4dB6I60&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=wWzK8cslhlsSN1gNZod7_g&_nc_ss=7b20f&oh=00_Af4GWqKc6nIqCHkqMaY0o9549H1cQgBLvemytahY6Lcj9Q&oe=6A1C16B3)

When the catalog is disabled, the storefront icon and catalog-related buttons do not appear in any views and the catalog preview with thumbnails does not appear in the business profile view.

If you disable the catalog, wa.me links to your catalog, as well as the **View catalog** button that appears when you send your catalog link in a message will display an **Invalid catalog link** warning when tapped.

### Request syntax

```http
POST /<BUSINESS_PHONE_NUMBER_ID>/whatsapp_commerce_settings
  ?is_catalog_visible=<IS_CATALOG_VISIBLE>
```

### Parameters

| Placeholder | Sample Value | Description |
| --- | --- | --- |
| `<BUSINESS_PHONE_NUMBER_ID>` | `106850078877666` | Business phone number ID. |
| `<IS_CATALOG_VISIBLE>` | `true` | Boolean. Set to `true` to show catalog storefront icon or `false` to hide it. Default value is `false`. |

### Sample request

```curl
curl -X POST 'https://graph.facebook.com/v25.0/106850078877666/whatsapp_commerce_settings?is_catalog_visible=true' \
-H 'Authorization: Bearer EAAJB...'
```

### Sample response

```json
{
  "success": true
}
```

## Get commerce settings

Use the [Commerce Settings API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/phone-number-api) to get an individual business phone number’s commerce settings.

### Request syntax

```http
GET /<BUSINESS_PHONE_NUMBER_ID>/whatsapp_commerce_settings
```

### Parameters

| Placeholder | Sample Value | Description |
| --- | --- | --- |
| `<BUSINESS_PHONE_NUMBER_ID>` | `106850078877666` | Business phone number ID. |

### Sample request

```curl
curl -X GET 'https://graph.facebook.com/v25.0/106850078877666/whatsapp_commerce_settings' \
-H 'Authorization: Bearer EAAJB...'
```

### Sample response

```json
{
  "data": [
    {
      "is_cart_enabled": true,
      "is_catalog_visible": true,
      "id": "727705352028726"
    }
  ]
}
```
