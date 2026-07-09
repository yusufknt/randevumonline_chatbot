# Messaging Limits | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/messaging-limits_

---

# Messaging Limits

Updated: May 8, 2026

The `messaging_limit_tier` field, which used to return a business phone number’s messaging limit, has been deprecated. [Request](https://developers.facebook.com/documentation/business-messaging/whatsapp/messaging-limits#via-api) the `whatsapp_business_manager_messaging_limit` field instead.

This document describes messaging limits for the WhatsApp Business Platform.

Messaging limits are the maximum number of unique WhatsApp user phone numbers your business can deliver messages to, outside of a [customer service window](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages#customer-service-windows), within a moving 24-hour period.

Messaging limits are calculated and set at the business portfolio level and are shared by all business phone numbers within a portfolio. This means that if a business portfolio has multiple business phone numbers, it’s possible for one number to consume all of the portfolio’s messaging capability within a given period.

Newly created business portfolios have a messaging limit of 250, but this limit can be increased to:

- 2,000 (by completing a [scaling path](https://developers.facebook.com/documentation/business-messaging/whatsapp/messaging-limits#scaling-paths) )
- 10,000 (via [automatic scaling](https://developers.facebook.com/documentation/business-messaging/whatsapp/messaging-limits#automatic-scaling) )
- 100,000 (via automatic scaling)
- Unlimited (via automatic scaling)

## Increasing your limit

You can increase your messaging limit to 2,000 by completing one of the [scaling paths](https://developers.facebook.com/documentation/business-messaging/whatsapp/messaging-limits#scaling-paths) below. After that, we will automatically increase your limit to the next higher limit if you meet our [automatic scaling criteria](https://developers.facebook.com/documentation/business-messaging/whatsapp/messaging-limits#automatic-scaling).

### Scaling paths

- [Verify your business](https://www.facebook.com/business/help/2058515294227817)
- Have your [solution provider verify your business](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/partner-led-business-verification) (if you were onboarded by one)
- Send 2,000 delivered messages outside of customer service windows to unique WhatsApp user phone numbers within a 30-day moving period, using templates with a high [quality rating](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-quality) .

Once you complete one of these paths, we will analyze your [message quality](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages#message-quality). Based on this analysis, your business portfolio’s eligibility for automatic scaling will either be approved or denied.

### Approvals

If your request is approved, we will immediately increase your business phone number’s messaging limit to 2,000 and notify you by email and developer alert. In addition, a [business_capability_update](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/business_capability_update) webhook will be triggered with `max_daily_conversations_per_business` (for webhooks v24.0 and newer) and `max_daily_conversation_per_phone` (for v23.0 and older, until February, 2026) set to the new limit.

Additional messaging limit increases for your business portfolio can now happen automatically, via [automatic scaling](https://developers.facebook.com/documentation/business-messaging/whatsapp/messaging-limits#automatic-scaling).

### Denials

If your request is denied, we will maintain your business phone number’s messaging limit at its current level and notify you via email and developer alert. In addition, an [account_alerts](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/account_alerts) webhook will be triggered, with the `alert_type` and `alert_description` properties indicating alternate methods you can pursue to increase your limit.

| `alert_type` Value | Action you can take |
| --- | --- |
| `INCREASED_CAPABILITIES_ELIGIBILITY_DEFERRED` | Send 2,000 delivered messages outside of customer service windows to unique WhatsApp user phone numbers in a 30-day moving period, using templates with a high [quality rating](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-quality). |
| `INCREASED_CAPABILITIES_ELIGIBILITY_FAILED` | Send 2,000 delivered messages outside of customer service windows to unique WhatsApp user phone numbers within a 30-day moving period, using templates with a high [quality rating](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-quality). |
| `INCREASED_CAPABILITIES_ELIGIBILITY_NEED_MORE_INFO` | [Verify your identity](https://www.facebook.com/business/help/587323819101032), or send 2,000 delivered messages outside of customer service windows to unique WhatsApp user phone numbers within a 30-day moving period, using templates with a high [quality rating](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-quality). |

## Automatic scaling

Once your business portfolio’s messaging limit has been increased to 2,000, we will determine if it should be increased further according to the following criteria:

- You are sending [high-quality messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages#message-quality) across all of your business phone numbers and templates
- In the last 7 days, your business has utilized at least half of your current messaging limit

If these criteria are met, we will increase your portfolio’s limit by one level within 6 hours.

## Checking your limit

### Via Meta Business Suite

Your business phone number’s current messaging limit is displayed in the [WhatsApp Manager](https://business.facebook.com/wa/manage/home/) > **Account tools** > **Messaging limits** panel:

![WhatsApp Manager Messaging Limits panel showing current portfolio limit and scaling status](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/535132607_2167690997071606_2519788358245522587_n.png?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=zu9Eqx6X83sQ7kNvwEgsaJn&_nc_oc=Adr5g2iEwOY13bUytW7mWU5Eyxtyz9r-QuKYF2QnSLR2PQVhAdDQJVtm_UI_tevHR04&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=1vDkM49Y5ZpjBjCm2SQXiw&_nc_ss=7b20f&oh=00_Af7l_K3M7EDicMYwg-9heznndIjYk72VH2com36Mfi8S3Q&oe=6A1C2759)

### Via API

Use the [WhatsApp Business Phone Number API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/whatsapp-business-account-phone-number-api#get-version-phone-number-id) and request the `whatsapp_business_manager_messaging_limit` field.

Note that the `messaging_limit_tier`, which used to return the phone number’s messaging limit, has been deprecated.

### Example request

```curl
curl 'https://graph.facebook.com/v25.0/106540352242922?fields=whatsapp_business_manager_messaging_limit' \
-H 'Authorization: Bearer EAAJB...'
```

Example response

```json
{
  "whatsapp_business_manager_messaging_limit": "TIER_250",
  "id": "106540352242922"
}
```
