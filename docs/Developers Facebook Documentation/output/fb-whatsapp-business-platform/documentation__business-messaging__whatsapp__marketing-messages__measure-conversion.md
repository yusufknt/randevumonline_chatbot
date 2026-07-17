# Setting up conversion measurement | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/measure-conversion_

---

# Setting up conversion measurement

Updated: Apr 20, 2026

Using Marketing Messages API for WhatsApp, you can integrate your marketing messages with events, allowing you to measure the rate and cost at which a Marketing message sent via Marketing Messages API for WhatsApp leads to a downfunnel event like “purchase” on your website or app.

Conversion measurement is built on the same events that you can send to Meta when using Ads, making it seamless for businesses who are already integrated with Events for Ads purposes (for example, via Pixel or Conversions API for websites, or Meta SDK in their mobile app), to leverage the same reporting automatically with no setup.

If a business is using both marketing messages on Marketing Messages API for WhatsApp and Ad Campaigns on the same business portfolio, conversion events reported will be automatically attributed to the last Meta touch (either Marketing Messages API for WhatsApp click or Ad click) before the event, based on the attribution window settings of each. For example, if a business is running both an Instagram Ad campaign and a Marketing message campaign on MM API for WhatsApp, each with a URL pointing to the same website for a sale, a user who purchases after clicking on both the Instagram Ad and the Marketing message will be attributed to either the MM API for WhatsApp click or the Ad click, based on the attribution window settings of each. This helps businesses better understand the holistic picture of their Ad and Marketing message campaigns in driving outcomes.

## Understanding linked Ad entities

When a business registers for Marketing Messages API for WhatsApp, read-only Ad accounts are created under their business portfolio, which are synced to each WhatsApp Business Account under the same portfolio. Note that marketing messages are separate and distinct from Ads - the use of “Ads” terminology below represents the use of Ads entities as technical constructs only.

No action is needed on the part of the business or partner - these linked read-only Ad accounts are kept in sync with any changes made to Marketing templates, so that any new or updated marketing templates are reflected by their linked ad entity.

Linking Marketing templates to Ad accounts provides several benefits:

