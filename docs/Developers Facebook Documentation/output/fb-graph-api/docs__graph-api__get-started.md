# Get Started - Graph API

_Source: https://developers.facebook.com/docs/graph-api/get-started_

---

# Get Started

This guide explains how to get started with receiving data from the Facebook Social Graph.

## Before You Start

You will need:

- [Register as a Meta Developer](https://developers.facebook.com/docs/development/register)
- A [Meta App](https://developers.facebook.com/docs/development/create-an-app) – This app will be for testing so there is no need to involve your app code when creating this Meta App.
- The [Graph API Explorer tool](https://developers.facebook.com/tools/explorer) open in a separate browser window
- A brief understanding of the structure of the Meta's social graph from our [Graph API Overview](https://developers.facebook.com/docs/graph-api/overview#nodes) guide

## Your First Request

### Step 1: Open the Graph API Explorer tool

[Open the Graph API Explorer in a new browser window.](https://developers.facebook.com/tools/explorer) This allows you to execute the examples as you read this tutorial.

The explorer loads with a default query with the `GET` method, the lastest version of the Graph API, the `/me` node and the `id` and `name` fields in the [Query String Field](https://developers.facebook.com/docs/graph-api/guides/explorer#query-string-field), and your Facebook App.

![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/232068365_563091814813799_6070357364579520404_n.png?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=4X9js7M_MgYQ7kNvwExG2uJ&_nc_oc=AdpJ3siEyzb3VoY7hfiSgeccgWAlbbwhNrj7jfmzIWr_lvJOEnHud5XlVU5gE60KEOA&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=CDR8kzpG3fkJ8n7hwoaTPA&_nc_ss=7b289&oh=00_Af5aLx47yg0c-UR3aAryJH7UUXG9HpMwCSbFHsV04-F9Mg&oe=6A1821A4)

### Step 2. Generate an Access Token

Click the **Generate Access Token** button. A **Log in With Facebook** window will pop up. This popup is your app asking for your permission to get your name and profile picture from Facebook.

|  |  |
| --- | --- |
| This flow is our [Facebook Login](https://developers.facebook.com/docs/facebook-login) product that allows a person to log into an app using their Facebook credentials. Facebook Login allows an app to ask a person to access the person's Facebook data, and for the person to accept or decline access. Your name and profile picture are public, to allow people to find you on Facebook, so no additional requirements are needed to run this request.  Click **Continue as...**  A User Access Token is created. This token contains information such as the app making the request, the person using the app to make a request, if the access token is still valid (it expires in about an hour), the expiration time, and the scope of data the app can request. In this request the scope is `public_profile` which includes your name and profile picture. |  |

|  |  |
| --- | --- |
|  | Click the information circle icon next to the acces token to view the token's information. |

### Step 3. Submit the Request

Click the **Submit** button in the upper right corner.

#### What You Should See

In the [Response Window](https://developers.facebook.com/docs/graph-api/guides/explorer#response-window), you will see a JSON response with your Facebook User ID and your name.

![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/232902382_904467853476103_7217229934737479641_n.png?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=aXZpdZQv650Q7kNvwGuVeF_&_nc_oc=AdrAT3Jlz60wXFXqAGIZy1bOf5br5qj90KH1y7z9a9lTsix1Qs7RwtgzZ8MsVk7H2OA&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=CDR8kzpG3fkJ8n7hwoaTPA&_nc_ss=7b289&oh=00_Af5qx400aXE5IcPTyXu7RlvtHez7JTVpb2bTmJEd60z-xw&oe=6A17FE23)

If you remove `?fields=id,name` from the query string field and click **Submit**, you will see the same result since `name` and `id` are the User node fields returned by default.

## Your Second Request

### Step 1. Let's Add a Field

Let's make the First Request a little more complex by adding another field, `email`. There are two ways to add fields:

- Click the search dropdown menu in the [Node Field Viewer](https://developers.facebook.com/docs/graph-api/guides/explorer#node-field-viewer) to the left of the response window
- Start typing in the query string field.

Let's add the `email` field and click **Submit**.

#### What You Should See

While the call did not fail, only the `name` and `id` fields were returned along with a debug message. Click the (Show) link to debug the request.

![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/233410295_959323958245691_7180707304587023135_n.png?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=ftbr5aQ54QUQ7kNvwH0XIof&_nc_oc=AdoaLMP9FYEBggBQviZH6l9ZxPDRfS6kMJ47yF7M_ZM02dHphyebcMxiI_TjOLDW7kw&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=CDR8kzpG3fkJ8n7hwoaTPA&_nc_ss=7b289&oh=00_Af7-qRmWCQGX4c0MBf4gA-VpzxUWUEGG5_XIviYMu60Osg&oe=6A17FC16)

Almost all nodes and fields need a specific permission to access them. The debug message is telling you that you need to give your app permission to access the email address that you have associated with your Facebook account.

### Step 2. Add a Permission

|  |  |
| --- | --- |
| In the right side panel, under **Permissions**, click the **Add a Permission** dropdown menu. Click **User Data Permissions** and select **email**. Generate A New User Access Token   Because you are changing the scope of the access token, you need to create a new one. Click **Generate Access Token**. Just like your first request, you must give your app permission to access your email in the Facebook Login dialog.  Once the new token has been created, click **Submit**. Now all fields in your request will be returned. |  |

Try getting your Facebook posts.

[See the steps.](#)

#### Links in the Response

Notice that `id` values returned in the response window are links. These links can represent nodes, such as User, Page, or Post. If you click on a link, the ID will replace the contents of the query string field. Now you can run requests on that node. Because this node is connected to the parent node, a Post of a User, you may not need to add permissions. You can click on a Post ID now since we will be using it in the next example.

Notice: Some IDs are a combination of the parent ID and a new ID string. For example, a User's Post will have a Post ID that looks something like this: `1028223264288_102224043055529` where `1028223264288` is the User ID.

## Let's Look at an Edge

The User node does not have many edges that can return data. Access to User objects can only be given by the User who owns the object. In most cases, a User owns an object if they created it.

For example, if you publish a post you can see information about the post such as when it was created, text, photos, and links shared in the post, and the number of reactions the post received. If you comment on your post, you will be able to get that comment, but if another person publishes a comment on your post, you will not be able to see the comment or who published it.

Try getting the number of reactions for one of your posts. You will want to take a look at the

[Object Reactions reference.](https://developers.facebook.com/docs/graph-api/reference/v13.0/object/reactions)

[See the steps.](#)

## Get the Code for your Request

The explorer tool lets you test requests and once you have a successful response, you can get the code to insert into your app code. At the bottom of the response window, click **Get Code**. The explorer offers Android, iOS, JavaScript, PHP, and cURL code. The code is pre-selected so you can just copy and paste.

![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/231948896_1065545040645743_5920314088559660186_n.png?_nc_cat=101&ccb=1-7&_nc_sid=e280be&_nc_ohc=Lh1ncPDykVUQ7kNvwHnrr8u&_nc_oc=Adr6nd16WwF7tFP-e03_2L6c4Bzf6CKXVayIexUJ2WShtZbs5PEyp5DonI4DTABZ6Tw&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=CDR8kzpG3fkJ8n7hwoaTPA&_nc_ss=7b289&oh=00_Af4bSAw4xQp-lFmLTl39wIdj41MAuTyElg4ce0vQFTGUfA&oe=6A18222C)

We recommend that you implement the Facebook SDK for your app. This SDK will include Facebook Login which allows your app to ask for permissions and get access tokens.

## Learn More

You can use the Graph API Explorer to test any request for Users, Pages, Groups, and more. Visit the [reference](https://developers.facebook.com/docs/graph-api/reference) for each node or edge to determine the permission and access token type required.

|  |  |
| --- | --- |
| - [Access Token](https://developers.facebook.com/docs/facebook-login/access-tokens) - [Facebook Login](https://developers.facebook.com/docs/facebook-login) - [Facebook SDKs](https://developers.facebook.com/docs#apis-and-sdks) | - [Graph API References](https://developers.facebook.com/docs/graph-api/reference) - [Graph API Explorer Guide](https://developers.facebook.com/docs/graph-api/guides/explorer) - [Login Security](https://developers.facebook.com/docs/facebook-login/security) - [Permissions Reference](https://developers.facebook.com/docs/permissions/reference) |
