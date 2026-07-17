# Send Marketing Messages

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/send-marketing-messages_

---

# Send Marketing Messages

Updated: May 5, 2026

Marketing Messages API for WhatsApp allows you to send marketing template messages only. To send other message types or receive messages, use Cloud API in parallel with Marketing Messages API for WhatsApp on the same business phone number.

If you use a partner’s UI portals or APIs to configure and send marketing messages, you can continue to do so, and do not need to use any of the capabilities described in this document - your partner will take care of integrating with MM API for WhatsApp’s message sending functions on your behalf.

## Prerequisites

Before you can send marketing messages via Marketing Messages API for WhatsApp, ensure the following:

- A WhatsApp Business Account (WABA) with [MM API for WhatsApp onboarding](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/onboarding) complete
- At least one registered business phone number associated with your WABA
- At least one approved marketing template
- An access token with the `whatsapp_business_messaging` permission
- A Meta Pixel or Conversions API integration (required for [conversion measurement](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/measure-conversion) )

## Create marketing templates

You can create marketing templates in several ways:

1. Via WhatsApp Business Manager UI
2. Via the Business Management API “Message Templates” endpoint
3. If you work with a partner, your partner may offer their own API or user interfaces for template creation, which leverage the “Message Templates” endpoint

See documentation on how to [Create and manage templates](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview).

When you create a new marketing template, it takes up to 10 minutes to sync with the corresponding Ad account. This sync enables message optimization and measurement of clicks and downstream conversions.

Templates inactive for longer than 7 days also require 10 minutes to sync after first use. Wait 10 minutes after creating new marketing templates or reactivating dormant templates before sending marketing traffic.

Marketing Messages API for WhatsApp supports all marketing templates. In addition, Marketing Messages API for WhatsApp provides the following features that are not available to marketing templates on Cloud API:

