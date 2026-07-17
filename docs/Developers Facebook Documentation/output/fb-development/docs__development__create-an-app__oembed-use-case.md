# oEmbed Use Case - App Development with Meta

_Source: https://developers.facebook.com/docs/development/create-an-app/oembed-use-case_

---

# Customize the Embed Facebook, Instagram and Threads Use Case

This document shows you how to customize the **Embed Facebook, Instagram and Threads** content in other websites use case you added to your app during the [app creation process](https://developers.facebook.com/docs/development/create-an-app/).

## Customize your use cases

As part of customizing your app, you will add each feature and/or permissions required for each use case.

1. Click **Embed Facebook, Instagram and Threads content in other websites**.
2. Click the **Add** button to the right of the **Threads oEmbed Read** feature.

Click **Settings** to get the following information:

- **Threads App ID**
- **Threads App secret**
- **Threads Display Name** – You can update the display at any time during development.

Repeat this step for each use case you added to your app.

## Test your use cases

Before you submit for App Review, you must make at least one successful API call to each endpoint of your use case. Visit our [oEmbed developer documentation](https://developers.facebook.com/docs/plugins) for more information on implementation and testing.

You can view the status of your testing and API call count for each use case by clicking **Use cases** in the left side menu and selecting the use case.

Some use cases require testing before the app can be submitted to App Review.

**Step 1.** Visit our [oEmbed developer documentation](https://developers.facebook.com/docs/plugins/oembed) for more information on implementation and testing.

**Step 2.** Click **Review > Testing** to view the status of your testing and API call count.

## App Review

**Step 1.** In the left side menu go to **Review > App Review**. Click the **Edit** button to start your submission. You will see a list of all permissions and features you are requesting, with links to the documentation for each.

**Step 2.** **Complete App Settings** – Click the arrow to the right to add [app settings](https://developers.facebook.com/docs/development/create-an-app/app-dashboard/basic-settings) such as app icon, privacy policy URL, and app category. **This step must be complete before continuing.**

**Step 3.** **Complete app verification** – For each platform on which your app is available, provide all the necessary details for how a Meta reviewer can log in to your app.
Provide detailed, step-by-step instructions on how a reviewer can test your integration and how you are using the requested permissions or features. Include any testing credentials required to access your integration.

**Step 4.** **How will your app use the advanced access for each permission?** – For each feature and permission your app needs, click the arrow to the right to:

- Provide a detailed description of how your app uses that specific permission or feature requested, how it adds value for a person using your app, and why it's necessary for app functionality.
- Provide a URL where we can test Oembed Read. – [Get the embed HTML](https://developers.facebook.com/docs/plugins/oembed) for any public post or video on our official [Facebook Page](https://www.facebook.com/facebook) or [Instagram Page](https://www.facebook.com/instagram) or the embed HTML for the page.
- Agree that any data your app receives through the permission or feature will be used in accordance with its allowed usage. Add the returned embed HTML to your own page where you will be displaying oEmbed content and enter that page's URL in the form field.

**Step 5.** Click the **Submit for Review** button in the lower right.

Once you have been approved for the oEmbed Read feature you may embed your own pages, posts, or videos using their respective URLs.

## Publish

## Publish (Optional)

You only need to publish your app if your app will access data that you don't own or manage or your app uses a product that requires it to be published, such as webhooks.

To publish your app you'll need to add any required settings. You can also add optional settings to your app. You can update these settings at any time during development.

You can also view your **App ID**, **App secret**.

### Basic settings

**Step 1.** To publish your app select **Publish** from the right side menu.

**Step 2.** Click **Go to app settings** to the right of **Privacy policy URL**. This will take you to **App settings > Basic**.

**Step 3.** If you haven't done so already, add the following required settings:

- **App icon**
- **Category**
- **Privacy Policy URL**
- **User data deletion**

You can also update your app's platform and Data Protection Officer contact information.

**Step 4.** Click **Save changes**.

**Step 5.** If you have no advanced settings to add or update, click **Publish** in the right side menu.

**Step 6.** When you are ready, click the **Publish** button in the bottom right corner.

### Advanced settings

**Step 1.** Click **App settings > Advanced** to update settings for the following:

- App authentication
- Download User Identifiers
- App Restrictions
- Security
- Domain manager
- App Page
- Advertising Accounts
- Tester Gatekeeper Allow List
- Share Redirect Allow List

**Step 2.** Click **Save changes**.

**Step 3.** Click **Publish** in the right side menu.

**Step 4.** When you are ready, click the **Publish** button in the bottom right corner.

Congratulations on completing your app!

## See Also

Visit the following to learn more about the app development process:

- [App Review](https://developers.facebook.com/docs/resp-plat-initiatives/app-review)
- [App Development](https://developers.facebook.com/docs/development)
- [Business verification](https://developers.facebook.com/docs/development/release/business-verification)
- [Data Use Checkup](https://developers.facebook.com/docs/development/maintaining-data-access/data-use-checkup)
- [Features Reference](https://developers.facebook.com/docs/features-reference)
- [Permissions Reference](https://developers.facebook.com/docs/permissions)
- [API Developer Documentation](https://developers.facebook.com/docs)
