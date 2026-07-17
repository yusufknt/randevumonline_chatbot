# Game play button | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/buttons/game-play_

---

# Game play button

Updated: Apr 22, 2026

The game play button launches an Instant Game that is associated with your Facebook Page. To customize how your game is opened, you can set a `payload` property in the request that is sent to the game on launch, as well as an optional `game_metadata.player_id` or `game_metadata.context_id` property, which allows your bot to start the game in a specific context against a single player or an existing group.

## Properties

| Property | Type | Description |
| --- | --- | --- |
| `type` | String | Type of button. Must be<br>`game_play`<br>. |
| `title` | String | Button title, for example “Play”. |
| `payload` | String | *Optional.*<br>Serialized JSON data sent to the game on launch. Deserialized by the Instant Games SDK. |
| `game_metadata` | Object | *Optional.*<br>Parameters specific to Instant Games. See<br>`game_metadata`<br>properties below. |

### `game_metadata` properties

By providing the optional `game_metadata`, you can trigger the game to be started against a specific `player_id` or in a specific `context_id`.

| Property | Type | Description |
| --- | --- | --- |
| `player_id` | String | *Optional.*<br>Player ID (Instant Game namespace) to play against. |
| `context_id` | String | *Optional.*<br>Context ID (Instant Game namespace) of the thread to play in. |

## Sample request

```http
{
  "type":"game_play",
  "title":"Play",
  "payload":"{<SERIALIZED_JSON_PAYLOAD>}",
  "game_metadata": { // Only one of the below
    "player_id": "<PLAYER_ID>",
    "context_id": "<CONTEXT_ID>"
  }
}
```

## Sample request with template

```bash
curl -X POST "https://graph.facebook.com/<LATEST_API_VERSION>/<PAGE_ID>/messages?access_token=<PAGE_ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "recipient": {
      "id": "<PSID>"
    },
    "message": {
      "attachment": {
        "type": "template",
        "payload": {
          "template_type": "button",
          "text": "Try the game play button!",
          "buttons": [
            {
              "type": "game_play",
              "title": "Play",
              "payload": "<SERIALIZED_JSON_PAYLOAD>",
              "game_metadata": {
                "player_id": "<PLAYER_ID>"
              }
            }
          ]
        }
      }
    }
  }'
```

## Sample response

```js
{
  "recipient_id": "1254477777772919",
  "message_id": "AG5Hz2Uq7tuwNEhXfYYKj8mJEM_QPpz5jdCK48PnKAjSdjfipqxqMvK8ma6AC8fplwlqLP_5cgXIbu7I3rBN0P"
}
```

## Related

- [Game play webhook event](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/webhook-events/messaging_game_plays) — the event sent to your bot when a user finishes a game round
