# API References | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/api-reference_

---

# API References

Updated: Apr 24, 2026

The Marketing Message API for Messenger is available exclusively to [**tech providers**](https://developers.facebook.com/docs/development/release/tech-providers) with an existing app that has successfully completed [Meta App Review](https://developers.facebook.com/docs/app-review) for the following permissions:

- ads_management
- pages_messaging
- paid_marketing_messages or marketing_messages_messenger

Currently, tech providers can only serve **businesses** located in the following regions:

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

In addition, messages can be sent to **users/subscribers** in all regions **except**:

- European Union
- Japan
- South Korea
- Australia
- United Kingdom

The Marketing Message API for Messenger is only available for Web applications.

## Overview

Below this page you will find examples of different message requests that can be made and variety of templates we offer as well as guidance for setup. The templates we currently support are:

- [Generic Template](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/api-reference/generic)
- [Button Template](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/api-reference/button)
- [Text Template](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/api-reference/text)
- [Media Template](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/api-reference/media)
- [Product Template](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/api-reference/product)
- [Receipt Template](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/api-reference/receipt)

For all templates the following request URI will be used:

```json
https://graph.facebook.com/v24.0/act_<AD_ACCOUNT_ID>/messages?access_token={PAGE_ACCESS_TOKEN}
```

## API Errors

| Code | Description |
| --- | --- |
| 2300000 | You cannot send a message unless the message campaign under which the message exists is active. |
| 2300001 | The message ID you supplied is invalid. The message with this ID either does not exist, or you do not have the permission to load it. |
| 2300002 | Messages cannot be sent if the message set under which the message exists is inactive. Please make sure your message set is activated. |
| 2300003 | The message must be in active status before it can be sent. |
| 2300004 | The subscription token you passed in could not be loaded. This could be because the token id you passed was invalid - or you may not have permissions to load it. |
| 2300005 | The page id behind your message does not match the page id on the messenger subscription token. Pages can only message their own subscribers. |
| 2300006 | Direct send messages can only be sent if the message campaign is created as a direct send campaign. Make sure you set is_direct_send = true when creating the campaign. |
| 2300007 | You need to pass in at least one of the two fields: lifetime_budget or daily_budget. |
| 2300008 | Failed to get the default bid amount for the message campaign. |
| 2300009 | The campaign metadata does not exist for the given message. |
| 2300010 | There is no valid message creative/payload for the given message sending request. |
| 2300011 | The payment method is missing for the ad account associated with the message campaign. |
| 2300012 | The message campaign is still being populated. Please try again later. |
| 2300013 | The business has not accepted the terms of service for marketing messages. |
| 2300014 | The ad account associated with the message campaign does not match the ad account associated with the request. |
| 2300015 | The budget for the message campaign has been reached. |
| 2300016 | The bid amount is too low. Please increase the bid amount. |
| 2300017 | The ad account has reached its spend limitation. |
| 2300018 | Failed to save the message attachment. Please verify the attachment is valid and try again. |
| 2300019 | The app has not accepted the terms of service for using Marketing Messages API for Messenger. Please go to the app dashboard -> Messenger -> Messenger API Settings to accept the terms of service. |
| 2300020 | The pacing type for direct send is invalid. |
| 2300021 | When media_type is ‘video’, a video_id must be provided. |
| 2300022 | When media_type is ‘image’, an image_url must be provided. |
| 2300023 | The button type is invalid. Valid button types are: web_url. |
| 2300024 | Button URL cannot be empty when provided. |
| 2300025 | Button title cannot be empty. |
| 2300026 | Too many buttons provided. Maximum of 3 buttons are allowed per message. |
| 2300027 | The attachment cannot be reused because it was created by a different page. |
| 2300030 | The ad account is not in a supported region. |
| 2300031 | The page is not in a supported region. |
| 2300032 | The subscription token is not in a supported region. |
| 2300033 | The campaign start time is in the future. Please wait until the start time has passed before sending messages. |
| 2300034 | The subscriber has stopped marketing messages subscription. |
| 2300035 | The minimum delay between messages has not been reached. Please wait until the minimum delay has passed before sending the next message. |
| 2300036 | The recipient cannot receive messages at this time. |
| 2300037 | The subscription token has expired, and can no longer be used to send a message. |
| 2300038 | Unable to resolve one or more placeholders in the message creative/payload. |
| 2300039 | Lack of the permission for the page. |
| 2300040 | This feature is not currently available. |
| 2300041 | The campaign is not ready for message delivery. Please try again later. |
| 2300042 | The recipient can’t receive any more marketing messages at this time. Please see the ‘F-Caps for Marketing Messages on Messenger’ section below for more detail. |
| 2300043 | The recipient can’t receive any more marketing messages at this time. Please see the ‘F-Caps for Marketing Messages on Messenger’ section below for more detail. |
| 2300044 | The recipient can’t receive any more marketing messages at this time. Please see the ‘F-Caps for Marketing Messages on Messenger’ section below for more detail. |
| 2300046 | Multiple image URLs are not supported in carousel format. Use single image URLs for each carousel element instead. |
| 2300047 | Message param cannot contain both multiple images and single image parameters. Please use only one image format. |
| 2300048 | Only one hero image is allowed in the message param. Please mark only one image as the hero image. |
| 2300052 | This person is not available right now. |
| 2300053 | This campaign has reached its lifetime budget, so your message couldn’t be sent. Increase the lifetime budget or create a new campaign to continue. |
| 2300054 | This campaign has reached its daily budget, so your message couldn’t be sent today. It will resume tomorrow, or you can increase the daily budget to send more messages per day. |
| 2300055 | Your message couldn’t be sent right now. Come back and try again in about 30 minutes. |
| 2300056 | Your account has reached its total spending limit, so your message couldn’t be sent. Increase or reset your spending limit in payment settings (and add funds if you use prepaid). |
| 2300057 | Your message couldn’t be sent right now. Try again later. |
| 2300058 | Your prepaid balance has run out, so your message couldn’t be sent. Add funds to your account to continue. |
| 2300059 | Your business stored balance is too low to send messages right now. Add funds to your stored balance and try again. |
| 2300060 | Your message couldn’t be sent right now. Try again later. |
| 2300061 | Your message couldn’t be sent right now. Come back and try again in about 30 minutes. |
| 2300062 | Your message couldn’t be sent right now. Try again in about 30 minutes. |
| 2300063 | We’re unable to process your request at this time. Come back and try again later. |
| 2300064 | The message creative is already in use by another campaign. |
| 2300065 | The page ID is required but was not provided in the request. |
| 2300066 | The page has not signed the Marketing Messages on Messenger Terms of Service. Please complete the onboarding process for the page and try again. |
| 2300067 | The ad account has not signed the Marketing Messages on Messenger Terms of Service. Please complete the onboarding process for the ad account and try again. |
| 2300068 | We’re unable to process your request at this time. Come back and try again later. |
| 2300069 | The required Terms of Service have not been signed. Please complete the onboarding process and try again. |
| 2300070 | The targeting options provided are invalid. |
| 2300071 | The message creative contains invalid aliases. |
| 2300072 | The message creative contains an invalid offer. |
| 2300073 | The message creative contains too many line breaks. |
| 2300074 | The message creative is missing a required call-to-action (CTA) button. |
| 2300075 | The button order in the message creative is invalid. |
| 2300076 | A required field is missing from the request. |
| 2300077 | The URL field provided is invalid. |
| 2300078 | The rate limit for sending messages has been exceeded. Please wait and try again. |
| 2300079 | The rate limit for creating campaigns has been exceeded. Please wait and try again. |
| 2300080 | The rate limit for querying subscriber tokens has been exceeded. Please wait and try again. |

## F-Caps for Marketing Messages on Messenger

### What is it?

Frequency caps (F-caps) are automated limits that help ensure people don’t receive too many marketing messages in a given period of time. The limits can apply both:

- Across all businesses (overall marketing message load), and
- From the same business (repeat messaging over time)
F-caps are based on signals like overall messaging activity and recent engagement with marketing messages. No action is required from your business. These limits are applied automatically. Why is it important? F-caps are designed to maintain a healthy messaging ecosystem by:
- Helping people have a more balanced, valuable messaging experience, and
- Helping marketing messages reach people who are more likely to be receptive and engage, improving overall campaign efficiency. How it applies to your business You may see that some marketing messages are not delivered to certain recipients at certain times due to these automated limits. This is expected behavior and does not require any setup or configuration.To maximize performance, focus on sending messages that are expected, timely, and relevant for your audience.
