# Conversational Components | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/conversational-components_

---

# Conversational Components

Updated: Mar 27, 2026

Conversational components are in-chat features that you can enable on business phone numbers. They make it easier for WhatsApp users to interact with your business. You can configure easy-to-use commands and provide pre-written ice breakers that users can tap.

## Limitations

If a WhatsApp user taps a [universal link](https://faq.whatsapp.com/425247423114725) (that is, **wa.me** link) configured with pre-filled text, the user interfaces for **ice breakers** are automatically dismissed.

## Configure using WhatsApp Manager (WAM)

You can configure all of these features in WhatsApp Manager on the specific numbers you choose:

1. Navigate to the [My Apps dashboard in the Meta for Developers site.](https://developers.facebook.com/apps/)
2. Select your app, then on the left panel select **Configuration** under **WhatsApp** .
3. Under **Phone Numbers** select **Manage Phone Numbers** .
4. On the far right of the phone number you want to configure, select the **Gear Icon** under **Settings** .
5. Select **Automations** .
6. Access and configure Conversational Components.

Solution Partners can configure these features for their customers as well if they have access to their customer’s WhatsApp Business account in WhatsApp Manager.

## Ice breakers

Ice breakers are customizable, tappable text strings that appear in a message thread the first time you chat with a user. For example, “Plan a trip” or “Create a workout plan”.

Ice breakers are great for service interactions, such as customer support or account servicing. For example, you can embed a WhatsApp button on your app or website. When users tap the button, they will be redirected to WhatsApp where they can choose from a set of customizable prompts, showing them how to interact with your services.

![Ice breakers displayed as tappable options in WhatsApp chat](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/565721000_1345385600653424_5234072759638667532_n.jpg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=ZE9gzEGvjQQQ7kNvwGKZjxe&_nc_oc=AdpEQWw6KoJ5DJzOsAf9hekYxjEaWOrFPeBMxuSZdbwqGQxgAMuLJpzc7rdoNcbBBSg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=Le7sqDJLbxdZFiYmuAZ7qw&_nc_ss=7b20f&oh=00_Af66LlI_rmsrUljhYMuoEsUr3leGLDLhx5yVqXl1xRWl9Q&oe=6A1C1851)

You can configure up to 4 ice breakers on a business phone number. Each ice breaker can have a maximum of 80 characters. Emojis are not supported.

When a user taps an ice breaker, it triggers a standard received message webhook. The ice breaker string is assigned to the `body` property in the payload. If the user attempts to message you instead of tapping an ice breaker, the keyboard will appear as an overlay, but it can be dismissed to see the ice breaker menu again.

If a WhatsApp user taps a [universal link](https://faq.whatsapp.com/425247423114725) (**wa.me** or **api.whatsapp.com** links) configured with pre-filled text, the user interfaces for **ice breakers** are automatically dismissed.

### Webhook payload

```json
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "<WHATSAPP_BUSINESS_ACCOUNT_ID>",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "<BUSINESS_DISPLAY_PHONE_NUMBER>",
              "phone_number_id": "<BUSINESS_PHONE_NUMBER_ID>"
            },
            "contacts": [
              {
                "profile": {
                  "name": "<WHATSAPP_USER_NAME>"
                },
                "wa_id": "<WHATSAPP_USER_ID>"
              }
            ],
            "messages": [
              {
                "from": "<WHATSAPP_USER_PHONE_NUMBER_ID>",
                "id": "<WHATSAPP_MESSAGE_ID>",
                "timestamp": "<TIMESTAMP>",
                "text": {
                  "body": "Plan a trip"
                },
                "type": "text"
              }
            ]
          },
          "field": "messages"
        }
      ]
    }
  ]
}
```

## Commands

Commands are text strings that WhatsApp users can see by typing a forward slash in a message thread with your business.

![Commands menu appearing when user types forward slash in WhatsApp](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/571105995_1345385610653423_1562585712301544837_n.jpg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=LFYMgoB16JgQ7kNvwFSz5hj&_nc_oc=AdoW1gwAOJHgkyfoyKheewj0mmyRaeYoXYAzCsVDg7ItA2lkGTDacfUBSUaHZOIPWlc&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=Le7sqDJLbxdZFiYmuAZ7qw&_nc_ss=7b20f&oh=00_Af6SthbWAjUvIL6Nu7N5-_lgpa-T48ulztGAzlzyhYfMWQ&oe=6A1C2A36)

Commands are composed of the command itself and a hint, which gives the user an idea of what can happen when they use the command. For example, you could define the command:

`/imagine - Create images using a text prompt`

When a WhatsApp user types, */imagine cars racing on Mars*, it would trigger a received message webhook with that exact text string assigned to the `body` property. You could then generate and return an image of cars racing on the planet Mars.

You can define up to 30 commands. Each command has a maximum of 32 characters, and each hint has a maximum of 256 characters. Emojis are not supported.

### Webhook payload

```json
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "<WHATSAPP_BUSINESS_ACCOUNT_ID>",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "<BUSINESS_DISPLAY_PHONE_NUMBER>",
              "phone_number_id": "<BUSINESS_PHONE_NUMBER_ID>"
            },
            "contacts": [
              {
                "profile": {
                  "name": "<WHATSAPP_USER_NAME>"
                },
                "wa_id": "<WHATSAPP_USER_ID>"
              }
            ],
            "messages": [
              {
                "from": "<WHATSAPP_USER_PHONE_NUMBER_ID>",
                "id": "<WHATSAPP_MESSAGE_ID>",
                "timestamp": "<TIMESTAMP>",
                "text": {
                  "body": "/imagine cars racing on Mars"
                },
                "type": "text"
              }
            ]
          },
          "field": "messages"
        }
      ]
    }
  ]
}
```

## Configure using the API

Using the API, you can also configure conversational components and view any configured values.

Use the [Conversational Automation API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/conversational-automation-api) to configure conversational components and view configured values on a given phone number.

### Configure conversational components via the API

You can configure conversational components on a given phone number by calling the POST endpoint.

Request syntax

```https
// Configure Commands with names and descriptions
POST /<PHONE_NUMBER_ID>/conversational_automation?commands=<COMMAND_LIST>

// Configure Prompts
POST /<PHONE_NUMBER_ID>/conversational_automation?prompts=<PROMPT>
```

Body properties

| Placeholder | Description | Sample Value |
| --- | --- | --- |
| `<PHONE_NUMBER_ID>`<br>*String* | **Required.**<br>A phone number ID on a WhatsApp Business Account. | `+12784358810` |
| `<COMMAND_LIST>`<br>*JSON* | **Optional.**<br>A list of commands to be configured. | `[<br> {<br> "command_name": "generate",<br> "command_description": "Create a new image"<br> },<br> {<br> "command_name": "rethink",<br> "command_description": "Generate new images from existing images"<br> }<br>]` |
| `<PROMPTS>`<br>*List of String* | **Optional.**<br>The prompt(s) to be configured. | `"prompts": ["Book a flight","plan a vacation"]` |

Sample request

```curl
   curl -X POST \
 'https://graph.facebook.com/v22.0/PHONE_NUMBER_ID/conversational_automation' \
 -H 'Authorization: Bearer ACCESS_TOKEN' \
 -H 'Content-Type: application/json' \
 -d '{
   "commands": [
     {
       "command_name": "tickets",
       "command_description": "Book flight tickets"
     },
     {
       "command_name": "hotel",
       "command_description": "Book hotel"
     }
   ],
   "prompts": ["Book a flight", "plan a vacation"]
}'
```

Sample response

```json
{
  "success": true
}
```

### View the current configuration using the API

You can view the current configuration of Conversational Components on a given phone number by calling the GET endpoint.

Request syntax

```https
GET  /<PHONE_NUMBER_ID>?fields=conversational_automation
```

Sample response

```json
{
  "conversational_automation": {
    "prompts": [
      "Find the best hotels in the area",
      "Find deals on rental cars"
    ],
    "commands": [
      {
        "command_name": "tickets",
        "command_description": "Book flight tickets"
      },
      {
        "command_name": "hotel",
        "command_description": "Book hotel"
      }
    ]
  },
  "id": "123456"
}
```

## Testing

To test conversational components once they have been configured, open the WhatsApp client and open a chat with your business phone number.

For ice breakers, if you already have a chat thread going with the business phone number, you must first delete the chat thread:

1. Open the thread in the WhatsApp client.
2. Tap the business phone number’s profile.
3. Tap **Clear Chat** > **Clear All Messages** .
4. **Delete Chat** .
5. Start a new chat thread with this business.

You can then send a message to the business phone number to test your ice breakers.
