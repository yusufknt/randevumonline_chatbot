# Versions | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/versions_

---

# Versions

Updated: Dec 11, 2025

The latest Embedded Signup Version is: `v4`

This guide provides an overview on versioning in Embedded Signup. The versioning cadence will align with Graph API. The versions are not
exclusive, partners can gradually roll out a new version of ES to reduce risk. The Embedded Signup version is determined inside of the **extras object** of the implementation code.

**Note: The refreshed UI, currently available in the public preview, will be rolled out to all versions of Embedded Signup in early September.**

## Available ES Versions

| Version | Date Introduced | Available Until |
| --- | --- | --- |
| [v4](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/version-4) | October 8th, 2025 | TBD |
| [v3-public-preview](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/version-3-public-preview) | August 14, 2025 | October, 2026 |
| [v2-public-preview](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/version-2-public-preview) | August 14, 2025 | October, 2026 |
| [v3](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/version-3) | May 29, 2025 | October, 2026 |
| v2 | January 2023 | October, 2026 |

## Overview of feature availability

| Version | Feature types | Features | Completion State | Prefilled Info | [Session Info Logging](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/implementation#session-logging-message-event-listener) | Products (via login config) |
| --- | --- | --- | --- | --- | --- | --- |
| `v4` | `whatsapp_business_app_onboarding` | `app_only_install` | Users can finish with a verified, unverified or no phone number | Can fill business information, no screens will be skipped. | Sent back for all flows | Marketing Messages API for WhatsApp(MM API for WhatsApp)<br>Click to WhatsApp Ads (CTWA)<br>Conversions API (WhatsApp) |
| `v3-public-preview` | `whatsapp_business_app_onboarding` | `app_only_install`<br>`marketing_messages_lite` | Users can finish with a verified, unverified or no phone number | Can fill business information, no screens will be skipped. | Sent back for all flows | Not supported |
| `v2-public-preview` | `only_waba_sharing`<br>`whatsapp_business_app_onboarding`<br>`marketing_messages_lite` | `app_only_install`<br>`marketing_messages_lite` | Users will finish with a verified phone number | Can fill business information, no screens will be skipped. | Sent back for all flows | Not supported |
| `v3` | `whatsapp_business_app_onboarding` | `app_only_install`<br>`marketing_messages_lite` | Users can finish with a verified, unverified or no phone number | Can fill business information, no screens will be skipped. | Sent back for all flows | Not supported |
| `v2` | `only_waba_sharing`<br>`whatsapp_business_app_onboarding`<br>`marketing_messages_lite` | `marketing_messages_lite` | Users will finish with a verified phone number | Can fill business information and skip screens | Partners are required to add a `sessionInfoVersion` to receive the callback | Not supported |

## Version 4

**Released:** October 8, 2025 | [Detailed changes](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/version-4)

**Login Configuration**

**Extras Configuration**

```js
extras: {} // The extras object is purposely empty for v4.
```

To use v4: You need to create a new [Facebook Login for Business Configuration](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/implementation/#step-2-create-a-facebook-login-for-business-configuration), and select your desired products. Selecting the products will automatically set you to v4.

## Version 3 Public Preview

**Released:** August 14, 2025 | **Available until:** October, 2026 | [Detailed changes](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/version-3-public-preview)

**Extras Configuration**

```js
extras: {
    setup: "<SETUP_DATA>",
    features: [
      {
        name: "<FEATURE_NAME>"
      }
    ],
    featureType: "<FEATURE_TYPE>",
    version: "<VERSION>"
}
```

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<PREFILL_DATA>` | Prefilled business data to inject data into Embedded Signup. | `{<br> "business": {<br> "name": "Jaspers Market"<br> }<br>}` |
| `<FEATURE_NAME>` | Indicates a flow or feature to enable. | **Possible Values:**<br>`app_only_install` — Allows partners to access WABAs via API using a granular token (BISU), without creating a (SUAT)<br>`marketing_messages_lite` — Enables the [Marketing Messages API for WhatsApp onboarding](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/overview) flow. |
| `<FEATURE_TYPE>` | Indicates a flow or feature to enable. | **Possible Values:**<br>`whatsapp_business_app_onboarding` — Enables the [WhatsApp Business App phone number onboarding](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users) custom flow.<br>Leave **blank** to enable the default onboarding flow. |
| `<VERSION>` | Indicates Embedded Signup version flow. | **Possible Values:**<br>`v3-public-preview`,<br>`v2-public-preview`,<br>`v3`,<br>`v2` |

## Version 2 Public Preview

**Released:** August 14, 2025 | **Available until:** October, 2026 | [Detailed changes](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/version-2-public-preview)

**Extras Configuration**

```js
extras: {
    setup: "<SETUP_DATA>",
    features: [
      {
        name: "<FEATURE_NAME>"
      }
    ],
    featureType: "<FEATURE_TYPE>",
    sessionInfoVersion: "<SESSION_INFO_VERSION>"
    version: "<VERSION>"
}
```

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<PREFILL_DATA>` | Prefilled business data to inject data into Embedded Signup. | `{<br> "business": {<br> "name": "Jaspers Market"<br> }<br>}` |
| `<FEATURE_NAME>` | Indicates a flow or feature to enable. | **Possible Values:**<br>`app_only_install` — Allows partners to access WABAs via API using a granular token (BISU), without creating a (SUAT)<br>`marketing_messages_lite` — Enables the [MM API for WhatsApp onboarding](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/overview) flow. |
| `<FEATURE_TYPE>` | Indicates a flow or feature to enable. | **Possible Values:**<br>`whatsapp_business_app_onboarding` — Enables the [WhatsApp Business App phone number onboarding](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users) custom flow.<br>`only_waba_sharing` - Enables the [WhatsApp Business App phone number onboarding](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users) custom flow. Will **NOT** show the new consolidated UI.<br>`marketing_messages_lite` - Enables the [MM API for WhatsApp onboarding](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/overview) custom flow. Will **NOT** show the new consolidated UI.<br>Leave **blank** to enable the default onboarding flow. |
| `<SESSION_INFO_VERSION>` | Indicates the returned session payload. | **Possible Values:**<br>`3` |
| `<VERSION>` | Indicates Embedded Signup version flow. | **Possible Values:**<br>`v3-public-preview`,<br>`v2-public-preview`,<br>`v3`,<br>`v2` |

## Version 3

| Column 1 | Column 2 | Column 3 | Column 4 |
| --- | --- | --- | --- |
| **Released:**<br>May 29, 2025 | **Available until:**<br>October, 2026 | [Blog post](https://developers.facebook.com/blog/post/2025/05/29/introducing-graph-api-v23-and-marketing-api-v23/) | [Detailed changes](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/version-3) |

**Extras Configuration**

```js
extras: {
    setup: "<SETUP_DATA>",
    features: [
      {
        name: "<FEATURE_NAME>"
      }
    ],
    featureType: "<FEATURE_TYPE>",
    version: "v3"
}
```

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<PREFILL_DATA>` | Prefilled business data to inject data into Embedded Signup. | `{<br> "business": {<br> "name": "Jaspers Market"<br> }<br>}` |
| `<FEATURE_NAME>` | Indicates a flow or feature to enable. | **Possible Values:**<br>`app_only_install` — Allows partners to access WABAs via API using a granular token (BISU), without creating a (SUAT)<br>`marketing_messages_lite` — Enables the [MM API for WhatsApp onboarding](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/overview) flow. |
| `<FEATURE_TYPE>` | Indicates a flow or feature to enable. | **Possible Values:**<br>`whatsapp_business_app_onboarding` — Enables the [WhatsApp Business App phone number onboarding](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users) custom flow.<br>Leave **blank** to enable the default onboarding flow. |
| `<VERSION>` | Indicates Embedded Signup version flow. | **Possible Values:**<br>`v3-public-preview`,<br>`v2-public-preview`,<br>`v3`,<br>`v2` |

## Version 2

| Column 1 | Column 2 |
| --- | --- |
| **Released:**<br>January 2023 | **Available until:**<br>October, 2026 |

**Extras Configuration**

```js
extras: {
    setup: "<SETUP_DATA>",
    features: [
      {
        name: "<FEATURE_NAME>"
      }
    ],
    featureType: "<FEATURE_TYPE>",
    sessionInfoVersion: "<SESSION_INFO_VERSION>",
}
```

Head to the [pre-fill screens page](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/pre-filled-data#injecting-data) to see how to inject customer business data into Embedded Signup.

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<PREFILL_DATA>` | Prefilled business data to inject data into Embedded Signup. | `{<br> "business": {<br> "name": "Jaspers Market"<br> }<br>}` |
| `<FEATURE_NAME>` | Indicates a flow or feature to enable. | **Possible Values:**<br>`app_only_install` — Allows partners to access WABAs via API using a granular token (BISU), without creating a (SUAT)<br>`marketing_messages_lite` — Enables the [MM API for WhatsApp onboarding](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/overview) flow. |
| `<FEATURE_TYPE>` | Indicates a flow or feature to enable. | **Possible Values:**<br>`whatsapp_business_app_onboarding` — Enables the [WhatsApp Business App phone number onboarding](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users) custom flow.<br>`only_waba_sharing` - Enables the [WhatsApp Business App phone number onboarding](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users) custom flow.<br>`marketing_messages_lite` - Enables the [MM API for WhatsApp onboarding](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/overview) custom flow.<br>Leave **blank** to enable the default onboarding flow. |
| `<SESSION_INFO_VERSION>` | Indicates the returned session payload. | **Possible Values:**<br>`3` |
| `<VERSION>` | Indicates Embedded Signup version flow. | **Possible Values:**<br>`v3-public-preview`,<br>`v2-public-preview`,<br>`v3`,<br>`v2` |
