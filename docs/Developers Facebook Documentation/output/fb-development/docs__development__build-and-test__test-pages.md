# Test Pages - App Development with Meta

_Source: https://developers.facebook.com/docs/development/build-and-test/test-pages_

---

# Test Pages

Test pages are [test user](https://developers.facebook.com/docs/development/build-and-test/test-users)-generated Facebook Pages that you can use to simulate real Facebook Pages when testing your app in [Development](https://developers.facebook.com/docs/development/build-and-test/app-modes#development-mode) mode. Test pages cannot interact with real Facebook users, and any data you generate with a test page will only be visible to test users on your app, or to real Facebook users who have an Administrator, Developer, or Tester [role](https://developers.facebook.com/docs/development/build-and-test/app-roles) on your app. Test pages are exempt from our spam and fake account detection systems, so they won't be disabled when you use them to test your app.

## Limitations

- Test pages can only be created by [test users](https://developers.facebook.com/docs/development/build-and-test/test-users).
- Test pages can only interact with test users or real Facebook users who have an Administrator, Developer, or Tester [role](https://developers.facebook.com/docs/development/build-and-test/app-roles) on your app.
- Only test users who are friends of a test user who created a test page can interact with the test page.

## Creating Test Pages

To create a test page, log into one of your app's [test users](https://developers.facebook.com/docs/development/build-and-test/test-users) and create a Facebook Page as you normally would.

To log in as a test user:

1. Go to the [Apps](https://developers.facebook.com/apps) panel and select your app to load it in the App Dashboard.
2. Go to **Roles** > **Test Users** and click an existing test user's **Edit** button.
3. Click **Log in as this test user** and complete the confirmation flow.

## Managing Test Pages

When logged into Facebook as a test user, you can edit the following test page attributes:

- Change the name of the test page.
- Add and update its settings such as its cover picture, profile picture, and description.
- Add and update business information such as a website, location, and business hours.
- Invite other test users to visit the page.
- Publish content, comment and react to posts, create events, and more.
- View page insights such as Page Views, Post Engagement, and Page Likes.

If you delete the test user who created the test page, all test pages created by the test user will be deleted as well.

## Test Pages Graph API Endpoints

You can manage test page using the Graph API.

App Administrators and Developers can use the [User Accounts](https://developers.facebook.com/docs/graph-api/reference/user/accounts) endpoint to:

- Get the ID for each test page that a test user has created.
- Get a Page access token for each test page that a test user has created.

App Administrators and Developers can use the [Page](https://developers.facebook.com/docs/graph-api/reference/page) endpoint to:

- Add and update Page settings such as a cover and profile picture, and description.
- Add and update business information such as a website, location, business hours, and more.
- Invite other Test Users to visit your Page.
- Publish content, comment and react to posts, create events, and more.
- View Page insights such as Page views, post engagement, and Page likes.
- Delete a Test Page.
