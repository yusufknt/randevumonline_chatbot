# FAQs for the Marketing Message API for Messenger | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/faq_

---

# FAQs for the Marketing Message API for Messenger

Updated: Mar 31, 2026

The following is a list of the frequently asked questions about the Marketing Message API for Messenger from Meta.

## Availability

**Question: What is availability for Marketing Message API for Messenger?**

**Answer:** The Marketing Message API for Messenger was launched to all tech providers on July 1, 2025. Businesses served by tech providers can only serve businesses in the following locations:

- Australia
- Brazil
- Chile
- Colombia
- Hong Kong

- India
- Indonesia
- Israel
- Malaysia
- Mexico

- New Zealand
- Peru
- Philippines
- Saudi Arabia
- Singapore

- Taiwan
- Thailand
- United Arab Emirates
- United States
- Vietnam (VN)

**Question: What is the availability for Messenger Recurring Notifications?**

**Answer:** Recurring Notifications will be deprecated on January 12, 2026.

Starting September 1, 2025, apps will no longer be able to integrate Recurring Notifications.

For existing partners and clients using Recurring Notifications, we will limit the frequency of sends from 1 per day (rolling 24-hour window) to 1 per 48 hours. This means a Page will only be able to send 1 Recurring Notification to each subscriber every rolling 48 hour window.

On February 10th, 2026, Recurring Notifications on the Messenger API will be discontinued for partners and businesses globally, except for the AU, EU, JP, KR, and UK geos. Starting on this date, the Messenger API will start returning errors if Recurring Notifications are trying to be sent, with the exception of within the 5 geos previously mentioned.

We urge all partners and clients to migrate to marketing messages before the end of 2025.

**Question: Are marketing messages on Messenger available on Ads Manager?**

**Answer:** There is no launch date to share for marketing messages on Ads Manager.

## POSITIONING

**Question: What are Messenger marketing messages?**

**Answer:** Marketing messages are a paid messaging solution that allows businesses to initiate Messenger chats to re-engage and retain interested customers as a way to boost engagement and drive sales.

**Question: How are marketing messages different from Recurring Notifications?**

**Answer:** Marketing messages in the Marketing API are an enhancement of Recurring Notifications. It supports all of the functionality of Recurring Notifications, plus new value-added features.

Freeform messages: Existing content from Recurring Notifications will carry over to marketing messages.

Existing subscribers: Existing subscribers (tokens) will carry over to marketing messages.

Direct send: As with Recurring Notifications, businesses using Marketing Message API for Messenger control the individual users (via tokens) who receive a message.

Outside 24 hour window: Marketing messages can also be sent outside of the 24-hour window and can trigger a new 24-hour window when users respond.

New value-added features:

Opt-ins: Easier opt-ins are available via subscribers from custom audience uploads and Ads that Click to Messenger.

Insights: More insights are available through new metrics like cost per delivered message, and cost per message link click.

Campaigns: Campaign send now has broadcasting capabilities to send the same message to all subscribers without controlling the exact individuals who receive messages.

**Question: What will happen to Recurring Notifications?**

**Answer:** Recurring Notifications will be deprecated on February 10, 2026.

Marketing Message API for Messenger will be the only re-engagement messaging solution available. We recommend that partners transition to marketing messages now. Key benefits:

Technical support: Meta’s product and engineering teams will provide direct support during onboarding and testing.

Incentives: Product development fund for partners and ad credits for end businesses.

Business migration: Help end businesses migrate now so there is no gap when Recurring Notifications is deprecated.

Feature development: Feedback now has an outsized impact on final pricing, feature specs, and prioritization.

To accurately test the future state, where marketing messages is the only re-engagement solution, we will disable Recurring Notifications for participating businesses during testing. Disabling will only happen after we have confirmed that the marketing messaging has been successfully integrated and clients have been onboarded to marketing messages.

**Question: How are marketing messages different from Ads that Click to Messenger or Live Video Ads?**

**Answer:** Ads provide a full funnel solution to find, convert, and re-engage users. Ads can also be used to get subscribers to marketing messages. Marketing messages can be used to retain users via messages that remain in the chat.

**Question: How are marketing messages different from Sponsored Messages?**

**Answer:** Sponsored Messages, deprecated on July 31, 2024, was an ephemeral ad format that appeared in inbox. Marketing messages is a persistent paid message sent outside the 24 hour window that appears within the chat thread.

