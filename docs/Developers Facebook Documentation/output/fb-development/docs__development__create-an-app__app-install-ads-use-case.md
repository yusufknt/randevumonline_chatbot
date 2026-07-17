# App Ads Use Case - App Development with Meta

_Source: https://developers.facebook.com/docs/development/create-an-app/app-install-ads-use-case_

---

# Customize the Create and Manage app ads with Meta Ads Manager Use Case

This guide shows you how to customize the **Create and manage app ads with Ads Manager** use case you added to your app during the [app creation process](https://developers.facebook.com/docs/development/create-an-app/).

## Customization steps

In the [dashboard](https://developers.facebook.com/apps/), go to click **Use Cases** in the left-side menu then click the **Customize** button for **Create & Manage app ads with Meta Ads Manager**. The dashboard will refresh to the **Customize use case** page.

#### Step 1. Connect your business portfolio and ad accounts

1. If you haven't already added a business portfolio to your app, or would like to change the business portfolio connect to your app, click **+ Business Portfolio** to add, update, or create one.
2. A pop-up window will appear showing a dropdown of business portfolios that you have full control and that can be connected to your app.

   - Both verified and unverified business portfolios are listed. You can add an unverified business portfolio however it must be verified before you can run ads.
   - If you don't have a Meta business portfolio or want to create a new one, click **Create new account**.
3. Add at least one ad account ID or click **Go to Business Settings** to create an ad account.

   - The ad accounts you add must be connected to the selected business portfolio, and you must have full control of the business portfolio and admin access to the ad accounts.

#### Step 2. Add platforms and app stores

1. Click **+ Platform** to tell us about the platforms and app stores that host your app.
2. For each platform you select, fill out the needed information.

#### Step 3. Set up App Events

1. Click **Set up App Events** or **App Events > Settings** in the left side menu to configure the events you want to track.
2. **Collect the Apple Advertising Identifier (IDFA) with App Events** and **Log in-app events automatically (recommended)** for Android and iOS are set to **Yes** by default.
3. You can add your iTunes Connect code to the **In-App Purchase Shared Secret** if your iOS app offers auto-renewable subscription purchases.
4. You can also log events for the Facebook SDK and set the **Session Timeout Interval**.
5. Click **Save changes**. You should be redirected to the **Quickstart**.

#### Quickstart

1. If you haven't already been redirected to the Quickstart, click **App Events > Quickstart** menu.
2. Select each platform (iOS, Android, Web) you will be tracking events for.
3. Complete the list of action items for each platform to set up events.
4. Go to the Events Manager to continue the setup and test your events. A new browser will open with the Events Manager **Data Sources Settings** tab for your app and platform.
5. Click **Check app eligibility** to ensure any events chosen use the same integration method as App Installs. Resolve any eligibility issues to continue.
6. Return to the App Dashboard to continue configuring your app.

You can also click the **Testing**, tools icon, in the left side menu to **Go to Events Manager** and **Test events** to test your setup later. Learn more about [the Events Manager test events tool](https://www.facebook.com/business/help/2040882565969969).

## Publish your app

Once you have completed development, and successfully completed App Review (if necessary), you can publish your app.

**Apps that require publishing** – If your app will access content you don't own or manage, or you have implemented a product, such as webhooks, that requires your app to be published, it will need to be published.

1. Click **Publish** in the left side menu. If any app settings are needed, you'll be directed to update them.
2. You can review your app's use cases and App Review approvals.
3. Click the **Publish** button in the lower-right.

**Note:** Some functionality, such as webhooks, require your app to be published.

## Create an ad campaign

With your use case set up complete, you’re ready to create your first app promotion ad campaign. In the **What’s next?** section, click **Go to Ads Manager** to create an ad campaign for your app.

Learn more about
[the Ads Manager.](https://www.facebook.com/business/tools/ads-manager)

## Update the use case

If, at any point, you want to change your app’s use case settings, you can return to your dashboard, click **Use cases**, the pencil icon, in the left side menu and select the use case from the dropdown menu.

## Helpful articles

Visit the following to learn more about the app development process:

- [App Development](https://developers.facebook.com/docs/development)
- [App Events API](https://developers.facebook.com/docs/app-events)
- [App Ads Developer Documentation](https://developers.facebook.com/docs/app-ads)
- [App Review](https://developers.facebook.com/docs/resp-plat-initiatives/app-review)
- [Business verification](https://developers.facebook.com/docs/development/release/business-verification)

#### Setting up ads

- [About the new Advantage+ campaign setup](https://www.facebook.com/business/help/1292656978738967)
- [Optimize your app ads](https://www.facebook.com/business/help/609993965848500)

#### Measuring your campaign performance

- [Measure the results of your app ads](https://www.facebook.com/business/help/305102563866933)
- [Measurement partner directory](https://www.facebook.com/business/partner-directory/search?solution_type=measurement)
- [Measuring installs and in-app conversions](https://developers.facebook.com/docs/app-ads/measuring/installs-and-in-app-conversions/)
