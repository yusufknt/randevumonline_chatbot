# Support for onboarded business customers | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/support/business-customer-support_

---

# Support for onboarded business customers

Updated: Nov 14, 2025

This document is intended to solve common problems encountered by business customers who have been onboarded onto the WhatsApp Business Platform by a [solution provider](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/overview).

## Contacting support

If you were onboarded to the WhatsApp Business Platform by a solution provider and you have [registered](https://developers.facebook.com/async/registration/) as a Meta developer, you can get help by opening a Direct Support ticket using the **Ask a Question** button at:

[https://business.facebook.com/direct-support/](https://business.facebook.com/direct-support/)

See our [Direct Support Information](https://www.facebook.com/business/help/182669425521252) Help Center article for more information about Direct Support.

## Billing and payments

### Billing and payment support

To get support specifically related to billing, payments, and payment methods, open a [Direct Support](https://business.facebook.com/direct-support/) ticket with the following form selections:

- **Topic** — **Dev: Billing, Credit & Pricing**
- **Request Type** — **Credit Card Billing**

If you do not see the **Dev: Billing, Credit & Pricing** topic, please contact your Tech Provider or Tech Partner and ask them to open a ticket for you.

### Add a payment method

If you have been onboarded to the WhatsApp Business Platform by a Tech Provider or Tech Partner, you must add a payment method to your WhatsApp Business Account before you can use their app to send and receive messages to WhatsApp users.

See our [Add a credit card to your WhatsApp Business Platform account](https://www.facebook.com/business/help/488291839463771) Help Center article to learn how to add a payment method to your account.

For more information about how pricing works on the WhatsApp Business Platform, see our [About billing for your WhatsApp Business account](https://www.facebook.com/business/help/2225184664363779?id=2129163877102343) Help Center article.

### Switch partners and remove previous line of credit

If your business customer worked with a partner in the past and still shares the previous credit line, they may see an error when attempting to switch to a new partner.

1. Backup your business customer’s messages.
2. Disconnect the business from WhatsApp Business app.
3. Reconnect your business in WhatsApp Business app.
4. Start onboarding process using the [WhatsApp Business app user onboarding](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users) flow.

### Transaction support

To get support for a specific transaction:

- access the Meta Business Suite **Billing & payments** panel at [https://business.facebook.com/billing_hub/](https://business.facebook.com/billing_hub/) .
- locate the transaction in either the **Accounts > WhatsApp Business accounts** tab, or the **Payment activity** panel.
- copy the entire transaction ID
- open a [Direct Support](https://business.facebook.com/direct-support/) ticket and include the transaction ID in the ticket

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/466908269_1627253861482438_5318686688053211395_n.png?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=ZSO9LKIU8awQ7kNvwHbMmPN&_nc_oc=Adp_Wvf5KS-SmgUYThieKkDzcHPZJHT_F4srlGMnyiAtb1NfPfCMBPScK8omRH9W33Q&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=yYXrlhrqvPvh1gSUktg48A&_nc_ss=7b20f&oh=00_Af6PVKQMT-DP78liWV9BmR33Kv2zOxxBctJ86XA1FXbRkQ&oe=6A1BFEF8)

### Payment errors

These are common payment errors you may encounter in the Meta Business Suite. If the proposed possible solutions do not work, please [contact support](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/support/business-customer-support#contacting-support).

| Error title and description | Possible solution |
| --- | --- |
| ***<CARD_TYPE> <CARD_NUMBER> hasn’t been verified.***<br>*We weren’t able to complete verification, please try again.* | Try again, making sure you are correctly entering the one-time-password sent to you by your bank.Make sure you are able to receive your bank’s one-time-password code.Contact your card’s issuing bank and ask if or why your card was blocked.Try again after a few days.Try another card. |
| **Couldn’t save payment method**<br>Couldn’t save payment method. You’ve already saved this payment method to the maximum number of ad accounts. Please use a different payment method. | Use an alternative credit card.<br>Note that we cannot increase the maximum number of accounts sharing a given credit card. There are no exceptions to this limitation. |
| **Request Not Completed**<br>We noticed something unusual and, for your security, this request couldn’t be completed. Please try again later, or visit our Help Center. | Ask your card’s issuing bank if any restrictions have been placed on the card.Try another card. |
| **Something went wrong**<br>We couldn’t complete your request. Please try again later. | Try again in a few days.Try another card. |

## Display names

Once a business phone number’s display name is reviewed, business customers can change their display name using WhatsApp Manager. Newly edited display names must undergo display name review again.

To edit a display name via WhatsApp Manager:

1. Access WhatsApp Manager at [https://business.facebook.com/wa/manage/home/](https://business.facebook.com/wa/manage/home/) .
2. Navigate to **Account tools** > **Phone numbers** .
3. Click the phone number.
4. Click the **Profile** tab.
5. Under **Display name** , use the **Edit** button to submit a new name.

This action, as well as the review outcome, triggers a [phone_number_name_update](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/phone_number_name_update) webhook.

## Unable to send template messages

If you are unable to send template messages, you likely have not added a valid payment method to your account. See our [Add a credit card to your WhatsApp Business Platform account](https://www.facebook.com/business/help/488291839463771) Help Center article to learn how to add a valid payment method.
