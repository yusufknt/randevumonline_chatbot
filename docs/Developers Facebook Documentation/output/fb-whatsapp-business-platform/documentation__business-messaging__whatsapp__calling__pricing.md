# Calling API Pricing | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/pricing_

---

# Calling API Pricing

Updated: Mar 30, 2026

**All user-initiated calls are free.**

## Overview

Businesses are charged for calls based on:

- Duration of the call (calculated in six-second pulses)
- Country code of the phone number being called
- Volume tier (based on minutes called within the calendar month) using same [tiering accrual](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing#tiering-accrual) as messaging

Note: Our systems count fractional pulses as one pulse. For example, a 56-second call (9.33 pulses) would be counted as 10 pulses.

For calls that cross pricing tiers (for example from the 0 - 50,000 tier to the 50,001 - 250,000 tier), the entire call is priced at the lower rate (that is, the rate of the higher volume tier).

A valid payment method is required to place calls.

**Note:** Call permission request messages are subject to [per-messaging pricing](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing).

## Rate cards and volume tiers

These rate cards represent the current rates and volume tiers for the WhatsApp Business Calling API, effective April 1, 2026, based on WhatsApp Business Account timezone.

| Currency | Rates |
| --- | --- |
| USD | USD rates |
| AED | AED rates |
| ARS | ARS rates |
| AUD | AUD rates |
| CLP | CLP rates |
| COP | COP rates |
| EUR | EUR rates |
| GBP | GBP rates |
| IDR | IDR rates |
| INR | INR rates |
| MXN | MXN rates |
| MYR | MYR rates |
| PEN | PEN rates |
| SAR | SAR rates |
| SGD | SGD rates |

### Updates to rate cards

**Previous updates**

- Effective April 1, 2026 – 8 new billing currencies introduced: AED (United Arab Emirates), ARS (Argentina), CLP (Chile), COP (Colombia), MYR (Malaysia), PEN (Peru), SAR (Saudi Arabia), SGD (Singapore).
- Effective January 1, 2026 – MXN (Mexico) rates introduced.

## How calling changes the 24 hour customer service window

Currently, when a WhatsApp user messages you, a [24-hour timer called a customer service window](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages#customer-service-windows) begins, or refreshes.

When you are within the window, your business can send any type of message to the WhatsApp user, which is otherwise not allowed.

With the introduction of the Calling API, the customer service window now also starts or refreshes for calls:

- When a WhatsApp user calls you, regardless of if you accept the call or not
- When a WhatsApp user accepts your call.

## Get cost and call analytics

Use the [WhatsApp Business Account API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/whatsapp-business-account-api#get-version-waba-id) with a `?fields=call_analytics` query parameter to obtain call analytics for your WhatsApp Business Account (WABA).

The endpoints can provide useful information like cost, counts of completed calls, and average call duration. Learn more about [call analytics](https://developers.facebook.com/documentation/business-messaging/whatsapp/analytics#call-analytics).
