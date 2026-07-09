# Permission Mapping - App Development with Meta

_Source: https://developers.facebook.com/docs/development/create-an-app/use-cases-permission-mapping_

---

# Use Case Permission Mapping

The following table shows you the permissions and features that are both required for a particular use case and additional, optional permissions and features that are available for that use case.

| Use Case | Required Permissions/Features | Optional Permissions/Features |
| --- | --- | --- |
| Access the Threads API | - `threads_basic` | - `threads_read_replies` - `threads_manage_replies` - `threads_content_publish` - `threads_manage_insights` - `threads_keyword_search` - `threads_profile_discovery` - `threads_manage_mentions` - `threads_delete` - `threads_location_tagging` - `threads_share_to_instagram` |
| Advertise on your app with Meta Audience Network | - `public_profile` |  |
| Authenticate and request data from users with Facebook Login | - `public_profile` | - `email` - `user_hometown` - `user_birthday` - `user_age_range` - `user_gender` - `user_link` - `user_friends` - `user_location` - `user_likes` - `user_photos` - `user_videos` - `user_posts` |
| Capture & manage ad leads with Marketing API | - `public_profile` - `ads_management` - `ads_read` - Ads Management Standard Access - `business_management` - `leads_retrieval` - `pages_manage_ads` - `pages_read_engagement` - `pages_show_list` | - `email` - `pages_manage_metadata` - Business Asset User Profile Access |
| Connect with customers through WhatsApp | - `whatsapp_business_messaging` - `whatsapp_business_management` - `public_profile` | - `business_management` - `whatsapp_business_manage_events` - `email` - `manage_app_solution` |
| Create & manage ads with Marketing API | - `public_profile` - `ads_management` - `ads_read` - Ads Management Standard Access - `business_management` - `pages_read_engagement` - `pages_show_list` | - `catalog_management` - `pages_manage_ads` - `email` - `threads_business_basic` - Business Asset User Profile Access |
| Embed Facebook, Instagram and Threads content in other websites |  | - Meta oEmbed Read - Threads oEmbed Read |
| Engage with customers on Messenger from Meta | - `public_profile` - `business_management` - `pages_manage_metadata` - `pages_messaging` - `pages_show_list` | - `email` - `ads_management` - `instagram_basic` - `instagram_manage_messages` - `pages_user_gender` - `pages_user_locale` - `pages_user_timezone` - `pages_utility_messaging` - `pages_read_engagement` - `paid_marketing_messages` - Business Asset User Profile Access - `marketing_messages_messenger` |
| Join ThreatExchange |  | - ThreatExchange |
| Launch an Instant Game on Facebook and Messenger | - `gaming_profile` - `gaming_user_picture` | - `gaming_user_locale` - `email` - Instant Games Zero Permission Access |
| Manage everything on your Page | - `business_management` - `pages_show_list` - `public_profile` | - `email` - `pages_read_engagement` - `pages_read_user_content` - `pages_manage_engagement` - `pages_manage_posts` - `pages_manage_metadata` - `read_insights` - Business Asset User Profile Access - `facebook_branded_content_ads_brand` - `facebook_creator_marketplace_discovery` - Live Video API |
| Manage messaging & content on Instagram | - `public_profile` | - `email` - `ads_management` - `ads_read` - `business_management` - `catalog_management` - Human Agent - `instagram_basic` - `instagram_business_basic` - `instagram_branded_content_ads_brand` - `instagram_branded_content_brand` - `instagram_branded_content_creator` - `instagram_creator_marketplace_discovery` - `instagram_creator_marketplace_messaging` - `instagram_business_content_publish` - `instagram_business_manage_comments` - `instagram_business_manage_insights` - `instagram_business_manage_messages` - `instagram_content_publish` - `instagram_manage_comments` - `instagram_manage_contents` - `instagram_manage_engagement` - `instagram_manage_insights` - `instagram_manage_messages` - `instagram_manage_upcoming_events` - Instagram Public Content Access - `instagram_shopping_tag_products` - `pages_read_engagement` - `pages_show_list` - Business Asset User Profile Access |
| Manage products with Catalog API | - `public_profile` - `catalog_management` | - `email` |
| Measure ad performance data with Marketing API | - `public_profile` - `ads_read` - `ads_management` - Ads Management Standard Access - `business_management` - `pages_read_engagement` - `pages_show_list` | - `email` - Business Asset User Profile Access |
| Share or create fundraisers on Facebook and Instagram | - `public_profile` - `manage_fundraisers` | - `email` |
