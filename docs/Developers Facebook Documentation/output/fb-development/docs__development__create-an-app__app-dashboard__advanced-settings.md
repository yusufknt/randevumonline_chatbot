# Advanced Settings - App Development with Meta

_Source: https://developers.facebook.com/docs/development/create-an-app/app-dashboard/advanced-settings_

---

# Advanced Settings

Advanced settings allow you to add a layer of security to your API calls, create a Page for your app, link a Business Manager and Ad Account to your app, control redirect sharing, or remove your app.

## Native or Desktop App

This toggle is used to validate API requests for native or desktop apps since app access tokens are considered insecure due to the app secret being embedded in the code creating an insecure app access token.

### Is App Secret Embedded In the Client

If the **Native or Desktop App** toggle is set to **Yes**, then you will need to set this field. This restricts the app secret usage to methods allowed by a [Client access token](https://developers.facebook.com/docs/facebook-login/access-tokens/#clienttokens).

## API Version Settings

The **API Version Settings** allow you to upgrade or set the [Graph API](https://developers.facebook.com/docs/graph-api) or [Marketing API](https://developers.facebook.com/docs/marketing-apis) default version your app uses for [un-versioned](https://developers.facebook.com/docs/apps/versions#unversioned_calls) API calls.

Learn more about [API versioning](https://developers.facebook.com/docs/apps/versions).

### Upgrade All Calls

The **Upgrade All Call**s setting allows you to specify the API version your app calls for all users of your app.

### Upgrade Calls for App Roles

The **Upgrade All Calls for App Roles** setting allows you to specify the API version your app calls for your developers. This allows you to test upgraded versions on developers before rolling out to the public.

## App Restrictions Settings

The **App Restrictions** settings allow you to specify who can use your app.

#### Use App Restrictions to Soft Launch

Consider soft launching your app in a few specific countries or specific age groups before releasing it to the world. By using this feature you can test how your app performs against a limited set of users in a specific location, allowing you to test and tweak your app before your full launch.

### References Alcohol

The **Reference Alcohol** settings restricts your app by age in some locations.

### Age Restriction

The **Age Restriction** settings prevents your app from being used by Facebook Users who don't meet the selected age criteria.

#### GDPR Restricted

If your app is available in European Union countries, they may have more strict age restriction requirements that differ from your global age restriction settings. You will be able to set **GDPR Restricted** and select the age restriction from the **GDPR Restriction** drop-down. **Note:** It must be a lower age than the selected global age.

### Social Discovery

The **Social Discovery** settings controls the publishing of app usage stories in the Facebook Ticker or Newsfeed. Selecting **No** will prevent app usage stories from appearing in News Feeds.

### Country Restricted

The **Country Restricted** setting allows you to restrict usage depending on the country of the user. Selecting **Yes** enables country-based app restrictions, which triggers additional settings to define these restrictions.

#### Allowed Countries

When **Country Restricted** is set to **Yes**, the **Allowed Countries** setting allows you to select the countries of users that are allowed to use your app. If no countries have been added to this list, your app will be available worldwide.

#### Use without location

When **Country Restricted** is set to **Yes**, the **Use Without Location** setting allows your app to be used by Facebook users whose location cannot be determined.

## Security Settings

The [Security](https://developers.facebook.com/docs/facebook-login/security) Settings found in the App Dashboard allow you to keep your app and its data as secure as possible.

### Server IP Allow List

List IP addresses that are allowed to use your app secret to keep API calls more secure.

### Update Settings IP Allow List

List IP addresses that are allowed to change the app's settings via the Graph API or any Facebook apps, including the App Dashboard itself.

### Update Notification Email

A notification will be sent to this email address whenever any app settings are changed using the App Dashboard. This can alert you to any unauthorized changes to your app settings.

### Client Token

The [client token](https://developers.facebook.com/docs/facebook-login/access-tokens/#clienttokens) is an identifier that you can embed into native mobile binaries or desktop apps to identify your app.

### Require App Secret

Require [App Secret](https://developers.facebook.com/docs/facebook-login/security#appsecret) or [App Secret Proof](https://developers.facebook.com/docs/facebook-login/security#proof) for API calls with access tokens used ouside of trusted contexts.

### Require 2-Factor Reauthorization

Set **Require 2-Factor Reauthorization** to **Yes** to require 2-Factor authorization to change app settings through API calls.

### Allow API Access to App Settings

Set **Allow API Access to App Settings** to **Yes** to allow your app's settings to be changed programmatically through API calls.

## Domain Manager

Add your domains to set options for [prefetching data](https://www.facebook.com/business/help/1514372351922333/) from your URLs. You can also use this to opt out of prefetching.

## App Page

Create a Facebook Page associated with your app. Your app's name must be in the Page's name and the Page's category must be set to **App Page**.

## Business Manager

Associate your app with a Business to use the [Business Mapping API](https://developers.facebook.com/docs/business-manager-api) to manage your app.

## Advertising Accounts Settings

### Authorized Ad Account IDs

Add Facebook Ad Accounts to advertise your app on Facebook.

## Share Redirect Settings

### Allow Cross Domain Share Redirects

Allow shares that redirect to your URLs from cross domain URLs.

#### Share Redirect Domain Allow List

If Allow Cross Domain Share Redirects is set to **No**, you can add the domains that are allowed redirect to your URLs when shared.

## Remove App

Allows an app administrator to [remove](https://developers.facebook.com/docs/development/create-an-app/app-dashboard/app-states#removed) the app.
