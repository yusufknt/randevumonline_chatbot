# App States - App Development with Meta

_Source: https://developers.facebook.com/docs/development/create-an-app/app-dashboard/app-states_

---

# App States

Meta apps can have various states, which are indicative of an app's activity or inactivity and can affect their ability to access and use our products and APIs. App states are different from [app modes](https://developers.facebook.com/docs/development/build-and-test/app-modes), which control who is able to access and use an app.

## Active

All newly created Meta apps start out in the **Active** state. Active apps can be used by app uses who are able to [access](https://developers.facebook.com/docs/development/build-and-test/app-modes) the app, can be loaded in the App Dashboard, can add and configure our products, and make calls to our APIs.

You can see all of the active apps that you have an [app role](https://developers.facebook.com/docs/development/build-and-test/app-roles) on by going to the [Apps](https://developers.facebook.com/apps) panel and filtering by **All Apps**. They also appear in the App Dashboard's [app selection dropdown menu](https://developers.facebook.com/docs/development/create-an-app/app-dashboard#app-selection-dropdown).

## Inactive

Apps that meet the following criteria may be placed in the **Inactive** state:

- Zero app users have logged into the app in the last 90 days
- The app has made no calls to any of our APIs in the last 90 days
- The app has received no webhook notifications in the last 90 days

Once an app has been placed in the Inactive state:

- All access tokens associated with the app will be invalidated
- The app will be prevented from accessing our APIs until access is restored

You can see all of the inactive apps that you have an [app role](https://developers.facebook.com/docs/development/build-and-test/app-roles) on by going to the Apps panel and filtering by **All Apps**. They also appear in the App Dashboard's [app selection dropdown menu](https://developers.facebook.com/docs/development/create-an-app/app-dashboard#app-selection-dropdown).

### Restoring Access

Administrators who load the app in the App Dashboard will be given the option to restore access. Restoring an app will:

- Automatically upgrade the app to the latest versions of the various APIs
- Re-enable webhooks notifications and upgrade them to the latest version

New access tokens must be generated. Also, any permissions that were removed from the app due to disuse while it was inactive must be re-approved through the [App Review](https://developers.facebook.com/docs/resp-plat-initiatives/app-review) process.

## Archived

Apps that have been archived by an app administrator will be in the **Archived** state. Once an app has been archived:

- Calls made by the app to any of our APIs will fail
- Webhooks will be deactivated
- App users will be unable to log into the app via Facebook Login for Business or Business Login for Instagram
- It will no longer appear in the [Apps](https://developers.facebook.com/apps) panel when filtering by **All Apps**
- [Developer notifications](https://developers.facebook.com/docs/development/create-an-app/developer-settings) for the app will be deactivated

Permissions granted to the app by app users, and access tokens associated with the app, will not be invalidated, and any [approved](https://developers.facebook.com/docs/resp-plat-initiatives/app-review) permissions and features will still be approved. However, archived apps are still subject to [inactivity](#inactive).

### Archiving Apps

To archive an app that you own, go to the [Apps](https://developers.facebook.com/apps) panel, click the app's **•••** icon, and select **Archive App**.

### Restoring Archived Apps

Any app administrator can restore an archived app by going to the [Apps](https://developers.facebook.com/apps) panel, filtering by **Archived**, clicking the app's **•••** icon, and selecting **Restore app**.

## Restricted

Apps that have been enforced upon for terms or policy violations will be in the **Restricted** state. To learn more about app enforcement and its impact on apps, and how to appeal an enforcement decision, refer to our [Enforcement](https://developers.facebook.com/docs/development/terms-and-policies/enforcement) document.

## Removed

Apps that have been [removed](https://developers.facebook.com/docs/development/create-an-app/app-dashboard/advanced-settings#remove-app) by an app administrator will be in the **Removed** state. Once an app has been removed:

- It cannot be used by anyone, including users with roles on the app
- It will be hidden from the App Center
- It will no longer appear in the [Apps](https://developers.facebook.com/apps) panel
- It cannot be loaded in the App Dashboard by anyone, including app admins
- Webhooks will be deactivated
- All access tokens associated with the app will be invalidated
- All [test apps](https://developers.facebook.com/docs/development/build-and-test/test-apps) will be removed.

Alternatively, you may wish to [archive](#archived) your app or set it to [Development](https://developers.facebook.com/docs/development/build-and-test/app-modes#development-mode) mode.

### Removing Apps

To remove an app that you own, go to the [Apps](https://developers.facebook.com/apps) panel, click the app's **•••** icon, and select **Remove App**. You can also remove an app by clicking the **Remove App** button in the **App Dashboard** > **Settings** > **Advanced** panel.

### Restoring Removed Apps

If you wish to restore an app that has been removed, you may file an [appeal](https://developers.facebook.com/appeal) (Make sure you are logged in to your Meta Developer account before clicking on this appeal URL). If the appeal is accepted, the app will return to an active state.
