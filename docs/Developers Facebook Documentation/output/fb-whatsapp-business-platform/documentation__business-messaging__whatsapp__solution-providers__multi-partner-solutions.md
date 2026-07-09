# Multi-Partner Solutions | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/multi-partner-solutions_

---

# Multi-Partner Solutions

Updated: Feb 27, 2026

This document explains how to set up Multi-Partner Solutions (“solutions”) and how to use them with [Embedded Signup](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/overview).

Multi-Partner Solutions allow Solution Partners and Tech Providers to jointly manage customer WhatsApp assets in order to provide WhatsApp messaging services to their customers. For example, if you are a Tech Provider and are unable to offer custom or full WhatsApp messaging services to your customers, you can work with a Solution Partner to offer your customers the Solution Partner’s services.

Once created and accepted via API or App Dashboard, the solution’s ID can be used to customize the Embedded Signup flow. Any customers onboarded via the customized flow can grant asset access to all of the solution’s partners.

Note that solutions can also be set up via an embedded button that triggers an interface that gathers app information from Tech Providers. This flow and the API calls involved are described in the [Multi-Partner Solution — Embedded Creation](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/multi-partner-solution-embedded-creation) document, but the information below is still relevant and should be read first.

## Requirements

You must be an approved [Solution Partner](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/overview#solution-partners), a Tech Provider who has completed the steps in our [Get Started for Tech Providers](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/get-started-for-tech-providers) document appropriate for your intended usage, or a Tech Provider who has been upgraded to a [Tech Partner](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/overview#tech-partners).

If your app will be calling our APIs to access onboarded customer data:

- The app must be the same app whose token will be used in API requests.
- The app must have undergone App Review and been approved for the [whatsapp_business_management](https://developers.facebook.com/docs/permissions#w) and [whatsapp_business_messaging](https://developers.facebook.com/docs/permissions#w) permissions.
- The app must be subscribed to the **account_updates** webhooks field and be able to successfully digest webhooks for onboarded customers.

## Creating Multi-Partner Solutions

Use the **App Dashboard** > **WhatsApp** > **Partner Solutions** panel to create, accept, and manage solutions.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/387755976_1054085509106646_2627484372064430460_n.png?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=uZMupkQxzZQQ7kNvwE3NTDT&_nc_oc=AdqdGdH83tIJ-FmQ0e5WjnOZSdfSEd_XhGoOFH8XATK-l4x30obp3GxaM9FjSDOFqFw&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=fUTjzEk5rUfSVdRtW-dDuw&_nc_ss=7b20f&oh=00_Af5pBbwALcnEEKVR9KMEyH7VrbV0ojncEB0MR5GwkGE0kQ&oe=6A1C31E0)

Solutions can be created by either partner of the solution. Once created, a solution request is sent to the invited partner, who can then use the panel in their App Dashboard to accept or decline the request. Once accepted, either partner can use the solution ID to customize the Embedded Signup flow and onboard business customers.

### Solution States

Solutions states are displayed in the **Partner solutions** panel. Solutions can have the following states:

| State | Description |
| --- | --- |
| **Active** | The solution has been accepted by the invited party and can be used to configure Embedded Signup for customer onboarding. |
| **Deactivated** | The solution has been deactivated.<br>Customers who attempt to access Embedded Signup configured for a solution in this state will see an error informing them that it cannot be used for onboarding at this time. |
| **Draft** | The solution has been initiated and saved, but you have not sent it to your partner.<br>Customers who attempt to access Embedded Signup configured for a solution in this state will see an error informing them that it cannot be used for onboarding at this time. |
| **Inactive** | The solution request was declined by your partner.<br>Customers who attempt to access Embedded Signup configured for a solution in this state will see an error informing them that it cannot be used for onboarding at this time. |
| **Pending** | Solution has not been accepted or declined by your partner.<br>Customers who attempt to access Embedded Signup configured for a solution in this state will see an error informing them that it cannot be used for onboarding at this time. |
| **Pending deactivation** | Your partner has requested to deactivate the solution. You can accept or decline this request. |

### Onboarding Limits

Tech Providers who are part of a solution can onboard up to 200 total new customers in a rolling one week period. Only customers who are new to the WhatsApp Business Platform count against this limit.

## Embedded Signup

[Embedded Signup](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/overview) can be configured and hosted by either of the solution’s partners, or both partners. Once implemented, customers who access it will see a customized version of the Embedded Signup flow, which makes it clear that by completing the flow they are granting WhatsApp data access to both partners:

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/387758256_729453148995242_4492854088232630406_n.png?_nc_cat=101&ccb=1-7&_nc_sid=e280be&_nc_ohc=bgVgQBvPdUkQ7kNvwE4QVrp&_nc_oc=Ado1RGbYmQGhZP-wo926jPaD4DK9V5qwlXsk45CVC3XQOk2l-ehia6kaf3pfUyibWHg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=fUTjzEk5rUfSVdRtW-dDuw&_nc_ss=7b20f&oh=00_Af6jN5v7E8TNTxDxCm8JE07aOykpGSqQyynNewORGON-_g&oe=6A1C0DF5)

