# Set a max-price for marketing messages (BETA) | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/pricing_

---

# Set a max-price for marketing messages (BETA)

Updated: Mar 17, 2026

Amidst our introduction of the max-price feature on the Marketing Messages API for WhatsApp, there is no change to how we charge on the WhatsApp Business Platform. We continue to charge on a per-message basis, as outlined [here](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing).

The max-price feature will become available via Limited Beta as of mid-May and be **optional** throughout 2026.

## What is a max-price?

As announced in March 2026 -- in 2026, we’re introducing new pricing features on the Marketing Messages API for WhatsApp to enable businesses to *drive higher ROI* and *have more control* to optimize spend for their marketing messaging campaigns.

Our first pricing feature allows businesses to **set a maximum price (max-price) per marketing message delivery; when a max-price is set, Meta will charge that max-price or lower for delivery**. Businesses can choose to set a max-price the same as, lower than, or higher than the published rate to achieve their objectives per campaign.

- *Lower costs while maintaining delivery rates similar to current WhatsApp campaigns* , by setting max-prices the same as published rates.
- *Target a broader range of customer cohorts on WhatsApp at lower cost* , by setting max-prices lower than published rates.
- *Increase delivery rates when customer engagement matters most* , like during holidays and peak sales periods, by setting max-prices higher than published rates.

The second pricing feature is the **reach estimation tool**, which helps businesses set the right max-price by helping them understand estimated delivery rates and costs at different max-prices.

### Max-price explainer

The max-price feature allows you to set the maximum price you are willing to pay per message delivery. You are charged your max-price or lower. In the API, you express this as a `bid_amount` value per 1,000 deliveries within the `bid_spec` object.

- Max-price explainer PDF

## Phased roll-out of the max-price feature

We plan to roll out our max-price feature in 3 phases:

1. Limited Beta starting **mid-May 2026** -- Any partner and any directly-integrated business can integrate and use the max-price feature and reach estimation tool. Each partner can enable these features for a limited number of clients.
2. Open Beta starting **October 2026** -- Any partner can enable these features for all their clients.
3. General Availability (GA) as of **Q2 2027** -- The max-price feature will become required in eligible geographies and fixed, published rates for marketing messages will only apply on the Cloud API.

## Before you begin

To use the max-price feature, you must:

