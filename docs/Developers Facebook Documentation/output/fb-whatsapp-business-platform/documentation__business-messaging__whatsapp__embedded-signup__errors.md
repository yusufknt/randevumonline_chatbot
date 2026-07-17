# Embedded Signup Flow Errors

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/errors_

---

# Embedded Signup Flow Errors

Updated: Feb 24, 2026

This guide helps you get acquainted with the different errors that may arise as you during [Embedded Signup flow](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/implementation) in your website or client portal.

## Abandoned flow screens

If a business customer prematurely abandons the Embedded Signup flow, the system sends a [message event](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/implementation#session-logging-message-event-listener) to the browser that spawned the flow, that indicates which screen the customer was viewing when they abandoned the flow.

The `data.current_step` property value indicates which screen the customer abandoned:

```
{
  data: {
    current_step: "<CURRENT_STEP>",
  },
  type: "WA_EMBEDDED_SIGNUP",
  event: "CANCEL",
  version: 3
}
```

| Current step value | Corresponding screen |
| --- | --- |
| `<BUSINESS_ACCOUNT_SELECTION>` | [Business portfolio screen](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/default-flow#business-portfolio-screen) |
| `<WABA_PHONE_PROFILE_PICKER>` | [WABA selection screen](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/default-flow#business-asset-selection-screen) |
| `<WHATSAPP_BUSINESS_PROFILE_SETUP>` | [WABA creation screen](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/default-flow#business-asset-creation-screen) |
| `<PHONE_NUMBER_SETUP>` | [Phone number addition screen](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/default-flow#phone-number-addition-screen) |
| `<PHONE_NUMBER_VERIFICATION>` | [Phone number verification screen](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/default-flow#phone-number-verification-screen) |
| `<PERMISSIONS>` | [Permissions review screen](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/default-flow#permissions-review-screen) |

## Business Manager account creation errors

| Error | Description |
| --- | --- |
| An error occurred while processing this request. Please try again later. | Business account creation could have failed due to various reasons. Please contact Support for further assistance.<br>Suggested Solution: Use an active Facebook account or contact Support for resolution. |
| You have reached the limit for the number of Businesses you can create at this time. | There is a limit to the number of Business Accounts that you can create.<br>Suggested Solution: Please use an existing Business Account. |
| Your Facebook account is too new to create a business account. Try again in an hour. | New Facebook accounts have to wait for some time to create a Business Manager account. Suggested Solution:<br>Use an existing active Facebook account or wait for a few hours before using your new account. The new Facebook account can be actively used during the wait period. |
| We limit how often you can post, comment or do other things in a given amount of time in order to help protect the community from spam. You can try again later. | Your Facebook account was flagged because of suspicious behavior.<br>Suggested Solution: Use an existing, active Facebook account with no prior issues. |
| You’re no longer allowed to use Facebook Products to advertise. You can’t run ads, manage advertising assets or create new ad or business accounts. | You are unable to create new Business Manager accounts due to previous suspicious behavior.<br>Suggested Solution: Use an existing, active Facebook account with no prior issues. |
| Your payment account is disabled | Your payment account was disabled due to previous suspicious behavior. |
| A User Can Only Create One Business User At One Time | You can only create a single Business Account within a given time period. Suggested Solution: Use an existing Business Account to onboard. |
| The name you chose for your business isn’t valid. Consider using xxx. | Invalid business name. Suggested Solution: Add a valid name that matches the name of your business. |

## WhatsApp Business Account creation errors

| Error | Description |
| --- | --- |
| Cannot Edit Verified Name: Name verification already in progress. | Edit name is not allowed when name verification already in progress. Suggested Solution: Please try again when the current name verification request is completed. |
| User does not have permission to create WhatsApp Business Accounts. | You do not have the Admin level permission needed to create WhatsApp Business Accounts under the Business Account you selected. Suggested Solution: Get Admin access to the Business Account to proceed or select an account you have Admin permissions for. |
| You can only create a limited number WhatsApp Business Accounts before your business and WhatsApp account verification is complete. You can create additional accounts after you are verified. | You tried to create multiple WhatsApp Business Accounts under an unverified business. Suggested Solution: You can create additional WhatsApp Business Accounts only when Business Verification and WhatsApp account checks are complete. Start Business Verification for the account by visiting Business Manager. |
| We can’t verify the Meta Business Account that you selected. Go back to the previous screen to select a different account, or go to Meta Business Manager for support. | The Meta Business Account selected doesn’t comply by our policies to use the WhatsApp Business Platform and couldn’t verified. Suggested Solution: Visit your Business Manager account to get more information about this Facebook Business Account. If your Business Verification submission is rejected, you should have received an email notification with the detailed reasons. You could try resubmitting your Business Verification if you think this was an error or create a WhatsApp Business Account using a Meta Business Account that has already been verified. |
| Something has gone wrong. You will need to contact support and try again. | This could be an intermittent issue on WhatsApp. Suggested Solution: You can retry the flow in a few minutes. |

## Phone setup errors

| Error | Description |
| --- | --- |
| Phone Number has been blocked. Please check alert prompt in<br>WhatsApp Manager Overview or follow instructions in Business Support Home. | If a phone number is blocked by WhatsApp it cannot be added to a WABA. Suggested Solution: You can find out the reason why your phone number is blocked and solutions to resolve it<br>by check alert prompt in WhatsApp Manager Overview or following instructions in [Business Support Home](https://business.facebook.com/business-support-home).<br>If you believe your phone number is blocked by error, please contact support. |
| You have already linked the maximum number of phone numbers allowed for this Business Account. Delete a phone number to continue or<br>request additional numbers. [Learn more](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers). | We currently impose phone number limit across all WhatsApp Business Account creation. Please refer to [Register Phone Number](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers#register-phone-number) for more info about these limits. Suggested Solution: Please ask business admin of the WhatsApp business account to follow steps under Delete Phone Number from a Waba in Phone Numbers doc or contact direct support to request register more than 20 phone numbers across all your WABAs. |
| This phone number already exists in your list of phone numbers. | You are trying to add a phone number that already exists in your WhatsApp Business Account. Suggested Solution: Go back into the flow or restart the flow to select the existing phone number. |
| This number is registered to an existing WhatsApp account. To use this number, disconnect it from the existing account. Then, return to this page and re-enter the number. Note: It may take up to 3 minutes for the number to become available. | The phone number was already registered on our platform (that is, WhatsApp Messenger, WhatsApp Business App, or WhatsApp Business API). Suggested Solution: [Deregister the number](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/support/migrating-phone-numbers-among-solution-partners-via-embedded-signup) if you want to use it, or register a new number. |
| Your verified name violates WhatsApp guidelines. Please edit your verified name and try again. | The name used for the phone number’s business profile does not meet our guidelines. Suggested Solution: Please reference the [Display Name guidelines](https://www.facebook.com/business/help/757569725593362) and try again. |
| Something has gone wrong. You will need to contact support and try again. | There was a problem in creating the phone number’s Business Profile. Suggested Solution: Re-enter the correct Business Profile name according to the [guidelines](https://www.facebook.com/business/help/757569725593362) and other details. |

## Phone verification errors

| Error | Description |
| --- | --- |
| Phone number ownership is already verified. | This phone number has already been verified. |
| Code couldn’t be verified: You tried to register this number too many<br>times. Try again later. | WhatsApp Business APIs only allow a limited number of phone number OTP verification attempts. Suggested Solution: Please try again later. |
| Your phone number doesn’t appear to be valid. Please double check it, or try again after 5 minutes. | An incorrect phone number was entered or numbers of this format are not supported. Suggested Solution:<br>Make sure the number is operational and verified by a telecom provider. Interactive Voice Response (IVR) numbers are not currently supported. |
| You have guessed too many times. | To block spam, the system only allows a limited number of verification attempts. Suggested Solution: You have to wait for about 12 hours before retrying. After this waiting period, come back to the flow and select existing accounts and phone numbers to verify again. |
| There was an error verifying this phone number. Please try again later. | There was a problem with the verification code. Suggested Solution: Please try again later. |
| You have requested your code too many times. | To block spam, the system only allows a limited number of verification tries. Suggested Solution: The system limits the number of times you can request a code within a certain time frame. Come back to the flow after the specified time and select existing accounts and phone numbers to request a code again. |

## Ad accounts

| Code | Description | Resolution |
| --- | --- | --- |
| 2655081 | You've reached the maximum number of ad accounts allowed for your business. To increase your ad account limit, make a payment, verify your business, and continue using our platform in good standing. | Increase your ad account limit by making a payment or completing<br>[business verification](https://www.facebook.com/business/help/2058515294227817)<br>. |
| 2655055 | Error linking WhatsApp Business Account with Ad account. Please try again. | Try again. |
| 1752004 | One or more of the ad accounts in your business manager are currently in bad standing or in review. All of your accounts must be in good standing to create or add new ad accounts. | 1. Go to<br>[Business Support Home](https://www.facebook.com/business-support-home)<br>.<br>2. Select your business.<br>3. Select your ad account to view any issues and available resolution options. |
| 1752140 | You've reached your ad account maximum. You can increase your limit by making a payment on your business account. See your ad account limit in Business Manager (go to Business Settings, then Business Info). | 1. Make a payment at<br>[Billing](https://www.facebook.com/ads/manager/account_settings/account_billing/)<br>to increase your limit.<br>2. Check your current limit in your<br>[settings](https://business.facebook.com/settings)<br>> Business Info.<br>3. Manage existing ad accounts at<br>[Meta Business Suite](https://business.facebook.com/)<br>> Accounts > Ad Accounts. |
| 2455008 | You've reached the maximum number of ad accounts allowed for a new business account. You'll be able to create more ad accounts after several weeks of following our policies or completing business verification. | 1. Continue to follow Meta policies to increase your ad account limit.<br>2. Complete<br>[business verification](https://www.facebook.com/business/help/2058515294227817) |
| 2494149 | There was an error creating your ad account. Please try again. | Try again. |
| 2446325 | This business account does not comply with our advertising policies or standards. Visit Business Support Home to resolve account issues. | Visit<br>[Business Support Home](https://www.facebook.com/business-support-home)<br>to resolve any account issues. |
| 1690214 | Your payment account is disabled. Contact the financial admin for this account or submit an appeal. | [Submit an appeal](https://www.facebook.com/help/contact/391647094929792)<br>. |

## Business account limits

| Code | Description | Resolution |
| --- | --- | --- |
| 2388098 | You can only create a limited number of WhatsApp Business Accounts before your business verification and WhatsApp account checks are complete. You can create additional accounts after you are verified. | Follow<br>[Partner-led Business Verification](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/partner-led-business-verification)<br>or submit documentation to start<br>[business verification](https://www.facebook.com/business/help/2058515294227817)<br>. |
| 1752089 | A user can only create one business account at a time. | A user can only create one business account at a time |
| 2494067 | You already have created the maximum number of WhatsApp Business Accounts allowed for this Business. Go to Meta Business Suite to delete a WhatsApp Business Account. | Go to<br>[Meta Business Suite](https://business.facebook.com/)<br>> Settings > Accounts > WhatsApp Accounts > Delete a WhatsApp Business Account. |
| 1690114 | You have reached the limit for the number of Businesses you can create at this time. | Delete a business and try again. |

## Business account names

| Code | Description | Resolution |
| --- | --- | --- |
| 1690089 | System users cannot have duplicate names. Please use another name. | Use a different name. |
| 1690091 | The name provided is not valid. | Use a different name. |
| 1690062 | The name provided is already in use. Please choose a different name. | Use a different name. |
| 2593010 | Your WABA name length exceeds max length (255 characters). Enter a shorter name. | Enter a shorter name less than or equal to 255 characters. |
| 3771014 | The link you entered is not valid. | Enter a valid link. |
| 2388010, 2388009 | Cannot edit verified name | See specific details in error message. |
| 1690090 | The name you chose for this Business Manager is not valid. Please choose another. | Use a different name. |

## CAPTCHA

| Code | Description | Resolution |
| --- | --- | --- |
| 2655091 | Please complete the CAPTCHA challenge before creating a business account. | Complete the CAPTCHA challenge before creating a business account. |

## WhatsApp Business app user onboarding

| Code | Description | Resolution |
| --- | --- | --- |
| 3441041 | The phone number you have entered is not associated with the business you selected. To continue, you need to unlink this phone number from that business or enter a different number. | 1. Enter a number associated with the business you selected.<br>2. Unlink the WhatsApp account associated with the entered number: Go to Meta Business Suite > Settings > Accounts > WhatsApp Accounts > Remove Account.<br>3. Unlink the phone number by deleting the number: Go to WhatsApp Manager > Phone Numbers tab. |
| 3441045 | Your phone number isn't eligible to connect to the WhatsApp Business Platform. | More activity on the WhatsApp Business App is needed to help determine eligibility. |
| 2655095, 2655048 | Your phone number isn’t registered with WhatsApp Business. To use this feature, register your number with the WhatsApp Business app or enter a different number. | 1.<br>[Register a phone number](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/registration)<br>through the WhatsApp Business app or WhatsApp Business API.<br>2. Enter a different number already connected to WhatsApp Business to continue. |
| 3441042 | This feature is unavailable for phone numbers from this region. Enter a phone number from a different region to continue. | Enter a phone number from a different region. |
| 2655093 | The business is already sharing this WhatsApp Business Account with a partner. Switching partners is not supported in this flow. Disconnect the current partner in the WhatsApp Business App, then return here to connect a new partner. | 1. Disconnect the current partner in the WhatsApp Business App<br>2. Connect a new partner. |
| 2655082 | The phone number is already linked to a Facebook Page. To continue, you need to unlink your account or enter a different phone number to continue. | To unlink a Facebook Page from a business portfolio:<br>1. Go to<br>[Meta Business Suite](https://business.facebook.com/)<br>.<br>2. Select your business.<br>3. Navigate to Settings > Accounts > Pages > Remove. |
| 3441049 | This phone number is already registered with the product. To use it here, disconnect it from the current account by opening the WhatsApp Business App, then go to Settings > Account > Business Platform. Select the connected business platform and tap "Disconnect". Please wait 15 minutes before retrying this process. | Disconnect it from the current account by opening the WhatsApp Business App, then go to Settings > Account > Business Platform. Select the connected business platform and tap "Disconnect". Please wait 15 minutes before retrying this process. |
| 3441030 | The phone number you entered is already registered. To proceed, enter a different phone number or deregister the current one. | Enter a different phone number or deregister the current one.<br>[About deregistering phone numbers](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/registration#register) |
| 3441047 | This feature is not available for accounts using marketing messages. Please select a different WhatsApp Business Account to continue. | Please select a different WhatsApp Business Account to continue. |
| 4563015 | Update your WhatsApp Business App to the latest version to use this phone number. | Update your WhatsApp Business App to the latest version. |
| 2655094 | Please disconnect your business platform to continue. Go to your WhatsApp Business App > Settings > Account > Business Platform. Click on the connected business platform and "Disconnect". Please wait for 15 minutes before retrying. | Go to your WhatsApp Business App > Settings > Account > Business Platform. Click on the connected business platform and "Disconnect". Please wait for 15 minutes before retrying. |

## OTP verification

| Code | Description | Resolution |
| --- | --- | --- |
| 2593037 | An error occurred while requesting your phone number verification code. Try again or reach out to support if the issue continues. | Try again or reach out to<br>[Business Support Home](https://www.facebook.com/business-support-home)<br>if the issue continues. |
| 2593039 | An error occurred while verifying your phone number verification code. Try again or reach out to support if the issue continues. | Try again or reach out to<br>[Business Support Home](https://www.facebook.com/business-support-home)<br>if the issue continues. |
| 2494158 | You have requested a verification code too many times. Please try again later. | Try again or reach out to<br>[Business Support Home](https://www.facebook.com/business-support-home)<br>if the issue continues. |
| 2388091 | Code Couldn't Be Sent | See error message for specific details. |
| 2388093 | Code Couldn't Be Verified | See error message for specific details. |

## Partner-led business verification

| Code | Description | Resolution |
| --- | --- | --- |
| 2494030 | Your business verification is in progress and must be completed before you can create a WhatsApp Business Account. Go to Meta Business Suite > Security Center > Business Verification to check the status. | Go to<br>[Meta Business Suite](https://business.facebook.com/)<br>> Security Center > Business Verification to check on your Business Verification status. |
| 2494143 | This business has started or attempted Partner-led business verification with another partner already. Currently, we do not support multiple partners performing Partner-led business verification for the same client business. The client business can either continue Partner-led business verification with the existing partner, or apply for Meta Business Verification instead. | The client business can either continue<br>[Partner-led Business Verification](https://developers.facebook.com/documentation/business-messaging/whatsapp/solution-providers/partner-led-business-verification)<br>with the existing partner, or apply for Meta Business Verification instead. |

## Phone number limits

| Code | Description | Resolution |
| --- | --- | --- |
| 3441051 | The phone number entered is invalid. Please verify it and try again or provide a new number. | Verify the number and try again. |
| 2655011 | The phone number is not linked to a WhatsApp Business Account. Verify the number or use a different one. | Verify the number and try again. |
| 2388002 | Cannot add phone number. | See error message for specific details. |

## Public test numbers

| Code | Description | Resolution |
| --- | --- | --- |
| 2655076 | You are unable to create virtual numbers. Check account status in Business Support Home. | Check account status in<br>[Business Support](https://www.facebook.com/business-support-home/)<br>home.<br>Select your business > WhatsApp Accounts > WhatsApp account to check if there are any restrictions on your account. |
| 2655005 | WhatsApp numbers are currently unavailable. Try again. | Try again. |

## Rate limiting

| Code | Description | Resolution |
| --- | --- | --- |
| 3441033, 3441046 | You have tried too many times. Try again later. | Try again later. |
| 1390006 | Warning! You are engaging in behavior that may be considered annoying or abusive by other users. Facebook's systems determined that you were going too fast when taking an action. You must significantly slow down. Further misuse of site features may result in a temporary block or your account being permanently disabled. | Try again later. |
| 1675004 | You have made too many requests in a short period of time. Please wait a few minutes before trying again. | Try again later. |
| 1390008 | We limit how often you can post, comment or do other things in a given amount of time in order to help protect the community from spam. You can try again later. | Try again later.<br>[Learn more about feature limits.](https://www.facebook.com/help/177066345680802) |

## Shared accounts

| Code | Description | Resolution |
| --- | --- | --- |
| 2655049 | This account is already shared with another partner, You can unshare this account with your partner, or create a new WhatsApp Business Account. | You can unshare this account with your partner, or create a new WhatsApp Business Account.<br>[About shared accounts.](https://www.facebook.com/business/help/524220081677109?id=2129163877102343A) |
| 2494029 | Your account wasn't able to be shared at this time. | Contact<br>[Business Support](https://www.facebook.com/business-support-home/)<br>. |
| 2593072 | The WhatsApp Business Account ID you entered (or selected) does not exist or cannot be accessed. | Please choose a different account to continue. |
| 2494028 | This account is shared with another partner. You can unshare this account or create a new WhatsApp Business account. | You can unshare this account or create a new WhatsApp Business account.<br>[About shared accounts](https://www.facebook.com/business/help/524220081677109?id=2129163877102343&ref=search_new_1) |
| 2494091 | Before you can share a WhatsApp Business Account, Business Solution Provider has to complete Business Verification. | The Business Solution Provider has to complete the business verification. |
| 2494120 | This WhatsApp Account Can't Be Shared. | Contact<br>[Business Support](https://www.facebook.com/business-support-home/)<br>. |
| 2494119 | Duplicate Service Provider Cannot Exist Under Parent WABA | This account is already shared. |

## System errors

| Code | Description | Resolution |
| --- | --- | --- |
| 1675030 | Error performing query. | Try again later. |
| 1675012 | There was a problem with this request. Try again later. | Try again later. |
| 2593030 | Your account couldn't be created. Try again later or visit Business Support Home to file a case. | Try again later or contact<br>[Business Support](https://www.facebook.com/business-support-home/)<br>. |
| 1357053 | Your account is currently restricted from performing this action, please review your account. | Please review your account. |
| 1752224 | A previous attempt to create the Business relationship is already in progress. | Try again. |
| 1752206 | The user cannot be added to the business. | Contact<br>[Business Support](https://www.facebook.com/business-support-home/)<br>. |
| 3441003 | Please retry in some time or reach support to get issue fixed. | Contact<br>[Business Support](https://www.facebook.com/business-support-home/)<br>. |
| 2593035 | Something went wrong while creating your phone number. Check that your number is correct and try again. If the issue persists, contact support for help. | Contact<br>[Business Support](https://www.facebook.com/business-support-home/)<br>. |
| 4056009 | Error occurred while setting up your account. | Contact<br>[Business Support](https://www.facebook.com/business-support-home/)<br>. |
| 1690061 | Asset already belongs to this Business Manager. | Contact<br>[Business Support](https://www.facebook.com/business-support-home/)<br>. |
| 1349246 | The following business assets were not granted the requested permissions. | Contact<br>[Business Support](https://www.facebook.com/business-support-home/)<br>. |
| 2655069 | Error Accepting Marketing Messages Lite TOS. Please try again. | Contact<br>[Business Support](https://www.facebook.com/business-support-home/)<br>. |
| 2494102 | Check the handle provided for the uploaded media in the request. | Contact<br>[Business Support](https://www.facebook.com/business-support-home/)<br>. |

## WhatsApp Business Account restricted

| Code | Description | Resolution |
| --- | --- | --- |
| 2655089, 3441040 | You cannot proceed with this operation since your WhatsApp Business account is currently restricted. To continue, select a different WhatsApp Business account or visit Business Support Home to resolve any issues with your account. | Visit<br>[Business Support](https://www.facebook.com/accountquality/advertising_access?enforcement=1)<br>, find your account and identify if there are any issues with the account. Submit an appeal if there is one. |
| 2388107 | To add a phone number, you'll need to address any restrictions on this account. To resolve this, visit Business Support Home. | See details in the<br>[Business Support](https://www.facebook.com/accountquality/advertising_access?enforcement=1) |
| 2859015 | You have been temporarily blocked from performing this action. | Contact<br>[Business Support](https://www.facebook.com/business-support-home/)<br>to see restrictions on your accounts. |
| 1784028 | Your business is prohibited from advertising, including pixel creation. | Contact<br>[Business Support](https://www.facebook.com/business-support-home/)<br>to see restrictions on your accounts. |
| 1404163 | You're no longer allowed to use Meta technologies to advertise. You can't run ads, manage advertising assets, or create new ad accounts or business portfolios. | See details in the<br>[Business Support Home](https://www.facebook.com/accountquality/advertising_access?enforcement=1) |

## Pages

| Code | Description | Resolution |
| --- | --- | --- |
| 1690181 | You cannot claim this page. You are not an admin on this page or you only have access via an agency. | Get a page admin to add you as an admin to the page or ask the page admin to complete this action. |
| 1752069 | As a security precaution, you aren't allowed to approve a request to add this Page to a Business Manager account because you were added as an admin on the Page less than a week ago. | Try again later. |

## Authentication

| Code | Description | Resolution |
| --- | --- | --- |
| 2859009 | To continue working in your account, you'll need to enable two-factor authentication. Navigate to the<br>[business settings page](https://business.facebook.com/settings/)<br>to set up now. | Follow the link in the error description. |
| 2859043 | We noticed you're attempting to access this business from a new device or location. To help keep your account safe, please refresh this page to start verification, or navigate to the business home page and verify when prompted. | Follow the link in the error description. |
| 2136001 | A challenge is required to process this secured action. | Follow the link in the error description. |
| 4612001 | You need to set up two-factor authentication in your profile settings. Go to Facebook Account Center, then select password and security settings to make your changes. | Follow the link in the error description. |
