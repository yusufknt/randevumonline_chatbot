# Interactive media carousel messages | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/interactive-media-carousel-messages_

---

# Interactive media carousel messages

Updated: Dec 22, 2025

Interactive media carousel messages display a set of horizontally scrollable media cards. Each card can display an image or video header, body text, and either quick-reply buttons or a URL button.

For example, this is an interactive media card carousel message showing three cards in a scrollable area (highlighted by a dotted rectangle), each with an image header, body text, and URL button:

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/600343323_2167777830292496_5403577751834566910_n.png?_nc_cat=110&ccb=1-7&_nc_sid=e280be&_nc_ohc=HjPg5Ew38bMQ7kNvwHrhRdp&_nc_oc=AdqsIVCMjtDLPlKnvQ6C3rowo4hxfVMZT0aUuErI1D22_TY8-JGCq9SW4VwD_rh10ew&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=ZTgKdfbQjVawkbj6d0y3BA&_nc_ss=7b20f&oh=00_Af5Rv3II9bzj80OcsU6kiFb9YIiVu0KcHWsKPF0onrPs3g&oe=6A1C2979)

This is the same message, but using quick-reply buttons instead of URL buttons:

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/600325826_4096765807302684_4781899173713977844_n.png?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=FLktFuTteWYQ7kNvwGSDFtD&_nc_oc=AdrHwqd8S9H9QF-oLQ1z0smDNfnYEVeC1E4X9546PCH31R0R6Uz0264ZRXqDhsrH4Rc&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=ZTgKdfbQjVawkbj6d0y3BA&_nc_ss=7b20f&oh=00_Af5kEYDlDGPSQ5KsFSqVu2D1Sl-MsRVIUjt7h35vLJKi8Q&oe=6A1C22E0)

## Components

- Messages must include between 2 and 10 cards.
- Main message body text is required.
- Main message headers, footers, and interactive components are not supported.
- Cards must include either an image or video header. Other header types are not supported.
- Card body text is optional.
- Cards must include either one URL button, or one or more quick-reply buttons. Button types and numbers must match across all cards (for example, if you define a card with 2 quick-reply buttons, all cards must define exactly 2 quick-reply buttons).

## Request syntax

```html
curl 'https://graph.facebook.com/<API_VERSION>/<BUSINESS_PHONE_NUMBER_ID>/messages' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <ACCESS_TOKEN>' \
-d '
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "<USER_PHONE_NUMBER>",
  "type": "interactive",
  "interactive": {
    "type": "carousel",
    "body": {
      "text": "<MESSAGE_BODY_TEXT>"
    },
    "action": {

      <!-- First card object -->
      "cards": [
        {
          "card_index": <CARD_INDEX>,
          "type": "cta_url",
          "header": {
            "type": "<HEADER_TYPE>",
            "<HEADER_TYPE>": {
              "link": "<MEDIA_ASSET_URL>"
            }
          },

          <!-- Card body text is optional -->
          "body": {
            "text": "<CARD_BODY_TEXT>"
          },

          "action": {
            <!-- Only if using a URL button -->
            "name": "cta_url",
            "parameters": {
              "display_text": "<URL_BUTTON_LABEL>",
              "url": "<URL_BUTTON_URL>"
            }
            <!-- Only if using one or more quick-reply buttons -->
            "buttons": [
              {
                "type": "quick_reply",
                "quick_reply": {
                  "id": "<QUICK_REPLY_BUTTON_ID>",
                  "title": "<QUICK_REPLY_BUTTON_LABEL>"
                }
              },
              <!-- Additional quick-reply buttons would follow -->
          }
        },
        <!-- Additional card objects would follow -->
      ]
    }
  }
}'
```

## Request parameters

| Placeholder | Description | Example value |
| --- | --- | --- |
| `<ACCESS_TOKEN>`<br>*String* | **Required.**<br>Access token. | `EAAJB...` |
| `<API_VERSION>`<br>*String* | **Optional.**<br>API version. | `v23.0` |
| `<BUSINESS_PHONE_NUMBER_ID>`<br>*Integer* | **Required.**<br>Business phone number ID. | `106540352242922` |
| `<CARD_BODY_TEXT>`<br>*String* | **Optional.**<br>Card body text. Max 160 characters, and up to 2 line breaks. | `*Blue Echeveria*\n\nA rosette-shaped succulent with powdery blue leaves, perfect for brightening up any space.` |
| `<CARD_INDEX>`<br>*Integer* | **Required.**<br>Zero-index card index. Cards will appear left to right in scrollable view, starting from 0. | `0` |
| `<HEADER_TYPE>`<br>*String* | **Required.**<br>Header type. Value can be:<br>`image`<br>— Indicates a card image header.<br>`video`<br>— Indicates a card video header.<br>See<br>[Supported media types](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/media)<br>. | `image` |
| `<MEDIA_ASSET_URL>`<br>*String* | **Required.**<br>Publicly available media asset URL. | `https://www.luckyshrub.com/assets/blue-echeveria.jpeg` |
| `<MESSAGE_BODY_TEXT>`<br>*String* | **Required.**<br>Main message body text. Maximum 1024 characters. | `Of course! Here are three of our latest arrivals, each under $25:` |
| `<QUICK_REPLY_BUTTON_ID>`<br>*String* | **Required if using a quick-reply button.**<br>Quick-reply button ID. Maximum 256 characters. | `learn-blue-echeveria` |
| `<QUICK_REPLY_BUTTON_LABEL>`<br>*String* | **Required if using a quick-reply button.**<br>Quick-reply button label text. Maximum 20 characters. | `Learn more` |
| `<URL_BUTTON_LABEL>`<br>*String* | **Required if using a URL button.**<br>URL button label text. Maximum 20 characters. | `Buy now` |
| `<URL_BUTTON_URL>`<br>*String* | **Required if using a URL button.**<br>URL to load in the device’s default web browser when tapped by the user. | `https://shop.luckyshrub.com/latest/blue-echeveria` |
| `<USER_PHONE_NUMBER>`<br>*String* | **Required.**<br>WhatsApp user phone number. | `16505551234` |

