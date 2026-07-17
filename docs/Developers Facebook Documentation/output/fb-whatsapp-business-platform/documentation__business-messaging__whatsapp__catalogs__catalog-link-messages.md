# Catalog link messages | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/catalogs/catalog-link-messages_

---

# Catalog link messages

Updated: Mar 3, 2026

You can send a link to your entire product catalog by assembling a wa.me link and including it in a standard [text message](https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/send-messages#text-messages). When sending a text message, you can use the optional `preview_url` set to `true` to have the message render a set of product catalog thumbnails of any URL in the message `body` string.

Note that if you [disable the catalog](https://developers.facebook.com/documentation/business-messaging/whatsapp/catalogs/set-commerce-settings#enable-disable-catalog), wa.me links and the **View Catalog** button in catalog link messages display an **Invalid catalog link** message when tapped.

To assemble a wa.me link, append your business phone number, including country code, to the end of the following string:

```http
https://wa.me/c/
```

For example:

```http
https://wa.me/c/15555455657
```
