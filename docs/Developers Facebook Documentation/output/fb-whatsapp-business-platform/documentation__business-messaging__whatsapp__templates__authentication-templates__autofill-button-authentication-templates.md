# One-tap autofill authentication templates | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/authentication-templates/autofill-button-authentication-templates_

---

# One-tap autofill authentication templates

Updated: Feb 6, 2026

**Deprecation extension announcement:** We will extend the migration deadline until October 15, 2026. On this date, the `PendingIntent`-based handshake method for authentication templates will be deprecated. If you are currently using `PendingIntent` to initiate handshakes or verify app identity, the [OTP Android SDK](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/authentication-templates/zero-tap-authentication-templates#using-the-sdk) is the preferred way to migrate.

One-tap autofill authentication templates allow you to send a one-time password or code along with an one-tap autofill button to your users. When a WhatsApp user taps the autofill button, the WhatsApp client triggers an activity which opens your app and delivers it the password or code.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/544891318_1193716362844107_2249981522588832509_n.png?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=6frwoFG8zmAQ7kNvwFPxMgY&_nc_oc=Ado3WJ6CX_uwn2KVQ-9-bcCoOKQWtNF1ceoyUbnaNRFf1aMyzIhDeZ9ZUOOTzmK0bnc&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=rKcL8grRZ-maJYhEgFua1g&_nc_ss=7b20f&oh=00_Af6bqZicSjts8ACyUAd74NkeNC_5MRGftWUJwfO5DWDd9w&oe=6A1C0CC1)

One-tap autofill button authentication templates consist of:

- Preset text: *<VERIFICATION_CODE> is your verification code.*
- An optional security disclaimer: *For your security, do not share this code.*
- An optional expiration warning (optional): *This code expires in <NUM_MINUTES> minutes.*
- A one-tap autofill button.

**Note**: The OTP Android SDK features a simplified workflow for implementing one-tap and zero-tap authentication templates. You can learn how to use it below.

## Limitations

One-tap autofill buttons are only supported on Android. If you send an authentication template to a WhatsApp user who is using a non-Android device, the WhatsApp client will display a copy code button instead.

URLs, media, and emojis are not supported.

## Creating authentication templates