- Have an active WhatsApp Business Account that has been [onboarded](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/onboarding) to the Marketing Messages API for WhatsApp.
- Be in a [country eligible for MM API for WhatsApp](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/get-started#geographic-availability-of-features) .

## Recommendations

Set your max-price at the template level. The `bid_amount` in `bid_spec` is what Meta’s delivery system optimizes against. Setting the right max-price when you create the template gives the system the best signal for delivery optimization.

The `per_message_bid_multiplier` scales the template’s `bid_amount` up or down for individual messages, but the delivery system generally gives better performance optimizing based on the original template-level `bid_amount` on large amount.

For example, if you set a template’s `bid_amount` to 50,000 and then apply a multiplier of 2.0 on every message, delivery performance might differ from setting the template’s `bid_amount` to 100,000 directly -- even though the effective max-price is the same. Hence we recommend setting up the bid at template level and update the template’s `bid_spec` if needed rather than changing the message level multiplier as a workaround.

Ramp up traffic gradually. When sending messages with a new max-price template for the first time, increase volume slowly before sending at scale. This aligns with [Template pacing](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-pacing) best practices and helps the delivery system optimize effectively.

## Create templates with max-price

Use the [Message Templates API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/template-api#post-version-waba-id-message-templates) to set a maximum price and include the `bid_spec` object in the request body.

### Request syntax

```html
curl 'https://graph.facebook.com/<API_VERSION>/<WHATSAPP_BUSINESS_ACCOUNT_ID>/message_templates' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '
  {
    "name": "seasonal_sale_promo",
    "category": "MARKETING",
    "language": "en",
    "components": [
      {
        "type": "BODY",
        "text": "Shop our seasonal sale! Up to 50% off selected items."
      }
    ],
    "bid_spec": {
      "bid_amount": "<BID_AMOUNT>",
      "bid_strategy": "LOWEST_COST_WITH_BID_CAP"
    }
}'
```

If `bid_spec` is not included, the template uses standard rate card pricing.

### Request parameters

| Column 1 | Column 2 | Column 3 |
| --- | --- | --- |
| Placeholder | Description | Example Value |
| `<ACCESS_TOKEN>`<br>*String* | **Required.**<br>[System token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens) or [business token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens). | `EAAA...` |
| `<API_VERSION>`<br>*String* | **Optional.**<br>Graph API version. | v25.0 |
| `<WABA_ID>`*String* | **Required.**<br>WhatsApp Business Account ID. | `102290129340398` |
| `<BID_AMOUNT>`<br>*int* | **Required.**<br>Maximum price per 1,000 message deliveries, expressed in your WABA currency’s smallest unit (cents for USD, paise for INR, peso for MXN). See [supported currencies](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing#updates-to-rate-cards) for a list of currencies. | `87000` |

### Calculating max-price amounts

The `bid_amount` represents your max-price per 1,000 deliveries in your WABA currency’s smallest unit. To convert from your desired per-delivery price:

- Convert your desired per-delivery price to your WABA currency’s smallest unit
- Multiply by 1,000 to express the value per 1,000 deliveries

**Example**: To set a max-price of ₹0.87 per delivery:

- Convert to paise: 0.87 Rupees = 87 paise
- Multiply by 1,000: 87 x 1,000 = 87,000

Set `bid_amount` to `87000`.

**Example**: To set a max-price of $0.05 USD per delivery:

- Convert to cents: $0.05 = 5 cents
- Multiply by 1,000: 5 x 1,000 = 5,000

Set `bid_amount` to `5000`.

## Retrieve max-price information

Use the [Template API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/template-api#get-version-template-id) to get the max-price setting on an existing template.

### Request syntax

```html
curl 'https://graph.facebook.com/<API_VERSION>/<TEMPLATE_ID>/?fields=bid_spec' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>'
```

### Request parameters

| Column 1 | Column 2 | Column 3 |
| --- | --- | --- |
| Placeholder | Description | Example Value |
| `<ACCESS_TOKEN>`<br>*String* | **Required.**<br>[System token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens) or [business token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens). | `EAAA...` |
| `<API_VERSION>`<br>*String* | **Optional.**<br>Graph API version. | v25.0 |
| `<TEMPLATE_ID>`<br>*String* | **Required.**<br>ID of the WhatsApp message template. | `1733678867511493` |

### Example response

```json
{
  "bid_spec": {
    "bid_strategy": "LOWEST_COST_WITH_BID_CAP",
    "bid_amount": 87000
  },
  "id": "1733678867511493"
}
```

## Update max-price for templates

Use the [Template API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/template-api#post-version-template-id) to update the max-price setting on an existing template.

You can update the `bid_spec` on templates that were originally created with a max-price. The same parameters apply.

You cannot add `bid_spec` to an existing template that was created without it. You must create a new template with `bid_spec` included.

Other constraints follow the standard [template editing limits](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview):

- **Approved templates** : Up to 100 edits per hour, 2,400 per day
- **Rejected or paused templates** : Unlimited edits

### Request syntax

```html
curl 'https://graph.facebook.com/<API_VERSION>/<TEMPLATE_ID>/' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
  "bid_spec": {
    "bid_strategy": "LOWEST_COST_WITH_BID_CAP",
    "bid_amount": <BID_AMOUNT>
  }
}'
```

### Request parameters

| Column 1 | Column 2 | Column 3 |
| --- | --- | --- |
| Placeholder | Description | Example Value |
| `<ACCESS_TOKEN>`<br>*String* | **Required.**<br>[System token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens) or [business token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens). | `EAAA...` |
| `<API_VERSION>`<br>*String* | **Optional.**<br>Graph API version. | v25.0 |
| `<TEMPLATE_ID>`<br>*String* | **Required.**<br>ID of the WhatsApp message template. The template must have been originally created with `bid_spec`. | `1733678867511493` |
| `<BID_AMOUNT>`<br>*int32* | **Required.**<br>Updated maximum price per 1,000 message deliveries, expressed in your WABA currency’s smallest unit. | `4000` |

## Adjust max-price when sending messages

The message-level max-price multiplier is subject to change during the beta period.

Use the [Marketing Messages API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/marketing-messages-lite-api) to apply a multiplier at sending time to adjust the template-level max-price for individual messages. This allows you to max-price higher or lower without editing the template.

### Request syntax

```html
curl 'https://graph.facebook.com/<API_VERSION>/<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>/marketing_messages' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
  "recipient_type": "individual",
  "messaging_product": "whatsapp",
  "to": "<WHATSAPP_USER_PHONE_NUMBER>",
  "type": "template",
  "template": {
    "name": "seasonal_sale_promo",
    "language": {
      "code": "en"
    }
  },
  "bid_spec": {
    "per_message_bid_multiplier": "<PER_MESSAGE_BID_MULTIPLIER>"
  }
}'
```

In this example, the multiplier of 1.5 increases the template’s `bid_amount` by 50%. If the template’s `bid_amount` is 2000, the effective max-price for this message becomes 3000.

### Request parameters

| Column 1 | Column 2 | Column 3 |
| --- | --- | --- |
| Placeholder | Description | Example Value |
| `<ACCESS_TOKEN>`<br>*String* | **Required.**<br>[System token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens) or [business token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens). | `EAAA...` |
| `<API_VERSION>`<br>*String* | **Optional.**<br>Graph API version. | v25.0 |
| `<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>`<br>*String* | **Required.**<br>WhatsApp business phone number ID. | `106540352242922` |
| `<WHATSAPP_USER_PHONE_NUMBER>`<br>*String* | **Required.**<br>WhatsApp user phone number. | `+16505551234` |
| `<PER_MESSAGE_BID_MULTIPLIER>`<br>*Float* | **Optional.** Default: `1`<br>A positive multiplier applied to the template’s `bid_amount`. For example, `1.5` increases the max-price by 50%, `0.5` decreases it by 50%, and `1` (default) uses the template’s max-price amount unchanged. | `1.5` |

## Estimate reach and costs

The Reach estimation helps you understand your expected deliveries and costs at different max-price levels.

### Request syntax

Use the [WhatsApp Business Account API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/whatsapp-business-account-api#get-version-waba-id) to get the estimated delivery ranges and cost ranges at various max-price amounts.

Estimates are generated using historical data and are for informational and planning purposes only. They do not guarantee future delivery outcomes, costs, or performance. Actual results may differ due to changes in platform conditions or other variables.

The `targeting_spec` value must be serialized JSON. For example:

```html
curl 'https://graph.facebook.com/<API_VERSION>/<WHATSAPP_BUSINESS_ACCOUNT_ID>/reachestimate?targeting_spec={"geo_locations":{"countries":["IN"]}}&date_interval=<DATE_INTERVAL>' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>'
```

### Request parameters

| Column 1 | Column 2 | Column 3 |
| --- | --- | --- |
| Placeholder | Description | Example Value |
| `<ACCESS_TOKEN>`<br>*String* | **Required.**<br>[System token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens) or [business token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens). | `EAAA...` |
| `<API_VERSION>`<br>*String* | **Optional.**<br>Graph API version. | v25.0 |
| `<WABA_ID>`*String* | **Required.**<br>WhatsApp Business Account ID. | `102290129340398` |
| `<DATE_INTERVAL>`<br>*Enum* | **Required.**<br>Lookback period for the historical data used to generate estimates. One of: `L1D` (last 1 day), `L7D` (last 7 days), `L14D` (last 14 days), `L28D` (last 28 days). | `L7D` |
| `<TARGETING_SPEC>`<br>*JSON* | **Required.**<br>Serialized JSON specifying geographic targeting. Must include `geo_locations` with a `countries` array. | `{"geo_locations":{"countries":["IN"]}}` |

### Example response

```json
{
  "waba_currency": "USD",
  "estimates": [
    {
      "bid_amount": 400,
      "users": 1000,
      "lower_bound_deliveries": 500,
      "upper_bound_deliveries": 570,
      "cost_lower_bound": 389.74,
      "cost_upper_bound": 390.74
    },
    {
      "bid_amount": 520,
      "users": 1000,
      "lower_bound_deliveries": 600,
      "upper_bound_deliveries": 650,
      "cost_lower_bound": 400.74,
      "cost_upper_bound": 510.74
    }
  ]
}
```

The response contains multiple `estimates` entries at different max-price amounts, allowing you to compare expected delivery volumes and costs across price points.

### Response fields

| Column 1 | Column 2 |
| --- | --- |
| Field | Description |
| waba_currency | The currency of your WhatsApp Business Account. |
| bid_amount | Max-price per 1,000 message deliveries, in the WABA currency’s smallest unit. |
| users | Targeted user count. Fixed at 1,000 during beta. |
| lower_bound_deliveries | Lower bound of the estimated delivery range for this max-price amount. |
| upper_bound_deliveries | Upper bound of the estimated delivery range for this max-price amount. |
| cost_lower_bound | Lower bound of the estimated average cost per 1,000 deliveries, in the WABA currency’s smallest unit. |
| cost_upper_bound | Upper bound of the estimated average cost per 1,000 deliveries, in the WABA currency’s smallest unit. |

## Metrics and billing

Messages sent with or without the max-price feature use the same **Marketing Lite** product type (SKU) for billing purposes.

Marketing messages sent with max-price appear in analytics with the following identifiers:

- **Pricing Analytics** [`/<WHATSAPP_BUSINESS_ACCOUNT_ID>?fields=pricing_analytics`](https://developers.facebook.com/documentation/business-messaging/whatsapp/analytics#pricing-analytics) : `pricing_category` = `MARKETING_LITE`
- **Template Analytics** [`/<WHATSAPP_BUSINESS_ACCOUNT_ID>?fields=template_analytics`](https://developers.facebook.com/documentation/business-messaging/whatsapp/analytics#template-analytics) : `product_type` = `MARKETING_MESSAGES_LITE_API`

Webhooks use lowercase `marketing_lite` for `pricing.category`, while analytics APIs use uppercase `MARKETING_LITE` for `pricing_category`.

### Pricing analytics response example

```json
{
  "pricing_analytics": {
    "data": [
      {
        "data_points": [
          {
            "start": 1748761200,
            "end": 1748847600,
            "country": "IN",
            "pricing_type": "REGULAR",
            "pricing_category": "MARKETING_LITE",
            "volume": 1,
            "cost": 10
          }
        ]
      }
    ]
  }
}
```

### Template analytics response example

```json
{
  "data": [
    {
      "granularity": "DAILY",
      "product_type": "MARKETING_MESSAGES_LITE_API",
      "data_points": [
        {
          "template_id": "1421988012088524",
          "start": 1718064000,
          "end": 1718150400,
          "sent": 1,
          "delivered": 1,
          "read": 1,
          "cost": [
            {
              "type": "amount_spent",
              "value": 0.01
            },
            {
              "type": "cost_per_delivered",
              "value": 0.01
            }
          ]
        }
      ]
    }
  ]
}
```

For more details on metrics, see [Viewing metrics](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/view-metrics).

## Error codes

| Column 1 | Column 2 | Column 3 |
| --- | --- | --- |
| Code | Message | Possible reasons and solutions |
| 131061 | Marketing templates containing bid_spec are not supported by the Cloud API. To use templates with bid_spec, please use the Marketing Messages API for WhatsApp. | You are sending a template with `bid_spec` to the Cloud API `/messages` endpoint. Send to the `/marketing_messages` endpoint instead. |
| 100 | You need to sign the testing legal agreement before sending out messages. | You have not signed the testing legal agreement. Please sign the agreement to gain access to this feature. |

For a full list of error codes, see [Error codes](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/error-codes).
