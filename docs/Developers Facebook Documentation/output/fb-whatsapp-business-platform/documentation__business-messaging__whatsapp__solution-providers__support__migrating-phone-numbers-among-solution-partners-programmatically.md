# Migrating a business phone number from one Solution Partner to another programmatically

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/support/migrating-phone-numbers-among-solution-partners-programmatically_

---

# Migrating a business phone number from one Solution Partner to another programmatically

Updated: Nov 26, 2025

This document describes how Solution Partners can migrate business phone numbers from one Solution Partner and WhatsApp Business Account (WABA) to another Solution Partner and WABA using the API. Only use this method if you are going to be working with the business customer using the On-Behalf-Of model (i.e. you will create and own the destination WABA and its assets and share them with the customer).

If you would like to migrate customer phone numbers via Embedded Signup (which is recommended), see our [Migrating Phone Numbers Between WhatsApp Business Accounts via Embedded Signup](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/support/migrating-phone-numbers-among-solution-partners-via-embedded-signup) document.

## Overview

Solution Partners and businesses directly integrated with the WhatsApp Business Platform can migrate a registered phone number from one WABA to another. Migrated phone numbers keep their display name, quality rating and [messaging limit](https://developers.facebook.com/documentation/business-messaging/whatsapp/messaging-limits), [Official Business Account](https://developers.facebook.com/documentation/business-messaging/whatsapp/official-business-accounts) status, and any [High quality](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-quality) message templates previously approved.

In practice, migration means that a business can keep the same phone number if:

- They are using the platform with one of our Solution Partners **and** want to switch to a different provider.
- They are using their own implementation **and** want to switch to a Solution Partner.

Only Solution Partners and businesses directly integrated with the WhatsApp Business Platform can perform the phone number migration.

The migration process involves 3 main assets:

| A source WABA | A phone number | A destination WABA |
| --- | --- | --- |
| The account the phone number is currently registered to. | The number that will be migrated. | The account the number will be migrated to. |

Phone migration is always initiated by the Solution Partner or business that owns the destination WABA.

WABAs are accounts created inside a business on Business Manager. Each business has an ID — that ID is also commonly known as Business Manager ID.

Both source and destination WABAs can be associated with businesses in two different ways:

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/565331603_1339318201260164_1404407423147875823_n.jpg?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=FF44uo8LMTkQ7kNvwHH1mzB&_nc_oc=AdpagtA-psfZtWxEdk5PYY9h8jYM0e3BXtc39NFcKzQaD66UX3RQ1bnlRBB2c8261Kg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=xYT_6Imj9ZP1A93u0j6iQg&_nc_ss=7b20f&oh=00_Af424mxkMgPV9qputVsV9WPh9bbFOP5HYoX3H7LNN0iKeA&oe=6A1C069C)

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/561215785_1339318267926824_6000455041075810602_n.jpg?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=grXcD199mC8Q7kNvwEwVF9W&_nc_oc=AdrDQ7PlU7c9EmSvxVzogr7-gieSheo2caRwODGZ6ZKQIGkidW9a2H0A-0_jWz48SNQ&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=xYT_6Imj9ZP1A93u0j6iQg&_nc_ss=7b20f&oh=00_Af7EXb-Rl3Jip4ct23dIa72lFfm_t14zQJyOk749svTtEA&oe=6A1C28FA)

### How migration works

Downtime

The API does not support bulk migration; business phone numbers must be migrated individually.

Message templates

All [high quality](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-quality) message templates in the source WABA will be duplicated and automatically approved in the destination WABA as long as the destination WABA can accommodate new templates. Existing message templates in the destination WABA will not be affected. Low quality, rejected, or pending templates will not be duplicated.

The duplicated templates will be subjected to [Template Categorization Guidelines](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-categorization) checks to ensure that the templates are correctly categorized. This may result in some of the duplicated templates being `REJECTED`.

If the destination WABA cannot accommodate all of the new templates, we will duplicate as many as we can until the destination WABA’S template limit has been reached. Un-duplicated templates must be re-created and submitted for approval if they are to be used by the destination WABA.

Please note that the quality ratings of templates will **NOT** be migrated. All migrated templates will start with an `UNKNOWN` rating. This rating will remain for the **first 24 hours**, after which a new rating will be generated if sufficient data is available.

Billing migration

Messages sent before migration are charged to the source business. Messages sent after migration are charged to the destination business. Messages sent from the source, and are not delivered before migration, are still charged to the source business when they get delivered.

