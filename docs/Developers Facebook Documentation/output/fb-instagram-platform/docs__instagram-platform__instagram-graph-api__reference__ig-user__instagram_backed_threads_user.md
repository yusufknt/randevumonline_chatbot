# Instagram-Backed Threads User - Instagram Platform

_Source: https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/instagram_backed_threads_user_

---

# IG User Instagram-Backed Threads User

Represents a [Threads account backed by an Instagram account](https://developers.facebook.com/docs/marketing-api/ad-creative/threads-ads#instagram-backed-threads-accounts).

You cannot log into Instagram-backed Threads accounts to manage posts.

### Requirements

| Type | Description |
| --- | --- |
| [Permissions](https://developers.facebook.com/docs/apps/review/login-permissions) | - [`instagram_basic`](https://developers.facebook.com/docs/facebook-login/permissions#instagram_basic) - [`threads_business_basic`](https://developers.facebook.com/docs/facebook-login/permissions#threads_business_basic) - [`pages_read_engagement`](https://developers.facebook.com/docs/permissions#pages_read_engagement)   If the app user was granted a role via the Business Manager on the [Page](https://developers.facebook.com/docs/instagram-api/overview#pages) connected to your app user's Instagram professional account, your app will also need one of:   - [`ads_management`](https://developers.facebook.com/docs/facebook-login/permissions#ads_management) - [`ads_read`](https://developers.facebook.com/docs/facebook-login/permissions#ads_read) |
| [Tokens](https://developers.facebook.com/docs/facebook-login/access-tokens) | A Facebook User [access token](https://developers.facebook.com/docs/instagram-api/overview#authentication). |

### Limitations

- You need to have at least an Advertiser role on the [Page that is linked to your Instagram account](https://developers.facebook.com/docs/instagram/ads-api/guides/pages-ig-account#via_page); Manager or Content Creator also work. Or you need to have the Instagram account [connected to a business account](https://developers.facebook.com/docs/instagram/ads-api/guides/ig-accounts-with-business-manager#claim_account) where you have appropriate roles.
- If you want to use this Threads account ID for Threads ads creation, make sure your Instagram account has the correct ads creation identity setup, either [business-claimed Instagram account](https://developers.facebook.com/docs/instagram/ads-api/guides/ig-accounts-with-business-manager) or [page-connected Instagram account](https://developers.facebook.com/docs/instagram/ads-api/guides/pages-ig-account).
- An Instagram account can have only one Instagram-backed Threads account. [Verify whether a specific Instagram accounts has an Instagram-backed Threads account](#reading) before attempting to create a new one. If one already exists, use that one.

## Reading

`GET /{ig-user-id}/instagram_backed_threads_user`

You can make an API request to get the Instagram-backed Threads account ID.

### Sample request

```
curl -G \
  -d "access_token=<ACCESS_TOKEN>"\
  -d "fields=threads_user_id" \
"https://graph.facebook.com/v25.0/<IG_USER_ID>/instagram_backed_threads_user"
```

### Sample response

```
{
  "data": [
    {
      "threads_user_id": "<THREADS_USER_ID>",
    }
  ],
}
```

## Creating

`POST /{ig-user-id}/instagram_backed_threads_user`

You can make an API call to create an Instagram-backed Threads account specifically for running ads on Threads.

### Sample request

```
curl \
  -F "access_token=<ACCESS_TOKEN>"\
"https://graph.facebook.com/v25.0/<IG_USER_ID>/instagram_backed_threads_user"
```

### Sample response

```
{
  "data": [
    {
      "threads_user_id": "<THREADS_USER_ID>",
    }
  ],
}
```

## Updating

This operation is not supported.

## Deleting

This operation is not supported.
