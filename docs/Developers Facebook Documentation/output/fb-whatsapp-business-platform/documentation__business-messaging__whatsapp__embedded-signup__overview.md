# Embedded Signup | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/overview_

---

# Embedded Signup

Updated: Nov 25, 2025

Embedded Signup is an authentication and authorization desktop- and mobile-compatible interface that makes it easy for your business customers to generate the assets you will need to successfully onboard them to the WhatsApp Business Platform.

The Embedded Signup flow gathers business-related information from your business customers, automatically generates all WhatsApp assets needed by the platform, and grants your app access to these assets, so you can quickly provide your business customers with WhatsApp messaging services.

## How it works

Embedded Signup leverages the Facebook Login for Business product and our JavaScript SDK. Once configured, you can add a link or button to your website or portal that launches the flow.

Business customers who click the link or button will be presented with a new window where they can:

- authenticate their identity using their Facebook or Meta Business Credentials
- accept terms of service for Cloud API, WhatsApp Business, Meta, Marketing Messages Lite API and Meta Business Tool Terms
- select multiple WhatsApp APIs and accept terms of service
- grant your app access to their WhatsApp assets
- select an existing business portfolio or create a new one
- select an existing WhatsApp Business Account (WABA) or create a new one
- enter and verify their business phone number (their own, or one you have provided)
- enter a display name that can appear in place of their number in the WhatsApp client

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/531995822_1112262264200439_63249353490863536_n.png?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=iEzrcxa_ngQQ7kNvwHH-iOq&_nc_oc=AdoKgiiY6AsHccX7Pnh3WVQGh8kaJaV_sp5cuafzGSEW8o_YvUWg34Botnpf7L2xf8A&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=gQ647IeCxcE1ik8EFdqltQ&_nc_ss=7b20f&oh=00_Af6IwykB52PjeNT_bkRFoVp9xwTdCNYE7TLaILJvHwa30A&oe=6A1C3340)

Upon successful completion, Embedded Signup returns the customer’s WABA ID, business phone number ID, and an exchangeable token code, to the window that spawned the flow. You must send this data to your server and use it in a server-to-server call to:

- exchange the code for a customer-scoped business token
- register the customer’s business phone number for Cloud API use
- subscribe your app to webhooks on the customer’s WABA
- share your credit line with the customer (Solution Partners only)

When these steps are complete, if you are a Solution Partner or are partnered with one, the customer can begin using your or your partner’s app for messaging immediately. If you are not a Solution Partner, or not partnered with one, the customer must first attach a payment method to their WABA before they can begin messaging.

We’re testing a new experience in the Embedded Signup flow for all versions. The flow itself is unchanged, but after completion, you may see a new **View your setup guide** button. Clicking it will take you to a new setup guidance page in WhatsApp Manager, which offers next steps on:

- Business verification
- Resolving integrity issues and accessing Business Support Home
- Sending the first message via a partner solution
- Sending business-initiated messages using templates

## Asset ownership

