# Multi-product messages | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/catalogs/multi-product-messages_

---

# Multi-product messages

Updated: Mar 3, 2026

Multi-Product Messages are interactive messages that display up to 30 products from your catalog, organized into sections. Customers can browse products, view details, add items to a cart, and send an order — all within WhatsApp.

Multi-Product message example:

Menu triggered when user clicks on Start Shopping:

![Multi-Product message example](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/561539953_1339318271260157_5511864003041128459_n.jpg?_nc_cat=111&ccb=1-7&_nc_sid=e280be&_nc_ohc=yU-j0EX9mr8Q7kNvwFJrWly&_nc_oc=AdqdeoD3ltSAAR_q-qv9KjwbynxoptvglMfEI-CGot9J_zlKlIQ5AsISxiQuDy9MAr4&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=L182YIL88MdAwPKf-9Pdzw&_nc_ss=7b20f&oh=00_Af5iKoxcwhZmByVuZRPHiHCeKpw4F0aLZHXDFF-_38gI6A&oe=6A1C0C89)

![Shopping menu triggered by Start Shopping button](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/560927761_1339318294593488_1812605316660293832_n.jpg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=SwovN3opriIQ7kNvwHiITwx&_nc_oc=Ado5Kws_zNsy-Qge9ilyMqARqiNCFDIQW4HAiEdfT4dYpr8W04eWT5W91YoL1rHsH2k&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=L182YIL88MdAwPKf-9Pdzw&_nc_ss=7b20f&oh=00_Af5r5lf3ptz-Xll19PJpg2KGC90jjgyAF6O8c6reklfy_g&oe=6A1BFCD7)

## Overview

Customers that receive Multi-Product Messages can perform 3 main actions:

