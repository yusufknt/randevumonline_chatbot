# Automatic Events API | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/automatic-events-api_

---

# Automatic Events API

Updated: Nov 18, 2025

Business customers who access Embedded Signup can opt in to automatic event identification:

![Embedded Signup opt-in screen for automatic event identification](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/503425036_1029531339304862_7305936950282438326_n.png?_nc_cat=106&ccb=1-7&_nc_sid=e280be&_nc_ohc=pJFRKgGMKeQQ7kNvwEHmhgc&_nc_oc=Adqc4U2Cb7-FrKCA19s2Vml6VGspixyAZ3k9ARumqTNBgXrca1O8cDLpJbouinciaiQ&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=rsAgLrRRIPTGMgk34TZlZw&_nc_ss=7b20f&oh=00_Af5lB3mgvDmCIQgCmbrEAU20GiS_AdF-Du2etw4qCal2aQ&oe=6A1C088D)

If a business customer opts in, Meta use a combination of regex and natural language processing to analyze the customer’s new message threads originating from Click-to-WhatsApp ads. If our analysis determines that a lead gen or purchase event occurred, an [automatic_events](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/automatic_events) webhook is triggered, describing the event. You can then report the event for the customer using the [Conversions API](https://developers.facebook.com/documentation/ads-commerce/conversions-api) so the customer can use it on a Meta surface (in 2026, see [Limitations](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/automatic-events-api#limitations) below).

To learn more about how this feature works, see these [additional resources](https://meta.highspot.com/items/6839e4fecd0bb354418ee7ec).

## Limitations

- Automatic event identification is a new feature. Your business customers won’t see or use automatic events reported via Conversions API in Meta surfaces until 2026. However, you can surface this information to your customers using your own solution before then. This allows them to gain a deeper understanding of their own customers’ needs, preferences, and ad performance.
- Automatic event identification is not available to business customers in the European Union, United Kingdom, or Japan.

## Requirements

- You have already [implemented](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/implementation) Embedded Signup and are able to onboard business customers who complete the flow.
- Your [webhook server](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/create-webhook-endpoint) is successfully processing webhooks.

## Setup

Automatic event identification is available as an opt-in feature to all business customers automatically. To receive event notifications, you must subscribe your app to the **automatic_events** webhook field. However, as soon as you do this, you may begin receiving these webhooks before you can process them. Therefore, complete these steps using a test app before moving your code to production and subscribing your production app to the webhook field.

### Step 1: Subscribe to the automatic_events webhook field

Navigate to the [App Dashboard](https://developers.facebook.com/apps) > **Webhooks** > **Configuration** panel and subscribe to the [automatic_events](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/automatic_events) webhook field.

### Step 2: Adjust your webhook callback

Adjust your webhook callback code so that it can successfully process **automatic_events** webhook payloads.

Lead gen event structure

```html
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "<WHATSAPP_BUSINESS_ACCOUNT_ID>",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "<BUSINESS_DISPLAY_PHONE_NUMBER>",
              "phone_number_id": "<BUSINESS_PHONE_NUMBER_ID>"
            },
            "automatic_events": [
              {
                "id": "<WHATSAPP_MESSAGE_ID>",
                "event_name": "LeadSubmitted",
                "timestamp": <WEBHOOK_TRIGGER_TIMESTAMP>,
                "ctwa_clid": "<CLICK_ID>"
              }
            ]
          },
          "field": "automatic_events"
        }
      ]
    }
  ]
}
```

Lead gen event example

```json
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "102290129340398",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "15550783881",
              "phone_number_id": "106540352242922"
            },
            "automatic_events": [
              {
                "id": "wamid.HBgLMTIwNjY3NzQ3OTgVAgASGBQzQUY3MDVCQzFBODE5ODU4MUZEOQA=",
                "event_name": "LeadSubmitted",
                "timestamp": 1749069089,
                "ctwa_clid": "Afc3nYt4TTydumlFFsatFz8bR2yHCtVA92Veu_zDE4DgAI-QqCwM6eC3-K3lTGHRiLxRTVXFEsdyKQQSa-2obZyuGBq_EYypt_OwbMihBV0pbUoRmrGnEjwFTHop-Px0TfA"
              }
            ]
          },
          "field": "automatic_events"
        }
      ]
    }
  ]
}
```

Purchase event structure

```html
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "<WHATSAPP_BUSINESS_ACCOUNT_ID>",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "<BUSINESS_DISPLAY_PHONE_NUMBER>",
              "phone_number_id": "<BUSINESS_PHONE_NUMBER_ID>"
            },
            "automatic_events": [
              {
                "id": "<WHATSAPP_MESSAGE_ID>",
                "event_name": "Purchase",
                "timestamp": <WEBHOOK_TRIGGER_TIMESTAMP>,
                "ctwa_clid": "<CLICK_ID>",
                "custom_data": {
                  "currency": "<CURRENCY_CODE>",
                  "value": <AMOUNT>
                }
              }
            ]
          },
          "field": "automatic_events"
        }
      ]
    }
  ]
}
```

Purchase event example

```json
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "102290129340398",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "15550783881",
              "phone_number_id": "106540352242922"
            },
            "automatic_events": [
              {
                "id": "wamid.HBgLMTIwNjY3NzQ3OTgVAgARGBIwRkU4NDI5Nzk3RjZDMzE2RUMA",
                "event_name": "Purchase",
                "timestamp": 1749069131,
                "ctwa_clid": "Afc3nYt4TTydumlFFsatFz8bR2yHCtVA92Veu_zDE4DgAI-QqCwM6eC3-K3lTGHRiLxRTVXFEsdyKQQSa-2obZyuGBq_EYypt_OwbMihBV0pbUoRmrGnEjwFTHop-Px0TfA",
                "custom_data": {
                  "currency": "USD",
                  "value": 25000
                }
              }
            ]
          },
          "field": "automatic_events"
        }
      ]
    }
  ]
}
```

### Step 3: Trigger webhooks

To trigger an **automatic_events** webhook:

1. Access your test implementation of Embedded Signup.
2. Authenticate the flow using a business that has a Click-to-WhatsApp ad already configured.
3. In the [Business Asset Creation Screen](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/default-flow#business-asset-creation-screen) , check the **Instruct Meta to automatically identify order and lead events** checkbox, and complete the flow.
4. Access the Click-to-WhatsApp ad and click it to send a message to the business.
5. Use the business to reply to the message with one of the strings below (must be exact).

- **For a purchase event:** *Your tracking number is AB123456789BR*
- **For a lead gen event:** *I am interested in learning more about the product*

After you have triggered both **automatic_events** webhook payloads, confirm that your webhook callback has processed each webhook according to your business needs.

### Step 4: Report each event using Conversions API (optional)

You can optionally report each event using the [Conversions API](https://developers.facebook.com/documentation/ads-commerce/conversions-api/business-messaging). Include any relevant values from the event webhook, as appropriate.

See [Send events via Conversions API](https://developers.facebook.com/documentation/ads-commerce/conversions-api/business-messaging#send-events-via-the-conversions-api-2) for additional information about reporting events.

Lead gen syntax

```html
curl 'https://graph.facebook.com/<API_VERSION>/<DATASET_ID>/events' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <ACCESS_TOKEN>' \
-d '
{
  "data": [
    {
      "event_name": "LeadSubmitted",
      "event_time": <WEBHOOK_TRIGGER_TIMESTAMP>,
      "action_source": "business_messaging",
      "messaging_channel": "whatsapp",
      "user_data": {
        "ctwa_clid": "<CLICK_ID>"
      },
      "messaging_outcome_data": {
        "outcome_type": "automatic_events"
      }
    }
  ]
}
'
```

Purchase event syntax

```html
curl 'https://graph.facebook.com/<API_VERSION>/<DATASET_ID>/events' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <ACCESS_TOKEN>' \
-d '
{
  "data": [
    {
      "event_name": "Purchase",
      "event_time": <WEBHOOK_TRIGGER_TIMESTAMP>,
      "action_source": "business_messaging",
      "messaging_channel": "whatsapp",
      "user_data": {
        "ctwa_clid": "<CLICK_ID>"
      },
      "custom_data": {
        "currency": "<CURRENCY_CODE>",
        "value": <AMOUNT>
      },
      "messaging_outcome_data": {
        "outcome_type": "automatic_events"
      }
    }
  ]
}
'
```

## Enabling and disabling via Meta Business Suite

Business customers who have already been onboarded via Embedded Signup can enable automatic event identification using Meta Business Suite.

![A WhatsApp Business Account selected in the Meta Business Suite's settings panel, with the summary tab showing checkboxes for opting in.](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/503429874_596845240111750_4726469615509960636_n.png?_nc_cat=111&ccb=1-7&_nc_sid=e280be&_nc_ohc=8C4ww4oKMxwQ7kNvwHBAX5f&_nc_oc=AdpOzzSjiI5RcziyX07d3oES-hitMyLoStqUipWkauXHB4FUCVZsERZe1nVOp945A30&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=rsAgLrRRIPTGMgk34TZlZw&_nc_ss=7b20f&oh=00_Af5PrTwsXiZbRwJPfoJzjr6810xjoKC_MJrlYw24uOXQ0Q&oe=6A1C306B)

If a business customer who you have already onboarded wants to enable this feature, you can send them these instructions:

1. Access Meta Business Suite at [https://business.facebook.com](https://business.facebook.com) .
2. Navigate to **Settings** > **Accounts** > **WhatsApp accounts** and click your WhatsApp Business Account.
3. Scroll down to **Privacy and data sharing** in the **Summary** tab.
4. Use the “ **Automatically identify** ... “ toggles to enable or disable automatic event identification as desired.
