# Measurement Partners | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/measurement-partners_

---

# Measurement Partners

Updated: Dec 12, 2025

A Measurement Partner is a third-party company that helps businesses measure the effectiveness of their marketing campaigns on our platform.

Measurement Partners gain read-only access to WhatsApp Business Account (WABA) analytics data and webhooks. Specifically, they can view phone numbers, message templates, and incoming messages, and can access WABA analytics data.

For a business to share their analytics data with a Measurement Partner, they must already have a WABA. Measurement Partners cannot create WABAs or send messages on behalf of their clients.

## Onboarding flow overview

Follow these steps to onboard as a Measurement Partner:

1. [Complete Tech Provider onboarding.](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/get-started-for-tech-providers)
2. Create your Facebook Login Button using the Measurement Partner ES template instructions below
3. Embed the Facebook Login Button on your website

## How to create Facebook Login button using the Measurement Partner ES template

Follow the steps below to create your Facebook Login button that will show the Measurement Partner ES flow to your customers.

## Step 1: Load the Facebook JavaScript SDK

See [Basic Setup](https://developers.facebook.com/docs/javascript/quickstart#loading) for instructions on loading the basic version of the Facebook JavaScript SDK with the options set to their most common defaults.

The `fbAsyncInit` function must be attached to the `window` object before the line of code loading the JavaScript SDK as the SDK calls this function to set up the Facebook Login information.

This setup uses the following parameters:

- `appId` — The Meta app ID
- `cookie` — Enables cookies to allow the server to access this session
- `xfbml` — Parses social plugins on the page
- `version` — The Graph API version to use

Example

```js
<script>
  window.fbAsyncInit = function () {
    // JavaScript SDK configuration and setup
    FB.init({
      appId:    '<i>facebook-app-id</i>', // Meta App ID
      cookie:   true, // enable cookies
      xfbml:    true, // parse social plugins on this page
      version:  'v25.0' //Graph API version
    });
  };
</script>
```

## Step 2: Create Facebook Login for Business Configuration

### Prerequisites

- You should have created an app in the App Dashboard on [https://developers.facebook.com/](https://developers.facebook.com/)
- Add the **[Facebook Login for Business](https://developers.facebook.com/documentation/facebook-login/facebook-login-for-business)** product to your app
- Follow [best practices](https://developers.facebook.com/documentation/facebook-login/security#enablejssdk) on how to set up **Client OAuth settings** , specifically settings like *Valid OAuth Redirect URIs* and *Allowed Domains for the JavaScript SDK*

### Process

1. In the **App Dashboard** , under **Facebook Login for Business** , click **Templates**
2. Click the **Use template** button for the **WhatsApp Measurement Partner** template.
3. Since all the template configuration details have been set, simply click **Create from template**
4. Copy and retain the **Configuration ID** and set this value in the Facebook Login Button script in the next step.

## Step 3: Set up Facebook Login

[Facebook Login](https://developers.facebook.com/documentation/facebook-login) allows you to place a button on your website or portal to initiate a connection to Facebook. Businesses can use this login flow to associate their Facebook profiles with their business presence (i.e., Business Manager) in order to streamline onboarding.

The Facebook Login button should be implemented in a location of your choice (platform portal, landing page, etc.) using the instructions below to trigger the Embedded Signup oAuth flow.

After loading the JavaScript SDK and initializing it with the proper information, set up the `FB.login()` function to trigger the Embedded Signup flow.

Make sure the following are included:

- The `response` callback function
- The `config_id` parameter
- The `extras` object with: The `setup` parameter for any [prefilled form data](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/pre-filled-data)

Example

```js
<script>
  window.fbAsyncInit = function () {
    // JavaScript SDK configuration and setup
    FB.init({
      appId:    '<i>your-facebook-app-id</i>', // Facebook App ID
      cookie:   true, // enable cookies
      xfbml:    true, // parse social plugins on this page
      version:  'v25.0' //Graph API version
    });
  };

  // Load the JavaScript SDK asynchronously
  (function (d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "https://connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
  }(document, 'script', 'facebook-jssdk'));

  // Facebook Login with JavaScript SDK
  function launchWhatsAppSignup() {
    // Conversion tracking code
    fbq && fbq('trackCustom', 'WhatsAppOnboardingStart', {appId: '<i>your-facebook-app-id</i>', feature: 'whatsapp_embedded_signup'});

    // Launch Facebook login
    FB.login(function (response) {
      if (response.authResponse) {
        const code = response.authResponse.code;
        // The returned code must be transmitted to your backend,
  // which will perform a server-to-server call from there to our servers for an access token
      } else {
        console.log('User cancelled login or did not fully authorize.');
      }
    }, {
      config_id: '<CONFIG_ID>', // configuration ID goes here
      response_type: 'code',    // must be set to 'code' for System User access token
      override_default_response_type: true, // when true, any response types passed in the "response_type" will take precedence over the default types
      extras: {
        setup: {
          ... // Prefilled data can go here
        }
      }
    });
  }
</script>
```

## Step 4: Create a login button

Create a button or link on your website to launch the Embedded Signup flow. Use the `onClick` function to call the `launchWhatsAppSignup()` function set up in Step 3 above.

Example

```js
<button onclick="launchWhatsAppSignup()" style="background-color: #1877f2; border: 0; border-radius: 4px; color: #fff; cursor: pointer; font-family: Helvetica, Arial, sans-serif; font-size: 16px; font-weight: bold; height: 40px; padding: 0 24px;">Login with Facebook</button>
```

## Embed your new Facebook Login button

Copy the button code to the desired location on your site.

## Testing the Embedded Signup flow for Measurement Partners

1. On the sidebar under **WhatsApp** , click **ES Integrations** and then scroll down to **Embedded sign-up launch** .
2. Under **Embedded sign-up dialog** , choose your Measurement Partner config and click **Login with Facebook** .
3. Follow the prompts to test the sign-up flow.
