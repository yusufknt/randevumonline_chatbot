# Create a test webhook endpoint | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/set-up-whatsapp-echo-bot_

---

# Create a test webhook endpoint

Updated: Nov 7, 2025

If you aren’t ready to create your own webhook endpoint yet, you can deploy a test webhook app on [Render.com](https://www.render.com/) that accepts webhook requests and dumps their contents to Render’s console.

*Only use this app for testing purposes.*

## Requirements

- A [Render](https://www.render.com/) account.
- A [GitHub](https://www.github.com/) account.

## Step 1: Create a GitHub repository

Sign into your GitHub account and create a new repo (public or private) with a name of your choice. Within the repo, create an `app.js` file and paste this code into it:

```js
// Import Express.js
const express = require('express');

// Create an Express app
const app = express();

// Middleware to parse JSON bodies
app.use(express.json());

// Set port and verify_token
const port = process.env.PORT || 3000;
const verifyToken = process.env.VERIFY_TOKEN;

// Route for GET requests
app.get('/', (req, res) => {
  const { 'hub.mode': mode, 'hub.challenge': challenge, 'hub.verify_token': token } = req.query;

  if (mode === 'subscribe' && token === verifyToken) {
    console.log('WEBHOOK VERIFIED');
    res.status(200).send(challenge);
  } else {
    res.status(403).end();
  }
});

// Route for POST requests
app.post('/', (req, res) => {
  const timestamp = new Date().toISOString().replace('T', ' ').slice(0, 19);
  console.log(`\n\nWebhook received ${timestamp}\n`);
  console.log(JSON.stringify(req.body, null, 2));
  res.status(200).end();
});

// Start the server
app.listen(port, () => {
  console.log(`\nListening on port ${port}\n`);
});
```

## Step 2: Deploy a Node Express app on Render

Follow Render’s instructions for [deploying a Node Express app](https://render.com/docs/deploy-node-express-app), with these differences:

- Skip step 1
- Use these settings for step 3: Build command: `npm install express`Start command: `node app.js`In the **Environment Variables** section, add the variable `VERIFY_TOKEN` and set it to a string of your choice (e.g. `vibecode`).

When you’re done, click the **Deploy your web service** button. This will take you to the app log where you will see your app being built, which can take a few minutes. You’ll know it’s done when you see “Your service is live” in the log.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/518314752_779138407775567_4233589617658404934_n.png?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=KGVVG0K8vDAQ7kNvwHZ7al7&_nc_oc=Adpf8K3ak6Jmp6Wcb50yjsqKsjYkqQtoQZdTSNaWwjcpkaUW-JBY-oYKD0Z9-06xLtA&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=UhCXbwSUhczjVSPoy10rGw&_nc_ss=7b20f&oh=00_Af4NM0RcSdnZSvOR-Gs-_HisvySjznsJLJYYIiNI3DcD4w&oe=6A1C1EC5)

Copy your deployed test webhook app URL, which is displayed at the top of the page under your GitHub repo name. (If you view the URL, you’ll get a 403 error, which is expected).

## Step 3: Add your test webhook app URL to your Meta app

Open a new window/tab, and navigate to the (Meta) [App Dashboard](https://developers.facebook.com/apps) > **WhatsApp** > **Webhooks** > **Configuration** panel.

Paste your test webhook app URL in the **Callback URL** field, and add the `VERIFY_TOKEN` environment variable string you set earlier to the **Verify token** field, then click **Verify and save**.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/518348561_1679202599393717_3427225193188619311_n.png?_nc_cat=111&ccb=1-7&_nc_sid=e280be&_nc_ohc=vxA9utHbQPwQ7kNvwGZzhE7&_nc_oc=AdpJuoPr2dVkhl9SlqoZxh5g_oj3FfAILYRRe-dRGHOLSKAVhNOaIvdDCC3pAJD820g&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=UhCXbwSUhczjVSPoy10rGw&_nc_ss=7b20f&oh=00_Af5u3x4vzhqbQLJxf0MZmG8vIRuQ8S9MU8lj_8OTKIVOJg&oe=6A1C1670)

If verification is successful, the Meta app dashboard should refresh and you should see a list of webhook fields you can subscribe to.

*Subscribe to the **messages** webhook field if you haven’t already.*

Also, in Render’s app log, if you see “WEBHOOK VERIFIED”, your test webhook app URL has been successfully verified.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/516871315_2146397049169598_3394446764023076795_n.png?_nc_cat=101&ccb=1-7&_nc_sid=e280be&_nc_ohc=uAwuS0qvcDMQ7kNvwGNrXaQ&_nc_oc=AdooiWyjCRX48qXbCWMBgL1AkkPMnT3hJWLzWKNpY-BFelcYgs9ICxVkf4oqF2rUi-E&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=UhCXbwSUhczjVSPoy10rGw&_nc_ss=7b20f&oh=00_Af4Wp7GCr9Bxm7i46kseuS9RoXOmjlFFrDODQfhwZ4cwAQ&oe=6A1C06D0)

## Step 4: Send a test message

Back in the Meta app dashboard **Configuration** panel, scroll down to the **messages** webhook field, subscribe to the field if you haven’t already, then click the **Test** link.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/518357131_2083466912058941_6508814785021877118_n.png?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=lw6qCRFWQ7cQ7kNvwGB_ZBg&_nc_oc=Adpxr-XW9PT1daAvTsp195sMDLtyXRoxfaUCR3b6sPIWQr5hHozp7NiLlxbsw-FiXD8&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=UhCXbwSUhczjVSPoy10rGw&_nc_ss=7b20f&oh=00_Af5SrRoQM5czb4bIY6vi2WLTf3z4Rn3LxOuv5NdgIxQlig&oe=6A1C148B)

This will send a test message to your test webhook app. Confirm that it appears in Render app log with “Webhook received” followed by a test JSON payload:

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/516488905_709538035232698_4800340255912767794_n.png?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=Mi7XBHdUaJUQ7kNvwGfQCYS&_nc_oc=AdpFjnOBvE8uhTj9uudIrrQdmy-M7Np0HvJikaTvuXDqWcGFPcSEs2Rp2hkY-xOWkYY&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=UhCXbwSUhczjVSPoy10rGw&_nc_ss=7b20f&oh=00_Af7rVLhSq2-jE0wmN_QtKpx8qVWbKEUGUQ0B9KCyMHCcuw&oe=6A1BFF81)

## Troubleshooting

If the test **messages** webhook doesn’t appear in the Render app dashboard log:

- Confirm that you successfully added your test webhook app URL to your Meta app (Step 3).
- Confirm that your app is subscribed to the **messages** webhook field.
- Make sure you are sending a **messages** test webhook; some test webhooks only work when your app is in Live mode, while others only work in Development mode ( **messages** test webhooks work in both modes).
