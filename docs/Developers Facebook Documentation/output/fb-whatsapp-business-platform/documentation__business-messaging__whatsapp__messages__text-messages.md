# Text messages

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/text-messages_

---

# Text messages

Updated: Nov 3, 2025

Text messages are messages containing only a text body and an optional link preview.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/440742591_797870012016470_1123226266833971975_n.png?_nc_cat=106&ccb=1-7&_nc_sid=e280be&_nc_ohc=sLrin0IGTz0Q7kNvwGdCQAP&_nc_oc=AdqwApMoa_IuDUFaNDAbMlDFqcyASKyq0g4KL4tseUUw2xOzTibyNEVEJa8ySZAj0xU&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=A3IMczsPWxUd4qy7qDZ-qA&_nc_ss=7b20f&oh=00_Af6SfoVCh82GmJx2l0S3VDB4OXxHMs7_HyqTasixaWijLQ&oe=6A1C146B)

## Request syntax

Use the [Messages API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api#post-version-phone-number-id-messages) to send a text message to a WhatsApp user.

```html
curl 'https://graph.facebook.com/<API_VERSION>/<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>/messages' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <ACCESS_TOKEN>' \
-d '
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "<WHATSAPP_USER_PHONE_NUMBER>",
  "type": "text",
  "text": {
    "preview_url": <ENABLE_LINK_PREVIEW>,
    "body": "<BODY_TEXT>"
  }
}'
```

### Request parameters

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<ACCESS_TOKEN>`<br>*String* | **Required.**<br>[System token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens) or [business token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens). | `EAAA...` |
| `<API_VERSION>`<br>*String* | **Optional.**<br>Graph API version. | v25.0 |
| `<BODY_TEXT>`<br>*String* | **Required.**<br>Body text. URLs are automatically hyperlinked.<br>Maximum 4096 characters. | `As requested, here's the link to our latest product: https://www.meta.com/quest/quest-3/` |
| `<ENABLE_LINK_PREVIEW>`<br>*Boolean* | **Optional.**<br>Set to `true` to have the WhatsApp client attempt to render a link preview of any URL in the body text string.<br>See [Link Preview](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/text-messages#link-preview) below. | `true` |
| `<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>`<br>*String* | **Required.**<br>WhatsApp business phone number ID. | `106540352242922` |
| `<WHATSAPP_USER_PHONE_NUMBER>`<br>*String* | **Required.**<br>WhatsApp user phone number. | `+16505551234` |

## Link preview

You can have the WhatsApp client attempt to render a preview of the first URL in the body text string, if it contains one. URLs must begin with `http://` or `https://`. If multiple URLs are in the body text string, only the first URL will be rendered.

If omitted, or if unable to retrieve a link preview, a clickable link will be rendered instead.

## Example request

Example request to send a text message with link previews enabled and a body text string that contains a link.

```curl
curl 'https://graph.facebook.com/v25.0/106540352242922/messages' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "+16505551234",
  "type": "text",
  "text": {
    "preview_url": true,
    "body": "As requested, here'\''s the link to our latest product: https://www.meta.com/quest/quest-3/"
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
