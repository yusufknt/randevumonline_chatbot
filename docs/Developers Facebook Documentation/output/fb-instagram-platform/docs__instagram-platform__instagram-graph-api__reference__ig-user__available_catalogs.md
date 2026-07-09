# Available Catalogs - Instagram Platform

_Source: https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/available_catalogs_

---

# IG User Available Catalogs

Represents a collection of product catalogs in an [IG User's](https://developers.facebook.com/docs/instagram-api/reference/ig-user) [Instagram Shop](https://l.facebook.com/l.php?u=https%3A%2F%2Fhelp.instagram.com%2F1187859655048322%2F&h=AUBKmIL5LkJtzouwifMEp9upPghA42Qzw46imQoRa-JWfoq1DYL3dB72zO86UWzjnH9wJ5d43esfxFtfv3UQx2yHdSqATw7LsO8O2WewBRXBDJbTE0yENOwycQ5W4qyLY7B_o_XMiNTzHw). See [Product Tagging](https://developers.facebook.com/docs/instagram-api/guides/product-tagging) guide for complete usage details.

Available for the Instagram API with Facebook Login.

## Creating

This operation is not supported.

## Reading

**`GET /<IG_USER_ID>/available_catalogs`**

Get the product catalog in an [IG User's](https://developers.facebook.com/docs/instagram-api/reference/ig-user) [Instagram Shop](https://l.facebook.com/l.php?u=https%3A%2F%2Fhelp.instagram.com%2F1187859655048322%2F&h=AUC1mfywzokynPrEGGGqJDjkRK6OonLPgT_puGIIiuCCalMgPMcCMGA22EZmZ1-Ar8JFQljY6_Ja-AnQFJ3a8MJdKLFPgiDXk8jmUpOFopjSZmVO4_FCaVDRsM7ZtKgZdQ8YVrXyCc2wxA).

### Limitations

- Instagram Creator accounts are not supported.
- Stories, Instagram TV, Reels, Live, and Mentions are not supported.
- Only returns data on a single catalog because Instagram Shops are limited to a single catalog.
- Collaborative catalogs (shopping partner or affiliate creator catalogs) are not supported.

### Requirements

| Type | Requirement |
| --- | --- |
| Access Tokens | User |
| [Business Roles](https://www.facebook.com/business/help/442345745885606) | The app user must have an admin role on the [Business Manager](https://business.facebook.com/) that owns the IG User's [Instagram Shop](https://l.facebook.com/l.php?u=https%3A%2F%2Fhelp.instagram.com%2F1187859655048322&h=AUBTY-TlQq1lfWoOAoYM7ASMKbuPPMujZXsmQkwgNsWNVwe7tQFZKJcT9A77jMg6QBRQPzBWKuW6PJXDtaF9U50-rRpdJGTWM_VXn2otnqYP5a078lSECeS5e28bmur2YK0LGYwvlmW4EA). |
| [Instagram Shop](https://l.facebook.com/l.php?u=https%3A%2F%2Fhelp.instagram.com%2F1187859655048322%2F&h=AUC9-S1A97rn8HGAMJdQiAh9ybduJWKBo4Zmspuhp2oiHI_K6m9edsSDyvJQR4PWJfGw0N2vNl8yCIibXqETcbdP9S0itx56vU8asUCnVtgcyavVVRhFldqV18-cVA7TfwEi8m4Wp7PNBQ) | The IG User must have an approved [Instagram Shop](https://l.facebook.com/l.php?u=https%3A%2F%2Fhelp.instagram.com%2F1187859655048322%2F&h=AUBbu3kwZ3YIaTTUJeAWQAOCT9ooGwkFWSVpa-jQIITYnRLepftC4mznBQYMUYIqDfKJjhwt9qoHpdXUjWj1Ont2spTTjr84Ra0DPGBvfweDimFd4Xc9YEOCruBn6OYqd3IR6TqyIqg5Pg) with a product catalog containing products. |
| [Permissions](https://developers.facebook.com/docs/permissions/) | `catalog_management` `instagram_basic` `instagram_shopping_tag_products`  If the app user was granted a role via the Business Manager on the [Facebook Page](https://developers.facebook.com/docs/instagram-api/overview#pages) connected to the targeted IG User, you will also need one of:  `ads_management` `ads_read` |

### Request Syntax

```
GET https://graph.facebook.com/<API_VERSION>/<IG_USER_ID>/available_catalogs
  ?fields=<LIST_OF_FIELDS>
  &access_token=<ACCESS_TOKEN>
```

### Path Parameters

| Placeholder | Value |
| --- | --- |
| `<API_VERSION>` | API version |
| `<IG_USER_ID>` | **Required.** App user's app-scoped user ID. |

### Query String Parameters

| Key | Placeholder | Value |
| --- | --- | --- |
| `access_token` | `<ACCESS_TOKEN>` | **Required.** App user's User access token. |
| `fields` | `<LIST_OF_FIELDS>` | Comma-separated list of catalog [fields](#response-contents) you want returned for each catalog in the result set. |

### Response

A JSON-formatted object containing the data you requested.

```
{
  "data": [
    {
      "catalog_id": "{catalog-id}",
      "catalog_name": "{catalog-name}",
      "shop_name": "{shop-name}",
      "product_count": {product-count}
    }
  ]
}
```

#### Response Contents

| Property | Value |
| --- | --- |
| `catalog_id` | Catalog ID. |
| `catalog_name` | Catalog name. |
| `shop_name` | Shop name. |
| `product_count` | Number of products in catalog. Includes all products regardless of review status. |

### cURL Example

#### Request

```
curl -i -X GET \
 "https://graph.facebook.com/v25.0/90010177253934/available_catalogs?access_token=EAAOc..."
```

#### Response

```
{
  "data": [
    {
      "catalog_id": "960179311066902",
      "catalog_name": "Jay's Favorite Snacks",
      "shop_name": "Jay's Bespoke",
      "product_count": 11
    }
  ]
}
```

## Updating

This operation is not supported.

## Deleting

This operation is not supported.
