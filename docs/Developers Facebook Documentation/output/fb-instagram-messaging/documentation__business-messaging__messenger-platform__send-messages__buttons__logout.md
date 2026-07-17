# Log out button | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/buttons/logout_

---

# Log out button

Updated: Apr 22, 2026

The log out button triggers the account unlinking flow, which unlinks the message recipient’s identity on Messenger from their account on your site.

For more on using the log out button for account unlinking, see [Account linking](https://developers.facebook.com/documentation/business-messaging/messenger-platform/identity/account-linking).

## Supported usage

The log out button is supported for use with the following:

- Generic template
- List template
- Button template
- Media template

## Properties

| Property | Type | Description |
| --- | --- | --- |
| `type` | String | Must be<br>`account_unlink`<br>. |

## Sample request

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
          "text": "Try the log out button!",
          "buttons": [
            {
              "type": "account_unlink"
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
