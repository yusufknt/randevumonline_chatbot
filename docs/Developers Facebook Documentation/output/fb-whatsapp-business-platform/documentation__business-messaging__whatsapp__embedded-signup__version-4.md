# Version 4 | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/version-4_

---

# Version 4

Updated: Dec 12, 2025

Release date: October 8, 2025. Check back soon for updates on additional supported products.

To upgrade to the v4 experience: You need to create a new [Facebook Login for Business Configuration](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/implementation/#step-2-create-a-facebook-login-for-business-configuration), and select your desired products. Selecting the products will automatically set you to v4.

See [screenshots](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/version-4#using-the-facebook-login-for-business-configuration-to-get-started-with-v4) below.

## Overview of v4 changes

- Simplified onboarding experience for businesses: You can onboard businesses to more business messaging in a single flow ([see supported products](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/version-4#supported-products)).Asset selection, business information, and permissions are each consolidated onto a single page.Asset admins can share assets from other business portfolios.Phone numbers are auto-linked to Facebook Pages when onboarding to ads that click to WhatsApp via the Marketing API.Value proposition and Terms of Service are clearly presented.
- The [Facebook Login for Business Configuration](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/version-4#using-the-facebook-login-for-business-configuration-to-get-started-with-v4) is used to define which products to add into your onboarding flow.

## Learn more

- [v4 - Cloud API flow](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/default-flow)

## Supported products

v4 supports additional business messaging products, ensuring businesses to set up and manage multiple communication channels from a single platform:

- **Conversions API (WhatsApp, Instagram, Messenger)** : Track and optimize messaging interactions by selecting the messaging platform you want to monitor, enabling enhanced measurement and optimization.
- **Click to WhatsApp Ads (CTWA)** : Create ads that direct users to initiate WhatsApp conversations with your business.
- **Click to Messenger Ads (CTM)** : Run advertising campaigns that start conversations with users on Facebook Messenger.
- **Click to Direct Ads (CTD)** : Launch Instagram ad campaigns that drive users to direct messaging conversations on Instagram Direct.

## All other supported products

v4 continues to support existing business messaging products, allowing businesses to seamlessly manage their established communication channels.

- **Cloud API** : Integrate and manage WhatsApp messaging at scale, enabling businesses to send and receive messages, automate workflows, and access advanced messaging features.
- **Marketing Messages API for WhatsApp** : Utilize to manage optimized marketing messaging , providing tools for message analytics, and enhanced customer engagement.
- **WhatsApp Business app user onboarding** : Onboarding WhatsApp Business app users continues to be supported through the [`feature_type` parameter](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users#step-2--customize-embedded-signup) .
- **Partner-led Business Verification (PLBV) support** : [PLBV](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/partner-led-business-verification) enables partners to verify business after onboarding via Embedded Signup. If you are considering this option, ensure you are an approved Select Solution or Premier Solution Partner, and [approved for access](https://www.facebook.com/business/help/1091073752691122) .
- **Automatic Events API** : [Automatic Events API](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/automatic-events-api) notifies your application about key events that occur through Click-to-WhatsApp ads.

## Use the Facebook Login for Business Configuration to get started with v4

v4 enables you to easily set up and change which products you want to include in your onboarding flow:

Step 1: Navigate to [App Dashboard](https://developers.facebook.com/apps) > **Facebook Login for Business** > **Configurations** to create a new configuration.

Step 2: Select **Embedded Signup** as the login variation.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/588554056_1899889040926861_7735493385836726995_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=uMekehLGT4cQ7kNvwFXvz31&_nc_oc=Adp3ME9wE63wLZjPnzppcIzBMRSzHCL0lAolQF_9UxOqIfZAwGTJD4X6HbHJLQY5T-M&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=5ZyJoT7HyN13Ou6mYcHX0g&_nc_ss=7b20f&oh=00_Af72x1qXtQQ2eFYJvWDgSTugLkfeqefU-vVVUCAL-HGM1A&oe=6A1C2836)

Step 3: Select which products you want to include in your onboarding flow. Selecting more than one product is optional.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/589045267_1817285795585343_2603642295217157227_n.png?_nc_cat=106&ccb=1-7&_nc_sid=e280be&_nc_ohc=kApQJqDT1esQ7kNvwE-z_Ly&_nc_oc=AdqaE4rg4rL2lTTgW5eLMZztAu8TTYzYLP4Gzm2pGVPu4f9Gc1neLqrINd4-6VGZPyw&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=5ZyJoT7HyN13Ou6mYcHX0g&_nc_ss=7b20f&oh=00_Af7EKttQs4M7vasvPLtvZNN7LvgyEof_RV3oaPiDcx9QSg&oe=6A1C087D)

Step 4: Copy the configuration id to use inside the Facebook Login SDK.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/588573995_1434645688667306_4273697828818050269_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=uZGtNobNJtEQ7kNvwGacqY_&_nc_oc=AdrswDV77BqP4_wirGoQftpCVgMZ9wN2EDFJnRhEX2xm2J2SMj4hC2X_KO_-QIEvXpA&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=5ZyJoT7HyN13Ou6mYcHX0g&_nc_ss=7b20f&oh=00_Af7nj300bujmi698RqsISoQr1XItsTBR33lDNCrkNgQiOA&oe=6A1C19C4)

## Required assets and permissions

When selecting products for v4, the flow will automatically select all necessary permissions and assets. You will need advanced access for all permissions automatically selected in the flow. If needed, you can select additional assets and permissions. The table below is a reference on what assets and permissions you need depending on what product you would like to offer.

| Product | Required assets | Required permissions (Advanced Access) |
| --- | --- | --- |
| [Cloud API](https://developers.facebook.com/documentation/business-messaging/whatsapp/about-the-platform#whatsapp-cloud-api) | WhatsApp Business accounts | whatsapp_business_management<br>whatsapp_business_messaging |
| [Click to WhatsApp (CTWA on Marketing API)](https://developers.facebook.com/documentation/ads-commerce/marketing-api/ad-creative/messaging-ads/click-to-whatsapp) | WhatsApp Business accounts<br>Facebook Pages<br>Ad accounts | ads_read<br>ads_management<br>pages_manage_ads<br>pages_read_engagement<br>pages_show_list |
| [Click to Messenger (CTM on MAPI)](https://developers.facebook.com/documentation/ads-commerce/marketing-api/ad-creative/messaging-ads/click-to-messenger) | Facebook Pages<br>Ad accounts | ads_management<br>pages_manage_ads<br>pages_read_engagement<br>pages_show_list |
| [Click to Instagram (CTD on MAPI)](https://developers.facebook.com/documentation/ads-commerce/marketing-api/ad-creative/messaging-ads/click-to-instagram) | Facebook Pages<br>Ad accounts<br>Instagram accounts | ads_management<br>pages_manage_ads<br>pages_read_engagement<br>pages_show_list |
| [Marketing Messages API for WhatsApp](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/overview) | WhatsApp Business accounts | whatsapp_business_management<br>whatsapp_business_messaging |
| [Conversions API for CTWA](https://developers.facebook.com/documentation/ads-commerce/conversions-api/business-messaging#ads-that-click-to-whatsapp) | WhatsApp Business accounts<br>Pixels | whatsapp_business_manage_events |
| [Conversions API for CTM](https://developers.facebook.com/documentation/ads-commerce/conversions-api/business-messaging#ads-that-click-to-messenger) | Facebook Pages<br>Ad accounts<br>Pixels | page_events |
| [Conversions API for CTD](https://developers.facebook.com/documentation/ads-commerce/conversions-api/business-messaging#ads-that-click-to-instagram-direct) | Facebook Pages<br>Ad accounts<br>Instagram accounts<br>Pixels | instagram_manage_events |
