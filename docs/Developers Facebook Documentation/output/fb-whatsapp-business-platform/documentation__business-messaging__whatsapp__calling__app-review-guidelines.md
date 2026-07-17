# Calling API App Review Guidelines | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/app-review-guidelines_

---

# Calling API App Review Guidelines

Updated: Nov 21, 2025

## Overview

The official page referenced by reviewers is [/docs/permissions#w](https://developers.facebook.com/docs/permissions#w). Use this guide as complementary to that page but treat that page as the official source when in doubt.

This page provides details to improve your chances of a successful App Review specifically for WhatsApp Business Calling API features.

## Guidelines

### For the WhatsApp business management permission

You should clearly show that your application can enable and disable calling features by displaying whether the Call Button icon is visible.

Share a video of you enabling and disabling the Call Button icon for the WhatsApp business either via cURL request, or via settings within your application UI.

Do this by enabling and disabling calling features, not simply toggling Call Button icon visibility.

- [Learn how to enable and disable Calling API features via API](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/call-settings#configure-update-business-phone-number-calling-settings)
- [Learn how to enable and disable Calling API features in WhatsApp Manager](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/call-settings#call-settings-in-whatsapp-manager)

Example

1. Display a chat thread between your business and a WhatsApp user that does not have the Call Button icon.
2. Use your developer app to enable Calling API features on the business phone number, which will display the Call Button icon.
3. Return to the same chat thread and display that the Call Button icon is visible.

### For the WhatsApp business messaging permission

You should clearly demonstrate your application can support **either of the following use cases:**

Use case 1: Place a business-initiated call

Share a video of you using your application to place a business-initiated call. Then display a user accepting the call on a WhatsApp mobile client.

Use case 2: Receive a user-initiated call

Share a video of a user placing a call to your business phone number. Then show your application receiving the incoming call.

Show either:

1. The incoming call in the WhatsApp client application UI.
2. The calling webhook as delivered to your application.
