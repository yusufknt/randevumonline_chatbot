# oEmbed Read - App Development with Meta

_Source: https://developers.facebook.com/docs/features-reference/oembed-read_

---

# oEmbed Read

On April 8, 2025, we introduced a new oEmbed feature, [**Meta oEmbed Read**](https://developers.facebook.com/docs/features-reference/meta-oembed-read) to replace the existing oEmbed Read feature. The current [oEmbed Read feature](https://developers.facebook.com/docs/features-reference/oembed-read) will be deprecated on November 3, 2025.

- Apps created after April 8, 2025 that implement oEmbed will use the new Meta oEmbed Read feature.
- Existing apps that already use the current oEmbed Read feature will be automatically updated to the new Meta oEmbed Read feature by November 3, 2025.



The following fields are no longer returned and will be fully deprecated on November 3, 2025:

- `author_name`
- `author_url`
- `thumbnail_height`
- `thumbnail_url`
- `thumbnail_width`



Read the [oEmbed Updates blog post](https://developers.facebook.com/blog/post/2025/04/08/oembed-updates/) from Meta to learn more.

*Requires [App Review](https://developers.facebook.com/docs/app-review).*

The **oEmbed Read** feature allows your app to get embed HTML and basic metadata for public Facebook and Instagram pages, posts, and videos. The allowed usage for this feature is to provide front-end views of Facebook and Instagram pages, posts, and videos. You may also use this permission to request analytics insights to improve your app and for marketing or advertising purposes, through the use of aggregated and de-identified or anonymized information (provided such data cannot be re-identified).

## Allowed Usage

- Provide front-end views of Facebook and Instagram pages, posts, and videos.

## Common Endpoints

- [/oembed\_page](https://developers.facebook.com/docs/graph-api/reference/oembed-page/)
- [/oembed\_post](https://developers.facebook.com/docs/graph-api/reference/oembed-post/)
- [/oembed\_video](https://developers.facebook.com/docs/graph-api/reference/oembed-video/)
- [/instagram\_oembed](https://developers.facebook.com/docs/graph-api/reference/instagram-oembed/)

## Additional Details

- This permission or feature requires successful completion of the App Review process before your app can access live data. [Learn More.](https://developers.facebook.com/docs/app-review)

- This permission or feature is only available with business verification. You may also need to sign additional contracts before your app can access data. [Learn More Here](https://developers.facebook.com/docs/development/release/business-verification)
