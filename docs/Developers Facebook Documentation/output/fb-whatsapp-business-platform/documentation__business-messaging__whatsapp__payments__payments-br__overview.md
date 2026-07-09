# Payments API - Brazil | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/overview_

---

# Payments API - Brazil

Updated: Nov 14, 2025

Payments API enable businesses to accept payments from their customers via WhatsApp. Businesses send `order_details` messages ([Orders API](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/orders)) to their customers, then get notified about payment status updates via webhook notifications.

Based on the selected use case, businesses can collect payment from the customers using one of the following integrations:

- [Dynamic Pix Codes](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/offsite-pix)
- [Payment Links](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/payment-links)
- [Boleto](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/boleto)
- [One-click offsite card payment](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/one-click-payments)
- [Order Details Template](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/orderdetailstemplate)

## How It Works

First, the business composes and sends an `order_details` message, which is a new type of interactive message. It contains the same 4 main components: header, body, footer, and action. Inside the action component, the business includes all the information needed for the customer to complete their payment.

Each `order_details` message **must** contain a **unique `reference_id`** provided by the business. This reference id is used throughout the flow to track the order.

Once the message is sent, the business waits for a payment or transaction status update. The type of the update depends on the integration type (e.g.: [Pix](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/offsite-pix), [Payment Links](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/payment-links), etc.). WhatsApp does **NOT** support payment reconciliations. The business must reconcile the payment with their payment service provider (PSP) using the `reference_id` of the order.

## Purchase Flow in App

In the WhatsApp customer app, the purchase flow has the following steps:

1. Buyers communicate with businesses and select a product.
2. Businesses send an `order_details` message to the buyer.
3. Buyers pay the order. For Pix, they will switch to their bank app and use the Pix Copy and Paste functionality. For Payment Links, the payment/checkout link opens in the web browser, and they complete the payment there.
4. Businesses send an `order_status` message indicating that the order is now `processing` .
