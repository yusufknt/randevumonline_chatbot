# Per-user marketing template message limits | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/marketing-templates/per-user-limits_

---

# Per-user marketing template message limits

Updated: Apr 29, 2026

## Overview

WhatsApp may limit the number of marketing template messages a WhatsApp user receives from any business in a given period of time when they are less likely to be receptive and engage with them. This is determined based on a number of factors, including a dynamic view of an individual’s recent marketing message read rate and how many messages they currently have in their inbox from friends, family, and businesses.

The per-user marketing limit adapts automatically over time based on a person’s recent engagement levels. While this may mean delivering fewer messages to some WhatsApp users during periods of lower marketing read rates or overall inbox activity, your ability to reach people when they are most engaged does not change.

### United States phone numbers

WhatsApp does not currently deliver marketing template messages to WhatsApp users with United States phone numbers (numbers composed of a +1 dialing code and a US area code). This pause is intended to allow us to focus on building a better consumer experience in the US, which will ultimately lead to improved outcomes for businesses. Attempting to send a template message to a WhatsApp user with a US phone number after this date will result in an error.

### Excluded countries

Per-user marketing template message limits are not currently active for messages sent from a business phone number in the European Economic Area, United Kingdom, Japan, or South Korea, or to a WhatsApp user in these countries.

### How limits are counted

Each marketing template message delivered counts towards the per-user marketing limit. If a WhatsApp user responds to a marketing message, it starts a 24-hour [customer service window](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages#customer-service-windows). Marketing messages sent within this window do not count towards the limit.

### Retry limits

To ensure your campaigns are most likely to reach your audience, we recommend waiting at least 24 hours before attempting to resend a marketing template message to a user that has reached their limit. Resending earlier than this will likely result in additional error responses and can reduce the accuracy of campaign delivery reporting.

WhatsApp enforces limits on excessive retry attempts of marketing template messages to users that have reached their per-user marketing template limit. If your WhatsApp Business Account (WABA) attempts to resend marketing messages multiple times within a 24-hour period to users who have already reached their messaging limit, further delivery attempts to these users may be unavailable for up to 24 hours and error code 131049 will be returned. This does not affect your ability to send marketing messages to other users.

## Error code

If a marketing template message is not delivered due to per-user marketing template limit enforcement or a business has repeatedly attempted to resend a message to a user that has reached their limit, the messages webhook is triggered with status set to failed and error code set to 131049. If you receive this error code, wait at least 24 hours before resending the template message.
