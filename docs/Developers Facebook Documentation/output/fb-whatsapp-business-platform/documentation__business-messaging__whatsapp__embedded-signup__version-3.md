# Version 3 | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/version-3_

---

# Version 3

Updated: Dec 11, 2025

We are introducing versioning cadence to Embedded Signup that will align with Graph API. v3 will be released on May 29th for all partners to adopt, which will include the following changes.

## Business customers can now complete the flow without a phone number

Previously in v2, you would always be required to register a verified phone number (unless partners enabled the bypass phone numbers flow) to complete the flow. You can now complete the flow with statuses like verified, unverified, or no phone number at all.
You can either go through Embedded Signup again, go on WhatsApp manager, or the partner can utilize [API calls to verify the number](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/registering-phone-numbers).

To determine the status of the phone number, visit the documentation on session info logging.

## Session Info Logging is automatically enabled

All partners who are on v3 will have session info logging enabled automatically. Partners will still have to add an event listener on the same window of Embedded Signup to process the incoming information.

## Adding the `features` property in the configuration

You can now utilize the features property to enable a range of features in Embedded Signup. The property allows you to add multiple features instead of just one in the featureType property from v2.

### v3 request syntax

```html
// Launch method and callback registration
const launchWhatsAppSignup = () => {
  FB.login(fbLoginCallback, {
    config_id: '<CONFIGURATION_ID>', // your configuration ID goes here
    response_type: 'code',
    override_default_response_type: true,
    extras: {
  version: 'v3'
  setup: {},
  features: [<FEATURE_NAME>],
      featureType: '<FEATURE_TYPE>'
    }
}
```

| Placeholder | Description | Example |
| --- | --- | --- |
| `<FEATURE_NAME>` | Name of feature to enable in ES configuration.<br>Note: You can leave the value blank to follow the default flow.<br>Values can be:<br>`app_only_install` — Allows partners to only access WABAs via API using a [business token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens).`marketing_messages_lite` — Enables the MM API for WhatsApp onboarding flow. | `{<br> features: [<br> {<br> name: 'marketing_messages_lite'<br> }<br> ]<br>}` |
| `<FEATURE_TYPE>` | Name of feature types to enable in ES configuration.<br>Value can only be `whatsapp_business_app_onboarding`, which enables the WhatsApp Business App phone number onboarding custom flow. | `whatsapp_business_app_onboarding` |

## Removal of multiple `featuretype` options in the ES Configuration

In [v2](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/versions#version-2), business customers enabling a custom flow would be required to complete the embedded sign up multiple times depending on the number of featureTypes added to the configuration.

### Removing `only_waba_sharing`

The [bypass phone number screen flow](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/bypass-phone-addition) allows for a streamlined onboarding process where the WABA is shared without the need to go through the phone number setup steps. This flow will no longer be supported in v3. If you want to use the flow, use v2.

### Removing `marketing_messages_lite`

Marketing Messages API for WhatsApp will still be supported through the features argument. If you would still like to use the flow, update your configuration to the following.

### Removing `coexistence`

To launch the WhatsApp Business App Onboarding flow, partners will have to use `whatsapp_business_app_onboarding` instead of `coexistence`.

## Embedded Signup Pre-Filled will no longer skip screens.

Partners will still be able to pre-fill business information in Embedded Signup, but the business customer will not have the option to bypass any screens in the flow. For partners who would still like to use the flow, you should stick to using v2.

## Measurement Partners must remain on v2

Please note that Measurement product onboarding will only be supported on v2 for the time being. Continuing to support Measurement partners is important and will be supported in a future version.
