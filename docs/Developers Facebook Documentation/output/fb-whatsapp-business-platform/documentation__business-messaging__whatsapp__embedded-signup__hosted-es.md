# Hosted Embedded Signup | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/hosted-es_

---

# Hosted Embedded Signup

Updated: Nov 4, 2025

If you don’t want to implement Embedded Signup by adding JavaScript code to your website or customer portal, you can instead use a link that, when clicked, displays a web page describing onboarding steps, and a button that launches the Embedded Signup flow:

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/557247008_1487309905743315_2332288243528054136_n.png?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=VXRtmYicTcAQ7kNvwG_xQxF&_nc_oc=AdrRT-5h1w0RfFzxKlM5IYVaJ9IErPKpGxUezG_QhkkHsVusI70-GZJDGKHbs8QNkYI&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=gkKxk7UF-jx7o4o7rBV0KA&_nc_ss=7b20f&oh=00_Af7KIUgXB06nB2r0ERiknA1zjcsxBFhr_llsDvBftrqnEQ&oe=6A1C198A)

## Limitations

Hosted Embedded Signup (“Hosted ES”) can only be used to onboard business customers to Cloud API, and the flow cannot be customized.

## Requirements

- You must have completed the steps to become a Solution Partner or Tech Provider.
- If your app is for messaging, it must be able to send messages, manage templates, and have a properly configured production webhook endpoint.
- Your app must be subscribed to the [account_update](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/account_update) webhook.
- Solution Partners must have a line of credit.

You will also need:

- Your [system token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens) .
- Your app secret.

## Step 1: Create a Facebook Login for Business configuration

If you don’t already have a Facebook Login for Business configuration, you must create one. A Facebook Login for Business configuration defines which permissions to request, and what additional information to collect, from business customers who access Embedded Signup.

Navigate to **Facebook Login for Business** > **Configurations** and click the **+ Create configuration** button to access the configuration flow.

Use a name that will help you differentiate this configuration from any others you may create in the future. When completing the flow, be sure to select the WhatsApp Embedded Signup login variation:

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/556678416_1155934729723662_8909215200649973782_n.png?_nc_cat=101&ccb=1-7&_nc_sid=e280be&_nc_ohc=NL0ZTpV4O1QQ7kNvwGv5wHA&_nc_oc=AdomMPkrFfTSRwu7sxYaqy42ZbgSRfKJY8M9oD5zwGjuBFFeNR_19AH-gCMRTYiN6_k&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=gkKxk7UF-jx7o4o7rBV0KA&_nc_ss=7b20f&oh=00_Af5GIaQGUSx4wrgaO335L7KiiBONkBFeUx8w9LNuPqVnpQ&oe=6A1C1028)

When choosing assets and permissions, select only those assets and permissions that you will actually need from your business customers.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/556838067_777912301525569_1334774809437446260_n.png?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=koUBC2RnTV8Q7kNvwFhuOIj&_nc_oc=AdoZl3kGTvtWvbwutQhjIYVNWFCATyeJjFb06dXWxsf95RDNu0ST6YtgDywHIMOlQt4&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=gkKxk7UF-jx7o4o7rBV0KA&_nc_ss=7b20f&oh=00_Af79XkOn_MJaR4sjDE8VWANDVuqrJO8XysDBgD0xPr4a1Q&oe=6A1C2321)

For example, if you select the **Catalogs** asset but don’t actually need access to customer catalogs, your customers will likely abandon the flow at the catalog selection screen and ask you for clarification.

## Step 2: Get the Hosted ES URL

Navigate to the **WhatsApp** > **Quickstart** panel and click the **View onboarding** button.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/556820792_1873904266492750_8998264804748617024_n.png?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=spbOHUjCPkUQ7kNvwGiYscg&_nc_oc=AdrbV5cGM45le3rJMR4WXdMeiAHcizzWCrQ386Kvh7txP9xuNM11LKwx7YS4elwYhs8&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=gkKxk7UF-jx7o4o7rBV0KA&_nc_ss=7b20f&oh=00_Af5vG4TT7UdfQeiaU_GqHxgUXH3jqtBmEw3DS-6jQv7ziQ&oe=6A1C14E9)

Locate the **Zero integration onboarding** card. The URL displayed in the card is the onboarding page URL:

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/556828984_1430417581383742_4223219994357738350_n.png?_nc_cat=101&ccb=1-7&_nc_sid=e280be&_nc_ohc=PlQ1m44ops0Q7kNvwGIK4aO&_nc_oc=Adr62Ly2ycTdcgVUNnjlGh_CSywW6RsPfb3gXB0YBdy07shDDCoL4VQmEX3P83Pkxl0&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=gkKxk7UF-jx7o4o7rBV0KA&_nc_ss=7b20f&oh=00_Af4pp8Ap7VcIhE_33NKAwQ9TLZm9wlHiFAsIgyBIHm1BZA&oe=6A1C2F6B)

Click the **Copy button** to copy the URL to your clipboard. Map this URL to a button on your website or customer portal that, when clicked, opens the URL in a new browser window.

To see what this looks like, you can load the URL in a new browser window or tab, or click the blue “new window” icon, which does the same thing.

