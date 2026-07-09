# Release - App Development with Meta

_Source: https://developers.facebook.com/docs/development/release_

---

# Publish

Once you have completed app [development and testing](https://developers.facebook.com/docs/development/build-and-test), you can publish your app. Publishing means to make your app available to accounts that do not have a [role](https://developers.facebook.com/docs/development/build-and-test/app-roles) on the app itself. This document lists the processes and app settings that may be required before you can publish your app successfully.

If your app will only be used by people who have a role on the app itself you do not need to complete any of these processes because your app is already available to these users.

If you have already published your app and want to add new functionality that requires App Review, follow the steps in our [App Review For Published Apps](https://developers.facebook.com/docs/app-review/introduction#app-review-for-live-apps) instructions.

## App Review

If your app will be used by anyone who does not have a role on it, it must undergo [App Review](https://developers.facebook.com/docs/app-review).

App Review is a process that allows you to request approval for specific API [permissions](https://developers.facebook.com/docs/permissions/reference) and [features](https://developers.facebook.com/docs/apps/features-reference) that your app needs to function properly. Only permissions approved through the App Review process can be granted to your app by app users without a role on the app, and only approved features will be active for those users.

App Review requires you to identify each of the permissions and features your app needs, describe why your app needs them, and show us how your app uses the data returned or accepted by our APIs.

Learn more about the [App Review](https://developers.facebook.com/docs/app-review) process.

## Business Verification

Business Verification is a process that allows us to verify your identity as a business entity. Apps that request advanced access for permissions and apps that allow other Businesses to access their own data must be connected to a Business that has completed [Business Verification](https://developers.facebook.com/docs/development/release/business-verification). Until then, app users from other Businesses will be unable to grant these apps permissions and all features will be inactive.

Learn more about [Business Verification](https://developers.facebook.com/docs/development/release/business-verification).

## Go live

To allow people, who do not have a role on your app, to use your app, you need to publish it. If your app requires App Review, App Review must be completed successfully before people can use your app.

### Use Case Apps

To publish your use case app go to the app dashboard **Publish > Go live** and click the **Go live** button in the bottom right corner.

### App Types

You must switch your app to [Live](https://developers.facebook.com/docs/development/build-and-test/app-modes) mode before it can request [App Review](https://developers.facebook.com/docs/app-review) approved permissions from app users who do not have a role on it, and before approved features will be active for those users. However, you should not switch to Live mode until all of the permissions and features that your app requires have been approved, and not before you have completed [Business Verification](https://developers.facebook.com/docs/development/release/business-verification) if required to do so. If you switch your app to Live mode prematurely, your app will be unable to request unapproved permission from app users, and any unapproved permissions will be inactive.

[Consumer](https://developers.facebook.com/docs/development/create-an-app/app-dashboard/app-types#consumer) apps behave a little differently because they also rely on [access levels](https://developers.facebook.com/docs/graph-api/overview/access-levels). Consumer apps in Live mode cannot request permissions with Standard Access from app users who do not have a [role](https://developers.facebook.com/docs/development/build-and-test/app-roles) on them, and features with Standard Access will be inactive for these users.

Business apps do not have app modes and rely exclusively on access levels.

### Releasing New Versions of Live Apps

If your app is already in published and you want to add new functionality that requires App Review, follow the steps in our [App Review For Live Apps](https://developers.facebook.com/docs/app-review/introduction#app-review-for-live-apps) instructions.

## Limited Release Using Geo-Restriction

If you want to release your app to a small set of users before making it available to everyone, you can configure app restrictions that only make your app available to users in certain age groups and geographic locations.

Learn more about [app restrictions](https://developers.facebook.com/docs/development/create-an-app/app-dashboard/advanced-settings#app-restrictions-settings).

## Learn More

- [App Roles](https://developers.facebook.com/docs/development/build-and-test/app-roles)
- [Claiming an App for your Business](https://developers.facebook.com/docs/marketing-api/business-asset-management/guides/apps)
- [Facebook Products](https://developers.facebook.com/products)
- [Businesses on Facebook](https://business.facebook.com/business/)
