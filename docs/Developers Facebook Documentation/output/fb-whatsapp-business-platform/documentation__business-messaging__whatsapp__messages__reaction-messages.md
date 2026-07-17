# Reaction messages | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/reaction-messages_

---

# Reaction messages

Updated: Nov 3, 2025

Reaction messages are emoji-reactions that you can apply to a previous WhatsApp user message that you have received.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/440791676_2613895758778914_1777908069161322734_n.png?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=tfwFYMS2fTEQ7kNvwGiif_j&_nc_oc=AdqZSoR0tv6XgCupny-IVOROiejuvFq8JE6t-a-hIvPavro_gY_OJWRxLYyJtcDTaL8&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=PNz0yNmAsWzdLFJA5ZSqOA&_nc_ss=7b20f&oh=00_Af4QCtpvlGlyeNUCjXwZN6QhSd9fANv64VVC9rPkOhO16Q&oe=6A1C0931)

## Limitations

When sending a reaction message, only a [sent message webhook](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/status) (`status` set to `sent`) will be triggered; delivered and read message webhooks will not be triggered.

## Request syntax

Use the [Messages API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api#post-version-phone-number-id-messages) to apply an emoji reaction on a message you have received from a WhatsApp user.

```html
curl 'https://graph.facebook.com/<API_VERSION>/<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>/messages' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <ACCESS_TOKEN>' \
-d '
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "<WHATSAPP_USER_PHONE_NUMBER>",
  "type": "reaction",
  "reaction": {
    "message_id": "<WHATSAPP_MESSAGE_ID>",
    "emoji": "<EMOJI>"
  }
}'
```

## Request parameters

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<ACCESS_TOKEN>`<br>*String* | **Required.**<br>[System token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens) or [business token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens). | `EAAA...` |
| `<API_VERSION>`<br>*String* | **Optional.**<br>Graph API version. | v25.0 |
| `<EMOJI>`<br>*String* | **Required.**<br>Unicode escape sequence of the emoji, or the emoji itself, to apply to the user message. | Unicode escape sequence example:<br>`\uD83D\uDE00`<br>Emoji example:<br>😀 |
| `<WHATSAPP_MESSAGE_ID>`<br>*String* | **Required.**<br>WhatsApp message ID of message you want to apply the emoji to.<br>If the message you are reacting to is more than 30 days old, doesn’t correspond to any message in the chat thread, has been deleted, or is itself a reaction message, the reaction message will not be delivered and you will receive a **messages** webhook with error code `131009`. | `wamid.HBgLMTY0NjcwNDM1OTUVAgASGBQzQUZCMTY0MDc2MUYwNzBDNTY5MAA=` |
| `<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>`<br>*String* | **Required.**<br>WhatsApp business phone number ID. | `106540352242922` |
| `<WHATSAPP_USER_PHONE_NUMBER>`<br>*String* | **Required.**<br>WhatsApp user phone number. | `+16505551234` |

## Example request

Example request to apply the grinning face emoji (😀) to a previously received user message.

```curl
curl 'https://graph.facebook.com/v25.0/106540352242922/messages' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "+16505551234",
  "type": "reaction",
  "reaction": {
    "message_id": "wamid.HBgLMTY0NjcwNDM1OTUVAgASGBQzQUZCMTY0MDc2MUYwNzBDNTY5MAA=",
    "emoji": "\uD83D\uDE00"
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
