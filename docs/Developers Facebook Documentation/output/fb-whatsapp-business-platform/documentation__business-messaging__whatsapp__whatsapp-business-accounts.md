# WhatsApp Business Accounts | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/whatsapp-business-accounts_

---

# WhatsApp Business Accounts

Updated: Oct 30, 2025

WhatsApp Business Accounts (“WABAs”) represent a business on the WhatsApp Business Platform. You must have a WABA to send and receive messages to and from WhatsApp users, and to create and manage templates.

There are several ways to create a WABA, which are described below. Once created, we recommend that you [connect your phone number](https://www.facebook.com/business/help/456220311516626) and [set up a payment method](https://www.facebook.com/business/help/2225184664363779).

## Limitations

- A WhatsApp Business Account (WABA) can have a maximum of 250 message templates.
- Meta Business Accounts are initially limited to 2 registered business phone numbers, but this limit can be increased to up to 20. See [Registered Number Limits](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers#registered-number-limits) .
- Meta Business Accounts are initially limited to 20 WABAs.
- A WABA must belong to only one Business Manager. You cannot have two or more Business Managers owning one WABA.
- A WABA’s time zone and currency cannot be edited once a line of credit has been attached to it. You cannot migrate a WABA from one business to another.

## Create a WABA via the App Dashboard

If you are going to be using Cloud API directly to send and receive messages, follow the steps in the [Cloud API Get Started](https://developers.facebook.com/documentation/business-messaging/whatsapp/get-started) documentation. Once you have completed these steps, you will have a test WABA and test business number, and have access to the **App Dashboard** > **WhatsApp** > **API Setup** panel.

The **API Setup** panel allows you to add a production business phone number, which generates a new WABA, which is then associated with that number.

## Create a WABA via a solution provider

If you are working with a solution provider (a business that offers WhatsApp messaging services to other businesses) who offers WhatsApp messaging services for you via the API, the solution provider will provide you with instructions. Typically this involves you completing the Embedded Signup flow, which gathers information about your business and generates a WABA for you, then using the provider’s app to access your newly created WABA and related assets.

See our [Create your WhatsApp Business Account with WhatsApp Business solution providers](https://www.facebook.com/business/help/524220081677109) Help Center article for more information.

## Create a WABA via Meta Business Suite

This feature is being released gradually over the next few weeks and may not be available to you immediately. Business portfolios with a Brazil or India address are currently unable to use this feature.

You can create a WABA using [Meta Business Suite](https://business.facebook.com). Use this method if you are working with a solution provider who provides WhatsApp messaging-related services via Meta Business Suite instead of Cloud API.

To create a WABA using Meta Business Suite:

1. Go to [https://business.facebook.com/](https://business.facebook.com/) and create a business portfolio, or sign into your existing account and select your existing portfolio if you already have one.
2. Navigate to the **Settings** (gear icon) > **Accounts** > **WhatsApp accounts** panel.
3. Click the blue **+Add** button and in the dropdown menu select **Create a new WhatsApp Business account** .
4. In the **Create a WhatsApp Business account** window that appears (pictured below), complete the flow.

## Share your WABA with a solution provider

You can share your WABA (or any of your business assets) with any business-verified solution provider (aka “partner”) using Meta Business Suite. Once shared, the partner can then use the Meta Business Suite to access your WABA and provide services.

### Notes

- If you are sharing your WABA with a Solution Provider (a type of partner who has a credit line), they must share their credit line with you before you will be able to use their app to send messages.
- You can share a WABA with up to two partners.

### If you have not shared an asset with the partner before

1. Ask the partner for their business portfolio ID. You will need this ID to complete the remaining steps.
2. Sign into [Meta Business Suite](https://business.facebook.com) . Use the top-left dropdown menu to select the business portfolio if you have multiple portfolios.
3. Navigate to the **Settings** (gear icon) > **Accounts** > **WhatsApp** accounts panel.
4. In the list of WABAs, select your WABA, or click its **Details** link.
5. In the details overlay that appears to the right (pictured below), click the **Assign partner** button.
6. In the **Share this WhatsApp Account with a partner** overlay that appears, enter the partner’s business portfolio ID and use the toggles to define which permissions to grant to the partner, then click the **Assign** button.
7. If your WABA is shared with the partner successfully, a **Partner added** message will appear. Click the **Done** button to dismiss it.
8. Back in the details overlay, click the **Partners** tab.
9. In the **Partners** tab, confirm that the partner’s name appears as a partner with appropriate permissions.
10. Inform the partner that you have successfully shared your WABA with them (and ask them to share their credit line if appropriate; see note above).

### If you have already shared an asset with the partner

1. Sign into [Meta Business Suite](https://business.facebook.com) . Use the top-left dropdown menu to select the business portfolio if you have multiple portfolios.
2. Navigate to the **Settings** (gear icon) > **Users** > **Partners** panel.
3. In the list of partners, click the name of the partner, or its **Details** link.
4. In the details overlay that appears to the right (pictured below), click the **Assign assets** button.
5. In the **Assign assets and permissions** window that appears, click the **WhatsApp accounts** asset type.
6. Check the checkbox next to your WABA, then use the toggles to define which permissions to grant to the partner and click the **Assign** button.
7. If successful, an **Assets assigned** message will appear. Click the **Done** button to dismiss the window.
8. Confirm that your WABA appears in the **Assets you assigned** tab with appropriate permissions.
9. Inform the partner that you have successfully shared your WABA with them (and to share their credit line if appropriate; see note above).

## Get WABA data via API

Use the [WhatsApp Business Account API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/whatsapp-business-account-api#get-version-waba-id) to get data on a WABA. Use the `fields` parameter to request specific fields on a WABA, or omit it to get default fields returned by the endpoint.

### Example request

```curl
curl 'https://graph.facebook.com/v25.0/102290129340398?fields=name,status,currency,country,business_verification_status' \
-H 'Authorization: Bearer EAAJB...'
```

### Example response

```json
{
  "name": "Lucky Shrub",
  "status": "ACTIVE",
  "currency": "USD",
  "country": "US",
  "business_verification_status": "verified",
  "id": "102290129340398"
}
```

## Access your WABA with WhatsApp Manager

You can access your WABA in WhatsApp Manager to see basic information like business phone number status, messaging metrics, and to perform basic tasks like template creation and editing.

To access your WABA in WhatsApp Manager:

1. Sign into [Meta Business Suite](https://business.facebook.com) . Use the top-left dropdown menu to select the business portfolio if you have multiple portfolios.
2. Navigate to the **Settings** (gear icon) > **Accounts** > **WhatsApp accounts** panel.
3. In the list of WABAs, select your WABA, or click its **Details** link.
4. In the **Summary** tab, click the **WhatsApp Manager** button.

## Webhooks

Subscribe to the [account_update](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/account_update) webhook to be notified of changes to a WhatsApp Business Account’s status, including changes due to policy and terms violations.

Every time your WABA has violated a policy, you will get a notification looking like this:

```json
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "whatsapp-business-account-id",
      "time": 1604703058,
      "changes": [
        {
          "field": "account_update",
          "value": {
            "phone_number": "16505551111",
            "event": "ACCOUNT_VIOLATION",
            "violation_info": {
              "violation_type": "ALCOHOL"
            }
          }
        }
      ]
    }
  ]
}
```

See our [WhatsApp Business Platform Policy Violations](https://developers.facebook.com/documentation/business-messaging/whatsapp/policy-enforcement-violations) document for a list of policy violations. If a restriction has been imposed, an **account_update** webhook will be triggered, describing the violation.

## Messaging On-Behalf-Of

The On-Behalf-Of WABA ownership model is deprecated and is no longer possible. See [OBO model deprecation](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/obo-model-deprecation) for details.
