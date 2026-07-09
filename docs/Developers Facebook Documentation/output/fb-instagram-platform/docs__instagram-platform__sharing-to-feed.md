# Sharing to Feed - Instagram Platform

_Source: https://developers.facebook.com/docs/instagram-platform/sharing-to-feed_

---

# Sharing to Feed

With Sharing to Feed, you can allow your app's Users to share your content to their Instagram Feed.

![](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/31739640_2065459473743293_5455162868888502272_n.png?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=9vl68lOfX6sQ7kNvwHNo95_&_nc_oc=Adoa1wVA329TwOfkP33jsNhPFMZN-B15jBkOrCJ2NgGX8Sby19tWpB0TPOjW4NpNcPs&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=BCDZevJ5AwgYf-KSihAq9Q&_nc_ss=7b289&oh=00_Af59ZMcGb6kKpzfr3rO630YQghbpTUre3Vrwxyh5AM3VEQ&oe=6A1BDC4F)

## Overview

By using Android **Implicit Intents** and iOS **Universal Links** or **Document Interaction**, your app can pass photos and videos to the Instagram app. The Instagram app will receive this content and load it in the feed composer so the User can publish it to their Instagram Feed.

## Android Developers

Android implementations use implicit intents with the EXTRA\_STREAM extra to prompt the User to select the Instagram app. Once selected, the intent will launch the Instagram app and pass it your content, which the Instagram App will then load in the Feed Composer.

In general, your sharing flow should:

1. Instantiate an implicit intent with the content you want to pass to the Instagram app.
2. Start an activity and check that it can resolve the implicit intent.
3. Resolve the activity if it is able to.

### Shareable Content

You can pass the following content to the Instagram app:

| Content | File Types | Description |
| --- | --- | --- |
| Image asset | JPEG, GIF, or PNG | - |
| File asset | MKV, MP4 | Minimum duration: 3 seconds Maximum duration: 10 minutes Minimum dimentions: 640x640 pixels |

### Sharing an Image Asset

```
String type = "image/*";
String filename = "/myPhoto.jpg";
String mediaPath = Environment.getExternalStorageDirectory() + filename;

createInstagramIntent(type, mediaPath);

private void createInstagramIntent(String type, String mediaPath){

    // Create the new Intent using the 'Send' action.
    Intent share = new Intent(Intent.ACTION_SEND);

    // Set the MIME type
    share.setType(type);

    // Create the URI from the media
    File media = new File(mediaPath);
    Uri uri = Uri.fromFile(media);

    // Add the URI to the Intent.
    share.putExtra(Intent.EXTRA_STREAM, uri);

    // Broadcast the Intent.
    startActivity(Intent.createChooser(share, "Share to"));
}
```

### Sharing a Video Asset

```
String type = "video/*";
String filename = "/myVideo.mp4";
String mediaPath = Environment.getExternalStorageDirectory() + filename;

createInstagramIntent(type, mediaPath);

private void createInstagramIntent(String type, String mediaPath){

    // Create the new Intent using the 'Send' action.
    Intent share = new Intent(Intent.ACTION_SEND);

    // Set the MIME type
    share.setType(type);

    // Create the URI from the media
    File media = new File(mediaPath);
    Uri uri = Uri.fromFile(media);

    // Add the URI to the Intent.
    share.putExtra(Intent.EXTRA_STREAM, uri);

    // Broadcast the Intent.
    startActivity(Intent.createChooser(share, "Share to"));
}
```

## iOS Developers

iOS implementations can use universal links to launch the Instagram app and pass it content, or have it perform a specific action.

### Universal Links

