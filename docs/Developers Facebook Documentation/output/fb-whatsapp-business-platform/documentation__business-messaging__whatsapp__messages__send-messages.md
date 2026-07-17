# Service messages | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages_

---

# Service messages

Updated: Apr 23, 2026

Service messages are free-form messages that you can send to WhatsApp users during a [customer service window](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages#customer-service-windows). You send them using the [Messages API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api) (part of the [Cloud API](https://developers.facebook.com/documentation/business-messaging/whatsapp/about-the-platform#whatsapp-cloud-api)). Unlike template messages, service messages do not require pre-approval — you can compose and send them as needed in response to a WhatsApp user’s message or call.

Service messages can only be sent via the Messages API. To message WhatsApp users outside of a customer service window, use template messages instead. See [Marketing messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/overview), [Utility messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/utility-templates/utility-templates), or [Authentication messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/authentication-templates/authentication-templates) to learn about template-based messaging.

## Customer service windows

When a WhatsApp user messages you or [calls you](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/pricing#how-calling-changes-the-24-hour-customer-service-window), a 24-hour timer called a customer service window starts. If the user messages or calls you again before the timer expires, the timer resets to 24 hours.

While the window is open, you can send any of the service message types listed below to the user. When the window closes, you can only send pre-approved [template messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview).

As a reminder, you can only send messages to WhatsApp users who have [opted-in](https://developers.facebook.com/documentation/business-messaging/whatsapp/getting-opt-in) to receiving messages from you.

**Known issue:** In rare cases, you may receive a message from a WhatsApp user but be unable to respond within the customer service window.

## Pricing

Service messages are billed under the SERVICE pricing category. See [Pricing](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing) for details.

## Message types

You can send the following types of service messages during an open customer service window.

[Address messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/address-messages) allow you to easily request a delivery address from WhatsApp users.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/441384197_454102407352120_3773045747928009795_n.png?_nc_cat=110&ccb=1-7&_nc_sid=e280be&_nc_ohc=PxUAdmQt_tgQ7kNvwE9O3Pv&_nc_oc=AdqyibNKnIiJa35uq4rDpnvKI6_K2fnf3J58WUQHPTmCYS8qkYL3ksvxNNpSZeQHRBg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=w1HThLGlTni1nGrudozATQ&_nc_ss=7b20f&oh=00_Af4-JiM26qR2wHqjVYdl1cYJ7tNjb1eNTtUMTelfzkcDhw&oe=6A1C1A22)

[Audio messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/audio-messages) display an audio icon and a link to an audio file. When the WhatsApp user taps the icon, the WhatsApp client loads and plays the audio file.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/441333612_1102926104368016_6233568143947105840_n.png?_nc_cat=106&ccb=1-7&_nc_sid=e280be&_nc_ohc=cuIDg_WNjhIQ7kNvwGRsvlP&_nc_oc=AdrdmzzIrXcwSuYmZioyVdtj06SnH31R39_t6U6KGDWPTgnRMRq1IMq0m1-NZMXnJ74&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=w1HThLGlTni1nGrudozATQ&_nc_ss=7b20f&oh=00_Af5eHDYx6Vnw2s9B-6N4l8apDihBwVaQO1GsjW4lviHObg&oe=6A1C1E2A)

[Contacts messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/contacts-messages) allow you to send rich contact information directly to WhatsApp users, such as names, phone numbers, physical addresses, and email addresses.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/440790666_990559829136435_3259503667945350761_n.png?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=tYaEeBq0OnAQ7kNvwEwVx9P&_nc_oc=Adp8WYonrt9B2P85lAgIlYDlhfzhYm_HrU4TWd2kJ9UjkKNtoABsHPOEHxq8o0Emqzs&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=w1HThLGlTni1nGrudozATQ&_nc_ss=7b20f&oh=00_Af6f6HPaG-FIsnto6AuxA9DiMXY3EmjIT-AuHVzaq033_w&oe=6A1C09CE)

