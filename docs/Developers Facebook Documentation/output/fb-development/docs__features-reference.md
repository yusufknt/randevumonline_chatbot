# Features Reference - App Development with Meta

_Source: https://developers.facebook.com/docs/features-reference_

---

# Features Reference

A features is an access grant that allow an app to access specific types of data through Meta's various APIs. These features cannot be granted to an app by an app user but are active or inactive depending on the app user's relationship to the app and the app's review status.

For apps that **are not approved** for a feature in Meta App Review, the feature is **only active for app users who have a role on the app or a role in a business portfolio that has claimed the app**. Exceptions are Page Public Content Access and Page Public Metadata Access.

For apps that are approved for a feature in Meta App Review, the feature is active for all app users.

## Ad Targeting Data Acces

The **Ad Targeting Data Access** feature allows access to ad targeting data within the Facebook Open Research and Transparency tool for election, political, and social issue ads that are run on Facebook from Meta and Instagram from Meta. The allowed usage of this functionality is to conduct research about Meta's role in society. You may also use this permission to request analytics insights to improve your app and for marketing or advertising purposes, through the use of aggregated and de-identified or anonymized information (provided such data cannot be re-identified).


***Allowed Usage***

- To conduct research about Meta's role in society

## Ads Management Standard Access

The **Ads Management Standard Access** feature allows your app to access the Marketing API. The allowed usage for this feature is to enable an unlimited number of ad accounts and lower rate limiting. At a minimum, ads\_read or ads\_management permission is required to use Ads Management Standard Access. You may also use this permission to request analytics insights to improve your app and for marketing or advertising purposes, through the use of aggregated and de-identified or anonymized information (provided such data cannot be re-identified).


***Allowed Usage***

- Enable an unlimited number of ad accounts and lower rate limiting.
- To read ads reports for ad accounts you own or have been granted access to by the ad account owner, request **Ads Management Standard Access**, along with the **ads\_read** permission.
- To read and manage ads for ad accounts you own or have been granted access to by the ad account owner, request **Ads Management Standard Access**, along with the **ads\_management** permission.
- To pull ads reports from a set of clients, and to read and manage ads from another set of clients, request **Ads Management Standard Access**, along with both **ads\_read** and **ads\_management** permissions.

## Business Asset User Profile Access

The **Business Asset User Profile Access** feature allows your app to read the User Fields for users engaging with your business assets such as id, ids\_for\_business, name, and picture. The allowed usage for this feature is to read one or more of the User Fields in a business app experience. You may also use this feature to request analytics insights to improve your app and for marketing or advertising purposes, through the use of aggregated and de-identified or anonymized information (provided such data cannot be re-identified).


***Allowed Usage***

You can use this feature if your app uses one or more of the User Fields in its business app experience.

## Human Agent

The **Human Agent** feature allows your app to have a human agent respond to user messages using the **human\_agent** tag within 7 days of a user's message. The allowed usage for this feature is to provide human agent support in cases where a user’s issue cannot be resolved in the standard messaging window. Examples include when the business is closed for the weekend, or if the issue requires more than 24 hours to resolve.


***Allowed Usage***

- Provide human agent support in cases where a user’s issue cannot be resolved in the standard messaging window.

## Instagram Public Content Access

The **Instagram Public Content Access** feature allows your app to access Instagram Graph API's Hashtag Search endpoints. The allowed usages for this feature is to discover content associated with your hashtag campaigns, understand public sentiment around your brand or identify contest, competition and sweepstakes entrants. It can also be used to provide customer support and better understand and manage your audience. You may also use this permission to request analytics insights to improve your app and for marketing or advertising purposes, through the use of aggregated and de-identified or anonymized information (provided such data cannot be re-identified).


***Allowed Usage***

- Discover content associated with its current campaign.
- Provide customer support.
- Identify entrants to its contests, competitions, or sweepstakes.
- Understand public sentiment around brand.
- Understand and manage their audience, develop their content strategy and obtain digital rights.

## Instant Games Zero Permission Access

The **Instant Games Zero Permission Access** feature allows your app to share user data including Instant Games context ID, and player ID, user profile, location and gameplay data. The allowed usage of this feature is to integrate user profiles in Instant Games on Meta’s network without gaining direct access to the user’s data.


***Allowed Usage***

- Integrate user profiles in Instant Games on Meta’s network

## Live Video API

The **Live Video API** feature allows your app to manage live videos for Pages, groups and User timelines when combined with the correct matching permission. The allowed usage for this feature is to publish live video content from your app to Facebook from a source other than mobile device cameras. To post to user timelines, you will also need access to the **publish\_video** permission. To post to Groups, you will also need access to the **publish\_to\_groups** permission. To post to Pages, you will also need access to the **pages\_manage\_posts**, **pages\_read\_user\_content**, and **pages\_show\_list** permissions, in addition to the **Live Video API** feature. You may also use this feature to request analytics insights to improve your app and for marketing or advertising purposes, through the use of aggregated and de-identified or anonymized information (provided such data cannot be re-identified).


***Allowed Usage***

