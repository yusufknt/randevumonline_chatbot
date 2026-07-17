# Multi-Partner Solution — Embedded creation | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/multi-partner-solution-embedded-creation_

---

# Multi-Partner Solution — Embedded creation

Updated: Dec 12, 2025

[Multi-Partner Solutions](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/multi-partner-solutions) (MPS) allow Solution Partners and Tech Providers to jointly manage customer WhatsApp assets in order to provide WhatsApp messaging services to customers.

If you are a Solution Partner, instead of using the app dashboard to create an MPS, you can create one using a snippet of JavaScript and an HTML button which you can embed somewhere on your website. Tech Providers who want to partner with you can use the button to grant your app permission to manage solutions for one or more of their apps, which you can then do using a series of API requests.

## Flow

Tech Providers who visit your website and click the embedded solution creation button will be asked to authenticate, and after doing so, will be presented with an interface that allows them to choose an existing app:

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/458542138_1146317889773905_7397800002017796139_n.png?_nc_cat=101&ccb=1-7&_nc_sid=e280be&_nc_ohc=sJdvsqVMGDIQ7kNvwFttXDl&_nc_oc=AdozMOdRBhYspodc4hxTZiFsiJA7NSTKDW_6Q-qnngYXVSVNz7VfqDFWFdLrxHpKLyI&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=8Plxlcew-a30jiOivLi6kg&_nc_ss=7b20f&oh=00_Af7LJB_taHuFweFbBlF1PRI8Nrwvhw9W2eABYDlUeLXWZQ&oe=6A1C1BFC)

After choosing an app, they can review and confirm that they will be granting your app permission to manage their app’s Multi-Partner Solutions.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/458977093_1267404221307200_5854548995664421217_n.png?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=txMzrhlU0zYQ7kNvwHr9NPI&_nc_oc=AdquVo13c-R7_c5cIZt15QNdZp5P5ZS15929fpSh99lBAHFbslbVuRF-AzS8EMFWewU&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=8Plxlcew-a30jiOivLi6kg&_nc_ss=7b20f&oh=00_Af5y17vH6VAT_BctPmlD-OEL3iZcY-hgo-1dsmGgDFd4Fg&oe=6A1C2FEB)

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/458647670_1843654972790451_9197042182528031487_n.png?_nc_cat=111&ccb=1-7&_nc_sid=e280be&_nc_ohc=QYK6kTeg7yMQ7kNvwGB8ETn&_nc_oc=AdotyuTNSCejYtLqldFxPLt8ASYBUNynltvWLNKOS70E4AGyr-EFaiu33-AlFZ570J0&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=8Plxlcew-a30jiOivLi6kg&_nc_ss=7b20f&oh=00_Af6bJaxyhrbygY4PdaMWjDhauj8ALIPL_jf5AurpdLfDYA&oe=6A1C02BB)

Once the Tech Provider dismisses the interface, a user access token will be generated and returned to flow, where you can capture it. You can then use the token in a series of API calls to get Tech Provider’s chosen app ID(s) and create and accept a solution.

## Requirements

