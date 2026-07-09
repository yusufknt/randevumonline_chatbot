# Display names | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/display-names_

---

# Display names

Updated: Mar 24, 2026

You must provide a display name when [registering](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/registration) a business phone number. The display name appears in your business phone number’s WhatsApp profile:

![WhatsApp business profile showing the display name](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/507127951_698062976515521_2852142619234157074_n.png?_nc_cat=110&ccb=1-7&_nc_sid=e280be&_nc_ohc=E92egQx3u-UQ7kNvwFquDA2&_nc_oc=Ado-KxWy4dovGVgP9erLWJ4gSxLiJPM0HfOe_IvTql7mdG34ebKEtFTrr9XX7sqlI_g&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=IOzNcm316duhuNftwie4yg&_nc_ss=7b20f&oh=00_Af6NI0itx0m7lGm2wRxzm0YSz9HX4qyEdvkozngSUAraHg&oe=6A1C0629)

It can also appear at the top of **individual chat** threads and the **chat list** if your business phone number is approved via [display name verification](https://developers.facebook.com/documentation/business-messaging/whatsapp/display-names#display-name-verification). Note that if a WhatsApp user edits your profile name in the WhatsApp client, the name they set will appear instead.

## Display name guidelines

See our [Display name guidelines for the WhatsApp Business Platform](https://www.facebook.com/business/help/757569725593362) Help Center article for naming guidelines.

## Display name verification

When you reach a [higher messaging limit](https://developers.facebook.com/documentation/business-messaging/whatsapp/messaging-limits), your business phone number’s display name automatically undergoes verification based on the [display name guidelines](https://www.facebook.com/business/help/757569725593362). When the process completes, a [phone_number_name_update](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/phone_number_name_update) webhook and Meta Business Suite notification are triggered.

If your display name is approved, the webhook has `decision` set to `APPROVED`, and the `name_status` field on your business phone number is set to `APPROVED`.

If your display name is rejected, the webhook has `decision` set to `REJECTED`, and the `name_status` field on your business phone number is set to `DECLINED`. Review the [display name guidelines](https://www.facebook.com/business/help/757569725593362) and [edit your display name](https://www.facebook.com/business/help/378834799515077) accordingly, or file an appeal via [Developer Support](https://developers.facebook.com/documentation/business-messaging/whatsapp/support#developer-support) or [Enterprise Developer Support](https://developers.facebook.com/documentation/business-messaging/whatsapp/support#enterprise-developer-support).

## View display name in WhatsApp Manager

Your business phone number’s display name appears in the **Name** column in the [WhatsApp Manager](https://business.facebook.com/latest/whatsapp_manager/) > **Account tools** > **Phone numbers** panel.

## Get display name and display name status via API

Request the `verified_name` and `name_status` field on your WhatsApp Business Phone Number ID to get its display name and display name status. See the [WhatsApp Business Phone Number API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/whatsapp-business-account-phone-number-api#get-version-phone-number-id) reference for a list of returnable values and their meanings.

The `verified_name` value doesn’t indicate whether the display name is approved. It represents the display name string that undergoes verification when eligible. The `name_status` field indicates its approval status.

### Example request

```curl
curl 'https://graph.facebook.com/v25.0/106540352242922?fields=verified_name%2Cname_status' \
-H 'Authorization: Bearer EAAJB...'
```

### Example response

Upon success:

```json
{
  "verified_name": "Lucky Shrub",
  "name_status": "APPROVED",
  "id": "106540352242922"
}
```

## Update display names

You can change a display name 10 times per 30-day period. After the display name change is approved, you have 14 days to [re-register the phone number](https://developers.facebook.com/documentation/business-messaging/whatsapp/display-names#re-register-after-display-name-approval). If the 14-day window expires without re-registration, you must submit the display name for review again.

**Note:** If your business phone number has [Official Business Account](https://developers.facebook.com/documentation/business-messaging/whatsapp/official-business-accounts) status, contact [direct support](https://developers.facebook.com/docs/whatsapp/contact-support#contacting-support) to change your display name.

### Update display name via WhatsApp Manager

To update your display name via WhatsApp Manager:

1. Navigate to [WhatsApp Manager](https://business.facebook.com/latest/whatsapp_manager/) > **Account tools** > **Phone numbers** .
2. Select your business phone number.
3. Click the **Profile** tab.
4. In the **Display name** section, click the **Edit** button and complete the flow.

Once you complete the flow, your display name undergoes [display name verification](https://developers.facebook.com/documentation/business-messaging/whatsapp/display-names#display-name-verification) again. After the display name is approved, you must [re-register the phone number](https://developers.facebook.com/documentation/business-messaging/whatsapp/display-names#re-register-after-display-name-approval). Re-registering before approval has no effect.

This information is also available in our [How to change your WhatsApp Business display name](https://www.facebook.com/business/help/378834799515077) Help Center article.

### Update display name via API

Use the [WhatsApp Business Phone Number API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/whatsapp-business-account-phone-number-api#post-version-phone-number-id)`new_display_name` field to update your display name via API.

Example request

```curl
curl -X POST 'https://graph.facebook.com/v25.0/106540352242922?new_display_name=Lucky%20Shrub' \
-H 'Authorization: Bearer EAAJB...'
```

Example response

Upon success:

```json
{
  "success": true
}
```

Upon success, your display name undergoes [display name verification](https://developers.facebook.com/documentation/business-messaging/whatsapp/display-names#display-name-verification). To check the verification status, request the `new_display_name` and `new_name_status` fields on your business phone number ID:

Example request

```curl
curl 'https://graph.facebook.com/v25.0/106540352242922?fields=new_display_name,new_name_status' \
-H 'Authorization: Bearer EAAJB...'
```

Example response

Upon success:

```json
{
  "new_display_name": "New Lucky Shrub",
  "new_name_status": "PENDING_REVIEW",
  "id": "106540352242922"
}
```

When your updated display name is approved, your business phone number’s `verified_name` and `name_status` fields update to reflect your new display name and name status, and [phone_number_name_update](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/phone_number_name_update) webhooks are triggered. You must then [re-register the phone number](https://developers.facebook.com/documentation/business-messaging/whatsapp/display-names#re-register-after-display-name-approval). Re-registering before approval has no effect.

## Re-register after display name approval

After updating your display name via [WhatsApp Manager](https://developers.facebook.com/documentation/business-messaging/whatsapp/display-names#update-display-name-via-whatsapp-manager) or [API](https://developers.facebook.com/documentation/business-messaging/whatsapp/display-names#update-display-name-via-api), you must re-register your phone number to solidify the new display name with WhatsApp servers.

1. Wait for the [phone_number_name_update](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/phone_number_name_update) webhook with `decision` set to `APPROVED` .
2. Call `POST /<PHONE_NUMBER_ID>/register` to re-register the phone number. See [Register a Business Phone Number](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/registration#register) for endpoint details.

**Important:** Wait for the display name change to be approved before re-registering. Re-registering before approval has no effect.

You can re-register programmatically via the API. You do **not** need to send the business through [Embedded Signup](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/overview) again.

### Example request

```curl
curl 'https://graph.facebook.com/v25.0/106540352242922/register' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "messaging_product": "whatsapp",
  "pin": "212834"
}'
```

### Example response

Upon success:

```json
{
  "success": true
}
```

## Learn more

The following Help Center articles provide additional information about display names.

- [About WhatsApp Business display name](https://www.facebook.com/business/help/338047025165344)
- [How to change your WhatsApp Business display name](https://www.facebook.com/business/help/378834799515077)
