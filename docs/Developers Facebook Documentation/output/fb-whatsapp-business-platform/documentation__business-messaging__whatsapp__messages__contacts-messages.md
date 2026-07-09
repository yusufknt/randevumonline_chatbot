# Contacts messages | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/contacts-messages_

---

# Contacts messages

Updated: Nov 3, 2025

Contacts messages allow you to send rich contact information directly to WhatsApp users, such as names, phone numbers, physical addresses, and email addresses.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/441381765_2668119610015051_1596469393832242771_n.png?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=PAIYI5bD9ncQ7kNvwGHHv43&_nc_oc=AdoRHE08suzlUK2ia7DXoPSH3n2zRkyYHY8Xxd_fMMgCiExRTosR40AN9Ft8kS_2eO8&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=TrgQ3VHgbXEKaWWZjWpn5w&_nc_ss=7b20f&oh=00_Af5KeFzT7fWRMfY0yOoZNhgLh6SkIVSuCjAt7M2-TwpYAg&oe=6A1C09F2)

When a WhatsApp user taps the message’s profile arrow, it displays the contact’s information in a profile view:

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/441391825_1516000578987481_5920245070887074504_n.png?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=svhhp3PUUvsQ7kNvwFzAuP6&_nc_oc=AdpHOqPmTztaiadwoxridya3zWJvd34PthySFq-a1CLDdJCLks-xjxIIOpsIyQLeFY8&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=TrgQ3VHgbXEKaWWZjWpn5w&_nc_ss=7b20f&oh=00_Af7tVKJA1wPQDR7qqP-E5VrCQxfhHgjhq8EPPPWE5fj4HQ&oe=6A1C06A7)

Each message can include information for up to 257 contacts, although it is recommended to send fewer for usability and negative feedback reasons.

