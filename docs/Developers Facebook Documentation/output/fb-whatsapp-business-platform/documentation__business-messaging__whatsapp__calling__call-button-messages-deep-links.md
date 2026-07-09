# Send WhatsApp Call Button Messages and Deep Links | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/call-button-messages-deep-links_

---

# Send WhatsApp Call Button Messages and Deep Links

Updated: Feb 25, 2026

## Overview

After you adopt Cloud API Calling features, you can raise awareness with your customers in two core ways:

- Send them a message with a WhatsApp call button
- Embed a calling deep link into your brand surfaces (website, application, and so on)

## Send interactive message with a WhatsApp call button

Use this endpoint to send a free-form interactive message with a WhatsApp call button during a [customer service window](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages#customer-service-windows) or an [open conversation window](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing#opening-conversations).

When a WhatsApp user clicks the call button, it initiates a WhatsApp call to the business number that sent the message.

A standard [message status webhook](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/status) will be sent in response to this message send.

![Screenshot showing WhatsApp call button message on mobile device](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/561384673_1339318434593474_5721045063886655968_n.jpg?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=Y-q3UNyKSQ0Q7kNvwHG1SJ9&_nc_oc=AdqSGEda2Yb7KnpGxfTiNTIy-p0GtdrJsHPjpz1K1RTkYGEC8lcUGcQbQBnKbF63nV8&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=w3gGTcaRfBCjugQBZzcGOw&_nc_ss=7b20f&oh=00_Af5EOgjE3O7vqDB-7sl-pBPzLm65IJXfYxktX1OoYWSjMQ&oe=6A1C1BB9)

Request syntax

```https
POST <PHONE_NUMBER_ID>/messages
```

| Placeholder | Description | Sample Value |
| --- | --- | --- |
| `<PHONE_NUMBER_ID>`<br>*Integer* | **Required**<br>The business phone number which you are sending messages from.<br>[Learn more about formatting phone numbers in Cloud API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api) | `+12784358810` |

Request body

```https
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "14085551234",
  "type": "interactive",
  "interactive" : {
    "type" : "voice_call",
    "body" : {
      "text": "You can call us on WhatsApp now for faster service!"
    },
    "action": {
      "name": "voice_call",
      "parameters": {
        "display_text": "Call on WhatsApp",
        "ttl_minutes": 100,
        "payload": "payload data"
      }
    }
  }
}
```

Body parameters

[Learn more about sending interactive free form messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api)

| Parameter | Description | Sample Value |
| --- | --- | --- |
| `to`<br>*Integer* | **Required**<br>The phone number of the WhatsApp user you are messaging.<br>[Learn more about formatting phone numbers in Cloud API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/whatsapp-business-account-phone-number-api) | `"17863476655"` |
| `type`<br>*String* | **Required**<br>The type of interactive message you are sending.<br>In this case, you are sending a `voice_call`.<br>[Learn more about interactive messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api) | `"voice_call"` |
| `action`<br>*String* | **Required**<br>The action of your interactive message.<br>Must be `voice_call`. | `"voice_call"` |
| `parameters`<br>*JSON Object* | **Optional**<br>Optional parameters for the WhatsApp calling button sent to the user.<br>Contains three values: `display_text`, `ttl_minutes`, and `payload`<br>`display_text` — (*String*) **Optional**<br>The display text on the WhatsApp calling button sent to the user.<br>Default is “Call Now”<br>Max length: 20 characters<br>`ttl_minutes` — (*Integer*) **Optional**<br>Time to live for the call-to-action (CTA) button in minutes.<br>Must be between 1 and 43200 (30 days)<br>Default value is 10080 (7 days)<br>`payload` — (*String*) **Optional**<br>An arbitrary string, useful for tracking.<br>Any app subscribed to the `calls` webhook field on the WhatsApp Business Account can get this string, as it is included in the `connect` and `terminate` webhook payloads under the `cta_payload` field.<br>Cloud API does not process this field, it just returns it as part of the webhooks.<br>Maximum 512 characters.<br>Payload is only available to WhatsApp client starting on version 2.25.27. | `"parameters": {<br>"display_text": "Call on WhatsApp",<br>"ttl_minutes": 100,<br>"payload": "payload data"<br>}` |

Success response

[Learn more about messaging success responses](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api)

Error response

Possible errors that can occur:

Sending this message to users on older app versions results in an error webhook with error code `131026`.

[View general Cloud API error codes](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/error-codes)

## Create and send WhatsApp call button template message

Use these endpoints to create and send a WhatsApp call button template message.

Once your call button template message is created, you can send a message to a WhatsApp user, inviting them to call your business.

[Learn more about creating and managing message templates](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview)

### Create call button message template

Use this endpoint to create a call button message template.

Request syntax

```https
POST/<WHATSAPP_BUSINESS_ACCOUNT_ID>/message_templates
```

| Parameter | Description | Sample Value |
| --- | --- | --- |
| `<WHATSAPP_BUSINESS_ACCOUNT_ID>`<br>*String* | **Required**<br>Your WhatsApp Business Account ID.<br>[Learn how to find your WABA ID](https://developers.facebook.com/documentation/business-messaging/whatsapp/whatsapp-business-accounts) | `"waba-90172398162498126"` |

Request body

```https
{
  "name": "<NAME>",
  "category": "<CATEGORY>",
  "language": "<LANGUAGE>",
  "components": [
    {
      "type": "BODY",
      "text": "You can call us on WhatsApp now for faster service!"
    },
    {
      "type": "BUTTONS",
      "buttons": [
        {
          "type": "voice_call",
          "text": "Call Now",
          "ttl_minutes": 1440
        },
        {
          "type": "URL",
          "text": "Contact Support",
          "url": "https://www.luckyshrub.com/support"
        }
      ]
    }
  ]
}
```

Body parameters

You can create and manage template messages through both Cloud API and the WhatsApp Business Manager interface.

When creating your call button template, ensure you configure `type` as `voice_call`.

[Learn more about creating and managing message templates](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview)

| Parameter | Description | Sample Value |
| --- | --- | --- |
| `type`<br>*String* | **Required**<br>The type of template message you are creating.<br>In this case, you are creating a `voice_call`. | `"voice_call"` |
| `text`<br>*String* | **Optional**<br>The display text on the WhatsApp calling button sent to the user.<br>Default is “Call Now”<br>Max length: 20 characters | `"Call Now"` |
| `ttl_minutes`<br>*Integer* | **Optional**<br>Time to live for the CTA button in minutes.<br>Must be between 1440 (1 day) and 43200 (30 days).<br>You can override this value when sending the message. | `1440` |

Success response

```https
{
  "id": "<ID>",
  "status": "<STATUS>",
  "category": "<CATEGORY>"
}
```

[*Learn more about messaging success responses*](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api)

Error response

Possible errors that can occur:

- Invalid `whatsapp-business-account-id`
- Permissions/Authorization errors
- Template structure/component validation alerts

[View general Cloud API error codes](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/error-codes)

### Send call button message template

Use this endpoint to **send** a call button message template.

The following is a simplified sample of the send template message request, however you can [learn more about how to send message templates here](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview).

Request syntax

```https
POST/<PHONE_NUMBER_ID>/messages
```

| Parameter | Description | Sample Value |
| --- | --- | --- |
| `<PHONE_NUMBER_ID>`<br>*String* | **Required**<br>The business phone number which you are sending a message from.<br>[Learn more about formatting phone numbers in Cloud API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/whatsapp-business-account-phone-number-api) | `+18762639988` |

Request body

```https
{
  "to": "14085551234",
  "messaging_product": "whatsapp",
  "type": "template",
  "recipient_type": "individual",
  "template": {
    "name": "wa_voice_call",
    "language": {
      "code": "en"
    },
    "components": [
      {
        "type": "button",
        "sub_type" : "voice_call",
        "parameters": [
          {
            "type": "ttl_minutes",
            "ttl_minutes": 100
          },
          {
            "type": "payload",
            "payload": "payload data"
          }
        ]
      }
    ]
  }
}
```

Request parameters

| Parameter | Description | Sample Value |
| --- | --- | --- |
| `ttl_minutes`<br>*Integer* | **Optional**<br>Time to live for the CTA button in minutes.<br>Must be between 1 and 43200 (30 days)<br>Default value is 10080 (7 days) | `10800` |
| `payload`<br>*String* | **Optional**<br>An arbitrary string, useful for tracking.<br>Any app subscribed to the `calls` webhook field on the WhatsApp Business Account can get this string, as it is included in the `connect` and `terminate` webhook payloads under the `cta_payload` field.<br>Cloud API does not process this field, it just returns it as part of the webhooks.<br>Maximum 512 characters.<br>Payload is only available to WhatsApp client starting on version 2.25.27. | `payload data` |

Success response

![Screenshot showing successful WhatsApp call button template message](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/566207608_1339317967926854_2361800073068017276_n.jpg?_nc_cat=101&ccb=1-7&_nc_sid=e280be&_nc_ohc=4cro-bh-zKYQ7kNvwF5iwBq&_nc_oc=Adq_oC6j-QgzImw5d2_JwVzx94HCah1X5_O17LQmIKGLI4uldD_Sbj2_NLbBfty29sM&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=w3gGTcaRfBCjugQBZzcGOw&_nc_ss=7b20f&oh=00_Af4VsTRX8SZWVLOe5-kI58CJeQ90XJMFC7_peHGLVwxP7w&oe=6A1BFDD3)

[Learn more about messaging success responses](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api)

## Calling deep links

Calling deep links are hyperlinks that route WhatsApp users to call your business.

The process to create a calling deep link is similar to a [chat deep link](https://faq.whatsapp.com/5913398998672934/?locale=en_US), except the format for the call deep link is `wa.me/call/<BUSINESS_PHONE_NUMBER>`

Note that deep links are not supported on WhatsApp desktop clients.

### Embed calling deep links

You can use calling deep links to advertise WhatsApp calling for your business.

Use these links anywhere where calling can be useful, like your website, primary application, or even as a QR code to be shared.

![Example of calling deep link embedded on a business website](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/560548572_1339317974593520_7716453845465534771_n.jpg?_nc_cat=111&ccb=1-7&_nc_sid=e280be&_nc_ohc=fG9AgG5UCocQ7kNvwE78JVV&_nc_oc=AdoKA0kjvfL06uKIyNnCF4PgmwQ6yiaWM-h_S_UKs_1qgi3f75pJFC02Iqkf3nEqE2o&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=w3gGTcaRfBCjugQBZzcGOw&_nc_ss=7b20f&oh=00_Af5V6KESNVjtJNbYLXj8-WhJGZ6LBh5l0ausZOHBvobJwA&oe=6A1C147A)

### Send calling deep links

You can also send messages to WhatsApp users with a calling deep link.

Since deep links can be made per business phone number, you can use calling deep links to prompt WhatsApp users to contact a different phone number with voice enabled.

The `wa.me/call/<BUSINESS_PHONE_NUMBER>` format is easy to copy, paste, and send, and does not require you to make a template in Business Manager.

![Screenshot showing WhatsApp message with calling deep link](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/561465638_1339317964593521_4488293728274608640_n.jpg?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=3NBz6pPy7pQQ7kNvwFx4wc9&_nc_oc=Adr9wRSQccyPJ1-XRpdi-FmD741wkp_WjlgEPUdeBsdr1qVLqQsUNSM7CBkeMu0DVCw&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=w3gGTcaRfBCjugQBZzcGOw&_nc_ss=7b20f&oh=00_Af4uP6EHK_ShONUqKE5G0s9RWadVlu4Ok8l2zzuDzcP-CQ&oe=6A1C102B)

### Send payload data in call deep link

You can also send a payload with the deep link. You can use the `biz_payload` query string when sending the call deep link to any user (`wa.me/call/<BUSINESS_PHONE_NUMBER>?biz_payload=payload`).

When a user calls using the provided deep link with the `biz_payload` any app subscribed to the `calls` webhook field on the WhatsApp Business Account can get this string, as it is included in the `connect` and `terminate` webhook payloads under the `deeplink_payload` field.

Payload in call deep link is only available to WhatsApp client starting on version 2.25.27.
