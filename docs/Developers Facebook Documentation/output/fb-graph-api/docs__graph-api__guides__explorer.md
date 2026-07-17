# Graph Explorer Guide - Graph API

_Source: https://developers.facebook.com/docs/graph-api/guides/explorer_

---

# Graph API Explorer Guide

|  |  |
| --- | --- |
| The Graph API Explorer tool allows you to construct and perform Graph API queries and see their responses for any apps on which you have an admin, developer, or tester role. | [Open the Graph API Explorer tool](https://developers.facebook.com/tools/explorer) |

## Common Uses

- Quickly generate access tokens
- Get code samples for your queries
- Generate debug information to include in support requests
- Test API queries with your production app's settings including permissions, features, and settings for your use cases
- Test API queries with your test or development app using permission and features on test users or test data

## Requirements

- A [Facebook Developer Account](https://developers.facebook.com/apps)
- An app for which you have a role, such as an [admin, developer, or tester role](https://developers.facebook.com/docs/apps#roles)

## Components

### Access Token

When you get an access token, it is displayed in the upper right of the tool. This is the token that is included in your Graph API query. You can copy this token and use it in your app to test your code.

Click the information icon to see information about the current token, including the app that it's tied to, and any permissions that have been granted by the User who is using the app (which is you).

You can generate a new access token if the token has expired or if you add new permissions.

### Meta App

The Meta App dropdown menu in the upper right displays all the apps on which you have an admin, developer, or tester role. Use the dropdown to select the app settings that you wish to test.

### User or Page

The User or Page dropdown menu allows you to get and exchange App, User, and Page access tokens for the currently selected app. You can also use it to uninstall your app from your User node, which destroys the current access token.

### Permissions

The Permission dropdown menu allows you to select permissions, such as `email`, `pages_show_list`, and `ads_management` permissions. This allows the current app user (which is you) to grant the app specific permissions. Only grant permissions that your app actually needs.

If your app is in development, you can grant your app any permission and your queries respect them for data owned by people with a role on your app. If your app is live, however, granting a permission that your app has not been approved for by the [App Review](https://developers.facebook.com/docs/apps/review) process causes your query to fail whenever you submit it.

### Query string Field

When you first enter the tool a default query appears. You can edit the query by typing in a new one, or by searching for and selecting fields in the field viewer after executing the query. You can also use the dropdown menus to switch between operation methods, and target different versions of the Graph API.

If you click the star icon at the end of the query field, the query is saved as a favorite. You can view your favorite queries by clicking the book icon.

### Node Field Viewer

When you submit a `GET` query on a node, the field viewer located in the left side of the window displays the name of the node and the fields returned by the Graph API. You can modify your query by searching for and selecting new fields, clicking the plus icon, and choosing from available fields, or unchecking unnecessary fields. These actions dynamically update your query in the query string field.

### Response Window

The response, located below the query string, shows the results returned from your last submitted query.

### Get Code

If you are happy with your query, click the Get Code button located in the botton center below the response, to generate sample code based on the query. Typically you won't be able to copy and paste the sample code directly in your code base, but it gives you a useful starting point.

### Copy Debug Information

If your query keeps failing and you can't figure out why, and you decide to contact Developer Support, click this button, located at the bottom center, to copy your query and response details to your clipboard. You can submit this information with your support request to help us figure out what's going on.

### Save Session

Click the Save Session button, located at the bottom center, to save the state of your query, with the access token removed. Include the link to this session if you decide to contact Developer Support.

## Sample Query

Try executing the default query that appears when you first load the Graph API Explorer. If you haven't already, [open the Graph API Explorer in a new window](https://developers.facebook.com/tools/explorer), select the app you want to test from the application dropdown menu, and get a User access token.

The default query appears in the query string field:

```
GET https://developers.facebook.com/v25.0/me?fields=id,name
```

The default query is requesting the `id` and `name` fields on the `/me` node, which is a special node that maps to either the `/User` or `/Page` node identified by the token. Since your are using a User access token, this maps to your User node.

The `id` and `name` fields are publicly available and can be returned if the User has granted your app the `default` or `public_profile` permissions. These permissions are pre-approved for all apps (you can confirm this by clicking the information icon in the **Access Token Field**), so you don't have to grant your app any additional permissions for the query to work. Click **Get Access Token** and confirm that you want to grant your app access to your publicly available User information.

Submit your query, and you should see your app-scoped User ID and name appear in the response window.
