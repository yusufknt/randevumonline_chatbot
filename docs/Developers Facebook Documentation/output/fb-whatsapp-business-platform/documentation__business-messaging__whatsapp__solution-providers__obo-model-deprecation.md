# On-Behalf-Of account ownership model deprecation | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/obo-model-deprecation_

---

# On-Behalf-Of account ownership model deprecation

Updated: Nov 14, 2025

We have deprecated the On-Behalf-Of (“OBO”) account ownership model and replaced it with [partner-initiated WABA creation](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/partner-initiated-waba-creation). All existing WABAs created under the OBO model should have been transferred to business customers by October 1, 2025. Post 1st October 2025, all the eligible OBO accounts will be auto-migrated in batches through the end of 2025.

## Deprecation timeline

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/485146176_691212949947759_244674574159890376_n.png?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=98MPJpHH2vkQ7kNvwHcmf7b&_nc_oc=Adoj1gsoqa4XtolUJB3vOysMsjNXP6QScQB4NrDl9EoQHT6IfiL7RuzqWwe0oDdDpRE&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=gjkw0vS5_OVw8HvqixiSdg&_nc_ss=7b20f&oh=00_Af4RwrVH2q4AnfcYgzv3XyOcg8srhTgfN6N_raq7oVSaRg&oe=6A1C2AC2)

- **March 24, 2025** : [partner-initiated WABA creation](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/partner-initiated-waba-creation) is made available to all Solution Providers.
- **September 29, 2025** : last day to onboard business customers to the OBO model.
- **October 1, 2025** : last day to transfer ownership of OBO model WABAs to business customers.

## Payment methods

Partner-initiated WABA creation does not support automatic payment setup. Instead, you must share your credit line with the business customer via the API. See [Partner-initiated WABA creation](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/partner-initiated-waba-creation) for details.

## Multi-Partner Solutions

Business customers cannot be onboarded to a Multi-Partner Solution as part of the
partner-initiated WABA creation process, but can be added to an MPS afterwards. See [Partner-initiated WABA creation](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/partner-initiated-waba-creation) for details.

## Marketing Messages API for WhatsApp

Existing OBO model WABAs need to be transferred to business customers if you want to use them with the Marketing Messages API for WhatsApp, but this can be done as part of the [Marketing Messages API for WhatsApp onboarding process](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/onboarding#onboard-via-a-partner-using-whatsapp-manager).