Please be aware that a contact’s metadata (e.g., addresses, birthdays, emails) may not be supported by the recipient, especially on their primary device. Please refer to this [documentation](https://faq.whatsapp.com/378279804439436/?cms_platform=android) for the definitions of primary and linked devices.

## Request syntax

Use the [Messages API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api#post-version-phone-number-id-messages) to send a contacts message to a WhatsApp user.

```html
curl 'https://graph.facebook.com/<API_VERSION>/<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>/messages' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <ACCESS_TOKEN>' \
-d '
{
  "messaging_product": "whatsapp",
  "to": "<WHATSAPP_USER_PHONE_NUMBER>",
  "type": "contacts",
  "contacts": [
    {
      "addresses": [
        {
          "street": "<STREET_NUMBER_AND_NAME>",
          "city": "<CITY>",
          "state": "<STATE_CODE>",
          "zip": "<ZIP_CODE>",
          "country": "<COUNTRY_NAME>",
          "country_code": "<COUNTRY_CODE>",
          "type": "<ADDRESS_TYPE>"
        }
        <!-- Additional addresses objects go here, if using -->
      ],
      "birthday": "<BIRTHDAY>",
      "emails": [
        {
          "email": "<EMAIL_ADDRESS>",
          "type": "<EMAIL_TYPE>"
        }
        <!-- Additional emails objects go here, if using -->
      ],
      "name": {
        "formatted_name": "<FULL_NAME>",
        "first_name": "<FIRST_NAME>",
        "last_name": "<LAST_NAME>",
        "middle_name": "<MIDDLE_NAME>",
        "suffix": "<SUFFIX>",
        "prefix": "<PREFIX>"
      },
      "org": {
        "company": "<COMPANY_OR_ORG_NAME>",
        "department": "<DEPARTMENT_NAME>",
        "title": "<JOB_TITLE>"
      },
      "phones": [
        {
          "phone": "<PHONE_NUMBER>",
          "type": "<PHONE_NUMBER_TYPE>",
          "wa_id": "<WHATSAPP_USER_ID>"
        }
        <!-- Additional phones objects go here, if using -->
      ],
      "urls": [
        {
          "url": "<WEBSITE_URL>",
          "type": "<WEBSITE_TYPE>"
        }
        <!-- Additional URLs go here, if using -->
      ]
    }
  ]
}'
```

## Request parameters

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<ACCESS_TOKEN>`<br>*String* | **Required.**<br>[System token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens) or [business token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens). | `EAAA...` |
| `<ADDRESS_TYPE>`<br>*String* | **Optional.**<br>Type of address, such as home or work. | `Home` |
| `<API_VERSION>`<br>*String* | **Optional.**<br>Graph API version. | v25.0 |
| `<BIRTHDAY>`<br>*String* | **Optional.**<br>Contact’s birthday. Must be in `YYYY-MM-DD` format. | `1999-01-23` |
| `<CITY>`<br>*String* | **Optional.**<br>City where the contact resides. | `Menlo Park` |
| `<COMPANY_OR_ORG_NAME>`<br>*String* | **Optional.**<br>Name of the company where the contact works. | `Lucky Shrub` |
| `<COUNTRY_CODE>`<br>*String* | **Optional.**<br>ISO two-letter country code. | `US` |
| `<COUNTRY_NAME>`<br>*String* | **Optional.**<br>Country name. | `United States` |
| `<DEPARTMENT_NAME>`<br>*String* | **Optional.**<br>Department within the company. | `Legal` |
| `<EMAIL_ADDRESS>`<br>*String* | **Optional.**<br>Email address of the contact. | `bjohnson@luckyshrub.com` |
| `<EMAIL_TYPE>`<br>*String* | **Optional.**<br>Type of email, such as personal or work. | `Work` |
| `<FIRST_NAME>`<br>*String* | **Optional.**<br>Contact’s first name. | `Barbara` |
| `<FORMATTED_NAME>`<br>*String* | **Required.**<br>Contact’s formatted name. This will appear in the message alongside the profile arrow button. | `Barbara J. Johnson` |
| `<JOB_TITLE>`<br>*String* | **Optional.**<br>Contact’s job title. | `Lead Counsel` |
| `<LAST_NAME>`<br>*String* | **Optional.**<br>Contact’s last name. | `Johnson` |
| `<MIDDLE_NAME>`<br>*String* | **Optional.**<br>Contact’s middle name. | `Joana` |
| `<PHONE_NUMBER>`<br>*String* | **Optional.**<br>WhatsApp user phone number. | `+16505559999` |
| `<PHONE_NUMBER_TYPE>`<br>*String* | **Optional.**<br>Type of phone number. For example, cell, mobile, main, iPhone, home, work, etc. | `Home` |
| `<PREFIX>`<br>*String* | **Optional.**<br>Prefix for the contact’s name, such as Mr., Ms., Dr., etc. | `Dr.` |
| `<STATE_CODE>`<br>*String* | **Optional.**<br>Two-letter state code. | `CA` |
| `<STREET_NUMBER_AND_NAME>`<br>*String* | **Optional.**<br>Street address of the contact. | `1 Lucky Shrub Way` |
| `<SUFFIX>`<br>*String* | **Optional.**<br>Suffix for the contact’s name, if applicable. | `Esq.` |
| `<WEBSITE_TYPE>`<br>*String* | **Optional.**<br>Type of website. For example, company, work, personal, Facebook Page, Instagram, etc. | `Company` |
| `<WEBSITE_URL>`<br>*String* | **Optional.**<br>Website URL associated with the contact or their company. | `https://www.luckyshrub.com` |
| `<WHATSAPP_USER_ID>`<br>*String* | **Optional.**<br>WhatsApp user ID. If omitted, the message will display an Invite to WhatsApp button instead of the standard buttons.<br>See [Button Behavior](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/contacts-messages#button-behavior) below. | `19175559999` |
| `<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>`<br>*String* | **Required.**<br>WhatsApp business phone number ID. | `106540352242922` |
| `<WHATSAPP_USER_PHONE_NUMBER>`<br>*String* | **Required.**<br>WhatsApp user phone number. | `+16505551234` |
| `<ZIP_CODE>`<br>*String* | **Optional.**<br>Postal or ZIP code. | `94025` |

## Button behavior

If you include the contact’s WhatsApp ID in the message (via the `wa_id` property), the message will include a **Message** and a **Save contact** button:

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/441399296_815661620463689_7258599973025915055_n.png?_nc_cat=102&ccb=1-7&_nc_sid=e280be&_nc_ohc=DmYTNqV2spMQ7kNvwF4EWj6&_nc_oc=AdqZNuvaG_IgONNeCkJH3wqF-PrLNBEPEitty_f7rvB5EBqh-ZtfjugX601Iv_WKxjk&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=TrgQ3VHgbXEKaWWZjWpn5w&_nc_ss=7b20f&oh=00_Af7-B0CfXETWVGBLvJifVN_GaWhdMmYuN9Y1xQa-P8UNOQ&oe=6A1C106A)

If the WhatsApp user taps the **Message** button, it will open a new message with the contact. If the user taps the **Save contact** button, they will be given the option to save the contact as a new contact, or to update an existing contact.

If you omit the `wa_id` property, both buttons will be replaced with an **Invite to WhatsApp** button:

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/441366594_855962089669296_5557083162637364924_n.png?_nc_cat=111&ccb=1-7&_nc_sid=e280be&_nc_ohc=Y-GBcYXcZVUQ7kNvwG0Ydf8&_nc_oc=AdqYAJQfhQb_G73ArqPesj8C_Fu1Eml3-8u_StkGuuXMH0DK__Lj4BFk1c_D2X58i64&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=TrgQ3VHgbXEKaWWZjWpn5w&_nc_ss=7b20f&oh=00_Af6vvOJic0E_mmzWbpn0S8fmjaUN1KgQa-KjWWnKSW0wlQ&oe=6A1C2E97)

## Example request

Example request to send a contacts message with two physical addresses, two email addresses, two phone numbers, and two website URLs.

```curl
curl 'https://graph.facebook.com/v25.0/106540352242922/messages' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "messaging_product": "whatsapp",
  "to": "+16505551234",
  "type": "contacts",
  "contacts": [
    {
      "addresses": [
        {
          "street": "1 Lucky Shrub Way",
          "city": "Menlo Park",
          "state": "CA",
          "zip": "94025",
          "country": "United States",
          "country_code": "US",
          "type": "Office"
        },
        {
          "street": "1 Hacker Way",
          "city": "Menlo Park",
          "state": "CA",
          "zip": "94025",
          "country": "United States",
          "country_code": "US",
          "type": "Pop-Up"
        }
      ],
      "birthday": "1999-01-23",
      "emails": [
        {
          "email": "bjohnson@luckyshrub.com",
          "type": "Work"
        },
        {
          "email": "bjohnson@luckyshrubplants.com",
          "type": "Work (old)"
        }
      ],
      "name": {
        "formatted_name": "Barbara J. Johnson",
        "first_name": "Barbara",
        "last_name": "Johnson",
        "middle_name": "Joana",
        "suffix": "Esq.",
        "prefix": "Dr."
      },
      "org": {
        "company": "Lucky Shrub",
        "department": "Legal",
        "title": "Lead Counsel"
      },
      "phones": [
        {
          "phone": "+16505559999",
          "type": "Landline"
        },
        {
          "phone": "+19175559999",
          "type": "Mobile",
          "wa_id": "19175559999"
        }
      ],
      "urls": [
        {
          "url": "https://www.luckyshrub.com",
          "type": "Company"
        },
        {
          "url": "https://www.facebook.com/luckyshrubplants",
          "type": "Company (FB)"
        }
      ]
    }
  ]
}'
```

## Example response

```json
{
  "messaging_product": "whatsapp",
  "contacts": [
    {
      "input": "+16505551234",
      "wa_id": "16505551234"
    }
  ],
  "messages": [
    {
      "id": "wamid.HBgLMTY0NjcwNDM1OTUVAgARGBI1RjQyNUE3NEYxMzAzMzQ5MkEA"
    }
  ]
}
```
