# Access Levels - App Development with Meta

_Source: https://developers.facebook.com/docs/graph-api/overview/access-levels_

---

# Access Levels

This document is only applicable to apps created using an App Type.

**[Advanced Access](https://developers.facebook.com/docs/graph-api/overview/access-levels/#advanced-access) now requires Business Verification**

As of February 1, 2023 apps requesting [advanced access](https://developers.facebook.com/docs/graph-api/overview/access-levels/#advanced-access) for permissions may have to be connected to a verified business. [See this blog post for more information.](https://developers.facebook.com/blog/post/2023/02/01/developer-platform-requiring-business-verification-for-advanced-access/)

Access levels are an additional layer of Graph API authorization that apply to [permissions](https://developers.facebook.com/docs/permissions/reference) and [features](https://developers.facebook.com/docs/apps/features-reference) for [Business](https://developers.facebook.com/docs/development/create-an-app/app-dashboard/app-types#business), [Consumer](https://developers.facebook.com/docs/development/create-an-app/app-dashboard/app-types#consumer), and [Gaming](https://developers.facebook.com/docs/development/create-an-app/app-dashboard/app-types#gaming-services) apps.

![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/130946061_668701493796906_1998528720072373367_n.png?_nc_cat=106&ccb=1-7&_nc_sid=e280be&_nc_ohc=tkv005CdlJgQ7kNvwGbFp4F&_nc_oc=AdrYL2KQtGTXBYCo__1Cd-9WosZQd4yExmyie68Iv6wPJ3Cze4voAGqYpKsgvuNwcz4&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=55AfQtehpcrpwirBCo9oIw&_nc_ss=7b289&oh=00_Af4ScGMlQmS7borkiHgnlgPTOJGSBBGN6pXlSSNq5NRuXA&oe=6A1BEDE0)

There are two access levels: [Standard](#standard-access) and [Advanced](#advanced-access). Apps can request permissions with Advanced Access from any app user, and features with Advanced Access are active for all app users. Permissions with Standard Access, however, can only be requested from app users who have a role on the requesting app, and features with Standard Access are only active for app users who have a role on the app.

If your app will only be used by people who have a role on it, the permissions and features your app requires will only need Standard Access. If your app will be used by people who do not have a role on it, the permissions and features that your app requires will need Advanced Access.

All Business, Consumer, and Gaming apps are automatically approved for Standard Access for all permissions and features. Advanced Access, however, must be approved on an individual permission and feature basis through the [App Review](https://developers.facebook.com/docs/app-review) process.

## Standard Access

[Permissions](https://developers.facebook.com/docs/permissions/reference) with Standard Access can only be requested from app users who have a [role](https://developers.facebook.com/docs/development/build-and-test/app-roles) on the requesting app. Similarly, [features](https://developers.facebook.com/docs/apps/features-reference) with Standard Access are only active for app users who have a role on the app.

[Business](https://developers.facebook.com/docs/development/create-an-app/app-dashboard/app-types#business), [Consumer](https://developers.facebook.com/docs/development/create-an-app/app-dashboard/app-types#consumer), and [Gaming](https://developers.facebook.com/docs/development/create-an-app/app-dashboard/app-types#gaming-services) apps are automatically approved for Standard Access for all permissions and features available to their app type.

Standard Access is intended for apps that will only be used by people who have roles on them, or used during app development, when testing API endpoints that the calling app has not been approved for.

## Advanced Access

[Permissions](https://developers.facebook.com/docs/permissions/reference) with Advanced Access can be requested from any app user, and [features](https://developers.facebook.com/docs/apps/features-reference) with Advanced Access are active for all app users. However, [Business Verification](https://developers.facebook.com/docs/development/release/business-verification) is required to get Advanced Access. In some cases additional [App Review](https://developers.facebook.com/docs/app-review) on an individual permission and feature basis might be required.

### Automatic Approval

Business and Gaming apps created before February 16, 2021 were automatically approved for Advanced Access for the [email](https://developers.facebook.com/docs/permissions/reference/email) and [public\_profile](https://developers.facebook.com/docs/permissions/reference/public_profile) permissions, as well as any permissions or features that were already approved through App Review, if they were using them.

All newly created Consumer apps are automatically approved for Advanced Access for the email and public\_profile permissions. However, both permissions are set to Standard Access by default and must be manually switched to Advanced Access. In addition, consumer apps must be in Live mode before they can request permissions with Advanced Access from non-role app users, and before features with Advanced Access will be active for non-role users.

## Data Use Checkup

Apps that have Advanced Access for a permission or feature must complete [Data Use Checkup](https://developers.facebook.com/docs/development/maintaining-data-access/data-use-checkup/), which is an annual process to certify that the app accesses Facebook APIs, products, and data in compliance with our [Platform Terms](https://developers.facebook.com/terms) and [Developer Policies](https://developers.facebook.com/devpolicy).

## Remove Access

If you want to signify that your app does not need a specific permission or feature, you can remove it by clicking the trash can icon alongside the permission or feature in the **App Review** > **Permissions and Features** panel. You can restore access to a removed permission or feature by searching for it again in the same panel and clicking its **Get Standard Access** button or **Get Advanced Access** button. Restoring Advanced Access to previously approved permissions or features does not require re-review.

All permissions and features can be removed except for [public\_profile](https://developers.facebook.com/docs/permissions/reference/public_profile).

## Changing Access Levels

App administrators can change access levels for individual permissions and features. Restoring Advanced Access to permissions and features does not require [re-review](https://developers.facebook.com/docs/app-review), but changing from Advanced to Standard will invalidate/deactivate any permission/feature for any app users who do not have a role on your app.
