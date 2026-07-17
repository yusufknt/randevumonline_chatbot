# Measure Campaign Performance on Marketing Message API for Messenger | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/measure-performance_

---

# Measure Campaign Performance on Marketing Message API for Messenger

Updated: Mar 3, 2026

This document explains how to obtain insights for a marketing message campaign, including:

- Number of messages delivered
- Message read and click rate
- Cost per delivery and click

## Insights on delivered messages

Send a `GET` request to the `<MESSAGE_CAMPAIGN_ID>/insights` endpoint to get insights for marketing messages campaign with the `fields` parameter set to one or more of the following fields:

- `marketing_messages_cost_per_delivered`
- `marketing_messages_cost_per_link_btn_click`
- `marketing_messages_delivered`
- `marketing_messages_link_btn_click`
- `marketing_messages_link_btn_click_rate`
- `marketing_messages_read_rate`
- `marketing_messages_spend`

### Sample request

*Formatted for readability.*

```html
curl -i -X GET \
     -H "Authorization: Bearer <SYSTEM_USER_ACCESS_TOKEN>" \
     "https://graph.facebook.com/<API_VERSION>/<MESSAGE_CAMPAIGN_ID>/insights \
       ?fields=marketing_messages_delivered,marketing_messages_read_rate"
```

### Field Reference

| Property | Description |
| --- | --- |
| `marketing_messages_cost_per_delivered` | The average cost per message delivered. [This metric is in development](https://www.facebook.com/business/help/metrics-labeling). |
| `marketing_messages_cost_per_link_btn_click` | The average cost for each message link click. This metric doesn’t include messages sent to Europe, Argentina, Turkey, South Korea and Japan. [This metric is in development](https://www.facebook.com/business/help/metrics-labeling). |
| `marketing_messages_delivered` | The number of messages a business sent to users that were delivered. Some messages may not be delivered, such as when a user’s device is out of service. This metric doesn’t include messages delivered to Europe and Japan. In some cases, this metric may be estimated and may differ from what’s shown on your invoice due to small variations in data processing. [This metric is in development](https://www.facebook.com/business/help/metrics-labeling). |
| `marketing_messages_link_btn_click` | The number of clicks or taps within the marketing message that led to advertiser-specified destinations, on or off Meta technologies. This metric doesn’t include messages sent to Europe, Argentina, Turkey, South Korea and Japan. [This metric is in development](https://www.facebook.com/business/help/metrics-labeling). |
| `marketing_messages_link_btn_click_rate` | The percentage of delivered messages that received a link click out of the total number of messages delivered. This metric doesn’t include messages sent to Europe, Argentina, Turkey, South Korea and Japan. [This metric is in development](https://www.facebook.com/business/help/metrics-labeling). |
| `marketing_messages_read_rate` | The number of messages read divided by the number of messages delivered. Some message reads may not be captured, such as when a customer has turned off read receipts. This metric doesn’t include messages sent to Europe and Japan. [This metric is in development](https://www.facebook.com/business/help/metrics-labeling). |
| `marketing_messages_spend` | The total amount of money you’ve spent on your campaign, set or message during its schedule. [This metric is in development](https://www.facebook.com/business/help/metrics-labeling). |

On success, your app receives a JSON object with the number of messages delivered, the read rate, and the start and stop date of the messaging campaign.

### Example response

```json
{
  "data": [
    {
      "marketing_messages_delivered": "2755",
      "marketing_messages_link_btn_click": "268",
      "marketing_messages_spend": "38.87",
      "marketing_messages_read_rate": "79.419238",
      "marketing_messages_link_btn_click_rate": "9.727768",
      "marketing_messages_cost_per_link_btn_click": "0.145037",
      "marketing_messages_delivery_rate": "0",
      "marketing_messages_cost_per_delivered": "0.014109",
      "date_start": "2024-05-01",
      "date_stop": "2025-07-29"
    }
  ],
  "paging": {
    "cursors": {
      "before": "MAZDZD",
      "after": "MAZDZD"
    }
  }
}
```

Additionally, insights under an ad account can be obtained by `act_<AD_ACCOUNT_ID>/insights` endpoint

Querying on time ranges and date presets is also supported for campaigns created March 1st or later. Below are query parameter options you can use to query on specific dates:

| Parameter Name | Description |
| --- | --- |
| `time_range`<br>{‘since’:YYYY-MM-DD,’until’:YYYY-MM-DD} | A single `time range` object. UNIX timestamp not supported. |
| `date_preset`<br>enum{today, yesterday, this_month, last_month, this_quarter, maximum, data_maximum, last_3d, last_7d, last_14d, last_28d, last_30d, last_90d, last_week_mon_sun, last_week_sun_sat, last_quarter, last_year, this_week_mon_today, this_week_sun_today, this_year} | Default value: `last_30d`<br>Represents a relative time range. This field is ignored if time_range is specified. |

## Next Steps

Now that you have learned how to get insights on your campaign, learn how to [increase a business’ subscribers](https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/get-subscription-tokens).
