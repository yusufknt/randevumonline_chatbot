# Get Started - Instagram Platform

_Source: https://developers.facebook.com/docs/instagram-platform/instagram-api-with-facebook-login/get-started_

---

# Getting Started

This document explains how to successfully call the Instagram API with Facebook Login for Business with your app and get an Instagram Business or Creator Account's media objects. It assumes you are familiar with and how to perform REST API calls. If you do not have an app yet, you can use the [Graph API Explorer](https://developers.facebook.com/tools/explorer) instead and skip steps 1 and 2.

## Before You Start

You will need access to the following:

- An [Instagram Business Account](https://l.facebook.com/l.php?u=https%3A%2F%2Fhelp.instagram.com%2F502981923235522&h=AUC0khFVuQWDMu89mIq0gdsWLhQKueM3PIsB2XYqv4TxpLDBkqKOIcGwtwcn-LjgFMkFDRuXQQCa50qAw7KRRRnVZmFnVavPLaOlKqPXyhUbBDpoAhgbNZeCVoXCcregVK34HG6YKmolbA) or [Instagram Creator Account](https://l.facebook.com/l.php?u=https%3A%2F%2Fhelp.instagram.com%2F1158274571010880&h=AUBg8XIQUXiP1rtLnS3jXmMOTJdqxZyHqpzasqzdQhfTdvsiCv62JDTLf6xk7LZUKXAVN6kTkBSEegWvFiol39DQw2JZvzqjmOk3W9rqeBHufSoLf6FA15fWMQ_s7ooAH0ODk8jFmTlKcg)
- A [Facebook Page connected to that account](https://developers.facebook.com/docs/instagram-api/overview#pages)
- A Facebook Developer account that can perform [Tasks on that Page](https://developers.facebook.com/docs/instagram-api/overview#tasks)
- A [registered Facebook App](https://developers.facebook.com/docs/development/register) with **Basic** settings configured

## 1. Configure Facebook Login for Business

Add the Facebook Login product to your app in the App Dashboard.

You can leave all settings on their defaults. If you are implementing Facebook Login for Business manually (which we don't recommend), enter your `redirect_uri` in the **Valid OAuth redirect URIs** field. If you will be using one of our SDKs, you can leave it blank.

## 2. Implement Facebook Login for Business

Follow our [Facebook Login for Business documentation](https://developers.facebook.com/docs/facebook-login-for-business) for your platform and implement the login into your app. Set up your implementation to request these permissions:

- [`instagram_basic`](https://developers.facebook.com/docs/apps/review/login-permissions#instagram-basic)
- [`pages_show_list`](https://developers.facebook.com/docs/apps/review/login-permissions#pages-show-list)

## 3. Get a User Access Token

Once you've implemented Facebook Login for Business, make sure you are signed into your Facebook Developer account, then access your app and trigger the Facebook Login for Business modal. Remember, your Facebook Developer account must be able to perform [Tasks](https://developers.facebook.com/docs/instagram-api/overview#tasks) on the [Facebook Page](https://developers.facebook.com/docs/instagram-api/overview#pages) connected to the Instagram account you want to query.

Once you have triggered the modal, click **OK** to grant your app the `instagram_basic` and `pages_show_list` permissions.

The API should return a User access token. Capture the token so your app can use it in the next few queries. If you are using the Graph API Explorer, it will be captured automatically and displayed in the **Access Token** field for reference:

![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/57308062_276123556625959_4652658984229011456_n.png?_nc_cat=110&ccb=1-7&_nc_sid=e280be&_nc_ohc=lkdmPmt5s7sQ7kNvwFfatW5&_nc_oc=AdpwOlLRrCzeMw852NiDoLxs4xyXQG0uFfQfwHpnv40Pel-llkvQHZiUa50Eynk6CRI&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=5c9K8Rb5BpjEPSDN9j3iQg&_nc_ss=7b289&oh=00_Af7wpqVRqUsLv_NqjPRpJOYsMwxV49SCS3tu2znH4MVncg&oe=6A1BFEDF)

## 4. Get the User's Pages

Query the `GET /me/accounts` endpoint (this translates to `GET /{user-id}/accounts`, which perform a `GET` on the Facebook [User](https://developers.facebook.com/docs/graph-api/reference/user) node, based on your access token).

```
curl -i -X GET \
 "https://graph.facebook.com/v25.0/me/accounts?access_token={access-token}"
```

This should return a collection of Facebook Pages that the current Facebook User can perform the `MANAGE`, `CREATE_CONTENT`, `MODERATE`, or `ADVERTISE` tasks on:

```
{
  "data": [
    {
      "access_token": "EAAJjmJ...",
      "category": "App Page",
      "category_list": [
        {
          "id": "2301",
          "name": "App Page"
        }
      ],
      "name": "Metricsaurus",
      "id": "134895793791914",  // capture the Page ID
      "tasks": [
        "ANALYZE",
        "ADVERTISE",
        "MODERATE",
        "CREATE_CONTENT",
        "MANAGE"
      ]
    }
  ]
}
```

Capture the ID of the Facebook Page that's connected to the Instagram account that you want to query. Keep in mind that your app users may be able to perform tasks on multiple pages, so you eventually will have to introduce logic that can determine the correct Page ID to capture (or devise a UI where your app users can identify the correct Page for you).

![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/57437240_2085096038272793_3947769475595501568_n.png?_nc_cat=106&ccb=1-7&_nc_sid=e280be&_nc_ohc=ApKx-MLyK7EQ7kNvwHfRHfC&_nc_oc=AdqHbSI4zojyFEOjB4XWjvxDrKb2yeXe-1ASwbCAEKIBAG0wKVYRsK3ClzCXhTwqSSs&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=5c9K8Rb5BpjEPSDN9j3iQg&_nc_ss=7b289&oh=00_Af53SZw8A9XKSGwkdP_3UYJNZ0L6gurS8cX9j1FDTXz5yg&oe=6A1BEE06)

## 5. Get the Page's Instagram Business Account

Use the Page ID you captured to query the `GET /{page-id}?fields=instagram_business_account` endpoint:

```
curl -i -X GET \
 "https://graph.facebook.com/v25.0/134895793791914?fields=instagram_business_account&access_token={access-token}"
```

This should return the [IG User](https://developers.facebook.com/docs/instagram-api/reference/ig-user) — an Instagram Business or Creator Account — that's connected to the Facebook Page.

```
{
  "instagram_business_account": {
    "id": "17841405822304914"  // Connected IG User ID
  },
  "id": "134895793791914"  // Facebook Page ID
}
```

Capture the [IG User](https://developers.facebook.com/docs/instagram-api/reference/ig-user) ID.

![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/57462471_316665542380805_102061440998834176_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=VW8N09DGJDwQ7kNvwG-MKiG&_nc_oc=AdpxgA3p-kNZdEfu3hsaWW4LOVdSUKE9QkSa2mYcz1SndNzLj3yAA-iOQO2GJsHD80U&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=5c9K8Rb5BpjEPSDN9j3iQg&_nc_ss=7b289&oh=00_Af5j67xhd6IORjfS4EqZrXlGEb0Q3aHUarhhBUR3apQz-g&oe=6A1BD339)

## 6. Get the Instagram Business Account's Media Objects

Use the [IG User](https://developers.facebook.com/docs/instagram-api/reference/ig-user) ID you captured to query the `GET /{ig-user-id}/media` endpoint:

```
curl -i -X GET \
 "https://graph.facebook.com/v25.0/17841405822304914/media?access_token={access-token}"
```

This should return the IDs of all the [IG Media](https://developers.facebook.com/docs/instagram-api/reference/ig-media) objects on the [IG User](https://developers.facebook.com/docs/instagram-api/reference/ig-user):

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

![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/57261700_588761411631102_2933352179429277696_n.png?_nc_cat=110&ccb=1-7&_nc_sid=e280be&_nc_ohc=p9ZnNCSTj6oQ7kNvwFbVaTQ&_nc_oc=AdpECR_GhII5lDKHF0URDEuLzfKCQJNJVGTPCoMRjJWk6HUNtcFhkwcO2yW-upYzSf8&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=5c9K8Rb5BpjEPSDN9j3iQg&_nc_ss=7b289&oh=00_Af4I8J3T60GrTUfoJwPphejuPitbrIPkGWpfgsTBMkrxPA&oe=6A1BCB3D)

If you are able to perform this final query successfully, you should be able to perform queries using any of the Instagram Platform endpoints — just refer to our various guides and references to learn what each endpoint can do and what permissions they require.

## Next Steps

- Develop your app further so it can successfully use any other endpoints it needs, and keep track of the permissions each endpoint requires
  - If you plan to implement [Instagram Messaging from Messenger Platform](https://developers.facebook.com/docs/messenger-platform/instagram) you will need additional permissions
- Complete the [App Review](https://developers.facebook.com/docs/instagram-api/overview#app-review) process and request approval for all of the permissions your app will need so your app users can grant them while your app is in [Live Mode](https://developers.facebook.com/docs/development/build-and-test/app-modes#live-mode)
- Switch your app to Live Mode and market it to potential users

Once your app is in Live Mode, any Facebook User who you've made your app available to can access an Instagram Business or Creator Account's data, as long as they have a Facebook User account that can perform Tasks on the Page connected to that Instagram Business or Creator Account.
