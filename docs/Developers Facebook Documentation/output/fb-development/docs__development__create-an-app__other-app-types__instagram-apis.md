# Instagram Platform - App Development with Meta

_Source: https://developers.facebook.com/docs/development/create-an-app/other-app-types/instagram-apis_

---

# Create a Meta App for Instagram Platform

This guide shows you how to create and customize a Meta app for your Instagram app in the App Dashboard.

### Before you Start

This guide assumes that you have read and implemented the requirements for [creating an app with Meta](https://developers.facebook.com/docs/development/create-an-app).

### Add to an existing app

If you are adding Instagram to an existing app, please start with [Step 6](#add-ig).

## 1. Start the app creation process

There are a number of ways to start the app creation flow.

- If you just came from the registration flow, click the **Create First App** button
- If you are on the App Dashboard, click **Create App** in the upper-right
- If you are on the dashboard for an existing app and want to create a new app, select the dropdown menu in the upper-left, and click the **Create New App** button

[Launch the Meta App Dashboard](https://developers.facebook.com/apps)

If you are unable to create an app, you might have reach the app limit. You are permitted to have a **developer or administrator role on a maximum of 15 apps** that are not already connected to a Meta Verified Business Account. If you have reached the app limit and are unable to create an application or accept a new pending role, take the following steps in the apps dashboard:

- Connect a [verified business portfolio](https://developers.facebook.com/docs/development/release/business-verification) to any apps that are not already connected to one.
- Remove any old or unused apps – Archived apps count towards the app limit; if you no longer require these apps, we suggest removing them
- Remove yourself as an administrator or developer from an app

## Step 2: Connect a business

You're required to connect your app to a business that has completed Business Verification before you can publish your app. However, you can connect a business now or at any time during the development process by clicking **App settings > Basic** in the left-side menu.

1. Select an option and click **Next**.

Learn more about
[Business Verification.
![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/310307727_3347317042262105_1088877051262827250_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=5SvUa0KxdZkQ7kNvwHcqah0&_nc_oc=AdpNPlkM5xCl8ncqAEi0DvJzLsMMV09WvXL6Z1STXmvsbKMnBfs-2mixKR1O9x9_AAg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=FMY_WpGp0_iyCtdjRenVnQ&_nc_ss=7b289&oh=00_Af7Q86ZwQUzqfij4Ql_LPI0YP0c-DZ36UVEqyR7RCLlZWA&oe=6A1BE7E2)](https://developers.facebook.com/docs/development/release/business-verification/)

## Step 3: Select your use case

To create an app that can access the Instagram product follow these steps:

1. Select the **Other** use case.
2. Click the **Next**.

## Step 4: Select your app type

Your app must be a business type app to be able to add the Instagram product.

1. Select **Business**.
2. Click **Next**.

## Step 5: Add app details

Add some details about your app.

1. **Add an app name** that will appear in the app dashboard.
2. **Add contact email** that Meta will use to contact you about your app.
3. Click **Next**.

You will be redirected to the app dashboard for your new app with products you can add to your app.

## Step 6. Add the Instagram product to your app

Add the Instagram product to your app by following these steps:

1. Scroll until you see the **Instagram** product. This allows Allow creators and businesses to manage messages and comments, publish content, track insights, hashtags and mentions.
2. Click **Set up**.

**API setup with Instagram login** is automatically added to your app. This allows your app users to log in to your app using their Instagram credentials. This setup allows you to build an app that can publish to Instagram, manage comments on Instagram media, and send and receive messages from people interested in your app user's Instagram social media using the Instagram API.

If you are building an app for a business that uses an Instagram Professional account that is linked to a Facebook Page select the **API setup with Facebook login**. This setup allows you to build an app that can publish content to Instagram and manage comments on Instagram media, for product tagging, Partnership Ads, and get metrics. Continue to the [API Setup with Facebook Login Developer Documentation](https://developers.facebook.com/docs/instagram-platform) to complete the set up.

## Step 7. Generate access tokens

Assign an Instagram account to get access tokens for testing Instagram API calls and webhooks subscriptions.

1. Add an Instagram account. This account must be public. Multiple accounts can be added for multiple testers.
2. You will be prompted to login to your Instagram account.

You can add or remove accounts at any time by clicking **App Roles > Roles** or **Instagram > API Setup with Instagram login** in the left-side menu.

### Step 8. Configure webhooks

Meta Webhooks allow you to receive real-time HTTP notifications of changes to specific objects in the Meta social graph. To use webhooks, please provide a callback URL for your app.

1. Click **Configure**.
2. Add your **Callback URL**.
3. Add your **Verify token**.
4. Click **Save**.
5. Click **Manage** to unsubscribe or change testing and subscription versions.

By default you are subscribed to all available webhooks for the Instagram product:

|  |  |
| --- | --- |
| - `comments` - `live_comments` - `message_reactions` - `messages` | - `messaging_optins` - `messaging_postbacks` - `messaging_referral` - `messaging_seen` |

Learn more about
[webhooks.
![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/310307727_3347317042262105_1088877051262827250_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=5SvUa0KxdZkQ7kNvwHcqah0&_nc_oc=AdpNPlkM5xCl8ncqAEi0DvJzLsMMV09WvXL6Z1STXmvsbKMnBfs-2mixKR1O9x9_AAg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=FMY_WpGp0_iyCtdjRenVnQ&_nc_ss=7b289&oh=00_Af7Q86ZwQUzqfij4Ql_LPI0YP0c-DZ36UVEqyR7RCLlZWA&oe=6A1BE7E2)](https://developers.facebook.com/docs/instagram/platform/instagram-api/webhooks)

## Step 9. Set up Instagram business login

Provide a secure way for your app users to give your app permissions to access data with business login.

1. Click **Set up** in the **3. Set up Instagram business login** section
2. Add your **Redirect URL** in the popup and click **Save**
3. Copy and paste the **Embed URL** in an anchor tag or button on your app or website to launch business login.
4. Click **Business login settings**
5. Add additional **OAuth Redirect URIs**, if applicable
6. Add your **Deauthorize callback URL**
7. Add your **Data deletion request URL**
8. Click **Save**

Learn more about
[business login.
![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/310307727_3347317042262105_1088877051262827250_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=5SvUa0KxdZkQ7kNvwHcqah0&_nc_oc=AdpNPlkM5xCl8ncqAEi0DvJzLsMMV09WvXL6Z1STXmvsbKMnBfs-2mixKR1O9x9_AAg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=FMY_WpGp0_iyCtdjRenVnQ&_nc_ss=7b289&oh=00_Af7Q86ZwQUzqfij4Ql_LPI0YP0c-DZ36UVEqyR7RCLlZWA&oe=6A1BE7E2)](https://developers.facebook.com/docs/instagram/platform/instagram-api/business-login)

## Step 10. Complete App Review

Instagram requires successful completion of the App Review process before your app can access live data. Submit your App Review request when you're ready.

If you are ready now complete the following steps:

1. Click the chevron to right of
   **Complete App Review.**
2. Click
   **Go to App Review.**

   A pop-up appears with a list of the
   **Requirements**
   for App Review:

   - Confirm that your app can be loaded and tested externally.
   - Provide clear use case details and describe step-by-step how a person uses your app.
   - Tell us how your case of Instagram permissions follows established usage guidelines. You will need to upload screen recordings that demonstrate how your app will use each permission.
3. Click
   **Continue.**

   A pop-up appears that shows the required and recommended permissions that have been added by default for the Instagram product. If your app will not need a recommended permission, uncheck it.

   #### Permissions

   - `instagram_business_basic`
   - `instagram_business_content_publish`
   - `instagram_business_manage_comments`
   - `instagram_business_manage_insights`
   - `instagram_business_manage_messages`

   #### Features

   - [Human Agent](https://developers.facebook.com/docs/features-reference/human-agent)If you have requested the `instagram_business_manage_messages` permission, the Human Agent feature is added automatically.

   **Note:** If you are adding Instagram to an existing app that has been approved for Advanced Access you may be [automatically granted Advanced Access to Instagram business permissions](#step-10-complete-app-review).

   You can add and remove permissions and features at any time during the development process.
4. Click **Continue** and you will be redirected to the **App Review > Requests** menu item in the left-side menu.

If you want to add more products or are not yet ready to submit for App Review, you can [return to the app dashboard](#step-10-complete-app-review) to submit at a later date.

## Next Steps

- **API Integration Helper** – Use the API Integration Helper in the App Dashboard to send a test message using the API.
- When you need to request Advanced Access, visit the [Instagram Platform App Review guide](https://developers.facebook.com/docs/instagram-platform/app-review) to learn how to submit your app for Meta App Review.

## See Also

Learn more about Meta app development, review, permissions, and more with the following developer documents:

- [Business login for Instagram](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/business-login)
- [Content Publishing API](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/content-publishing)
- [Comment Moderation API](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/comment-moderation)
- [Instagram Messaging API](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/messaging-api)
- [Logos and Trademarks](https://developers.facebook.com/docs/app-review/resources/logos)
- [Permissions Reference](https://developers.facebook.com/docs/permissions#i)
- [Webhooks from Meta](https://developers.facebook.com/docs/graph-api/webhooks)
