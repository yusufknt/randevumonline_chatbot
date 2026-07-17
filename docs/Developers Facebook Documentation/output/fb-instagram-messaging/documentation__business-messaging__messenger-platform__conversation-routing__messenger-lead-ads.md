# Messenger Lead Generation Ads | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/conversation-routing/messenger-lead-ads_

---

# Messenger Lead Generation Ads

Updated: May 5, 2026

Advertisers can select a specific app to receive messages from a Messenger Lead Ads campaign. For more information, see [Messenger Lead Ads](https://www.facebook.com/business/help/734075733714274?id=371525583593535). To test a Lead Generation Ad, you can use [this sample ad](https://www.facebook.com/ads/experience/confirmation/?experience_id=2170497373124589) injected into your feed.

This feature is for businesses that drive leads into Messenger and want to use an app to follow up on collected leads. The ad delivery model can optimize for lead completion as its objective while providing conversation routing functionality for apps to handle follow-up for completed leads.

When a person clicks on a Messenger Lead Ad, the Messenger Leadgen app (App ID: `413038776280800`) takes thread control and prompts the person with the questions defined in the ad. The person either completes or does not complete the automated flow. After the flow ends, thread control is passed to your app (if defined) or released (when no app is defined).

While a lead generation ad is ongoing, webhooks are not sent to apps by default. After the flow ends, your app can get a summary message of what happened or retrieve the history of messages using the [Conversations API](https://developers.facebook.com/docs/graph-api/reference/page/conversations).

The Page Inbox can always be used to control the thread and reply.

## Prerequisites

Before you start, make sure you have:

- A [Facebook App](https://developers.facebook.com/documentation/business-messaging/messenger-platform/get-started) configured for Messenger Platform
- The `pages_messaging` and `pages_manage_metadata` [permissions](https://developers.facebook.com/docs/pages/overview/permissions-features#permission-dependencies)
- Your app subscribed to the `messages` and `messaging_handovers` [webhook fields](https://developers.facebook.com/documentation/business-messaging/messenger-platform/webhooks#subscribe-to-meta-webhooks)
- Your app authorized in the Page’s **Advanced Messaging** settings
- The [Conversation Routing](https://developers.facebook.com/documentation/business-messaging/messenger-platform/conversation-routing) protocol enabled for your Page

## Creating an ad with an app

For this example shows the creation of a Messenger Lead Ad using [Ads Manager](https://www.facebook.com/business/help/2398917563501477). For these types of ads you can define the content that will be used to qualify the lead and the target app that will take over to follow up on leads.

### Create a Message Template

The Message Template defines the questions used to qualify the lead. This flow defines when the answer means that this is a complete or disqualified lead.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/653405008_1459945502530766_5733593155693782844_n.png?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=UnpkABA4uK0Q7kNvwFi4qAJ&_nc_oc=AdpLm7ckSO_ADnmU64ayhY_imrg6xvFKuo-OGaUCuoriobCBxxLpk7WlrQMeIbvD5Zk&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=AMfbbVw2IXzfzgQhciJtig&_nc_ss=7b20f&oh=00_Af6HU__TmRVHwvx9GQAQrdy7sCFHFiswxOT3kTzecDDuiQ&oe=6A1C2154)

### Connect an App

In the **Advanced** tab of the Message Template, select **Connect An App**. This toggle is only available to Pages with an authorized app in the **Advanced Messaging** Page setting. Once active, you can select the desired app. Save and finish — your target app will get thread control after the lead flow finishes.

Note that you can also select to send a summary message. This setting allows the app to get a message webhook with the content of the information collected during lead submission.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/652320111_1459945605864089_6304170515393647571_n.png?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=9c9teNLxXksQ7kNvwE4pXTX&_nc_oc=AdqC2L6Su4eRUUvc_zpVMct-o7Y1cobXz6j2r89zLxQ-tUOdulXR0IZJMFF-Jv-vgMo&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=AMfbbVw2IXzfzgQhciJtig&_nc_ss=7b20f&oh=00_Af48Eqh5ZFD8TpBs68xVl-5_Lv_lsIwd5sWu4GdpYBD4LQ&oe=6A1C3C73)

### Setup Thread Control Window

When the conversation starts from the ad, the app will have control of the thread for 1 day (24 hours) from the last user message. Businesses with longer leads / sales cycles can extend thread control for up to 7 days by setting receiving_app_control_expiration from 1 to 7. Any invalid values for receiving_app_control_expiration would lead to the thread control window set to 1 day. Additionally, any [Conversation Routing](https://developers.facebook.com/documentation/business-messaging/messenger-platform/conversation-routing) actions would also reset the thread control window to 1 day.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/653700866_1459945552530761_2051432269066693757_n.png?_nc_cat=102&ccb=1-7&_nc_sid=e280be&_nc_ohc=-fPW0845dpkQ7kNvwHt2tz6&_nc_oc=Adr4wGOSW1fIm-7eItj2Ng_qJp__7t9_Oc_J46_L_feGBZdj9f-keb7OgWLZgUwpVwE&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=AMfbbVw2IXzfzgQhciJtig&_nc_ss=7b20f&oh=00_Af4ASwDZHJeJFbvJB1_ff_A4cVMwUkbvLd-OGyL7uNXh9Q&oe=6A1C2C76)
Here’s a sample JSON template from the above image which defines the `receiving_app_control_expiration`.

```json
{
    "message": {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "button",
                "text": "Hi! Please let us know how we can help you",
                "buttons": [
                    {
                        "title": "Show me the product!",
                        "type": "web_url",
                        "url": "http://www.facebook.com/"
                    },
                    {
                        "title": "Tell me more",
                        "type": "postback",
                        "payload": "USER_DEFINED_PAYLOAD"
                    }
                ]
            }
        },
        "receiving_app_id": 1278416343931139,
        "receiving_app_control_expiration": 4
    }
}
```

## Expected Webhooks

On every lead submission you can use the target app to get thread control. Once that thread control is passed the standard messaging window will be open to allow for follow ups using Send API.

### Summary Message

This message is only sent for Lead Ads with summary message enabled and the lead is completed. The structure of the webhook mocks a message sent by the person to the Page and contains all info shared during the lead flow.

Note that this summary message will not appear in the thread for either the person or the Page. The goal of this message is to help apps that are not listening to `messaging_handovers` get an initial message to trigger them with context to get started.

```json
{
    "object": "page",
    "entry": [
        {
            "time": 1661209504608,
            "id": "104508901353867",
            "messaging": [
                {
                    "sender": {
                        "id": "5794982867201265"
                    },
                    "recipient": {
                        "id": "542998526103632"
                    },
                    "timestamp": 1661209328,
                    "message": {
                        "mid": "m_2OF0H5fb2HNRyjM0rt2FVBAaDQp_p5DQlffdEXNVyOrraxQCt0tFwWXwq3QctcvbpjSX1rSY8BX9Y2IXwPirWA",
                        "text": "Lead summary:\nAre you interested in becoming a reseller?: Yes\nWhat city is your store located?: Menlo Park"
                    },
                    "hop_context": {
                        "app_id": 498721317747541,
                        "metadata": "messenger_lead_gen_complete"
                    }
                }
            ]
        }
    ]
}
```

### For apps subscribed to Conversation Routing events

The change in thread control triggers webhooks to apps subscribed to the `messaging_handovers` field. In the following example, the ad is configured to pass thread control to app `2262510160704936`. On completion, thread control passes from the Leadgen app (`413038776280800`) to the target app, and the metadata reads `messenger_lead_gen_complete`.

If the lead flow is dropped or the person is disqualified, the metadata shows `messenger_lead_gen_incomplete` instead. This allows your app to have a fallback experience for non-leads.

Note that this webhook triggers on thread control changes, so it arrives before the summary message webhook when enabled. You can use this to either ignore or expect the summary webhook.

```json
{
    "object": "page",
    "entry": [
        {
            "id": "104508901353867",
            "time": 1662056205364,
            "messaging": [
                {
                    "recipient": {
                        "id": "542998526103632"
                    },
                    "timestamp": 1662056205364,
                    "sender": {
                        "id": "5794982867201265"
                    },
                    "pass_thread_control": {
                        "previous_owner_app_id": 413038776280800,
                        "new_owner_app_id": 2262510160704936,
                        "metadata": "messenger_lead_gen_complete"
                    }
                }
            ],
            "hop_context": [
                {
                    "app_id": 2262510160704936,
                    "metadata": "messenger_lead_gen_complete"
                }
            ]
        }
    ]
}
```

## Sending follow-up messages

After your app receives thread control, you can send follow-up messages to the lead using the [Send API](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/send-api). The standard 24-hour messaging window applies from the time of the person’s last message.

To send a follow-up message, make a `POST` request to the `/<PAGE_ID>/messages` endpoint using the PSID from the webhook event:

```curl
curl -X POST "https://graph.facebook.com/<API_VERSION>/<PAGE_ID>/messages" \
    -d "recipient={'id':'<PSID>'}" \
    -d "messaging_type=RESPONSE" \
    -d "message={'text':'Thanks for your interest! A team member will follow up shortly.'}" \
    -d "access_token=<PAGE_ACCESS_TOKEN>"
```

## Retrieving lead data

To retrieve the history of messages from a lead conversation, use the [Conversations API](https://developers.facebook.com/docs/graph-api/reference/page/conversations). Send a `GET` request to get the conversation and its messages:

```curl
curl -i -X GET "https://graph.facebook.com/<API_VERSION>/<PAGE_ID>/conversations?fields=participants,messages{message,created_time}&access_token=<PAGE_ACCESS_TOKEN>"
```

This returns the full conversation thread, including the lead qualification questions and answers exchanged during the automated flow.
