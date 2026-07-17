# Checkout button templates | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/checkout-button-templates_

---

# Checkout button templates

Updated: Dec 12, 2025

Checkout button templates are marketing templates that can showcase one or more products along with corresponding checkout buttons that WhatsApp users can use to make purchases without leaving the WhatsApp client.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/461864193_1053025166222560_1984323495828319066_n.png?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=FmfxIzef9PsQ7kNvwFMwLMO&_nc_oc=AdoWrvT_GTuqHlkZQsriAaxoOMMZe4O9PQnj2iliQnSqvrPFQPdK-qgUMS6WqfIPbjQ&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=Pr5we6IJ2Azp5Jw_vRULyQ&_nc_ss=7b20f&oh=00_Af79yopuqcuvOXD3-s5VwTEMTrPE1IASz3fmmNSyAL9D8w&oe=6A1C1C7C)

## Single products

Checkout button templates can show a single product image or video header, along with message body text, message footer, a single checkout button, and up to 9 quick-reply buttons.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/461716389_980926930508984_4731907095777942335_n.png?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=CGp7GMEqwFgQ7kNvwHRrkkL&_nc_oc=AdqWgI4SqrWGWSBzbx8-TI0BF6kFzEWMXiE5YfKPPUY9j30t82GKRbFT08wwSboYI40&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=Pr5we6IJ2Azp5Jw_vRULyQ&_nc_ss=7b20f&oh=00_Af7NiytLwa2z1Wzgo4yClNKBVBhMtHJnIdMwY0snqiRrBw&oe=6A1C34B7)

WhatsApp users who tap the button will see details of the order:

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/461898315_2387340868275631_829544685895208004_n.png?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=2AKRqt-jrDUQ7kNvwErU912&_nc_oc=Adq8dwfZQxs2iLS6ySaDHAICpMZbs5dGShDdEVtA460eqAjlme16H4P-rEebBrUQJDY&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=Pr5we6IJ2Azp5Jw_vRULyQ&_nc_ss=7b20f&oh=00_Af6vnDD2IkjZmiz_HM5WCKP6B2v66BNdLNuspeXmgLDXsQ&oe=6A1C280B)

Users can proceed by selecting shipping information provided by you (if you know their information and supplied it in the send message payload)...

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/461872330_923861569791765_2740463248926355079_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=dBYgMV8v9HsQ7kNvwEEeRWV&_nc_oc=Adoeeq1tS83Fe5lzfL1_RELL2sW2dPJAVQG7hLHg3iR2x3RBFdrskAgfnWzWPLKEXSQ&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=Pr5we6IJ2Azp5Jw_vRULyQ&_nc_ss=7b20f&oh=00_Af7pFzQGvDwI9NYnO8iomQK-VqcIINbpjQVQCmIGoofydA&oe=6A1C17AA)

... or can add their own shipping information:

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/461774395_433815155940531_3266765354702751375_n.png?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=BDwAWT72S68Q7kNvwGYBOLp&_nc_oc=Adp7QjBn3YnWi1VvsosqBDoGl-hoNirjZU9DsMZ6zo8QCIXF4VB8rKciLFl4kd3hOlE&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=Pr5we6IJ2Azp5Jw_vRULyQ&_nc_ss=7b20f&oh=00_Af6RWQYJi8pp04BeFa_2hVO89kBxySUXLWaSLtAjbRXYjA&oe=6A1C2A99)

## Enabling coupons, realtime inventory, and pricing updates

Enabling coupons, realtime inventory and pricing updates is currently in beta and only available to India businesses and WhatsApp users with an India country calling code. Please reach out to whatsappindia-bizpayments-support@meta.com to know more.

To enable coupons, realtime inventory and pricing updates, you can set up a checkout endpoint that can exchange data in real time to update the order on the WhatsApp client. It enables businesses to receive the shipping address and offers coupons based on the order and allows users to apply the coupon. It also enables businesses to validate inventory and serviceability on the order before the user completes the checkout.

