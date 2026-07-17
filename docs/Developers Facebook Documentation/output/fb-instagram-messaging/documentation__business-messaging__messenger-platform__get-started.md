# Developer Platform

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/get-started_

---

# Get Started – Send a Message with Messenger Platform

Updated: May 5, 2026

Learn how your business can send a message to a customer using the Messenger Platform.

You can use this tutorial to send a message from **your app** or, if you don’t have a fully functional app or just want to explore, you can use our **Graph API Explorer**.

## Before You Start

This guide assumes you have read the [Messenger Platform Overview](https://developers.facebook.com/documentation/business-messaging/messenger-platform/overview) and implemented the needed components for sending and receiving messages and notifications.

### Requirements

To make a successful call to the Meta social graph to send a message, your app will need:

- The `pages_show_list` permission and a User access token , requested by you. This allows your app, or the Graph API Explorer, to get your Page ID .
- The `pages_messaging` permission and a Page access token , requested by a person who can perform the `MESSAGING` task on your Page, allows your app to get the conversation ID and your Page-scoped ID (PSID)

You can get access tokens 3 different ways:

- [Facebook Login](https://developers.facebook.com/documentation/facebook-login/overview) in your app
- The [App Dashboard](https://developers.facebook.com/apps) in Messenger > Settings
- The Graph API Explorer, [(shown below)](https://developers.facebook.com/documentation/business-messaging/messenger-platform/get-started#gx-tool)

### Start a Conversation

Log in to your Facebook account and send a message to your test Page to create a **PSID** for the customer (you) that is specific for the Page and a **conversation ID** representing the conversation between the customer (you) and the Page.

## Use Your App

If you have already subscribed to the messaging Webhooks, you can get the PSID, the conversation ID, and the message text from the Webhook notification, and move to [**Step 2**](https://developers.facebook.com/documentation/business-messaging/messenger-platform/get-started#step-2-send-the-customer-a-message).

### Step 1. Get the IDs

You will need the ID for your Page, the PSID for the person who sent the message (you) and the conversation ID.

Get the Page ID & Page Access Token

To obtain your Page ID, send a `GET` request to the `/<USER_ID>/accounts` endpoint, replacing `<USER_ID>` with your actual ID. You can also use `me` in place of your User ID.

The `me` endpoint is a special endpoint that represents the ID for the User, Page, or App that is requesting the access token. In the following example, you will use a User access token in the request so `me` will represent your User ID.

Sample Request

```curl
curl -i -X GET "https://graph.facebook.com/<API_VERSION>/me/accounts
    ?access_token=<USER_ACCESS_TOKEN>"
```

Example Response

On success, your app will receive a JSON object with the Page ID as well as a Page access token that you can use in subsequent requests.

```json
{
  "data": [
    {
      "access_token": "EAABkWcj...",    // PAGE-ACCESS-TOKEN
      "category": "Pet Service",
      "category_list": [
        {
          "id": "144982405562750",
          "name": "Pet Service"
        }
      ],
      "name": "Cisco Dog Page",
      "id": "4225...",                   // PAGE-ID
      "tasks": [
        "ADVERTISE",
        "ANALYZE",
        "CREATE_CONTENT",
        "MESSAGING",
        "MODERATE",
        "MANAGE"
      ]
    }
  ]
}
```

Get the PSID & Message ID

To obtain the PSID and message ID, send a `GET` request to the `/<PAGE_ID>/conversations` endpoint with the `participants` and `messages{id,message}` fields.

Sample Request

```curl
curl -i -X GET "https://graph.facebook.com/<API_VERSION>/<PAGE_ID>/conversations?fields=participants,messages{id,message}&access_token=<PAGE_ACCESS_TOKEN>"
```

Example Response

On success, your app will receive the following JSON response:

```json
{
  "data": [
    {
      "participants": {
        "data": [
          {
            "name": "CUSTOMER-NAME",
            "email": "PSID@facebook.com",
            "id": "PSID"
          },
          {
            "name": "PAGE-NAME",
            "email": "PAGE-ID@facebook.com",
            "id": "PAGE-ID"
          }
        ]
      },
      "messages": {
        "data": [
          {
            "id": "m_MeS2...",   // Message ID
            "message": "hello"
          },
          {
            "id": "m_Nl1...",    // Message ID
            "message": "CUSTOMER-NAME"
          }
        ]
      },
      "id": "t_10224..."        // Conversation ID
    }
  ]
}
```

### Step 2. Send the Customer a Message

To respond to the message a customer sent to your Page, send a `POST` request to the `/<PAGE_ID>/messages` endpoint with the `recipient` parameter set to the customer’s PSID, `messaging_type` parameter set to `RESPONSE`, and the `message` parameter set to your response. **Note** that this must be sent within 24 hours of your Page receiving the customer’s message.

Sample Request

```curl
curl -X POST "https://graph.facebook.com/<API_VERSION>/<PAGE_ID>/messages" \
    -d "recipient={'id':'<PSID>'}" \
    -d "messaging_type=RESPONSE" \
    -d "message={'text':'You did it!'}" \
    -d "access_token=<PAGE_ACCESS_TOKEN>"
```

On success, your app will receive the following JSON response:

```json
{
  "recipient_id": "1008...",    // The customer's PSID
  "message_id": "m_AG5Hz2..."}  // The message ID
```

## Use the Graph API Explorer Tool

If you have already subscribed to the messaging Webhooks, you can get the PSID, the conversation ID, and the message text from the Webhook notification, and move to [**Step 2**](https://developers.facebook.com/documentation/business-messaging/messenger-platform/get-started#step-2-send-the-customer-a-message-2).

### Step 1. Get the IDs

You will need the ID for your Page, the Page-scoped ID (PSID) for the person who sent the message (you) and the message ID.

[Open the Graph API Explorer](https://developers.facebook.com/tools/explorer/) in a new browser tab or window.

The explorer loads with a default query with the `GET` method, the lastest version of the Graph API, the `/me` node and the `id` and `name` fields in the Query String Field, and your Facebook App. If you would like to run this default query, you can click **Generate Access Token** then **Submit**. This query will create a User access token and return your name and User ID.

The `me` endpoint is a special endpoint that represents the ID for the User, Page, or App that is requesting the access token. In the following example, you will use a User access token in the request so me will represent your User ID. In Step 4, `me` will represent your Page since are using a Page access token.

To get the Page ID for your Page:

1. Replace the Query String Field string with either `me/accounts` or `/<USER_ID>/accounts` . If you ran the default query, you can click the ID in the response and it will automatically be moved to the Query String Field.
2. Go the Add a permission dropdown menu in the right side panel and select the `pages_show_list` permission then click Generate Access Token .
3. The popup window allows you to agree that the app can access the list of your Pages.
4. Click Submit to run the query.

To get the Message ID and the PSID:

1. Click the Page ID in the response to move it to the Query String Field and add `/conversations?fields=participants,messages{id,message}` to the query.
2. Go to the Add a Permission dropdown menu and select the `pages_messaging` permission then click Generate Access Token .
3. Another popup window will ask you to agree that the app can access the conversations of your Pages.
4. Click Submit to run the query.
5. Copy the Page ID and PSID for Step 3.

### Step 2. Send the Customer a Message

To respond to the message the customer sent to your Page:

1. In the Response Window, click the message ID for the message you want to reply to.
2. In the upper left, switch the method from `GET` to `POST` .
3. In the Node Field Viewer to the left of the Response Window, click the + Add parameter under the Params tab. Add the following: `recipient` set to `{id:<PSID>}``messaging_type` set to `RESPONSE``message` set to `{text:'Hello, new customer!'}`
4. Click Submit .

**Note** that when using the `RESPONSE` message type, the message must be sent within 24 hours of your Page receiving the customer’s message or an error will occur.

## Next Steps

- [Attach Media Assets to your Message](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/saving-assets)
- [Send a customer a message after the 24-hour messaging window](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/send-api)
- [Create a Message Template](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/templates)

## Learn More

- [Graph API](https://developers.facebook.com/docs/graph-api)
- [Graph API Explorer Tool](https://developers.facebook.com/docs/graph-api/guides/explorer)
- [Page Access Tokens](https://developers.facebook.com/documentation/facebook-login/guides/access-tokens)
- [Page Permissions and Tasks](https://developers.facebook.com/docs/pages/overview/permissions-features)
- [Page/Messages Reference](https://developers.facebook.com/docs/graph-api/reference/page/messages)

### Developer Support

- Use the [Meta Status tool](https://metastatus.com) to check for the status and outages of Meta business products.
- Use the [Meta Developer Support tool](https://developers.facebook.com/support) to report bugs and view reported bugs, get help with Ads or Business Manager, and more.
