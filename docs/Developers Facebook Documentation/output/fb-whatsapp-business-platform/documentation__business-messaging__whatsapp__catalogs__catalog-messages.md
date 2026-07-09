# Catalog messages | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/catalogs/catalog-messages_

---

# Catalog messages

Updated: Mar 3, 2026

Catalog messages let you showcase your product catalog entirely within WhatsApp.

Catalog messages display a product thumbnail header image of your choice, custom body text, a fixed text header, a fixed text sub-header, and a **View catalog** button.

![Catalog message example showing View catalog button](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/353831413_931793014769642_1489938023342123500_n.png?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=bg7JkrdZgWkQ7kNvwFtSqJP&_nc_oc=Adqi2o9Ag5s7BHe3lvroGLHg8arXVxiggTFtPfpZxo0LBA96AB0ktzOt8IfdtLGNGqo&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=duF-aHx-gSoVYTIz3eBSHg&_nc_ss=7b20f&oh=00_Af63AcvvmdvTtntYKagxxyuwq2lYtIZiywN1fLE2ScAqig&oe=6A1C24D5)

When a customer taps the **View catalog** button, your product catalog appears within WhatsApp.

![Product catalog displayed within WhatsApp](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/353808079_9331603410246288_3629219693038191737_n.png?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=Tjzfo9GLP9wQ7kNvwEnnrmm&_nc_oc=AdoVfEhnDqlVglEUtaWEpE3kAJaHyZsSMGoufXHVv9VYMv-KXFdCVurknFg71-A90_I&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=duF-aHx-gSoVYTIz3eBSHg&_nc_ss=7b20f&oh=00_Af6qcXQoU5IstPu5AMUv5BPWfEtjHEJIbcsbQCARVsu54A&oe=6A1C19E8)

## Requirements

You must have [inventory uploaded to Meta](https://developers.facebook.com/documentation/business-messaging/whatsapp/catalogs/upload-inventory) in an ecommerce catalog [connected to your WhatsApp Business Account](https://www.facebook.com/business/help/158662536425974).

## Request syntax

Use the [Messages API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api#post-version-phone-number-id-messages) to send a catalog message.

```json
POST /<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>/messages
```

## Post body

```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "<TO>",
  "type": "interactive",
  "interactive" : {
    "type" : "catalog_message",
    "body" : {
      "text": "<BODY_TEXT>"
    },
    "action": {
      "name": "catalog_message",

      /* Parameters object is optional */
      "parameters": {
        "thumbnail_product_retailer_id": "<THUMBNAIL_PRODUCT_RETAILER_ID>"
      }
    },

    /* Footer object is optional */
    "footer": {
      "text": "<FOOTER_TEXT>"
  }
}
```

## Properties

| Placeholder | Description | Sample Value |
| --- | --- | --- |
| `<BODY_TEXT>`<br>*String* | **Required.**<br>Text to appear in the message body.<br>Maximum 1024 characters. | `Hello! Thanks for your interest. Ordering is easy. Just visit our catalog and add items to purchase.` |
| `<FOOTER_TEXT>`<br>*String* | **Optional.**<br>Text to appear in the message footer.<br>Maximum 60 characters. | `Best grocery deals on WhatsApp!` |
| `<THUMBNAIL_PRODUCT_RETAILER_ID>`<br>*String* | **Optional.**<br>Item SKU number. Labeled as **Content ID** in the Commerce Manager.<br>The thumbnail of this item will be used as the message’s header image.<br>If the `parameters` object is omitted, the product image of the first item in your catalog will be used. | `2lc20305pt` |
| `<TO>`<br>*String* | Customer phone number. | `+16505551234` |

## Example request

```curl
curl 'https://graph.facebook.com/v17.0/106540352242922/messages' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "+16505551234",
  "type": "interactive",
  "interactive": {
    "type": "catalog_message",
    "body": {
      "text": "Hello! Thanks for your interest. Ordering is easy. Just visit our catalog and add items to purchase."
    },
    "action": {
      "name": "catalog_message",
      "parameters": {
        "thumbnail_product_retailer_id": "2lc20305pt"
      }
    },
    "footer": {
      "text": "Best grocery deals on WhatsApp!"
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
      "id": "wamid.HBgLMTY1MDM4Nzk0MzkVAgARGBI0ODVEREUwQzEzQkVBRjQ1RUUA"
    }
  ]
}
```
