# Catalogs - Webhooks from Meta

_Source: https://developers.facebook.com/docs/graph-api/webhooks/getting-started/webhooks-for-catalogs_

---

# Webhooks for Catalogs

Webhooks for catalogs allow you to get real-time notifications for certain data changes.

To set up Webhooks for catalogs, the following steps are required:

1. [Set up your endpoint and configure the Webhooks](#setup).
2. [Subscribe your app under your catalog](#subscribe).

## Set up Endpoint and Webhooks

Follow our [Webhooks Getting Started guide](https://developers.facebook.com/docs/graph-api/webhooks/getting-started) to create your endpoint and configure your Webhooks. When you configure your webhooks, make sure to choose `Catalog`.

![](https://lookaside.fbsbx.com/elementpath/media/?media_id=1476119800125789&version=1762401082)



Subscribe to one or more fields below:

| Field | Description |
| --- | --- |
| `product_feed` | Notifies you when the data from a [Product Feed](https://developers.facebook.com/docs/marketing-api/reference/product-feed/) has persisted. |
| `items_batch` | Notifies you when the data from a [Product Catalog Items Batch](https://developers.facebook.com/docs/marketing-api/reference/product-catalog/items_batch/) session has persisted. |

For the Webhook data structure, refer to the [Webhooks Reference - Catalog.](https://developers.facebook.com/docs/graph-api/webhooks/reference/catalog/)

## Subscribe Your App

You need to subscribe your app to Webhook notifications for your catalog. You app should have edit permission to the catalog to complete this step. The app should also have `catalog_management` permission.

To subscribe your app, have your app send a `POST` request `subscribed_apps` for the catalog:

```
curl -X POST \
  "https://graph.facebook.com/<VERSION>/<CATALOG_ID>/subscribed_apps?access_token=<ACCESS_TOKEN>" \
-d 'app_id=<APP_ID>'
```

To see which apps are subscribed for your catalog, send a `GET` request:

```
curl -X GET \
  "https://graph.facebook.com/<VERSION>/<CATALOG_ID>/subscribed_apps?access_token=<ACCESS_TOKEN>"
```

On success, you will see this response:

```
{
  "data": [
    {
      "name": "<APP_NAME>",
      "id": "<APP_ID>"
    }
  ]
}
```

To remove an app from subscription, send a `DELETE` request:

```
curl -X DELETE \
  "https://graph.facebook.com/<VERSION>/<CATALOG_ID>/subscribed_apps?access_token=<ACCESS_TOKEN>" \
-d 'app_id=<APP_ID>'
```
