# WhatsApp for Business Platform Status | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/support/api-status-page_

---

# WhatsApp for Business Platform Status

Updated: Nov 17, 2025

Meta provides a [WhatsApp Business API Status page](https://status.fb.com/whatsapp-business-api) that reports real-time service status updates for the WhatsApp Business Platform. This includes detailed Cloud API [availability](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/api-status-page#availability) and [latency](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/api-status-page#latency) metrics for better observability of the platform. You can monitor this page to check whether the services are currently experiencing disruptions or outages. The status page also reports when the services have no known issues.

If you are having issues with the platform, it is important to check this page first to determine if the problem is on our end or if it is your business implementation, hardware, or your network. If we report no known issues with the services and you are experiencing issues then contact [Direct Support](https://developers.facebook.com/documentation/business-messaging/whatsapp/support#enterprise-developer-support) to determine and resolve your issues.

To stay up to date on the platform’s performance we recommend subscribing to the status page through the **RSS Feed** button on the WhatsApp Business API Status Page itself. See [RSS Feed](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/api-status-page#rss-feed) for more information.

The status page provides the following features:

- Up to date detailed status report for WhatsApp for Business Platform services
- History of past service disruptions or outages
- Cloud API specific availability and latency metrics
- Link to our RSS feed that you can use for instant notifications

These features are described in more detail below.

## Overview

The WhatsApp Business Platform Status page main functionality is to report real-time status information for the services that drive WhatsApp for Business Platform and are important to you. These services are:

1. **Cloud API**
2. **Cloud API - Localized Storage**
3. **WhatsApp Business Account Management**
4. **Embedded Signup**
5. **Marketing Messages API for WhatsApp**

The status page provides the following features:

- Up to date detailed status report for WhatsApp for Business Platform services
- History of past service disruptions or outages
- Cloud API specific availability and latency metrics
- Link to our RSS feed that you can use for instant notifications

These features are described in more detail below.

### Status indicators

The WhatsApp Business Platform Status page provides status indicators for each service. Since these services run independently, there is a chance that one service could be functioning normally, while the other is experiencing a minor or major disruption. The following table lists each color coded indicator based on the service status:

| Status Indicator | Status Image | Description |
| --- | --- | --- |
| Green Checkmark | ![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/559906217_1339318154593502_1924487776241144230_n.jpg?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=0fzVXiLgMYAQ7kNvwE-LYSE&_nc_oc=Adr6kU1kSI7KO1d-3tHQZn6_yaJ8rSEb-fseFCVgE5ywxjkDAiUnEoW3q4N3bllZ2ZU&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=LdYFs89DZifzP5h2t0ta_A&_nc_ss=7b20f&oh=00_Af78ZFDWd4zZqlG7aKdme6-fSo9h4YipP5uJmvH0SMY0dw&oe=6A1C0799) | The service is up, running, and has no known issues or a recent issue has been resolved. |
| Yellow Triangle | ![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/560932715_1339318177926833_7203738193856039359_n.jpg?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=XpQqQIHLVOAQ7kNvwF8VBor&_nc_oc=Adroy-MAnZXxZ0rPqN8I9U3VoLZmOXHzUVNVK3fO9-D3hVfUtsyDXSjsv7X1stimsyg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=LdYFs89DZifzP5h2t0ta_A&_nc_ss=7b20f&oh=00_Af64LEyHHkgNfFKHHDil_KBxqgPfIgiFrv1SapmpxVE9Lg&oe=6A1C1BA8) | The service is in recovery from disruptions or the service is experiencing some disruptions. |
| Red Stop-sign | ![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/560013461_1339318191260165_1427748895640689159_n.jpg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=RudQZBv1Hd8Q7kNvwF56ht5&_nc_oc=Adp6znSnwt93yQmP5HBgWdK4Dtf1HiMMIO-5zcax92dOVpa42YgOL55Ld2Pm7jrPYso&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=LdYFs89DZifzP5h2t0ta_A&_nc_ss=7b20f&oh=00_Af6Z6OHzIDGHlaFFDoE5hc0ueZFtt8dCqnYb7bbIDugVvg&oe=6A1C0C4E) | The service is currently down or experiencing major disruptions. |

You can select the down arrow to see more information about the disruption. If the status has a green checkmark (Resolved), selecting the down arrow provides information about the date, time, and severity of the most recent disruption in the past seven days. If the service has not had a minor or major disruption in the past seven days, the message will reflect this.

### Page controls

Cloud API

Select the **Cloud API** service drop down arrow to view more information, such as the timestamp on the last service check and, if applicable, more details about the status. Information about this service includes, for example, issues related to media uploads and downloads, as well as messaging rates.

Detailed Cloud API availability and latency metrics are also available for better observability of the platform. Please note that due to processing, availability numbers for the prior month will be updated by the 10th business day of the new calendar month. This is relevant only for the previous month section.

Cloud API - localized storage

Select the **Cloud API - Localized Storage** service drop down arrow to view more information, such as the timestamp on the last service check and, if applicable, more details about the status. Information about this service includes, for example, issues related to storing or retrieving messages from an in-country storage database. Phone numbers using Localized Storage are not included in Cloud API availability and latency metrics, as a result of using different storage infrastructure. Instead, alerts on variations from platform targets that impact Localized Storage numbers will be surfaced separately here.

WhatsApp Business Account Management

Select the **WhatsApp Business Account Management** service drop down arrow to view more information, such as the timestamp on the last service check and, if applicable, more details about the status.

Embedded Signup

Select the **Embedded Signup** service drop down arrow to view more information, such as the timestamp on the last service check and, if applicable, more details about the status. Information about this service includes, for example, issues related to creating Business Manager accounts and WhatsApp business accounts.

Marketing Messages API for WhatsApp

Select the **Marketing Messages API for WhatsApp** service drop down arrow to view more information, such as the timestamp on the last service check and, if applicable, more details about the status. Information about this service includes, for example, issues related to media uploads and downloads, as well as messaging rates.

Detailed Marketing Messages API for WhatsApp availability and latency metrics are also available for better observability of the platform. Please note that due to processing, availability numbers for the prior month will be updated by the 10th business day of the new calendar month. This is relevant only for the previous month section.

View history

Click this button to see the history from the past seven days of any issues that occurred with both services. If there were no issues, the status will state that there was none.

RSS feed

Click this button to subscribe to the RSS feed for WhatsApp Business Platform service status. You’ll need to use your browser or third-party application to subscribe to the RSS feed.

## Availability

Cloud API is considered available unless it has been unable to send or receive messages for at least 10 consecutive minutes.

```json
Availability =  100 * (A - B)/A
```

Where:

- A = the total number of minutes in the calendar month
- B = the total number of minutes that WhatsApp Business Platform (Cloud API) is not available to send or receive messages, as detected by WhatsApp in the calendar month

## Latency

Cloud API computes latency across inbound and outbound messages, which are defined as follows:

- **Outbound** : Time from when our servers receive a send message request from the business to when the message is ready to be transmitted to the WhatsApp user’s device from our servers.
- **Inbound** : Time from when we receive a message from a WhatsApp user to when our systems make the first attempt to send a corresponding [messages webhook](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages) to the WhatsApp Business Account’s callback URL.

The following messages and processes are excluded from latency computations:

- Time spent fetching assets (image, videos, etc.) hosted on Meta servers (assets hosted on business’s servers are excluded from computation).
- Messages held in queues when the receiver is not connected.
- Messages held in queues while awaiting spam and scam checks.
- Messages status webhooks (sent, delivered, read, etc.).
- Messages to/from businesses leveraging [local storage](https://developers.facebook.com/documentation/business-messaging/whatsapp/local-storage) .

We reserve the right to exclude messages sent from businesses that we suspect are in violation of our terms and policies from calculations.

### Latency percentiles

Cloud API exposes P90 and P99 latency percentiles. As an example, P99 latency is the 99th latency percentile; this means 99% of requests will be faster than the given latency number, and only 1% of the requests will be slower.

P90/P99 values are computed across inbound and outbound messages.

## See also

- [WhatsApp Business API Status page](https://metastatus.com/whatsapp-business-api)
- [Support](https://developers.facebook.com/documentation/business-messaging/whatsapp/support)
- [Reliability FAQs](https://developers.facebook.com/documentation/business-messaging/whatsapp/support#reliability-faqs)