Setting up the checkout endpoint consists of the following steps and it’s the same method that [WhatsApp Flows endpoint](https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/guides/implementingyourflowendpoint#implementing-endpoint-for-flows) uses to share the data with WhatsApp clients.

- Create a key pair and upload and sign the public key using the [Cloud API](https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/cloud-api/reference/whatsapp-business-encryption#set-business-public-key) .
- [Setup the endpoint](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/checkout-button-templates#setup_the_endpoint)
- [Implement Payload Encryption/Decryption](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/checkout-button-templates#implement_encryption_decryption)
- [Link the checkout endpoint with payment configuration](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/checkout-button-templates#link_checkout_endpoint)
- [Implement checkout endpoint logic](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/checkout-button-templates#implement_checkout_logic)

### Set up the endpoint

WhatsApp client makes a HTTPS request to exchange the data with the business endpoint. You should make sure the endpoint is configured probably to accept the request and link the endpoint url with the [payment configuration](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/pg#link-your-payment-account):

```html
https://business.com/checkout
```

Your server must be enabled to receive and process `POST` requests, use `HTTPS` and have a valid TLS/SSL certificate installed. This certificate does not have to be used in payload encryption/decryption.

### Implement Encryption/Decryption

The body of each request contains the encrypted payload and has the following form:

Sample endpoint request syntax

```html
{
  encrypted_flow_data: "<ENCRYPTED_FLOW_DATA>",
  encrypted_aes_key: "<ENCRYPTED_AES_KEY>",
  initial_vector: "<INITIAL_VECTOR>"
}
```

| Parameter | Description |
| --- | --- |
| `encrypted_flow_data`<br>string | **Required.**<br>The encrypted request payload. |
| `encrypted_aes_key`<br>string | **Required.**<br>The encrypted 128-bit AES key. |
| `initial_vector`<br>string | **Required.**<br>The 128-bit initialization vector. |

After processing the decrypted request, create a response and encrypt it before sending it back to the WhatsApp client. Encrypt the payload using the AES key received in the request and send it back as a Base64 string.

You can refer to examples of how to [decrypt and encrypt](https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/guides/implementingyourflowendpoint#request-decryption-and-encryption).

If a request can not be decrypted, the endpoint should return HTTP 421 response status code (see [Business Endpoint Error Codes](https://developers.facebook.com/documentation/business-messaging/whatsapp/flows/reference/error-codes#endpoint_error_codes) for more details).

Sample endpoint response

```curl
curl -i -H "Content-Type: application/json" -X POST -d '{
"encrypted_flow_data":"4Wor0bpfvrNqnkH+XQZLn3HnU2Zi7hG\\/UHjISS93Fzn9J7youssaLeXlNUH",
"encrypted_aes_key":"ufA0fXD1Wz...",
"initial_vector":"G\\/1rq1naEOMR4TJHFvIs\\/Q==."
}' 'https://business.com/checkout'

HTTP/2 200
content-type: text/plain
content-length: 232
date: Wed, 06 Jul 2022 14:03:03 GMT

yZcJQaH3AqfzKgjn64vAcASaJrOMN27S6CESyU68WN/cDCP6abskoMa/pPjszXGKyyh/23lw84HW6ZilMfU6KL3j5AWwOx6GWNwtq8Aj7gz/Y7R+LccmJWxKo2UccMu5xJlduIFlFlOS1gAnOwKrk8wpuprsi4jAOspw3xO2uh3J883aC/csu/MhRPiYCaGGy/tTNvVDmb2Gw1WXFmpvLsZ/SBrgG0cDQJjQzpTO
```

### Link the checkout endpoint with payment configuration

The business should have payment gateway based [payment configuration](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/pg#link-your-payment-account) and reach out to whatsappindia-bizpayments-support@meta.com to enable the WhatsApp business account for checkout endpoint linking with with payment configuration.

Prior to linking the checkout endpoint, you should create a [payment configuration](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/pg#link-your-payment-account) and link with the payment gateway account. We advise you to use the linked payment configuration only with checkout button template integration.

You can achieve the endpoint linking with payment configuration by following [Onboarding API’s - Link data endpoint](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/onboarding-apis#link-or-update-data-endpoint)

### Implement checkout endpoint logic

WhatsApp checkout endpoint integration inherits the ‘data_exchange’ similar to Flows and supports a set of subactions based on the user interaction and passes the relevant information in each of these actions to allow businesses to provide user specific coupons and enable businesses to update the pricing information accordingly.

| Sub Action | Method | Description |
| --- | --- | --- |
| `get_coupons` | Request | When users click on a savings offer CTA, WhatsApp passes [order parameters](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/pg#paramobject) excluding the [payment settings](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/pg#paymentsettingsobject). It also passes the `user phone number` as an input parameter.<br>`{<br> "input":<br> {<br> "user_id": "user_phone_number"<br> }<br>}`<br>Refer [get coupons request](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/checkout-button-templates#get_coupon_request) example to understand the order and input parameters |
|  | Response | Checkout endpoint expected to pass the list of coupon information, such as code, id and description.<br>`{<br> "coupons":<br> [<br> {<br> "code": "coupon_code",<br> "id": "coupon_id",<br> "description": "coupon_description"<br> }<br> ]<br><br>}`<br>Refer [get coupons response](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/checkout-button-templates#get_coupon_response) example to understand the expected response. |
| `apply_coupon` | Request | When users select or enter a coupon, WhatsApp passes [order parameters](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/pg#paramobject) excluding the [payment settings](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/pg#paymentsettingsobject). It also passes the `user phone number` and information about the coupon to be applied as an input parameter.<br>`{<br> "input":<br> {<br> "user_id": "user_phone_number",<br> "coupon":<br> {<br> "code": "WELCOME70"<br> }<br> }<br>}`<br>Refer [apply coupon request](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/checkout-button-templates#apply_coupon_request) example to understand the order and input parameters |
|  | Response | Checkout endpoint expected to update the item and order pricing in [order parameters](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/pg#paramobject) and attach the coupon with the order<br>Refer to [apply coupon response](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/checkout-button-templates#apply_coupon_response) example to understand the expected response. |
| `remove_coupon` | Request | When users try to remove an applied coupon, WhatsApp passes [order parameters](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/pg#paramobject) excluding the [payment settings](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/pg#paymentsettingsobject). It also passes the `user phone number` as an input parameter.<br>`{<br> "input":<br> {<br> "user_id": "user_phone_number"<br> }<br>}`<br>Refer [remove coupon request](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/checkout-button-templates#remove_coupon_request) example to understand the expected response. |
|  | Response | Checkout endpoint expected to update the item and order pricing in [order parameters](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/pg#paramobject) and remove the coupon attached with the order.<br>Refer [remove coupon response](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/checkout-button-templates#remove_coupon_response) example to understand the expected response. |
| `apply_shipping` | Request | When users try to submit a shipping address, WhatsApp passes [order parameters](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/pg#paramobject) excluding the [payment settings](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/pg#paymentsettingsobject). It also passes the `user phone number` and shipping information as an input parameter.<br>`{<br> "input":<br> {<br> "user_id": "user_phone_number"<br> }<br>}`<br>Refer to the [apply shipping request](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/checkout-button-templates#apply_shipping_request) example to understand the expected response. |
|  | Response | Checkout endpoint expected to update the item and shipping pricing in [order parameters](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/pg#paramobject).<br>Refer to the [apply shipping response](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/checkout-button-templates#apply_shipping_response) example to understand the expected response. |

We have created a [checkout endpoint example](https://github.com/WhatsApp/WhatsApp-Checkout-Button-Template-Endpoint) in Node.js that you can clone (remix) on Glitch to create your own endpoint and quickly prototype your checkout logic. Follow the instructions in the [README.md](https://github.com/WhatsApp/WhatsApp-Checkout-Button-Template-Endpoint/blob/main/README.md) file to get started. Using Glitch is entirely optional. You can clone the example code from Glitch and run it in any environment you prefer.

Upon completing the above steps, when business sends the checkout template with the linked payment configuration, WhatsApp enables the coupons, realtime inventory and pricing updates and allows users to apply coupons and share shipping addresses.

When enabled the `Apply a savings offer` will appear in the order summary screen

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/566208922_1339318471260137_8031940610378006006_n.jpg?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=RQlU2uOmBTkQ7kNvwGbnidN&_nc_oc=AdoUW_9ISZ2wkZBZ1DCEHZ1eDsGfgLMdjQvkH4mNXpKNLjjzabab7a9p3FeZNgErDqc&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=Pr5we6IJ2Azp5Jw_vRULyQ&_nc_ss=7b20f&oh=00_Af5BuJWBDgIGzC_UtxOjW298AFqa2MeaV1apA63g7yNyvA&oe=6A1C32E0)

User can click on `Apply a savings offer` to explore the coupons, at this point WhatsApp makes `get_coupons` request to fetch the list coupons based on the passed order and `user phone number` information.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/560013461_1339318424593475_5113635030322783543_n.jpg?_nc_cat=111&ccb=1-7&_nc_sid=e280be&_nc_ohc=4aIFcAEiGeIQ7kNvwH-yAR3&_nc_oc=AdrlQl-E09n69cNGiYhyz_NdlT0-3chykzloT-uWAZvBbwS3AQAIIK99rH77tTf37aU&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=Pr5we6IJ2Azp5Jw_vRULyQ&_nc_ss=7b20f&oh=00_Af706KVZVcC2N3CY7I_iO40TnvJIEmrmZmdetHoUZfxCaQ&oe=6A1C2BEB)

When the user tries to apply a coupon, WhatsApp makes `apply_coupon` and allow businesses to update the order or item pricing based on the selected coupon.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/560498579_1339318444593473_8466127193448601632_n.jpg?_nc_cat=110&ccb=1-7&_nc_sid=e280be&_nc_ohc=HcDzD8pQZxgQ7kNvwGYA9gc&_nc_oc=AdopjdJmoURQFua9p9CAJCSwfWAkirp9pp5ZJPq-KKdXCH8gBOlk_kQNKLyPhscZ6FU&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=Pr5we6IJ2Azp5Jw_vRULyQ&_nc_ss=7b20f&oh=00_Af4q1HMk_eXcaHrF3Kri3tp_5Y2xctpBQEiB_tF1L2GEJA&oe=6A1C09B9)

Similar to coupons, user can share the shipping address by clicking on `Add shipping address` and select the addresses saved with the businesses or add new address. WhatsApp makes `apply_shipping` request when user tries to submit the address and allow businesses to check inventory and logistics based on the address provided.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/561725167_1339318187926832_1852627850653076539_n.jpg?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=dRzWZ2cG3EYQ7kNvwE-1F4p&_nc_oc=AdoiM07KpT-Jnj6-jVYX2nutVxm9Mm8plKWL5FBPLF-tDYylvu_ChPCxzSWLQCttd0A&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=Pr5we6IJ2Azp5Jw_vRULyQ&_nc_ss=7b20f&oh=00_Af6Z9X81X3PE7uhwXFtifbQl-UnkKqZLqdPJUJ1G8awnTw&oe=6A1C3092)![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/560467967_1339318057926845_5662577297785116122_n.jpg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=QNXR30F5GYsQ7kNvwH5S5Pj&_nc_oc=AdpzeNPh1AHKBswC00j8yHAMpwHUesUgIpPx_mRCHlK77L_SJWAKPqdYcs_Ov1T9dU4&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=Pr5we6IJ2Azp5Jw_vRULyQ&_nc_ss=7b20f&oh=00_Af5SLDlt2zk7_vj0M2y0p87Ad5Pmotv-jutq6MgtVZB2BQ&oe=6A1C2CE4)

Users can then continue to place the order using their preferred payment method set up in the WhatsApp client:

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/461783140_456335920794267_694558377704466245_n.png?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=pHoqYkT57bEQ7kNvwE4GGTd&_nc_oc=Adqbeyqz7jx3LQXISt0z-dd4B_-eXyol0PBTHL7_Qs5jZ14NLET3jL25SOjbtVm8YJc&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=Pr5we6IJ2Azp5Jw_vRULyQ&_nc_ss=7b20f&oh=00_Af78hMufsZbWKNPcwQu2B7_0JahnOCsGTnM5XSux_OI5rA&oe=6A1C27DD)

Once the order is processed, a [payment webhook](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/pg#step-2--receive-webhook-about-transaction-status) is triggered.

## Multiple products

You can create a [media card carousel template](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/marketing-templates/media-card-carousel-templates) that showcases up to 10 products in a card carousel, each with their own checkout button. To do this, simply create a media card carousel template as you normally would, but replace one of the buttons with a [checkout button](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/checkout-button-templates#checkout-buttons), and make sure that it is the first button in the card.

Checkout buttons in media card carousel templates trigger the same order and payment flow as checkout buttons in templates that showcase a single product.

## Checkout buttons

Each checkout button in a template must correspond to a single product. Checkout buttons, when creating a template, must have the following non-customizable syntax:

```json
{
  "type": "order_details",
  "text": "Buy now"
}
```

Note that this is simply a button definition. The actual details about the product that maps to this button are included when you [send the template](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/checkout-button-templates#send-a-checkout-button-template) in a template message. For example:

```json
{
  "type": "button",
  "sub_type": "order_details",
  "index": 0,
  "parameters": [
    {
      "type": "action",
      "action": {
        "order_details": {
          "reference_id": "abc.123_xyz-1",
          "type": "physical-goods",
          "currency": "INR",
          "payment_settings": [
            {
              "type": "payment_gateway",
              "payment_gateway": {
                "type": "razorpay",
                "configuration_name": "prod-razor-pay-config-05"
              }
            }
          ],
          "shipping_info": {
            "country": "IN",
            "addresses": [
              {
                "name": "Nidhi Tripathi",
                "phone_number": "919000090000",
                "address": "Bandra Kurla Complex",
                "city": "Mumbai",
                "state": "Maharastra",
                "in_pin_code": "400051",
                "house_number": "12",
                "tower_number": "5",
                "building_name": "One BKC",
                "landmark_area": "Near BKC Circle"
              }
            ]
          },
          "order": {
            "items": [
              {
                "amount": {
                  "offset": 100,
                  "value": 200000
                },
                "sale_amount": {
                  "offset": 100,
                  "value": 150000
                },
                "name": "Blue Elf Aloe",
                "quantity": 1,
                "country_of_origin": "India",
                "importer_name": "Lucky Shrub Imports and Exports",
                "importer_address": {
                  "address_line1": "One BKC",
                  "address_line2": "Bandra Kurla Complex",
                  "city": "Mumbai",
                  "zone_code": "MH",
                  "postal_code": "400051",
                  "country_code": "IN"
                }
              }
            ],
            "subtotal": {
              "offset": 100,
              "value": 150000
            },
            "shipping": {
              "offset": 100,
              "value": 20000
            },
            "tax": {
              "offset": 100,
              "value": 10000
            },
            "discount": {
              "offset": 100,
              "value": 15000,
              "description": "Additional 10% off"
            },
            "status": "pending",
            "expiration": {
              "timestamp": "1726627150"
            }
          },
          "total_amount": {
            "offset": 100,
            "value": 165000
          }
        }
      }
    }
  ]
}
```

If you are sending a [media card carousel template](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/marketing-templates/media-card-carousel-templates) (which can have two or more products), each checkout button must be defined in the template, and the item details that map to each button must be included when sending the template.

## Creating checkout button templates

Use the [**POST /<WHATSAPP_BUSINESS_ACCOUNT_ID>/message_templates**](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-account/template-api#post-version-waba-id-message-templates) endpoint to create a template that uses a checkout button.

### Request syntax

```json
POST /<WHATSAPP_BUSINESS_ACCOUNT_ID>/message_templates
```

### Post body

The post body below is for a checkout button template that shows a single button. See the [Media Card Carousel Templates](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/marketing-templates/media-card-carousel-templates) document to see carousel template post body syntax.

```json
{
  "name": "<TEMPLATE_NAME>",
  "language": "<TEMPLATE_LANGUAGE>",
  "category": "marketing",
  "components": [
    {
      "type": "header",
      "format": "<MESSAGE_HEADER_FORMAT>",
      "example": {
        "header_handle": [
          "<MESSAGE_HEADER_ASSET_HANDLE>"
        ]
      }
    },
    {
      "type": "body",
      "text": "<MESSAGE_BODY_TEXT>",
      "example": {
        "body_text": [
          [
            "<MESSAGE_BODY_TEXT_VARIABLE_EXAMPLE>",
            "<MESSAGE_BODY_TEXT_VARIABLE_EXAMPLE>"
          ]
        ]
      }
    },

    /* Footer component is optional */
    {
      "type": "footer",
      "text": "<MESSAGE_FOOTER_TEXT>"
    },

    {
      "type": "buttons",
      "buttons": [
        {
          "type": "order_details",
          "text": "Buy now"
        },

        /* Quick-reply buttons are optional; up to 9 permitted */
        {
          "type": "quick_reply",
          "text": "<QUICK_REPLY_BUTTON_LABEL_TEXT>"
        }
      ]
    }
  ]
}
```

### Post body parameters

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<MESSAGE_BODY_TEXT>`<br>*String* | **Required.**<br>Message body text. Supports variables.<br>Maximum 1024 characters. | `Hi {{1}}! The {{2}} is back in stock! Order now before it's gone!` |
| `<MESSAGE_BODY_TEXT_VARIABLE_EXAMPLE>`<br>*String* | **Required if message body text string uses variables.**<br>Message body text example variable string(s). Number of strings must match the number of variable placeholders in the message body text string.<br>If message body text uses a single variable, `body_text` value can be a string, otherwise it must be an array containing an array of strings. | `Pablo` |
| `<MESSAGE_FOOTER_TEXT>`<br>*String* | **Required if using a message footer.**<br>Message footer text string.<br>60 characters maximum. | `Tap 'Stop' below to stop back-in-stock reminders.` |
| `<MESSAGE_HEADER_ASSET_HANDLE>`<br>*String* | **Required if using a non-text media header.**<br>Uploaded media asset handle. Use the [Resumable Upload API](https://developers.facebook.com/docs/graph-api/guides/upload) to generate an asset handle.<br>Media assets are automatically cropped to a wide ratio based on the WhatsApp user’s device. | `4::anBlZw==:ARa525ZJ1g0J-8egeiRvb4Z4r9RSi9qeKF7-wXsUiaDFsll5CKbu5H7h_9mTW0TDfA8LEGHC4bAeXtJJiVQADMp5Ooe2huQlhpBxMadJiu3qVg:e:1724535430:634974688087057:100089620928913:ARaQoFQMm6BlbI3MYo4` |
| `<MESSAGE_HEADER_FORMAT>`<br>*String* | **Required.**<br>Message header format. Value can be `image` or `video`. | `image` |
| `<QUICK_REPLY_BUTTON_LABEL_TEXT>`<br>*String* | **Required if using a quick-reply button.**<br>Quick-reply button label text.<br>Maximum 25 characters. | `Stop` |
| `<TEMPLATE_LANGUAGE>`<br>*String* | **Required.**<br>Template [language and locale code](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/supported-languages). | `en_US` |
| `<TEMPLATE_NAME>`<br>*String* | **Required.**<br>Template name.<br>Maximum 512 characters. | `item_back_in_stock_v1` |

### Example request

This example request creates a checkout button template with a single image message header, message body text that uses two variables, a footer, a single checkout button, and a quick-reply button.

```curl
curl 'https://graph.facebook.com/v25.0/102290129340398/message_templates' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "name": "item_back_in_stock_v1",
  "language": "en_US",
  "category": "marketing",
  "components": [
    {
      "type": "header",
      "format": "image",
      "example": {
        "header_handle": [
          "3:NDU..."
        ]
      }
    },
    {
      "type": "body",
      "text": "Hi {{1}}! The {{2}} is back in stock! Order now before it\'s gone!",
      "example": {
        "body_text": [
          [
            "Pablo",
            "Blue Elf Aloe"
          ]
        ]
      }
    },
    {
      "type": "footer",
      "text": "Tap \'Stop\' below to stop back-in-stock reminders."
    },
    {
      "type": "buttons",
      "buttons": [
        {
          "type": "order_details",
          "text": "Buy now"
        },
        {
          "type": "quick_reply",
          "text": "Stop"
        }
      ]
    }
  ]
}'
```

## Send a checkout button template

Once your checkout button template or carousel template has been approved, you can send it in a template message.

### Request syntax

Use the [**POST /<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>/messages**](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api) endpoint to send an approved checkout button template or carousel template to a WhatsApp user.

```json
POST /<WHATSAPP_BUSINESS_PHONE_NUMBER_ID>/messages
```

### Post body

This post body syntax is for a checkout button template. See [Sending Media Card Carousel Templates](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/marketing-templates/media-card-carousel-templates) for media card carousel template post body payload syntax.

```json
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "<WHATSAPP_USER_PHONE_NUMBER>",
  "type": "template",
  "template": {
    "name": "<TEMPLATE_NAME>",
    "language": {
      "policy": "deterministic",
      "code": "<TEMPLATE_LANGUAGE>"
    },
    "components": [
      {
        "type": "header",
        "parameters": [
          {
            "type": "<MESSAGE_HEADER_FORMAT>",
            "<MESSAGE_HEADER_FORMAT>": {
              "id": "<MESSAGE_HEADER_ASSET_ID>"
            }
          }
        ]
      },
      {
        "type": "body",
        "parameters": [
          {
            <MESSAGE_BODY_TEXT_VARIABLE>
          },
          {
            <MESSAGE_BODY_TEXT_VARIABLE>
          }
        ]
      },
      {
        "type": "button",
        "sub_type": "order_details",
        "index": 0,
        "parameters": [
          {
            "type": "action",
            "action": {
              "order_details": {
                "reference_id": "<REFERENCE_ID>",
                "currency": "INR",
                "type": "<PRODUCT_TYPE>",
                "payment_settings": [
                  {
                    "type": "payment_gateway",
                    "payment_gateway": {
                      "type": "<PAYMENT_GATEWAY_NAME>",
                      "configuration_name": "<PAYMENT_GATEWAY_CONFIGURATION_NAME>"
                    }
                  }
                ],

                /* "shipping_info" required for physical-goods type, else omit */
                "shipping_info": {
                  "country": "IN",
                  "addresses": [

                    /* object required if you know recipient's address, otherwise omit (i.e., set "addresses" to an empty array) */
                    {
                      "name": "<SHIPPING_INFO_NAME>",
                      "phone_number": "<SHIPPING_INFO_PHONE_NUMBER>",
                      "address": "<SHIPPING_INFO_ADDRESS>",
                      "city": "<SHIPPING_INFO_CITY>",
                      "state": "<SHIPPING_INFO_STATE>",
                      "in_pin_code": "<SHIPPING_INFO_INDIA_PIN>",
                      "landmark_area": "<SHIPPING_INFO_LANDMARK_AREA>",
                      "house_number": "<SHIPPING_INFO_HOUSE_NUMBER>",
                      "tower_number": "<SHIPPING_INFO_TOWER_NUMBER>",
                      "building_name": "<SHIPPING_INFO_BUILDING_NAME>"
                    }

                  ]
                },

                "order": {
                  "items": [
                    {
                      "amount": {
                        "offset": 100,
                        "value": <ITEM_PRICE>
                      },

                      /* "sale_amount" optional */
                      "sale_amount": {
                        "offset": 100,
                        "value": <SALE_PRICE>
                      },

                      "name": "<ITEM_NAME>",
                      "quantity": <ITEM_QUANTITY>,
                      "country_of_origin": "<ITEM_COUNTRY_OF_ORIGIN>",
                      "importer_name": "<IMPORTER_NAME>",
                      "importer_address": {
                        "address_line1": "<IMPORTER_ADDRESS_LINE_1>",
                        "address_line2": "<IMPORTER_ADDRESS_LINE_2>",
                        "city": "<IMPORTER_CITY>",
                        "zone_code": "<IMPORTER_ZONE_CODE>",
                        "postal_code": "<IMPORTER_POSTAL_CODE>",
                        "country_code": "IN"
                      }
                    }
                  ],
                  "subtotal": {
                    "offset": 100,
                    "value": <SUBTOTAL_AMOUNT>
                  }
                  "shipping": {
                    "offset": 100,
                    "value": <SHIPPING_AMOUNT>
                  },
                  "tax": {
                    "offset": 100,
                    "value": <TAX_AMOUNT>,
                    "description": "<TAX_DESCRIPTION>"
                  },

                  /* "discount" optional */
                  "discount": {
                    "offset": 100,
                    "value": <DISCOUNT_AMOUNT>,
                    "description": "<DISCOUNT_DESCRIPTION>"
                  },
                  "status": "pending",

                  /* "expiration" optional */
                  "expiration": {
                    "timestamp": "<EXPIRATION_TIMESTAMP>"
                  }
                },
                "total_amount": {
                  "offset": 100,
                  "value": <TOTAL_AMOUNT>
                }
              }
            }
          }
        ]
      }
    ]
  }
}
```

### Post body parameters

| Placeholder | Description | Example Value |
| --- | --- | --- |
| `<DISCOUNT_AMOUNT>`<br>*Integer* | **Required if using a discount.**<br>Discount amount, multiplied by discount.offset value.<br>For example, to represent a discount of ₹2, the value would be `200`.<br>Discount amount applies to the order subtotal. | `15000` |
| `<DISCOUNT_DESCRIPTION>`<br>*String* | **Optional.**<br>Discount description.<br>Maximum 60 characters. | `Additional 10% off` |
| `<EXPIRATION_TIMESTAMP>`<br>*String* | **Required if using an order expiration.**<br>UTC timestamp indicating when we should disable the **Buy now** button. The timestamp will be used to generate a text string that appears at the bottom of the **Order details** window. For example:<br>*This order expires on September 30, 2024 at 12:00 PM.*<br>WhatsApp users who view the message after this time will be unable to purchase the item using the checkout button.<br>Values must represent a UTC time at least 300 seconds from when the send message request is sent to us. | `1726692927` |
| `<IMPORTER_ADDRESS_LINE_1>`<br>*String* | **Required.**<br>Importer address, line 1 (door, tower, number, street, etc.).<br>Maximum 100 characters. | `One BKC` |
| `<IMPORTER_ADDRESS_LINE_2>`<br>*String* | **Optional.**<br>Importer address, line 2 (landmark, area, etc.).<br>Maximum 100 characters. | `Bandra Kurla Complex` |
| `<IMPORTER_CITY>`<br>*String* | **Required.**<br>Importer city.<br>Maximum 120 characters. | `Mumbai` |
| `<IMPORTER_NAME>`<br>*String* | **Required.**<br>Importer name.<br>Maximum 200 characters. | `Lucky Shrub Imports and Exports` |
| `<IMPORTER_POSTAL_CODE>`<br>*String* | **Required.**<br>Importer 6-digit postal index number.<br>Maximum 6 digits. | `400051` |
| `<IMPORTER_ZONE_CODE>`<br>*String* | **Required.**<br>Importer two-letter zone code. | `MH` |
| `<ITEM_COUNTRY_OF_ORIGIN>`<br>*String* | **Required.**<br>Item’s country of origin.<br>Maximum 100 characters. | `India` |
| `<ITEM_NAME>`<br>*String* | **Required.**<br>Item name.<br>Maximum 60 characters. | `Blue Elf Aloe` |
| `<ITEM_PRICE>`<br>*Integer* | **Required.**<br>Individual item price (price per item), multiplied by amount.offset value.<br>For example, to represent an item price of ₹12.99, the value would be `1299`. | `200000` |
| `<ITEM_QUANTITY>`<br>*Integer* | **Required.**<br>Number of items in order, if order is placed.<br>Maximum 100 integers. | `1` |
| `<MESSAGE_BODY_TEXT_VARIABLE>`<br>*Object* | **Required if template message body text uses variables, otherwise omit.**<br>Object describing a message variable. If the template uses multiple variables, you must define an object for each variable.<br>Supports `text`, `currency`, and `date_time` types. See [Messages Parameters](https://developers.facebook.com/documentation/business-messaging/whatsapp/reference/whatsapp-business-phone-number/message-api#parameter-object).<br>There is no maximum character limit on this value, but it does count against the message body text limit of 1024 characters. | `{<br>"type":"text",<br>"text": "Nidhi"<br>}` |
| `<MESSAGE_HEADER_ASSET_ID>`<br>*String* | **Required.**<br>Header asset’s uploaded media asset ID. Use the [**POST /<BUSINESS_PHONE_NUMBER_ID>/media**](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/media#upload-media) endpoint to generate an asset ID. | `1558081531584829` |
| `<MESSAGE_HEADER_FORMAT>`<br>*String* | **Required.**<br>Indicates header type and a matching property name.<br>Note that the `<MESSAGE_HEADER_FORMAT>` placeholder appears twice in the post body example above, as it serves as a placeholder for the type property’s value and its matching property name.<br>Value can be `image` or `video`. | `image` |
| `<PAYMENT_GATEWAY_CONFIGURATION_NAME>`<br>*String* | **Required.**<br>Configuration name of payment gateway you have [configured](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/onboarding-apis) on your WhatsApp Business Account. | `prod-razor-pay-config-05` |
| `<PAYMENT_GATEWAY_NAME>`<br>*String* | **Required.**<br>Name of payment gateway you have [configured](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/onboarding-apis) on your WhatsApp Business Account.<br>Values can be:<br>`razorpay``payu``zaakpay` | `razorpay` |
| `<PRODUCT_TYPE>`<br>*String* | **Required.**<br>Product type. Value can be `digital-goods` or `physical-goods`. | `digital-goods` |
| `<QUICK_REPLY_BUTTON_PAYLOAD>`<br>*String* | **Optional.**<br>Value to be included in messages webhooks (`messages.button.payload`) when the button is tapped. | `opt-out` |
| `<REFERENCE_ID>`<br>*String* | **Required.**<br>Your unique order or invoice reference ID. Case-sensitive. Cannot be empty. Will be preceded by a hash (#) symbol in the checkout flow.<br>Value must be unique for each checkout button template message. If sending a carousel template, each checkout button must have a unique reference ID.<br>If you need to send multiple messages for the same order/invoice, it is recommended to append a sequence number to the value (for example, -1).<br>Values can only contain English letters, numbers, underscores, dashes, or dots.<br>Maximum 35 characters. | `abc.123_xyz-1` |
| `<SALE_PRICE>`<br>*Integer* | **Required if using a sale amount.**<br>Sale price, multiplied by `sale.offset` value.<br>For example, to represent a sale price of ₹10, the value would be `1000`. | `150000` |
| `<SHIPPING_AMOUNT>`<br>*Integer* | **Required.**<br>Order shipping cost, multiplied by `shipping.offset` value.<br>For example, to represent a shipping cost of ₹.99, the value would be `99`. | `20000` |
| `<SHIPPING_INFO_ADDRESS>`<br>*String* | **Required if you know the recipient’s shipping information.**<br>Product recipient’s address.<br>Maximum 512 characters. | `Bandra Kurla Complex` |
| `<SHIPPING_INFO_BUILDING_NAME>`<br>*String* | **Optional.**<br>Product recipient’s building name.<br>Maximum 128 characters. | `One BKC` |
| `<SHIPPING_INFO_CITY>`<br>*String* | **Required if you know the recipient’s shipping information.**<br>Full name of product recipient’s city.<br>Maximum 100 characters. | `Mumbai` |
| `<SHIPPING_INFO_FLOOR_NUMBER>`<br>*String* | **Optional.**<br>Product recipient’s floor number.<br>Maximum 10 characters. | `2` |
| `<SHIPPING_INFO_HOUSE_NUMBER>`<br>*String* | **Optional.**<br>Product recipient’s house number.<br>Maximum 8 characters. | `12` |
| `<SHIPPING_INFO_INDIA_PIN>`<br>*String* | **Required if you know the recipient’s shipping information.**<br>Product recipient’s postal index number.<br>Maximum 6 characters. | `400051` |
| `<SHIPPING_INFO_LANDMARK_AREA>`<br>*String* | **Optional.**<br>Product recipient’s landmark area.<br>Maximum 128 characters. | `Near BKC Circle` |
| `<SHIPPING_INFO_NAME>`<br>*String* | **Required if you know the recipient’s shipping information.**<br>Product recipient’s full name.<br>Maximum 256 characters. | `Nidhi Tripathi` |
| `<SHIPPING_INFO_PHONE_NUMBER>`<br>*String* | **Required if you know the recipient’s shipping information.**<br>Product recipient’s WhatsApp phone number.<br>Maximum 12 characters. | `919000090000` |
| `<SHIPPING_INFO_STATE>`<br>*String* | **Required if you know the recipient’s shipping information.**<br>Full name of product recipient’s state.<br>Maximum 100 characters. | `Maharastra` |
| `<SHIPPING_INFO_TOWER_NUMBER>`<br>*String* | **Optional.**<br>Product recipient’s tower number.<br>Maximum 8 characters. | `2` |
| `<SUBTOTAL_AMOUNT>`<br>*Integer* | **Required.**<br>Order subtotal. Calculate by multiplying `<ITEM_PRICE>` by `<ITEM_QUANTITY>` by `subtotal.offset`.<br>For example, if the template is for placing a single order containing 2 items priced at ₹12.99, the value would be `2598`. | `150000` |
| `<TAX_AMOUNT>`<br>*Integer* | **Required.**<br>Tax amount, multiplied by `tax.offset`.<br>For example, to represent a tax amount of ₹5, the value would be `500`. | `10000` |
| `<TAX_DESCRIPTION>`<br>*String* | **Optional.**<br>Tax description.<br>Maximum 60 characters. | `Sales tax` |
| `<TEMPLATE_LANGUAGE>`<br>*String* | **Required.**<br>Template [language and locale code](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/supported-languages). | `en_US` |
| `<TEMPLATE_NAME>`<br>*String* | **Required.**<br>Template name.<br>Maximum 512 characters. | `item_back_in_stock_v1` |
| `<TOTAL_AMOUNT>`<br>*Integer* | **Required.**<br>Total amount of order, multiplied by `total_amount.offset` value.<br>For example, to represent a total amount of ₹18, value be `1800`.<br>Must be a sum of:<br>`order.subtotal.value``order.shipping.value``order.tax.value`<br>Minus:<br>`order.discount.value` | `165000` |
| `<WHATSAPP_USER_PHONE_NUMBER>`<br>*String* | **Required.**<br>WhatsApp user phone number. | `+16505551234` |

### Example request

```curl
curl 'https://graph.facebook.com/v25.0/106540352242922/messages' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer EAAJB...' \
-d '
{
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": "+16505551234",
  "type": "template",
  "template": {
    "name": "item_back_in_stock_v2",
    "language": {
      "policy": "deterministic",
      "code": "en_US"
    },
    "components": [
      {
        "type": "header",
        "parameters": [
          {
            "type": "image",
            "image": {
              "id": "1558081531584829"
            }
          }
        ]
      },
      {
        "type": "body",
        "parameters": [
          {
            "type": "text",
            "text": "Nidhi"
          },
          {
            "type": "text",
            "text": "Blue Elf Aloe"
          }
        ]
      },
      {
        "type": "button",
        "sub_type": "order_details",
        "index": 0,
        "parameters": [
          {
            "type": "action",
            "action": {
              "order_details": {
                "reference_id": "abc.123_xyz-1",
                "type": "physical-goods",
                "currency": "INR",
                "payment_settings": [
                  {
                    "type": "payment_gateway",
                    "payment_gateway": {
                      "type": "razorpay",
                      "configuration_name": "prod-razor-pay-config-05"
                    }
                  }
                ],
                "shipping_info": {
                  "country": "IN",
                  "addresses": [
                    {
                      "name": "Nidhi Tripathi",
                      "phone_number": "919000090000",
                      "address": "Bandra Kurla Complex",
                      "city": "Mumbai",
                      "state": "Maharastra",
                      "in_pin_code": "400051",
                      "house_number": "12",
                      "tower_number": "5",
                      "building_name": "One BKC",
                      "landmark_area": "Near BKC Circle"
                    }
                  ]
                },
                "order": {
                  "items": [
                    {
                      "amount": {
                        "offset": 100,
                        "value": 200000
                      },
                      "sale_amount": {
                        "offset": 100,
                        "value": 150000
                      },
                      "name": "Blue Elf Aloe",
                      "quantity": 1,
                      "country_of_origin": "India",
                      "importer_name": "Lucky Shrub Imports and Exports",
                      "importer_address": {
                        "address_line1": "One BKC",
                        "address_line2": "Bandra Kurla Complex",
                        "city": "Mumbai",
                        "zone_code": "MH",
                        "postal_code": "400051",
                        "country_code": "IN"
                      }
                    }
                  ],
                  "subtotal": {
                    "offset": 100,
                    "value": 150000
                  },
                  "shipping": {
                    "offset": 100,
                    "value": 20000
                  },
                  "tax": {
                    "offset": 100,
                    "value": 10000
                  },
                  "discount": {
                    "offset": 100,
                    "value": 15000,
                    "description": "Additional 10% off"
                  },
                  "status": "pending",
                  "expiration": {
                    "timestamp": "1726627150"
                  }
                },
                "total_amount": {
                  "offset": 100,
                  "value": 165000
                }
              }
            }
          }
        ]
      }
    ]
  }
}'
```

The following sample request and responses are only supported with [Enabling coupons, realtime inventory and pricing updates](https://developers.facebook.com/documentation/business-messaging/whatsapp/payments/payments-in/checkout-button-templates#enabling_coupons_inventory) feature and it is currently in beta and only available to India businesses and WhatsApp users with an India country calling code. Please reach out to whatsappindia-bizpayments-support@meta.com to know more.

### Get coupons - endpoint sample request

```json
      {
    "data":
    {
        "order_details":
        {
            "reference_id": "abc.123_xyz-1",
            "type": "physical-goods",
            "currency": "INR",
            "shipping_info":
            {
                "country": "IN",
                "addresses":
                [
                    {
                        "name": "Nidhi Tripathi",
                        "phone_number": "919000090000",
                        "address": "Bandra Kurla Complex",
                        "city": "Mumbai",
                        "state": "Maharastra",
                        "in_pin_code": "400051",
                        "house_number": "12",
                        "tower_number": "5",
                        "building_name": "One BKC",
                        "landmark_area": "Near BKC Circle"
                    }
                ]
            },
            "order":
            {
                "items":
                [
                    {
                        "amount":
                        {
                            "offset": 100,
                            "value": 200000
                        },
                        "sale_amount":
                        {
                            "offset": 100,
                            "value": 150000
                        },
                        "name": "Blue Elf Aloe",
                        "quantity": 1,
                        "country_of_origin": "India",
                        "importer_name": "Lucky Shrub Imports and Exports",
                        "importer_address":
                        {
                            "address_line1": "One BKC",
                            "address_line2": "Bandra Kurla Complex",
                            "city": "Mumbai",
                            "zone_code": "MH",
                            "postal_code": "400051",
                            "country_code": "IN"
                        }
                    }
                ],
                "subtotal":
                {
                    "offset": 100,
                    "value": 150000
                },
                "shipping":
                {
                    "offset": 100,
                    "value": 20000
                },
                "tax":
                {
                    "offset": 100,
                    "value": 10000
                },
                "discount":
                {
                    "offset": 100,
                    "value": 15000,
                    "description": "Additional 10% off"
                },
                "status": "pending",
                "expiration":
                {
                    "timestamp": "1726627150",
                    "description": "order expires in 5 min"
                }
            },
            "total_amount":
            {
                "offset": 100,
                "value": 165000
            }
        },
        "input":
        {
            "user_id": "919000090000"
        }
    },
    "action": "data_exchange",
    "sub_action": "get_coupons",
    "version": "1.0"
}
```

### Get coupons - endpoint sample response

```json
      {
    "version": "1.0",
    "sub_action": "get_coupons",
    "data":
    {
        "coupons":
        [
            {
                "description": "Save R20 on the order",
                "code": "TRYNEW20",
                "id": "try_new_20_id"
            },
            {
                "description": "Save R30 on the order",
                "code": "TRYNEW30",
                "id": "try_new_30_id"
            },
            {
                "description": "Save R50 on the order",
                "code": "TRYNEW50",
                "id": "try_new50_id"
            }
        ]
    }
}
```

### Apply coupon - endpoint sample request

```json
      {
    "data":
    {
        "order_details":
        {
            "reference_id": "abc.123_xyz-1",
            "type": "physical-goods",
            "currency": "INR",
            "shipping_info":
            {
                "country": "IN",
                "addresses":
                [
                    {
                        "name": "Nidhi Tripathi",
                        "phone_number": "919000090000",
                        "address": "Bandra Kurla Complex",
                        "city": "Mumbai",
                        "state": "Maharastra",
                        "in_pin_code": "400051",
                        "house_number": "12",
                        "tower_number": "5",
                        "building_name": "One BKC",
                        "landmark_area": "Near BKC Circle"
                    }
                ]
            },
            "order":
            {
                "items":
                [
                    {
                        "amount":
                        {
                            "offset": 100,
                            "value": 200000
                        },
                        "sale_amount":
                        {
                            "offset": 100,
                            "value": 150000
                        },
                        "name": "Blue Elf Aloe",
                        "quantity": 1,
                        "country_of_origin": "India",
                        "importer_name": "Lucky Shrub Imports and Exports",
                        "importer_address":
                        {
                            "address_line1": "One BKC",
                            "address_line2": "Bandra Kurla Complex",
                            "city": "Mumbai",
                            "zone_code": "MH",
                            "postal_code": "400051",
                            "country_code": "IN"
                        }
                    }
                ],
                "subtotal":
                {
                    "offset": 100,
                    "value": 150000
                },
                "shipping":
                {
                    "offset": 100,
                    "value": 20000
                },
                "tax":
                {
                    "offset": 100,
                    "value": 10000
                },
                "discount":
                {
                    "offset": 100,
                    "value": 15000,
                    "description": "Additional 10% off"
                },
                "status": "pending",
                "expiration":
                {
                    "timestamp": "1726627150",
                    "description": "order expires in 5 min"
                }
            },
            "total_amount":
            {
                "offset": 100,
                "value": 165000
            }
        },
        "input":
        {
            "user_id": "919000090000",
            "coupon":
            {
                "code": "TRYNEW10"
            }
        }
    },
    "action": "data_exchange",
    "sub_action": "apply_coupon",
    "version": "1.0"
}
```

### Apply coupon - endpoint sample response

```json
      {
    "sub_action": "apply_coupon",
    "version": "1.0",
    "data":
    {
        "order_details":
        {
            "reference_id": "abc.123_xyz-1",
            "type": "physical-goods",
            "currency": "INR",
            "shipping_info":
            {
                "country": "IN",
                "addresses":
                [
                    {
                        "name": "Nidhi Tripathi",
                        "phone_number": "919000090000",
                        "address": "Bandra Kurla Complex",
                        "city": "Mumbai",
                        "state": "Maharastra",
                        "in_pin_code": "400051",
                        "house_number": "12",
                        "tower_number": "5",
                        "building_name": "One BKC",
                        "landmark_area": "Near BKC Circle"
                    }
                ]
            },
            "order":
            {
                "items":
                [
                    {
                        "amount":
                        {
                            "offset": 100,
                            "value": 200000
                        },
                        "sale_amount":
                        {
                            "offset": 100,
                            "value": 150000
                        },
                        "name": "Blue Elf Aloe",
                        "quantity": 1,
                        "country_of_origin": "India",
                        "importer_name": "Lucky Shrub Imports and Exports",
                        "importer_address":
                        {
                            "address_line1": "One BKC",
                            "address_line2": "Bandra Kurla Complex",
                            "city": "Mumbai",
                            "zone_code": "MH",
                            "postal_code": "400051",
                            "country_code": "IN"
                        }
                    }
                ],
                "subtotal":
                {
                    "offset": 100,
                    "value": 150000
                },
                "shipping":
                {
                    "offset": 100,
                    "value": 20000
                },
                "tax":
                {
                    "offset": 100,
                    "value": 10000
                },
                "discount":
                {
                    "offset": 100,
                    "value": 15000,
                    "description": "Additional 10% off"
                },
                "status": "pending",
                "expiration":
                {
                    "timestamp": "1726627150",
                    "description": "order expires in 5 min"
                }
            },
            "coupon":
            {
                "code": "TRYNEW10",
                "discount":
                {
                    "value": 16500,
                    "offset": 100
                }
            },
            "total_amount":
            {
                "offset": 100,
                "value": 148500
            }
        }
    }
}
```

### Remove coupon - endpoint sample request

```json
      {
    "data":
    {
        "order_details":
        {
            "reference_id": "abc.123_xyz-1",
            "type": "physical-goods",
            "currency": "INR",
            "shipping_info":
            {
                "country": "IN",
                "addresses":
                [
                    {
                        "name": "Nidhi Tripathi",
                        "phone_number": "919000090000",
                        "address": "Bandra Kurla Complex",
                        "city": "Mumbai",
                        "state": "Maharastra",
                        "in_pin_code": "400051",
                        "house_number": "12",
                        "tower_number": "5",
                        "building_name": "One BKC",
                        "landmark_area": "Near BKC Circle"
                    }
                ]
            },
            "order":
            {
                "items":
                [
                    {
                        "amount":
                        {
                            "offset": 100,
                            "value": 200000
                        },
                        "sale_amount":
                        {
                            "offset": 100,
                            "value": 150000
                        },
                        "name": "Blue Elf Aloe",
                        "quantity": 1,
                        "country_of_origin": "India",
                        "importer_name": "Lucky Shrub Imports and Exports",
                        "importer_address":
                        {
                            "address_line1": "One BKC",
                            "address_line2": "Bandra Kurla Complex",
                            "city": "Mumbai",
                            "zone_code": "MH",
                            "postal_code": "400051",
                            "country_code": "IN"
                        }
                    }
                ],
                "subtotal":
                {
                    "offset": 100,
                    "value": 150000
                },
                "shipping":
                {
                    "offset": 100,
                    "value": 20000
                },
                "tax":
                {
                    "offset": 100,
                    "value": 10000
                },
                "discount":
                {
                    "offset": 100,
                    "value": 15000,
                    "description": "Additional 10% off"
                },
                "status": "pending",
                "expiration":
                {
                    "timestamp": "1726627150",
                    "description": "order expires in 5 min"
                }
            },
            "coupon":
            {
                "code": "TRYNEW10",
                "discount":
                {
                    "value": 16500,
                    "offset": 100
                }
            },
            "total_amount":
            {
                "offset": 100,
                "value": 148500
            }
        },
        "input":
        {
            "user_id": "919000090000"
        }
    },
    "action": "data_exchange",
    "sub_action": "remove_coupon",
    "version": "1.0"
}
```

### Remove coupon - endpoint sample response

```json
      {
    "sub_action": "remove_coupon",
    "version": "1.0",
    "data":
    {
        "order_details":
        {
            "reference_id": "abc.123_xyz-1",
            "type": "physical-goods",
            "currency": "INR",
            "shipping_info":
            {
                "country": "IN",
                "addresses":
                [
                    {
                        "name": "Nidhi Tripathi",
                        "phone_number": "919000090000",
                        "address": "Bandra Kurla Complex",
                        "city": "Mumbai",
                        "state": "Maharastra",
                        "in_pin_code": "400051",
                        "house_number": "12",
                        "tower_number": "5",
                        "building_name": "One BKC",
                        "landmark_area": "Near BKC Circle"
                    }
                ]
            },
            "order":
            {
                "items":
                [
                    {
                        "amount":
                        {
                            "offset": 100,
                            "value": 200000
                        },
                        "sale_amount":
                        {
                            "offset": 100,
                            "value": 150000
                        },
                        "name": "Blue Elf Aloe",
                        "quantity": 1,
                        "country_of_origin": "India",
                        "importer_name": "Lucky Shrub Imports and Exports",
                        "importer_address":
                        {
                            "address_line1": "One BKC",
                            "address_line2": "Bandra Kurla Complex",
                            "city": "Mumbai",
                            "zone_code": "MH",
                            "postal_code": "400051",
                            "country_code": "IN"
                        }
                    }
                ],
                "subtotal":
                {
                    "offset": 100,
                    "value": 150000
                },
                "shipping":
                {
                    "offset": 100,
                    "value": 20000
                },
                "tax":
                {
                    "offset": 100,
                    "value": 10000
                },
                "discount":
                {
                    "offset": 100,
                    "value": 15000,
                    "description": "Additional 10% off"
                },
                "status": "pending",
                "expiration":
                {
                    "timestamp": "1726627150",
                    "description": "order expires in 5 min"
                }
            },
            "total_amount":
            {
                "offset": 100,
                "value": 165000
            }
        }
    }
}
```

### Apply shipping - endpoint sample request

```json
      {
    "data":
    {
        "order_details":
        {
            "reference_id": "abc.123_xyz-1",
            "type": "physical-goods",
            "currency": "INR",
            "shipping_info":
            {
                "country": "IN",
                "addresses":
                [
                    {
                        "name": "Nidhi Tripathi",
                        "phone_number": "919000090000",
                        "address": "Bandra Kurla Complex",
                        "city": "Mumbai",
                        "state": "Maharastra",
                        "in_pin_code": "400051",
                        "house_number": "12",
                        "tower_number": "5",
                        "building_name": "One BKC",
                        "landmark_area": "Near BKC Circle"
                    }
                ]
            },
            "order":
            {
                "items":
                [
                    {
                        "amount":
                        {
                            "offset": 100,
                            "value": 200000
                        },
                        "sale_amount":
                        {
                            "offset": 100,
                            "value": 150000
                        },
                        "name": "Blue Elf Aloe",
                        "quantity": 1,
                        "country_of_origin": "India",
                        "importer_name": "Lucky Shrub Imports and Exports",
                        "importer_address":
                        {
                            "address_line1": "One BKC",
                            "address_line2": "Bandra Kurla Complex",
                            "city": "Mumbai",
                            "zone_code": "MH",
                            "postal_code": "400051",
                            "country_code": "IN"
                        }
                    }
                ],
                "subtotal":
                {
                    "offset": 100,
                    "value": 150000
                },
                "shipping":
                {
                    "offset": 100,
                    "value": 20000
                },
                "tax":
                {
                    "offset": 100,
                    "value": 10000
                },
                "discount":
                {
                    "offset": 100,
                    "value": 15000,
                    "description": "Additional 10% off"
                },
                "status": "pending",
                "expiration":
                {
                    "timestamp": "1726627150",
                    "description": "order expires in 5 min"
                }
            },
            "coupon":
            {
                "code": "TRYNEW10",
                "discount":
                {
                    "value": 16500,
                    "offset": 100
                }
            },
            "total_amount":
            {
                "offset": 100,
                "value": 148500
            }
        },
        "input":
        {
            "user_id": "919000090000",
            "selected_address":
            {
                "name": "Nidhi Tripathi",
                "phone_number": "919000090000",
                "address": "Bandra Kurla Complex",
                "city": "Mumbai",
                "state": "Maharastra",
                "in_pin_code": "400051",
                "house_number": "12",
                "tower_number": "5",
                "building_name": "One BKC",
                "landmark_area": "Near BKC Circle"
            }
        }
    },
    "action": "data_exchange",
    "sub_action": "apply_shipping",
    "version": "1.0"
}
```

### Apply shipping - endpoint sample response

```json
      {
    "sub_action": "apply_shipping",
    "version": "1.0",
    "data":
    {
        "order_details":
        {
            "reference_id": "abc.123_xyz-1",
            "type": "physical-goods",
            "currency": "INR",
            "shipping_info":
            {
                "country": "IN",
                "addresses":
                [
                    {
                        "name": "Nidhi Tripathi",
                        "phone_number": "919000090000",
                        "address": "Bandra Kurla Complex",
                        "city": "Mumbai",
                        "state": "Maharastra",
                        "in_pin_code": "400051",
                        "house_number": "12",
                        "tower_number": "5",
                        "building_name": "One BKC",
                        "landmark_area": "Near BKC Circle"
                    }
                ],
                "selected_address":
                {
                    "name": "Nidhi Tripathi",
                    "phone_number": "919000090000",
                    "address": "Bandra Kurla Complex",
                    "city": "Mumbai",
                    "state": "Maharastra",
                    "in_pin_code": "400051",
                    "house_number": "12",
                    "tower_number": "5",
                    "building_name": "One BKC",
                    "landmark_area": "Near BKC Circle"
                }
            },
            "order":
            {
                "items":
                [
                    {
                        "amount":
                        {
                            "offset": 100,
                            "value": 200000
                        },
                        "sale_amount":
                        {
                            "offset": 100,
                            "value": 150000
                        },
                        "name": "Blue Elf Aloe",
                        "quantity": 1,
                        "country_of_origin": "India",
                        "importer_name": "Lucky Shrub Imports and Exports",
                        "importer_address":
                        {
                            "address_line1": "One BKC",
                            "address_line2": "Bandra Kurla Complex",
                            "city": "Mumbai",
                            "zone_code": "MH",
                            "postal_code": "400051",
                            "country_code": "IN"
                        }
                    }
                ],
                "subtotal":
                {
                    "offset": 100,
                    "value": 150000
                },
                "shipping":
                {
                    "offset": 100,
                    "value": 40000
                },
                "tax":
                {
                    "offset": 100,
                    "value": 10000
                },
                "discount":
                {
                    "offset": 100,
                    "value": 15000,
                    "description": "Additional 10% off"
                },
                "status": "pending",
                "expiration":
                {
                    "timestamp": "1726627150",
                    "description": "order expires in 5 min"
                }
            },
            "coupon":
            {
                "code": "TRYNEW10",
                "discount":
                {
                    "value": 16500,
                    "offset": 100
                }
            },
            "total_amount":
            {
                "offset": 100,
                "value": 168500
            }
        }
    }
}
```
