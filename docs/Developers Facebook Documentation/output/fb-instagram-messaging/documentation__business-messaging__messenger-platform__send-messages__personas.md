# Personas | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/personas_

---

# Personas

Updated: Apr 22, 2026

The Personas API allows you to create and manage personas for your business messaging experience. A persona may be backed by a human agent or a bot. When you introduce a persona into a conversation, the persona’s profile picture is shown and all messages sent by the persona are accompanied by an annotation above the message that states the persona name and the business it represents.

## Best practices

- The `name` of a persona is freeform with a maximum of 50 characters. A first name and last name or initial, such as “John Z.”, is recommended.
- The Page name is still shown at the top of the conversation when using a persona. It is not necessary to include the company name in the `name` field.
- The persona should not be overly generic.
- The persona should be clearly distinguished from the Page or bot itself.
- The persona should not attempt to deceive the recipient.
- You can create a persona quickly. It is not necessary to sync your entire database of agents in advance.

## Before you start

You will need the following:

- A Page access token requested by someone who can perform the `MESSAGING` task on the Page
- The `pages_messaging` permission
- Your `<PAGE_ID>`
- A profile picture URL for your persona. The API downloads the image and re-uploads it to Meta servers. The image size may not exceed 8 MB.

## Create a persona

To create a persona, send a `POST` request to the `/<PAGE_ID>/personas` endpoint with the `name` and `profile_picture_url` parameters.

### Request parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `name` | String | The display name of the persona. Maximum 50 characters. |
| `profile_picture_url` | String | The URL of the profile picture for the persona. The image is downloaded and re-uploaded to Meta servers. |

### Sample request

```
curl -X POST "https://graph.facebook.com/<LATEST_API_VERSION>/<PAGE_ID>/personas?access_token=<PAGE_ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Adam",
    "profile_picture_url": "https://example.com/adam-image.jpg"
  }'
```

### Sample response

```json
{
  "id": "<PERSONA_ID>"
}
```

| Property | Type | Description |
| --- | --- | --- |
| `id` | String | The unique ID of the persona. |

## Get all personas

To get a list of all personas associated with your Page, send a `GET` request to the `/<PAGE_ID>/personas` endpoint. Results are paginated using cursor-based pagination.

You can use the `fields` parameter to select which fields to return. You can also use the `limit`, `after`, and `before` parameters to paginate large result sets.

### Sample request

```
curl -X GET "https://graph.facebook.com/<LATEST_API_VERSION>/<PAGE_ID>/personas?access_token=<PAGE_ACCESS_TOKEN>"
```

### Sample response

```json
{
  "data": [
    {
      "name": "Adam",
      "profile_picture_url": "https://facebook.com/adam-image.jpg",
      "id": "<PERSONA_A_ID>"
    },
    {
      "name": "David Mark",
      "profile_picture_url": "https://facebook.com/david-image.jpg",
      "id": "<PERSONA_B_ID>"
    }
  ],
  "paging": {
    "cursors": {
      "before": "QVFIUlMtR2ZATQlRtVUZALUlloV1",
      "after": "QVFIUkpnMGx0aTNvUjJNVmJUT0Yw"
    }
  }
}
```

| Property | Type | Description |
| --- | --- | --- |
| `data` | Array | An array of persona objects. |
| `paging` | Object | Contains<br>`before`<br>and<br>`after`<br>cursors for paginating large result sets. |

## Get a specific persona

To get the details of a specific persona, send a `GET` request to the `/<PERSONA_ID>` endpoint.

### Sample request

```
curl -X GET "https://graph.facebook.com/<LATEST_API_VERSION>/<PERSONA_ID>?access_token=<PAGE_ACCESS_TOKEN>"
```

### Sample response

```json
{
  "name": "Adam",
  "profile_picture_url": "https://facebook.com/adam-image.jpg",
  "id": "<PERSONA_ID>"
}
```

| Property | Type | Description |
| --- | --- | --- |
| `name` | String | The display name of the persona. |
| `profile_picture_url` | String | The URL of the profile picture for the persona. |
| `id` | String | The unique ID of the persona. |

## Send a message as a persona

To send a message as a persona, send a `POST` request to the `/<PAGE_ID>/messages` endpoint with the `persona_id` parameter along with the `recipient` and `message` parameters. If you do not include `persona_id`, the message is sent using the Page’s identity.

### Sample request

```
curl -X POST "https://graph.facebook.com/<LATEST_API_VERSION>/<PAGE_ID>/messages?access_token=<PAGE_ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "recipient": { "id": "<PSID>" },
    "message": { "text": "Hello world!" },
    "persona_id": "<PERSONA_ID>"
  }'
```

## Delete a persona

To delete a persona, send a `DELETE` request to the `/<PERSONA_ID>` endpoint. Deleting a persona is a soft delete — messages previously sent by this persona continue to appear in the conversation history, but the persona can no longer send new messages.

### Sample request

```
curl -X DELETE "https://graph.facebook.com/<LATEST_API_VERSION>/<PERSONA_ID>?access_token=<PAGE_ACCESS_TOKEN>"
```

### Sample response

```json
{
  "success": true
}
```

| Property | Type | Description |
| --- | --- | --- |
| `success` | Boolean | Whether the delete operation succeeded. |

## Learn more

### Developer Support

- Use the [Meta Status tool](https://metastatus.com) to check for the status and outages of Meta business products.
- Use the [Meta Developer Support tool](https://developers.facebook.com/support) to report bugs and view reported bugs, get help with Ads or Business Manager, and more.
