# Support | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/support_

---

# Support

Updated: Nov 14, 2025

This document describes support channels available to solution providers, troubleshooting tips, and resources you may need to provide to onboarded customers.

## Support channels

Solution providers have access to all support channels. See [Support](https://developers.facebook.com/documentation/business-messaging/whatsapp/support).

## Migrating business customer assets

### Tech Providers

- [Migrating a WABA from one Multi-Partner Solution to another via Embedded Signup](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/support/migrating-wabas-among-solutions-via-embedded-signup)
- [Migrating a WABA from one Multi-Partner Solution to another via Meta Business Suite](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/support/migrating-wabas-among-solutions-via-meta-business-suite)
- [Migrating business customers off of a Multi-Partner Solution via Embedded Signup](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/support/migrating-customers-off-solutions-via-embedded-signup)
- [Migrating business customers off of a Multi-Partner Solution via Meta Business Suite](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/support/migrating-customers-off-solutions-via-meta-business-suite)

### Solution Partners

- [Migrating a WABA from one Solution Partner to another via Embedded Signup](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/support/migrating-wabas-among-solution-partners-via-embedded-signup)
- [Adding a WABA to a Multi-Partner Solution](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/support/adding-waba-to-mps)
- [Migrating a business phone number from one Solution Partner to another via Embedded Signup](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/support/migrating-phone-numbers-among-solution-partners-via-embedded-signup)
- [Migrating a business phone number from one Solution Partner to another programmatically](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/support/migrating-phone-numbers-among-solution-partners-programmatically)

## Troubleshooting

### Onboarded business customers can’t send messages

There may be situations where business customers can’t send messages after completing the Embedded Signup flow. The following checks may help resolve this issue:

- Verify that a valid payment method is attached to the WhatsApp Business Account. If there isn’t a payment method attached (either a credit line for business customers onboarded via a Solution Provider, or a credit card for customers onboarded via a Tech Provider or Tech Partner), the customer will be unable to send template messages.
- Check if a different business phone number was registered as part of the onboarding process. If this is the case, you must register the problematic number for use with Cloud API.
- Check if the WhatsApp Business Account has been disabled. We automatically disable WhatsApp Business Accounts that violate our policies, so this may be the reason.

## Feature requests

Your suggestions are valuable in helping us continue to improve our platform and meet your needs. To request a feature, submit a [Direct Support](https://business.facebook.com/direct-support/) ticket or [platform bug report](https://developers.facebook.com/support/bugs/).

Please provide as much detail as possible about the feature you’re requesting. Include a clear description of the feature, its intended use, and any relevant use case examples. If you have any supporting documentation, images, or other resources related to the feature, include them as well.

We will review your request and may reach out to you for further clarification. Thank you!
