# Reject or end a call | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling/consumer2biz/reject-end-call_

---

# Reject or end a call

Updated: Mar 23, 2026

You can reject an incoming call before accepting it, or terminate an active call that is already connected.

## Before you begin

- Complete the setup described in the [Calling overview](https://developers.facebook.com/documentation/business-messaging/messenger-platform/calling)

## Reject an incoming call

### Request syntax

```curl
POST /{page-id}/calls
{
  "platform": "messenger",
  "call_id": "{call-id}",
  "action": "reject"
}
```

### Request parameters

| Property | Description |
| --- | --- |
| `platform` Optional string | Only `Messenger` is supported |
| `call_id` string | ID of the call from the connect webhook |
| `action` string | Set to `reject` |

### Example response

```json
{
  "success" : true
}
```

### Error response

The following errors can occur:

- Invalid call ID or Page ID
- Call already rejected
- Cannot reject a failed or completed call
- Permissions or authorization errors

For more details, see the [Messenger Platform error codes reference](https://developers.facebook.com/documentation/business-messaging/messenger-platform/error-codes).

## Terminate an active call

### Request syntax

```curl
POST /{page-id}/calls
{
  "platform": "messenger",
  "call_id": "{call-id}",
  "action" : "terminate"
}
```

### Request parameters

| Property | Description |
| --- | --- |
| `platform` Optional string | Only `Messenger` is supported |
| `call_id` string | ID of the call from the connect webhook or accept response |
| `action` string | Set to `terminate` |

### Example response

```json
{
  "success" : true
}
```

### Error response

The following errors can occur:

- Invalid call ID or Page ID
- Call already terminated
- Cannot terminate a failed or completed call
- Permissions or authorization errors

For more details, see the [Messenger Platform error codes reference](https://developers.facebook.com/documentation/business-messaging/messenger-platform/error-codes).
