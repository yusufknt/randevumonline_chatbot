# Contacts messages webhook reference | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/contacts_

---

# Contacts messages webhook reference

Updated: Oct 22, 2025

This reference describes trigger events and payload contents for the WhatsApp Business Account **messages** webhook for messages containing one or more contacts.

## Triggers

- A WhatsApp user sends one or more contacts to a business.
- A WhatsApp user sends one or more contacts to a business via a Click to WhatsApp ad.

## Syntax

Note that many contact object properties may be omitted if the WhatsApp user chooses not to share them, or their device prevents them from being shared.

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
                "type": "contacts",
                "contacts": [
                  {
                    "addresses": [
                      {
                        "city": "<CONTACT_CITY>",
                        "country": "<CONTACT_COUNTRY>",
                        "country_code": "<CONTACT_COUNTRY_CODE>",
                        "state": "<CONTACT_STATE>",
                        "street": "<CONTACT_STREET>",
                        "type": "<CONTACT_ADDRESS_TYPE>",
                        "zip": "<CONTACT_ZIP>"
                      }
                    ],
                    "birthday": "<CONTACT_BIRTHDAY>",
                    "emails": [
                      {
                        "email": "<CONTACT_EMAIL>",
                        "type": "<CONTACT_EMAIL_TYPE>"
                      }
                    ],
                    "name": {
                      "formatted_name": "<CONTACT_FORMATTED_NAME>",
                      "first_name": "<CONTACT_FIRST_NAME>",
                      "last_name": "<CONTACT_LAST_NAME>",
                      "middle_name": "<CONTACT_MIDDLE_NAME>",
                      "suffix": "<CONTACT_NAME_SUFFIX>",
                      "prefix": "<CONTACT_NAME_PREFIX>"
                    },
                    "org": {
                      "company": "<CONTACT_ORG_COMPANY>",
                      "department": "<CONTACT_ORG_DEPARTMENT>",
                      "title": "<CONTACT_ORG_TITLE>"
                    },
                    "phones": [
                      {
                        "phone": "<CONTACT_PHONE>",
                        "wa_id": "<CONTACT_WHATSAPP_PHONE_NUMBER>",
                        "type": "<CONTACT_PHONE_TYPE>"
                      }
                    ],
                    "urls": [
                      {
                        "url": "<CONTACT_URL>",
                        "type": "<CONTACT_URL_TYPE>"
                      }
                    ]
                  }
                ],

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
| `<CONTACT_ADDRESS_TYPE>`<br>*String* | Type of address, such as home or work. | `Home` |
| `<CONTACT_BIRTHDAY>`<br>*String* | Contact birthday. | `1999-01-23` |
| `<CONTACT_CITY>`<br>*String* | City mentioned in the contact address. | `Menlo Park` |
| `<CONTACT_COUNTRY_CODE>`<br>*String* | ISO country code on the contact address. | `US` |
| `<CONTACT_COUNTRY>`<br>*String* | Country mentioned in the contact address. | `United States` |
| `<CONTACT_EMAIL_TYPE>`<br>*String* | Type of email, such as personal or work. | `Personal` |
| `<CONTACT_EMAIL>`<br>*String* | Email address of the contact. | `bjohson@socialtsunami.com` |
| `<CONTACT_FIRST_NAME>`<br>*String* | Contact’s first name. | `Barbara` |
| `<CONTACT_FORMATTED_NAME>`<br>*String* | Contact’s formatted name. | `Barbara J. Johnson` |
| `<CONTACT_LAST_NAME>`<br>*String* | Contact’s last name. | `Johnson` |
| `<CONTACT_MIDDLE_NAME>`<br>*String* | Contact’s middle name. | `Joana` |
| `<CONTACT_NAME_PREFIX>`<br>*String* | Contact’s name prefix. | `Dr.` |
| `<CONTACT_NAME_SUFFIX>`<br>*String* | Contact’s name suffix. | `Esq.` |
| `<CONTACT_ORG_COMPANY>`<br>*String* | Name of the company where the contact works. | `Social Tsunami` |
| `<CONTACT_ORG_DEPARTMENT>`<br>*String* | Name of the department where the contact works. | `Engineering` |
| `<CONTACT_ORG_TITLE>`<br>*String* | Contact’s job title. | `Software Engineer` |
| `<CONTACT_PHONE_TYPE>`<br>*String* | Type of phone number. For example, cell, mobile, main, iPhone, home, work, etc. | `CELL` |
| `<CONTACT_PHONE>`<br>*String* | Contact’s phone number. | `+14125550829` |
| `<CONTACT_STATE>`<br>*String* | State mentioned in the contact address. | `CA` |
| `<CONTACT_STREET>`<br>*String* | Street mentioned in the contact address. | `1 Hacker Way` |
| `<CONTACT_URL_TYPE>`<br>*String* | Type of website. For example, company, work, personal, Facebook Page, Instagram, etc. | `Company` |
| `<CONTACT_URL>`<br>*String* | Website URL associated with the contact or their company. | `socialtsunami.com` |
| `<CONTACT_WHATSAPP_PHONE_NUMBER>`<br>*String* | Contact’s WhatsApp number. | `14125550829` |
| `<CONTACT_ZIP>`<br>*String* | Zip code in the contact address. | `94025` |
| `<IDENTITY_KEY_HASH>`<br>*String* | Identity key hash. Only included if you have enabled the [identity change check](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers) feature. | `DF2lS5v2W6x=` |
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
                "id": "wamid.HBgLMTY1MDM4Nzk0MzkVAgASGBQzQTRBNjU5OUFFRTAzODEwMTQ0RgA=",
                "timestamp": "1744344496",
                "type": "contacts",
                "contacts": [
                  {
                    "name": {
                      "first_name": "Barbara",
                      "last_name": "Johnson",
                      "formatted_name": "Barbara J. Johnson"
                    },
                    "org": {
                      "company": "Social Tsunami"
                    },
                    "phones": [
                      {
                        "phone": "+1 (415) 555-0829",
                        "wa_id": "14125550829",
                        "type": "MOBILE"
                      }
                    ]
                  }
                ]
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
