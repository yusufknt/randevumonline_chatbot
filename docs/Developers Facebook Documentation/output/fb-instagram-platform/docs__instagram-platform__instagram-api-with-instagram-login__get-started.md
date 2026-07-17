# Get started - Instagram Platform

_Source: https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/get-started_

---

# Get Started

This document explains how to make your first call using the Instagram API with Instagram Login to obtain information about your Instagram professional account, including your User ID, username, and media objects.

## Before You Start

This guide assumes you have read the [Instagram Platform Overview](https://developers.facebook.com/docs/instagram-platform/overview) and implemented the needed components for using this API, such as a Meta login flow and a webhooks server to receive notifications.

If your current Meta app type is **not** a Business type app you will need to create a new app and [select **Business** during the creation process.![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/310307727_3347317042262105_1088877051262827250_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=5SvUa0KxdZkQ7kNvwHcqah0&_nc_oc=AdpNPlkM5xCl8ncqAEi0DvJzLsMMV09WvXL6Z1STXmvsbKMnBfs-2mixKR1O9x9_AAg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=Z45HMjsBCFTFg7lns8n7Qw&_nc_ss=7b289&oh=00_Af4yhC6wZz-wbMGqrMGSeEKeWxLUE8Hos-cWYITlYtS81g&oe=6A1BE7E2)](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/create-a-meta-app-with-instagram#step-4--select-your-app-type) If this new app needs Advanced Access, App Review is required.

## Get an access token

An access token contains information about the app making the request, the token's expiration date, the app user's Instagram User ID and the permissions the user has granted the app. You can get an Instagram user access token using one of the following methods:

**[Business Login for Instagram
![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/310307727_3347317042262105_1088877051262827250_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=5SvUa0KxdZkQ7kNvwHcqah0&_nc_oc=AdpNPlkM5xCl8ncqAEi0DvJzLsMMV09WvXL6Z1STXmvsbKMnBfs-2mixKR1O9x9_AAg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=Z45HMjsBCFTFg7lns8n7Qw&_nc_ss=7b289&oh=00_Af4yhC6wZz-wbMGqrMGSeEKeWxLUE8Hos-cWYITlYtS81g&oe=6A1BE7E2)](https://developers.facebook.com/docs/instagram/platform/instagram-api/business-login)**

If you have implemented Business Login for Instagram into your app, log in to your app.

**[App Dashboard
![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/310307727_3347317042262105_1088877051262827250_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=5SvUa0KxdZkQ7kNvwHcqah0&_nc_oc=AdpNPlkM5xCl8ncqAEi0DvJzLsMMV09WvXL6Z1STXmvsbKMnBfs-2mixKR1O9x9_AAg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=Z45HMjsBCFTFg7lns8n7Qw&_nc_ss=7b289&oh=00_Af4yhC6wZz-wbMGqrMGSeEKeWxLUE8Hos-cWYITlYtS81g&oe=6A1BE7E2)](https://developers.facebook.com/apps)**

If you have not implemented Business Login for Instagram, Get an access token via the App Dashboard.

1. In your app dashboard, click **Instagram > API setup with Instagram business login** in the left side menu.
2. Click **Generate token** next to the Instagram account you want to access.
3. Log into Instagram.
4. Copy the access token.

Access tokens from the business login flow are short-lived and valid for 1 hour. Access tokens from the App Dashboard are long-lived and are valid for 60 days. [Learn how to extend the expiry of any access token.](https://developers.facebook.com/docs/instagram/platform/instagram-api/business-login#get-a-long-lived-access-token)

## Get the app user ID & username

To obtain your app user's Instagram professional account user ID and username, send a `GET` request to the `/me` endpoint with the following parameters:

- `fields` set to a comma-separated list with `user_id` and `username`
- `access_token` set to the access token from the app dashboard

**Note:** The `/me` endpoint represents the app user's ID received from the access token, in this example, your user ID.

### Example request

*Formatted for readability.*

```
curl -i -X GET \
 "https://graph.instagram.com/v25.0/me
      ?fields=user_id,username
      &access_token=Ealkdfj..."
```

On success, your app receives a JSON object with the app user's Instagram user ID and the username of the Instagram professional account.

```
{
  "data": [
    {
      "user_id": "<IG_ID>"
      "username": "<IG_USERNAME>"
    }
  ]
}
```

### Fields

You can use the `fields` query string parameter to request the following fields on a User.

| Field Name | Description |
| --- | --- |
| `id` | The app user's app-scoped ID |
| `user_id` | The Instagram professional acount ID, `<IG_ID>`, for your app user. This ID is value of the `id` field received in webhook notifications for this account. |
| `username` | The app user's Instagram username. |
| `name` | The app user's name |
| `account_type` | The app user's account type. Can be `Business` or `Media_Creator`. |
| `profile_picture_url` | The URL for the app user's profile picture. |
| `followers_count` | The number of followers of the app user's Instagram professional account |
| `follows_count` | The number of Instagram accounts the app user's Instagram professional account follows |
| `media_count` | The number of Media object on the User |

## Get an app user's media objects

To get media objects, send a `GET` request to the `/<IG_ID>/media` endpoint.

### Example request

*Formatted for readability.*

```
curl -i -X GET \
 "https://graph.instagram.com/v25.0/<IG_ID>/media?access_token=<INSTAGRAM_USER_ACCESS_TOKEN>"
```

On success your app receives a JSON object with the IDs of all the [IG Media](https://developers.facebook.com/docs/instagram-api/reference/ig-media) objects on the [IG User](https://developers.facebook.com/docs/instagram-api/reference/ig-user):

```
{
  "data": [
    {
      "id": "17918195224117851"
    },
    {
      "id": "17895695668004550"
    },
    {
      "id": "17899305451014820"
    },
    {
      "id": "17896450804038745"
    },
    {
      "id": "17881042411086627"
    },
    {
      "id": "17869102915168123"
    }
  ],
  "paging": {
    "cursors": {
      "before": "QVFIUkdGRXA2eHNNTUs4T1ZAXNGFxQTAtd3U4QjBLd1B2NXRMM1NkcnhqRFdBcEUzSDVJZATFoLWtXMWZAGU2VrRTk2RHVtTVlDckI2NjN0UERFa2JrUk4yMW13",
      "after": "QVFIUmlwbnFsM3N2cV9lZAFdCa0hDeV9qMVliT0VuMmJyNENxZA180c0t6VjFQVEJaTE9XV085aU92OUFLNFB6Szd2amo5aV9rTlVBcnNlWmEtMzYxcE1HSFR3"
    }
  }
}
```

If you are able to perform this final query successfully, you should be able to perform queries using any of the Instagram API with Instagram Login endpoints — just see our various guides and references to learn what each endpoint can do and what permissions they require.

## Next Steps

Now that you know how to get access tokens and Instagram User IDs for your app users, learn how to [subscribe your app users to Instagram webhooks notifications.](https://developers.facebook.com/docs/instagram/platform/instagram-api/webhooks)
