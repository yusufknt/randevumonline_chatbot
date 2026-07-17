# Template previews | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/authentication-templates/template-preview_

---

# Template previews

Updated: Nov 4, 2025

You can generate previews of authentication template text in various languages that include or exclude the security recommendation string and code expiration string using the [Message Template Previews API](https://developers.facebook.com/docs/graph-api/reference/whats-app-business-account/message_template_previews#Reading).

### Request syntax

```https
GET /<WHATSAPP_BUSINESS_ACCOUNT_ID>/message_template_previews
  ?category=AUTHENTICATION,
  &language=<LANGUAGE>, // Optional
  &add_security_recommendation=<ADD_SECURITY_RECOMMENDATION>, // Optional
  &code_expiration_minutes=<CODE_EXPIRATION_MINUTES>, // Optional
  &button_types=<BUTTON_TYPES> // Optional
```

### Request parameters

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<LANGUAGE>`<br>*Comma-separated list* | **Optional.**<br>Comma-separated list of [language and locale codes](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/supported-languages) of language versions you want returned.<br>If omitted, versions of all supported languages will be returned. | `en_US,es_ES` |
| `<ADD_SECURITY_RECOMMENDATION>`<br>*Boolean* | **Optional.**<br>Set to `true` if you want the security recommendation body string included in the response.<br>If omitted, the security recommendation string will not be included. | `true` |
| `<CODE_EXPIRATION_MINUTES>`<br>*Int64* | **Optional.**<br>Set to an integer if you want the code expiration footer string included in the response.<br>If omitted, the code expiration footer string will not be included.<br>Value indicates number of minutes until code expires.<br>Minimum `1`, maximum `90`. | `10` |
| `<BUTTON_TYPES>`<br>*Comma-separated list of strings* | **Required.**<br>Comma-separated list of strings indicating button type.<br>If included, the response will include the button text for each button in the response.<br>For authentication templates, this value must be `OTP`. | `OTP` |

### Example request

```curl
curl 'https://graph.facebook.com/v17.0/102290129340398/message_template_previews?category=AUTHENTICATION&languages=en_US,es_ES&add_security_recommendation=true&code_expiration_minutes=10&button_types=OTP' \
-H 'Authorization: Bearer EAAJB...'
```

### Example response

```json
{
  "data": [
    {
      "body": "*{{1}}* is your verification code. For your security, do not share this code.",
      "buttons": [
        {
          "autofill_text": "Autofill",
          "text": "Copy code"
        }
      ],
      "footer": "This code expires in 10 minutes.",
      "language": "en_US"
    },
    {
      "body": "Tu código de verificación es *{{1}}*. Por tu seguridad, no lo compartas.",
      "buttons": [
        {
          "autofill_text": "Autocompletar",
          "text": "Copiar código"
        }
      ],
      "footer": "Este código caduca en 10 minutos.",
      "language": "es_ES"
    }
  ]
}
```
