# Onboard business customers | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/onboard-business-customers_

---

# Onboard business customers

Updated: Feb 10, 2026

The MM API for WhatsApp onboarding process is designed to be simple for you as a partner to adopt, making it quick and easy for [solution providers](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/overview) (including Solution Partners, Tech Providers, and Tech Partners) to onboard current customers from Cloud API onto the MM API for WhatsApp. If your business directly integrates with Cloud API without a partner, follow the instructions below to accept the Terms of Service and onboard to the MM API for WhatsApp via WhatsApp Manager.

## Before you begin

Your app must have advanced access for the following permissions:

- **`whatsapp_business_messaging`** : This permission allows the app to call the MM API for WhatsApp to send messages.
- **`whatsapp_business_management`** : This permission enables the app to manage WABAs, Phone Numbers, and Templates via [WhatsApp Business Management API](https://developers.facebook.com/documentation/business-messaging/whatsapp/analytics) .
- **`ads_read`** (optional): This permission grants the app access to the [Insights API](https://developers.facebook.com/documentation/ads-commerce/marketing-api/insights) , allowing partners to retrieve metrics on conversions.

If your app does not already have advanced access for these permissions, request advanced access via [App Review](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/app-review).

## Solution partner integration overview

To assist your customers in using the MM API for WhatsApp, several steps are required:

| Step | Notes |
| --- | --- |
| 1: Onboard yourself | Enroll via [App Dashboard](https://developers.facebook.com/apps) and follow instructions under the [Onboarding yourself](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/onboard-business-customers#onboarding-yourself). |
| 2: Send messages | Same Template endpoint and message send payload as Cloud API - only the ‘send message’ endpoint changes. |
| 3: View metrics | **New!** Integrate with the Insights API to view the metrics as Cloud API (sent/read/delivered), plus new metrics like Website and App conversions. |

## Onboarding yourself

### Register yourself for MM API for WhatsApp

To enroll, a solution provider must:

1. Navigate to the **[App Dashboard](https://developers.facebook.com/apps)** > **WhatsApp** > **Quickstart** panel
2. On the **Quickstart** page, locate the “Improve ROI with Marketing Messages API for WhatsApp” card and click the “Get started” button
3. Request any missing app review permissions by clicking the “Request permission” button. See “ [Submit for app review](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/app-review) ” for more information
4. Click on “Continue to integration guide” to accept the Terms of Service

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/475969838_666164382411179_8539011248692952115_n.png?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=kDfYBktGjJQQ7kNvwE_Y0Cs&_nc_oc=AdoLW1rjUGE79X1OqMzXRfWnI3-btpy2xGIO6jXXXGMy4CjAtRCgfjQftAHRKj7vCh4&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=FxqK-l_rixpruo46S4GLcQ&_nc_ss=7b20f&oh=00_Af53u2d-jKbYg_ckQ90hVyeBkfhzzK6rwzWRbCy3lhZ7hQ&oe=6A1BFE40)

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/540765034_1761649757794419_9069938397320792839_n.png?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=TLiGrWT5MAwQ7kNvwFdwu1F&_nc_oc=AdpAEdfq1SrUqzj7poCAIgahP42iDcN44z2Px5nuS9Qjy8XgSyhpfgHt8M0pdMWREoE&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=FxqK-l_rixpruo46S4GLcQ&_nc_ss=7b20f&oh=00_Af7he3K9yfLJuU6-HmQmvLwv5QIFRwE83l6ZwQ8U6c1Muw&oe=6A1C2499)

### Submit for app review for Advanced App permissions

Solution Providers must use an App with the following Advanced App permissions, when using the MM API for WhatsApp.

If you do not already have an App with the following Advanced App Permissions, it is necessary for your App to go through [App review](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/app-review):

| Advanced App Permission | Required in order to do the following on behalf of your customer |
| --- | --- |
| `whatsapp_business_messaging` | Call the MM API for WhatsApp ‘send messages’ endpoint, to send messages via Marketing Messages API for WhatsApp |
| `whatsapp_business_management` | Call WABA, Phone Number, and Template endpoints, for managing WABAs, Phone Numbers, and Templates; and retrieve basic metrics via [WhatsApp Business Management API](https://developers.facebook.com/documentation/business-messaging/whatsapp/analytics) |
| `ads_read` (optional) | This permission is optional, and is only required to call the [Insights API](https://developers.facebook.com/documentation/ads-commerce/marketing-api/insights), allowing a partner to fetch advanced metrics on conversions (e.g. Web conversions, App conversions) |

For the app review submission, prepare a screen recording of how each permission is used. It is recommended to show a sample of each action in the “Required in order to do …” column above, to demonstrate each permission in use.

## Onboarding end businesses

There are multiple ways that a partner can onboard a business they work with to the MM API for WhatsApp, and fetch the required access tokens needed to send messages and fetch metrics on their behalf:

- **via WhatsApp Manager** (recommended)
- **via Embedded Signup**

### Self-onboard to MM API for WhatsApp via WhatsApp Manager (recommended)

If your business integrates with Cloud API with a solution provider, they can [onboard directly via WhatsApp Manager](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/onboarding).

### Onboard a business to MM API for WhatsApp using Embedded Signup

MM API for WhatsApp has its own embedded signup flow for Solution Providers to use, which:

- allows your clients to register for Cloud API and MM API for WhatsApp
- allows you to request an access token with the necessary permissions to send messages via MM API for WhatsApp and retrieve metrics from the Insights API on behalf of your customers.

Step 1: Integrate with the Facebook Login SDK

If you have not already done so for Cloud API, set up the Facebook JavaScript SDK and Facebook Login to embed the signup flow into your website or client portal. You may embed the flow in multiple webpages or portals that you own.

Step 2: Set up a new permission configuration

Follow the instructions in [Step 2 of the Embedded Signup docs](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/implementation#step-2--create-a-facebook-login-for-business-configuration) to create a new Facebook Login for Business configuration. Select the following in your configuration:

Assets:

- WhatsApp accounts
- (Do not select the other options of Ad accounts, Pages, Catalogues, Pixels, Instagram accounts)

Permissions:

- `ads_read` (optional)
- `whatsapp_business_management`
- `whatsapp_business_messaging`

Step 3: Launch Embedded Signup

Refer to the [Embedded Sign up implementation](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/implementation) document and add `marketing_messages_lite` to the list of features before onboarding WhatsApp SMB users.

```html
{
  "config_id": "<config_id>",
  "response_type": "code",
  "override_default_response_type": true,
  "extras": {
    "featureType": "whatsapp_business_app_onboarding",
    "sessionInfoVersion": "3",
    "features": [
      {
        "name": "marketing_messages_lite"
      }
    ],
    "version": "v3"
  }
}
```

Step 4: Wait for the onboarding confirmation webhook

Once a business admin completes the MM API for WhatsApp onboarding flow, and any backend onboarding processes complete successfully, an `account_update` webhook will be sent for each WABA under the BMID, to indicate that onboarding has successfully completed.

See the [Onboarding](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/onboarding) for details on the `account_update` webhook.

After a business goes through the Embedded Signup flow for MM API for WhatsApp, the returned system user app token will have permission to send messages via MM API for WhatsApp, and fetch metrics via the Insights API.

## Onboard a business to Marketing Messages API for WhatsApp using the Intent API

Partners can use the Intent API to onboard a business to Marketing Messages API for WhatsApp (MM API for WhatsApp) while automatically marking all On-behalf-of (OBO) WABAs to be transferred to your customer, and receive an async (webhook) notification when the onboarding is complete to fetch the necessary access tokens.

If an end business has any OBO WABAs that do not currently have an OBO migration intent set, this intent will automatically be set for all OBO WABAs between the partner and end business through this API call.

1) Call the intent API

Calling the intent API to onboard a BMID to MM API for WhatsApp will trigger an email to all admins of that BMID, directing them to an onboarding flow in Business Manager. Meta will contact admins of the BMID until they either onboard or reject the invitation to onboard.

Partners must use a System User Access Token for the App with advanced permissions to call the intent API for each of their eligible end businesses.

An eligible end business is one that:

- Has not yet signed the MM API for WhatsApp ToS
- Is currently a partner business as dictated by 1+ shared or OBO WABAs with the BSP
- Has 1+ WABAs in an MM API for WhatsApp eligible tax country

Request:

```html
curl -i -X POST \
"https://graph.facebook.com/<API_VERSION>/<END_BUSINESS_ID>/onboard_partners_to_mm_lite?access_token=<SYSTEM_USER_ACCESS_TOKEN>"
```

Optional Body:

If a partner wants to migrate OBO WABAs to a WhatsApp Business Solution as opposed to being shared solely with the partner, an optional solution_id can be passed into the API call.

```html
{
  "solution_id": "<MULTI-PARTNER_SOLUTION_ID>"
}
```

Response:

```html
{
  "request_id": "893436979557695"
}
```

- Error: Invalid recipient type Reason: The end business is not eligible to onboard onto MM API for WhatsApp because
 They have either accepted the ToS alreadyThe end business is not in an allowlisted countryThere are no country eligible WABAs shared with the BSP
- Error: Your business has already sent this request. To follow up on the request, contact the business you’re requesting access from. Reason: There is already a request to this end business to onboard onto MM API for WhatsApp using this flow.
- Error: The app does not have sufficient permissions to call this API. Reason: The app SUAT used to call the API must have advanced access on at least whatsapp_business_messaging and whatsapp_business_management.
- What is the expected behavior for OBO WABAs and the migration intent that gets set? 1 shared, 4 OBO with intent
 Call succeeds, creating an MM API for WhatsApp intent, does not set new OBO intent0 shared, 5 OBO with intent
 Call succeeds, creating an MM API for WhatsApp intent, does not set new OBO intent1 shared, 4 OBO without intent
 Call succeeds, creating an MM API for WhatsApp intent, sets new OBO intent0 shared, 5 OBO without intent
 Call succeeds, creating an MM API for WhatsApp intent, contingent on setting OBO intent0 shared, 0 OBO
 Call fails, no MM API for WhatsAppor OBO intent is set

2) Wait for the onboarding confirmation webhook

Once a business admin completes the MM API for WhatsApp onboarding flow, and any backend onboarding processes complete successfully, a new account_update webhook will be sent for each WABA under the BMID, to indicate that onboarding has successfully completed.

3) Fetch an updated Business Integration System User Access Token (BISUAT)
In order to call the Insights API, you will need a Business Integration System User Access Token scoped to the Ad account that is linked to the WABA you are managing.
Follow the guide in the “Business Integration System User Access Token Management API” section to fetch your existing token for managing ad account IDs received in the webhook.

Request syntax:

```html
curl -i -X POST "https://graph.facebook.com/<API_VERSION>/<CLIENT_BUSINESS_ID>/system_user_access_tokens
    ?appsecret_proof="<APPSECRET_PROOF_HASH>"
    &access_token="<SYSTEM_USER_ACCESS_TOKEN>"
    &fetch_only=true
```

| Object | Description | Example Value |
| --- | --- | --- |
| `<API_VERSION>` | Graph API version. | v23.0 |
| `<APPSECRET_PROOF_HASH>` | Required. The appsecret_proof is a sha256 hash of your access token ensuring API calls are from a server are more secure. [Learn more](https://developers.facebook.com/docs/graph-api/guides/secure-requests#generate-the-proof). | e3b0c... |
| `<CLIENT_BUSINESS_ID>` | Required. Client business ID. | 2780023991704 |
| `<SYSTEM_USER_ACCESS_TOKEN>` | Required. This access token requires the business_management permission. | EAAJZC... |

Response syntax

```html
{
  "access_token": "<NEW_ACCESS_TOKEN>"
}
```

### Onboard WhatsApp Business app users

You can configure Embedded Signup to [allow business customers to onboard using their existing WhatsApp Business app account and phone number:](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users)

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/477341352_1809983926468415_3794578338113490554_n.png?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=SWGfy-RnFc4Q7kNvwFL36xb&_nc_oc=AdquW8j2xDfh8hTx-AllSWaAlSpXuqytiw5PMmv1wkkec_pwxybzYQIYFt0Bf6iAIDY&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=FxqK-l_rixpruo46S4GLcQ&_nc_ss=7b20f&oh=00_Af4EnwR804F5n1q2bMPjju4vTqAju391qJmA4XEpqqS6gA&oe=6A1C2ADB)

Businesses who are successfully onboarded after choosing this option will then be able to use your app to message their customers at scale, but still have the ability to send messages on a one-to-one basis using the WhatsApp Business app.

Note: To ensure accurate metrics tracking, we recommend that business customers avoid clicking links in their own marketing messages. Clicking these links may affect tracking data and could lead to skewed results.

### Offboard WhatsApp Business app users

When you offboard a WhatsApp Business app phone number, you will automatically be offboarded from MM API for WhatsApp. The ad account will be disabled and unlinked which will prevent conversion metrics tracking.

## Help the business set up Conversion measurement

See [Setting up conversion measurement](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/measure-conversion) for details on how businesses can measure when a marketing message from MM API for WhatsApp leads to a conversion (e.g. add to cart, purchase).

Partners are **strongly recommended** to work with their clients to set up Conversion reporting, so that they can take advantage of measuring the improved metrics and optimizations MM API for WhatsApp provides.

## Sending messages

See [Sending messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/send-marketing-messages) for documentation on how to send messages and receive webhooks on behalf of your customers via MM API for WhatsApp.

## Viewing metrics

See the Guide to [Viewing metrics](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/view-metrics) for documentation on how to:

- Fetch the IDs of the Ad entities mapped to a business’ WABAs and Templates, in order to call Insights APIs.
- Fetch metrics for messages sent via MM API for WhatsApp.

Partners are **strongly recommended** to fetch metrics using the Ads Insights APIs (not Business Management APIs), as these APIs provide richer metrics reporting, including conversion reporting from sources such as Web and App conversion events.

After integrating with reporting APIs (Insights API recommended), surface these metrics in your dashboards and APIs for your customers to use.

Reach out to your Partner Manager for suggestions on metrics best practices, including a copy of Meta’s “**Business Messaging Reporting Dashboards Playbook**” for partners.
