# WhatsApp Business Platform | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/overview_

---

What's next for business messaging and AI? Watch the Conversations keynote live on June 3.

Register now

WhatsApp Business Platform

Drive revenue growth, boost efficiency, and deliver exceptional customer experiences with the WhatsApp Business Platform—our enterprise-grade APIs for messaging and calling.

Demo the API

Preview an interactive experience showing how Jasper’s Market (our demo retail business) connects with customers using the WhatsApp Business Platform.

Demo retail business

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.8562-6/547429620_764982376167016_715228206216507834_n.png?stp=dst-webp&_nc_cat=105&ccb=1-7&_nc_sid=9a942e&_nc_ohc=ybN8T4DFAX4Q7kNvwEKGhpc&_nc_oc=AdrEjvu6Ev-pULbckVRZAi9TN5uWjCzLfD3V4AjdwsDq-FeWphxtYoDgoY_QxaaaY5M&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=UrpHncEDnOH4_Xl7XF427g&_nc_ss=7b20f&oh=00_Af4E8mKkmj8LNbuFtFJhhwRx46bA2PCcl233UKdFNNMOYw&oe=6A07AA7E)

Demo the API on your phone

Scan the QR code to start your live, interactive experience with our demo retail business, Jasper’s Market.

![Image](https://lookaside.fbsbx.com/elementpath/media/?media_id=2017431862353093&version=1778016448&transcode_extension=webp)

Demo on the desktop app instead

Download the sample app

import requests

url = "https://graph.facebook.com/<API_VERSION>/<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>/messages"
headers = {
 "Authorization": "Bearer <ACCESS_TOKEN>",
 "Content-Type": "application/json",
}
data = {
 "messaging_product": "whatsapp",
 "to": "<WHATSAPP_USER_PHONE_NUMBER>",
 "type": "template",
 "template": {
 "name": "hello_world",
 "language": {"code": "en_US"},
 }
}
 
response = requests.post(url, headers=headers, json=data, timeout=30)
print(response.json())

const url = "https://graph.facebook.com/<API_VERSION>/<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>/messages";
const headers = {
 "Authorization": "Bearer <ACCESS_TOKEN>",
 "Content-Type": "application/json",
};
const body = {
 messaging_product: "whatsapp",
 to: "<WHATSAPP_USER_PHONE_NUMBER>",
 type: "template",
 template: {
 name: "hello_world",
 language: { code: "en_US" },
 },
};
const response = await fetch(url, {
 method: "POST",
 headers,
 body: JSON.stringify(body),
});
const data = await response.json();
console.log(data);

curl -X POST 'https://graph.facebook.com/<API_VERSION>/<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>/messages' \
 --header 'Authorization: Bearer <ACCESS_TOKEN>' \
 --header 'Content-Type: application/json' \
 --data '{
 "messaging_product": "whatsapp",
 "to": "<WHATSAPP_USER_PHONE_NUMBER>",
 "type": "template",
 "template": {
 "name": "hello_world",
 "language": { "code": "en_US" }
 }
 }'

Essentials

Start building conversational experiences that delight your customers

About the platform

Learn more about the key components of the platform and how things work together.

Messaging

Learn about the different message types and how to send them.

Pricing

Learn how pricing on the WhatsApp Business Platform works.

Templates

Learn how to create and manage template messages.

Webhooks

Learn what webhooks are and how they are a core component of Business Messaging.

Authentication and authorization

Learn how access controls and permissions work on the platform.

About the APIs

Learn about the APIs that are part of the WhatsApp Business Platform

Cloud API

Send and receive WhatsApp messages, make WhatsApp calls, and more from your business phone number.

Marketing Messages API for WhatsApp

Access new features not available on Cloud API and get automatic optimizations, so high engagement messages can reach more customers.

Business Management API

Programmatically manage your WhatsApp business account and its assets.

New releases

Explore our newest features and launches

WhatsApp API Calling

Seamless, secure, and personalized voice calling natively within WhatsApp chat to drive superior business outcomes.

Groups API

Drive sales and solve customer problems with groups on the WhatsApp Business Platform.

API solutions for WhatsApp Business app users

Use both the WhatsApp Business app and API with the same phone number to simplify onboarding and unlock new features to scale your business.

Partner resources

Build WhatsApp solutions for your business customers.

Become a Tech Provider

Follow this guide to onboard as a WhatsApp Tech Provider so that you can start providing messaging services to your clients.

Onboard customers

Learn how to build Embedded Signup; a flow to onboard customers directly from your website.

MM API for WhatsApp Partner Guide

Learn how to integrate with MM API for WhatsApp and onboard your customers to send marketing messages with optimizations.

Not a developer?

View the Partner Showcase to find a partner tailored to fit your business needs.