Use the [Message Templates API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/template-api#post-version-waba-id-message-templates) to create authentication templates.

### Request syntax

```json
curl 'https://graph.facebook.com/v25.0/<WHATSAPP_BUSINESS_ACCOUNT_ID>/message_templates' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d
'{
  "name": "<TEMPLATE_NAME>",
  "language": "<TEMPLATE_LANGUAGE>",
  "category": "authentication",
  "message_send_ttl_seconds": <TIME_T0_LIVE>, // Optional
  "components": [
    {
      "type": "body",
      "add_security_recommendation": <SECURITY_RECOMMENDATION> // Optional
    },
    {
      "type": "footer",
      "code_expiration_minutes": <CODE_EXPIRATION> // Optional
    },
    {
      "type": "buttons",
      "buttons": [
        {
          "type": "otp",
          "otp_type": "one_tap",
          "text": "<COPY_CODE_BUTTON_TEXT>",  // Optional
          "autofill_text": "<AUTOFILL_BUTTON_TEXT>", // Optional
          "supported_apps": [
            {
              "package_name": "<PACKAGE_NAME>",
              "signature_hash": "<SIGNATURE_HASH>"
            }
          ]
        }
      ]
    }
  ]
}'
```

Note that in your template creation request the button type is designated as `otp`, but upon creation the button type will be set to `url`. You can confirm this by performing a GET request on a newly created authentication template and analyzing its components.

### Request parameters

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<AUTOFILL_BUTTON_TEXT>`<br>*String* | **Optional.**<br>One-tap autofill button label text.<br>If omitted, the autofill text will default to a pre-set value, localized to the template’s language. For example, `Autofill` for English (US).<br>Maximum 25 characters. | `Autofill` |
| `<CODE_EXPIRATION>`<br>*Integer* | **Optional.**<br>Indicates the number of minutes the password or code is valid.<br>If included, the code expiration warning and this value will be displayed in the delivered message. The button will be disabled in the delivered message the indicated number of minutes from when the message was sent.<br>If omitted, the code expiration warning will not be displayed in the delivered message. In addition, the button will be disabled 10 minutes from when the message was sent.<br>Minimum 1, maximum 90. | `5` |
| `<COPY_CODE_BUTTON_TEXT>`<br>*String* | **Optional.**<br>Copy code button label text.<br>If omitted, the text will default to a pre-set value localized to the template’s language. For example, `Copy Code` for English (US).<br>If included, the authentication template message will display a copy code button with this text if the message fails the [eligibility check](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/authentication-templates/autofill-button-authentication-templates#eligibility-check).<br>Maximum 25 characters. | `Copy Code` |
| `<PACKAGE_NAME>`<br>*String* | **Required.**<br>Your Android app’s package name.<br>The string must have at least two segments (one or more dots), and each segment must start with a letter.<br>All characters must be alphanumeric or an underscore [`a-zA-Z0-9_`].<br>If using Graph API version 20.0 or older, you can define your app’s package name outside of the `supported_apps` array, but this is not recommended. See [Supported Apps](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/authentication-templates/autofill-button-authentication-templates#supported-apps) below.<br>Maximum 224 characters. | `com.example.luckyshrub` |
| `<SECURITY_RECOMMENDATION>`<br>*Boolean* | **Optional.**<br>Set to `true` if you want the template to include the string, *For your security, do not share this code.* Set to `false` to exclude the string. | `true` |
| `<SIGNATURE_HASH>`<br>*String* | **Required.**<br>Your app signing key hash. See [App Signing Key Hash](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/authentication-templates/autofill-button-authentication-templates#app-signing-key-hash) below.<br>All characters must be either alphanumeric, `+`, `/`, or `=` (`a-zA-Z0-9+/=`).<br>If using Graph API version 20.0 or older, you can define your app’s signature hash outside of the `supported_apps` array, but this is not recommended. See [Supported Apps](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/authentication-templates/autofill-button-authentication-templates#supported-apps) below.<br>Must be exactly 11 characters. | `K8a/AINcGX7` |
| `<TEMPLATE_LANGUAGE>`<br>*String* | **Required.**<br>Template [language and locale code](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/supported-languages). | `en_US` |
| `<TEMPLATE_NAME>`<br>*String* | **Required.**<br>Template name.<br>Maximum 512 characters. | `verification_code` |
| `<TIME_TO_LIVE>`<br>*Integer* | **Optional.**<br>Authentication message time-to-live value, in seconds. See [Customizing Time-To-Live](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview#customizing-time-to-live). | `60` |

### Example request

This example creates a template named “authentication_code_autofill_button” categorized as `authentication` with all optional text strings enabled and a one-tap autofill button.

```json
curl 'https://graph.facebook.com/v25.0/102290129340398/message_templates' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "name": "authentication_code_autofill_button",
  "language": "en_US",
  "category": "authentication",
  "message_send_ttl_seconds": 60,
  "components": [
    {
      "type": "body",
      "add_security_recommendation": true
    },
    {
      "type": "footer",
      "code_expiration_minutes": 10
    },
    {
      "type": "buttons",
      "buttons": [
        {
          "type": "otp",
          "otp_type": "one_tap",
          "text": "Copy Code",
          "autofill_text": "Autofill",
          "package_name": "com.example.luckyshrub",
          "signature_hash": "K8a/AINcGX7"
        }
      ]
    }
  ]
}'
```

### Example response

```json
{
  "id": "594425479261596",
  "status": "PENDING",
  "category": "AUTHENTICATION"
}
```

## Webhooks

The [button messages webhook](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/button) is triggered whenever a user taps the “I didn’t request a code” button within the message.

### Example webhook

```html
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "320580347795883",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "metadata": {
              "display_phone_number": "12345678",
              "phone_number_id": "1234567890"
            },
            "contacts": [
              {
                "profile": {
                  "name": "John"
                },
                "wa_id": "12345678"
              }
            ],
            "messages": [
              {
                "context": {
                  "from": "12345678",
                  "id": "wamid.HBgLMTIxMTU1NTE0NTYVAgARGBJDMDEyMTFDNTE5NkFCOUU3QTEA"
                },
                "from": "12345678",
                "id": "wamid.HBgLMTIxMTU1NTE0NTYVAgASGCBBQ0I3MjdCNUUzMTE0QjhFQkM4RkQ4MEU3QkE0MUNEMgA=",
                "timestamp": "1753919111",
                "from_logical_id": "131063108133020",
                "type": "button",
                "button": {
                  "payload": "DID_NOT_REQUEST_CODE",
                  "text": "I didn't request a code"
                }
              }
            ]
          },
          "field": "messages"
        }
      ]
    }
  ]
}
```

## App signing key hash

You must include your app signing key hash in your post body.

To calculate your hash, follow Google’s instructions for [computing your app’s hash string](https://developers.google.com/identity/sms-retriever/verify#computing_your_apps_hash_string).

Alternatively, if you follow Google’s instructions and download your app signing key certificate (step 1), you can use your certificate with the [sms_retriever_hash_v9.sh](http://tinyurl.com/43bkdrdt) shell script to compute the hash. For example:

```sh
./sms_retriever_hash_v9.sh --package "com.example.myapplication" --keystore ~/.android/debug.keystore
```

## Supported apps

The `supported_apps` array allows you define pairs of app package names and signing key hashes for up to 5 apps. This can be useful if you have different app builds and want each of them to be able to initiate the handshake:

```json
"buttons": [
  {
    "type": "otp",
    ...
    "supported_apps": [
      {
        "package_name": "<PACKAGE_NAME_1>",
        "signature_hash": "<SIGNATURE_HASH_1>"
      },
      {
        "package_name": "<PACKAGE_NAME_2>",
        "signature_hash": "<SIGNATURE_HASH_2>"
      },
      ...
    ]
  }
]
```

Alternatively, if you are using Graph API version 20.0 or older and have only a single app, you can define the app’s package name and signing key hash as `buttons` object properties, but this is not recommended as we will stop supporting this method starting with version 21.0:

```json
"buttons": [
  {
    "type": "otp",
    ...
    "package_name": "<PACKAGE_NAME>",
    "signature_hash": "<SIGNATURE_HASH>"
  }
]
```

## Handshake

You must signal to the WhatsApp client to expect imminent delivery of a password or code. You can do this by initiating a “handshake”.

A handshake is an Android intent and public class that you implement but that the WhatsApp client can start.

When a user in your app requests a one-time password or verification code and chooses for it to be delivered to their WhatsApp number, first perform the handshake, then call our API to send the authentication template message. When the WhatsApp client receives the message, it will perform an eligibility check, and if there are no errors, start the intent and display the message to the user. Finally, when the user taps the message’s one-tap autofill button, we automatically load your app and pass it the password or code.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/335941006_3334832200114460_5878835743521475587_n.png?_nc_cat=101&ccb=1-7&_nc_sid=e280be&_nc_ohc=v_C0f0-lWsYQ7kNvwFQG6vp&_nc_oc=Adr8YgzZL-JClXzybzl85cggDMMzvO6MItpodaerEbP1r4h4ey2dpqBOVFpc3fhOv60&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=rKcL8grRZ-maJYhEgFua1g&_nc_ss=7b20f&oh=00_Af5JCm4e583k-OFM_RjtB3VAVYASYRcYOsikUU8IpWu0aQ&oe=6A1C2B6C)

If you do not perform a handshake before sending the message, or the message fails an eligibility check, the delivered message will display a copy code button instead of a one-tap button.

### Eligibility check

The WhatsApp client performs the following checks when it receives an authentication template message. If any check fails, the one-tap autofill button will be replaced with a copy code button.

- The handshake was initiated no more than 10 minutes ago (or no more than the number of minutes indicated by the template’s `code_expiration_minutes` property, if present).
- The package name in the message (defined in the `package_name` property in the `components` array upon template creation) matches the package name set on the intent. The match is determined through the `getCreatorPackage` method called in the `PendingIntent` object provided by your application.
- None of the other apps that you included in the template’s list of `supported_apps` initiated a handshake in the last 10 minutes (or the number of minutes indicated by the template’s `code_expiration_minutes` property, if present).
- The app signing key hash in the message (defined in the `signature_hash` property in the components array upon template creation) matches your installed app’s signing key hash.
- The message includes the one-tap autofill button text.
- Your app has defined an activity to receive the password or code.

### Android notifications

Android notifications indicating receipt of a WhatsApp authentication template message will only appear on the user’s Android device if:

- The user is logged into the WhatsApp app or WhatsApp Business app with the phone number (account) that the message was sent to.
- The user is logged into your app.
- Android OS is KitKat (4.4, API 19) or above.
- **Show notifications** is enabled ( **Settings** > **Notifications** ) in the WhatsApp app or WhatsApp Business app.
- Device level notification is enabled for the WhatsApp app or WhatsApp Business app.
- Prior message threads in the WhatsApp app or WhatsApp Business app between the user and your business are not muted.

### Using the SDK

The OTP Android SDK can be used to perform handshakes, as well as other functions in both one-tap and zero-tap authentication templates.

To access SDK functionality, add the following configuration to your Gradle file:

```java
dependencies {
…
    implementation 'com.whatsapp.otp:whatsapp-otp-android-sdk:1.0.0'
…
}
```

To your repositories, add `mavenCentral()`:

```java
repositories {
…
    mavenCentral()
…
}
```

### Activity

Declare an activity and intent filter that can receive the one-time password or code. The intent filter must have the action name `com.whatsapp.otp.OTP_RETRIEVED`.

```java
<activity
   android:name=".ReceiveCodeActivity"
   android:enabled="true"
   android:exported="true"
   android:launchMode="standard">
   <intent-filter>
       <action android:name="com.whatsapp.otp.OTP_RETRIEVED" />
   </intent-filter>
