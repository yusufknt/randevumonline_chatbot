# Website field optional | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/website-optional_

---

# Website field optional

Updated: Nov 4, 2025

This feature is currently only available to approved **Select Solution** and **Premier** Solution Partners. See our [Sign up for partner-led business verification](https://www.facebook.com/business/help/1091073752691122) Help Center article to learn how to request approval.

By default, the website field is required in the [business portfolio screen](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/default-flow#business-portfolio-screen). If you have been approved for [Partner-led Business Verification](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/partner-led-business-verification) however, the website field will become optional and will be accompanied by a **My business does not have a website or profile page** checkbox:

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/467331606_2133248890410157_3569145607260288812_n.png?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=wYgUqOBxtu8Q7kNvwE9mecz&_nc_oc=AdqLfHzvXuWGA2NzCFOYpUmA7Uqny1F-J04Nfe-d1-VrWBYzayK5IzPH6vRyJj4Fsc4&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=iyaj718u8rCFAxavYy_d3w&_nc_ss=7b20f&oh=00_Af6xtj-8_MuJkaCQ2SMGArn03Sk4f9_FPtMqFaOgcAJciw&oe=6A1C1984)

When a business customer checks this box and completes the flow, the customer’s WhatsApp assets and exchangeable token code will be generated and returned in a [message event](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/implementation#session-logging-message-event-listener) and [JavaScript response](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/implementation#response-callback), as usual.

However, the [account_update webhook](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/website-optional#webhook) that’s triggered when the customer completes the flow will have `event` set to `PARTNER_CLIENT_CERTIFICATION_NEEDED`, which indicates that you must verify their business as part of the onboarding process.

Onboard the customer as you normally would, and when you’re done, complete the steps described in our [Partner-led Business Verification](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/partner-led-business-verification) document to verify their business. **The customer will not be able to send messages until their business is verified.**

- [Onboarding business customers as a Solution Provider](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-customers-as-a-solution-partner)
- [Onboarding business customers as a Tech Provider](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-customers-as-a-tech-provider)

Note that if you are unable to verify your customer’s business, the customer must first add a website on their own using [Meta Business Suite > Settings > Business info](https://business.facebook.com/settings/info), or they won’t be able to send messages. Once they have added a website and it has been accepted, they can also [verify their business](https://www.facebook.com/business/help/2058515294227817) on their own, if they choose to do so.

## Webhook

When a business customer successfully completes the flow, an **account_update** webhook will be triggered with `event` set to `PARTNER_CLIENT_CERTIFICATION_NEEDED`.

```html
{
  "entry": [
    {
      "id": "<WHATSAPP_BUSINESS_ACCOUNT_ID>",
      "time": <WEBHOOK_SENT_TIMESTAMP>,
      "changes": [
        {
          "value": {
            "event": "PARTNER_CLIENT_CERTIFICATION_NEEDED",
            "partner_client_certification_needed_info": {
              "client_business_id": "<CUSTOMER_BUSINESS_PORTFOLIO_ID>"
            }
          },
          "field": "account_update"
        }
      ]
    }
  ],
  "object": "whatsapp_business_account"
}
```

When you receive this webhook, onboard the customer as you normally would, then complete the steps described in the [Partner-led Business Verification](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/partner-led-business-verification) document to verify the customer’s business.
