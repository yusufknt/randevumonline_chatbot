# Payment Request CTA Templates (Brazil) | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/payment-request-cta_

---

# Payment Request CTA Templates (Brazil)

Updated: 2026-5-06

# WhatsApp Business Messaging API: Payment Request CTA Button (Brazil)

This feature is currently being rolled out and may not yet be available for your WhatsApp Business Account. If you do not see this option, it will be enabled for your account soon.

## Overview

**Payment request CTA buttons** enable merchants in Brazil to request payments from customers through template messages on WhatsApp, without requiring order details API integration. Merchants simply embed Pix, Boleto, or Payment Link information in their message templates, allowing customers to pay directly from the conversation.

## Key Benefits

- **Simplified Integration** Payment codes (Pix, Boleto, Payment Link) can be embedded in templates with minimal API complexity.
- **Flexible Payment Requests** Choose any supported payment method and customize payment details.
- **Flexible Button Combinations** Payment request buttons can be combined with other button types within a message template, allowing businesses to offer a variety of actions—not limited to payments—in a single message.
- **Multiple Payment Options** Businesses can include up to three payment request buttons in a message, each supporting a different payment method. This enables customers to choose their preferred payment option directly from the conversation.

## Supported Payment Methods

- **Pix Dynamic Code**
- **Boleto**
- **Payment Link**

## Creating a Payment Request Template on WhatsApp Manager

To create a template with payment request CTA, business needs a business portfolio with a WhatsApp Business Account.

In **WhatsApp Manager** > **Account tools**:

1. Click on `create template`
2. Select `Utility` or `Marketing` category to see the `Default` template format option.
3. Select `Default` template format, and click **Next**
4. Enter the desired `template name` and supported `locale` Depending on the number of `locales` selected there will be an equal number of template variants and businesses need to fill in the template details in respective locale.
5. Fill in template components such as `Header` , `Body` and optional `footer` text. For the `Header`, you can choose one of three media types: `Text`, `Image` or `Document`. Choose `Document` if you want to send **PDF files** in the header of this template.
6. Add a button of type ‘Request Payment’ from the Buttons menu.
7. Select ‘Pix’, ‘Boleto’, or ‘Payment Link’ from the Payment Type dropdown menu.
Enter a sample value in the provided field. Note: The value entered is for demonstration purposes only. The actual code or URI will be unique to each customer interaction and will be included in the send payload.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/643964605_1446106083914708_4271285282642761996_n.png?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=wfUEG0-PbIkQ7kNvwHL30pM&_nc_oc=AdrBPaFvWjWYR0zuD8v3iMDisZNi-5GU-jpCBW9aGUIsbXlQUqta2-4c_HKGitxXrho&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=baQMk1iWZieWZl5lb5jfGg&_nc_ss=7b20f&oh=00_Af6eG5nl7PBza_knpYCvkRwbOyxd4Pgvm0yBZrZVOtOUSg&oe=6A1C3861)

