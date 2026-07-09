# Product Appeal - Instagram Platform

_Source: https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/product_appeal_

---

# IG User Product Appeal

Represents a rejected product's appeal status. See [Product Tagging](https://developers.facebook.com/docs/instagram-api/guides/product-tagging) guide for complete usage details.

## Creating

**`POST /{ig-user-id}/product_appeal`**

Appeal a rejected product.

### Limitations

- Instagram Creator accounts are not supported.
- Stories, Instagram TV, Reels, Live, and Mentions are not supported.

### Requirements

| Type | Requirement |
| --- | --- |
| Access Tokens | User |
| [Business Roles](https://www.facebook.com/business/help/442345745885606) | The app user must have an admin role on the [Business Manager](https://business.facebook.com/) that owns the IG User's [Instagram Shop](https://l.facebook.com/l.php?u=https%3A%2F%2Fhelp.instagram.com%2F1187859655048322&h=AUDh5yC6v2TbrQn-wqaOtjOTWjNGAAUCJAQgWP58Ixx8fOV1yhfdBtjS2pXRXu-bK43qGtxbFTrFyXOLSdsgw369LFL7qWgUPCZKEV4SUmP77DYZ06NoTE_98BBMjw7Ksk-KOWxmOgC-lw). |
| [Instagram Shop](https://l.facebook.com/l.php?u=https%3A%2F%2Fhelp.instagram.com%2F1187859655048322%2F&h=AUCkcDlNnZMmwaHvco2cn7dJNetfLTUzNcKpnBRH-AzNF6cBB2su7co5eBBKFVXkAbGKlgZMdNOegIkN9tL0ndSuU3LpJ2ISVXRIfvPxDnEPJWdQJq-z0bW7RW0gNwlpLAAr59674OsfOQ) | The IG User must have an approved [Instagram Shop](https://l.facebook.com/l.php?u=https%3A%2F%2Fhelp.instagram.com%2F1187859655048322%2F&h=AUD_CO5lWOzuO7yae_qBF9l-nDR1gMdfwGDTRWCMQQjKGSXJorjKWgg0t1bZrA15BpC5ap5rvH9CHQRflDGVSdCyB1trgzvtEQ3ybpvpq6D3WRH2SuJhdhlrPmXKImNpekfbyU2AoFLwwA) with a product catalog containing products. |
| [Permissions](https://developers.facebook.com/docs/permissions) | `catalog_management` `instagram_basic` `instagram_shopping_tag_products`   If the app user was granted a role via the Business Manager on the Facebook Page connected to the targeted IG User, you will also need one of:   `ads_management` `ads_read` |

### Request Syntax

```
POST https://graph.facebook.com/{api-version}/{ig-user-id}/product_appeal
  ?appeal_reason={appeal-reason}
  &product_id={product-id}
  &access_token={access-token}
```

### Path Parameters

| Placeholder | Value |
| --- | --- |
| `{api-version}` | API version |
| `{ig-user-id}` | **Required.** App user's app-scoped user ID. |

### Query String Parameters

| Key | Placeholder | Value |
| --- | --- | --- |
| `access_token` | `{access-token}` | **Required.** App user's User access token. |
| `appeal_reason` | `{appeal-reason}` | **Required.** Explanation of why the product should be approved. |
| `product_id` | `{product-id}` | **Required.** Product ID. |

### Response

An object indicating success or failure. Response does not indicate appeal outcome.

```
{
  "success": {success}
}
```

#### Response Contents

| Property | Value |
| --- | --- |
| `success` | Indicates if API accepted request (`true`) or did not accept request (`false`). Response does not indicate appeal outcome. |

### cURL Example

#### Request

```
curl -i -X POST \
 "https://graph.facebook.com/v25.0/90010177253934/product_appeal?appeal_reason=product%20is%20a%20toy%20and%20not%20a%20real%20weapon&product_id=4382881195057752&access_token=EAAOc..."
```

#### Response

```
{
  "success": true
}
```

## Reading

**`GET /{ig-user-id}/product_appeal`**

Get appeal status of a rejected product.

### Limitations

- Instagram Creator accounts are not supported.
- Stories, Instagram TV, Reels, Live, and Mentions are not supported.

### Requirements

| Type | Requirement |
| --- | --- |
| Access tokens | User |
| [Business Roles](https://www.facebook.com/business/help/442345745885606) | The app user must have an admin role on the [Business Manager](https://business.facebook.com/) that owns the IG User's [Instagram Shop](https://l.facebook.com/l.php?u=https%3A%2F%2Fhelp.instagram.com%2F1187859655048322&h=AUCTMimzHerzpDQXg3Ob27hi_qHHa3WV3APypWfTdS_qoqv9CMABubP9GUXJghrpwTraN14gTQaDr2PMK0UEo-wALSn_sk0x3AFvj-cmqoy2EaLtQ82ogUhMIvKUxu1AAv1h7foe8nk25Q). |
| [Instagram Shop](https://l.facebook.com/l.php?u=https%3A%2F%2Fhelp.instagram.com%2F1187859655048322%2F&h=AUBMxzMtD13rRzdeUK7nrcJ4-8O2QRx-iz-kvyMdjzOs_8FuDjAdG4X4sLlY_t5BWrJBKdWNHMOkd5xRO_vghXxsfTn-edCXE4crpis_gup-9kYuU4hl-tMx_NCyQ4YxS51lVrqcqDmU_A) | The IG User must have an approved [Instagram Shop](https://l.facebook.com/l.php?u=https%3A%2F%2Fhelp.instagram.com%2F1187859655048322%2F&h=AUBJ_dQU2wrDhKh0QWKqRIUq6dhoN9A_eDHhPWZDiRSm9zHtdgGHPQLhy97u92xKTcj8RC4DMsUk2IokOXrjoXppRanKhxS45R7U9ubSTQ7LXCDp9iXNVVSKSbQWBpqsA1RGqT-zrPDXYw) with a product catalog containing products. |
| [Permissions](https://developers.facebook.com/docs/permissions) | `catalog_management` `instagram_basic` `instagram_shopping_tag_products`   If the app user was granted a role via the Business Manager on the Facebook Page connected to the targeted IG User, you will also need one of:    - `ads_management` - `ads_read` |

### Request Syntax

```
GET https://graph.facebook.com/{api-version}/{ig-user-id}/product_appeal
  ?product_id={product-id}
  &access_token={access-token}
```

### Path Parameters

| Placeholder | Value |
| --- | --- |
| `{api-version}` | API version |
| `{ig-user-id}` | **Required.** App user's app-scoped user ID. |

### Query String Parameters

| Key | Placeholder | Value |
| --- | --- | --- |
| `access_token` | `{access-token}` | **Required.** App user's User access token. |
| `product_id` | `{product-id}` | **Required.** Product ID. |

### Response

A JSON-formatted object containing an array of appeal status metadata.

```
{
  "data": [
    {
      "eligible_for_appeal": {eligible-for-appeal},
      "product_id": {product-id},
      "review_status": "{review-status}"
    }
  ]
}
```

#### Response Contents

| Property | Value |
| --- | --- |
| `eligible_for_appeal` | Indicates if decision can be appealed (yes if `true`, no if `false`). |
| `product_id` | Product ID. |
| `review_status` | Review status. Value can be:    - `approved` — Product is approved. - `rejected` — Product was rejected - `pending` — Still undergoing review. - `outdated` — Product was approved but has been edited and requires reapproval. - `""` — No review status. - `no_review` — No review status. |

### cURL Example

#### Request

```
curl -i -X GET \
 "https://graph.facebook.com/v25.0/90010177253934/product_appeal?product_id=4029274203846188&access_token=EAAOc..."
```

#### Response

```
{
  "data": [
    {
      "product_id": 4029274203846188,
      "review_status": "approved",
      "eligible_for_appeal": false
    }
  ]
}
```

## Updating

This operation is not supported.

## Deleting

This operation is not supported.
