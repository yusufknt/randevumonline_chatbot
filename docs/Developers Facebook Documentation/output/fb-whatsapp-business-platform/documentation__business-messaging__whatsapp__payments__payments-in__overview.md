# Payments API — India | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/overview_

---

# Payments API — India

Updated: Nov 26, 2025

The Payments API enables you to accept payments from your customers through all UPI apps installed on their devices and other payment methods like cards, NetBanking, and wallets via WhatsApp.

You can send invoice (`order_details`) messages to your customers, then get notified about payment status updates through webhook notifications from the payment gateway.

## Know the differences in the models of integration

The integration model you use depends on your payment gateway. The two models differ in the following ways:

1. **[UPI Intent Mode](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/upi-intent)** : This mode can be used with any Payment Gateway provided they support UPI Intent generation.
2. **[Payment Gateway Deep Integration Mode](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/pg)** : Currently supported for Razorpay, PayU, Billdesk and Zaakpay only.

| User Experience | UPI Intent Mode | Payment Gateway Deep Integration Mode |
| --- | --- | --- |
| **Native support for “Other payment methods”**<br>For example: Netbanking, cards, wallets | ❌<br>Alternative: Send payment links | ✅ |
| **Native support for UPI Intent** | ✅ | ✅ |
| **Native Payment Status Notification** | ❌ | ✅ |

| Integration Features | UPI Intent Mode | Payment Gateway Deep Integration Mode |
| --- | --- | --- |
| **Refunds from WhatsApp APIs** | ❌ | ✅ |
| **Payment Status from WhatsApp webhooks** | ❌ | ✅ |

## Prerequisites for integration

1. **Essential Payments APIs are available at SP/TP**
2. **Access to merchant order trigger APIs / CSVs** needed to trigger an order. (for example, amount, goods or service details)
3. **Access to payment posting APIs** needed to close an order (for example, ticket generation APIs to create tickets once payment is received)

### Full payment gateway deep integration mode

1. **Find out payment gateway account owner** : This authorizes linking the account to WhatsApp Business Manager.

### UPI Intent mode

1. **Find out VPA IDs, MCC, and PC** for your business from the merchant’s payment gateway.
2. **Access to payment gateway API docs** :
3. UPI Intent S2S calls
4. Webhook configuration for payment status

## Example use cases and features needed

| Use case | Essential Feature Set |
| --- | --- |
| **Buying Tickets**<br>For example: Metro, bus, event tickets | Order Details MessagePayment Status Webhook/APIOrder Status MessageRefund |
| **Payment Reminders**<br>Example: Bill payments, subscription renewals, insurance renewals | Order Details TemplatePayment Status Webhook/APIOrder Status MessageRefund |

## Support

- In case you run into an issue, reach out to [direct support](https://business.facebook.com/direct-support/) . *Make sure to choose the correct case type: **“WaBiz: Business Payments API”** so you get a faster resolution.*
- [Sign up for office hours](https://outlook.office365.com/owa/calendar/WhatsappBusinessPaymentsIndiaOfficeHourse@meta.com/bookings/) . *Make sure to write down your issues in the form provided*