**Question: What can businesses send using marketing messages?**

**Answer:** The marketing messages format is customizable and flexible, making it suitable for various industries and use cases, such as entertainment, e-commerce, retail, travel, and more.

**Question: Are Messenger Utility Templates related to marketing messages?**

**Answer:** Utility template messages (approved by Meta) on the Messenger API are for businesses to send timely, transactional updates to users, such as appointment updates and event reminders, and are not allowed to contain marketing content.

While Utility templates are meant to replace three of Messenger’s Message Tags, `account_update`, `confirmed_event_update`, and `post_purchase_update`, these tags will be deprecated on January 12, 2026.

## PRODUCT AND INTEGRATION BASICS

**Question: How do marketing messages work?**

**Answer:** First, businesses must get subscribers to their marketing messages. Then, they can use their Meta Business Partner’s platform to set up, edit, and send marketing messages to their subscribers. Metrics for marketing messages can be viewed on their partner’s platform or in Ads Manager.

**Question: How do businesses get marketing messages subscribers?**

**Answer:** Ways to get subscribers:

Ads that Click to Messenger – Any user that clicks and responds to these ads are immediately subscribed to marketing messages from the business’ Facebook Page.

Upload a CRM List – Upload a list of users with a phone number and/or email; any user from the list who are matched with existing Facebook profiles will be immediately subscribed to marketing messages from the Page.

Send Opt-in messages – Send marketing message opt-in templates from the Meta Business Partner’s platform or in Messenger chat.

**Question: What are the options for marketing message integration for Meta Business Partners?**

**Answer:** We offer 2 send styles for marketing messages. Partners can integrate with any of these styles:

1. Campaign send is good for businesses that want to use a campaign structure to target a subscriber pool with the same broadcast message, and do not need control over the exact individuals within the pool that get delivery. Details:
Campaign structure (campaign, message set, message) is required
Message content must be the same for all recipients (for example. broadcast)
Businesses control targeting at subscriber pool level and cannot control exact individuals getting delivery (This is an important point because in the future we might introduce performance optimizations such as link clicks and conversions - so Meta would optimize delivery to those in the pool likely to click as an example.)
Measurement is aggregated at campaign, message set, and message level - like ads
Available in Ads Manager and Marketing API
2. Direct send is good for businesses that want to send unique message content, customized at the user level via freeform content, and control the exact individuals that get delivery (delivery/read receipts) because this message might be integrated with their chatbot flows. Details:
Message content can either be the same for everyone (for example. broadcast) or freeform per user via user level message customization
Businesses control the exact individuals who will get the message and when
Measurement is aggregated at campaign, message set, and message level - like ads, and also available at user level via delivery and read receipts from webhooks
Available only in Marketing API via a full API endpoint spec or a simplified endpoint spec that streamlines the integration process

**Question: Are there any limits on the number of marketing messages campaigns that a Page can have?**

**Answer:** No

**Question: Are performance optimizations available for delivery?**

**Answer:** Currently, there is no performance optimization. For campaign and direct send styles, in Ads Manager and Marketing API, we will maximize immediate delivery to try to reach everyone in the subscriber pool/specified individuals based on the bid (if relevant) and budget. We understand this means in reality today there is not much delivery recipient difference between campaign and direct send.

**Question: What are the differences between marketing messages in Ads Manager vs. Marketing API?**

**Answer:** Marketing messages in Ads Manager offer a simplified solution, while the API offers more customization and flexibility.
Marketing messages in Ads Manager is only campaign send and supports getting subscribers automatically from CRM upload and Ads that Click to Messenger.
Marketing Message API for Messenger offers both campaign send and direct send styles and supports getting subscribers from all 3 ways.

**Question: How do partners integrate with Marketing Message API for Messenger?**

**Answer:** Partners must first meet technical prerequisites for integrating with Marketing Message API for Messenger:
Have a Meta developer account, a business account, a Facebook Page for your business, and an ad account with a payment method set up.
Have an established “Business” type developer app. Your app must have the Messenger product configured with the Facebook Page you intend to use and “Advanced” access for the required permissions.
Create a Facebook Login for Business (FBL4B) configuration. You need to generate a system user access token in the Graph API Explorer simulating the Facebook Login For Business (FBL4B) flow.
Have a handler for Messenger webhook notifications set up in your application code.

Then, partners can integrate with marketing messages on Marketing API and our developer documentation is found here.

**Question: Are there best practices for how partners should build their UX/UI to support marketing messages?**