## Example requests

### URL buttons example

This example request sends a media carousel message composed of 3 cards, each with an image header, card body text, and a URL button.

```curl
curl 'https://graph.facebook.com/v23.0/106540352242922/messages' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "16505551234",
  "type": "interactive",
  "interactive": {
    "type": "carousel",
    "body": {
      "text": "Of course! Here are three of our latest arrivals, each under $25:"
    },
    "action": {
      "cards": [
        {
          "card_index": 0,
          "type": "cta_url",
          "header": {
            "type": "image",
            "image": {
              "link": "https://www.luckyshrub.com/assets/blue-echeveria.jpeg"
            }
          },
          "body": {
            "text": "*Blue Echeveria*\n\nA rosette-shaped succulent with powdery blue leaves, perfect for brightening up any space."
          },
          "action": {
            "name": "cta_url",
            "parameters": {
              "display_text": "Buy now",
              "url": "https://shop.luckyshrub.com/latest/blue-echeveria"
            }
          }
        },
        {
          "card_index": 1,
          "type": "cta_url",
          "header": {
            "type": "image",
            "image": {
              "link": "https://www.luckyshrub.com/assets/zebra-haworthia.jpeg"
            }
          },
          "body": {
            "text": "*Zebra Haworthia*\n\nStriking white stripes on deep green leaves give this compact succulent a bold, modern look."
          },
          "action": {
            "name": "cta_url",
            "parameters": {
              "display_text": "Buy now",
              "url": "https://shop.luckyshrub.com/latest/zebra-haworthia"
            }
          }
        },
        {
          "card_index": 2,
          "type": "cta_url",
          "header": {
            "type": "image",
            "image": {
              "link": "https://www.luckyshrub.com/assets/panda-plant.jpeg"
            }
          },
          "body": {
            "text": "*Panda Plant*\n\nSoft, fuzzy leaves with chocolate-brown edges—adorable and easy to care for."
          },
          "action": {
            "name": "cta_url",
            "parameters": {
              "display_text": "Buy now",
              "url": "https://shop.luckyshrub.com/latest/panda-plant"
            }
          }
        }
      ]
    }
  }
}'
```

### Quick-reply buttons example

This example request sends a media carousel message composed of 3 cards, each with an image header, card body text, and two quick-reply buttons.

```curl
curl 'https://graph.facebook.com/v23.0/106540352242922/messages' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "16505551234",
  "type": "interactive",
  "interactive": {
    "type": "carousel",
    "body": {
      "text": "Of course! Here are three of our latest arrivals, each under $25:"
    },
    "action": {
      "cards": [
        {
          "card_index": 0,
          "type": "cta_url",
          "header": {
            "type": "image",
            "image": {
              "link": "https://www.luckyshrub.com/assets/blue-echeveria.jpeg"
            }
          },
          "body": {
            "text": "*Blue Echeveria*\n\nA rosette-shaped succulent with powdery blue leaves, perfect for brightening up any space."
          },
          "action": {
            "buttons": [
              {
                "type": "quick_reply",
                "quick_reply": {
                  "id": "learn-blue-echeveria",
                  "title": "Learn more"
                }
              },
              {
                "type": "quick_reply",
                "quick_reply": {
                  "id": "fav-blue-echeveria",
                  "title": "Add to favorites"
                }
              }
            ]
          }
        },
        {
          "card_index": 1,
          "type": "cta_url",
          "header": {
            "type": "image",
            "image": {
              "link": "https://www.luckyshrub.com/assets/zebra-haworthia.jpeg"
            }
          },
          "body": {
            "text": "*Zebra Haworthia*\n\nStriking white stripes on deep green leaves give this compact succulent a bold, modern look."
          },
          "action": {
            "buttons": [
              {
                "type": "quick_reply",
                "quick_reply": {
                  "id": "learn-zebra-haworthia",
                  "title": "Learn more"
                }
              },
              {
                "type": "quick_reply",
                "quick_reply": {
                  "id": "fav-zebra-haworthia",
                  "title": "Add to favorites"
                }
              }
            ]
          }
        },
        {
          "card_index": 2,
          "type": "cta_url",
          "header": {
            "type": "image",
            "image": {
              "link": "https://www.luckyshrub.com/assets/panda-plant.jpeg"
            }
          },
          "body": {
            "text": "*Panda Plant*\n\nSoft, fuzzy leaves with chocolate-brown edges—adorable and easy to care for."
          },
          "action": {
            "buttons": [
              {
                "type": "quick_reply",
                "quick_reply": {
                  "id": "learn-panda-plant",
                  "title": "Learn more"
                }
              },
              {
                "type": "quick_reply",
                "quick_reply": {
                  "id": "fav-panda-plant",
                  "title": "Add to favorites"
                }
              }
            ]
          }
        }
      ]
    }
  }
}'
```

## Example response

```json
{
  "messaging_product": "whatsapp",
  "contacts": [
    {
      "input": "+16505551234",
      "wa_id": "16505551234"
    }
  ],
  "messages": [
    {
      "id": "wamid.HBgLMTY0NjcwNDM1OTUVAgARGBI1RjQyNUE3NEYxMzAzMzQ5MkEA"
    }
  ]
}
```
