# Developer Data Security Best Practices - App Development with Meta

_Source: https://developers.facebook.com/docs/development/data-security_

---

# Developer Data Security Best Practices

If you use Platform as a developer, you are responsible for securing Platform Data in a way that meets or exceeds industry standards given the data’s sensitivity. Below are some key principles and industry best practices that developers may find helpful when deciding on security measures for Platform Data. These best practices are provided as guidance only and cannot guarantee you have met your obligations under Meta’s Platform Terms, as they do not (and cannot) cover every conceivable scenario. Whether you have met or exceeded industry standards will depend on the sensitivity of the Platform Data you access and/or process and your unique technical circumstances.

| Principle | Best Practices |
| --- | --- |
| Secure Communication (data in transit) | - Use trusted certificate authorities (CAs) - Ensure certificates are configured properly - Use the most updated versions of Transport Layer Security (TLS) possible - Enforce encryption for all network connections - Test to verify network connections are not accidentally sending data in the clear - Verify that metadata in HTTP headers doesn’t include personal information |
| Secure Data at Rest | - Use standard encryption; don’t roll your own or rely on data encoding or obfuscation - Enable any platform level controls where available - Verify that the data is encrypted - Protect all systems against malware |
| Manage Keys and Passwords | - Don’t keep passwords in the clear or embed them in code - Don’t use vendor-supplied defaults for system passwords - Use key management systems when available - Have a system for maintaining keys (assigning, revoking, rotating, deleting) - Utilize two-factor authentication when available - Provide two-factor as an option to users |
| Employ Access Controls and Account Management | - Separate roles and functions with different accounts and credentials - Have a system for maintaining accounts (assigning, revoking, reviewing access and privileges, removing) |
| Apply Updates and Patches | - Have a system for keeping system code and environments updated, including servers, virtual machines (VMs), distributions, libraries, packages, and anti-virus software/programs - Have a system for maintaining and patching production facing systems including   - Core libraries   - Web services   - Outward facing services |
| Monitor and Log | - Have a system in place for logging access to user data, tracing where user data was sent and stored - Monitor transfers of user data and key points where user data can leave the system (e.g., third parties, public endpoints) |
| Application Security and Securing APIs | - Be familiar with basic app security practices including   - Assessing permissions and data needs (aligning data access to purpose of use)   - Testing APIs and endpoints for data leakage   - Testing transmissions to and from third parties for data leakage   - Scanning app and code for common security flaws before deployment - Be familiar with basic coding practices to address fundamental security concerns - Regularly test security systems and processes |