**Answer:** We recommend that partners build UX/UI on their platform for uploading and managing subscribers, creating marketing messages, and viewing reporting. We have design best practices here.

**Question: How many marketing messages can each subscriber receive?**

**Answer:** An individual Page can send up to one marketing message to a unique user per day.

**Question: How does pricing work for marketing messages?**

**Answer:** Marketing messages have a simple, stable pricing model where businesses only pay per message for messages that are delivered to the user’s device.

To help businesses estimate their budget, in Ads Manager, we show a suggested bid and estimated delivery volume based on your budget. In Marketing API, we offer the capability to estimate delivery volume based on the budget. The bid component is optional in Marketing Message API for Messenger.

Businesses are billed directly by Meta and marketing messages spent are broken out on the same bill as Meta ads. Bills can be found in Business Manager.

**Question: What is the difference between daily vs. lifetime budget?**

**Answer:** Since marketing messages are paid, businesses need to set up a daily budget or a lifetime budget for running marketing messages. With a daily budget, an end date for the schedule is not necessary. A daily budget caps the daily spend to the amount that is set. Once you hit the daily budget, no more marketing messages will be sent. A lifetime budget requires an end date for the schedule. The lifetime budget caps the marketing messages spend for that period of time. Once the lifetime budget is reached, no more marketing messages will be sent within that time period.

**Question: How does the schedule and budget work together to send marketing messages to subscribers?**

**Answer:** For example, a Page has a total of 1,000 subscribers (500 from opt-in template, 200 from a first custom audience upload, and 300 from a second custom audience upload). A marketing message campaign (direct send) is set up with a lifetime budget of $100 and schedule of 5 days. Assume sending each marketing message costs $1. On day 1, the Page uses the partner’s audience management UI for marketing messages to send to 20 subscribers they select. This means they spent $20. On day 2, the Page doesn’t send any messages. On day 3, they select another 50 subscribers to send to and they spend $50. So far their total spend is $70 across 3 days. On day 4, they select another 50 subscribers to send to, but only 30 were successfully sent, so they spent only because the lifetime budget cap was reached at 30 subscribers (). On day 5, they do not send any messages. On day 6, they try to send to 20 subscribers, but the campaign fails because the schedule has been completed after 5 days.

**Question: How can partners and businesses estimate the cost of a marketing messages campaign?**

**Answer:** Partners first need to integrate with our Estimation API so that businesses can get a sense of the pricing. Businesses would need to input either a daily or lifetime budget and the API would return an estimated volume of messages delivered. Adjust the budget input to see how delivery volume might change. This will help estimate delivery volume for a given daily or lifetime budget.

**Question: What measurement is available for marketing messages?**

**Answer:** We currently have the following metrics in development for alpha and are also available in view-only mode in Ads Manager:
Marketing_messages_delivered: number of messages your business sent to users that were delivered.
Marketing_messages_link_btn_click: number of clicks or taps within the marketing message that led to advertiser-specified destinations, on or off Meta technologies
Marketing_messages_spend: total amount of money you’ve spent on your campaign, set or message during its schedule
Marketing_messages_read_rate: number of messages read divided by the number of messages delivered
Marketing_messages_link_btn_click_rate: percentage of delivered messages that received a link click out of the total number of messages delivered
Marketing_messages_cost_per_link_btn_click: average cost for each message link click
Marketing_messages_cost_per_delivered: average cost per message delivered

Direct send also provides delivery and read receipts via webhooks.

**Question: What controls are in place to ensure a good customer experience?**

**Answer:** Customers can opt-out at any time by clicking on a link in-thread that comes with every marketing message. The opt-out copy is set by Meta and cannot be changed by businesses. Opting out is only opting out of marketing messages sent by the Page. Users can receive other messages sent by the Page. Users also have the standard Messenger mute, block, and report options.

**Question: How does marketing messages impact the Standard Messaging window?**

**Answer:** Marketing messages are delivered anytime and not restricted to the 24 hour window. If a customer replies to a marketing message it opens the window where businesses have up to 24 hours to respond to that customer. Businesses are not charged for their replies within the 24 hour window.

**Question: What integrity policies are Marketing Message API for Messenger subject to?**

**Answer:** Marketing messages are subject to Messenger integrity policies, which are enforced on a Page level and will affect all messages, including marketing messages, sent by the Page if there is an integrity strike.