1. Click submit.
2. Once submitted, templates will be [categorized as per the guidelines](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-categorization#template-category-guidelines) and undergo the [approval process](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-review#approval-process) .
3. The template will be approved or rejected after the template components are verified by the system. If business believe the category determined is not consistent with our template category guidelines, please confirm there are no [common issues](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-review) that leads to rejections and if you are looking for further clarification you may [request a review](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-categorization#requesting-review) of the template via [Business Support](https://business.facebook.com/business-support-home/)
. Once approved template [status](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview#template-status) will be changed to `ACTIVE`Please be informed that template’s status can change automatically from `ACTIVE` to `PAUSED` or `DISABLED` based on customer feedback and engagement. We recommend that you [monitor status changes](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-review#common-rejection-reasons) and take appropriate actions whenever such change occurs.

## Creating a Payment Request Template Using APIs

Endpoint

```bash
POST /{WHATSAPP_BUSINESS_ACCOUNT_ID}/message_templates
```

Request body

```json
{
  "name": "<TEMPLATE_NAME>",
  "language": "<TEMPLATE_LANGUAGE_CODE>",
  "category": "UTILITY",
  "components": [
    {
      "type": "HEADER",
      "format": "text",
      "text": "Header Text"
    },
    {
      "type": "BODY",
      "text": "Body Text"
    },
    {
      "type": "FOOTER",
      "text": "Footer text"
    },
    {
      "type": "BUTTONS",
      "buttons": [
        {
          "type": "PAYMENT_REQUEST",
          "text": "Copy Boleto code",
          "payment_setting": {
            "type": "boleto",
            "boleto": {
              "digitable_line": "03399026944140000002628346101018898510000008848"
            }
          }
        },
        {
          "type": "PAYMENT_REQUEST",
          "text": "Copy Pix code",
          "payment_setting": {
            "type": "pix_dynamic_code",
            "pix_dynamic_code": {
              "code": "00020101021226700014br.gov.bcb.pix2548pix.example.com..."
            }
          }
        },
        {
          "type": "PAYMENT_REQUEST",
          "text": "Open payment link",
          "payment_setting": {
            "type": "payment_link",
            "payment_link": {
              "uri": "https://my-payment-link-url"
            }
          }
        }
      ]
    }
  ]
}
```

Example response

```json
{
  "id": "123455683495832",
  "status": "Approved",
  "category": "UTILITY"
}
```

## Sending Payment Request Messages

The following image shows examples of payment request template messages rendered in WhatsApp, with Pix, Boleto, and Payment Link buttons respectively.

![Three examples of payment request CTA template messages in WhatsApp showing Pix, Boleto, and Payment Link buttons](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/671726563_1482845433574106_2190347823547508578_n.png?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=0BuwGjRqfH0Q7kNvwEOvxfq&_nc_oc=AdoP1_irp2jf8FICJCY8ave19i7jrBQEoFIRvceUjjSj8fAyWa_aDwv1BfeEBcmqsjA&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=baQMk1iWZieWZl5lb5jfGg&_nc_ss=7b20f&oh=00_Af7NWKfhiFVFvURzDBsvb2Eg2gGHev3GM13fbqGlTa2Ucg&oe=6A1C338C)

Endpoint

```bash
POST /{PHONE_NUMBER_ID}/messages
```

Request body

```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "<PHONE_NUMBER>",
  "type": "template",
  "template": {
    "name": "<TEMPLATE_NAME>",
    "language": {
      "code": "<LANGUAGE>"
    },
    "components": [
      {
        "type": "button",
        "sub_type": "payment_request",
        "index": "0",
        "parameters": [
          {
            "type": "action",
            "action": {
              "payment_request": {
                "payment_setting": {
                  "type": "boleto",
                  "boleto": {
                    "digitable_line": "03399026944140000002628346101018898510000008848"
                  }
                }
              }
            }
          }
        ]
      },
      {
        "type": "button",
        "sub_type": "payment_request",
        "index": "1",
        "parameters": [
          {
            "type": "action",
            "action": {
              "payment_request": {
                "payment_setting": {
                  "type": "pix_dynamic_code",
                  "pix_dynamic_code": {
                    "code": "00020101021226700014br.gov.bcb.pix2548pix.example.com..."
                  }
                }
              }
            }
          }
        ]
      },
      {
        "type": "button",
        "sub_type": "payment_request",
        "index": "2",
        "parameters": [
          {
            "type": "action",
            "action": {
              "payment_request": {
                "payment_setting": {
                  "type": "payment_link",
                  "payment_link": {
                    "uri": "https://my-payment-link-url"
                  }
                }
              }
            }
          }
        ]
      }
    ]
  }
}
```

Example response

```json
{
  "messaging_product": "whatsapp",
  "contacts": [
    {
      "input": "<PHONE_NUMBER>",
      "wa_id": "<PHONE_NUMBER>"
    }
  ],
  "messages": [
    {
      "id": "wamid.HBgNNTUxMTk4Nzg2NjI5NRUCABEYEjUxOTBGNEU0RDA2MjdCMUVBOQA=",
      "message_status": "accepted"
    }
  ]
}
```

## Combining with limited-time offer templates

Payment request CTA buttons can be combined with limited-time offer templates to send time-sensitive payment requests that display a countdown timer alongside payment options. To add the `limited_time_offer` component to your template, include it in the `components` array of your [template creation payload](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/payment-request-cta#creating-a-payment-request-template-using-apis). For the full component schema, supported header formats, and button ordering requirements, see [Limited-time offer templates](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/marketing-templates/limited-time-offer-templates).

The following images show examples of limited-time offer templates combined with payment request CTA buttons rendered in WhatsApp.

![Limited-time offer template with a payment link button and a URL button in WhatsApp](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/670598387_1482845463574103_1631971666174253422_n.png?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=fZOklzlR_0wQ7kNvwGaIiw3&_nc_oc=AdpF5ShqLqgQ5NubaSwBBoXDXE1ATSTcgZxBaDINjlNvmk0hPv8_5vW0Ve397HsSH7U&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=baQMk1iWZieWZl5lb5jfGg&_nc_ss=7b20f&oh=00_Af5JEgBXCKHLGgwOH8HLwrJIPYBchGy3Z_fBjAx94p39yg&oe=6A1C0066)![Limited-time offer template with Pix code and payment link buttons in WhatsApp](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/670446224_1482845466907436_5665108244682362561_n.png?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=tgGVdBqqsaUQ7kNvwH9gYgn&_nc_oc=AdquxL8Io6WsXjAnv891bW36aT3gVYVYsvVxPABp0tKhiNZKlwMgrp3FwBouRZtKQRw&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=baQMk1iWZieWZl5lb5jfGg&_nc_ss=7b20f&oh=00_Af6Jsm3gZeR_1KiPCg1Ru2B-vCD87JxcI1lkcBWbUIoUIA&oe=6A1C0FDF)

### Managing payment code and link expiration

The payment request CTA button remains active in the conversation even after the limited-time offer is displayed as expired. WhatsApp does not automatically disable the payment button when the Pix code, Boleto, or Payment Link is no longer valid. You are responsible for managing the expiration of the underlying payment code or link to match your offer’s validity — whether the offer is time-bound, inventory-limited, or invalidated for any other reason.

## Parameters

Buttons Object

| Field Name | Optional? | Type | Description |
| --- | --- | --- | --- |
| `type` | Required | String | Must be `PAYMENT_REQUEST` for payment messages. |
| `text` | Required | String | The button label. Must be `Copy Pix code` for `pix_dynamic_code`, `Copy Boleto code` for `boleto`, or `Open payment link` for `payment_link`. |
| `payment_setting` | Required | [Payment Setting Object](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-br/payment-request-cta#paymentsettingsobject) | Payment configuration object. |

Payment Setting

| Field Name | Optional? | Type | Description |
| --- | --- | --- | --- |
| `type` | Required | String | One of `pix_dynamic_code`, `payment_link`, `boleto`. |
| One of the following objects: `pix_dynamic_code`, `payment_link`, `boleto`. | Required | Object | Payment instructions which will be displayed to buyers during the checkout process. |

Dynamic Pix code object

| Field Name | Optional? | Type | Description |
| --- | --- | --- | --- |
| `pix_dynamic_code` | Required | String | The dynamic Pix code which will be copied by the buyer. |

Payment link object

| Field Name | Optional? | Type | Description |
| --- | --- | --- | --- |
| `uri` | Required | String | The Payment Link’s uri which will be opened in the web browser, when user taps on the Payment Link CTA button. |

Boleto object

| Field Name | Optional? | Type | Description |
| --- | --- | --- | --- |
| `digitable_line` | Required | String | The Boleto digital line / code which will be copied to the clipboard, when user taps on the Boleto CTA button. |
