# Quick Start Tutorial | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/getting-started/quick-start_

---

# Quick Start Tutorial

Updated: May 1, 2026

This tutorial guides you through everything you need to know to build your first Messenger experience. Before you begin, choose one of the options under [Starter Projects](https://developers.facebook.com/documentation/business-messaging/messenger-platform/getting-started/quick-start#starter) to get the code you need to start, then follow the steps under [Getting Started](https://developers.facebook.com/documentation/business-messaging/messenger-platform/getting-started/quick-start#getting_started) to get set up.

To run the finished code, [fork it on GitHub](https://github.com/fbsamples/messenger-platform-samples/tree/master/quick-start).

### Contents

- [Starter Project](https://developers.facebook.com/documentation/business-messaging/messenger-platform/getting-started/quick-start#starter)
- [Get Started](https://developers.facebook.com/documentation/business-messaging/messenger-platform/getting-started/quick-start#getting_started)
- [Build the Experience](https://developers.facebook.com/documentation/business-messaging/messenger-platform/getting-started/quick-start#build)

## Starter project

Before you begin this quick start, make sure you have completed one of the following to ensure you have the starter code you need. The starter code provides a basic webhook that you will use as the foundation of the Messenger experience.

### Option 1: Build it yourself

The [webhook setup guide](https://developers.facebook.com/documentation/business-messaging/messenger-platform/webhooks) walks you through building your first webhook that you can use with this quick start from start to finish.

### Option 2: Download it from GitHub

Download the webhook starter code from GitHub, and deploy it to a server of your choice.

## Get started

Before you build your first Messenger experience, start by setting up the credentials for your app.

### Set up your Facebook app

If you have not already, follow the [app setup guide](https://developers.facebook.com/documentation/business-messaging/messenger-platform/webhooks) to set up your Facebook app for use with the Messenger Platform.

Standard access

Until your app has been submitted and approved for public use on Messenger through Meta’s App Review, Page tokens only allow your Page to interact with Facebook accounts that have been granted the Administrator, Developer, or Tester role for your app.

To grant these roles to other Facebook accounts, go to the ‘Roles’ tab of your app settings.

### Generate a Page access token

All requests to Messenger Platform APIs are authenticated by including a page-level access token in the `access_token` parameter of the query string.

If you did not already do so when you [set up your Facebook app](https://developers.facebook.com/documentation/business-messaging/messenger-platform/webhooks), generate a Page access token, by doing the following:

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/21880169_1674641772566050_8350580527064940544_n.png?_nc_cat=101&ccb=1-7&_nc_sid=e280be&_nc_ohc=bNal4CVfkp0Q7kNvwH54UCO&_nc_oc=AdqcwEOZ0f1EA4ed_6UNJL9DPnUx5K5edVAqV3_N8DpsGyW06tGcRyMVWofGYyTO0fE&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=G-GnGl_PMb_qhHAbhGWbVg&_nc_ss=7b20f&oh=00_Af5KhMSIJRGRQhmsIhHN7Yr6P-lxplk0cA9tc87fXm7vuw&oe=6A1C103B)

1. In the **Token Generation** section of your app’s Messenger settings, select the Facebook Page you want to generate a token for from the **Page** dropdown. An access token will appear in the **Page Access Token** field.
2. Click the **Page Access Token** field to copy the token to your clipboard.

The generated token will NOT be saved in this UI. Each time you select a Page from the dropdown, a new token will be generated. If a new token is generated, previously created tokens will continue to function.

### Save your Page token as an environment variable

Keep sensitive information like your Page access token secure by not hard-coding it into your webhook.

To do this, add the following to your environment variables, where `<PAGE_ACCESS_TOKEN>` is the access token you generated and `<VERIFY_TOKEN>` is a random string that you set to verify your webhook:

```bash
PAGE_ACCESS_TOKEN="<PAGE_ACCESS_TOKEN>"
VERIFY_TOKEN="<VERIFY_TOKEN>"
```

### Add your Page and verify tokens to your webhook

Now add your Page access token and verify token at the top of your `app.js` file to use in your webhook logic:

```javascript
const PAGE_ACCESS_TOKEN = process.env.PAGE_ACCESS_TOKEN;
const VERIFY_TOKEN = process.env.VERIFY_TOKEN;
```

Your setup is now complete.

## Build the experience

In this tutorial, you build a simple Messenger experience that does the following:

1. Parses the message and sender’s page-scoped ID from an incoming webhook event.
2. Handles `messages` and `messaging_postbacks` webhook events.
3. Sends messages via the Send API.
4. Responds to text messages with a text message.
5. Responds to an image attachment with a generic template that uses the received image.
6. Responds conditionally to a postback payload.

### Stub out handler functions

To start, stub out three functions that handle the incoming webhook event types you want to support, as well as responding via the Send API. Append the following to your `app.js` file:

```javascript
// Handles messages events
function handleMessage(sender_psid, received_message) {
  ...
}

// Handles messaging_postbacks events
function handlePostback(sender_psid, received_postback) {
  ...
}

// Sends response messages via the Send API
function callSendAPI(sender_psid, response) {
  ...
}
```

### Get the sender’s page-scoped ID

To respond to people on Messenger, you first need to know who they are. In Messenger, this is accomplished by getting the message sender’s page-scoped ID (PSID) from the incoming webhook event.

### What is a PSID?

A person is assigned a unique page-scoped ID (PSID) for each Facebook Page they start a conversation with. The PSID is used to identify a person when sending messages.

If you completed one of the options in the [Starter Project](https://developers.facebook.com/documentation/business-messaging/messenger-platform/getting-started/quick-start#starter) section above, you should have a basic `/webhook` endpoint that accepts `POST` requests and logs the body of received webhook events that looks like this:

```javascript
app.post('/webhook', (req, res) => {

  // Parse the request body from the POST
  let body = req.body;

  // Check the webhook event is from a Page subscription
  if (body.object === 'page') {

    // Iterate over each entry - there may be multiple if batched
    body.entry.forEach(function(entry) {

      // Get the webhook event. entry.messaging is an array, but
      // will only ever contain one event, so we get index 0
      let webhook_event = entry.messaging[0];
      console.log(webhook_event);

    });

    // Return a '200 OK' response to all events
    res.status(200).send('EVENT_RECEIVED');

  } else {
    // Return a '404 Not Found' if event is not from a page subscription
    res.sendStatus(404);
  }

});
```

To get the sender’s PSID, update the `body.entry.forEach` block with the following code to extract the PSID from the `sender.id` property of the event:

```javascript
body.entry.forEach(function(entry) {

  // Gets the body of the webhook event
  let webhook_event = entry.messaging[0];
  console.log(webhook_event);

  // Get the sender PSID
  let sender_psid = webhook_event.sender.id;
  console.log('Sender PSID: ' + sender_psid);

});
```

Test it

Open Messenger and send a message to the Facebook Page associated with your Messenger experience. You will not receive a response in Messenger, but you should see a message with your PSID logged to the console where your webhook is running:

```
Sender PSID: 1254938275682919
```

### Parse the webhook event type

Your experience needs to handle two types of webhook events: `messages` and `messaging_postback`. The name of the event type is not included in the event body, but you can determine it by checking for certain object properties.

What are webhook events?

The Messenger Platform sends webhook events to notify you of actions that occur in Messenger. Events are sent in JSON format as `POST` requests to your [webhook](https://developers.facebook.com/documentation/business-messaging/messenger-platform/webhooks). For more information, see [Webhook Events](https://developers.facebook.com/documentation/business-messaging/messenger-platform/webhooks).

To do this, update the `body.entry.forEach` block of your webhook with a conditional that checks whether the received event contains a `message` or `postback` property. This also adds calls to the `handleMessage()` and `handlePostback()` functions that you stubbed out earlier:

```javascript
body.entry.forEach(function(entry) {

  // Gets the body of the webhook event
  let webhook_event = entry.messaging[0];
  console.log(webhook_event);

  // Get the sender PSID
  let sender_psid = webhook_event.sender.id;
  console.log('Sender PSID: ' + sender_psid);

  // Check if the event is a message or postback and
  // pass the event to the appropriate handler function
  if (webhook_event.message) {
    handleMessage(sender_psid, webhook_event.message);
  } else if (webhook_event.postback) {
    handlePostback(sender_psid, webhook_event.postback);
  }

});
```

### Handle text messages

Now that incoming messages are routed to the appropriate handler function, update `handleMessage()` to handle and respond to basic text messages. Define the message payload of the response, then pass that payload to `callSendAPI()`. To respond with a basic text message, define a JSON object with a `"text"` property:

```javascript
function handleMessage(sender_psid, received_message) {

  let response;

  // Check if the message contains text
  if (received_message.text) {

    // Create the payload for a basic text message
    response = {
      "text": `You sent the message: "${received_message.text}". Now send me an image!`
    }
  }

  // Sends the response message
  callSendAPI(sender_psid, response);
}
```

### Send a message with the Send API

Time to send your first message with the Messenger Platform’s Send API!

In `handleMessage()`, you are calling `callSendAPI()`, so now you need to update it to construct the full request body and send it to the Messenger Platform. A request to the Send API has two properties:

- `recipient` : Sets the intended message recipient. In this case, you identify the person by their PSID.
- `message` : Sets the details of the message to be sent. Here, you set it to the message object passed in from your `handleMessage()` function.

To construct the request body, update the stub for `callSendAPI()` to the following:

```javascript
function callSendAPI(sender_psid, response) {
  // Construct the message body
  let request_body = {
    "recipient": {
      "id": sender_psid
    },
    "message": response
  }
}
```

Now send the message by submitting a `POST` request to the Send API at `https://graph.facebook.com/v21.0/me/messages`.

Note that you must append your `PAGE_ACCESS_TOKEN` in the `access_token` parameter of the URL query string.

Making HTTP Requests

This quick start uses the Node.js `request` module for sending HTTP requests back to the Messenger Platform, but you can use any HTTP client you like.

To install the request module, run `npm install request --save` from the command line, then import it by adding the following to the top of `app.js`:

```javascript
const request = require('request');
```

```javascript
function callSendAPI(sender_psid, response) {
  // Construct the message body
  let request_body = {
    "recipient": {
      "id": sender_psid
    },
    "message": response
  }

  // Send the HTTP request to the Messenger Platform
  request({
    "uri": "https://graph.facebook.com/v21.0/me/messages",
    "qs": { "access_token": process.env.PAGE_ACCESS_TOKEN },
    "method": "POST",
    "json": request_body
  }, (err, res, body) => {
    if (!err) {
      console.log('message sent!')
    } else {
      console.error("Unable to send message:" + err);
    }
  });
}
```

![Messenger conversation showing the echo response to a text message](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/651193025_1459945602530756_248014944894474888_n.png?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=lk1pcrK-Pr8Q7kNvwHAZHMZ&_nc_oc=Adr0g8bsiMmV6x24CmE6aD6JWcyUFxYiQFFahQnv_DIifDBCP2gKUlbCmkG-xa-65IE&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=G-GnGl_PMb_qhHAbhGWbVg&_nc_ss=7b20f&oh=00_Af5bENNF2kW_8AKhgUs6E8_sHx5cNcG_inyLurwLqW7dLQ&oe=6A1C1888)

Test it

In Messenger, send another text message to your Facebook Page. You should receive an automated response from your Messenger experience that echoes back your message and prompts you to send an image.

### Handle attachments

Since the response prompts the message recipient to send an image, the next step is to update your code to handle an attachment. Sent attachments are automatically saved by the Messenger Platform and made available via a URL in the `payload.url` property of each index in the `attachments` array, so you also extract this from the event.

What attachment types are supported?

Your Messenger experience can send and receive most asset types, including images, audio, video, and files. Media is displayed and is even playable in the conversation, allowing you to create media-rich experiences.

To determine if the message is an attachment, update the conditional in your `handleMessage()` function to check the `received_message` for an `attachments` property, then extract the URL for it. In a real-world bot you would iterate the array to check for multiple attachments, but for the purpose of this quick start, you get the first attachment only.

```javascript
function handleMessage(sender_psid, received_message) {

  let response;

  // Checks if the message contains text
  if (received_message.text) {

    // Creates the payload for a basic text message, which
    // will be added to the body of our request to the Send API
    response = {
      "text": `You sent the message: "${received_message.text}". Now send me an attachment!`
    }

  } else if (received_message.attachments) {

    // Gets the URL of the message attachment
    let attachment_url = received_message.attachments[0].payload.url;

  }

  // Sends the response message
  callSendAPI(sender_psid, response);
}
```

### Send a structured message

Next, respond to the image with a generic template message. The generic template is the most commonly used structured message type, and allows you to send an image, text, and buttons in one message.

Are other message templates available?

Yes! The Messenger Platform provides a set of useful message templates, each designed to support a different, common message structure, including lists, receipts, buttons, and more. For complete details, see [Templates](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/templates).

Message templates are defined in the `attachment` property of the message, which contains `type` and `payload` properties. The `payload` is where you set the details of the generic template in the following properties:

- `template_type` : Sets the type of template used for the message. This example uses the generic template, so the value is `generic` .
- `elements` : Sets the custom properties of the template. For the generic template, you specify a title, subtitle, image, and two postback buttons.

For the structured message, use the `attachment_url` that was sent as the `image_url` to display in the template, and include a couple of postback buttons to allow the message recipient to respond. To construct the message payload and send the generic template, update `handleMessage()` to the following:

```javascript
function handleMessage(sender_psid, received_message) {
  let response;

  // Checks if the message contains text
  if (received_message.text) {
    // Create the payload for a basic text message, which
    // will be added to the body of our request to the Send API
    response = {
      "text": `You sent the message: "${received_message.text}". Now send me an attachment!`
    }
  } else if (received_message.attachments) {
    // Get the URL of the message attachment
    let attachment_url = received_message.attachments[0].payload.url;
    response = {
      "attachment": {
        "type": "template",
        "payload": {
          "template_type": "generic",
          "elements": [{
            "title": "Is this the right picture?",
            "subtitle": "Tap a button to answer.",
            "image_url": attachment_url,
            "buttons": [
              {
                "type": "postback",
                "title": "Yes!",
                "payload": "yes",
              },
              {
                "type": "postback",
                "title": "No!",
                "payload": "no",
              }
            ],
          }]
        }
      }
    }
  }

  // Send the response message
  callSendAPI(sender_psid, response);
}
```

![Messenger conversation showing the generic template response with an image and postback buttons](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/651690036_1459945679197415_5126650271800155767_n.png?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=kqBe4-9mTt0Q7kNvwELzsq9&_nc_oc=Adoq-V9uJo4iozJhsRegsD06K8F-oihx_X3saGq2vVou1Yj9eHag-15O3_VYklqW64A&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=G-GnGl_PMb_qhHAbhGWbVg&_nc_ss=7b20f&oh=00_Af54GsaoAsAhh7cZVERjGH8jG6TC1BgcUSPjOBUHFJiKwQ&oe=6A1C4093)

Test it

In Messenger, send an image to your Facebook Page. Your Messenger experience should respond with a generic template.

### Handle postbacks

The last step is to handle the `messaging_postbacks` webhook event that is sent when the message recipient taps one of the postback buttons in the generic template.

What can I do with postbacks?

The [postback button](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/buttons/postback) sends a [`messaging_postbacks`](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/webhook-events/messaging_postbacks) webhook event to your webhook that includes a custom string of up to 1,000 characters in the `payload` property. This allows you to easily implement different postback payloads that you can parse and respond to with specific behaviors.

Since the generic template allows the message recipient to choose from two postback buttons, you respond based on the value of the `payload` property of the postback event. To do this, update your `handlePostback()` stub to the following:

```javascript
function handlePostback(sender_psid, received_postback) {
  let response;

  // Get the payload for the postback
  let payload = received_postback.payload;

  // Set the response based on the postback payload
  if (payload === 'yes') {
    response = { "text": "Thanks!" }
  } else if (payload === 'no') {
    response = { "text": "Oops, try sending another image." }
  }
  // Send the message to acknowledge the postback
  callSendAPI(sender_psid, response);
}
```

![Messenger conversation showing different text responses for each postback button](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/653709857_1459945589197424_8992472264603771484_n.png?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=x35d8qCxgnAQ7kNvwFoA9EL&_nc_oc=AdrNeCS7sJJW613wA9BZQG1o0zxs_Pj4lx0vF2Pw6RB62DRHw2V4Z70_Z-aDisjb8dw&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=G-GnGl_PMb_qhHAbhGWbVg&_nc_ss=7b20f&oh=00_Af62KqANCH7e6BXM7vF5trL3UtOxDKfU7oHBHNPOMtPMtw&oe=6A1C2077)

Test it

In Messenger, tap each of the postback buttons on the generic template. You should receive a different text response for each button.

If everything went well, you just finished building your first Messenger experience!

### Developer Support

- Use the [Meta Status tool](https://metastatus.com) to check for the status and outages of Meta business products.
- Use the [Meta Developer Support tool](https://developers.facebook.com/support) to report bugs and view reported bugs, get help with Ads or Business Manager, and more.
