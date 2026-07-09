# Customize the Engage with customers on Messenger Use Case | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/create-an-app_

---

# Customize the Engage with customers on Messenger Use Case

Updated: May 14, 2025

The following content is from the Meta App Development documentation. Please refer to the Development documentation to learn more about the
[Meta App Development process.](https://developers.facebook.com/docs/development)

This document shows you how to customize the Engage with customers on Messenger use case you added to your app during the [app creation process](https://developers.facebook.com/docs/development/create-an-app).

1. Click **Dashboard** in menu to the left in the App Dashboard. Each use case that you have added to your app is listed here.
2. Select the use case you want to customize. This allows you to add settings and permissions to make your app work the way you want it to.
3. Add permissions that your app needs and remove permissions that your app doesn’t need. If a permission or feature is required for a use case, it can’t be removed.
4. Click **Ready to test** to test each use case. If you need to submit your app for Meta App Review, you must test each use case. The [**Meta’s Graph API Explorer**](https://developers.facebook.com/tools/explorer) allows you to test your queries and get access tokens and code samples for your queries.
5. Click **Dashboard** to repeat the above for each use case.

## Permissions and features

1. To customize the Messenger Platform use case, select **Customize the Engage with customers on Messenger from Meta use case** . You are redirected to a list of permissions.
2. Click **Add** next to each additional feature or permission that your app needs to work the way you want it to.
3. If your app requires [App Review](https://developers.facebook.com/docs/resp-plat-initiatives/individual-processes/app-review) click the **Actions** button and select **+ Add to App Review** . You’ll complete the review submission later.

### Messenger from Meta use cases permissions and features

The following table shows the permissions and features available for the Messenger from Meta use cases.

| Feature or Permission | API usage | Allowed actions |
| --- | --- | --- |
| [Business Asset User Profile](https://developers.facebook.com/docs/features-reference/business-asset-user-profile-access) | Optional for this use case. | Can be added to this use case. |
| [`ads_management`](https://developers.facebook.com/docs/permissions#ads_management) | Optional for this use case. | Can be added to this use case. |
| [`business_management`](https://developers.facebook.com/docs/permissions#business_management) | **Required** for this use case. | **Cannot be removed** for this use case. |
| [`email`](https://developers.facebook.com/docs/permissions#email) | Optional for this use case. | Can be added to this use case. |
| [`instagram_basic`](https://developers.facebook.com/docs/permissions#instagram_basic) | Optional for this use case. | Can be added to this use case. |
| [`instagram_manage_messages`](https://developers.facebook.com/docs/permissions#instagram_manage_messages) | Optional for this use case. | Can be added to this use case. |
| [`page_manage_metadata`](https://developers.facebook.com/docs/permissions#page_manage_metadata) | **Required** for this use case. | **Cannot be removed** for this use case. |
| [`pages_messaging`](https://developers.facebook.com/docs/permissions#pages_messaging) | **Required** for this use case. | **Cannot be removed** for this use case. |
| [`pages_read_engagement`](https://developers.facebook.com/docs/permissions#pages_read_engagement) | Optional for this use case. | Can be added to this use case. |
| [`pages_show_list`](https://developers.facebook.com/docs/permissions#pages_show_list) | **Required** for this use case. | **Cannot be removed** for this use case. |
| [`pages_user_gender`](https://developers.facebook.com/docs/permissions#pages_user_gender) | Optional for this use case. | Can be added to this use case. |
| [`pages_user_locale`](https://developers.facebook.com/docs/permissions#pages_user_locale) | Optional for this use case. | Can be added to this use case. |
| [`pages_user_timezone`](https://developers.facebook.com/docs/permissions#pages_user_timezone) | Optional for this use case. | Can be added to this use case. |
| [`pages_utility_messaging`](https://developers.facebook.com/docs/permissions#pages_utility_messaging) | Optional for this use case. | Can be added to this use case. |
| [`paid_marketing_messages`](https://developers.facebook.com/docs/permissions#paid_marketing_messages) | Optional for this use case. | Can be added to this use case. |
| [`public_profile`](https://developers.facebook.com/docs/permissions#public_profile) | **Required** for this use case. | **Cannot be removed** for this use case.<br>Can increase access for any use case.* |

* **Increasing access to this permission or feature will affect other use cases** – This permission or feature is part of more than one use case on this app. Any changes made to the access level of this permission or feature will affect the use cases listed below. This change might mean new requirements and reviews.

### Messenger API Setup

1. In the **Configure webhooks** section, add your **Callback URL** and **Verify token** to configure webhooks or use services that help you set up an endpoint.
2. In the **Generate access tokens** section, click **Connect** to add Facebook pages to your app.
3. Click **Continue** , or log into a Facebook account, in the dialog popup.
4. Select the Pages you want to connect to this app and click **Continue** .
5. Click **Save** then **Got it** to return to the App Dashboard.
6. In the **Generate access tokens** section, click **Add Subscriptions** to subscribe to available Page webhook fields.
7. Select each field you want to subscribe to and click **Confirm** .

The **Complete App Review** section has a **Request Permission** button with a popup that adds additional permissions. Select any additional feature or permission that your app needs to work the way you want it to.

## Customize Facebook Login for Business

If you are implementing [Facebook Login for Business](https://developers.facebook.com/documentation/facebook-login/facebook-login-for-business) in your app, follow these steps.

### Settings

1. Click **Facebook Login for Business** in the menu to the left in the App Dashboard.
2. Select **Settings** .
3. Add your **Redirect URI** and click **Check URI** to validate it.
4. Customize the **Client OAuth settings** .
5. Add your **Deauthorize Callback URL** .
6. Add your **Data Deletion Request URL** .
7. Click **Save changes** .

### Quickstart

Use the Quickstart to add Facebook Login for Business to your app.

1. Click **Quickstart** .
2. Select and customize each platform for this app.
3. Add the **Facebook Login Button** to your app.

### Configurations

This optional feature of Facebook Login for Business allows you to create multiple configurations and present them to different sets of users. Configurations allow you to choose:

- The type of login variation to present to your app users.
- The type of access token you want to request from your business clients, a User access token or System-user access token and token expiration
- If you select User access token then your app users will log in using their personal Facebook account.
- If you select System-user access token your app users will be required to log in using a business portfolio. This is only required if this configuration needs continuous access to business assets, such as Facebook Pages, ad accounts or Instagram accounts.
- The business assets you want to request from your clients.
- The permissions your app users are required to grant your app.

## Become a Tech Provider

If your app needs to access business data owned by other business portfolios to provide services or functionality to those businesses, you must become a Tech Provider. This option will require additional data questions and approval through App Review before publishing.

1. Click **Become a Tech Provider** .
2. Click **Yes, I’m a Tech Provider** . The App Dashboard is updated to include additional items listed on **Dashboard** for your use cases.
3. Click **Business verification** to add a verified business portfolio or add a business portfolio and start the verification process.

## App Review

1. In the left side menu go to **Review > App Review** . Click the **Edit** button to start your submission. All permissions and features you are requesting, with links to the documentation for each, are listed here.
2. **Complete App Settings** – Click **Review your app settings** to add or update any [app settings](https://developers.facebook.com/docs/development/create-an-app/app-dashboard/basic-settings) such as app icon, privacy policy URL, and app category. **This step must be complete before continuing.**
3. **Reviewer instructions** – Click **Provide reviewer instructions** A popup dialog appears for each platform on which you app is available. Select each platform and answer the questions with questions for our reviewers to test your use case implementations. Click **Done** .
4. Click each permission and feature you requested.
5. Click the checkbox to agree to use each permission or feature in accordance with its allowed usage. If your app doesn’t use a permission or feature listed, remove it by clicking the trashcan icon.
6. Click the **Submit for Review** button in the lower right.

## Publish

### Required app assets

To publish your app, you need the following assets:

- An app icon – Your app’s unique icon image; this file must be less than 5 MB, between 512 x 512 and 1024 x 1024 pixels, and in JPEG, GIF or PNG format.
- Contact information for a Data Protection Officer, if you are doing business in the European Union.
- A [Privacy Policy](https://en.wikipedia.org/wiki/Privacy_policy) URL for your app
- A [data deletion](https://developers.facebook.com/docs/development/create-an-app/app-dashboard/data-deletion-callback) URL with instructions or a callback that allows your app user to delete their data from your app.

1. When you are ready to publish, select **Publish** in the left side menu.
2. **Review** your use cases and requirements.
3. Click **Publish** in the lower right corner.

## See Also

Visit the following to learn more about the app development process:

- [App Development](https://developers.facebook.com/docs/development)
- [Business verification](https://developers.facebook.com/docs/development/release/business-verification)
- [Permissions Reference](https://developers.facebook.com/docs/permissions)
- [Messenger Developer Documentation](https://developers.facebook.com/documentation/business-messaging/messenger-platform)
