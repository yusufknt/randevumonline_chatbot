# Test Apps - App Development with Meta

_Source: https://developers.facebook.com/docs/development/build-and-test/test-apps_

---

# Test Apps

Test apps are child apps created from other, non-child (i.e. parent) apps. They are primarily used to clone parent apps that are already in [Live](https://developers.facebook.com/docs/development/build-and-test/app-modes#live-mode) mode in order to test new [reviewable](https://developers.facebook.com/docs/app-review) permissions and features without compromising the functionality of the cloned parent app.

![Screenshot of App Selection dropdown meny in App Dashboard toolbar with Create Test App button displayed.](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/132131435_864715260997752_3537093673129395753_n.png?_nc_cat=102&ccb=1-7&_nc_sid=e280be&_nc_ohc=Xi8oU0co_k4Q7kNvwH-i9Fe&_nc_oc=AdqbWpWaeRl3QNALh1i6uQwjSsW7YI6Xsg2rtuMy2SDsu1VREdWX7WtZZLyrhXg8Y7Y&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=QznNLzSfTDGb13Hz_brf4w&_nc_ss=7b289&oh=00_Af7-addctzZRyq3750OBVrwvGnytMlv1t7JwaBcPhDbgXg&oe=6A1BE928)

Test apps are always in [Development](https://developers.facebook.com/docs/development/build-and-test/app-modes#development-mode) mode and inherit their parent app settings at the time that they are created. Once created, you can adjust a test app's settings to suit your testing needs.

## Limitations

- Parent apps can only have 50 child test apps.
- User IDs are scoped to the parent app.

## Test App Roles

Test apps inherit the [Administrators](https://developers.facebook.com/docs/development/build-and-test/app-roles#admin) from their parents. As with non-test apps, Administrators have full control over the test app's settings, including the ability to add and remove people from roles.

People who have been added as Administrators to test apps (instead of inherited from their parents) can only perform admin actions on those test apps.

## Creating Test Apps

To create a test app:

1. Load the app that you want to clone in the App Dashboard.
2. In the upper-left corner of the dashboard, click the app selection dropdown menu and click **Create Test App**.
3. Name the app and click **Create Test App**.

You can now adjust your test app's settings and products and test new features and permissions without affecting the app from which it was cloned.

## Testing Test Apps

Testing a test app is just like testing any other app; update any SDK configurations that rely on your app ID and app secret with the test app's corresponding values and grant the test app relevant permissions using any user who has a role on the app itself.

## Removing Test Apps

You can remove test apps like you would any Facebook app.

1. In the Dashboard select the test app you would like to remove.
2. In the left navigation pane, click **Settings** > **Advanced**.
3. Scroll down and click **Remove App**.

Note: If you remove a parent app, all of its test apps will also be removed.

## FAQs

[I have already created apps for development, QA or staging. Can I merge these apps into my production app's Test Apps list?](#faq_726113361672658)

No. We suggest creating new test apps and migrating your development teams to use these new test apps for development, testing, QA, and staging purposes.

[Permalink](#faq_726113361672658)

[My production app's settings have change. Can I push these updates to my test apps?](#faq_156905329523539)

No. You will need to change settings in each test app manually or create a new test app to reflect the new settings.

[Permalink](#faq_156905329523539)

[I created a test app with settings that I want my production app to use. Is there an easy way to update my production app with these settings?](#faq_390923895550274)

No. You will need to update your production app's settings manually.

[Permalink](#faq_390923895550274)
