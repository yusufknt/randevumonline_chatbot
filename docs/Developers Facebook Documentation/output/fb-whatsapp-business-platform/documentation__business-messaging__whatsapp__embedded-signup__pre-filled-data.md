# Pre-filling screens | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/pre-filled-data_

---

# Pre-filling screens

Updated: Nov 10, 2025

If you know details about your customer’s business, such as its name and address, you can inject this data into Embedded Signup. This can pre-fill screens or bypass them altogether, dramatically reducing the amount of input and interaction required by your customers.

For example, here is the business portfolio screen, pre-filled with business’s name, email address, website, country, and a pre-verified business phone number:

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/465727373_1573223883300812_8312998736298536563_n.png?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=l3RkhQMGmpkQ7kNvwGt-Ifc&_nc_oc=AdqgV-Jm2YDc2L09RZko7sWuY6yY2z57rtRhiTdc-QnLoc7BpJaxuWur6VGiy6ESVY0&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=ETWjD-bM7Xyl4kOFuS759w&_nc_ss=7b20f&oh=00_Af5OKVAT_XyL9Rg9HEPnPFJJcr2OIqegxs3jr0IFNX-NxA&oe=6A1C2907)

We recommend that you inject [business portfolio data](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/pre-filled-data#business-portfolio-data), a [pre-verified number](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/pre-filled-data#pre-verified-phone-numbers), and [phone profile data](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/pre-filled-data#phone-profile-data). Injecting this data provides the best experience for your customer, as it:

- entirely pre-fills the business portfolio screen
- bypasses the WhatsApp Business Account (WABA) selection and creation screens
- bypasses the business phone number selection and verification screens
- automatically sets the business phone number’s profile information in the WhatsApp client

## Embedded Signup Integration Helper

The Embedded Signup Integration Helper provides a convenient way for you to create pre-filled data payloads and test their impact on the flow. To access the payload tool:

- Navigate to **App Dashboard** > **WhatsApp** > **Embedded Signup Builder** .
- Locate the **Embedded Signup Setup** section.
- Locate the **Embedded Signup Pre-fill** row.
- Click the **Edit pre-fill data** button.

## Injecting Data

The `FB.login` function, which gets called when a business customer launches Embedded Signup, accepts an object as an argument. Use this object’s `extras.setup` property to inject data:

```js
// Launch method and callback registration
const launchWhatsAppSignup = () => {
  FB.login(fbLoginCallback, {
    config_id: '<CONFIGURATION_ID>', // your configuration ID goes here
    response_type: 'code',
    override_default_response_type: true,
    extras: {
      setup: {
        business: {
          // Business portfolio data goes here
        },
        preVerifiedPhone: {
          // Pre-verified phone number IDs go here
        },
        phone: {
          // Phone number profile data goes here
        },
        whatsAppBusinessAccount: {
          // WABA IDs go here
        }
      },
      featureType: '',
      sessionInfoVersion: '3',
    }
  });
}
```

### Business portfolio data

You can inject the following business portfolio details into the business portfolio screen:

- business portfolio name
- business portfolio email address
- business portfolio website
- business portfolio country (as well as additional address details)
- business phone number

Alternatively, you can inject *just an existing business portfolio ID*, and its existing details will automatically be injected into the screen. This can be useful if you want a pre-verified phone number to be associated with the customer’s existing business portfolio.

Injecting business portfolio data will pre-fill the business portfolio screen and also cause Embedded Signup to skip the WABA selection and WABA creation screens.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/465818706_1256612865537779_5095106003564232822_n.png?_nc_cat=110&ccb=1-7&_nc_sid=e280be&_nc_ohc=ER8W6e4nrAQQ7kNvwGojsYx&_nc_oc=Adp8at3h48UizI8xTX6xNGLH3RP44ObYKEFlXYWl-n4JQCcIRUfxF1Evg-egZpx7kYY&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=ETWjD-bM7Xyl4kOFuS759w&_nc_ss=7b20f&oh=00_Af6DgfiexfbCfl5oZcOx9n-SAXkXy78usHxfnk7H5FOV7g&oe=6A1C0A5A)

Injecting business phone number data will pre-fill the [phone number addition screen](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/default-flow#phone-number-addition-screen):

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/466044438_1065156355155603_6571589207868521084_n.png?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=x7oLYLv9eQoQ7kNvwHRZFHP&_nc_oc=AdphoX2Q3xWMNB1K8oyd-69bEDBNs8Kbmw5x5iwDvnHsPWIFva-AJ0rAbS441tSPcLw&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=ETWjD-bM7Xyl4kOFuS759w&_nc_ss=7b20f&oh=00_Af4n0vxhOIUsoXnvOJOsE7r3Wi3FR6V-Dzb3kxhI_O8sFg&oe=6A1C3410)

