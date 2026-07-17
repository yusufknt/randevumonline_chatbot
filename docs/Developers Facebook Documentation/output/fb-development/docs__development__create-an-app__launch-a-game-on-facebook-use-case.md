# Launch a game on Facebook Use Case - App Development with Meta

_Source: https://developers.facebook.com/docs/development/create-an-app/launch-a-game-on-facebook-use-case_

---

# Customize the Launch a Game on Facebook Use Case

This document shows you how to customize the **Launch a Game on Facebook** use case you added to your app during the [app creation process](https://developers.facebook.com/docs/development/create-an-app/).

## Use case customization

Under **Launch a game on Facebook** use case, you can see that the following have been added to your use case:

- **Facebook Login for Gaming**
- **Instant Games**
- The `gaming_profile` permission
- The `gaming_user_picture` permission

Click the **Customize** button to the right of **Launch a game on Facebook** to customize the following items for your use case:

- **Details** – Add a tagline, description, images and icons, game preview videos, and more
- **Localize** – Translate your game content in up to 104 languages
- **Web hosting** – Upload your game client code directly to Facebook instead of hosting it on your own servers
- **Login settings** – Add more permissions to ask users for access
- **Feedback** – Get all feedback submitted from players within the last 90 days

## Facebook Login for Gaming

### Settings

Facebook Login for Gaming allows you to control oAuth settings, and add a deauthorization callback URL and redirect URI validator.

### Quickstart

The Facebook Login for Gaming quickstart allows you to quickly implement Facebook Login for Gaming in your app.

## Permissions

You will see a list of permissions that are available in the Instant Games use case with a full description and requirements for each.

- `email` – Can be added if your app needs a person's email address
- `gaming_profile` – Automatically added and can not be removed
- `gaming_user_locale` – Can be added if your app needs a person's locale
- `gaming_user_picture` – Automatically added and can not be removed

After you add a permission to your app, you can see the status for that permission:

- Ready for live mode – This permission has been approved in App Review
- Ready to Testing – You can test API calls to endpoints that require this permission
- Verification Required – This permission has not yet been approved in App Review

You can also see the number of successful API calls you have made to endpoints that require each permission.

## Next Steps

Now that you have successfully customized your Launch a game on Facebook use case, you can [add additional use cases](https://developers.facebook.com/docs/development/create-an-app/instant-games-use-case/additional-uses-cases) or [update the settings for your app](https://developers.facebook.com/docs/development/create-an-app/app-dashboard/basic-settings) in the app Dashboard.

## See Also

To learn more about the concepts, endpoints, and permissions mentioned in this document, please visit the following guides:

- [Facebook Login for Gaming](https://developers.facebook.com/docs/development/create-an-app/facebook-login-for-games-use-case)
- [Instant Games](https://developers.facebook.com/docs/games/build/instant-games/)
- [Permissions Reference](https://developers.facebook.com/docs/permissions)
