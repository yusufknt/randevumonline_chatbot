# Media upload components | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/reference/media_upload_

---

# Media upload components

Updated: Apr 15, 2026

WhatsApp does not guarantee that data (such as images, videos, or documents) shared with you by your customers is non-malicious. Make sure to implement appropriate risk mitigations when processing such data (for example, using well-tested and up-to-date media and document processing libraries).

## Flow JSON components

Two components can be used to ask users to upload media

- PhotoPicker: allows uploading media from camera or gallery
- DocumentPicker: allows uploading media from files or gallery

## PhotoPicker

Supported starting with Flow JSON version 4.0.

| Parameter | Description |
| --- | --- |
| `type`(required)string | PhotoPicker |
| `name`(required)string | Component’s name. Should be distinct among all components on a screen. |
| `label`(required)string | Header text for the component.<br>Dynamic "${data.label}" OR "${screen.<screen_id>.data.label}"<br>Max length: 80 characters |
| `description`string | Body text for the component.<br>Dynamic "${data.description}" OR "${screen.<screen_id>.data.description}"<br>Max length: 300 characters |
| `photo-source`enum | Specifies the source where the image can be selected from.<br>Values: {'camera_gallery', 'camera', 'gallery'}<br>Default: 'camera_gallery'<br>camera_gallery: user can select from gallery or take a photogallery: user can select only from gallerycamera: user can only take a photo |
| `max-file-size-kb`Integer | Specifies the maximum file size (in kibibytes) that can be uploaded.<br>Default value: 25600 (25 MiB) <br>Allowed range: [1, 25600] |
| `min-uploaded-photos`Integer | Specifies the minimum number of photos that are required.<br>This property determines whether the component is optional (set to 0) or required (set above 0).<br>Default value: 0 <br>Allowed range: [0, 30]<br>Note: Above limits apply if media files are sent to the endpoint via "data_exchange" action. For images or documents sent as part of the response message, no more of 10 files can be attached. Additionally, the aggregated size of them cannot exceed 100 MiB. |
| `max-uploaded-photos`Integer | Specifies the maximum number of photos that can be uploaded.<br>Default value: 30 <br>Allowed range: [1, 30]<br>Note: Above limits apply if media files are sent to the endpoint via "data_exchange" action. For images or documents sent as part of the response message, no more of 10 files can be attached. Additionally, the aggregated size of them cannot exceed 100 MiB. |
| `enabled`Boolean \| String | Specifies if user interaction will be enabled on the component(true = enabled, false = disabled).<br>Dynamic "${data.is_enabled}" OR "${screen.<screen_id>.data.is_enabled}"<br>Default: true |
| `visible`Boolean \| String | Specifies if the component will be visible on the screen(true = visible, false = hidden).<br>Dynamic "${data.is_visible}" OR ${screen.<screen_id>.data.visible}"<br>Default: true |
| `error-message`String \| Object | Specifies errors when processing the images.<br>Dynamic “${data.error_message}”<br>String: specifies a generic error for the whole component.Object: specifies image specific errors. Only use with dynamic data as media id must be supplied<br>The format for Object is the following:<br>{"media_id_1" : "error_message 1", "media_id_2" : "error_message 2"}<br>Check the [endpoint handling](https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/reference/media_upload#endpoint-media-handling) section below to find out more about the media ids. |

### **Example**

Note that the image selection behaviour is mocked in this preview. The actual behaviour on device will be similar to the image selection in WhatsApp chats.

### Limitations and Restrictions

The table below outlines the constraints associated with the PhotoPicker component.

| Constraint | Validation error |
| --- | --- |
| `min-uploaded-photos` should not exceed `max-uploaded-photos` | “min-uploaded-photos” cannot be greater than “max-uploaded-photos” for PhotoPicker component ${component_name}. |
| PhotoPicker cannot be initialised using Form `init-values` | Invalid value found for property at ${path}. “init-values” property should not contain a value for PhotoPicker component. |
| Only 1 PhotoPicker is allowed per screen | You can only have a maximum of 1 component of type PhotoPicker per screen. |
| Using both PhotoPicker and DocumentPicker components on a single screen is not allowed. | You can only have a maximum of 1 component of type PhotoPicker or DocumentPicker per screen. |
| The PhotoPicker is not allowed in the `navigate` action payload.<br>To access the component’s value from a different screen, you can utilize<br>[Global Dynamic Referencing](https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/reference/flowjson#global-data). | The PhotoPicker component’s value is not allowed in the payload of the navigate action. |
| The PhotoPicker component is restricted to top-level usage within the payloads of the `data_exchange` or `complete` action.<br>Valid:<br>`"on-click-action":<br>{<br> "name": "data_exchange",<br> "payload":<br> {<br> "media": "${form.photo_picker}"<br> }<br>}`<br>Invalid:<br>`"on-click-action":<br>{<br> "name": "data_exchange",<br> "payload":<br> {<br> "media": {"photo": "${form.photo_picker}"}<br> }<br>}` | The PhotoPicker can only be used as the value of a top-level string property in the action payload. |
| No more than 10 images or documents can be sent as part of the response message. | Additionally, the maximum aggregated size of attached images or documents cannot exceed 100 MiB. |

## DocumentPicker

Supported starting with Flow JSON version 4.0.

| Parameter | Description |
| --- | --- |
| `type`(required)string | DocumentPicker |
| `name`(required)string | Component’s name. Should be distinct among all components on a screen. |
| `label`(required)string | Header text for the component.<br>Dynamic "${data.label}" OR "${screen.<screen_id>.data.label}"<br>Max length: 80 characters |
| `description`string | Body text for the component.<br>Dynamic "${data.description}" OR "${screen.<screen_id>.data.description}"<br>Max length: 300 characters |
| `max-file-size-kb`Integer | Specifies the maximum file size (in kibibytes) that can be uploaded.<br>Default value: 25600 (25 MiB) <br>Allowed range: [1, 25600] |
| `min-uploaded-documents`Integer | Specifies the minimum number of documents that are required.<br>This property determines whether the component is optional (set to 0) or required (set above 0).<br>Default value: 0 <br>Allowed range: [0, 30]<br>Note: Above limits apply if media files are sent to the endpoint via "data_exchange" action. For images or documents sent as part of the response message, no more of 10 files can be attached. Additionally, the aggregated size of them cannot exceed 100 MiB. |
| `max-uploaded-documents`Integer | Specifies the maximum number of documents that can be uploaded.<br>Default value: 30 <br>Allowed range: [1, 30]<br>Note: Above limits apply if media files are sent to the endpoint via "data_exchange" action. For images or documents sent as part of the response message, no more of 10 files can be attached. Additionally, the aggregated size of them cannot exceed 100 MiB. |
| `allowed-mime-types`Array <string> | Specifies which document mime types can be selected. If it contains “image/jpeg”, picking photos from the gallery will be available as well.<br>Default: Any document from the supported mime types can be selected<br>Supported values:<br>application/gzipapplication/mswordapplication/pdfapplication/vnd.ms-excelapplication/vnd.ms-powerpointapplication/vnd.oasis.opendocument.presentationapplication/vnd.oasis.opendocument.spreadsheetapplication/vnd.oasis.opendocument.textapplication/vnd.openxmlformats-officedocument.presentationml.presentationapplication/vnd.openxmlformats-officedocument.spreadsheetml.sheetapplication/vnd.openxmlformats-officedocument.wordprocessingml.documentapplication/x-7z-compressedapplication/zipimage/avifimage/gifimage/heicimage/heifimage/jpegimage/pngimage/tiffimage/webptext/plainvideo/mp4video/mpeg<br>Note: some old Android and iOS OS versions don’t understand all mime types above. As a result, a user might be able to select a file with a different mime type to the ones specified. |
| `enabled`Boolean \| String | Specifies if user interaction will be enabled on the component(true = enabled, false = disabled).<br>Dynamic "${data.is_enabled}" OR "${screen.<screen_id>.data.is_enabled}"<br>Default: true |
| `visible`Boolean \| String | Specifies if the component will be visible on the screen(true = visible, false = hidden).<br>Dynamic "${data.is_visible}" OR ${screen.<screen_id>.data.visible}"<br>Default: true |
| `error-message`String \| Object | Specifies errors when processing the documents.<br>Dynamic “${data.error_message}”<br>String: specifies a generic error for the whole component.Object: specifies document specific errors. Only use with dynamic data as media id must be supplied<br>The format for Object is the following:<br>{"media_id_1" : "error_message 2", "media_id_2" : "error_message 2"}<br>Check the [endpoint handling](https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/reference/media_upload#endpoint-media-handling) section below to find out more about the media ids. |

### **Example**

Note that the document selection behaviour is mocked in this preview. The actual behaviour on device will be similar to the document selection in WhatsApp chats.

### Limitations and Restrictions

The table below outlines the constraints associated with the DocumentPicker component.

| Constraint | Validation error |
| --- | --- |
| `min-uploaded-documents` should not exceed `max-uploaded-documents` | “min-uploaded-documents” cannot be greater than “max-uploaded-documents” for DocumentPicker component ${component_name}. |
| DocumentPicker cannot be initialised using Form `init-values` | Invalid value found for property at ${path}. “init-values” property should not contain a value for DocumentPicker component. |
| Only 1 DocumentPicker is allowed per screen | You can only have a maximum of 1 component of type DocumentPicker per screen. |
| Using both PhotoPicker and DocumentPicker components on a single screen is not allowed. | You can only have a maximum of 1 component of type PhotoPicker or DocumentPicker per screen. |
| The DocumentPicker is not allowed in the `navigate` action payload.<br>To access the component’s value from a different screen, you can utilize [Global Dynamic Referencing](https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/reference/flowjson#global-data). | The DocumentPicker component’s value is not allowed in the payload of the navigate action. |
| The DocumentPicker component is restricted to top-level usage within the payloads of the `data_exchange` or `complete` action.<br>Valid:<br>`"on-click-action":<br>{<br> "name": "data_exchange",<br> "payload":<br> {<br> "media": "${form.document_picker}"<br> }<br>}`<br>Invalid:<br>`"on-click-action":<br>{<br> "name": "data_exchange",<br> "payload":<br> {<br> "media": {"document": "${form.document_picker}"}<br> }<br>}` | The DocumentPicker can only be used as the value of a top-level string property in the action payload. |
| No more than 10 images or documents can be sent as part of the response message. | Additionally, the maximum aggregated size of attached images or documents cannot exceed 100 MiB. |

## Handling media

### Endpoint

Media uploaded by the users are temporarily (up to 20 days) stored in WhatsApp CDN. Files are encrypted using AES256-CBC+HMAC-SHA256+pkcs7 cryptographic algorithms.

In your endpoint implementation, you must download, decrypt, and validate each media file.

Here’s a payload example for a photo or document.

```json
"photo_picker":[{
     "media_id": "790aba14-5f4a-4dbd-aa9e-0d75401da14b",
     "cdn_url": "https://mmg.whatsapp.net/v/redacted",
     "file_name": "IMG_5237.jpg"
     "encryption_metadata": {
       "encrypted_hash": "/QvkBvpBED2q2AHPIFuhXfLpkn22zj2kO6ggzjvhHv0=",
       "iv": "5SHjLrrsfPXTSJTcbrVSkg==",
       "encryption_key": "lPa4SXcWbk3sy2so3OxjyXmpV4aE6CcIKd+4byr5hBw=",
       "hmac_key": "15l+E9Z5gcL15WH9OQ8GgK7VVCKkfbVigoSiM9djvGU=",
       "plaintext_hash": "AOF2dHXVEpm9efk9udNy3R1cUJWnpjFwQKGBEdALqXI="
     }]
```

Decrypting and validating media

The files stored in WhatsApp CDN contain the encrypted media and the first 10 bytes of the HMAC-SHA256 (concatenated at the end). For reference, `cdn_file = ciphertext & hmac10`.

Perform the following steps to decrypt the media:

1. Download cdn_file file from cdn_url
2. Make sure SHA256(cdn_file) == enc_hash
3. Validate HMAC-SHA256 Calculate HMAC with hmac_key, initialization vector (encryption_metadata.iv) and ciphertexMake sure first 10 bytes == hmac10
4. Decrypt media content Run AES with CBC mode and initialization vector (encryption_metadata.iv) on ciphertexRemove padding (AES256 uses blocks of 16 bytes, padding algorithm is pkcs7). We’ll call this decrypted_media
5. Validate the decrypted media Make sure SHA256(decrypted_media) = plaintext_hash

## Response message (Cloud API)

Media can be received in the [response message webhook](https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/guides/receiveflowresponse).

Here’s a truncated example using PhotoPicker (same structure for DocumentPicker)

```json
{
    "nfm_reply": {
        // [... redacted ... ]
        "response_json": {
            "photo_picker": [
                {
                    "file_name": "IMG_5237.jpg",
                    "mime_type": "image/jpeg",
                    "sha256": "PqHgadp8cJ/N6mvAYGNMxhs9Ra5hbZFcctCtCClXsMU=",
                    "id": "3631120727156756"
                }
            ],
            "flow_token": "xyz",
            "name": "John"
        }
    }
}
```

The media can be downloaded following the same [steps as for regular image and document messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/media#download-media).
