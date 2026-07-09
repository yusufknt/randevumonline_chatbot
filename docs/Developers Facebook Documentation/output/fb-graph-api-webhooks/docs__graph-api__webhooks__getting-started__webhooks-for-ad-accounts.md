# Ad Accounts - Webhooks from Meta

_Source: https://developers.facebook.com/docs/graph-api/webhooks/getting-started/webhooks-for-ad-accounts_

---

# Webhooks for Ad Accounts

Webhooks for ad accounts allow you to get real-time notifications for certain ads changes.

## Before You Begin

1. [Set up your endpoint and configure the Webhooks](#setup).
2. [Subscribe your app under your ad account](#subscribe).

## Endpoint and Webhooks Setup

Follow our [Webhooks Getting Started guide](https://developers.facebook.com/docs/graph-api/webhooks/getting-started) to create your endpoint and configure your webhooks by choosing **Ad Account**.

![](https://lookaside.fbsbx.com/elementpath/media/?media_id=249334528266072&version=1766447472)

You can get real-time notifications for ad object status changes by subscribing to one or more fields below.

| Field | Description |
| --- | --- |
| `with_issues_ad_objects` | Notifies you when a campaign, ad set, or ad under the ad account changes to the `WITH_ISSUES` status. |
| `in_process_ad_objects` | Notifies you when a campaign, ad set, or ad is finished processing and exits the `IN_PROCESS` status. |
| `ad_recommendations` | Notifies you when ad recommendations are generated for your ads. |
| `creative_fatigue` | Notifies you when your ad enters or exits fatigue. Provides more granular information with different fatigue levels such as `Low`, `Medium`, and `High`. Only sends notifications for ads that have an `ACTIVE` status. |
| `product_set_issue` | Notifies you when a product set encounters issues that affect your ads. |

See [Post-Processing](https://developers.facebook.com/docs/marketing-api/using-the-api/post-processing/) for more information.

## Webhook Subscription

You need to subscribe your app to webhook notifications for your ad account. You app should have edit permission to the ad account to complete this step. The app should also have `ads_management` permission.

### Subscribe your app

To subscribe your app, send a `POST` request to the `/{ad-account-id}/subscribed_apps` endpoint with the app ID.

#### Example request

```
curl -i -X POST \
  -d "access_token=<ACCESS_TOKEN>" \
  -d "app_id=<APP_ID>" \
"https://graph.facebook.com/v25.0/act_<AD_ACCOUNT_ID>/subscribed_apps"
```

#### Example response

On success, you'll receive this response:

```
{
  "success": "true"
}
```

### Retrieve an ad account's app subscriptions

To see which of your ad account's apps have subscriptions, send a `GET` request to the `/{ad-account-id}/subscribed_apps` endpoint.

#### Example request

```
curl -i -X GET \
  -d "access_token=<ACCESS_TOKEN>" \
"https://graph.facebook.com/v25.0/act_<AD_ACCOUNT_ID>/subscribed_apps"
```

#### Example response

On success, you'll receive this response:

```
{
  "data":[
    {
      "name": "<APP_NAME>",
      "id": "<APP_ID>"
    }
  ]
}
```

### Delete an app's subscriptions

To remove a subscription from an app, send a `DELETE` request to the `/{ad-account-id}/subscribed_apps` endpoint.

#### Example request

```
curl -X DELETE \
  -d "access_token=<ACCESS_TOKEN>" \
"https://graph.facebook.com/v25.0/act_<AD_ACCOUNT_ID>/subscribed_apps"
```

#### Example response

On success, you'll receive this response:

```
{
  "success": "true"
}
```

## Subscribe with Graph API Explorer

You can also subscribe an app with the [Graph API Explorer](https://developers.facebook.com/tools/explorer).

Replace the `me?fields=id,name` query with `act_<AD_ACCOUNT_ID>/subscribed_apps`. Running this will subscribe the app you have selected in the **Meta App** dropdown menu. Or you can subscribe a different app by specifying `subscribed_apps` as an input parameter with the app Id.

**Note:** The app must have permission to edit the ad account in order to subscribe.

```
[
  {
    "object": "ad_account",
    "entry": [
      {
        "id": "0",
        "time": 1568132516,
        "changes": [
          {
            "field": "with_issues_ad_objects",
            "value": {
              "id": "111111111111",
              "level": "AD",
              "error_code": "567",
              "error_summary": "error summary",
              "error_message": "error message"
            }
          }
        ]
      }
    ]
  }
]
```
