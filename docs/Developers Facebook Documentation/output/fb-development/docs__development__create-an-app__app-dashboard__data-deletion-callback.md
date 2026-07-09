# Data Deletion Callback - App Development with Meta

_Source: https://developers.facebook.com/docs/development/create-an-app/app-dashboard/data-deletion-callback_

---

# Data Deletion Request Callback

Apps that access user data must provide a way for users to request that their data be deleted. In accordance with Meta’s Platform Terms, all apps must inform users in their privacy policy how to request deletion of their data. Additionally, apps can implement a data deletion request callback, which is outlined in more detail below.

The data deletion callback is called whenever an app user removes your app and requests that you delete their data. Your app users can do this by going to their Facebook profile and clicking the **Send Request** button on the **Settings & Privacy** > **Settings** > **Apps and Websites** page.

This generates a POST with a signed request that is sent to your app. The signed request contains an app-scoped ID identifying the user making the request. For an example of how to parse the request and the structure of the parsed request, see the following section.

In response to the user request, you should acknowledge receiving a user data deletion request through the technical means we provide, and provide a link and a confirmation number. The link and confirmation number must give the user access to a human-readable explanation of the status of their request, including a legitimate justification for any refusal to delete (where legitimate will vary based on jurisdiction and our case-by-case interpretation of our policy as it relates to their stated reasons).

See the **[FAQ](https://developers.facebook.com/docs/development/create-an-app/app-dashboard/data-deletion-callback/#FAQs)** section for answers to frequently asked questions.

## Implementing the Callback

To parse and respond to the request, you should implement a "data deletion request" callback. Your callback must use the secure HTTPS protocol and must be listed in the **Data Deletion Request URL** field in the Settings in the App Dashboard.

The Data Deletion Request callback that you implement must do the following:

- Initiate the deletion of any data your app has from Facebook about the user.
- Return a JSON response that contains a URL where the user can check the status of their deletion request and an alphanumeric confirmation code. The JSON response has the following form:
  `{ url: '<url>', confirmation_code: '<code>' }`

Failure to comply with these requirements may result in your callback being removed or your app being disabled.

You can implement this callback in any language, but the following code is an example of the callback in PHP.

```
<?php
header('Content-Type: application/json');

$signed_request = $_POST['signed_request'];
$data = parse_signed_request($signed_request);
$user_id = $data['user_id'];

// Start data deletion

$status_url = 'https://www.<your_website>.com/deletion?id=abc123'; // URL to track the deletion
$confirmation_code = 'abc123'; // unique code for the deletion request

$data = array(
  'url' => $status_url,
  'confirmation_code' => $confirmation_code
);
echo json_encode($data);

function parse_signed_request($signed_request) {
  list($encoded_sig, $payload) = explode('.', $signed_request, 2);

  $secret = "appsecret"; // Use your app secret here

  // decode the data
  $sig = base64_url_decode($encoded_sig);
  $data = json_decode(base64_url_decode($payload), true);

  // confirm the signature
  $expected_sig = hash_hmac('sha256', $payload, $secret, $raw = true);
  if ($sig !== $expected_sig) {
    error_log('Bad Signed JSON signature!');
    return null;
  }

  return $data;
}

function base64_url_decode($input) {
  return base64_decode(strtr($input, '-_', '+/'));
}
?>
```

This produces a JSON object that looks like this, in which `user_id` is the relevant field for your callback.

```
{
   "algorithm": "HMAC-SHA256",
   "expires": 1291840400,
   "issued_at": 1291836800,
   "user_id": "218471"
}
```

For more information on signed requests, see [Using a Signed Request](https://developers.facebook.com/docs/games/gamesonfacebook/login/#parsingsr) in the [Login for Games on Facebook](https://developers.facebook.com/docs/games/gamesonfacebook/login/) topic.

## Testing Your Callback

To test your callback:

1. Log in to your app with Facebook Login.
2. Go to your Facebook profile's **Apps and Websites** settings tab: <https://www.facebook.com/settings?tab=applications>
3. Remove your app.
4. Click the **View Removed Apps and Websites** link.
5. In the popup, click the **View** button to the right of the application.
6. In the window, appeared click **Send Request** to trigger your callback.

## User Data Deletion Request FAQs

**Q: Why did I receive this notice? Is this email spam?**

A: This is not a spam email. You received this notice because a user of your app requested that their data be deleted. Please take action by promptly deleting all associated user data in your records for the requested ID. User data deletion requests are captured under applicable privacy laws, so Meta expects that you will handle this matter promptly.

**Q: How often can I expect to receive this notice?**

A: Every 21 days, you will receive an alert including the user identifiers you are required to delete (which you can download in your app advanced settings page).

**Q: How do I access the list of IDs that need to be deleted?**

A: You can access these in the advanced settings page of your app dashboard, under “User Data Deletion Requests”.

**Q: These user ids are not present in our records. What do we do?**

A: You can disregard user IDs that do not currently appear in your database.

**Q: Who are the users requesting these deletions?**

A: These users have requested that their data be deleted. You will find current user IDs in the list that you can download from your developer dashboard.

**Q: If I don't delete the data, is my app at risk of deletion or deactivation?**

A: Nonaction will not result in deactivation; however, we do require developers to promptly delete user data upon the request of a user.

**Q: How long do I have before I have to take action?**

A: We ask that you take action in deleting these user IDs promptly.

**Q: Do I have to submit proof of deletion?**

A: No, you do not have to submit proof of deletion.

**Q: What is an app scoped user ID?**

A: An app-scoped user ID (ASID) is a unique ID that Facebook creates for a user when they log into a Facebook app for the first time or with Limited Login. ASIDs are specific to the app and cannot be used by other apps.

**Q: What is a page scoped user ID?**

A: A Page-scoped User ID (PSID) is a unique ID that Facebook assigns to a user when they interact with a Facebook Page through Messenger.

**Q: What is an instant game player ID?**

A: ID issued by the Instant Game SDK for each user as the unique identifier. Note that Instant Game Player ID and ASID are different even for the same user of the same app.

**Q: What should I do if I don’t see user identifiers available to download on the app advanced settings page.**

A: Please ensure you are an admin or developer of the app, and go to the app advanced settings page. Look for the “Download User Identifiers” card, and you should see a list of user identifiers for the last 60 days.

**Q: The file attachment name does not match up with the notification date. What should I do?**

A: Please download and take action on all available files.

**Q: Is implementing the Data Deletion Callback URL still required if the dev is able to point the user to a help page that provides deletion instructions for their account?**

A: Developers need to specify either a data deletion callback instruction URL or a callback URL found in Basic Settings for your app.

**Q: How long do I have to download the file of user IDs before the file expires?**

A: The file will expire in 60 days.
