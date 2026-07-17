# Separate Ad Accounts Policy - App Development with Meta

_Source: https://developers.facebook.com/docs/development/terms-and-policies/separate-ad-accounts_

---

# Developer Policy

Note: The following serves as supplementary material to complement the official Developer Policies. To ensure that you keep your app’s policy compliant, please review the [Developer Policies](https://developers.facebook.com/devpolicy) and
[Platform Terms](https://developers.facebook.com/terms/dfc_platform_terms).

Developer Policy 10.5 states: *“Don't combine multiple end advertisers or their Meta business assets in the same ad account, unless you meet the requirements described here or as otherwise approved by Meta in writing”.*

This policy requires you to maintain a clear separation between each end advertiser and their assets, so that you can easily identify and track ownership and accountability for ad content, spend, and data for every end advertiser. This policy also helps reduce disruption to other end advertisers when an issue related to one end advertiser (or its assets) requires enforcement action.

Alternative to Maintaining Separate Accounts: If you implement a `vendor_id` and/or `brand` field in your Product Catalog, and/or in your Meta Pixel and Conversions (CAPI) integrations, you will be considered to be in compliance with Developer Policy 10.5, provided you properly implement such fields and remain in compliance with all Meta terms, conditions, and policies related to the foregoing. Meta reserves the right to revoke this alternative at any time if, in our sole discretion, we determine that it is necessary to protect Meta, its users, or the integrity of its products.

### **Required signals**

Implement **at least one** of:

- **vendor\_id**
- **brand**

### **Required surfaces**

You must include the chosen signal(s) in **at least one** of:

- **Product Catalog data**
- **Meta Pixel/CAPI event data**
