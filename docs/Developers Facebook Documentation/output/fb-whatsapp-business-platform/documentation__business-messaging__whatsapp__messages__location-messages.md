# Location messages | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/location-messages_

---

# Location messages

Updated: Nov 3, 2025

Location messages allow you to send a location’s latitude and longitude coordinates to a WhatsApp user.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/440753150_1614554799358194_4095127988263974385_n.png?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=kpOY_sFoeWQQ7kNvwFjHIOU&_nc_oc=AdrUVyTFU3wFI6q5VOq0yF4J76Cv8uCeGlqWgzlvFUepyPYTwtlHd3271GQvCQeCHzU&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=Kdd18htRUKOGiX4FtMMX9w&_nc_ss=7b20f&oh=00_Af7MAEWJ2FR-tHbI3dyxDH0VIYGnrHYibvU5f0uXgZIb1g&oe=6A1C24E1)

## Request syntax

Use the [Messages API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api#post-version-phone-number-id-messages) to send a location message to a WhatsApp user.

```html
curl 'https://graph.facebook.com/<API_VERSION>/<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>/messages' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <ACCESS_TOKEN>' \
-d '
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "<WHATSAPP_USER_PHONE_NUMBER>",
  "type": "location",
  "location": {
    "latitude": "<LOCATION_LATITUDE>",
    "longitude": "<LOCATION_LONGITUDE>",
    "name": "<LOCATION_NAME>",
    "address": "<LOCATION_ADDRESS>"
  }
}'
```

## Request parameters

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<ACCESS_TOKEN>`<br>*String* | **Required.**<br>[System token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens) or [business token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens). | `EAAA...` |
| `<API_VERSION>`<br>*String* | **Optional.**<br>Graph API version. | v25.0 |
| `<LOCATION_ADDRESS>`<br>*String* | **Optional.**<br>Location address. | `101 Forest Ave, Palo Alto, CA 94301` |
| `<LOCATION_LATITUDE>`<br>*String* | **Required.**<br>Location latitude in decimal degrees. | `37.44216251868683` |
| `<LOCATION_LONGITUDE>`<br>*String* | **Required.**<br>Location longitude in decimal degrees. | `-122.16153582049394` |
| `<LOCATION_NAME>`<br>*String* | **Optional.**<br>Location name. | `Philz Coffee` |
| `<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>`<br>*String* | **Required.**<br>WhatsApp business phone number ID. | `106540352242922` |
| `<WHATSAPP_USER_PHONE_NUMBER>`<br>*String* | **Required.**<br>WhatsApp user phone number. | `+16505551234` |

## Example request

Example request to send a location message with a name and address.

```curl
curl 'https://graph.facebook.com/v25.0/106540352242922/messages' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "+16505551234",
  "type": "location",
  "location": {
    "latitude": "37.44216251868683",
    "longitude": "-122.16153582049394",
    "name": "Philz Coffee",
    "address": "101 Forest Ave, Palo Alto, CA 94301"
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
      "id": "wamid.HBgLMTY0NjcwNDM1OTUVAgARGBI1RjQyNUE3NEYxMzAzMzQ5MkEA"
    }
  ]
}
```
