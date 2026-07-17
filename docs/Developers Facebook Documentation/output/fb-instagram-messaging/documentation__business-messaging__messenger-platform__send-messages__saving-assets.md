# Saving assets | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/saving-assets_

---

# Saving assets

Updated: Apr 22, 2026

**Attachment IDs expire after 90 days.** After an attachment ID expires, you need to re-upload your media to get a new attachment ID. Attachments in message threads never expire and are visible until a user deletes the message from the thread. If your use case allows, you can [upload and send in one step](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/saving-assets#upload-and-send) to avoid this expiration.

To optimize sending assets, you may optionally have the Messenger Platform save an asset when it is sent. This is useful if you plan on sending the same attachments repeatedly, since it eliminates the need to upload an asset with each request.

The Messenger Platform offers two APIs that allow you to save assets for later use: the [Send API](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/saving-assets#send-api) and the [Attachment Upload API](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/saving-assets#attachment-upload-api). Both APIs support saving assets from URL and from your local file system.

## Supported asset types

The Messenger Platform supports saving the following asset types, up to 25 MB in size:

- `image` — 8 MB max for URL uploads
- `audio` — `Content-Type` header must use type `audio` (for example, `audio/mp3` )
- `video` — 75-second fetch timeout for URL uploads
- `file`

## Save with the Send API

The Send API allows you to save an asset that is sent with a message, as an alternative to uploading it in advance with the Attachment Upload API. Send a `POST` request with `payload.is_reusable` set to `true` to the `/<PAGE_ID>/messages` endpoint.

### Save from URL

```json
{
  "recipient": {
    "id": "<PSID>"
  },
  "message": {
    "attachment": {
      "type": "<ASSET_TYPE>",
      "payload": {
        "url": "<ASSET_URL>",
        "is_reusable": true
      }
    }
  }
}
```

### Save from file

Submit your message request as form data, and specify the file location in the `filedata` field:

```
curl  \
  -F 'recipient={"id":"<PSID>"}' \
  -F 'message={"attachment":{"type":"<ASSET_TYPE>", "payload":{"is_reusable":true}}}' \
  -F 'filedata=@/tmp/shirt.png;type=image/png' \
  "https://graph.facebook.com/v25.0/me/messages?access_token=<PAGE_ACCESS_TOKEN>"
```

### Response

The response contains an `attachment_id` that can be used to attach the asset to future messages. This ID is private and only the page that originally sent the attachment can reuse it.

```curl
{
  "recipient_id": "1254444444682919",
  "message_id": "m_AG5Hz2Uq7tuwNEhXfYYKj8mJEM_QPpz5jdCK48PnKAjSdjfipqxqMvK8ma6AC8fplwlqLP_5cgXIbu7I3rBN0P",
  "attachment_id": "687799999980546"
}
```

## Save with the Attachment Upload API

The Attachment Upload API allows you to upload assets in advance. This is useful if you know you will need to send particular assets repeatedly. Send a `POST` request to the `/<PAGE_ID>/message_attachments` endpoint.

### Save from URL

```
curl --location --request POST 'https://graph.facebook.com/v2.10/me/message_attachments?access_token=<PAGE_ACCESS_TOKEN>' \
--header 'Content-Type: application/json' \
--data-raw '{
  "message":{
    "attachment":{
      "type":"image",
      "payload":{
        "url":"http://www.messenger-rocks.com/image.jpg",
        "is_reusable": true
      }
    }
  }
}'
```

### Save from file

Submit your request as form data, and specify the file location in the `filedata` field:

```
curl  \
  -F 'recipient={"id":"<PSID>"}' \
  -F 'message={"attachment":{"type":"<ASSET_TYPE>", "payload":{"is_reusable":true}}}' \
  -F 'filedata=@/tmp/shirt.png;type=image/png' \
  "https://graph.facebook.com/v25.0/me/messages?access_token=<PAGE_ACCESS_TOKEN>"
```

### Response

```curl
{
  "attachment_id":"1857777774821032"
}
```

## Send a saved asset

To send a message with a previously uploaded asset (uploaded with `is_reusable` set to `true`), send a `POST` request to the `/<PAGE_ID>/messages` endpoint with the `attachment_id` in the payload:

```
curl -X POST "https://graph.facebook.com/<LATEST_API_VERSION>/<PAGE_ID>/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "recipient": {
      "id": "<PSID>"
    },
    "message": {
      "attachment": {
        "type": "image",
        "payload": {
          "attachment_id": "<ATTACHMENT_ID>"
        }
      }
    }
  }' \
  -F "access_token=<PAGE_ACCESS_TOKEN>"
```

## Upload and send in one step

You can upload media and send it in a single API request. This avoids the 90-day attachment ID expiration since the attachment is not saved for reuse.

Do **not** set `is_reusable` to `true` when uploading and sending in one step. Attachments in the user’s message thread are always private.

```
curl -X POST "https://graph.facebook.com/<LATEST_API_VERSION>/<PAGE_ID>/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "recipient": {
      "id": "<PSID>"
    },
    "message": {
      "attachment": {
        "type": "image",
        "payload": {
          "url": "https://example.com/image.jpg"
        }
      }
    }
  }' \
  -F "access_token=<PAGE_ACCESS_TOKEN>"
```

## Properties

For attachments from a URL, provide the following properties in the body of the request as a JSON object. For attachments from file, send properties as form data.

### `message.attachment` properties

| Property | Type | Description |
| --- | --- | --- |
| `type` | String | The type of the attachment. Must be one of:<br>`image`<br>,<br>`video`<br>,<br>`audio`<br>,<br>`file`<br>. |
| `payload` | Object | Object that describes the attachment. See<br>`payload`<br>properties below. |

### `message.attachment.payload` properties

| Property | Type | Description |
| --- | --- | --- |
| `url` | String | *Optional.*<br>URL of the file to upload. Max file size is 8 MB for images and 25 MB for all other file types (after encoding). Timeout is 75 seconds for videos and 10 seconds for all other file types. |
| `is_reusable` | Boolean | *Optional.*<br>Defaults to<br>`false`<br>. Set to<br>`true`<br>only when you upload and send in separate steps. Do<br>**not**<br>set to<br>`true`<br>if you upload and send in one API call. Attachment IDs expire after 90 days. |
| `attachment_id` | String | *Optional.*<br>The ID of a previously uploaded attachment. Used when sending a saved asset. |

## Error codes

| Error code | Subcode | Description |
| --- | --- | --- |
| 100 | 2018074 | Possible invalid ID or you do not own the attachment. |
| 100 | 2018008 | Failed to fetch the file from the URL. Check that the URL is valid, with a valid SSL certificate, valid file size, and that the server is responding fast enough to avoid timeouts. |
| 100 | 2018294 | Video upload timed out or video is corrupted. Videos that cannot be fetched within 75 seconds time out. |
| 100 | 2018047 | Upload attachment failure. A common cause is that the provided media type does not match the type of file provided in the URL. |

## Learn more

### Developer Support

- Use the [Meta Status tool](https://metastatus.com) to check for the status and outages of Meta business products.
- Use the [Meta Developer Support tool](https://developers.facebook.com/support) to report bugs and view reported bugs, get help with Ads or Business Manager, and more.
