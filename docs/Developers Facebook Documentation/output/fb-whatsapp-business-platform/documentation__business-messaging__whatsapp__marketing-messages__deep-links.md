# Deep links | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/deep-links_

---

# Deep links

Updated: Feb 10, 2026

You can map an [Android deep link](https://developer.android.com/training/app-links/deep-linking) to a marketing template URL button that, when tapped, loads a particular location or content within your app.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/499229465_1266088541526902_7472965918950036987_n.png?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=Rqixcd4wYqUQ7kNvwFILDhz&_nc_oc=Adpdlr9JH4OEtVnsqN3d4yHlrgaZaHWTs9bG-wg9ivKL--e9FWyX-4t4L5HqWDYaeo0&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=dPJIAMcnF_c5Ly6mTu7MdQ&_nc_ss=7b20f&oh=00_Af4699eVl_FRaZkDkpEArsbuTNwAC8ZOhGzmTxOjQHsvcA&oe=6A1C0EC5)

If you have not onboarded to the Marketing Messages API for WhatsApp (MM API for WhatsApp), your marketing templates will not display any conversion metrics. Learn more about how to [measure conversion](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/measure-conversion).

## Template creation via WhatsApp Manager

To create a template with a button mapped to an Android deep link:

1. Access [WhatsApp Manager](https://business.facebook.com/latest/whatsapp_manager/) .
2. Navigate to the **Message templates** > **Manage templates** panel and click the **Create template** button.
3. Select **Marketing** (tab) > **Custom** (radio button) and click the **Next** button.
4. In the **Buttons** section, click the **+ Add buttons** dropdown menu and select **Visit website** .
5. Check the **Track app conversions** checkbox to reveal the deep link fields (pictured below).
6. Complete each field using their tooltips or [form field](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/deep-links#form-fields) descriptions below as guidance.
7. Add any additional components you’d like your template to use, name your template, and submit it for approval.

Note that you can also use the **Manage templates** panel to edit an existing template and add a deep link-mapped button, but the template will have to undergo template review again.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/524030257_747636164413080_2609413167857336367_n.png?_nc_cat=101&ccb=1-7&_nc_sid=e280be&_nc_ohc=bpOaVXVZM5wQ7kNvwEDKciV&_nc_oc=AdpSjRzCEskxBNW5bx7EjHCDTtOGL2FXB7kbCUehyD-uhECqtyX0xHImnSohyAvT-aE&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=dPJIAMcnF_c5Ly6mTu7MdQ&_nc_ss=7b20f&oh=00_Af5KS-BL5jkk_YRcvwPVc9aNyjTju37Iek_lMMXDE0XzWQ&oe=6A1C03D2)

### Form fields

| Field label | Description | Example value |
| --- | --- | --- |
| Android deep link | **Required.**<br>Android deep link URI. | luckyshrub://deals/summer_solstice |
| Android fallback URL | **Optional.**<br>Fallback URL.<br>If the WhatsApp client cannot load the deep link URI, the client will load this URL in the device’s default web browser.<br>If omitted, the client will attempt to load the URL specified in the Website URL field instead. | https://www.luckyshrub.com/deals/summer_solstice |
| Button Text | **Required.**<br>Button label text.<br>Maximum 25 characters. | View deal |
| Meta app ID | **Required.**<br>This is a list of the Meta app(s) associated with your business portfolio. Select the app whose access token you will use to send the template. | Lucky Shrub (634974688087057) |
| Type of Action | Required.<br>Must be set to **Visit website**. | Visit website |
| URL Type | **Required.**<br>Set to **Static** if your Android deep link or Android fallback URL has no dynamic values, otherwise set to **Dynamic**. | Static |
| Website URL | **Required.**<br>URL of a website to load if the WhatsApp user views the message on a non-Android device, or if the WhatsApp client cannot load your Android deep link URI and no Android fallback URL is specified. | https://www.luckyshrub.com/ |

## Template creation via API

Use the [Message Templates API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/template-api#post-version-waba-id-message-templates) to create the template and include a URL button component mapped to your Android deep link.

Note that you can also use the [Template API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/template-api#post-version-template-id) to edit an existing template and add a URL button component, but the template will have to undergo template review again.

### Request syntax

Template components can vary based on your needs. This example syntax creates a marketing template with the following components:

- **text header** , without parameters
- **body** , without parameters
- **URL button** , mapped to a deep link URI and fallback URL

```html
'https://graph.facebook.com/<API_VERSION>/<WHATSAPP_BUSINESS_ACCOUNT_ID>/message_templates' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <ACCESS_TOKEN>' \
-d '
{
  "name": "<TEMPLATE_NAME>",
  "language": "<TEMPLATE_LANGUAGE>",
  "category": "marketing",
  "components": [
    {
      "type": "header",
      "format": "text",
      "text": "<HEADER_TEXT>"
    },
    {
      "type": "body",
      "text": "<BODY_TEXT>"
    },
    {
      "type": "buttons",
      "buttons": [
        {
          "type": "url",
          "text": "<BUTTON_LABEL_TEXT>",
          "url": "<BUTTON_URL>",
          "app_deep_link": {
            "meta_app_id": <META_APP_ID>,
            "android_deep_link": "<ANDROID_DEEP_LINK>",
            "android_fallback_playstore_url": "<FALLBACK_URL>"
          }
        }
      ]
    }
  ]
}'
```

### Request parameters

| Placeholder | Description | Example value |
| --- | --- | --- |
| `<ACCESS_TOKEN>`*String* | **Required.**[System token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens) or [business token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens). | `EAAJB...` |
| `<ANDROID_DEEP_LINK>`*String* | **Required if using a URL button component mapped to a deep link.**[Android deep link](https://developer.android.com/training/app-links/deep-linking) URI. The WhatsApp client will attempt to load this URI if the WhatsApp user taps the button on an Android device. | `luckyshrub://deals/summer/` |
| `<API_VERSION>`*String* | **Optional**<br>Graph API [version](https://developers.facebook.com/docs/graph-api/guides/versioning). | `v22.0` |
| `<BODY_TEXT>`*String* | **Required if using a body component.**<br>Template body text. Variables are supported.<br>Maximum 1024 characters. | `Beat the heat with our sizzling summer deals on succulents! At Lucky Shrub, we...` |
| `<BUTTON_LABEL_TEXT>`*String* | **Required if using a URL button component.**<br>Button label text.<br>Maximum 25 characters. | `View Deals` |
| `<BUTTON_URL>`*String* | **Required if using a URL button component.**<br>URL of a website that the WhatsApp client will attempt to load in the device’s default web browser when the button is tapped.<br>For deep links, this URL only be used if the WhatsApp user taps the button on a non-Android device. | `https://www.luckyshrub.com/deals/summer/` |
| `<FALLBACK_URL>`*String* | **Required if using a URL button mapped to a deep link.**<br>URL of a website that the WhatsApp client will attempt to load in the device’s default web browser when the button is tapped but unable to load the Android deep link URI. | `https://www.luckyshrub.com/deals/summer/` |
| `<HEADER_TEXT>`*String* | **Required if using a text header component.**<br>Template header text string.<br>Supports up to 1 parameter. If this string contains a parameter, you must include an `example` property.<br>Maximum 60 characters. | `Sizzling Summer Deals at Lucky Shrub` |
| `<META_APP_ID>`*Integer* | **Required if using a URL button mapped to a deep link.**<br>Your Meta app ID. | `634974688087057` |
| `<TEMPLATE_LANGUAGE>`*String* | **Required.**<br>Template [language and locale code](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/supported-languages). | `en_US` |
| `<TEMPLATE_NAME>`*String* | **Required.**<br>Template name.<br>Maximum 512 characters. | `summer_deals_deep_link_v1` |
| `<WHATSAPP_BUSINESS_ACCOUNT_ID>`*String* | **Required.**<br>WhatsApp Business Account ID. | `102290129340398` |

## Example request

```curl
curl 'https://graph.facebook.com/v22.0/102290129340398/message_templates' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "name": "summer_deals_deep_link_v1",
  "language": "en_US",
  "category": "marketing",
  "components": [
    {
      "type": "header",
      "format": "text",
      "text": "Sizzling Summer Deals at Lucky Shrub"
    },
    {
      "type": "body",
      "text": "Beat the heat with our sizzling summer deals on succulents! At Lucky Shrub, we're passionate about bringing a touch of greenery to your life. Our succulents are not only low-maintenance and easy to care for, but they also add a pop of color and style to any room. Use the button below to see our Summer Steals!"
    },
    {
      "type": "buttons",
      "buttons": [
        {
          "type": "url",
          "text": "View Deals",
          "url": "https://www.luckyshrub.com/deals/summer/",
          "app_deep_link": {
            "meta_app_id": 634974688087057,
            "android_deep_link": "luckyshrub://deals/summer/",
            "android_fallback_playstore_url": "https://www.luckyshrub.com/deals/summer/"
          }
        }
      ]
    }
  ]
}'
```

## Viewing metrics

See our [Viewing metrics](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/view-metrics) document.