**Common UI and API for marketing teams:** Businesses can view their Marketing Messages API for WhatsApp marketing campaigns and campaign metrics as “Campaigns” in Ads Manager’s “Marketing Messages” tab, and via API using the Marketing API “[Insights API](https://developers.facebook.com/documentation/ads-commerce/marketing-api/insights)”. Using these interfaces helps a business’ marketing teams view their Ads and Marketing message campaigns using common interfaces and terminology, instead of viewing Ad campaigns in one place and marketing campaigns sent via WhatsApp in another.

- **New metrics:** The Ads Manager UI and Insights API report new Conversion metrics (for example, Web, App) that Cloud API and the Business Management API do not support. When Marketing template messages sent via MM API for WhatsApp lead to Conversion events (for example, add to cart, purchase) that a business reports from their website or app, these conversion events are attributed to the Marketing message and are shown in metrics, leading to a better understanding of Marketing message ROI. Reporting events is done via integration with Pixel or Conversions API for Web and App Events and the Meta SDK.

## Template-to-Ad-sync guidelines

- Marketing templates map to Ads only once during initial onboarding to Marketing Messages API for WhatsApp.
- Syncs must be completed for templates to display correct app conversion metrics.
- Ads syncing can take up to 10 minutes.
- Avoid sending messages with new templates before syncing completes to prevent errors or loss of optimization and tracking.
- Existing templates prior to initial onboarding will not have conversion metrics enabled.
- To reactivate unused templates for over 7 days: Send one message using the template and wait 10 minutes for Ad sync to re-activate.

![Diagram showing template-to-Ad sync flow](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/476235279_4018761408406419_4409302645887282875_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=X6et4Y-asaYQ7kNvwEbSfhi&_nc_oc=Adqnbf79NvR7jh0-w_opod-4GmuoUeOIWUTuVnFkrHDjHt6Yns2UZ2m9dWAGRu_klC4&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=9vg72tqvf4E8ct7zLguGsw&_nc_ss=7b20f&oh=00_Af7MYE8TqWBDJUskmUoxpHLI9aVG_N8tgn_KItGzlpShkg&oe=6A1C2E8B)

## Understanding automatic objective setting

In order to measure Conversion events, Marketing Messages API for WhatsApp automatically syncs Marketing templates to corresponding Ads entities (Campaigns, Message sets, and Ads) with configurations that allow for Conversion reporting of an assumed objective.

This linking process happens automatically, to reduce the integration complexity of Marketing Messages API for WhatsApp for businesses. For those familiar with Meta’s Ads ecosystem, note that these Campaign and Ad Set parameters will not change how messages are delivered via Marketing Messages API for WhatsApp - they are only set so that reported events can be correctly attributed.

The following table shows how Marketing templates are mapped to Ads entities.

|  | Campaign parameters | Message Set parameters |
| --- | --- | --- |
| Marketing templates with no CTA URL button | Objective:OUTCOME_SALES | OptimizationGoal: Impression |
| Marketing templates with a CTA URL button that points to a website or app without event reporting enabled. | Objective:LINK_CLICKS | OptimizationGoal: LinkClicks |
| Marketing templates with a CTA URL button that points to a website or app with event reporting enabled. | Objective:LINK_CLICKS | OptimizationGoal: OffsiteConversion |

- Event reporting is detected by whether the URL points to a website or app which the same business portfolio has enabled for event reporting via Pixel, Conversions API, or Meta SDK.

While most changes to Templates will be automatically synced with Ads (for example, text content), Campaign and Message set parameters are synced only once when a business first onboards to Marketing Messages API for WhatsApp or creates a new Template, in order to maintain a consistent campaign and message set structure when reporting on clicks and conversions from messages sent using that Template. This means that if you wish to add, edit, or remove a URL from a CTA button on a Template, you must create a new Template in order to correctly capture click and conversion metrics for the updated URL.

## URL requirements for conversion measurement

Meta appends a click ID to the URLs you send in CTA buttons on marketing template messages. The purpose of the click ID is to attribute events you report via Meta Pixel, Conversions API (web or app events), or the Meta SDK.

The click ID is Meta-generated and is commonly attached as the `fbclid` query parameter.

Example URL with `fbclid` query parameter:

```
https://www.jaspersmarket.com/?fbclid=IwAR2F4-dbP0l7Mn1IawQQGCINEz7PYXQvwjNwB_qa2ofrHyiLjcbCRxTDMgk
```

### URL compatibility (short links, redirects, and URL rewriting)

Some short-link and redirect services can interfere with conversion measurement if they strip, overwrite, or fail to forward query parameters that Meta appends. If you use a short-link provider or URL rewriting service, ensure it preserves all query parameters end-to-end.

**Example where fbclid is dropped:**

- You configure your CTA destination as: `https://www.jaspersmarket.com/checkout?campaign=whatsapp_template`
- Your link partner rewrites it to a short link that redirects to your site: `https://www.example.com/jaspersmarket`
- Before sending, Meta appends a click ID to the short link: `https://www.example.com/jaspersmarket?fbclid=xyz789`
- When the user clicks, the short-link service redirects to your site but drops the query string, sending the user to: `https://www.jaspersmarket.com/checkout?campaign=whatsapp_template` (missing `fbclid=xyz789` )

The click ID is not preserved through the redirect, which can reduce Meta’s ability to attribute conversions to the originating click.

### URL parameter ordering issues

Appending additional query parameters after the `fbclid` parameter can cause redirection issues on some platforms. If your system adds custom parameters to a URL, ensure that the `fbclid` parameter is not disrupted or truncated by subsequent parameters. Test the full URL (with all parameters) to confirm that the destination resolves correctly and that `fbclid` is accessible to your site or app.

### Recommendations

If you use short links or redirects:

- Test that the final URL retains all query parameters (including `fbclid` ).
- Validate conversion reporting in Ads Manager and Insights API before sending production workloads.
- Avoid appending parameters after `fbclid` in ways that could disrupt the URL structure.

If you experience issues, work with your partner to ensure query parameters are preserved, or reach out to Meta with details.

## Android deep links for conversion measurement

Android routes deep links using intent filters declared by apps. A deep link URL has three parts:

- Scheme (for example, `https` , `myapp` ) — helps determine which app can open the link
- Path (for example, `/product/123` ) — the route inside the app
- Query parameters (for example, `?fbclid=...` ) — includes attribution data like `fbclid` , `campaignId` , `al_applink_data` , and others

When a user taps a deep link, Android:

- Finds apps with intent filters that match the URL (scheme/host/path).
- Creates an implicit Intent.
- Delivers it to the target Activity (often via `onCreate()` and/or `onNewIntent()` ), where the app must read the full URL (including query parameters).

Android passes the URL, but your app must explicitly capture and persist attribution parameters. If you don’t, they can be effectively “lost” after the first screen.

Attribution parameters like `fbclid` can be stripped, cached incorrectly, or not passed through as expected due to one or more of:

- Android intent resolution behavior (multiple handlers, re-launch behavior, or activity launch modes)
- How WhatsApp invokes app links (intermediary parsing and handoff to Android)
- Receiving app implementation gaps, for example: Only reading the URL in `onCreate()` but not `onNewIntent()`Not persisting the parameters for later use (install/deferred deep linking/session attribution)Redirecting internally and dropping query params when rebuilding a new URI

### Implementation checklist

To ensure the click ID works correctly, the receiving Android app should:

- Read the full URI from the incoming Intent Handle both cold start (`onCreate()`) and warm start/re-use (`onNewIntent()`)
- Extract attribution params (at minimum `fbclid` , and any others you rely on)
- Persist them for later conversion reporting/session attribution Store in a durable place (for example, `SharedPreferences` or a database) with a timestampRefresh if a newer value arrives (these identifiers can change over sessions)
- Do not drop query parameters when redirecting internally If your app converts a URI to an internal route, ensure you carry attribution params forward or persist them before routing

### Test deep link parameter preservation on Android

When you open a deep link that includes `fbclid`, your app should be able to log (or otherwise confirm) that it received the URI including `fbclid`, and that it persisted it for subsequent events.

Use a test link like:

```
myapp://some/path?fbclid=TEST123&campaignId=TESTCAMPAIGN
```

Or an `https://` app link equivalent if you support it.

Test using adb

You can simulate what Android does by sending an Intent yourself:

```
adb shell am start -W -a android.intent.action.VIEW \
  -d "myapp://some/path?fbclid=TEST123&campaignId=TESTCAMPAIGN"
```

Then confirm your app receives `fbclid` and persists it.

## Measure website conversions with Meta Pixel or Conversions API

Businesses who are reporting events from their website using Meta Pixel or Conversions API for web, can measure when clicking on a URL in a marketing message sent via Marketing Messages API for WhatsApp leads to a conversion event.

If a business is not yet reporting Offsite Conversion events from their website, see the following documentation to set up event reporting:

**Tutorial**: [Get started with the Meta Pixel and Conversions API](https://www.facebookblueprint.com/student/activity/212737)

Once a business is reporting events via Pixel or Conversions API, the following standard events are automatically associated with website visitors who arrived at the site via a CTA URL from a marketing message sent via MM API for WhatsApp:

- Add to cart
- Initiate checkout
- Purchase
- Purchase value

- Complete registration
- Add to wishlist
- Add payment info
- Search
- Lead
- View content
- Custom events

When a user clicks a CTA URL in a Marketing Messages API for WhatsApp message and performs any of the above events, Meta will automatically attribute the conversion event to the MM API for WhatsApp Campaign, and make those analytics available to you or your Partner via the Insights API, which your Partner may surface on their own reporting surfaces that you are accustomed to using.

Note that if this conversion event is also being used to measure the efficacy of Ads on Facebook or Instagram, Meta will attribute the conversion to the ‘last touch’ interaction of the user. For example, if a user arrives at your website via an ad on Facebook, and then closes their browser window and later that day returns to your website via clicking a link from a MM API for WhatsApp message and purchases an item, that purchase conversion event will be attributed to the MM API for WhatsApp campaign (and not the ad on Facebook) as the most recent interaction.

## Measure app conversions with Meta SDK or Conversions API

Businesses can use Marketing Messages API for WhatsApp to measure when marketing messages lead users to perform app events, such as purchases and app activations. See [Conversions API for App Events](https://developers.facebook.com/documentation/ads-commerce/conversions-api/app-events) for an introduction to app events.

The following app conversion events are available for MM API for WhatsApp:

- App Purchase
- App Purchase value
- App Add to cart
- App Initiate checkout
- App Activations

- App Complete registration
- App Add to wishlist
- App Add payment info
- App Level achieved
- App Rate
- App Tutorial completion
- App Search
- App View content
- App Other

Businesses can capture App conversion events in 3 ways. See [Conversions API for App Events](https://developers.facebook.com/documentation/ads-commerce/conversions-api/app-events) for more information.

1. Via the Meta SDK
2. Via the Conversions API
3. Via a 3rd party mobile measurement partner, who sends events to Meta on your behalf

### Using the Meta SDK

1. If your app is using Meta SDK, [upgrade](https://developers.facebook.com/documentation/android/upgrading-4x) your SDK version to Meta Android SDK v17.0.2 or above. Note iOS app measurement is currently not supported.
2. If your app is using a supported Mobile Measurement Partner (MMP), check with your MMP to get your app ready.
3. If your app is using Conversions API, learn how to [send campaign_ids parameters with app events](https://developers.facebook.com/documentation/ads-commerce/conversions-api/parameters/app-data#campaign-ids) . To get campaign_ids, you’ll need to parse `campaign_ids` from `al_applink_data parameters` from the deep link that the user clicked from.

Example deep link:

```https
exampleapp://applink/ad_landing_recommend?data={"goods_id":"39109246","page_type":"B"}&al_applink_data={"target_url":"https://www.exampleapp.com&fbclid=IwZXh0bgNhZW0BMAABHbKVD62Fa0uTdpAh6KZn16BmrnWgsTbZgiCEsKGLOcF9RDncEAsbJKWp0Q_aem_y0zBYthdxb0j9epvkZum7w","extras":{"fb_app_id":312563225523989},"referer_app_link":{"url":"fb:///?app_id=312563225523989","app_name":"Facebook"},"campaign_ids":"IwAR2rBBgtFjvI_IUUes4nZ6FcQ0dtqujIz1w9JIwrs1YKKn7tGIIqC4kKrXk_wapm_fVVosPGBQJWpvSW8Z8emXg_aem_pyDxR3ch5qDkVdd0Y138yg","ad_id":"1234567","adgroup_id":"1234567","campaign_id":"1234567","campaign_group_id":"1234567","account_id":"1234567"}
```

Make sure you have pixel/conversions set up for the fallback website URL as well.

### Via a 3rd party mobile measurement partner

Some mobile measurement platforms will automatically forward App conversion events to Meta on your behalf. No integration effort is needed on your part. See [Partner showcase](https://business.facebook.com/messaging/partner-showcase/)
