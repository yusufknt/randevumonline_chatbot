# Document messages

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/document-messages_

---

# Document messages

Updated: Nov 3, 2025

Document messages are messages that display a document icon, linked to a document, that a WhatsApp user can tap to download.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/441287424_3695370760733536_48188157634176922_n.png?_nc_cat=101&ccb=1-7&_nc_sid=e280be&_nc_ohc=G-Tb5RIqv4IQ7kNvwEtlAkK&_nc_oc=AdrgILfkR3hGV-RpelBUb2mOhq7UeWYssLEOSoZVYzDKw25R_Vb-rR9dSsreoLZiJaQ&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=egVa_bPbzSo8cOmWZb7rHw&_nc_ss=7b20f&oh=00_Af5Go6QqTVkNwX7FY6tAE_wA8pITpb4mmL8kEwlR2SrsDw&oe=6A1C2C88)

## Request syntax

Use the [Messages API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api#post-version-phone-number-id-messages) to send a document message to a WhatsApp user.

```html
curl 'https://graph.facebook.com/<API_VERSION>/<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>/messages' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "<WHATSAPP_USER_PHONE_NUMBER>",
  "type": "document",
  "document": {
    "id": "<MEDIA_ID>", <!-- Only if using uploaded media -->
    "link": "<MEDIA_URL>", <!-- Only if using hosted media (not recommended) -->
    "caption": "<MEDIA_CAPTION_TEXT>",
    "filename": "<MEDIA_FILENAME>",
    "caption": "<MEDIA_CAPTION_TEXT>"
  }
}'
```

## Request parameters

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<ACCESS_TOKEN>`<br>*String* | **Required.**<br>[System token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens) or [business token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens). | `EAAA...` |
| `<API_VERSION>`<br>*String* | **Optional.**<br>Graph API version. | v25.0 |
| `<MEDIA_CAPTION_TEXT>`<br>*String* | **Optional.**<br>Media asset caption text.<br>Maximum 1024 characters. | `Lucky Shrub Invoice` |
| `<MEDIA_FILENAME>`<br>*String* | **Optional.**<br>Document filename, with extension. The WhatsApp client will use an appropriate file type icon based on the extension. | `lucky-shrub-invoice.pdf` |
| `<MEDIA_ID>`<br>*String* | **Required if using uploaded media, otherwise omit.**<br>ID of the [uploaded media asset](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/media#upload-media). | `1013859600285441` |
| `<MEDIA_URL>`<br>*String* | **Required if using hosted media, otherwise omit.**<br>URL of the media asset hosted on your public server. For better performance, we recommend using `id` and an [uploaded media asset ID](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/media#upload-media) instead. | `https://www.luckyshrub.com/invoices/FmOzfD9cKf/lucky-shrub-invoice.pdf` |
| `<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>`<br>*String* | **Required.**<br>WhatsApp business phone number ID. | `106540352242922` |
| `<WHATSAPP_USER_PHONE_NUMBER>`<br>*String* | **Required.**<br>WhatsApp user phone number. | `+16505551234` |

## Supported document types

| Document Type | Extension | MIME Type | Max Size |
| --- | --- | --- | --- |
| Text | .txt | text/plain | 100 MB |
| Microsoft Excel | .xls | application/vnd.ms-excel | 100 MB |
| Microsoft Excel | .xlsx | application/vnd.openxmlformats-officedocument.spreadsheetml.sheet | 100 MB |
| Microsoft Word | .doc | application/msword | 100 MB |
| Microsoft Word | .docx | application/vnd.openxmlformats-officedocument.wordprocessingml.document | 100 MB |
| Microsoft PowerPoint | .ppt | application/vnd.ms-powerpoint | 100 MB |
| Microsoft PowerPoint | .pptx | application/vnd.openxmlformats-officedocument.presentationml.presentation | 100 MB |
| PDF | .pdf | application/pdf | 100 MB |

Only the above listed document types are officially supported and guaranteed to display correctly in the WhatsApp client. Other file types may be sent via the API, but they are not supported and may not be handled as expected.

## Example request

Example request to send a PDF in a document message with a caption to a WhatsApp user.

```curl
curl 'https://graph.facebook.com/v25.0/106540352242922/messages' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "+16505551234",
  "type": "document",
  "document": {
    "id": "1376223850470843",
    "filename": "order_abc123.pdf",
    "caption": "Your order confirmation (PDF)"
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
