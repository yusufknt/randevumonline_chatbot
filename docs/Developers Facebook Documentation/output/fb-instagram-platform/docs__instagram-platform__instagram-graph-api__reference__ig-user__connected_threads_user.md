# Connected Threads User - Instagram Platform

_Source: https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/connected_threads_user_

---

# IG User Connected Threads User

Represents a [Threads account connected to an Instagram account](https://developers.facebook.com/docs/marketing-api/ad-creative/threads-ads#instagram-connected-threads-accounts).

### Requirements

| Type | Description |
| --- | --- |
| [Permissions](https://developers.facebook.com/docs/apps/review/login-permissions) | - [`instagram_basic`](https://developers.facebook.com/docs/facebook-login/permissions#instagram_basic) - [`threads_business_basic`](https://developers.facebook.com/docs/facebook-login/permissions#threads_business_basic) - [`pages_read_engagement`](https://developers.facebook.com/docs/permissions#pages_read_engagement)   If the app user was granted a role via the Business Manager on the [Page](https://developers.facebook.com/docs/instagram-api/overview#pages) connected to your app user's Instagram professional account, your app will also need one of:   - [`ads_management`](https://developers.facebook.com/docs/facebook-login/permissions#ads_management) - [`ads_read`](https://developers.facebook.com/docs/facebook-login/permissions#ads_read) |
| [Tokens](https://developers.facebook.com/docs/facebook-login/access-tokens) | A Facebook User [access token](https://developers.facebook.com/docs/instagram-api/overview#authentication). |

### Limitations

- You need to have at least an Advertiser role on the [Page that is linked to your Instagram account](https://developers.facebook.com/docs/instagram/ads-api/guides/pages-ig-account#via_page); Manager or Content Creator also work. Or you need to have the Instagram account [connected to a business account](https://developers.facebook.com/docs/instagram/ads-api/guides/ig-accounts-with-business-manager#claim_account) where you have appropriate roles.
- If you want to use this Threads account ID for Threads ads creation, make sure your connected Instagram account has the correct ads creation identity setup, either [business-claimed Instagram account](https://developers.facebook.com/docs/instagram/ads-api/guides/ig-accounts-with-business-manager) or [page-connected Instagram account](https://developers.facebook.com/docs/instagram/ads-api/guides/pages-ig-account).
- An Instagram account can have only one Instagram-connected Threads account. [Verify whether a specific Instagram account has an Instagram-connected Threads account](#reading) before attempting to create a new one. If one already exists, use that one.

## Reading

`GET /{ig-user-id}/connected_threads_user`

Once you [connect a Threads account to a valid Instagram account](https://l.facebook.com/l.php?u=https%3A%2F%2Fhelp.instagram.com%2F1747515265645443&h=AUCBT9quEebPcs5a0Gp5rM3ncuVAtCPwspa3dfYjoIF_Wt9EtRusAy_L5Dqs0Zb1X91miqX12O4wTeTho68qgLIZIoohds_3yB92v34i1bje-j3pDuOkaozTREY62RMPH_Syczm7bb8NwA), you can make an API request to get the Threads account ID.

### Sample request

```
curl -G \
  -d "access_token=<ACCESS_TOKEN>"\
  -d "fields=threads_user_id" \
"https://graph.facebook.com/v25.0/<IG_USER_ID>/connected_threads_user"
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

This operation is not supported.

## Updating

This operation is not supported.

## Deleting

This operation is not supported.
