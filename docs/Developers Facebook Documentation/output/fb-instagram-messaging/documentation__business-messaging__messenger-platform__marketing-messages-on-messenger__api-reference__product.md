# Product Template | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/marketing-messages-on-messenger/api-reference/product_

---

# Product Template

Updated: Oct 23, 2025

Product Templates can be utilized to send specific products to users, the message will show up as a carousel where users will swipe to see each product. Up to 10 products can be placed in a single product template Marketing Message.

`product_ids` can be obtained via [Catalog API](https://developers.facebook.com/micro_site/url/?click_from_context_menu=true&country=IL&destination=https%3A%2F%2Fdevelopers.facebook.com%2Fdocs%2Fmarketing-api%2Fcatalog%2F&event_type=click&last_nav_impression_id=1juaopFxTKpw1E27D&max_percent_page_viewed=46&max_viewport_height_px=874&max_viewport_width_px=1728&orig_http_referrer=https%3A%2F%2Fdevelopers.facebook.com%2Fdocs%2Fmessenger-platform%2Fsend-messages%2Ftemplate%2Fproduct&orig_request_uri=https%3A%2F%2Fdevelopers.facebook.com%2Fajax%2Fdocs%2Fnav%2F%3Fpath1%3Dmessenger-platform%26path2%3Dsend-messages%26path3%3Dtemplate%26path4%3Dproduct&region=emea&scrolled=true&session_id=1MbHHwcGUGjDoO5j5&site=developers) or via [Facebook Commerce Manager](https://developers.facebook.com/micro_site/url/?click_from_context_menu=true&country=IL&destination=https%3A%2F%2Fwww.facebook.com%2Fbusiness%2Fhelp%2F2371372636254534%3Fid%3D533228987210412&event_type=click&last_nav_impression_id=1juaopFxTKpw1E27D&max_percent_page_viewed=46&max_viewport_height_px=874&max_viewport_width_px=1728&orig_http_referrer=https%3A%2F%2Fdevelopers.facebook.com%2Fdocs%2Fmessenger-platform%2Fsend-messages%2Ftemplate%2Fproduct&orig_request_uri=https%3A%2F%2Fdevelopers.facebook.com%2Fajax%2Fdocs%2Fnav%2F%3Fpath1%3Dmessenger-platform%26path2%3Dsend-messages%26path3%3Dtemplate%26path4%3Dproduct&region=emea&scrolled=true&session_id=1MbHHwcGUGjDoO5j5&site=developers). Product template only supports `product_ids` owned by the same page.

```json
{
  "message_id": "<MESSAGE_ID>",
  "messenger_delivery_data": {
    "subscription_token": "<SUBSCRIPTION_TOKEN>"
  },
  "message":{
    "attachment": {
      "type": "template",
      "payload": {
        "template_type": "product",
        "elements": [
          {
            "id": "<PRODUCT_ID>"
          },
          {
            "id": "<PRODUCT_ID>"
          },
          {
            "id": "<PRODUCT_ID>"
          }
        ]
      }
    }
  }
}
```
