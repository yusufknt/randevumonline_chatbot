# Send order details template message | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/orderdetailstemplate_

---

# Send order details template message

Updated: Oct 31, 2025

## Overview

Order details message template is a template with [interactive components](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview#components) that extends the call-to-action button to support sending order details and provides a richer experience compared to templates with only text components.

Once your Order details message templates have been created and approved, you can use the approved template to send the template message with order or bill information to prompt them to make a payment.

Before sending an order details template message, businesses need to create a template with an “open order details” call-to-action button. See [Create Message Templates for Your WhatsApp Business Account](https://www.facebook.com/business/help/2055875911147364?id=2129163877102343) for more information on prerequisites and how to create a template.

## Creating an order details template on WhatsApp Manager

To create an order details template, business needs a business portfolio with a WhatsApp Business Account.

In **WhatsApp Manager** > **Account tools**:

1. Click on `create template`
2. Select `Utility` category to expand `Order details message` option
3. Enter the desired `template name` and supported `locale` Depending on the number of `locales` selected there will be an equal number of template variants and businesses need to fill in the template details in respective locale.
4. Please fill in template components such as `Header` , `Body` and optional `footer` text and submit.
5. Once submitted, templates will be [categorized as per the guidelines](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-categorization#template-category-guidelines) and undergo the [approval process](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-review#approval-process) refrain from having [marketing content](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-categorization#marketing-templates) as part of template components.
6. The template will be approved or rejected after the template components are verified by the system. If business believe the category determined is not consistent with our template category guidelines, please confirm there are no [common issues](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-review) that leads to rejections and if you are looking for further clarification you may [request a review](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-categorization#requesting-review) of the template via [Business Support](https://business.facebook.com/business-support-home/)
7. Once approved template [status](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview#template-status) will be changed to `ACTIVE` Please be informed that template’s status can change automatically from `ACTIVE` to `PAUSED` or `DISABLED` based on customer feedback and engagement. We recommend that you [monitor status changes](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-review#common-rejection-reasons) and take appropriate actions whenever such change occurs.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/561631212_1339317814593536_2945252722681774358_n.jpg?_nc_cat=106&ccb=1-7&_nc_sid=e280be&_nc_ohc=lESN5fgVd40Q7kNvwGcqsFn&_nc_oc=AdpTaDRqhAQXohPFWklWRflqtN6j6Tc7BVXxl1UTl4qptFtb5BhYjKAlV3eQBLUt0kA&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=QiI6mfmDYpPAU01bDpPZpg&_nc_ss=7b20f&oh=00_Af6dHgcDVy0o2Vbw2TKW68HKkPqZgfHySA-wENhIjKcyng&oe=6A1C077D)

## Creating an order details template using template creation APIs

To create a template through API and understand the general syntax, required categories and
components please refer to [templates API](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview#creating-templates). All the guidelines outlined above in creating templates apply through API as well.

Order details template is categorized as “Utility” template and apart from ‘name’ and ‘language’ of
choice, it has general template components such as HEADER, BODY, FOOTER and a fixed BUTTON with “ORDER_DETAILS” type and “Review and Pay” text.

```html
POST https://graph.facebook.com/<API_VERSION>/<WHATSAPP_BUSINESS_BUSINESS_ID>/message_templates
{
  "name": "<TEMPLATE_NAME>",
  "language": "<LANGUAGE_AND_LOCALE_CODE>",
  "category": "UTILITY",
  /* Businesses can create the order details template under marketing category by including display_format attribute */
  /* "display_format": "order_details",*/
  "components": [
    {
      "type": "HEADER",
      "format": "TEXT",
      "text": "<TEMPLATE_HEADER_TEXT>"
    },
    {
      "type": "BODY",
      "text": "<TEMPLATE_BODY_TEXT>"
    },
    {
      "type": "FOOTER",
      "text": "<TEMPLATE_FOOTER_TEXT>"
    },
    {
      "type": "BUTTONS",
      "buttons": [
        {
          "type": "ORDER_DETAILS",
          "text": "Review and Pay"
        }
      ]
    }
  ]
}
```

## Sending order details template message

Order details template message allows the businesses to send invoice(order_details) message as predefined `Open order details` call-to-action button component parameters. It supports businesses to send all payment integration (such as [UPI Intent](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/upi-intent#step-2--assemble-the-interactive-object), [Payment Gateway](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/pg#step-1) or [Payment Links](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/payment-links#step-2--assemble-the-interactive-object)) integration as button parameters.

To send an order details template message, make a `POST` call to `/PHONE_NUMBER_ID/messages` endpoint and attach a message object with `type=template`. Then, add a template object with a predefined `Open order details` call-to-action button.

For example following sample describes how to send [UPI Intent](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/upi-intent#step-2--assemble-the-interactive-object) in order details template message parameters to prompt the consumer to make a payment.

The below example shows an example payload with `upi` as the payment type. For other variants of the `payment_settings` block (for example, for the type `payment_gateway` type), refer to this [document](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/pg#step-1).

```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "<PHONE_NUMBER>",
  "type": "template",
  "template": {
    "name": "<TEMPLATE_NAME>",
    "language": {
      "policy": "deterministic",
      "code": "<LANGUAGE_AND_LOCALE_CODE>"
    },
    "components": [
      {
        "type": "header",
        "parameters": [
          {
            "type": "image", // Uses header with image as an example
            "image": {
              "link": "http(s)://the-url"
            }
          }
        ]
      },
      {
        "type": "button",
        "sub_type": "order_details",
        "index": 0,
        "parameters": [
          {
            "type": "action",
            "action": {
              "order_details": {
                "currency": "INR",
                "order": {
                  "discount": {
                    "offset": 100,
                    "value": 250
                  },
                  "items": [
                    {
                      "amount": {
                        "offset": 100,
                        "value": 400
                      },
                      "name": "<ORDER_ITEM_NAME>",
                      "quantity": 1,
                      "retailer_id": "<ORDER_ITEM_RETAILER_ID>",
                      "country_of_origin": "<ORIGIN_COUNTRY>",
                      "importer_name": "<IMPORTER_NAME>",
                      "importer_address": {
                        "address_line1": "<IMPORTER_ADDRESS>",
                        "city": "<CITY>",
                        "country_code": "<COUNTRY>",
                        "postal_code": "<ZIP_CODE>"
                      }
                    }
                  ],
                  "shipping": {
                    "offset": 100,
                    "value": 0
                  },
                  "status": "pending",
                  "subtotal": {
                    "offset": 100,
                    "value": 400
                  },
                  "tax": {
                    "offset": 100,
                    "value": 500
                  }
                },
                "payment_settings": [
                  {
                    "type": "upi_intent_link",
                    "upi_intent_link": {
                      "link": "upi://pay?pa=merchant_vpa&pn=merchant%20Name&mc=mc_code&purpose=purpose_code&tr=transaction_record"
                    }
                  }
                ],
                "payment_configuration": "unique_payment_config_id",
                "payment_type": "upi",
                "reference_id": "reference_id_value",
                "total_amount": {
                  "offset": 100,
                  "value": 650
                },
                "type": "digital-goods"
              }
            }
          }
        ]
      }
    ]
  }
}
```

Once the order details template message is delivered, a successful response will include an object with an identifier prefixed with wamid. Use the ID listed after wamid to track your message status.

```json
{
    "messaging_product": "whatsapp",
    "contacts": [
        {
            "input": "<PHONE_NUMBER>",
            "wa_id": "<WHATSAPP_ID>"
        }
    ],
    "messages": [
        {
            "id": "wamid.ID"
        }
    ]
}
```

## Post order details template message flow

After the order details template message delivery the rest of the payment flow is the same as “Sending invoice in customer session window” and depends on the chosen [payment integration](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/overview) order details parameters. For more details refer [UPI Intent](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/upi-intent#step-5--consumer-pays-for-the-order), [Payment Gateway](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/pg#step-2--receive-webhook-about-transaction-status) and [Payment Links](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/payment-links#step-5--consumer-pays-for-the-order) post payments flows.