</activity>
```

This is the activity that the WhatsApp app or WhatsApp Business app will start once the authentication template message is received and it passes all [eligibility checks](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/authentication-templates/autofill-button-authentication-templates#eligibility-check).

### Activity class

Using the SDK (Preferred)

Define the activity public class and instantiate a `WhatsAppOtpIncomingIntentHandler` object to handle the intent. The `.processOtpCode()` method validates the handshake ID against the expected value you stored during handshake initiation and handles errors.

```java
public class ReceiveCodeActivity extends AppCompatActivity {

      @Override
      protected void onCreate(Bundle savedInstanceState) {
          super.onCreate(savedInstanceState);
          WhatsAppOtpIncomingIntentHandler incomingIntentHandler = new WhatsAppOtpIncomingIntentHandler();

          // Retrieve the expected handshake ID that was stored during handshake initiation
          String expectedHandshakeId = retrieveStoredHandshakeId();

          incomingIntentHandler.processOtpCode(
                                 getIntent(),
                                 expectedHandshakeId,
                                 (code) -> {
                                   // The handshake ID has been validated by the SDK
                                   validateCode(code);
                                 },
                                 // call your function to handle errors
                                 (error, exception) -> handleError(error, exception));
    }
```

Without the SDK

Define the activity public class that can accept the code once it has been passed to your app. The activity should validate the `request_id` (handshake ID) to ensure the OTP code is coming from a legitimate handshake initiated by your app.

```java
public class ReceiveCodeActivity extends AppCompatActivity {

