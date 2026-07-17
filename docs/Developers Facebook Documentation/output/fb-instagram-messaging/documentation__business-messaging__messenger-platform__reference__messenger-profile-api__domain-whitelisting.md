# whitelisted_domains Reference | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/messenger-profile-api/domain-whitelisting_

---

# whitelisted_domains Reference

Updated: Jul 1, 2025

Messenger Profile API

`whitelisted_domains` is a property of the Messenger Profile API. For information on retrieving, setting, updating, and deleting `whitelisted_domains`, see the [Messenger Profile API Reference](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/messenger-profile-api).

The `whitelisted_domains` property of your bot’s Messenger profile specifies a list of third-party domains that are accessible in the Messenger webview for use with the [Messenger Extensions SDK](https://developers.facebook.com/documentation/business-messaging/messenger-platform/webview), and the [Checkbox Plugin](https://developers.facebook.com/documentation/business-messaging/messenger-platform/discovery).

## Requirements

To set or update the domain whitelist you must have the ‘Administrator’ role for the Page associated with the bot.

Domain Name and HTTPS Required

Domains must meet the following requirements to be whitelisted:

- Served over HTTPS
- Use a fully qualified domain name, such as https://www.messenger.com/. IP addresses and localhost are not supported for whitelisting.

## Whitelisting in Page Settings

In addition to using the Messenger Profile API, Page admins may also update their domain whitelist in Page settings by doing the following:

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/24233971_162986520866800_981524615547322368_n.png?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=DzYc3u73dAYQ7kNvwHu-T-Q&_nc_oc=AdqkrxnBlOd0NG4W5Ad9Uc4dac3_siTfFEMkB7wWERRFIKEnegO0G_6FioTX2La4ysw&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=WW44vgMd-i4pjNNrwBCLFQ&_nc_ss=7b20f&oh=00_Af4ajh7Uxj1NDTyL-Ocmy0i2NT5a2RRARXFSqwDFSmaF4Q&oe=6A1C2186)

1. Click **Settings** at the top of your Page
2. Click **Advance Messaging** on the left
3. Edit whitelisted domains for your page in the **Whitelisted Domains** section

## `whitelisted_domains` Format

```curl
{
  "whitelisted_domains":[
    "<WHITELISTED_DOMAIN>",
    "<WHITELISTED_DOMAIN>",
    ...
  ]
}
```

## Properties

| Property | Type | Description |
| --- | --- | --- |
| `whitelisted_domains` | Array<String> | A list of domains being used. All domains must be valid. Up to 50 domains allowed. |

## Rate Limit

Calls to the Messenger Profile API are limited to 10 API calls per 10 minute interval. This rate limit is enforced per Page.
