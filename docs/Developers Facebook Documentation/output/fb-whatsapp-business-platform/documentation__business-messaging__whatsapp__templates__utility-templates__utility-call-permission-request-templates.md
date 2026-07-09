# Call permission request templates | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/utility-templates/utility-call-permission-request-templates_

---

# Call permission request templates

Updated: Apr 22, 2026

Call permission request templates allow you to request permission to call WhatsApp users. They are composed of a required **body** component and a **call permission request** component. When a WhatsApp user receives the message, they can grant or deny your business permission to call them.

Call permission request templates can be categorized as either `MARKETING` or `UTILITY`. This page demonstrates creating and sending a call permission request template with the `UTILITY` category. See [Call permission request message template](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/marketing-templates/call-permission-request-message-template/) for a marketing example.

![A call permission request template message in WhatsApp showing the body text with the first_name parameter resolved to Pablo, and an annotated callout pointing to the call permission request component](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/672686350_1488549909670325_2826717779551935932_n.jpg?_nc_cat=111&ccb=1-7&_nc_sid=e280be&_nc_ohc=tqkPuStCuRYQ7kNvwG5rhNG&_nc_oc=AdpjYEJ8revHhYYLDGR1JTN-mO9FJGzX-ae6L_fijKxCCvHvcEVU5qzygwFqUHqDwLs&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=diOta9FZhgWfW6qN_UDdZQ&_nc_ss=7b20f&oh=00_Af5Z_CMBeRSMuMqC08nlL6gYo3r9fl_0lbJ6hU3xP537YQ&oe=6A1C075D)

## Limitations

- Only templates categorized as `MARKETING` or `UTILITY` can include a call permission request component
- Body text is required and must not be empty
- The call permission request component cannot be combined with other interactive components

## Create a call permission request template

