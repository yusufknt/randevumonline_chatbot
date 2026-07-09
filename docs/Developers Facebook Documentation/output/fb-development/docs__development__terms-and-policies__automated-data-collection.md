# Automated Data Collection - App Development with Meta

_Source: https://developers.facebook.com/docs/development/terms-and-policies/automated-data-collection_

---

# Automated Data Collection

## Abide by our Policies and Terms of Service by accessing data only through the Platform APIs

Facebook offers Platform APIs to allow developers to retrieve data from Facebook and develop functionality, while respecting users’ privacy. For most Platform APIs, developers must register with Facebook following [our guidelines](https://developers.facebook.com/docs/development/register) in order to have programmatic access to data through the APIs made available.

Platform APIs are the only allowable means to access data programmatically, unless you have our prior written permission. Using other tools and techniques to circumvent the protections we’ve placed on Platform Data constitutes a violation of Facebook’s [Terms of Service](https://www.facebook.com/terms.php) and does not align with users’ privacy expectations.

When creating your Platform integration, you’ve agreed to Facebook’s Terms of Service. One of these terms is: “You may not access or collect data from our Products using automated means (without our prior permission) or attempt to access data you do not have permission to access, regardless of whether such automated access or collection is undertaken while logged-in to a Facebook account.” [(Terms of Service 3.2.3)](https://www.facebook.com/terms.php).

It’s important to note that these terms still apply even if the conduct is not intentional or if you’re unsuccessful in your attempts to collect data.

We’ve developed the following resources to help you identify disallowed traffic and remove it from your code.

## How do I know if I'm making requests that are disallowed by Facebook?

If you are accessing any data on Facebook in a way that does not follow the instructions in the [Developer Documentation](https://developers.facebook.com/docs/), those requests likely violate Facebook policies. Here are some practical steps to identify potentially unauthorized behavior:

1. Allowable requests can only be directed to graph.facebook.com. Making requests outside of graph.facebook.com constitutes a violation. Please review each instance in your code where data requests fall outside of Platform API endpoints and make necessary adjustments. For example, you can search your code for instances of facebook.com, mobile.facebook.com, instagram.com or Facebook’s graphql.
2. Review your logs for 4xx or 3xx response codes. Receiving redirect or client error responses could indicate that you are making requests outside of our allowable APIs.
3. Make sure that the data you’re trying to access has been explicitly made available by Facebook through Platform APIs. Attempting to access data that has not been made available through these APIs constitutes a violation of our terms and policies. Please review the [Developer Documentation](https://developers.facebook.com/docs/) to understand what data points can be accessed and what permissions are required.
4. Make sure that your application has obtained appropriate permissions for the data it is requesting. A number of data points are only available after submitting for App Review. The permissions required to access data points that are not provided by default should be requested through the [App Dashboard](https://developers.facebook.com/apps/). You can learn more about permissions in the [Permissions Reference](https://developers.facebook.com/docs/permissions/reference) documentation.
5. The use of scripts, HTTP libraries, javascript or other executable code to automate actions or perform requests of Facebook data outside of the Platform APIs is not allowed. Make sure that you are not taking actions to facilitate the automated access of Platform Data, even if such technology is publicly available.

## More information and ways to contact us

View our public documentation for the most updated information:

- [Facebook Login](https://developers.facebook.com/docs/facebook-login/)
- [Instagram Platform](https://developers.facebook.com/docs/instagram/)
- [Business Developer Platform](https://developers.facebook.com/docs/business-developer-platform/)
- [Groups API](https://developers.facebook.com/docs/groups-api/)
- [Marketing API](https://developers.facebook.com/docs/marketing-apis/)
- [Pages API](https://developers.facebook.com/docs/pages/)

Visit our [Developer Support](https://developers.facebook.com/support) page for additional information or to contact us.
Additional details regarding available APIs can be found in the [Developer Documentation](https://developers.facebook.com/docs/).
