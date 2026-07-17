# Best Practices | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/guides/bestpractices_

---

# Best Practices

Updated: Feb 10, 2026

These are guidelines to optimize both the WhatsApp Flows user and developer experience.

## Setup

### Flows shouldn’t be long

Users should enter flows aiming to complete a task as quickly as possible, with tasks taking no longer than 5 minutes to complete.

### Don’t have more than one task per screen

Screens with too many tasks may look messy and overwhelm the user. If the flow needs the user to complete multiple tasks, try splitting them up over several screens.

### Don’t use too many components per screen

Too many components will make your screens look messy and may overwhelm users. It will also take longer to load.

### Build for caching

Once a user has completed a screen and moves onto the next, their information will be cached. If there are too many components on a single screen and the user exits the flow, they will lose all of this information, which could be frustrating for users.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/652277310_1459945522530764_4667306230082696048_n.png?_nc_cat=102&ccb=1-7&_nc_sid=e280be&_nc_ohc=X9EexFZRRI4Q7kNvwEaLYFQ&_nc_oc=AdrTsCxyb_sO_UyymBP_cGfB4_9x8_sebc_hFtOIa8pS1hzk7BEHn2GtwFzptOF8UJI&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=Vn2CtFzPJSuba7Gp9oY1VA&_nc_ss=7b20f&oh=00_Af72s7sS5yi5BB9Gty6OAJQnYhRvDdOf61Zx5dyRT-pnMg&oe=6A1C2A31)

### Use flows without the endpoint whenever possible

- They often offer better experience for consumers
- They are faster to build and integrate
- They allow for the dynamic data to be injected in them at the time of sending

### Only use endpoint powered flows, when the live data is required while user completes a flow - e.g. for ticket booking.

- Prefer to make the first screen a data-channel-less to optimise flow opening
- Use an endpoint only for the specific screens which require it and use a navigate action otherwise

## Technical

### Latency

In order to achieve the best latency:

- Reduce the number of calls to third party platforms
- Use async calls to slow third party platforms
- Cache data to prevent re-fetching unchanged data

Requests to the WhatsApp Flows data endpoint time out after **10 seconds.**

### `flow_token` Expiration Management

We recommend having longer flow token expiration times, in the range of 2 to 3 days, to give more time for users to engage with flow messages after receiving them.

If that is not possible for security reasons, consider embedding a re-authentication mechanism in the flow, or set a user-friendly message for an [invalid flow token error](https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/reference/error-codes#endpoint_error_codes) with the recommended action to receive a new flow message.

If you have a business requirement to limit the flow message flow time, the timing should start only once the flow message has been opened, which is when the data channel receives the `INIT` request.

## Design

### Call-to-Actions (CTAs)

The CTA should always tell the user what will happen next or what task is being completed on each screen, for example **Confirm booking.**

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/651794737_1459945729197410_2240860389340405752_n.png?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=qsV274msQQEQ7kNvwHeKkss&_nc_oc=AdoM_QdiJPA0V9Na8qoeQub2rTv_hlLdKzXfEUhGt9j_5Vb38g_JSkwZ2wGDVY5wPss&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=Vn2CtFzPJSuba7Gp9oY1VA&_nc_ss=7b20f&oh=00_Af6-x5wl3EM0DelPEVC6HGd98J1fyHrfb0QhE1NNPCpTgA&oe=6A1C16A5)

### Capitalization

Use sentence case on screen titles, headings and CTAs. Use consistent capitalization throughout each flow.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/650683262_1459945695864080_813175482456100048_n.png?_nc_cat=102&ccb=1-7&_nc_sid=e280be&_nc_ohc=xnQwr1nOMrYQ7kNvwEGRAVL&_nc_oc=Adp8sS5auOVdauqBPW0uOl6Y_5OfIUY194_WIyYKwtC4UZoAx3sNzy-2RsqzFV90jgg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=Vn2CtFzPJSuba7Gp9oY1VA&_nc_ss=7b20f&oh=00_Af74NiyiEDk-CnVx23jxHfyRoPb5JwyOad-DppMkaFse2g&oe=6A1C2365)

### Emojis

Always consider the context of the content when using emojis, such as:

- Are they appropriate to use?
- Will they add to the content?
- Do they reflect the business brand?

### Error Handling

