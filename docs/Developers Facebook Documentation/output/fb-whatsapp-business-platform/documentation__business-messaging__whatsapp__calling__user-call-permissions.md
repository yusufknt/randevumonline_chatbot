# Obtain User Call Permissions | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/user-call-permissions_

---

# Obtain User Call Permissions

Updated: Nov 13, 2025

As of November 3, 2025, permanent permissions is now available. Users can now grant a business ongoing permission to call. Users can review and change calling permission for a business at any time in the business profile.

Call permission related features are available only in regions where [business initiated calling is available](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling#availability).

## Overview

If you want to place a call to a WhatsApp user, your business must receive user permission first. When a WhatsApp user grants call permissions, they can be either temporary or permanent.

Business does not have control over this permission as it is only granted by the user and can only be revoked by the user, at any time. Permanent permission data will be stored until it is revoked.

You can obtain calling permission from a WhatsApp user in any of the following ways:

1. **Send a call permission request to the user** — Send a free-form or templated message requesting calling permission from the user. User has the option to choose between temporary or permanent.
2. **Callback permission is provided by the WhatsApp user** — The WhatsApp user automatically provides temporary call permissions by placing a call to the business. The [callback setting must be enabled](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/call-settings#configure-update-business-phone-number-calling-settings) on the business phone number.
3. **WhatsApp user provides call permission via Business Profile** — The WhatsApp user provides call permissions to the business through their business profile.

### Limits (Per business + WhatsApp user pair)

- Temporary permissions are **granted for 7 calendar days (168 hours)** Calculated as the number of seconds in a day multiplied by 7, from time of user’s approval.
- Permanent permissions do not expire, but they have the same connected calls limit.
- Your business can make a maximum of **100 connected calls every 24 hours**
- These limits are on the **business phone number**

These limits are in place to protect WhatsApp users from unwanted calls.

When you test your WhatsApp Calling integration using public test numbers (PTNs) and sandbox accounts, Calling API restrictions are relaxed.

[Learn more about testing your WhatsApp Calling API integration](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling#testing-and-sandbox-accounts)

## Call permission request basics

You may proactively request a calling permission from a WhatsApp user by sending a permission request message, either as a:

- Free form interactive message
- Template message

The WhatsApp user may approve (temporary or permanent), decline, or simply not respond to a call permission request.

**With permissions, the WhatsApp user is in control.** Even if the user provides calling permission, they can revoke that granted permission request at any time. Conversely, if the user declines a permission request, they can still grant calling permission, up until the permission request expires.

**A call permission request expires** when any of the following occurs:

- The WhatsApp user interacts with a subsequent new call permission request from the business
- 7 days after the permission was accepted or declined by the consumer
- 7 days after the permission was delivered if the consumer does not respond to the request

[View client UI behavior for expired permission requests](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/user-call-permissions#call-permission-request-expiration-scenarios)

To ensure an optimal user experience around business initiated calling, the following limits are enforced:

1. **When sending a calling permission request message** Maximum of 1 permission request in 24hMaximum 2 permission requests within 7 days. *These limits reset when any connected call (business-initiated/user-initiated) is made between the business and WhatsApp user.**These limits apply toward permissions requests sent either as free form or template messages.*
2. **When business-initiated calls go unanswered or are rejected** 2 consecutive unanswered calls result in a system message to reconsider an approved permission4 consecutive unanswered calls result in an approved permission being automatically revoked. The user may again update this if they so choose.

[View client UI behavior for consecutive unanswered calls](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/user-call-permissions#consecutive-unanswered-calls)

## Free form vs template call permission request message

Call permission request messages are subject to [messaging charges](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing)

A call permission request message can be sent to users in one of the following ways:

**Send a free form message**

- When you are within a customer service window with a WhatsApp user, you can send a free form message with a call permission request.
- Although a text body will be optional, you should send one to build context with the user. In the case of free form calling permission request messages, header and footer sections are not supported.
- Since the customer service window is open, there is no need to create a conversation window.

**Create and send a template message**

- Sending a template message allows you to initiate a user conversation with a call permission request.
- Context (that is, a text body) is required when sending a template message with a call permission request.
- With template messages, you can further customize your permission request by adding a message header and footer.

![Criteria for sending call permission request messages](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/565169286_1339318287926822_4224200115246538359_n.jpg?_nc_cat=106&ccb=1-7&_nc_sid=e280be&_nc_ohc=aoEPwSiY3joQ7kNvwFt1oyR&_nc_oc=AdrI4BpB3Do6Mzqu_IY4LJEUMXh2mSrK8bq_tKH7dJH510AUMT-QoyJwLMuehGJSJeA&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=sGEzwtCZrPyORFJM3zKldA&_nc_ss=7b20f&oh=00_Af5ryr52i3k9yMnI05v9fAGaGbQNNGw8N9TTu8O1XB3A7g&oe=6A1C0128)

## Client application UI experience

### Call permission request flow and sample messages

Allow calls

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/569920259_1349837820208202_5589372317839283055_n.jpg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=02rd-2aDarAQ7kNvwFgPxQV&_nc_oc=AdrI9IpxDP2dXqViqXbizNA7jzOLrFdKycPJNVn8PM8VruSEeDhwOuH_JSuX9BJTYUU&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=sGEzwtCZrPyORFJM3zKldA&_nc_ss=7b20f&oh=00_Af6e19BYvZytZ5a6XKJjuUuAR-3xI4C9B6TFuLvFBydwJg&oe=6A1BFD4B)

Temporarily allow calls

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/571212662_1349837823541535_8439494695603356474_n.jpg?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=V-TVy2smRCQQ7kNvwH7DyVS&_nc_oc=AdrlQVnKq0Oh7oj5epjwxJ9KBQTO-PV3-Ps-J0JsZL4lwsUC2gUHInHjSxySePOuRW4&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=sGEzwtCZrPyORFJM3zKldA&_nc_ss=7b20f&oh=00_Af4BKGUkbiCNAvTexerlj203o71gdJJ_2VMLrtaaVUfNdg&oe=6A1C2505)

### Template message

With header, footer and body
![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/571144430_1349837860208198_1480615658143744665_n.jpg?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=_9k7sanxWp4Q7kNvwHgZkFI&_nc_oc=AdqFr8KcrrfKlIpTlMuZo3ln0Trig4bnDXsuyHjNyQbuzMn0BRV3B5QDdX3YQduKpic&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=sGEzwtCZrPyORFJM3zKldA&_nc_ss=7b20f&oh=00_Af6bCgmJ_f4bI_LNfcCkS1be0w1bTTcrVZ45ifg3fbX4iQ&oe=6A1C0495)

With body only
![Free form message with body only](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/571213506_1349837833541534_3400449897824410954_n.jpg?_nc_cat=106&ccb=1-7&_nc_sid=e280be&_nc_ohc=5p1keV2MY0MQ7kNvwEH1MaW&_nc_oc=AdoQOxyiFwUUmEwnEhHxWOVkmNsmHI61EZQQESABYj5tNIQHw50vBbvzVeHag_Ghem0&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=sGEzwtCZrPyORFJM3zKldA&_nc_ss=7b20f&oh=00_Af5N_qk4tSmy74sn3YO3LlW8PgVgOv7weIRHtfWD6o3tbA&oe=6A1C0A01)

With no text body
![Free form message with no text body](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/571762588_1349837766874874_7988101620410646138_n.jpg?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=2_VSt9CJJfIQ7kNvwGOIGhk&_nc_oc=AdrT0QYXDMt0JIkoYEAnjwxcGJYsIgxjz_-co_BQohfARLxSman_FqT6lltIVS876MU&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=sGEzwtCZrPyORFJM3zKldA&_nc_ss=7b20f&oh=00_Af56N-bd9f0Us3WpfrXZy3DzgwOZP691dQNCeXdwpas__A&oe=6A1C2809)

Free form message types

With no text body
![Template message with no text body](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/571762588_1349837766874874_7988101620410646138_n.jpg?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=2_VSt9CJJfIQ7kNvwGOIGhk&_nc_oc=AdrT0QYXDMt0JIkoYEAnjwxcGJYsIgxjz_-co_BQohfARLxSman_FqT6lltIVS876MU&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=sGEzwtCZrPyORFJM3zKldA&_nc_ss=7b20f&oh=00_Af56N-bd9f0Us3WpfrXZy3DzgwOZP691dQNCeXdwpas__A&oe=6A1C2809)

With text body only
![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/571213506_1349837833541534_3400449897824410954_n.jpg?_nc_cat=106&ccb=1-7&_nc_sid=e280be&_nc_ohc=5p1keV2MY0MQ7kNvwEH1MaW&_nc_oc=AdoQOxyiFwUUmEwnEhHxWOVkmNsmHI61EZQQESABYj5tNIQHw50vBbvzVeHag_Ghem0&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=sGEzwtCZrPyORFJM3zKldA&_nc_ss=7b20f&oh=00_Af5N_qk4tSmy74sn3YO3LlW8PgVgOv7weIRHtfWD6o3tbA&oe=6A1C0A01)

### Updating call permission on business profile

Users always have the option to change the permission using a new option on the business profile.

| Update call permission on business profile |
| --- |
| ![Business profile screen showing call permission update options](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/571034903_1349837813541536_6048092876982828292_n.jpg?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=pfZ0_oWEBqgQ7kNvwFZlWSf&_nc_oc=Adr1C6o7Zqpv8amR6mv7VkhJYpzhBl350c46CxpEqdfDF2Def0tBtHHcAKePnXwFFAI&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=sGEzwtCZrPyORFJM3zKldA&_nc_ss=7b20f&oh=00_Af51wfPDDwnSwD6n4jIAnHOI4IzJtR2klHlEIMQ75cNcyg&oe=6A1C2901) |

### Consecutive unanswered calls

| Consecutive unanswered calls |
| --- |
| 2 consecutive unanswered calls — System message for user to update permission<br>![System message displayed after 2 consecutive unanswered calls](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/571296922_1349837800208204_1367855784989927722_n.jpg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=SYP-9X6bX6MQ7kNvwGNkzE5&_nc_oc=Adp3gPftQaDqcGUzIShYAC45AgXypUpHXHbisXdY4X4Hm4rc_sYSpMNu-tfz63j3leI&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=sGEzwtCZrPyORFJM3zKldA&_nc_ss=7b20f&oh=00_Af4HqYKxL1OTTbaA7FSSVwAgJPhtumIwMvJ6OiPWjY68Tg&oe=6A1C3196) |
| 4 consecutive unanswered calls — Permissions automatically revoked<br>![Notification shown when permissions are automatically revoked after 4 unanswered calls](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/571213183_1349837840208200_3862806014736476146_n.jpg?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=4qGZW-iDZO8Q7kNvwGeewwN&_nc_oc=AdqArycugRyLNFtXPljUZaS44U69Aw6PXliTp5W-hxUgyBBpA6mDxY-qX3rq9AtnKlI&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=sGEzwtCZrPyORFJM3zKldA&_nc_ss=7b20f&oh=00_Af51XC7CXLxK3lMf74ZA83br0XaxISQzEef5sayE-e6q7Q&oe=6A1C147B) |

### Call permission request expiration scenarios

Permission request expires after 7 days — User interacts with request
![Permission request expires after 7 days — User interacts with request](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/571301842_1349837853541532_6081659828181485282_n.jpg?_nc_cat=101&ccb=1-7&_nc_sid=e280be&_nc_ohc=fNwKnMHnaNgQ7kNvwFJYrnz&_nc_oc=AdqHMM9m7-2ozluqjrpWT2hnF9nSGWXkEmCV9883yPYVJK_IozbwhUYlAQLs4iEwMqo&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=sGEzwtCZrPyORFJM3zKldA&_nc_ss=7b20f&oh=00_Af482rW0ci75OqxrAB7MEmF9KBfE3q03bWGIJ6uJTgwEog&oe=6A1C10CF)

Permission request expires after 7 days — User does not interact
![Permission request expires after 7 days — User does not interact](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/572387488_1349837806874870_6917394151589767244_n.jpg?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=dEFw4uNP3UUQ7kNvwECHRTO&_nc_oc=AdrZuozcyh6G83qBAkCNXlZCTr2u99ZpsOxJOghUFsKN0yHgjAwdTKdvmtb2e7aBqCQ&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=sGEzwtCZrPyORFJM3zKldA&_nc_ss=7b20f&oh=00_Af404flXqK7Il8eOxLwKjBgBobmxgSV4Cpa_REuk8lEw4g&oe=6A1C191A)

Previous permission request expires immediately — User does not interact / New call permission request is received
![Previous permission request expires immediately — User does not interact / New call permission request is received](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/574278576_1349837836874867_6096441569227206157_n.jpg?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=6U-ISJetWJsQ7kNvwEroBfT&_nc_oc=AdrJGNA4aJYKArkp1t3_SPG-EsOJLvGGIG0_ZRx0TK8oHXx8VqmE70Z413imrZv9Whg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=sGEzwtCZrPyORFJM3zKldA&_nc_ss=7b20f&oh=00_Af7rFou-S0rfJ7GqBLeZxcEeTk7g6lqEmFtTRmm-gH1fkg&oe=6A1C0623)

Previous permission request expires immediately — User allows / Interacts with the new request
![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/571174456_1349837843541533_5439194533822125836_n.jpg?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=6POuiSkFAbIQ7kNvwHDP8hM&_nc_oc=Adpl5FpkT18yMT0iAuPZ14as11V3pnucHgkYkME8EuZuWxRcCl-lC_oPKxP-nGijQdI&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=sGEzwtCZrPyORFJM3zKldA&_nc_ss=7b20f&oh=00_Af5CRTAAezpSspeyqKtkiDUfxKlaU9FtYuEACEaBB2JLwA&oe=6A1C3313)

## Send free form call permission request message

Call permission request messages are subject to [messaging charges](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing)

Use this endpoint to send a free form interactive message with a call permission request during a [customer service window](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages#customer-service-windows). A standard [message status webhook](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/status) will be sent in response to this message send.

**Note:** The call permission request interactive object cannot be edited by the business. Only the message body can be customized.

[See how this message is rendered on the WhatsApp client](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/user-call-permissions#call-permission-request-flow-and-sample-messages)

Request syntax

```https
POST <PHONE_NUMBER_ID>/messages
```

| Parameter | Description | Sample Value |
| --- | --- | --- |
| `<PHONE_NUMBER_ID>`<br>*Integer* | **Required**<br>The business phone number which you are sending messages from.<br>[Learn more about formatting phone numbers in Cloud API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/whatsapp-business-account-phone-number-api) | `+18274459827` |

Request body

```https
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "<PHONE_NUMBER_ID> or <WHATSAPP_ID>",
  "type": "interactive",
  "interactive": {
    "type": "call_permission_request",
    "action": {
      "name": "call_permission_request"
    },
    "body": {
      "text": "We would like to call you to help support your query on Order No: ON-12853."
    }
  }
}
```

Body parameters

| Parameter | Description | Sample Value |
| --- | --- | --- |
| `to`<br>*Integer* | **Required**<br>The phone number of the WhatsApp user you are messaging<br>[Learn more about formatting phone numbers in Cloud API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/whatsapp-business-account-phone-number-api) | `+17863476655` |
| `type`<br>*String* | **Required**<br>The type of interactive message you are sending.<br>In this case, you are sending a `call_permission_request`.<br>[Learn more about interactive messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api) | `“call_permission_request”` |
| `action`<br>*String* | **Required**<br>The action of your interactive message.<br>Must be `call_permission_request`. | `“call_permission_request”` |
| `body`<br>*String* | **Optional**<br>The body of your message.<br>Although this field is optional, it is highly recommended you give context to the WhatsApp user when you request permission to call them. | `"Allow us to call you so we can support you with your order."` |

Success response

```json
{
  "messaging_product": "whatsapp",
  "contacts": [{
      "input": "+1-408-555-1234",
      "wa_id": "14085551234"
    }],
  "messages": [{
      "id": "wamid.gBGGFlaCmZ9plHrf2Mh-o"
    }]
}
```

[*Learn more about messaging success responses*](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api)

Error response

Possible errors that can occur:

- Invalid `phone-number-id`
- Permissions/Authorization errors
- Rate limit reached
- Sending this message to users on older app versions will result in error webhook with error code [131026](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/error-codes)
- Calling not enabled
- Calling restriction errors

[View general Cloud API Error Codes here](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/error-codes)

## Create and send call permission request template messages

Call permission request messages are subject to [messaging charges](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing)

Use these endpoints to create and send a call permission request message template.

Once your permission request template message is created, your business can send the template message to the user as a call permission request outside of a customer service window.

[Learn more about creating and managing message templates](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview)

### Create message template

Use this endpoint to create a call permission request message template.

Request syntax

```https
POST/<WHATSAPP_BUSINESS_ACCOUNT_ID>/message_templates
```

| Parameter | Description | Sample Value |
| --- | --- | --- |
| `<WHATSAPP_BUSINESS_ACCOUNT_ID>`<br>*String* | **Required**<br>Your WhatsApp Business Account ID.<br>[Learn how to find your WABA ID](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/whatsapp-business-account-api) | `“waba-90172398162498126”` |

Request body

```json
{
  "name": "sample_cpr_template",
  "language": "en",
  "category": "[MARKETING|UTILITY]",
  "components": [
     {
      "type": "HEADER",
      "text": "Support of Order No: {{1}}",
      "example": {
        "body_text": [
          [
            "ON-12345"
          ]
        ]
      }
    },
    {
      "type": "BODY",
      "text": "We would like to call you to help support your query on Order No: {{1}} for the item {{2}}.",
      "example": {
        "body_text": [
          [
            "ON-12345",
            "Avocados"
          ]
        ]
      }
    },
    {
      "type": "FOOTER",
      "text": "Talk to you soon!"
    },
    {
      "type": "call_permission_request"
    }
  ]
}
```

Body parameters

Creating and managing template messages can be done both through Cloud API and the WhatsApp Business Manager interface.

When creating your call permission request template, ensure you configure `type` as `call_permission_request`.

[Learn more about creating and managing message templates](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview)

| Parameter | Description | Sample Value |
| --- | --- | --- |
| `type`<br>*String* | **Required**<br>The type of template message you are creating.<br>In this case, you are creating a `call_permission_request`. | `“call_permission_request”` |

Template status response

```https
{
  "id": "<ID>",
  "status": "<STATUS>",
  "category": "<CATEGORY>"
}
```

[*Learn more about template status response*](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview#template-status)

Error response

Possible errors that can occur:

- Invalid WABA id
- Permissions/Authorization errors
- Template structure/component validation alerts

[View general Cloud API Error Codes here](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/error-codes)

### Send message template

Use this endpoint to send a call permission request message template

The following is a simplified sample of the send template message request, however you can [learn more about how to send message templates here.](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview)

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
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "+13287759822", // The WhatsApp user who will receive the template message
  "type": "template",
  "template": {
    "name": "sample_cpr_template", // The call permission request template name
    "language": {
      "code": "en"
    },
    "components": [ // Body text parameters such as customer name and order number
      {
        "type": "body",
        "parameters": [
          {
            "type": "text",
            "text": "John Smith"
          },
          {
            "type": "text",
            "text": "order #1522"
          }
        ]
      }
    ]
  }
}
```

[Learn more about sending template messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview)

## Get current call permission state

Use this endpoint to get the call permission state for a business phone number with a single WhatsApp user phone number.

### Request syntax

```https
GET /<PHONE_NUMBER_ID>/call_permissions?user_wa_id=<CONSUMER_WHATSAPP_ID>
```

### Request parameters

| Parameter | Description | Sample Value |
| --- | --- | --- |
| `<PHONE_NUMBER_ID>`<br>*String* | **Required**<br>The business phone number you are fetching permissions against.<br>[Learn more about formatting phone numbers in Cloud API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/whatsapp-business-account-phone-number-api) | `+18762639988` |
| `<CONSUMER_WHATSAPP_ID>`<br>*Integer* | **Required**<br>The phone number of the WhatsApp user who you are requesting call permissions from.<br>[Learn more about formatting phone numbers in Cloud API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/whatsapp-business-account-phone-number-api) | `+13057765456` |

Response body

```https
{
  "messaging_product": "whatsapp",
  "permission": {
    "status": "temporary",
    "expiration_time": 1745343479
  },
  "actions": [
    {
      "action_name": "send_call_permission_request",
      "can_perform_action": true,
      "limits": [
        {
          "time_period": "PT24H",
          "max_allowed": 1,
          "current_usage": 0,
        },
        {
          "time_period": "P7D",
          "max_allowed": 2,
          "current_usage": 1,
        }
      ]
    },
    {
      "action_name": "start_call",
      "can_perform_action": false,
      "limits": [
        {
          "time_period": "PT24H",
          "max_allowed": 5,
          "current_usage": 5,
          "limit_expiration_time": 1745622600,
        }
      ]
    }
  ]
}
```

Response parameters

| Parameter | Description |
| --- | --- |
| `permission`<br>*JSON Object* | The permission object contains two values:<br>`status` *(String)* — The current status of the permission.<br>Can be either:<br>`“no_permission”``"temporary"``“permanent”`<br>`expiration` *(Integer)* — The Unix time at which the permission will expire in UTC timezone.<br>If the permission is permanent, this field won’t be present. |
| `actions`<br>*JSON Object* | A list of actions a business phone number may undertake to facilitate a call permission or a business initiated call.<br>Current actions are:<br>`send_call_permission_request`: Represents the action of sending new call permissions request messages to the WhatsApp user.<br>`start_call`: Represents the action of establishing a new call with the WhatsApp user. Establishing a new call means that the call was successfully picked up by the consumer.<br>For example, `send_call_permission_request` having a `can_perform_action` of `true` means that your business can send a call permission request to the WhatsApp user in question<br>`can_perform_action` (*Boolean*) —<br>A flag indicating whether the action can be performed now, taking into account all limits. |
| `limits`<br>*JSON Object* | A list of time-bound restrictions for the given `action_name`.<br>Each `action_name` has 1 or more restrictions depending on the timeframe.<br>For example, a business can only send 2 permission requests in a 24-hour period.<br>`limits` contains the following fields:<br>`time_period` (*String*) — The span of time in which the limit applies, represented in the ISO 8601 format.<br>`max_allowed` (*Integer*) — The maximum number of actions allowed within the specified time period.<br>`current_usage` (*Integer*) — The current number of actions the business has taken within the specified time period.<br>`limit_expiration_time` (*Integer*) — The Unix time at which the limit will expire in UTC timezone.<br>If `current_usage` is under the max allowed for the limit, this field won’t be present. |

Error response

Possible errors that can occur:

- Invalid `phone-number-id`
- If the consumer phone number is uncallable, the api response will be `no_permission` .
- Permissions/Authorization errors.
- Rate limit reached. A maximum of 100 requests in a 1 second window can be made to the API.
- Calling is not enabled for the business phone number.

[View Calling API Error Codes and Troubleshooting for more information](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/troubleshooting)

[View general Cloud API Error Codes here](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/error-codes)

## User call permission reply webhook

This webhook is delivered whenever a user selects or updates their calling permissions. It could be in response to a call permission request sent by the business or it could be the user proactively making a decision.

The webhook fields values change depending on the circumstances of the user permission decision:

- the user accepts or rejects the request
- the user approves permission by responding to a request or by calling the business
- the user permission is an automatic callback permission in response to a user-initiated call
- the user permission is automatically revoked in response to 4 consecutive unanswered business-initiated calls

Lastly, the user can grant permanent calling permission to the business, which is represented in the `is_permanent` parameter.

No webhook is sent when a temporary permission expires. The `expiration_timestamp` field included in the accepted permission webhook indicates the time this permission will expire. Alternatively the current permission state can be queried from the [get current call permission state](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/user-call-permissions#get-current-call-permission-state) endpoint.

Webhook sample

```https
{
. . .

"messages": [{
    "from": "{customer_phone_number}",
    "id": "wamid.sH0kFlaCGg0xcvZbgmg90lHrg2dL",
    "timestamp": "{timestamp}",
    "context": {
          "from": "{customer_phone_number}",
          "id": "wamid.gBGGFlaCmZ9plHrf2Mh-o"
    },
    "interactive": {
       "type":  "call_permission_reply",
        "call_permission_reply": {
            "response":"accept",
            "is_permanent":false,
            "expiration_timestamp": "{timestamp}",
            "response_source": "user_action"
       }
    }
 ],
. . .
}
```

Webhook values

| Placeholder | Description |
| --- | --- |
| `customer_phone_number`<br>*String* | The phone number of the customer |
| `context.id`<br>*String* | Can be either of two values<br>Message ID of the permission request message sent by the business to the customer number. Shows when a permission decision is made by the user in response to a call permission request.Call ID of the missed call placed by the business to the customer number. Shows when callback permission is enabled in settings and the user calls the business. |
| `response`<br>*String* | The WhatsApp users response to the call permission request message<br>Can be `accept` or `reject` |
| `is_permanent`<br>*Boolean* | Indicates if the permission is permanent or not. For temporary permission this will always be false. |
| `expiration_timestamp`<br>*Integer* | Time in seconds when this call permission expires if the WhatsApp user approved it |
| `response_source`<br>*String* | The source of this permission<br>Possible values for accepted call permissions are:<br>`user_action`: User approved or rejected the permission`automatic`: An automatic permission approval due to the WhatsApp user initiating the call |

Webhook sample scenarios

| Scenario | Webhook sample |
| --- | --- |
| The WhatsApp user approves a temporary call permission from a call permission request message | `{<br>. . .<br><br>"messages": [{<br> "from": "{customer_phone_number}",<br> "id": "wamid.sH0kFlaCGg0xcvZbgmg90lHrg2dL",<br> "timestamp": "1767168000",<br> "context": {<br> "from": "{customer_phone_number}",<br> "id": "wamid.gBGGFlaCmZ9plHrf2Mh-o"<br> },<br> "interactive": {<br> "type": "call_permission_reply",<br> "call_permission_reply": {<br> "response":"accept",<br> "is_permanent":false,<br> "expiration_timestamp": "1768550400",<br> "response_source": "user_action"<br> }<br> }<br> ],<br>. . .<br>}` |
| The WhatsApp users approves a permanent call permission from a call permission request message | `{<br>. . .<br><br>"messages": [{<br> "from": "{customer_phone_number}",<br> "id": "wamid.sH0kFlaCGg0xcvZbgmg90lHrg2dL",<br> "timestamp": "1767168000",<br> "context": {<br> "from": "{customer_phone_number}",<br> "id": "wamid.gBGGFlaCmZ9plHrf2Mh-o"<br> },<br> "interactive": {<br> "type": "call_permission_reply",<br> "call_permission_reply": {<br> "response":"accept",<br> "is_permanent":true,<br> "response_source": "user_action"<br> }<br> }<br> ],<br>. . .<br>}` |
| The WhatsApp users approves a permanent call permission from the business profile | `{<br>. . .<br><br>"messages": [{<br> "from": "{customer_phone_number}",<br> "id": "wamid.sH0kFlaCGg0xcvZbgmg90lHrg2dL",<br> "timestamp": "1767168000",<br> "interactive": {<br> "type": "call_permission_reply",<br> "call_permission_reply": {<br> "response":"accept",<br> "is_permanent":true,<br> "response_source": "user_action"<br> }<br> }<br> ],<br>. . .<br>}` |
| The WhatsApp users rejects a call permission after receiving a call permission request message | `{<br>. . .<br><br>"messages": [{<br> "from": "{customer_phone_number}",<br> "id": "wamid.sH0kFlaCGg0xcvZbgmg90lHrg2dL",<br> "timestamp": "1767168000",<br> "context": {<br> "from": "{customer_phone_number}",<br> "id": "wamid.gBGGFlaCmZ9plHrf2Mh-o"<br> },<br> "interactive": {<br> "type": "call_permission_reply",<br> "call_permission_reply": {<br> "response":"reject",<br> "response_source": "user_action"<br> }<br> }<br> ],<br>. . .<br>}` |
| An automatic temporary callback permission is granted to the business when the WhatsApp user calls the business | `{<br>. . .<br><br>"messages": [{<br> "from": "{customer_phone_number}",<br> "id": "wamid.sH0kFlaCGg0xcvZbgmg90lHrg2dL",<br> "timestamp": "1767168000",<br> "context": {<br> "from": "{customer_phone_number}",<br> "id": "wacid.gBGGF4lasdnlasdHrf2Mh-o"<br> },<br> "interactive": {<br> "type": "call_permission_reply",<br> "call_permission_reply": {<br> "response":"accept",<br> "is_permanent":false,<br> "expiration_timestamp": "1768550400",<br> "response_source": "automatic"<br> }<br> }<br> ],<br>. . .<br>}` |
| A call permission is automatically revoked when a business makes 4 consecutive unanswered calls to the WhatsApp user | `{<br>. . .<br><br>"messages": [{<br> "from": "{customer_phone_number}",<br> "id": "wamid.sH0kFlaCGg0xcvZbgmg90lHrg2dL",<br> "timestamp": "1767168000",<br> "interactive": {<br> "type": "call_permission_reply",<br> "call_permission_reply": {<br> "response":"reject",<br> "response_source": "automatic"<br> }<br> }<br> ],<br>. . .<br>}` |
