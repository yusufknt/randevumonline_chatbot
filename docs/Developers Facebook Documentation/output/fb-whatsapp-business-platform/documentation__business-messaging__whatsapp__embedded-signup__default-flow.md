# Cloud API flow | Developer Documentation

_Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/default-flow_

---

# Cloud API flow

Updated: Nov 11, 2025

This document describes the default screens that your business customers will be presented with as they navigate the Embedded Signup flow. Note that if you inject [pre-filled data](https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/pre-filled-data), you can pre-fill some of these screens, and bypass many of them entirely, reducing the likelihood of errors and making it much easier for your business customers to onboard onto the platform. This is the UI flow for the latest version v4.

## Screens

### Authentication screen

This screen authenticates business customers using their Facebook or Meta Business Suite credentials.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/530819633_636229419515187_227138492125594706_n.png?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=t9qv0C3w-OQQ7kNvwGtHEJv&_nc_oc=AdrvWUgv7DFaVazC4dOhxFwHvr0YLDdJ_EtjhIpJsfqBmeK-MSSNtDYVY9gYibrMrNo&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=H2divo3bBoRDb2d5hj_Bzg&_nc_ss=7b20f&oh=00_Af5aZl2L1VX-SRpJuf1WvMRgu-3xkJvkidNqV3SQdPnPOA&oe=6A1C2194)

### Authorization screen

This screen describes the data the business customer will be permitting your app to access.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/531995822_1112262264200439_63249353490863536_n.png?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=iEzrcxa_ngQQ7kNvwHH-iOq&_nc_oc=AdoKgiiY6AsHccX7Pnh3WVQGh8kaJaV_sp5cuafzGSEW8o_YvUWg34Botnpf7L2xf8A&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=H2divo3bBoRDb2d5hj_Bzg&_nc_ss=7b20f&oh=00_Af5LGpBkydNpqfCYmO66FRnaNyCO7Vm8pOTmF7VY7PEUwQ&oe=6A1C3340)

### Business Asset Selection Screen

This screen gives customers the option to select existing business assets such as a Meta business portfolio and WhatsApp Business Account.

Users also have the option to create new assets if they have not reached their portfolio limit.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/532045601_1897587967686145_847324094190786110_n.png?_nc_cat=102&ccb=1-7&_nc_sid=e280be&_nc_ohc=fQupgosVnXMQ7kNvwEW56bb&_nc_oc=AdoCeXHnkvdTkIimkHHLF914Q689jwxx693DPUmfikru-T_YGew_klzcNXtQ49IyF8A&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=H2divo3bBoRDb2d5hj_Bzg&_nc_ss=7b20f&oh=00_Af4Xg_pwVHFaTu_mFwRmLqcyZseJD6pFBVdxgBHrlYdRTA&oe=6A1C312E)

### Business Asset Creation Screen

This screen gives customers the option to select existing business assets such as a Meta business portfolio and WhatsApp Business Account.

Users also have the option to create new assets if they have not reached their portfolio limit.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/530852550_1105248814823575_6797431386886245236_n.png?_nc_cat=106&ccb=1-7&_nc_sid=e280be&_nc_ohc=ZAc0N7-zZYQQ7kNvwFkjMwG&_nc_oc=AdoBZVUvSYI2O-S8WnI5_TUktwcP7j8Xa08EuzXYou2_LRvgpmmFaIEhXBpqhatTNio&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=H2divo3bBoRDb2d5hj_Bzg&_nc_ss=7b20f&oh=00_Af6xXtLfNNjBvqAmA2DEO7dOX1ZRUPlUXKf8C9K3dkiAjA&oe=6A1C2E43)

### Phone number addition screen

This screen allows the business customer to enter a new business phone number to associate with their WhatsApp Business Account.

It also allows the customer to choose how they wish to receive their verification code, which they will need to provide in the next step.

If you are providing phone numbers to your customers, you will have to deliver these codes to your customers, or provide pre-verified numbers instead.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/579214248_1544901606717694_7187028527222587188_n.png?_nc_cat=110&ccb=1-7&_nc_sid=e280be&_nc_ohc=nf1Rw0TBI-8Q7kNvwE9dK20&_nc_oc=AdqZ6_Eyzj7zT0LfFGfn_Up_1RwFsnmjttA6sJzJ-4_6ElPMuH-2c6kdVoAUV6KXyP4&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=H2divo3bBoRDb2d5hj_Bzg&_nc_ss=7b20f&oh=00_Af6Vi0dwlcvLD-5DD_Txgh5w4WUDMAYPDHTiXs8WAfsiLg&oe=6A1C0D7E)

### Phone number verification screen

This screen allows the business customer to verify ownership of the business phone number they entered in the previous step.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/557624038_1991414544970922_7818680630707794930_n.png?_nc_cat=110&ccb=1-7&_nc_sid=e280be&_nc_ohc=XxFDoA3i5QIQ7kNvwE9H246&_nc_oc=Adp0JrBUbyg24JTBAmxhlGMe7lF6LGDjEDqKLBuZ0T7kF64SQQ0B5nV8jZxAjvTOY2A&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=H2divo3bBoRDb2d5hj_Bzg&_nc_ss=7b20f&oh=00_Af78rUYBXLENjyWh4NCyyjQCa0Gk8Ux7khMna_EWPST0GQ&oe=6A1C2D20)

### Permissions review screen

This screen provides a summary of the permissions the business customer will be granting to your app.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/530797839_1261352201871305_6011316801343038234_n.png?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=3CB_apBFN3YQ7kNvwHeYnH_&_nc_oc=AdrR7qEjoSt29ChMbOhyddZlbu3JWI6e7EXNRkQQ4A_Kd_JfCT2ePFt2aJWnKcWPtkE&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=H2divo3bBoRDb2d5hj_Bzg&_nc_ss=7b20f&oh=00_Af4W3yQLxZ84WHpZSQ9QT8P0vOMskATfZQzusmlK3ttBbg&oe=6A1C1529)

### Success screen

This screen indicates that Meta successfully created and associated all of the business customer’s assets (business portfolio, WABA, phone number display profile, and business phone number).

When the customer clicks Finish, a message event will be triggered, containing the customer’s WABA ID and business phone number ID, which you must then use to onboard the customer to the platform.

![Image](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/532564823_655188414258906_330922092450163709_n.png?_nc_cat=111&ccb=1-7&_nc_sid=e280be&_nc_ohc=IR63T-dx6ZkQ7kNvwHQqMPj&_nc_oc=Ado3nD3CE5p9xx9mJ1-q6kz_RZBcm22Kuqk_vwhhw4NiN3c6b6dbxhiRH98MyFAvB5s&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=H2divo3bBoRDb2d5hj_Bzg&_nc_ss=7b20f&oh=00_Af529AkE0vKAGsvwpTBAtSkVMaWBbQDVQFRtI-kHR8AwHg&oe=6A1C0CAC)