- App users can publish live video content from your app to Facebook.

## Marketing API Access Tier

The **Marketing API Access Tier** feature allows your app access to higher rate limits, unlimited ad account management, higher system user limits, and the Business Manager API. At a minimum, **ads\_read** or **ads\_management** permission is required to use this feature. The allowed usage of this functionality is to enable your app users to scale their marketing operations and manage advertising assets more efficiently; to read ads reports for ad accounts you own or have been granted access to by the ad account owner (must request the ads\_read permission); to read and manage ads for ad accounts you own or have been granted access to by the ad account owner (must request the ads\_management permission); to pull ads reports from a set of clients, and to read and manage ads from another set of clients (must request the ads\_read permission, and the ads\_management permission). You may also use this permission to request analytics insights to improve your app and for marketing or advertising purposes, through the use of aggregated and de-identified or anonymized information (provided such data cannot be re-identified).


***Allowed Usage***

- Enable your app users to scale their marketing operations and manage advertising assets
- To read ads reports for ad accounts you own or have been granted access to by the ad account owner, request the ads\_read permission.
- To read and manage ads for ad accounts you own or have been granted access to by the ad account owner, request the ads\_management permission.
- To pull ads reports from a set of clients, and to read and manage ads from another set of clients, request the ads\_read permission and the ads\_management permission.

## Meta oEmbed Read

The **Meta oEmbed Read** feature allows your app to get embed HTML and basic metadata for public Facebook and Instagram pages, posts, and videos. The allowed usage for this feature is to provide front-end views of public Facebook and Instagram pages, posts, and videos.


***Allowed Usage***

- To provide front-end views of public Facebook and Instagram pages, posts, and videos

## Page Mentioning

The **Page Mentioning** feature allows your app mention any Facebook Page when publishing posts on the Pages managed by your app. To use Page Mentioning, your app needs to have been granted the **manage\_pages** and **publish\_pages** permissions. The allowed usage for this feature is to to let people use your app to publish Page posts that mention other Pages or to mention Pages relevant to the content in your page post. You may also use this permission to request analytics insights to improve your app and for marketing or advertising purposes, through the use of aggregated and de-identified or anonymized information (provided such data cannot be re-identified).


***Allowed Usage***

- Allow people to use your app to publish Page posts that mention other Pages.
- Mention Pages relevant to the content in your page post.

## Page Public Content Access

The **Page Public Content Access** feature allows an app access to the Pages Search API and to read public data for Pages for which you lack the **pages\_read\_engagement** permission and the **pages\_read\_user\_content** permission. Readable data includes business metadata, public comments and posts. The allowed usage for this feature is to analyze and/or display posts and engagement on Pages.


***Allowed Usage***

- Analyze and/or display posts and engagement on Pages.

## Page Public Metadata Access

The **Page Public Metadata Access** allows your app access to the [Pages Search API](https://developers.facebook.com/docs/pages/searching) and to read public data for Pages for which you lack the [pages\_read\_engagement permission](https://developers.facebook.com/docs/permissions/reference/pages_read_engagement) and the [pages\_read\_user\_content permission](https://developers.facebook.com/docs/permissions/reference/pages_read_user_content). The allowed usage for this feature is to analyze engagement with public Pages by viewing Like and follower counts, or aggregate public-facing **About** Page information from multiple, disparate pages. You may also use this permission to request analytics insights to improve your app and for marketing or advertising purposes, through the use of aggregated and de-identified or anonymized information (provided such data cannot be re-identified).


***Allowed Usage***

- Analyze engagement with public Pages by viewing Like and follower counts.
- Aggregate public-facing "about" Page information from multiple, disparate pages.

## Threads oEmbed Read

The **Threads oEmbed Read** feature allows an app to embed content of Threads posts, such as photos and videos, in other websites. The allowed usage for this feature is to provide front-end views of Threads posts. You may also use this permission to request analytics insights to improve your app and for marketing or advertising purposes, through the use of aggregated and de-identified or anonymized information (provided such data cannot be re-identified).


***Allowed Usage***

- Provide front-end views of Threads posts

## Threat Exchange

The **ThreatExchange** feature allows your app to share threat data among a select group of vetted industry partners. The allowed usage for this feature is to share threat data with a specific group of partners to achieve their security goals. You may also use this feature to request analytics insights to improve your app and for marketing or advertising purposes, through the use of aggregated and de-identified or anonymized information (provided such data cannot be re-identified).


***Allowed Usage***

- Share threat data with a specific group of partners to achieve their security goals.

## Learn More

Learn more about developing with Meta with the following guides:

- [Access Levels](https://developers.facebook.com/docs/graph-api/overview/access-levels)
- [App Development](https://developers.facebook.com/docs/development/create-an-app)
- [App Review](https://developers.facebook.com/docs/app-review)
- [App Roles](https://developers.facebook.com/docs/development/build-and-test/app-roles)
- [Business Roles](https://www.facebook.com/business/help/442345745885606)
- [Permissions Reference](https://developers.facebook.com/docs/permissions/reference)
