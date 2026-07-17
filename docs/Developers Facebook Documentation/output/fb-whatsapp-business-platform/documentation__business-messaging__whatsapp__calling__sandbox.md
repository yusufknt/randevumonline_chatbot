# Set Up a Sandbox Account for Calling | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/sandbox_

---

# Set Up a Sandbox Account for Calling

Updated: Apr 7, 2026

Sandbox accounts are only available to you if you are a Tech Partner.

## Overview

A WhatsApp sandbox account is a mock WhatsApp Business Account that you can use to test your Calling API integration. Use a calling sandbox account to test the following features:

- Initiate and receive calls using the Calling API
- Validate calling webhook events
- Simulate onboarding flows without creating real business assets

## Sandbox account calling limits

The following table outlines the calling limits for sandbox accounts. These limits are subject to change.

| Limit | Description | Production number limit | Public test number limit |
| --- | --- | --- | --- |
| Connected call limit | Number of calls a business is allowed to make on approved permissions. | 100 connected calls per 24 hrs | No change |
| Call Permission Request message limits | Limits the number of call permission request messages that can be sent to the same consumer | 1 request per day<br>2 requests per week | 25 requests per day<br>100 requests per week |
| Unanswered call limits | When a business initiated call goes unanswered (In essence, is rejected by the user or missed by the user). | Nudge on 2 consecutive unanswered calls<br>Revoke permission on 4 consecutive unanswered calls | Nudge on 5 consecutive unanswered calls<br>Revoke on 10 consecutive unanswered calls |
| Temporary call duration | Duration a business can call the user after permission is approved. | 7 days | No change |

## Set up a sandbox account

### Step 1. Claim a sandbox account

Follow the instructions in [Embedded Signup Overview — Claiming sandbox accounts](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/overview#claiming-sandbox-accounts) to claim your sandbox account.

### Step 2. Obtain credentials and identifiers for your sandbox account

1. In the [App Dashboard](https://developers.facebook.com/apps) , navigate to your app, then select **WhatsApp** > **Embedded Signup Builder** in the sidebar. **Note: Keep this tab open and available as you will use it multiple times throughout this process.**
2. Ensure that the **Features** dropdown is empty, then click **Login with Facebook** .
3. A popup with the embedded signup experience will show. Under **Business portfolio** select **Sandbox Business** .
4. Fill in the rest of the required information, then click **Next** .
5. On the next screen, in the **Create or Select a WhatsApp Business Profile** dropdown, select **Test Number** .
6. Once the login flow is complete, in the **Exchange Token** section, click **Get Token** . **Note: Retain this token for future sandbox account API use.**
7. In the **Fetch Shared WhatsApp Business Account** section, click **Fetch WABA details** .
8. Under **WhatsApp business account field** , copy the **Value** for the `id` row. **Note: Retain this ID since it is the WhatsApp Business Account ID for the sandbox WABA.**
9. In the **Fetch phone numbers** section, click **Fetch phone numbers** .
10. Under **ID** , copy the value. **Note: Retain this ID since it is the phone number ID for your sandbox account test phone number.**

### Step 3. Register your test phone number and subscribe to your WABA

*Prerequisites*

*Ensure that you have the following information from the previous steps:*

- *Your sandbox account token string*
- *Your sandbox account WABA ID*
- *Your test phone number ID*

To complete these next steps, you will use the [Graph API Explorer tool](https://developers.facebook.com/tools/explorer/).

- **Note: Keep this window open as you will use the configuration you created again in later steps in this guide.**

1. Navigate to the [Graph API Explorer tool](https://developers.facebook.com/tools/explorer/) .
2. Ensure you are on the latest version of the API.
3. Click **Generate Access Token** and follow the prompts.
4. Under **Permissions** , add the `whatsapp_business_management` and `whatsapp_business_messaging` permissions
5. In the endpoint builder, enter `/<YOUR_SANDBOX_WABA_ID>/subscribed_apps` , then click **Submit** .

```curl
{
  "success": true
}
```

1. Next, register your test phone number by entering `/<YOUR_SANDBOX_TEST_PHONE_NUMBER_ID>/register` in the endpoint builder.
2. In the left sidebar, click JSON, then enter the following JSON body, then click Submit:

```curl
{
  "messaging_product": "whatsapp",
  "pin": "123456"
}
```

1. You should receive a standard `success` response:

```curl
{
  "success": true
}
```

### Step 4. Test your messaging functionality

1. In the [Graph API Explorer tool](https://developers.facebook.com/tools/explorer/) , enter `/<YOUR_SANDBOX_TEST_PHONE_NUMBER_ID>/messages` in the endpoint builder.
2. In the left sidebar, click **JSON** , then enter the following JSON body, then click **Submit** :

```curl
{
  "messaging_product": "whatsapp",
  "to": "YOUR_NUMBER", // Replace this value with phone number of your device.
  "type": "template",
  "template": {
    "name": "hello_world",
    "language": { "code": "en_US" }
  }
}
```

1. You will receive a response with a `"message_status": "accepted"` value, and you should receive a text message on your device.

### Step 5. Configure webhooks and permissions

- Navigate to the [App Dashboard](https://developers.facebook.com/apps) .
- Click the app you are using with WhatsApp.
- Select **Use cases** (pencil icon) from the sidebar.
- Under **Connect with customers through WhatsApp** , click **Customize** .
- In the left sidebar, click **Configuration** .
- Under **Callback URL** , add the callback URL for your webhook server. If you do not have a webhook server, you can follow our [instructions to create a test webhook server](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/set-up-whatsapp-echo-bot).
- Under **Verify token** , add an arbitrary verification string.
- Click **Verify and save** .
- On the next page, in the **Select product** dropdown, click **WhatsApp Business Account** .
- Under **Webhook fields** , in the **calls** row, click the toggle button to subscribe to the `calls` webhook field.

### Finish: Enable calling features on your test phone number

1. In the [Graph API Explorer tool](https://developers.facebook.com/tools/explorer/) , enter `/<YOUR_SANDBOX_TEST_PHONE_NUMBER_ID>/settings` in the endpoint builder.
2. In the left sidebar, click **JSON** , then enter the following JSON body, then click **Submit** :

```curl
{
  "calling": {
    "status": "ENABLED",
    "call_icon_visibility": "DEFAULT",
    "callback_permission_status": "ENABLED"
  }
}
```

1. You should receive a standard `success` response:

```curl
{
  "success": true
}
```

1. Finally, under **Access Token** , copy the access token down for future use. **Note: Retain this access token as you will use it to make API calls for testing your Calling API integration.**

## Test business-initiated calling

Before you can test business-initiated calls (BIC), you must provide user calling permissions to your sandbox account.

You can do this on the client device you are using for testing:

1. On your client device, open WhatsApp.
2. Navigate to the message thread you have with your sandbox business phone number.
3. At the top of the screen, tap the sandbox business phone number.
4. Scroll down and tap **Business Calling Permission** .
5. Tap **Allow calls** .

You can now use your Calling API integration to call the client device and test your integration.

[Learn more about how to make business-initiated calls.](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/business-initiated-calls)

## Test user-initiated calling

You can test user-initiated calls (UIC) on the client device you are using for testing:

1. On your client device, open WhatsApp.
2. Navigate to the message thread you have with your sandbox business phone number.
3. Tap the phone icon at the top of the screen to call the sandbox business phone number.
4. Confirm a successful call connection.

[Learn more about how to handle user-initiated calls.](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/user-initiated-calls)
