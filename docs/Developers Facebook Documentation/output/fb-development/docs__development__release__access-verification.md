# Access Verification - App Development with Meta

_Source: https://developers.facebook.com/docs/development/release/access-verification_

---

# Access Verification

To ensure that only [businesses](https://business.facebook.com/) with a legitimate use case can access another business's business data, some API endpoints perform a [verification check](#verification-check) when called by an app that has been created or claimed by a business, or by a [business app](https://developers.facebook.com/docs/development/create-an-app/app-dashboard/app-types#business) that has yet to be connected to a business. If the business that created, claimed, or is connected to the app has been verified as a [Tech Provider](https://developers.facebook.com/docs/development/release/tech-providers), the endpoints will process the request normally. If the business has not been verified as a Tech Provider, however, the endpoints will reject the call and return an error.

Access verification is the process we use to determine if a business operates as a Tech Provider.

## Which businesses require access verification?

Any business that has created or claimed an app that will be used by other businesses and requires any of the permissions listed below must be verified as a Tech Provider before other businesses can use the app.

Note that access verification is independent of [App Review](https://developers.facebook.com/docs/resp-plat-initiatives/app-review) and permission [access levels](https://developers.facebook.com/docs/graph-api/overview/access-levels).

## [Permissions](https://developers.facebook.com/docs/permissions/)

|  |  |
| --- | --- |
| - `ads_management` - `ads_read` - `attribution_read` - `business_management` - `catalog_management` - `facebook_creator_marketplace_discovery` - `instagram_basic` - `instagram_business_basic` - `instagram_business_content_publish` - `instagram_content_publish` - `instagram_creator_marketplace_discovery` - `instagram_manage_insights` - `leads_retrieval` - `manage_app_solution` - `page_events` - `pages_manage_ads` - `pages_manage_cta` - `pages_manage_engagement` | - `pages_manage_instant_articles` - `pages_manage_posts` - `pages_read_engagement` - `pages_read_user_content` - `pages_show_list` - `pages_utility_messaging` - `publish_video` - `read_insights` - `threads_basic` - `threads_content_publish` - `threads_keyword_search` - `threads_manage_insights` - `threads_manage_mentions` - `threads_manage_replies` - `threads_read_replies` - `whatsapp_business_management` |

## Verification Check

When an app claimed by a business calls an endpoint that requires any of the permissions listed above, the endpoint first checks if the person who granted the permission has a [role](https://developers.facebook.com/docs/development/build-and-test/app-roles) on the app itself. If the person **does** have a role on the app, the endpoint accepts the call and continues processing the request.

If the person **does not** have a role on the app, however, the endpoint checks if the app's claimant business has been verified as a Tech Provider. If the business has been verified as a Tech Provider, the endpoint processes the request normally, otherwise, it rejects the call and returns the following error:

- Error code: `100`
- Description: `Unsupported get request. Object with ID` <OBJECT\_ID> `does not exist, cannot be loaded due to missing permissions, or does not support this operation.`

Refer to the [Marketing API Error Codes](https://developers.facebook.com/docs/marketing-api/error-reference) documentation for more information about error codes.

Note that the verification check is performed on the app's claimant business but is only triggered when an app it has claimed calls an endpoint that has implemented the verification check. This means that once a business has been verified as a Tech Provider, any apps that it claims will pass the verification check.

## How to complete access verification

[Business admins](https://www.facebook.com/business/help/442345745885606) of an unverified Tech Provider business that claims a new app will receive an email notification about the access verification requirement whenever an [app administrator](https://developers.facebook.com/docs/development/build-and-test/app-roles#administrator) requests [Advanced Access](https://developers.facebook.com/docs/graph-api/overview/access-levels#advanced-access) for any of the permissions listed above.

The email will include a link to the verification form, but the form can also be accessed from the [App Dashboard](https://developers.facebook.com/docs/development/create-an-app/app-dashboard) by navigating to the **Basics** > **Verifications** > **Access verification** panel.

To complete verification, any person with Admin access on the business must categorize and describe how the business uses other businesses' data to provide a service for those businesses.

Once a business admin has completed the process a decision will be made within approximately 5 days.

If the business is verified as a Tech Provider, business admins will receive a confirmation email and app admins will receive a confirmation developer alert. Verified businesses won't have to verify again, however, under certain conditions a business may temporarily [lose its verified status](#losing-verified-status).

If the business is denied Tech Provider verification, business admins will receive a rejection email and app admins will receive a rejection developer alert, and all calls to endpoints that require the permissions above will fail if the app user has no [role](https://developers.facebook.com/docs/development/build-and-test/app-roles) on the calling app.

If the rejected businesses's use case changes, a business admin may complete the process again to be reconsidered.

### Prerequisites

Before a business admin can begin the access verification process:

- a business admin must complete [Business Verification](https://developers.facebook.com/docs/development/release/business-verification)
- there must be no [restrictions](https://www.facebook.com/business/help/422289316306981) on the business account

## Existing Business

Admins of businesses that have already claimed apps that are used by other businesses and require any of the permissions above will automatically be sent an email about the access verification requirement. App administrators will also receive a developer alert about this requirement.

Once the email has been sent, business admins will have 60 days to complete the verification process. If the process is not completed within 60 days, all calls to endpoints that require any of the permission above will gradually be subjected to [verification checks](#verification-check).

## Losing Verified Status

A business that has been verified as a Tech Provider will be considered unverified under these conditions:

- The business's [verification](https://developers.facebook.com/docs/development/release/business-verification) status changes to **unverified**
- The app becomes disconnected from the business that created or claimed it
- The business account becomes [restricted](https://www.facebook.com/business/help/422289316306981)

Once these conditions are reversed the business will automatically be considered to be a verified Tech Provider again.

## See Also

- [Tech Providers](https://developers.facebook.com/docs/development/release/tech-providers)
