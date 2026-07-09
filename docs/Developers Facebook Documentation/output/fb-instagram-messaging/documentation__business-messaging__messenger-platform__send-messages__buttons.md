# Buttons | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/buttons_

---

# Buttons

Updated: Apr 22, 2026

Most [message templates](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/templates), as well as the [persistent menu](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/messenger-profile-api/persistent-menu), support buttons that invoke different types of actions. These buttons allow you to offer the message recipient actions they can take in response to the template, such as opening the Messenger webview, starting a payment flow, sending a postback message to your webhook, and more.

For message templates, buttons are defined by objects in the `buttons` array. For the persistent menu, buttons are defined by objects in the `call_to_actions` array.

## Button types

| Button | Type value | Description |
| --- | --- | --- |
| [URL button](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/buttons/url) | `web_url` | Opens a web page in the Messenger webview |
| [Postback button](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/buttons/postback) | `postback` | Sends a postback event to your webhook |
| [Call button](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/buttons/call) | `phone_number` | Dials a phone number |
| [Log in button](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/buttons/login) | `account_link` | Triggers the account linking authentication flow |
| [Log out button](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/buttons/logout) | `account_unlink` | Unlinks a linked account |
| [Game play button](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/buttons/game-play) | `game_play` | Launches an Instant Game |

## Best practices

- Use buttons to prompt for follow-up or further interaction with a particular message.
- Start with a verb to help people understand the action they are taking.
- Use URL buttons for tasks that you want completed on your website (for example, purchases or account linking). Make it clear you are sending people outside of Messenger.
- Send a response after someone taps a callback button. This confirms that you have processed or completed their action (for example, canceling a reservation or answering a question).
- Do not use buttons when their action depends on the current state of the bot, since buttons are permanently available in the thread.
- Do not use more than 1-3 words or add punctuation. Keep your text under 20 characters, including spaces.
- Do not rely on URLs for every button. The more interactions you can build within Messenger, the more seamless your experience will be.
- Do not use a single callback button. When there is only one button to choose from, people often think it is a continuation of your message text and do not understand it is an action you want them to take.

## Learn more

- [Quick replies](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/quick-replies) — get message recipient input with inline buttons
- [Message templates](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/templates) — structured messages that support buttons
- [Persistent menu](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/messenger-profile-api/persistent-menu) — always-available menu with button actions
