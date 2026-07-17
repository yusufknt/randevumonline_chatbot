# Address Messages | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/address-messages_

---

# Address Messages

Updated: Nov 7, 2025

This feature is only available for businesses based in India and their India customers.

Address messages give your users a simpler way to share the shipping address with the business on WhatsApp.

Address messages are interactive messages that contain the 4 main parts: `header`, `body`, `footer`, and `action`. Inside the action component business specifies the name “address_message” and relevant parameters.

Below table outlines the fields that are supported by the address message.

| Field Name | Display Label | Input Type | Supported Countries | Limitations |
| --- | --- | --- | --- | --- |
| `name` | Name | text | India | None |
| `phone_number` | Phone Number | tel | India | Valid phone numbers only |
| `in_pin_code` | Pin Code | text | India | Max length: 6 |
| `house_number` | Flat/House Number | text | India | None |
| `floor_number` | Floor Number | text | India | None |
| `tower_number` | Tower Number | text | India | None |
| `building_name` | Building/Apartment Name | text | India | None |
| `address` | Address | text | India | None |
| `landmark_area` | Landmark/Area | text | India | None |
| `city` | City | text | India | None |
| `state` | State | text | India | None |

## Sample API call

This is a sample API call for the address message. The `country` attribute is a mandatory field in the action parameters. If it is not included, there will be a validation error.

```curl
curl -X  POST \
'https://graph.facebook.com/<API_VERSION>/<FROM_PHONE_NUMBER_ID>/messages' \
-H 'Authorization: Bearer <ACCESS_TOKEN>' \
-H 'Content-Type: application/json' \
-d '
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "<PHONE_NUMBER>",
  "type": "interactive",
  "interactive": {
    "type": "address_message",
    "body": {
      "text": "Thanks for your order! Tell us what address you’d like this order delivered to."
    },
    "action": {
      "name": "address_message",
      "parameters": {
        "country": "<COUNTRY_ISO_CODE>"
      }
    }
  }
}'
```

## Error Handling

If the area code of the phone number for the given country is not correct, businesses will be unable to request the address message from the recipient. For example, businesses will be unable to request an address message from a recipient that has the country as “India” but has a phone number with an area code of “65”.

Once the address message is sent, the business waits for the user to fill in the address and send it back. The user entered address is shared through the [webhook](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/overview) registered in the [setup process](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/overview).

## Address Message Steps

The steps involved in an Address Message are the following:

1. Business sends an address message with the action name `address_message` to the user
2. User interacts with the message by clicking on the CTA, which brings up an Address Message screen. The user fills out their address and submits the form
3. After the address message form is submitted by the user, the partner receives a webhook notification, which contains the details of the address submitted by the user

Sample India Address Message

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/565829166_1339318437926807_3659527486531714210_n.jpg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=7YP1MPsVnjoQ7kNvwEQzoes&_nc_oc=Ado1koDMmw86HReHJ_8boCan8--VTsvJS6IZySCcfDzqjZoJSztYwDiIfTk88ebYgQQ&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=cKEEl_DZe5W2V89qmrAPMA&_nc_ss=7b20f&oh=00_Af5PpobdCnMyT0JocHWtEb2OjwfR8e_ij07Jy9vfFXiLug&oe=6A1C11B3)![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/560182401_1339318284593489_3917170764968888761_n.jpg?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=ya4tErIB_88Q7kNvwG3fq_J&_nc_oc=Adq1vOcLMuhgdrwDPGDs9nkztNFfy9ws1VB6BT2S7iYGeRAESg-kCN6VIp06m6_Rkfo&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=cKEEl_DZe5W2V89qmrAPMA&_nc_ss=7b20f&oh=00_Af5KgX8BLxiPgCSD8KShu2PAn2Ka3ylhXta0ODOGQ47ulQ&oe=6A1C24A3)![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/561656043_1339318467926804_8340276620740620111_n.jpg?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=AdwtItf-Hu0Q7kNvwFV2oNR&_nc_oc=AdpZCxxZc7l-n0F3CfJpmYsYEXX7SZKnhrD5zdqEiml7VthoDE1WPghUxoACsk6wpkQ&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=cKEEl_DZe5W2V89qmrAPMA&_nc_ss=7b20f&oh=00_Af5xT-pt9D3wJEqAOUdLwtp4PH0NmTwDIpMTi__iCpgeAA&oe=6A1C1093)![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/561778150_1339318131260171_5843569977396603182_n.jpg?_nc_cat=101&ccb=1-7&_nc_sid=e280be&_nc_ohc=u0h9sdv8RvkQ7kNvwGmGAjH&_nc_oc=AdrDc01FMY9FUJ0tN5RsFf-YNt9xWozvCP-dhtyp0ZhJvtwhfIHleQ0iyiBXWYmCuG0&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=cKEEl_DZe5W2V89qmrAPMA&_nc_ss=7b20f&oh=00_Af5q8HPRySYedZhWWws4Bm950KQAkHlKGoLeDQl9sqxzfg&oe=6A1C0A52)

