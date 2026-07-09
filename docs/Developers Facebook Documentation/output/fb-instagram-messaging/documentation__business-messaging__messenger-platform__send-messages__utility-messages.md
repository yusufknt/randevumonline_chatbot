# Developer Platform

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/utility-messages_

---

# Send a utility message

Updated: Mar 13, 2026

This document shows you how to send a utility message.

What’s a utility message?

A utility message is a message, created from a template, sent to your customers that contain order or account status updates, and appointment or event reminders, and can be personalized with a customer’s name, locale, appointment or event date, and more. A utility message template contains placeholder values such as a person’s name, order id, tracking number, and so on, that are filled in at the time the message is sent to the consumer. Your app users can create their own utility message templates or use one of Meta’s utility message templates to create these messages.

### How it works

There are a number of flows for your app users to send utility messages:

**Use a Meta template**

1. Search for a template
2. Clone it to the Page’s template library
3. Send a message

Create and send a Page-owned template

1. Create a template
2. Receive approval (within seconds of creation)
3. Send a message

Use an existing Page-owned template

1. Search for a template (already approved)
2. Send a message

**Note:** Facebook Pages are not required to be linked to a business to send utility messages.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/652657104_1459945485864101_3844678865154611518_n.png?_nc_cat=110&ccb=1-7&_nc_sid=e280be&_nc_ohc=ryNnyBaUQoIQ7kNvwFESenQ&_nc_oc=Adpcy_6gy3ansei4w-c0wsT_awYwHctcziCyFQvwvk75p5LW4Pc_dDRC5Els4nZL54k&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=1SG7jKFcsKh21N4ZtoBekw&_nc_ss=7b20f&oh=00_Af7MAEgYu_FQEjpZ8rKu2Doq4994r23Szls0udq4_7AGnw&oe=6A1C4539)

## Before You Start

This guide assumes you have set up your webhooks server to receive notifications and subscribed to the `message_template_status_update` field as well as other webhook messaging fields your app user’s utility messages need.

You need the following:

- The ID for the Page sending the message
- The Page-scoped ID of the customer receiving the message
- A Page access token from your app user who is sending the message
- Your app user has granted your app the `page_utility_messaging` permission

### Limitations

