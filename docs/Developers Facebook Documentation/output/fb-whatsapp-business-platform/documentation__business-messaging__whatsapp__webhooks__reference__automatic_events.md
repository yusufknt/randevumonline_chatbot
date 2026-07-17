# automatic_events webhook reference | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/automatic_events_

---

# automatic_events webhook reference

Updated: Nov 5, 2025

This reference describes trigger events and payload contents for the WhatsApp Business Account `automatic_events` webhook.

The **automatic_events** webhook notifies you when we detect a purchase or lead event in a chat thread between you and a WhatsApp user who has messaged you via your Click to WhatsApp ad, if you have opted-in to [Automatic Events](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/automatic-events-api) reporting.

## Triggers

- A lead event is detected in a chat thread between a business and user who has messaged the business via a Click to WhatsApp Ad.
- A purchase event is detected in a chat thread between a business and user who has messaged the business via a Click to WhatsApp Ad.

## Syntax

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
                "event_name": "<EVENT_NAME>",
                "timestamp": <WEBHOOK_TRIGGER_TIMESTAMP>,
                "ctwa_clid": "<AD_CLICK_ID>",

                <!-- Only included for purchase events -->
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

## Parameters

| Placeholder | Description | Example value |
| --- | --- | --- |
| `<AD_CLICK_ID>`<br>*String* | Click to WhatsApp ad click ID.<br>The `ctwa_clid` property is omitted entirely for messages originating from an ad in WhatsApp Status ([WhatsApp Status ad placements](https://www.facebook.com/business/help/1074444721456755)). | `Aff-n8ZTODiE79d22KtAwQKj9e_mIEOOj27vDVwFjN80dp4_0NiNhEgpGo0AHemvuSoifXaytfTzcchptiErTKCqTrJ5nW1h7IHYeYymGb5K5J5iTROpBhWAGaIAeUzHL50` |
| `<AMOUNT>`<br>*String* | Purchase amount, calculated as product price multiplied by 1000. | `25000` |
| `<BUSINESS_DISPLAY_PHONE_NUMBER>`<br>*String* | Business display phone number. | `15550783881` |
| `<BUSINESS_PHONE_NUMBER_ID>`<br>*String* | Business phone number ID. | `106540352242922` |
| `<CURRENCY_CODE>`<br>*String* | Currency code. | `USD` |
| `<EVENT_NAME>`<br>*String* | Event name. Values can be:<br>`LeadSubmitted` — Indicates a lead event.`Purchase` — Indicates a purchase event. | `Purchase` |
| `<WEBHOOK_TRIGGER_TIMESTAMP>`<br>*Integer* | Unix timestamp indicating when the webhook was triggered. | `1739321024` |
| `<WHATSAPP_MESSAGE_ID>`<br>*String* | WhatsApp message ID. | `wamid.HBgLMTY1MDM4Nzk0MzkVAgASGBQzQUFERjg0NDEzNDdFODU3MUMxMAA=` |
| `<WHATSAPP_BUSINESS_ACCOUNT_ID>`<br>*String* | WhatsApp Business Account ID. | `102290129340398` |

## Examples

### Lead gen event

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

### Purchase event

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