- Facebook Login for Business must be [configured on your app](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/implementation#step-2--create-a-facebook-login-for-business-configuration) , with **Valid OAuth Redirect URIs** and **Allowed Domains for the JavasScript SDK** set. You should already have set these values when configuring Embedded Signup.
- Your app must undergo App Review and be approved for advanced access for the **manage_app_solution** permission.

## Embedded creation button

### Step 1: Grant permission to app

Access the Meta Business Suite and use your system user to grant your app the **manage_app_solution** permission.

1. Log into [business.facebook.com](https://business.facebook.com) .
2. Use the business portfolio dropdown menu on the left to locate your business portfolio and click the gear icon (for settings).
3. Navigate to **Users** > **System Users** .
4. Click the system user who has business asset access on your app and WhatsApp Business Account.
5. Click the **Generate token** button.
6. Select your app.
7. Set an expiration date for the token.
8. Select the **manage_app_solution** permission.
9. Generate a token.

Use this token when accepting any Multi-Partner Solutions you create for your partners (see below).

### Step 2: Add embedded button code

Add the following code to your website or portal, or wherever you plan on directing Tech Providers who will be working with you as part of an MPS. Be sure to replace `<SOLUTION_PARTNER_APP_ID>` with your app ID.

```https
<!-- Load JavaScript SDK asynchronously -->
<script async defer crossorigin="anonymous" src="https://connect.facebook.net/en_US/sdk.js"></script>

<script>
  // Configure JavaScript SDK
  window.fbAsyncInit = function() {
    FB.init({
      appId: "<SOLUTION_PARTNER_APP_ID>", // Replace with your app ID
      cookie: true,
      xfbml: true,
      version: "v20.0"
    });
  };

  // Launch MPS creation flow
  function launchSolutionCreationFlow() {
    FB.login(
      function (response) {
        if (response.authResponse) {
          const accessToken = response.authResponse.accessToken;
          console.log(accessToken); // Replace with your code that captures access token
        } else {
          console.log("User failed to authorize"); // Replace with your code that logs auth failure
        }
      },
      {
        scope: "manage_app_solution"
      }
    );
  }
</script>

<button onclick="launchSolutionCreationFlow()" style="background-color: #1877f2; border: 0; border-radius: 4px; color: #fff; cursor: pointer; font-family: Helvetica, Arial, sans-serif; font-size: 16px; font-weight: bold; height: 40px; padding: 0 24px;">Launch Solution Creation</button>
```

Direct prospective Tech Provider partners to this location and instruct them to complete the flow. Let them know that completing the flow does not create the solution (it requires some API calls on your part) and that you’ll provide them with the solution ID once it has been created.

## Solution creation

### Step 1: Capture user token

Anytime a Tech Provider uses the embedded solution creation button and completes the flow, the flow returns an `authResponse` object (`response.authResponse`) that has an `accessToken` property:

```json
{
  status: "connected",
  authResponse: {
    accessToken: "<USER_ACCESS_TOKEN>",
    expiresIn:"<TOKEN_EXPIRATION_TIMESTAMP>",
    reauthorize_required_in:"<SECONDS_UNTIL_REAUTH_REQUIRED>",
    signedRequest:"<SIGNED_PARAMETER>",
    userID:"<USER_ID>"
  }
}
```

Capture the `accessToken` property value. This is the Tech Provider’s user access token, which you will need next.

### Step 2: Get app details

Use the Tech Provider’s user access token and the [Assigned Applications API](https://developers.facebook.com/docs/graph-api/reference/user/assigned_applications) to get a list of app IDs that the Tech Provider selected when they completed the flow.

Example request

```curl
curl 'https://graph.facebook.com/v20.0/me/application_details' \
-H 'Authorization: Bearer EAAJB'
```

Example response

Example response of a Tech Provider who selected a single app in the flow.

```json
{
  "data": [
    {
      "link": "www.mediamonsoon.com",
      "name": "media_monsoon_prod",
      "id": "634974688087057"
    }
  ]
}
```

Each object in the response describes an app the Tech Provider selected when completing the flow. Capture the `id` property value of each app for the next step.

### Step 3: Create a solution for Tech Provider

Use the Tech Provider’s access token and an app ID from the previous step to make a request to the [Solution Creation API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/application/solution-creation-api#post-version-application-id-whatsapp-business-solution).

Repeat this request for each app ID returned in the previous step.

Request Syntax

```https
POST /<APP_ID>/whatsapp_business_solution
```

```json
{
  "owner_permissions": ["MESSAGING"],
  "partner_app_id": "<SOLUTION_PARTNER_APP_ID>",
  "partner_permissions": ["MESSAGING"],
  "solution_name": "<SOLUTION_NAME>"
}
```

- `<SOLUTION_PARTNER_APP_ID>` — Your app ID.
- `<SOLUTION_NAME>` — Name to give the solution. This name will appear in the App Dashboard for both you and the Tech Provider, so the name should be unique and distinguishable from other solutions you or the Tech Provider may later initiate or accept.

Response

Upon success, the API will create a solution and associate your app and the Tech Provider’s app to it.

```json
{
  "solution_id": "<SOLUTION_ID>"
}
```

Capture the `solution_id` value. This is the solution ID, which you will need in the next step.

### Step 4: Accept the solution

Use your system user access token from the [Grant Permission to App](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/multi-partner-solution-embedded-creation#step-1-grant-permission-to-app) step and the solution ID to make a request to the [Solution Accept API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-solution/solution-accept-api#post-version-solution-id-accept) for any solutions you have created for Tech Providers.

Example request

```curl
curl -X POST 'https://graph.facebook.com/v20.0/795033096057724/accept' \
-H 'Authorization: Bearer EAAAT...
```

Example response

Upon success:

```json
{
  "success": true
}
```

Once you have accepted the solution, inform the Tech Partner that the solution has been created successfully, and provide them with any solution IDs you have created and accepted.
