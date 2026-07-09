# App-Only Install | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/app-only-install_

---

# App-Only Install

Updated: Nov 4, 2025

You can configure Embedded Signup so that only [business tokens](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens) can be used to access assets owned by customers onboarded via the flow. This approach offers enhanced security by reducing risk associated with [system tokens](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens), flexibility in simplifying onboarding for other Meta assets, and scalability to support a larger number of onboardings. By using a granular token, you can also reduce the negative impact in case of a compromised token, making it a more secure and efficient way to manage your business customer assets.

Note that App-Only Install can’t be used to [onboard WhatsApp Business app users](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users).

## Enabling the feature in Embedded Signup v3

To enable this feature, set `features` to `app_only_install` in the Embedded Signup configuration.

```html
{
  "config_id": "<CONFIGURATION_ID>",
  "response_type": "code",
  "override_default_response_type": true,
  "extras": {
    "version": "v3",
    "features": [
      {
        "name": "app_only_install"
      }
    ]
  }
}
```

To enable this feature along with a [Multi-Partner Solution](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/multi-partner-solutions):

```html
{
  "config_id": "<CONFIG_ID>",
  "response_type": "code",
  "override_default_response_type": true,
  "extras": {
    "version": "v3",
    "features": [
      {
        "name": "app_only_install"
      }
    ],
    "setup": {
      "solutionID": "<SOLUTION_ID>"
    }
  }
}
```

When a business customer successfully completes the flow, the [session logging message event](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/implementation#session-logging-message-event-listener) will have `event` set to `FINISH_GRANT_ONLY_API_ACCESS`:

```html
{
  data: {
    phone_number_id: "<CUSTOMER_BUSINESS_PHONE_NUMBER_ID>",
    waba_id: "<CUSTOMER_WABA_ID>",
    business_id: "<CUSTOMER_BUSINESS_ID>",
  },
  type: "WA_EMBEDDED_SIGNUP",
  event: "FINISH_GRANT_ONLY_API_ACCESS",
}
```

When a business customer successfully completes the flow, an **account_update** webhook is triggered with `event` set to `PARTNER_APP_INSTALLED`.

```html
{
  "entry": [
    {
      "id": "<PARTNER_BUSINESS_ID_1>",
      "time": "<WEBHOOK_TRIGGER_TIMESTAMP>",
      "changes": [
        {
          "value": {
            "event": "PARTNER_APP_INSTALLED",
            "waba_info": {
              "waba_id": "<WABA_ID>",
              "owner_business_id": "<WABA_OWNER_BUSINESS_ID>",
              "partner_app_id": "<APP_ID>",
              "solution_id": "<SOLUTION_ID>",
              "solution_partner_business_ids": [
                "<PARTNER_BUSINESS_ID_1>",
                "<PARTNER_BUSINESS_ID_2>"
              ]
            }
          }
        }
      ],
      "field": "account_update",
      "object": "whatsapp_business_account"
    }
  ]
}
```

If an onboarded business customer uses [Meta Business Suite](https://business.facebook.com) to uninstall/remove the app, an **account_update** webhook is triggered with `event` set to `PARTNER_APP_UNINSTALLED`.

```html
{
  "entry": [
    {
      "id": "<PARTNER_BUSINESS_ID>",
      "time": "<WEBHOOK_TRIGGER_TIMESTAMP>",
      "changes": [
        {
          "value": {
            "event": "PARTNER_APP_UNINSTALLED"
          },
          "field": "account_update"
        }
      ]
    }
  ],
  "object": "whatsapp_business_account"
}
```

You can use the [System User Access Tokens API](https://developers.facebook.com/documentation/ads-commerce/marketing-api/reference/business/system_user_access_tokens) to get an onboarded business customer’s business token.

```html
curl -i -X POST "https://graph.facebook.com/v22.0/<CUSTOMER_BUSINESS_PORTFOLIO_ID>/system_user_access_tokens
  ?appsecret_proof=<APPSECRET_PROOF_HASH>
  &access_token=<ACCESS_TOKEN>
  &system_user_id=<SYSTEM_USER_ID>
  &fetch_only=true"
```
