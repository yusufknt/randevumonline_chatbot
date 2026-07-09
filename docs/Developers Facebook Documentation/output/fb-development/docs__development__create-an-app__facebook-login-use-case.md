# Facebook Login Use Case - App Development with Meta

_Source: https://developers.facebook.com/docs/development/create-an-app/facebook-login-use-case_

---

# Customize the Authenticate and request data from users with Facebook Login Use Case

This document shows you how to customize the **Facebook Login Use Case** use case you added to your app during the [app creation process](https://developers.facebook.com/docs/development/create-an-app/).

## Customize use cases

### Permissions and features

1. If you are not already on the **Use cases** page of the dashboard, click **Use cases**, or pencil icon, in the left-side menu.
2. Click on a use case to view the permissions and features that are available, both required and optional, for that use case.
3. Click the **Add** button to the right of each permission or feature you'd like to add. If, during development, you find that your app doesn't use the permission or feature, you can return here and remove it.
4. Additional actions are available for certain permissions and features.
   - To request a higher rate limit for the Ads Management Standard Access feature, click the **Actions** button and select **Request higher limit**.
     - If you are ready to submit your app for App Review, continue to the [App Review section](https://developers.facebook.com/docs/app-review). If not, click **Use cases**, or pencil icon, in the left-side menu to continue to customize your use cases.
   - To increase access for the `public_profile` permission, allow your app to serve user who don't have a role on your app or the business connected to your app, click the **Increase access** button.
   - If, during development, you find that your app doesn't need a higher rate limir or increased access to `public_profile`, you can return here and remove it.

| Use Case Feature or Permission | Allowed Actions |
| --- | --- |
| [`email`](https://developers.facebook.com/docs/permissions#email) | Optional for all use cases. |
| [`public_profile`](https://developers.facebook.com/docs/permissions#public_profile) | **Required for all use cases**. |

#### Settings

Facebook Login allows you to control oAuth settings, and add a deauthorization callback URL and redirect URI validator.

#### Quickstart

The Facebook Login quickstart allows you to quickly get the code to implement Facebook Login into your app.

After you add a permission to your app, you can see the status for that permission:

- Ready for live mode – This permission has been approved in App Review and you can publish your app
- Ready for testing – You can test API calls to endpoints that require this permission and complete App Review permission testing requirements
- Verification required – This permission requires a verified Meta Business Account added to the app

You can also see the number of successful API calls you have made to endpoints that require each permission.

## Add more use cases

Click the **Go back** button in the upper right or **Use cases** in the left side menu to add more use cases to your app.

These are the use cases most commonly used with the use case you chose when you created this app.

| Use case | Available permissions to add and code to implement |
| --- | --- |
| **Use additional Facebook user data for personalization** – Choose data permissions to personalize the app experience for users logging in with their Facebook account.   **Only add permissions that your app will use.**   All of these permissions require App Review before you can publish your app and go live. | `user_age_range` `user_birthday` `user_friends` `user_gender` `user_hometown` `user_likes` `user_link` `user_location` `user_photos` `user_posts` `user_videos` |
| **Track engagement with App Events** – Meta App Events allows your app to understand how people engage with your business across, devices, platforms and websites. | [Meta App Events](https://developers.facebook.com/docs/app-events/overview/) |
| **Get real-time notifications with Webhooks** – Get automatic HTML notifications when app users make changes related to the permissions that you've added to your app. | [Meta Webhooks](https://developers.facebook.com/docs/graph-api/webhooks/) |

## Next Steps

Now that you have successfully customized your Facebook Login use case, let's [update the settings for your app](https://developers.facebook.com/docs/development/create-an-app/app-dashboard/basic-settings) on the app Dashboard.

## See Also

To learn more about the concepts, endpoints, and permissions mentioned in this document, please visit the following guides:

- [Facebook Login Overview](https://developers.facebook.com/docs/facebook-login)
- [Meta App Events Overview](https://developers.facebook.com/docs/app-events/overview/)
- [Meta Webhooks Overview](https://developers.facebook.com/docs/graph-api/webhooks/)
- [Permissions Reference](https://developers.facebook.com/docs/permissions)
