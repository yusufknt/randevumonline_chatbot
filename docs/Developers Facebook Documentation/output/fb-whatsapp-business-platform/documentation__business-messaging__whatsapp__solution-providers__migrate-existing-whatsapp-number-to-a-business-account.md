# Migrate an existing WhatsApp Number to a Business Account | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/migrate-existing-whatsapp-number-to-a-business-account_

---

# Migrate an existing WhatsApp Number to a Business Account

Updated: Oct 31, 2025

To use an existing WhatsApp Messenger phone number with Cloud API, you must first delete your WhatsApp Messenger account.

To use an existing WhatsApp Business app phone number with Cloud API, you must either delete your account, or onboard to the platform [using a solution provider](https://business.facebook.com/messaging/partner-showcase) who supports [business app number onboarding](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users). **Remember to back up your chat history from the WhatsApp Business App. These are guides on how to do so for [Android](https://faq.whatsapp.com/744445782709185/?helpref=faq_content) or [iOS](https://faq.whatsapp.com/180225246548988/).**

Note that if you delete your WhatsApp Business app phone number and then register it for use with Cloud API using the steps below, your existing messaging history will be lost, and you will be unable to use that number with the WhatsApp Business app again, unless you deregister the number from Cloud API. If you onboard via a solution provider who supports business app number onboarding, you will be able to use both the WhatsApp Business app and the solution partner’s app concurrently, and your messaging history will be preserved.

## Deleting a WhatsApp Messenger or WhatsApp Business app account

1. Open WhatsApp Messenger or WhatsApp Business app on your Android or iPhone
2. Navigate to Settings > Account
3. Select Delete my account. Messages sent to this phone number will be queued in the meantime
4. Follow the steps to delete the WhatsApp account for that phone number. It may take up to 3 minutes for the disconnected number to become available

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/53155930_1040983749443056_7137221020057862144_n.png?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=35tPbXpFKtwQ7kNvwE36YCb&_nc_oc=AdqEa3IWpOVeZ_fQAnXwuXyBj-9NZxCs3_R1lNZM6xZAhsPNOxrV3YuKIGRPFioUadM&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=PvnKoY___Mv_okBFw09g_w&_nc_ss=7b20f&oh=00_Af525utz16mq81FgJYJg78rGJJKbXMAkOOgAsBlHrdiYSQ&oe=6A1C0801)

*Account Settings*

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/53231721_413403332756635_1839237629032267776_n.png?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=tQfb3r1Vu9sQ7kNvwFDJIto&_nc_oc=AdppnBf6WNUr-IBGNVkgw17Pqhdd8U2lzsKhwj3Y2kAurQ1RVJFJ-4uLugCHoGXK8so&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=PvnKoY___Mv_okBFw09g_w&_nc_ss=7b20f&oh=00_Af4x_awjdj7vkZkJIBMePqpAlSA3if99ml-xwAGuTAEhmg&oe=6A1C1F5A)

*Delete My Account*

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/53128269_407915336420893_2688327795590823936_n.png?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=j-9ArMJt-1kQ7kNvwEVAZyZ&_nc_oc=Ado1jXn9f0Cy-T4p1bIJudGO3_A7q-9gG3SNgEl5iKBmpjlssT48FvtsjGGOrM7KX_s&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=PvnKoY___Mv_okBFw09g_w&_nc_ss=7b20f&oh=00_Af62vXBNn_5XXQfgdNdMrPFEwGcenhSyu7CLewoeLTGDKg&oe=6A1C05BF)

*Deletion Steps*

Once the number is available, follow the instructions to [Add a Phone Number](https://developers.facebook.com/documentation/business-messaging/whatsapp/get-started).