Use the [Message Templates API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/template-api) to [create a call permission request template](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/template-api#post-version-waba-id-message-templates).

### Request syntax

```bash
curl -X POST \
  'https://graph.facebook.com/<API_VERSION>/<WHATSAPP_BUSINESS_ACCOUNT_ID>/message_templates' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "<TEMPLATE_NAME>",
    "language": "<TEMPLATE_LANGUAGE>",
    "category": "<CATEGORY>",
    "parameter_format": "named",
    "components": [
      {
        "type": "body",
        "text": "<BODY_TEXT>",
        "example": {
          "body_text_named_params": [
            {
              "param_name": "<PARAM_NAME>",
              "example": "<EXAMPLE_PARAM_VALUE>"
            }
          ]
        }
      },
      {
        "type": "call_permission_request"
      }
   ]
}'
```

### Request parameters

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<ACCESS_TOKEN>`<br>*String* | **Required.**<br>[System token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens) or [business token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens). | `EAAA...` |
| `<API_VERSION>`<br>*String* | **Optional.**<br>Graph API version. | v25.0 |
| `<BODY_TEXT>`<br>*String* | **Required.**<br>Body text string. Supports named parameters in `{{parameter_name}}` format.<br>Maximum 1024 characters. | `Hi {{first_name}}, we would like to call you to assist with your recent order. Our support team is ready to help.` |
| `<CATEGORY>`<br>*Enum* | **Required.**<br>Template category. Must be `MARKETING` or `UTILITY`. | `UTILITY` |
| `<EXAMPLE_PARAM_VALUE>`<br>*String* | **Required if body text uses named parameters.**<br>Example value for the named parameter. | `Pablo` |
| `<PARAM_NAME>`<br>*String* | **Required if body text uses named parameters.**<br>Name of the parameter, matching the placeholder in the body text. | `first_name` |
| `<TEMPLATE_LANGUAGE>`<br>*Enum* | **Required.**<br>Template [language and locale code](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/supported-languages). | `en_US` |
| `<TEMPLATE_NAME>`<br>*String* | **Required.**<br>Template name.<br>Maximum 512 characters. | `order_support_call` |
| `<WHATSAPP_BUSINESS_ACCOUNT_ID>`<br>*String* | **Required.**<br>WhatsApp Business account ID. | `106540352242922` |

### Example request

```bash
curl -X POST \
  'https://graph.facebook.com/v23.0/106540352242922/message_templates' \
  -H 'Authorization: Bearer EAAJB...' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "order_support_call",
    "language": "en_US",
    "category": "UTILITY",
    "parameter_format": "named",
    "components": [
      {
        "type": "body",
        "text": "Hi {{first_name}}, we would like to call you to assist with your recent order. Our support team is ready to help.",
        "example": {
          "body_text_named_params": [
            {
              "param_name": "first_name",
              "example": "Pablo"
            }
          ]
        }
      },
      {
        "type": "call_permission_request"
      }
   ]
}'
```

### Example response

```json
{
  "id": "546151681022936",
  "status": "PENDING",
  "category": "UTILITY"
}
```

## Send a call permission request template

Use the [Messages API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api) to [send an approved call permission request template](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api#post-version-phone-number-id-messages) in a template message.

### Request syntax

```bash
curl -X POST \
  'https://graph.facebook.com/<API_VERSION>/<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>/messages' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
    "messaging_product": "whatsapp",
    "recipient_type": "individual",
    "to": "<WHATSAPP_USER_PHONE_NUMBER>",
    "type": "template",
    "template": {
      "name": "<TEMPLATE_NAME>",
      "language": {
        "policy": "deterministic",
        "code": "<TEMPLATE_LANGUAGE_CODE>"
      },
      "components": [
        {
          "type": "body",
          "parameters": [
            {
              "type": "text",
              "parameter_name": "<PARAM_NAME>",
              "text": "<PARAM_VALUE>"
            }
          ]
        }
      ]
    }
}'
```

### Request parameters

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<ACCESS_TOKEN>`<br>*String* | **Required.**<br>[System token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens) or [business token](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#business-integration-system-user-access-tokens). | `EAAA...` |
| `<API_VERSION>`<br>*String* | **Optional.**<br>Graph API version. | v25.0 |
| `<PARAM_NAME>`<br>*String* | **Required if the template body uses named parameters.**<br>Name of the parameter to replace in the template body. | `first_name` |
| `<PARAM_VALUE>`<br>*String* | **Required if the template body uses named parameters.**<br>Value to substitute for the named parameter. | `Pablo` |
| `<TEMPLATE_LANGUAGE_CODE>`<br>*Enum* | **Required.**<br>Template [language and locale code](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/supported-languages). | `en_US` |
| `<TEMPLATE_NAME>`<br>*String* | **Required.**<br>Name of the template to send. | `order_support_call` |
| `<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>`<br>*String* | **Required.**<br>WhatsApp business phone number ID. | `106540352242922` |
| `<WHATSAPP_USER_PHONE_NUMBER>`<br>*String* | **Required.**<br>WhatsApp user phone number. | `+16505551234` |

### Example request

```bash
curl -X POST \
  'https://graph.facebook.com/v23.0/106540352242922/messages' \
  -H 'Authorization: Bearer EAAJB...' \
  -H 'Content-Type: application/json' \
  -d '{
    "messaging_product": "whatsapp",
    "recipient_type": "individual",
    "to": "+15551234567",
    "type": "template",
    "template": {
      "name": "order_support_call",
      "language": {
        "policy": "deterministic",
        "code": "en_US"
      },
      "components": [
        {
          "type": "body",
          "parameters": [
            {
              "type": "text",
              "parameter_name": "first_name",
              "text": "Pablo"
            }
          ]
        }
      ]
    }
}'
```

### Example response

```json
{
  "messaging_product": "whatsapp",
  "contacts": [
    {
      "input": "+15551234567",
      "wa_id": "15551234567"
    }
  ],
  "messages": [
    {
      "id": "wamid.HBgLMTMyMzI4NjU2NzgVAgARGBJBQzRBRDBEMDEwQzVBM0M0QkIA",
      "message_status": "accepted"
    }
  ]
}
```
