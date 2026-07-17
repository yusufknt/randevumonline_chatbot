# Migration Guide - Instagram Platform

_Source: https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/migration-guide_

---

# Migrate your App

This guide will help you determine whether you should migrate your existing app to the new Instagram product and how to implement it.

## Why migrate your app

The Instagram API with Instagram Login offers a streamlined and efficient way for your app users to manage their Instagram professional accounts without the need for a Facebook Page or Facebook presence. With only two permissions required for each functionality – `instagram_business_basic` and the permission specific to messaging, comment moderation, or content publishing – the onboarding process has been significantly simplified, going from an average of 12 steps to just two. As a result, we've seen a significant improvement in onboarding success rates.

## Should you migrate your app

Use the following table to determine if you should implement the Instagram product into your app:

| Component | [Instagram API setup with Instagram Login](https://developers.facebook.com/docs/instagram/platform/instagram-api) | [Instagram API setup with Facebook Login](https://developers.facebook.com/docs/instagram-platform/instagram-graph-api) |
| --- | --- | --- |
| **Access token type** | Instagram User | Facebook User or Page |
| **Authorization type** | [Business Login for Instagram](https://developers.facebook.com/docs/instagram/platform/instagram-api/business-login) | [Facebook Login for Business](https://developers.facebook.com/docs/facebook-login/facebook-login-for-business/) |
| **Comment moderation** |  |  |
| **Content publishing** |  |  |
| **Facebook Page** | x | Required |
| **Hashtag search** | x |  |
| [**Insights**](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-facebook-login/insights) |  |  |
| **Mentions** |  |  |
| **Messaging** |  | [via Messenger Platform](https://developers.facebook.com/docs/messenger-platform/instagram) |
| [**Product tagging**](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-facebook-login/product-tagging) | x |  |
| [**Partnership Ads**](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-facebook-login/partnership-ads) | x |  |

## Migration Steps

You will need to take the following steps to migrate your app.

### Step 1. Add Instagram

Follow the [Create a Meta app with Instagram guide
![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/310307727_3347317042262105_1088877051262827250_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=5SvUa0KxdZkQ7kNvwHcqah0&_nc_oc=AdpNPlkM5xCl8ncqAEi0DvJzLsMMV09WvXL6Z1STXmvsbKMnBfs-2mixKR1O9x9_AAg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=f2bR40gUmG4d1RlKC-Y95A&_nc_ss=7b289&oh=00_Af6wZCObAsgOihADDfGeAHKWN9Ox1HkMmBcsVlJ5dAQm7Q&oe=6A1BE7E2)](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/create-a-meta-app-with-instagram/) to add the Instagram product to your existing business type app.

If your current Meta app type is **not** a Business type app you will need to create a new app and [select **Business** during the creation process.![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/310307727_3347317042262105_1088877051262827250_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=5SvUa0KxdZkQ7kNvwHcqah0&_nc_oc=AdpNPlkM5xCl8ncqAEi0DvJzLsMMV09WvXL6Z1STXmvsbKMnBfs-2mixKR1O9x9_AAg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=f2bR40gUmG4d1RlKC-Y95A&_nc_ss=7b289&oh=00_Af6wZCObAsgOihADDfGeAHKWN9Ox1HkMmBcsVlJ5dAQm7Q&oe=6A1BE7E2)](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/create-a-meta-app-with-instagram#step-4--select-your-app-type)

If this new app needs Advanced Access, [App Review ![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/310307727_3347317042262105_1088877051262827250_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=5SvUa0KxdZkQ7kNvwHcqah0&_nc_oc=AdpNPlkM5xCl8ncqAEi0DvJzLsMMV09WvXL6Z1STXmvsbKMnBfs-2mixKR1O9x9_AAg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=f2bR40gUmG4d1RlKC-Y95A&_nc_ss=7b289&oh=00_Af6wZCObAsgOihADDfGeAHKWN9Ox1HkMmBcsVlJ5dAQm7Q&oe=6A1BE7E2)](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/create-a-meta-app-with-instagram#step-10--complete-app-review) is required and will be handled within the Instagram product flow instead of the App Review item in the left side dashboard menu.

You will configure:

- Instagram Login for Business
- Permissions and features
- Webhooks

### Step 2. Update your code

1. Copy and paste the **Embed URL** in an anchor tag or button on your app or website to launch the Business Login for Instagram flow. This flow will give your app an Instagram User access token.
2. Update the host URL in your code so that your API calls use `graph.instagram.com`.
3. Update your API calls to use an Instagram User access token. This will update the `/me` endpoint calls to use an Instagram Professional account ID instead of a Facebook Page ID
4. Replace your Meta app ID and app secret with the Instagram app ID and secret found in the app dashboard; **Instagram > API setup with Instagram login > 3. Set up Instagram business login > Business login settings**.
