# Permissions | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/permissions_

---

# Permissions

Updated: Nov 5, 2025

Platform endpoints are gated by permissions. References for each endpoint indicated which permissions it requires, but in general, you will need the following:

- [whatsapp_business_management](https://developers.facebook.com/docs/permissions#whatsapp_business_management) — needed to access metadata on your WhatsApp Business Account, template management, getting business phone numbers associated with your WABA, all analytics, and to receive webhooks notifying you of changes to your WhatsApp Business Account
- [whatsapp_business_messaging](https://developers.facebook.com/docs/permissions#whatsapp_business_messaging) — needed to send any type of message to a WhatsApp users, and to receive incoming message and message status webhooks

Depending on your business needs, you may also need these permissions:

- [business_management](https://developers.facebook.com/docs/permissions#business_management) — only needed if you need to programmatically access your business portfolio (this is rarely needed, since you can access your portfolio using [Meta Business Suite](https://business.facebook.com/) .
- [whatsapp_business_manage_events](https://developers.facebook.com/docs/permissions#whatsapp_business_manage_events) — only needed if you are sending marketing templates with [Marketing Messages API for WhatsApp](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/overview) , in conjunction with the [Conversions API](https://developers.facebook.com/documentation/ads-commerce/conversions-api) , for event tracking.
- [ads_read](https://developers.facebook.com/docs/permissions#ads_read) — only needed if you are using [Marketing Messages API for WhatsApp](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/overview) in conjunction with the [Insights API](https://developers.facebook.com/documentation/ads-commerce/marketing-api/insights) to get conversion metrics

## App Review

If you are a [solution provider](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/overview) and other businesses will be using your app to access their data, your app must undergo [App Review](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/app-review), and you must be approved for **advanced access** for any permissions your app needs. If you aren’t approved for advanced access for a given permission, your app users will be unable to grant your app that permission.

If you are a direct developer and will only be accessing your own business data, you do not need to under App Review and do not need advanced access for any permissions.

## How to get permissions

App users must grant your app individual permissions. If you are a direct developer and are using a system token, when you create a [system token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens), you must create a system user and use it to grant your app individual permissions as part of the system token creation process:

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/465115001_533379429601225_2797461055613545929_n.png?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=sokjlPSKCH4Q7kNvwFciAQ0&_nc_oc=Adp20j5KNNnvIg1k-OMbvVmvsLsuPoA8dSyTtDqB2p_tOQ6ZMIr5Osnfpth8hUyik0U&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=W6u0gWBfpLIKdOJcblPUFQ&_nc_ss=7b20f&oh=00_Af6slas1mpqvXD71CD1K-7WbjmrE-YAhaEZENAGT-FRCKg&oe=6A1C3059)

If you are a [solution provider](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/overview) using [business tokens](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens), the Embedded Signup [authorization screen](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/default-flow#authorization-screen) allows the user to grant your app permissions for which you have advanced access approval:

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/464191580_1337884324044562_8279151817864174578_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=7TEW7BzWfYMQ7kNvwEsnwi3&_nc_oc=AdqEH7RjAxX1UfNWK5uYmC3KU7Lo4HFuSZPe9hpvf9owR1d8xpPnVQrk4iyOGt4j4AM&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=W6u0gWBfpLIKdOJcblPUFQ&_nc_ss=7b20f&oh=00_Af5WqtyODik99Mg-rKBAF1D7HUGFO0INKm2OFRFpLad1-Q&oe=6A1C2597)

## Checking for granted permissions

Use the **debug_token** endpoint to see which permissions the token granter has granted to your app. Alternatively, you can use the [access token debugger](https://developers.facebook.com/tools/debug/accesstoken/) tool, which returns the same information.

### Request syntax

```html
curl 'https://graph.facebook.com/<API_VERSION>/debug_token?input_token=<ACCESS_TOKEN_TO_CHECK>' \
-H 'Authorization: Bearer <ACCESS_TOKEN>'
```

### Response syntax

Granted permissions are assigned to the `scopes` property.

```json
{
    "data": {
        "app_id": "634974688087057",
        "type": "SYSTEM_USER",
        "application": "Lucky Shrub",
        "data_access_expires_at": 0,
        "expires_at": 0,
        "is_valid": true,
        "issued_at": 1712099387,
        "scopes": [
            "whatsapp_business_management",
            "whatsapp_business_messaging"
        ],
        "granular_scopes": [
            {
                "scope": "whatsapp_business_management"
            },
            {
                "scope": "whatsapp_business_messaging"
            }
        ],
        "user_id": "104169029247128"
    }
}
```
