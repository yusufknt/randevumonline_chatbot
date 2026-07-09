# App Review | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/app-review_

---

# App Review

Updated: Nov 6, 2025

App Review is part of [app development](https://developers.facebook.com/docs/development) that enables us to verify that your app uses our Products and APIs in an approved manner. Meta needs to validate how you intend to use the requested permissions to make sure it is compliant with our requirements and policies.

Businesses first need to develop a prototype of their product so they can demonstrate their use case with a video recording for the App Review submission. To pass App Review, it is important that you ask for only the permissions your app needs; **requesting unnecessary permissions is a common reason for rejection** during app review.

The following video provides a brief overview of the App Review process:

Business apps are automatically approved for [Standard Access](https://developers.facebook.com/docs/graph-api/overview/access-levels#standard-access) for all Permissions and Features available to the Business app type, so you can test your app while you are in this access level. Make sure your test users have a `developer` or `admin` role in the Meta app being used to implement embedded signup. This means that if you are using the API for yourself as a Direct Developer, you do not need advanced access or app review.

If you are building an app that other businesses will be using, you must request advanced access for any permissions your app needs.
You can request [Advanced Access](https://developers.facebook.com/docs/graph-api/overview/access-levels#advanced-access) by submitting your app to App Review.

## Permissions

Commonly requested permissions and what to include to get approval for Advanced Access:

| Permission | Description | What to include in your submission |
| --- | --- | --- |
| [whatsapp_business_management](https://developers.facebook.com/docs/permissions#w) | The whatsapp_business_management permission allows your app to read and/or manage WhatsApp business assets you own or have been granted access to by other businesses through this permission. These business assets include WhatsApp Business Accounts, business phone numbers, message templates, QR codes and their associated messages, and webhook subscriptions. | **Written:** Explain how you will use this permission to access the business assets of business customers who you have onboarded onto the platform.<br>**Video:** Record a video of your app, or WhatsApp Manager, being used to create a message template. |
| [whatsapp_business_messaging](https://developers.facebook.com/docs/permissions#w) | The whatsapp_business_messaging permission allows an app to send WhatsApp messages and make calls to a specific phone number, upload and retrieve media from messages, manage and get WhatsApp business profile information, and to register those phone numbers with Meta. | **Written:** Explain what messaging functionality your app offers to business customers who you have onboarded onto the platform, and how they perform those functions.<br>**Video:** Record a video showing your app being used to send a message to a WhatsApp number, and the WhatsApp client (either web or mobile app) receiving and displaying the sent message. If you wish, you can use the **App Dashboard** > **WhatsApp** > **API Setup** panel to generate a cURL request that you can integrate into your app to send the message.<br>If you are partnering with a Solution Partner and plan to use their API, ask the Solution Partner to share a video with you that you can submit as part of your submission. |
| [whatsapp_business_manage_events](https://developers.facebook.com/docs/permissions#w)<br>Only request this permission if you are using the [Marketing Messages API for WhatsApp](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/overview) with [Conversions API](https://developers.facebook.com/documentation/ads-commerce/conversions-api). | The **whatsapp_business_manage_events** permission allows an app to log events, such as purchase, add-to-cart, leads and more, on behalf of a WhatsApp Business Account administered by an app user. The allowed usage for this permission is to log events on WhatsApp Business Accounts and send this activity data to Meta for ads targeting, optimization and reporting. | This permission is automatically approved if you already have advanced access for `whatsapp_business_messaging` permission. |

The average turnaround time for app reviews is about 24 hours. We recommend starting the app review process as soon as possible. You don’t need to wait for Embedded Signup to be fully implemented to start this process.

## Reducing chances of app review rejection

You must request Advanced access for the permissions above.

You can request these permissions in a single bulk submission, or as separate submissions. For each permission, an explanation and screen recording specific to the permission being requested is required.

As part of your submission, you must include separate screen recordings that show how your app uses each permission in your submission. The video can be a screen recording directly from your computer, or a recording using a digital camera or camera phone. You will need to attach this file to your App Review submission.

Do not submit a video that includes multiple permissions supporting different use cases. You must submit a different video clip for each permission. Your submission may be rejected if you highlight multiple permissions being used as part of the same video.

Both written descriptions and screen recordings are required for each permission. If you include a screen recording that shows how your app uses a permission, but fail to include a description of how it uses it, your submission will be rejected.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/496716242_1475889623405133_5410416263043243743_n.png?_nc_cat=110&ccb=1-7&_nc_sid=e280be&_nc_ohc=V9ibP-2E-4wQ7kNvwG1vwZn&_nc_oc=AdoofPtJkQxb05TotBHhpilE3bVilfV8Wdypi3LrS4Sf14erSqlZJvV4MzKfl1D9Ysg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=Q78lve4J2HBO7rynNG_jlw&_nc_ss=7b20f&oh=00_Af5xW0PzEMluWPJPjKrETHo-qEQNEAmTb_rLA2YsK6RG2w&oe=6A1C041A)

Submissions in draft mode will not be reviewed, so don’t forget to **submit your App Review submission!**

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/503769387_653066754402874_3122829917621506762_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=ze2xezu9dlcQ7kNvwFAb8bg&_nc_oc=AdriSG3bJNJGDGy1ow-Kbr0ywa1Cjri23smodkr77btTBGW1zhE3xp5ys9BjkXzBS7E&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=Q78lve4J2HBO7rynNG_jlw&_nc_ss=7b20f&oh=00_Af6f2Dt2audnVLcf7S7QP4fIG1CwYdbeBL5R86OK9B8cog&oe=6A1C0D15)

## Examples

This is an example of a screen recording showing a developer using their app to submit a template for approval. This demonstrates the developer’s app using the **whatsapp_business_management** permission, which the developer requested in their App Review submission.

This is a screenshot from an example screen recording showing a developer using their app to send and receive a message to and from a WhatsApp user number (right-click and open in a new tab to see a larger version). This demonstrates the developer’s app using the **whatsapp_business_messaging** permission, which the developer requested in their App Review submission.

Note that **you cannot submit a screenshot**, you must submit a screen recording.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/501582465_1425064645196941_2695325123378401168_n.png?_nc_cat=106&ccb=1-7&_nc_sid=e280be&_nc_ohc=xz83Y69ajJwQ7kNvwGwI2Au&_nc_oc=AdqO_omIniWTiz5iJIQNcpMPPWTAt0vY6WkQU5YprCYmUYR3NlllhzPs6FqGp6Xz-RA&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=Q78lve4J2HBO7rynNG_jlw&_nc_ss=7b20f&oh=00_Af71f2sgS8GE9nDONy5s0vSBrTQuPYeF-ZHdJkZDMhPtzA&oe=6A1BFC69)