Business customers onboarded via Embedded Signup own all of their WhatsApp assets, which they can leverage with other Meta solutions such as [Ads that Click to WhatsApp](https://www.facebook.com/business/help/447934475640650).

Business customers also have full access to [WhatsApp Manager](https://business.facebook.com/wa/manage/), which they can use to access their assets. Note that you cannot restrict this access in any way. Refer to available assets [here](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/version-4).

## Limitations

### Onboarding limits

By default, you can onboard up to 10 new business customers in a rolling 7-day window. Only newly onboarded customers count against this limit. You can see your current onboarded customer count in the **WhatsApp Manager** > **Partner overview** panel. You will be notified by email if you approach this limit.

If you complete Business Verification, App Review, and Access Verification, we will automatically increase your limit to 200 new business customers in a rolling 7-day window. If you need to onboard more than 200 customers per week, apply to become a [Meta Business Partner](https://business.whatsapp.com/partners/become-a-partner).

**Note:** Existing WhatsApp Business Accounts (WABAs) that were originally created via the developer app cannot be selected or onboarded directly through the Embedded Signup flow.

### Business customer messaging limits

Business customers onboarded via Embedded Signup start with standard [messaging limits](https://developers.facebook.com/documentation/business-messaging/whatsapp/messaging-limits), which can be increased through API usage.

### Business customer phone number limits

- Business phone numbers can only be registered for use with Cloud API.
- Business phone numbers already in use with the [WhatsApp Business app](https://business.whatsapp.com/products/business-app) are supported, but require you customize the flow to enable [WhatsApp Business app user onboarding](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users) .
- Business customers onboarded via Embedded Signup start with default [messaging limits](https://developers.facebook.com/documentation/business-messaging/whatsapp/messaging-limits) .

## Cloud API flow

See [Cloud API Flow](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/default-flow) for descriptions of each screen that your business customers will be presented with as part of the default implementation of Embedded Signup.

Note that if you know information about your customer’s business, you can [inject this data](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/pre-filled-data), which can significantly reduce the number of screens that your customers have to interact with.

## Access tokens

Embedded Signup generates [business tokens](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens). When a business customer completes the Embedded Signup flow, an exchangeable token code will be returned as a message event and captured by the JavaScript SDK. You must exchange this code for a business token using a server-to-server call.

If you are a Tech Provider, you will use business tokens exclusively.

If you are a Solution Partner, you will use your [system user access token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens) (“system token”) to share your credit line with onboarded business customers, and business tokens for everything else. Note that the system user who the token represents must have granted your app the **business_management** permission, and must have been granted an **Admin** or **Financial Editor** role on your business portfolio, in order to be able to share your credit line.

## Permissions

Embedded Signup can be configured to support business messaging products for your customers. If you are only interested in the Cloud API flow you are likely only going to need:

- **whatsapp_business_management** — necessary if your app needs access to onboarded customer WhatsApp Business Account settings and message templates.
- **whatsapp_business_messaging** — necessary if your app needs access to onboarded customer business phone number settings, or if your app will be used by customers to send and receive messages.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/557723935_1324509125987117_1998262003463700459_n.png?_nc_cat=102&ccb=1-7&_nc_sid=e280be&_nc_ohc=hu1QIiWzDKUQ7kNvwHhxkLq&_nc_oc=Adp4WslYxvHCzvg85rZaO4eYCDikbj-B6lxplikQB7s3VpXHdor8-rlAwRpbYG2pKm8&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=gQ647IeCxcE1ik8EFdqltQ&_nc_ss=7b20f&oh=00_Af7ITtRQMlRGL7uqgpb88rdTb5rpQZu3vU3wJ_dE3fYfsg&oe=6A1C321F)

You can specify which permissions your app needs during the [implementation](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/implementation) process.

Note that while your app is in development mode, these permissions will appear in Embedded Signup’s [authorization screen](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/default-flow#authorization-screen) to anyone who has an **admin**, **developer**, or **tester** role on your app. However, once you switch your app to live mode, only permissions that have been approved for advanced access through the [App Review](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/app-review) process will appear in the flow.

## Billing

### Solution Partners

If you are a Solution Partner, you must already have a [line of credit](https://www.facebook.com/business/help/1684730811624773?id=2129163877102343) and have accepted the Credit Allocation API terms in the **Business Settings** > **Payments** panel in the Meta Business Suite. In addition, you must share your line of credit with any customers as part of the onboarding process.

### Tech Providers and Tech Partners

If you are a Tech Provider or Tech Partner, your onboarded business customers must add a payment method to their WhatsApp Business Account. They can do this by following the steps described in our [Add a credit card to your WhatsApp Business Platform account](https://www.facebook.com/business/help/488291839463771) Help Center article.

## Sandbox accounts

You can test the Embedded Signup flow using your own Facebook account, but this can result in additional business portfolios, WABAs, and business phone numbers. If you don’t want to clutter your Facebook account with test data, you can claim a sandbox test account instead, and use it to simulate a business customer completing the flow.

When you complete the flow using the sandbox account, the sandbox account’s [WABA ID, business phone number ID](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/implementation#session-logging-message-event-listener), and an [exchangeable token code](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/implementation#response-callback) will be returned, just as if it were a real customer completing the flow.

### Sandbox account limitations

- Sandbox accounts are valid for 30 days, after which they will be deactivated and must be reclaimed in order to be used again.
- The sandbox account cannot be used to create additional sandbox business portfolios, WABAs, or business phone numbers; the assets are generated automatically and will appear in the Embedded Signup flow.
- The sandbox account is associated with the app’s admin. In order for the sandbox account’s assets to appear in the Embedded Signup flow, the app admin must be signed into their Meta developer account.
- The sandbox account’s business portfolio will not appear in the Meta Business Suite or WhatsApp Manager
- You can exchange the returned token code for the sandbox account’s business token and use it to get data on the account’s WABA ID, but the business phone number cannot be used to send or receive messages.

### Claiming sandbox accounts

To claim your sandbox account:

1. Navigate to the [App Dashboard](https://developers.facebook.com/apps) > **WhatsApp** > **Quickstart** panel.
2. Locate the **Testing Integrations** section.
3. Click the **Claim sandbox account** button.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/513080744_1153803566552470_4289383978669775503_n.png?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=O21Sn-eXzoYQ7kNvwG8QTER&_nc_oc=Adrp3piJxPQULg6S0OuDFQbDPF-0Ms1J04i9MWzBrIhA18n9-Vo7gKaIIxbhctTRFOo&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=gQ647IeCxcE1ik8EFdqltQ&_nc_ss=7b20f&oh=00_Af6Hc3h9-Ndct8kbKMKna-WKzLrfpovynP9w047vc8iZdw&oe=6A1C1F13)

### Deleting sandbox accounts

Sandbox account deletion is being released gradually over several weeks, starting June 25, 2025.

If you are done testing and want to keep your testing environment clean, you can delete your sandbox account. Deleting a sandbox account is irreversible and removes all associated test data. If you accidentally delete your sandbox account but need to test again, you must claim a new one.

To delete your sandbox account:

1. Navigate to the [App Dashboard](https://developers.facebook.com/apps) > **WhatsApp** > **Quickstart** panel.
2. Locate the **Testing Integrations** section, then locate your sandbox account.
3. Click your sandbox account’s **Delete account** button.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/511293188_1404444270796306_3723440624353556557_n.png?_nc_cat=101&ccb=1-7&_nc_sid=e280be&_nc_ohc=nkX7xtoK0dgQ7kNvwHtXht7&_nc_oc=AdpmEiYcGnH5pe7gAxyu3BANKrxvAugJg8zGgrF3-c7w0A90KBVviuTJme59ECd8xfk&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=gQ647IeCxcE1ik8EFdqltQ&_nc_ss=7b20f&oh=00_Af6BMBZz9-98XiWrY4kCmOB14aaelZqMWrnMwjAFV0DfBw&oe=6A1C0E6C)

## 555 business phone numbers

Business customers can claim up to two 555 business phone numbers. These numbers behave the same way as standard business phone numbers (subject to pricing rules, impacted by quality ratings, etc.), but must have their display names approved before they can be used to send messages. In addition, 555 numbers:

- Have a US country calling code (+1)
- Have a 555 area code
- Are verified automatically
- Cannot be migrated to another WhatsApp Business Account, or used outside of the WhatsApp Business platform

If your business customers are eligible for 555 numbers, the [phone number addition screen](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/default-flow#phone-number-addition-screen) will automatically give them the option to choose a 555 number:

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/557624038_1991414544970922_7818680630707794930_n.png?_nc_cat=110&ccb=1-7&_nc_sid=e280be&_nc_ohc=XxFDoA3i5QIQ7kNvwE9H246&_nc_oc=Adp0JrBUbyg24JTBAmxhlGMe7lF6LGDjEDqKLBuZ0T7kF64SQQ0B5nV8jZxAjvTOY2A&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=gQ647IeCxcE1ik8EFdqltQ&_nc_ss=7b20f&oh=00_Af4Q4Fvfr9FKW-kQnj1LXvtyn_9COPssKbJJRpzqTko1Eg&oe=6A1C2D20)

## WhatsApp Asset migration

Embedded Signup can be used to migrate onboarded business customer assets in several ways. See [Migrating business customer assets](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/support#migrating-business-customer-assets).

## App Review

You will not be able to onboard business customers until your app has been approved for **advanced access** for each of the permissions it requires.

See [App Review](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/app-review) to learn more about App Review and what you must provide in order to complete the process successfully.

## Embedded Signup Integration Helper

The Embedded Signup Integration Helper is a setup and testing tool within the App Dashboard. The tool allows you to:

- launch Embedded Signup in various flow configurations
- see data that gets returned when a business customer completes the flow
- generate implementation code and onboarding queries, which you can copy and paste into your website, business customer portal, and server
- send API queries to endpoints you will need to use when onboarding customers who complete the flow

You can access the integration helper by navigating to **App Dashboard** > **WhatsApp** > **Embedded Signup Builder**.

**Note:** The Embedded Signup Integration Helper is available only for Business-type apps. You can view your app type at the top of the app dashboard.

## Webhooks

As part of the onboarding process, you must subscribe your app to webhooks on the WABA of each business customer who completes the Embedded Signup flow.

Webhooks will be triggered and sent to the callback URL configured on your app, according to the webhook fields you have subscribed to. This means that all webhooks for all of your onboarded business customers will be sent to your app’s callback URL. However, you can override the callback URL on an individual WhatsApp Business Account or business phone number. See [Webhook Overrides](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/override) to learn how to do this.

## Localization

The Embedded Signup flow is available in 30 languages. The localized flow is automatically triggered based on the language that the business customer uses Facebook in.

Arabic, Czech, Danish, Greek, English (UK), Spanish (Spain), Spanish, Finnish, French (France), Hebrew, Hindi, Hungarian, Indonesian, Italian, Japanese, Korean, Norwegian (bokmal), Dutch, Polish, Portuguese (Brazil), Portuguese (Portugal), Romanian, Russian, Swedish, Thai, Turkish, Vietnamese, Simplified Chinese (China), Traditional Chinese (Hong Kong), Traditional Chinese (Taiwan).

## Next steps

Learn how to [implement Embedded Signup](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/implementation) into your website or portal.
