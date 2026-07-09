# App Review - Instagram Platform

_Source: https://developers.facebook.com/docs/instagram-platform/app-review_

---

# App Review for Instagram API

Your app must complete App Review before it can request permissions with Advanced Access from any app user and features with Advanced Access are active for all app users.

## Development scenarios

The following table contains the possible development scenarios and the corresponding App Review requirements.

| Development scenario | Login type | Access level | App Review |
| --- | --- | --- | --- |
| My app is only for a business I own or manage. | No login or Instagram Login | Standard Access | Not required |
| My app is only for a business I own or manage. | No login or Facebook Login | Standard Access | Not required |
| I am a Tech Provider and my app serves multiple businesses. | Instagram Login | Advanced Access | **Required** |
| I am a Tech Provider and my app serves multiple businesses. | Facebook Login | Advanced Access | **Required** |

## Available permissions & features

The permissions and features you can request Advanced Access for are dependent on the login type.

Your app can either use Facebook Login or Instagram Login but not both.

|  |  |
| --- | --- |
| [Instagram API with Facebook Login](https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/business-login-for-instagram)   - Human Agent - Instagram Public Content Access - `ads_management` - `business_management` - `catalog_management` - `instagram_basic` - `instagram_branded_content_ads_brand` - `instagram_branded_content_brand` - `instagram_branded_content_creator` - `instagram_content_publishing` - `instagram_manage_comments` - `instagram_manage_events` - `instagram_manage_insights` - `instagram_manage_messages` - `instagram_manage_upcoming_events` - `instagram_shopping_tag_products` - `pages_read_engagement` - `pages_show_list` | [Instagram API with Instagram Login](https://developers.facebook.com/docs/instagram/platform/instagram-api/business-login)   - Human Agent - `instagram_business_basic` - `instagram_business_content_publishing` - `instagram_business_manage_comments` - `instagram_business_manage_messages` |

### Migrated apps

If you are migrating your app to Instagram API with Instagram Login from Instagram API with Facebook Login, your app might automatically be granted Advanced Access for the corresponding Instagram API permission and App Review isn't required.

If your app is not automatically granted Advanced Access, then you will need to submit for App Review.

| [Instagram API with Facebook Login](https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/business-login-for-instagram) | [Instagram API with Instagram Login](https://developers.facebook.com/docs/instagram/platform/instagram-api/business-login) |
| --- | --- |
| `instagram_basic` | `instagram_business_basic` |
| `instagram_content_publishing` | `instagram_business_content_publishing` |
| `instagram_manage_comments` | `instagram_business_manage_comments` |
| `instagram_manage_messages` | `instagram_business_manage_messages` |

If you need to submit for App Review you must follow the instructions in the [**Start a submission** section below](#start-a-submission). The submission flow in the App Dashboard has changed.

## Start a submission

To submit for App Review, go to the App Dashboard.

1. In the left-side menu under **Products**, go to **Instagram > API setup with Instagram login**.
2. Click the chevron in the upper right corner of the **Complete app review** section.
3. Review the permissions and features you are requesting Advanced Access for and click **Continue to app review**. You'll be redirected to **App Review > Requests** in the dashboard.
4. Click the **Edit** button to trigger the review flow.

## Request for App Review

You will see a list of action items that are required. These include the following:

- Confirm that your app can be loaded and tested externally
- Verify that the login button or link is visible in your app and screencast, and adheres to our brand guidelines
- Provide clear use case details and describe step-by-step how a person uses your app
  Tell us how your use of each permission you have requested follows established usage guidelines
- To request Advanced Access to certain permissions, you need to make at least 1 successful API call

### Complete App Settings

Add or upate your app's settings.

Click the **Review your app settings** to add or update the following:

1. App icon (1024x1024) – The icon for your app
2. Privacy Policy URL – The privacy policy URL that your app users can visit to view your privacy policy
3. App Category – The app category that best represents your app's functionality
4. Business Email – The email, set in your Developer Settings, where App Review results and developer alert emails are sent

### Complete App Verification

Provide detailed instructions for Meta app reviwers to log in and test your app.

Click **Provide verification details** to provide detailed step-by-step instructions, for each platform on which your app is available, for Meta app reviewers so they can log in to your app to test your integration and how you are using each permission and feature.

1. Platform Settings
   - Provide **detailed step-by-step instructions for Meta reviewers to log in and test your app** on each platform, Android, iOS, Web, and so on, on which your app is available. Be specific about when and how your app uses each permission and feature and how a reviewer can test each usage.
2. Credentials (If applicable)
   - If needed, provide any required test credentials for Meta reviewers to log into your app or website.

**NOTE:** Web or mobile Web is the only platform that currently supports Instagram API with Instagram Login.

![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/453385011_853085869681207_5149396634646446049_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=iqrM9GdW6P4Q7kNvwG_xvIe&_nc_oc=AdoWKOGXws9Y45FypcsC1q3uP3g6jJuux6OacqzkKmM-U-IoAtWcQ5ARRqtIixSOpYU&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=GIyydxh-pbGefHdZzdl3nA&_nc_ss=7b289&oh=00_Af63Xt2AUQgl0JPXeyVzR9UOsVv6dL6LLG1jE6AKhxrY6g&oe=6A1BEBC6)

### Permission & feature requests

Provide a description for how your app uses a specific permission and include a screencast showing this usage.

Click the arrow icon to the right of each **How will your app use** question for each permission or feature that you have requested. You will be asked to:

- Describe how your app uses that specific permission or feature
- Upload a screencast showing the end-to-end user experience for that specific permission or feature. The screencast only needs to showcase how your app is using that permission or feature.
- Agree that you will comply with the allowed usage for that permission or feature.
- If a permission or feature is dependent on another permission, you must include this permission in your submission.

If you request permissions or features that your app does not use or does not align with the allowed usage for that permission or feature, your submission will not be approved.

![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/453238879_501155255607182_3048020962529192094_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=aW-jtdXENVgQ7kNvwHbOZxC&_nc_oc=Adpf-PCeGd6tmGfnwIpeBh3fxEPwRZtFb-XYqf-UroCjMNTRqJ2Dl3DdYCSMZn7d-eM&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=GIyydxh-pbGefHdZzdl3nA&_nc_ss=7b289&oh=00_Af4Zq10OXvrvJjrwe64ocsFRIi1MBpnIwN7CfFfzVa_BMQ&oe=6A1BDC9A)

### Screencast guidance

To ensure that your screen recording is accessible to all our reviewers, please follow these guidelines:

- **Use English as the app UI language** – If possible, please set the app UI language to English before recording the screen recording. This will make it easier for the review team to understand the content of your app.
- **Provide captions and tool-tips** – If your app is not available in English, or if there are any parts of the app that are not self-explanatory, please provide captions and tool-tips to explain what is happening on screen. This will help the review team understand what you are showcasing and how the app works.
- **Explain the meaning of buttons and other UI elements** – Please take the time to explain the meaning of any buttons or other UI elements that are not immediately obvious. This will help the review team understand how to use your app and what each button does.

### Completed items

When an item is complete, the circle with a check mark will be filled in.

![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/453405956_2251768315215785_5370163649097362503_n.png?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=QRYJ_1RtOroQ7kNvwEKJ4Ty&_nc_oc=AdroNqhz7Up4fGybDXlvjNF0a8z9gTB7xpmL0mod3iOS6zVBhGa5vZiswhLF9morNQc&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=GIyydxh-pbGefHdZzdl3nA&_nc_ss=7b289&oh=00_Af6gRZpOuTfckWU9INfn6OG5lObYB7zKtMpU0NTTMzVk8Q&oe=6A1BD9B6)

## See Also

See the following documents to learn more about Meta App Review:

- [Access Levels
  ![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/310307727_3347317042262105_1088877051262827250_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=5SvUa0KxdZkQ7kNvwHcqah0&_nc_oc=AdpNPlkM5xCl8ncqAEi0DvJzLsMMV09WvXL6Z1STXmvsbKMnBfs-2mixKR1O9x9_AAg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=GIyydxh-pbGefHdZzdl3nA&_nc_ss=7b289&oh=00_Af7Vfr_GCfS9hM0I1PF11eFj0aaf4ENSSlfDTyjWGOB6ug&oe=6A1BE7E2)](https://developers.facebook.com/docs/graph-api/overview/access-levels)
- [App Development with Meta
  ![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/310307727_3347317042262105_1088877051262827250_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=5SvUa0KxdZkQ7kNvwHcqah0&_nc_oc=AdpNPlkM5xCl8ncqAEi0DvJzLsMMV09WvXL6Z1STXmvsbKMnBfs-2mixKR1O9x9_AAg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=GIyydxh-pbGefHdZzdl3nA&_nc_ss=7b289&oh=00_Af7Vfr_GCfS9hM0I1PF11eFj0aaf4ENSSlfDTyjWGOB6ug&oe=6A1BE7E2)](https://developers.facebook.com/docs/development)
- [Best Practices for Meta App Review
  ![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/310307727_3347317042262105_1088877051262827250_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=5SvUa0KxdZkQ7kNvwHcqah0&_nc_oc=AdpNPlkM5xCl8ncqAEi0DvJzLsMMV09WvXL6Z1STXmvsbKMnBfs-2mixKR1O9x9_AAg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=GIyydxh-pbGefHdZzdl3nA&_nc_ss=7b289&oh=00_Af7Vfr_GCfS9hM0I1PF11eFj0aaf4ENSSlfDTyjWGOB6ug&oe=6A1BE7E2)](https://developers.facebook.com/docs/resp-plat-initiatives/app-review/before-you-submit)
- [Common Mistakes
  ![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/310307727_3347317042262105_1088877051262827250_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=5SvUa0KxdZkQ7kNvwHcqah0&_nc_oc=AdpNPlkM5xCl8ncqAEi0DvJzLsMMV09WvXL6Z1STXmvsbKMnBfs-2mixKR1O9x9_AAg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=GIyydxh-pbGefHdZzdl3nA&_nc_ss=7b289&oh=00_Af7Vfr_GCfS9hM0I1PF11eFj0aaf4ENSSlfDTyjWGOB6ug&oe=6A1BE7E2)](https://developers.facebook.com/docs/app-review/submission-guide/common-mistakes)
  of App Review submissions
- [Meta App Review
  ![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/310307727_3347317042262105_1088877051262827250_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=5SvUa0KxdZkQ7kNvwHcqah0&_nc_oc=AdpNPlkM5xCl8ncqAEi0DvJzLsMMV09WvXL6Z1STXmvsbKMnBfs-2mixKR1O9x9_AAg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=GIyydxh-pbGefHdZzdl3nA&_nc_ss=7b289&oh=00_Af7Vfr_GCfS9hM0I1PF11eFj0aaf4ENSSlfDTyjWGOB6ug&oe=6A1BE7E2)](https://developers.facebook.com/docs/resp-plat-initiatives/app-review)
- [Sample Submissions
  ![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/310307727_3347317042262105_1088877051262827250_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=5SvUa0KxdZkQ7kNvwHcqah0&_nc_oc=AdpNPlkM5xCl8ncqAEi0DvJzLsMMV09WvXL6Z1STXmvsbKMnBfs-2mixKR1O9x9_AAg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=GIyydxh-pbGefHdZzdl3nA&_nc_ss=7b289&oh=00_Af7Vfr_GCfS9hM0I1PF11eFj0aaf4ENSSlfDTyjWGOB6ug&oe=6A1BE7E2)](https://developers.facebook.com/docs/app-review/submission-guide/screen-recordings)