When a customer completes the flow, all of the customer’s WhatsApp assets that we need are automatically generated, and access to those assets is granted to both partners of the solution.

## Billing

Customers onboarded via Embedded Signup configured with a solution ID share the credit line of the Solution Partner associated with the solution.

## Step 1: Determine Solution Details

Contact your potential partner and work together to determine:

- A solution name. The solution name will appear in the **Partner Solutions** panel in the App Dashboard for both you and your partner, so you should both agree on a name that can be distinguished from other solutions you may initiate or accept.
- Who will create and initiate the solution request. Either partner can do this. If you are initiating the request, you will need your partner’s app ID.
- Who will host Embedded Signup configured with the solution ID. Either or both partners can do this.
- Anything else, such as contracts, service level agreements, services provided, billing processes, etc. This is left to the discretion of you and your partner, subject to each of your separate agreements with Meta.

## Step 2: Subscribe to Webhooks

Subscribe to the **account_update** and **partner_solutions** webhooks fields. These webhooks will inform you when new business customers are onboarded, and when partner solutions that you are associated with are created or edited.

See the [Webhooks](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/multi-partner-solutions#webhooks) section below for example payloads and what to look for when you receive any of these webhooks.

## Step 3: Create a Solution

If you are creating the solution, navigate to the **App Dashboard** > **WhatsApp** > **Partner solutions** panel and click the **Create a partner solution** button.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/387766072_815168047024704_8866666397602417825_n.png?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=8uGY-dFpS9EQ7kNvwH9p2My&_nc_oc=AdoatgAd64sIpuFWqKxFLX0zINPMp-n_cRYAlANvEYNbmTM26ldrsRD-daMKosp5m5c&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=fUTjzEk5rUfSVdRtW-dDuw&_nc_ss=7b20f&oh=00_Af4b_Gj9Q2Bcnh8YH6pEYNAonZLclweoWObIFVx-uPfoKA&oe=6A1C1751)

Use your partner’s app ID to complete the flow. As part of the creation flow you can designate which solution partner apps can be used by onboarded business customers to send messages (**Only me**, **Only my partner**).

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/466044298_1209676256996747_5273108359679787011_n.png?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=-H3WjH8GeikQ7kNvwFswh1t&_nc_oc=AdorwfLpfaj2XwntAFQohHQ3RymvYjdcqYsCwVNvovLAbtOyY7n9aszEQQjsI1MAIiI&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=fUTjzEk5rUfSVdRtW-dDuw&_nc_ss=7b20f&oh=00_Af6oCnP6cqB7_I0LsUiCM0t8qSUsPbO5Q0xHo1aH18mtEw&oe=6A1C0E9A)

Upon creation, an email and Meta Business Suite notification will be sent to your partner, and a **partner_solutions** webhook will be triggered.

The partner solution will appear in the **Partner solutions** panel with a **Pending** status until accepted by your partner. If accepted, its status will change to **Active**. If declined, its status will change to **Inactive**.

## Step 4: Accept The Solution Request

Everyone with admin (**Full control**) privileges on your business portfolio will be notified by email and Meta Business Suite notification when your partner sends you a partner solution request.

In addition, a [**partner_solutions**](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/multi-partner-solutions#partner-solutions-webhook) webhook will be triggered with `event` set to `SOLUTION_CREATED` and `solution_status` set to `INITIATED`. Capture the included solution ID (`solution_id`) if you will be accepting/rejecting and managing the solution via API.

You can use either the App Dashboard or the API to accept the partner solution request.

### Via App Dashboard

The request will appear in the **App Dashboard** > **WhatsApp** > **Partner solutions** panel with a **Pending** status.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/465912134_539074672234606_4001016335689190990_n.png?_nc_cat=111&ccb=1-7&_nc_sid=e280be&_nc_ohc=ubg5ZRJUBjQQ7kNvwHZlxhq&_nc_oc=AdpCfQDDkDhciw75itL1qB2iMvIfyc3Q_ZUiANI72h2k7xjMwNgNsDVOmlS1fEaoZb8&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=fUTjzEk5rUfSVdRtW-dDuw&_nc_ss=7b20f&oh=00_Af5R7KNx_tTH987dqCQQ91LYrz5S0XOx8lMgwk5LcO_RNQ&oe=6A1C1C31)

