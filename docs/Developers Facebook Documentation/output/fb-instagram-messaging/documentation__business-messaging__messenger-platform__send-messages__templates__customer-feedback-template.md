# Customer Feedback Template | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/templates/customer-feedback-template_

---

# Customer Feedback Template

Updated: Mar 23, 2026

This functionality is in development. Meta can change or remove this functionality at any time.

Messenger helps brands build lasting relationships through conversation. Whether you are talking to a loyal customer or someone brand new, Messenger lets businesses help customers with their pre and post purchase inquiries. Every interaction is an opportunity for the businesses to delight the customer. And, businesses now have more robust tools such as Customer Feedback Template to measure the experience they provide to their customers. With Customer Feedback Template businesses can:

1. **Increase response rates** for your customer feedback surveys with Messenger’s native customer feedback template.
2. **Aggregate customer satisfaction ratings across channels easily** with built-in Messenger templates such as Customer Satisfaction (CSAT), Net Promoter Score (NPS) and Customer Effort Score (CES) surveys.
3. **Reduce biases and inconsistency** in survey scores with optimized UX.

CSAT

CES

NPS

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/192379282_159923619437508_6420384473285754162_n.gif?_nc_cat=110&ccb=1-7&_nc_sid=e280be&_nc_ohc=M6QvhF3oxTYQ7kNvwFTOeru&_nc_oc=AdqjWNzJhkzkU8UuPfdN6p8zT51hQboW1WLKo-cJYBLPbPAvvBDEK_bPhw0nq9XRi2o&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=soWVSi3qHrER4lER-jv5Kg&_nc_ss=7b20f&oh=00_Af77WdOwUY07EDcRopYBjRYefl5uDlS4_vyd8kt3FyfeQA&oe=6A1C12B7)

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/192394645_784940269049775_2246604535870055803_n.gif?_nc_cat=111&ccb=1-7&_nc_sid=e280be&_nc_ohc=mNFbQgT2CfAQ7kNvwGDH1GO&_nc_oc=Ado3_rBWvtqKcrUy8qrKjGFy_Ow2LPZDtBi7pW8dJc_yhRvVK6mG7chKMjUZ8SixuLE&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=soWVSi3qHrER4lER-jv5Kg&_nc_ss=7b20f&oh=00_Af570Rnf4BQAtQNS5y-rY86bVRdi88J68JC8kojf-5pmPA&oe=6A1C252A)

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/192703940_158265832933445_2830539281971663398_n.gif?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=w0bU-n5xnuoQ7kNvwEeLiVf&_nc_oc=AdokrVwi_BIhaG5zVmdLL0HM_TDYBRColyI0NHpo6hoM7mV_bM4VzAdXQpULcSFCVPc&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=soWVSi3qHrER4lER-jv5Kg&_nc_ss=7b20f&oh=00_Af4axnEjtlwTp-iLWiyvkDNQzpGU4tVmuqIUWj3aX6jH2A&oe=6A1C44AC)

### Use case details:

**Allowed:**

- Post purchase feedback collection via NPS
- Post customer service conversation feedback collection via CSAT and CES

**Not allowed:**

- User research survey unrelated to a preceding interaction
- Promotional survey, any survey wording or content that are promotional in nature

## Flow Walkthrough

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/643889203_1445181520673831_2129008959093999483_n.png?_nc_cat=106&ccb=1-7&_nc_sid=e280be&_nc_ohc=XkAnxVxRdmwQ7kNvwFn3iZK&_nc_oc=AdrBzbor699dbRRXa9JiMlQOBl0asXmi50qtOAo6ChDNHkBv07gla3MNqT62Cbu0CiY&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=soWVSi3qHrER4lER-jv5Kg&_nc_ss=7b20f&oh=00_Af4r8LgoPPbLr9o7IDZ_IlC8URQTqfsaV_v1qichXSLAoQ&oe=6A1C1636)
A typical flow using the Customer Feedback template is shown above:

