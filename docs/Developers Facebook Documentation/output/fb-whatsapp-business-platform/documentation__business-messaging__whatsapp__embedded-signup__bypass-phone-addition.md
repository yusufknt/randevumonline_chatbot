# Bypassing the phone number addition screen | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/bypass-phone-addition_

---

# Bypassing the phone number addition screen

Updated: Nov 14, 2025

This document describes how to customize Embedded Signup to bypass the [phone number addition screen](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/default-flow#phone-number-addition-screen) (shown below) and [phone number verification screen](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/default-flow#phone-number-verification-screen).

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/464076811_858112679765152_5952854678961541773_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=JTcrQ_8fY44Q7kNvwELwPqM&_nc_oc=Adq0nw1md23RB25_fzz_51oHY0Sefmkgd00C8ZJV6KV5vnZAzLKoCI5hM0UXwpxuQ8w&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=5KlrBKFDSakZHL075IIYUQ&_nc_ss=7b20f&oh=00_Af4f_ZdZaO0Ho659fLTSQXQ1siQvQZeAd-NI6WHjwqznPw&oe=6A1C1FCE)

If you don’t want your business customers to have to enter or choose a business phone number in the phone number addition screen, you can customize Embedded Signup to skip the screen entirely. However, after a customer successfully completes the customized flow, you must [programmatically create and register their business phone number](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/registering-phone-numbers), or build a UI in your app that allows them to do this.

## Enabling the feature

To enable this feature, set `featureType` to `only_waba_sharing` in the [launch method and callback registration](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/implementation#launch-method-and-callback-registration) portion of the Embedded Signup code:

```js
// Launch method and callback registration
const launchWhatsAppSignup = () => {
  FB.login(fbLoginCallback, {
    config_id: '<CONFIGURATION_ID>', // your configuration ID goes here
    response_type: 'code',
    override_default_response_type: true,
    extras: {
      setup: {},
      featureType: 'only_waba_sharing', // set to only_waba_sharing
      sessionInfoVersion: '3',
    }
  });
}
```

When a business customer successfully completes the flow, the [session logging message event](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/implementation#session-logging-message-event-listener) will have `event` set to `FINISH_ONLY_WABA`:

```html
{
  data: {
    phone_number_id: "<CUSTOMER_BUSINESS_PHONE_NUMBER_ID>",
    waba_id: "<CUSTOMER_WABA_ID>"
  },
  type: "WA_EMBEDDED_SIGNUP",
  event: "FINISH_ONLY_WABA",
  version: 3
}
```
