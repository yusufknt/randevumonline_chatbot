# Location request messages | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/location-request-messages_

---

# Location request messages

Updated: Nov 3, 2025

Location request messages display **body text** and a **send location button**. When a WhatsApp user taps the button, a location sharing screen appears which the user can then use to share their location.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/411712787_1346691626211128_4092487602815472288_n.png?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=ihRXemxXvJwQ7kNvwGJP_zS&_nc_oc=AdroXX3QZy0pKPkkrS5MNhzjLzgXnCpbVMocFpEJzqU1eaoB1qQoHVhU8sJMDGY8wQU&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=-sVeWJmhD6YDR7wPjSZwJw&_nc_ss=7b20f&oh=00_Af7KyGovkIDN_AmAeBrozyXKXzIhyvc5q3dwkaABqSxpIQ&oe=6A1C1F6A)

Once the user shares their location, a **messages** webhook is triggered, containing the user’s location details.

## Request syntax

Use the [Messages API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api#post-version-phone-number-id-messages) to send a location request message to a WhatsApp user.

```html
curl 'https://graph.facebook.com/<API_VERSION>/<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>/messages' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <ACCESS_TOKEN>' \
-d '
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "type": "interactive",
  "to": "<WHATSAPP_USER_PHONE_NUMBER>",
  "interactive": {
    "type": "location_request_message",
    "body": {
      "text": "<BODY_TEXT>"
    },
    "action": {
      "name": "send_location"
    }
  }
}'
```

## Request parameters

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<ACCESS_TOKEN>`<br>*String* | **Required.**<br>[System token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens) or [business token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens). | `EAAA...` |
| `<API_VERSION>`<br>*String* | **Optional.**<br>Graph API version. | v25.0 |
| `<BODY_TEXT>`<br>*String* | **Required.**<br>Message body text. Supports URLs.<br>Maximum 1024 characters. | `Let's start with your pickup. You can either manually *enter an address* or *share your current location*.` |
| `<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>`<br>*String* | **Required.**<br>WhatsApp business phone number ID. | `106540352242922` |
| `<WHATSAPP_USER_PHONE_NUMBER>`<br>*String* | **Required.**<br>WhatsApp user phone number. | `+16505551234` |

## Webhook syntax

When a WhatsApp user shares their location in response to your message, a **messages** webhook is triggered containing the user’s location details.

```json
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
              "display_phone_number": "<WHATSAPP_BUSINESS_DISPLAY_PHONE_NUMBER>",
              "phone_number_id": "<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>"
            },
            "contacts": [
              {
                "profile": {
                  "name": "<WHATSAPP_USER_NAME>"
                },
                "wa_id": "<WHATSAPP_USER_ID>"
              }
            ],
            "messages": [
              {
                "context": {
                  "from": "<WHATSAPP_BUSINESS_PHONE_NUMBER>",
                  "id": "<WHATSAPP_CONTEXT_MESSAGE_ID>"
                },
                "from": "<WHATSAPP_USER_ID>",
                "id": "<WHATSAPP_MESSAGE_ID>",
                "timestamp": "<TIMESTAMP>",
                "location": {
                  "address": "<LOCATION_ADDRESS>",
                  "latitude": <LOCATION_LATITUDE>,
                  "longitude": <LOCATION_LONGITUDE>,
                  "name": "<LOCATION_NAME>"
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

## Webhook parameters

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<LOCATION_ADDRESS>`<br>*String* | Location address.<br>This parameter will only appear if the WhatsApp user chooses to share it. | `1071 5th Ave, New York, NY 10128` |
| `<LOCATION_LATITUDE>`<br>*Number* | Location latitude in decimal degrees. | `40.782910059774` |
| `<LOCATION_LONGITUDE>`<br>*Number* | Location longitude in decimal degrees. | `-73.959075808525` |
| `<LOCATION_NAME>`<br>*String* | Location name.<br>This parameter will only appear if the WhatsApp user chooses to share it. | `Solomon R. Guggenheim Museum` |
| `<TIMESTAMP>`<br>*String* | UNIX timestamp indicating when our servers processed the WhatsApp user’s message. | `1702920965` |
| `<WHATSAPP_BUSINESS_ACCOUNT_ID>`<br>*String* | WhatsApp Business Account ID. | `102290129340398` |
| `<WHATSAPP_BUSINESS_DISPLAY_PHONE_NUMBER>`<br>*String* | WhatsApp business phone number’s display number. | `15550783881` |
| `<WHATSAPP_BUSINESS_PHONE_NUMBER>`<br>*String* | WhatsApp business phone number. | `15550783881` |
| `<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>`<br>*String* | WhatsApp business phone number ID. | `106540352242922` |
| `<WHATSAPP_CONTEXT_MESSAGE_ID>`<br>*String* | WhatsApp message ID of message that the user is responding to. | `wamid.HBgLMTY0NjcwNDM1OTUVAgARGBI1QjJGRjI1RDY0RkE4Nzg4QzcA` |
| `<WHATSAPP_MESSAGE_ID>`<br>*String* | WhatsApp message ID of the user’s message. | `wamid.HBgLMTY0NjcwNDM1OTUVAgASGBQzQTRCRDcwNzgzMTRDNTAwRTgwRQA=` |
| `<WHATSAPP_USER_ID>`<br>*String* | WhatsApp user’s WhatsApp ID. | `16505551234` |
| `<WHATSAPP_USER_NAME>`<br>*String* | WhatsApp user’s name. | `Pablo Morales` |

## Example request

```curl
curl 'https://graph.facebook.com/v25.0/106540352242922/messages' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "type": "interactive",
  "to": "+16505551234",
  "interactive": {
    "type": "location_request_message",
    "body": {
      "text": "Let'\''s start with your pickup. You can either manually *enter an address* or *share your current location*."
    },
    "action": {
      "name": "send_location"
    }
  }
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
      "id": "wamid.HBgLMTY0NjcwNDM1OTUVAgARGBJCNUQ5RUNBNTk3OEQ2M0ZEQzgA"
    }
  ]
}
```

## Example webhook

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
                  "name": "Pablo Morales"
                },
                "wa_id": "16505551234"
              }
            ],
            "messages": [
              {
                "context": {
                  "from": "15550783881",
                  "id": "wamid.HBgLMTY0NjcwNDM1OTUVAgARGBI1QjJGRjI1RDY0RkE4Nzg4QzcA"
                },
                "from": "16505551234",
                "id": "wamid.HBgLMTY0NjcwNDM1OTUVAgASGBQzQTRCRDcwNzgzMTRDNTAwRTgwRQA=",
                "timestamp": "1702920965",
                "location": {
                  "address": "1071 5th Ave, New York, NY 10128",
                  "latitude": 40.782910059774,
                  "longitude": -73.959075808525,
                  "name": "Solomon R. Guggenheim Museum"
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