1. After a case has been completed the Customer Feedback template is triggered into the thread via the Send API (detailed in sections below). The template will have a title, disclaimer and a button to start the rating flow.
2. Tapping the button will trigger the bottom sheet to pop up which will have the configured scoring components.
3. A customer selects a score and can provide additional text if the business has configured the free-form text input (detailed in sections below). Once the scores are selected the Submit button pops up.
4. Customer completes feedback and taps the Submit button.
5. Feedback is sent to the business via the configured web-hook URL.
6. The bottom sheet collapses and the template in the thread will have the button replaced with Complete. An admin text will show that the feedback has been shared with the business.
7. Note: As long as the Submit button is not tapped, the customer can collapse and come back to give feedback provided the template has not expired (an expiry can be set for the template, detailed in sections below)

Details of the template and its setup is provided in the following sections.

## Score Types

We support the most commonly used scoring standards in the industry which include CSAT, NPS, CES as well as Free Form inputs.

Below are the various scoring options and their nomenclature for our API calls.

```js
Score Type: CSAT
    type: "csat "
    default_title: "How would you rate your experience with <business>?"
    options: "one_to_five", "five_stars" (default if no option set), "five_emojis"
    payload: "1", "2", "3", "4", "5"

Score Type: NPS
    type: "nps"
    default_title: "How likely are you to recommend <business> to a friend?"
    options: "zero_to_ten" (also default if no option set)
    payload: "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"

Score Type: CES
    type: "ces"
    defaut_title: "Overall, how easy was it to solve your problem today?"
    options: "one_to_seven" (also default if no option set)
    payload: "1", "2", "3", "4", "5", "6", "7"
```

**CSAT(Customer Satisfaction Score)** will be able to support views with 1 to 5, 5 stars or 5 emojis, default if none is provided would be **“five_stars”**. You can provide your own custom title for the question, if none is provided, the **default_title** will be chosen. Note: default_titles will be translated and localized to the locale of the user. Custom titles will not be translated, you would have to perform the translation yourselves if needed.

Selecting a score in any of the view formats will translate to a numeric score from 1 to 5 which will be the value that would be sent to your web-hook. That is what the payload fields show above. An example CSAT view using five_stars is shown below.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/104114593_540263709976958_4941858584795044930_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=tE5d1O402ekQ7kNvwHGJj_B&_nc_oc=AdoVbpcJ5pCV9QIYJGwNOnIZekE00isK-8c9BmR-BWhyNkhjtzyPuMkWpOUrkdm9_2U&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=soWVSi3qHrER4lER-jv5Kg&_nc_ss=7b20f&oh=00_Af4zYXdIsUiZMuYX8C0UajKGSiN8bP0VIINTSb_Ij8SerQ&oe=6A1C4191)

**NPS(Net Promoter Score)** will be able to support views with numbers from 0 to 10, default if none is provided would be **“zero_to_ten”**.. You can provide your own custom title for the question, if none is provided, the **default_title** will be chosen. Note: default_titles will be translated and localized to the locale of the user. Custom titles will not be translated, you would have to perform the translation yourselves if needed.

Selecting a score will translate to a numeric score from 0 to 10, which will be the value that would be sent to your web-hook. An example NPS view is shown below.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/103631685_656826515174329_6652044623311997817_n.png?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=xZCqKfH6tqwQ7kNvwG_889e&_nc_oc=Adp3A_pwmE4JVWZLUgQkTk8SJFBuRIULDCgxTDkHF3TKOgbMNDoh2YcwqHVYBBIvvck&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=soWVSi3qHrER4lER-jv5Kg&_nc_ss=7b20f&oh=00_Af7MOmjgF59IofLGifFh6k299TdMaicUSqy0hiY9lqVz0w&oe=6A1C2C4B)

