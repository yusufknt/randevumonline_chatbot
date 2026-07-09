# No Storage | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/no-storage_

---

# No Storage

Updated: Dec 1, 2025

“No Storage” is a custom configuration of Cloud API [local storage](https://developers.facebook.com/documentation/business-messaging/whatsapp/local-storage), where the data in-transit is kept for up to an hour in Meta data centers and the data is not persisted at rest (that is to say, not in Meta data centers nor in AWS In-Country stores).

- Outgoing/incoming messages are stored for a maximum of 1 hour in Meta data centers.
- Outgoing/incoming media blobs are stored for a maximum of 1 hour in Meta data centers.
- You can pass a custom time-to-live (TTL) — from 1 hour to 30 days — when uploading media to override the 1 hour expiration (particularly useful for marketing campaigns which reuse the same media)

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/559308894_1116451836859295_8169970485040161301_n.png?_nc_cat=102&ccb=1-7&_nc_sid=e280be&_nc_ohc=6eY-xfOFuB4Q7kNvwGUoVOu&_nc_oc=AdrBeTvMTTod64GHAuQZKHWbmaNuIjxq5nwmJdmBmlqKa2HWhpoiTQ380KAoZquosvE&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=531ODFcVgVwzcVwR8PFg7g&_nc_ss=7b20f&oh=00_Af75XcHpukEo9VekXpsg-ZLD7nt8FTb7v64J2PMlOhkfCA&oe=6A1C34D5)

## Limitations

When the No Storage feature is enabled, message content is not stored at rest for 30 days as is typical with Cloud API. This introduces the following limitations, which can put a small fraction of your total messaging volume at risk of non-delivery.

- **Message decryption failures** — If a message fails to decrypt on the consumer side, Cloud API can only retry sending the message within a 1-hour TTL window. After this 1-hour window, Cloud API cannot retry the message. You will receive an error webhook indicating the failure. See: [Retry Receipt Failures](https://developers.facebook.com/documentation/business-messaging/whatsapp/no-storage#retry-receipt-failures) .
- **Webhook delivery failures** — Normally, Cloud API retries undelivered webhooks (such as incoming messages or receipts) for up to 7 days. With No Storage enabled, webhook retries are limited to 1 hour. If your webhook server is unavailable beyond this window, the webhook (including incoming messages, receipts, etc.) will be permanently lost. See: [Failure to Deliver Webhooks](https://developers.facebook.com/documentation/business-messaging/whatsapp/no-storage#failure-to-deliver-webhooks) .
- **Incoming media messages** — Media attached to incoming messages will be available for download for up to 1 hour. After 1 hour, the media is permanently deleted and cannot be retrieved.

## Enable No Storage

### Request syntax (v21.0 or newer)

Enable the feature before registration using the [Settings API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/settings-api#post-version-phone-number-id-settings).

```html
curl 'https://graph.facebook.com/<API_VERSION>/<BUSINESS_PHONE_NUMBER_ID>/settings' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <ACCESS_TOKEN>' \
-d '
{
  "storage_configuration": {
    "status": "NO_STORAGE_ENABLED",
    "retention_minutes": 60
  }
}'
```

Currently, only the `60` value is allowed for the `retention_minutes` parameter, as it is the only retention duration we are supporting.

### Request syntax (v20.0 or older)

Enable the feature within the [Register API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/register-api#post-version-phone-number-id-register) registration request.

```html
curl 'https://graph.facebook.com/<API_VERSION>/<BUSINESS_PHONE_NUMBER_ID>/settings' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <ACCESS_TOKEN>' \
-d '
{
  "messaging_product": "whatsapp",
  "pin": "123456",
  "tier": "test",
  "meta_store_retention_minutes": 60
}'
```

- Currently only the 60 value is allowed for the meta_store_retention_minutes parameter as it is the only retention duration we are supporting.
- `meta_store_retention_minutes` cannot be used alongside with `data_localization_region` .

## Disable No Storage

To disable No Storage, you must de-register the business phone number using the [Deregister API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/phone-number-deregister-api#post-version-phone-number-id-deregister), then register the number again without the `meta_store_retention_minutes` parameter.

### Example deregister syntax

```html
curl -X POST 'https://graph.facebook.com/<API_VERSION>/<BUSINESS_PHONE_NUMBER_ID>/deregister' \
-H 'Authorization: Bearer <ACCESS_TOKEN>'
```

## Override outgoing media TTL

The default 1-hour TTL for No Storage-enabled business phone numbers also applies to [media uploaded on the number](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/media#upload-media). If you want to override the default 1-hour TTL, you can include the new `ttl_minutes` parameter when uploading media.

### Example syntax

```html
curl 'https://graph.facebook.com/<API_VERSION>/<BUSINESS_PHONE_NUMBER_ID>/media' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <ACCESS_TOKEN>' \
-d '
{
  "messaging_product": "whatsapp",
  "file": "file=<FILE_NAME>;type=<FILE_MIME_TYPE>",
  "ttl_minutes": "120"
}'
```

- `ttl_minutes` range is from 1 hour ( `60` ) to 30 days ( `43200` ).
- The API currently does not return the expiration date of the media in the response API.

## Error webhooks

### Retry receipt failures

In the case of WhatsApp client decryption failures, we will stop attempting to deliver an undelivared message from a No Storage-enabled number once the TTL is reached. In these cases, a [status messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/status) webhook is triggered with error code `131036`:

Example payload

```json
{
  "object": "whatsapp_business_account",
  "entry": [{
    "id": "102290129340398",
    "changes": [{
      "field": "messages",
      "value": {
        "messaging_product": "whatsapp",
        "metadata": {
          "display_phone_number": "15550783881",
          "phone_number_id": "106540352242922"
        },
        "statuses": [{
          "id": "wamid.HBgMNDQ3ODI1MDYzOTQxFQIAERgSN0MzMTg0Nzk2RkMwOEQ5NTQ2AA==",
          "status": "failed",
          "timestamp": "1712597457",
          "recipient_id": "16505551234",
          "errors": [{
              "code": 131036,
              "title": "Message failed to be delivered on at least one of the user's device",
              "message": "Message failed to be delivered on at least one of the user's device",
              "error_data": {
                "details": "Message payload not found"
              }
            }]
        }]
      }
    }]
  }]
}
```

Notes:

- This error is sent only if we fail to honor a retry receipt sent by the primary device. If the retry fails for a secondary device, we ignore it, as the message will be delivered when syncing with the primary device.
- It is possible that the message has been successfully delivered to secondary devices but not the primary device. In this case, the webhook will be sent.

### Failure to deliver webhooks

By default, Cloud API retries for up to 7 days to deliver incoming [messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages#incoming-messages) webhooks. For No Storage-enabled business phone numbers, if we fail to deliver an incoming message webhook, we will drop it and instead send an [errors messages](https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/errors) webhook with error code `131035`:

```json
{
  "object": "whatsapp_business_account",
  "entry": [{
    "id": "102290129340398",
    "changes": [{
      "field": "messages",
      "value": {
        "messaging_product": "whatsapp",
        "metadata": {
          "display_phone_number": "15550783881",
          "phone_number_id": "106540352242922"
        },
        "errors": [{
            "code": 131035,
            "title": "Webhook could not be delivered within data retention limit",
            "message": "Webhook could not be delivered within data retention limit",
            "error_data": {
              "details": "Webhook could not be delivered within data retention limit"
            }
          }]
      }
    }]
  }]
}
```
