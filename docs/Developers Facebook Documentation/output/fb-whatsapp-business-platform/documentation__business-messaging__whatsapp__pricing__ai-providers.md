# New pricing policy for AI Providers leveraging the WhatsApp Business Platform | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/ai-providers_

---

# New pricing policy for AI Providers leveraging the WhatsApp Business Platform

Updated: Mar 4, 2026

This page is specific to “AI Providers” using the WhatsApp Business Platform. This does NOT change how Meta charges all other businesses using the WhatsApp Business Platform. Refer to the [pricing page](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing).

### Who this applies to

This is specific to “AI Providers” using the WhatsApp Business Platform, as defined in our [Terms of Service](https://www.whatsapp.com/legal/business-solution-terms/) updated on January 15, 2026: Providers and developers of artificial intelligence or machine learning technologies, such as large language models, generative artificial intelligence platforms, general-purpose artificial intelligence assistants, or similar technologies who provide certain services on WhatsApp Business Platform.

This does **NOT** change how or what Meta charges all other businesses using the WhatsApp Business Platform. They will continue to be charged as outlined in the [pricing explainer](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing#cloud-api-and-marketing-messages-api-for-whatsapp). This includes *not* being charged for non-template messages sent in an open customer service window. This also does not change the mechanics of the [customer service window](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages#customer-service-windows).

### Why Meta is charging

*Specifically for third party AI Providers:*

- Effective January 15, 2026, WhatsApp’s [Terms of Service update](https://www.whatsapp.com/legal/business-solution-terms/) “AI Providers” are only permitted to offer general purpose AI assistants on the WhatsApp Business Platform where Meta is legally required to permit this use case.
- Effective February 16, 2026, in countries where Meta is legally required to support AI Providers usage of the WhatsApp Business Platform, Meta will charge AI Providers for non-template messages sent to WhatsApp users in these countries.

### What and where Meta will charge

*Effective February 16, 2026* – Meta will charge for:

- Each non-template message ( `"type":"text", "type":"image"` , and so on)
- Delivered from an “AI Provider”
- To a user in a market where Meta is legally required to permit AI Providers to use the WhatsApp Business Platform

Markets and effective dates (as of January 28, 2026):

Effective **February 16, 2026**, this applies to Italy (+39).

Effective **March 11, 2026**, this applies to the following countries:

- Austria (+43)
- Belgium (+32)
- Brazil (+55)
- Bulgaria (+359)
- Croatia (+385)
- Cyprus (+357)
- Czech Republic (+420)
- Denmark (+45)
- Estonia (+372)
- Finland (+358)
- France (+33)
- Germany (+49)
- Greece (+30)
- Hungary (+36)
- Iceland (+354)
- Ireland (+353)
- Latvia (+371)
- Liechtenstein (+423)
- Lithuania (+370)
- Luxembourg (+352)
- Malta (+356)
- Netherlands (+31)
- Norway (+47)
- Poland (+48)
- Portugal (+351)
- Romania (+40)
- Slovakia (+421)
- Slovenia (+386)
- Spain (+34)
- Sweden (+46)

For example: If a user in Italy sends an AI Provider a prompt, and the AI Provider delivers three non-template message responses to the user over a span of 5 minutes, that will incur three charges.

### Rates

- AI Provider rates for non-template messages CSV (March 4, 2026).
- AI Provider rates for non-template messages PDF (March 4, 2026).

*These rates are specific to AI Providers using the WhatsApp Business Platform. To see rates for marketing, utility, and authentication messages, please refer to [Pricing on the WhatsApp Business Platform](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing).*

### Analytics

The Pricing Analytics API will include a new `<PRICING_CATEGORY>` value of `AI_BOT` to reflect AI Provider traffic.

```
{
  "start": <START_TIMESTAMP>,
  "end": <END_TIMESTAMP>,
  "phone_number": "<BUSINESS_PHONE_NUMBER>",
  "country": "<COUNTRY_CODE>",
  "pricing_type": "REGULAR",
  "pricing_category": "AI_BOT",
  "volume": <VOLUME>,
  "cost": <COST>
}
```

### Webhooks

The [webhooks](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing#webhooks) will reflect the `<PRICING_CATEGORY>` for these non-template messages from “AI Providers” as `general_purpose_ai`.

Billable messages have `type` set to `regular` in the pricing object of status [messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/status) webhooks:

```
"pricing": {
 "billable": true,
 "pricing_model": "PMP",
 "type": "regular",
 "category": "<general_purpose_ai>"
}
```
