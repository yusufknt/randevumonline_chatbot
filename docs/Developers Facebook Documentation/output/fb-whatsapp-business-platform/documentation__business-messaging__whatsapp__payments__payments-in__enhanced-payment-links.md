# Enhanced Payment Links | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/enhanced-payment-links_

---

# Enhanced Payment Links

Updated: Dec 12, 2025

## Overview

Enhanced Payment Links is a feature that transforms existing payment gateway URLs into rich, native payment experiences within WhatsApp.

It converts existing payment links into an in-app checkout flow - no changes to your payment backend, reconciliation, or callback setup are required. When a supported payment link is sent through a message template, it automatically renders as a structured payment bubble featuring:

- **Amount and currency** clearly displayed
- **“Pay Now” CTA** for seamless checkout
- **In-app checkout** via UPI Intent or hosted payment page

This feature significantly improves payment conversion rates by reducing checkout friction and increasing consumer trust.

**Superfast Setup**: Merchants can independently create the required [WhatsApp templates](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/enhanced-payment-links#template-requirements) and embed payment links from [supported payment gateways](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/enhanced-payment-links#supported-payment-gateways) - no BSP involvement is needed.

This feature is not publicly available yet. To request access, please reach out to your BSP or Meta representative with your **WABA ID**, **sample payment link**, and **preferred Payment Gateway** (Razorpay, PayU, or Cashfree).

## User Experience

On supported WhatsApp versions, the payment link renders as an enhanced bubble:

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/564690767_1339318147926836_7876647427034457125_n.jpg?_nc_cat=102&ccb=1-7&_nc_sid=e280be&_nc_ohc=q6s_0wSoo7kQ7kNvwEclcDT&_nc_oc=AdomiHmPmGZ7FfiafzwcbeLI3KcSsY-UuyrHcX6iX77lqwAqWJISQ9E_8D7Ebaxfwgk&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=j5dgOC5wCEL93W9PxN7LYg&_nc_ss=7b20f&oh=00_Af6IqF-DbMgB79x-pFMMVhF4fbRDBeyvEMojG81QjmhRqQ&oe=6A1C2D93)

1. **Rich Payment Card** : Displays Amount, currency, and CTA button
2. **In-App Checkout** : *UPI*: Direct app-switch to UPI apps (Google Pay, PhonePe, Paytm, etc.)*Other methods*: In-app browser for cards, net banking, or wallets
3. **Automatic Status Updates** : The payment card automatically updates to reflect the payment status on completion or expiry, and disables the “Pay Now” button to prevent duplicate payments.

## Prerequisites

Enhanced Payment Links is an experience that works with both existing BSP APIs and WhatsApp Business Cloud API. Neither BSPs nor merchants need to make any backend, API, reconciliation, or callback changes to enable this feature. Your existing payment gateway integration remains completely unchanged.

To use Enhanced Payment Links:

