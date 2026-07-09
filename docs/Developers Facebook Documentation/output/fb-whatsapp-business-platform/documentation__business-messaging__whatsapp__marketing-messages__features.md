# Features | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/features_

---

# Features

Updated: Feb 10, 2026

Marketing Messages API for WhatsApp offers added features that are not available on Cloud API, such as performance benchmarks and recommendations, time-to-live, and automated creative optimizations (in testing).

For more detail, see the comparison tables below.

## Optimization features

| Description | Marketing Messages API for WhatsApp (Supports Marketing) | Cloud API (Supports Auth, Utility, Service, Marketing) |
| --- | --- | --- |
| **Quality-based delivery:** Improving deliveries of high engagement messages. | **Yes:** Marketing Messages API for WhatsApp factors if a message is high engagement into delivery decisions, offering up to 9% higher deliveries vs. Cloud API (see footnote below). High engagement marketing messages refers to messages that are expected by users, relevant, and timely, and therefore more likely to be read and clicked. | **No:** Message quality does not factor into per-user marketing message limits. No ability to increase delivery for high engagement messages. |
| **Automated creative optimizations:** Automatic enhancements to creative to increase message performance. | **Yes (pilot):** Automatically enhance the visual appeal and engagement of marketing template messages. See full list of capabilities [here](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/send-marketing-messages#automatic-creative-optimizations). | **No** |

## Marketing message formats

| Description | Marketing Messages API for WhatsApp (Supports Marketing) | Cloud API (Supports Auth, Utility, Service, Marketing) |
| --- | --- | --- |
| **Animated Image (GIF) Header:** Marketing message templates support a GIF [media type in the header](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/components#media-headers). | **Yes** | **No** |
| **Android App Deep Links:** [Links](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/deep-links) that directly open up the app on a customer’s phone. | **Yes** | **No** |
| **Customizable Message Validity Periods:** Set a [time-to-live for messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/send-marketing-messages#create-marketing-templates) that should expire if they cannot be delivered soon enough. | **Yes:** TTL can range from 12 hours to 30 days. | **Limited:** Only supports Authentication and Utility messages. |
| **Basic marketing message formats:** [Media, carousel, product catalog, flow, interactive list, interactive reply, etc.](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/marketing-templates) | **Yes** | **Yes** |

## Guidance

| Description | Marketing Messages API for WhatsApp (Supports Marketing) | Cloud API (Supports Auth, Utility, Service, Marketing) |
| --- | --- | --- |
| **Benchmarks:** Comparison of read and click rates versus similar templates from businesses in your region. | **Yes** | **No** |
| **Recommendations:** Evidence-based recommendations to improve the performance of your template. | **Yes** | **No** |

## Metrics

| Description | Marketing Messages API for WhatsApp (Supports Marketing) | Cloud API (Supports Auth, Utility, Service, Marketing) |
| --- | --- | --- |
| **Conversion metrics:** Conversions on Web and App. | **Yes:** [Measure marketing messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/measure-conversion#measure-app-conversions-with-meta-sdk-or-app-events-api) leading users to perform app events, such as “Add to Cart”, “Checkout Initiated”, and “Purchase”. | **No** |
| **Cost metrics:** [Spend per Template, Cost per click, Cost per delivery.](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/view-metrics) | **Yes** | **Yes** |
| **Basic metrics:** [Sent, delivered, read, clicked, errors.](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/view-metrics) | **Yes** | **Yes** |

## Enterprise, Security & Compliance Features

| Description | Marketing Messages API for WhatsApp (Supports Marketing) | Cloud API (Supports Auth, Utility, Service, Marketing) |
| --- | --- | --- |
| **Local Storage Support:** Phone numbers with [Local Storage enabled.](https://developers.facebook.com/documentation/business-messaging/whatsapp/local-storage) | **Yes** | **Yes** |
| **Compliance certification:** Compliance resources available on the [Business Messaging Compliance Center](https://www.facebook.com/business/business-messaging/compliance). | **Yes:** Certification for LGPD, GDPR, System Audit Report, SOC, ISO27001. | **Yes:** Certification for LGPD, GDPR, System Audit Report, SOC, ISO27001. |
| **Automatic throughput upgrades:** Automatic upgrades (and webhook notifications) to a phone number’s [messaging throughput](https://developers.facebook.com/documentation/business-messaging/whatsapp/throughput). | **Yes** | **Yes** |
| **Real-time service status updates:** [Uptime and availability metrics](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/api-status-page) are live on [metastatus.com](https://metastatus.com/whatsapp-business-api?fbclid=IwY2xjawM2uLNleHRuA2FlbQIxMQBicmlkETFPWE5PUldSeE95a2tuMnA1AR4r-Af63nidsmVRDdEJ4WtriGpxdlenOA60_uzhuqXHr06lE0-d2S9pnJm_Ww_aem_WtrDEZEwN2EZflsD4vmusQ). | **Yes** | **Yes** |

## Onboarding

| Description | Marketing Messages API for WhatsApp (Supports Marketing) | Cloud API (Supports Auth, Utility, Service, Marketing) |
| --- | --- | --- |
| **Streamlined Onboarding:** [Onboard via Embedded Signup, Intent API, and Intent UI](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/onboarding). | **Yes** | **Limited:** Embedded signup only. |
| **Error Codes:** Graph API [error codes](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/error-codes#marketing-messages-api-for-whatsapp-error-codes). | **Yes:** [Specific Marketing Messages API for WhatsApp error codes](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/error-codes#marketing-messages-api-for-whatsapp-error-codes). | **Yes** |
| **Onboarding Status via API:** Granular [eligibility status data and error codes](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/changelog#july-15--2025). | **Yes:** A [new eligibility status field](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/onboarding#eligibility-requirements) has been introduced to better report on the API onboarding status. | **Limited** |
| **WhatsApp Business app user onboarding:** [Onboard WhatsApp Business app users.](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/onboard-business-customers#onboard-whatsapp-business-app-users) | **Yes** | **Yes** |

## Footnote

The A/B test was conducted with ~12 million delivered marketing messages sent by advertisers in India between 1st Jan 2025 to 31st Jan 2025. It compared Marketing Messages API for WhatsApp optimized delivery to standard Cloud API delivery for high engagement messages only (that is to say, more reads, clicks, etc.) and the analysis consisted of a t-test at 95% confidence.