This onboarding page looks like this:

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/557247008_1487309905743315_2332288243528054136_n.png?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=VXRtmYicTcAQ7kNvwG_xQxF&_nc_oc=AdrRT-5h1w0RfFzxKlM5IYVaJ9IErPKpGxUezG_QhkkHsVusI70-GZJDGKHbs8QNkYI&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=gkKxk7UF-jx7o4o7rBV0KA&_nc_ss=7b20f&oh=00_Af7KIUgXB06nB2r0ERiknA1zjcsxBFhr_llsDvBftrqnEQ&oe=6A1C198A)

Click the **Get started** button. This is the flow that business customers who click the button on your website or customer portal will see. Complete the flow if you wish.

## Step 3: Capture customer asset IDs

When a business customer completes the flow, an [account_update](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/account_update) webhook is triggered with `event` set to `PARTNER_ADDED`. Capture the customer’s WhatsApp Business Account ID and business portfolio ID from the webhook payload.

## Step 4: Generate an HMAC-SHA256 hash

Generate an HMAC-SHA256 hash of your app secret and system token.

### Bash example for Linux and macOS

```html
echo -n "<SYSTEM_TOKEN>" | openssl dgst -sha256 -hmac "<APP_SECRET>"
```

- `<SYSTEM_TOKEN>` — Your system token.
- `<APP_SECRET>` — Your app secret ( [**App Dashboard**](https://developers.facebook.com/apps) > **App settings** > **Basic** )

## Step 5: Get a business token

Use the [System User Access Tokens API](https://developers.facebook.com/documentation/ads-commerce/marketing-api/reference/business/system_user_access_tokens) to get and capture the customer’s [business token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens). (Target the customer’s business portfolio ID, not yours).

### Request syntax

```html
curl 'https://graph.facebook.com/<API_VERSION>/<BUSINESS_PORTFOLIO_ID>/system_user_access_tokens' \
-H 'Content-Type: application/x-www-form-urlencoded' \
-H 'Authorization: Bearer <SYSTEM_TOKEN>' \
-d 'appsecret_proof=<APPSECRET_PROOF>' \
-d 'fetch_only=true'
```

- `<API_VERSION>` — API version.
- `<APPSECRET_PROOF>` — HMAC-SHA256 hash of your app secret and system token.
- `<BUSINESS_PORTFOLIO_ID>` — Business customer’s business portfolio ID.
- `<SYSTEM_TOKEN>` — Your system token.

### Response syntax

Upon success:

```html
{
  "access_token": "<BUSINESS_TOKEN>"
}
```

- `<BUSINESS_TOKEN>` — The business customer’s business token.

## Step 6: Get the customer’s business phone number ID

Use the [Phone Numbers API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/phone-number-management-api) to get and capture the business customer’s business phone number ID.

### Request syntax

```html
curl 'https://graph.facebook.com/<API_VERSION>/<WHATSAPP_BUSINESS_ACCOUNT_ID>/phone_numbers' \
-H 'Authorization: Bearer <BUSINESS_TOKEN>'
```

- `<API_VERSION>` — API version.
- `<BUSINESS_TOKEN>` — Business customer’s business token.
- `<WABA_ID>` — Business customer’s WhatsApp Business Account ID.

### Response syntax

```html
{
  "data": [
    {
      "verified_name": "<VERIFIED_NAME>",
      "code_verification_status": "<CODE_VERIFICATION_STATUS>",
      "display_phone_number": "<DISPLAY_PHONE_NUMBER>",
      "quality_rating": "<QUALITY_RATING>",
      "platform_type": "<PLATFORM_TYPE>",
      "throughput": {
        "level": "<THROUGHPUT_LEVEL>"
      },
      "last_onboarded_time": "<LAST_ONBOARDED_TIME>",
      "webhook_configuration": {
        "application": "<WEBHOOK_CALLBACK_URL>"
      },
      "id": "<BUSINESS_PHONE_NUMBER_ID>"
    }
  ]
}
```

- `<BUSINESS_PHONE_NUMBER_ID>` — Business phone number ID.
- `<CODE_VERIFICATION_STATUS>` — Business phone number verification status.
- `<DISPLAY_PHONE_NUMBER>` — Business display phone number.
- `<LAST_ONBOARDED_TIME>` — Unix timestamp indicating when the number was added the business customer’s WhatsApp Business Account (essentially, when the customer successfully completed the flow.)
- `<PLATFORM_TYPE>` — Platform.
- `<QUALITY_RATING>` — Business phone number quality rating.
- `<THROUGHPUT_LEVEL>` — Throughput level.
- `<VERIFIED_NAME>` — Business phone number verified name.
- `<WEBHOOK_CALLBACK_URL>` — Webhook callback URL associated with the number.

## Step 7: Onboard the customer

Onboard the business customer by completing the steps in the appropriate onboarding guide below:

- [Onboarding business customers as a Tech Provider or Tech Partner](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-customers-as-a-tech-provider) (skip step 1)
- [Onboarding business customers as a Solution Partner](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-customers-as-a-solution-partner) (skip step 1)
