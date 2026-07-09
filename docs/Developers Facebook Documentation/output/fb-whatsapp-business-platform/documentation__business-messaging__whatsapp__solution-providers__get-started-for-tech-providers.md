# Become a Tech Provider | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/get-started-for-tech-providers_

---

# Become a Tech Provider

Updated: Nov 20, 2025

This document describes the steps you must take to become a [Tech Provider](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/overview#tech-providers).

As a Tech Provider, you can independently provide all WhatsApp messaging services to business customers who you have onboarded, or you can work with a [Solution Partner](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/overview#solution-partners) to jointly offer these services. If you are partnering with a Solution Partner, ask them for their app ID, which you will need to complete these steps.

## Before you start

You need the following:

- A [Meta app](https://developers.facebook.com/docs/development/create-an-app) with the WhatsApp use case and a connected [business portfolio](https://www.facebook.com/business/help/486932075688253)

During the app creation process you can create a business portfolio.

If you prefer to onboard with a Solution Partner, you will need to provide your partner’s app ID.

## Go to the app dashboard

In the [Meta App Dashboard](https://developers.facebook.com/apps) go to **Use cases > Customize** (pencil icon) and click the **Customize** button for the WhatsApp use case, then select **Tech Provider onboarding** from the left-side menu.

On this page of the dashboard, you will find links to the [WhatsApp Embedded Signup developer documentation](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/overview), [Developer Support](https://developers.facebook.com/support/), and [Success Stories](https://developers.facebook.com/success-stories/) as well as steps to complete the Tech Provider onboarding process.

## Step 1: Verify your business

To become a tech provider you need to [verify your business with Meta](https://www.facebook.com/business/help/2058515294227817). If you already have a verified business, and linked it to your app during the app creation process, this step will be marked as completed and you can [start the app review process](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/app-review).

Click **Start verification** to verify your business. You’ll need the following information:

- Verify business details – Provide your business name, address, phone number, email and website for verification.
- Confirm your connection – Select a way for us to get in touch to confirm your connection to the business.
- Upload documents – You might need to upload accepted documents to confirm these details if your business is not found.

Your business must be verified before you can start the app review process.

## Step 2: App Review

Once you have completed business verification, you can submit your app for App Review. You’ll need to complete the following tasks:

- Review your app settings
- Create and submit videos of your app
- Submit documentation for App Review

### Review your app settings

Your app will need [basic settings](https://developers.facebook.com/docs/development/create-an-app/app-dashboard/basic-settings) such as an app icon, privacy policy, and app category.

### Videos

To pass App Review, you need to submit video evidence of your capabilities to send messages and manage templates.

- The first video must show a message created and sent from your app and received in the WhatsApp client (mobile app or web app).
- The second video must show your app being used to create a message template.

As an alternative, you can capture a screen recording of the **API Setup** cURL script being used by you to send a message to a WhatsApp user number you have added as a test recipient number, in lieu of sending a message using your or your partner’s app. Similarly, you can capture a screen recording of the **WhatsApp Manager** being used by you to create a template message, instead of your or your partner’s app.

If you are partnering with a Solution Partner, you can use your current integration with them to demostrate these actions.

### Submit documentation for App Review

Get approval to access advanced permissions and features so that your can manage your clients’ accounts and information.

App Review is the process that will grant you advanced access to the following permissions which are required to become a Tech Provider.

- Advanced access to `whatsapp_business_messaging` will allow you to send messages for customers.
- Advanced access to `whatsapp_business_management` allows you to onboard customers and manage their assets.

Click the **Begin App Review** button to start your submission.

[Learn more about App Review](https://developers.facebook.com/documentation/resp-plat-initiatives/individual-processes/app-review).

## Onboard with an existing Solution Partner

If you prefer to onboard with a Solution Partner, click the **Onboard with a Solution Partner** button at the bottom of the page.

After clicking the **Onboard with a Solution Partner** button, the Tech Provider onboarding page will refresh to this flow. The flow is identical to the Tech Provider flow with the additional App Review step to **Create a partner solution** by entering your partner’s app ID to create a partner solution.

To onboard without a partner, you can do so by clicking the **Onboard without a partner** button at the bottom of the page.

## Support

Confirmed Tech Providers have access to all support channels. See [Support](https://developers.facebook.com/documentation/business-messaging/whatsapp/support).

## Next steps

- Onboarding business customers - Onboarding business customers via [Embedded Signup](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/overview) .
- [Onboard WhatsApp Business app users](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users) - If your business customers already use the WhatsApp Business app, you can configure Embedded Signup to onboard them using their existing account and phone number.
- Webhooks - Before your app users can use your app to send and receive messages or manage templates, you must set up [Webhooks](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/overview) .
- Billing - Your onboarded business customers must [add a credit card to your WhatsApp Business Platform Account](https://www.facebook.com/business/help/488291839463771) .
