# Instagram API with Instagram Login - Instagram Platform

_Source: https://developers.facebook.com/docs/instagram/platform/instagram-api_

---

# Instagram API with Instagram Login

The Instagram API with Instagram Login allows
[Instagram professionals](https://l.facebook.com/l.php?u=https%3A%2F%2Fhelp.instagram.com%2F502981923235522&h=AUCzg5v65v51iQuoI1r22YfAIo7AS-NRRnzI26-aab-qzBpsWGCjhMUR71tBqYNQU-gIi8tqqcPTUyNu24dGj2zMYupqZxDKujdoIm_lk3wa_oVflJtzZ-nsGvp2ZMz6InFsKwsK49nU7Q)
— businesses and creators — to use your app to manage their presence on Instagram. The API can be used to:

Instagram Media Insights are now available for Instagram API with Instagram Login. [Learn more.](https://developers.facebook.com/docs/instagram-platform/reference/instagram-media/insights)

- **Comment moderation** – Manage and reply to comments on their media
- **Content publishing** – Get and publish their media
- **Media Insights** - Get insights on their media
- **Mentions** – Identify media where they have been @mentioned by other Instagram users
- **Messaging** – Send and receive messages with customers or people interested in their Instagram account

**Note:** This API setup does not require a Facebook Page to be linked to the Instagram professional account.

To ensure consistency between scope values and permission names, we are introducing new `scope` values for the Instagram API with Instagram login. The new `scope` values are:

- `instagram_business_basic`
- `instagram_business_content_publish`
- `instagram_business_manage_messages`
- `instagram_business_manage_comments`

These will replace the existing `business_basic`, `business_content_publish`, `business_manage_comments` and `business_manage_messages` `scope` values, respectively.

Please note that the old scope values will be deprecated on **January 27, 2025**. It is essential to update your code before this date to avoid any disruption in your app's functionality. Failure to do so will result in your app being unable to call the Instagram endpoints.

## Limitations

- This API setup cannot access ads or tagging.

## Next Steps

Next, read the [**Overview**](https://developers.facebook.com/docs/instagram/platform/instagram-api/overview) to learn about the core concepts, components, and usage requirements for this API.

## See Also

- [Instagram API with Facebook Login](https://developers.facebook.com/docs/instagram-api)
- [Instagram Messaging with Messenger Platform](https://developers.facebook.com/docs/messenger-platform/instagram)
- [Instagram professional accounts](https://l.facebook.com/l.php?u=https%3A%2F%2Fhelp.instagram.com%2F502981923235522&h=AUC87T66F4l8-2MndvuYWu3WEbnhveR_zJj8q3zAXoeQ1SD72UhT61QiGTPBfrJd63KlQd6aip-vPnhJ25WR2baFc-Uo0txdP8LVqtsH54NIz-wdrLfiW1EfZqbd-c1oj_S31jDX_zK3qo4LySsQP8ugAis)