Note that even if you inject data, the business customer can still edit this data using the **Edit** button, if they wish.

When a business customer completes the flow, the business portfolio information you injected will be used to create the business customer’s business portfolio and WABA.

Business object syntax

```html
setup: {
  business: {
    id: <BUSINESS_PORTFOLIO_ID>,
    name: '<BUSINESS_PORTFOLIO_NAME>',
    email: '<BUSINESS_PORTFOLIO_EMAIL_ADDRESS>',
    website: '<BUSINESS_PORTFOLIO_WEBSITE>',
    address: {
      streetAddress1: '<BUSINESS_PORTFOLIO_STREET_ADDRESS_LINE_1>',
      streetAddress2: '<BUSINESS_PORTFOLIO_STREET_ADDRESS_LINE_2>',
      city: '<BUSINESS_PORTFOLIO_CITY>',
      state: '<BUSINESS_PORTFOLIO_STATE>',
      zipPostal: '<BUSINESS_PORTFOLIO_ZIP_CODE>',
      country: '<BUSINESS_PORTFOLIO_COUNTRY>'
    },
    phone: {
      code: <BUSINESS_PORTFOLIO_COUNTRY_CALLING_CODE>,
      number: '<BUSINESS_PORTFOLIO_PHONE_NUMBER>'
    },
    timezone: '<BUSINESS_PORTFOLIO_TIME_ZONE>'
  }
}
```

Business object parameters

| Placeholder | Description | Example value |
| --- | --- | --- |
| `<BUSINESS_PORTFOLIO_ID>`<br>*Integer or null* | **Required if using an existing business portfolio, otherwise set to null or omit to create a new portfolio.**<br>Set to the business customer’s existing business portfolio ID if you want to pre-fill the screen with data already set on the business portfolio, or if you want to associate a pre-verified phone number with this portfolio.<br>If set to a portfolio ID, we will check if the business customer owns the portfolio.<br>If they own it, we will inject its existing data into the flow and ignore all other business object properties.<br>If they do not own it, we will inject `business.name`, `business.email`, `business.website`, and `address.country` values, if they are **all** set. If **any** are not set, the flow will display the default business portfolio screen instead.<br>Set to `null` (or omit the `id` property entirely) if you want to create a new business portfolio based on injected `business.name`, `business.email`, `business.website`, and `address.country` values. | `2729063490586005` |
| `<BUSINESS_PORTFOLIO_NAME>`<br>*String* | **Required if creating a new business portfolio.**<br>Business portfolio name.<br>If this name matches the name of an existing business portfolio owned by the business customer, the existing portfolio will be used instead (it will be treated as if you assigned the existing portfolio’s ID to the `id` property).<br>This name will also be used as the WhatsApp Business Account name, which is only visible in the WhatsApp Manager.<br>Maximum 100 characters. | `Wind & Wool` |
| `<BUSINESS_PORTFOLIO_EMAIL_ADDRESS>`<br>*String* | **Required if creating a new business portfolio.**<br>The business’s email address.<br>This information will appear in the **Meta Business Suite** > **Business portfolio** > **Settings** > **Business info** panel. | `support@windandwool.com` |
| `<BUSINESS_PORTFOLIO_COUNTRY_CALLING_CODE>`<br>*Integer* | **Required if injecting a business phone number.**<br>Business phone number country calling code. | `1` |
| `<BUSINESS_PORTFOLIO_PHONE_NUMBER>`<br>*String* | **Required if injecting a business phone number.**<br>Business phone number, without country calling code. | `6505559999` |
| `<BUSINESS_PORTFOLIO_WEBSITE>`<br>*String* | **Required if creating a new business portfolio.**<br>The business’s website URL.<br>This information will appear in the **Meta Business Suite** > **Business portfolio** > **Settings** > **Business info** panel. | `https://windandwool.com/` |
| `<BUSINESS_PORTFOLIO_STREET_ADDRESS_LINE_1>`<br>*String* | The business’s street address, line 1.<br>This information will appear in the **Meta Business Suite** > **Business portfolio** > **Settings** > **Business info** panel. | `1 Hacker Way` |
| `<BUSINESS_PORTFOLIO_STREET_ADDRESS_LINE_2>`<br>*String* | The business’s street address, line 2.<br>This information will appear in the **Meta Business Suite** > **Business portfolio** > **Settings** > **Business info** panel. | `Suite 1` |
| `<BUSINESS_PORTFOLIO_CITY>`<br>*String* | The business’s city address.<br>This information will appear in the **Meta Business Suite** > **Business portfolio** > **Settings** > **Business info** panel. | `Menlo Park` |
| `<BUSINESS_PORTFOLIO_STATE>`<br>*String* | The business’s state address.<br>This information will appear in the **Meta Business Suite** > **Business portfolio** > **Settings** > **Business info** panel. | `California` |
| `<BUSINESS_PORTFOLIO_ZIP_CODE>`<br>*String* | The business’s zip code address.<br>This information will appear in the **Meta Business Suite** > **Business portfolio** > **Settings** > **Business info** panel. | `94025` |
| `<BUSINESS_PORTFOLIO_COUNTRY>`<br>*String* | **Required if creating a new business portfolio.**<br>Business address [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) country code. | `US` |
| `<BUSINESS_PORTFOLIO_TIME_ZONE>`<br>*String* | The business’s time zone in<br>[UTC offset](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) format. | `UTC-07:00` |

