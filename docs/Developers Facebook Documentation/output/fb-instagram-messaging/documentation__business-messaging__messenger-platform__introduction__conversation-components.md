# Conversation Components | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/introduction/conversation-components_

---

# Conversation Components

Updated: Oct 13, 2020

Conversations are a lot more than simple text messages when you are building a bot on the Messenger Platform. In addition to text, the Platform allows you to send rich-media, like audio, video, and images, and provides a set of structured messaging options in the form of message templates, quick replies, buttons and more. This is intended to be an overview of the components that are available for you to create your Messenger experience in-conversation.

In addition to these conversation components, the Messenger Platform supports a full webview that allows you to enrich your in-conversation Messenger experience by extending it to the web. For more information on using the webview, see [Webview](https://developers.facebook.com/documentation/business-messaging/messenger-platform/webview).

### Available Conversation Components

- [Text Messages](https://developers.facebook.com/documentation/business-messaging/messenger-platform/introduction/conversation-components#text_messages)
- [Assets & Attachments](https://developers.facebook.com/documentation/business-messaging/messenger-platform/introduction/conversation-components#attachments)
- [Message Templates](https://developers.facebook.com/documentation/business-messaging/messenger-platform/introduction/conversation-components#templates)
- [Quick Replies](https://developers.facebook.com/documentation/business-messaging/messenger-platform/introduction/conversation-components#quick_replies)
- [Sender Actions](https://developers.facebook.com/documentation/business-messaging/messenger-platform/introduction/conversation-components#sender_actions)
- [Welcome Screen](https://developers.facebook.com/documentation/business-messaging/messenger-platform/introduction/conversation-components#welcome_screen)
- [Persistent Menu](https://developers.facebook.com/documentation/business-messaging/messenger-platform/introduction/conversation-components#persistent_menu)

## Text Messages

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/13503471_1613963512265939_694041731_n.png?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=87BfivWetT4Q7kNvwE_p1TT&_nc_oc=AdqO0melxfs3_MnM5TjOdjQv7y9iR57ZhTBxLhbI2RPsTfdN06h8que_CfNqD8ZsUms&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=ZNGPWvbdPLP9Gyxh1exH7g&_nc_ss=7b20f&oh=00_Af4UbBiaIDvtwc3-r1c9mk-Sk_18LxaZKMY7tgyzqAWDMg&oe=6A1C17B7)

Simple text is the foundation of any experience on Messenger, and is one of the most important tools at your disposal if you goal is to create a conversational experience. Try processing text messages with the Messenger Platform’s [built-in natural language processing (NLP)](https://developers.facebook.com/documentation/business-messaging/messenger-platform/built-in-nlp) feature to handle all kinds of interactions with simple text.

## Assets & Attachments

In addition to text, the Messenger Platform allows you to send rich media assets as standalone messages or attached to structured [message templates](https://developers.facebook.com/documentation/business-messaging/messenger-platform/introduction/conversation-components#templates). Supported asset types included the following:

- Audio
- Video
- Images
- Files

Assets may be sent from a URL or your file system. For assets you intend to send multiple times, you may upload them in advance with the [Attachment Upload API](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/attachment-upload-api) or upload them the first time they are sent with the [Send API](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/saving-assets#send_api) to eliminate the time and bandwidth overhead of uploading with each send. Saved assets are sent with an `attachment_id` that is assigned when they are uploaded.

## Message Templates

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/14235537_178238889274354_2098325353_n.png?_nc_cat=110&ccb=1-7&_nc_sid=e280be&_nc_ohc=8_nri4WhoXYQ7kNvwG9W4sE&_nc_oc=Adpt3NhFSK64LAwTHwltloENy4WzJfFRP0Gm57B_J1IjRO5YgxdE9rgJhAc9uVXbJ3o&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=ZNGPWvbdPLP9Gyxh1exH7g&_nc_ss=7b20f&oh=00_Af5HRG7cOgcguKf1j4yWxDGaeDpVFgwYl2HSkgHO9q-hkA&oe=6A1C2B52)

Message templates are structured message types intended to support different use cases, and are useful for presenting information in-conversation that would be difficult to render or sloppy-looking with simple text. Templates also support [buttons](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/buttons) that extend their functionality.

The following message templates are available:

- [Generic template](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/templates#generic)
- [Button template](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/templates#button)
- [Receipt template](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/templates#receipt)
- [Airline templates](https://developers.facebook.com/docs/messenger-platform/send-messages/template/airline)
- [Media Template](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/templates#media)

Message templates also support a set of buttons that add functionality, such as opening the webview, sending a postback to your webhook, sharing content, and more.

## Quick Replies

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/653704888_1459945669197416_1856728963803525854_n.png?_nc_cat=106&ccb=1-7&_nc_sid=e280be&_nc_ohc=8fJ79ATl9jYQ7kNvwG_yFYf&_nc_oc=AdpSh_nE5hC9J0f8-gfCA7nFPiBZAWYqcQQ6lP25GBdRX5-h4vqolVIaP5heVuT_kzQ&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=ZNGPWvbdPLP9Gyxh1exH7g&_nc_ss=7b20f&oh=00_Af4nFgOG4IPEszfQQjhJ67B4OyfrwrgutgfojT7UHLTttw&oe=6A1C14DE)

Quick Replies allow you present a preset set of options to the message recipient, which appear prominently above the composer. When a quick reply is tapped, the set is replaced with a single text message that is sent to your webhook. You may also add an image to a Quick Reply.

## Sender Actions

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/13480169_570751053131489_689799179_n.png?_nc_cat=111&ccb=1-7&_nc_sid=e280be&_nc_ohc=v-UwtDo0v0oQ7kNvwGeRcn6&_nc_oc=Adrt2tYkjrvqX63VdWkwEUMFBmSS0tn_-maYn9fqLwo1XI74n_t892PRho9Ja32PbDQ&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=ZNGPWvbdPLP9Gyxh1exH7g&_nc_ss=7b20f&oh=00_Af5TS8IzO_iC7COgI_XyqJgFN0S3Y2uYutZfDIDBZA6xTg&oe=6A1C31E4)

An important aspect of creating a Messenger bot is setting expectations. Sender actions are an important tool for accomplishing this that gives you the ability to programmatically control the standard Messenger typing, and read receipt indicators in-conversation. For example, when you begin processing a message, you might set the read receipt indicator so the person interacting with your bot knows their message has been seen, then you might set the typing indicator to show them that a response is in-progress.

## Welcome Screen

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/641631633_1445181510673832_8753613653176897326_n.png?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=qrb0ahqgNj8Q7kNvwGmhfl7&_nc_oc=AdoZZ7Ka-4eyqDBTzw-RF9iaBpwfSPgrqrDF0xyvTzUfKoWKakS7lHXwqErQNxW3lCY&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=ZNGPWvbdPLP9Gyxh1exH7g&_nc_ss=7b20f&oh=00_Af7HZnmr5a2HqOD1r2d4WTpgkAQMzlntSiKmbQOt7Li5JA&oe=6A1C2A74)

The welcome screen is the first thing people see when they start a new conversation with your Messenger bot, and includes the name, description, profile picture and cover photo from your Facebook Page. You may also set optional [greeting text](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/messenger-profile-api/greeting) for the welcome screen, which can be used to introduce the purpose of your bot.

A conversation with your bot begins when the [get started button](https://developers.facebook.com/documentation/business-messaging/messenger-platform/discovery/welcome-screen) is tapped.

## Persistent Menu

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/641632137_1445181560673827_7485593691845895443_n.jpg?_nc_cat=110&ccb=1-7&_nc_sid=e280be&_nc_ohc=2biFt335RaMQ7kNvwF8eFY4&_nc_oc=AdpooRuXk8UT2fIfxdsuDOcAbFEK04k-WvSW6PJVxpShcAWPH5ZkB_PpNw5NTjiQrkM&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=ZNGPWvbdPLP9Gyxh1exH7g&_nc_ss=7b20f&oh=00_Af6pLdgbSk3Y0v0qmDYy2Z5zv48HtxvpDZrM8Pn83sPzCA&oe=6A1C1C16)

The persistent menu is an always-on user interface element that helps people discover and more easily access your bot’s functionality throughout the conversation. This menu should contain top-level actions that a person can enact at any point. You may also optionally make the persistent menu the only way to interact with your bot by disabling the composer.