**CES(Customer Effort Score)** will be able to support views with numbers from 1 to 7, default if none is provided would be **“one_to_seven”**. You can provide your own custom title for the question, if none is provided, the **default_title** will be chosen. Note: default_titles will be translated and localized to the locale of the user. Custom titles will not be translated, you would have to perform the translation yourselves if needed.
Selecting a score will translate to a numeric score from 1 to 7, which will be the value that would be sent to your web-hook. An example CES view is shown below.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/102468843_552125318756128_3061439580152725875_n.png?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=iqOybxuwAPsQ7kNvwGiqjx8&_nc_oc=Adqi5-gKBJlcdlXOwcl31Ci9SP611gDB3RL1oxd0k24chUNeR7aTrS1lr4HIVP6NHvQ&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=soWVSi3qHrER4lER-jv5Kg&_nc_ss=7b20f&oh=00_Af5-HxJCfUeN1T870aVqIfNVEVw6hzmLC7CgOOV0S2r3Ug&oe=6A1C3801)

**Optional Free Form Input Field**: To each of the score types you can also attach an additional free-form input. This input can be optionally set and can be used if you need text feedback in addition to the score a customer selects. Please note, a customer can choose to submit a score without providing text feedback. **Also, the form input has a character limit of 400**. Below is an example for a CSAT score type with five_stars and the additional free-from input.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/103264941_339812680321966_5268255617441433079_n.png?_nc_cat=106&ccb=1-7&_nc_sid=e280be&_nc_ohc=FHSvoedWaGIQ7kNvwHw6e1P&_nc_oc=Adp3lDXQI20r4D3xULa8gPyrPulstKkuRZHMz4ZA2k3HlJ_pHrmm79LiyphqU06sLVI&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=soWVSi3qHrER4lER-jv5Kg&_nc_ss=7b20f&oh=00_Af6iudlhuGC-t3uOUFelJfGiO3mKPxdOCP2_uadPyFD52A&oe=6A1C3F9C)

## Score Labels

For each of the scoring options you can also set the score labels to clearly define the level of the lowest value and the highest value in the template. The values that you can use are below. Please note, some values are default for certain score options, provided in parentheses below. For e.g. if no score label for CSAT is provided, it will take neg_pos as the default. You could also choose “none” if you would like to not show any labels at all.

```js
"neg_pos" = Negative - Positive (default value for CSAT)
"hard_easy" = Hard - Easy (default value for CES)
"dis_sat" = Very Dissatisfied - Very Satisfied
"unlike_like" = Very Unlikely - Very Likely (default value for NPS)
"poor_great" = Poor - Great
"none" = ""
```

For eg. a CSAT five_stars score option with *neg_pos* set would show the Negative and Positive indicators as below.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/103782756_396685794556196_3062528507879611930_n.png?_nc_cat=111&ccb=1-7&_nc_sid=e280be&_nc_ohc=r038zDqu6lYQ7kNvwFf21PJ&_nc_oc=AdqD9ZQyBLTUDxV6BtQ7ltadaUAwhd8SaH5hmvOqnE7SY6kSiD3HmgBozyjwk6zlPiI&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=soWVSi3qHrER4lER-jv5Kg&_nc_ss=7b20f&oh=00_Af66qEDgG3gmVNSzpepEclAuuVYPPXd_BIJXRVs-0axnDA&oe=6A1C2EF8)

## 24 hour restriction

