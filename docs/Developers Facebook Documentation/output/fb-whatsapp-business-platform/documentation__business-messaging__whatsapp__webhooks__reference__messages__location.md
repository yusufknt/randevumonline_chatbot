# Location messages webhook reference | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/location_

---

# Location messages webhook reference

Updated: Oct 22, 2025

This reference describes trigger events and payload contents for the WhatsApp Business Account **messages** webhook for messages containing location information.

## Triggers

- A WhatsApp user sends a location message to a business.
- A WhatsApp user sends a location to a business via a Click to WhatsApp ad.

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
            "contacts": [
              {
                "profile": {
                  "name": "<WHATSAPP_USER_PROFILE_NAME>"
                },
                "wa_id": "<WHATSAPP_USER_ID>",
                "identity_key_hash": "<IDENTITY_KEY_HASH>" <!-- only included if identity change check enabled -->
              }
            ],
            "messages": [
              {
                "from": "<WHATSAPP_USER_PHONE_NUMBER>",
                "id": "<WHATSAPP_MESSAGE_ID>",
                "timestamp": "<WEBHOOK_TRIGGER_TIMESTAMP>",
                "location": {
                  "address": "<LOCATION_ADDRESS>",
                  "latitude": <LOCATION_LATITUDE>,
                  "longitude": <LOCATION_LONGITUDE>,
                  "name": "<LOCATION_NAME>",
                  "url": "<LOCATION_URL>"
                },
                "type": "location",

                <!-- only included if message sent via a Click to WhatsApp ad -->
                "referral": {
                  "source_url": "<AD_URL>",
                  "source_id": "<AD_ID>",
                  "source_type": "ad",
                  "body": "<AD_PRIMARY_TEXT>",
                  "headline": "<AD_HEADLINE>",
                  "media_type": "<AD_MEDIA_TYPE>",
                  "image_url": "<AD_IMAGE_URL>",
                  "video_url": "<AD_VIDEO_URL>",
                  "thumbnail_url": "<AD_VIDEO_THUMBNAIL>",
                  "ctwa_clid": "<AD_CLICK_ID>",
                  "welcome_message": {
                    "text": "<AD_GREETING_TEXT>"
                  }
                }
              }
            ]
          },
          "field": "messages"
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
| `<AD_GREETING_TEXT>`<br>*String* | Click to WhatsApp ad greeting text. | `Hi there! Let us know how we can help!` |
| `<AD_HEADLINE>`<br>*String* | Click to WhatsApp ad headline. | `Chat with us` |
| `<AD_ID>`<br>*String* | Click to WhatsApp ad ID. | `120226305854810726` |
| `<AD_IMAGE_URL>`<br>*String* | Click to WhatsApp ad image URL. Only included if the ad is an image ad. | `https://scontent.xx.fbcdn.net/v/t45.1...` |
| `<AD_MEDIA_TYPE>`<br>*String* | Click to WhatsApp ad media type. Values can be:<br>`image` — Indicates an image ad.<br>`video` — Indicates a video ad. | `image` |
| `<AD_PRIMARY_TEXT>`<br>*String* | Click to WhatsApp ad primary text. | `Summer succulents are here!` |
| `<AD_URL>`<br>*String* | Click to WhatsApp ad URL. | `https://fb.me/3cr4Wqqkv` |
| `<AD_VIDEO_THUMBNAIL>`<br>*String* | Click to WhatsApp ad video thumbnail URL. Only included if ad is a video ad. | `https://scontent.xx.fbcdn.net/v/t45.3...` |
| `<AD_VIDEO_URL>`<br>*String* | Click to WhatsApp ad video URL. Only included if ad is a video ad. | `https://scontent.xx.fbcdn.net/v/t45.2...` |
| `<BUSINESS_DISPLAY_PHONE_NUMBER>`<br>*String* | Business display phone number. | `15550783881` |
| `<BUSINESS_PHONE_NUMBER_ID>`<br>*String* | Business phone number ID. | `106540352242922` |
| `<IDENTITY_KEY_HASH>`<br>*String* | Identity key hash. Only included if you have enabled the [identity change check](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers) feature. | `DF2lS5v2W6x=` |
| `<LOCATION_ADDRESS>`<br>*String* | Location address. | `101 Forest Ave, Palo Alto, CA 94301` |
| `<LOCATION_LATITUDE>`<br>*Float* | Location latitude in decimal degrees. | `37.44221496582` |
| `<LOCATION_LONGITUDE>`<br>*Float* | Location longitude in decimal degrees. | `-122.16165924072` |
| `<LOCATION_NAME>`<br>*String* | Location name. | `Philz Coffee` |
| `<LOCATION_URL>`<br>*String* | Location URL. Usually only included for business locations. | `https://philzcoffee.com/` |
| `<WEBHOOK_TRIGGER_TIMESTAMP>`<br>*String* | Unix timestamp indicating when the webhook was triggered. | `1739321024` |
| `<WHATSAPP_BUSINESS_ACCOUNT_ID>`<br>*String* | WhatsApp Business Account ID. | `102290129340398` |
| `<WHATSAPP_MESSAGE_ID>`<br>*String* | WhatsApp message ID. | `wamid.HBgLMTY1MDM4Nzk0MzkVAgASGBQzQUFERjg0NDEzNDdFODU3MUMxMAA=` |
| `<WHATSAPP_USER_ID>`<br>*String* | WhatsApp user ID. Note that a WhatsApp user’s ID and phone number may not always match. | `16505551234` |
| `<WHATSAPP_USER_PHONE_NUMBER>`<br>*String* | WhatsApp user phone number. This is the same value returned by the API as the `input` value when sending a message to a WhatsApp user. Note that a WhatsApp user’s phone number and ID may not always match. | `+16505551234` |
| `<WHATSAPP_USER_PROFILE_NAME>`<br>*String* | WhatsApp user’s name as it appears in their profile in the WhatsApp client. | `Sheena Nelson` |

## Example

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
            "contacts": [
              {
                "profile": {
                  "name": "Sheena Nelson"
                },
                "wa_id": "16505551234"
              }
            ],
            "messages": [
              {
                "from": "16505551234",
                "id": "wamid.HBgLMTY1MDM4Nzk0MzkVAgASGBQzQUFERjg0NDEzNDdFODU3MUMxMAA=",
                "timestamp": "1744344496",
                "location": {
                  "address": "101 Forest Ave, Palo Alto, CA 94301",
                  "latitude": 37.44221496582,
                  "longitude": -122.16165924072,
                  "name": "Philz Coffee",
                  "url": "https://philzcoffee.com/"
                },
                "type": "location"
              }
            ]
          },
          "field": "messages"
        }
      ]
    }
  ]
}
```
