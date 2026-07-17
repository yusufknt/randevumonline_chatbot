# Business profiles | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/business-profiles_

---

# Business profiles

Updated: Oct 5, 2025

Your business phone number’s profile displays additional information such as address, website, and description. You can add this information when registering your phone number or update it later via WhatsApp Manager or API.

![Screenshot of a WhatsApp business profile displaying company information](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/507476070_1379105613180336_7510619276605653298_n.png?_nc_cat=106&ccb=1-7&_nc_sid=e280be&_nc_ohc=Tlq52cv9_igQ7kNvwGyDLki&_nc_oc=AdpcBpLiA9_464rmdVApOFuV6-CyxPfqJGhra88ZY2wja8Fmq1aZzNUhYtXnGU6h4eI&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=7P0UFC8BeSHQE7nDFFD0wA&_nc_ss=7b20f&oh=00_Af4IEtVc6-rdLr8RC4Bzc7_6voaYPZH2DdIArAOMzSRlrw&oe=6A1C0D1D)

## Viewing or updating your profile via WhatsApp Manager

To view or update your business profile via WhatsApp Manager:

1. Navigate to [WhatsApp Manager](https://business.facebook.com/latest/whatsapp_manager/) > **Account tools** > **Phone numbers** .
2. Select your business phone number.
3. Click the **Profile** tab to view your current profile.
4. Use the form to set new profile values.

## Getting your profile via API

Use the [WhatsApp Business Profile API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/whatsapp-business-profile-api#get-version-phone-number-id-whatsapp-business-profile) to get specific business profile fields:

### Example request

```curl
curl 'https://graph.facebook.com/v25.0/106540352242922/whatsapp_business_profile?fields=about,address,description,email,profile_picture_url,websites,vertical' \
-H 'Authorization: Bearer EAAJB...'
```

### Example response

Upon success:

```json
{
  "data": [
    {
      "about": "Succulent specialists!",
      "address": "1 Hacker Way, Menlo Park, CA 94025",
      "description": "At Lucky Shrub, we specialize in providing a...",
      "email": "lucky@luckyshrub.com",
      "profile_picture_url": "https://pps.whatsapp.net/v/t61.24...",
      "websites": [
        "https://www.luckyshrub.com/"
      ],
      "vertical": "RETAIL",
      "messaging_product": "whatsapp"
    }
  ]
}
```

## Updating your profile via API

Use the [WhatsApp Business Profile API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/whatsapp-business-profile-api#post-version-phone-number-id-whatsapp-business-profile) to update specific business profile fields:

### Example request

```curl
curl 'https://graph.facebook.com/v25.0/106540352242922/whatsapp_business_profile' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
--data-raw '
{
  "about": "Succulent specialists!",
  "address": "1 Hacker Way, Menlo Park, CA 94025",
  "description": "At Lucky Shrub, we specialize in providing a diverse range of high-quality succulents to suit your needs. From rare and exotic varieties to timeless classics, our collection has something for everyone.",
  "email": "lucky@luckyshrub.com",
  "messaging_product": "whatsapp",
  "profile_picture_handle": "4::aW...",
  "vertical": "RETAIL",
  "websites": "[\n  \"https://www.luckyshrub.com\"\n]"
}'
```

### Example response

Upon success:

```json
{
  "success": true
}
```
