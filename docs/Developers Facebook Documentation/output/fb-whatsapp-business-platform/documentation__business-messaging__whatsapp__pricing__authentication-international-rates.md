# Authentication-international rates | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/authentication-international-rates_

---

# Authentication-international rates

Updated: Dec 12, 2025

Specific countries have an **authentication-international** rate in our [rate cards](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing#rate-cards). If you send an authentication template message to a WhatsApp user whose country calling code is for a country that has an authentication-international rate, the delivered message will be billed the country’s authentication–international rate if:

- your business is [eligible](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/authentication-international-rates#eligibility) for authentication-international rates
- your business is based in another country (see [Primary Business Location](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/authentication-international-rates#primary-business-location) )
- the message was delivered on or after your [start time](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/authentication-international-rates#start-times) for that country

For example, if your business is based in Indonesia and you send an authentication template message to a WhatsApp user who has a +62 (Indonesia) country calling code, and the message is delivered, you will not be billed the authentication-international rate since you are based in the same country as the user. If your business is based in India, however, you will be billed the authentication-international rate, if you meet all of the criteria above.

See [Examples](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/authentication-international-rates#examples) for additional example scenarios.

Status [messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/status) webhooks that include pricing details and [pricing analytics](https://developers.facebook.com/documentation/business-messaging/whatsapp/analytics#pricing-analytics) will indicate if a message or set of messages were billed the authentication-international rate.

## Eligibility

If your business sends more than 750K messages outside of customer service windows in a moving 30-day period, across all of your WhatsApp Business Accounts, with unique WhatsApp users whose country calling codes are for a country that has an authentication-international rate, it will be deemed eligible for authentication-international rates.

Once deemed eligible, we will set your [start times](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/authentication-international-rates#start-times) 30 days out for each country that has an authentication-international rate. In addition, we will attempt to determine your [primary business location](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/authentication-international-rates#primary-business-location) using publicly-available information.

We will then send you an [eligibility email](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/authentication-international-rates#eligibility-email) that includes these start times and the country that we set as your primary business location (if we were able to determine the country). This provides you with 30 days notice before authentication-international rates apply. [Webhooks](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/authentication-international-rates#webhooks) will also be triggered that include your start times and your primary business location (if we set it).

Note that eligibility is permanent. Once your business is deemed eligible, all authentication template messages sent on or after your start time will be charged the authentication-international rate in markets where authorization-international rates apply.

## Countries with authentication-international rates

The following countries have authentication-international rates:

- Egypt
- India
- Indonesia
- Malaysia
- Nigeria
- Pakistan
- Saudi Arabia
- South Africa
- United Arab Emirates

Please see [Rate cards](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing#rate-cards) for more details about the rates.

## Start times

Start times are business- and country-specific timestamps. They indicate when newly-delivered authentication template messages are subject to authentication-international rates. Authentication template messages sent by your business and delivered to WhatsApp users in these countries **on or after these dates** only will be charged authentication-international rates.

Start times are set when your business is first deemed eligible for authentication-international rates, and are 30 days from your eligibility date, so you will always have 30-days notice before the authentication-international rate applies.

Start times are included in your [eligibility email](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/authentication-international-rates#eligibility-email) and [webhooks](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/authentication-international-rates#webhooks). You can also get these times by requesting the `auth_international_rate_eligibility` field on any of your business’s WhatsApp Business Accounts:

### Request

```html
curl 'https://graph.facebook.com/<API_VERSION>/<WABA_ID>?fields=auth_international_rate_eligibility' \
-H 'Authorization: <ACCESS_TOKEN>'
```

### Request parameters

| Placeholder | Description | Example value |
| --- | --- | --- |
| `<ACCESS_TOKEN>`<br>*String* | **Required.**<br>[System token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens) or [business token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens). | `EAAA...` |
| `<API_VERSION>`<br>*String* | **Optional.**<br>Graph API version. | v25.0 |
| `<WABA_ID>`*String* | **Required.**<br>WhatsApp Business Account ID. | `102290129340398` |

### Response

Upon success:

```html
{
  "id": "<WABA_ID>",
  "auth_international_rate_eligibility": {
    "start_time": <START_TIME>,
    "exception_countries": [
      <EXCEPTION_COUNTRY>,
      <EXCEPTION_COUNTRY>,
      ...
    ]
  }
}
```

### Response parameters

| Placeholder | Description | Example value |
| --- | --- | --- |
| `<WABA_ID>` | WhatsApp Business Account (WABA) ID. | `102290129340398` |
| `<START_TIME>` | Unix timestamp indicating start time for all countries with authentication-international pricing for which you do not have an [exception](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/authentication-international-rates#exception-countries). | `1732057507` |
| `<EXCEPTION_COUNTRY>` | A unique object describing a country that has an exception start time. See [exception country](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/authentication-international-rates#exception-countries).<br>For most WhatsApp Business Accounts, the `exception_countries` array will be empty. | `{<br>"country_code": "ID",<br>"start_time": 1742450707<br>}` |

## Primary business location

Your primary business location is the country where your business is based. It will appear in the Business Manager under the **Primary Business Location** field starting May 1, 2024, if we are able to determine where your business is based using publicly-available information.

The following publicly-available information is used to determine where your business is based:

- Where your business may be publicly-traded and listed
- Your business’s corporate structure (where a parent or may be based or publicly-traded)

We will attempt to determine where your business is based when:

- It is deemed [eligible](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/authentication-international-rates#eligibility) for authentication-international rates
- You [edit your primary business location](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/authentication-international-rates#set-or-edit-your-primary-business-location) using the Business Manager.

This process can take up to 3 business days. The outcome of this determination can be:

- **Verified** — We determined where your business is based and set your primary business location to this country (which also triggers a webhook).
- **Need more information** — We require more information in order to make a determination.
- **Rejected** — We disagreed with the country you designated in the Business Manager (if you used it to edit the **Primary Business Location** field)

You will be notified of the outcome in your initial [eligibility email](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/authentication-international-rates#eligibility-email), or in a separate email if you used the Business Manager to edit your location.

If rejected or if we need more information, or if you disagree with the country we determined to be the primary business location, you can use the Business Manager to edit your location.

Note that if your primary business location status is not verified but you are past your start time for a given country, any authentication messages that you send to a WhatsApp user in that country will be billed the authentication-international rate.

### Set or edit your primary business location

To set or edit your primary business location:

1. [Navigate to Business Settings by clicking here](https://business.facebook.com/settings/info?edit_pbl=true)
2. Select the country of the business’s primary location of operation from the dropdown, or enter it in the text field. Note that this is the location where your business has its headquarters and maintains its bookkeeping records.
3. Click **Next**
4. Answer the questions on the screen. These answers will help Meta verify your primary business location.
5. Click **Next**
6. Click **Submit for review**

*Note: You won’t be able to make any changes while your verification is under review.*

### Primary business location status

The **Primary Business Location** field in the Business Manager will also display a status:

- **Verified** — We have verified your business’s primary location.
- **Pending verification** — We are in the process of determining your business’s primary location.
- **Rejected** — We disagreed with the country you designated, based on publicly available information and what you included when you edited your location. You can manually edit your location again and include different information as part of your submission.

### Get your location via API

You can use the API to see if your business’s primary business location is set by requesting the `primary_business_location` field on your WhatsApp Business Account (WABA):

Request

```html
curl 'https://graph.facebook.com/<API_VERSION>/<WABA_ID>?fields=primary_business_location' \
-H 'Authorization: Bearer <ACCESS_TOKEN>'
```

### Response:

Upon success:

```html
{
  "id": "<WABA_ID>",
  "primary_business_location": "<COUNTRY_CODE>"
}
```

- `<WABA_ID>` — WhatsApp Business Account ID.
- `<COUNTRY_CODE>` — Two-character country code indicating the country where we have determined the business to be based.

## Eligibility email

By sending authentication messages over WhatsApp, you acknowledge and agree that when your business is deemed eligible for authentication-international rates, an email will be sent to all of the email addresses associated with the admins of your accounts, and all third parties that your WhatsApp Business Accounts have been shared with (e.g. admins of Solution Partners that have access to your WhatsApp Business Accounts), to alert them that the threshold of eligibility has been reached.

The email will include:

- Your exact [start times](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/authentication-international-rates#start-times) for each country that has an authentication-international rate.
- The country that we set as your [primary business location](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/authentication-international-rates#primary-business-location) .

## Exception countries

Authentication-international rates for applicable countries will begin on the same date, unless otherwise specified in your eligibility email, the `exception_countries` array in [eligibility webhooks](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/authentication-international-rates#eligibility-webhook), or the `exception_countries` array returned when [requesting](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/authentication-international-rates#request) the `auth_international_rate_eligibility` field on your WhatsApp Business Account (WABA).

You will always be charged the domestic rate for your primary business location, even if it appears in the either `exception_countries` array.

### Example Scenario

In the following examples, assume this scenario:

- there are three countries, identified by three fictitious country codes: A, B, and C
- countries A and B have authentication-international rates
- country C does not have an authentication-international rate
- the business portfolio has a WABA with ID 12345

Requesting the `auth_international_rate_eligibility` field on WABA 12345 returns:

```json
{
  "id": "12345",
  "auth_international_rate_eligibility": {
    "start_time": 1717225200, // Indicates country A start time: June 1, 2024
    "exception_countries": [
      {
        "country_code": "B",
        "start_time": 1719817200 // Indicates country B start time: July 1, 2024
      }
    ]
  }
}
```

Country C is not represented in the response because it does not have an authentication-international rate.

### Scenario 1

The business’s primary business location is country C.

- The authentication-international rate applies for country A on June 1, 2024.
- The authentication-international rate applies for country B on July 1, 2024.

### Scenario 2

The business’s primary business location is country B.

- The authentication-international rate applies for country A on June 1, 2024.

The authentication-international rate for country B does not apply because the business’s primary business location is also country B.

## Webhooks

### Eligibility webhook

An `account_update` webhook will be triggered if your business is deemed eligible for international rates. The webhook will include start times for each country that has an authentication-international rate.

Please see [Rate cards](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing#rate-cards) for the list of countries with authentication-international rates.

```html
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "<WABA_ID>",
      "time": <WEBHOOK_SENT_TIMESTAMP>,
      "changes": [
        {
          "field": "account_update",
          "value": {
            "auth_international_rate_eligibility": {
              "exception_countries": [
                {
                  "country_code": "<EXCEPTION_COUNTRY_CODE>",
                  "start_time": <EXCEPTION_START_TIME>
                }
              ],
              "start_time": <START_TIME>
            },
            "event": "AUTH_INTL_PRICE_ELIGIBILITY_UPDATE"
          }
        }
      ]
    }
  ]
}
```

- `<WABA_ID>` — WhatsApp Business Account ID.
- `<WEBHOOK_SENT_TIMESTAMP>` — Unix timestamp indicating when the webhook was sent.
- `<EXCEPTION_COUNTRY_CODE>` — Two-letter country code (e.g. `ID` for Indonesia) of the country with a start time exception.
- `<EXCEPTION_START_TIME>` — Unix timestamp indicating authentication-international rate start time for the exception country.
- `<START_TIME_INDIA>` — Unix timestamp indicating start time for all countries with authentication-international pricing **for which you do not have an exception** .

### Primary business location update webhook

Subscribe to the `account_update` webhook to be notified when the business’s [primary business location](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/authentication-international-rates#primary-business-location) is set. If we are able to determine the country where your business is based, we will set your location to that country and trigger an `account_update` webhook with the country’s two-character country code assigned to the `BUSINESS_PRIMARY_LOCATION_COUNTRY_UPDATE` property.

```json
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "<WABA_ID>",
      "time": <TIMESTAMP>,
      "changes": [
        {
          "field": "account_update",
          "value": {
            "country": "<COUNTRY_CODE>",
            "event": "BUSINESS_PRIMARY_LOCATION_COUNTRY_UPDATE"
          }
        }
      ]
    }
  ]
}
```

- `<WABA_ID>` — WhatsApp Business Account ID.
- `<TIMESTAMP>` — Unix timestamp indicating when the webhook was sent.
- `<COUNTRY_CODE>` — ISO 3166-1 alpha-2 country code, indicating the country where we have determined the business to be based.

### Pricing in messages webhook

If an authentication template message is billed the authentication-international rate, the `pricing` object in status [messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/status) webhooks will have `category` set to `authentication_international`.

```json
"pricing": {
"billable": true,
"pricing_model": "PMP",
"type": "regular",
"category": "authentication_international"
}
```

## Examples

A business with an **Indonesia** [primary business location](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/authentication-international-rates#primary-business-location) send an authentication template message to a WhatsApp user:

| User location | Is business eligible? | Is on/after start time? | Rate billed |
| --- | --- | --- | --- |
| Indonesia | - | - | Authentication |
| India | No | - | Authentication |
| India | Yes | No | Authentication |
| India | Yes | Yes | Authentication-International |

A business with an India primary business location sends an authentication template message to a WhatsApp user:

| User location | Is business eligible? | Is on/after start time? | Rate billed |
| --- | --- | --- | --- |
| India | - | - | Authentication |
| Indonesia | No | - | Authentication |
| Indonesia | Yes | No | Authentication |
| Indonesia | Yes | Yes | Authentication-International |

A business with a primary business location that does not have an authentication-international rate sends an authentication template message to a WhatsApp user:

| User location | Is business eligible? | Is on/after start time? | Rate billed |
| --- | --- | --- | --- |
| Indonesia | No | - | Authentication |
| Indonesia | Yes | No | Authentication |
| Indonesia | Yes | Yes | Authentication-International |
| India | No | - | Authentication |
| India | Yes | No | Authentication |
| India | Yes | Yes | Authentication-International |
