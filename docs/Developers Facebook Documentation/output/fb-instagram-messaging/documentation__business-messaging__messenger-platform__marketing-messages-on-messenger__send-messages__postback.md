# Postback Button Setup | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/send-messages/postback_

---

# Postback Button Setup

Updated: Nov 21, 2025

Postback buttons allow you to define a payload that will be sent to your webhook whenever a user clicks the button. This can enable a feature that allows for automated chat responses with clients. To get started, familiarize yourself with the data that we will send your webhook on postback button click:

```json
{
  "field": "messaging_postbacks",
  "value": {
    "sender": {
      "user_ref": "USER_REF_ID"
    },
    "recipient": {
      "id": "PAGE_ID"
    },
    "timestamp": "1527459824",
    "postback": {
      "mid": "m_MESSAGE_ID",
      "title": "TITLE_FOR_THE_CTA",
      "payload": "USER_DEFINED_PAYLOAD",
      "referral": {
        "ref": "USER_DEFINED_REFERRAL_PARAM",
        "source": "SHORT_URL",
        "type": "OPEN_THREAD"
      }
    }
  }
}
```

Reference the following table to understand what each of the above fields is referring to:

| Property | Description |
| --- | --- |
| `postback.mid` | The ID for the message |
| `postback.payload` | Information defined in the CTA `payload` parameter. This is only included in the webhook notification sent to the app that sent the message to the person. |
| `postback.referral` | Information about the action the person took to enter a conversation.<br>The referral property information is included in the webhook notification only when a person starts a conversation using one of the following then clicking a CTA such as a Get Started button:<br>An m.me LinkA Click to Messenger AdA Messenger QR CodeA Welcome Screen |
| `postback.referral.ref` | The arbitrary data that was originally passed in the `ref` param added to the m.me link. Only alphanumeric characters as well as -, _, and = are supported |
| `postback.referral.source` | The URL for this referral. For m.me links, the value of source is `“SHORTLINK”`. For referrals from Messenger Conversation Ads, the value of source is `"ADS"` |
| `postback.referral.type` | The identifier for the referral. For referrals coming from m.me links, it will always be `"OPEN_THREAD"`. |
| `postback.title` | The title for the Call To Action (CTA) that a person clicked |
| `recipient.id` | The ID for your Facebook Page |
| `sender.user_ref` | The ID for the reference for a person who took an action, such as clicked a Get Started, or Persistent Menu item, that sent a message |
| `timestamp` | The Unix timestamp for date when the webhook notification was sent to your server |

Follow these steps to set up and enable your own webhook to start working with postback messages:

1. You will need to [setup a webhook](https://developers.facebook.com/documentation/business-messaging/messenger-platform/webhooks) to respond to the payload that we send when the button is clicked.
2. Open your app on the [developers’ app page](https://developers.facebook.com/apps/)
3. On the left-hand side select `Webhooks` .
4. Click the `Select product` dropdown and choose `Page` .
5. Fill in your webhook information and click `Verify and save` .
6. In the `Webhook fields` section, find the field `messaging_postbacks` and make sure the subscribe toggle is turned on.
7. You can send a test postback button with any payload and confirm that, on click, your webhook logs the event.
