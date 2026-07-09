# message_template_components_update webhook reference | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/message_template_components_update_

---

# message_template_components_update webhook reference

Updated: Nov 14, 2025

This reference describes trigger events and payload contents for the WhatsApp Business Account `message_template_components_update` webhook.

The **message_template_components_update** webhook notifies you of changes to a template’s components.

## Triggers

- A template is edited.

## Syntax

```html
{
  "entry": [
    {
      "id": "<WHATSAPP_BUSINESS_ACCOUNT_ID>",
      "time": <WEBHOOK_TRIGGER_TIMESTAMP>,
      "changes": [
        {
          "value": {
            "message_template_id": <TEMPLATE_ID>,
            "message_template_name": "<TEMPLATE_NAME>",
            "message_template_language": "<TEMPLATE_LANGUAGE_AND_LOCALE_CODE>",
            "message_template_element": "<TEMPLATE_BODY_TEXT>,

            <!-- only included if template has a text header -->
            "message_template_title": "<TEMPLATE_HEADER_TEXT>",

            <!-- only included if template has a footer -->
            "message_template_footer": "<TEMPLATE_FOOTER_TEXT>",

            <!-- only included if template has a url or phone number button -->
            "message_template_buttons": [
              {
                "message_template_button_type": "<BUTTON_TYPE>",
                "message_template_button_text": "<BUTTON_LABEL_TEXT>",

                <!--only included for url buttons -->
                "message_template_button_url": "<BUTTON_URL>",

                <!--only included for phone number buttons -->
                "message_template_button_phone_number": "<BUTTON_PHONE_NUMBER>"
              }
            ]
          },
          "field": "message_template_components_update"
        }
      ]
    }
  ],
  "object": "whatsapp_business_account"
}
```

## Parameters

| Placeholder | Description | Example value |
| --- | --- | --- |
| `<BUTTON_LABEL_TEXT>`<br>*String* | Button label text. | `Email support` |
| `<BUTTON_PHONE_NUMBER>`<br>*String* | Button phone number. | `+15550783881` |
| `<BUTTON_TYPE>`<br>*String* | [Button type](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/components#buttons).<br>Values can include:<br>`CATALOG``COPY_CODE``EXTENSION``FLOW`, `MPM``ORDER_DETAILS``OTP``PHONE_NUMBER``POSTBACK``REMINDER``SEND_LOCATION``SPM``QUICK_REPLY``URL``VOICE_CALL` | `URL` |
| `<BUTTON_URL>`<br>*String* | Button URL. | `https://www.luckyshrub.com/support` |
| `<TEMPLATE_BODY_TEXT>`<br>*String* | Template body text. | `Thank you for your order, {{1}}! Your order number is {{2}}. If you have any questions, contact support using the buttons below. Thanks again!` |
| `<TEMPLATE_FOOTER_TEXT>`<br>*String* | Template footer text. | `Lucky Shrub: the Succulent Specialists!` |
| `<TEMPLATE_HEADER_TEXT>`<br>*String* | Template header text. | `Your order is confirmed!` |
| `<TEMPLATE_ID>`<br>*Integer* | Template ID. | `1315502779341834` |
| `<TEMPLATE_LANGUAGE_AND_LOCALE_CODE>`<br>*String* | Template [language and locale](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/supported-languages) code. | `en_US` |
| `<TEMPLATE_NAME>`<br>*String* | Template name. | `order_confirmation` |
| `<WEBHOOK_TRIGGER_TIMESTAMP>`<br>*Integer* | Unix timestamp indicating when the webhook was triggered. | `1739321024` |
| `<WHATSAPP_BUSINESS_ACCOUNT_ID>`<br>*String* | WhatsApp Business Account ID. | `102290129340398` |

## Example

```json
{
  "entry": [
    {
      "id": "102290129340398",
      "time": 1751250234,
      "changes": [
        {
          "value": {
            "message_template_id": 1315502779341834,
            "message_template_name": "order_confirmation",
            "message_template_language": "en_US",
            "message_template_title": "Your order is confirmed!",
            "message_template_element": "Thank you for your order, {{1}}! Your order number is {{2}}. If you have any questions, contact support using the buttons below. Thanks again!",
            "message_template_footer": "Lucky Shrub: the Succulent Specialists!",
            "message_template_buttons": [
              {
                "message_template_button_type": "PHONE_NUMBER",
                "message_template_button_text": "Phone support",
                "message_template_button_phone_number": "+15550783881"
              },
              {
                "message_template_button_type": "URL",
                "message_template_button_text": "Email support",
                "message_template_button_url": "https://www.luckyshrub.com/support"
              }
            ]
          },
          "field": "message_template_components_update"
        }
      ]
    }
  ],
  "object": "whatsapp_business_account"
}
```
