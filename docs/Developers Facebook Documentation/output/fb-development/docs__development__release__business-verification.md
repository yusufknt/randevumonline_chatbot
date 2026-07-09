# Business Verification - App Development with Meta

_Source: https://developers.facebook.com/docs/development/release/business-verification_

---

# Business Verification

**[Advanced Access](https://developers.facebook.com/docs/graph-api/overview/access-levels/#advanced-access) now requires Business Verification.**

As of February 1, 2023, if your app requires advanced level access to permissions, you might need to complete [Business Verification](https://developers.facebook.com/docs/development/release/business-verification). [See this blog post for more information.](https://developers.facebook.com/blog/post/2023/02/01/developer-platform-requiring-business-verification-for-advanced-access/)

Business Verification is a process that allows us to gather information about you and your Business so we can verify your identity as a business entity.

Apps that request [advanced access](https://developers.facebook.com/docs/graph-api/overview/access-levels/#advanced-access) for permissions and apps that allow other [Businesses](https://business.facebook.com/) to access their own data must be connected to a Business that has completed Business Verification. Until then, app users from other Businesses will be unable to grant these apps [permissions](https://developers.facebook.com/docs/permissions/reference) and all [features](https://developers.facebook.com/docs/apps/features-reference) will be inactive.

If your app will only be used by app users who have a [role](https://developers.facebook.com/docs/development/build-and-test/app-roles) on the app itself you do not need to complete verification; these users can grant your app any permissions at any time and all features are always active.

You can use the App Dashboard to connect your app to a Business that you're an Admin of, regardless of whether or not the Business has been verified, but the verification process itself must be completed in the Facebook Business Manager. If you do not have a Business, you will be given the option to create one.

Note that anyone with an Administrator role on your app can connect it to a Business, but only someone with an Admin role in the Business will be able to complete the verification process.

## Step 1: Connect your app to a Business

Load your app in the App Dashboard and go to **Settings** > **Basic** > **Verification** and click the Start Verification button or the **+ Business Verification** link if you have previously completed Individual Verification.

![Verification section in the Basic Settings panel.](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/143865101_957211231353134_6810255425904105080_n.png?_nc_cat=102&ccb=1-7&_nc_sid=e280be&_nc_ohc=zTOsHmH93-YQ7kNvwFldOuM&_nc_oc=Adp5PovjQTfp7F3dyQ9uqAp9-MIoaFL89qIh6nCuEfBITT6uolagVZ6y7kRIgRVI9Ew&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=c_KaESpZbL8byXXUCWoeLw&_nc_ss=7b289&oh=00_Af5pC0m4MX1x4OnNixZ6ZzMzQf0j5wilv-csyor0xVBxWw&oe=6A1BF627)

If your Facebook developer account is already associated with a Facebook Business account, you will be given the option to select a Business within it:

![Business selection modal with a verified Business selected.](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/144081810_241994877493212_2655917975499900173_n.png?_nc_cat=102&ccb=1-7&_nc_sid=e280be&_nc_ohc=ZqV2cGTnmg8Q7kNvwEAanc1&_nc_oc=Adp6Z_jTjsj0BONx1xwbRkxl5BN-pg86oG-9rM_fvyTsR_9j9hsjFahSgG_NBfZbvSw&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=c_KaESpZbL8byXXUCWoeLw&_nc_ss=7b289&oh=00_Af7f3iQEoCxd_qJYswpsx-O9oDvtkLf5D7E3PLbja60LTw&oe=6A1BD9AE)

If you don't have a Facebook Business account, or if your account contains no Businesses, you will be prompted to create one.

Connecting your app to a verified Business completes the connection process and there's nothing else you have to do. The **Verification** section should show that your app is now connected to a verified Business:

![Verification section showing 'Verified' alongside the name of the Business that has been connected to the app.](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/142987006_267806678357731_3713867277959890685_n.png?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=X8yLpVsDBEUQ7kNvwFSilkx&_nc_oc=Adq59YhYF6yP0SO1YyPhM6WuSvCilfIKVFEwGJ9EkChYcOuIxgyuiegfeQ54barZ5l8&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=c_KaESpZbL8byXXUCWoeLw&_nc_ss=7b289&oh=00_Af4HsoX4Q6rEzICZOPN1ISJbksjHbhydo2ZL_dHFZ22zsA&oe=6A1BCA71)

If, however, you connected your app to an unverified Business, you must complete the verification process in the Business Manager.

## Step 2: Verify your Business

If you connected your app to an unverified Business, you or Admin of the Business must complete the verification process within the Business Manager.

![Business selection modal with an unverified Business selected.](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/143769130_241837180871082_6770952626487554480_n.png?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=fZm4hwjoXBkQ7kNvwG5rJwO&_nc_oc=AdreuqxVcT8VtLq--Aow25SqQoEDolTadLN_bQVJf3pK5UWcM05J48Qw7vdWcsGPBsM&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=c_KaESpZbL8byXXUCWoeLw&_nc_ss=7b289&oh=00_Af5d7a-7CC8w7yaJxzYRQc_cc-xeb_FiWQDuPYE7PAb0Zg&oe=6A1BF645)

Click Start Business Verification to load the unverified Business in the Business Manager and complete the verification process.

Refer to our Business Manager Help Center's [About Business Verification](https://www.facebook.com/business/help/1095661473946872) topic for an explanation of the process and a list of documents you will need.

Once you have completed verification, return to the Basic Settings panel. You should see that your app is now connected to a verified Business:

![Verification section showing 'Verified' alongside the name of the Business that has been connected to the app.](https://scontent.fyei5-1.fna.fbcdn.net/v/t39.2365-6/144376827_121772393150711_6581279437038461255_n.png?_nc_cat=110&ccb=1-7&_nc_sid=e280be&_nc_ohc=HC3PoB1DeNgQ7kNvwGm7l0x&_nc_oc=Adq78IFRRlCJAI2Z8ua47MWxdKmOAHJG-kp4KBYk-Wzm05w0NdDoin431cPcf2ZSaJg&_nc_zt=14&_nc_ht=scontent.fyei5-1.fna&_nc_gid=c_KaESpZbL8byXXUCWoeLw&_nc_ss=7b289&oh=00_Af4qlZHlsvGtTq-MOfeQzHVW8jHqcsomAJq9szbD5tYdOg&oe=6A1BEEB8)