Use the [universal links](https://l.facebook.com/l.php?u=https%3A%2F%2Fdeveloper.apple.com%2Fdocumentation%2Fxcode%2Fallowing-apps-and-websites-to-link-to-your-content&h=AUCq24_vI4UL7r7qGgV2696u_s9SNE3jwAT3eopzRgLtOZp9l9pxJTo72_g3uYPWoLt0aGtEKS1ImBgDhK3jKXJ5Dt7jXd5UQh73_e14vNboLkuuK-2va5ayhYhdMSvUjKRaRQBqsVgYAQ) listed in the following table to perform actions in the Instagram app.

| Universal link | Action |
| --- | --- |
| https://www.instagram.com | Launch the Instagram app. |
| https://www.instagram.com/create/story | Launch the Instagram app with the camera view or photo library on non-camera devices. |
| https://www.instagram.com/p/{media\_id} | Launch the Instagram app and load the post that matches the specified ID value (`int`). |
| https://www.instagram.com/{username} | Launch the Instagram app and load the Instagram user that matches the specified username value (`string`). |
| https://www.instagram.com/explore/locations/{location\_id} | Launch the Instagram app and load the location feed that matches the specified ID value (`int`). |
| https://www.instagram.com/explore/tags/{tag\_name} | Launch the Instagram app and load the page for the hashtag that matches the specified name value (`string`). |

### Sample Objective-C Code

The following example in Objective-C launches the Instagram app with the camera view.

```
NSURL *instagramURL = [NSURL URLWithString:@"https://www.instagram.com/create/story"];
if ([[UIApplication sharedApplication] canOpenURL:instagramURL]) {
    [[UIApplication sharedApplication] openURL:instagramURL];
}
```

### Document Interaction

If your application creates photos and you'd like your users to share these photos using Instagram, you can use the [Document Interaction API](https://l.facebook.com/l.php?u=https%3A%2F%2Fdeveloper.apple.com%2Flibrary%2Fcontent%2Fdocumentation%2FFileManagement%2FConceptual%2FDocumentInteraction_TopicsForIOS%2FIntroduction%2FIntroduction.html&h=AUAmOPY9cUDkD5JdMbG0sIUImvQv89JeuKB3AmNlu3LwzqrIWh_m-D9x3MWSJTMXRaITQKwVGpDdlHM7za26jlgcPeJYvY_4YDkpoSJRl8X_Uw__a3jxff0thlO5JtFR1d39zeH8n0nQjg) to open your photo in Instagram's sharing flow.

You must first save your file in PNG or JPEG (preferred) format and use the filename extension `.ig`. Using the iOS Document Interaction APIs you can trigger the photo to be opened by Instagram. The Identifier for our Document Interaction UTI is `com.instagram.photo`, and it conforms to the *public/jpeg* and *public/png* UTIs. See the Apple documentation articles: [Previewing and Opening Files](https://l.facebook.com/l.php?u=https%3A%2F%2Fdeveloper.apple.com%2Flibrary%2Fcontent%2Fdocumentation%2FFileManagement%2FConceptual%2FDocumentInteraction_TopicsForIOS%2FArticles%2FPreviewingandOpeningItems.html%23%2F%2Fapple_ref%2Fdoc%2Fuid%2FTP40010410-SW1&h=AUCYfOlD1loJ7A0FP65xYGRpMYJxUvNu0Orj0ZkVj3IJaE6BvV4Nq-6IpjRVi0k2yE9FTNN2qdI77Up3ATVzQapU9XOmfLlf4leRZYN3PpkNWKYA5jq0Dy1KB7Utd93G6MVRY3o1aDwPRA) and the [UIDocumentInteractionController Class Reference](https://l.facebook.com/l.php?u=https%3A%2F%2Fdeveloper.apple.com%2Flibrary%2Fcontent%2F%23documentation%2FUIKit%2FReference%2FUIDocumentInteractionController_class%2FReference%2FReference.html&h=AUCizd6Hjnbcjj7LqdOqR3EQggJDWSjWAcHSSHoN0IRXXci1CxCALhtTJzJzsdeFI2nRUEsqVoj0qghHr6a0Iof5mDsbqElKtoDViqC5AzAR7D4I0eOEQazyCLfTghSsX7qRRBj1Zwox-A) for more information.

Alternatively, if you want to show **only** Instagram in the application list (instead of Instagram plus any other *public/jpeg*-conforming apps) you can specify the extension class `igo`, which is of type `com.instagram.exclusivegram`.

When triggered, Instagram will immediately present the user with our filter screen. The image is preloaded and sized appropriately for Instagram. For best results, Instagram prefers opening a JPEG that is 640px by 640px square. If the image is larger, it will be resized dynamically.