| Requirement | Description |
| --- | --- |
| **Allowlisted WABA** | Your WABA ID must be enabled for Enhanced Payment Links. Submit a request to your BSP or Meta representative with your WABA ID, preferred payment gateway(s), and sample payment links for validation. |
| **Supported Payment Gateway** | An active account with Razorpay, PayU, or Cashfree |
| **Compliant Template** | A message template configured with no header and a dynamic URL button (see<br>[Template Requirements](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/enhanced-payment-links#template-requirements)<br>) |

### Supported Payment Gateways

| Payment Gateway | Status |
| --- | --- |
| Razorpay | ✅ Supported |
| PayU | ✅ Supported |
| Cashfree | ✅ Supported |

## Integration Flow

The following diagram illustrates the end-to-end flow, from sending an Enhanced Payment Link to payment completion and callbacks:

![End-to-end EPL flow: Merchant creates payment link via PG, sends template message, consumer pays in-app, PG sends webhook to merchant (unchanged), WhatsApp updates payment card automatically](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/651759898_1455745979617385_4466368405017366786_n.png?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=TWFlr_cckDUQ7kNvwEn9P2R&_nc_oc=AdqfGNM_GkrTs82Fu6jTkW6h0XQ1Th8lmXZ-fYySMLb18axJ3-w7hlThvjXe4mtHgyU&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=j5dgOC5wCEL93W9PxN7LYg&_nc_ss=7b20f&oh=00_Af7DxG_tiX7tIrGLU4ub2hArNe0yJil7WXr24fgE18dmSg&oe=6A1C1E90)

**Steps:**

1. **Generate payment link** - Your server calls the payment gateway API (Razorpay, PayU, or Cashfree) to create a payment link for the transaction.
2. **Receive payment link URL** - The payment gateway returns a URL (for example, `https://rzp.io/i/abc123XYZ` ).
3. **Send template message** - Your server sends a template message via the Cloud API or your BSP, embedding the dynamic portion of the payment link (the suffix) in the button component.
4. **Message delivered on WhatsApp** - The consumer receives an enhanced payment bubble with the amount, currency, and a “Pay Now” button for in-app checkout.
5. **Consumer completes payment** - The consumer taps “Pay Now” and pays via UPI apps, cards, net banking, or wallets within WhatsApp.
6. **Payment gateway sends callback to merchant** - Your existing webhook endpoint receives the payment status callback with the same payload format as before. No changes to your webhook URL, payload handling, or reconciliation logic are needed.
7. **WhatsApp updates the payment card** - The payment card automatically reflects the payment status (success, or expiry) and disables the “Pay Now” button to prevent duplicate payments. This happens independently and requires no merchant action.

## Template Requirements

Enhanced Payment Link templates must follow these constraints:

| Component | Requirement |
| --- | --- |
| **Header** | None — templates must<br>**not**<br>include a media header (image, video, or document) |
| **Button** | Exactly<br>**one**<br>dynamic URL button with a<br>[supported PG link prefix](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/enhanced-payment-links#dynamic-url-prefix-configuration) |

Merchants can independently create these templates without involving their BSP. Templates can be created using any one of the following methods:

1. [Template Library](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-library) (recommended)
2. [WhatsApp Manager](https://business.facebook.com/wa/manage/message-templates)
3. [Business Management API](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview)
4. BSP Dashboard

### Example Template Configuration

Your business can enable customers to pay using their favorite UPI apps or other payment methods accepted by supporting Payment Gateways without leaving WhatsApp.

```bash
Body: "Hi 1, reminder to pay for your insurance renewal #2. Amount: ₹3"

Button:
  - Type of Action: "Visit website"
  - Button Text: "Pay Now"
  - URL Type: Dynamic
  - Website URL: https://pg.io/i/
```

**Important**: The button URL must be configured as **dynamic** to pass the payment link at send time.

### Dynamic URL Prefix Configuration

When creating your template, the dynamic URL button requires a **URL prefix** that matches your payment gateway’s domain. Use one of the following prefixes based on your PG:

Razorpay

| URL Prefix |
| --- |
| `https://rzp.io/rzp/` |
| `https://rzp.io/i/` |

PayU

| URL Prefix |
| --- |
| `https://pmny.in/PAYUMN/` |
| `https://api.payu.in/` |
| `https://u.payu.in/PAYUMN/` |

Cashfree

| URL Prefix |
| --- |
| `https://payments.cashfree.com/links` |
| `https://payments.cashfree.com/link/` |
| `https://cfre.in/CSHFRE/` |

**Note**: The URL prefix you configure in your template must match the format of payment links generated by your PG. When sending the message, pass only the dynamic portion (e.g., the link ID) in the button parameter.

## Payment Link Requirements

| Requirement | Details |
| --- | --- |
| Environment | Must be from production environment (not sandbox/test mode) |
| Status | Link must be active and not expired |
| Gateway | Must be from a supported PG (see<br>[Supported Payment Gateways](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/enhanced-payment-links#supported-payment-gateways)<br>) |
| URL Format | Must match one of the supported URL prefixes for your PG |

**Using wrapped or redirected payment links?** Enhanced Payment Links requires direct payment gateway URLs that match the [supported URL prefixes](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/enhanced-payment-links#dynamic-url-prefix-configuration). If your implementation wraps payment gateway links under your own domain (e.g., `yourdomain.com/pay/...`) or redirects to the payment gateway from a hosted page, the enhanced experience will not render automatically. In such cases, you will need to update your workflow to pass the direct payment gateway link in the template button instead of your wrapped or redirected URL.

### Generating Payment Links

Refer to your payment gateway’s documentation:

- **Razorpay** : [Create Payment Link (API)](https://razorpay.com/docs/api/payments/payment-links/create-standard/) [Dashboard](https://razorpay.com/docs/payments/payment-links/create/)
- **PayU** : [Payment Links](https://docs.payu.in/reference/create-payment-links)
- **Cashfree** : [Payment Links](https://www.cashfree.com/docs/payments/no-code/payment-link)

## Sending Payment Links

Use the Cloud API to send a template containing the payment link.

### Request

```bash
POST /{phone-number-id}/messages
```

### Example

```bash
curl -X POST "https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/messages" \
  -H "Authorization: Bearer {ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "messaging_product": "whatsapp",
    "to": "919876543210",
    "type": "template",
    "template": {
      "name": "payment_reminder",
      "language": {
        "code": "en"
      },
      "components": [
        {
          "type": "body",
          "parameters": [
            {"type": "text", "text": "Rishi"},
            {"type": "text", "text": "ORD-12345"},
            {"type": "text", "text": "1,999"}
          ]
        },
        {
          "type": "button",
          "sub_type": "url",
          "index": "0",
          "parameters": [
            {
              "type": "text",
              "text": "abc123XYZ"
            }
          ]
        }
      ]
    }
  }'
```

In this example, if the template URL prefix is https://pg.io/i/, the final URL becomes https://pg.io/i/abc123XYZ.

### Button Component

The payment link suffix is passed in the button component:

```json
{
  "type": "button",
  "sub_type": "url",
  "index": "0",
  "parameters": [
    {
      "type": "text",
      "text": "{PAYMENT_LINK_SUFFIX}"
    }
  ]
}
```

| Field | Type | Description |
| --- | --- | --- |
| type | string | Must be “button” |
| sub_type | string | Must be “url” |
| index | string | Button index, “0” for the first button |
| parameters[].type | string | Must be “text” |
| parameters[].text | string | The dynamic portion of the payment link URL (appended to the template’s URL prefix) |

## Payment Reconciliation and Callbacks

Enhanced Payment Links does not modify your existing payment processing or backend infrastructure. This means:

| Aspect | Impact |
| --- | --- |
| **Payment callbacks/webhooks** | No change. Your existing webhook endpoints and callback flows from your payment gateway continue to work as-is. |
| **Reconciliation** | No change. Reconciliation remains the same as configured on your payment gateway (Razorpay, PayU, or Cashfree). |
| **Settlement** | No change. Settlement flows and timelines are unaffected. |

No backend integration changes are required to adopt Enhanced Payment Links.

## Reporting

Reporting for Enhanced Payment Links is split across two sources:

| Metric | Source | Details |
| --- | --- | --- |
| **Link clicks** | WhatsApp | Click metrics on payment gateway links are available from WhatsApp analytics. |
| **Payment status, success/failure rates, refunds, settlements** | Payment gateway | All payment-level reporting remains on your payment gateway (Razorpay, PayU, or Cashfree). Use your existing dashboards and reports. |

No additional reporting setup is required. WhatsApp provides visibility into link engagement, while your payment gateway continues to be the source of truth for all payment and transaction metrics.

## Best Practices

| Practice | Details |
| --- | --- |
| **Use production links** | Sandbox/test links will not render enhanced bubbles |
| **Set reasonable expiry** | 24-48 hours balances conversion and security |
| **Include context** | Add amount and order details in the message body |
| **One button only** | Multiple buttons are not supported |
| **Match URL prefix** | Ensure template URL prefix matches your PG’s link format |

## Limitations

- Only **one payment link** per template message
- **No header** components allowed
- **Single button** required
- Enhanced rendering depends on recipient’s WhatsApp version
- Currently available for **India** only
- **Payment metrics behavior** : Enhanced Payment Links create a UPI intent on every “Pay now” tap. This means: Total payment attempt counts will be higher than pre-EPLExpired intents are reported as failures, which may inflate failure rates (eg: Razorpay webhooks for expired UPI intents: “Payment was unsuccessful as you could not complete it in time”)**Recommendation**: Exclude payment expiry errors when calculating your success metrics.

## Troubleshooting

### Payment link not rendering as enhanced bubble

| Check | Action |
| --- | --- |
| WABA allowlisted? | Confirm with your BSP or Meta representative |
| Supported PG? | Must be Razorpay, PayU, or Cashfree |
| URL prefix correct? | Template URL prefix must match your PG’s supported formats |
| Link active? | Verify link hasn’t expired |
| Template compliant? | No header, single dynamic URL button |

**Note**: If your template gets miscategorized, you can appeal the assigned category. See the [Template Categorization Guide](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-categorization) for details on the appeal process. To avoid categorization uncertainty altogether, consider using a [**Utility Template**](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-library) from the template library, this ensures correct categorization and provides guidance on template content structure.

## Getting Help

- **Direct API users or Meta Managed Businesses** : Contact your Meta representative
- **BSP partners** : Reach out to your BSP for integration support
- **Payment gateway issues** : Consult your PG’s documentation or support team

*See also: [Message Templates](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview), [Cloud API Messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api), [Payments Overview](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/overview)*
