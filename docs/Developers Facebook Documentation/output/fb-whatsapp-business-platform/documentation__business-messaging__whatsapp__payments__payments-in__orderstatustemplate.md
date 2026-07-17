# Send order status template message | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/orderstatustemplate_

---

# Send order status template message

Updated: Nov 14, 2025

## Overview

An Order status template is a template with interactive [components](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/components) that extends the call-to-action button to support updating order status through a template. It allows the businesses to update the order status outside of the [customer session window](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages#customer-service-windows) in use cases such as charging the card for past order and updating about a shipment on order placed in the past.

Upon receiving the payment signals, the businesses must update the order status to keep the user up to date. Currently we support the following order status values

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/580096545_24841067635515588_5834437320752684752_n.png?_nc_cat=111&ccb=1-7&_nc_sid=e280be&_nc_ohc=c6z-_Dz4qx0Q7kNvwFTfTpg&_nc_oc=AdrRm1k4qvR-syeCh7QwCZKUc5xufuvP8bA-6wQtRjImTEjzu2p982AnV-7QSd0SWqk&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=luOxijyThyVH8qj87OgqCw&_nc_ss=7b20f&oh=00_Af6zckRq2cOI-_pe9gPesmcGsrKnCjEjND5xcPyK1uCbgg&oe=6A1C2310)

| Value | Description |
| --- | --- |
| `pending` | User has not successfully paid yet |
| `processing` | User payment authorized, merchant/partner is fulfilling the order, performing service, etc. |
| `partially-shipped` | A portion of the products in the order have been shipped by the merchant |
| `shipped` | All the products in the order have been shipped by the merchant |
| `completed` | The order is completed and no further action is expected from the user or the partner/merchant |
| `canceled` | The partner/merchant would like to cancel the `order_details` message for the order/invoice. The status update will fail if there is already a `successful` or `pending` payment for this `order_details` message |

## Creating an order status template

To create an order status template, the business needs a business portfolio with a WhatsApp Business Account, and access to the WhatsApp Manager.

In **WhatsApp Manager** > **Account tools**:

1. Click on `create template`
2. Select `Utility` category to expand `Order details message` option
3. Enter the desired `template name` and supported `locale` Depending on the number of `locales` selected there will be an equal number of template variants and businesses need to fill in the template details in respective locale.
4. Please fill in template components such as `Body` and optional `footer` text and submit.
5. Once submitted, templates will be [categorized as per the guidelines](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-categorization#template-category-guidelines) and undergo the [approval process](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-review#approval-process) refrain from having [marketing content](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-categorization#marketing-templates) as part of template components.
6. The template will be approved or rejected after the template components are verified by the system. If business believe the category determined is not consistent with our template category guidelines, please confirm there are no [common issues](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-review) that leads to rejections and if you are looking for further clarification you may [request a review](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-categorization#requesting-review) of the template via [Business Support](https://business.facebook.com/business-support-home/)
7. Once approved template [status](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview#template-status) will be changed to `ACTIVE` Please be informed that template’s status can change automatically from `ACTIVE` to `PAUSED` or `DISABLED` based on customer feedback and engagement. We recommend that you [monitor status changes](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-review#common-rejection-reasons) and take appropriate actions whenever such change occurs.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/580081490_1541180930238272_2112454248678172804_n.gif?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=V8IG1y0uOIwQ7kNvwEsyHiX&_nc_oc=AdpJS2vxs-wjqK19vP1LEEBJSfyxs_oIWTQIpC5iMUug1x_y1pSeGkEoIRjzOqtLlOA&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=luOxijyThyVH8qj87OgqCw&_nc_ss=7b20f&oh=00_Af6TqH5l5uFhGBhFO1BUHIMiFg2VtzGWUMwbJJtRPTrcHA&oe=6A1C270D)

## Creating an order status template using template creation APIs

To create a template through API and understand the general syntax, required categories and
components please refer to our [Templates](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview) document. All the guidelines outlined above in creating templates apply through API as well.

Order status template is categorized as “Utility” template and apart from ‘name’ and ‘language’ of
choice, it has general template components such as BODY, FOOTER and additionally sub category as “ORDER_STATUS”.

```html
POST https://graph.facebook.com/<API_VERSION>/<WHATSAPP_BUSINESS_BUSINESS_ID>/message_templates
{
  "name": "<TEMPLATE_NAME>",
  "language": "<LANGUAGE_AND_LOCALE_CODE>",
  "category": "UTILITY",
  "sub_category": "ORDER_STATUS",
  "components": [
    {
      "type": "BODY",
      "text": "<TEMPLATE_BODY_TEXT>"
    },
    {
      "type": "FOOTER",
      "text": "<TEMPLATE_FOOTER_TEXT>"
    }
  ]
}
```

## Sending order status template message

Order status template message allows the businesses to send update on the status of the
order as template component parameters.

To send an order status template message, make a `POST` call to `/<PHONE_NUMBER_ID>/messages`
endpoint and attach a message object with `type=template`. Then, add a [template object](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api#template-object) with a
`order_status` component and parameters with latest status on order with order `reference-id`.

For example, the following sample describes how to send `shipped` status on the placed order.

```html
  curl -X  POST \
  'https://graph.facebook.com/<API_VERSION>/<FROM_PHONE_NUMBER_ID>/messages' \
 -H 'Authorization: Bearer <ACCESS_TOKEN>' \
 -H 'Content-Type: application/json' \
 -d '{
    "messaging_product": "whatsapp",
    "recipient_type": "individual",
    "to": "<PHONE_NUMBER>",
    "type": "template",
    "template":
    {
        "name": "<TEMPLATE_NAME>",
        "language":
        {
            "policy": "deterministic",
            "code": "<LANGUAGE_AND_LOCALE_CODE>"
        },
        "components":
        [
            {
                "type": "order_status",
                "parameters": [{
                    "type": "order_status",
                    "order_status":
                    {
                        "reference_id": "reference_id_value",
                        "order":
                        {
                            "status": "processing | partially_shipped | shipped | completed | canceled",
                            "description": "<OPTIONAL_DESCRIPTION>"
                        }
                    }
                }]
            }
        ]
    }
}
```

Upon sending an `order_status` message with an invalid transition, you will receive an error webhook with the error code `2046` and message `New order status was not correctly transitioned`.

## Canceling an order

An order can be canceled by sending an `order_status` message with the status `canceled`. The customer cannot pay for an order that is canceled. The customer receives an `order_status` message and the order details page is updated to show that the order is canceled and the `Continue` button removed. The optional text shown below `Order canceled` on the order details page can be specified using the description field in the `order_status` message.

An order can be canceled only if the user has not already paid for the order. If the user has paid and the business sends a order_status message with canceled status will receive an error webhook with error code `2047` and message `Could not change order status to 'canceled'`.