Example Business Object

```js
setup: {
  business: {
    name: 'Wind & Wool',
    email: 'support@windandwool.com',
    website: 'https://windandwool.com/',
    address: {
      streetAddress1: '1 Hacker Way',
      streetAddress2: 'Suite 1',
      city: 'Menlo Park',
      state: 'California',
      zipPostal: '94025',
      country: 'US'
    },
    phone: {
      code: 1,
      number: '6505559999'
    },
    timezone: 'UTC-07:00'
  }
}
```

### Pre-verified phone numbers

You can inject a [pre-verified business phone number](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/pre-verified-numbers) ID into Embedded Signup, which will cause Embedded Signup to skip the [phone number addition](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/default-flow#phone-number-addition-screen) and [phone number verification](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/default-flow#phone-number-verification-screen) screens.

If you are injecting a pre-verified phone number along with business portfolio data (either creating a new portfolio or using an existing one), the [business portfolio screen](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/default-flow#business-portfolio-screen) will be pre-filled with the pre-verified number:

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/465901723_348914194949317_6482687639584528008_n.png?_nc_cat=110&ccb=1-7&_nc_sid=e280be&_nc_ohc=cJItGqRP_9sQ7kNvwHEARP2&_nc_oc=AdoCnGs511zGK2V49jvta016RJRUDqcIdZoTUECUcO0HAd6bzWe_Ig5Y-QbIQi-SIXc&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=ETWjD-bM7Xyl4kOFuS759w&_nc_ss=7b20f&oh=00_Af6hfnrK_TA_WvTjZqZS2RV6AFlgzE_6VyfjmRBu3vumLA&oe=6A1C2A72)

If you are not injecting business portfolio data along with a pre-verified number ID, the number will appear in the [WABA selection screen](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/default-flow#business-asset-selection-screen):

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/465853311_1297615144933767_5353203651542728771_n.png?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=ey2VTtx-ldkQ7kNvwFobKEA&_nc_oc=AdrsKeqDPMdbcyZaXDLODndYGvtGjJm5jns11zdxnb0R6kEo6chhSN3iwr6Vv3txfnk&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=ETWjD-bM7Xyl4kOFuS759w&_nc_ss=7b20f&oh=00_Af5wMy34enpulu6YA3lgpaEITkkzrwlqrxO3wyxCCH7o8g&oe=6A1C0CD1)

PreVerifiedPhone object syntax

```html
setup: {
  preVerifiedPhone: {
    ids: [
      '<PRE-VERIFIED_PHONE_NUMBER_ID>'
    ]
  }
}
```

Replace `<PRE-VERIFIED_PHONE_NUMBER_ID>` with a unique, pre-verified business phone number ID.

Note that although the `ids` value accepts an array of strings, if you include more than one pre-verified business phone number ID, only the first ID in the array will appear in the WABA selection screen.

Example preVerifiedPhone object

```js
setup: {
  preVerifiedPhone: {
    ids: [
      '106540352242922'
    ]
  }
}
```

### Phone profile data

You can inject the following phone number profile data. This data does not pre-fill any Embedded Signup screens, but it does populate the business phone number’s profile in the WhatsApp client, which is visible to WhatsApp users.

- Phone number profile display name
- Phone number category
- Phone number description

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/466002126_2208553189514290_7696161917337366109_n.png?_nc_cat=101&ccb=1-7&_nc_sid=e280be&_nc_ohc=txBbOMmotjcQ7kNvwEircqR&_nc_oc=AdpVtd3wj3EQfs95OT9wWAKkwGLfpsP2sbYXiii9Oaspm-mxlmTXIgz746vkGKiP8kI&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=ETWjD-bM7Xyl4kOFuS759w&_nc_ss=7b20f&oh=00_Af6pIiGsmaGYzvwergLddnAPYUf1NF79MxDm5MFSbNZCHA&oe=6A1C225F)

