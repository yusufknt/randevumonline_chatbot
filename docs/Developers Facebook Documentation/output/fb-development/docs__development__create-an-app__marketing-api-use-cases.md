# Marketing API Use Cases - App Development with Meta

_Source: https://developers.facebook.com/docs/development/create-an-app/marketing-api-use-cases_

---

# Marketing API Use Cases

This document shows you how to customize one or more of the following Marketing API use cases you added to your app during the [app creation process](https://developers.facebook.com/docs/development/create-an-app/):

- **Capture & manage ad leads with Marketing API**
- **Create & manage ads with Marketing API**
- **Measure ad performance data with Marketing API**

The following products have been automatically added to your app:

- [Facebook Login for Business](https://developers.facebook.com/docs/facebook-login/facebook-login-for-business/) – Authenticate your app users and create configuration that requests the business assets and permissions from your app users that your app needs to work properly.
- [Webhooks](https://developers.facebook.com/docs/graph-api/webhooks/getting-started/webhooks-for-ad-accounts) – Subscribe to changes and receive updates in real time without calling the API.

### Marketing API use cases permissions and features

The following table shows the permissions and features available for the Marketing API use cases.

| Feature or Permission | Marketing API usage | Allowed actions |
| --- | --- | --- |
| [Ads Management Standard Access](https://developers.facebook.com/docs/features-reference/ads-management-standard-access/) | **Required for all use cases**. | **Cannot be removed for any use case.**  Can request a higher Marketing API rate limit for any use case.﹡ |
| [Business Asset User Profile](https://developers.facebook.com/docs/features-reference/business-asset-user-profile-access/) | Optional for all use cases. | Can be added for any use case. |
| [`ads_management`](https://developers.facebook.com/docs/permissions#ads_management) | **Required for all use cases**. | **Cannot be removed for any use case.** |
| [`ads_read`](https://developers.facebook.com/docs/permissions#ads_read) | **Required for all use cases**. | **Cannot be removed for any use case.** |
| [`business_management`](https://developers.facebook.com/docs/permissions#business_management) | **Required for all use cases**. | **Cannot be removed for any use case.** |
| [`catalog_management`](https://developers.facebook.com/docs/permissions#catalog_management) | Optional for Create & manage ads.  Unavailable for Capture & manage ad leads.  Unavailable for Measure ad performance. | Can be added for Create & manage ads.  Cannot be added for Capture & manage ad leads.  Cannot be added for Measure ad performance. |
| [`email`](https://developers.facebook.com/docs/permissions#email) | Optional for all use cases. | Can be added for any use case. |
| [`leads_retrieval`](https://developers.facebook.com/docs/permissions#leads_retrieval) | **Required for Capture & manage ad leads**.  Unavailable for Create & manage ads.  Unavailable for Measure ad performance. | **Cannot be removed for Capture & manage ad leads.**  Cannot be added for Create & manage ads.  Cannot be added for Measure ad performance. |
| [`page_manage_ads`](https://developers.facebook.com/docs/permissions#page_manage_ads) | **Required for Capture & manage ad leads**.  Optional for Create & manage ads.  Unavailable for Measure ad performance. | **Cannot be removed for Capture & manage ad leads.**  Optional for Create & manage ads.  Cannot be added for Measure ad performance. |
| [`page_manage_metadata`](https://developers.facebook.com/docs/permissions#page_manage_metadata) | Unavailable for Create & manage ads.  Optional for Capture & manage ad leads.  Unavailable for Measure ad performance. | Unavailable for Create & manage ads.  Optional for Capture & manage ad leads.  Unavailable for Measure ad performance. |
| [`pages_read_engagement`](https://developers.facebook.com/docs/permissions#pages_read_engagement) | **Required for all use cases**. | **Cannot be removed for any use case.** |
| [`pages_show_list`](https://developers.facebook.com/docs/permissions#pages_show_list) | **Required for all use cases**. | **Cannot be removed for any use case.** |
| [`public_profile`](https://developers.facebook.com/docs/permissions#public_profile) | **Required for all use cases**. | **Cannot be removed for any use case.**  Can increase access for any use case.﹡﹡ |
| [`threads_business_basic`](https://developers.facebook.com/docs/permissions#threads_business_basic) | Optional for Create & manage ads.  Unavailable for Measure ad performance.  Unavailable for Capture & manage ad leads. | Can be added for Create & manage ads.  Cannot be added for Capture & manage ad leads.  Cannot be added for Measure ad performance. |

﹡ **Request a higher Marketing API rate limit** – A higher rate limit and an unlimited number of ad accounts with Ads Management Standard Access requires approval through App Review with other annual reviews to maintain it. Select Request to add Ads Management Standard Access to your App Review submission. [Learn more about Ads Management Standard Access.](https://developers.facebook.com/docs/features-reference/ads-management-standard-access/)

﹡﹡ **Increasing access to this privilege will affect other use cases** – This privilege is part of more than one use case on this app. Any changes made to the access level of this privilege will affect the use cases listed below. This change might mean new requirements and reviews.

## Use case customization

### Permissions and features

1. If you are not already on the **Use cases** page of the dashboard, click **Use cases**, or pencil icon, in the left-side menu.
2. Click on a use case to view the permissions and features that are available, both required and optional, for that use case.
3. Click the **Add** button to the right of each permission or feature you'd like to add. If, during development, you find that your app doesn't use the permission or feature, you can return here and remove it.
4. Additional actions are available for certain permissions and features.
   - To request a higher rate limit for the Ads Management Standard Access feature, click the **Actions** button and select **Request higher limit**.
     - If you are ready to submit your app for App Review, continue to the [App Review section](https://developers.facebook.com/docs/app-review). If not, click **Use cases**, or pencil icon, in the left-side menu to continue to customize your use cases.
   - To increase access for the `public_profile` permission, allow your app to serve user who don't have a role on your app or the business connected to your app, click the **Increase access** button.
   - If, during development, you find that your app doesn't need a higher rate limir or increased access to `public_profile`, you can return here and remove it.

### Quickstart

Marketing API QuickStart provides a guided, tutorial, hands-on coding experience, it steps you through the process of building a small application in a few minutes.

1. Click **Quickstart** in the left-side menu.
2. Click **Create an Ad Campaign** to generate code samples to create an ad campaign.
3. Click **Next** to get code samples using the [Meta Business SDK](https://developers.facebook.com/docs/business-sdk/).
4. Select a coding language from the dropdown menu and click **Next**.
5. Click **Create Sandbox Ad Account**. A sandbox ad account lets you test ad creation and reporting using the Facebook Marketing API without incurring charges. These ad accounts don't require a payment method and the ads you create won't run. You can also create reports showing mock ad performance data.
6. In the popup, add required information and click **Create**. Be sure that once you select a Facebook Page you click the checkbox before clicking Create. 1. The page should refresh to show you sandbox. Click **Next**.
7. Click **Generate Access Token**.
8. In the popup select the permissions to associate with your access token and click **Get Token**. This token is valid for 2 months. Click **Next**.
9. A code sample has been generated with your access token, ad account ID, and app ID that will create an ad campaign. You can:
   - **Download Sample Code** to add to your app
   - **Try in Graph API Explorer** to try the code in Meta's testing tool
   - **Try it in Postman** to try the code in the Postman tool
   - **View More Examples** to go to Github to see more examples
10. Click **Next** to see the steps for **How to run your Downloaded Sample Code**.

### Tools

Click **Tools** in the left-side menu to:

- Generate new access tokens
- Update your ad account sandbox
- [Read the Marketing API Developer Documentation](https://developers.facebook.com/docs/marketing-api/)

### Settings

Click **Settings** in the left-side menu to:

- Connect a business portfolio to your app, change the business portfolio currently connected to your app, or start the business verification process. You can add an unverified business portfolio however it must be verified before you can run ads.
  - If you don't have a business portfolio or want to create a new one, click **Create new account**.
- [Read the Marketing API Developer Documentation](https://developers.facebook.com/docs/marketing-api/).
- View the [**Ads API access level**](https://developers.facebook.com/docs/marketing-api/get-started/authorization/).
- Enable [Marketing API version auto-upgrade](https://developers.facebook.com/docs/marketing-api/versions/) to automatically update API calls from deprecated Marketing API versions.

### Webhooks (optional)

A majority of Meta developers use webhooks to get real-time notifications and reduce the number of API calls, and thus reducing the change of rate limiting. Webhooks is automatically added but it is optional.

To receive webhooks from Meta, you need to:

1. [Create an endpoint](https://developers.facebook.com/docs/development/create-an-app/docs/graph-api/webhooks/getting-started) on your server to receive and process these HTTP notifications
2. [Send a `POST` request to subscribe your app](https://developers.facebook.com/docs/development/create-an-app/docs/graph-api/webhooks/getting-started/webhooks-for-ad-account) to webhooks
3. Configure webhooks in your app's dashboard (the step listed in this section)

To configure webhooks for your use case in the app's dashboard, follow these steps. These steps assumes you are in the **Use cases > Customize > Customize use case** dashboard and have selected the **Webhooks** option in the menu.

1. **Select product** - In the dropdown select the assets, such as Page and Ad Account, you'd like to be notified about.
2. Add your **Callback URL**, the endpoint you created to receive webhooks.
3. Add your **Verify token** that Meta will use as part of the callback URL verification.
4. You can add client authentication to the verification process by sliding **Mutual TLS** from No to **Yes**. (Optional)

**Note:** To receive webhook notifications your app must be published. App Review is not required to use webhooks.

### Update a use case

If, at any point during development, you want to update a use case, you can return to the dashboard, click **Use cases** (pencil icon) in the left-side menu and click **Customize**.

## Customize Facebook Login for Business

If you are implementing [Facebook Login for Business](https://developers.facebook.com/docs/facebook-login/facebook-login-for-business/) in your app, follow these steps.

### Settings

1. Click **Facebook Login for Business** in the menu to the left in the App Dashboard.
2. Select **Settings**.
3. Add your **Redirect URI** and click **Check URI** to validate it.
4. Customize the **Client OAuth settings**.
5. Add your **Deauthorize Callback URL**.
6. Add your **Data Deletion Request URL**.
7. Click **Save changes**.

### Quickstart

Use the Quickstart to add Facebook Login for Business to your app.

1. Click **Quickstart**.
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

## See also

Visit the following to learn more about the app development process:

- [App Development](https://developers.facebook.com/docs/development)
- [App Review](https://developers.facebook.com/docs/resp-plat-initiatives/app-review)
- [Business verification](https://developers.facebook.com/docs/development/release/business-verification)
- [Marketing API](https://developers.facebook.com/docs/marketing-apis)
