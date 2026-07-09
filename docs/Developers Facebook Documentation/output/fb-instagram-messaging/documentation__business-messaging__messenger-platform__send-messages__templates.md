# Message Templates | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/templates_

---

# Message Templates

Updated: May 5, 2026

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/653709044_1459945712530745_8920098130391271130_n.png?_nc_cat=102&ccb=1-7&_nc_sid=e280be&_nc_ohc=G_l8sNkHU_AQ7kNvwGpb-3A&_nc_oc=Ado16pdB3nlAckXiu4D6eFIkoE-ERnnFy9cKePB83TBEKBUB9zz0x6t9_qnPC4iHrY0&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=pB1uQCOwWBPyzeUKQxYnlg&_nc_ss=7b20f&oh=00_Af7nQ5sKc-kXHO3XR1bZC_HOTbCGAiADRV_WzCttD1CsKQ&oe=6A1C1CC8)

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/651905094_1459945655864084_7491184152236363977_n.png?_nc_cat=111&ccb=1-7&_nc_sid=e280be&_nc_ohc=uSNr2xj3mEsQ7kNvwG4susF&_nc_oc=AdqEPP2lX-j7ZpG5FMVuw7Y4rWVmOYgFJNrJif9ucMiJjcc5iJbFQmMRz_5LBHgZTO4&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=pB1uQCOwWBPyzeUKQxYnlg&_nc_ss=7b20f&oh=00_Af5BJbHVmfZdJQGa7KBjcdctsAemy7j9XxcLGjBlMHwc7A&oe=6A1C217F)

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/653709911_1459945609197422_5713478735784336329_n.png?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=oLnAuPT20PsQ7kNvwHeSJc_&_nc_oc=AdpojbdCEgBiq3vSw9hNmpDaMN_VJOJyQE0y_cTdeBbNKgfUy4Kqdwi2pY8O3oCV-i8&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=pB1uQCOwWBPyzeUKQxYnlg&_nc_ss=7b20f&oh=00_Af6qDpBq1tfvdO4j1h9lIOGVBPTAEAkO67uxOEo3Ka6pEg&oe=6A1C17F3)

Message templates offer a way for you to offer a richer in-conversation experience than standard text messages by integrating buttons, images, lists, and more alongside text a single message. Templates can be use for many purposes, such as displaying product information, asking the message recipient to choose from a pre-determined set of options, and showing search results.

## Available templates

The following templates are available for sending structured messages:

| Template | Description | Use case |
| --- | --- | --- |
| [Button](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/template/button) | Text message with up to three attached buttons. | Offer the recipient predefined response options or actions to take. |
| [Generic](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/template/generic) | Structured message with a title, subtitle, image, and up to three buttons. Supports a<br>`default_action`<br>URL. | Display product cards, search results, or content previews. |
| [Media](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/template/media) | Send images, GIFs, or video as a structured message with a button. Videos and GIFs are playable in the conversation. | Share rich media with an optional call-to-action. |
| [Receipt](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/template/receipt) | Order confirmation with order summary, payment details, and shipping information. | Send purchase confirmations and order receipts. |
| [Product](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/template/product) | Renders products from your<br>[catalog](https://www.facebook.com/business/help/1275400645914358)<br>. Product details (image, title, price) are pulled automatically. | Showcase products from your catalog in a conversation. |
| [Coupon](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/template/coupon) | Send a coupon or discount offer in a structured format. | Deliver promotional offers or discount codes. |
| [Customer Feedback](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/templates/customer-feedback-template) | Native feedback survey template for measuring customer experience. Supports rating scales and free-text responses. | Collect customer satisfaction data after a support interaction. |
| [Utility Messaging](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/utility-messages) | Pre-approved template for order updates, account notifications, and appointment reminders with personalized details and call-to-action buttons. | Send transactional updates such as shipping status, appointment reminders, or account alerts. |

## Choosing a template

Use this guide to select the right template for your use case:

- **Presenting options or actions** → [Button template](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/template/button)
- **Displaying a product, article, or content card** → [Generic template](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/template/generic)
- **Sharing an image, GIF, or video** → [Media template](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/template/media)
- **Confirming a purchase or order** → [Receipt template](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/template/receipt)
- **Showcasing catalog products** → [Product template](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/template/product)
- **Sending a promotional offer** → [Coupon template](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/template/coupon)
- **Collecting feedback after an interaction** → [Customer Feedback template](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/templates/customer-feedback-template)
- **Sending transactional updates (orders, appointments, accounts)** → [Utility Messaging template](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/utility-messages)

## Send a Message Template

To send a message template, send a `POST` request to the `/<PAGE_ID>/messages` endpoint with the recipient’s Page-scoped ID, the `messaging_type`, and the message attachment containing the template type and payload with details about the specific template, such as title, images, and buttons.

```curl
curl -X POST -H "Content-Type: application/json" -d '{
  "recipient":{
    "id":"<PSID>"
  },
  "messaging_type":"RESPONSE",
  "message":{
    "attachment":{
      "type":"template",
      "payload":{
        "template_type":"<TEMPLATE_TYPE>",
        "elements":[
          {
            "title":"<TEMPLATE_TITLE>",
            ...
          }
        ]
      }
    }
  }
}' "https://graph.facebook.com/<API_VERSION>/<PAGE_ID>/messages?access_token=<PAGE_ACCESS_TOKEN>"
```

The body of the request follows a standard format for all template types, with the `message.attachment.payload` property containing the type and content details that are specific to each template type.

## Using Buttons

Most message templates allow you to incorporate one or more [buttons](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/buttons) as part of the template. These buttons allow you to offer the message recipient actions they can take in response to the template.

The type of buttons that can be used vary by template. See the specific template reference documentation for more information.

For more on button types available in the Messenger Platform, see [Buttons](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/buttons).
