# Get Started - Instagram Messaging

_Source: https://developers.facebook.com/docs/instagram-messaging/get-started_

---

# Getting Started

This document explains how to successfully call Messenger API support for Instagram (also known as Instagram Messaging API in our Developer Policies) with your app and get Instagram professional account messages.

**Note:** If your app users don't have a Facebook Page linked to their Instagram professional account, learn more about building an app with [the Instagram API with Instagram Login](https://developers.facebook.com/docs/instagram/platform/instagram-api).

## Before You Start

You will need access to the following:

- An Instagram [professional account](https://www.facebook.com/help/instagram/138925576505882)
- A Facebook Page connected to that [account](https://developers.facebook.com/docs/instagram-api/overview#pages)
- A Meta Developer account that can perform the [`MODERATE` task](https://developers.facebook.com/docs/instagram-api/overview#tasks) on that Page
- A [Meta App](https://developers.facebook.com/docs/apps#register) created with the Facebook Login Use Case and with Basic settings configured

Developers that are new to the Messenger Platform

- Follow the step-by-step guide detailed below on how to generate Page Access Token, webhooks setup.
- Learn about the various [platform features](https://developers.facebook.com/docs/messenger-platform/instagram/features) and adopt those that suit your needs.

Developers with prior experience on the Messenger Platform

- Access token and webhooks concepts are similar. Messenger API support for Instagram will require `instagram_manage_messages` in the Page Access Token and Instagram topic webhooks subscribed.
- Most of the features are similar to Messenger API. Review the details on feature list and adopt those that suits your needs.

### Login Flow

You can use Facebook Login for Business or Business Login for Instagram to ask your app users for the need permissions.

The
[Business Login for Instagram](https://developers.facebook.com/docs/instagram/business-login-for-instagram) flow allows a person to complete the following during the login flow:

- convert their Instagram account to an Instagram professional account
- create a Facebook Page for their business
- connect that Page to their Instagram professional account

To implement Business Login for Instagram, visit our
[Business Login for Instagram guide](https://developers.facebook.com/docs/instagram/business-login-for-instagram) then return to this guide.

## 1. Get a User Access Token

Make sure you are signed into your Facebook Developer account, then access your app and trigger the Facebook Login modal. Remember, your Facebook Developer account must be able to perform [Tasks](https://developers.facebook.com/docs/pages-api/overview#tasks) with at least "Moderate" level access on the [Facebook Page](https://developers.facebook.com/docs/pages-api/overview) connected to the Instagram account you want to query.

Once you have triggered the modal, click OK to grant your app the `instagram_basic`, `instagram_manage_messages`, and `pages_manage_metadata` permissions.

The API should return a User access token. Capture the token so your app can use it in the next few queries. If you are using the Graph API Explorer, it will be captured automatically and displayed in the Access Token field for reference:

![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/142020930_4059362647408614_1740112770862669549_n.png?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=pqI9XezjoFoQ7kNvwGhIVj3&_nc_oc=AdpI9wrj0cOt4SVFvhRYga_MHL60fiVjLpRHP459LyJMZ9e15OBf1ul0wKaarXg2kzs&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=9IszOGIlgzYmr89IMggwPg&_nc_ss=7b289&oh=00_Af58PqiWL3iiAaAQZAQp7_QPvX3RyQC7ubPuWMwQXFKMdQ&oe=6A1C1984)

## 2. Get the User's Pages

Query the `GET /me/accounts` endpoint (this translates to `GET /{user-id}/accounts`, which perform a GET on the Facebook [User](https://developers.facebook.com/docs/graph-api/reference/user) node, based on your access token).

```
curl -i -X GET \
 "https://graph.facebook.com/v9.0/me/accounts?access_token={access-token}"
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

## 3. Get the Page Access Token

In order to perform various Instagram Messaging API calls, you will need to use the associated Page Access Token (PAT) of the relevant Instagram professional account that has been previously granted via FB login flow.

Send a `GET` request to the `/{page-id}` endpoint using your User access token. For example:

```
curl -i -X GET "https://graph.facebook.com/{page-id}?
  fields=access_token&
  access_token={user-access-token}"
```

On success, your app gets this response:

```
{
  "access_token":"{page-access-token}",
  "id":"{page-id}"
}
```

- If you used a short-lived User access token, the Page access token is valid for only 1 hour.
- If you used a long-lived User access token, the Page access token has no expiration date.

To generate a long-lived Page access token, you can follow the guide [here](https://developers.facebook.com/docs/facebook-login/access-tokens/refreshing/#get-a-long-lived-page-access-token).

## 3a. Get the Page Access Token via Instagram Developer Dashboard Tool

This tool is currently being rolled out to all developers over the coming weeks. If you don't see the settings under the App Dashboard, you can leverage Step 1-5 above to generate Page Access Tokens.

Optionally, if you own the assets(Instagram account and FB page) that you want to onboard to Messenger API support for Instagram, you can leverage the Instagram setup tool under the Developer App Dashboard to allow you to easily setup Page Access Tokens and Webhooks. You can find the tool under Developer app dashboard → Messenger → Instagram Settings. Existing way of configuring tokens and webhook will still work, but this tool will give you an easier way to setup your environment.

![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/196275801_927883678049780_255440934045349593_n.png?_nc_cat=106&ccb=1-7&_nc_sid=e280be&_nc_ohc=bJYYBwOMvTEQ7kNvwGP9ovB&_nc_oc=AdrmgX0O_NvVm0FtqDt_zuYGuNNaafkl857uNh4etfGPG39EArS2TGtoklzEwR-EFko&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=9IszOGIlgzYmr89IMggwPg&_nc_ss=7b289&oh=00_Af4zSEc2vrQJZU3vHWBVZZ9V3hdb4Mk7MBiUDrOEXfFz_Q&oe=6A1C4707)

## 4. Enable Message Control Connected Tools Settings

In order to manage Instagram messages via API, Instagram professional accounts will need to enable the connected tools toggle under message controls settings. This setting can be found by going to:

**Instagram Settings > Messages and story replies >Message controls > Connected Tools > toggle Allow Access to Messages**

## 5. Get the Instagram professional account's Inbox Objects

Use the Page ID you captured and the Page Access Token (PAT) to query the `GET /{page-id}/conversations?platform=instagram` endpoint:

```
curl -i -X GET \
 "https://graph.facebook.com/v9.0/17841405822304914/conversations?platform=instagram&access_token={access-token}"
```

This should return the IDs of all the thread objects on the Instagram user:

```
{
  "data": [
    {
      "id": "aWdfZAG06MTpJR01lc3NhZA2VUaHJlYWQ6OTAwMTAxNDYyOTkyODI6MzQwMjgyMzY2ODQxNzEwMzAwOTQ5MTI4MTM2MDk5MDc1MzYyOTgx"
    },
    {
      "id": "aWdfZAG06MTpJR01lc3NhZA2VUaHJlYWQ6OTAwMTAxNDYyOTkyODI6MzQwMjgyMzY2ODQxNzEwMzAwOTQ5MTI4MTYzMzQ2MzE5NjM1NDcy"
    },
    {
      "id": "aWdfZAG06MTpJR01lc3NhZA2VUaHJlYWQ6OTAwMTAxNDYyOTkyODI6MzQwMjgyMzY2ODQxNzEwMzAwOTQ5MTI4MTk3MTY0NjI2NzAyMjMw"
    },
    {
      "id": "aWdfZAG06MTpJR01lc3NhZA2VUaHJlYWQ6OTAwMTAxNDYyOTkyODI6MzQwMjgyMzY2ODQxNzEwMzAwOTQ5MTI4MzkzNDI5MDYzMzkyNjU0"
    }
}
```

If you can perform this final query successfully, you should be able to perform queries using any of the Messenger API support for Instagram endpoints - just refer to our various guides and references to learn what each endpoint can do and what permission they require.

## Next Steps

- [Develop your app further](https://developers.facebook.com/docs/messenger-platform/instagram/features) so it can successfully use any other endpoints it needs, and keep track of the permissions each endpoint requires
- Complete the [webhook setup](https://developers.facebook.com/docs/messenger-platform/webhooks) so it can receive real time notifications whenever user sends a message to the Instagram professional account.
- Complete the [App Review](https://developers.facebook.com/docs/messenger-platform/instagram/app-review/) process and request approval for all permissions your app will need so your app users can grant them while your app is in production.

### Developer Support

- Use the [Meta Status tool](https://l.facebook.com/l.php?u=https%3A%2F%2Fmetastatus.com%2F&h=AUCRIP4ZvfCzxNtxhQbSq4-crTBt1uOduR65uDut6r48TyADvAbIy8THLd6Ecp3D-kosnq_HKR3tNJAWunl0j2gayTvvd3RQvOsNDSBivCXXBQgJh_Gkyapr2ETN8DRGpd8-CIDO-BtOvA) to check for the status and outages of Meta business products.
- Use the [Meta Developer Support tool](https://developers.facebook.com/support) to report bugs and view reported bugs, get help with Ads or Business Manager, and more.
