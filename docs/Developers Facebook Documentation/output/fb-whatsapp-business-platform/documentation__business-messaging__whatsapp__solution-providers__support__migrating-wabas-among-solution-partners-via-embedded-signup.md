# Migrating a WABA from one Solution Partner to another via Embedded Signup | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/support/migrating-wabas-among-solution-partners-via-embedded-signup_

---

# Migrating a WABA from one Solution Partner to another via Embedded Signup

Updated: Nov 4, 2025

If you are a Solution Partner, business customers can switch from their current Solution Partner over to you by unsharing their WABA with their current partner and resharing it with you. All business phone numbers and templates associated will continue to work normally once the process is complete.

Once the customer initiates the process, they will be unable to send messages again until you replace their current credit line with yours. This happens on the 1st of the following month in which you use the API to share your credit line. Note, however, that you cannot use the API to share your credit line (with a customer who has switched partners) the last 3 days or first 4 days of any month. Therefore, to ensure the shortest amount of downtime for customers, advise them to begin the process near the end of the month, but at least 3 days before it ends, so you can perform the API call in the same month.

## Limitations

- Customers must own their WABA. WABAs owned by Solution Partners (the [On-Behalf-Of model](https://developers.facebook.com/documentation/business-messaging/whatsapp/whatsapp-business-accounts#messaging-on-behalf-of) ) are not supported.
- Once the customer initiates the process, they will be prevented from sending messages until your credit line replaces their current credit line. This happens on the 1st of the month after which you successfully use the API to share your credit line with the customer.
- Your credit line currency must match the customer WABA’s currency at the time of migration.
- You cannot use the API to share your credit line (with a customer who has switched providers) the last 3 days or first 4 days of any month.
- Business phone numbers must be re-registered as part of the process.

## Step 1: Instruct the customer to unshare their WABA

Instruct the customer to use the Meta Business Suite to unshare their WhatsApp Business Account with their current partner. They can do this by navigating to:

**Business Settings** > **Accounts** (menu section) > **WhatsApp Accounts** > **Partners** (tab)

Once in the **Partners** tab, they can select their current partner, click the delete icon (trash can), and complete the flow to unshare their WABA.

You can provide the customer with the following link, which allows them to directly load their business portfolio in the Business Settings panel:

`https://business.facebook.com/settings`

Alternatively, you can direct the customer to the following Help Center article:

[Manage Your WhatsApp Business Solution Provider’s Permissions](https://www.facebook.com/business/help/861444384718867)

Keep in mind that once the customer completes this step, they will be prevented from sending messages until your credit line replaces their current credit line. This happens on the first of the month *after* you share your credit line with the customer.

If the customer attempts to send a message during this period, the API will return error code `131042` and a `messages` webhook will be sent to their current Solution Partner containing the same code.

## Step 2: Instruct the customer to complete Embedded Signup

If you do not take action, Meta will move your account to your business portfolio after 90 days. This process will not interrupt your messaging services.

Direct the customer to your implementation of Embedded Signup. Instruct them to complete the flow and to select their existing WABA when they see the **This WhatsApp Business account was previously shared** warning.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/435163409_465518599131244_3999655418914952752_n.png?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=kXhyIfjVV80Q7kNvwE6LXQE&_nc_oc=AdocgDrUPKUwgofE1EAmbXITpsfz7AavLMDFKZAmQRALFMBIghVskR9pzeuXwnlPZec&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=9viww6qbKKZWqe2WRxhaYA&_nc_ss=7b20f&oh=00_Af6yHfwI3ou_SN4pQYP32bTUQVNdamNfC_kKxvg2NN9fgw&oe=6A1C1B22)

Once they select their existing WABA and proceed, the flow will end, so they do not need to select a business phone number.

## Step 3: Get asset IDs from the session log message event listener

Capture the customer’s WABA ID and business phone number captured by the [session log message event listener](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/implementation#session-logging-message-event-listener) when they complete the flow.

Note that their business phone number will not be included in the session log via this flow.

## Step 4: Exchange the token code for a business token

[Exchange the token code](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-customers-as-a-solution-partner#step-1--exchange-the-token-code-for-a-business-token) captured by the [response callback](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/implementation#response-callback) for the customer’s [business token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens).

## Step 5: Add your system user to the customer’s WABA

If you are using a [system token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens) (which is not recommended) instead of a business token, add your system user to the customer’s WABA using the Business Manager in Meta Business Suite.

[**Business Settings**](https://business.facebook.com/settings) > **Accounts** (menu section) > **WhatsApp Accounts** > [Customer WABA] > **People** (tab) > **Assign People** (button)

## Step 6: Share your credit line with the customer

[Share your credit line](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/share-and-revoke-credit-lines#sharing-your-credit-line) with the customer. This change will not be reflected until the first of the following month. Until then, the customer will continue to share their previous Solution Partner’s credit line, but will be prevented from sending messages.

On the first of the following month, your credit line will replace the customer’s previous credit line, and the customer can resume messaging.

### Example

- **April 20:** A customer unshares their WABA with their previous Solution Partner. The customer is now prevented from messaging.
- **April 21:** The customer completes your implementation of Embedded Signup. You capture the customer’s credentials and access token, and share your credit line with them. The previous Solution Partner’s credit line is still shared with the customer, but the customer is still being prevented from messaging.
- **May 1:** Your credit line replaces the customer’s previous credit line. The customer can now send messages again. Any [billable messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing) sent by the customer will be billed to your credit line.