   @Override
   protected void onCreate(Bundle savedInstanceState) {
       super.onCreate(savedInstanceState);
       Intent intent = getIntent();

       // Extract the handshake ID from the intent
       String incomingRequestId = intent.getStringExtra("request_id");

       // Retrieve the previously stored handshake ID
       String storedRequestId = retrieveStoredRequestId();

       // Validate the handshake ID matches
       if (storedRequestId != null && storedRequestId.equals(incomingRequestId)) {
         // use OTP code
         String otpCode = intent.getStringExtra("code");
         // ...
       }
   }
}
```

### Initiating the handshake

Using the SDK (Preferred)

Performing a handshake can be done by instantiating the `WhatsAppOtpHandler` object and passing in your context to the `.sendOtpIntentToWhatsApp()` method. The method returns a UUID (handshake ID) that must be stored and used to validate the incoming OTP code later:

```java
WhatsAppOtpHandler whatsAppOtpHandler = new WhatsAppOtpHandler();
UUID handshakeId = whatsAppOtpHandler.sendOtpIntentToWhatsApp(context);
// Store handshakeId to validate the received OTP code later
```

Without the SDK

This example demonstrates one way to initiate a handshake with the WhatsApp client. The handshake includes a `request_id` (UUID) that must be stored and validated when receiving the OTP code.

```java
private String currentRequestId;

public void sendOtpIntentToWhatsApp() {
   // Generate a unique handshake ID
   currentRequestId = UUID.randomUUID().toString();
   // Store this ID for later validation when receiving the OTP
   storeRequestId(currentRequestId);

   // Send OTP_REQUESTED intent to both WA and WA Business App
   sendOtpIntentToWhatsApp("com.whatsapp", currentRequestId);
   sendOtpIntentToWhatsApp("com.whatsapp.w4b", currentRequestId);
}

private void sendOtpIntentToWhatsApp(String packageName, String requestId) {

  /**
  * Starting with Build.VERSION_CODES.S, it will be required to explicitly
  * specify the mutability of  PendingIntents on creation with either
  * (@link #FLAG_IMMUTABLE} or FLAG_MUTABLE
  */
  int flags = Build.VERSION.SDK_INT >= Build.VERSION_CODES.S ? FLAG_IMMUTABLE : 0;
  PendingIntent pi = PendingIntent.getActivity(
      getApplicationContext(),
      0,
      new Intent(),
      flags);

  // Send OTP_REQUESTED intent to WhatsApp
  Intent intentToWhatsApp = new Intent();
  intentToWhatsApp.setPackage(packageName);
  intentToWhatsApp.setAction("com.whatsapp.otp.OTP_REQUESTED");
  // WA will use this to verify the identity of the caller app.
  Bundle extras = intentToWhatsApp.getExtras();
  if (extras == null) {
     extras = new Bundle();
  }
  extras.putParcelable("_ci_", pi);
  // Add the handshake ID for secure validation
  intentToWhatsApp.putExtra("request_id", requestId);
  intentToWhatsApp.putExtras(extras);
  getApplicationContext().sendBroadcast(intentToWhatsApp);
}
```

### Checking if WhatsApp is installed on Android

You can check WhatsApp installation before offering WhatsApp as an option if you expect both WhatsApp and your app to be on the same device.

First, you need to add the following to your `AndroidManifest.xml` file:

```xml
<queries>
    <package android:name="com.whatsapp"/>
    <package android:name="com.whatsapp.w4b"/>
</queries>
```

Using the SDK (Preferred)

Instantiate the `WhatsAppOtpHandler` object:

```java
WhatsAppOtpHandler whatsAppOtpHandler = new WhatsAppOtpHandler();
```

Check if the WhatsApp client is installed by passing the `isWhatsAppInstalled` method as the clause in an `If` statement:

```java
If (whatsAppOtpHandler.isWhatsAppInstalled(context)) {
    // ... do something
}
```

Without the SDK

```java
if (this.isWhatsAppInstalled(context)) {
    // ... do something
}

public boolean isWhatsAppInstalled(final @NonNull Context context){
    return isWhatsAppInstalled(context, "com.whatsapp") ||
           isWhatsAppInstalled(context, "com.whatsapp.w4b");
  }

