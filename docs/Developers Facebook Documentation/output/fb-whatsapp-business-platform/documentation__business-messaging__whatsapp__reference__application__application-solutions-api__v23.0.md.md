# WhatsApp Business Multi-Partner Solutions - Application Solutions API

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/application/application-solutions-api/v23.0.md_

---

```
## Base URL

| URL | Description |
|-----|-------------|
| https://graph.facebook.com | Production Graph API server |

## APIs

| Method | Endpoint |
|--------|----------|
| GET | [/{Version}/{Application-ID}/whatsapp_business_solutions](#get-version-application-id-whatsapp-business-solutions) |

<jumplink id="get-version-application-id-whatsapp-business-solutions"></jumplink>
## GET /{Version}/{Application-ID}/whatsapp_business_solutions

Get Multi-Partner Solutions for Application

Retrieve all WhatsApp Business Multi-Partner Solutions associated with the specified application.
This includes both solutions owned by the application and solutions where the application
acts as a partner.

**Use Cases:**
- Retrieve all solutions for an application's portfolio management
- Filter solutions by ownership role (owner vs partner)
- Monitor solution lifecycle and status changes across multiple solutions
- Verify solution configuration before business onboarding operations
- Check pending approval requests and status transitions

**Filtering:**
Use the `role` parameter to filter solutions by the application's relationship:
- `OWNER`: Only solutions owned by this application
- `PARTNER`: Only solutions where this application is a partner
- No role parameter: All solutions (both owned and partnered)

**Rate Limiting:**
Standard Graph API rate limits apply. Use appropriate retry logic with exponential backoff.

**Caching:**
Solution details can be cached for short periods, but status information may change
frequently during transitions. Implement appropriate cache invalidation strategies.

### Header Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| User-Agent | string |  | The user agent string identifying the client software making the request. |
| Authorization | string | ✓ | Bearer token for API authentication. This should be a valid access token obtained through the appropriate OAuth flow or system user token. |

### Path Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| Version | string | ✓ | Graph API version to use for this request. Determines the API behavior and available features. |
| Application-ID | string | ✓ | Your Meta Application ID. This ID can be found in your App Dashboard and represents the application for which you want to retrieve associated Multi-Partner Solutions. |

### Query Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| role | [WhatsAppBusinessSolutionApplicationRole](#whatsappbusinesssolutionapplicationrole) |  | Filter solutions by the application's relationship role. If not specified, all solutions (both owned and partnered) will be returned. |
| fields | string |  | Comma-separated list of fields to include in the response. If not specified, default fields will be returned (name, status, status_for_pending_request). Available fields: id, name, status, status_for_pending_request, owner_app, owner_permissions |
| limit | integer [min: 1, max: 100] |  | Maximum number of solutions to return in a single request. Default is 25, maximum is 100. |
| after | string |  | Cursor for pagination. Use this to get the next page of results. |
| before | string |  | Cursor for pagination. Use this to get the previous page of results. |

### Responses

**200**

Successfully retrieved Multi-Partner Solutions for the application

**Content Type**: `application/json`

**Schema**: [WhatsAppBusinessSolutionsResponse](#whatsappbusinesssolutionsresponse)

**400**

Bad Request - Invalid parameters or malformed request

**Content Type**: `application/json`

**Schema**: [GraphAPIError](#graphapierror)

**Example**:\n```json\n{
    "error": {
        "message": "Invalid parameter: application_id must be a valid numeric string",
        "type": "OAuthException",
        "code": 100,
        "fbtrace_id": "AXsgnV2Cm3ZMGF3dF_cfYIn"
    }
}\n```

**401**

Unauthorized - Invalid or missing access token

**Content Type**: `application/json`

**Schema**: [GraphAPIError](#graphapierror)

**Example**:\n```json\n{
    "error": {
        "message": "Invalid OAuth access token",
        "type": "OAuthException",
        "code": 190,
        "error_subcode": 463,
        "fbtrace_id": "AXsgnV2Cm3ZMGF3dF_cfYIn"
    }
}\n```

**403**

Forbidden - Insufficient permissions or access denied

**Content Type**: `application/json`

**Schema**: [GraphAPIError](#graphapierror)

**Example**:\n```json\n{
    "error": {
        "message": "Your app doesn't have permission to access Multi-Partner Solutions for this application",
        "type": "OAuthException",
        "code": 200,
        "error_subcode": 1349174,
        "fbtrace_id": "AXsgnV2Cm3ZMGF3dF_cfYIn",
        "error_user_title": "Permission Denied",
        "error_user_msg": "Your app doesn't have permission to access this resource"
    }
}\n```

**404**

Not Found - Application ID does not exist or is not accessible

**Content Type**: `application/json`

**Schema**: [GraphAPIError](#graphapierror)

**Example**:\n```json\n{
    "error": {
        "message": "Application not found",
        "type": "GraphMethodException",
        "code": 803,
        "fbtrace_id": "AXsgnV2Cm3ZMGF3dF_cfYIn"
    }
}\n```

**422**

Unprocessable Entity - Request parameters are valid but cannot be processed

**Content Type**: `application/json`

**Schema**: [GraphAPIError](#graphapierror)

**Example**:\n```json\n{
    "error": {
        "message": "The requested fields are not available for these solutions",
        "type": "GraphMethodException",
        "code": 100,
        "fbtrace_id": "AXsgnV2Cm3ZMGF3dF_cfYIn"
    }
}\n```

**429**

Too Many Requests - Rate limit exceeded

**Content Type**: `application/json`

**Schema**: [GraphAPIError](#graphapierror)

**Example**:\n```json\n{
    "error": {
        "message": "Application request limit reached",
        "type": "OAuthException",
        "code": 4,
        "error_subcode": 2446079,
        "fbtrace_id": "AXsgnV2Cm3ZMGF3dF_cfYIn",
        "is_transient": true
    }
}\n```

**500**

Internal Server Error - Unexpected server error

**Content Type**: `application/json`

**Schema**: [GraphAPIError](#graphapierror)

**Example**:\n```json\n{
    "error": {
        "message": "An unexpected error occurred. Please retry your request",
        "type": "GraphMethodException",
        "code": 2,
        "fbtrace_id": "AXsgnV2Cm3ZMGF3dF_cfYIn",
        "is_transient": true
    }
}\n```

# Components

## Schemas

<jumplink id="whatsappbusinesssolution"></jumplink>
### WhatsAppBusinessSolution

Multi-Partner Solution details and configuration

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| id | string | ✓ | Unique identifier for the Multi-Partner Solution |
| name | string | ✓ | Human-readable name of the Multi-Partner Solution |
| status | [WhatsAppBusinessSolutionStatus](#whatsappbusinesssolutionstatus) | ✓ |  |
| status_for_pending_request | [WhatsAppBusinessSolutionPendingStatus](#whatsappbusinesssolutionpendingstatus) | ✓ |  |
| owner_app | [ApplicationNode](#applicationnode) |  |  |
| owner_permissions | array of [WhatsAppBusinessAccountPermissionTask](#whatsappbusinessaccountpermissiontask) |  | List of WhatsApp Business Account permissions granted to the solution owner |

<jumplink id="whatsappbusinesssolutionstatus"></jumplink>
### WhatsAppBusinessSolutionStatus

Current effective status of the Multi-Partner Solution

**Type**: string

**Enum Values**: "DRAFT", "INITIATED", "ACTIVE", "REJECTED", "DEACTIVATED"

<jumplink id="whatsappbusinesssolutionpendingstatus"></jumplink>
### WhatsAppBusinessSolutionPendingStatus

Status of any pending solution status transition requests

**Type**: string

**Enum Values**: "PENDING_ACTIVATION", "PENDING_DEACTIVATION", "NONE"

<jumplink id="whatsappbusinessaccountpermissiontask"></jumplink>
### WhatsAppBusinessAccountPermissionTask

Granular permission tasks for WhatsApp Business Account access

**Type**: string

**Enum Values**: "MANAGE", "DEVELOP", "MANAGE_TEMPLATES", "MANAGE_PHONE", "VIEW_COST", "MANAGE_EXTENSIONS", "VIEW_PHONE_ASSETS", "MANAGE_PHONE_ASSETS", "VIEW_TEMPLATES", "VIEW_INSIGHTS", "RECEIVE_INCOMING_MESSAGES", "MANAGE_BILLING", "MANAGE_USERS", "MESSAGING", "FULL_CONTROL"

<jumplink id="whatsappbusinesssolutionapplicationrole"></jumplink>
### WhatsAppBusinessSolutionApplicationRole

Role of the application in relation to the Multi-Partner Solution

**Type**: string

**Enum Values**: "OWNER", "PARTNER"

<jumplink id="applicationnode"></jumplink>
### ApplicationNode

Meta application that owns the Multi-Partner Solution

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| id | string |  | Unique identifier for the Meta application |
| name | string |  | Name of the Meta application |

<jumplink id="whatsappbusinesssolutionsresponse"></jumplink>
### WhatsAppBusinessSolutionsResponse

Response containing list of Multi-Partner Solutions with pagination

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| data | array of [WhatsAppBusinessSolution](#whatsappbusinesssolution) |  | Array of Multi-Partner Solutions |
| paging | [CursorPaging](#cursorpaging) |  |  |

<jumplink id="cursorpaging"></jumplink>
### CursorPaging

Cursor-based pagination information

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| cursors | [Cursors](#object-cursors-1) |  |  |
| previous | string |  | Graph API endpoint URL for the previous page of data |
| next | string |  | Graph API endpoint URL for the next page of data |

<jumplink id="graphapierror"></jumplink>
### GraphAPIError

Standard Graph API error response

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| error | [Error](#object-error-2) | ✓ |  |

## Inline Object Definitions

<jumplink id="object-cursors-1"></jumplink>
### Cursors

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| before | string |  | Cursor pointing to the start of the page of data that has been returned |
| after | string |  | Cursor pointing to the end of the page of data that has been returned |

<jumplink id="object-error-2"></jumplink>
### Error

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| message | string | ✓ | Human-readable error message |
| type | string | ✓ | Error category type |
| code | integer | ✓ | Numeric error code |
| error_subcode | integer |  | More specific error subcode when available |
| fbtrace_id | string |  | Unique identifier for debugging and support requests with Meta |
| is_transient | boolean |  | Indicates whether this error is temporary and the request should be retried |
| error_user_title | string |  | User-friendly error title for display purposes |
| error_user_msg | string |  | User-friendly error message for display purposes |

## Authentication

| Scheme | Type | Location |
|--------|------|----------|
| bearerAuth | HTTP Bearer | Header: `Authorization` |

### Usage Examples

- **bearerAuth**: Include `Authorization: Bearer your-token-here` in request headers

### Global Authentication Requirements

All endpoints require: bearerAuth
```