## TROUBLESHOOTING PARTNER INTEGRATION AND BUSINESS ONBOARDING

### PAYMENT

**Question: What should businesses do if they encounter issues related to their payment method during set-up?**

**Answer:** A valid payment, typically in the form of a credit card, is required to set up an ad account before sending marketing messages. If there are issues related to the payment setup, please refer to the troubleshooting guidelines provided.

**Question: What happens if advertisers do not have enough payment for marketing messages? Will an error be communicated to the developer partner?**

**Answer:** Partners will see the error code/message when calling the send message API `/act_<AD_ACCOUNT_ID>/messages`.

### ONBOARDING and CAMPAIGN SENDING

**Question: During the Facebook Login set up process, what should businesses do if their Page or Ad Account does not show up in the assets dropdown?**

**Answer:** If this happens during the asset selection step of set-up (image below), please check these possible reasons:
Incorrect Business Portfolio selected: please check that you are selecting the correct Business Portfolio that both the Page and Ad Account are under
Incompatible “Agency” use case: To set up the Page and Ad Account, you must be the Business Admin of the owning Business Portfolio that these assets belong to. For example, if the Page was “shared” with you to manage but you are not the Business Admin of the Page’s owning Business Portfolio, you will be unable to complete the set up for the Page. Please ensure Business Admin for the Business Portfolio, Page and Ad Account completes the set up.

**Question: Some campaigns are active but don’t send and display an error message saying “The message must be in active status before it can be sent”. What should I do?**

**Answer:** After creating a campaign, please wait for at least 60 minutes to allow the campaign to populate correctly before sending.

**Question: Will webhooks be sent out when the campaign is fully populated, or how can partners check that the campaign has been fully populated and is ready for sending messages?**

**Answer:** For now, a 10-minute waiting time is needed after the campaign has been set to active status before the message can be sent. There will be an exception code or message from the message send API if the 10-minute waiting time has not been passed. We will explore the possibility of developing a webhook that sends a notification when the campaign is fully populated.

**Question: What happens if users reply to a marketing message?**

**Answer:** When users reply to a marketing message, it will be as if they are messaging the page. As such, any general automations or chatbot capabilities that have been set up for the page will take over. Businesses can also manually respond to the message.

**Question: How does message failure work when the 12 hours and 90 day limits are reached? Does the API specify which users cannot be messaged?**

**Answer:** Yes the send message API `/act_<AD_ACCOUNT_ID>/messages` will respond with an error if the limitations are reached.

**Question: What does the topic_title field in the payload mean?**

**Answer:** The topic title is a default area and does not have a particular meaning.

### OPT-IN and OPT-OUT

**Question: If partners have PSID, can the PSID be uploaded in the custom audience upload?**

**Answer:** No, PSID cannot be uploaded as part of the CRM list upload. The upload only supports email and phone number; at least one is required to match users in the list to Facebook profiles. If you want to use the PSID to get subscribers, you can send the opt-in template to them to ask for an explicit opt-in in chat.

**Question: Will every interaction between the same user and the same Page will have a different PSID?**

**Answer:** We do not rely on PSID for marketing message interactions between a user and page. The same user with the same page would only have one unique subscriber token. One subscriber cannot have more than one subscriber token.

**Question: How long do subscription tokens last?**

**Answer:** Subscription tokens do not expire unless a subscriber opts out.

**Question: How can businesses get details on who the subscribers are?**

**Answer:** For privacy reasons, we do not share comprehensive profile data on the subscribers. If you have PSID, you may be able to use it to get basic information we share about your subscriber.

**Question: What can users do if they want to stop marketing messages?**

**Answer:** Every marketing message gets sent with a link for users to opt out of receiving future marketing messages. Users may continue to receive other messages from the page. Users can also use that link to block or report the page.

**Question: If users opt-out, are they able to opt back in?**

**Answer:** Yes, they are able to opt back in again through the various opt-in options we offer. For example, if a client runs ads that click to Messenger, the user can click on it to opt in again. If they are sent an opt-in message in-thread, they can opt-in again through that template.

**Question: Will client pages get impacted if users opt-out frequently?**

**Answer:** Page operations and access to the platform are not typically impacted based on opt-out rates. Pages should be mindful to adhere to Messenger platform integrity policies.

**Question: Are webhooks sent for opt-outs - when subscribers revoke their consent?**

**Answer:** We currently do not send opt-out webhooks. This is something we can explore for future updates to the product.
