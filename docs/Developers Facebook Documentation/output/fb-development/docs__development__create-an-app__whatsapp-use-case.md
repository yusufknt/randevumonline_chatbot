# WhatsApp Use Case - App Development with Meta

_Source: https://developers.facebook.com/docs/development/create-an-app/whatsapp-use-case_

---

# Customize the Connect with customers through WhatsApp Use Case

This document shows you how to customize the **Connect with customers through WhatsApp** use case you added to your app during the [app creation process](https://developers.facebook.com/docs/development/create-an-app/) in Meta's App Dashboard.

After creating your app with the WhatsApp use case you are redirected to the **Customize use case > Connect on WhatsApp** page in the dashboard. You can also click the pencil icon **Use cases** menu item to the left then select the WhatsApp use case **Customize** button.

The left-side menu lists ways in which you can customize use case settings and permissions to make your app work the way you want it to.

- [**Permissions and features**](#permissions-and-features) - View required and optional permissions for this use case and add them to an App Review submission, if applicable.
- [**Quickstart**](#quickstart) - Start using the API and learn how to scale your business, improve ROI, and manage your WhatsApp Business account.
- [**API Setup**](#api-setup) - Generate access tokens, send and receive messages, and configure webhooks and the WhatsApp SDK.
- [**Configuration**](#configuration) - Configure webhooks and the WhatsApp SDK.
- [**Resources**](#resources) – View the WhatsApp developer documentation, Meta Blueprint courses, and support resources.
- [**Tech Provider onboarding**](#tech-provider-onboarding) – Start scaling the WhatsApp Business Platform for your business.
- [**Partner Solutions**](#partner-solutions) – Create a partner solution.
- [**Embedded Signup Builder**](#embedded-signup-builder) – Integrate Embedded Signup flow into your website or client portal.

## Permissions and features

On this page of the dashboard, you will be able to view the required and optional permissions for this use case.

### Available permissions

| Permission | Description |
| --- | --- |
| `business_management` | Optional. You only need this permission if you plan to access your business portfolio programmatically. If you use Meta Business Suite to view your portfolio, this permission is not required. |
| `email` | Optional. You only need this permission if you plan to access your business portfolio programmatically. If you use Meta Business Suite to view your portfolio, this permission is not required. |
| `public_profile` | **Required.** This permission is required to access the WhatsApp APIs. |
| `whatsapp_business_manage_events` | Optional. You only need this permission if you plan to access the Marketing Messages Lite API with the Conversions API. |
| `whatsapp_business_management` | **Required.** This permission is required to access the WhatsApp APIs. |
| `whatsapp_business_messaging` | **Required.** This permission is required to access the WhatsApp APIs. |

### View required permissions

The following permissions are required and have been added to your app by default:

- `public_profile`
- `whatsapp_business_management`
- `whatsapp_business_messaging`

These permissions are required for the WhatsApp use case and can't be removed.

### Add optional permissions

Click the **Add** button next to each optional permission that you want to add.

If your app requires App Review:

1. Click the **Actions** button next to each permission.
2. Select **+Add to App Review**. Only add permissions that your app requires for it to function the way you want it to. Adding unneeded or unused permissions can result in rejection in App Review.
3. In the popup window, follow the links to learn more about [Access verification](https://developers.facebook.com/docs/development/release/access-verification/) and [Business verification](https://developers.facebook.com/docs/development/release/business-verification) and [App Review](https://developers.facebook.com/docs/resp-plat-initiatives/individual-processes/app-review) then click **Continue**.

You'll complete the App Review submission process as part of the [Tech Provider onboarding](#tech-provider-onboarding) flow.

## Quickstart

On this page of the dashboard, you'll see a list of the following items:

- **Start the [API Setup](#api-setup)** – Get set up on the Cloud API by adding a phone number and sending your first message.
- **Scale your business**
  - Start the process to **Become a Tech Provider**.
  - Agree to the marketing messages terms of service and learn about [sending marketing messages](https://developers.facebook.com/docs/whatsapp/marketing-messages-lite-api) to **Improve ROI**
- **WhatsApp Business**.
  - **Account information** – Visit the [WhatsApp Manager](https://business.facebook.com/latest/whatsapp_manager/overview/) to see alerts, insights, and for your WhatsApp account.
  - **Message Template** – Visit the [WhatsApp Manager](https://business.facebook.com/latest/whatsapp_manager/message_templates/) to create and update message templates and explore samples templates.
  - **WhatsApp Flows** – Visit the [WhatsApp Manager](https://business.facebook.com/latest/whatsapp_manager/flows/) to edit and preview your Flows.
  - **Phone numbers** – Visit the [WhatsApp Manager](https://business.facebook.com/latest/whatsapp_manager/phone-numbers/) to view, add, and manage your phone numbers.
- [**Configuration**](#configuration)
  - **Webhooks** – Configure and manage your webhook callbacks.
  - **WhatsApp SDK** – Follow the link to the GitHub WhatsApp SDK repository.
- [**Documentation and support**](#documentation-and-support)
  - **Need support?** – Contact our support team and review open bug reports and support tickets.
  - **Documentation** – Explore the WhatsApp developer documentation to learn how to build on the WhatsApp Business Platform
  - **Tutorials** – Learn about important API features and how to get set up.

## API Setup

On this page of the dashboard, you can:

- **Access Token** – Generate short-lived access tokens to test your API calls.
- **Send and receive messages**:

  1. Select **From** and **To** phone numbers for the API request.
  2. Send messages using the API or Postman.
  3. [Configure webhooks](#configuration) to receive Messages.
  4. Learn about the [WhatsApp Business API](https://developers.facebook.com/docs/whatsapp/).
  5. Add and verify a phone number people will see when they chat with you, and add information about your business and WhatsApp Business profile.
  6. Add a payment method in the [business manager](https://business.facebook.com/latest/settings/whatsapp_account) to start sending business-initiated messages to your customers.
- **Improve ROI** - Agree to the marketing messages terms of service and learn how to [send marketing messages](https://developers.facebook.com/docs/whatsapp/marketing-messages-lite-api).

## Configuration

- **Webhooks** - Configure and manage your webhook callbacks and add your verify token in the dashboard.
- **Permanent token** - Visit the developer documentation to [learn how to create a permanent token](https://developers.facebook.com/docs/whatsapp/business-management-api/get-started#1--acquire-an-access-token-using-a-system-user-or-facebook-login) to access the WhatsApp Business API.
- **Phone numbers** - Manage production and test phone numbers in the [WhatsApp Manager](https://business.facebook.com/latest/whatsapp_manager/overview/).
- **Test account** - Delete your business: This will unlink your application and delete your business portfolio, test WhatsApp Business Accounts, and phone numbers.

## Resources

Find links for the [developer documentation](https://developers.facebook.com/docs/whatsapp) and [Meta's Blueprint courses](https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.facebookblueprint.com%2Fstudent%2Fcollection%2F409587-meta-whatsapp-business-platform-for-developers-courses&h=AUCcooEHA47LbfKuQ3kWaMoK1WrBmZPYxs-t6FXtibirOn6vQTQBIEQ-qxT211IimP1F6ncVfD0t0rGfSFMPLm1aYQ27jAOi62GC57wpBz7d4g209Scyr_RxxCK6xjSqd-5bPo3arOoGhg) as well as resources for contacting [support](https://developers.facebook.com/support/) , [viewing bug reports](https://developers.facebook.com/support/bugs/), and [reviewing your open support tickets](https://business.facebook.com/direct-support/).

## Tech Provider onboarding

If you are a Tech Provider, you can onboard your clients to the WhatsApp Business API.

On this page of the dashboard, you'll find links to the [WhatsApp Embedded Signup developer documentation](https://developers.facebook.com/docs/whatsapp/embedded-signup/), [Developer Support](https://developers.facebook.com/support/), and [Success Stories](https://developers.facebook.com/success-stories/) as well as steps to complete the Tech Provider onboarding process. This process includes:

### [Business verification](https://www.facebook.com/business/help/2058515294227817)

Click **Start verification** to verify your business. You'll need the following information:

- Verify business details – Provide your business name, address, phone number, email and website for verification.
- Confirm your connection – Select a way for us to get in touch to confirm your connection to the business.
- Upload documents – You might need to upload accepted documents to confirm these details if your business is not found.

### [App Review](https://developers.facebook.com/docs/resp-plat-initiatives/individual-processes/app-review)

Once you have completed business verification, you can submit your app for App Review. You'll need to provide the following:

- Review your app settings – Your app will need [basic settings](https://developers.facebook.com/docs/development/create-an-app/app-dashboard/basic-settings) such as an app icon, privacy policy, and app category.
- Videos – To pass App Review, you need to submit video evidence of your capabilities to send messages and manage templates.
- Submit for App Review

If you prefer to onboard with a Solution Partner, you can do so by clicking the **Onboard with a Solution Partner** button at the bottom of the page. You will need to provide your partner’s app ID during onboarding to create a partner solution.

### Onboard with an existing Solution Partner

After you click the **Onboard with a Solution Partner** button, the Tech Provider onboarding page will refresh to this flow. The flow is identical to the Tech Provider flow with the additional App Review step to **Create a partner solution** by entering your partner’s app ID to create a partner solution.

To onboard without a partner, you can do so by clicking the **Onboard without a partner** button at the bottom of the page.

## Partner solutions

On this page of the dashboard, you can create a partner solution. Click the **Create a partner solution** button to start the process or the [**Learn more** button](https://developers.facebook.com/docs/whatsapp/solution-providers/multi-partner-solutions) to visit the developer documentation. Once you click the **Create a partner solution** button the modal will appear for you to enter:

1. **Solution name** - The name for your solution
2. **Partner app ID** - Your partner's app ID. Your partner must then accept this solution request before customers can onboard to this solution. [Learn more.](https://developers.facebook.com/docs/whatsapp/solution-providers/multi-partner-solutions/#step-4--accept-the-solution-request)
3. **Permission configuration** - Select the permissions.

Click the **Send Request** button when you are ready to send your partner a request.

## Embedded Signup Builder

**Getting started with WhatsApp Embedded Signup** - Embedded Signup allows Solution Partners to onboard to the WhatsApp Business Platform directly from their website.

### Business and app status

In this section you can follow links to learn more about:

- [Business verification](https://www.facebook.com/business/help/2058515294227817)
- [App Review](https://developers.facebook.com/docs/resp-plat-initiatives/individual-processes/app-review)
- [Messaging Limits](https://developers.facebook.com/docs/whatsapp/messaging-limits/)

### App Setup

- [Facebook Login for Business Configurations](https://developers.facebook.com/docs/facebook-login/facebook-login-for-business/#create-a-whatsapp-embedded-signup-configuration) - Facebook Login for Business allows you to create one or more login experiences in the Meta App Dashboard based on the needs of your app. You can specify the access token type, assets, and permissions your app needs, and save it as a configuration. During login, your app users are presented with a configuration that allows them to grant your app access to their business assets. **You need to create a login configuration for Embedded Signup.**
- Click the **Create configuration** button to start the process.
- [Manage domains](https://developers.facebook.com/docs/facebook-login/web/#redirecturl) - Add your domain to allowlist and enable Login with the JavaScript SDK for your app so that you can start adding Embedded Signup on your website.
- Click the **Add allowlist** button to add domains.
- [App Roles](https://developers.facebook.com/docs/development/build-and-test/app-roles/) - App roles allow you to control who has permission to edit your app.
- Click **Update roles** to add and manage app administrators and developers.

### Embedded Signup Setup

- [JavaScript SDK](https://developers.facebook.com/docs/javascript) - Get the JavaScript SDK code that enables you to use Facebook Login.
- [Create a System User Access Token](https://developers.facebook.com/docs/marketing-api/system-users/overview/) - To continue integration with WhatsApp Cloud API, you need to create a system user token.
  1. Click the [Business Settings](https://business.facebook.com/latest/settings/system_users) link to generate a system user access token in the Business Manager.
  2. Copy the access token and paste it into the **System User Access Token** field in the Embedded Signup Builder.
- Pre-verified phone numbers - Click the **Add phone number** button to add a pre-verified phone number to your Embedded Signup Builder.
- Configure a webhook - If you haven't already, [configure a webhook](#configuration) to receive messages from your customers.
  1. Add your Callback URL
  2. Add your Verify Token
  3. Click **Verify and Save** to save your changes and verify your webhook.
- [Embedded Signup Pre-fill](https://developers.facebook.com/docs/whatsapp/embedded-signup/pre-filled-data/) - If you know details about your customer's business, such as its name and address, you can inject this data into Embedded Signup.
  1. Click the **Edit pre-fill** button to add pre-fill data in the modal.
  2. Click **Set prefill** to save your changes.
  3. Copy and paste the JSON code into your Embedded Signup code.
- [Session info setup](https://developers.facebook.com/docs/whatsapp/embedded-signup/implementation#step-7--optional---session-logging) -
  You can get detailed information about a user as they go through the Embedded Signup user journey.
  1. Copy and paste the code into your Embedded Signup code.
- Embedded Signup code setup - Sequence of steps to implement the Embedded Signup flow code.
  1. If you haven't already, add the JavaScript SDK to your website.
  2. If you haven't already, add the Session info setup code to your website.
  3. Copy and paste the callback code into your website.
  4. Copy and paste the set up method to be called on user click to open the Embedded Signup flow.
  5. Copy and paste the code to add a button to your page to open the Embedded Signup flow.
  6. Once the flow is complete, your callback function will send the code and IDs to your backend to continue integration. Copy and paste the code to set up the API.
- [Embedded Signup Launch](https://developers.facebook.com/docs/whatsapp/embedded-signup/implementation#step-8--launch-the-flow) - Go through the Embedded Signup flow to share a WhatsApp account and get token for.
  1. Embedded Signup Dialog - Select an item from each of the following dropdown menus:
- A Login Configuration
- An Embedded Signup Version
- An Info Version, if applicable
- Features
- Feature type, if applicable
- Click **Login with Facebook** to start the Embedded Signup flow.
- Copy and paste your Meta-hosted Embedded Signup URL into your website.
- The **Session Logging Response** will return a post-message with the WABA ID and Phone Number IDs.
  1. Exchange Token - When the user completes the login dialog flow, we will redirect the user to your redirect URL and include a code. You must then exchange this code for an access token by performing a server-to-server call to our servers.
- Copy and paste the authorization code into your website.
- Copy and paste the code to exchange the authorization code for an access token.

## Publish

**Note:** Some use cases require your app to be published.

### Required app assets

To publish your app, you need the following assets:

- An app icon – Your app's unique icon image; this file must be less than 5 MB, between 512 x 512 and 1024 x 1024 pixels, and in JPEG, GIF or PNG format.
- Contact information for a Data Protection Officer, if you are doing business in the European Union.
- A [Privacy Policy](https://l.facebook.com/l.php?u=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FPrivacy_policy&h=AUBxHiw7cG_j8JqPcCXASn0_66lXsLG4N9618XvKAhCAzY3EHSkcxE_Ko4dy1ci6e2JhCTESrqmbb4-hQCFjD-DHSlJEw5YnjRsHgL1G1GzYI2kr91vKd5O90pNIYDtWj7wTDy8PvefsQQ) URL for your app
- A [data deletion](https://developers.facebook.com/docs/development/create-an-app/app-dashboard/data-deletion-callback/) URL with instructions or a callback that allows your app user to delete their data from your app.

1. When you are ready to publish, select **Publish** in the left side menu.
2. **Review** your use cases and requirements.
3. Click **Publish** in the lower right corner.

## See Also

Visit the following to learn more about the app development process:

- [App Review](https://developers.facebook.com/docs/resp-plat-initiatives/app-review)
- [Business verification](https://developers.facebook.com/docs/development/release/business-verification)
- [Permissions Reference](https://developers.facebook.com/docs/permissions/)
- [WhatsApp Business Platform Developer Documentation](https://developers.facebook.com/docs/whatsapp)