Rate limits

Standard [Graph API rate limits](https://developers.facebook.com/docs/graph-api/overview/rate-limiting) apply to the migration.

Limitations

- Test business phone numbers issued by WhatsApp cannot be migrated.
- Business phone numbers in use with the WhatsApp Business App cannot be migrated using this process. To migrate a number from the WhatsApp Business app, see [Migrating an Existing Number for Cloud API](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/migrate-existing-whatsapp-number-to-a-business-account).
- Uploaded media IDs and message IDs can continue to be used.
- The API does not support bulk migration; business phone numbers must be migrated individually.
- Business phone numbers must have an approved display name (`name_status` is `APPROVED` ).
- Business phone numbers cannot have any associated pending display name change requests.
- Quality ratings of the templates will NOT be migrated. All new migrated templates will start with an `APPROVED` rating, and the new rating of the migrated templates will be established using the past 24h data.

Summary

Migrated:

- Display name
- Quality rating of the phone number
- Messaging limits
- Official Business Account status
- Any High quality message templates previously approved

Not Migrated:

- Low quality, rejected, or pending message templates.
- Quality rating of the template

## Before you start

To be eligible for migration, a business’s assets must meet the following criteria:

| Asset | Requirements for Migration |
| --- | --- |
| Phone number | Must be currently registered with the source WABA.If two-step verification was ever enabled for this number, the source WABA owner needs to [disable it](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers#disabling-two-step-verification).<br>The phone number’s owner is responsible for reaching out to the source WABA’s owner. |
| Source WABA | Must have Business Verification completed and approved.WABA’s review status must be `Approved`. |
| Destination WABA | Must have Business Verification and WABA review completed and approved.Must have a [payment method](https://www.facebook.com/business/help/1684730811624773) set up. |
| Webhooks | **Phone numbers on Cloud API only**<br>At least one app must be subscribed to webhooks for the destination WABA. See [Webhooks in Cloud API](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/overview). |

### Permissions

All API calls for phone migration must be made with an application that has `whatsapp_business_management` permission. See [Using The WhatsApp Business Management API](https://developers.facebook.com/documentation/business-messaging/whatsapp/get-started) section to learn more about App Review, Access Tokens, and making API calls. Phone migration is always initiated by the Solution Partner or business that owns the destination WABA.

### Preparing the destination WABA

The type of destination WABA determines what needs to be done for the account to be ready for migration:

| Type of WABA | Considerations for Solution Partners performing migration |
| --- | --- |
| Existing WABA | Confirm that the existing (destination) WABA has a payment method set up.<br>If the source WABA is on Cloud API, make sure at least one app is subscribed to webhooks for the destination WABA. |
| New WABA created by a Solution Partner messaging for a customer | When creating a new WABA in the Business Manager, a Solution Partner must:<br>Enter an Account Name for the customer (WABA Name)Select a [payment method](https://www.facebook.com/business/help/1684730811624773?id=2129163877102343)Select **Client’s Account** in the **Messaging for** field, andEnter the customer’s Business Manager ID — see [Find Your Business ID in Business Manager](https://www.facebook.com/business/help/1181250022022158?id=180505742745347).<br>Solution Partners can then instruct their customers to accept the **Messaging For** request sent to their Business Manager. To guide your customers, see [Create Your WhatsApp Business Account With WhatsApp Solution Partners](https://www.facebook.com/business/help/524220081677109). Once the request has been accepted, the destination WABA is ready for phone migration.<br>If the source WABA is on Cloud API, make sure at least one app is subscribed to webhooks for the destination WABA. |
| New WABA created by a customer and shared with a Solution Partner via Embedded Signup | This type of WABA is created once a customer goes through the Embedded Signup flow on the Solution Partner’s website. To guide your customers, see [Create Your WhatsApp Business Account With WhatsApp Solution Partners, Embedded Signup](https://www.facebook.com/business/help/524220081677109). During the Embedded Signup flow, instruct the customer to:<br>Select the same business as the one that owns their existing WABA.Do not add a phone number via signup flow —we’ll be using the migration API for this. Customers can finish the Embedded Signup flow after creating their WhatsApp Business Account.<br>Use Embedded Signup APIs to [get the WABA created by the customer](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/manage-accounts#get-list-of-shared-wabas), [add system users](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens), and [set up a payment method for the WABA](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/share-and-revoke-credit-lines#sharing-your-credit-line).<br>Since the WABA is already shared with the Solution Partner, the WABA is ready for phone migration. **Reminder:** The migration only happens if the customer’s business has completed Business Verification.<br>If the source WABA is on Cloud API, make sure at least one app is subscribed to webhooks for the destination WABA. |

### Source WABA deletion

If you plan on deleting the source WABA after completing migration, verify that all of the templates you require have been duplicated in the destination WABA **before deleting the source WABA**.

## Get started

All migration calls are made to the endpoint with the destination WABA’s ID. Phone migration is always initiated by the Solution Partner or business that owns the destination WABA.

### Step 1: Disable two-step verification

Two-step verification must be disabled on the phone number before you can initiate migration. This can be done via the [Meta Business Manager](https://business.facebook.com).

If you own the source WABA and the phone number owner has asked you to migrate their number, you can disable two-step verification yourself. If you do not own the source WABA, the phone number owner must ask the source WABA owner to disable two-step verification on their phone number.

### Step 2: Initiate phone migration

Use the [Phone Numbers API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/phone-number-management-api#post-version-waba-id-phone-numbers) to initiate the migration — remember that `WHATSAPP_BUSINESS_ACCOUNT_ID` represents the ID of the destination WABA. On the call, specify the following fields:

| Name | Description |
| --- | --- |
| `cc` | **Required.**<br>Numerical country code for the phone number being registered. |
| `phone_number` | **Required.**<br>Phone number being migrated, without the country code or plus symbol (`+`). |
| `migrate_phone_number` | **Required.**<br>To migrate a phone number, set this to `true`. |

To find the ID of a WhatsApp Business Account, go to [Business Manager](https://business.facebook.com/) > Business Settings > Accounts > WhatsApp Business Accounts. Find the account you want to use and click on it. A panel opens, with information about the account, including the ID.

API call example:

```html
curl -X POST \
  'https://graph.facebook.com/v25.0/<DESTINATION_WHATSAPP_BUSINESS_ACCOUNT_ID>/phone_numbers' \
  -d 'cc=1' \
  -d 'phone_number=<PHONE_NUMBER>' \
  -d 'migrate_phone_number=true' \
  -d 'access_token=<ACCESS_TOKEN>'
```

A successful API call returns:

```html
{
  'id': '<PHONE_NUMBER_ID>'
}
```

### Step 3: Verify phone ownership

Now that you have requested the migration, you need to confirm it by verifying ownership of the phone number. To do that, use the [Request Code API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-pre-verified-phone-number/request-verification-code-api#post-version-pre-verified-phone-number-id-request-code) to request a registration code. Here, `PHONE_NUMBER_ID` represents the ID returned from Step 1.

On the call, specify the following fields:

| Name | Description |
| --- | --- |
| `code_method` | **Required.**<br>Method of receiving the registration code. Supported values: `SMS` and `VOICE`. |
| `language` | **Required.**<br>Language in which you want to receive the registration code. See [language codes](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/supported-languages). |

A sample call looks like this:

```html
curl -X POST \
'https://graph.facebook.com/v25.0/<PHONE_NUMBER_ID>/request_code' \
  -d 'code_method=SMS' \
  -d 'language=en_US' \
  -d 'access_token=<ACCESS_TOKEN>'
```

If your API call returns `success: true`, you should get your code via the selected `code_method` to the phone number being migrated —it may take a few minutes for the code to be delivered. The phone number’s owner needs to provide this code before you can verify the code.

To verify the code, use the [Verify Code API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/verify-code-api#post-version-phone-number-id-verify-code). Specify the following field:

| Name | Description |
| --- | --- |
| `code` | **Required.**<br>6-digit registration code received after making the `/PHONE_NUMBER_ID/request_code` call. |

For example:

```html
curl -X POST \
'https://graph.facebook.com/v25.0/<PHONE_NUMBER_ID>/verify_code' \
  -d 'code=<6-DIGIT-CODE>' \
  -d 'access_token=<ACCESS_TOKEN>'
```

If your API call returns `{"success":true}`, the ownership of your phone number is verified.

### Step 4: Register phone number

Use the [Register API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/register-api#post-version-phone-number-id-register) along with your 6-digit PIN to register the phone number again. See [Register the business phone number](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/registration#register-phone).

## Troubleshooting

If the template migration process fails, please refer to the following documentation for instructions on how to manually trigger a template migration: [Template Migration](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-migration).
