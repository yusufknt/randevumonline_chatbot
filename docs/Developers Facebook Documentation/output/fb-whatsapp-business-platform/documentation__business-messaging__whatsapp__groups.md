# Groups API | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/groups_

---

# Groups API

Updated: Nov 14, 2025

**Eligibility for Groups API**

The Groups API is now open to all businesses with an [Official Business Account (OBA)](https://developers.facebook.com/documentation/business-messaging/whatsapp/official-business-accounts)

The Groups API enables you to programmatically create groups for messaging and collaboration.

## How it works

Groups are an invite-only experience where participants join using a group invite link you send them. This invite link provides context about the group, helping the user decide whether they want to join.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/583332263_2097826120969757_476207660850437421_n.png?_nc_cat=111&ccb=1-7&_nc_sid=e280be&_nc_ohc=biI3yu7RIJ0Q7kNvwEPNy6M&_nc_oc=AdqYRAUVA_kNUs3vZCTT4CQQz1bJDxJd6ywhzoNayAufWcg1ZioIOsRcqyq9t9G_UW0&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=VF0hUMV9iKBDsJwb8F7PaA&_nc_ss=7b20f&oh=00_Af5upHdVwhNDdFCjYdjerntlxHJYrUyeXJ1Z7EQ3Q1aaYA&oe=6A1C00BB)

## Get Started

When you are ready to start using the Groups API, head on over to our “Get Started” guide for more information:

[Get Started with Groups API](https://developers.facebook.com/documentation/business-messaging/whatsapp/groups/get-started)

## Quick Facts

- **Max group participants:** 8
- **Supported message types:** Text, media, text-based templates, and media-based templates
- **Max groups you can create:** 10,000 per business number
- **Max Cloud API businesses per group:** 1

## Analytics

**Performance metrics are not available for message templates used in Groups.**

Please create new templates specifically for Groups use instead of repurposing templates used for one-to-one messaging.

## Limits

**Eligibility for Groups API**

To qualify for groups features, your business must be an [Official Business Account (OBA)](https://developers.facebook.com/documentation/business-messaging/whatsapp/official-business-accounts)

*Groups are **not available** for [WhatsApp Business app phone numbers](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users) and phone numbers onboarded to [Multi-solution Conversations](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/multi-solution-conversations)*.

*The [Calling API](https://developers.facebook.com/documentation/business-messaging/whatsapp/calling) is not supported in groups.*

- **Non-supported message types:** CallingDisappearing messagesView-onceAuthCommerce messagesInteractive messages
- **Non-supported actions:** Admin hide group participant listEdit messageDelete messageMarking message as read

## Pricing

The Groups API uses [per-message pricing](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing).

[Learn more about Groups API pricing here](https://developers.facebook.com/documentation/business-messaging/whatsapp/groups/pricing)

## Features and reference

### Group management features

- [Create and delete group](https://developers.facebook.com/documentation/business-messaging/whatsapp/groups/reference#create-group)
- [Groups with join requests enabled](https://developers.facebook.com/documentation/business-messaging/whatsapp/groups/reference#groups-with-join-requests)
- [Get and reset group invite link](https://developers.facebook.com/documentation/business-messaging/whatsapp/groups/reference#get-and-reset-group-invite-link)
- [Send group invite link template message](https://developers.facebook.com/documentation/business-messaging/whatsapp/groups/reference#send-group-invite-link-template-message)
- [Remove group participants](https://developers.facebook.com/documentation/business-messaging/whatsapp/groups/reference#remove-group-participants-endpoint)
- [Get group info](https://developers.facebook.com/documentation/business-messaging/whatsapp/groups/reference#get-group-info)
- [Get active groups](https://developers.facebook.com/documentation/business-messaging/whatsapp/groups/reference#get-active-groups)
- [Update group settings](https://developers.facebook.com/documentation/business-messaging/whatsapp/groups/reference#update-group-settings)

[*View Group Management reference*](https://developers.facebook.com/documentation/business-messaging/whatsapp/groups/reference)

### Group messaging features

- [Send group messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/groups/groups-messaging#send-group-message)
- [Receive group messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/groups/groups-messaging#receive-group-messages)
- [Pin and unpin group message](https://developers.facebook.com/documentation/business-messaging/whatsapp/groups/groups-messaging#pin-and-unpin-group-message)

[*View Group Messaging reference*](https://developers.facebook.com/documentation/business-messaging/whatsapp/groups/groups-messaging)
