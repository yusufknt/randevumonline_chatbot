# Partner-initiated WABA creation | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/partner-initiated-waba-creation_

---

# Partner-initiated WABA creation

Updated: Nov 14, 2025

If you are a Solution Partner and you don’t want to onboard a business customer with [Embedded Signup](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/overview), you can use Meta Business Suite to initiate WABA creation for a business customer. This generates a WABA creation request which your business customer can review in Meta Business Suite. The customer can then accept the request (or decline it) and optionally add a business phone number.

If accepted, the WABA will be created and its ownership will be assigned to the customer. You will also be given access to the WABA based on the permissions you defined when you initiated the request. You can then use your [system token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens) to add a business phone number to the customer’s WABA (if they opted not to create one) and share your credit line with the customer, which completes the onboarding process.

Note that if you use this method to create a WABA for a business customer, and the customer accepts it, you must use your system token when accessing the WABA (a [business token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens) will not work), and you must use the API to share your credit line with the customer (it cannot be shared as part of the initiation or acceptance process).

## Initiating WABA creation

1. Access [Meta Business Suite](https://business.facebook.com/) .
2. If you have multiple business portfolios, select the appropriate portfolio using the dropdown menu at the top-left of the page.
3. Navigate to the **Settings** (gear icon) > **Accounts** > **WhatsApp accounts** panel.
4. Click the blue **Add** dropdown button and select **Request a new WhatsApp Business account for a client** .
5. Complete the flow, filling out each field as appropriate.
6. Navigate to the **Settings** > **Requests** > **Other requests** panel and click the **Sent** tab and verify that your invitation has been sent to the business customer.
7. Instruct the customer to accept the request. See [Business customer instructions](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/partner-initiated-waba-creation#business-customer-instructions) below for content you can send them.

## Onboarding business customers

1. Listen for an **account_update** webhook with the `event` property set to `PARTNER_ADDED` or `PARTNER_APP_INSTALLED` , or look for a developer notification or developer alert, indicating that the customer has accepted your request.
2. If the customer accepted your request, navigate to the **Settings** (gear icon) > **Accounts** > **WhatsApp accounts** panel and confirm that you see the customer’s WABA in the list of WABAs.
3. If the WABA doesn’t have a business phone number, click the three-dot menu to the far right of the WABA’s name, select **Add phone number** , and complete the flow. Alternatively, you can [add a phone number programmatically](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/registering-phone-numbers) using the API.
4. [Share your credit line](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/share-and-revoke-credit-lines#alternate-method-for-sharing-your-credit-line) with the customer.

This completes the onboarding process. You can now use your system token to provide WhatsApp messaging services to the customer.

## Business customer instructions

Once you have confirmed that the invitation has been sent, instruct the business customer to review and accept the request in the Meta Business Suite. Invitations that have not been accepted within 90 days will be canceled automatically.

You can send them the following instructions:

1. *Access Meta Business Suite at [https://business.facebook.com](https://business.facebook.com).*
2. *If you have multiple business portfolios, select the appropriate portfolio using the dropdown menu at the top-left of the page.*
3. *Navigate to the **Settings** (gear icon) > **Requests** > **Other Requests** panel and click the **Received** tab.*
4. *Locate the invitation and review its contents (or decline the invitation).*
5. *Add and verify a business phone number (optional).*
6. *Confirm the invitation.*
7. *Navigate to the **Accounts** > **WhatsApp account** panel and confirm that your WhatsApp Business Account has been created and shared with your Solution Partner.*

## Adding phone numbers

Once the business customer has shared their WABA with you, you can register a business phone number for the customer in one of two ways:

- **Via WhatsApp Manager** : Navigate to the [**WhatsApp Manager**](https://business.facebook.com/latest/whatsapp_manager/) > **Overview** panel and locate the WABA in the WhatsApp account section. Click the three-dot menu to the far right of the WABA’s name, click **Add phone number** , and complete the flow.
- **Via API** : See [Registering business phone numbers](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/registering-phone-numbers) .

Alternatively, you can instruct the customer to add a number on their own using the WhatsApp Manager.

### Canceling invitations

To cancel an invitation that has not been accepted yet, navigate to the **Settings** (gear icon) > **Requests** panel and click the **Sent** tab. Locate the invitation and click its **Cancel** button.

### Payment methods

Business customers cannot add their own payment method to a WABA created via the partner-initiated WABA creation process. You must use the API to [share your credit line](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/share-and-revoke-credit-lines#alternate-method-for-sharing-your-credit-line) with any business customer who accepts your creation request.

### Multi-Partner Solutions

If you are part of a [Multi-Partner Solution](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/multi-partner-solutions) (“MPS”), you can share a WABA created through the partner-initiated WABA creation process with other MPS participants after you have successfully [onboarded the WABA](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/partner-initiated-waba-creation#onboarding-business-customers).

To share the WABA with other MPS participants, you have two options:

- **Recommended** : direct the customer to your (or your partner’s) MPS-configured implementation of Embedded Signup, and instruct them to complete the flow using their existing WABA name, business portfolio, and business phone number.
- Use the API to [add the WABA to your MPS](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/support/adding-waba-to-mps) .

## WABA Sharing model

With the WABA Sharing model, a business customer creates and grants access to their WABA to a solution provider using Embedded Signup.

When a customer successfully completes a solution provider’s Embedded Signup flow, a WABA is created under the customer’s business portfolio (and is thus owned by the customer) and a webhook is triggered, notifying the partner. The partner can then use the contents of the webhook and the customer’s [business token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens) to onboard the customer and provide message services via the API.

## Onboarding customers to the WABA Sharing model

To onboard a business customer to the WABA Sharing model, you must use Embedded Signup. See the [Embedded Signup](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/overview) documentation to learn how to implement Embedded Signup, and how to onboard business customers as a Solution Provider.

## On-Behalf-Of model

The On-Behalf-Of WABA ownership model has been deprecated and is no longer possible. See [On-Behalf-Of account ownership model deprecation](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/obo-model-deprecation) for details.
