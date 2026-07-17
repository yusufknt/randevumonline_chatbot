# Children - Instagram Platform

_Source: https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-media/children_

---

# Children

Represents a collection of [IG Media](https://developers.facebook.com/docs/instagram-api/reference/ig-media) objects on an album [IG Media](https://developers.facebook.com/docs/instagram-api/reference/ig-media).

### Requirements

|  | Instagram AP with Instagram Loging | Instagram API with Facebook Login |
| --- | --- | --- |
| **Access Tokens** | - Instagram User user access token | - [Facebook User access token](https://developers.facebook.com/docs/facebook-login/access-tokens/#usertokens) |
| **Host URL** | `graph.instagram.com` | `graph.facebook.com` |
| **Login Type** | Business Login for Instagram | Facebook Login for Business |
| [**Permissions**](https://developers.facebook.com/docs/permissions/reference#i) | - `instagram_business_basic` | - `instagram_basic` - `pages_read_engagement`   If the app user was granted a role via the Business Manager on the [Page](https://developers.facebook.com/docs/instagram-api/overview#pages) connected to the targeted IG User, you will also need one of:   - `ads_management` - `ads_read` |

## Creating

This operation is not supported.

## Reading

### Getting Child Media Objects

`GET /<IG_MEDIA_ID>/children`

Returns a list of [IG Media](https://developers.facebook.com/docs/instagram-api/reference/ig-media) objects on an album [IG Media](https://developers.facebook.com/docs/instagram-api/reference/ig-media) object.

#### Limitations

- Some fields, such as `permalink`, cannot be used on photos within albums (children).

#### Sample Request

```
GET graph.facebook.com
  /17896450804038745/children
```

#### Sample Response

```
{
  "data": [
    {
      "id": "17880997618081620"
    },
    {
      "id": "17871527143187462"
    }
  ]
}
```

## Updating

This operation is not supported.

## Deleting

This operation is not supported.
