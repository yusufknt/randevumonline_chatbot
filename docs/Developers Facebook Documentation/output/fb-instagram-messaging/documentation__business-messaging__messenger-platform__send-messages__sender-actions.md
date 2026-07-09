# Sender Actions | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/sender-actions_

---

# Sender Actions

Updated: Jan 21, 2026

This guide explains how to display your actions in a conversation to let message recipients know that you have seen and are processing their message.

## Display a Sender Action

To display the action for a sender in the conversation, send a `POST` request to the [`/PAGE-ID/messages` endpoint](https://developers.facebook.com/docs/graph-api/reference/page/messages) with the `sender_action` parameter set to `typing_on`.

```curl
curl -X POST -H "Content-Type: application/json" -d '{
  "recipient":{
    "id":"<PSID>"
  },
  "sender_action":"typing_on"
}' "https://graph.facebook.com/VERSION/PAGE-ID/messages?access_token=PAGE-ACCESS_TOKEN;"
```

## React or unreact to a message

To send a reaction, send a `POST` request to `/PAGE-ID/messages` with `recipient` containing the Page-scoped ID (`<PSID>`); `sender_action` set to `react`; `payload` containing the `message_id` set to the message ID to react to; and `reaction` set to any emoji reaction(`<😊/🎉/etc>`) or a valid UTF-8 representation of an emoji.

To edit a sent reaction, repeat this request with the reaction set to the new emoji reaction.

To remove a reaction, repeat this request with `sender_action` set to unreact with the payload containing `message_id` only.

Sample Request

```curl
curl -X POST -H "Content-Type: application/json" -d '{
    "recipient": {
      "id": "{PSID}"
    },
    "sender_action": "react",  // Or set to unreact to remove the reaction
    "payload": {
      "message_id": "<MESSAGE_ID>",
      "reaction":"😊/ 🎉/ \ud83d\udc4b" // Omit if removing a reaction
    }
  }' "https://graph.facebook.com/v25.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
```

On success, your app will receive the following JSON response with the recipient’s ID and the message ID.

```json
{ "recipient_id": "PAGE-SCOPED-ID" }
```

### Limitations

- Requests to display sender action should only include the `sender_action` parameter and the `recipient` object. All other Send API properties, such as text and templates, should be sent in a separate request.
- The recipient must be signed in for sender actions to be displayed.

Visit the [Page Messages reference](https://developers.facebook.com/docs/graph-api/reference/page/messages#parameters) for a complete list of sender actions.

### Best Practices

- Send the `mark_seen` indicator when your bot receives a message so that the user does not feel ignored.
- Send the `typing_on` indicator when your bot receives a message it will respond to. This helps create a conversational experience.
- Send `typing_on` and `typing_off` actions in the [separate batch requests](https://developers.facebook.com/docs/graph-api/making-multiple-requests). Batched requests are executed in order very quickly. This quick execution may result in the `typing_on` indicator being displayed for a fraction of a second if both actions are sent in the same batch.
- Do not allow an unnatural amount of time (too long or too short) to pass between `typing_on` and `typing_off` sender actions. Ideally, the user should feel that a real person was typing the message in the elapsed time.

## See Also

- For a complete list of API calls and request properties, see the [Send API Reference](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/send-api).

### Developer Support

- Use the [Meta Status tool](https://metastatus.com) to check for the status and outages of Meta business products.
- Use the [Meta Developer Support tool](https://developers.facebook.com/support) to report bugs and view reported bugs, get help with Ads or Business Manager, and more.
