# Identity Change | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/identity-change_

---

# Identity Change

Updated: Oct 24, 2025

A business may want to communicate private information with a customer via WhatsApp. In order to do that securely, the business must first establish trust that they are communicating with the right person via authentication (this is done off WhatsApp today).

Once trust is established between a business and a WhatsApp account, the business does not know when the person with access to the WhatsApp account may have changed.

Businesses using the WhatsApp Business Platform can choose to be notified when there was a potential update to a customer’s identity. This gives businesses a signal that the person behind the account may have changed.

In this situation, the best practice would be for the business to break the trust and authenticate the user again to re-establish trust before continuing to send personal information.

If a business opts in to this feature, they will be informed when they receive messages from users who have potentially changed ownership and will be blocked from sending messages to such users until the business acknowledges it’s safe to send the message. This will protect the business and their customers from leaking sensitive information.

## Trigger

The trigger for notifying a business is the identity for a WhatsApp account has changed.

When a business receives this signal they may want to invoke a re-authentication flow to ensure they are always exchanging personal information securely.

## Recommended Workflow

1. The business opts in to receive notifications when WhatsApp identifies a WhatsApp account with whom they are communicating is potentially under control of a different person.
2. When WhatsApp detects a potential change in the user’s cryptographic identity, WhatsApp sends notification to the business.
3. The business breaks trust with user (for example, unlinking the WhatsApp as trusted channel on their CRM)
4. The business initiates re-authentication workflow (typically done off WhatsApp).
5. The business acknowledges receipt of notification and continues to communicate with the account when they deem it safe to do so (usually following successful authentication).

All outgoing messages to the user will be blocked until the business acknowledges receipt of the notification signaling that the person in control of the WhatsApp account could have changed. Since it is the business’s responsibility to establish trust with the user before sharing sensitive information, the business is recommended to re-authenticate the user (off WhatsApp) before acknowledging the notification, which would enable the business and user to continue exchanging personal information on WhatsApp. Acknowledging the notification does *not* ensure the user is “trusted”.
