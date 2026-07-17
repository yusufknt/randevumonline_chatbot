# Conversation-based pricing (DEPRECATED) | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/conversation-based-pricing_

---

# Conversation-based pricing (DEPRECATED)

Updated: Nov 14, 2025

Conversation-based pricing is deprecated. It was replaced on July 1, 2025, with [per-message pricing](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing). The document below is for reference purposes only.

This document explains how conversation-based pricing works on the WhatsApp Business Platform.

Charges are applied per conversation, not per individual message sent or received.

Conversations are 24-hour message threads between you and your customers. They are opened and charged when messages you send to customers are delivered. The criteria that determines when a conversation is opened and how it is categorized is explained below.

Businesses are responsible for reviewing the category assigned to their approved templates. Whenever a template is used, a business accepts the charges associated with the category applied to the template at time of use.

## Conversation categories

Conversations are categorized with one of the following categories:

- **Marketing** — Enables you to achieve a wide range of goals, from generating awareness to driving sales and retargeting customers. Examples include new product, service, or feature announcements, targeted promotions/offers, and cart abandonment reminders.
- **Utility** — Enables you to follow-up on user actions or requests. Examples include opt-in confirmation, order/delivery management (e.g., delivery update); account updates or alerts (for example., payment reminder); or feedback surveys.
- **Authentication** — Enables you authenticate users with one-time pass codes, potentially at multiple steps in the login process (e.g., account verification, account recovery, integrity challenges).
- **Service** — Enables you to resolve customer inquiries.

Marketing, utility, and authentication conversations can only be opened with template messages. Service conversations can be opened with any type of message other than a template message.