The following sequence diagram shows a typical integration flow for an address message.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/564006097_1339318367926814_6312454230710951737_n.jpg?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=es0nCbttj3YQ7kNvwEpgKCp&_nc_oc=AdqXcBQk-Dm2gW7CH8fDzPY-_fBSma8qc1G8GqjfCnnwea-5ElzwtO3EfI5ZhFxTGxk&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=cKEEl_DZe5W2V89qmrAPMA&_nc_ss=7b20f&oh=00_Af5y-cOYZ_EhI6_B4XAz_E2RyjSEvJviwPLh_eOfFqnDPA&oe=6A1C30D3)

## Additional Action Parameters

The business can pass additional attributes such as `values`, `validation_errors`, or `saved_addresses` as part of the interactive action parameters. You can find information on each of their usage below.

| Action Parameter | Usage |
| --- | --- |
| `values` | Businesses prefill this for address fields (eg. prefilling the city address field with “India”) |
| `saved_addresses` | For businesses, they can pass in saved addresses previously associated with the user.<br>For users, they are presented with the option to choose the saved address instead of manually filling it in |
| `validation_errors` | Businesses can throw errors in the address fields and WhatsApp will prevent the user from submitting the address until the issue(s) are/is resolved. |

### Send Address Message to a User

Use the [Messages API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api#post-version-phone-number-id-messages) to send an end-to-end encrypted address message to the user:

```curl
curl -X  POST \
'https://graph.facebook.com/<API_VERSION>/<FROM_PHONE_NUMBER_ID>/messages' \
-H 'Authorization: Bearer <ACCESS_TOKEN>' \
-H 'Content-Type: application/json' \
-d '
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "<PHONE_NUMBER>",
  "type": "interactive",
  "interactive": {
    "type": "address_message",
    "body": {
      "text": "Thanks for your order! Tell us what address you’d like this order delivered to."
    },
    "action": {
      "name": "address_message",
      "parameters": "JSON Payload"
    }
  }
}'
```

To send an address message without any saved addresses, WhatsApp will prompt the user or business with an address form to enter a new address.

```curl
curl -X  POST \
'https://graph.facebook.com/<API_VERSION>/<FROM_PHONE_NUMBER_ID>/messages' \
-H 'Authorization: Bearer <ACCESS_TOKEN>' \
-H 'Content-Type: application/json' \
-d '
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "+91xxxxxxxxxx",
  "type": "interactive",
  "interactive": {
    "type": "address_message",
    "body": {
      "text": "Thanks for your order! Tell us what address you’d like this order delivered to."
    },
    "action": {
      "name": "address_message",
      "parameters": {
        "country": "IN",
        "values": {
          "name": "<CUSTOMER_NAME>",
          "phone_number": "+91xxxxxxxxxx"
        }
      }
    }
  }
}'
```

To send an address message with saved addresses, WhatsApp will prompt the user or business with an option to select among the saved addresses or add an address option. Users can ignore the saved address and enter a new address.

```curl
curl -X  POST \
'https://graph.facebook.com/<API_VERSION>/<FROM_PHONE_NUMBER_ID>/messages' \
-H 'Authorization: Bearer <ACCESS_TOKEN>' \
-H 'Content-Type: application/json' \
-d '
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "91xxxxxxxxxx",
  "type": "interactive",
  "interactive": {
    "type": "address_message",
    "body": {
      "text": "Thanks for your order! Tell us what address you’d like this order delivered to."
    },
    "action": {
      "name": "address_message",
      "parameters": {
        "country": "IN",
        "saved_addresses": [
          {
            "id": "address1",
            "value": {
              "name": "<CUSTOMER_NAME>",
              "phone_number": "+91xxxxxxxxxx",
              "in_pin_code": "400063",
              "floor_number": "8",
              "building_name": "",
              "address": "Wing A, Cello Triumph,IB Patel Rd",
              "landmark_area": "Goregaon",
              "city": "Mumbai"
            }
          }
        ]
      }
    }
  }
}'
```

## Check Your Response

A successful response includes a `messages` object with an ID for the newly created message.

```json
{
  "messaging_product": "whatsapp",
  "contacts": [
    {
      "input": "<PHONE_NUMBER>",
      "wa_id": "<WHATSAPP_ID>"
    }
  ],
  "messages": [
    {
      "id": "wamid.ID"
    }
  ]
}
```

An unsuccessful response contains an error message. See [Error and Status Codes](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/error-codes) for more information.

## Send an Address Message with Validation Errors

An address message should be re-sent to the user in the case of a validation error on the business server. The business should send back the set of values previously entered by the user, along with the respective validation errors for each invalid field, as shown in the sample payloads below.

```curl
curl -X  POST \
'https://graph.facebook.com/<API_VERSION>/<FROM_PHONE_NUMBER_ID>/messages' \
-H 'Authorization: Bearer <ACCESS_TOKEN>' \
-H 'Content-Type: application/json' \
-d
'{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "91xxxxxxxxxx",
  "type": "interactive",
  "interactive": {
    "type": "address_message",
    "body": {
      "text": "Thanks for your order! Tell us what address you’d like this order delivered to."
    },
    "action": {
      "name": "address_message",
      "parameters": {
          "country": "IN",
          "values": {
             "name": "CUSTOMER_NAME",
             "phone_number": "+91xxxxxxxxxx",
             "in_pin_code": "666666",
             "address": "Some other location",
             "city": "Delhi"
          },
          "validation_errors": {
             "in_pin_code": "We could not locate this pin code."
          }
       }
    }
  }
}'
```

## Receive Notifications for Address Submissions

Businesses will receive address submission notifications through [webhooks](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/overview), such as the one shown below.

```json
{
  "messages": [
    {
      "id": "gBGGFlAwCWFvAgmrzrKijase8yA",
      "from": "<PHONE_NUMBER>",
      "interactive": {
        "type": "interactive",
        "action": "address_message",
        "nfm_reply": {
          "name": "address_message",
          "response_json": "<response_json from client>",
          "body": "<body text from client>"
        },
        "timestamp": "1670394125"
      }
    }
  ]
}
```

The webhook notification has the following values.

| Field Name | Type | Description |
| --- | --- | --- |
| `interactive` | Object | Holds the response from the client |
| `type` | String | Would be `nfm_reply` indicating it is a Native Flow Response (NFM) from the client |
| `nfm_reply` | Object | Holds the data received from the client |
| `response_json` | String | The values of the address fields filled by the user in JSON format that are always present |
| `body` (Optional) | String | Body text from client, what the user sees |
| `name` (Optional) | String | Would be `address_message` indicating the type of NFM action response from the client |

An address message reply as an NFM response type for an India address message request is shown below.

```json
{
  "messages": [
    {
      "context": {
        "from": "FROM_PHONE_NUMBER_ID",
        "id": "wamid.HBgLMTIwNjU1NTAxMDcVAgARGBI3NjNFN0U5QzMzNDlCQjY0M0QA"
      },
      "from": "<PHONE_NUMBER>",
      "id": "wamid.HBgLMTIwNjU1NTAxMDcVAgASGCA5RDhBNENEMEQ3RENEOEEzMEI0RUExRDczN0I1NThFQwA=",
      "timestamp": "1671498855",
      "type": "interactive",
      "interactive": {
        "type": "nfm_reply",
        "nfm_reply": {
          "response_json": "{\"saved_address_id\":\"address1\",\"values\":{\"in_pin_code\":\"400063\",\"building_name\":\"\",\"landmark_area\":\"Goregaon\",\"address\":\"Wing A, Cello Triumph, IB Patel Rd\",\"city\":\"Mumbai\",\"name\":\"CUSTOMER_NAME\",\"phone_number\":\"+91xxxxxxxxxx\",\"floor_number\":\"8\"}}",
          "body": "CUSTOMER_NAME\n +91xxxxxxxxxx\n 400063, Goregaon, Wing A, Cello Triumph,IB Patel Rd, Mumbai, 8",
          "name": "address_message"
        }
      }
    }
  ]
}
```

## Feature Not Supported

In the case where the client does not support `address_message`, messages are silently dropped and an error message is sent back to the business in a webhook. The webhook notification that would be sent back is shown below:

```json
{
  "statuses": [
    {
      "errors": [
        {
          "code": 1026,
          "href": "/docs/whatsapp/api/errors",
          "title": "Receiver Incapable"
        }
      ],
      "id": "gBGGFlAwCWFvAgkyHMGKnRu4JeA",
      "message": {
        "recipient_id": "+91xxxxxxxxxx"
      },
      "recipient_id": "91xxxxxxxxxx",
      "status": "failed",
      "timestamp": "1670394125",
      "type": "message"
    }
  ]
}
```
