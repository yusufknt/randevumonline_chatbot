# Marketing Message API for Messenger overview | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/get-started_

---

# Marketing Message API for Messenger overview

Updated: May 5, 2026

This page provides an overview of the integration steps for the Marketing Message API for Messenger, which enables businesses to send paid marketing messages to people who have opted in to receive them.

The Marketing Message API for Messenger is available exclusively to [**tech providers**](https://developers.facebook.com/docs/development/release/tech-providers) with an existing app that has successfully completed [Meta App Review](https://developers.facebook.com/docs/app-review) for the following permissions:

- ads_management
- pages_messaging
- paid_marketing_messages or marketing_messages_messenger

Currently, tech providers can only serve **businesses** located in the following regions:

- Australia
- Brazil
- Chile
- Colombia
- Hong Kong

- India
- Indonesia
- Israel
- Malaysia
- Mexico

- New Zealand
- Peru
- Philippines
- Saudi Arabia
- Singapore

- Taiwan
- Thailand
- United Arab Emirates
- United States
- Vietnam (VN)

In addition, messages can be sent to **users/subscribers** in all regions **except**:

- European Union
- Japan
- South Korea
- Australia
- United Kingdom

The Marketing Message API for Messenger is only available for Web applications.

## Preparation

Prepare the following items to ensure a smooth integration with the Marketing Message API for Messenger:

- A [Meta developer account](https://developers.facebook.com/docs/development/register)
- A [Facebook Page](https://www.facebook.com/business/help/473994396650734) , [Meta business portfolio](https://www.facebook.com/business/help/1710077379203657) (optional), and a [Meta ad account that is eligible for marketing messages in Ads Manager](https://www.facebook.com/business/help/407323696966570) to use as test accounts. Ensure the ad account has a payment method set up. Follow this [guide](https://www.facebook.com/business/help/354027251751870) for setting up payment.
- You must have an established **Business type** [Meta app](https://developers.facebook.com/docs/development/create-an-app) . Your app must be in [Live mode](https://developers.facebook.com/docs/development/build-and-test/app-modes) for testing the product.Your app must have these 3 required features:
 [Messenger product](https://developers.facebook.com/documentation/business-messaging/messenger-platform) configured with the Facebook Page you intend to use.[Facebook Login for Business](https://developers.facebook.com/documentation/facebook-login/facebook-login-for-business)[Marketing API Access Tier](https://developers.facebook.com/docs/features-reference#marketing-api-access-tier)Your app must have **Advanced access** for 3 required permissions:
 `ads_management``pages_messaging``paid_marketing_messages` or `marketing_messages_messenger`
- A server that can receive [Messenger webhook event notifications](https://developers.facebook.com/documentation/business-messaging/messenger-platform/webhooks#event-notifications) .
- The app should be owned by a Meta business portfolio that is different from the one associated with your test accounts (Facebook Page, Meta business portfolio, and Meta ad account).

## Integration overview

The following steps outline the typical integration flow for supporting businesses in sending paid Marketing Messages:

| Step | Summary |
| --- | --- |
| 1: Onboarding | Create a new Facebook Login for Business configuration in the [Meta App Dashboard](https://developers.facebook.com/apps) to onboard businesses using your app. This new configuration asks businesses for the required permissions, access tokens, assets, and to sign the Terms of Service. |
| 2: [Get a list of existing subscribers](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/get-subscription-tokens) | **Businesses can only send Marketing Messages to people who have opted in to receive them.**<br>Get a list of a business’ subscription tokens that represent people who have opted in to receive Marketing Messages from that business. See [Get subscription tokens](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/get-subscription-tokens) for details. |
| 3: Sending messages | You will need to support businesses in composing and sending of Marketing Messages by building a UI in your app.<br>Once you’re ready to send the Marketing Message campaign, select one of two API options:<br>[A simplified endpoint](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/send-messages) - **our recommended option** which is easier to integrate with and covers most marketing messages needs, or[A traditional endpoint that uses the Marketing API](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/additional-resources/send-messages-mapi). |
| 4: [Monitor results](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/measure-performance) | Integrate with Meta’s insights and campaign management APIs to allow businesses using your app to view metrics for marketing message campaign performance. See [Measure campaign performance](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/measure-performance) for details. |
| 5: [Grow marketing messages audience](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/grow-marketing-messages-audience) | Growing the subscriber base increases the reach of marketing message campaigns. Multiple options are available, such as turning people who clicked Click-to-Messenger ads into subscribers. See [Grow your audience](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/grow-marketing-messages-audience) for details. |

## Next Steps

Now that you understand the integration steps, you can begin the [onboarding process](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/onboard-businesses).

## See also

- [Marketing Message API Reference](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/api-reference) — full API endpoint documentation
- [Marketing Messages FAQ](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/faq) — common questions about marketing messages
- [Messenger Platform Policy](https://developers.facebook.com/documentation/business-messaging/messenger-platform/policy) — messaging policies and compliance requirements