If you do not include this data, the category will be set to **Other**, and the business customer must set or edit their profile data on their own.

Your customers can do this in the [**WhatsApp Manager** > **Account tools** > **Phone numbers** panel](https://business.facebook.com/latest/whatsapp_manager/phone_numbers/) by selecting their business phone number and accessing the **Profile** tab. You can also provide a way for them to update it programmatically by using the [WhatsApp Business Profile API](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/whatsapp-business-profile-api#post-version-phone-number-id-whatsapp-business-profile).

Phone object syntax

```html
setup: {
  phone: {
    displayName: '<PHONE_PROFILE_DISPLAY_NAME>',
    category: '<PHONE_PROFILE_DISPLAY_CATEGORY>',
    description: '<PHONE_PROFILE_DISPLAY_DESCRIPTION>'
  }
}
```

Phone object parameters

| Placeholder | Description | Example value |
| --- | --- | --- |
| `<PHONE_PROFILE_DISPLAY_NAME>`<br>*String* | **Required.**<br>Business profile display name, visible to WhatsApp users in the WhatsApp client (see screenshot above). | `Wind & Wool` |
| `<PHONE_PROFILE_DISPLAY_CATEGORY>`<br>*String* | **Required.**<br>Business profile display category.<br>See the vertical field in the [GET /<WHATSAPP_BUSINESS_PHONE_ID>/whatsapp_business_profile](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/whatsapp-business-profile-api#fields) endpoint reference for a list of possible values. | `APPAREL` |
| `<PHONE_PROFILE_DISPLAY_DESCRIPTION>`<br>*String* | **Required.**<br>Business phone number profile description.<br>Maximum 512 characters.Rendered emojis are supported however their unicode values are not. Emoji unicode values must be Java- or JavaScript-escape encoded.Hyperlinks can be included but will not render as clickable links.Markdown is not supported. | `Bespoke artisan apparel and lifestyle goods from upcoming designers.` |

Example phone object

```js
setup: {
  phone: {
    displayName: 'Wind & Wool',
    category: 'APPAREL',
    description: 'Bespoke artisan apparel and lifestyle goods from upcoming designers.'
  }
}
```

### WhatsApp Business Accounts

If you are injecting a pre-verified phone number, you can also include a WABA ID. This will associate the pre-verified number with the existing WABA instead of with a new one that the business customer would be prompted to create as part of the flow.

WhatsAppBusinessAccount object syntax

```html
setup: {
  whatsAppBusinessAccount: {
    ids: '<WABA_ID>'
  }
}
```

Replace `<WABA_ID>` with a unique WABA ID.

Example whatsAppBusinessAccount object

This example associates a pre-verified phone number with an existing WABA.

```js
setup: {
  preVerifiedPhone: {
    ids: [
      '106540352242922'
    ]
  },
  whatsAppBusinessAccount: {
    id: [
      '432428883295692'
    ]
  }
}
```

## Examples

### New business portfolio, pre-verified number, and display profile

```js
// Launch method and callback registration
const launchWhatsAppSignup = () => {
  FB.login(fbLoginCallback, {
    config_id: '31602279155865',
    response_type: 'code',
    override_default_response_type: true,
    extras: {
      setup: {
        business: {
          name: 'Wind & Wool',
          email: 'support@windandwool.com',
          website: 'https://windandwool.com/',
          address: {
            streetAddress1: '1 Hacker Way',
            streetAddress2: 'Suite 1',
            city: 'Menlo Park',
            state: 'California',
            zipPostal: '94025',
            country: 'US'
          },
          phone: {
            code: 1,
            number: '6505559999'
          },
          timezone: 'UTC-07:00'
        },
        preVerifiedPhone: {
          ids: [
            '106540352242922'
          ]
        },
        phone: {
          displayName: 'Wind & Wool',
          category: 'APPAREL',
          description: 'Bespoke artisan apparel and lifestyle goods from upcoming designers.'
        }
      },
      featureType: '',
      sessionInfoVersion: '3',
    }
  });
}
```

### Existing business portfolio, pre-verified number, and display profile

```js
// Launch method and callback registration
const launchWhatsAppSignup = () => {
  FB.login(fbLoginCallback, {
    config_id: '31602279155865',
    response_type: 'code',
    override_default_response_type: true,
    extras: {
      setup: {
        business: {
          id: '2729063490586005'
        },
        preVerifiedPhone: {
          ids: [
            '106540352242922'
          ]
        },
        phone: {
          displayName: 'Wind & Wool',
          category: 'APPAREL',
          description: 'Bespoke artisan apparel and lifestyle goods from upcoming designers.'
        }
      },
      featureType: '',
      sessionInfoVersion: '3',
    }
  });
}
```