The standard messaging window for sending the template to a user is 24 hours after the user’s last message. We encourage you to send the template within the 24 hour window for better customer experience and response rates. We also recognize that sometimes surveys will need to be sent outside this window. For that, you can use the [message-tag](https://developers.facebook.com/documentation/business-messaging/messenger-platform/reference/send-api#sending): **CUSTOMER_FEEDBACK** while sending the template. This tag allows you to send the template within 7 days after the user’s last message.
Please note, the tag can only be used with the customer feedback template. Use in any other form is prohibited and will fail.

## API details:

### Sending a template to the thread:

With the specific nomenclature out of the way, let us now look at the API that can be used to send the Customer Satisfaction Template to a thread.

A call should be made to the Send API with the following POST structure. Example values filled in:

```
  curl -X POST -H "Content-Type: application/json" -d '{
  "recipient": {
    "id": "<PSID>"
  },
  "message": {
    "attachment": {
      "type": "template",
      "payload": {
        "template_type": "customer_feedback",
        "title": "Rate your experience with Original Coast Clothing.", // Business needs to define.
        "subtitle": "Let Original Coast Clothing know how they are doing by answering two questions", // Business needs to define.
        "button_title": "Rate Experience", // Business needs to define.
        "feedback_screens": [{
          "questions":[{
            "id": "hauydmns8", // Unique id for question that business sets
            "type": "csat",
            "title": "How would you rate your experience with Original Coast Clothing?", // Optional. If business does not define, we show standard text. Standard text based on question type ("csat", "nps", "ces" >>> "text")
            "score_label": "neg_pos", // Optional
            "score_option": "five_stars", // Optional
            "follow_up": // Optional. Inherits the title and id from the previous question on the same page.  Only free-from input is allowed. No other title will show.
            {
              "type": "free_form",
              "placeholder": "Give additional feedback" // Optional
            }
          }]
        }],
        "business_privacy":
        {
            "url": "https://www.example.com"
         },
        "expires_in_days" : 3 // Optional, default 1 day, business defines 1-7 days
      }
    }
  }
}' "https://graph.facebook.com/v7.0/me/messages?access_token=<PAGE_ACCESS_TOKEN>"
```

### API Properties:

| Property | Type | Description |
| --- | --- | --- |
| `id` | String | *Required*. The `PSID` of the customer. |
| `attachment.type` | String | *Required*. Must be “template”. |
| `template_type` | String | *Required*. Must be “customer_feedback”. |
| `title` | String | *Required*. Defines the main title of the template that gets sent to the thread with the button to open the feedback form. **Max 65 chars allowed. No URLs.** |
| `subtitle` | String | *Required*. Defines the sub-title of the template that gets sent to the thread with the button to open the feedback form. **Max 80 chars allowed. No URLs.** |
| `button_title` | String | *Required*. Defines the button title for the button that will open the feedback form. **Max 20 chars allowed. No URLs.** |
| `feedback_screens` | Array<`Objects`> | *Required*. This is an array of objects. Each object represents 1 page. Please note we only support one page and one question per page right now. If multiple pages or multiple questions per page are set, we will throw an error back. |
| `questions` | Array<`question`> | *Required*. Each page may have up to 1 questions. This is an array of objects. Each object represents 1 question. |
| `question.id` | String | *Required*. Alphanumeric. Maximum 80 characters. Must be unique throughout the entire form. You shall use these as the unique identifiers of the questions which would be sent back in the response to help you tie context back to your system. Ids should be alpha numeric and can contain any number of underscores(_) for e.g. banjkkl__2345 is a valid id, abnj-4567 is not a valid id due to the “-”. |
| `question.type` | String | *Required*. The type of the question. Currently supported values include: “csat”, “nps”, “ces”, “free_form. Please check Score Types section above for more details. |
| `question.title` | String | *Optional*. You can provide your own custom title for the question, if none is provided, the default_title will be chosen. Please check Score Types section above for more details. Note: default_titles will be translated and localized to the locale of the user. Custom titles will not be translated, you would have to perform the translation yourselves if needed. **Min 5 chars and Max 85 chars allowed. No URLs.** |
| `question.score_label` | String | *Optional*. Field to define the level labels for low and high values. Please check Score Level Indicators section above for details. Values include ‘neg_pos’, ‘hard_easy’, ‘dis_sat’, ‘unlike_like’,’poor_great’ |
| `question.score_option` | String | *Optional*. Field to define the score selector views. For e.g. values include ‘1_to_5’, ‘five_stars’, ‘five_emojis’ for csat type. Please check Score Types section above for more details. |
| `question.follow_up` | `Object` | *Optional*. Object to set a free form input. Inherits the title and id from the previous question on the same page. Only free-from input is allowed. |
| `question.follow_up.type` | String | *Required*. Set value as ‘free_form’. |
| `question.follow_up.placeholder` | String | *Optional*. Placeholder to be shown inside the free form text input. Defaults to **“Give additional feedback”**, if none provided. **Max 65 chars allowed. No URLs.** |
| `business_privacy` | `Object` | *Required*. Object to provide your privacy policies in the template. |
| `business_privacy.url` | String | *Required*. The link to your hosted privacy policy. Example, the “privacy policy” link in the screenshots. You only need to provide the URL, and the link text will be automatically generated in the template. |
| `expires_in_days` | Integer | *Optional*. Set the time for template expiration in minutes. You can set a value between 1 to 7. Unit is days. If no value is set then a default of 1 day would be set. |

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/103260056_2779439025617991_1201279550415615271_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=isF9hzMPm4kQ7kNvwF91ZBo&_nc_oc=AdqRXiq5Qqya-c6JTkh9TtLOb0BYF9p44uGtkJR6dSib7bpRxcFl86-UOIUL77Cxnzw&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=soWVSi3qHrER4lER-jv5Kg&_nc_ss=7b20f&oh=00_Af6dcv_ackKwS36LnGiB3ezrend6LD46NUlF3A8TnpgSJg&oe=6A1C3DB4)

