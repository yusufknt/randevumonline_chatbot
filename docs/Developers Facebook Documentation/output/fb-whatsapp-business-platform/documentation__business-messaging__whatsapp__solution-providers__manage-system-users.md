# Manage System Users | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/manage-system-users_

---

# Manage System Users

Updated: Nov 14, 2025

Adding your System User to shared WhatsApp Business Accounts allows you to programmatically manage the accounts. On this guide, we go over actions BSPs may need to perform to manage their system users.

For help creating a system user and generating your system user access token, see [Access Tokens, System User access tokens](https://developers.facebook.com/documentation/business-messaging/whatsapp/access-tokens#system-user-access-tokens).

## Retrieve System User IDs

You can cache the System User IDs for future use.

### Request

```curl
curl -i -X GET "https://graph.facebook.com/<API_VERSION>/<WHATSAPP_BUSINESS_ACCOUNT_ID>/system_users
  ?access_token=<SYSTEM_USER_ACCESS_TOKEN>"
```

To find the ID of a business, go to [Business Manager](https://business.facebook.com/) > Business Settings > Business Info. There, you will see information about the business, including the ID.

### Response

```json
{
  "data": [
    {
      "id": "1972555232742222",
      "name": "My System User",
      "role": "EMPLOYEE"
    }
  ]
}
```

## Add System Users to a WhatsApp Business Account

For this API call, **you need to use the access token of a System User with admin permissions**.

### Request syntax

In the following example, use the ID for the assigned WABA.

```html
curl -i -X POST "https://graph.facebook.com/<API_VERSION>/<WHATSAPP_BUSINESS_ACCOUNT_ID>/assigned_users
  ?user=<ASSIGNED_USER_ID>
  &tasks=['<ASSIGNED_USERS_TASKS_AND_PERMISSIONS>']
  &access_token=<SYSTEM_USER_ACCESS_TOKEN>"
```

To find the ID of a WhatsApp Business Account, go to [Business Manager](https://business.facebook.com/) > Business Settings > Accounts > WhatsApp Business Accounts. Find the account you want to use and click on it. A panel opens, with information about the account, including the ID.

For the `<ASSIGNED_USER_ID>`, use the system user ID returned from [your `/<WHATSAPP_BUSINESS_ACCOUNT_ID>/system_users` call](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/manage-system-users#retrieve-system-user-ids).

### Permissions

| Name | Description |
| --- | --- |
| `MANAGE` | Provides admin access.<br>Users can have admin access on a WhatsApp Business Account that is shared with Admin permissions.<br>Note: If you are a Solution Partner trying to add a user to a WhatsApp Business Account that is shared with you via a [Multi-Partner Solution](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/multi-partner-solutions), then you would need to account for the following scenarios:<br>If you are not granted `MESSAGING` permission on the solution, then you need to decide which granular tasks you need when adding the user to the shared WhatsApp Business Account: `DEVELOP`, `MANAGE_TEMPLATES`, `MANAGE_PHONE`, `VIEW_COST`, `MANAGE_EXTENSIONS`, `VIEW_PHONE_ASSETS`, `MANAGE_PHONE_ASSETS`, `VIEW_TEMPLATES`, `VIEW_INSIGHTS`, `MANAGE_USERS`, `MANAGE_BILLING`.In such scenario, also note that `MANAGE_BILLING` is needed for sharing Line of Credit.MANAGE will only work if you are given full access on the solution i.e. including `MESSAGING`. |
| `DEVELOP` | Provides developer access.<br>Users can have developer access on a WhatsApp Business Account that is shared with Standard permissions. |

### Response

```json
{
  "success": true
}
```

## Retrieve assigned users

You can fetch the assigned users of the WhatsApp Business Account to verify that the user was added. This is not a required step but helps with validation.

### Request syntax

In the following example, use the ID for the assigned WABA.

```html
curl -i -X GET "https://graph.facebook.com/<API_VERSION>/<WHATSAPP_BUSINESS_ACCOUNT_ID>/assigned_users
  ?business=<WHATSAPP_BUSINESS_ACCOUNT_ID>
  &access_token=<SYSTEM_USER_ACCESS_TOKEN>"
```

### Response

```json
{
  "data": [
    {
      "id": "1972385232742142",
      "name": "Anna Flex",
      "tasks": [
        "MANAGE"
      ]
    },
    {
      "id": "1972385232752545",
      "name": "Jasper Brown",
      "tasks": [
        "DEVELOP"
      ]
    }
  ]
}
```

## See Also

- Reference: [WhatsApp Business Account](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/whatsapp-business-account-api)