[Document messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/document-messages) display a document icon, linked to a document that a WhatsApp user can tap to download.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/440797712_455258680228442_8760882695056096687_n.png?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=N8DGcNij-W0Q7kNvwFH9Lwl&_nc_oc=AdqWjII70lrjOdDLFWbHTknvvTOfx8QQkU8mAlMsK23eY89ywyLMOzv5DTPlV-PlpYA&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=w1HThLGlTni1nGrudozATQ&_nc_ss=7b20f&oh=00_Af5ob2QIb5U215qou-FH7btqrvnNpkfamwGbxsmHvqX1Uw&oe=6A1C11CE)

[Image messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/image-messages) display a single image and an optional caption.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/439831684_1373893986606126_2007013942518250478_n.png?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=TsflQjK89uUQ7kNvwECF9Ro&_nc_oc=Ado2L_WQoaRXsuHuBGBN9MFkmsegpxm307VEImrvTTf3qwOtE-TMp0krcixgQAp_6aE&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=w1HThLGlTni1nGrudozATQ&_nc_ss=7b20f&oh=00_Af44jZ91YVkb_tooZf5qZMJwZHGR7zkPKg8Y0W7VbgGwCw&oe=6A1C2DCC)

[Interactive CTA URL button messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/interactive-cta-url-messages) allow you to map any URL to a button, so you don’t have to include lengthy or obscure raw URLs in the message body.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/499710913_741192228581303_6833492513238538123_n.png?_nc_cat=102&ccb=1-7&_nc_sid=e280be&_nc_ohc=iRDUw7FspcYQ7kNvwGLTdTF&_nc_oc=AdqvHpxHNuGEFJYbJWS7-0z861JE2xh6JL6wIYnryfS7ko7ZZPTPXIfTyNFcX8i7yxg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=w1HThLGlTni1nGrudozATQ&_nc_ss=7b20f&oh=00_Af4KMahTexvxfQHUWKbx7TkaDMF5ZAJl8vgxNjfMQovbRg&oe=6A1C188A)

[Interactive voice call messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/call-button-messages-deep-links/#send-interactive-message-with-a-whatsapp-call-button) allow you to trigger a WhatsApp call from users.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/561384673_1339318434593474_5721045063886655968_n.jpg?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=Y-q3UNyKSQ0Q7kNvwHG1SJ9&_nc_oc=AdqSGEda2Yb7KnpGxfTiNTIy-p0GtdrJsHPjpz1K1RTkYGEC8lcUGcQbQBnKbF63nV8&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=w1HThLGlTni1nGrudozATQ&_nc_ss=7b20f&oh=00_Af6WC0cUPxBWO3fVLQ3XDCvG1b_q-AyTgOUB5MAzqM-vYQ&oe=6A1C1BB9)

[Interactive Flow messages](https://developers.facebook.com/docs/whatsapp/cloud-api/messages/interactive-flow-messages) allow you to send structured messages that are more natural or comfortable for your customers. For example, you can use WhatsApp Flows to book appointments, browse products, collect customer feedback, get new sales leads, or anything else.

For details, see the [WhatsApp Flows](https://developers.facebook.com/docs/whatsapp/flows) documentation.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/459207270_1257913005205310_7321941208385331189_n.png?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=BxO2dmsNnk4Q7kNvwH6AzUo&_nc_oc=Adq8fbQsFj2s1oc31SqEmrhu-vQXCwho5PAXW34greNVJFkp_LkCO_L2p3SCaRXhJd4&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=w1HThLGlTni1nGrudozATQ&_nc_ss=7b20f&oh=00_Af60L5VB7Uyj4Cxb8g6DcDfG24e-Z2p2zUR4ASV2lJb2HQ&oe=6A1C1F37)

[Interactive list messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/interactive-list-messages) allow you to present WhatsApp users with a list of options to choose from.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/440871648_773297808277279_825530086722343543_n.png?_nc_cat=110&ccb=1-7&_nc_sid=e280be&_nc_ohc=gLGJeAFw0bwQ7kNvwFrabtx&_nc_oc=Ado1vktYgdwEa5klCRu--8yJYMFF8abvmd5hNxo4i82nLEqdRgVsD7zWl31szdpR4oI&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=w1HThLGlTni1nGrudozATQ&_nc_ss=7b20f&oh=00_Af6Df9Q_JE-J0pHcNDMeK5G3ViaOctfYtbSXEijQDvt2Aw&oe=6A1C1CE8)

[Interactive location request messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/location-request-messages) display body text and a send location button. When a WhatsApp user taps the button, a location sharing screen appears which the user can use to share their location.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/440778444_741946064791848_335647298308114961_n.png?_nc_cat=111&ccb=1-7&_nc_sid=e280be&_nc_ohc=thQ3C9lK2b0Q7kNvwHxwScK&_nc_oc=AdqAwdcbT0wRNTdZ1_Eb-NkZrdrkXqR2apxrMWgHj-T5k2URQ3hKmUuZMxFz4fBXrdY&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=w1HThLGlTni1nGrudozATQ&_nc_ss=7b20f&oh=00_Af7ZlAgqChMQo-MtiJdMXurwk19Z20eUbNmsXMRNa4Vg4A&oe=6A1C1E51)

[Interactive reply buttons](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/interactive-reply-buttons-messages) messages allow you to send up to three predefined replies for users to choose from.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/440770231_408356378658790_997875267478158577_n.png?_nc_cat=106&ccb=1-7&_nc_sid=e280be&_nc_ohc=JnbG6sK1AcwQ7kNvwGWFA8P&_nc_oc=AdpZEH29WT2Y_LYhKHD4SJHq8UuEqKKbU3vjCc5XoQQqKaDQuC_zLDvFL985Y4A_9zs&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=w1HThLGlTni1nGrudozATQ&_nc_ss=7b20f&oh=00_Af4lvxhplyhUUqcAkMug83_WIH7l80ZCgrjYL7LxxUyaJw&oe=6A1C3018)

