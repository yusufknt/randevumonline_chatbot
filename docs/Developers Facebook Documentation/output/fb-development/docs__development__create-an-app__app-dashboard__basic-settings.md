# Basic Settings - App Development with Meta

_Source: https://developers.facebook.com/docs/development/create-an-app/app-dashboard/basic-settings_

---

# Basic Settings

The Basic settings page gives you one place to configure important settings, like your apps' name, contact email, and category, and find the app secret assigned to your app by Meta. The settings listed in this document are needed for you to build an app on the Meta Platform.

## General Settings

General settings contains unique identifiers assigned to your app and allows you to provide additional information to further define and describe your app. These identifiers allows us to identify your app when it makes API calls, and helps us determine which permissions and features your app has been granted by app users, and are used to generate access tokens.

### App ID

When you create a Facebook app we generate and assign it a unique ID. This ID must be included when making any calls to our APIs. All of our SDKs provide a way for you to easily set this value in your codebase so that will automatically be included with any API calls.

### App Secret

Your app secret is used in some of the [Facebook Login](https://developers.facebook.com/docs/facebook-login) flows to generate an [App access token](https://developers.facebook.com/docs/facebook-login/access-tokens/#apptokens) which can make API requests on behalf of any user of the app. It is extremely important that an App Secret be stored securely and not be included in any code that could be accessed by anyone other than a developer of the app.

We recommend that App access tokens only be used directly from your app's servers in order to provide the best security. For native apps, we suggest that the app communicates with your own server and the server then makes the API requests to Facebook using the App access token.

#### Resetting App Secret

If your App Secret is compromised, you should reset it immediately in the [Basic Settings of your App Dashboard](https://developers.facebook.com/apps/). It is not possible to programmatically rotate the app secret.

If Meta discovers the app secret has been leaked and user data is at risk, Meta will notify you to reset the app secret immediately. If you do not reply in a timely manner, Meta will reset the app secret. This will cause all the business integrations to stop working as user data grants for the app will be revoked. This is a very disruptive process which will only happen if there is a risk to user data and you do not reset the app secret quickly.

### Display Name

The display name is the user facing name of your app that will be displayed in the [App Center](https://developers.facebook.com/docs/games/listing/). This field is required to switch your app to Live mode.

#### Display Name Guidelines

Follow these guidelines when choosing or modifying your app's display name, otherwise it will be rejected during [App Review](https://developers.facebook.com/docs/app-review).

- Do not use names that include Facebook or FB, or any names of Facebook products such as Oculus, WhatsApp, or Instagram.
- Do not use "F", "Book", or "Face" in your name if it could be perceived as a reference to Facebook.
- Do not use [our brands](https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.facebookbrand.com%2Ftrademarks&h=AUBU7RTQnVPUJnDsmJhEzvuWrakxd_QVlgvNdohEtLRymhWW2PyzuAX2bepunoVntR1KWO5mR7VIu7GdTsr-akW3469plB4D3ItQxliue1-GeXrcbJMT9dg_e1Im8XUdEM4O5IxQ9iAZHA) in a way that implies partnership, sponsorship, or endorsement by us.
- Do not combine any part of [our brands](https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.facebookbrand.com%2Ftrademarks&h=AUBrXejzUiKUGWzzSF_ztWbHMY6SPq6TponMPQlLf1TpYNAZtAy-PpHZyrgaOCpbgHUH7LxzAFMwevDnjQDLlpCal4_Tbu65mMW6AGfFnah-PsFemw8fRhDwi1HoyyMDTrFsJYZXhDBEjA) with your name.
- Do not use names or logos that imitate or could be confused with [our brands](https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.facebookbrand.com%2Ftrademarks&h=AUDYggMAJn0iqRELILM4dA_k-sdtcsb_wpuJk14eHfCYIhqleBqhybldv9TEflruM0jFMMNeeeZIRenYcCp3dc_1ws0UHxG2bM5MfERSRBuqqixtOzM_MHGAximKa9kJwLsCfZidJ3JlWQ)
- Do not present our brand assets in a way that make them the most distinctive or prominent feature of your app.

### Namespace

The namespace URL links to your app's Canvas page. The Canvas page is used to tell user about your app.

### App Domains

Domains and subdomains of your app for app installation and are used during Graph API request for verification.

### Contact Email

The contact email is the email address where [developer notifications](https://developers.facebook.com/docs/development/create-an-app/developer-settings) will be sent. These notifications will also surface in the Alerts in the App Dashboard. This field is required to switch your app to Live mode.

### Privacy Policy URL

The Privacy Policy URL links to your app's privacy policy that applies to your app users.

### Terms of Service URL

The Terms of Service URL links to the Terms of Service for your app that applies to your app users. This field is required to switch your app to Live mode.

### User Data Deletion

The User Data Delection URL links to explicit instructions for your app users on how to delete their data from your app. This URL may be the relevant section in the application's Privacy Policy.

The data deletion URL is called when users remove your app by way of the Facebook's Apps and Website settings page, and then in the Removed section, click your app and request that their data be deleted.

Learn more about [data deletion](https://developers.facebook.com/docs/development/create-an-app/app-dashboard/data-deletion-callback).

### App Icon

The App Icon represents your app in the App Center. This field is required to switch your app to Live mode.

#### App Icon Guidelines

Follow these guidelines when uploading or replacing your app icon, otherwise it will be rejected during [App Review](https://developers.facebook.com/docs/app-review).

- Do not use or incorporate any of our logos, trademarks, icons, or any modified forms or variations of them. This includes logos, trademarks, and icons for any of our products, such as Facebook, Instagram, Oculus, or WhatsApp.
- Do not include "Facebook" or "FB".

### Category

Your app’s [category](https://developers.facebook.com/docs/development/create-an-app/app-dashboard/app-categories) helps users discover new apps based on their search. This field is required to switch your app to Live mode.

### App Purpose

Your app's purpose is used during App Review to tell us how your app will access and use your data or data of others. This field is required to switch your app to Live mode.

## Business Verification

Business Verification is a process that allows Facebook to verify your identity as a business entity. This is required io access data that is not owned by you. While verification is not required to Go Live, you will not be able to access data you do not own until verification is complete.

Learn more about [Business Verification](https://developers.facebook.com/docs/development/release/business-verification).

### Verification Status

After you have submitted for verification, your status will be Pending then Verified once Meta has verified your Business information.

## Data Protection Officer Contact Information

The General Data Protection Regulation (GDPR) requires certain companies that serve individuals in the European Union to designate and publish contact information for a Data Protection Officer (DPO) who can assist with matters related to the processing of personal information. This information will be made available in your apps and website settings so that your app users can contact your DPO if they have questions about how their data is processed and used.
