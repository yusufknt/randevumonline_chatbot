# Marketing Message API for Messenger Changelog | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/changelog_

---

# Marketing Message API for Messenger Changelog

Updated: May 6, 2026

## May 6, 2026

Partner Billing Onboarding Flow Launched

- Launched a new [Partner Billing Flow (Flow 3)](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/onboard-businesses#flow-3-partner-billing-flow-suat) for the Marketing Message API for Messenger, allowing partners to bill marketing message sends to their own ad account instead of the client’s.
- The flow uses the same SUAT and `paid_marketing_messages` permission as Flow 1 (Business Portfolio Flow). After the client completes login, the partner connects their own ad account to the client’s Business Integration System User (BISU) by calling the new `POST https://api.facebook.com/system_accounts/<BISU_ID>/asset-connections` endpoint.
- Requires the `business_management` permission in addition to the standard MAPI-D permissions; complete App Review for `business_management` before serving clients with this flow.
- See the [updated onboarding documentation](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/onboard-businesses#flow-3-partner-billing-flow-suat) for full setup instructions, including the asset-connections endpoint call pattern (host, version, body format).

## May 5, 2026

[`POST /act_<AD_ACCOUNT_ID>/messages`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/send-messages)

marketing_message_delivery_failed

Webhook Coverage Improvement

- Improved `marketing_message_delivery_failed` webhook coverage to cover the majority of errors during the async message sending phase.

New Pacing Info Unavailable Error Code

- New error code 2300028 is returned when campaign pacing information is not yet ready at send time.
- Verify that the ad account and payment method are in good status. Applications should retry after 1 hour when receiving this error.

default_action

URL Fix for Generic Template

- Card and image taps in Generic Template messages now correctly open the `default_action` URL per the API specification, instead of the first button URL.
- Fixed a bug where `default_action` incorrectly required a title field.

Video Rendering Fix for Remote URL API

- Videos uploaded via the Remote URL API now render correctly in Messenger, resolving cases where videos failed to display.

1-Hour Warm-Up Enforced for All Advertisers

- All advertisers now observe the standard 1-hour warm-up period before sending marketing messages after campaign creation. Previously, some advertisers were exempt from this warm-up requirement.

[`DELETE /act_<AD_ACCOUNT_ID>/customaudiences`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/grow-marketing-messages-audience#custom-audience-api)

Custom Audiences API REMOVE_USER Now Preserves Opt-In Status

- When you send a DELETE/REMOVE_USER request for a Custom Audiences API subscriber, the user is now removed from the custom audience while their overall marketing message opt-in remains intact.
- Previously, REMOVE_USER triggered a full opt-out from all marketing messages.

## May 1, 2026

Estimation API

- Enhanced estimates calculation to consider per recipient country pricing, billing constraints etc., producing more accurate delivery and cost estimates. More details: [estimates API](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/send-messages#delivery-estimation)

## April 24, 2026

[`Error Code`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/api-reference)

- Improved Error Codes for Message Sending Failures, added more explanation for the F-cap error

## April 10, 2026

[`POST /act_<AD_ACCOUNT_ID>/messages`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/send-messages)

Frequency Capping Now Enforced on All Marketing Messages

- Marketing message frequency caps are now enabled and enforcing on all sends. Three independent rules are applied: Weekly cap: A message is blocked if the user’s marketing-message-to-organic-threads ratio exceeds 20% over the trailing 7 days (unless the user received zero marketing messages that week).Daily cap: A message is blocked if the user’s marketing-message-to-organic-threads ratio exceeds 40% over the trailing 1 day (unless the user received zero marketing messages that day).Minimum organic threads: A message is blocked if the user has not had a minimum number of organic conversation threads between consecutive marketing messages (unless the user’s last organic activity was more than 7 days ago).
- Messages that exceed frequency caps will be blocked and the API will return one of the following error codes: WEEKLY_MM_LOAD_CAP_REACHED — the weekly cap was exceeded.DAILY_MM_LOAD_CAP_REACHED — the daily cap was exceeded.MIN_ORGANIC_THREAD_NOT_REACHED — the minimum organic threads requirement was not met.
- Applications should handle these error codes and avoid immediately retrying the same recipient, as the cap will remain in effect until the user’s organic messaging activity changes.

Daily-Budget Campaign End-Time Bug Fix

- Fixed a bug where daily-budget campaigns were bypassing campaign end-time enforcement, causing messages to be sent after their campaign end times.
- Daily-budget campaigns now correctly stop sending when their end time is reached.

Creative Validation Fix

- Fixed a bug where campaigns without a valid message payload were incorrectly passing the creative validation check.
- Campaigns without a valid message payload are now correctly rejected at send time.

[`POST /act_<AD_ACCOUNT_ID>/message_campaign`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/send-messages)

Daily-Budget Campaigns No Longer Have Artificial End Time

- Daily-budget campaigns are no longer assigned an automatic 30-day end time at creation.
- Daily-budget campaigns now run indefinitely until manually paused or stopped, matching standard Ads behavior.

Webhooks Now Fire for Newly Created Active Campaigns

- Fixed a bug where message campaign and message campaign group webhooks were not firing for campaigns created with an active run status.
- Webhooks now correctly trigger on both creation and update of active campaigns.

Webhook Payload Ad Account ID Fix

- Fixed a bug where the AD_ACCOUNT webhook payload was emitting the wrong ad account ID.
- The webhook now correctly returns the legacy/payment ad account ID, consistent with other API responses.

## April 8, 2026

[`POST /act_<AD_ACCOUNT_ID>/message_campaign`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/send-messages)

[`POST /act_<AD_ACCOUNT_ID>/campaigns`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/send-messages)

[`POST /act_<AD_ACCOUNT_ID>/adsets`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/send-messages)

[`POST /act_<AD_ACCOUNT_ID>/ads`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/send-messages)

Improved Error Codes for Campaign Creation

- Fixed a bug where specific error codes for campaign creation deny rules (creative-reused, TOS-not-signed) were not being returned correctly, causing callers to receive generic errors.
- New API error codes 2300064–2300067 now correctly surface to partners.

## March 31, 2026

[`POST /act_<AD_ACCOUNT_ID>/messages`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/send-messages)

Delivery Failed Webhook Coverage Improvement

- Improved the `marketing_message_delivery_failed` webhook coverage to report all message drops during the async message sending stage.

Pacing Errors Now Surfaced With Specific Error Codes

- The following error codes are now returned when a message send is rejected due to limits: 2300069: Campaign lifetime budget reached.2300070: Campaign daily budget reached.2300071: Pacing limit reached.2300072: Account spend cap reached.2300073: Account daily spending limit reached.2300074: Prepay balance depleted.2300075: Business stored balance depleted.2300076: Daily spending limit reached.2300077: Flex billing limit reached.2300078: Brand extended credit limit reached.2300079: Daily spending limit reached.2300068: Default fallback for other pacing limits not applicable to Marketing Messages.
- These replace previously generic error responses, enabling partners to programmatically determine the exact reason for rejections and take appropriate action (e.g., pause campaigns, increase budgets, or wait for daily limits to reset).

## March 26, 2026

[`POST /act_<AD_ACCOUNT_ID>/message_campaign`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/send-messages)

[`POST /act_<AD_ACCOUNT_ID>/campaigns`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/send-messages)

[`POST /act_<AD_ACCOUNT_ID>/adsets`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/send-messages)

[`POST /act_<AD_ACCOUNT_ID>/ads`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/send-messages)

Region Deny Rule for Campaign Creation

- Campaign creation is now blocked for ad accounts in non-supported regions at the message campaign, message set, and message level.
- Each layer returns a clear “region not supported” error instead of failing silently or returning a generic error.

## March 19, 2026

[`POST /act_<AD_ACCOUNT_ID>/messages`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/send-messages)

Specific Error Code for Recipient Not Available

- The Send API now returns error code 1893047 (RECIPIENT_NOT_AVAILABLE) instead of a generic internal error when the recipient is not available for receiving the message.
- This can occur due to various reasons such as account issues or platform enforcement actions.

## March 16, 2026

[`GET /<CAMPAIGN_ID>/insights`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/measure-performance)

Insights time_range and date_preset Support

- The `time_range` and `date_preset` parameters now work for all metrics on the [insights endpoint](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/measure-performance) .

[`GET /<APP_ID>/`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/onboard-businesses)

Business Manager No Longer Required for Onboarding

- We have launched a new [onboarding flow](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/onboard-businesses) where Business Manager access is no longer required for using the Marketing Message API for Messenger.
- The [business-onboarding documentation](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/onboard-businesses) has been updated with guidance on how to choose the right onboarding flow for your app, along with detailed setup instructions for each flow.

[`POST /act_<AD_ACCOUNT_ID>/messages`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/send-messages)

Improved Error Codes for Message Sending Failures

- New specific error codes have been introduced to provide clearer feedback when message sending fails: 2300018 (ATTACHMENT_SAVE_FAILURE): Returned when an attachment fails to save during message processing.2300027 (ATTACHMENT_REUSE_NOT_ALLOWED): Returned when attempting to reuse an attachment that is not permitted for reuse.2300052 (RECIPIENT_UNAVAILABLE): Returned when a recipient is no longer reachable or available to receive marketing messages.
- These replace previously generic error codes, enabling more precise troubleshooting.

Pacing Error Responses Now Include Remaining Wait Time

- When a message send is rejected due to pacing limits, the error response now includes a remaining_seconds field in error_data.
- This allows your application to programmatically determine how long to wait before retrying, rather than relying on fixed backoff strategies.

[`POST /<PAGE>/notification_message_tokens`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/get-subscription-tokens)

New Rate Limit Error Code for Subscription Token Queries

- A new error code 2300080 is now returned when the Subscription Tokens API rate limit is exceeded.
- This replaces the generic TOO_MANY_CALLS error, making it easier to distinguish token query rate limits from other API rate limits.

## March 9, 2026

[`POST /act_<AD_ACCOUNT_ID>/messages`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/send-messages)

Coupon Code Greeting Personalization Enabled

- Personalization macros (e.g., `{{first_name}}` ) are now enabled on the coupon-code pre-message greeting for coupon-template marketing messages.

## March 5, 2026

Asset-Based (UAT) Onboarding Flow Launched Globally

- The [asset-based (UAT) onboarding flow](https://developers.facebook.com/docs/marketing-messages-on-messenger/onboard-businesses#flow-2--asset-based-flow--uat-) without Business Portfolio requirement for the Marketing Message API for Messenger is now available to all Partner Apps.
- Partners can now complete asset-based (UAT) onboarding self-service.

## January 22, 2026

Webhook Recipient-ID Validation Fix

- Fixed a bug where click and read webhooks were emitting `recipient_id=0` when the page-scoped ID was null, causing webhook delivery to silently fail for partners.
- Webhooks now correctly pass null instead, preventing validation failures.

## January 17, 2026

[`POST /act_<AD_ACCOUNT_ID>/messages`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/send-messages)

Buttons With Support For App Destination Deeplinks

- Freeform templates now support [buttons with deeplinks](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/api-reference/generic) so that users can seamlessly navigate to specific destinations or features within your app.

## January 6, 2026

[`POST /act_<AD_ACCOUNT_ID>/messages`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/send-messages)

Personalized Greetings for Freeform Messages

- Freeform templates now support adding a greeting which shows up as a separate message before the marketing message.
- Businesses can use this greeting to create a more engaging conversational experience, as well as make use of the `{{first_name}}` , `{{last_name}}` , and `{{full_name}}` macros.
- For implementation details please see the [documentation](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/api-reference/generic) .

## November 20, 2025

[`POST /act_<AD_ACCOUNT_ID>/messages`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/send-messages)

Introducing Quick Replies

- We are excited to introduce [Quick Replies for the Marketing Message API for Messenger](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/send-messages/quick-replies) .
- Quick replies let you display up to 13 customizable buttons in a Messenger conversation, each with a title and optional image, shown above the message composer.
- They can be used to prompt users for specific actions or information, including text responses, phone number, or email address.
- When a user taps a quick reply, the buttons disappear and the selected response is sent to your webhook along with any associated payload.

Webhooks for Message Deliveries and Clicks

- The Marketing Message API for Messenger now supports webhooks for message delivery and click events.
- The new [message delivery webhook](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/send-messages#webhook-message-delivery-notification) notifies your application when a marketing message is successfully delivered to at least one user’s Messenger client.
- The [click webhook](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/send-messages#webhook-message-click-notification) sends a notification when a user clicks on a marketing message, enabling real-time tracking of user engagement.

Disable Usage of Postback Buttons With Video Attachment

- Postback buttons cannot be used with video attachments due to restrictions with the template.

## November 7, 2025

[`POST /act_<AD_ACCOUNT_ID>/customaudiences`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/grow-marketing-messages-audience#custom-audience-api)

Facebook Page in Custom Audience API

- You can now access the `messenger_marketing_messages_page` field in the Custom Audiences API for Marketing Messages custom audiences.
- Returning the associated Facebook Page in the Custom Audience API helps ensure you use the correct Page Access Token when making queries with the Subscription Tokens API.

[`POST /<PAGE>/notification_message_tokens`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/get-subscription-tokens)

Parameter to Remove Duplicate Recipients in Subscription Tokens API

- You can now obtain a single token per recipient by using the `do_not_return_duplicates` parameter in the Subscription Tokens API.
- In the Recurring Notifications API, recipients may have multiple tokens if they subscribe to different Topics. This filter helps prevent sending multiple Marketing Messages to the same recipient.

## November 6, 2025

[`POST /act_<AD_ACCOUNT_ID>/messages`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/send-messages)

Introducing Coupon Codes and LTO Format

- We are excited to announce the launch of the coupon codes and limited time offers (LTO) message formats.
- You can now send marketing messages that feature a coupon, with the option to include an expiration time and display a running timer.
- For additional details please see the [documentation](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/api-reference/coupon) .

## November 3, 2025

[`POST /act_<AD_ACCOUNT_ID>/messages`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/send-messages)

Introducing the Image Grid Format

- With the addition of this new format you can now showcase several images in a grid pattern within your marketing message.
- To do so, include the `image_urls` parameter in your message payload and specify the images you would like to display.
- For more details please visit the [documentation](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/api-reference/generic) .

## October 20, 2025

[`POST /act_<AD_ACCOUNT_ID>/messages`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/send-messages)

Improved Reliability for Message Sending

- Improved the reliability of sending direct marketing messages using the Marketing Message API for Messenger.
- Implemented more descriptive and explicit error messages to improve troubleshooting and transparency.

Webhooks for Message Sending

- We are excited to announce the launch of the message send status webhook feature.
- After a page sends a marketing message, your application can now receive a webhook notification confirming the message has been sent.
- For setup and additional details please visit the [documentation](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/send-messages#webhook-message-sent-notification) .

Remove Per-Campaign Send Restriction

- Previously, campaigns were limited to sending only one marketing message to a subscriber within a 90-day period.
- This restriction has now been lifted, allowing the same campaign to send multiple messages to the same subscriber in a 90-day window.

## October 6, 2025

[`POST act_<AD_ACCOUNT_ID>/campaigns`](https://developers.facebook.com/documentation/ads-commerce/marketing-api/ad-creative/messaging-ads/click-to-messenger)

CTM Ads Is Now Available to All Users

- [Click-to-Messenger (CTM) Ads](https://developers.facebook.com/documentation/ads-commerce/marketing-api/ad-creative/messaging-ads/click-to-messenger) supply has successfully completed its experimentation phase and is now available to all users using Marketing Messages on Messenger.
- With this launch, businesses can expect a higher rate of subscriber growth through the opt-in flow.

[`POST /act_<AD_ACCOUNT_ID>/messages`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/send-messages)

Postback Support

- We have enabled postback support for Marketing Messages ensuring that a user’s action on a marketing message button will be sent back to the message thread.
- To enable postback, clients can setup a webhook and add it onto their app and when the button is clicked an event will be sent to that
webhook

## September 26, 2025

[`POST /act_<AD_ACCOUNT_ID>/messages`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/send-messages)

Add personalization macros

- Enable personalization macros to the title and subtitle fields for all formats. `{{first_name}}` , `{{last_name}}` , and `{{full_name}}` can be added into the `title` and `subtitle` strings to enable personalized marketing messages. For carousel, each element can have a personalized `title` and `subtitle` . Buttons do not have personalization enabled.

## September 8, 2025

[`POST /act_<AD_ACCOUNT_ID>/customaudiences`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/grow-marketing-messages-audience#custom-audience-api)

Upload Status Webhook for Custom Audience API

- When uploading a list of subscribers using the Custom Audience API, we now support a webhook that triggers when the subscriber upload and matching process is complete.
- This can be used to keep track of when a created custom audience is ready to use.

[`GET /<PAGE_ID>/notification_message_tokens`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/get-subscription-tokens)

Increase Limit for Fetching Subscriber Tokens

- Increase the page limit from 100 to 1000.
- Increase the endpoint request limit from 200 per hour per DAU to 1000 per hour per DAU.
- As a result of these changes, the maximum number of subscriber tokens that can be fetched within a period of 1 hour from 20,000 per DAU to 1,000,000 per DAU.

Fix Missing Subscriber Tokens With Filters

- Previously, filtering subscription tokens by custom audience IDs did not return any tokens due to restrictive filtering logic.
- Using custom audience ID filters will now correctly return all matching tokens.

[`POST /act_<AD_ACCOUNT_ID>/messages`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/send-messages)

Fix Missing Marketing Message From Page’s Inbox

- Due to privacy reasons, marketing messages sent to custom audience subscribers were not be visible to the page after delivery.
- Once the user responds to these messages, these messages will now become visible to the page.

## August 25, 2025

[`POST /act_<AD_ACCOUNT_ID>/messages`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/send-messages)

Allow the Creation of Marketing Messages Without a Button

- When sending a marketing message, it is no longer necessary for the message payload attachment to include a button.

Improved Message Sending for Custom Audience Subscribers

- Increase the proportion of custom audience subscribers which are eligible to receive a marketing message by 10%.

[`POST /act_<AD_ACCOUNT_ID>/message_campaign`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/send-messages)

Check Terms of Service During Campaign Creation

- Return an error response during campaign creation when the business has not signed the Marketing Message API for Messenger Terms of Service.

## August 11, 2025

[`POST /act_<AD_ACCOUNT_ID>/messages`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/send-messages)

Cooldown Between Message Sends

- The `subscription_token` message sending cooldown has been updated from 24 hours to 12 hours. This means marketing messages sent using the same `subscription_token` now require only a 12-hour wait between sends, allowing for more frequent communication with users.

## July 31, 2025

[`POST /<CUSTOM_AUDIENCE_ID>/users`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/grow-marketing-messages-audience)

[`GET /<PAGE_ID>/notification_message_tokens`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/get-subscription-tokens)

Custom Audience Segmentation For Subscription Tokens

- When uploading a list of subscribers via `/<CUSTOM_AUDIENCE_ID>/users` in the [Custom Audience API](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/get-subscription-tokens#custom-audience-api) , the corresponding Custom Audience ID(s) will be included in the subscription token’s `custom_audience_ids` field. Note that a single subscription token can be associated with multiple custom audience uploads.
- You can filter subscription tokens by one or more Custom Audience IDs using the optional `custom_audience_ids` query parameter on the `/<PAGE_ID>/notification_message_tokens` endpoint.
- To safeguard user privacy, the `/<PAGE_ID>/notification_message_tokens` endpoint will only return subscription tokens for a given Custom Audience if there are 100 or more matched users in that audience upload. If fewer than 100 users match, tokens for that Custom Audience will be excluded from the response.

[`GET act_<AD_ACCOUNT_ID>/insights`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/measure-performance)

Measure a Marketing Messages on Messenger Campaign Performance

- Insights under an ad account can be obtained by the `act_<AD_ACCOUNT_ID>/insights` endpoint

## July 1, 2025

Introducing the Marketing Message API for Messenger!
