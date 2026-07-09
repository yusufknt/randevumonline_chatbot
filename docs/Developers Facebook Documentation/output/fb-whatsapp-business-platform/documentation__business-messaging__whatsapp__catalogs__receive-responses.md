# Receive responses from customers | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/catalogs/receive-responses_

---

# Receive responses from customers

Updated: Mar 3, 2026

After receiving single- or multi-product messages, WhatsApp users can ask for more information about a product or place an order. These actions are communicated via the [messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages) webhook.

## Sent message status

Sent message statuses (sent, delivered, read) are described in [status messages webhooks](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/status).

## Asking for information

Whenever a WhatsApp user receives a single- or multi-product message, they can ask for more information by sending you a text message in an existing WhatsApp thread, or by tapping a **Message business** or **Message** button when viewing a specific product.

Messages sent after tapping a **Message business** or **Message** button are described in [text messages webhooks](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/text) and a `context` property will be included, whose value is an object describing the product the user was viewing when they tapped the button.

## Orders

When a WhatsApp user adds one or more products to their WhatsApp shopping cart and places an order, the [order messages webhook](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/order) is triggered, describing the contents of the order. Use the order contents to fulfill the order.
