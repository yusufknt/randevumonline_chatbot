# oEmbed - Instagram Platform

_Source: https://developers.facebook.com/docs/instagram-platform/oembed_

---

# Embed an Instagram Post

You can query the Instagram oEmbed endpoint to get an Instagram post’s embed HTML and basic metadata in order to display the post in another website or app. Supports photo, video, Reel, and Feed posts.

Visit the [Instagram Help Center](https://l.facebook.com/l.php?u=https%3A%2F%2Fhelp.instagram.com%2F620154495870484&h=AUCZYUx5kNDK8uRLhXJNRiiZTTjVkjZ3bmUGeL318Frhpl_1nceBERWxX7XWtj5mKqZhzHIlnWGP-4c6YjbJ6ycq12-3-qRKcCKD7egDGWEnCyeWpPIlvOlq1IJSq0EgrqTNmsR9v_qz8Q) to learn how to get the embed code from a public Instagram post or profile.

### Common uses

- Embed a post in a blog
- Embed a post in a website
- Render a post in a content management system
- Render a post in a messaging app

## Requirements

This guide assumes you are [a registered Meta developer
![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/310307727_3347317042262105_1088877051262827250_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=5SvUa0KxdZkQ7kNvwHcqah0&_nc_oc=AdpNPlkM5xCl8ncqAEi0DvJzLsMMV09WvXL6Z1STXmvsbKMnBfs-2mixKR1O9x9_AAg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=1Yn5kipzbGwZrQ79ue_f3A&_nc_ss=7b289&oh=00_Af5IX86ddhXhtgwQhCd8LE6d5_15VuNg-NGmEF8TK7QeNA&oe=6A1BE7E2)](https://developers.facebook.com/docs/development/register) and have created a [Meta app.
![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/310307727_3347317042262105_1088877051262827250_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=5SvUa0KxdZkQ7kNvwHcqah0&_nc_oc=AdpNPlkM5xCl8ncqAEi0DvJzLsMMV09WvXL6Z1STXmvsbKMnBfs-2mixKR1O9x9_AAg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=1Yn5kipzbGwZrQ79ue_f3A&_nc_ss=7b289&oh=00_Af5IX86ddhXhtgwQhCd8LE6d5_15VuNg-NGmEF8TK7QeNA&oe=6A1BE7E2)](https://developers.facebook.com/docs/development)

You will need the following:

#### Access levels

- [Advanced Access](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/overview#access-levels)

  for the Meta oEmbed Read feature – Requires

  [Meta App Review](#app-review-submission)

#### Access tokens

- [An app access token,
  ![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/310307727_3347317042262105_1088877051262827250_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=5SvUa0KxdZkQ7kNvwHcqah0&_nc_oc=AdpNPlkM5xCl8ncqAEi0DvJzLsMMV09WvXL6Z1STXmvsbKMnBfs-2mixKR1O9x9_AAg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=1Yn5kipzbGwZrQ79ue_f3A&_nc_ss=7b289&oh=00_Af5IX86ddhXhtgwQhCd8LE6d5_15VuNg-NGmEF8TK7QeNA&oe=6A1BE7E2)](https://developers.facebook.com/docs/facebook-login/guides/access-tokens#apptokens)
  if your app accesses the oEmbed endpoint from a backend server
- [An client access token,
  ![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/310307727_3347317042262105_1088877051262827250_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=5SvUa0KxdZkQ7kNvwHcqah0&_nc_oc=AdpNPlkM5xCl8ncqAEi0DvJzLsMMV09WvXL6Z1STXmvsbKMnBfs-2mixKR1O9x9_AAg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=1Yn5kipzbGwZrQ79ue_f3A&_nc_ss=7b289&oh=00_Af5IX86ddhXhtgwQhCd8LE6d5_15VuNg-NGmEF8TK7QeNA&oe=6A1BE7E2)](https://developers.facebook.com/docs/facebook-login/guides/access-tokens#clienttokens)
  if your app accesses the oEmbed endpoint from a user agent, such as a mobile device or web browser

#### Base URL

All endpoints can be accessed via the `graph.facebook.com` host.

#### Endpoints

- [`GET /instagram_oembed`](https://developers.facebook.com/docs/instagram-platform/docs/graph-api/reference/instagram-oembed)

#### Features

- [Meta oEmbed Read feature
  ![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/310307727_3347317042262105_1088877051262827250_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=5SvUa0KxdZkQ7kNvwHcqah0&_nc_oc=AdpNPlkM5xCl8ncqAEi0DvJzLsMMV09WvXL6Z1STXmvsbKMnBfs-2mixKR1O9x9_AAg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=1Yn5kipzbGwZrQ79ue_f3A&_nc_ss=7b289&oh=00_Af5IX86ddhXhtgwQhCd8LE6d5_15VuNg-NGmEF8TK7QeNA&oe=6A1BE7E2)](https://developers.facebook.com/docs/features-reference/meta-oembed-read)

### Limitations

- The Instagram oEmbed endpoint is **only** meant to be used for embedding Instagram content in websites and apps. It is not to be used for any other purpose. **Using metadata and page, post, or video content (or their derivations) from the endpoint for any purpose other than providing a front-end view of the page, post, or video is strictly prohibited**. This prohibition encompasses consuming, manipulating, extracting, or persisting the metadata and content, including but not limited to deriving information about pages, posts, and videos from the metadata for analytics purposes.
- Posts on private, inactive, and age-restricted Instagram accounts are not supported.
- Accounts that have [disabled **Embeds**](https://l.facebook.com/l.php?u=https%3A%2F%2Fhelp.instagram.com%2F252460186989212%2F&h=AUDp63mCEed6Egaw5dniXOOFGERe3jv2iSUprrWa8ofZLdftxN8Dgxx13kfCWp9iVBjHdbbqNI2IfoKBTaRb9ygzYkcLepmQTrZelNuSkbqAWKv8-8z1b28DYuJS3bnQ5wsQiHOdtcB7Tg) are not supported.
- Stories are not supported.
- Shadow DOM is not supported.

### Rate limits

Rate limits are dependent on the type of access token your app includes in each request.

#### App token rate limits

Apps that rely on app access tokens can make up to 5 million requests per 24 hours.

#### Client token rate limits

Client token rate limits are significantly lower than app token rate limits. We do not reveal the actual limit as it will change depending on your app activity. However, you can safely assume that your app will not reach its limit unless it exhibits bot-like behavior, such as batching thousands of requests, or sending thousands of requests per agent or app user.

## Get an embed HTML

You can get an embed HTML programmatically or [in the Instagram app.
![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/310307727_3347317042262105_1088877051262827250_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=5SvUa0KxdZkQ7kNvwHcqah0&_nc_oc=AdpNPlkM5xCl8ncqAEi0DvJzLsMMV09WvXL6Z1STXmvsbKMnBfs-2mixKR1O9x9_AAg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=1Yn5kipzbGwZrQ79ue_f3A&_nc_ss=7b289&oh=00_Af5IX86ddhXhtgwQhCd8LE6d5_15VuNg-NGmEF8TK7QeNA&oe=6A1BE7E2)](https://developers.facebook.com/docs/instagram-platform/embed-button)

To programmatically get an Intagram post's embed HTML, send a request to:

```
GET /instagram_oembed?url=<URL_OF_THE_POST>&access_token=<ACCESS_TOKEN>
```

Replace `<URL_OF_THE_POST>` with the [URL](#url-formats) of the Instagram post that you want to query and `<ACCESS_TOKEN>` with your app or client access token or pass it to us in an `Authorization` HTTP header.

`Authorization: Bearer <ACCESS_TOKEN>`

If you are using a client access token, remember that you must combine it with your Meta App ID using a pipe symbol otherwise the request will fail.

Upon success, the API will respond with a JSON object containing the post's embed HTML and additional data. The embed HTML will be assigned to the `html` property.

Refer to the [Instagram oEmbed reference![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/310307727_3347317042262105_1088877051262827250_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=5SvUa0KxdZkQ7kNvwHcqah0&_nc_oc=AdpNPlkM5xCl8ncqAEi0DvJzLsMMV09WvXL6Z1STXmvsbKMnBfs-2mixKR1O9x9_AAg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=1Yn5kipzbGwZrQ79ue_f3A&_nc_ss=7b289&oh=00_Af5IX86ddhXhtgwQhCd8LE6d5_15VuNg-NGmEF8TK7QeNA&oe=6A1BE7E2)](https://developers.facebook.com/docs/graph-api/reference/instagram-oembed) for a list of [query string parameters![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/310307727_3347317042262105_1088877051262827250_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=5SvUa0KxdZkQ7kNvwHcqah0&_nc_oc=AdpNPlkM5xCl8ncqAEi0DvJzLsMMV09WvXL6Z1STXmvsbKMnBfs-2mixKR1O9x9_AAg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=1Yn5kipzbGwZrQ79ue_f3A&_nc_ss=7b289&oh=00_Af5IX86ddhXhtgwQhCd8LE6d5_15VuNg-NGmEF8TK7QeNA&oe=6A1BE7E2)](https://developers.facebook.com/docs/graph-api/reference/instagram-oembed#parameters) you can include to augment the request. You may also include the `fields` query string parameter to specify which [fields![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/310307727_3347317042262105_1088877051262827250_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=5SvUa0KxdZkQ7kNvwHcqah0&_nc_oc=AdpNPlkM5xCl8ncqAEi0DvJzLsMMV09WvXL6Z1STXmvsbKMnBfs-2mixKR1O9x9_AAg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=1Yn5kipzbGwZrQ79ue_f3A&_nc_ss=7b289&oh=00_Af5IX86ddhXhtgwQhCd8LE6d5_15VuNg-NGmEF8TK7QeNA&oe=6A1BE7E2)](https://developers.facebook.com/docs/graph-api/reference/instagram-oembed#fields) you want returned. If omitted, all default Fields will be included in the response.

### Sample requests

```
curl -X GET \
  "https://graph.facebook.com/v25.0/instagram_oembed?url=https://www.instagram.com/p/fA9uwTtkSN/&access_token=IGQVJ..."
```

```
curl -i -X GET \
     --header "Authorization: Bearer 96481..." \
     "https://graph.facebook.com/v25.0/instagram_oembed?url=https%3A%2F%2Fwww.instagram.com%2Fp%2FfA9uwTtkSN"
```

### Sample Response

Some values truncated with an ellipsis (`...`) for readability.

```
{
  "version": "1.0",
  "author_name": "diegoquinteiro",
  "provider_name": "Instagram",
  "provider_url": "https://www.instagram.com/",
  "type": "rich",
  "width": 658,
  "html": "<blockquote class=\"instagram-media\" data-instgrm-ca...",
  "thumbnail_width": 640,
  "thumbnail_height": 640
}
```

### URL Formats

The `url` query string parameter accepts the following URL formats:

`https://www.instagram.com/p/{media-shortcode}/`
`https://www.instagram.com/tv/{media-shortcode}/`
`https://www.instagram.com/{username}/guide/{slug}/{guide_id}`

### Embed JS

The embed HTML contains a reference to the Instagram [embed.js](https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.instagram.com%2Fstatic%2Fbundles%2Fmetro%2FEmbedSDK.js%2F33cd2c5d5d59.js&h=AUCxSCjn5jDJijQOvwTd2LFt3XFSQQmWR4KGQg1lCVUMUlbQwAjgFumvJ7FuHKKSB2ujvs2ceU8Dr0RYGsmdLlMT7ZhOBPOjb9ovM2hqOZB3KkFCIQwlBt_7k-yDIAgK4mm9QnZTfUkCXQ) JavaScript library. When the library loads, it scans the page for the post HTML and generates the fully rendered post. If you want to load the library separately, include the `omitscript=true` query string parameter in your request. To manually initialize the embed HTML, call the `instgrm.Embeds.process()` function after loading the library.

### Post Size

The embedded post is responsive and will adapt to the size of its container. This means that the height will vary depending on the container width and the length of the caption. You can set the maximum width by including the `maxwidth` query string parameter in your request.

## Get thumbnails

We recommend that you render all of the post’s embed HTML whenever possible. If you are unable to do this, you can get a post’s thumbnail image URL and render that instead. If you do this, however, you must provide clear attribution next to the image, including attribution to the original author and to Instagram, and a link to the Instagram post that you are querying.

To get a post’s thumbnail URL and attribution information, send a request to:

```
GET /instagram_oembed
  ?url=<URL_OF_THE_POST>
  &maxwidth=<MAX_WIDTH>
  &fields=thumbnail_url,author_name,provider_name,provider_url
  &access_token=<ACCESS_TOKEN>
```

Replace `<URL_OF_THE_POST>` with the URL of the Instagram post you want to query, `<MAX_WIDTH>` with the maximum size of the thumbnail you want to render, and `<ACCESS_TOKEN>` with your app or client access token.

### Sample request

```
curl -i -X GET \
  "https://graph.facebook.com/v25.0/instagram_oembed?url=https%3A%2F%2Fwww.instagram.com%2Fp%2FfA9uwTtkSN&maxwidth=320&fields=thumbnail_url%2Cauthor_name%2Cprovider_name%2Cprovider_url&access_token=96481..."
```

### Sample Response

Some values truncated with an ellipsis (`...`) for readability.

```
{
  "thumbnail_url": "https://scontent.cdninstagram.com/v/t51.288...",
  "author_name": "diegoquinteiro",
  "provider_name": "Instagram",
  "provider_url": "https://www.instagram.com/"
}
```

## App Review submission

When you submit your app for review, in the **Tell Us Why You're Requesting Oembed Read > Please provide a URL where we can test Oembed Read** form field, use the Instagram oEmbed endpoint to get the embed HTML for any public post on our official [Facebook Page](https://www.facebook.com/facebook) or [Instagram Page](https://www.facebook.com/instagram). Then, add the returned embed HTML to where you will be displaying oEmbed content and enter that page's URL in the form field.

![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/198744124_168302945267129_761601492054025632_n.png?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=JbE56YALjqwQ7kNvwG_s9j_&_nc_oc=AdoZRiqrtx3XXKXNZ4VhzgSFUDSTZRy50MrCmF5HyLnKhUq6Zth3cTOHzXwTobRQ8nU&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=1Yn5kipzbGwZrQ79ue_f3A&_nc_ss=7b289&oh=00_Af7GRx-LPQCe9FHMrR4KOZU6ClUDhOZH-62BAeC9n8R9zQ&oe=6A1BFFA1)

Once you have been approved for the oEmbed Read feature you may embed your own pages, posts, or videos using their respective URLs.