- Errors should be clearly communicated to the user, include what has happened and how to resolve it.
- Make sure validation rules are clearly communicated, such as if a user tries to enter a password that is not long enough.
- If the flow is exchanging data with your endpoint and a screen becomes invalid (eg. appointment booking), take the user back to the previous screen rather than ending the flow.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/651763608_1459945499197433_5530225472011935941_n.png?_nc_cat=101&ccb=1-7&_nc_sid=e280be&_nc_ohc=8LF_nbUJCtEQ7kNvwERnSyo&_nc_oc=AdpRY_He7awS4i2KTsiHliFONQvY_zbPyWdYcJvbyf2nfUTwGA7pPidZLYAhiR0lO8M&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=Vn2CtFzPJSuba7Gp9oY1VA&_nc_ss=7b20f&oh=00_Af4gaNHlkqCWkvRkkg0dvsFssvwin_btxQsSMPkUsnAYfQ&oe=6A1C19A4)

### Diverging Flows

If you need to create a sub flow for certain use cases (eg. a forgot password flow), try to keep it to a maximum of 3 screens and always take the user back to the main flow and task at hand.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/653853743_1459945649197418_4892987482333801249_n.png?_nc_cat=111&ccb=1-7&_nc_sid=e280be&_nc_ohc=zrlmjbFf5vYQ7kNvwFxRk_D&_nc_oc=AdogPgu_JG1kU5ETqggHQvR3gs-551jnzAK9ZeSF1-r4rIUom1XzdLSLRPRXwX5LNB0&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=Vn2CtFzPJSuba7Gp9oY1VA&_nc_ss=7b20f&oh=00_Af6Lhkksn0Ap1e9Er_644-UrfHqsV85Y1m5RBqK0ZnkLrQ&oe=6A1C0693)

### Form Quality

- Always use the right components for specific actions, for example use the date picker to capture DOB.
- If an input requires a lot of text, use the text area component and not the text input.
- Questions and from labels must provide full clarity on what it is asking the user.
- Forms or questions should be logically ordered, for example first name, last name etc.
- Forms that are not critical to completing a task should be made optional to the user.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/650262846_1459945529197430_4164859470529278961_n.png?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=UWNg2sW7dZAQ7kNvwGIem3K&_nc_oc=AdoUs1nXxHGjIROAqwGQ4QLczh8zk8JnpeCMygnxwWzQTaPGAgA-bm8HbPJM-QDwwKc&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=Vn2CtFzPJSuba7Gp9oY1VA&_nc_ss=7b20f&oh=00_Af6rmNSjNLNLHS2JR-EBsTQ055UDygqmfDa8Z8iMuI7o3w&oe=6A1C2A63)

### Formatting

Ensure that any information is correctly formatted for context, for example currency symbols, phone numbers, and dates.

### Grammar and Spelling

- Always check the content in your flows before publishing.
- Ensure you use consistent spelling and capitalization for certain terms.
- Check your grammar such as ensuring sentences use full-stops.

### Helper Text

Helper text should provide clarity for users, eg. the correct format for a phone number, date input, or email address.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/653708488_1459945645864085_8384520835334405020_n.png?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=0dZ3miC4GbkQ7kNvwGPvbgo&_nc_oc=AdrbMTM571MRTir_sIprS3OepDiJIJt29dzqJTNskElTzdvbQAs2reh05zOSQ_-PNyA&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=Vn2CtFzPJSuba7Gp9oY1VA&_nc_ss=7b20f&oh=00_Af48aqp45Id0JTjIgTrNUXCkvAK0a2-OvhOaV-GKkStjgA&oe=6A1C11CD)

### Initiation Flow

The chat should provide clarity

Users will choose to open a flow based on the clarity of the initiation messages. The exchange should feel conversational, providing context and clear task-focused actions for the user.

Users want to complete a task

The CTA should go hand-in-hand with the message content. It should be short and concise, telling the user what task they can expect to complete by opening the flow.

There should be no surprises

The first screen of the flow should mirror the action of the CTA. Any deviations from the task at hand will result in a bad experience for the user, resulting in them closing the flow.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/653700264_1459945642530752_4315354198930332437_n.png?_nc_cat=101&ccb=1-7&_nc_sid=e280be&_nc_ohc=nCSoZAA6oAMQ7kNvwEHmMQ6&_nc_oc=AdojJ4yesHy6yqwft7jNMEcpVMqArciUlcN_fDjEnIkuVXXdd_Iq9LbOtVO2ICUk_Hw&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=Vn2CtFzPJSuba7Gp9oY1VA&_nc_ss=7b20f&oh=00_Af4w7MyOgDhD37XH-CnxPu7bSM7DJBWCpZSd9C-4j5pusw&oe=6A1C1315)