- Utility messages must not contain marketing materials. Learn more in our [Marketing Messages documentation](https://developers.facebook.com/docs/messenger-platform/marketing-messages) .

## Meta utility message templates

Meta has a number of pre-approved templates that your app users can use to send utility templates.

### Step 1. Search for a template

To get a list of Meta utility message templates, send a `GET` request to the `/message_template_library` endpoint. Add additional parameters to refine your search. In the following example we are searching for English templates that include the word “order” in the name or message content.

```html
curl -X GET "https://graph.facebook.com/v25.0/message_template_library?name_or_content=order&language=en?access_token=EAACE..."
```

On success your app receives a JSON response with a list of templates that match the query. The template’s `name` value is needed to use the template for your app user’s utility messages.

```html
{
  "data": [
    {
      "name": "order_confirmation_1",
      "language": "en",
      "category": "UTILITY",
      "topic": "ORDER_MANAGEMENT",
      "usecase": "DELIVERY_CONFIRMATION",
      "industry": [
        "E_COMMERCE"
      ],
      "body": "{{1}}, your order was successfully delivered!

You can track your package and manage your order below.",
      "body_params": [
        "John"
      ],
      "body_param_types": [
        "TEXT"
      ],
      "buttons": [
        {
          "type": "URL",
          "text": "Manage order",
          "url": "https://www.example.com"
        }
      ],
      "id": "7635027653257090"
    },
    ...                               // List is truncated for brevity
  ]
}
```

### Step 2. Clone the template

To clone a Meta utility message template to a Page’s template library, send a `POST` request to the `/<PAGE_ID>/message_templates` endpoint with the following parameters:

- `name` set to the name of the cloned template
- `category` set to `UTILITY`
- `language` set to the language code for this message
- `library_template_name` set to the name of the Meta template being cloned ( `order_confirmation_1` )

In the following example, the the cloned template requires the additional `library_template_body_inputs` and `library_template_button_inputs` parameters set to the components containing the app user’s values.

```html
curl -X POST -H "Content-Type: application/json"
     -d '{
           "name": "jaspers_market_order_confirmation_1",
           "category": "UTILITY",
           "language": "en_US",
           "library_template_name”: "order_confirmation_1",
           "library_template_body_inputs": [
             {
                "type": "body",
                "text": "{{1}}, your order was successfully delivered!\n\n You can track your package and manage your order below."
             }
           ],
           "library_template_button_inputs": [
             {
                "type": "URL",
                "text": "Manage your order",
                "url": {
                  "base_url": "https://www.jaspersmarket.com/"
                }
             }
           ]
         }' "https://graph.facebook.com/v25.0/1909458034523498/message_templates?access_token=EAACE..."
```

On success your app receives a JSON response with the template’s ID, the approval status, and the template category.

```
{
  "id": "102295129340398",
  "status": "APPROVED",
  "category": "UTILITY"
}
```

### Step 3. Send a message

To send a utility message from a cloned Meta template, send a `POST` request to the `/<PAGE_ID>/messages` endpoint with the following parameters:

- `recipient.id` set to the Page-scoped ID for the person your app user is sending the message to
- `messaging_type` set to `UTILITY`
- `template` with the following parameters: `name` set to the name of the specific template being used to create the message`language.code` set to the language code for this message`components` array with the following parameters:
 `type` set to `body``parameters.type` set to `text``parameter.text` set to the input needed for the template

```html
curl -X POST -H "Content-Type: application/json" -d '{
  "recipient": {
    "id":"2348927398743287"
  },
  "template": {
    "name": "jaspers_market_order_confirmation_1",
    "language": { "code": "en" },
    "components": [
      {
        "type": "body",
        "parameters": [
          {
            "type": "body",
            "text": "566701"
          }
        ]
      }
    ]
  }
}' "https://graph.facebook.com/v25.0/1909458034523498/messages?access_token=EAACE..."
```

## Page-owned utility message template

Your app users can create their own template for their utility messages.

### Step 1. Create a Page-owned template

To create a utility message template, send a `POST` request to the `/<PAGE_ID>/message_templates` endpoint with the following required parameters:

- `name` set to the name of the template
- `language` set to the language of the message text
- `category` set to `UTILITY`
- `components` set to an array of message components including an example with message values

### Parameter Formats

Templates support two parameter formats:

- **Named parameters** — Placeholders use descriptive names: `{{customer_name}}`, `{{order_id}}`. Set `parameter_format` to `NAMED` when creating the template. Example values are provided in the `body_text_named_params` and `header_text_named_params` fields using `param_name` and `example` pairs.
- **Positional parameters** (default) — Placeholders use sequential numbers: `{{1}}`, `{{2}}`, `{{3}}`. Example values are provided in the `body_text` and `header_text` fields. This is the default format when `parameter_format` is not specified.

Text-Only Templates (Named Parameters)

In the following example, we use named parameters with descriptive placeholder names. The `parameter_format` is set to `NAMED`, and example values are provided using `body_text_named_params` and `header_text_named_params` with `param_name` and `example` pairs.

```html
curl -H 'Content-Type: application/json' \
     -d '{
           "name": "jaspers_market_order_delivery_update_named_us",
           "language": "en",
           "category": "UTILITY",
           "parameter_format": "NAMED",
           "components": [
            {
              "type": "HEADER",
              "format": "TEXT",
              "text":"{{order_type}} Update",
              "example": {
               "header_text_named_params": [
                 {
                   "param_name": "order_type",
                   "example": "Order"
                 }
               ]
              }
             },
             {
               "type": "BODY",
               "text": "Good news! Your order #{{order_id}} is on its way. Thank you for your order, {{customer_name}}!",
               "example": {
                 "body_text_named_params": [
                   {
                     "param_name": "order_id",
                     "example": "566701"
                   },
                   {
                     "param_name": "customer_name",
                     "example": "John"
                   }
                 ]
               }
             }
           ]
         }' "https://graph.facebook.com/v25.0/102290129340398/message_templates?access_token=EAAJB..."
```

Text-Only Templates (Positional Parameters)

In the following example, we have message body text and header text. The body component and header component includes example customer information that would be used to customize the message.

```html
curl -H 'Content-Type: application/json' \
     -d '{
           "name": "jaspers_market_order_delivery_update_us",
           "language": "en",
           "category": "UTILITY",
           "components": [
            {
              "type": "HEADER",
              "format": "TEXT",
              "text":"{{1}} Update",
              "example": {
               "header_text":["Order"]
              }
             },
             {
               "type": "BODY",
               "text": "Good news! Your order #{{1}} is on its way. Thank you for your order!",
               "example": {
                 "body_text": [
                   [
                     "566701"
                   ]
                 ]
               }
             }
           ]
         }' "https://graph.facebook.com/v25.0/102290129340398/message_templates?access_token=EAAJB..."
```

Text + Image Templates

You can also create templates with images. Images need to be first uploaded using the [Resumable Upload API](https://developers.facebook.com/docs/graph-api/guides/upload) to generate the handle for the image. You can then use the handle and pass it in the Header component while creating the template.

```html
curl -H 'Content-Type: application/json' \
     -d '{
           "name": "jaspers_market_order_delivery_update_named_us",
           "language": "en",
           "category": "UTILITY",
           "parameter_format": "NAMED",
           "components": [
             {
              "type": "HEADER",
              "format": "IMAGE",
              "text":"{{order_type}} Update",
              "example": {
               "header_handle": ["4:dGVzdF9pbWFn......."],
               "header_text_named_params": [
                 {
                   "param_name": "order_type",
                   "example": "Order"
                 }
               ]
              }
             },
             {
               "type": "BODY",
               "text": "Good news! Your order #{{order_id}} is on its way. Thank you for your order, {{customer_name}}!",
               "example": {
                 "body_text_named_params": [
                   {
                     "param_name": "order_id",
                     "example": "566701"
                   },
                   {
                     "param_name": "customer_name",
                     "example": "John"
                   }
                 ]
               }
             }
           ]
         }' "https://graph.facebook.com/v25.0/102290129340398/message_templates?access_token=EAAJB..."
```

On success your app receives a JSON response with the template ID, the review status, and the template category.

```
{
  "id": "104595129340398",
  "status": "APPROVED",
  "category": "UTILITY"
}
```

### Step 2. Send a message

To send a utility message using a template from your app user’s template library, send a `POST` request to the `/<PAGE_ID>/messages` endpoint with the following required parameters:

- `recipient.id` set to the Page-scoped ID for the person your app user is sending the message to
- `message.template` set to a list of parameters:
- `name` set to the name of the specific template being used to create the message
- `language` set to the language code for this template
- `components` set to an array of component objects with parameters to fill in the template placeholders

Sending with Positional Parameters

For templates created with positional parameters (the default), parameters are matched by position. In the following example, `{{1}}` in the header will be replaced with the first header parameter, and `{{1}}` in the body will be replaced with the first body parameter.

```html
curl -X POST -H "Content-Type: application/json" -d '{
  "recipient": {
    "id": "2348927398743287"
  },
  "message": {
    "template": {
      "name": "jaspers_market_order_delivery_update_us",
      "language": {
        "code": "en"
      },
      "components": [
        {
          "type": "header",
          "parameters": [
            {
              "type": "text",
              "text": "Order"
            }
          ]
        },
        {
          "type": "body",
          "parameters": [
            {
              "type": "text",
              "text": "566701"
            }
          ]
        }
      ]
    }
  }
}' "https://graph.facebook.com/v25.0/1909458034523498/messages?access_token=EAACE..."
```

Sending with Named Parameters

For templates created with `parameter_format` set to `NAMED`, include the `parameter_name` field in each parameter to match it to the corresponding placeholder in the template. In the following example, `{{order_type}}` in the header and `{{order_id}}` and `{{customer_name}}` in the body will be replaced with their respective values.

```html
curl -X POST -H "Content-Type: application/json" -d '{
  "recipient": {
    "id": "2348927398743287"
  },
  "message": {
    "template": {
      "name": "jaspers_market_order_delivery_update_named_us",
      "language": {
        "code": "en"
      },
      "components": [
        {
          "type": "header",
          "parameters": [
            {
              "type": "text",
              "parameter_name": "order_type",
              "text": "Order"
            }
          ]
        },
        {
          "type": "body",
          "parameters": [
            {
              "type": "text",
              "parameter_name": "order_id",
              "text": "566701"
            },
            {
              "type": "text",
              "parameter_name": "customer_name",
              "text": "John"
            }
          ]
        }
      ]
    }
  }
}' "https://graph.facebook.com/v25.0/1909458034523498/messages?access_token=EAACE..."
```

On success your app will receive a JSON response with the recipient ID and message ID.

```json
{
  "recipient_id": "25381719828140932",
  "message_id": "m_zm2fACsz21560tai1om-TvABABVG5smou58Xoe7OB4ekibklqP8d2WdzC-Z8j2LVG1G43QVrtVr-jwVZFg72kg"
}
```

## Use an existing Page’s template

### Step 1. Search for a template

To get a list of a Page’s utility message templates, send a `GET` request to the `/<PAGE_ID>/message_templates` endpoint.

Add additional parameters to find specific utility message types. In the following example we are searching for templates that include the word “`delivery_confirmation`” in the template name.

```html
curl -X GET "https://graph.facebook.com/v25.0/102290129340398/message_templates?name=delivery_confirmation&access_token=EAAJB..."
```

On success your app receives a JSON response with a list of templates that match your query. You will need the template `name` value to use the template for your app user’s utility messages.

```html
{
  "data": [
    {
      "name": "delivery_confirmation_1",
      "language": "en",
      "category": "UTILITY",
      "topic": "ORDER_MANAGEMENT",
      "usecase": "DELIVERY_CONFIRMATION",
      "industry": [
        "E_COMMERCE"
      ],
      "body": "{{1}}, your order was successfully delivered!",
      "body_params": [
        "Mark"
      ],
      "body_param_types": [
        "TEXT"
      ],
      "id": "7635027653257090"
    },
    {
      "name": "delivery_confirmation_2",
    ...
    },
  ]
}
```

### Step 2. Send a message

To send a utility message using a template from your app user’s template library, send a `POST` request to the `/<PAGE_ID>/messages` endpoint with the following required parameters:

- `recipient.id` set to the Page-scoped ID for the person your app user is sending the message to
- `message.template` set to a list of parameters:
- `name` set to the name of the specific template being used to create the message
- `language` set to the language code for this template
- `components` set to an array of component objects with parameters to fill in the template placeholders

Sending with Positional Parameters

For templates created with positional parameters (the default), parameters are matched by position. In the following example, `{{1}}` in the header will be replaced with the first header parameter, and `{{1}}` in the body will be replaced with the first body parameter.

```html
curl -X POST -H "Content-Type: application/json" -d '{
  "recipient": {
    "id": "2348927398743287"
  },
  "message": {
    "template": {
      "name": "jaspers_market_order_delivery_update_us",
      "language": {
        "code": "en"
      },
      "components": [
        {
          "type": "header",
          "parameters": [
            {
              "type": "text",
              "text": "Order"
            }
          ]
        },
        {
          "type": "body",
          "parameters": [
            {
              "type": "text",
              "text": "566701"
            }
          ]
        }
      ]
    }
  }
}' "https://graph.facebook.com/v25.0/1909458034523498/messages?access_token=EAACE..."
```

Sending with Named Parameters

For templates created with `parameter_format` set to `NAMED`, include the `parameter_name` field in each parameter to match it to the corresponding placeholder in the template. In the following example, `{{order_type}}` in the header and `{{order_id}}` and `{{customer_name}}` in the body will be replaced with their respective values.

```html
curl -X POST -H "Content-Type: application/json" -d '{
  "recipient": {
    "id": "2348927398743287"
  },
  "message": {
    "template": {
      "name": "jaspers_market_order_delivery_update_named_us",
      "language": {
        "code": "en"
      },
      "components": [
        {
          "type": "header",
          "parameters": [
            {
              "type": "text",
              "parameter_name": "order_type",
              "text": "Order"
            }
          ]
        },
        {
          "type": "body",
          "parameters": [
            {
              "type": "text",
              "parameter_name": "order_id",
              "text": "566701"
            },
            {
              "type": "text",
              "parameter_name": "customer_name",
              "text": "John"
            }
          ]
        }
      ]
    }
  }
}' "https://graph.facebook.com/v25.0/1909458034523498/messages?access_token=EAACE..."
```

On success your app will receive a JSON response with the recipient ID and message ID.

```json
{
  "recipient_id": "25381719828140932",
  "message_id": "m_zm2fACsz21560tai1om-TvABABVG5smou58Xoe7OB4ekibklqP8d2WdzC-Z8j2LVG1G43QVrtVr-jwVZFg72kg"
}
```

## Use a Template with Customizable Postback Button

### Step 1. Create a template with a postback button

To create a utility message template, send a `POST` request to the `/<PAGE_ID>/message_templates` endpoint with the following required parameters:

- `name` set to the name of the template
- `language` set to the language of the message text
- `category` set to `UTILITY`
- `components` set to an array of message components including an example with message values

In the following example, we have a customizable message body text and a `POSTBACK` button with a customizable payload.

Using Positional Parameters

```html
curl -X POST -H "Content-Type: application/json" -d '{
  "name": "jaspers_market_order_confirmation_update_us",
  "language": "en",
  "category": "UTILITY",
  "components": [
    {
      "type": "BODY",
      "text": "Your order is now {{1}}",
      "example": {
        "body_text": [
          [
            "Your order is now confirmed"
          ]
        ]
      }
    },
    {
      "type": "BUTTONS",
      "buttons": [
        {
          "type": "POSTBACK",
          "text": "Track Order",
          "payload": "order_id_{{2}}"
        }
      ]
    }
  ]
}' "https://graph.facebook.com/v21.0/1909458034523498/messages?access_token=EAACE..."
```

Using Named Parameters

You can also use named parameters for the body text by setting `parameter_format` to `NAMED`. Note that button payloads continue to use positional parameters.

```html
curl -X POST -H "Content-Type: application/json" -d '{
  "name": "jaspers_market_order_confirmation_update_named_us",
  "language": "en",
  "category": "UTILITY",
  "parameter_format": "NAMED",
  "components": [
    {
      "type": "BODY",
      "text": "Your order is now {{order_status}}",
      "example": {
        "body_text_named_params": [
          {
            "param_name": "order_status",
            "example": "confirmed"
          }
        ]
      }
    },
    {
      "type": "BUTTONS",
      "buttons": [
        {
          "type": "POSTBACK",
          "text": "Track Order",
          "payload": "order_id_{{number}}"
        }
      ]
    }
  ]
}' "https://graph.facebook.com/v21.0/1909458034523498/messages?access_token=EAACE..."
```

On success your app receives a JSON response with the template ID, the review status, and the template category.

```
{
  "id": "104595129340398",
  "status": "APPROVED",
  "category": "UTILITY"
}
```

### Step 2. Send a message

To send a utility message using a template from your app user’s template library, send a `POST` request to the `/<PAGE_ID>/messages` endpoint with the following required parameters:

- `recipient.id` set to the Page-scoped ID for the person your app user is sending the message to
- `message.template` set to a list of parameters: `name` set to the name of the specific template being used to create the message`language` set to the language code for this template`components` set to the name of the app user’s template library

Add additional parameters to customize the message. In the following example, `{{1}}` and `{{2}}` will be replaced with the recipient’s order ID, updating both the body text and the `POSTBACK` button’s payload.

**Note:** The example uses positional parameters. If your template was created with `parameter_format` set to `NAMED`, you must include the `parameter_name` field in each body parameter. The button payload remains the same for both positional and named parameter formats. See [Send a message](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/utility-messages#step-2--send-a-message) for details.

```html
curl -X POST -H "Content-Type: application/json" -d '{
  "recipient": {
    "id": "25381719828140932"
  },
  "messaging_type": "UTILITY",
  "message": {
    "template": {
      "name": "jaspers_market_order_confirmation_update_us",
      "language": {
        "code": "en"
      },
      "components": [
        {
          "type": "body",
          "parameters": [
            {
              "type": "text",
              "text": "confirmed"
            }
          ]
        },
        {
          "type": "buttons",
          "parameters": [
            {
              "type": "POSTBACK",
              "payload": "12345"
            }
          ]
        }
      ]
    }
  }
}' "https://graph.facebook.com/v21.0/1909458034523498/messages?access_token=EAACE..."
```

On success your app will receive a JSON response with the template ID, review status, and template category.

```json
{
  "recipient_id": "25381719828140932",
  "message_id": "m_zm2fACsz21560tai1om-TvABABVG5smou58Xoe7OB4ekibklqP8d2WdzC-Z8j2LVG1G43QVrtVr-jwVZFg72kg"
}
```

## Use a Template with Customizable URL Button

### Step 1. Create a template with a URL button

To create a utility message template, send a `POST` request to the `/<PAGE_ID>/message_templates` endpoint with the following required parameters:

- `name` set to the name of the template
- `language` set to the language of the message text
- `category` set to `UTILITY`
- `components` set to an array of message components including an example with message values

In the following example, we have a customizable message body text and a `URL` button with a customizable URL.

Using Positional Parameters

```html
curl -X POST -H "Content-Type: application/json" -d '{
  "name": "jaspers_market_order_confirmation_update_us",
  "language": "en",
  "category": "UTILITY",
  "components": [
    {
      "type": "BODY",
      "text": "Your order is now {{1}}",
      "example": {
        "body_text": [
          [
            "Your order is now confirmed"
          ]
        ]
      }
    },
    {
      "type": "BUTTONS",
      "buttons": [
        {
          "type": "URL",
          "text": "Track Order",
          "url": "http://www.example.com/orders/{{1}}",
          "example": {
            "url_suffix_example": "https://www.example.com/orders/1234"
          }
        }
      ]
    }
  ]
}' "https://graph.facebook.com/v21.0/1909458034523498/messages?access_token=EAACE..."
```

Using Named Parameters

You can also use named parameters for the body text by setting `parameter_format` to `NAMED`. Note that URL button suffixes continue to use positional parameters.

```html
curl -X POST -H "Content-Type: application/json" -d '{
  "name": "jaspers_market_order_confirmation_update_named_us",
  "language": "en",
  "category": "UTILITY",
  "parameter_format": "NAMED",
  "components": [
    {
      "type": "BODY",
      "text": "Your order is now {{order_status}}",
      "example": {
        "body_text_named_params": [
          {
            "param_name": "order_status",
            "example": "confirmed"
          }
        ]
      }
    },
    {
      "type": "BUTTONS",
      "buttons": [
        {
          "type": "URL",
          "text": "Track Order",
          "url": "http://www.example.com/orders/{{url_suffix}}",
          "example": {
            "url_suffix_example": "https://www.example.com/orders/1234"
          }
        }
      ]
    }
  ]
}' "https://graph.facebook.com/v21.0/1909458034523498/messages?access_token=EAACE..."
```

On success your app receives a JSON response with the template ID, the review status, and the template category.

```
{
  "id": "104595129340398",
  "status": "APPROVED",
  "category": "UTILITY"
}
```

### Step 2. Send a message

To send a utility message using a template from your app user’s template library, send a `POST` request to the `/<PAGE_ID>/messages` endpoint with the following required parameters:

- `recipient.id` set to the Page-scoped ID for the person your app user is sending the message to
- `message.template` set to a list of parameters: `name` set to the name of the specific template being used to create the message`language` set to the language code for this template`components` set to the name of the app user’s template library

Add additional parameters to customize the message. In the following example, `{{1}}` in the body text will be replaced with with the word `confirmed` and the `{{1}}` in the URL of the button will be replaced with the order ID.

**Note:** The example uses positional parameters. If your template was created with `parameter_format` set to `NAMED`, you must include the `parameter_name` field in each body parameter. The button URL suffix remains the same for both positional and named parameter formats. See [Send a message](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/utility-messages#step-2--send-a-message) for details.

```html
curl -X POST -H "Content-Type: application/json" -d '{
  "recipient": {
    "id": "25381719828140932"
  },
  "messaging_type": "UTILITY",
  "message": {
    "template": {
      "name": "jaspers_market_order_confirmation_update_us",
      "language": {
        "code": "en"
      },
      "components": [
        {
          "type": "body",
          "parameters": [
            {
              "type": "text",
              "text": "confirmed"
            }
          ]
        },
        {
          "type": "buttons",
          "parameters": [
            {
              "type": "URL",
              "url": "1234"
            }
          ]
        }
      ]
    }
  }
}' "https://graph.facebook.com/v21.0/1909458034523498/messages?access_token=EAACE..."
```

On success your app will receive a JSON response with the template ID, review status, and template category.

```json
{
  "recipient_id": "25381719828140932",
  "message_id": "m_zm2fACsz21560tai1om-TvABABVG5smou58Xoe7OB4ekibklqP8d2WdzC-Z8j2LVG1G43QVrtVr-jwVZFg72kg"
}
```

## Utility Messages in Conversation API

Utility Messages that use only a `BODY` component will be represented in the Conversation API the same as [basic text](https://developers.facebook.com/documentation/business-messaging/messenger-platform/introduction/conversation-components#text_messages) messages whereas messages that use a `HEADER` and `BUTTONS` components will be represented the same as
[generic template messages](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/templates#generic).

### Example: Utility Message with Only a Body in Conversation API

```html
curl -X GET "https://graph.facebook.com/v21.0/me/messages?access_token=EAACE..."
```

```json
{
  "data": [
    {
      "messages": {
        "data": [
          {
            "message": "Good news! Your order #123123123 is confirmed!",
            "id": "m_-9paUc9QYpm9VbVRgslJlNAcspcsz2P9LWJH6flWihChxY9ujvS623AfYOMWiHeq_fgsSh4GXjGwTPWN9Slm2Q"
          },
  ...
}
```

### Example: Utility Message With Header or Buttons in Conversation API

```html
curl -X GET "https://graph.facebook.com/v21.0/me/messages?access_token=EAACE..."
```

```json
{
  "data": [
    {
      "messages": {
        "data": [
          {
            "attachments": {
              "data": [
                {
                  "generic_template": {
                    "title": "Order is being shipped",
                    "subtitle": "Good news! Your order #123123123 is now shipped. The tracking number is #track123"
                  }
                }
              ]
            },
            "message": "",
            "id": "m_qvfnMpHYUNzLf__jekbCjdAcspcsz2P9LWJH6flWihCIJ-wkOtKKkRzUDwl0nKO-is6mGR_WeP0caoCVKTWfLw"
          },
  ...
}
```

## Common Template Rejection Reasons

Submissions are commonly rejected for the following reasons, so make sure you avoid these mistakes.

### Parameter Formatting

- Variable parameters are missing or have mismatched curly braces. The correct format is {{1}}.
- Variable parameters contain special characters such as a #, $, or %.
- Variable parameters are not sequential. For example, {{1}}, {{2}}, {{4}}, {{5}} are defined but {{3}} does not exist.
- Template contains too many variable parameters relative to the message length. You need to decrease the number of variable parameters or increase the message length.
- The message template cannot start or end with a parameter. In essence, dangling parameters are not allowed. In this case, the template will not be able to be created.

The below table shows various rejection reason codes and their details.

| Rejection Reason Code | Description |
| --- | --- |
| `INCORRECT_PARAMS` | Your template has incorrect parameter formatting. Parameters must use double curly braces (e.g., `{{1}}` for positional parameters). Common issues include:<br>Using single braces (e.g., `{1}`)Mixing positional and named parameter formatsInvalid positional parameters (e.g., `{{1a}}`, `{{name}}` when using positional format) |
| `PARAMS_TO_WORD_RATIO_EXCEED_LIMIT` | The template contains too many variable parameters relative to the message length |
| `TAG_SHOULD_BE_MARKETING` | Template doesn’t qualify for Utility Messages due to presence of marketing related content |

### Content and Policy Violations

- The message template contains content that violates Utility Messages policy: When you offer goods or services for sale, we consider all messages and media related to your goods or services, including any descriptions, prices, fees, taxes and/or any required legal disclosures, to constitute transactions.
- Do not request sensitive identifiers from users. For example, do not ask people to share full length individual payment card numbers, financial account numbers, National Identification numbers, or other sensitive identifiers. This also includes not requesting documents from users that might contain sensitive identifiers. Requesting partial identifiers (ex: last 4 digits of their Social Security number) is OK.
- The content contains potentially abusive or threatening content, such as threatening a customer with legal action or threatening to publicly shame them.

## See Also

To learn more about the concepts and endpoints mentioned in this document, please visit the following guides:

- [Message Template Library API Reference](https://developers.facebook.com/docs/messenger-platform/reference/templates/message-template-library)
