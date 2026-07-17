# Link Previews | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/link-previews_

---

# Link Previews

Updated: Nov 5, 2025

WhatsApp supports link previews when the link is sent via chat or shared via status. WhatsApp will attempt to perform a link preview when possible for a better user experience. To enable this experience, WhatsApp relies on link owners to define properties that are specifically optimized for WhatsApp. Not meeting these requirements may risk the link to be not previewed.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/316961531_1509723012881470_8719776711697314858_n.png?_nc_cat=106&ccb=1-7&_nc_sid=e280be&_nc_ohc=E6ZfqLkPUfkQ7kNvwGbWb1w&_nc_oc=AdrOKPlqTZndXRiTQVns3ZHDJGPQwgI9QAnn26xu4XBtnYE628C7kJpYu0Ge-C7s0GM&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=izgbLsNLv1XgM3Bpjr95Rw&_nc_ss=7b20f&oh=00_Af6tRgfebAeeQdM1P2z2Nukoc2SBZomAZlap0q3irAT09g&oe=6A1C2EE4)

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/316956074_903853424360664_8885274580316527555_n.png?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=x6EkoU8UKbgQ7kNvwFcOalE&_nc_oc=AdpHEv0h783WhBTSWWXqjP2L4p9QGu9MEp-rfrZU2f1Ae9C7ns5Q7hBY3CU8m0Adn2I&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=izgbLsNLv1XgM3Bpjr95Rw&_nc_ss=7b20f&oh=00_Af7re6u9pmWXTzBesMCFXa1VLx98pDn0R1XiPWiBf699Jw&oe=6A1C12AF)

## Get Started

To get started with enabling link previews, websites need to add HTML mark-ups to the HEAD section on the page.

```html
<head>
  <meta property="og:title" content=”WhatsApp"/>
  <meta property="og:description" content="Simple. Secure. Reliable messaging."/>
  <meta property="og:url" content="https://whatsapp.com"/>
  <meta property="og:image"content="https://static.whatsapp.net/rsrc.php/ym/r/36B424nhiL4.svg"/>
</head>
```

The `<head>` containing the HTML mark-ups must appear within the first 300KB of the HTML. The entire HTML does not need to fit within 300KB.

The `<og:title>`, `<og:description>` and `<og:url>` mark-ups must be inside the `<head>` tag. They should not be empty.

The `<og:title>` mark-up represents the title of the content without any branding. WhatsApp will display this in primary text color, in bold and in at most 2 lines.

The `<og:description>` mark-up represents the description of the content. WhatsApp will display this in a smaller size than the title and in secondary text color. It is limited to 1 or 2 lines and 80 characters will suffice.

The `<og:url>` mark-up represents the canonical URL of the page. The URL should be undecorated, without session variables, user identifying parameters and counters.

The `<og:image>` mark-up is an absolute URL for an image used as the thumbnail for the link preview. This image should be under 600KB in size. Image should be 300px or more in width with 4:1 width/height or less aspect ratio.

WhatsApp will make the best attempt to show link previews, eg: relaxing requirements, looking for other HTML mark-ups and reverting to small link previews. However, this should not be relied on. It’s not guaranteed to work (and continue to work).

WhatsApp crawls the web page via an HTTP GET request.

The request will have the `User-Agent` header set to `WhatsApp/2.x.x.x A|I|N`, where `x` are major/minor numeric versions of WhatsApp and `A|I|N` is for Android, iOS and web respectively. Some examples of valid `User-Agent` header values: `WhatsApp/2.22.20.72 A`, `WhatsApp/2.22.19.78 I`, `WhatsApp/2.2236.3 N`. Web site owners can identify such incoming requests and can customize the content (mark-ups and images) accordingly.

The request will also have the `Accept-Language` header set to the language selected by the recipient, if any. Some examples of valid `Accept-Language` header values are: `en` , `fr`, `de`. Similarly, web site owners can customize the content language accordingly. Note that the language set by the recipient will also be seen by the recipient.

## How to verify?

Start with composing a message with the link to test (not tap to send yet). On behalf of the sender, WhatsApp will crawl this URL and attempt to generate a link preview.

If a preview does not come up above the composer box after 10 seconds, please check all the requirements above are met. Else, continue with sending the message by tapping the “send” button.

If a preview does not show up in the expected large size, please check the image requirements above are met. Else, link previews are all working as expected. Congratulations, you’re all set!