- **Time-To-Live (TTL) for Marketing template messages:** If Meta is unable to deliver a message to a WhatsApp user, Meta will retry the delivery for a period of time known as a time-to-live, TTL, or the message validity period. TTL is available for Authentication and Utility template messages on Cloud API, but TTL for Marketing template messages is exclusively available on MM API for WhatsApp. See documentation on how to [Create and Manage Templates via API](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview#time-to-live--ttl---customization--defaults--min-max-values--and-compatibility) or [How to set a custom message validity period via UI](https://www.facebook.com/business/help/1305007343713790) for details on how to set TTLs for Marketing template messages.

## Automatic creative optimizations

Automatic creative optimizations test variations with different creative treatments and optimize marketing messages based on practices observed from high-performing creatives. You can disable them using the [template-level opt-out](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/send-marketing-messages#configure-automatic-creative-optimizations-template-level) or [WhatsApp Business Account-level opt-out](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/send-marketing-messages#configure-automatic-creative-optimizations-whatsapp-business-account-level), giving you flexibility and control over how creative enhancements are applied. These are similar to [Advantage+ creative](https://www.facebook.com/business/help/297506218282224?id=649869995454285) for ads.

Automatic creative optimizations like text extraction and highlighting have driven an average increase of 13.9%* in click-through rates (CTR).

This feature introduces creative variability for performance optimization, meaning the output may vary between messages even with the same input. This capability tests minor variations of your existing image header and automatically selects the variant getting the highest click-through rate over time, with no input needed from you. We are continuously exploring and testing new automatic creative optimizations to help maximize your campaign performance. As new variations become available, they may be applied to opted-in templates to drive better business results.

### Image filtering

For some campaigns, Meta automatically applies the most effective filters to header images in order to enhance the images’ quality and appeal:

![Example of automatic image filtering optimization](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/677529769_26661613513447780_7533727623640867902_n.png?_nc_cat=106&ccb=1-7&_nc_sid=e280be&_nc_ohc=uOcjwFjIj3sQ7kNvwG_kgMF&_nc_oc=AdoBeKfyp02XYKrDU-wWpOtLBAhlQAFlXljrdAbBO6f---u72eF0LTvL1JFgVzJyoBQ&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=xlv85iW3cqYy4WTZC5RWsA&_nc_ss=7b20f&oh=00_Af7vT6NsiDpd2SeqR-oAL9FIiBk1olle8xaOKMsiZZAc0A&oe=6A1C0114)

### Headline extraction

For some campaigns, Meta extracts keywords or phrases from your message to create a headline for your body text to highlight key information.

![Example of headline extraction from message content](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/568356332_1741218023258733_764318396409509397_n.png?_nc_cat=102&ccb=1-7&_nc_sid=e280be&_nc_ohc=WFL7DALSfcYQ7kNvwE7ujBd&_nc_oc=AdqRtFDNTGlgj6Z9A_u9lG86WfuXv0nBZEiif_kQ5iD5-5LJ1l0YcXqB-uCrBUDXMi8&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=xlv85iW3cqYy4WTZC5RWsA&_nc_ss=7b20f&oh=00_Af6Ovis15tktS8M2w9AcO1ogNyl-tL3jT3H6T42DYyz38A&oe=6A1C2E73)

### Tap-target title extraction

For some campaigns, Meta extracts keywords or phrases from your message to create a title for the tap-target area to highlight key information.

![Example of tap-target title extraction](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/565927808_1275784957569302_5821755358925562973_n.png?_nc_cat=110&ccb=1-7&_nc_sid=e280be&_nc_ohc=IrJISrzqNDIQ7kNvwG0wpBu&_nc_oc=AdqjQNtSIARXnuDHzMSForl1mpnAD9CFW6Dt0jxvZ7NAHdt58yGIXQDFWjpceBhyq-s&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=xlv85iW3cqYy4WTZC5RWsA&_nc_ss=7b20f&oh=00_Af74Ltd4U3eDG_6Z2jNsDol3X4NiSkQ6BJAvqRNW6uSwvg&oe=6A1C20BF)

### Text formatting

For some campaigns, Meta updates the formatting of text (for example, removing unnecessary spaces, bolding phrases) to increase performance and message digestibility. No text content is changed - format only.

![Example of text formatting optimization](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/571559956_1527237245143422_4708127400362964555_n.png?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=OpgRDfGI1SIQ7kNvwH_rBnC&_nc_oc=Adr8T2Azqi28iAc6JgTMz2Bp3nfkrSTSx57yEB1NxZzirgOleNcNaCJFCitSQXXR5fg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=xlv85iW3cqYy4WTZC5RWsA&_nc_ss=7b20f&oh=00_Af7VI8eYgUvu98GlXg7wbZ5lAJwZa-n9DZkxT6utAGMGBQ&oe=6A1C2274)

### Coming soon

We are continuously exploring and testing new automatic creative optimizations to help maximize your campaign performance. While we expect to make these enhancements available in the future, our plans are subject to change.

Product extensions

Meta enhances single-image creatives by appending a set of additional catalog products users are likely to engage or convert with, creating more personalized and relevant experiences.

![Example of product extensions with catalog items](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/571739475_802429889249611_5730968219809248185_n.png?_nc_cat=110&ccb=1-7&_nc_sid=e280be&_nc_ohc=KtLdpHw5zKMQ7kNvwHqNZ5q&_nc_oc=Adoy2cXejaOBi3FpMbfV5EWFyp32-kZpdUyImuKCxhkVB4kPSmARv1JEQbvIOoj2Uow&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=xlv85iW3cqYy4WTZC5RWsA&_nc_ss=7b20f&oh=00_Af7l3H8yabBcfFRlBanYS3jDIasGwLVggn3XDb5dYm0c1Q&oe=6A1C3024)

Auto promotion tag

For some campaigns, Meta will automatically extract the promotion tag, like “30% off”, “50% discount”, “Free shipping” from messages to create a promotion tag and put it into the image to highlight promotion information.

![Example of auto promotion tag](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/637942395_939879988503659_167364162728640941_n.png?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=0RSavklxu5YQ7kNvwGqAGU6&_nc_oc=Adr9p_Q1aHM3hOTyO7QiKEw6MdWXID_wqtiX8MPpqwAFW2NmHs1m_CN0Gs38Q6BHLX0&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=xlv85iW3cqYy4WTZC5RWsA&_nc_ss=7b20f&oh=00_Af7PtNKUN0yCHCpNbfzaUZTz9SGUhXsrABzrMAhN9YcK2A&oe=6A1C141A)

Image banner

For some campaigns, Meta will apply colorful paddings to transform the image creative to the optimal aspect ratio to enhance visual appeal and improve media digestibility.

![Example of image banner](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/653896851_955520363827866_5438895605954795647_n.jpg?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=RNvz4GvhV4kQ7kNvwHowKt2&_nc_oc=AdpK8R0mBXrxVTY2uUhXY-J4uaDE6cYHDejUQIfBcmGjBQFTgfIZhQGXGAWC16eHgrA&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=xlv85iW3cqYy4WTZC5RWsA&_nc_ss=7b20f&oh=00_Af4t3kOJmD-HMV1iklO9GxhnE_agFgnaQMI9897vtD2H9Q&oe=6A1C2CD7)

Dynamic CTA

For some campaigns, Meta will dynamically tailor CTA text to match the message or URL’s value prop, driving higher engagement through relevance.

![Example of dynamic CTA](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/677212286_854225160372759_4660251937918768355_n.png?_nc_cat=102&ccb=1-7&_nc_sid=e280be&_nc_ohc=Y4PsKLlqWBkQ7kNvwHg1QJ_&_nc_oc=Ado7Ui8kal8oTgzLm_eeA1t9jZNUHP8gbNSTdroMMrmX39dl-s15wwsV-ofDxACSdB8&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=xlv85iW3cqYy4WTZC5RWsA&_nc_ss=7b20f&oh=00_Af6LECTCLnZFDGqfCLc89xhYu4Az8oRhDNfugKdxNT9yYA&oe=6A1C08FE)

Hyperlink formatting

For some campaigns, Meta will detect meaningful promotional keyphrases (such as discounts, offers, and incentives) to convert into a hyperlink mapped to the CTA, or transform URL links in the message body by shortening the link or applying hyperlink formatting to adjacent keyphrases to improve message digestibility.

![Example of hyperlink formatting](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/674451038_956397106746830_2610563006647121618_n.png?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=i44LrO5TcIQQ7kNvwFlsU6M&_nc_oc=Adp83zM19s1p5fpZGPKuGWPAq7f3UIlLnycWZkupLftbgtuXfWoKMHmaM7LOFKqXLwE&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=xlv85iW3cqYy4WTZC5RWsA&_nc_ss=7b20f&oh=00_Af6bVSJs99ocht-RvXaISpIoVAv2YnkCKnFqX_ZlIfawyg&oe=6A1C22DE)

![Example of hyperlink formatting with link shortening](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/681141013_1278712087154990_8011007445621042379_n.png?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=jYuf0Z1att4Q7kNvwFqbheB&_nc_oc=AdrPiMvqTKvsFXhzrSQUwKK-r4UJoekl0DWkwSwhC0vQHhcMBurJyIxNplT1Y0eFYlY&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=xlv85iW3cqYy4WTZC5RWsA&_nc_ss=7b20f&oh=00_Af5iaUz-86-TFl9SbFe10Qs15VxEEs7ZhoVD1VNI3YUfQQ&oe=6A1C1515)

Profile end card

For some campaigns, Meta may append a business profile card at the end of a single-image marketing message, displaying WhatsApp business profile details to help WhatsApp users learn more about the sender and encourage engagement. The end card features publicly available details from a business profile, such as business category, short description, and website URL.

![Example of profile end card](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/689822816_2137893413421708_1844542132308630318_n.png?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=nRAER69e0QEQ7kNvwGPi77y&_nc_oc=AdrAYxRsnf058nxeThEluOZDDk0hR8gk8MKvyUsPxzL4Rjs6aE3fw9rsAOPLftsNaVE&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=xlv85iW3cqYy4WTZC5RWsA&_nc_ss=7b20f&oh=00_Af5PY75XRe2qucm3keG9R44eSAgnIBrHM-Ab4cZCyGJPCA&oe=6A1C2E85)

### Paused or deprecated

We have paused the following automatic creative optimizations, and you should not expect these to be applied to your marketing messages. We will update documentation if we restart any of these in the future:

- **Image cropping** : Meta automatically crops header images to an optimal dimension, ensuring your visuals are always perfectly framed without cutting off image text.
- **Text overlays** : Meta automatically adds a text overlay onto your image using your message content.
- **Image animation** : Meta automatically transforms your header image into an animated GIF.
- **Image background generation** : Meta automatically generates a new image background.

Footnotes

*This finding is based on an A/B test conducted with over 50 million delivered marketing messages sent by about 200 advertisers on MM API for WhatsApp between December 1, 2025, and January 7, 2026. It compared CTR for messages with automatic creative optimizations applied to messages without any applied, and the results were statistically significant at 95% confidence.

### Configure automatic creative optimizations (template-level)

All optimization features are enabled by default, but you can use the `creative_features_spec` object to specify which optimizations you want to enable (“opt-in”) or disable (“opt-out”) on a given template. To do this, set each optimization’s `enroll_status` property to either `OPT_IN` or `OPT_OUT` upon template creation, or when editing an existing template.

### Request syntax

Use the [Message Templates API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/template-api#post-version-waba-id-message-templates) to configure automatic creative optimizations at a template level.

```html
POST /<WHATSAPP_BUSINESS_ACCOUNT_ID>/message_templates
{
  "name": "<TEMPLATE_NAME>",
  "language": "<TEMPLATE_LANGUAGE_AND_LOCALE_CODE>",
  "components": [<TEMPLATE_COMPONENTS>],
  "degrees_of_freedom_spec": {
    "creative_features_spec": {
      "image_brightness_and_contrast": {
        "enroll_status": "OPT_OUT"
      },
      "image_touchups": {
        "enroll_status": "OPT_IN"
      },
      "add_text_overlay": {
        "enroll_status": "OPT_OUT"
      },
      "image_animation": {
        "enroll_status": "OPT_IN"
      },
      "image_background_gen": {
        "enroll_status": "OPT_IN"
      },
      "auto_promotion_tag": {
        "enroll_status": "OPT_IN"
      },
     "text_extraction_for_headline": {
       "enroll_status": "OPT_IN"
     },
     "text_extraction_for_tap_target": {
       "enroll_status": "OPT_IN"
     },
      "product_extensions": {
        "enroll_status": "OPT_OUT"
      },
      "text_formatting_optimization": {
        "enroll_status": "OPT_OUT"
      }
    }
  }
}
```

Use the [Template API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/template-api#get-version-template-id) to retrieve automatic creative optimizations statuses at a template level.

### Request syntax

```html
GET /<TEMPLATE_ID>?fields=degrees_of_freedom_spec
```

### Example response

```json
{
  "degrees_of_freedom_spec": {
    "creative_features_spec": [
      {
        "key": "IMAGE_BRIGHTNESS_AND_CONTRAST",
        "value": { "enroll_status": "OPT_OUT" }
      },
      {
        "key": "IMAGE_TOUCHUPS",
        "value": { "enroll_status": "OPT_OUT" }
      },
      {
        "key": "ADD_TEXT_OVERLAY",
        "value": { "enroll_status": "OPT_IN" }
      },
      {
        "key": "IMAGE_ANIMATION",
        "value": { "enroll_status": "OPT_OUT" }
      },
      {
        "key": "IMAGE_BACKGROUND_GEN",
        "value": { "enroll_status": "OPT_OUT" }
      },
      {
        "key": "AUTO_PROMOTION_TAG",
        "value": { "enroll_status": "OPT_OUT" }
      },
      {
        "key": "TEXT_EXTRACTION_FOR_HEADLINE",
        "value": { "enroll_status": "OPT_OUT" }
      },
      {
        "key": "TEXT_EXTRACTION_FOR_TAP_TARGET",
        "value": { "enroll_status": "OPT_OUT" }
      },
      {
        "key": "PRODUCT_EXTENSIONS",
        "value": { "enroll_status": "OPT_IN" }
      },
      {
        "key": "TEXT_FORMATTING_OPTIMIZATION",
        "value": { "enroll_status": "OPT_IN" }
      }
    ]
  },
  "id": "123456789"
}
```

### Configure automatic creative optimizations (WhatsApp Business Account-level)

All optimization features are disabled by default, but you can use the `creative_features_spec` object to specify which optimizations you want to enable (“opt-in”) or disable (“opt-out”) for the entire WhatsApp Business Account. To do this, set each optimization’s `enroll_status` property that you wish to modify to either `OPT_IN` or `OPT_OUT`.

### Request syntax

Use the [WhatsApp Business Account API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/whatsapp-business-account-api#post-version-waba-id) to configure automatic creative optimizations at a WhatsApp Business Account level.

```html
POST /<WHATSAPP_BUSINESS_ACCOUNT_ID>
{
  "degrees_of_freedom_spec": {
    "creative_features_spec": {
      "image_touchups": {
        "enroll_status": "OPT_IN"
      },
      "image_animation": {
        "enroll_status": "OPT_IN"
      },
      "image_brightness_and_contrast": {
        "enroll_status": "OPT_IN"
      },
      "add_text_overlay": {
        "enroll_status": "OPT_IN"
      },
      "image_background_gen": {
        "enroll_status": "OPT_IN"
      },
      "auto_promotion_tag": {
        "enroll_status": "OPT_IN"
      },
      "text_extraction_for_headline": {
        "enroll_status": "OPT_IN"
      },
      "product_extensions": {
        "enroll_status": "OPT_IN"
      },
      "text_extraction_for_tap_target": {
        "enroll_status": "OPT_IN"
      },
      "text_formatting_optimization": {
        "enroll_status": "OPT_OUT"
      }
    }
  }
}
```

### Request syntax

Use the [WhatsApp Business Account API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/whatsapp-business-account-api#get-version-waba-id) to retrieve automatic creative optimizations statuses at a WhatsApp Business Account level.

```html
GET /<WHATSAPP_BUSINESS_ACCOUNT_ID>?fields=degrees_of_freedom_spec
```

### Example response

```json
{
  "degrees_of_freedom_spec": {
    "data": [
      {
        "creative_features_spec": [
          {
            "image_brightness_and_contrast": "OPT_IN",
            "image_touchups": "OPT_IN",
            "add_text_overlay": "OPT_IN",
            "image_animation": "OPT_IN",
            "image_background_gen": "OPT_IN",
            "auto_promotion_tag": "OPT_IN",
            "text_extraction_for_headline": "OPT_IN",
            "product_extensions": "OPT_IN",
            "text_extraction_for_tap_target": "OPT_IN",
            "text_formatting_optimization": "OPT_IN"
          }
        ]
      }
    ]
  },
  "id": "1234567890"
}
```

## Other optimizations

### Text truncation

Meta truncates text to a specific line-count to increase performance. No text content is changed, the original text is still accessible through the “Read more” button. The exact line count truncation rules are as follows:

- **Messages without any CTA, but with a link in the message body** (overrides the below rules): truncated to 5 lines
- **Messages with a media header** ( [Image](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/image-messages) , [Video](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/video-messages) , [Document](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/document-messages) , [Location](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/components#media-header) , and [GIF](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/components#media-header) ): truncated to 3 lines
- **Messages without a header** (that is, [Text messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/components#body) ): truncated to 4 lines

## Send marketing template messages

Sending messages follows the same API payload syntax as Sending Messages on Cloud API, and requires the same permissions.

The `/marketing_messages` endpoint supports **only** marketing template messages for MM API for WhatsApp and Cloud API. All other message types (freeform, Authentication, Service, Utility) are not supported, and will produce an error.

Marketing messages will only be sent via MM API for WhatsApp when the business customer has met all [onboarding requirements](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/onboarding). If onboarding requirements are not met, the marketing messages will still be routed via Cloud API. You may disable the ability to route to Cloud API by setting the optional field `product_policy` to `STRICT`.

Note: You may still use the `/messages` endpoint to send marketing messages through the Cloud API, unless you have [disabled marketing messages on Cloud API](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/send-marketing-messages#disable-marketing-messages-on-cloud-api).

| Endpoint | Authentication |
| --- | --- |
| `/PHONE_NUMBER_ID/marketing_messages` | Developers can authenticate their API calls with the access token generated in the **App Dashboard > WhatsApp > API Setup**.<br>If you are a business messaging service provider, you must authenticate with an access token with the `whatsapp_business_messaging` permission. |

### Request syntax

```html
POST /<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>/marketing_messages
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "<WHATSAPP_USER_PHONE_NUMBER>",
  "type": "<MESSAGE_TYPE>",
  "<MESSAGE_TYPE>": {
    <MESSAGE_CONTENTS>
  },
  <!-- Optional -->
  "product_policy": "<PRODUCT_POLICY>",
  "message_activity_sharing": <SHARE_MESSAGING_ACTIVITY?>
}
```

MM API for WhatsApp provides the following additional features that are not available to Marketing template messages on Cloud API:

- **Product fallback policy:** Set `product_policy` to `CLOUD_API_FALLBACK` to have the API send the outgoing message via Cloud API, if [onboarding requirements](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/onboarding) have not been met. Set to `STRICT` if you do not want the API to fallback to sending the message via Cloud API.
- **Message activity sharing:** `message_activity_sharing` is an optional parameter at the message level that enables or disables sharing message activities (for example, message read) for that specific marketing message to Meta to help optimize marketing messages. If this parameter is not provided, the default WABA-level setting will be applied. You can always edit your default setting in Business Settings (see Changelog for a screenshot of this).

For details on message types, reference the Cloud API [Message Types documentation](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages#message-types), as MM API for WhatsApp uses the same message send formatting.

### Sending to a BSUID (business-scoped user ID)

Marketing Messages API for WhatsApp supports sending messages using a phone number, a BSUID (or parent BSUID), or both. Sending to phone numbers is recommended where available, primarily so you continue to receive phone numbers in webhooks. See [Business-scoped user IDs](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-scoped-user-ids) for an overview of BSUIDs.

Request

```html
curl 'https://graph.facebook.com/<API_VERSION>/<BUSINESS_PHONE_NUMBER_ID>/marketing_messages' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <ACCESS_TOKEN>' \
-d '
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "<USER_PHONE_NUMBER>",
  "recipient": "<BSUID>",
  "type": "template",
  "template": {
    <EXPECTED_TEMPLATE_PARAMETERS>
  }
}'
```

Field reference

| Field | Change | Description |
| --- | --- | --- |
| `to` | Now optional | WhatsApp user phone number (individual) or group ID (group). If provided, takes precedence over<br>`recipient`<br>. |
| `recipient` | New (optional) | User BSUID or parent BSUID for individual messages. Used only when<br>`to`<br>is omitted. |

Precedence and validation

- At least one of `to` or `recipient` must be provided. Requests omitting both fail.
- If both are provided, `to` (phone number) is used for processing and delivery, and `recipient` is ignored.
- Sending by BSUID disables Marketing Messages Lite API delivery optimization for that send. See [limitations](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/send-marketing-messages#limitations-when-sending-by-bsuid) below.

Response

The response adds a `user_id` field and changes the semantics of `input` and `wa_id`:

```html
{
  "messaging_product": "whatsapp",
  "contacts": [
    {
      "input": "<USER_PHONE_NUMBER_OR_BSUID>",
      "wa_id": "<USER_PHONE_NUMBER>",
      "user_id": "<BSUID>"
    }
  ],
  "messages": [
    {
      "id": "<WHATSAPP_MESSAGE_ID>"
    }
  ]
}
```

| Field | Description |
| --- | --- |
| `input` | The user’s phone number if the message was sent by phone number, the user’s BSUID (or parent BSUID) if sent by BSUID, or the group ID if sent to a group. |
| `wa_id` | The user’s phone number. Omitted when the message was sent using a BSUID. |
| `user_id` | The user’s BSUID (or parent BSUID) when the message was sent using a BSUID. Omitted when only a phone number is provided or when both phone number and BSUID are provided. |

Example — send to phone number

```json
{
  "messaging_product": "whatsapp",
  "contacts": [
    { "input": "+16505551234", "wa_id": "16505551234" }
  ],
  "messages": [
    { "id": "wamid.HBgLMTY0NjcwNDM1OTUVAgARGBI1RjQyNUE3NEYxMzAzMzQ5MkEA" }
  ]
}
```

Example — send to BSUID

```json
{
  "messaging_product": "whatsapp",
  "contacts": [
    {
      "input": "US.13491208655302741918",
      "user_id": "US.13491208655302741918"
    }
  ],
  "messages": [
    { "id": "wamid.HBgLMTY0NjcwNDM1OTUVAgARGBI1RjQyNUE3NEYxMzAzMzQ5MkEA" }
  ]
}
```

Example — when both phone number and BSUID are omitted

```json
{
  "error": {
    "message": "The parameter to is required.",
    "type": "OAuthException",
    "code": 100,
    "fbtrace_id": "ANPlYYIqhnaWG-FIJ-rABkS"
  }
}
```

### Limitations when sending by BSUID

- **Delivery optimization is not applied.** Marketing Messages Lite API delivery optimization does not run for sends addressed by BSUID.
- **Dynamic pricing (`bid_spec`) is not supported with BSUID recipients.** Sending a marketing template that includes `bid_spec` to a BSUID recipient returns error `131062` . To use `bid_spec` , send to the user’s phone number, or use a template without `bid_spec` .

### Error: `131062` — BSUID recipients not supported for this message

| Field | Value |
| --- | --- |
| **Code** | `131062` |
| **Type** | `OAuthException` |
| **Message** | “Business-scoped User ID (BSUID) recipients are not supported for this message.” |

This error is returned when:

- The template uses `bid_spec` (dynamic pricing) and the recipient is a BSUID.
- An authentication template is sent to a BSUID recipient.

```json
{
  "error": {
    "message": "(#131062) Business-scoped User ID (BSUID) recipients are not supported for this message.",
    "type": "OAuthException",
    "code": 131062,
    "error_data": {
      "messaging_product": "whatsapp",
      "details": "The template specified in the request uses bid_spec, which is not supported for Business-scoped user ID (BSUID) recipients. To send this template, please provide the phone number of recipients or use a template without the bid_spec field."
    }
  }
}
```

## Disable marketing messages on Cloud API

If your business has onboarded to MM API for WhatsApp, you can disable the ability to send Marketing category templates through the Cloud API `/messages` endpoint. When this option is activated, the `/messages` endpoint rejects Marketing category templates. You can decide whether to send marketing messages through the `/marketing_messages` endpoint or disable this option.

This setting has no effect on WhatsApp Business Accounts (WABAs) that have not started the MM API for WhatsApp onboarding process; it only takes effect on WABAs that have fully onboarded. WABAs that have started the onboarding process but have not signed the Terms of Service (ToS) may experience blocked marketing messages, as described in [Fallback behavior on `/marketing_messages`](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/send-marketing-messages#mm-api-fallback-behavior).

### Request syntax

Use the [WhatsApp Business Account API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/whatsapp-business-account-api#post-version-waba-id) to enable or disable marketing messages on Cloud API.

```html
POST /<WHATSAPP_BUSINESS_ACCOUNT_ID>
{
  "disable_marketing_messages_on_cloud_api": true | false
}
```

Set `disable_marketing_messages_on_cloud_api` to `true` to block Marketing category templates on the Cloud API `/messages` endpoint. Set to `false` to allow Marketing category templates on Cloud API (default).

### Example request

The following request disables marketing messages on Cloud API for the specified WhatsApp Business Account.

```curl
curl 'https://graph.facebook.com/v25.0/102290129340398' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "disable_marketing_messages_on_cloud_api": true
}'
```

### Example response

```json
{
  "id": "102290129340398"
}
```

### Request syntax

Use the [WhatsApp Business Account API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/whatsapp-business-account-api#get-version-waba-id) to check the current value.

```html
GET /<WHATSAPP_BUSINESS_ACCOUNT_ID>?fields=disable_marketing_messages_on_cloud_api
```

### Example response

```json
{
  "disable_marketing_messages_on_cloud_api": true,
  "id": "102290129340398"
}
```

### Error response

If `disable_marketing_messages_on_cloud_api` is set to `true` and you attempt to send a Marketing category template through the Cloud API `/messages` endpoint, the API returns the following error:

```json
{
  "error": {
    "message": "(#131063) Marketing templates disabled for Cloud API",
    "type": "OAuthException",
    "code": 131063,
    "error_data": {
      "messaging_product": "whatsapp",
      "details": "Your template is categorized as Marketing, but marketing templates are currently disabled for your Cloud API configuration. To send this template, use the Marketing Messages API for WhatsApp or enable marketing templates on Cloud API by turning off disable_marketing_messages_on_cloud_api."
    },
    "fbtrace_id": "ABzNMWIqsLJ7hbj8xd5ytay"
  }
}
```

### Fallback behavior on `/marketing_messages`

When `disable_marketing_messages_on_cloud_api` is set to `true`, the fallback to Cloud API for the `/marketing_messages` endpoint is also affected:

- **MM API ToS signed** : The `/marketing_messages` endpoint works normally. No change in behavior.
- **MM API ToS not signed** : Marketing template messages sent to `/marketing_messages` would normally fall back to Cloud API, but the fallback is now rejected with error `131063` because the opt-in blocks marketing templates on Cloud API.

To avoid this error, ensure your WABA has completed all [onboarding requirements](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/onboarding) before enabling this setting.

**Note:** When the per-message `product_policy` is set to `STRICT`, no fallback to Cloud API is attempted regardless of the `disable_marketing_messages_on_cloud_api` setting. The fallback behavior described above only applies when `product_policy` is set to the default of `CLOUD_API_FALLBACK`.

### Re-enable marketing messages on Cloud API

To restore the ability to send Marketing category templates through the Cloud API `/messages` endpoint, set `disable_marketing_messages_on_cloud_api` to `false`:

```curl
curl 'https://graph.facebook.com/v25.0/102290129340398' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "disable_marketing_messages_on_cloud_api": false
}'
```

This restores the default behavior — Marketing category templates are accepted on the `/messages` endpoint again.

## Receiving message status webhooks

MM API for WhatsApp triggers status [messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/status) webhooks (sent, delivered, read). In addition, status messages webhooks that describe a message sent via MM API for WhatsApp, and that include pricing information, will have `pricing.category` and `conversation.type` set to `marketing_lite`. If the message is routed via Cloud API, `pricing.category` will be set to `marketing`.

```https
{
  "conversation": {
    "id": "<CONVERSATION_ID>",
    "origin": {
      "type": "marketing_lite"
    }
  },
  "pricing": {
    "billable": true,
    "pricing_model": "PMP",
    "category": "marketing_lite"
  }
}
```

Maintain logs of each outgoing message ID, and whether that ID was sent via Cloud API or MM API for WhatsApp, in order to use the unique message ID returned in message status webhooks to identify the origin of the sent message.

## Receiving incoming messages

MM API for WhatsApp is a send-only API. It does not receive incoming messages from consumers. To receive incoming messages on a business phone number, use Cloud API in parallel with MM API for WhatsApp on the same phone number.
