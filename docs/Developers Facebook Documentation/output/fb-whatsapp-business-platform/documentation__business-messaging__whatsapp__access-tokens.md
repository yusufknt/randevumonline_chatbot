# Access Tokens Guide | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens_

---

# Access Tokens Guide

Updated: Apr 29, 2026

The platform supports the following access token types. The type you use depends on who will be using your application, and whether you are a [solution provider](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/overview).

- If you are a **direct developer** , meaning only you or your business will be accessing your own data, use a [System User access token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens) .
- If you are a **Tech Provider** , use a [Business Integration System User access token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens) .
- If you are a **solution partner** , use [System User access tokens](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens) to share your line of credit with newly onboarded customers, and [Business Integration System User access tokens](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens) for everything else.

## System user access tokens

System user access tokens (“system tokens”) represent you, your business, organization, or people within them. The main advantage of these tokens is that they are long-lived and can represent automated services within your business that don’t require any user input.

System tokens rely on system users. Most endpoints check if the user identified by the token has access to the queried resource. If the user doesn’t have access to the resource, the system rejects the request with error code `200`.

System users can be [admins](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#admin-system-users) or [employees](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#employee-system-users).

### Admin system users

By default, admin system users have full access to all WhatsApp Business Accounts (WABAs) and their assets owned by or shared with you or your business portfolio.

Admin system users are useful if your app needs access to all of the business portfolio’s assets, without having to manually grant business asset access to each asset whenever it is created, or shared with your business portfolio.

You can override an admin system user’s default business asset access by granting partial access on a per-WABA basis. See [Business Asset Access](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-asset-access) to learn how to set and override access.

### Employee system users

Employee system users must be granted access to individual WABAs that are owned by, or shared with, your business portfolio. If your app will only need access to a few WABAs that you own, an employee system user should be sufficient.

Once created, you must grant **Partial** or **Full**[business asset access](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-asset-access) to each WABA that the system user needs to access.

### Generate system user access tokens

To generate a system token, access the [**Business settings**](https://business.facebook.com/settings/) panel and then click **System Users**:

![Business settings panel showing System Users option](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/465045103_469826065488878_468932947489962332_n.png?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=Cim1QYvYKCQQ7kNvwEkqxiN&_nc_oc=AdqTKiuvq5z7YOtrKg9pAG8upcIkXTBDrcqPZkkAaiMCXPMDhx3hzRm5PyBtErKC1NI&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=L2fUU9oQiu55O8JzgMIEUw&_nc_ss=7b20f&oh=00_Af72z-8US4zg8leQPoEZ-ej7CENqxzTkCTI9UDq29zhBpA&oe=6A1C03FE)

Click the **+Add** button, and in the **Create system user** window that appears, enter a system user name and assign it an **Admin** or **Employee** role:

![Create system user dialog with name field and role selector](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/465150702_510049308508353_7881035250572985544_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=_JUPDl8SlZcQ7kNvwHwESX2&_nc_oc=AdoZHnzAuyjjVxIYb9cvn2VlqjSbL-AhGAdL6zxsOM5GsUzn9hhgA9eIY2slR2Ji_Go&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=L2fUU9oQiu55O8JzgMIEUw&_nc_ss=7b20f&oh=00_Af4NKwXIHt5DbRHdmmPwzXNgO1_k5IZN_hUJIrFcgJCCXA&oe=6A1C0A8E)

Once you create the admin system user, it appears in the list of system users. Click the system user’s name to display the asset assignment overlay:

![System users list showing asset assignment overlay](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/465056956_862633796067178_7287331611550335065_n.png?_nc_cat=111&ccb=1-7&_nc_sid=e280be&_nc_ohc=099LaAJJywMQ7kNvwFdmkru&_nc_oc=AdrIvJCAsCxDcbIyiUDTtlBxEVsPw32qBIknPC3nLsA2fI7DJ04L1TPOmNcTRXm-lQU&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=L2fUU9oQiu55O8JzgMIEUw&_nc_ss=7b20f&oh=00_Af4vIsa2GMWaaSzYxihcyCrdqsDSmc31HDpJmaGCXAFMpg&oe=6A1C1316)

Click the **Assign assets** button to display the **Select assets and assign permissions** window:

![Select assets and assign permissions dialog](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/465238023_523683013888319_4402098107854849013_n.png?_nc_cat=111&ccb=1-7&_nc_sid=e280be&_nc_ohc=W6eDO6MK7moQ7kNvwGFkP9q&_nc_oc=AdprKLr-VhInoVkADH3dipJFTO59712tOeCn0Cm_TZB2dvPHDff90ABHmFYpCFdLHiw&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=L2fUU9oQiu55O8JzgMIEUw&_nc_ss=7b20f&oh=00_Af45ui6niFSomBT81x4p_qXBFkinNIwPpMcV3RGIViSPPw&oe=6A1C243F)

Select your app and grant your system user the **Manage app** permission, then click the **Assign assets** button to confirm and dismiss the window.

Back in the **System Users** panel, reload the page to confirm that your system user has been granted **Full control** of your app. It may take a few minutes for the permissions to be granted, so reload the page after a few minutes if your app doesn’t appear as an assigned asset. Once the asset has been assigned, it should look like this:

![System user with full control of app displayed](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/465048557_1084025226566535_5772232306997286547_n.png?_nc_cat=111&ccb=1-7&_nc_sid=e280be&_nc_ohc=ReUB4WGc6acQ7kNvwGxdPGe&_nc_oc=AdqollxmD0QTn5ZXG7UBaiAATDbwUkw7tbLL6T241lbATio-IErkp6XHWtLj39_w4pE&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=L2fUU9oQiu55O8JzgMIEUw&_nc_ss=7b20f&oh=00_Af4UcslbBT3__NzoJi2bFbP4eVQCHgYkjdVv2g7uGcterg&oe=6A1C1998)

Once you see that your system user has been granted full control of your app, in the asset assignment overlay, click the **Generate token** button. In the window that appears, select your app, choose a token expiration preference, and assign your app these three Graph API permissions:

- `business_management`
- `whatsapp_business_management`
- `whatsapp_business_messaging`

You can search for `business` to find these permissions quickly:

![Token generation dialog showing business permissions search](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/465115001_533379429601225_2797461055613545929_n.png?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=sokjlPSKCH4Q7kNvwFciAQ0&_nc_oc=Adp20j5KNNnvIg1k-OMbvVmvsLsuPoA8dSyTtDqB2p_tOQ6ZMIr5Osnfpth8hUyik0U&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=L2fUU9oQiu55O8JzgMIEUw&_nc_ss=7b20f&oh=00_Af4wl9s4FYVYfHnq5_qIIy-FXJSbRNnvhfwF3XLARYGd5Q&oe=6A1C3059)

Click the **Generate token** button and copy the token when it appears.

## Business Integration System User access tokens

Business Integration system user access tokens (“business tokens”) are scoped to individual onboarded customers and should be used by Tech Providers and solution partners when accessing onboarded customer data.

These tokens are useful for apps that perform programmatic, automated actions on customer WABAs, without having to rely on input from an app user, or requiring future re-authentication.

To generate a Business Integration System User access token, you must implement Embedded Signup (configured with Facebook Login for Businesses) and exchange the code returned to you when a customer completes the flow.

See [Embedded Signup](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/overview) and [Business Integration System User access tokens](https://developers.facebook.com/documentation/facebook-login/facebook-login-for-business#business-integration-system-user-access-tokens) to learn more about these tokens and how to generate them.

## User access tokens

Although User access tokens are supported and can be used by all app developers, you likely will only use them when you first use the App Dashboard to [send your first test message](https://developers.facebook.com/documentation/business-messaging/whatsapp/get-started). As you develop your app, however, you most likely will switch to a System User access token (and eventually a Business System User access token, if you are a Tech Provider or a Solution Provider). This is because user access tokens expire quickly, so you will have to keep generating a new one every few hours.

There are several ways to generate a User access token:

- Access the **App Dashboard** > **WhatsApp** > **API setup** panel. This panel always generates a new User access token whenever you visit it. The token is automatically scoped to your user, since you are signed into your developer account when you access the panel.
- Use [Graph API Explorer](https://developers.facebook.com/tools/explorer) .
- Implement [Facebook Login](https://developers.facebook.com/documentation/facebook-login) .

## Use tokens in requests

When making API requests, include your token in an authorization request header, preceded by `Bearer`. For example:

```curl
curl 'https://graph.facebook.com/v18.0/102290129340398/message_templates' \
-H 'Authorization: Bearer EAAJB...' \
```

## Token format

Access tokens are opaque strings. A full token looks like this:

```
EAAJBsbCmS80BO4hZBf5xYKFaFW7kVMNxAWzIInZB7q1PuZCLiEqKh3gZDZD
```

Tokens can vary in length and their internal structure and characteristics can change over time. Do not parse, decode, or make assumptions about the format of an access token — treat it as an opaque string. Use a variable-length data type without a specific maximum size to store access tokens.

## Business asset access

After creating a system user, you must set business asset access levels. Many endpoints require the system user whose token is included in API requests to have either **Partial** or **Full** business asset access to the WABA being queried (or its assets). If the system user doesn’t have this access, these endpoints return error code `200`.

If you set a system user’s business asset access on a WABA to **Partial** access, you can further restrict access to certain assets or actions on the WABA. For example, if you have a large business and want a certain department to only have read access to a WABA’s template and business phone number data, you could create a system user for that department and set granular access to view only for that data.

To set business asset access on a WABA, follow these steps:

1. Sign into [Meta Business Suite](https://business.facebook.com) .
2. Locate your business portfolio in the dropdown menu at the top of the page and click its **Settings** (gear) icon.
3. Navigate to **Accounts** > **WhatsApp Accounts** .
4. Select the appropriate WABA.
5. Select the **WhatsApp Account Access** tab.
6. Click the **+Add people** button.
7. Select the appropriate system user and assign appropriate access levels on the WABA.

![WhatsApp Account Access tab with Add people button](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/458274092_845026414442989_6944264004016403962_n.png?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=OEfAvO2Vd_YQ7kNvwG_c3Za&_nc_oc=AdpZNMULmu2Crk7bv5wi8CCsZS_-shsbokgsuuovfxXpaVNp_ima4wtcfIuc55KbUXM&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=L2fUU9oQiu55O8JzgMIEUw&_nc_ss=7b20f&oh=00_Af5mAP6lC24upE3johGLRhrU0eK79UeKbmI5lnhfqDg7vg&oe=6A1C166E)
