# Groups API Error Codes and Troubleshooting | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/groups/error-codes_

---

# Groups API Error Codes and Troubleshooting

Updated: Oct 31, 2025

## Error Codes

| Code | Description | HTTP Status Code |
| --- | --- | --- |
| `131020`<br>Bad Group | Cannot send messages to single member groups. | `400`<br>Bad Request |
| `131041`<br>Group unknown | The group was not found, either because it doesn’t exist or you are not a member. | `400`<br>Bad Request |
| `131059`<br>Invalid cursor | The cursor has either expired or become corrupted. Start pagination from the beginning again. | `400`<br>Bad Request |
| `131201`<br>Request partially succeeded | Not all participant-level operations in the request succeeded. | `206`<br>Partial Content Success |
| `131202`<br>Duplicate participant | Duplicate participants in the participant array input. | `400`<br>Bad Request |
| `131204`<br>Participant overlimit | Group participant size exceeds limit. | `400`<br>Bad Request |
| `131207`<br>Group suspended | The group violates platform policies. | `403`<br>Forbidden |
| `131208`<br>Group Rate Limit Hit | Group operation failed because there were too many group operations from this phone number in a short period. | `429`<br>Too many requests |
| `131209`<br>Invalid Group Profile Picture Aspect Ratio | Width and height of the image must be equal. | `400`<br>Bad Request |
| `131210`<br>Image is Too Small to Process | Image width and height must be greater than 192px. | `400`<br>Bad Request |
| `131211`<br>Group create limit reached | Reached the limit for the maximum number of groups that can be created for this number. | `400`<br>Bad Request |
| `131212`<br>Participant is not a part of the group. | Participant is not a part of the group. | `400`<br>Bad Request |
| `131213`<br>Group join request does not exist. | Group join request does not exist. | `400`<br>Bad Request |
| `131214`<br>Group creation is temporarily disabled | Group creation is temporarily disabled due to excessive marketing messages sent by the WABA in customer service window over the past 7 days. | `400`<br>Bad Request |
| `131215`<br>This phone number is not eligible to access Groups APIs | Groups APIs are only available for eligible phone numbers. Please check eligibility for Groups APIs in our documentation - /documentation/business-messaging/whatsapp/groups/get-started | `400`<br>Bad Request |
