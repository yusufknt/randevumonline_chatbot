# Metrics API | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/reference/metrics_api_

---

# Metrics API

Updated: Feb 4, 2026

Metrics API will be deprecated on **30th of April 2026**

The Metrics API enables you to query system metrics related to flows. Essentially, these metrics allow you to track the performance of the endpoint that the flow uses to send requests. The metrics include the number of requests sent to an endpoint, the number of errors, the distribution of request latency, error rate, and endpoint availability.

There is a threshold for the minimum number of requests within a flow. The rule is as follows: if a flow generated fewer than 250 requests, an exception will be thrown, indicating that there is not enough data. Once this threshold is reached, the data will be returned in the usual manner.

Flow metrics are still being developed and may change as we improve our methodologies. We encourage you to use these metrics for directional guidance, but use caution when using them for historical comparisons or strategic planning.

## Available Flow Metrics

All metrics are not realtime. In some cases it may take a couple of hours for metric events to be ingested and become available for querying.

Every metric has a unique name which acts as a metric identifier and an associated data object.

| Metric Name | Metric Data Object |
| --- | --- |
| `ENDPOINT_REQUEST_COUNT`<br>Flow endpoint request count. | Endpoint request count for a given period of time. Single value.<br>Example:<br>`[<br> {<br> "key": "value",<br> "value": 315<br> }<br>]`<br>In this example there are 15 endpoint requests. |
| `ENDPOINT_REQUEST_ERROR`<br>Flow endpoint errors. | Endpoint request errors aggregated by error types:<br>`timeout_error` — Endpoint request exceeded the request time limit.`unexpected_http_status_code` — Endpoint request has failed. Received error http response code.`cannot_be_served` — Endpoint request has not been executed because the flow can not be served.`no_http_response_error` — Endpoint request has failed. Internal error.<br>Example:<br>`[<br> {<br> "key": "timeout_error",<br> "value": 5<br> },<br> {<br> "key": "unexpected_http_status_code",<br> "value": 10<br> }<br>]`<br>In this example there are 15 endpoint requests. 5 of which failed with `timeout_error` and 10 with `unexpected_http_status_code` errors. |
| `ENDPOINT_REQUEST_ERROR_RATE`<br>Flow endpoint request error rate. | Ratio between endpoint request errors and endpoint request count for a given period of time. Single value.<br>Example:<br>`[<br> {<br> "key": "value",<br> "value": 0.24<br> }<br>]`<br>In this example there is a ratio of 0.24, which means that 24% of the endpoint requests have failed. |
| `ENDPOINT_REQUEST_LATENCY_SECONDS_CEIL`<br>Flow endpoint latency in seconds. | Endpoint request latencies grouped into 10 categories, each representing value in seconds. The last category is for request latency of 10+ seconds.<br>The time is rounded up to the nearest second. For example, if a request takes 1.1 seconds, it falls into the 2nd category, representing latency of 2 seconds.<br>Example:<br>`[<br> {<br> "key": "1",<br> "value": 410<br> },<br> {<br> "key": "3",<br> "value": 61<br> },<br> {<br> "key": "10",<br> "value": 2<br> },<br> {<br> "key": "10+",<br> "value": 33<br> }<br>]`<br>In this example, there are a total of 16 endpoint requests:<br>410 requests executed with latency less than 1 second;61 request executed with latency between 2 and 3 seconds;2 requests executed with latency between 9 and 10 seconds;33 requests executed with latency more than 10 seconds. |
| `ENDPOINT_AVAILABILITY`<br>Flow endpoint request error rate. | We run a periodical availability check for a flow endpoint starting from `data_api_version` 3.0. This metric records results of this check for a given period of time.<br>Example:<br>`[<br> {<br> "key": "succeeded",<br> "value": 10<br> },<br> {<br> "key": "failed",<br> "value": 5<br> }<br>]`<br>In this example there are 15 availability check results for a given period of time. 10 times the check has succeeded and 5 times failed. |

## Variables Required for API Calls

The following variables are required in these API calls.

| Key | Value |
| --- | --- |
| Base-URL | https://graph.facebook.com/v16.0 |
| User-Access-Token | This can be retrieved by copying the *Temporary access token* from your app which expires in 24 hours.<br>Alternatively, you can generate a [System User Access Token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens). |
| Flow-ID | ID of the flow you want to get metrics for. |

## API endpoints

### Querying metric data points

This endpoint allows you to retrive a particular metric data points for a specified time period and granularity.

**Sample Request**

```curl
curl '{Base-URL}/{Flow-ID}?fields=metric.name(ENDPOINT_REQUEST_ERROR).granularity(day).since(2024-01-28).until(2024-01-30)'
--header 'Authorization: Bearer {ACCESS-TOKEN}'
```

| Parameter | Description | Required |
| --- | --- | --- |
| `name`string | Metric name. See [available metrics](https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/reference/metrics_api#available_metrics). | ✓ |
| `granularity`string | Time granularity, value being one of:<br>`DAY` - values are segmented by days`HOUR` - values are segmented by hours`LIFETIME` - values for the entire period | ✓ |
| `since`string: YYYY-MM-DD | Start of the time period. If not specified, the oldest allowed date will be used.<br>Oldest allowed date depends on the specified time granularity:<br>`DAY` - 90 days from the current date`HOUR` - 30 days from the current date |  |
| `until`string: YYYY-MM-DD | End of the time period. If not specified, the current date will be used. |  |

**Sample Response**

```json
{
  "id": "<Flow-ID>"
  "metric": {
    "granularity": "DAY",
    "name": "ENDPOINT_REQUEST_ERROR",
    "data_points": [
      {
        "timestamp": "2024-01-28T08:00:00+0000",
        "data": [
          {
            "key": "timeout_error",
             "value": 5
          }
        ]
      },
      {
        "timestamp": "2024-01-29T08:00:00+0000",
        "data": [
          {
            "key": "unexpected_http_status_code",
            "value": 12
          }
        ]
      }
    ]
  }
}
```

| Field | Description |
| --- | --- |
| `id`string | The unique ID of the flow. |
| `metric`object | Metric response object. |
| `metric.granularity`string | Requested time granularity. |
| `metric.name`string | Requested metric name. |
| `metric.data_points`array of objects | A list of metric data points. |
| `metric.data_points.timestamp`string: datetime in ISO 8601 format | Timestamp of the begining of the data point interval. |
| `metric.data_points.data`array of key-value objects | Metric specific data object. See [available metrics](https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/reference/metrics_api#available_metrics) for details. |
