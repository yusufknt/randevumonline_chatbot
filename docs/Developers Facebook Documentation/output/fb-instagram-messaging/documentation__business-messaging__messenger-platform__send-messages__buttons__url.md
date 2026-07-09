# URL button | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/buttons/url_

---

# URL button

Updated: Apr 22, 2026

The URL button opens a web page in the [Messenger webview](https://developers.facebook.com/documentation/business-messaging/messenger-platform/webview). This allows you to enrich the conversation with a web-based experience, where you have the full development flexibility of the web. For example, you might display a product summary in-conversation, then use the URL button to open the full product page on your website.

## App Links

If the site contains [App Links](https://developers.facebook.com/documentation/applinks/metadata-reference), the button launches the specified native app.

[The Facebook Crawler](https://developers.facebook.com/docs/sharing/webmasters/crawler) needs to read the app link metatags for the redirect to work. If you just implemented the tags in your website, you can request a new scrape with the [Sharing Debugger Tool](https://developers.facebook.com/tools/debug/sharing/). After the crawler has scraped the site, new URL buttons sent should follow the redirect behavior.

## Supported usage

The URL button is supported for use with the following:

- Persistent menu
- Generic template
- List template
- Button template
- Media template

## Messenger Extensions SDK — required domain whitelisting

To display a webpage with the [Messenger Extensions SDK](https://developers.facebook.com/documentation/business-messaging/messenger-platform/webview/extensions) enabled in the Messenger webview you **must** allowlist the domain, including sub-domain, in the [`whitelisted_domains` property of your bot’s Messenger Profile](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/messenger-profile-api/domain-whitelisting). This ensures that only trusted domains have access to user information available via SDK functions.

For more information on allowlisting domains, see the [`whitelisted_domains` reference](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/messenger-profile-api/domain-whitelisting).

## Properties

| Property | Type | Description |
| --- | --- | --- |
| `type` | String | Type of button. Must be<br>`web_url`<br>. |
| `title` | String | Button title. 20 character limit. |
| `url` | String | The URL opened in a mobile browser when the button is tapped. Must use HTTPS protocol if<br>`messenger_extensions`<br>is<br>`true`<br>. |
| `webview_height_ratio` | String | *Optional.*<br>Height of the webview. Valid values:<br>`compact`<br>,<br>`tall`<br>,<br>`full`<br>. Defaults to<br>`full`<br>. |
| `messenger_extensions` | Boolean | *Optional.*<br>Must be<br>`true`<br>if using Messenger Extensions. |
| `fallback_url` | String | *Optional.*<br>The URL to use on clients that don’t support<br>[Messenger Extensions](https://developers.facebook.com/documentation/business-messaging/messenger-platform/webview)<br>. If not defined, the<br>`url`<br>is used as the fallback. May only be specified if<br>`messenger_extensions`<br>is<br>`true`<br>. |
| `webview_share_button` | String | *Optional.*<br>Set to<br>`hide`<br>to disable the share button in the webview (for sensitive info). This does not affect any shares initiated by the developer using Extensions. |

## Sample request

```bash
curl -X POST "https://graph.facebook.com/<LATEST_API_VERSION>/<PAGE_ID>/messages?access_token=<PAGE_ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "recipient": {
      "id": "<PSID>"
    },
    "message": {
      "attachment": {
        "type": "template",
        "payload": {
          "template_type": "button",
          "text": "Try the URL button!",
          "buttons": [
            {
              "type": "web_url",
              "url": "https://www.example.com/",
              "title": "URL Button",
              "webview_height_ratio": "full"
            }
          ]
        }
      }
    }
  }'
```

## Sample response

```js
{
  "recipient_id": "1254477777772919",
  "message_id": "AG5Hz2Uq7tuwNEhXfYYKj8mJEM_QPpz5jdCK48PnKAjSdjfipqxqMvK8ma6AC8fplwlqLP_5cgXIbu7I3rBN0P"
}
```
