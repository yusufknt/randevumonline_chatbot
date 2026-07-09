# Pricing on the WhatsApp Business Platform | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing_

---

# Pricing on the WhatsApp Business Platform

Updated: Mar 30, 2026

This document explains how pricing works on the WhatsApp Business Platform.

## Cloud API and Marketing Messages API for WhatsApp

To align with industry-standards, effective July 1, 2025, Meta now charges on a **per-message basis**:

- You are only charged when a [template message](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview) is delivered ( `"type":"template"` ).
- Rates vary based on the template’s [category](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing#message-template-categories) and the recipient WhatsApp phone number’s [country calling code](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing#country-calling-codes) .

Meta provides value to businesses in several ways:

- All non-template messages are free ( `"type":"text"` , `"type":"image"` , and so on). These can only be sent within an open [customer service window](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages#customer-service-windows) . See [Sending messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages#sending-messages) for a list of message types.
- Utility templates delivered within an open customer service window are free.
- You can unlock [lower rates](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing#volume-tiers) for utility and authentication template messages, based on messaging volume.
- All messages are free for 72 hours, including template messages, if sent within an open [free entry point window](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing#free-entry-point-windows) .

## Pricing explainer

Our pricing explainer PDF outlines how Meta charges and the various ways Meta provides value to businesses, in PDF form:

Pricing Explainer PDF

## Message template categories

Unlike non-template messages, template messages are the only message type that can be sent outside of a customer service window. Templates can be categorized as:

- Marketing
- Utility
- Authentication

See [Template categorization](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-categorization) to learn how template categorization works.

### Template messages vs. non-template messages

![Diagram showing template messages vs non-template messages pricing](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/571069280_1541820816822527_6328052606712176022_n.png?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=_WxAiMaL1OEQ7kNvwHY53eq&_nc_oc=AdoTsrb9fs0bllhpvmlkK-Umn1MB3x3SK6hDWXbnu3Yu17isDX1RZe4xA4fymJLE27E&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=DawDLQcngS5jU82g2O5KKA&_nc_ss=7b20f&oh=00_Af7bUby24JFnqpYh0VuTQetfPgE9WDYXrajMdiUvtziCgA&oe=6A1C026F)

- CSW = [Customer service window](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages#customer-service-windows)
- FEP = [Free entry point window](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing#free-entry-point-windows)

Businesses are responsible for reviewing the category assigned to their approved templates. Whenever a template is used, a business accepts the charges associated with the category applied to the template at time of use.

## Charge example

In the example below, a business sends 4 messages to a WhatsApp user but is only charged for 2 (1 marketing charge, 1 utility charge).

| Hour | Action | Rate | Reason |
| --- | --- | --- | --- |
| 0 | You send a marketing template message to a WhatsApp user, promoting your new product. | Marketing | All marketing template messages are charged. |
| 2 | The user messages you about the product.<br>This opens a 24 hour [customer service window](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages#customer-service-windows) (“CSW”). | - | Messages sent from a WhatsApp user to a business are not charged. |
| 3 | You send a [text message](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/text-messages) to the user (`"type":"text"`), describing the product in more detail. | None | All non-template messages are free within an open customer service window. |
| 4 | The user purchases the product and you send them a utility template confirming their order. | None | The CSW is still open, and utility templates sent within an open CSW are free. |
| 26 | The CSW closes, which means you can no longer send non-template messages. | - | 24 hours have passed since the user last messaged you. |
| 30 | You send a utility template message to the user, updating them on their order. | Utility | Utility template messages sent outside of a CSW are charged, and no open CSW exists between you and the user. |

## Pricing calendar

To better enable our customers to plan and prepare for pricing updates, the following pricing calendar applies for messaging and voice on the WhatsApp Business Platform:

- Meta may update pricing only *on the 1st day of each quarter* , thus up to 4 times per year: January 1, April 1, July 1, and/or October 1.
- Meta will provide advanced notice that is better aligned to the effort required to implement different types of pricing updates, per below:

| Type of pricing update | Examples | Minimum advance notice |
| --- | --- | --- |
| **Rate card update** | Updating the [rate](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing#rates) for a given market–product<br>Updating the volume tiers for a given market–product (utility and authentication only)<br>Moving a market from one [pricing region](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing#country-calling-codes) (e.g. “Other”) to another or to be standalone on the rate card | 1 month |
| **Pricing model add-on** | Our July 1, 2025, introduction of new [volume tiers](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing#volume-tiers) for utility and authentication messages | 3 months |
| **Pricing model change** | Our July 1, 2025 update to our pricing model, from conversation-based pricing to per-message pricing | 6 months |

## Rates

Rates vary based on [template category](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-categorization), [volume tier](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing#volume-tiers), and [country/region](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing#country-calling-codes) rate.

### Rate cards and volume tiers

These rate cards reflect our current rates and volume tiers, effective April 1, 2026, based on WhatsApp Business Account timezone. This information is also available interactively on our [WhatsApp Business website](https://business.whatsapp.com/products/platform-pricing#rates).

| Currency | Rates(CSV) | Volume tiers(CSV) | Rates and Volume tiers(PDF) |
| --- | --- | --- | --- |
| USD | USD rates | USD volume tiers | USD rates and volume tiers |
| AED | AED rates | AED volume tiers | AED rates and volume tiers |
| ARS | ARS rates | ARS volume tiers | ARS rates and volume tiers |
| AUD | AUD rates | AUD volume tiers | AUD rates and volume tiers |
| CLP | CLP rates | CLP volume tiers | CLP rates and volume tiers |
| COP | COP rates | COP volume tiers | COP rates and volume tiers |
| EUR | EUR rates | EUR volume tiers | EUR rates and volume tiers |
| GBP | GBP rates | GBP volume tiers | GBP rates and volume tiers |
| IDR | IDR rates | IDR volume tiers | IDR rates and volume tiers |
| INR | INR rates | INR volume tiers | INR rates and volume tiers |
| MXN | MXN rates | MXN volume tiers | MXN rates and volume tiers |
| MYR | MYR rates | MYR volume tiers | MYR rates and volume tiers |
| PEN | PEN rates | PEN volume tiers | PEN rates and volume tiers |
| SAR | SAR rates | SAR volume tiers | SAR rates and volume tiers |
| SGD | SGD rates | SGD volume tiers | SGD rates and volume tiers |

### Updates to rate cards

Below represents future updates to our rates. See our [rate cards](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing#rate-cards-and-volume-tiers) above for current rates.

**Rate cards effective July 1, 2026**

Effective July 1, 2026, as of 9am PT – Eligible customers can create new WhatsApp Business Accounts in BRL (Brazilian Reals). This is only available for Solution Partners and directly-integrated clients whose Sold-To country is Brazil in [Billing Hub](https://business.facebook.com/billing_hub/legal_entities). Per our [pricing calendar](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing#pricing-calendar), Meta will publish per-message rates in BRL by June 1, 2026.

**Billing localization for India and Brazil**

Meta is introducing billing localization to help eligible customers to better manage costs of messaging amidst currency fluctuations. This will apply to the markets below, and specifically to Solution Partners and directly-integrated clients whose Sold-To country in Billing Hub is a market below:

- [India](https://www.facebook.com/business/help/2301408543603167) – As of January 1, 2026.
- [Brazil](https://www.facebook.com/business/help/4344414845795884) – As of July 1, 2026.

**Previous updates**

- Effective April 1, 2026 at 12am by WhatsApp Business Account timezone, the rate updates below applied: Saudi Arabia – Higher marketing message rate.India – Higher authentication-international rate.Pakistan – Higher utility and authentication rates. No change to the authentication-international rate.Turkey – Lower utility and authentication rates.8 new billing currencies introduced: ARS (Argentina), CLP (Chile), COP (Colombia), MYR (Malaysia), PEN (Peru), SAR (Saudi Arabia), SGD (Singapore), AED (United Arab Emirates).
- Effective January 1, 2026 at 12am by WhatsApp Business Account timezone, the rate updates below applied: India - Higher marketing rate.France, Egypt - Lower marketing rates.North America - Lower utility and authentication rates.
- Effective October 1, 2025 at 12am by WhatsApp Business Account timezone, the rate updates below applied: Colombia – Higher utility and authentication rates.Mexico – Lower marketing rates.United Arab Emirates – Higher marketing message rate.Argentina, Egypt, Saudi Arabia – Lower utility and authentication rates.Zimbabwe is mapped to our “Rest of Africa” region vs. “Other”. Messages delivered to WhatsApp users with a +263 country calling code (Zimbabwe) will be charged “Rest of Africa” rates.
- Effective July 1, 2025 – Lower utility and authentication message rates across several markets, to ensure pricing is on-par to alternate channels for these use cases. Marketing conversation rates became marketing message rates.
- Effective April 1, 2025 – Lowered [authentication-international conversation rates](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/authentication-international-rates) for Egypt, Nigeria, Pakistan, and South Africa.
- Effective February 1, 2025 – Lowered [authentication conversation rates](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing#rates) for Egypt, Malaysia, Nigeria, Pakistan, Saudi Arabia, South Africa, and the United Arab Emirates.
- Effective November 1, 2024 – [Service conversations](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/conversation-based-pricing#service-conversations) are now free for all businesses.
- Effective October 1, 2024 – Updated [marketing conversation rates](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing#rates) in India, Saudi Arabia, the United Arab Emirates, and the United Kingdom.
- Effective August 1, 2024 – Lowered [utility conversation rates](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing#rates) .

### Authentication-international rates

Specific countries have an authentication-international rate. Our rate cards reflect these rates. See [Authentication-International rates](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/authentication-international-rates) to learn about these rates and if they apply to you.

### Country calling codes

Charges for conversations are based on the country calling code of the recipient WhatsApp phone number. The table below shows how Meta maps country calling codes to countries or regions. If a country is not listed below, it maps to **Other**.

This information is also available in a CSV file:

Country Calling Codes and Regional Rate Mapping CSV

| Markets | Calling Code<br>(and network prefix if applicable) |
| --- | --- |
| Countries<br>ArgentinaBrazilChileColombiaEgyptFranceGermanyIndiaIndonesiaIsraelItalyMalaysiaMexicoNetherlandsNigeriaPakistanPeruRussiaSaudi ArabiaSouth AfricaSpainTurkeyUnited Arab EmiratesUnited Kingdom | 545556572033499162972396052312349251796627349097144 |
| North America<br>Canada<br><br>United States | 1<br><br>1 |
| Rest of Africa<br>Algeria<br><br>Angola<br><br>Benin<br><br>Botswana<br><br>Burkina Faso<br><br>Burundi<br><br>Cameroon<br><br>Chad<br><br>Republic of the Congo (Brazzaville)<br><br>Eritrea<br><br>Ethiopia<br><br>Gabon<br><br>Gambia<br><br>Ghana<br><br>Guinea-Bissau<br><br>Ivory Coast<br><br>Kenya<br><br>Lesotho<br><br>Liberia<br><br>Libya<br><br>Madagascar<br><br>Malawi<br><br>Mali<br><br>Mauritania<br><br>Morocco<br><br>Mozambique<br><br>Namibia<br><br>Niger<br><br>Rwanda<br><br>Senegal<br><br>Sierra Leone<br><br>Somalia<br><br>South Sudan<br><br>Sudan<br><br>Swaziland<br><br>Tanzania<br><br>Togo<br><br>Tunisia<br><br>Uganda<br><br>Zambia<br><br>Zimbabwe | 213<br><br>244<br><br>229<br><br>267<br><br>226<br><br>257<br><br>237<br><br>235<br><br>242<br><br>291<br><br>251<br><br>241<br><br>220<br><br>233<br><br>245<br><br>225<br><br>254<br><br>266<br><br>231<br><br>218<br><br>261<br><br>265<br><br>223<br><br>222<br><br>212<br><br>258<br><br>264<br><br>227<br><br>250<br><br>221<br><br>232<br><br>252<br><br>211<br><br>249<br><br>268<br><br>255<br><br>228<br><br>216<br><br>256<br><br>260<br><br>263 |
| Rest of Asia Pacific<br>Afghanistan<br><br>Australia<br><br>Bangladesh<br><br>Cambodia<br><br>China<br><br>Hong Kong<br><br>Japan<br><br>Laos<br><br>Mongolia<br><br>Nepal<br><br>New Zealand<br><br>Papua New Guinea<br><br>Philippines<br><br>Singapore<br><br>Sri Lanka<br><br>Taiwan<br><br>Tajikistan<br><br>Thailand<br><br>Turkmenistan<br><br>Uzbekistan<br><br>Vietnam | 93<br><br>61<br><br>880<br><br>855<br><br>86<br><br>852<br><br>81<br><br>856<br><br>976<br><br>977<br><br>64<br><br>675<br><br>63<br><br>65<br><br>94<br><br>886<br><br>992<br><br>66<br><br>993<br><br>998<br><br>84 |
| Rest of Central and Eastern Europe<br>Albania<br><br>Armenia<br><br>Azerbaijan<br><br>Belarus<br><br>Bulgaria<br><br>Croatia<br><br>Czech Republic<br><br>Georgia<br><br>Greece<br><br>Hungary<br><br>Latvia<br><br>Lithuania<br><br>Moldova<br><br>North Macedonia<br><br>Poland<br><br>Romania<br><br>Serbia<br><br>Slovakia<br><br>Slovenia<br><br>Ukraine | 355<br><br>374<br><br>994<br><br>375<br><br>359<br><br>385<br><br>420<br><br>995<br><br>30<br><br>36<br><br>371<br><br>370<br><br>373<br><br>389<br><br>48<br><br>40<br><br>381<br><br>421<br><br>386<br><br>380 |
| Rest of Western Europe<br>Austria<br><br>Belgium<br><br>Denmark<br><br>Finland<br><br>Ireland<br><br>Norway<br><br>Portugal<br><br>Sweden<br><br>Switzerland | 43<br><br>32<br><br>45<br><br>358<br><br>353<br><br>47<br><br>351<br><br>46<br><br>41 |
| Rest of Latin America<br>Bolivia<br><br>Costa Rica<br><br>Dominican Republic<br><br>Ecuador<br><br>El Salvador<br><br>Guatemala<br><br>Haiti<br><br>Honduras<br><br>Jamaica<br><br>Nicaragua<br><br>Panama<br><br>Paraguay<br><br>Puerto Rico<br><br>Uruguay<br><br>Venezuela | 591<br><br>506<br><br>1 (809, 829, 849)<br><br>593<br><br>503<br><br>502<br><br>509<br><br>504<br><br>1 (658, 876)<br><br>505<br><br>507<br><br>595<br><br>1 (787, 939)<br><br>598<br><br>58 |
| Rest of Middle East<br>Bahrain<br><br>Iraq<br><br>Jordan<br><br>Kuwait<br><br>Lebanon<br><br>Oman<br><br>Qatar<br><br>Yemen | 973<br><br>964<br><br>962<br><br>965<br><br>961<br><br>968<br><br>974<br><br>967 |
| Other<br>All other countries | Varies by country |

## Volume tiers

You can unlock lower utility and authentication rates based on the number of messages you send in a month.

### Tiering accrual

- **Messages are aggregated at the business portfolio level, across all WhatsApp Business Accounts (WABAs) owned by the portfolio** — To determine what tier rates may apply in a given month for a given market–category pair, Meta aggregates messages across all of a business portfolio’s WABAs for each market-category pair (e.g., Brazil–authentication, Brazil–utility, India–authentication, and so on).
- **Only messages that are charged count toward the tiers** — Thus, the following messages do not count: Utility templates delivered to WhatsApp users within an open customer service window.Utility templates delivered within a [free entry point window](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing#free-entry-point-windows).
- **Volume tiers will be determined solely by Meta** — All insights data is approximate due to small variations in data processing. Undue reliance should not be placed on insights data.

### Key dynamics

- **Tiers are market–category specific** — Volume tiers are aligned to our rate cards and differ by market (e.g., Brazil or Rest of Latin America) and category (utility, authentication).
- **Rates are tier-specific** — When a business sends enough messages at a given market–category pair to reach the next tier, they unlock the rate of the next tier, specifically for messages in that tier. This rate applies across all of their WABAs.
- **Tiers reset monthly** — At the start of the next month (12am WABA timezone), message count resets to 0 and businesses begin to accrue messages toward that month.

### Volume tiers examples

The table below is illustrative and only highlights the dynamics of volume tiers. Please refer to our [rate cards](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing#rate-cards-and-volume-tiers) to see the rates charged.

![Table showing volume tier rate examples](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/502514970_1202956304344062_4629097874159039633_n.png?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=mHJGFF_pgcQQ7kNvwHRxhyV&_nc_oc=Adq210Uwg0N-1mT91xCNTrFqWfXWHR1wHOv97IT2lr5cFt0iGrG8vgGeAP4cCogb7Ac&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=DawDLQcngS5jU82g2O5KKA&_nc_ss=7b20f&oh=00_Af6nj5wpnqHZJQRLeBHaSPCJ7o1EZbomjkT9eXdvPUw9QQ&oe=6A1C0291)

Below are several examples to highlight how the tiers work and what is charged in a given month, for a given market–category. These examples refer to the illustrative table above:

Example 1: A business that sends a total of B authentication messages in a month to India is charged:

- List rate for the first A messages.
- Tier rate 1 for messages A+1 to B.
- Total charges for that month = Rate per tier 𝗑 messages in each tier.

Example 2: A business that starts to be charged our authentication-international rates on the 15th day of the month:

- Day 1 to 14 of that month: Volume tiers apply on the authentication rate.
- Day 15 onward of that month: Volume tiers apply on the authentication-international rate, with messages continuing to accrue in that month. For example, if a business has already reached the Tier 2, the business would be charged Tier 2’s authentication-international rate:

Example 3: A business has 3 WABAs sending authentication messages to India. For WABA A, it is still July 31 based on their timezone. For WABAs B and C, it is already August 1 based on their timezone. For July, the business is already being charged Tier Rate 1.

- The business portfolio will be accruing toward tiers for both July (via WABA A) and August (via WABAs B, C) for a period of time.
- The business can reach the next tier for July, via WABA A. If that happens, messages for the remainder of July for WABA A will be charged Tier Rate 2.

Example 4: A business has 3 WABAs, integrated across 2 solution providers. Provider 1 sends the first B messages in a given month, and provider 2 starts sending messages as of when the business is in the 3rd tier. The business does not send enough messages that month to reach the next tier. What we would charge each provider:

- Provider 1: List rate for A messages, then Tier Rate 1 from A+1 to B, and Tier Rate 2 for B+1 to C.
- Provider 2: Tier Rate 2 across all of their messages.

### Tiering webhooks

Starting October 1, 2025, an [account_update](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/account_update) webhook with `event` set to `VOLUME_BASED_PRICING_TIER_UPDATE` will be triggered when your WhatsApp Business Account reaches a new volume tier, in any market, in a given month. This complements our [pricing_analytics](https://developers.facebook.com/documentation/business-messaging/whatsapp/analytics#pricing-analytics) endpoint, which will continue to provide intra-month tiering progress and tiering information for delivered messages.

Example webhook:

```json
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "102290129340398",
      "time": 1743451903,
      "changes": [
        {
          "value": {
            "volume_tier_info": {
                "tier_update_time": 1743451903,
                "pricing_category": "UTILITY",
                "tier": "25000001:50000000",
                "effective_month": "2025-11",
                "region": "India"
            },
            "event": "VOLUME_BASED_PRICING_TIER_UPDATE"
          },
          "field": "account_update"
        }
      ]
    }
  ]
}
```

- `tier_update_time` tells when your WABA reached a higher volume tier (Unix timestamp).
- `pricing_category` tells you the template category for which your new volume tier rate applies.
- `tier` tells you the new volume tier’s lower and upper bounds.
- `effective_month` tells you the month in which your new volume tier rate is in effect.
- `region` tells you the WhatsApp user country/region for which your new volume tier rate applies.

Note that it’s possible for multiple [account_update](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/account_update) webhooks to be triggered that describe the same tier switch event. In these cases, use the webhook with the smaller `tier_update_time` Unix timestamp as the official webhook.

### Tiering analytics

You can get [volume tier information](https://developers.facebook.com/documentation/business-messaging/whatsapp/analytics#volume-tier-information) via [template analytics](https://developers.facebook.com/documentation/business-messaging/whatsapp/analytics#template-analytics).

## Free non-template messages

Non-template messages, which can only be sent within an open [customer service window](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages#customer-service-windows), are free. These messages will have `type` set to `free_customer_service` in the `pricing` object of status [messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/status) webhooks:

```json
"pricing": {
  "billable": false,
  "pricing_model": "PMP",
  "type": "free_customer_service",
  "category": "service"
}
```

## Free utility template messages

Utility template messages sent within an open [customer service window](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages#customer-service-windows) are free. These messages will have `type` set to `free_customer_service` and `category` set to `utility` in the `pricing` object of status [messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/status) webhooks:

```json
"pricing": {
  "billable": false,
  "pricing_model": "PMP",
  "type": "free_customer_service",
  "category": "utility"
}
```

### Edge case

If you send a message to a WhatsApp user prior to July 1, 2025 (which is when Meta switched from conversation-based pricing to per-message pricing), a utility conversation is opened between you and a user that spans the switch to per-message pricing (the conversation was opened before the switch but won’t close until after the switch). In this case, utility templates sent to the user after the switch while the conversation is open will be free, but attributed to the open conversation. In status [messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/status) webhooks, these messages will have a `pricing_model` of `CBP` and the utility conversation ID will be assigned to `conversation.id`. Once the conversation closes, subsequent utility messages will use per-message pricing, which will be reflected in new webhooks.

## Free Entry Point windows

If a WhatsApp user messages you via a Click to WhatsApp Ad or Facebook Page Call-to-Action button using a device running our Android or iOS app (our desktop and web apps are not supported):

- A 24-hour [customer service window](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages#customer-service-windows) is opened (as normal).
- If you respond within 24 hours using any type of message, the message will be free, and a Free Entry Point (“FEP”) window will be opened, starting from the time when you responded.

FEP windows remain open for 72 hours. While open, you can send any type of message to the user at no charge. Note, however, that the customer service window is independent of the FEP window, so if the customer service window closes, you will only be able to send template messages.

## New max-price feature for Marketing Messages API for WhatsApp

Starting in 2026, businesses integrated into Marketing Messages API for WhatsApp can choose to set a [max-price](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/pricing) per marketing message delivery; when a max-price is set, Meta will charge that max-price or lower for delivery.

## New pricing policy for AI Providers leveraging WhatsApp Business Platform

Click [here](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/ai-providers) to learn more about our new pricing policy for “AI Providers” leveraging WhatsApp Business Platform, which is effective February 16, 2026 and updated as of March 4, 2026.

## Analytics

Use the [pricing_analytics field](https://developers.facebook.com/documentation/business-messaging/whatsapp/analytics#pricing-analytics) to get per-message pricing breakdowns and tiering information for delivered messages.

## Webhooks

Billable messages have `type` set to `regular` in the `pricing` object of status [messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/status) webhooks:

```html
"pricing": {
  "billable": true,
  "pricing_model": "PMP",
  "type": "regular",
  "category": "<PRICING_CATEGORY>"
}
```

The `<PRICING_CATEGORY>` tells you what rate was applied (e.g. `marketing`). See the status messages webhook reference for a list of possible values.

Note that currently, tiering information is not included in any webhooks. Use the [pricing_analytics field](https://developers.facebook.com/documentation/business-messaging/whatsapp/analytics#pricing-analytics) to get tiering information for delivered messages.

## Billing

Billing and billing-related actions are handled through the Meta Business Suite. See [About Billing For Your WhatsApp Business Account](https://www.facebook.com/business/help/2225184664363779) for more information.

## WhatsApp Business Calling API pricing

The WhatsApp Business Calling API has different pricing. See our [Calling API pricing document](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/pricing) to learn more.

## Conversation-based pricing

[Conversation-based pricing](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/conversation-based-pricing) is deprecated. It was replaced with per-message pricing on July 1, 2025.
