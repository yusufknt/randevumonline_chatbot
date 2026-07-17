# commands Reference | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/messenger-profile-api/commands_

---

# commands Reference

Updated: Jan 11, 2024

Commands are tappable keywords that a user can invoke at any time to perform specific actions within the Messenger experience. Users can invoke multiple commands in a single message. For example, if your travel assistant supports commands such as **flights** and **hotels**, a message from a user might be, “Help me book **flights** and **hotels** to Mexico for the last week of December.” Messenger automatically highlights the commands in the composer as the user taps them. These commands then trigger a [webhook](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/webhook-events/messages) to send the list of commands invoked by the user. Only the command name(s) will be sent to your app via webhook. Your app can then use the webhook as confirmation of the user’s intent to run a command, and parse the message text appropriately.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/643444790_1445181547340495_1812315071955543768_n.png?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=Pm11MEStnXsQ7kNvwHjueI_&_nc_oc=Adp7gDJ_L6xAFKC1fp1GaRS8ip4NsPunDvx5PJOgLDeOCGqUCQe6plKDLpQEujuQaUY&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=liVJBbSonBKyrwGlikWxEg&_nc_ss=7b20f&oh=00_Af7QM2Gw1sG3gATHtbu4TVqPHgpC6yDWfD_I2zvoea4McA&oe=6A1C19CC)

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/642846692_1445181514007165_8330696329476061990_n.png?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=rmonj8MxL5wQ7kNvwH4PFU6&_nc_oc=Adq4ZyNz0bGBzSAXzMIFuG59LYsbcHThRZ-zyqTB_DTmswH5V4XNhqsj1TOhO6q5M_M&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=liVJBbSonBKyrwGlikWxEg&_nc_ss=7b20f&oh=00_Af6g8-1XlAGYxzbsQ5PF7hXMM_ar7-zCDoT30o_IwskXbA&oe=6A1C2904)

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/641350442_1445181420673841_4742531359156181903_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=t9lS8anJJacQ7kNvwHo9mBG&_nc_oc=AdoeDqiFHbOC3oVxqETbS00ebbUumWjYh2i4dZIJ-lfBreqr46ZyRUDLmYMUlYqY9rU&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=liVJBbSonBKyrwGlikWxEg&_nc_ss=7b20f&oh=00_Af69vJX5T6vqVTQp7k_xvxRwi-JfW_Qt0eRMwCug-elK5Q&oe=6A1C3B91)

Users can invoke commands in three ways, as seen in the screenshots above:

1. From the Commands menu, which is a static menu accessed by tapping a hamburger menu icon next to the composer
2. By typing a forward slash or @ in the composer
3. From a “popover” above the composer, which is a bubble with a single command that will show up when the user types a word that is also a command supported by your Messenger experience

The Commands menu appears automatically when you set up Commands. No further action is needed on your part.

A key difference between Commands and the Persistent Menu is that tapping a Persistent Menu item sends the keyword to the thread, whereas tapping a Command sends the command to the composer, allowing the user to add additional context.

## `commands` Format

```json
"commands": [
  {
    "locale": "default",
    "commands": [
      {
        "name": "flights",
        "description": "Find real-time flights and fares"
      },
      {
        "name": "hotels",
        "description": "Find real-time hotel rooms and rates"
      },
      {
        "name": "currency",
        "description": "Find real-time currency exchange rates"
      },
      {
        "name": "weather",
        "description": "Find real-time weather reports and forecasts"
      }
    ]
  }
]
```

## Localization

You may provide default and localized commands, to be displayed based on the user’s locale. To do this, specify a separate object in the `commands` array for each locale. To specify the locale for each object, set the `locale` property to a [supported locale](https://developers.facebook.com/documentation/business-messaging/messenger-platform/messenger-profile/supported-locales):

```json
"commands": [
  {
    "locale": "default",
    "commands": [...]
  },
  {
    "locale": "zh_CN",
    "commands": [...]
  }
]
```

## Properties

| Property | Type | Description |
| --- | --- | --- |
| `locale` | String | Locale of the `commands` array. The corresponding array of commands will be displayed when the user’s locale matches the provided locale.<br><br>You must at least specify commands for the default locale, which will be displayed if no provided locale matches the user’s locale.<br><br>See the [list of supported locales](https://developers.facebook.com/documentation/business-messaging/messenger-platform/messenger-profile/supported-locales) |
| `commands` | Array<`command`> | An array of commands to display to users in the provided locale.<br><br>The array should contain a minimum of 1 and a maximum of 100 commands. |

### `command` object

| Property | Type | Description |
| --- | --- | --- |
| `name` | String | The name of the command. Keep it short and easy for users to remember. The command should not begin with a `/` (slash character).<br><br>Minimum of 1 and maximum of 32 characters. |
| `description` | String | Description of the command. Use the description to educate users about what the command does and how to use it.<br><br>Minimum of 1 and maximum of 64 characters. |

## Example API calls

### Example GET request

```curl
curl -X GET "https://graph.facebook.com/v25.0/me/messenger_profile?fields=commands&access_token=<PAGE_ACCESS_TOKEN>"
```

### Example response

```json
{
  "data": [
    {
      "commands": [
        {
          "locale": "default",
          "commands": [
            {
              "name": "flights",
              "description": "Find real-time flights and fares"
            },
            {
              "name": "hotels",
              "description": "Find real-time hotel rooms and rates"
            },
            {
              "name": "currency",
              "description": "Find real-time currency exchange rates"
            },
            {
              "name": "weather",
              "description": "Find real-time weather reports and forecasts"
            }
          ]
        }
      ]
    }
  ]
}
```

### Example POST request

The following POST request could be used to set or update commands.

```curl
curl -X POST -H "Content-Type: application/json" -d '{
    "commands": [
        {
            "locale": "default",
            "commands": [
                {
                    "name": "flights",
                    "description": "Find real-time flights and fares"
                },
                {
                    "name": "hotels",
                    "description": "Find real-time hotel rooms and rates"
                },
                {
                    "name": "currency",
                    "description": "Find real-time currency exchange rates"
                },
                {
                    "name": "weather",
                    "description": "Find real-time weather reports and forecasts"
                }
            ]
        }
    ]
}' "https://graph.facebook.com/v25.0/me/messenger_profile?access_token=<PAGE_ACCESS_TOKEN>"
```

### Example response

```json
{
    "result": "success"
}
```

## Rate Limit

Calls to the Messenger Profile API are limited to 10 API calls per 10 minutes interval. This rate limit is enforced per Page.
