# Instagram Use Case - App Development with Meta

_Source: https://developers.facebook.com/docs/development/create-an-app/instagram-use-case_

---

# Customize the Manage messaging and content on Instagram Use Case

This document shows you how to customize the Instagram API use case you added to your app during the [app creation process](https://developers.facebook.com/docs/development/create-an-app/).

## Use case customization

1. Click **Dashboard** in menu to the left in the App Dashboard. Each use case that you have added to your app is listed here.
2. Select the use case you want to customize. This allows you to add settings and permissions to make your app work the way you want it to.
3. Add permissions that your app needs and remove permissions that your app doesn't need.
   - If a permission or feature is required for a use case, it can't be removed.
4. Click **Ready to test** to test each use case. If you need to submit your app for Meta App Review, you must test each use case. The [**Meta's Graph API Explorer**](https://developers.facebook.com/tools/explorer) allows you to test your queries and get access tokens and code samples for your queries.
5. Click **Dashboard** to repeat the above for each use case.

To customize the Instagram use case, click **Customize the Manage messaging and content on Instagram use case**.

It is recommended that you set up the API since permissions and features specific to the setup are added by default. Select one of the following API setups:

- [**API setup with Instagram Login**](#ig-login) – App users log in with their Instagram credentials
- [**API setup with Facebook Login**](#fb-login) – App users log in with their Facebook credentials

You can only add one setup per app. If you want to implement both setups, create an app for each setup.

### API setup with Instagram Login

To customize the Instagram use case so that your app uses Business Login for Instagram to log users in to your app, select **API setup with Instagram Login** in the left side menu. The app name, **Instagram app ID**, and **Instagram app secret** are shown and can be used for test API calls.

1. Click **Add all required permissions**. The `instagram_business_basic` and `instagram_business_manage_messages` permission are required for this functionality and added by default.
2. In the **Generate access tokens** section click **Add account**.
3. Click **Continue** and log in to your Instagram account in the popup window.
4. Click **Save** then **Got it** to return to the App Dashboard.
5. In the **Configure webhooks** section, add your **Callback URL** and **Verify token** to configure webhooks or use services that help you set up an endpoint.
6. Click **Verify and save**. The verification must be successful to subscribe to webhooks fields.
7. In the **Configure webhooks** section, subscribe to available Instagram webhooks.
8. Click **Set up** in the **Set up Instagram business login**.
9. Add your **Redirect URL** and click **Save**.
10. Click **Business login settings** and add your Deauthorization callback URL and Data deletion request URL and click **Save.** You can also add additional redirect URIs.
11. If you are ready to submit your app for review, click **Go to app review** in the **Complete app review** section. This is only required if you are creating solutions for clients.

### API integration helper

The API Integration Helper allows you to send a test message using the Instagram API. Only available for apps that use Business Login for Instagram .

### API setup with Facebook Login

To customize the Instagram use case so that your app uses Facebook Login for Business to log users in to your app, select **API setup with Facebook Login** in the left side menu.

1. If you are implementing content management, click **Add all required permissions**. The following permissions are added by default and are required to manage content:
   - `business_management`
   - `instagram_basic`
   - `instagram_content_publishing`
   - `pages_read_engagement`
   - `pages_show_list`
2. If you are implementing messaging, click **Add required messaging permissions**. The following permissions are added by default and are required to send messages:
   - `business_management`
   - `instagram_basic`
   - `instagram_manage_messages`
   - `pages_read_engagement`
   - `pages_show_list`

#### Webhooks

Set up webhooks to subscribe to changes and receive updates in real time without calling the API.

1. Click **Add more to this use case** to and click **Get real-time notifications with Webhooks** if you are setting up webhooks for your app.
2. Add **Instagram** from the **Webhooks Select product** dropdown menu.
3. In the **Configure webhooks** section, add your **Callback URL** and **Verify token** to configure webhooks or use services that help you set up an endpoint.
4. Select each field you want to subscribe to.

#### Complete setup

1. Follow the links to our developer documentation to complete your setup:
   - [Set up Facebook Login for Business](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-facebook-login/business-login-for-instagram)
   - [Learn how to submit your app for review](https://developers.facebook.com/docs/instagram-platform/overview#app-review)
   - [Configure webhooks](https://developers.facebook.com/docs/instagram-platform/webhooks)

### Permissions and features

Before you submit for review, if required, you can add additional features and permissions available for this use case that your app needs to work as you want it to.

1. Click **Permissions and features** in the menu to the left to add additional available permissions.

## Become a tech provider (optional)

Become a Tech Provider if this app will be for clients or other business portfolios.

1. Click **Become a Tech Provider**. You will need to:
   - [Verify your business](https://developers.facebook.com/docs/development/create-an-app/docs/development/release/business-verification/)
   - Verify that your business is [allowed to access another business portfolio's data](https://developers.facebook.com/docs/development/release/access-verification/)
   - [Complete App Review](https://developers.facebook.com/docs/resp-plat-initiatives/individual-processes/app-review/)
2. Click **Yes, I'm a Tech Provider**.

You will be redirected to **Dashboard** which will display **App customization and requirements**. You will see the status for each customization and requirement with the status for each item instead of your app's rate limit usage. Each item must be completed before you can publish your app. When each item is complete the circle icon will be filled in.

- **Add and customize use cases** – Clicking on a use case takes you to **Use cases > Customize > Customize use case** for that use case where you can update the use case or add more use cases.
- [**Prepare and submit for App Review**](#review).
  - **Review and complete testing requirements** will take you to **Review > Testing**.
  - **Business Verification** will take you to **Review > Verification**.
  - [**App Review**](#review) will take you to **Review > App Review**.
- [**Publish your app**](#publish)

## App Review

**Apps that require App Review** – If your app will access data your don't own or manage, it requires App Review before your app users can grant access.

1. In the left side menu go to **Review > App Review**. Click the **Edit** button to start your submission. You will see a list of all permissions and features you are requesting, with links to the documentation for each.
2. **Complete App Settings** – Click the arrow to the right to add [app settings](https://developers.facebook.com/docs/development/create-an-app/app-dashboard/basic-settings/) such as app icon, privacy policy URL, and app category. **This step must be complete before continuing.**
3. **Complete app verification** – For each platform on which your app is available, provide all the necessary details for how a Meta reviewer can log in to your app.
   - Provide detailed, step-by-step instructions on how a reviewer can test your integration and how you are using the requested permissions or features. Include any testing credentials required to access your integration.
4. **How will your app use the advanced access for each permission?** – For each feature and permission your app needs, click the arrow to the right to:
   - Provide a detailed description of how your app uses that specific permission or feature requested, how it adds value for a person using your app, and why it's necessary for app functionality.
   - Upload a screen recording that demonstrates how your app will use this permission or feature so Meta reviewers can confirm it is used correctly and does not violate Meta policies. [Learn more.](https://developers.facebook.com/docs/development/create-an-app/docs/app-review/submission-guide/screen-recordings/)
   - Agree that any data your app receives through the permission or feature will be used in accordance with its allowed usage.
5. Click the **Submit for Review** button in the lower-right.

## Publish your app

Once you have completed development, and successfully completed App Review (if necessary), you can publish your app.

**Apps that require publishing** – If your app will access content you don't own or manage, or you have implemented a product, such as webhooks, that requires your app to be published, it will need to be published.

1. Click **Publish** in the left side menu. If any app settings are needed, you'll be directed to update them.
2. You can review your app's use cases and App Review approvals.
3. Click the **Publish** button in the lower-right.

**Note:** Some functionality, such as webhooks, require your app to be published.

## See Also

Visit the following to learn more about the app development process:

- [App Development](https://developers.facebook.com/docs/development)
- [Business verification](https://developers.facebook.com/docs/development/release/business-verification)
- [Permissions Reference](https://developers.facebook.com/docs/permissions)
- [Instagram API Developer Documentation](https://developers.facebook.com/docs/instagram-platform)
