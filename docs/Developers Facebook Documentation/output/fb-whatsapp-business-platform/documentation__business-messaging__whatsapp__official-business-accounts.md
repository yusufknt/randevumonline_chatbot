# Official Business Accounts | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/official-business-accounts_

---

# Official Business Accounts

Updated: Apr 24, 2026

An Official Business Account (“OBA”) is a business phone number owned by a business that has been verified as an authentic business according to specific [criteria](https://developers.facebook.com/documentation/business-messaging/whatsapp/official-business-accounts#eligibility). Official Business Account business phone numbers have a blue checkmark beside their name in the contacts view.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/456954377_453386597161620_5745766558871976538_n.png?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=eil2GIWeDXEQ7kNvwE7TT4v&_nc_oc=Adr1D5SBdEqrXHMcL4HLp1ryRb7Xfxy648b5NP3KKZd4PYix_NSuh5aUcDGbR8kRfx4&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=2DLYU01YYFCuY4zR8xXl4w&_nc_ss=7b20f&oh=00_Af7_Juq-ZHRMpg1B5zqvoMcEA4rvYj7GsfNuGVrtIAmzXw&oe=6A1C34B3)

You can request OBA status for a business phone number using WhatsApp Manager or API. Once we’ve reviewed your request, you will receive a notification letting you know if your business phone has been granted OBA Number status or not. If your request is rejected, you can submit a new request after 30 days.

We do not grant OBA status to business employees, test accounts, and WhatsApp Business app phone numbers.

## Eligibility

To be eligible for OBA, the following criteria must be met:

- The business must comply with the [WhatsApp Business Messaging Policy](https://business.whatsapp.com/policy) .
- The business must be registered on the WhatsApp Business Platform for at least 30 days.
- The business portfolio that owns the number has been verified through [Business Verification](https://www.facebook.com/business/help/2058515294227817) .
- The business phone number has enabled [two-step verification](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers#two-step-verification) .
- The business phone number’s display name has been [approved](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers#display-name-verification) .

If you meet the above criteria but do not see an option to apply for OBA in [WhatsApp Manager](http://business.facebook.com/wa/manage/), please reach out to your Meta point-of-contact, Solution Provider support, or Meta Support to check if you are eligible for the application process.

**Note:** If a business phone number is not an Official Business Account (OBA), it will not appear in search results when users search for it within the WhatsApp application. However, if a user adds the number to their contacts, the display name will appear in their search results. For improved discoverability, we recommend applying for OBA status.

## Denied Requests

If your request has been denied, it means our team has reviewed your account and determined that it does not meet the eligibility requirements at this time. You must wait 30 days before submitting another request.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/457031264_766028162210302_4155505657500024802_n.png?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=qtoJ3rvwIu4Q7kNvwGJGNQn&_nc_oc=AdpMKQSigZmE-G3YViZ0RxGkV6ChEHzeq2z8ELiuaNry2C0IALBWQu7i-UNKGuTT8SQ&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=2DLYU01YYFCuY4zR8xXl4w&_nc_ss=7b20f&oh=00_Af5KwGydWHIp1EhGBGTEv8WrGX7-MFdUuZaa8VJdu7boGg&oe=6A1C32C2)

In the meantime, this decision does not limit your ability to share your business details. Each business phone number also has a business profile which includes the profile picture, email, website, and business description. These are fields that you can edit at any time.

## Requesting OBA status via WhatsApp Manager

- Access [**WhatsApp Manager**](https://business.facebook.com/latest/whatsapp_manager/) > **Overview** , and click the business phone number:

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/456997811_1368661294090266_2491166291934528895_n.png?_nc_cat=106&ccb=1-7&_nc_sid=e280be&_nc_ohc=tXMOkXpcq1AQ7kNvwFRJ1j5&_nc_oc=AdortIyitgM0OFxgkdBqVZztbcY6yjSrF746FECmY-w3K5zXwyIFOylGUSdkI8YD7I0&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=2DLYU01YYFCuY4zR8xXl4w&_nc_ss=7b20f&oh=00_Af79Z5zVL7GH1mwClQxhNYvHkomUMb7yXDsqZnxWB8ko2Q&oe=6A1C1F04)

- Enable two-step verification if it isn’t enabled already.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/456954365_532463442507497_4571397701593651380_n.png?_nc_cat=110&ccb=1-7&_nc_sid=e280be&_nc_ohc=owl36IO-xTMQ7kNvwGXEK8J&_nc_oc=AdrUQ112qZkZjoLco90DUPhUDpchxUvdxnq5VTCQJ0YqO6QpVKg-_qhyQxIcff00ARI&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=2DLYU01YYFCuY4zR8xXl4w&_nc_ss=7b20f&oh=00_Af766BAzKCVCwMQSGvgFQMhCaHVGZq043hMBhbIBtn_jSQ&oe=6A1C3162)

- Click on the **Submit Request** button under **Phone numbers** > **Profile** > **Official business account** .

## Getting OBA status via API

Use the [Official Business Account Status API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/whatsapp-business-account-official-business-account-status-api#get-version-phone-number-id-official-business-account) to request the `official_business_account` field on your business phone number to get the status of an OBA request.

### Example request

```curl
curl 'https://graph.facebook.com/v25.0/106540352242922?fields=official_business_account' \
-H 'Authorization: Bearer EAAJB...'
```

### Example response

Upon success:

```json
{
  "official_business_account": {
    "oba_status": "NOT_STARTED"
  },
  "id": "106540352242922"
}
```