See [Message Types](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages#message-types) to learn more about the various types of messages you can send to customers.

## Opening conversations

Conversations are opened when you send a message to a customer under the following conditions.

### Marketing, Utility, and Authentication Conversations

When you send an approved marketing, utility, or authentication template to a customer, we check if an open conversation matching the template’s **category** already exists between you and the customer. If one exists, no new conversation is opened. If one does not exist, a new **conversation of that category** is opened, lasting 24 hours.

For example:

- **Hour 0:** You send a targeted promotion (marketing [template message](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview) ) to a customer. No open marketing conversation exists between you and the customer, so a marketing conversation lasting 24 hours is opened.
- **Hour 4:** The customer completes an order on your site, so you send them an order confirmation (utility template message). No open utility conversation exists between you and the customer, so a utility conversation lasting 24 hours is opened.
- **Hour 10:** You send a shipment confirmation (utility template message) to the customer. An open utility conversation already exists between you and the customer, so a new utility conversation is not opened.

To learn more about template categories and how to choose an appropriate category when creating templates, see [Template Categorization](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-categorization).

For additional examples, see our pricing explainer PDF.

### Service conversations

Service conversations are now free. This change does not affect how service conversations are opened.

A service conversation is opened when any message other than a template message is delivered to your customer and no open conversation of **any category** exists between you and the customer.

Note that a [customer service window](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages#customer-service-windows) must exist between you and the customer before you can send them a non-template message.

For example:

- **Hour 0:** You send a targeted promotion (marketing template) to a customer. No open marketing conversation exists between you and the customer, so a marketing conversation lasting 24 hours is opened.
- **Hour 4:** The customer messages you. This opens a customer service window between you and the customer, allowing you to send them any type of message for the next 24 hours.
- **Hour 5:** You send an interactive list message to the customer. An open conversation already exists between you and the customer (a marketing conversation in this case), so a service conversation is not opened.
- **Hour 24:** The marketing conversation expires.
- **Hour 25:** The 24-hour customer service window is still open, so you send a second text message to the customer. No open conversation exists between you and the customer anymore, so a service conversation is opened, lasting 24 hours.
- **Hour 26:** The 24-hour customer service window is still open, so you send a third text message to the customer. An open service conversation already exists between you and the customer, so a new service conversation is not opened.

For additional examples, see our pricing explainer PDF.

## Customer Service Windows

See [Customer Service Windows](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages#customer-service-windows).

## Conversation duration

Marketing, utility, authentication, and service conversations last 24 hours unless closed by a newly opened [free-entry point conversation](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/conversation-based-pricing#free-entry-point-conversations).

Free-entry point conversations last 72 hours.

## Multiple conversations

It is possible to have multiple open conversations between you and a customer. This can happen in the following situations:

- An open marketing, utility, or authentication conversation exists between you and a customer and you send them a template message of a different category within 24 hours.
- An open service conversation exists between you and a customer and you send them a template message within 24 hours.

## Free Tier conversations

As of November 1, 2024, you can open an unlimited number of service conversations at no charge. See [Free Service Conversations](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/conversation-based-pricing) to learn more.

## Free Entry Point conversations

A free entry point conversation is opened if (1) a customer using a device running Android or iOS (the desktop and web clients are not supported) messages you via a [Click to WhatsApp Ad](https://www.facebook.com/business/help/447934475640650/) or [Facebook Page Call-to-Action](https://www.facebook.com/help/977869848936797) button and (2) you respond within 24 hours. If you do not respond within 24 hours, a free entry point conversation is not opened and you must use a template to message the customer, which opens a marketing, utility, or authentication conversation, per the category of the template.

The free entry point conversation is opened as soon as your message is delivered and lasts 72 hours. When a free entry point conversation is opened, it automatically closes all other open conversations between you and the customer, and no new conversations will be opened until the free entry point conversation expires.

Once the free entry point conversation is opened, you can send any type of message to the customer without incurring additional charges. However, you can only send non-templates messages if there is an open customer service window between you and the customer.

For example, if the customer messages you via a Click to WhatsApp Ad at 10am and you respond via a template message at 10pm the same day:

- The free entry point conversation starts at 10pm and lasts 72 hours.
- You can send template messages at no charge in those 72 hours.
- You can send non-template messages until 10am the next day, at which point the [customer service window](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages#customer-service-windows) closes, as it is independent of the free entry point conversation (if the customer messages you again, however, it opens another 24-hour customer service window in which you can send any type of message).

## Rates

Rates vary based on conversation category and country/region rate. You can download the rate card below that corresponds to your WhatsApp Business Account’s currency to see our rates by country/region for each conversation category.

These rates apply for any conversation opened on or after June 1, 2023 at 12:00 AM, based on WhatsApp Business Account time zone.

### Rate Cards

These rate cards represent the current rates on our platform.

- Rates in USD
- Rates in INR
- Rates in IDR
- Rates in EUR
- Rates in GBP
- Rates in AUD

### Authentication-International rates

Starting June 1, 2024, we are introducing authentication-international rates. See [Authentication-International Rates](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/authentication-international-rates) to learn about these rates and if they apply to you.

Effective April 1, 2025, we are lowering our authentication-international rates in Egypt, Nigeria, Pakistan and South Africa, as part of continued efforts to ensure our prices are on-par with alternate channels.

### Marketing Messages API for WhatsApp pricing

Per-message pricing is coming to Marketing Messages API for WhatsApp. Starting July 1, 2025, Cloud API marketing rates will apply to messages sent via Marketing Messages API for WhatsApp.

Marketing Messages API for WhatsApp has different pricing. View the [Marketing Messages API for WhatsApp pricing document](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing) for details.

### WhatsApp Business Calling API pricing

The WhatsApp Business Calling API has different pricing. View the [Calling API pricing document](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/pricing) for details.

### Updates to rate cards

As announced in June 2024, we may update rates up-to-quarterly. For marketing, updates are to reflect demand and the value these messages deliver. For utility and authentication, our objective is to price on-par with alternate channels.

To support these efforts, we have made the following updates:

- Effective April 1, 2025 Lowered [authentication-international pricing rates](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/authentication-international-rates) for Egypt, Nigeria, Pakistan, and South Africa.
- Effective February 1, 2025 Lowered [authentication pricing rates](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing#rates) for Egypt, Malaysia, Nigeria, Pakistan, Saudi Arabia, South Africa, and the United Arab Emirates.Added [authentication-international pricing rates](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/authentication-international-rates) for Egypt, Malaysia, Nigeria, Pakistan, Saudi Arabia, South Africa, and the United Arab Emirates.
- Effective November 1, 2024 [Service conversations](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing#service-conversations) are now free for all businesses, including via AI-enabled conversational experiences.
- Effective October 1, 2024 Updated [pricing rates](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing#rates) in India, Saudi Arabia, the United Arab Emirates, and the United Kingdom.
- Effective August 1, 2024 Lowered utility conversation [pricing rates](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing#rates).

### Country calling codes

Charges for conversations are based on the country of the user’s phone number. We rely on your customer’s country calling code and network prefix (area code) to determine their country. The table below shows how we map country codes to countries or regions. If a country is not listed below, it maps to Other.

| Markets | Calling Code<br>(and network prefix if applicable) |
| --- | --- |
| Countries<br>ArgentinaBrazilChileColombiaEgyptFranceGermanyIndiaIndonesiaIsraelItalyMalaysiaMexicoNetherlandsNigeriaPakistanPeruRussiaSaudi ArabiaSouth AfricaSpainTurkeyUnited Arab EmiratesUnited Kingdom | 545556572033499162972396052312349251796627349097144 |
| North America<br>Canada<br><br>United States | 1<br><br>1 |
| Rest of Africa<br>Algeria<br><br>Angola<br><br>Benin<br><br>Botswana<br><br>Burkina Faso<br><br>Burundi<br><br>Cameroon<br><br>Chad<br><br>Republic of the Congo (Brazzaville)<br><br>Eritrea<br><br>Ethiopia<br><br>Gabon<br><br>Gambia<br><br>Ghana<br><br>Guinea-Bissau<br><br>Ivory Coast<br><br>Kenya<br><br>Lesotho<br><br>Liberia<br><br>Libya<br><br>Madagascar<br><br>Malawi<br><br>Mali<br><br>Mauritania<br><br>Morocco<br><br>Mozambique<br><br>Namibia<br><br>Niger<br><br>Rwanda<br><br>Senegal<br><br>Sierra Leone<br><br>Somalia<br><br>South Sudan<br><br>Sudan<br><br>Swaziland<br><br>Tanzania<br><br>Togo<br><br>Tunisia<br><br>Uganda<br><br>Zambia | 213<br><br>244<br><br>229<br><br>267<br><br>226<br><br>257<br><br>237<br><br>235<br><br>242<br><br>291<br><br>251<br><br>241<br><br>220<br><br>233<br><br>245<br><br>225<br><br>254<br><br>266<br><br>231<br><br>218<br><br>261<br><br>265<br><br>223<br><br>222<br><br>212<br><br>258<br><br>264<br><br>227<br><br>250<br><br>221<br><br>232<br><br>252<br><br>211<br><br>249<br><br>268<br><br>255<br><br>228<br><br>216<br><br>256<br><br>260 |
| Rest of Asia Pacific<br>Afghanistan<br><br>Australia<br><br>Bangladesh<br><br>Cambodia<br><br>China<br><br>Hong Kong<br><br>Japan<br><br>Laos<br><br>Mongolia<br><br>Nepal<br><br>New Zealand<br><br>Papua New Guinea<br><br>Philippines<br><br>Singapore<br><br>Sri Lanka<br><br>Taiwan<br><br>Tajikistan<br><br>Thailand<br><br>Turkmenistan<br><br>Uzbekistan<br><br>Vietnam | 93<br><br>61<br><br>880<br><br>855<br><br>86<br><br>852<br><br>81<br><br>856<br><br>976<br><br>977<br><br>64<br><br>675<br><br>63<br><br>65<br><br>94<br><br>886<br><br>992<br><br>66<br><br>993<br><br>998<br><br>84 |
| Rest of Central & Eastern Europe<br>Albania<br><br>Armenia<br><br>Azerbaijan<br><br>Belarus<br><br>Bulgaria<br><br>Croatia<br><br>Czech Republic<br><br>Georgia<br><br>Greece<br><br>Hungary<br><br>Latvia<br><br>Lithuania<br><br>Moldova<br><br>North Macedonia<br><br>Poland<br><br>Romania<br><br>Serbia<br><br>Slovakia<br><br>Slovenia<br><br>Ukraine | 355<br><br>374<br><br>994<br><br>375<br><br>359<br><br>385<br><br>420<br><br>995<br><br>30<br><br>36<br><br>371<br><br>370<br><br>373<br><br>389<br><br>48<br><br>40<br><br>381<br><br>421<br><br>386<br><br>380 |
| Rest of Western Europe<br>Austria<br><br>Belgium<br><br>Denmark<br><br>Finland<br><br>Ireland<br><br>Norway<br><br>Portugal<br><br>Sweden<br><br>Switzerland | 43<br><br>32<br><br>45<br><br>358<br><br>353<br><br>47<br><br>351<br><br>46<br><br>41 |
| Rest of Latin America<br>Bolivia<br><br>Costa Rica<br><br>Dominican Republic<br><br>Ecuador<br><br>El Salvador<br><br>Guatemala<br><br>Haiti<br><br>Honduras<br><br>Jamaica<br><br>Nicaragua<br><br>Panama<br><br>Paraguay<br><br>Puerto Rico<br><br>Uruguay<br><br>Venezuela | 591<br><br>506<br><br>1 (809, 829, 849)<br><br>593<br><br>503<br><br>502<br><br>509<br><br>504<br><br>1 (658, 876)<br><br>505<br><br>507<br><br>595<br><br>1 (787, 939)<br><br>598<br><br>58 |
| Rest of Middle East<br>Bahrain<br><br>Iraq<br><br>Jordan<br><br>Kuwait<br><br>Lebanon<br><br>Oman<br><br>Qatar<br><br>Yemen | 973<br><br>964<br><br>962<br><br>965<br><br>961<br><br>968<br><br>974<br><br>967 |
| Other<br>All other countries | Varies by country |

The information in the table above is also available in a CSV file:

- Country Calling Codes and Regional Rate Mapping CSV

## Webhooks

Pricing information is included in all message webhooks. See:

- Cloud API: [Message Status Updates](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/status)
- On-Premises API (deprecated): Message Status Updates

## Billing

Billing and billing-related actions are handled through the Meta Business Suite. See [About Billing For Your WhatsApp Business Account](https://www.facebook.com/business/help/2225184664363779) for more information.

## Marketing Messages API for WhatsApp

If you are using the Marketing Messages API for WhatsApp, such usage is subject to Marketing Messages API for WhatsApp pricing. See the [Marketing Messages API for WhatsApp pricing](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing) document for pricing information and rate cards.

## See also

- [Conversations](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages)
- [About Billing For Your WhatsApp Business Account](https://www.facebook.com/business/help/2225184664363779)
- [Pricing](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing)
- [Template Categorization](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-categorization)
- [Sending messages with Cloud API](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages)