### Login Screens

Some flows may need login screens to complete tasks. However, there are factors to consider when including them in your flows.

Use only when necessary

Including a login screen may be off putting for some users, so try to only use them when absolutely necessary. If you do need one, set the expectations for users so it doesn’t come as a surprise.

Sense of place within flow

Research has shown that login screens may confuse users within flows. Some people thought screens would take them to an external page, outside of WhatsApp. This may result in users losing their sense of place within the flow.

Users need to see the benefit of logging in

The placement of login screens is key. If they are too early in the flow, users will not be motivated to continue. Showing the benefits upfront will make users want to complete the flow. Aim to make the login screen one of the last steps before completion.

### Navigation

- Always set expectations for how long it will take to complete a task, eg. “It should only take a few minutes to complete.”
- Help the user know where they are in the flow by using short, concise action-oriented screen titles, such as “Book appointment.”
- Use screen titles to show progress where possible, eg. “Question 1 of 3.”
- End the flow with a summary screen, especially if there have been multiple steps, so users can review and complete the task with clarity.

### Opt-in

- It should be clear what the user is consenting to.
- You should try to include a “Read more” CTA which links to the relevant information, eg. Terms and Conditions.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/651719810_1459945465864103_6134028857871079489_n.png?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=peYy1FyOtbQQ7kNvwEtK3lg&_nc_oc=AdoWZgyyRbH4oTx_emRYCshE9X1fKnqbQFj-PtLzxnGUuboQLIYvBzuXnrxYu0_6Zjw&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=Vn2CtFzPJSuba7Gp9oY1VA&_nc_ss=7b20f&oh=00_Af7CkWyHRQuhOWjNMkzEMq_PI7S797OaTRUcHEyWPoXkNg&oe=6A1C3791)

### Options and lists

- Keep it simple, try not to use more than 10 options per screen.
- Only use dropdown options when there are 8 or more options.
- Use a radio button if there is only one selection to make.
- Use checkboxes if the user can select multiple options.
- Always make the option at the top of the list the default selection.

### Termination Flow

Set expectations

The last screen should clearly tell the user what will happen when they end the flow. They will also want confirmation of their actions. Sending a summary message should make the user feel reassured.

Keep the size of the completion payload minimal

We strongly recommend to only include data inputted by the user in the Flow’s completion payload, and to keep the payload size to a minimum. Avoid leveraging the completion payload to send base64 images.

Bookend your flows

We recommend responding to a user with a message when they submit a Flow. These messages should provide the user with information about next steps, and who they can get in touch with if they have any questions or if they want to edit or cancel a task.

As of Flows version 5.1, upon submitting a Flow, a user will be able to access a summary of their submitted data via the Flow response message UI. By default, all user-input data is included in the response message, with the exception of [text entry fields of type password and passcode](https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/reference/components#textinput). Businesses have the option to specify which data fields contain sensitive information by leveraging the `sensitive` property. These fields will not appear in the response message. For more details on how to configure sensitive fields, please refer to our [documentation](https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/reference/flowjson#additional-information-on-sensitive-fields).

### Trust and Support

- The business logo (profile photo) should be simple and identifiable in the footer so the user knows and trusts the flow.
- Add a CTA within your flow that enables your users to get in touch when needed. This can also be done in follow-up messages once the user has completed the flow.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/652218479_1459945489197434_2048823773378475966_n.png?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=J_zSe38ughcQ7kNvwHcubRq&_nc_oc=AdoNBbg5MeX8P3ymdgYw2An1GMy0yDj1SLoOF-us8b7BrPxZt9RpJPjrAa-oBf4xbkk&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=Vn2CtFzPJSuba7Gp9oY1VA&_nc_ss=7b20f&oh=00_Af4jFEnzvgNtsHZVktLc27H6PIR8xHIxCkHdcoaLmvPxlA&oe=6A1C2F44)

### Writing Content

- Make sure your content follows a simple, clear hierarchy using a heading, body and captions
- Do not repeat content unnecessarily, for example: “Complete registration”“Complete registration below”
