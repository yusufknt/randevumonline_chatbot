# Page Public Metadata Access - App Development with Meta

_Source: https://developers.facebook.com/docs/features-reference/page-public-metadata-access_

---

# Page Public Metadata Access

*Requires [App Review](https://developers.facebook.com/docs/app-review).*

The **Page Public Metadata Access** allows your app access to the [Pages Search API](https://developers.facebook.com/docs/pages/searching) and to read public data for Pages for which you lack the [pages\_read\_engagement permission](https://developers.facebook.com/docs/permissions/reference/pages_read_engagement) and the [pages\_read\_user\_content permission](https://developers.facebook.com/docs/permissions/reference/pages_read_user_content). The allowed usage for this feature is to analyze engagement with public Pages by viewing Like and follower counts, or aggregate public-facing **About** Page information from multiple, disparate pages. You may also use this permission to request analytics insights to improve your app and for marketing or advertising purposes, through the use of aggregated and de-identified or anonymized information (provided such data cannot be re-identified).

## Allowed Usage

- Analyze engagement with public Pages by viewing Like and follower counts.
- Aggregate public-facing "about" Page information from multiple, disparate pages.

## Common Endpoints

[/page](https://developers.facebook.com/docs/graph-api/reference/page)

## Additional Details

- This permission or feature requires successful completion of the App Review process before your app can access live data. [Learn More.](https://developers.facebook.com/docs/app-review)
- This permission or feature is only available with business verification. You may also need to sign additional contracts before your app can access data. [Learn More Here](https://developers.facebook.com/docs/development/release/business-verification)
- If your app also needs to read the [Page Feed](https://developers.facebook.com/docs/graph-api/reference/page/feed) edge, or [Comments](https://developers.facebook.com/docs/graph-api/reference/comment) on a Page's [Posts](https://developers.facebook.com/docs/graph-api/reference/post), request the [Page Public Content Access](#page-public-content-access) feature instead.
- This feature is superseded by the Page Public Content Access (PPCA) feature. If your App Review submission includes PPCA, or your app has already been approved for PPCA, you cannot request this permission.
- If your app also needs to create, update, or delete data on a Page, request the [`pages_read_engagement`](https://developers.facebook.com/docs/permission/reference/pages_read_engagement) permission instead.