If you have multiple solutions and are having a hard time locating the solution request, use the dropdown menu in the top-right corner of the panel and filter by **Pending**.

Confirm that everything is correct before accepting the request, as solutions cannot be declined once they have been accepted.

Once you accept the solution, its status will be set to **Active** and you and your partner can use its ID to [configure Embedded Signup](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/multi-partner-solutions#step-5-configure-embedded-signup).

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/465996567_886269830277358_6720016141752033956_n.png?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=Lk_OXhrdqJEQ7kNvwGzlbWp&_nc_oc=AdoSlOyadM68s2vD-NM9Njq01xLDOR8ep_P9AE6a81Zt9hDebUL8Ry9nrvA4XWsz7tw&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=fUTjzEk5rUfSVdRtW-dDuw&_nc_ss=7b20f&oh=00_Af78VpO5FQ39RHHZBcbkNX24WSlAcEi65DY8zKOwrTuJ4w&oe=6A1BFEB9)

If any information is incorrect, decline the request and ask your partner to submit a new request with the correct settings. Your partner will automatically be notified by email and Meta Business Suite notification if you decline the request.

### Via API

Before accepting the solution, use the [Solution API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-solution/solution-details-api#get-version-solution-id) to get details about the solution and confirm that everything is correct, as solutions cannot be declined once they have been accepted.

Include the following fields in your query:

- `name`
- `owner_permissions`
- `partners{partner_permissions,partner_app}`

Example request

```curl
curl -g 'https://graph.facebook.com/v25.0/795033096057724&fields=name,owner_permissions,partners{partner_permissions,partner_app}' \
-H 'Authorization: Bearer EAAAT...'
```

Example response

```json
{
  "name": "Social OVD with Lucky Shrub",
  "owner_permissions": [
    "MANAGE",
    "DEVELOP",
    "MANAGE_TEMPLATES",
    "MANAGE_PHONE",
    "VIEW_COST",
    "MANAGE_EXTENSIONS",
    "VIEW_PHONE_ASSETS",
    "MANAGE_PHONE_ASSETS",
    "VIEW_TEMPLATES",
    "VIEW_INSIGHTS"
  ],
  "partners": {
    "data": [
      {
        "partner_permissions": [
          "MANAGE",
          "DEVELOP",
          "MANAGE_TEMPLATES",
          "MANAGE_PHONE",
          "VIEW_COST",
          "MANAGE_EXTENSIONS",
          "VIEW_PHONE_ASSETS",
          "MANAGE_PHONE_ASSETS",
          "VIEW_TEMPLATES",
          "VIEW_INSIGHTS"
        ],
        "partner_app": {
          "link": "https://www.facebook.com/games/?app_id=21202248997039",
          "name": "Lucky Shrub",
          "id": "21202248997039"
        },
        "id": "795033099391057"
      }
    ],
    "paging": {
      "cursors": {
        "before": "QVFIUl9hX0RqLUZAPemJQVWdsYTl5WlBsY0lCb0FNTExOY2N2NzJtRENZAbDd3azBNXzhPZAndqaU5sSXdfWWJaSXJ1S2pqMi0tQUdUdm1LTGZATUDNIdGRNNE1B",
        "after": "QVFIUl9hX0RqLUZAPemJQVWdsYTl5WlBsY0lCb0FNTExOY2N2NzJtRENZAbDd3azBNXzhPZAndqaU5sSXdfWWJaSXJ1S2pqMi0tQUdUdm1LTGZATUDNIdGRNNE1B"
      }
    }
  },
  "id": "795033096057724"
}
```

- `name` — the name of the solution, as it appears in the App Dashboard.
- `owner_permissions` — the permissions your partner’s app will be granted by business customers who onboard via Embedded Signup.
- `partner_permissions` — the permissions your app will be granted by business customers who onboard via Embedded Signup.
- `partner_app` — the app (your app) that will be granted the permissions identified in `partner_permissions` .

If everything is correct, use the [Solution Accept API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-solution/solution-accept-api#post-version-solution-id-accept) to accept the solution request, otherwise use the [Solution Reject API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-solution/solution-reject-api#post-version-solution-id-reject) to reject it.

Example accept request

```curl
curl -X POST 'https://graph.facebook.com/v25.0/795033096057724/accept' \
-H 'Authorization: Bearer EAAAT...'
```

Example reject request

```curl
curl -X POST 'https://graph.facebook.com/v25.0/795033096057724/reject' \
-H 'Authorization: Bearer EAAAT...'
```

Example response

Upon success:

```json
{
  "success": true
}
```

## Step 5: Configure Embedded Signup

Assign the solution ID to the `solutionID` property in the `extras.setup` object within the [launch method and callback registration](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/implementation#launch-method-and-callback-registration) portion of the Embedded Signup code.

```html
// Launch method and callback registration
const launchWhatsAppSignup = () => {
  FB.login(fbLoginCallback, {
    config_id: '<CONFIGURATION_ID>', // your configuration ID goes here, ensure it is in quotes
    response_type: 'code',
    override_default_response_type: true,
    extras: {
      setup: {
        solutionID: '<SOLUTION_ID>' // add solution ID here, ensure it is in quotes
      },
      featureType: '',
      sessionInfoVersion: '3',
    }
  });
}
```

Both you and your partner’s business portfolio (**Business Settings** > **Business Info**) will appear throughout the Embedded Signup flow.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/387758256_729453148995242_4492854088232630406_n.png?_nc_cat=101&ccb=1-7&_nc_sid=e280be&_nc_ohc=bgVgQBvPdUkQ7kNvwE4QVrp&_nc_oc=Ado1RGbYmQGhZP-wo926jPaD4DK9V5qwlXsk45CVC3XQOk2l-ehia6kaf3pfUyibWHg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=fUTjzEk5rUfSVdRtW-dDuw&_nc_ss=7b20f&oh=00_Af6jN5v7E8TNTxDxCm8JE07aOykpGSqQyynNewORGON-_g&oe=6A1C0DF5)

Once configured, surface the customized Embedded SIgnup flow to customers on your platform wherever you feel it is appropriate. Note that if you have multiple active partner solutions, it is your responsibility to inject the correct solution ID into your Embedded Signup configuration and surface it to your intended customers, otherwise a customer could be onboarded using the wrong solution.

## Step 6: Listen for Onboarded Business Customers

To listen for onboarded customers, your app must be subscribed to the [**account_update**](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/multi-partner-solutions#account-update-webhook) webhook field.

When a customer completes the Embedded Signup flow configured with your solution, an account update webhook is triggered with a `PARTNER_ADDED` or `PARTNER_APP_INSTALLED` event. Capture the `waba_id`, `solution_id`, and `owner_business_id` property values contained in the webhook payload, as well as any other values you may need in order to provide the customer with WhatsApp messaging services.

In addition, we will send an email to admins of the business portfolio that owns the app, and a Meta Business Suite notification to the business portfolio that owns the app.

## Step 7: Share Your Credit Line (Solution Partners only)

If you are a Solution Partner, [share your line of credit](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/share-and-revoke-credit-lines#sharing-your-credit-line) with any business customers newly onboarded via the partner solution.

**Note**: If you are a Solution Partner trying to add a user to a WhatsApp Business Account that is shared with you, you would need to account for the following scenarios:

- If you are not granted the `MESSAGING` permission on the solution, then you need to decide which granular tasks you need when adding the user to the shared WhatsApp Business Account: `DEVELOP` , `MANAGE_TEMPLATES` , `MANAGE_PHONE` , `VIEW_COST` , `MANAGE_EXTENSIONS` , `VIEW_PHONE_ASSETS` , `MANAGE_PHONE_ASSETS` , `VIEW_TEMPLATES` , `VIEW_INSIGHTS` , `MANAGE_USERS` , and `MANAGE_BILLING` .
- In this scenario, also note that `MANAGE_BILLING` is needed for credit line sharing.
- `MANAGE` will only work if you are given **Full access** on the solution, i.e. including `MESSAGING` .

## Webhooks

### account_update

When a new business customer has successfully completed the Embedded Signup flow, an **account_update** webhook will be triggered with the `event` property set to `PARTNER_ADDED`.

```json
{
  "entry": [
    {
      "id": "<BUSINESS_PORTFOLIO_ID>",
      "time": <TIMESTAMP>,
      "changes": [
        {
          "value": {
            "event": "<EVENT>",
            "waba_info": {
              "waba_id": "<BUSINESS_CUSTOMER_WABA_ID>",
              "owner_business_id": "<BUSINESS_CUSTOMER_BUSINESS_PORTFOLIO_ID>",
              "solution_id": "<SOLUTION_ID>",
              "solution_partner_business_ids": [<SOLUTION_BUSINESS_PORTFOLIO_IDS>]
            }
          },
          "field": "account_update"
        }
      ]
    }
  ],
  "object": "whatsapp_business_account"
}
```

Payload Properties

| Placeholder | Description | Example |
| --- | --- | --- |
| `<BUSINESS_PORTFOLIO_ID>` | Your business portfolio ID. | `506914307656634` |
| `<BUSINESS_CUSTOMER_BUSINESS_PORTFOLIO_ID>` | Onboarded customer’s business portfolio ID. | `6143763655652543` |
| `<BUSINESS_CUSTOMER_WABA_ID>` | Onboarded customer’s WhatsApp Business Account ID. | `102290129340398` |
| `<EVENT>` | If set to `PARTNER_ADDED`, indicates that the business customer has successfully completed the Embedded Signup flow. | `PARTNER_ADDED` |
| `<SOLUTION_BUSINESS_PORTFOLIO_IDS>` | Strings of business portfolio IDs of the Tech Provider (or Tech Partner) and Solution Partner associated with the solution. | `"506914307656634","116133292427920"` |
| `<SOLUTION_ID>` | Solution ID. | `303610109049230` |
| `<TIMESTAMP>` | UNIX timestamp indicating when the customer successfully completed the Embedded Signup flow. | `1690592557` |

### partner_solutions

When a Multi-Partner Solution is created or modified, a **partner_solutions** webhook describing the change will be triggered.

```json
{
  "entry": [
    {
      "id": "<BUSINESS_PORTFOLIO_ID>",
      "time": <TIMESTAMP>,
      "changes": [
        {
          "value": {
            "event": "SOLUTION_CREATED",
            "solution_id": "<SOLUTION_ID>",
            "solution_status": "INITIATED"
          },
          "field": "partner_solutions"
        }
      ]
    }
  ],
  "object": "whatsapp_business_account"
}
```

Payload Properties

| Placeholder | Description | Example |
| --- | --- | --- |
| `<BUSINESS_PORTFOLIO_ID>` | Your business portfolio ID. | `506914307656634` |
| `<EVENT>` | Event description. Values can be:<br>`SOLUTION_CREATED` — Solution created.`SOLUTION_UPDATED` — The `solution_status` has changed. | `SOLUTION_CREATED` |
| `<SOLUTION_ID>` | Solution ID. | `774485461512159` |
| `<SOLUTION_STATUS>` | Solution status. Values can be:<br>`ACTIVE` — The solution partner has accepted the solution request and it can be used with Embedded Signup.`DEACTIVATED` — The solution has been deactivated and cannot be used with Embedded Signup to onboard business customers.`DRAFT` — Solution has been drafted but invitation has not been sent to the solution partner.`INITIATED` — The solution partner has been invited to accept the solution, but has yet to accept or reject the request.`PENDING` — The solution partner has yet to accept or reject the solution request.`PENDING_DEACTIVATION` — The solution owner requested for an active solution to be deactivated but the solution partner has yet to accept the deactivation request.`REJECTED` — The solution partner has rejected the solution request. | `INITIATED` |
| `<TIMESTAMP>` | UNIX timestamp indicating when the customer successfully completed the Embedded Signup flow. | `1718143652` |

## Editing or Deactivating Solutions

You can use the App Dashboard or API to edit or deactivate a solution.

When you request deactivation, the solution’s status will change to **Pending deactivation** and your partner will be notified by email and Meta Business Suite notification. In addition, a [**partner_solutions**](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/multi-partner-solutions#partner-solutions-webhook) webhook will be triggered with `event` set to `SOLUTION_UPDATED` and `solution_status` set to `PENDING_DEACTIVATION`. Your partner can then accept or reject your request.

Note that partner solutions can still be used to onboard customers until your partner accepts the deactivation request.

If the deactivation request is rejected, the solution will remain in an **Active** state and can continue to be used to onboard customers.

If the deactivation request is accepted, the solution status will be set to **Deactivated** and can no longer be used to onboard business customers, so make sure that neither you nor your partner are surfacing it to business customers.

### Limitations

- You can only edit solutions that were created by you.
- You can request deactivation of any solutions that you create which are in an **Active** state.

### Via App Dashboard

Use the **App Dashboard** > **WhatsApp** > **Partner solutions** panel to edit or deactivate a solution. Note that you can only edit solutions that were initiated by you.

| State | Permitted actions |
| --- | --- |
| **Active** | You may edit the solution name, or deactivate the solution. |
| **Deactivated** | Solutions in this state cannot be edited. |
| **Draft** | You may edit the solution name. |
| **Inactive** | You may edit the solution name. |
| **Pending** | Solutions in this state cannot be edited until accepted or declined by your partner. |
| **Pending deactivation** | You may accept or decline the partner’s deactivation request. |

### Via API

### Send deactivation request

Use the [Send Deactivation Request API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-solution/send-deactivation-request-api#post-version-solution-id-send-deactivation-request) to send a solution deactivation request. You must be the solution owner in order to send this request.

Example request

```curl
curl -X POST 'https://graph.facebook.com/v20.0/795033096057724/send_deactivation_request \
-H 'Authorization: Bearer EAAAT...'
```

Example response

Upon success:

```json
{
    "success": true
}
```

### Accept deactivation request

Use the [Accept Deactivation Request API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-solution/accept-deactivation-request-api#post-version-solution-id-accept-deactivation-request) to accept a solution deactivation request. You must be the solution owner in order to send this request.

Example request

```curl
curl -X POST 'https://graph.facebook.com/v20.0/795033096057724/accept_deactivation_request \
-H 'Authorization: Bearer EAAAT...'
```

Example response

Upon success:

```json
{
    "success": true
}
```

### Reject deactivation request

Use the [Reject Deactivation Request API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-solution/reject-deactivation-request-api#post-version-solution-id-reject-deactivation-request) to reject a solution deactivation request. You must be the solution owner in order to send this request.

Example request

```curl
curl -X POST 'https://graph.facebook.com/v20.0/795033096057724/reject_deactivation_request \
-H 'Authorization: Bearer EAAAT...'
```

Example response

Upon success:

```json
{
    "success": true
}
```

## Manually Checking for Onboarded Customers

As a fallback in case of webhook problems, you can manually check for onboarded customers using the [Client WhatsApp Business Accounts API](https://developers.facebook.com/documentation/ads-commerce/marketing-api/reference/business/client_whatsapp_business_accounts#get-version-business-id-client-whatsapp-business-accounts), which returns WABA IDs of all customers newly onboarded via the solution.

### Request Syntax

```https
GET /<BUSINESS_PORTFOLIO_ID>/client_whatsapp_business_accounts
  ?filtering=[
    {
      "field":"partners",
      "operator":"ALL",
      "value":[
        "<PARTNER_BUSINESS_PORTFOLIO_ID>"
      ]
    }
  ]
```

Replace `<PARTNER_BUSINESS_PORTFOLIO_ID>` with your partner’s business portfolio ID.

### Response

```json
{
  "data": [
    {
      "id": "<CUSTOMER_WABA_ID>",
      "name": "<CUSTOMER_WABA_NAME>",
      "timezone_id": "<CUSTOMER_WABA_TIMEZONE_ID>",
      "business_type": "ent",
      "message_template_namespace": "<MESSAGE_TEMPLATE_NAMESPACE>"
    }
    ...
  ],
  "paging": {
    "cursors": {
      "before": "<BEFORE>",
      "after": "<AFTER>"
    },
    "next": "<NEXT>"
  }
}
```

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<CUSTOMER_WABA_ID>` | Customer WhatsApp Business Account ID. | `102290129340398` |
| `<CUSTOMER_WABA_NAME>` | Customer WhatsApp Business Account name. | `Cool New Customer 2` |
| `<CUSTOMER_WABA_TIMEZONE_ID>` | Customer WhatsApp Business Account timezone ID. | `7` |
| `<BEFORE>` | Paginated results cursor. See [Paginated Results](https://developers.facebook.com/docs/graph-api/results). | `QVFIU...` |
| `<AFTER>` | Paginated results cursor. See [Paginated Results](https://developers.facebook.com/docs/graph-api/results). | `QVFIU...` |
| `<NEXT>` | Paginated results link. See [Paginated Results](https://developers.facebook.com/docs/graph-api/results). | `https://graph.facebook.com/v18.0/50691...` |

### Example Request

```curl
curl -g 'https://graph.facebook.com/v25.0/506914307656634/client_whatsapp_business_accounts?filtering=[{%22field%22%3A%22partners%22%2C%20%22operator%22%3A%20%22ALL%22%2C%20%22value%22%3A%20[%22520744086200222%22]}]' \
-H 'Authorization: Bearer EAAJB...'
```

### Example Response

```json
{
  "data": [
    {
      "id": "102290129340398",
      "name": "Cool New Customer 2",
      "timezone_id": "7",
      "business_type": "ent",
      "message_template_namespace": "<MESSAGE_TEMPLATE_NAMESPACE>"
    },
    {
      "id": "112077945305052",
      "name": "Cool New Customer 1",
      "timezone_id": "7",
      "business_type": "ent",
      "message_template_namespace": "<MESSAGE_TEMPLATE_NAMESPACE>"
    }
    ...
  ],
  "paging": {
    "cursors": {
      "before": "QVFIU...",
      "after": "QVFIU..."
    },
    "next": "https://graph.facebook.com/v25.0/50691..."
  }
}
```

## Getting Solution Data

### Get fields on a solution

Use the [Solution API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-solution/solution-details-api#get-version-solution-id) to get default fields on a solution, or use the `fields` query string parameter to request specific fields.

Example Request

```curl
curl 'https://graph.facebook.com/v25.0/17602267745700?fields=name,status,partners' \
-H 'Authorization: Bearer EAAAT...'
```

Example Response

```json
{
  "name": "Social OVD with Lucky Shrub",
  "status": "ACTIVE",
  "partners": {
    "data": [
      {
        "partner_app": {
          "link": "https://www.socialoverdrive.com/",
          "name": "Social Overdrive",
          "id": "637576208107267"
        },
        "status": "ACCEPTED",
        "id": "17602267745704"
      }
    ],
    "paging": {
      "cursors": {
        "before": "QVFIUmxnSE9LUFliNzlUTWdhTlYzQjBtekprSC0wQUdoZAGRYbFlzeUpDMG9yNkF1OHYyel9tcUlBbGhFckxJQ1Y3UFZA4dUkycEk0WDJwRGYzT2JYbVhEdFdB",
        "after": "QVFIUmxnSE9LUFliNzlUTWdhTlYzQjBtekprSC0wQUdoZAGRYbFlzeUpDMG9yNkF1OHYyel9tcUlBbGhFckxJQ1Y3UFZA4dUkycEk0WDJwRGYzT2JYbVhEdFdB"
      }
    }
  },
  "id": "17602267745700"
}
```

### Get solutions associated with your app

Use the [WhatsApp Business Solutions API](https://developers.facebook.com/docs/graph-api/reference/application/whatsapp_business_solutions) to get a list of solutions your app is associated with.

Example Request

```curl
curl 'https://graph.facebook.com/v25.0/21202248997039/whatsapp_business_solutions' \
-H 'Authorization: Bearer EAAAT...'
```

Example Response

```json
{
  "data": [
    {
      "name": "Social OVD with Lucky Shrub",
      "status": "INITIATED",
      "status_for_pending_request": "PENDING_ACTIVATION",
      "id": "19702253086782"
    },
    {
      "name": "Social OVD with Social Brew",
      "status": "ACTIVE",
      "status_for_pending_request": "NONE",
      "id": "17602267745700"
    }
  ],
  "paging": {
    "cursors": {
      "before": "QVFIUkxlbkhTZA1VleGwyWHd3SmlSMnlnelhlbUVSSjVYQmU2aXVmb1YyWk9JTkx3b2gwNE9FS3J2ejMzNENxbmh1bWZAqSkZAJUzNfbmF4NmtPaFYxQldaaXR3",
      "after": "QVFIUlgyLTlQYWV0eTNGWXVhcTJnOEhzY1lvUDloVV8wUUxVQk9YMVJ5UGlBZAmx1Q1BjaEVwd0tWdmNvRU9jdGRiNnlrc193alRNaDV2SXZAfN1kybDBibEFR"
    }
  }
}
```

### Get solutions that onboarded a WABA

Use the [Solutions API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/whatsapp-business-account-solutions-list-api#get-version-waba-id-solutions) to get a list of solutions that onboarded a specific WABA.

Example Request

```curl
curl 'https://graph.facebook.com/v25.0/102290129340398/solutions' \
-H 'Authorization: Bearer EAAAT...'
```

Example Response

```json
{
  "data": [
    {
      "name": "Social OVD with Social Brew",
      "status": "ACTIVE",
      "status_for_pending_request": "NONE",
      "id": "17602267745700"
    }
  ],
  "paging": {
    "cursors": {
      "before": "QVFIUjZACTFNmWURVTHN2NFVaM2ZApd2RaOGIxOU5wenpQZADFkbVdtSEJDSGFDelhDOU5hT28xcmJLS05TM3U0UUFmdVNGUWFfdjdJb1o2OTVNY083ZAHYtc2x3",
      "after": "QVFIUjZACTFNmWURVTHN2NFVaM2ZApd2RaOGIxOU5wenpQZADFkbVdtSEJDSGFDelhDOU5hT28xcmJLS05TM3U0UUFmdVNGUWFfdjdJb1o2OTVNY083ZAHYtc2x3"
    }
  }
}
```

### Get partners of a solution

Use the [Partners API](https://developers.facebook.com/docs/graph-api/reference/whats-app-business-solution/partners) to get a list of partners of a solution.

Example Request

```curl
curl 'https://graph.facebook.com/v25.0/17602267745700/partners' \
-H 'Authorization: Bearer EAAAT...'
```

Example Response

```json
{
  "data": [
    {
      "partner_app": {
        "link": "https://www.socialoverdrive.com",
        "name": "Social Overdrive",
        "id": "637576208107267"
      },
      "status": "ACCEPTED",
      "id": "17602267745704"
    }
  ],
  "paging": {
    "cursors": {
      "before": "QVFIUmxnSE9LUFliNzlUTWdhTlYzQjBtekprSC0wQUdoZAGRYbFlzeUpDMG9yNkF1OHYyel9tcUlBbGhFckxJQ1Y3UFZA4dUkycEk0WDJwRGYzT2JYbVhEdFdB",
      "after": "QVFIUmxnSE9LUFliNzlUTWdhTlYzQjBtekprSC0wQUdoZAGRYbFlzeUpDMG9yNkF1OHYyel9tcUlBbGhFckxJQ1Y3UFZA4dUkycEk0WDJwRGYzT2JYbVhEdFdB"
    }
  }
}
```

## Getting customer business tokens

If you are not hosting Embedded Signup but want to get an onboarded business customer’s [business integration system user access token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens) (“business token”), you can get their token using the business portfolio ID and solution ID contained in the [account_update](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/multi-partner-solutions#account-update-webhook) webhook that was triggered when the customer completed the Embedded Signup flow.

### Request

Use the [GET /<SOLUTION_ID>/access_token](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-solution/access-token-api#Reading) endpoint and request the `business_id` parameter to get an onboarded business customer’s [business token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens).

```html
curl 'https://graph.facebook.com/<API_VERSION>/<SOLUTION_ID>/access_token?business_id=<CUSTOMER_BUSINESS_PORTFOLIO_ID>' \
-H 'Authorization: Bearer <SYSTEM_TOKEN>'
```

### Request parameters

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<API_VERSION>`<br>*String* | **Optional.**<br>Graph API version. | v25.0 |
| `<CUSTOMER_BUSINESS_PORTFOLIO_ID>` | **Required.**<br>The onboarded business customer’s business portfolio ID.<br>This is included in [account_update webhooks](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/manage-webhooks#onboarded-business-customer) when the business customer completes Embedded Signup. | `2729063490586005` |
| `<SOLUTION_ID>` | **Required.**<br>Your Multi-Partner Solution ID. | `303610109049230` |
| `<SYSTEM_TOKEN>` | **Required.**<br>Your [system user access token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens). | `EAAAN6tcBzAUBOZC82CW7iR2LiaZBwUHS4Y7FDtQxRUPy1PHZClDGZBZCgWdrTisgMjpFKiZAi1FBBQNO2IqZBAzdZAA16lmUs0XgRcCf6z1LLxQCgLXDEpg80d41UZBt1FKJZCqJFcTYXJvSMeHLvOdZwFyZBrV9ZPHZASSqxDZBUZASyFdzjiy2A1sippEsF4DVV5W2IlkOSr2LrMLuYoNMYBy8xQczzOKDOMccqHEZD` |

### Response

Upon success:

```html
{
  "data": [
    {
      "access_token": "<CUSTOMER_BUSINESS_TOKEN>"
    }
  ]
}
```

## Migrating business customer assets among solutions

You have several options for migrating business customer assets to and from Multi-Partner Solutions. See [Migrating business customer assets](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/support#migrating-business-customer-assets).
