# WhatsApp Business Platform policy and spam enforcement | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/policy-enforcement_

---

# WhatsApp Business Platform policy and spam enforcement

Updated: Nov 4, 2025

To maintain high-quality experiences at scale on the WhatsApp Business Platform, WhatsApp will enforce on WhatsApp Business Accounts that repeatedly violate the [WhatsApp Business Messaging Policy](https://www.whatsapp.com/legal/business-policy/), the [WhatsApp Commerce Policy](https://www.whatsapp.com/legal/commerce-policy/), or the [WhatsApp Business Terms of Service](https://www.whatsapp.com/legal/business-terms).

The goal of this guide is to educate businesses on how this enforcement system works and the product experience.

This document does not include information on [messaging limits](https://developers.facebook.com/documentation/business-messaging/whatsapp/messaging-limits) based on quality rating.

## How it works

Initially, WhatsApp Business Accounts will get a warning with information on the policy they violated.

If Business Accounts repeatedly violate the [WhatsApp Business Terms of Service](https://www.whatsapp.com/legal/business-terms), such as sending spam, template misclassifications, or high-risk policy categories such as adult content, sale of alcohol and tobacco, drugs, gambling and unsafe supplements, they might start seeing messaging restrictions that gradually increase in duration.

These restrictions can look like:

- 1 or 3 day block on sending marketing, utility, and authentication template messages and adding additional phone numbers to the account
- 5, 7, or 30 day block on sending any messages and adding additional phone numbers to the account
- An account lock, which is an indefinite block on sending any messages; can only be removed via an appeal
- Eventually be permanently disabled from the WhatsApp Business Platform, if the business does not make changes after multiple warnings and feature limits or blocks

In some cases, where there is evidence of a policy violation that causes severe harm to our users, such as child exploitation, scams, terrorism, or the sale of illegal drugs, WhatsApp will immediately offboard these Business accounts.

We might also limit or offboard your business from WhatsApp if your account receives excessive negative feedback from users.

Violations might be appealed or acknowledged, based on violation type and eligibility.

## Product experience

We have a comprehensive product experience so that businesses and Solution Providers can access transparent, granular and actionable information about violations via multiple channels.

### Business Support Home

When a business account violates a policy, additional detail can be found by reviewing the violation in the [Business Support Home](https://business.facebook.com/business-support-home) section of Meta Business Suite or Business Manager.

To access **Business Support Home** in Meta Business Suite:

1. Sign into [Meta Business Suite](https://business.facebook.com) .
2. Click **All tools** in the left-side menu, then click **Business Support Home** .
3. Click **Account Overview** (the speedometer icon) in the left-side menu, if necessary.

To access **Business Support Home** in Business Manager:

1. Sign into [Business Manager](https://business.facebook.com) .
2. Click the **All tools** icon (three horizontal lines) at the top of the page, then click **Business Support Home** .
3. Click **Account Overview** (the speedometer icon) in the left-side menu, if necessary.

### Understanding violations

Violation updates include the following information:

- Summary of policy violated and link to the policy itself.
- Examples of which content is allowed or disallowed based on that policy.
- Whether there are any active restrictions on the account and what happens if the violation happens again.
- How to avoid future policy violations and links to helpful resources.
- How to appeal.

Notifications about violations are also:

- Surfaced in the **Business Manager Notifications Center** and as a banner in **WhatsApp Manager** .
- Sent as an email to all admins set in **Business Manager** . To ensure proper delivery of notifications, please ensure admin information displayed in Business Manager is accurate and up-to-date.
- Sent as a [webhook notification](https://developers.facebook.com/documentation/business-messaging/whatsapp/policy-enforcement#webhooks) to those subscribed.

### Enforcement actions

Accounts can become restricted or disabled depending on the number and severity of issues. Specific restrictions can be viewed in [Business Support Home](https://developers.facebook.com/documentation/business-messaging/whatsapp/policy-enforcement#business-support-home) along with information on next steps and requesting a review for a particular policy issue.

Restricted or disabled accounts can still appeal or acknowledge issues. If issues are reversed following the appeal or acknowledgment, the account returns to its previous status.

## Webhooks

Integrate with webhooks to receive real-time notifications about changes to a WhatsApp Business Account (WABA). Subscribe to the [account_update](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/account_update) webhook to receive real-time notifications whenever a WhatsApp Business Account has violated a policy, and when applicable, messaging restriction type and duration. This ensures businesses can quickly adjust behavior to avoid additional warnings and/or enforcement actions.

## Appeals

If a business believes it is actually compliant with WhatsApp policies, it can appeal the violation by requesting a review. When a business appeals a violation, the WhatsApp team reviews the appeal against the violation policy to make a decision on if the violation should be reconsidered. This review might result in WhatsApp reversing the violation.

**Note:** Not all spam violations might be appealed. Businesses might have to wait until the restriction period ends to begin messaging again.

This is how you request a decision review:

1. From the **Business Support Home** page, select the relevant WhatsApp Business Account.
2. Choose from the list of violations and click **Request Review** .
3. A new dialog opens in Business Manager. Enter supporting details and click **Submit** .
4. After submission, the request and the issue are moved to the **In Review** tab.
5. The appeal review decision will be sent via Business Manager and typically takes 24 to 48 hours. The appealed violation will either remain **Unchanged** or be set as **Reversed** .

## Preventing future violations

- Read the [Commerce](https://www.whatsapp.com/legal/commerce-policy/) and [Business](https://www.whatsapp.com/legal/business-policy/) Policies and review [this article](https://faq.whatsapp.com/general/whatsapp-business-api/how-to-comply-with-the-whatsapp-business-and-commerce-policies) that answers frequently asked questions about these policies.
- Subscribe to the [account_update](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/account_update) webhook to receive real-time notifications whenever a Business Account has violated a policy, and when applicable, messaging restriction type and duration.
- Adjust behavior on the platform quickly to avoid additional warnings and/or enforcement actions.
- Review best practices for sending high-quality messages on WhatsApp defined in the [WhatsApp Business Messaging Policy](https://www.whatsapp.com/legal/business-policy/) .
