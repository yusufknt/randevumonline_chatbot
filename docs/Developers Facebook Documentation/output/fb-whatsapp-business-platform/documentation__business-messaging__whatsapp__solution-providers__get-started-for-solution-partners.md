# Get started as a Solution Partner | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/get-started-for-solution-partners_

---

# Get started as a Solution Partner

Updated: Dec 12, 2025

This guide goes over the steps [Solution Partners](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/overview#solution-partners) need to take in order to offer the Cloud API to their customers. There are 4 main stages:

1. [Prepare & Plan](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/get-started-for-solution-partners#prepare-plan)
2. [Set up Assets](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/get-started-for-solution-partners#set-up-assets)
3. [Sign Contracts](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/get-started-for-solution-partners#sign-contracts)
4. [Build Integration](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/get-started-for-solution-partners#build-integration)

After you’re done, please [keep up with monthly updates](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/get-started-for-solution-partners#keep-up-with-monthly-updates).

## Prepare & plan

### Read documentation

Before you start, we recommend reading through our [developer documentation](https://developers.facebook.com/documentation/business-messaging/whatsapp/about-the-platform#whatsapp-cloud-api) and our [Postman collection](https://www.postman.com/meta/workspace/whatsapp-business-platform/collection/13382743-84d01ff8-4253-4720-b454-af661f36acc2). This helps you understand how the Cloud API works, including how to get started and migrate numbers.

### Plan onboarding & migration

**We recommend that you use Embedded Signup to onboard new business customers to the Cloud API.** If you haven’t already, implement [Embedded Signup](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/overview). Embedded Signup is the fastest and easiest way to register business customers, enabling them to start sending messages in less than five minutes.

## Set up assets

To use the Cloud API, Solution Partners need to have the following assets:

| Asset | Specific Instructions |
| --- | --- |
| **Business portfolio** | You can use an existing one, or [set up a new one](https://www.facebook.com/business/help/1710077379203657). Save the business portfolio ID. |
| **WhatsApp Business Account** (WABA) | See [Create a WhatsApp Business Account for the WhatsApp Business API](https://www.facebook.com/business/help/2087193751603668) for help. |
| [**Meta App**](https://developers.facebook.com/apps/) | If you don’t have an app, you need to [create one](https://developers.facebook.com/docs/development/create-an-app) with the **Business** type. Remember to add a display name and a contact email to your app.<br>As a (Solution Partner), your app must go through [App Review](https://developers.facebook.com/docs/app-review) and request Advanced Access to the following permissions:<br>[`whatsapp_business_management`](https://developers.facebook.com/docs/permissions/reference/whatsapp_business_management) — Used to manage phone numbers, message templates, registration, business profile under a WhatsApp Business Account. To get this permission, your app must go through [App Review](https://developers.facebook.com/docs/app-review).[`whatsapp_business_messaging`](https://developers.facebook.com/docs/permissions/reference/whatsapp_business_messaging) — Used to send/receive messages from WhatsApp users, upload/download media under a WhatsApp Business Account. To get this permission, your app must go through [App Review](https://developers.facebook.com/docs/app-review).[`whatsapp_business_manage_events`](https://developers.facebook.com/docs/permissions#whatsapp_business_manage_events) — Used to log events—such as purchases, add-to-cart actions, leads, and more under a WhatsApp Business Account. Only request this permission if you are using the [Marketing Messages API for WhatsApp](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/overview) with [Conversions API](https://developers.facebook.com/documentation/ads-commerce/conversions-api). To get this permission, your app must go through [App Review](https://developers.facebook.com/docs/app-review).<br>As a Solution Partner, you can also feel free to use the same Meta app across different clients and WABAs. But be aware that each app can only have one webhook endpoint and each app needs to go through App Review. |
| **System User** | See [Add system users to your business portfolio](https://www.facebook.com/business/help/503306463479099) for help.<br>Currently, a Meta App with `whatsapp_business_messaging`, `whatsapp_business_management`, `whatsapp_business_manage_events`, and `business_messaging` permissions has access to up to:<br>1 admin system user1 employee system user<br>We recommend using the admin system user for your production deployment. See [About business portfolio access](https://www.facebook.com/business/help/442345745885606) for more information. |
| **Business Phone Number** | This is the phone number the business will use to send messages. Phone numbers need to be verified through SMS/voice call.<br>For Solution Partners and Direct Developers: If you wish to use your own number, then you should [add a phone number](https://www.facebook.com/business/help/456220311516626) in WhatsApp Manager and verify it with the [Verify Code API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/verify-code-api#post-version-phone-number-id-verify-code).<br>For business customers of Solution Partners: If you wish to use your own number, then you should add and verify their numbers using the Solution Partner’s [Embedded Signup flow](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/overview).<br>There is no limit to the amount of business phone numbers that can be onboarded to the Cloud API. |
| **Consumer Phone Number** | This is a phone number that is currently using the consumer WhatsApp app. This number will be receiving the messages sent by your business phone number. |

## Sign contracts

### Accepting Terms of Service

In order to access the WhatsApp Business Messaging Cloud API you need to first accept the WhatsApp Business Platform Terms of Service on behalf of your business.

To do so, navigate to [WhatsApp Manager](https://business.facebook.com/wa/manage/) and accept the Terms of Service in the informational banner.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/573027894_844716734562313_3897613670462505628_n.png?_nc_cat=110&ccb=1-7&_nc_sid=e280be&_nc_ohc=mBIkXQbWOAwQ7kNvwFukD0o&_nc_oc=AdpJuSoWNspMS5l3NyflL1V3S27UpSexUvs3t0lsSNaPFJ_Tc-ThccY1vPfJFKO102A&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=yXnmCTYfX1JQO6uO9Z0bYw&_nc_ss=7b20f&oh=00_Af6FmALH_HzajXYH-v3fL4F6QUx7Z7Mx5fOezQWXUNCwVQ&oe=6A1C1CD9)

For any new Cloud API businesses, you will need to accept Terms of Service before you can start using Cloud API. Registration calls will fail until you accept the Terms of Service.

You as a developer need to accept the Terms of Service. If you are a Solution Partner, you do not need your customers to accept.

## Build integration

### Step 1: Get system user access token

Graph API calls use access tokens for authentication. For more information, see [Access Tokens](https://developers.facebook.com/documentation/facebook-login/guides/access-tokens). We recommend using your system user to generate your token.

To generate a system user access token:

1. Go to [Business portfolio](https://business.facebook.com/) > Business Settings > Users > System Users to view the system user you created.
2. Click on that user and select Add Assets. This action launches a new window.
3. Under Select Asset Type on the left side pane, select Apps. Under Select Assets, choose the Meta app you want to use (your app must have the correct permissions). Enable Develop App for that app.
4. Select Save Changes to save your settings and return to the system user main screen.
5. Now you are ready to generate your token. In the system user main screen, click Generate Token and select your Meta app.
6. After selecting the app, you will see a list of available permissions.
Select `whatsapp_business_management` , `whatsapp_business_messaging` , and `whatsapp_business_manage_events` . Click Generate Token.
7. A new window opens with your system user, assigned app and access token. Save your token.
8. Optionally, you can click on your token and see the Token Debugger. In your debugger, you should see the permissions you have selected. You can also directly paste your token into the [Access Token Debugger](https://developers.facebook.com/tools/debug/accesstoken).

### Step 2: Set up webhooks

With Webhooks set up, you can receive real-time HTTP notifications from the WhatsApp Business Platform. This means you get notified when, for example, you get a message from a customer or there are changes to your WhatsApp Business Account (WABA).

To set up your webhook endpoint, you need to create an internet-facing web server with a URL that meets Meta’s and WhatsApp’s requirements. See our [Webhooks](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/overview) document for more information. If you need an endpoint for testing purposes, [you can deploy a test app](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/set-up-whatsapp-echo-bot) that simply dumps webhook payloads to your console.

App setup

Once the endpoint is ready, configure it to be used by your Meta app:

In the App Dashboard, go to **WhatsApp** > **Configuration**, then click the **Edit** button.

- Callback URL: This is the URL Meta will be sending the events to. See the [Webhooks, Getting Started](https://developers.facebook.com/docs/graph-api/webhooks/getting-started) guide for information on creating the URL.
- Verify Token: This string is set up by you, when you create your webhook endpoint.

After adding the information, click **Verify and Save**.

After saving, back in the **Configuration** panel, click the **Manage** button and subscribe to individual webhook fields. To receive notifications of customer messages, be sure to subscribe to the **messages** webhook field.

You only need to set up Webhooks once for every application you have. You can use the same Webhook to receive multiple event types from multiple WhatsApp Business Accounts, or set up an override. For more information, see our Webhooks section.

### Step 3: Subscribe to your WABA

To make sure you get notifications for the correct account, subscribe your app:

```html
curl -X POST \
'https://graph.facebook.com/v25.0/<WHATSAPP_BUSINESS_ACCOUNT_ID>/subscribed_apps' \
-H 'Authorization: Bearer <ACCESS_TOKEN>'
```

If you get the response below, all Webhook events for the phone numbers under this account will be sent to your configured Webhooks endpoint.

```json
{
  "success": true
}
```

### Step 4: Get phone number ID

To send messages, you need to register the phone number you want to use. Before you can register it, you need to get the phone number’s ID. To get your phone number’s ID, make the following API call:

```html
curl -X GET \
'https://graph.facebook.com/v25.0/<WHATSAPP_BUSINESS_ACCOUNT_ID>/phone_numbers' \
-H 'Authorization: Bearer <ACCESS_TOKEN>'
```

If the request is successful, the response includes all phone numbers connected to your WABA:

```json
{
  "data": [
    {
      "verified_name": "Jasper's Market",
      "display_phone_number": "+1 631-555-5555",
      "id": "1906385232743451",
      "quality_rating": "GREEN"
    },
    {
      "verified_name": "Jasper's Ice Cream",
      "display_phone_number": "+1 631-555-5556",
      "id": "1913623884432103",
      "quality_rating": "NA"
    }
  ]
}
```

Save the ID for the phone number you want to register. See [Read Phone Numbers](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers) for more information about this endpoint.

Migration exception

If you are migrating a phone number from the On-Premises API to the Cloud API, there are extra steps you need to perform before registering a phone number with the Cloud API. See [Migrate From On-Premises API to Cloud API](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/migrating-from-onprem-to-cloud) for the full process.

### Step 5: Register phone number

With the phone number’s ID in hand, you can register it. In the registration API call, you perform two actions at the same time:

1. Register the phone.
2. [Enable two-step verification](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/two-step-verification) by setting a 6-digit registration code —you must set this code on your end. Save and memorize this code as it can be requested later.

**Setting up two-factor authentication is a requirement to use the Cloud API. If you do not set it up, you will get an onboarding failure message:**

![Onboard Failure: To continue working in your account, please refresh the page to authenticate. Or navigate to the business settings page and authenticate when prompted.](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/561060937_1339318307926820_7669657060757741637_n.jpg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=jo72O8OqNNoQ7kNvwHDfhC6&_nc_oc=AdogAk_1mJqOCvT-Nm8SWt-itkYNPu-EkYvOXMjxeaH6a8wiUVApfSlXPdW7wgaRoGY&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=yXnmCTYfX1JQO6uO9Z0bYw&_nc_ss=7b20f&oh=00_Af5Cb23YKmgpPY4xfBqCVRrGU9WE6tuVMNkMcEMi6-WHAg&oe=6A1C1290)

Sample request:

```html
curl -X POST \
'https://graph.facebook.com/v25.0/<FROM_PHONE_NUMBER_ID>/register' \
-H 'Authorization: Bearer <ACCESS_TOKEN>' \
-H 'Content-Type: application/json' \
-d '{"messaging_product": "whatsapp","pin": "<6_DIGIT_PIN>"}'
```

Sample response:

```json
{
  "success": true
}
```

Embedded Signup users

A phone number **must** be registered up to 14 days after going through the Embedded Signup flow. If a number is not registered during that window, the phone must go through to the Embedded Signup flow again prior to registration.

### Step 6: Receive a message From consumer app

Once participating customers send a message to your business, you get **24 hours of free messages with them** —that window of time is called the customer service window. For testing purposes, we want to enable this window, so you can send as many messages as you would like.

From a personal WhatsApp iOS/Android app, send a message to the phone number you just registered. Once the message is sent, you should receive an incoming message to your Webhook with a notification in the following format.

```json
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "102290129340398",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "16315551234",
              "phone_number_id": "PHONE_NUMBER_ID"
            },
            "contacts": [
              {
                "profile": {
                  "name": "Kerry Fisher"
                },
                "wa_id": "16315555555"
              }
            ],
            "messages": [
              {
                "from": "16315555555",
                "id": "wamid.ABGGFlA5FpafAgo6tHcNmNjXmuSf",
                "timestamp": "1602139392",
                "text": {
                  "body": "Hello!"
                },
                "type": "text"
                }
            ]
          },
        "field": "messages"
        }
      ]
    }
  ]
}
```

### Step 7: Send a test message

Once you have enabled the customer service window, you can send a test message to the consumer number you used in the previous step. To do that, make the following API call:

```html
curl -X  POST \
'https://graph.facebook.com/v25.0/<FROM_PHONE_NUMBER_ID>/messages' \
-H 'Authorization: Bearer <ACCESS_TOKEN>' \
-H 'Content-Type: application/json' \
-d '{"messaging_product": "whatsapp", "to": "16315555555","text": {"body" : "hello world!"}}'
```

If your call is successful, your response will include a message ID. Use that ID to track the progress of your messages through Webhooks. The maximum length of the ID is 128 characters.

Sample response:

```json
{
  "id":"wamid.gBGGFlaCGg0xcvAdgmZ9plHrf2Mh-o"
}
```

With the Cloud API, there is no longer a way to explicitly check if a phone number has a WhatsApp ID. To send someone a message using the Cloud API, just send it directly to the WhatsApp user’s phone number after they have [opted-in](https://developers.facebook.com/documentation/business-messaging/whatsapp/getting-opt-in). See [Sending messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages).

## Onboard WhatsApp Business app users

If your business customers already use the [WhatsApp Business app](https://business.whatsapp.com/products/business-app), you can configure Embedded Signup to [onboard them using their existing account and phone number](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users). Onboarded customers can use your app to message at scale while continuing to use the WhatsApp Business app for one-to-one conversations.

## Keep up with monthly updates

We will release Cloud API updates on the first Tuesday of every month. Those will include new features and improvements. You don’t need to do any work to use any of the new features, since the Cloud API updates automatically.

## FAQs

### General FAQs

Which company will be providing the Cloud API?

WhatsApp develops and operates the WhatsApp Business API, which enables businesses to communicate with WhatsApp consumer users on the WhatsApp network. When using the Cloud API, Meta will host the WhatsApp Business API for you and provide an endpoint for the WhatsApp service for your incoming and outgoing WhatsApp communications.

Are there any additional costs for the Cloud API?

Access to Cloud API is free, and we expect it to generate additional cost savings for developers, as Meta hosts and maintains the Cloud API.

### Technical implementation FAQs

What is the architecture of the Cloud API?

The Cloud API architecture significantly simplifies the Solution Partner’s operational and infrastructure requirements to integrate with WhatsApp Business Platform. First, it removes the infrastructure requirements to run Business API docker containers (CAPEX savings). Second, it obviates the need of operational responsibilities to manage the deployment (OPEX savings).
![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/574916010_1357390812786236_2094506065743510683_n.jpg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=OHCG0WQM1VsQ7kNvwHb_81I&_nc_oc=AdrVVk6rh0pEygWV1lV30UOOnXmNVYN_wqYEl_qMxRcopCuIbIRWLFY4Z2bIwB4TvlY&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=yXnmCTYfX1JQO6uO9Z0bYw&_nc_ss=7b20f&oh=00_Af64HDJHEZfHOzSKa4l6S3DanJROagQROb7UHbsX-gLyRA&oe=6A1C1754)

What will disaster recovery look like: if a region is unavailable, how much time does it take to move messages to another region?

We will have disaster recovery and data replication across multiple regions. The expected downtime would be within our SLA and usually in the order of less than a minute to less than five minutes.

### Data privacy & security FAQs

Where are the servers for Cloud API?

Cloud API processes messages on servers in [Meta data centers](https://datacenters.atmeta.com/all-locations/). If a business opts to use Cloud API Local Storage, message data is stored in data centers located in another [designated country](https://developers.facebook.com/documentation/business-messaging/whatsapp/local-storage).

Is the Cloud API end-to-end encrypted? What is the encryption model?

See [Cloud API Overview, Encryption](https://developers.facebook.com/documentation/business-messaging/whatsapp/about-the-platform#encryption).

What happens to message data at rest? How long is it stored?

Cloud API messages at rest are encrypted. Messages have a maximum retention period of 30 days in order to provide the base features and functionality of the Cloud API service; for example, retransmissions.

Does Meta have access to encryption keys?

In order to send and receive messages through Cloud API, Cloud API manages the encryption/decryption keys on behalf of the business. For more detail, see the [WhatsApp Encryption Overview technical whitepaper](https://www.whatsapp.com/security/WhatsApp-Security-Whitepaper.pdf).

### Regulatory compliance FAQs

How does Cloud API comply with regional data protection laws (such as GDPR, LGPD, and PDPB)?

Meta takes data protection and people’s privacy very seriously and we comply with applicable legal, industry, and regulatory requirements governing data protection, as well as industry best practices. Cloud API customers must meet their own obligations under data protection laws, such as the General Data Protection Regulation (GDPR). Please visit our [Meta Business Messaging Compliance Center](https://www.facebook.com/business/business-messaging/compliance) to learn more.
