# Partners | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/overview_

---

# Partners

Updated: Apr 2, 2026

This documentation contains information, instructions, and resources for **partners** — businesses that provide, or want to provide, WhatsApp messaging services to other businesses. If you are building an app that will not be used by other businesses, refer to our [Cloud API Get Started](https://developers.facebook.com/documentation/business-messaging/whatsapp/get-started) guide instead.

Partners are business entities that deploy value-added solutions as WhatsApp authorized service providers on behalf of their clients. Partners include Solution Partners, Tech Providers, and Tech Partners.

## Solution Partners

Solution Partners are [Meta Business Partners](https://www.facebook.com/business/marketing-partners/become-a-partner) that provide a full range of WhatsApp Business Platform services to other businesses (clients), such as messaging services, billing, integration support, and customer support.

Solution Partners have [credit lines](https://www.facebook.com/business/help/1684730811624773?id=2129163877102343) which can be extended to business customers who they bring on board, thus removing the need for those customers to enter their own payment method during the onboarding process. Furthermore, Solution Partners can directly invoice their customers for the WhatsApp Business Platform services provided through their apps.

In addition, Solution Partners have access to [Direct Support](https://developers.facebook.com/documentation/business-messaging/whatsapp/support#enterprise-developer-support) and are eligible to participate in the [Meta Business Partner SMB Accelerator Program](https://www.facebook.com/business/marketing-partners/mbp-smb-accelerator), which offers incentive, accreditation, and enablement services.

Note that becoming a Solution Partner is a lengthy process, so if you don’t need a credit line and don’t need to invoice your business customers for API usage directly, consider becoming a Tech Provider instead.

See [Get started for Solution Partners](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/get-started-for-solution-partners).

## Tech Providers

Tech Providers are similar to Solution Partners in that they also can offer a full range of WhatsApp Business Platform services to other businesses, either by providing these services on their own, or by [partnering with a Solution Partner](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/multi-partner-solutions) who already offers these services.

Unlike Solution Partners, however, Tech Providers do not have credit lines. Instead, business customers onboarded by Tech Providers must provide their own payment method after onboarding is complete. Meta will then bill these customers for API usage, and the Tech Provider will bill for other services.

Tech Providers also cannot participate in the [Meta Business Partner SMB Accelerator Program](https://www.facebook.com/business/marketing-partners/mbp-smb-accelerator), unless they upgrade to a Tech Partner. However, Tech Providers do have access to [Direct Support](https://developers.facebook.com/documentation/business-messaging/whatsapp/support#enterprise-developer-support).

To learn how to become a Tech Provider, see [Become a Tech Provider](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/get-started-for-tech-providers).

## Tech Partners

Tech Partners are Tech Providers who are, or are eligible to become, [Meta Business Partners](https://www.facebook.com/business/marketing-partners/become-a-partner). Tech Providers who apply to become a Meta Business Partner and are approved are eligible to participate in the [Meta Business Partner SMB Accelerator Program](https://www.facebook.com/business/marketing-partners/mbp-smb-accelerator).

To learn how to upgrade to a Tech Partner, see [Upgrading to a Tech Partner](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/upgrade-to-tech-partner).

## Other partners

If you just want to use Meta Business Suite to provide WhatsApp messaging-related services to business customers (that is, you **don’t need API access**), you only need a verified business portfolio.

1. Go to [https://business.facebook.com](https://business.facebook.com/) and create a business portfolio, or sign into your existing Meta Business Suite account if you already have one.
2. Complete the [business verification steps](https://www.facebook.com/business/help/2058515294227817) described in our Help Center article.

Once your business is verified, provide your business portfolio ID to any business customers for whom you wish to provide service, and ask them to [share their WhatsApp Business account](https://developers.facebook.com/documentation/business-messaging/whatsapp/whatsapp-business-accounts#share-your-waba-with-a-solution-provider) with you. Once shared, you can use Meta Business Suite to access their account and provide services.

## Comparison

|  | Solution Partners | Tech Providers | Tech Partners |
| --- | --- | --- | --- |
| Can offer full WhatsApp Business Platform services to onboarded customers | Yes | Yes | Yes |
| Has a credit line | Yes | No | No |
| Customers bypass payment method collection | Yes | No | No |
| Bills customers directly for API usage (vs. Meta billing customers for usage) | Yes | No | No |
| Is a Meta Business Partner | Yes | No | Yes |
| Eligible for accelerator program | Yes | No | Yes |
| Access to Direct Support | Yes | Yes | Yes |

## Onboarding business customers

There are multiple ways for you to onboard business customers.

### Embedded Signup

[Embedded Signup](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/overview) is a scalable, authentication and authorization interface that can be launched directly from your website or customer portal. Embedded Signup automatically generates all required WhatsApp assets for business customers who successfully complete the flow, and authorizes your app to access those assets.

### Onboard WhatsApp Business app users

You can configure Embedded Signup to [onboard business customers who already use the WhatsApp Business app](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users). These customers can connect their existing WhatsApp Business app account and phone number to Cloud API, allowing them to use your app to message at scale while still using the WhatsApp Business app for one-to-one conversations.

### Hosted Embedded Signup

[Hosted Embedded Signup](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/hosted-es) (“Hosted ES”) is an alternative and simpler way of implementing Embedded Signup that doesn’t require you to configure and host the implementation code on your website or portal.

### Partner-initiated account creation

If you are a Solution Partner, you can [initiate WhatsApp Business account creation](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/partner-initiated-waba-creation) for a business customer who can then use Meta Business Suite to approve or decline creation.

### Meta Business Suite

Your business customers can [use Meta Business Suite to create a WhatsApp Business account](https://developers.facebook.com/documentation/business-messaging/whatsapp/whatsapp-business-accounts#create-a-waba-via-meta-business-suite) on their own and [share it with you](https://developers.facebook.com/documentation/business-messaging/whatsapp/whatsapp-business-accounts#share-your-waba-with-a-solution-provider).

## Multi-Partner Solutions

[Multi-Partner Solutions](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/multi-partner-solutions) allow partners to jointly manage onboarded business customer assets to provide comprehensive WhatsApp messaging services. For example, if you are a Tech Provider, you may wish to create a multi-partner solution with a Solution Partner who can share their credit line with business customers onboarded via your joint solution.

## Access tokens

If you are a Tech Provider or Tech Partner, you should use **business tokens** exclusively. If you are a Solution Partner, you should use a system token only when sharing your credit line with onboarded business customers; in all other cases, use business tokens.

### System tokens

System tokens are described in our API documentation, as they are used by non-partners as well. See [System User Access tokens](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens) to learn how to create a system user and token.

When creating your system user, aside from granting it any permissions and roles your app needs, also grant it the **Finance editor** role:

1. Sign into the [Meta Business Suite](https://business.facebook.com/) .
2. Locate your business portfolio in the top-left dropdown menu and click its **Settings** (gear) icon.
3. Click **Business settings** .
4. Navigate to **Users** > **System Users** .
5. Edit the user and grant it the **Finance editor** role.

This will allow your app to use the API to share your credit line with onboarded customers.

### Business tokens

[Business tokens](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens) are access tokens scoped to individual onboarded business customers. Use these tokens when accessing onboarded customer data, such as WhatsApp Business Accounts, message templates, business phone numbers, and when sending and receiving messages for your customers.

To get a business token that is scoped to a customer, you must exchange a code returned to you when that customer completes the [Embedded Signup](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/overview) flow. This process is described in the Onboarding Business Customers section of the Embedded Signup documentation.

## Permissions

The [permissions](https://developers.facebook.com/documentation/business-messaging/whatsapp/permissions) your app requires from onboarded customers depends on the services you provide. These are described in broad terms below but are largely determined by the endpoints your app will be querying.

The most commonly needed permissions are:

- **whatsapp_business_management** — necessary if your app needs access to onboarded customer WhatsApp Business account settings and message templates.
- **whatsapp_business_messaging** — necessary if your app needs access to onboarded customer business phone number settings, or if your app will be used by customers to send and receive messages.

Note that before your app can be granted these permissions by your business customers, the permissions must be approved through the [App Review](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/app-review) process.

## App Review

Before you can officially begin onboarding business customers, you must submit your app for [App Review](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/app-review) and request **advanced access** approval for any permissions your app requires.

If advanced access is not approved for a given permission, the permission will not appear in the Embedded Signup flow and your business customers will be unable to grant it to your app.

## Business Verification

To be eligible for increased messaging limits, business phone number limits, and Official Business Account status, your business customers must verify their business. Your business customers can submit their business for verification by following the instructions in the following Help Center article:

[How to Verify Your Business on Meta](https://www.facebook.com/business/help/2058515294227817?id=180505742745347)

Alternatively, if you are a **Select Solution** or **Premier** Solution Partner, you can submit a customer’s business for verification on their behalf, which has a much faster turnaround time. See [Partner-led Business Verification](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/partner-led-business-verification).
