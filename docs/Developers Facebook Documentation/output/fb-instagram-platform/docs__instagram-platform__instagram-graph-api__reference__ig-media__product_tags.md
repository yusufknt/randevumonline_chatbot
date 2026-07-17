# Product Tags - Instagram Platform

_Source: https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-media/product_tags_

---

# IG Media Product Tags

Represents product tags on an [IG Media](https://developers.facebook.com/docs/instagram-api/reference/ig-media). See [Product Tagging](https://developers.facebook.com/docs/instagram-api/guides/product-tagging) guide for complete usage details.

Available for the Instagram API with Facebook Login.

## Creating

**`POST /<IG_MEDIA_ID>/product_tags`**

Create or update product tags on an existing [IG Media](https://developers.facebook.com/docs/instagram-api/reference/ig-media).

### Limitations

- Instagram Creator accounts are not supported.
- Stories, Instagram TV, Live, and Mentions are not supported.
- Tagging media is additive until the tag limit has been reached (20 for feed posts, 30 for Reels). If the targeted media has already been tagged by a product in the request, the old tag's `x` and `y` values will be updated with their new values (a new tag will not be added).

### Requirements

| Type | Requirement |
| --- | --- |
| Access Tokens | User |
| [Business Roles](https://www.facebook.com/business/help/442345745885606) | The app user must have an admin role on the [Business Manager](https://business.facebook.com/) that owns the IG User's [Instagram Shop](https://l.facebook.com/l.php?u=https%3A%2F%2Fhelp.instagram.com%2F1187859655048322&h=AUCaFraTfQrR7VKDbrxdiT2Rt6jN-ew4Ja7RT-CxV5MDcxkmo4qzWQDJbB9DvPaEnKyzTS2r3kj49YnImVSagDcWgwFeOECH-rQhX7t9tTItDx3Q_fHi14YmJEZ2KH6w_1mop06iDhoPzQ). |
| [Instagram Shop](https://l.facebook.com/l.php?u=https%3A%2F%2Fhelp.instagram.com%2F1187859655048322%2F&h=AUB4JqBBTUaiEV4cu0p0O0NWJWRiziEy4WnKWE42_yhGkLPORTz9OhHxob0H0OZOEfsWa1_7BlrLQUGH9cgHkpJwgp9RgU9u4JqV6cMa6PFfIkbMQCd2OtPRWLpaBVy552k7I36ttpWWpw) | The IG User that owns the IG Media must have an approved [Instagram Shop](https://l.facebook.com/l.php?u=https%3A%2F%2Fhelp.instagram.com%2F1187859655048322%2F&h=AUA59XYxSAd8pTlJ3fEqOvJ3QFcomspSljQux9ImHUwCeP1tWCKTxKrpW22UC3lfPEYV_pNnSN9SAWWXfjcsXhslaIugiMM8p-PGkzPKqbi_lzI210eTvtb2oJQus8iqAb7Y0fcsZnZ5dQ) with a product catalog containing products. |
| [Permissions](https://developers.facebook.com/docs/permissions) | - `ad_reads` - [`catalog_management` - `instagram_basic` - `instagram_shopping_tag_products`   If the app user was granted a role via the Business Manager on the [Page](https://developers.facebook.com/docs/instagram-api/overview#pages) connected to the targeted IG User, you will also need:  `ads_management` |

### Request Syntax

```
POST https://graph.facebook.com/<API_VERSION>/<IG_MEDIA_ID>/product_tags
  ?updated_tags=<LIST_OF_UPDATED_TAGS>
  &access_token=<ACCESS_TOKEN>
```

### Path Parameters

| Placeholder | Value |
| --- | --- |
| `<API_VERSION>` | API version |
| `<IG_MEDIA_ID>` | **Required.** IG Media ID. |

### Query String Parameters

| Key | Placeholder | Value |
| --- | --- | --- |
| `access_token` | `<ACCESS_TOKEN>` | **Required.** App user's User access token. |
| `updated_tags` | `<LIST_OF_UPDATED_TAGS>` | **Required. Applies only to images and videos**. An array of objects specifying which product tags to tag the image or video with (maximum of 20 for Feed posts, maximum of 30 for Reels; tags and product IDs must be unique). Each object should have the following information:    - `product_id` — **Required.** Product ID. - `x` — **Images only.** An optional float that indicates percentage distance from left edge of the published media image. Value must be within `0.0`–`1.0` range. - `y` — **Images only.** An optional float that indicates percentage distance from top edge of the published media image. Value must be within `0.0`–`1.0` range.   For example:   `[{product_id:'3231775643511089',x:0.5,y:0.8}]` |

### Response

An object indicating success or failure.

```
{
  "success": {success}
}
```

#### Response Contents

| Property | Value |
| --- | --- |
| `success` | Returns `true` if able to update the IG Media's product tags, otherwise returns `false`. |

### cURL Example

#### Request

```
curl -i -X POST \
 "https://graph.facebook.com/v25.0/90010778325754/product_tags?updated_tags=%5B%0A%20%20%7B%0A%20%20%20%20product_id%3A'3859448974125379'%2C%0A%20%20%20%20x%3A%200.5%2C%0A%20%20%20%20y%3A%200.8%0A%20%20%7D%0A%5D&access_token=EAAOc..."
```

For reference, here is the HTML-decoded POST payload string:

```
https://graph.facebook.com/v25.0/90010778325754/product_tags?updated_tags=[
  {
    product_id:'3859448974125379',
    x: 0.5,
    y: 0.8
  }
]&access_token=EAAOc...
```

#### Response

```
{
  "success": true
}
```

## Reading

**`GET /<IG_MEDIA_ID>/product_tags`**

Get a collection of product tags on an [IG Media](https://developers.facebook.com/docs/instagram-api/reference/ig-media). See the [Product Tagging](https://developers.facebook.com/docs/instagram-api/guides/product-tagging) guide for complete product tagging steps.

### Limitations

- Instagram Creator accounts are not supported.
- Stories, Instagram TV, Reels, Live, and Mentions are not supported.

### Requirements

| Type | Requirement |
| --- | --- |
| Access Tokens | User |
| [Business Roles](https://www.facebook.com/business/help/442345745885606) | The app user must have an admin role on the [Business Manager](https://business.facebook.com/) that owns the IG User's [Instagram Shop](https://l.facebook.com/l.php?u=https%3A%2F%2Fhelp.instagram.com%2F1187859655048322&h=AUAQV6HyQ3289ZDI_9PdRhVV61c8Y_tQWTtRIHKvp9HIUDp1Hf7ASyowBImX17BTk4reoZE3kkxWgLsgBZ3vbeDOw7XZk3CbeT41a1RUtZJFXIO9YCmShoO6SE22l36eXfmhHk8fG1699g). |
| [Instagram Shop](https://l.facebook.com/l.php?u=https%3A%2F%2Fhelp.instagram.com%2F1187859655048322%2F&h=AUDwJcILF_2dmpWJmr9rHwnHRQ6qOze0-s76VAQ8GqUpyvdJbhDt0qC6z0VLWWQOi6-YZLhcLGjcIoxiJZhTyl3vAO3-68w--KpZLiOJP_kDaE999JrOC0QXtWDGKr7caJzEKLSTyiyR5w) | The IG User that owns the IG Media must have an approved [Instagram Shop](https://l.facebook.com/l.php?u=https%3A%2F%2Fhelp.instagram.com%2F1187859655048322%2F&h=AUDLbpI7t6TmeJeNL5BZYidAeikVpxAnYXEVOOuPdyVg9Vj7i1YfSsJHzqs1I80CC3SEPxVEHmS4DMjG6pBAlCJWx7YQ62e4_gW75Wv8O4KWW3PneIZkra6KhfVSqnrBe7ezyHvwOC1MZw) with a product catalog containing products. |
| [Permissions](https://developers.facebook.com/docs/permissions) | - `ad_reads` - `catalog_management` - `instagram_basic` - `instagram_shopping_tag_products`   If the app user was granted a role via the Business Manager on the [Page](https://developers.facebook.com/docs/instagram-api/overview#pages) connected to the targeted IG User, you will also need:   - `ads_management` |

### Request Syntax

```
GET https://graph.facebook.com/<API_VERSION>/<IG_MEDIA_ID>/product_tags
  ?access_token=<ACCESS_TOKEN>
```

### Path Parameters

| Placeholder | Value |
| --- | --- |
| `<API_VERSION>` | API version |
| `<IG_MEDIA_ID>` | **Required.** IG Media ID. |

### Query String Parameters

| Key | Placeholder | Value |
| --- | --- | --- |
| `access_token` | `<ACCESS_TOKEN>` | **Required.** App user's User access token. |

### Response

A JSON-formatted object containing an array of product tags on an IG Media. Responses can include the following product tag fields:

```
{
  "data": [
    {
      "product_id": {product-id},
      "merchant_id": {merchant-id},
      "name": "{name}",
      "price_string": "{price-string}",
      "image_url": "{image-url}",
      "review_status": "{review-status}",
      "is_checkout": {is-checkout},
      "stripped_price_string": "{stripped-price-string}",
      "string_sale_price_string": "{string-sale-price-string}",
      "x": {x},
      "y": {y}
    }
  ]
}
```

#### Response Contents

| Property | Value |
| --- | --- |
| `product_id` | Product ID. |
| `merchant_id` | Merchant ID. |
| `name` | Product name. |
| `price_string` | Price string. |
| `image_url` | Product image URL. |
| `review_status` | Product review status. Values can be:    - `approved` — Product is approved. - `rejected` — Product was rejected - `pending` — Still undergoing review. - `outdated` — Product was approved but has been edited and requires reapproval. - `""` — No review status. |
| `is_checkout` | If `true`, product can be purchased directly through the Instagram app. If `false`, product can only be purchased on the merchant's website. |
| `stripped_price_string` | Product short price string (price displayed in constrained spaces, such as `$100` instead of `100 USD`). |
| `string_sale_price_string` | Product sale price. |
| `x` | A float that indicates percentage distance from left edge of media image. Value within `0.0`–`1.0` range. |
| `y` | A float that indicates percentage distance from top edge of media image. Value within `0.0`–`1.0` range. |

### cURL Example

#### Request

```
curl -i -X GET \
 "https://graph.facebook.com/v25.0/90010778325754/product_tags?access_token=EAAOc..."
```

#### Response

```
{
  "data": [
    {
      "product_id": 3231775643511089,
      "merchant_id": 90010177253934,
      "name": "Gummy Bears",
      "price_string": "$3.50",
      "image_url": "https://scont...",
      "review_status": "approved",
      "is_checkout": true,
      "stripped_price_string": "$3.50",
      "stripped_sale_price_string": "$3",
      "x": 0.5,
      "y": 0.80000001192093
    }
  ]
}
```

## Updating

See [Creating](#creating).