  public boolean isWhatsAppInstalled(final @NonNull Context context,
      final @NonNull String type){
    final Intent intent = new Intent();
    intent.setPackage(type);
    intent.setAction("com.whatsapp.otp.OTP_REQUESTED");
    PackageManager packageManager = context.getPackageManager();
    List<ResolveInfo> receivers = packageManager.queryBroadcastReceivers(intent, 0);
    return !receivers.isEmpty();
  }
}
```

### Checking if WhatsApp is installed on iOS

Use the following code in your iOS application to check if WhatsApp is installed

```swift
let schemeURL = URL(string: "whatsapp://otp")!
let isWhatsAppInstalled = UIApplication.shared.canOpenURL(schemeURL)
```

### Error signals

See [Error Signals](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/authentication-templates/error-signals) that can help with debugging.

### Handshake ID error codes

The following error codes may be returned when using the SDK with handshake ID validation:

| Error Code | Description |
| --- | --- |
| `HANDSHAKE_ID_MISSING` | The handshake ID was not included in the intent from WhatsApp |
| `HANDSHAKE_ID_INVALID_FORMAT` | The handshake ID is not a valid UUID format |
| `HANDSHAKE_ID_MISMATCH` | The handshake ID in the intent does not match the expected value |

### Sample app

See our [WhatsApp One-Time Password (OTP) Sample App](https://github.com/WhatsApp/WhatsApp-OTP-Sample-App) for Android on Github. The sample app demonstrates how to send and receive OTP passwords and codes via the API, how to integrate the one-tap autofill and copy code buttons, how to create a template, and how to spin up a sample server.

## Sending authentication template

This document explains how to send approved [authentication templates with one-time password buttons](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/authentication-templates/authentication-templates).

Note that **you must first initiate a handshake** between your app and the WhatsApp client. See [Handshake](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/authentication-templates/autofill-button-authentication-templates#handshake) above.

### Request

Use the [Messages API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api#post-version-phone-number-id-messages) to send an [authentication template message with a one-time password button](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/authentication-templates/authentication-templates).

### Request syntax

```json
curl -X POST "https://graph.facebook.com/v23.0/<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>/messages" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "messaging_product": "whatsapp",
    "recipient_type": "individual",
    "to": "<CUSTOMER_PHONE_NUMBER>",
    "type": "template",
    "template": {
      "name": "<TEMPLATE_NAME>",
      "language": {
        "code": "<TEMPLATE_LANGUAGE_CODE>"
      },
      "components": [
        {
          "type": "body",
          "parameters": [
            {
              "type": "text",
              "text": "<ONE-TIME PASSWORD>"
            }
          ]
        },
        {
          "type": "button",
          "sub_type": "url",
          "index": 0,
          "parameters": [
            {
              "type": "text",
              "text": "<ONE-TIME PASSWORD>"
            }
          ]
        }
      ]
    }
  }'
