# IG User - Instagram Platform

_Source: https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user_

---

# IG User

Represents an [Instagram Business Account](https://l.facebook.com/l.php?u=https%3A%2F%2Fhelp.instagram.com%2F502981923235522&h=AUAaT2vRp2iP7rCdDZWJggJWz2nVHkOn_cOZAA68izz_2lKVO2UUu1MaBtkK3QJBFu5uqayARQy52Km5YWv1JL6cB-fqtnAuXvO5XGusk6ZCCRXZjSsqekQ2vBOBS5plVrqhPN404LUxbA) or an [Instagram Creator Account](https://l.facebook.com/l.php?u=https%3A%2F%2Fhelp.instagram.com%2F1158274571010880&h=AUCvk2N4_UwMwE1KrPXzSyAkvYfgpPk5OjEH9awAv1r9xuH1qCDd3DT6iV03382gn0nzRzJDKNvnujH-VPAUiHvUyGTwFjHrE7lIM-o6AtHI3U4dsPU5BYnuuTSlK6KbjOE7wNWexRihnw).

Throughout our documentation we use "Instagram User" and "Instagram Account" interchangeably. Both represent your app user's Instagram professional account.

### Requirements

|  | Instagram API with Instagram Login | Instagram API with Facebook Login |
| --- | --- | --- |
| **Access Tokens** | - Instagram User user access token | - [Facebook User access token](https://developers.facebook.com/docs/facebook-login/access-tokens/#usertokens) |
| **Host URL** | `graph.instagram.com` | `graph.facebook.com` |
| **Login Type** | Business Login for Instagram | Facebook Login for Business |
| [**Permissions**](https://developers.facebook.com/docs/permissions/reference#i) | - `instagram_business_basic` | - `instagram_basic` - `pages_read_engagement`   If the app user was granted a role via the Business Manager on the [Page](https://developers.facebook.com/docs/instagram-api/overview#pages) connected to the targeted IG User, you will also need one of:   - `ads_management` - `ads_read`   If you are requesting the `shopping_product_tag_eligibility` field for [product tagging](https://developers.facebook.com/docs/instagram-api/guides/product-tagging), you will also need:   - `catalog_management` - `instagram_shopping_tag_products` |
| **[Business Roles](https://www.facebook.com/business/help/442345745885606)** | Not applicable. | If you are requesting the `shopping_product_tag_eligibility` field for [product tagging](https://developers.facebook.com/docs/instagram-api/guides/product-tagging), the app user must have an admin role on the [Business Manager](https://business.facebook.com/) that owns the IG User's [Instagram Shop](https://l.facebook.com/l.php?u=https%3A%2F%2Fhelp.instagram.com%2F1187859655048322&h=AUCtciW1qH_h2cMyKpwYED7c7A3tLAVTINDNdw2OoCh3qSQiXNCrW3CrPDVgRxJgb1tKeIOld_TCFgFcKcyAx6PD5xAeYwpkuXasaZ0JgOUj7uIho7pSxwJBgw30d5xG0F1lUDnZ26_hAQ). |
| **[Instagram Shop](https://l.facebook.com/l.php?u=https%3A%2F%2Fhelp.instagram.com%2F1187859655048322%2F&h=AUB7VNr5vDBG_j9-HY-3ICnXB3mwfswaMqxQJ5RjP_M_ZtIyVohWDJWdlHc-Vj1ij0WWQvmhn29OBRcogovQ2i7vseXOUaheASfyX2p9eTfABP2N70DdgcnNIAhNUWmQGVoL_Q9fIbjgWw)** | Not applicable. | If you are requesting the `shopping_product_tag_eligibility` field for [product tagging](https://developers.facebook.com/docs/instagram-api/guides/product-tagging), the IG User must have an approved [Instagram Shop](https://l.facebook.com/l.php?u=https%3A%2F%2Fhelp.instagram.com%2F1187859655048322%2F&h=AUD33kaOEuKEzKOIR4AGpHdVkVcvPy-9FCw9p_fVNQg0sJHFZzxrUjYYxMy4dvRV7DvQx8OwtWqmOlsGA98dtaIRKEeUPmk-EgF57U7N-ZZdzT1nCLz7T-T_cjCyn1o3MTvaHwrkCtJa5A) with a product catalog containing products. |

## Creating

This operation is not supported.

## Reading

**`GET /<IG_USER_ID>`**

Get fields and edges on an Instagram Business or Creator Account.

If you are migrating from Marketing API Instagram Ads endpoints to Instagram Platform endpoints, be aware that some field names are different.

### Request Syntax

```
GET https://graph.facebook.com/<API_VERSION>/<IG_USER_ID>
  ?fields=<LIST_OF_FIELDS>
  &access_token=<ACCESS_TOKEN>
```

### Path Parameters

| Placeholder | Value |
| --- | --- |
| `<API_VERSION>` | API [version](https://developers.facebook.com/docs/graph-api/guides/versioning). |
| `<IG_USER_ID>` | **Required.** IG User ID. |

### Query String Parameters

| Key | Placeholder | Value |
| --- | --- | --- |
| `access_token` | `<ACCESS_TOKEN>` | **Required.** App user's [User](https://developers.facebook.com/docs/facebook-login/access-tokens/#usertokens) access token. |
| `fields` | `<LIST_OF_FIELDS>` | Comma-separated list of IG User [fields](#fields) you want returned for each IG User in the result set. |

### Fields

Public fields can be returned by an edge using field expansion. Only a few fields will be available for accessing [Page-backed Instagram accounts](https://developers.facebook.com/docs/instagram/ads-api/guides/pages-ig-account#pbia).

| Field Name | Description |
| --- | --- |
| `alt_text`  Public | Descriptive text for images, for accessibility. |
| `biography`  Public | Profile bio text. |
| `followers_count`  Public | Total number of Instagram users following the user. |
| `follows_count` | Total number of Instagram users the user follows. |
| `has_profile_pic` | Indicates whether your app user's Instagram professional account has a profile picture. |
| `id`  Public | App-scoped User ID. Available for Page-backed Instagram accounts. |
| `is_published` | Indicates whether your app user's Instagram account is published. Available for Page-backed Instagram accounts. |
| `legacy_instagram_user_id` | Your app user's Instagram ID that was created for Marketing API endpoints for v21.0 and older. Available for Page-backed Instagram accounts. |
| `media_count`  Public | Total number of IG Media published on your app user's account. |
| `name` | Your app user's Instagram profile name. |
| `profile_picture_url` | Your app user's Instagram profile picture URL. |
| `collaborative_media_search` | Look up a specific collaborative media by ID. Access via field expansion. Available for Instagram API with Facebook Login only. |
| `shopping_product_tag_eligibility` | Returns `true` if your app user has set up an [Instagram Shop](https://l.facebook.com/l.php?u=https%3A%2F%2Fhelp.instagram.com%2F1187859655048322%2F&h=AUB3zOSVlr6Rj0dNWcw6DAYr3Mn4LM02kPX8c70BkrVAG4-rDaNjD7Ab2sv9zF2BOciwqyytEZ27L9bs6O3KGVchOHROLb3me3wtyuywAG59KfSjAQzxYiCGO2vQs2ctrk66uzUZ-5pcxA) and is therefore eligible for product tagging, otherwise returns `false`. |
| `username`  Public | Your app user's Instagram profile username. |
| `website`  Public | Your app user's website URL. |

### Edges

| Edge | Description |
| --- | --- |
| [`agencies`](https://developers.facebook.com/docs/instagram-api/reference/ig-user/agencies) | A list of businesses that can advertise for this Instagram professional account. |
| [`authorized_adaccounts`](https://developers.facebook.com/docs/instagram-api/reference/ig-user/authorized-adaccounts) | Ad accounts that can advertise for this Instagram professional account. |
| [`business_discovery`](https://developers.facebook.com/docs/instagram-api/reference/ig-user/business_discovery) | Get data about other Instagram Business or Instagram Creator [IG Users](https://developers.facebook.com/docs/instagram-api/reference/ig-user). |
| [`connected_threads_user`](https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/connected_threads_user) | Represents a Threads account connected to an Instagram account. |
| [`content_publishing_limit`](https://developers.facebook.com/docs/instagram-api/reference/ig-user/content_publishing_limit) | Represents an [IG User's](https://developers.facebook.com/docs/instagram-api/reference/ig-user) current [content publishing](https://developers.facebook.com/docs/instagram-api/guides/content-publishing) usage. |
| [`insights`](https://developers.facebook.com/docs/instagram-api/reference/ig-user/insights) | Represents social interaction metrics on an [IG User](https://developers.facebook.com/docs/instagram-api/reference/ig-user). |
| [`instagram_backed_threads_user`](https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/instagram_backed_threads_user) | Represents a Threads account backed by an Instagram account. |
| [`live_media`](https://developers.facebook.com/docs/instagram-api/reference/ig-user/live_media) | Represents a collection of live video [IG Media](https://developers.facebook.com/docs/instagram-api/reference/ig-media) on an [IG User](https://developers.facebook.com/docs/instagram-api/reference/ig-user). |
| [`media`](https://developers.facebook.com/docs/instagram-api/reference/ig-user/media) | Represents a collection of [IG Media](https://developers.facebook.com/docs/instagram-api/reference/ig-media) on an [IG User](https://developers.facebook.com/docs/instagram-api/reference/ig-user). |
| [`media_publish`](https://developers.facebook.com/docs/instagram-api/reference/ig-user/media_publish) | Publish an [IG Container](https://developers.facebook.com/docs/instagram-api/reference/ig-container) on an Instagram Business [IG User](https://developers.facebook.com/docs/instagram-api/reference/ig-user). |
| [`mentions`](https://developers.facebook.com/docs/instagram-api/reference/ig-user/mentions) | Create an [IG Comment](https://developers.facebook.com/docs/instagram-api/reference/ig-comment) on an IG Comment or captioned [IG Media](https://developers.facebook.com/docs/instagram-api/reference/ig-media) that an [IG User](https://developers.facebook.com/docs/instagram-api/reference/ig-user) has been @mentioned in by another Instagram user. |
| [`mentioned_comment`](https://developers.facebook.com/docs/instagram-api/reference/ig-user/mentioned_comment) | Get data on an [IG Comment](https://developers.facebook.com/docs/instagram-api/reference/ig-comment) in which an [IG User](https://developers.facebook.com/docs/instagram-api/reference/ig-user) has been @mentioned by another Instagram user. |
| [`mentioned_media`](https://developers.facebook.com/docs/instagram-api/reference/ig-user/mentioned_media) | Get data on an [IG Media](https://developers.facebook.com/docs/instagram-api/reference/ig-media) in which an [IG User](https://developers.facebook.com/docs/instagram-api/reference/ig-user) has been @mentioned in a caption by another Instagram user. |
| [`recently_searched_hashtags`](https://developers.facebook.com/docs/instagram-api/reference/ig-user/recently_searched_hashtags) | Get [IG Hashtags](https://developers.facebook.com/docs/instagram-api/reference/ig-hashtag) that an [IG User](https://developers.facebook.com/docs/instagram-api/reference/ig-user) has searched for within the last 7 days. |
| [`stories`](https://developers.facebook.com/docs/instagram-api/reference/ig-user/stories) | Represents a collection of story [IG Media](https://developers.facebook.com/docs/instagram-api/reference/ig-media) objects on an [IG User](https://developers.facebook.com/docs/instagram-api/reference/ig-user). |
| [`tags`](https://developers.facebook.com/docs/instagram-api/reference/ig-user/tags) | Represents a collection of [IG Media](https://developers.facebook.com/docs/instagram-api/reference/ig-media) in which an [IG User](https://developers.facebook.com/docs/instagram-api/reference/ig-user) has been tagged by another Instagram user. |
| [`upcoming_events`](https://developers.facebook.com/docs/instagram-api/reference/ig-user/upcoming-events) | A list of events this Instagram professional account is hosting. |
| [`collaboration_invites`](https://developers.facebook.com/docs/instagram-api/reference/ig-user/collaboration_invites) | Represents a collection of [`IG Media`](https://developers.facebook.com/docs/instagram-api/reference/ig-media) object attributes (media\_id, media\_owner\_username, caption, media\_url) for which the IG user has been invited for collaboration. |
| [`collaborative_media`](https://developers.facebook.com/docs/instagram-api/reference/ig-user/collaborative_media) | Represents a collection of [IG Media](https://developers.facebook.com/docs/instagram-api/reference/ig-media) where the IG User is an accepted collaborator. Does not include media the user owns directly. Available for Instagram API with Facebook Login only. |

### Response

A JSON-formatted object containing default and requested [fields](#fields) and [edges](#edges).

```
{
  "<FIELD>":"<VALUE>",
  ...
}
```

### cURL Example

#### Request

```
curl -X GET \
  'https://graph.facebook.com/v25.0/17841405822304914?fields=biography%2Cid%2Cusername%2Cwebsite&access_token=EAACwX...'
```

#### Response

```
{
  "biography": "Dino data crunching app",
  "id": "17841405822304914",
  "username": "metricsaurus",
  "website": "http://www.metricsaurus.com/"
}
```

## Updating

This operation is not supported.

## Deleting

This operation is not supported.