### Restrictions:

Please re-note the following restrictions that apply to the template.

- A template can have: 1 title + 1 scoring component + 1 free-form input box1 title + 1 scoring component1 title + 1 free-form input
- A template CANNOT have: More than 1 titleMore than 1 scoring component

Please check individual field restrictions in the API properties table above.

### Receiving data on submission:

After the template is sent in thread, you shall wait and expect the customer to fill in the information and submit it. Your web-hook server will receive a “**messaging_feedback**” event (i.e., an event that contains the submitted data) once the customer submits the feedback. Please ensure you have subscribed to the “**messaging_feedback**” webhook subscription for your app and page in the app dashboard.

Note: The customer will have the time; set in the **expires_in_days** field of the send request (default 1 day, if not set) to fill the template and submit the feedback. The form will auto-expire after the set time, after which the in-thread entry point will no longer be available.

The received feedback event will be as below:

```
  {
  "object": "page",
  "entry": [{
    "time": <timestamp>,
    "messaging": [{
      "sender": {
        "id": "<PSID>"
      },
      "recipient": {
        "id": "<page_id>"
      },
      "messaging_feedback": {
        "feedback_screens": [{
          "screen_id": 0,
          "questions": {
            "hauydmns8": {
              "type": "csat",
              "payload" : "5",
              "follow_up": {
                "type": "free_form",
                "payload" : "I am very satisfied!"
              }
            }
          }
        }]
      }
    }]
  }]
}
```

### Receive Event Properties:

| Property | Type | Description |
| --- | --- | --- |
| `time` | Integer | The timestamp when the customer submits the feedback. |
| sender `id` | String | The customer `PSID`. |
| recipient `id` | String | The page `ID` of your business page. |
| `messaging_feedback` | `Object` | The standard key of a “messaging_feedback” event. This holds an array of feedback_screens with an array of object of feedback question responses. |
| `messaging_feedback.feedback_screens` | Array<`Objects`> | Holds feedback by the customer. Each object represents a form page of your original request, with customer feedbacks. Each object has a key “screen_id”, which is the form page index, and a key “questions”, which holds your question ids and customer answers. The objects are present in the same sequence as your original request. |
| `feedback_screens.questions` | `Object` | Holds questions in a form page. Each object has the key as the question id, and the value answered by the customer. |
| `question.<id>` | String | question.id set in the Send API request, as a key to the responses submitted by the customer. |
| `question.<id>.type` | String | Defines the type of the scoring mechanism used. For e.g csat, nps, ces etc |
| `question.<id>.payload` | String | Score value selected by the customer. |
| `question.<id>.follow_up` | `Object` | Object that stores the value of the free form text input if set. |
| `follow_up.type` | String | Will be set to free_form to identify free form responses vs other responses. |
| `follow_up.payload` | String | Free form text feedback provided by the customer. |