```

### Request parameters

| Placeholder | Description | Sample Value |
| --- | --- | --- |
| `<CUSTOMER_PHONE_NUMBER>` | The customer’s WhatsApp phone number. | `12015553931` |
| `<ONE-TIME PASSWORD>` | The one-time password or verification code to be delivered to the customer.<br>Note that this value must appear twice in the payload.<br>Maximum 15 characters. | `J$FpnYnP` |
| `<TEMPLATE_LANGUAGE_CODE>` | The template’s [language and locale code](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/supported-languages). | `en_US` |
| `<TEMPLATE_NAME>` | The template’s name. | `verification_code` |

### Response

Upon success, the API will respond with:

```json
{
  "messaging_product": "whatsapp",
  "contacts": [
    {
      "input": "<INPUT>",
      "wa_id": "<WA_ID>"
    }
  ],
  "messages": [
    {
      "id": "<ID>"
    }
  ]
}
```

### Response parameters

| Placeholder | Description | Sample Value |
| --- | --- | --- |
| `<INPUT>`<br>*String* | The customer phone number that the message was sent to. This may not match `wa_id`. | `+16315551234` |
| `<WA_ID>`<br>*String* | WhatsApp ID of the customer who the message was sent to. This may not match `input`. | `+16315551234` |
| `<ID>`<br>*String* | WhatsApp message ID. You can use the ID listed after “wamid.” to track your message status. | `wamid.HBgLMTY1MDM4Nzk0MzkVAgARGBI3N0EyQUJDMjFEQzZCQUMzODMA` |

### Example request

```curl
curl -L 'https://graph.facebook.com/v25.0/105954558954427/messages' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '{
      "messaging_product": "whatsapp",
      "recipient_type": "individual",
      "to": "12015553931",
      "type": "template",
      "template": {
        "name": "verification_code",
        "language": {
          "code": "en_US"
      },
      "components": [
        {
          "type": "body",
          "parameters": [
            {
              "type": "text",
              "text": "J$FpnYnP"
            }
          ]
        },
        {
          "type": "button",
          "sub_type": "url",
          "index": "0",
          "parameters": [
            {
              "type": "text",
              "text": "J$FpnYnP"
            }
          ]
        }
      ]
    }
  }'
```

### Example response

```json
{
  "messaging_product": "whatsapp",
  "contacts": [
    {
      "input": "12015553931",
      "wa_id": "12015553931"
    }
  ],
  "messages": [
    {
      "id": "wamid.HBgLMTY1MDM4Nzk0MzkVAgARGBI4Qzc5QkNGNTc5NTMyMDU5QzEA"
    }
  ]
}
```