[Location messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/location-messages) allow you to send a location’s latitude and longitude coordinates to a WhatsApp user.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/440739359_451301924241746_5496230692221042707_n.png?_nc_cat=102&ccb=1-7&_nc_sid=e280be&_nc_ohc=WOLaywvATD4Q7kNvwFa67PU&_nc_oc=Adpwg3P3saGr5wBlMhsMe1gzQJ_F2lEbO6ug56SH02-uA4YNd4bfI3sR2dWVKeew9QA&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=w1HThLGlTni1nGrudozATQ&_nc_ss=7b20f&oh=00_Af5PTw1rz66z5A1K9EMbYvGkxNBxD1LPMHSIDX2LMpR0jQ&oe=6A1C0054)

[Sticker messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/sticker-messages) display animated or static sticker images in a WhatsApp message.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/440786426_1111584576559135_6735562667160992382_n.png?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=R6uI_FPkR8oQ7kNvwE5sc8R&_nc_oc=AdoiujHg7KJ8nvFoMt7Z2tBXmKC_6yUlEWzfn6FU8cFuSlOwBWIYIFqT6F-rJfTPchk&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=w1HThLGlTni1nGrudozATQ&_nc_ss=7b20f&oh=00_Af6Cwsmvz-ACR0ebG5fKNKl1wZayxM_tMNl3xE6cMxWw3A&oe=6A1C222F)

[Text messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/text-messages) are messages containing only a text body and an optional link preview.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/440778097_900237625125034_93345957848876145_n.png?_nc_cat=111&ccb=1-7&_nc_sid=e280be&_nc_ohc=wuJFaIw5EdkQ7kNvwFT43ju&_nc_oc=AdrWph5ZFAGUiEDpCHW3tm0BC5_kFyQ35Rbe6i3rzP5nIHDQyy0qFCF8dKT7IQK9Rak&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=w1HThLGlTni1nGrudozATQ&_nc_ss=7b20f&oh=00_Af6qCIeLV7NWs734Qas6M-hqmujqAGNPgFaaQocJtKkDlw&oe=6A1C294F)

[Video messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/video-messages) display a thumbnail preview of a video image with an optional caption. When the WhatsApp user taps the preview, it loads the video and displays it to the user.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/441312822_455518227141854_5770420105763186824_n.png?_nc_cat=110&ccb=1-7&_nc_sid=e280be&_nc_ohc=drV-guDfKjkQ7kNvwFOkZOe&_nc_oc=AdoLHIHgfEiPpjDcLkRuGd11Gwtw4nDoCYHGwiZ7M5CSg-b47A3WVFNOyEYIgdhgi68&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=w1HThLGlTni1nGrudozATQ&_nc_ss=7b20f&oh=00_Af695iQpsFdqY9p3yPzUzBDN6s2ey269gXhGXrTiNsFtqQ&oe=6A1C09E7)

