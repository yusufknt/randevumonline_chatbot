# Data Security Requirements

_Source: https://developers.facebook.com/docs/development/maintaining-data-access/data-protection-assessment/data-security_

---

# Data Security Requirements

Here you can find security requirements to help with the Data Protection Assessment. If your assessment questions start with 3.1, you received it on or after February 15, 2024.

If your assessment is not numbered, you received it before February, 2024. **[Go here](https://developers.facebook.com/docs/resp-plat-initiatives/data-protection-assessment/data-security/version2.5)** to find help on the security requirements for the prior version of the Data Protection Assessment (version 2.5).

For assessments received after May 5th 2025, please go to [this page](https://developers.facebook.com/docs/resp-plat-initiatives/data-access-renewal/tutorial/data-security) for further guidance.

These data security requirements are intended to provide helpful information and assist you in completing Meta’s Data Protection Assessment. For any given question, please note there may be more than one way to demonstrate that you meet our requirements. Only a member of Meta’s review team can make a final determination on whether the evidence provided meets the requirements of our Data Protection Assessment. In addition to using this guide, we recommend consulting with your Chief Information Officer, the person with an equivalent role within your organization, or a qualified cybersecurity firm when preparing your responses to Meta’s Data Protection Assessment to ensure your responses are complete and accurate.

[](blob:https://developers.facebook.com/1dd2dc2d-1fca-4a46-a59b-de1a38693431)

If you have access to certain
types of platform data, you

Play

-3:46

Mute

Enter Fullscreen

Sharing and reporting options

![](https://static.xx.fbcdn.net/rsrc.php/v4/y4/r/-PAXP-deijE.gif)

Something went wrong

We're having trouble playing this video.

[Learn more](https://www.facebook.com/help/396404120401278/list)

A subset of the DPA questionnaire is focused on Platform Term 6, which outlines data security requirements. We recommend you utilize this document to understand the expectations, requirements, and related evidence with respect to data security use and processing as defined in Meta Platform Terms.

Apps with access to certain types of Platform Data from Meta are required to complete the annual Data Protection Assessment (DPA). DPA is designed to determine whether developers meet the requirements of [Meta Platform Terms](https://developers.facebook.com/terms/dfc_platform_terms/) as it relates to the use, sharing, and protection of Platform Data. A subset of the DPA questionnaire is focused on Platform Term 6, which outlines data security requirements. We recommend you utilize this document to understand the expectations, requirements, and related evidence with respect to data security use and processing as defined in Meta Platform Terms.

Note there is a [glossary](#glossary) included at the end of this document with key terms and definitions.

## Q3.1-7 questions - Information security certification

### All questions

3.1-7.a, 3.1-7.a.i.A, 3.1-7.a.i.B

### Summary

You may have undergone an audit by an accredited third party and received certification(s) regarding your information security practices. Sharing such a certification provides helpful context for our reviews.

We do not require any information security certifications, but if you provide a valid ISO 27001, ISO 27018, or SOC 2 Type 2, they will be taken into account during our reviews.

### Changes from prior version

None

### Additional guidance

None

### External resources

Not familiar with information security certifications? Review these resources.

- [AICPA: SOC 2 for Service Organizations: Trust Services Criteria](https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.aicpa-cima.com%2Ftopic%2Faudit-assurance%2Faudit-and-assurance-greater-than-soc-2&h=AUCpI1ve0F3qVQNIAASAX0KsmQpgyg6jdNqOUyfR57ZW06xEhOgvB9Vu_SnqJflBgBBW1RK8iMOdAWLNRjjQ4V5MB_Cod9b6Y2Wo_VUWjIDdzm66Oqb4hON8_vrkRqlKS5Stmezfbh99nQ)
- [ISO: ISO/IEC 27001:2022](https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.iso.org%2Fstandard%2F27001&h=AUD-dmAYX70dj5Xvt6uyPCayByTHQcAJu6rzILhkV9O7H3Fbrt9tpQU_14A8yMPUB10XY7IXz0Z3wJyjT5OHj3IDZObjklURK16CZ8KO-RnU-M84xLkvYmLmbxF1miZztT9AAp0J20eYkQ)
- [ISO: ISO/IEC 27018:2019](https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.iso.org%2Fstandard%2F76559.html&h=AUAcJkxe_KdeLt_Znn2DRlkPvLMQ8zvdP3ehlrf12UcRMi2O-5yjp_y23P0H30MP5yQywruk5h1ojgxkoUKOexM2mN4QixKHPPzlHXUBI1sPGo8-rz4PQLH1JUmn8728ffffZj5gxN62Hw)

### Evidence examples

None

## Q3.1-8 Questions - Storage of Platform Data in a Server or Backend Environment

### All questions

3.1-8.a, 3.1-8.b, 3.1-8.a.i

### Summary

In order to perform our reviews accurately, we need to first understand how Platform Data is processed and stored by your system or application.

This section asks if you store Platform Data in a backend environment, and if so:

- Which specific Platform Data attributes
- What backend hosting approach(es) are used

### Changes from prior version

- You will now be asked to indicate what Platform Data attributes you store in your backend environment.
- You will also be asked to indicate what hosting solutions/infrastructure you use to process Platform Data in your backend environment.

### Additional guidance

None

### External resources

Not familiar with security in server or backend environments? Review these resources.

- [CSA: Cloud Security Alliance](https://l.facebook.com/l.php?u=https%3A%2F%2Fcloudsecurityalliance.org%2F&h=AUDyxaT7OfxAIAxt2zRVggaV-wJxjJT1Onja7sph6lXFwOI2EE3lNnWWZ2NlJLIbuodKsIbboiOy2GbvQMaFwzXRnxJzBFBqRzk9DRliDPZw5y9Lum629bysohaBhC4gzCd9Xt4FCSYxvg)
- [AWS: Security best practices for Amazon S3](https://l.facebook.com/l.php?u=https%3A%2F%2Fdocs.aws.amazon.com%2FAmazonS3%2Flatest%2Fuserguide%2Fsecurity-best-practices.html&h=AUDqkIOJqEtt5MNSvtG1KxLbtL-QKBz0bCEsJtmVUq7Z16nMWGdUhVwTJkk0RmBnvu3GSO4EzUKYwOAwfKeP0Qpao-7cfFQDncgBfMsMxQU6N6ciM2dSbhdSGC5Jfhub-sYOt6BLPfpcRg)
- [Azure: Azure security baseline for Storage](https://l.facebook.com/l.php?u=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fsecurity%2Fbenchmark%2Fazure%2Fbaselines%2Fstorage-security-baseline&h=AUDCP6IZ5yNXFE-kUDZx5BkfSySItZq9rDNqywuKrsoamKy3ldxwA4_vFzBg4_rEhpKVCBNUEKzsy4yWyWW2LGqX-5f2cxMSZydXl-7HXG6cQZ1-kEQqPEw6ylHOrRH5rmmTp8tAQKYZJQ)
- [GCP: Google Cloud security best practices](https://l.facebook.com/l.php?u=https%3A%2F%2Fcloud.google.com%2Fsecurity%2Fbest-practices&h=AUBMadAlhxz10SAWWwS9kUek3jxjL5hHRJKIr20VAJtdBOcAb5f6MAhbboFOjmNzh48KKwPpKwCipCVFC7QOOnl8MIF91YeCSQ6lyhp9JKfbYlhDnreYLP3nfBVNTRvPzSkZLLu9YqMRmA)
- [Heroku: Heroku Security](https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.heroku.com%2Fpolicy%2Fsecurity&h=AUCEaLmn1RoHgR6p_XOJTdvbX3ATJwnweTxkunIWYrKpbp5o15oUb-iXN-S2VPYIMgpcsShUa9iKVjZVSU1m8Z3DK_hsFj3oevNpnSvqfUOmCLleC8bg8x_djP3hd6S1sceiyzfwKnYxuiZ_S5xRQ_Gjg9s)
- [Alibaba Cloud: Cloud Security on Alibaba Cloud](https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.alibabacloud.com%2Fsolutions%2Fsecurity&h=AUA9-_rsuFqi37Kor1O3rbMuuVnLWobsrwJhiwGhxQHdbdFVBi7B2CsWZdP-4g-V5RwV-XHIYJHOyW_Vo0gwh8u0_XeAyBETWDa5mJN7dBjaAP3wav3ah9CqQ_0e4t75YVnOh_FBmRaNZg)
- [Tencent Cloud: TencentDB for MySQL Security White Papers](https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.tencentcloud.com%2Fdocument%2Fproduct%2F236%2F35293&h=AUAFeHCLP7BbFnBGNq3TKa7stQQExMjAqQUFZAbClIB_WQDuYgjHg5QdXSTKxxF1YQKrVbQI2L2UbHIx8LzFaXHgEhUAVJqlShlWDsLK0B9eEMWHgVdz1Vjmm_Jukfe-dDKpb4aJDlT1rg)
- Oracle Infrastructure:
  - [Oracle Infrastructure and Platform Cloud Services Security](https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.oracle.com%2Fassets%2Foracle-inf-cloud-security-wp-3840537.pdf&h=AUCY5EAvzT3sJSwW6E-tdUi9_mpzdTRrDgCvr9fNZTDLVbErTo4-DIjFOkKa9VSfxfC4_AkWgZqBmO-9RwYINTvQOhk0mPW-W8i6-o39qmf9chGS2lpAMB0V35FEO_Wgkg0OvS-h3J4J8w)
  - [Oracle Cloud Infrastructure Security Guide](https://l.facebook.com/l.php?u=https%3A%2F%2Fdocs.oracle.com%2Fen-us%2Fiaas%2FContent%2FSecurity%2FConcepts%2Fsecurity_guide.htm&h=AUBKUj8tPQ4K9OhWzH9-tFeY_XA0e4Pbv2IMnyE5B2Jn_Xc0-Z0u1ulofD2EyL4FWWQHlD9qEmCemROfyff5lpHefL6S7EjnZcfTnz64thwGuOH3XlcGVN8C0F7i2rXQTnGB8bWdPgl4Mw)
- [Digital Ocean: Digital Ocean Data Security](https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.digitalocean.com%2Fsecurity%2Fshared-responsibility-model-droplets&h=AUC9OLACmnFo7ZyCI1ohUtUft2xhg8RSbBCbMEWaHJ3NTOa_P3LCFIcH3hf1_6KKzmhuB5lpncEVgPcoe5WelFc89PPbI0XnKin0yC9q4VbAdxB9xoP_UBKT5QNxyWkBDeorOO0Za_yihQ)
- [Cisco: What Is Data Center Security](https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.cisco.com%2Fc%2Fen%2Fus%2Fsolutions%2Fsecurity%2Fsecure-data-center-solution%2Fwhat-is-data-center-security.html&h=AUDjOj-T04j6UXj_2UyauXtXVY_VbH6CgVRz6iSwQSUwixC_GeWOS2vkYrfzy1stFZq3uWevnCDVG9P_QQ30LVKimvwAaHi4VmZDYkmH4Ry6o_fu8T9UdBoovPep3ejMkuxFVKEO5iA1qw)

### Evidence examples

Developers are not required to provide evidence in response to this question.

## Q3.1-9 Questions - Protecting Platform Data at Rest in a Server or Backend Environment

### All questions

3.1-9.a, 3.1-9.b, 3.1-9.b.i, 3.1-9.b.ii, 3.1-9.c.i, 3.1-9.c.ii

### Summary

Encryption at rest protects Platform Data by making the data indecipherable without a separate decryption key. This provides an additional layer of protection against unauthorized read access in cloud or server environments where Platform Data tends to be concentrated.

You must encrypt all Platform Data stored within your backend environments. You may be asked to provide policy/procedure documentation and screenshot proof to demonstrate you have implemented this control.

This section asks if Platform Data stored in your backend environment is protected with encryption at rest or another acceptable approach to reduce the risk of data loss.

### Changes from prior version

- If you only store Meta User IDs or hashed User IDs in your backend environment, you are not required to answer these questions.
- If you do not protect Platform Data in your backend environment with encryption at rest, you will be asked if your hosting provider has an ISO 27001 or SOC 2 certificate that meets certain criteria.

### Additional guidance

**Q3.1-9.a, Q3.1-9.b Requirements**

You must encrypt all Platform Data stored within your backend environments. You may be asked to provide policy/procedure documentation and screenshot proof to demonstrate you have implemented this control.

| Policy/Procedure Evidence | Implementation Evidence |
| --- | --- |
| Q3.1-9.a.i, Q3.1-9.b.i - Provide a written explanation (e.g., a policy or procedure document) that states ALL Platform Data is encrypted at rest, including back-ups if necessary. | Q3.1-9.a.ii, Q3.1-9.b.ii - Provide one or more screenshots showing your implementation of encryption at rest. For example, one or more of these:   - A configuration in a dashboard/ console - A graphical user interface (GUI) that shows encryption through code - Encrypted fields (please redact any unencrypted data in the screenshot). |

**Q3.1-9.c Requirements**

If you do not implement encryption at rest in the server side environment, you may be protecting Platform Data in an alternative way that is still acceptable.

- Confirm that your responsible hosting provider has demonstrated to an independent auditor that sufficient physical security and secure media handling controls are in place (i.e., ISO 27001:2013: Control A.11 for Physical and Environmental Security and Control A.8.3 for secure media handling, SOC 2 Type 2: Control CC6.4 for physical security and CC6.5 for secure media handling).
- Provide the date that your hosting provider’s ISO 27001 or SOC 2 certificate issued. The certificate is invalid if the SOC 2 Type 2 issuance date is older than 1 year or if the ISO 27001 is older than 3 years compared to the date of your DPA dispatch.

### External resources

Not familiar with encryption at rest in a server or backend environment? Review these resources.

- [NIST - Protection of Data at Rest](https://l.facebook.com/l.php?u=https%3A%2F%2Fcsrc.nist.gov%2Fcsrc%2Fmedia%2Fprojects%2Fcryptographic-module-validation-program%2Fdocuments%2Fsecurity-policies%2F140sp2089.pdf&h=AUD128ONLOVga9yf_XR6itktIJrwYf8R8M4jsXqeiQiYrMMM7AiWO6OR4DERRDiT09WRW8B7ECsBCefP_dKe0d-6s9M1_anwa4vbX2Tl3UJiIn5MvOG0rtuheMZE16sc1Lw08j_XBQS-2w)
- [CIS - Encrypt Data at Rest - Essential Guide to Election Security](https://l.facebook.com/l.php?u=https%3A%2F%2Fessentialguide.docs.cisecurity.org%2Fen%2Flatest%2Fbp%2Fencrypt_data_at_rest.html&h=AUDh0lmpMS5SXea-IXd71f7J0c3muz_ko14pKvQ2hTv4FnnVw15bfMZS9euZNhcAjJeYjCyEnHvdiAn-Svc3PXV6BeWvveYVhrQl2EZQuE7a4wUcfmeQ60nI2APEe1mOT08cx9mryqhExg)
- [OWASP - Cryptographic Storage - OWASP Cheat Sheet Series](https://l.facebook.com/l.php?u=https%3A%2F%2Fcheatsheetseries.owasp.org%2Fcheatsheets%2FCryptographic_Storage_Cheat_Sheet.html&h=AUDMOsfFr3OcplSYiIHNDfERtxCh4p57P9dOnBFnxNYrfIHZv8cC2nMDFb9Aq9Jt6e3gawRxOY4cJAIJwJqs_cPsDmTJXaL8GO8kggvD2AKcq8BLzBTY5_kN-1GqGYdRZE0iw_6jFEhbYA)
- [AWS - Encrypting File Data with Amazon Elastic File System](https://l.facebook.com/l.php?u=https%3A%2F%2Fdocs.aws.amazon.com%2Fwhitepapers%2Flatest%2Fefs-encrypted-file-systems%2Fencryption-of-data-at-rest.html&h=AUDLev7xMAh5hUcT6MTPemgOzqJZ6pNpY2WgZzQQMG0NQ2aPNWBHB_-YGRznjoB8Hpp5dreTGFazuKMwcQ7wvdpbKCNSmGjHGHhIuUNWaSzo3i6jFuFS6rFQ9eJSn8Igvdmuq4XAfoTOOQ)
- [GCP - Default encryption at rest | Documentation | Google Cloud](https://l.facebook.com/l.php?u=https%3A%2F%2Fcloud.google.com%2Fdocs%2Fsecurity%2Fencryption%2Fdefault-encryption&h=AUCMxgiYEw9LkCfVGW0BlOz6LnYTTlxHYQTHeIaacLa8s_cnP-oi4KOPsrvivL60cnMOpb3K2qb6aPhA29jUAl32O9DRH3rn5U8qig6Zbbo4XEHFJOdArhWV9Wf9IAIYZNHUA09h3JumLA)
- [Azure - Azure Data Encryption-at-Rest - Azure Security | Microsoft Learn](https://l.facebook.com/l.php?u=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fazure%2Fsecurity%2Ffundamentals%2Fencryption-atrest&h=AUBrQZVm_BuiiWJKR4vWcntq5MK3h_bn5CjUv1pC2wPOB1t7l0ufnPX7kCYmrt10jxK7YG3nB0f8OHsnIJPTHsN6r8M27MSQQXuMYNGRr4--gvVa6ufV80ATzR1uzOowkw3a-adkqTvjEQ)

### Evidence examples

[Q3.1-9 evidence examples](https://developers.facebook.com/docs/resp-plat-initiatives/data-protection-assessment/data-security/version3.1#q319)

## Q3.1-10 Questions - Protecting Platform Data at Rest on Organizational and Personal Devices

### All questions

3.1-10, 3.1-10.a, 3.1-10.a.i, 3.1-10.a.ii, 3.1-10.a.iii, 3.1-10.a.iv, 3.1-10.b, 3.1-10.c, 3.1-10.c.i, 3.1-10.c.ii, 3.1-10.d

### Summary

If your organization allows Platform Data on devices like employee laptops or removable storage (e.g., USB drives), that data is at high risk of unauthorized access if the device is lost or stolen. We require developers to take steps to limit this risk to Platform Data.

If you don’t allow storage of Platform Data on devices, but it is still accessible to members of your organization, we require developers to take steps to limit unauthorized use/storage.

This question asks if you have technical or administrative controls to limit the risk of loss of confidentiality of Platform Data stored on organizational and personal devices.

### Changes from prior version

Changed questionnaire to ask specifically whether technical or administrative controls are in place specific to protection of storage of Platform Data on organizational devices and removable media.

### Additional guidance

**Q3.1-10.a Requirements**

This requirement applies to all developers that have at least one member that could process Platform Data on an organizational or personal device such as a work or personal laptop computer.

If you store Platform Data on organizational devices or removable media:

**You must have EITHER technical controls OR administrative controls** relevant to Platform Data stored on organizational devices (e.g., laptops) and removable media.

**Acceptable Technical Controls:**

| Policy/Procedure Evidence | Implementation Evidence |
| --- | --- |
| Q3.1-10.a.i - A written explanation (e.g., a policy or procedure document) that outlines you have implemented ONE of the following controls:   1. Full disk encryption for all organizational devices where Platform Data is held, or 2. Use of Data Loss Prevention software to monitor and log actions related to the stored Platform Data | Q3.1-10.a.ii - A screenshot that demonstrates you have implemented one of the accepted technical controls (see left). Please note the control must be enforced at an organizational level through a configuration dashboard, ruleset, etc. A screenshot of the control implemented on a single device will NOT be accepted. |

**Acceptable Administrative Controls:**

| Policy/Procedure Evidence | Implementation Evidence |
| --- | --- |
| Q3.1-10.a.iii - Policy/procedure document (must be a file upload) that states BOTH of the following:   1. The allowable business purposes for processing Platform Data on organizational or personal devices 2. A requirement to delete the data when this purpose no longer exists | Q3.1-10.a.iv - Confirm that all people in your organization who may process Platform Data on organizational or personal devices:   1. Have been informed of the acceptable use policy for this data 2. Have acknowledged their understanding of this policy 3. Are informed of this policy as part of their onboarding as new employees |

**Q3.1-10.b, Q3.1-10.c Requirements**

If you do not store platform data on organizational devices but it is still accessible to members of your organization, we require that you forbid storage of platform data on all organizational devices and removable media:

| Policy/Procedure Evidence | Implementation Evidence |
| --- | --- |
| Q3.1-10.b.i, Q3.1-10.c.i - A written policy/procedure document (must be an uploaded file) that clearly states that storage of Platform Data on organizational devices (laptops, tablets, etc.) and removable media (USB devices, phones, etc.) is forbidden.   Please highlight or circle the clause in your policy that relates to this control. If you have data classification and data handling policies to determine controls on platform data storage, please indicate how you have classified Platform Data. | Q3.1-10.b.ii, Q3.1-10.c.ii - Confirm that all people in your organization:   1. Have been informed of the policy prohibiting them from storing Platform Data on organizational or personal devices 2. Have acknowledged their understanding of this policy 3. Are informed of this policy as part of their onboarding as new employees |

**Q3.1-10.d Requirements**

If you store Platform Data neither in a backend environment nor on organizational devices and removable media, please provide a data flow diagram to demonstrate how you are processing Platform Data. Your diagram should:

1. Show how your app makes calls to Meta APIs, such as graph.Meta.com and identify all components that use Platform Data, including those that store, cache, process, or transfer Platform Data across networks
2. Describe the primary use cases (i.e., flows that provide valuable outcomes to users of your app) that you support

### External resources

Not familiar with encryption at rest on organizational and personal devices? Review these resources.

- [CIS: EI-ISAC Encrypt Data at Rest](https://l.facebook.com/l.php?u=https%3A%2F%2Fessentialguide.docs.cisecurity.org%2Fen%2Flatest%2Fbp%2Fencrypt_data_at_rest.html&h=AUDcuJVKJSYeypIZN1Y19DwqIT3btyhk1nNm7J2ICi0ZonKyZf13tqatttxIfcZK-iZYqJ33FC1S8ExtleRSCyTX5SjL-BZqVHDQ14WBebZuG_CfKNiiAdbKtYZqkS9j0s-FU59tVsOoXw)
- [OWASP: OWASP Cheat Sheet Series](https://l.facebook.com/l.php?u=https%3A%2F%2Fcheatsheetseries.owasp.org%2Fcheatsheets%2FCryptographic_Storage_Cheat_Sheet.html&h=AUCs8gbNTekeLZk9bnA1JuxomU8SIHqGHKQ8ByXnKRVqCSSTs6FRQmw08VztUR1LhKEVXOwQjub10uphge0XWd3a_RohLvDcy1vFNHb-7qMHxGy5SjaiX8Sx0zF_cMgHl_6u7iCP4Dsjtg)
- [Apple IOS: FileVault on MAC OS](https://l.facebook.com/l.php?u=https%3A%2F%2Fsupport.apple.com%2Fguide%2Fmac-help%2Fhow-does-filevault-work-on-a-mac-flvlt001%2Fmac&h=AUC82Of7rpKcmSZpzIaxbKMbWaEA3aSg0GLi-_vsMdr0a2Aew_dL5LcowvGMNC6MB_s3SGbOOaN9GZE0LGPc9S4kVwoAoqvyJbs__2Tw59ssY3YfYOYrANK9RCS84NtEK2H3OZZtm5v4Fw)
- [Linux: Linux Disk Encryption](https://l.facebook.com/l.php?u=https%3A%2F%2Fdevconnected.com%2Fhow-to-encrypt-file-on-linux%2F%23%3A%7E%3Atext%3DTo%2520encrypt%2520files%2520using%2520a%2Cthat%2520you%2520want%2520to%2520encrypt.%26text%3DThe%2520%25E2%2580%259Cgpg%25E2%2580%259D%2520command%2520will%2520create%2520a%2520file%2520with%2520a%2520%25E2%2580%259C&h=AUBsvj5FbxR6u_NZ8wLktlzBb1fgqzLaHGmOrAjthdxYkHc90ZT-yy1vHKNlKxTBdGxO-oEzv8tminDav6l5ytSIcGUVh364iBFrY1GGNzoEmLIyL5meSXnpNGD1GDbDAue7_CLFzhGmhg)
- [MS O365: Set up encryption in Microsoft 365 Enterprise](https://l.facebook.com/l.php?u=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fpurview%2Fset-up-encryption&h=AUBpsdIYj3vk7MagkfU75xTDJyP6tknVjNnJcF7dPGEfTj5DbqcUAFSKaE_V2r2J0i9ITOBb-p805d3FGavrBViwtdIb5Ga06vRNXtKqgXg8lSoEH9KcvkoxauqvgN32bcvZH_Ggg7jNqA)

### Evidence examples

[Q3.1-10 evidence examples](https://developers.facebook.com/docs/resp-plat-initiatives/data-protection-assessment/data-security/version3.1#310)

## Q3.1-11 Questions - Protecting Platform Data in Transit

### All questions

3.1-11.a, 3.1-11.b, 3.1-11.c, 3.1-11.a.i, 3.1-11.a.ii

### Summary

Platform Data transmitted across the internet is accessible to anyone that can observe the network traffic. Therefore it must be protected with encryption to prevent those unauthorized parties from being able to read the data.

- Encryption in transit protects Platform Data when it is transmitted across untrusted networks (e.g., the internet) by making it indecipherable except for the origin and the destination devices
- In other words, parties in the middle of the transmission would not be able to read Platform Data even if they can see the network traffic (this is also called a man-in-the-middle attack)
- TLS is the most prevalent form of encryption in transit because it’s the technology that browsers use to secure communications to websites like banks

This section asks if you always protect Platform Data with encryption in transit when sending it over the Internet.

### Changes from prior version

None

### Additional guidance

This requirement applies to all developers who transmit Platform Data over the internet for any reason other than requests directly to Meta:

- Platform Data must never be transmitted across untrusted or third party networks in unencrypted format including transmission of platform data to your cloud environment outside of a Virtual Private Cloud (VPC)
- For all web listeners (e.g., internet-facing load balancers) that receive or return Platform Data, you must:
  - Enable TLS 1.2 or above
  - Disable SSL v2 and SSL v3
  - TLS 1.0 and TLS 1.1 may only be used for compatibility with client devices that are not capable of TLS 1.2 or greater
- Meta recommends, but does not require, that encryption in transit be applied to transmissions of Platform Data that are entirely within private networks, e.g., within a Virtual Private Cloud (VPC)

**Q3.1-11.a Requirements**

| Policy/Procedure Evidence | Implementation Evidence |
| --- | --- |
| Q3.1-11.a.i - Provide a written explanation (e.g., a policy or procedure document) that demonstrates you enable TLS 1.2 encryption or greater for all network connections that pass through, or connect, or cross public networks where Platform Data is transmitted. Your policy should include the following:    1. Platform Data is never transmitted without encryption 2. SSL version 2 and SSL version 3 are never used | Q3.1-11.a.ii - Provide evidence (e.g., a full screen capture of the results of a Qualys SSL report run against one of your web domains) that demonstrates you enable security protocol TLS 1.2 or greater for data in transit. |

The table below summarizes encryption in transit policy for different transmission types:

| Type of Transmission | Encryption in Transit Policy |
| --- | --- |
| To and from end user devices (mobile phones, PCs, tablets, etc.) and the server or cloud infrastructure | - TLS 1.2 or greater must be enabled for compatible devices - TLS 1.0 and 1.1 may be enabled for compatibility with older devices |
| To and from the server or cloud infrastructure and any remote server, cloud infrastructure, or 4th party service | - TLS 1.2 or greater must be enforced |
| To and from components entirely within the private data center, server, or cloud infrastructure | - TLS encryption is recommended but not required for Platform Data transfers that are entirely within a private cloud network |
| To and from Meta and any device, server, or cloud infrastructure | - Out of Scope for Data Protection Assessment - Meta controls the TLS policy for these transfers |

### External resources

Not familiar with encryption in transit? Review these resources.

- [NCSC (UK): UK National Cyber Security Centre - data in transit](https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.ncsc.gov.uk%2Fcollection%2Fcloud%2Fthe-cloud-security-principles%2Fprinciple-1-data-in-transit-protection&h=AUBP6wzXeszTZMsMmftzXEOHhwxWkhamgEckLJABDy_NMwr3nPb60URr8Nb9sSIa_6qjACHWAhZTG7-rtmEVTI_6q6qZ9ETYH1qrXP5Go_UsH7VZIrn3MYYkHUZSm5rXJNAVhs6RctWRmQ)
- [AWS Well Architected: SEC09-BP02 Enforce encryption in transit](https://l.facebook.com/l.php?u=https%3A%2F%2Fdocs.aws.amazon.com%2Fwellarchitected%2Flatest%2Fframework%2Fsec_protect_data_transit_encrypt.html&h=AUALjdglWlh_Sn5Wy2dPY30j232h5CuxS_K-3PrA10stChkbeinjhtWQCdOZRyhBDJNPM3U0FzKOqerEll2Gz0g-vU73_1_WrmtGFPohyrefQ-40jy_vdKtLOUc5cc6viGjjArymtHsoZRUQxk0tazPJq1Q)
- [LinkedIn Collaborative Articles: What are the best practices for testing and auditing your data encryption in transit and at rest?](https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.linkedin.com%2Fadvice%2F0%2Fwhat-best-practices-testing-auditing-your%23how-to-encrypt-data-in-transit&h=AUALweraxofUFkeIyb28zSIOnWf9Vq9QfozMCe7rRXafgsxcTky5bnp3ZC-aGrWOnKHxv1mu_E7kO3bGoJelmgrKt_k13yZkORh3XSoFFToq8hx0EoMVVXm0kktFTgWRnTcgmA33nKz6sQ)

### Evidence examples

[Q3.1-11 evidence examples](https://developers.facebook.com/docs/resp-plat-initiatives/data-protection-assessment/data-security/version3.1#311)

## Q3.1-12 Questions - Application and Cloud Security Testing

### All questions

3.1-12.a , 3.1-12.a.i, 3.1-12.a.ii, 3.1-12.b, 3.1-12.b.i, 3.1-12.b.ii, 3.1-12.c, 3.1-12.c.i, 3.1-12.c.ii

### Summary

You must test for vulnerabilities and security issues so that they can be discovered proactively, ideally preventing security incidents before they happen

- Developers write software and operate apps and systems to process Platform Data
- These apps and systems may contain security vulnerabilities that malicious actors can exploit, putting Platform Data at risk
- You must take steps to find and resolve these kinds of vulnerabilities

This section asks about steps you take to test your software and cloud configuration for vulnerabilities and security issues.

### Changes from prior version

- Added a question about the specific tool or process you use to test your software or backend environment for vulnerabilities.
- Added a question about your approach for testing your cloud environment for security misconfigurations, if applicable.

### Additional guidance

**Q3.1-12.a, Q3.1-12.b Requirements**

This requirement is applicable to all developers.

| Policy/Procedure Evidence | Implementation Evidence |
| --- | --- |
| Q3.1-12.a.i, Q3.1-12.b.i - Provide a written explanation (e.g., a policy or procedure document) that states how you test the software you use to process Platform Data for vulnerabilities and security issues.   The following testing procedures should all be included in your written explanation:   1. Test for security vulnerabilities at least once every 12 months 2. Have a process to triage the findings based on severity 3. Ensure that high severity vulnerabilities, which could lead to unauthorized access to Platform Data, are remediated in a timely manner | Q3.1-12.a.ii, Q3.1-12.b.ii - You must have tested your software used to process Platform Data for security vulnerabilities by conducting ONE of the following:   - A penetration test of your app/system, OR - A vulnerability scan / static analysis of your software    The following details should be included in your evidence:   1. An explanation of the scope and testing methodology 2. The date when the testing activity took place (To be acceptable, the date must be no earlier than 12 months prior to the date that we notified you about this assessment) 3. If applicable, a summary of any unremediated critical and high severity vulnerabilities   [Remove or redact sensitive information](https://developers.facebook.com/docs/development/maintaining-data-access/data-protection-assessment/data-security#redact-evidence) such as detailed vulnerability reproduction steps from the evidence before submitting. |

**Vulnerability Disclosure Program (VDP)**

If you are operating a functioning Vulnerability Disclosure Program (VDP), e.g., using the [BugCrowd](https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.bugcrowd.com%2Fglossary%2Fvulnerability-disclosure-program-vdp%2F%3Ffbclid%3DIwAR1kjHH1T9UiElOPLlgUM2DJKlW8RQfCyVVCEXm_oGKOblW3F39OrqDewXw&h=AUBaJrO-zyx43iIVWaIi8ZezFwiXz5WoZ174q-rYskwlZhJRxxgmt--LvkvPsQ1MIftcvziZVNnY2-uCtloje0O3nfQcFv3Ht_kctFS6xQ8QdhdMGmYwBKn5jVclzOjitqYrdq4Pa74oBw), [HackerOne](https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.hackerone.com%2Fproduct%2Fresponse-vulnerability-disclosure-program%3Ffbclid%3DIwAR34jZtGcKVi3CTwRzUdSpjYovOu04Ak0BHMOflmtZyd7ZIz4eGyJ0sV778&h=AUD8vOj2re7UW08m9z6CmpIM6Q4k3GcRTf46bRlDpFnxI397-M7H1i2hUph_WJHsnl5tV7DNZznEtH_IlfHMGZ09ZvGaXxGFSEvYvq2SYmblt1AMErI3kmAtxO9kjLdQ0naKPJlX4zQ-Bw) platforms, or another platform meeting industry standards, you may present this as an alternative protection instead of a pen test or vulnerability scan. To demonstrate this, you must submit the following evidence:

| Policy/Procedure Evidence | Implementation Evidence |
| --- | --- |
| Q3.1-12.a.i, Q3.1-12.b.i - Provide a written description or policy/procedure document that describes your vulnerability disclosure program. Your document should state that:    1. There are no exclusions to the scope of the VDP relevant to the way you process Platform Data 2. Submitted (valid) vulnerabilities are assigned a severity score, e.g., using CVSS 3.1 3. Vulnerabilities are resolved in a reasonable amount of time, typically fewer than 90 days after the submission date | Q3.1-12.a.ii, Q3.1-12.b.ii - Provide screenshot proof of use of your vulnerability disclosure program:    1. A statement of scope and how that interrelates with the software used to process Platform Data, AND 2. A report of the actual vulnerability submissions in the program over the past 12 months from your DPA dispatch date. The report should include the vulnerability title, submission date, resolution date (if resolved) and severity category / score. Our team will check whether or not that there is actual ongoing vulnerability research and reporting within the past 12 months prior to your DPA dispatch date, typically indicated by at least 1 valid vulnerability report per month. If you have more than one app, we would typically expect the number of vulnerability reports through your program to scale up proportionally.    [Remove or redact sensitive information](https://developers.facebook.com/docs/development/maintaining-data-access/data-protection-assessment/data-security#redact-evidence) such as detailed vulnerability reproduction steps from the evidence before submitting. |

**Q3.1-12.c Requirements**

If you store Platform Data in a backend environment hosted by a cloud provider, you must test your cloud configuration for security issues. This requirement applies irrespective of the hosting approach (e.g., BaaS, PaaS, IaaS, self hosted, or hybrid), except if you are using a no-code backend.

| Policy/Procedure Evidence | Implementation Evidence |
| --- | --- |
| Q3.1-12.c.i - Provide a written explanation (e.g., a policy or procedure document) that includes all of the following:    1. Test for security vulnerabilities at least once every 12 months 2. Have a process to triage the findings based on severity 3. Ensure that high severity vulnerabilities, which could lead to unauthorized access to Platform Data, are remediated in a timely manner | Q3.1-12.c.ii - You must have tested the cloud environments you use to process Platform Data for security misconfigurations. The evidence you provide must include all of the following:    1. An explanation of the scope and testing methodology 2. The date when the testing activity took place (To be acceptable, the date must be no earlier than 12 months prior to the date that we notified you about this assessment) 3. If applicable, a summary of any unremediated critical and high severity vulnerabilities    [Remove or redact sensitive information](https://developers.facebook.com/docs/development/maintaining-data-access/data-protection-assessment/data-security#redact-evidence) such as detailed vulnerability reproduction steps from the evidence before submitting. |

### External resources

Not familiar with application and cloud security testing? Review these resources.

- [NIST: Open source and commercial SAST tools](https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.nist.gov%2Fitl%2Fssd%2Fsoftware-quality-group%2Fsource-code-security-analyzers%3Ffbclid%3DIwAR1VZ6_Kh35ZXkZ4CIVNnBtMI7YngIQEinvpeZGBcHGvyFUOzqrO1nZkiBU&h=AUATs3wlVeIc8wt93JIrR1XsBTVMZeSxugSOmjppida7rbJwBDdMdKPd6hCkWoAwbs6Wpck_P3wO54ZsfeSumEG9R57ctc5kkzLv6pPs8H4ocNc9h43g0tqX_jJHsUn9QspoVXEvh0iuZQ)
- [NIST: NISTIR 8397 Guidelines on Minimum Standards for Developer Verification of Software](https://l.facebook.com/l.php?u=https%3A%2F%2Fnvlpubs.nist.gov%2Fnistpubs%2Fir%2F2021%2FNIST.IR.8397.pdf&h=AUDlqR_TAz_Q5FVIOIKQvgAz6HZJFjXmolaFbD9bcFwpLosygnpsz3r39B6hQU6tQtUeVVjfFgwp6Lu4Z02umegr8JEYGa5kEWYZWhLMgCoBVjvaWlbobdb5HGYiqePbScLLACyz5d2QpQ)
- [OWASP: OWASP Code Review Guide v2](https://l.facebook.com/l.php?u=https%3A%2F%2Fowasp.org%2Fwww-pdf-archive%2FOWASP_Code_Review_Guide_v2.pdf&h=AUBtG1L2h004pjkZffCPJykYyLIwWVrOK0s6yyf6CPwa4Fjn3RIEUn4odXGySFLEtQxIdCFD4_uuMxD4PI2ZJXRo68tD5_XMDJQiNP5PkiNpspIFqGj8EgTzgc91tX1AZWfaP0NXZI7YHA)
- [GitHub: AKS DevSecOps Workshop](https://l.facebook.com/l.php?u=https%3A%2F%2Fazure.github.io%2FAKS-DevSecOps-Workshop%2Fmodules%2FModule3%2Fintro.html&h=AUATcPg-FmpG3vmdzc_gZ6vAcA7BROV1NQcATaEZkrlNsUzLiTVftQlLYlQ7wissiaNzamh2F6jyNcDr84_VxJ5qZ24V5-TaIqfxVvJDiBHwNh4LDe-1gZMLjb5px5iLB9J2UTlZg1WfhQ)
- [BugCrowd:10 Essentials to Look for in a Crowdsourced Security Platform](https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.bugcrowd.com%2Fblog%2F10-essentials-to-look-for-in-a-crowdsourced-security-platform%2F&h=AUBou1uiEQfiUM2A3r6gPm1KEEa4l1SP3UutOoSQhhC8ZnpIegrzEjufqbUTJ8l7UHuGbM49NArzOmqTRi-9bWKVJ72X0d95Ff68qskIn3dULhOE8gSLB3oyPva7VyFUEHSsaWMfpW41og)
- [AWS Security Hub: SEC 11. Incorporate and validate the security properties of applications throughout the SSDLC](https://l.facebook.com/l.php?u=https%3A%2F%2Fdocs.aws.amazon.com%2Fwellarchitected%2Flatest%2Fframework%2Fsec-11.html&h=AUDu7hD4gVDx22yuMbIY3oiAdvfTDUd3Xkur5_FgqfGFCDPFvE9cfYG8Fhpi-4F8Ed7vJ1hdWko4rLjBAUc9EkfPbdL4XHyjP8-dkGIvWYh_Opi__JnXBR7oqCuv3KfoBm4tmE7Zzn1wIw)
- [NCC Group: Best Practices of the use of SAST within a Real-World SDLC](https://l.facebook.com/l.php?u=https%3A%2F%2Fresearch.nccgroup.com%2Fwp-content%2Fuploads%2F2020%2F07%2Fncc-group-best-practices-for-static-code-aanalysis.pdf&h=AUAysWNgQo3gPFGWS8OvPuVQNXrlMwjEN-Q3-Q2NsMjK3CoxislXBhGcao4J-Ol-cewPq1ue0RcQHvR4E56VBO3tYeolO7fhf3rpAP36UgFZjGzEwekpLWibDdPLENFqQvVtwq93_DEHHw)
- [CIS Benchmarks: Foundational Cloud Security with CIS Benchmarks](https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.cisecurity.org%2Finsights%2Fblog%2Ffoundational-cloud-security-with-cis-benchmarks&h=AUDlM-p3w0gFhZ67cHoV7BC4Ke8H0VfrQkegr8qVZMNwIJOZoB_PqcobVLsJ0pdV6n1PsZSMQmcGeDrs_IDgExyIGMz9MofnJ5t7_1NV0JlWRsJRHNssyN4_xWeW4I6p3NK0ub0qKocH4A)
- [Scout Suite: GitHub - nccgroup/ScoutSuite: Multi-Cloud Security Auditing Tool](https://l.facebook.com/l.php?u=https%3A%2F%2Fgithub.com%2Fnccgroup%2FScoutSuite&h=AUDy8USo0vL-8lcdK4Imhs1PTsvtV_AZZvVx1gWka19Y3H9s2wbjBz5cwC2Q8di932oSqN3ydOA8WQdlj7rDFvfpRzOrQe2nmczt7juOitK21__iQNXRe4IoAbHF_iP2LkqZYvYAMYDs8g)

### Evidence examples

[Q3.1-12 evidence examples](https://developers.facebook.com/docs/resp-plat-initiatives/data-protection-assessment/data-security/version3.1#312)

## Q3.1-13: Protect the App Secret and Meta Access Tokens

### All questions

3.1-13.a, 3.1-13.b, 3.1-13.c, 3.1-13.c.i, 3.1-13.c.ii, 3.1-13.d, 3.1-13.d.i, 3.1-13.d.ii

### Summary

App secrets and access tokens are fundamental to the security of how Meta APIs make decisions about what actions to allow. If an unauthorized party gains access to these credentials they could call Meta APIs - impersonating the real developer - and take any of the actions that we have granted the app (e.g., reading data from Meta APIs about an app’s users).

- You have access to sensitive credentials as a part of the use of Meta’s Platform. Specifically:
  - Access Token - When people authorize the app, the software gets a credential called an access token that’s used in subsequent API calls
  - App Secret - Meta shares an app secret with developers with the expectation that only trusted parties (e.g., app admins) within the organization have access to this secret
- An unauthorized party who is able to read these sensitive credentials can use them to call Meta APIs as if they are you (this is sometimes called token impersonation) leading to unauthorized access to Platform Data
- Therefore these credentials must be protected from unauthorized access to prevent impersonation

This section asks questions about how you protect these attributes on the client and server side, as applicable.

### Changes from prior version

Refactored to ask about protecting app secret and access tokens on client and backend environments separately.

### Additional guidance

**Q3.1-13.c Requirements**

This question pertains to protecting Meta User Access Tokens stored in your backend environment.

| Policy/Procedure Evidence | Implementation Evidence |
| --- | --- |
| Q3.1-13.c.i - Provide a written explanation (e.g., a policy or procedure document) that describes your approach to protecting Meta User Access Tokens:   Your written explanation should include:   1. A description of how user access tokens are protected from unauthorized read access 2. A requirement that user access tokens must never be written to log files in cleartext (unencrypted) form | Q3.1-13.c.ii - Provide screenshot proof that Meta User Access Tokens are:   - Stored in a data vault / secrets manager   OR - Encrypted at the application or field/column level   If access tokens are not encrypted/ protected server side, you must:   1. Store the app secret in a vault (or is using a Key Management System - KMS)    AND 2. Enable the “Require App Secret” setting in their developer console    Make sure that you do not include (i.e., remove or redact) the plaintext values of any secrets or access tokens in the evidence that you submit. |

**Q3.1-13.d Requirements**

This question pertains to storage of Meta App Secrets.

| Policy/Procedure Evidence | Implementation Evidence |
| --- | --- |
| Q3.1-13.d.i - Provide a written explanation (e.g., a policy or procedure document) that describes your approach to protecting the Meta App Secret. Your response should include:    1. Description of how the app secret is protected from unauthorized read access On Server Side - ONE of the following must be true:  - Must be in a data vault or a secrets manager, OR - Must be on a secure server in an encrypted format via app-level encryption (not stored in plain text,) OR - Must not be stored at all on the server side  2. A requirement that the app secret must never be written to log files in cleartext (unencrypted) form | Q3.1-13.d.ii - Provide screenshot proof that the Meta App Secret is either:   - Stored in a data vault / secrets manager   OR - Encrypted at the application or field/column level   If the developer does not protect or encrypt the app secret   - The “Desktop/Native” Type is enabled in their Meta developer console.   Make sure that you do not include (i.e., please remove or redact) the plaintext values of any secrets or access tokens in the evidence that you submit. |

**Acceptable Alternative Protections**

1. If you do not protect access tokens stored server side with a data vault or via app-level encryption, you may:

1. Protect the app secret by using a vault or application encryption where the key is only accessible to the app
2. AND configure the app to [require app secret proof for all API calls to Meta](https://developers.facebook.com/docs/graph-api/securing-requests%20/#require-proof)

2. If approach #1 above is not viable (i.e., cannot require appsecret proof because it would block certain necessary API calls), then Meta will consider any other controls that you have in place to limit the risk of unauthorized use of the access tokens compared to the the risk of misuse of stored access tokens

### External resources

- [OWASP Secrets Management Cheat Sheet](https://l.facebook.com/l.php?u=https%3A%2F%2Fcheatsheetseries.owasp.org%2Fcheatsheets%2FSecrets_Management_Cheat_Sheet.html&h=AUDf9A52rFmk9X468Qh3AtqApr6V7XT8EtLdKn9QYY3AnyTISU8Lz11SkJ6a0EkTD2GyUQnyI6clw1wIbd9LE_kEiao9xahBJmJbVHguGr9fAkwlC0rwP_2RaSi7VO0-JTrNTfIqlibuow)
- [NIST Digital Identity Guidelines](https://l.facebook.com/l.php?u=https%3A%2F%2Fpages.nist.gov%2F800-63-3%2Fsp800-63b.html&h=AUDyOwTQOYgtWoOFCkhBWbGvQhiWFoIrTJ6bhvUcc2WpqId5hNojdXCrZ8Tf4Ofk7lOytr6TXoGKuKChK35GBsMq__4zJUPMZYFSg0VYg_vPR7x2S8AP_2E7P8LAULONglhBUMbbk69neA)
- [AWS Secrets Manager Service Provider Documentation](https://l.facebook.com/l.php?u=https%3A%2F%2Faws.amazon.com%2Fsecrets-manager%2Fresources%2F%3Fsecrets-whats-new.sort-by%3Ditem.additionalFields.postDateTime%26secrets-whats-new.sort-order%3Ddesc%26aws-secrets-manager-resources-blog.sort-by%3Ditem.additionalFields.createdDate%26aws-secrets-manager-resources-blog.sort-order%3Ddesc&h=AUAPRttMF19nWuw7fzN7uJ_zOPnFM7iXNV9QA-QdF6EKrJlGYJP_zeRnIArrg7bDIIn4FCpPikyrvKrV-zoyNQKaMoxmu4cXVs_gm8v1cZOy2JQgIpF6L2Ge_Se_sc2dp_tLgHlDB0WNtw)
- [GCP Secret Manager Service Provider Documentation](https://l.facebook.com/l.php?u=https%3A%2F%2Fcloud.google.com%2Fsecurity%2Fproducts%2Fsecret-manager&h=AUBpWkaNXWvC_h2MbE7zOQgVvgjkqPh9BXtA4cqLbwMBw-mQ8rwcmqB9rzWB6b6HpXHyfJa7QbPlx1nDRE_dZAOxfW05GG4kGdwvS1WmkiCrsOVsTb3NhSB0aLHGmOoMud_7W-PVoZ76vw)

### Evidence examples

[Q3.1-13 evidence examples](https://developers.facebook.com/docs/resp-plat-initiatives/data-protection-assessment/data-security/version3.1#313)

## Q3.1-15 Questions - Protecting Accounts from Unauthorized Access

### All questions

3.1-15.a, 3.1-15.b, 3.1-15.c, 3.1-15.d, 3.1-15.e, 3.1-15.e.i, 3.1-15.e.ii

### Summary

A common technique used by adversaries to gain access to confidential data is to start by gaining access to tools that a developer uses to build or operate their app/system. Sophisticated tools exist to hack into accounts that are protected only by password and present the risk of account takeover attacks. The intent of these questions is to ensure developers have implemented multi-factor authentication to mitigate these risks.

This section asks about how you protect accounts against unauthorized access using multi factor authentication or another approach.

### Changes from prior version

Refactored to ask about protecting against unauthorized access using multi-factor authentication or another approach for each of these separately:

- Collaboration and communication tools
- Code repository
- Backend software deployment tools
- Backend administrative console
- Remote access to backend servers

### Additional guidance

**Q3.1-15.e Requirements**

Related to an organization’s processing of Platform Data, remote access to all tools listed above (if applicable) must be protected with multi factor authentication (i.e., not simply a password):

| Policy/Procedure Evidence | Implementation Evidence |
| --- | --- |
| Q3.1-15.e.i - Provide a written explanation (e.g., a policy or procedure document) that states your requirements for multi-factor authentication (MFA) or other measures to prevent account takeover.   Your explanation should include requirements for all access to any collaboration and communication tools, code repositories, software deployment tools, backend administrative tools, and remote access to servers via a tool like SSH. | Q3.1-15.e.ii - Provide screenshot proof that MFA is enforced on ONE or MORE of the tools applicable to the environment that are listed above (i.e., collaboration tools, code repository, cloud/server deployment, cloud/server administrative portal, cloud/server remote access)   - For example, if you’re using an SSO provider this may be a screenshot of a global configuration for the organization or a screenshot of a per-app configuration - If you do not have an SSO provider, this may be a screenshot of the configuration of a particular tool   Evidence provided should show that MFA is enforced for all employees and users that have access to your remote development environment. A screenshot of MFA enabled on a single endpoint device will not be accepted. |

**Acceptable Alternative Protections**

Meta recommends that developers protect against account takeover by requiring MFA. However, when MFA is not used, developers must take other steps to protect against unauthorized access in line with industry best practices for password complexity rules (see The Center for Internet Security (CIS) Password Policy Guide here: [https://www.cisecurity.org/insights/white-papers/cis-password-policy-guide](https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.cisecurity.org%2Finsights%2Fwhite-papers%2Fcis-password-policy-guide&h=AUDoahbGNdHZaaDPxyqcxcSQbkoQaM3KbVQSm0M0hEwlvmsXQ9Z-2Ly5PqsKliUstqPrh33aknh-g0D6suLClRS_Ed4tKNlU0B4IAyqy0wIyf0UY3kRPjaGeasHmfaTCiKVz8zrABMBneg)).

| Policy/Procedure Evidence | Implementation Evidence |
| --- | --- |
| Q3.1-15.e.i - Provide a written explanation (e.g., a policy or procedure document) that demonstrates you enforce:   1. Password specific requirements  - Enforce password length of at least 8 characters - Require at least one number and/or special character - Restrict password reuse, or formally define number of iterations before reuse is allowed - Require minimum password age of 1 day (i.e., if a password is changed, the system doesn’t allow it to be changed again for 24 hours)  2. Authentication backoff delays 3. Automatic account lockouts with at most 10 failed login attempts | Q3.1-15.e.ii - Provide a global configuration or dashboard demonstrating password complexity policies. |

### External resources

Not familiar with protecting accounts from unauthorized access? Review these resources.

- [NIST: NIST SP 800-218](https://l.facebook.com/l.php?u=https%3A%2F%2Fcsrc.nist.gov%2Fpubs%2Fsp%2F800%2F218%2Ffinal&h=AUA9bv7Wb7GSXnmVk0-jVzELJ9UK0Que_PGjoEPIokQbKH19EfRax1Qv6aXkX2e6u6F-p2lD1YRqcTFD1e9MWZRrc8amI5bbDpP30JAcvrfk0kyGaI-xuF0dziOSApJ8oBDGfIIHe3YOEcDaQroUxQsse-U)
- [OWASP: Enforce Access Controls](https://l.facebook.com/l.php?u=https%3A%2F%2Fowasp.org%2Fwww-project-proactive-controls%2Fv3%2Fen%2Fc7-enforce-access-controls&h=AUDPzAkKPvMn1c8M4iBxanW13DO4SUTWHayn-8w96H9N2I9-Ypi1ayzTLEp1fuBIBYOHqMBbrNgMwLWFH6Q8WYgyL2kaWm29WtlZjyk6aMN_hKKoAznNtg4xSNoptbMzGq17z1w8fKAj5A)

### Evidence examples

[Q3.1-15 evidence examples](https://developers.facebook.com/docs/resp-plat-initiatives/data-protection-assessment/data-security/version3.1#315)

## Q3.1-16 Questions - Access Controls

### All questions

3.1-16, 3.1-16.a, 3.1-16.a.i, 3.1-16.a.ii

### Summary

Accounts are the basic unit of management for granting people access to systems, data, and administrative functions. Having good account management hygiene is an important part of preventing unauthorized use of accounts to gain access to Platform Data. The intent of this question is to ensure developers are following the principle of least privilege and have a systematic way for managing accounts, granting permissions or privileges, and revoking access when it’s no longer needed.

This section asks about the systems and processes you use to manage access to your systems / tools.

### Changes from prior version

Refactored to ask a question about the specific processes you have in place for reviewing and revoking access under different circumstances.

### Additional guidance

You must have a tool or process for managing accounts for each of the these tools/systems/apps:

- Those used to communicate with one another, e.g., Slack or business email
- Those used to ship software, e.g. code repository and
- Administer and operate the system (as applicable to processing Platform Data)

You must regularly review (i.e., not less than once every 12 months) access grants and have a process for revoking access when: (1) it’s no longer required, (2) no longer being used, and (3) when a person departs the organization

Meta does not require:

- That any particular tool be used – a developer may use a directory product like Google Cloud identity or Microsoft Azure Active Directory, a cloud product like AWS Identity and Access Management (IAM), or use a spreadsheet that is kept up to date regularly.
- That there be a single consolidated tool for managing accounts across these various access types.

**Q3.1-16.a Requirements**

| Policy/Procedure Evidence | Implementation Evidence |
| --- | --- |
| Q3.1-16.a.ii - Provide a written explanation (e.g., a policy or procedure document) that covers your account management practices. We expect this document to contain procedures for:   - Revoking access that is no longer required - Revoking access that is no longer being used - Revoking access promptly when a person leaves your organization (e.g., when an employee resigns or is terminated) - Reviewing access at least once every 12 months | Q3.1-16.a.iii - Provide evidence from AT LEAST ONE of the following tools or processes that is in place to manage accounts (or denote as not applicable to the environment):   - Business email and collaboration tools - Code repository - Cloud/server deployment tools - Cloud/server administrative portal - Cloud/server remote login (e.g., SSH or remote desktop)   For example you could provide evidence that demonstrates people that have departed your organization have had their access to these tools revoked |

### External resources

Not familiar with access controls? Review these resources.

- [NIST: NIST SP 800-218](https://l.facebook.com/l.php?u=https%3A%2F%2Fcsrc.nist.gov%2Fpubs%2Fsp%2F800%2F218%2Ffinal&h=AUCNcYV7HGnUiQo4gojlZUylbHrAzrsi6mzM06ne-QGnsdPeky-VnNSr75pB6NiwXqf3gMb0fpG2cHjfmhEbIfPYZGSLoYPU_xi4vj9LxeOELlRe1Wwu2jWZjKPsOmJxho9c8UmAJ5NZ1Q)
- [OWASP: Enforce Access Controls](https://l.facebook.com/l.php?u=https%3A%2F%2Fowasp.org%2Fwww-project-proactive-controls%2Fv3%2Fen%2Fc7-enforce-access-controls&h=AUDlNNiM-Zpt3nGnHt5kQHIdSg2Hv4lJmbpbvUMpmqRwJv5O9wp6TPBJ_JxHARWVvCjyKP7R5sW3WcvyTZxUiNXxNDXa1kGfpa6WhZIu4bnKSrXXsGTgB0TUGcwuLmm288nONfeIrDLgwQ)

### Evidence examples

[Q3.1-16 evidence examples](https://developers.facebook.com/docs/resp-plat-initiatives/data-protection-assessment/data-security/version3.1#316)

## Q3.1-17 Questions - Keep Software Up to Date

### All questions

3.1-17.a, 3.1-17.a.i, 3.1-17.a.ii, 3.1-17.b, 3.1-17.b.i, 3.1-17.b.ii, 3.1-17.c, 3.1-17.c.i, 3.1-17.c.ii

### Summary

Software components are routinely updated or patched to resolve security vulnerabilities, and eventually these components will reach their end of life when they are no longer supported. Developers who package or rely on these components must keep up to date to avoid running software with known vulnerabilities. Therefore, developers using Meta’s platform must have a systematic way to identify, prioritize, and apply patches for all relevant parts of their tech stack.

This section asks about the systems and processes you use to keep software up to date.

### Changes from prior version

Refactored to ask about your approach for keeping different types of software up to date, in separate questions:

- Third-party software in your backend environment
- Third-party code in your mobile app
- Other third-party software used by people in your organization to build and operate your app

### Additional guidance

For the following software components, as applicable, you must have a defined and repeatable way of identifying available patches that resolve security vulnerabilities, prioritizing based on risk, and applying patches as an ongoing activity:

1. Libraries, SDKs, packages, app containers, and operating systems used in a cloud or server environment
2. Libraries, SDKs, packages used on client devices, e.g., within mobile apps
3. Operating systems and applications used by members to build and operate the app/system, e.g., operating systems and browsers running on employee laptops

Meta does not require the use of any particular tool for these activities. It’s common that an organization would use different approaches for keeping different types of software up to date (e.g., libraries that are packaged with the app vs operating system updates for employee laptops).

This requirement applies irrespective of the hosting approach (e.g., BaaS, PaaS, IaaS, self hosted, or hybrid), although the set of components that you are responsible for keeping up to date will vary
Start by identifying the in-scope types of software in the environment, e.g., Libraries, SDKs, Packages, Virtual Machine images, app containers, and operating systems, Browsers, operating systems, and other applications used by the employees / contributors.

You may have one or more tools that you use for the following activities:

- Inventory - document via a screenshot or document that a tool or process that, ultimately, represents a list of in-scope libraries, packages, SDKs, containers, app servers and operating systems that need to be patched. There needs to be inventories for a representative of the software types (e.g., cloud app(s), client app(s), employee devices).
- Identifying available software patches - a tool or process must exist for identifying security patches that exist that are relevant to the inventory.
- Prioritizing - there needs to be a tool or process (e.g., Jira tickets, GitHub issues, tracking spreadsheet) by which relevant patches are assigned a priority
  - Patching
  - Document via a screenshot or document that demonstrates that, after relevant patches have been identified and prioritized, that they are then rolled out into the various destinations.
- Include policies around time to resolve and use of End of Life (EOL) software.

**Q3.1-17.a Requirements related to third-party software in your backend environment, if applicable:**

| Policy/Procedure Evidence | Implementation Evidence |
| --- | --- |
| Q3.1-17.a.i - Provide a written explanation (e.g., a policy or procedure document) that describes how you keep code and backend environments updated. Your response should describe that your patch management system:   1. Has a defined and repeatable way of identifying patches in third-party software that resolve security vulnerabilities 2. Prioritizes available patches based on risk (e.g., based on CVSS severity) 3. Applies patches as an ongoing activity | Q3.1-17.a.ii - Provide screenshot evidence that shows how you keep code and backend environments updated. This evidence can come in the form of:   1. Dependency Scanners - The following details should be included in your evidence:  - An explanation of the scope and testing methodology - The date when the testing activity took place (To be acceptable, the date must be no earlier than 12 months prior to the date that we notified you about this assessment.) - If applicable, a summary of any unremediated critical and high severity vulnerabilities  2. OR a spreadsheet or equivalent tool for manually tracking what services you are using and what needs to be updated |

**Q3.1-17.b Requirements related to third-party code in your mobile app, if applicable:**

| Policy/Procedure Evidence | Implementation Evidence |
| --- | --- |
| Q3.1-17.b.i - Provide a written explanation (e.g., a policy or procedure document) that describes how you keep third-party code in your mobile app updated. Your response should describe that your patch management system:   1. Has a defined and repeatable way of identifying patches in third-party software that resolve security vulnerabilities 2. Prioritizes available patches based on risk (e.g., based on CVSS severity) 3. Applies patches as an ongoing activity | Q3.1-17.b.ii - Provide screenshot evidence that shows how you keep third-party code in your mobile app updated. This evidence can come in the form of:   1. Mobile dependency scans - The following details should be included in your evidence:  - An explanation of the scope and testing methodology - The date when the testing activity took place (To be acceptable, the date must be no earlier than 12 months prior to the date that we notified you about this assessment.) - If applicable, a summary of any unremediated critical and high severity vulnerabilities  2. OR a spreadsheet or equivalent tool for manually tracking what services you are using and what needs to be updated |

**Q3.1-17.c Requirements related to other third-party software used by people in your organization to build and operate your app, if applicable:**

| Policy/Procedure Evidence | Implementation Evidence |
| --- | --- |
| Q3.1-17.c.i - Provide a written explanation (e.g., a policy or procedure document) that describes how you keep third-party software and antivirus software on organizational devices updated. Your response should describe that your patch management system:   1. Has a defined and repeatable way of identifying patches in third-party software that resolve security vulnerabilities 2. Prioritizes available patches based on risk (e.g., based on CVSS severity) 3. Applies patches as an ongoing activity | Q3.1-17.c.ii - Provide screenshot evidence that shows how you keep third-party software and antivirus software on organizational devices updated. This evidence can come in the form of:   1. A tooling configuration that shows how you push OS/software updates across your organization such as Chef, OR 2. a tooling configuration that shows that antivirus software is set to automatically update across your organization, OR 3. a spreadsheet or equivalent tool for manually tracking what services you are using and what needs to be updated |

### External resources

Not familiar with keeping software up to date? Review these resources.

- [OWASP - OWASP Vulnerable Dependency Management Cheat Sheet](https://l.facebook.com/l.php?u=https%3A%2F%2Fcheatsheetseries.owasp.org%2Fcheatsheets%2FVulnerable_Dependency_Management_Cheat_Sheet.html&h=AUDvMctbWJA-8-h2vJM8KWGGnpIPJjau3Kw0Y30mnVMRWzn7yMJyKg3syTPZYLSydyDMonOpHUBGXYY76WuJRzgdBZ-LBSzdH6y7lSo6VXnPu5L2Ng00PahmyN-wqdTYg1UyOsTK7m2Urg)
- [OWASP OWASP Checking for Weaknesses in Third Party Libraries](https://l.facebook.com/l.php?u=https%3A%2F%2Fmas.owasp.org%2FMASTG%2Ftests%2Fios%2FMASVS-CODE%2FMASTG-TEST-0085%2F%23overview&h=AUB89gJT6CYdHkXIkVuI9s8S2EUaeu180FQfohCcwiiv5GkyRa6y0SVx6VCigLHIchIGglbc1WG8gRetTyX8IdMjtjk4ijBn8f0hbqsX2TdQ6HKHnOlu_xIIQCQpvgAkpHC3t9fRTIgB4A)
- [CSF Tools - 7: Continuous Vulnerability Management - CSF Tools](https://l.facebook.com/l.php?u=https%3A%2F%2Fcsf.tools%2Freference%2Fcritical-security-controls%2Fversion-8%2Fcsc-7%2F&h=AUAWWQdu5s5ukF_3VveVxWWZnpAi4zsEahHQNVFlnrU_eF7uQ9_jdTu6_IwV4qnBApirfnYWn4UbN28AlahPEwImozpwRwYYf81Fok4rJkxHCADIpJHb1zqsavaZG1NvAgWhaEPLdkPsSQ)
- [AWS - AWS SEC 11 incorporate and validate the security properties of applications throughout the design, development, and deployment lifecycle](https://l.facebook.com/l.php?u=https%3A%2F%2Fdocs.aws.amazon.com%2Fwellarchitected%2Flatest%2Fframework%2Fsec-11.html&h=AUCZTmZXaI1qMCDCmRlL-0vONnyWN5sJ9nBKqz6tYlnwix9VvRs8dfUMMiRwjh7rT10ABTnjm686LO5-J7he13sdRWYcx3KfQs2y9UhBMSMAD9HHIsOQUSbrUrXiL0ymQyzJcNnz3dJn_w)

### Evidence examples

[Q3.1-17 evidence examples](https://developers.facebook.com/docs/resp-plat-initiatives/data-protection-assessment/data-security/version3.1#317)

## Q3.1-22 Questions - Administrator and Application Logging in Backend Environment

### All questions

3.1-22, 3.1-22.a, 3.1-22.a.i, 3.1-22.b, 3.1-22.b.i, 3.1-22.b.ii, 3.1-22.b.iii, 3.1-22.c, 3.1-22.d, 3.1-22.e, 3.1-22.e.i, 3.1-22.e.ii, 3.1-22.e.iii, 3.1-22.f, 3.1-22.f.i, 3.1-22.f.ii, 3.1-22.g, 3.1-22.g.i

### Summary

Without reliable log files it can be difficult to impossible for a developer to detect unauthorized access to Platform Data. Audit logs allow an organization to record the fact that an event occurred, e.g. that a particular user executed a query against database tables containing Platform Data. These logs can then support processes like triggering automated alerts based on suspicious activity or forensic analysis after a security incident has been identified. The intent of this question is to determine if developers have implemented controls around admin and application event logging to flag and escalate potential security incidents.

### Changes from prior version

- This section is new as of questionnaire v3.

### Additional guidance

**Q3.1-22.a Requirements**

| Policy/Procedure Evidence | Implementation Evidence |
| --- | --- |
| Q3.1-22.a - Provide a written explanation (e.g., a policy or procedure document)that describes your approach to collecting admin audit logs. Your response should:   1. State admin logs are collected, AND 2. Describe what events are logged (unsuccessful login attempts, auditing / deleting of audit admin logs, and granting / revoking access admin privileges to accounts) | Q3.1-22.a.i - Provide screenshot evidence that shows how you collect admin audit logs. This evidence can come in the form of:   1. A tool dashboard showing admin audit logs are being collected along with the type of WHAT events are audited, OR 2. Directory listing of files that indicate they are admin logs with date stamps   Evidence provided must meet the following requirements:   - Screenshots and logs must be within 3 months from the date you received your Data Protection Assessment - Redacted logs are acceptable as long as the event type and date are displayed |

**Q3.1-22.b Requirements**

| Policy/Procedure Evidence | Implementation Evidence |
| --- | --- |
| Q3.1-22.b.ii - Provide a written explanation (e.g., a policy or procedure document) that describes your approach to collecting application event logs. Your response should:   1. State application event logs are collected, AND 2. Describe that you log the following attributes:  - Event type - Date and time - Success or failure indicator - Meta user ID (when shared with you) | Q3.1-22.b.iii - Provide screenshot evidence that shows how you collect application event logs. This evidence can come in the form of:   1. A tool dashboard showing application event logs are being collected along with the type of WHAT events are audited, OR 2. Directory listing of files that indicate they are application event logs with date stamps   Evidence provided must meet the following requirements:   - Screenshots and logs must be within 3 months from the date you received your Data Protection Assessment - Redacted logs are acceptable as long as the event type and date are displayed |

**Q3.1-22.e.i Requirements**

| Policy/Procedure Evidence | Implementation Evidence |
| --- | --- |
| Q3.1-22.e.ii - Provide a written explanation (e.g., a policy or procedure document) that describes your approach to reviewing application event logs. Your response should:   1. State application event logs are reviewed at least once every seven days, AND 2. Describe the use of an automated solution/ program to review logs, eg. a security information and event management tool (SIEM)   Please note that due to anticipatedly large amounts of data we expect to be captured in application event logs, we will not accept responses that indicate reviews conducted are solely manual. | Q3.1-22.e.iii - Provide screenshot evidence that shows how you review application event logs. This evidence can come in the form of:   - Command line tools - System event monitoring tools - Automated alerting tools - Automated notifications for auditable events greater than your SIEM’s configured threshold |

**Q3.1-22.f.i Requirements**

| Policy/Procedure Evidence (no screenshot evidence needed): |
| --- |
| Q3.1-22.f.ii - Provide a written explanation (e.g., a policy or procedure document) that describes your approach to reviewing admin logs. Your response should:   1. State admin audit logs are reviewed at least once every seven days   Please note that manual review of admin audit logs is acceptable. |

**Q3.1-22.g Requirements**

| Policy/Procedure Evidence (no screenshot evidence needed): |
| --- |
| Q3.1-22.g.i - Provide a written explanation (e.g., a policy or procedure document) that states how you investigate everyday security events or incidents in your backend environments where Platform Data is stored, which result in risk or damage to your audit logs. Your approach should describe:   1. Steps to determine valid or invalid (positive or false positive) security event 2. Escalation steps   *Reminder: If a security event or incident occurs, our [policies](https://developers.facebook.com/docs/graph-api/securing-requests%20/#require-proof) require you to promptly report it to us.* |

### External resources

Not familiar with audit logs? Review these resources:

- [Data Dog - Audit Logging Overview](https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.datadoghq.com%2Fknowledge-center%2Faudit-logging%2F&h=AUAc2zhyOHvH2ERpXRAHFYgjjOIQjREcKvyATprwpnapYql9WmefjlirCx1PIkmv_ld0Uq-m0l5HRmZg27B_AQP8m8wzexlYmbtw4KRm8G1iLVU41HLpEJz4Bs4HK-sXwr0qc4iSh46zWg)
  \*[CIS - Center for Internet Security (CIS): Audit Log Management Policy Template](https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.cisecurity.org%2Finsights%2Fwhite-papers%2Faudit-log-management-policy-template-for-cis-control-8&h=AUC-YkD9-iL-qgjyIR-_eRX9w19K_0Es0Oe-eltEeh9Ife7DBQDsVXk9t5bHWwZHnHV77BKqK0Fsw3F01FsPG1yNS2k2-mTuW2iPcOKCLf6bS0bennrqFS_pFralC0w6xAkYywIfx8PALZfV37K9cYlCSes)
- [Worldbank: Practitioner's Guide: Tamper-proof logs](https://l.facebook.com/l.php?u=https%3A%2F%2Fid4d.worldbank.org%2Fguide%2Ftamper-proof-logs&h=AUAs9CrIPFn49hFJfRc_LaohQT7Vfpqf_jWg1zYVDq1fye9QIoCmrY_jh6Z3HoAtlg2ERocrV7Vu_eJyvEdStkZtkc3pgAdB-2FeMvmJSCpW04I54AkiRbKiWDpFr4ij_Uf7KSxucBkDAg)
- [CSF Tools - NIST Controls: Audit and Accountability](https://l.facebook.com/l.php?u=https%3A%2F%2Fcsf.tools%2Freference%2Fnist-sp-800-53%2Fr5%2Fau%2F&h=AUAzi2mqLmwvPv7E6gm_uc_Za9dr2QFvXMV5QkFyrwTJ7o-6gHR9weUQ05vl9uDA0CrcRQQGS1C-2t58YrRGYGCTtmlAXqxdY9JJ-uGkjDTDNni_id0PF0_WwsWAvGTU6xmkJjxAj6FpAw)
- [AICPA - SOC 2 AICPA Trust Criteria, specifically CC7.2 and CC7.3](https://l.facebook.com/l.php?u=https%3A%2F%2Fus.aicpa.org%2Fcontent%2Fdam%2Faicpa%2Finterestareas%2Ffrc%2Fassuranceadvisoryservices%2Fdownloadabledocuments%2Ftrust-services-criteria-2020.pdf&h=AUBvuEwBZNtx5RLRSnyLED68zwVA-I4n3oerPNDTJRfBuk6-9tb00_Kuntli4hYAyExF1xb55xrZODfBm-rCBXc8QhabBwhRG5VN2dkAxAaicVH993Yw4pAaCUSZ_ujuwaQZUTIdOI7f3g)
- [OWASP - OWASP Logging Cheat Sheet](https://l.facebook.com/l.php?u=https%3A%2F%2Fcheatsheetseries.owasp.org%2Fcheatsheets%2FLogging_Cheat_Sheet.html&h=AUAmH_FYiX4mNJ5Cnpsuk058npPStlyAQk-YdVOmMa5kcARefUCVGbN10xKeV2oN8K9l1drKstCt5oDSVEIhBkFb3HvFUOmb0iaC_NhR10lSJMZA5_7l2puo383caAnbikGiz3eblAJFOw)

The following resources are not available free-of-charge, but offer valuable information and guidance:

- [ISO 27001:2013](https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.iso.org%2Fobp%2Fui%2F%23iso%3Astd%3Aiso-iec%3A27001%3Aed-2%3Av1%3Aen&h=AUDxeBqL9M4-WmFBDT436ZvYV22YQbR7dVOiD0Y-Es9ZBhbRyqBu7ZXGGEYCBU-v5qMxI_J5qL5OS_minFdVct2Z_pywFpX5rqZSWHZFWVBWBFV03hRczj6mTZaQuSkY98Z4fM77RNv0og)
- [Annex A.12.4 - Logging and Monitoring](https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.isms.online%2Fiso-27001%2Fannex-a-12-operations-security%2F%23what-is-annex-a-12-4&h=AUAnOgXSjiDFGfdGkl-iAJ4630gT93sdIg_B457YV9WynpxDR9mrZCaQUvF3TbwMLWlmhbAXEwxgCzxSToND6QOdV395pHNa-njI8QPzyQ9ll8WdSrmAu9epnm4jvE0u_yPdQBX2DPue3g)

### Evidence examples

[Q3.1-22 evidence examples](https://developers.facebook.com/docs/resp-plat-initiatives/data-protection-assessment/data-security/version3.1#3122)

## Q3.1-23 Questions - Security Processes for People that have access to Platform Data

### All questions

3.1-23

### Summary

Ensuring personnel are properly trained in the safe handling and protection of confidential data, including Platform Data, along with recognizing signs of potential compromise will reduce the likelihood a security incident.

### Changes from prior version

- This section is new as of questionnaire v3.

### Additional guidance

None

### External resources

Not familiar with personnel security? Review these resources:

- [CSF Tools - CSF Tools: Personnel Security](https://l.facebook.com/l.php?u=https%3A%2F%2Fcsf.tools%2Freference%2Fnist-sp-800-53%2Fr5%2Fps%2F&h=AUD8x1Fx9Vkfo_6ZI0w2YMFq9Nj1kPdY6k_C_hLwA0hMTYyX8lp2WOBwrxSmI10vHSJECrjktqlygjvR3zZcSxVCjYGL8fFkQIpMgyNhZOJjQ8w0eiZmGVm1jtHi4qiZ0WMwEEaN3HdqbbWeNBw1obj6mPA)
- [Information Security Program - Personnel Security Policy Best Practices](https://l.facebook.com/l.php?u=https%3A%2F%2Finformationsecurityprogram.com%2Fpersonnel-security-policy-best-practices%2F&h=AUAMpGXoFztB9GIRjf7n38oy5uvuJ1KVv7cm23PLKmJjz9C8QHhnOwf_H3eOixpPELcqBLdifhCipvgiuBdTSZqiIgXh4snkq1VPagE85WuWRo2KOatiUPZ04UrsE-Wd5IOoTxipCi_PdA)
- [IFSec Global - How a personnel security policy can combat the insider threat](https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.ifsecglobal.com%2Fsecurity%2Fpersonnel-security-policy-combat-insider-threat%2F&h=AUABoQucLUbzHP9pA0jzlWWeHAOLVTDJF8WyexMZhBT6dDTUmJ_6dG-BFUwKlS8K841wnvU0Xqx25iMkENqyIJKYceHkxeMD5V9KUQ3M5jPKOJOXCx8SeC3t025VEAtaYrPiLxqLo5EgDg)

### Evidence examples

Developers are not required to provide evidence in response to this question.

# Glossary

## A

**3rd party** - in risk management terminology, 3rd party refers to developers on Meta’s platform (1st party is Meta itself; 2nd party is people that use Meta’s products)

**4th party** - in risk management terminology, 4th party refers to the firms that developers rely on to provide them services that enable their business (1st party is Meta, 2nd party is Meta’s users, and 3rd party is developers on Meta’s platform)

**Access token** - a credential, like a password, that allows software to call an API to take some action (e.g., read data from a user’s profile).

**Admin Audit Logs** - records of actions taken by users with elevated privileges in data systems. Properly configured, admin audit logs record the actions that a system administrator takes within the system, for example executing programs or scripts, creating or disabling accounts, resetting passwords or changing multifactor authentication configurations and the editing, moving or deleting of log files within a system.

**Amazon Web Services (AWS)** - Amazon’s suite of cloud computing services

**App scoped ID (ASID**) - a unique identifier that Meta generates when a person chooses to use an app. ASIDs help improve privacy for users by making it more difficult for data sets to correlate users across apps, since a single user using two apps will have different ASIDs in each app.

**App secret** - a shared secret that Meta makes available to developers via the app dashboard. Possession of the app secret authorizes software to take some actions via the Graph API, so developers need to take care that unauthorized parties are not able to get access to the app secret.

**App compromise** - if a malicious actor is able to gain unauthorized access to an organization’s internal network via a misconfiguration or vulnerability in their app (e.g., a software vulnerability in a webapp) it’s called app compromise. A defense against app compromise is to pen test the app. See also network compromise.

**Application container** - a container packages up software code and related dependencies so that the app will run on different types of servers (e.g., servers running different operating systems like Linux or Windows Server). A developer will create a container image that packages their app. An application container engine or runtime hosts (runs) the container image.

**Application encryption** - a method of protecting data where the application software itself does the encryption and decryption operations. In contrast, Transport Layer Security (TLS) seamlessly encrypts data in transit when an application establishes a secure connection to a remote server (e.g., using HTTPS) and cloud providers offer services to transparently encrypt data at rest.

**Application event logs** - are structured records of events and activities generated by software applications. They capture a wide range of information, including error messages, user interactions, system events, and application-specific data.

**Application Programming Interface (API)** - allows two computers to talk to each other over a network, for example a mobile app fetching today’s weather for a certain location from a centralized weather forecasting system

**Appsecret proof** - an additional layer of security for API calls to Meta whereby a developer generates a parameter (the appsecret proof) that demonstrates that they possess the app secret. The appsecret proof is the product of a hashing function (also called a one-way function) based on the app secret and access token. Configuring an app to require appsecret proofs during Graph API invocations reduces the potential harm from a breach of user access tokens, since those access tokens cannot be used without the additional appsecret proof parameter.

## B

**Backend environment** - In system architecture, frontend refers to the part of the system that runs on user devices (e.g., a mobile app on an Android or iPhone or a web app on the user’s laptop), whereas backend refers to the part of the system that runs remote from end users on computers that are controlled by the developer or a hosting provider. Backend environments have network, compute, and storage resources and are hosted in a cloud or other type of server environment like a data center.

**Backend as a Service (BaaS)** - a style of cloud computing that provides a suite of server-side capabilities for an app developer so that the developer can focus on building the frontend (i.e., the part of an app that users interact with). BaaS solutions are similar to PaaS and, in addition, add services like user authentication and mobile push notifications. For example, these are some popular BaaS products: AWS Amplify, Azure Mobile Apps, Firebase, and MongoDB Switch.

## C

**Cipher text** - a synonym for encrypted data, cipher text is the name given to data that has been made unreadable via some encryption algorithm. The opposite of cipher text is plain text.

**Client side** - people typically interact with internet-accessible services by opening a website in a browser or by running a mobile app on a phone or tablet. The browser or mobile apps are referred to as local clients or client side. Clients make requests from remote computers (servers) via the internet.

**Cloud computing** - refers to a style of managing server computers, networks, and storage so that an organization doesn’t need to worry about the physical environment (i.e., a data center full of server racks and network cables). Instead, the organization can provision these assets on demand and pay for the services that they consume.

**Cloud configuration** - the set of cloud computing options that an organization has set in relation to their use of a cloud provider running some software. Examples of cloud configuration include what sorts of network connections are allowed or blocked, where log files are written and how long they are kept, and the set of users who are authorized to make changes to the cloud configuration.

**Compensating controls** - a security control that differs from some baseline set of requirements but is intended to deliver comparable protection against a risk.

## D

**Database** - software that allows arbitrary data to be stored, read, updated, and deleted. Databases can run on clients and on servers. Organizations that integrate with the Meta platform will commonly store data they fetch from the Graph API in a database that runs server side.

**Decryption** - process by which encrypted data is transformed back into its original format. In other words, decryption changes cipher text into plain text.

**Dynamic Application Security Testing (DAST)** - is a program used by developers to analyze a web application (web app), while in runtime, and identify any security vulnerabilities or weaknesses. Using DAST, a tester examines an application while it's working and attempts to attack it as a hacker would.

## E

**Encryption** - process by which data is transformed into a format that is unusable to anyone that cannot decrypt it. In other words, encryption changes plain text into cipher text.

**Encryption at rest** - data that has been protected with encryption when written to persistent storage (e.g., a disk drive). Encryption at rest provides an additional layer of protection against unauthorized access since an actor that’s able to read the raw files on the storage device will see cipher text and will not be able to decrypt it unless they are also able to gain access to the decryption key.

**Encryption in transit** - data that has been protected with encryption when transmitted across a network. Encryption in transmit provides protection against eavesdropping along the network path since an actor that’s able to read the network packets will see cipher text and will not be able to decrypt it unless they are also able to gain access to the decryption key.

**End of Life (EOL) software** - when an organization chooses to stop support (e.g., create patches to resolve security vulnerabilities) for a software product that software is considered EOL. Since this software is no longer maintained, it’s very risky to run any EOL software.

## G

**Google Cloud Platform (GCP)** - Google’s suite of cloud computing services

**Graph API** - the primary way for apps to read and write to the Meta social graph. All Meta SDKs and products interact with the Graph API in some way.

## H

**Hashing function** - a cryptographic function that takes any data as input and outputs a short code that cannot be reversed into the original input. In cryptography, hashing functions are used to protect data like passwords – instead of storing a user’s password in plaintext that could be stolen, passwords are first transformed with a hash function and then stored. Later, to confirm that a user has input the correct password, the system will use the same hash function to transform the input and compare the resulting hash against the stored value. Also called a one-way function since the output hash cannot be reversed into the original input.

**Hosted environment** - refers to a set of remote servers, networks, and storage devices that an organization is running in their own data center or within a data center co-located (or colo) with other customers. This arrangement is relatively uncommon in the modern era since cloud computing has become more popular.

## I

**Identity Provider (IdP)** - a cloud service used to centralize management of digital identities and authenticate users. Organizations that use an IdP typically configure cloud apps to rely on the IdP for user authentication. The organization can then manage users by creating, granting access to selected apps, and disabling user accounts centrally within the IdP instead of having to do this repeatedly in each cloud app.

**Identity and Access Management (IAM)** - refers to the category of tools and processes that are used to manage accounts and grant access to systems.

**Infrastructure as a Service (IaaS)** - a cloud computing approach that lets customers configure computing, storage, and networking services without having responsibility for the physical assets themselves (e.g., managing a data center full of servers, network devices, and storage arrays). Compared to Paas, IaaS gives an organization more control over the configuration of their cloud assets but at the cost of more complexity to manage those assets. For example, these are some popular IaaS products: AWS EC2, Microsoft Azure IaaS, and Google Compute Engine.

## L

**Library** - pre-existing software building blocks, typically from an external company or developer, that’s used to handle certain tasks within another developer’s app or system. Libraries simplify development of an app since a developer doesn’t have to reinvent the wheel when a library already exists for a given function. However, libraries can contain security vulnerabilities – or can themselves include additional libraries that do – so developers who use libraries as part of their app need to know what libraries are in use and keep them up to date over time.

## M

**Mobile client or mobile app** - an app that a person installs onto a phone or table from a mobile app store (e.g., iOS App Store or Google Play Store). It’s common for mobile clients to communicate over the internet with an organization’s REST API and may also communicate with other parties (e.g., to the Graph API via the Facebook SDK for Android).

**Multi-Factor Authentication (MFA)** - an authentication approach that requires more than one factor to gain access to an app or system. MFA, in contrast to single factor authentication that relies on just a password to authenticate a user, will typically require a password plus one or more of these: a code sent via email or SMS, a code from an authenticator app, a biometric scan, or a security key. MFA protects against account takeovers by making it more difficult for unauthorized actors to force their way into an account, e.g., by repeatedly attempting to login to an account by using a known email address and common passwords until successful.

## N

**Native software** - apps that are downloaded and installed onto laptops or mobile devices are referred to as native software (e.g., the Facebook app for iOS). In contrast, an app that runs within a browser is referred to as a webapp (e.g., opening Facebook using the Chrome browser).

**Network compromise** - if a malicious actor is able to gain unauthorized access to an organization’s internal network via a misconfiguration or vulnerability in the network itself it’s called a network compromise. A defense against network compromise is to run a network scan to identify misconfigurations and vulnerabilities in the internet-facing network. See also application compromise.

**Network scan** - a risk management process that uses software to: (1) identify active servers on a network that will respond to remote communications, and then (2) see if any of those servers are running old versions of software that is known to be vulnerable to one or more security exploits. An organization may use network scanning periodically to make sure that there are no unexpected open ports on their network perimeter, for example.

**Node Package Manager (NPM)** - a tool used by JavaScript developers to speed up development by allowing pre-built packages to be included in a developer’s app or system. NPM includes features to audit the set of packages that are in use by an app and to identify packages that have known security vulnerabilities.

## O

**Object storage buckets** - a type of persistent storage in the cloud that makes it simple for organizations to store files into persistent storage, including files that are very large, without having to worry about scaling physical assets like storage arrays or how to back these files up to ensure they aren’t lost in the case of a disaster like a fire or flood.

**Operating System** - the software running on a computer or mobile device that allows applications to run and use that computer’s processor, memory, storage, and network resources. For example, Microsoft’s Windows, Apple’s macOS or iOS, and Linux.

**Organization member** - someone with a role and responsibilities within an organization, for example an employee, a contractor, a contingent worker, an intern, or a volunteer.

**Organizational device** - a computer or mobile device used by an organization member in the context of doing work for the organization.

## P

**Package** - synonym for content library

**Patch** - software updates that resolve security vulnerabilities, fix bugs, or add new functionality. All sorts of software gets patched, including Operating Systems, containers, libraries, and SDKs.

**Penetration test** - a simulated attack against an app or system where the tester attempts to find vulnerabilities in the code or configuration that could be exploited by an unauthorized actor. Pen testers will use similar tools to cyber criminals to conduct reconnaissance, scan for potential weaknesses, and test vulnerabilities that could be used to gain unauthorized access. At the conclusion of a pen test, the tester will create a report that describes the findings along with the severity of each and the organization that maintains the software is responsible for crafting fixes to resolve the vulnerabilities.

**Plain text** - a synonym for unencrypted data, plain text is the name given to data that has not been protected by encryption.

**Platform as a Service (PaaS)** - a cloud computing approach whereby a customer deploys an application into a platform managed by the cloud provider. Compared to IaaS, PaaS is simpler for customers to manage since not only the physical assets (i.e., the servers, storage devices, and network devices) are managed by the cloud host but also the operating system and application container where the customer’s app runs. For example, these are some popular PaaS products: AWS Elastic Beanstalk, Google App Engine, Force.com.

**Platform Data** - see the definition in [Meta’s Platform Terms](https://developers.facebook.com/terms/dfc_platform_terms/#glossary).

**Platform Term 6.a.i** - Refers to Meta’s Platform Terms section (6) heading (a) paragraph (i), which describes platform developers’ obligations related to data security.

**Port** - when a client makes a connection to a server over the internet the destination address has two parts: (1) an Internet Protocol (IP) address for the server and (2) a port number on that server that a particular application will respond to. Common protocols use reserved ports (e.g., HTTPS uses 443) but a developer can use custom ports for network communications if desired.

## R

**REST API** - a widely adopted style of building web-accessible services where the client and server communicate using the HTTP protocol. A developer on the Meta platform might host a REST API on a subdomain like api.example.com that their mobile app sends and receives Platform Data to/from.

## S

**Secure Shell (SSH)** - a communication scheme that allows administrators to remotely login to servers and run programs on those servers. Referred to as secure since the communications between the client and server are protected against eavesdropping unlike earlier protocols like Telnet. Also called Secure Socket Shell.

**Secure Sockets Layer (SSL)** - An obsolete and insecure version of encryption in transit. The modern secure version is called Transport Layer Security (TLS).

**Security information and event management (SIEM)** - technology supports threat detection, compliance and security incident management through the collection and analysis (both near real time and historical) of security events, as well as a wide variety of other event and contextual data sources.

**Server** - a computer that provides services remotely over a network. Browsers and mobile apps connect to servers over the internet.

**Serverless computing** - a style of cloud computing where the cloud host manages the physical infrastructure, the server operating system, and the container. A developer is only responsible for custom code and associated libraries along with the cloud configuration.

**Server side** - data or computation on the other side of a network connection (i.e., on a server) is referred to as server side. In contrast, data or computation on a local device like a laptop or mobile device is referred to as client side.

**Single Sign On (SSO)** - an arrangement where apps rely on a centralized user directory (i.e., an IdP) to authenticate users. In addition to centralizing user account and app access administration for the organization, users benefit by having a single set of credentials instead of requiring users to maintain different credentials (e.g., username and password) for each different app.

**Software Development Kit (SDK)** - a building block of code that a developer can use to simplify the development process for a given need. For example, Meta creates and maintains SDKs that simplify working with the Graph API for iOS and Android developers. Similar to a library, developers that use SDKs in their apps need to keep them up to date over time.

**Software as a Service (SaaS)** - allows customers to use cloud-based apps via the internet. Unlike PaaS or IaaS, a customer of a SaaS app does not deploy custom code nor have responsibility for configuring, upgrading, or patching the SaaS app as all of these are the responsibility of the SaaS software vendor. For example, these are some popular SaaS products: Dropbox, MailChip, Salesforce, Slack.

**Static analysis** - see Static Application Security Testing

**Static Application Security Testing (SAST)** - an approach for finding vulnerabilities in software by running a specialized tool against the source code. A SAST tool will identify potential vulnerabilities, such as those listed in the OWASP Top 10 project, and then the developer is responsible for reviewing the findings, distinguishing true positives from false positives, and fixing vulnerabilities in the software. SAST can be useful because it can allow developers to find vulnerabilities before they are deployed into production, but unlike a penetration test a SAST tool will not be able to find vulnerabilities related to the production configuration of the app.

**System Administrator Audit Logs** - See Admin Audit Logs.

## T

**Transparent data encryption** - a type of encryption at rest that typically applies to database storage (i.e., the database contents themselves and its log files). In this arrangement, the database software manages the encryption keys and transparently handles the encryption operations (upon writes) and decryption operations (upon reads).

**Transport Layer Security (TLS)** - an encryption in transit scheme that uses encryption to protect data transmitted over networks from eavesdroppers along the network path. TLS is the modern secure version of the obsolete earlier technology called SSL.

**Two-Factor Authentication (2Fac)** - a synonym for Multi-Factor Authentication.

## V

**Vault** - a secret management system for sensitive data like encryption keys, access tokens, and other credentials. A vault allows tight control over who is able to access the secrets it contains and offers additional services like keeping audit logs.

**Virtual Machine (VM)** - very similar to an Application Container – a VM runs in a host called a hypervisor whereas an Application Container runs in a container engine. The main difference is that a VM image contains an Operating System whereas an Application Container will not. Both VMs and Application Containers contain application(s) and dependencies like libraries.

**Virtual Private Cloud (VPC)** - term used by AWS to refer to a set of cloud resources that resembles a traditional network in a data center in the pre-cloud era.

**Vulnerability** - a flaw in a system or app that could be exploited, e.g., to read data that the actor otherwise would not be entitled to read

**Vulnerability Disclosure Program (VDP)** - an approach whereby organizations solicit security vulnerability reports from researchers (sometimes called ethical hackers) so that the vulnerabilities can be discovered and fixed before malicious actors exploit them. An effective VDP requires a set of researchers who
are actively looking for vulnerabilities, analysts within the organization to review and triage incoming disclosures, and engineers who are knowledgeable about cybersecurity that are able to create and deploy fixes for vulnerabilities.

**Vulnerability scan** - an approach that uses software to look for vulnerabilities in servers, networks, and apps. Compared to a penetration test, a vulnerability scan is cheaper to run and hence can be run repeatedly (e.g., monthly or quarterly) but it’s typical that a pen test will find vulnerabilities that a vulnerability scan misses because skilled penetration testers bring analytical skills and instincts that are hard to replicate with strictly automated approaches. See also network scan.

## W

**Webapp** - Webapps are programs that run inside browsers and are comprised of resources like HTML documents, JavaScript code, videos and other media, and CSS for styling. In contrast to a mobile app that a person installs onto a mobile phone from an app store, people simply fetch a webapp from a remote server using their browser (e.g., www.facebook.com) without the need for an installation step.