1. View products: Customers can see a list of products. Whenever a customer clicks on a specific item, the product’s latest info is fetched and the product displays in a Product Detail Page (PDP) format. Currently, PDPs only support product images — any videos or GIFs added to the product won’t be displayed in the PDP.
2. Add products to a cart: Whenever a user adds a product to the shopping cart, the item’s latest info is fetched. If there has been a state change on any of the items, a dialog saying “One or more items in your cart have been updated” is displayed — see [Product updates](https://developers.facebook.com/documentation/business-messaging/whatsapp/catalogs/share-products#product-updates) for more information. A cart persists in a chat thread between you and your customer until the cart is sent to you — see [Shopping cart experience](https://developers.facebook.com/documentation/business-messaging/whatsapp/catalogs/share-products#shopping-cart-experience) for details.
3. Send a shopping cart to you: After adding all needed items, customers can send their cart to you. After that, you can define the next steps, such as requesting delivery info or giving payment options.

If your customer has multiple devices linked to their account, Multi-Product Messages will be synced between devices. However, the shopping cart is local to each specific device. See [Shopping cart experience](https://developers.facebook.com/documentation/business-messaging/whatsapp/catalogs/share-products#shopping-cart-experience) for details.

Currently, Multi-Product Messages can be received on the following platforms:

- iOS: 2.21.100
- Android: 2.21.9.15
- Web: The web client supports this feature.

If the customer’s app version does not support Multi-Product Messages, they will instead receive a message explaining that they were unable to receive a message because they are using an outdated version of WhatsApp. You also receive a webhook notification indicating the message was unable to be delivered due to the customer using an outdated version of WhatsApp.

## Expected behavior

Multi-Product Messages can be:

- Forwarded by one user to another.
- Reopened by a user within the same chat thread.

Multi-Product Messages cannot be:

- Sent as notifications. They can only be sent as part of existing chat threads.

## Use cases

Multi-Product Messages are best for guiding customers to a specific subset of your inventory, such as:

- Shopping in a conversational way. For example, using search functionality to allow customers to type a shopping list and send back a Multi-Product Message in response.
- Navigating to a specific category. For example, fitness apparel.
- Personalized offers or recommendations.
- Re-ordering previously ordered items. For example, a user can re-order their regular take-out order of less than 30 items.

Multi-Product Messages can also be used as part of a human agent flow. However, you need to build the tooling to allow the human agent to generate a Multi-Product Message in thread.

### Why you should use them

Multi-Product Messages lend themselves best to user experiences that are simple and personalized, where it’s a better experience to guide the customer to a subset of items most relevant to them, rather than browsing your full inventory.

Simple and efficient

Combining the features with navigation tools like Natural Language Processing (NLP), text search or List Messages and Reply Buttons to get to what the customer is looking for fast.

Personal

Populated dynamically so can be personalized to the customer or situation. For example, you can show a Multi-Product Message of a customer’s most frequently ordered items.

Business outcomes

A high-performing channel for driving orders. During testing, businesses had an average 7% conversion of Multi-Product Messages sent to carts received.

No templates

Interactive messages do not require templates or pre-approvals. They are generated in real-time and will always reflect the latest item details, pricing and stock levels from your inventory.

## Send a multi-product message

Before sending product messages, follow the get started best suited for your needs:

- [Direct developers](https://developers.facebook.com/documentation/business-messaging/whatsapp/get-started)
- [Solution providers](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/overview)

All API calls mentioned in this guide must be authenticated with an access token. You can authenticate your API calls with the access token generated in the **App Dashboard** > **WhatsApp** > **API Setup** panel. If you are a solution provider, you must authenticate with an access token with the [whatsapp_business_messaging](https://developers.facebook.com/docs/permissions/reference/whatsapp_business_messaging) permission.

### Step 1: Assemble the interactive object

To send a Multi-Product Message, assemble an `interactive` object of type `product_list` with the following components:

| Required Components | Optional Components |
| --- | --- |
| Header Object — Header’s type must be set to text. Remember to add a text object with the desired content.Body ObjectAction Object - Must include catalog_id and sections.<br> Sections must be an array of objects describing each section using title and product_items.<br> Each section’s product_items value must be an array describing each product in the section using product_retailer_id and the product’s SKU number. | Footer Object |

See [Messages, Interactive Object](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api) for full information. By the end of the process, the interactive object should look something like this:

```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "PHONE_NUMBER",
  "type": "interactive",
  "interactive": {
    "type": "product_list",
    "header":{
      "type": "text",
      "text": "HEADER_CONTENT"
    },
    "body": {
      "text": "BODY_CONTENT"
    },
    "footer": {
      "text": "FOOTER_CONTENT"
    },
    "action": {
      "catalog_id": "CATALOG_ID",
      "sections": [
        {
          "title": "SECTION_TITLE",
          "product_items": [
            { "product_retailer_id": "PRODUCT-SKU" },
            { "product_retailer_id": "PRODUCT-SKU" }
            ...
          ]

        },
        {
          "title": "SECTION_TITLE",
          "product_items": [
            { "product_retailer_id": "PRODUCT-SKU" },
            { "product_retailer_id": "PRODUCT-SKU" }
            ...
          ]
        }
      ]
    }
  }
}
```

Missing items

If none of the items provided in the API call matches a product from your product catalog, an error message is sent and the Multi-Product Message is not sent to the user.

At least one item from the products list must match an item from your product catalog. In this case:

- Messages are sent successfully
- Items without a match are dropped
- You receive an error message asking for a catalog update

### Step 2: Add common message parameters

Once the interactive object is complete, append the other parameters that make a message: `recipient_type`, `to`, `messaging_product`, and `type`. Remember to set the `type` to `interactive`.

```curl
curl -X  POST https://graph.facebook.com/v25.0/FROM_PHONE_NUMBER/messages \
 -H 'Authorization: Bearer ACCESS_TOKEN' \
 - d '{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "PHONE_NUMBER",
  "type": "interactive",
  "interactive": {
  // INTERACTIVE OBJECT GOES HERE
}'
```

For all available parameters, see [Reference, Messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api).

### Step 3: Send the message

Use the [Messages API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api#post-version-phone-number-id-messages) to send the JSON object you have assembled in steps 1 and 2. If your message is sent successfully, you get the following response:

```json
{
  "messaging_product": "whatsapp",
  "contacts": [{
      "input": "PHONE_NUMBER",
      "wa_id": "WHATSAPP_ID"
    }],
  "messages": [{
      "id": "wamid.ID"
    }]
}
```