[Reaction messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/reaction-messages) are emoji-reactions that you can apply to a previous WhatsApp user message that you have received.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/440758814_464628532577869_3703934471348865877_n.png?_nc_cat=111&ccb=1-7&_nc_sid=e280be&_nc_ohc=HFSSqsY5TgkQ7kNvwHvkFPk&_nc_oc=AdoUkI4If_nHoiNPl8FqSBQkXzm0-JG07s6c3K_ugUrd0xobOvg9f2I0kayP9Yha8qQ&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=w1HThLGlTni1nGrudozATQ&_nc_ss=7b20f&oh=00_Af6MJUa3YNl-Dm2QLoh1h1nxB8YNPCmBzgoxgGYs13d0hQ&oe=6A1C2312)

## Message quality

Your message quality is based on how messages have been received by WhatsApp users over the past seven days and is weighted by recency. It is determined by a combination of user feedback signals like blocks, reports, mutes, archives, and reasons users provide when they block you.

Guidelines for sending high-quality messages:

- Make sure your messages follow the [WhatsApp Business Messaging Policy](https://business.whatsapp.com/policy) .
- Only send messages to WhatsApp users who have opted into receiving messages from your business.
- Make the messages highly personalized and useful to users.
- Avoid sending open-ended welcome or introductory messages.
- Avoid sending too many messages per day.
- Optimize your messages for content and length.

Your business phone number’s status, [quality rating](https://www.facebook.com/business/help/896873687365001), and [messaging limits](https://developers.facebook.com/documentation/business-messaging/whatsapp/messaging-limits) are displayed in the [WhatsApp Manager](https://business.facebook.com/wa/manage/home/) > **Account tools** > **Phone numbers** panel.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/532273545_1018217176902582_4720629988037795374_n.png?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=7lfZ_DIAZiwQ7kNvwFfaFm1&_nc_oc=AdoxpLVm1xKC_xFVhgKRGSPdIWxfz8qfYBYvKnhwCCp8BNTPywCnHsxBwTOgagJUKMc&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=w1HThLGlTni1nGrudozATQ&_nc_ss=7b20f&oh=00_Af5Yz0KGD5EB7XCJxCK9TMtWQbewHl6dFviuCPEKjWIDvQ&oe=6A1C1C74)

Numbers with high traffic commonly experience quality changes within short intervals (even within minutes).

## Requests

All send message requests use the [Messages API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api#post-version-phone-number-id-messages):

```html
POST /<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>/messages
```

The post body varies depending on the [type of message](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages#message-types) you want to send, but the payload uses the following common syntax:

```html
{
  "messaging_product": "whatsapp",
  "recipient_type": "<RECIPIENT_TYPE>",
  "to": "<WHATSAPP_USER_PHONE_NUMBER>",
  "type": "<MESSAGE_TYPE>",
  "<MESSAGE_TYPE>": {<MESSAGE_CONTENTS>}
}
```

The `type` property value in the post body payload indicates the [type of message](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages#message-types) to send, and a property matching that type must be included that describes the message’s contents.

The `recipient_type` property can be either `individual` for 1:1 messaging, or `group` for group messages.

See the [Groups API documentation](https://developers.facebook.com/documentation/business-messaging/whatsapp/groups) for details.

For example, this is a request to send a [text message](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/text-messages) to a WhatsApp user. Note that `type` is set to `text`, and a `text` object follows, which describes the message’s contents:

```curl
curl 'https://graph.facebook.com/v25.0/106540352242922/messages' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "+16505551234",
  "type": "text",
  "text": {
    "preview_url": true,
    "body": "As requested, here'\''s the link to our latest product: https://www.meta.com/quest/quest-3/"
  }
}'
```

If delivered, the message appears like this in the WhatsApp client:

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/440778097_900237625125034_93345957848876145_n.png?_nc_cat=111&ccb=1-7&_nc_sid=e280be&_nc_ohc=wuJFaIw5EdkQ7kNvwFT43ju&_nc_oc=AdrWph5ZFAGUiEDpCHW3tm0BC5_kFyQ35Rbe6i3rzP5nIHDQyy0qFCF8dKT7IQK9Rak&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=w1HThLGlTni1nGrudozATQ&_nc_ss=7b20f&oh=00_Af6qCIeLV7NWs734Qas6M-hqmujqAGNPgFaaQocJtKkDlw&oe=6A1C294F)

## Responses

The API returns the following JSON response when it successfully accepts your send message request. This response only indicates that the API successfully **accepted your request** — it does not indicate successful delivery of your message. You receive delivery status via **messages** webhooks instead.

### Response syntax

```html
{
  "messaging_product": "whatsapp",
  "contacts": [
    {
      "input": "<WHATSAPP_USER_PHONE_NUMBER>",
      "wa_id": "<WHATSAPP_USER_ID>"
    }
  ],
  "messages": [
    {
      "id": "<WHATSAPP_MESSAGE_ID>",
      "group_id": "<GROUP_ID>", <!-- Only included if messaging a group -->
      "message_status": "<PACING_STATUS>" <!-- Only included if sending a template -->
    }
  ]
}
```

### Response contents

| Placeholder | Description | Sample Value |
| --- | --- | --- |
| `<GROUP_ID>`<br>*String* | The string identifier of a group made using the Groups API.<br>This field shows when messages are sent, received, or read from a group.<br>[Learn more about the Groups API](https://developers.facebook.com/documentation/business-messaging/whatsapp/groups) | `Y2FwaV9ncm91cDoxNzA1NTU1MDEzOToxMjAzNjM0MDQ2OTQyMzM4MjAZD` |
| `<PACING_STATUS>`<br>*String* | Indicates [template pacing](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-pacing) status. The `message_status` property is only included in responses when sending a [template message](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview) that uses a template that is being paced. | `wamid.HBgLMTY0NjcwNDM1OTUVAgARGBI4MjZGRDA0OUE2OTQ3RkEyMzcA` |
| `<WHATSAPP_USER_PHONE_NUMBER>`<br>*String* | WhatsApp user’s WhatsApp phone number. May not match `wa_id` value. | `+16505551234` |
| `<WHATSAPP_USER_ID>`<br>*String* | WhatsApp user’s WhatsApp ID. May not match `input` value. | `16505551234` |
| `<WHATSAPP_MESSAGE_ID>`<br>*String* | WhatsApp Message ID. This ID appears in associated **messages** webhooks, such as sent, read, and delivered webhooks. | `wamid.HBgLMTY0NjcwNDM1OTUVAgARGBI4MjZGRDA0OUE2OTQ3RkEyMzcA` |

## Commerce messages

Commerce messages are interactive messages used in conjunction with a product catalog. See [Share Products With Customers](https://developers.facebook.com/documentation/business-messaging/whatsapp/catalogs/share-products) to see how to use these types of messages.

## Read receipts

You can let a WhatsApp user know you have read their message by [marking it as read](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/mark-message-as-read), which causes two blue check marks (called “read receipts”) to appear below the user’s message:

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/491643461_603380552708521_8284248965365504291_n.png?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=_mrSzwZxTVsQ7kNvwHy65A7&_nc_oc=Adq-GkfjMIFueLzUK5bOlh36eZ0JzlOb-s8Z1EukafM3nHtdP5hPibFbLjZitzQ7bk4&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=w1HThLGlTni1nGrudozATQ&_nc_ss=7b20f&oh=00_Af5llMQO6XbZ_M5kxClQ1bOZ74OWiY9Fz3LZhxwe1ZqhYw&oe=6A1C2670)

## Typing indicators

If it may take you a few seconds or more to respond to a WhatsApp user, you can let them know that you are preparing a response by [displaying a typing indicator](https://developers.facebook.com/documentation/business-messaging/whatsapp/typing-indicators) and read receipts in the WhatsApp client:

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/488360772_654124507349470_2240843625651955811_n.png?_nc_cat=110&ccb=1-7&_nc_sid=e280be&_nc_ohc=HglXs-ME1DsQ7kNvwGXuqUZ&_nc_oc=AdqZSFu8HwDXebycSx_Rjm2a2Wl5Al1wcmRYpe0LVwBSc-aNbtz7ztKESq2jk6hV1DQ&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=w1HThLGlTni1nGrudozATQ&_nc_ss=7b20f&oh=00_Af4_0v_yxGs1Ta_SmJHC85j5zyUZKlNV3AIGCf_r4wEk3w&oe=6A1C145C)

## Contextual replies

You can send a message to a WhatsApp user as a [contextual reply](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/contextual-replies), which quotes a previous message in a contextual bubble:

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/441349069_1363509007609494_6528221959622289637_n.png?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Cbh6OS-UtgQQ7kNvwEFeGr_&_nc_oc=AdqnvELwYGGJ_gFdVHV0TfzGUVGNtyA6_9z6ACwDOZG94XlxzuWSivaf6ey2rZi0dmw&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=w1HThLGlTni1nGrudozATQ&_nc_ss=7b20f&oh=00_Af7qjhTm1-PNwyONPuVt6XqZ9BVlZenqAKfGV4d2kzvGHA&oe=6A1C2A6B)

This makes it easier for the user to know which specific message you are replying to.

## Webhooks

Messages sent to WhatsApp users trigger **messages** webhooks, so be sure to subscribe to this topic to receive message status notifications.

## WhatsApp user phone number formats

Plus signs (`+`), hyphens (`-`), parenthesis (`(`,`)`), and spaces are supported in send message requests.

We highly recommend that you include both the plus sign and country calling code when sending a message to a customer. If the plus sign is omitted, your business phone number’s country calling code is prepended to the customer’s phone number. This can result in undelivered or misdelivered messages.

For example, if your business is in India (country calling code `91`) and you send a message to the following customer phone number in various formats:

| Number In Send Message Request | Number Message Delivered To | Outcome |
| --- | --- | --- |
| `+16315551234` | `+16315551234` | Correct number |
| `+1 (631) 555-1234` | `+16315551234` | Correct number |
| `(631) 555-1234` | `+916315551234` | Potentially wrong number |
| `1 (631) 555-1234` | `+9116315551234` | Potentially wrong number |

Note: For Brazil and Mexico, the extra added prefix of the phone number may be modified by the Cloud API. This is a standard behavior of the system and is not considered a bug.

## Media caching

If you are using a link (`link`) to a media asset on your server (as opposed to the ID (`id`) of an asset you have uploaded to the Meta servers), the Cloud API internally caches the asset for 10 minutes. The cached asset is reused in subsequent send message requests if the link in subsequent payloads is the same as the link in the initial payload.

If you don’t want the cached asset reused in a subsequent message within the 10 minute time period, append a random query string to the asset link in the new send message request payload. The Cloud API treats this as a new asset, fetches it from your server, and caches it for 10 minutes.

For example:

- Asset link in first send message request: `https://link.to.media/sample.jpg` — asset fetched, cached for 10 minutes
- Asset link in second send message request: `https://link.to.media/sample.jpg` — cached asset reused
- Asset link in third send message request: `https://link.to.media/sample.jpg?abc123` — asset fetched, cached for 10 minutes

## Delivery sequence of multiple messages

When sending a series of messages, the order in which messages are delivered is not guaranteed to match the order of your API requests. If you need to ensure the sequence of message delivery, confirm receipt of a `delivered` status in a [status messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/status) webhook before sending the next message in your message sequence.

## Message time-to-live (TTL)

If the Cloud API is unable to deliver a message to a WhatsApp user, it retries delivery for a period of time known as a time-to-live, TTL, or the message validity period.

### Default TTL

- All messages except authentication templates: **30 days** .
- Authentication templates: **10 minutes**

### Customizing TTL for templates

You can customize the default TTL for authentication and utility templates, and for marketing templates sent using the Marketing Messages API for WhatsApp. See [Time-to-live](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/time-to-live) for details.

### When TTL is exceeded: Dropped messages

The platform drops messages that cannot be delivered within the default or customized TTL.

If you do not receive a status messages webhook with `status` set to `delivered` before the TTL is exceeded, assume the message was dropped.

If you send a message that fails (`status` set to `failed`), there could be a minor delay before you receive the webhook, so you may wish to build in a small buffer before assuming the message was dropped.

## Troubleshooting

If you are experiencing problems with message delivery, see [Message Not Delivered](https://developers.facebook.com/documentation/business-messaging/whatsapp/support#message-not-delivered).
