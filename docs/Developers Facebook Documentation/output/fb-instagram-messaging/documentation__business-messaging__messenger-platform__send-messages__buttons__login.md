# Log in button | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/buttons/login_

---

# Log in button

Updated: Apr 22, 2026

The log in button triggers the [account linking authentication flow](https://developers.facebook.com/documentation/business-messaging/messenger-platform/identity/account-linking), which lets you link the message recipient’s identity on Messenger with their account on your site by directing them to your web-based login flow for authentication.

For more on using the log in button for account linking, see [Account linking](https://developers.facebook.com/documentation/business-messaging/messenger-platform/identity/account-linking).

## Supported usage

The log in button is supported for use with the following:

- Generic template
- List template
- Button template
- Media template

## Properties

| Property | Type | Description |
| --- | --- | --- |
| `type` | String | Must be<br>`account_link`<br>. |
| `url` | String | [Authentication](https://developers.facebook.com/documentation/business-messaging/messenger-platform/identity/account-linking)<br>callback URL. Must use HTTPS protocol. |

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
          "text": "Try the log in button!",
          "buttons": [
            {
              "type": "account_link",
              "url": "https://www.example.com/authorize"
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
