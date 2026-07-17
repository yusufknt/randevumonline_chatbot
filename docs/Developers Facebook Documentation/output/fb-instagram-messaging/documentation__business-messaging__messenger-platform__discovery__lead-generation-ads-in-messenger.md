# Lead Generation Ads in Messenger | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/discovery/lead-generation-ads-in-messenger_

---

# Lead Generation Ads in Messenger

Updated: May 7, 2024

Apart from [Click To Messenger Ads](https://developers.facebook.com/documentation/ads-commerce/marketing-api/ad-creative/messaging-ads/click-to-messenger), there are ads that help you ask automated questions to generate leads or potential clients. These ads can be displayed on Facebook and Instagram to find customers who are interested in your business’s products or services.

- [Customer Experience](https://developers.facebook.com/documentation/business-messaging/messenger-platform/discovery/lead-generation-ads-in-messenger#userexperience)
- [Follow up on Leads using Messenger Platform](https://developers.facebook.com/documentation/business-messaging/messenger-platform/discovery/lead-generation-ads-in-messenger#follow_on_leads_with_apps)
- [Creating a Lead Generation Ad](https://developers.facebook.com/documentation/business-messaging/messenger-platform/discovery/lead-generation-ads-in-messenger#create_lead_ad)
- [Connect an App to a Lead Generation Ad](https://developers.facebook.com/documentation/business-messaging/messenger-platform/discovery/lead-generation-ads-in-messenger#connnect_an_app)
- [Using Keywords to end automated questions](https://developers.facebook.com/documentation/business-messaging/messenger-platform/discovery/lead-generation-ads-in-messenger#stop_keywords)
- [Expected App Webhooks](https://developers.facebook.com/documentation/business-messaging/messenger-platform/discovery/lead-generation-ads-in-messenger#webhooks) [Referral Webhook](https://developers.facebook.com/documentation/business-messaging/messenger-platform/discovery/lead-generation-ads-in-messenger#referral)[Summary Message](https://developers.facebook.com/documentation/business-messaging/messenger-platform/discovery/lead-generation-ads-in-messenger#summary)[Handover Protocol Events (HOP)](https://developers.facebook.com/documentation/business-messaging/messenger-platform/discovery/lead-generation-ads-in-messenger#handover)
- [FAQ](https://developers.facebook.com/documentation/business-messaging/messenger-platform/discovery/lead-generation-ads-in-messenger#faq)

## Customer Experience

When a customer clicks a lead generation ad, a Messenger conversation will be created between your business and the customer. The messages will contain a set of questions specified during ad creation. People qualified according to your questions will be marked as completed leads.

To test by injecting a demo ad into your feed:

Both complete and incomplete leads will show up on the Page Inbox tool. You can then follow up on those leads in different ways:

- For Messenger Platform Integrations. After the lead flow is completed, thread control is passed to the selected App. See [Lead Generation Ad to app handover](https://developers.facebook.com/docs/messenger-platform/handover-protocol/messenger-lead-ads-hop)
- On **Page Inbox** : Lead conversations will be available in a dedicated folder
- In **Ads Manager** leads are available for download. Leads can be downloaded as either an *xlsx* or *csv* file.

Your business will only be able to view the conversation once the potential customer does the first reply after clicking on the ad. If the customer takes no action, no webhooks notifications are sent.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/645077560_1449248576933792_5826297898565788633_n.png?_nc_cat=106&ccb=1-7&_nc_sid=e280be&_nc_ohc=wrVNtSZH6FsQ7kNvwEeehmk&_nc_oc=AdqvHVaWRWrEsv2219OelCexi2PbZ2bzw1TSChpRNaVPgfXklCy9gpOb4j7MsWdkT3c&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=kXj5vxsRd6-jc8KqTYhTWw&_nc_ss=7b20f&oh=00_Af73YbJ44zrzcs5qMJnYlPBXcj4FvnhZC1YhFkUhlE00aw&oe=6A1C4181)

## Follow up on Leads using Messenger Platform

The use case for this feature is when a Business drive leads into Messenger but wants to use an app to follow up on collected leads. For the specific use case of leads, the ad delivery model can optimize for lead completion as objective while providing handover functionality for Apps to then handle the follow up for completed leads.

Advertisers may select a specific app to receive messages from a Messenger Lead Ads campaign. More info on [Messenger Lead Ads app handover](https://developers.facebook.com/docs/messenger-platform/handover-protocol/messenger-lead-ads-hop)

## Creating a Lead Generation Ad

Create a Click To Messenger: Lead Generation Ads using Ads Manager. For more details see [instructions to create a lead generation ad that clicks to Messenger.](https://www.facebook.com/business/help/2398917563501477). Once the ad is created you can use the Message Template to define qualification questions.

### Create a Message Template

The **Message Template** defines the questions used to qualify a person as a lead. This flow defines the meaning of each answer. It will result in either, a *complete* lead or a *disqualified* lead.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/645554294_1449248546933795_4112648503318216354_n.png?_nc_cat=101&ccb=1-7&_nc_sid=e280be&_nc_ohc=QMTo1cINHqsQ7kNvwHj_ft_&_nc_oc=AdoI_DP0nYpHy4i0FOBrXy2GDl7j2Dala5wHspgp2e0R5_RkW0zZdW45_K4rlFGn31U&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=kXj5vxsRd6-jc8KqTYhTWw&_nc_ss=7b20f&oh=00_Af7kJ_IRhChqsuIQ6TT_x6YaAa5NfzO5i1npeBqV8Fpckg&oe=6A1C30F4)

### Connect an App to a Lead Generation Ad

In the **Advanced** Tab of the **Message Template** select *Connect An App*. This toggle is only available to Pages with authorized app in the Advanced Messaging page setting. Once active you can select the desired app. You can now Save and Finish and expect the target app will get thread control after the lead flow finishes.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/646666760_1449248550267128_3170328816952291131_n.png?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=NXeXGAatVAYQ7kNvwG6wJoG&_nc_oc=AdoZg9i2MXvMiCCBfQft8ExAlKd48QFWsxGUeSVgZ87DZ6p0IUY05WJ16Y6K5ksQdBU&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=kXj5vxsRd6-jc8KqTYhTWw&_nc_ss=7b20f&oh=00_Af7WPnXwPV8v8K0KKbJarP2ucjd8cceToh6D8JRfNW-8Hw&oe=6A1C2E1C)

Optional settings

***Allow connected app to interrupt:*** This checkbox setting allows the selected app to get *message webhooks* during the lead generation process as well as use Send API to interrupt the lead generation flow. Note that when an app interrupts the lead generation flow, the action is treated as a takeover. When the ad is interrupted it will be prevented from recording the complete lead signal that is used for ad delivery optimization.

***Send lead summary to connected app:*** This checkbox setting allows the selected app to get a *message webhook* with the information collected during lead submission process. This feature is meant for apps that can’t process the referal webhook that already contains this information and that is sent by default.

### Using Keywords to end automated questions

This optional advanced feature is intended for businesses that support customer care over Messenger. It can assist customers who want to stop the lead generation flow to get customer support.

Stop keywords like ‘agent’, ‘support’, ‘stop’, ‘customer care’ can be set on the ad. If the potential customer messages any of those keywords or phrases (case insensitive). The lead generation flow will be interrupted, and the thread control will be released back to the business.

If an App is connected to the Page, the stop message will be sent to the App as a message webhook. This allows the App to respond to the user’s request.

The **Confirmation message** will be triggered if a keyword to end the lead generation flow is detected. This message will not be sent to apps as a message webhook although the trigger keyword will trigger as a message webhook event.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/644836124_1449248586933791_4627948646976664098_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=Z8RHekxVMgUQ7kNvwGCQ8RT&_nc_oc=Adrt2m6pC_AFARBzmMcODYmaAcP5hYuwwG_Cq82wK5ySzNsseCqozCuoVelhTD-aD6Q&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=kXj5vxsRd6-jc8KqTYhTWw&_nc_ss=7b20f&oh=00_Af6BZDwtK9bTT3SC04KnAurQ6gOMmaIMOZZO4qsmAbdZjA&oe=6A1C1A1A)

## Expected App Webhooks

### Referral Webhook

The Lead Referral webhook is always sent to apps subscribed to [`messaging_referrals`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/webhook-events/messaging_referrals) webhook events after the Click-To-Messenger Ad ends. This event can be used as trigger to follow up messages or assign the lead to an agent for lead nurturing. The webhook contains all the lead collected information along with the type of ending; `LEAD_COMPLETE` if the person succefully finished the lead generation flow or `LEAD_INCOMPLETE` if the person did not finished the lead generation flow or selected a disqualifiying choice.

Since the standard messaging window is open when this event is triggered. Apps can use Send API to send follow ups in Messenger.

```
{
    "object": "page",
    "entry": [
        {
            "time": 1665424582475,
            "id": "542998526103632",
            "messaging": [
                {
                    "sender": {
                        "id": "5794982867201265"
                    },
                    "recipient": {
                        "id": "542998526103632"
                    },
                    "timestamp": 1665424533,
                    "referral": {
                        "source": "ADS",
                        "type": "LEAD_COMPLETE",
                        "ad_id": "6302572858686",
                        "ads_context_data": {
                            "ad_title": "Find Wholesalers Ad",
                            "post_id": "559217392549680",
                            "photo_url": "https://scontent.xx.fbcdn.net/..."
                        }
                    },
                    "lead": {
                        "data": [
                            {
                                "question": "Are you interested in becoming a reseller?",
                                "answer": "Yes"
                            },
                            {
                                "question": "What city is your store located?",
                                "answer": "Menlo Park"
                            }
                        ]
                    }
                }
            ]
        }
    ]
}
```

### Summary Message Webhook

This message is only sent for Lead Ads with the summary message enabled at the ad level (*Send lead summary to connected app* checkbox) when the lead is completed. The structure of the webhook mocks a message sent by the person to the Page and contains all info shared during the lead flow.

Note that this summary message will not appear in the thread for either the person or the Page. The goal of this message is to help apps that are not listening to the new `messaging_referrals` and get an initial message to trigger them with context to get started.

```
{
    "object": "page",
    "entry": [
        {
            "time": 1661209504608,
            "id": "542998526103632",
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
                        "text": "Lead summary:
Are you interested in becoming a reseller?: Yes
What city is your store located?: Menlo Park"
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

### Handover Protocol Events (HOP)

The change in thread control will trigger webhooks to apps subscribed to the `messaging_handover` field. More details on [Handover Protocol Webhook Event for Click To Messenger, Lead Generation Ads](https://developers.facebook.com/docs/messenger-platform/handover-protocol/messenger-lead-ads-hop)

### FAQ

How do I install a Messenger App?

Apps are installed from the app website using [Facebook Login](https://developers.facebook.com/documentation/facebook-login) and granting pages_messaging permission to a particular Page. Authorized Apps will show up in Page settings inside Advanced messaging.

I can’t see my app in the connect app drop down

Only Authorized Apps for the Page will show up. You can see Authorized apps in Page settings inside Advanced messaging.Apps are installed from the app website using [Facebook Login](https://developers.facebook.com/documentation/facebook-login) and granting pages_messaging permission to a particular Page.

Can I have more than one bot connected to a page?

Yes, more than one app can be subscribed to a page. When multiple apps handle the same conversation is best to use the [Handover Protocol](https://developers.facebook.com/docs/messenger-platform/handover-protocol) to handle which bot owns the thread at any given time.

What happens if the user sends more messages after lead submission?

After the lead submission ends Apps will get webhooks on user messages and can reply to them. If an app was selected as part of the App then only that selected app will be allowed to reply and will get webhooks on the messaging channel. The messaging window is open and the App can reply using Send API

What happens to Send API while a Lead Generation Ad is in progress?

By Default Send API and Webhooks are blocked while a Lead Generation Ad is in progress. App Id: 413038776280800 for Messenger Lead Gen App will have thread control. This behavior can be disabled using the Block Send API toggle on the Create Template dialog inside the Ad

My app is not getting the Summary message webhook

Send Summary is enabled by default only when an App is selected, in the Create Template dialog inside the Ad. Note the summary can be disabled on the ad after selected the connected App. Even when an app is not selected the Lead Gen Ad will pass thread control to the Handover primary reciver, when set, or just release thread control.
Any follow up message after the lead is submitted will be sent to subscribed Apps. Apps can query Conversation API to retrieve the message history and get the information shared during the lead generation.

What happens if the person clicks on the Ad but does not complete the lead or is disqualified?

As long as the user replies to the first question the messaging window will be open. If the anwers provided disqualify thre user or the user does not reply, then the ad experience will end and the ad will pass thread control to the target app and provide the metadata "messenger_lead_gen_incomplete" this allows business to have a fallback experience to convert non leads into customers. See [HOP webhook after Lead Ad](https://developers.facebook.com/docs/messenger-platform/handover-protocol/messenger-lead-ads-hop) for more info
