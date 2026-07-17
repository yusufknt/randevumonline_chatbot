# Customizing the default flow | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/custom-flows_

---

# Customizing the default flow

Updated: Nov 14, 2025

This document provides an overview of the various ways that you can customize Embedded Signup’s default flow to present different versions of the flow to your business customers.

## Onboard WhatsApp Business app users

You can configure Embedded Signup to [allow business customers to onboard using their existing WhatsApp Business app account and phone number](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users):

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/477341352_1809983926468415_3794578338113490554_n.png?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=SWGfy-RnFc4Q7kNvwFL36xb&_nc_oc=AdquW8j2xDfh8hTx-AllSWaAlSpXuqytiw5PMmv1wkkec_pwxybzYQIYFt0Bf6iAIDY&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=nCIDloOf2yq3pEDEYYDJhQ&_nc_ss=7b20f&oh=00_Af6JHVoQQZddV4faOyIezLWSo6G7R2xnnuWkGhl_CjhEeg&oe=6A1C2ADB)

Businesses who are successfully onboarded after choosing this option will then be able to use your app to message their customers at scale, but still have the ability to send messages on a one-to-one basis using the WhatsApp Business app.

## Pre-filling screens

You can pre-fill many of Embedded Signup’s default flow screens with a business customer’s business data. [Pre-filling screens](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/pre-filled-data) can dramatically reduce the amount of input and interaction required by your customers, and shorten flow.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/465727373_1573223883300812_8312998736298536563_n.png?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=l3RkhQMGmpkQ7kNvwGt-Ifc&_nc_oc=AdqgV-Jm2YDc2L09RZko7sWuY6yY2z57rtRhiTdc-QnLoc7BpJaxuWur6VGiy6ESVY0&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=nCIDloOf2yq3pEDEYYDJhQ&_nc_ss=7b20f&oh=00_Af4mwxftf-V_JegiQUF1fL2pwDTG3FGi3pOGAbYG3DVdSQ&oe=6A1C2907)

## Bypassing phone number addition and verification

You can customize Embedded Signup to entirely [skip the phone number addition and verification screens](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/bypass-phone-addition). This can be useful if you don’t want business customers to have to enter a phone number, retrieve the verification code sent to the number, and then verify the code using the number.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/464076811_858112679765152_5952854678961541773_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=JTcrQ_8fY44Q7kNvwELwPqM&_nc_oc=Adq0nw1md23RB25_fzz_51oHY0Sefmkgd00C8ZJV6KV5vnZAzLKoCI5hM0UXwpxuQ8w&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=nCIDloOf2yq3pEDEYYDJhQ&_nc_ss=7b20f&oh=00_Af6xtDV1OLFuBU63vpTgMjKOlOIUbWIETx8xMFy5y5AbAg&oe=6A1C1FCE)

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/464106774_850690680604728_8102449662662242044_n.png?_nc_cat=106&ccb=1-7&_nc_sid=e280be&_nc_ohc=ox1zao5ISNIQ7kNvwHg1hsF&_nc_oc=AdrOe2pYoGHbUgkeA9JDgvNCuuMMoRfZ7MbBhH9FiHNbrt5jzCqf6RyW3O1eANChRFw&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=nCIDloOf2yq3pEDEYYDJhQ&_nc_ss=7b20f&oh=00_Af5bK6Adr_NWF3ga2s1NLzI4Tl7Vn_ZINca4h6twTCCR8g&oe=6A1C0F47)

## App-Only Install

[App-Only Install](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/app-only-install) is a way to configure Embedded Signup so that only business tokens can be used to access assets owned by customers onboarded via the flow. This does not affect the flow itself, only which tokens must be used.
