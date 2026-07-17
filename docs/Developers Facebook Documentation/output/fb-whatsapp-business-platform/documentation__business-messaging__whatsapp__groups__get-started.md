# Get started with Groups API | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/groups/get-started_

---

# Get started with Groups API

Updated: Nov 14, 2025

**Eligibility for Groups API**

To qualify for groups features, your business must be an [Official Business Account (OBA)](https://developers.facebook.com/documentation/business-messaging/whatsapp/official-business-accounts)

## Overview

Groups on are invite-only, meaning that potential group participants are ultimately in control of whether they want to join the group or not.

When you create a group, a unique invite link that is generated which you can share to potential group participants. This link includes information about the group, enabling users to make an informed decision about whether or not they want to join the group.

Once a user joins the group, a webhook is triggered, signaling that you are now eligible to send messages to the group.

For a complete overview of available features, see the [Groups API Features](https://developers.facebook.com/documentation/business-messaging/whatsapp/groups/get-started#features) below.

## How to start using groups

### Prerequisites

Before you get started with the Groups API, ensure that:

1. Your business number is in use with Cloud API (not the WhatsApp Business app).
2. Your webhook server is set up for use with Cloud API.
3. Your app is subscribed to the following groups webhook fields: `group_lifecycle_update``group_participants_update``group_settings_update``group_status_update`
4. Your app is subscribed to the WhatsApp Business Account of your business phone number.
5. Your app has the `whatsapp_business_messaging` permission for the business number.

### Step 2: Create a group

Use the [Create Group endpoint](https://developers.facebook.com/documentation/business-messaging/whatsapp/groups/reference#create-group) to create a group, providing a subject and an optional description. Once a group has been successfully created, a [`group_lifecycle_update` webhook for successful group creation](https://developers.facebook.com/documentation/business-messaging/whatsapp/groups/webhooks#group-create-succeed) will be returned. This webhook will include a `invite_link` field with the invite link that you can now share with potential group participants.

### Step 3: Invite WhatsApp users to the group

3.1 Add a group invite link template in

Template Library

to your account templates:

1. Navigate to [Template Library](https://business.facebook.com/wa/manage/template-library)
2. On the left, click the **Group invite link** dropdown, then click the **Group invite upon request** checkbox.
3. Select the template you want to use, give it a name, and click **Submit**

3.2 Send the invite link to potential group participants

Once the template has been approved, use the template to invite members to the group using the invite link provided in the webhook from Step 2.

You can follow the instructions in the [Send Group Invite Link Template Message reference](https://developers.facebook.com/documentation/business-messaging/whatsapp/groups/reference#send-group-invite-link-template-message) to send the invite link with the template you just added to your account.

3.3 Notification of when participants join the group

When a participant joins, a [`group_participants_update` webhook for a group participant joining webhook](https://developers.facebook.com/documentation/business-messaging/whatsapp/groups/webhooks#group-participants-update-webhook) will be triggered.

### Step 4: Send and receive messages

You can now use the [Cloud API send message endpoint](https://developers.facebook.com/documentation/business-messaging/whatsapp/groups/groups-messaging#send-group-message) to send messages to the group.

[Sent, delivered, and read status webhooks](https://developers.facebook.com/documentation/business-messaging/whatsapp/groups/webhooks#group-message-status-webhooks) will be triggered when there are updates in the group. Replies from participants will also trigger webhooks.

[Learn more about how to send and receive group messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/groups/groups-messaging)

## Features

To learn more about all the features available in groups:

- Visit the [Group Management reference](https://developers.facebook.com/documentation/business-messaging/whatsapp/groups/reference) to learn more about features available for managing groups.
- Visit the [Group Messaging reference](https://developers.facebook.com/documentation/business-messaging/whatsapp/groups/groups-messaging) to understand sending, receiving, and other messaging functions in groups.
