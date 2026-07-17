# Migrating a WABA from one Multi-Partner Solution to another via Embedded Signup | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/support/migrating-wabas-among-solutions-via-embedded-signup_

---

# Migrating a WABA from one Multi-Partner Solution to another via Embedded Signup

Updated: Nov 10, 2025

If you are a Tech Provider, you can use the API and [Embedded Signup](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/overview) to migrate a business customer’s WABA from one Multi-Partner Solution (the “source solution”) to another (the “destination solution”).

As part of this process, a new WhatsApp Business Account (WABA) will be created for the business customer, templates within the source WABA will be duplicated in the destination WABA, and access to the WABA and its assets will be granted to the destination solution’s Solution Partner.

## Requirements

Your app (or apps, if you are using separate apps) used to create or accept the source and destination Multi-Partner Solutions must be associated with the same business portfolio.
The destination solution must also be in an Active state.

## Templates

Templates are automatically duplicated in the destination WABA and initially granted the same status as their source counterparts.

After duplication however, templates are re-checked to ensure they are correctly categorized according to our [guidelines](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing). This may result in some duplicated templates having their `status` set to `REJECTED`.

Only templates with both a `status` of `APPROVED` and `quality_score` of `GREEN` are eligible for duplication. If the destination WABA cannot accommodate all of the new templates, we will duplicate as many as we can until the destination WABA’s template limit has been reached. Unduplicated templates must be re-created and submitted for approval if they are to be used by the destination WABA.

Note that **template quality ratings are not duplicated**. All duplicated templates will start with an `UNKNOWN` rating. This rating will remain for the first 24 hours, after which a new rating will be generated if sufficient data is available.

## Billing

Messages delivered before migration is complete are charged to the old Solution Partner. Undelivered messages sent before migration is complete will be charged to the old Solution Partner if they are delivered after migration is complete.

Messages delivered after migration is complete are charged to the business customer.

## Tech Provider steps

### Step 1: Tag the customer’s WABA for migration

Use the [POST /<WHATSAPP_BUSINESS_ACCOUNT>/set_solution_migration_intent](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/set-solution-migration-intent-api#Creating) endpoint to tag the business customer’s WABA for migration. This generates a [migration intent](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/migration-intent-api), which indicates your intent to migrate the WABA.

Request

```html
curl 'https://graph.facebook.com/<API_VERSION>/<WABA_ID>/set_solution_migration_intent' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <BUSINESS_TOKEN>' \
-d '
{
  "solution_id": "<DESTINATION_MULTI-PARTNER_SOLUTION_ID>"
}'
```

Response

Upon success:

```html
{
  "id": "<MIGRATION_INTENT_ID>"
}
```

Capture the migration intent ID.

### Step 2: Disable two-step verification on the business phone number

If you have access to the business customer’s WABA in WhatsApp Manager, disable two-step verification on the business phone number associated with their WABA.

Alternatively, you can instruct the business customer to do this on their own. You can provide them with these instructions:

1. *Access WhatsApp Manager at [https://business.facebook.com/latest/whatsapp_manager/](https://business.facebook.com/latest/whatsapp_manager/).*
2. *Navigate to **Account tools** > **Phone numbers**, and click the phone number’s settings (gear) icon. If you don’t see your business phone number, click **Overview** in the menu on the left, then locate the number and click it.*
3. *Click the **Two-step verification** tab.*
4. *Click the **Turn off two-step verification** button and complete the flow.*

### Step 3: Instruct the customer to complete Embedded Signup

Instruct the customer to complete the Solution Partner’s implementation of Embedded Signup.

Make sure that you are directing the customer to the Embedded Signup implementation correctly configured with the destination Multi-Partner Solution ID, otherwise the customer could be onboarded via the wrong solution.

You can provide the customer with these instructions:

1. *Enter your existing business portfolio name in the [business portfolio screen](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/default-flow#business-portfolio-screen).*
2. *Create a new WhatsApp Business Account (WABA) in the [WABA selection screen](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/default-flow#business-asset-selection-screen).*
3. *Enter your existing business phone number in the [phone number addition screen](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/default-flow#phone-number-addition-screen). This will trigger a warning that the number will be moved to a new WhatsApp Business Account.*

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/466392707_1274428157316091_5418623531369238611_n.png?_nc_cat=110&ccb=1-7&_nc_sid=e280be&_nc_ohc=uakCo-3l844Q7kNvwF-Kso0&_nc_oc=AdpJWa30dyIiUZWNBWOfLyeV7ilmAtdsy_p6Gv2uHefqoMES8O4-dDMIwusTniTvmJM&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=6j3C8IyUOIiYUxAHZu-Zvg&_nc_ss=7b20f&oh=00_Af4abSr6WhFgViYxEefI_9NgbJenZz5tOhUGart8dcwRiA&oe=6A1C1575)

## Solution Partner steps

Provide the Tech Provider with a link to your implementation of Embedded Signup configured with the Multi-Partner Solution ID. Whenever a business customer completes your implementation’s flow successfully, [onboard the business customer](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-customers-as-a-solution-partner) as you normally would.
