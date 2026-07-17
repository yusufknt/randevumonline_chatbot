# App Roles - App Development with Meta

_Source: https://developers.facebook.com/docs/development/build-and-test/app-roles_

---

# App Roles

App Roles allow you to control access to your app while it is in development. Each role confers a different level of access to your app. We recommend that you only give as much access to a person as they need. This provides greater security for your app and limits potential harm if a person's account is compromised.

You can send role invitations to other Meta developers and users by using the **Roles** section of the Meta App Dashboard. If your app is connected to a business portfolio, you must use the Business Manager to manage roles for your app. [Learn more.](https://www.facebook.com/business/help/business/help/299504287548592)

## Requirements

In order to have an Administrator, Developer or Analytics role on an app, a person must have a Meta Developer Account.

### Limitations

- Apps can have up to 500 administrators.
- An app that is linked to a Business Manager with Business Verification can have up to a combined total of 500 analytics users and testers.
  - Most apps, not linked, can have up to 50 testers.

## Assign a role

You can send invitations for Administrator, Developer, or Analytics roles for your app to other registered Meta developers, and Tester role invitations to both registered Meta developers and regular users by using the Roles panel.

### Administrator

Administrators have complete access to an app. They can grant the app any permission while it is in development, and all features are active for Admins while it is in development. They can change all app settings, reset the app secret, remove the app, and view Credits and Insights. Administrators can also assign and remove roles to people and change the permissions of others. Administrators of apps should only add other people as administrators if they are fully trusted and must have full control of the app.

### Developer

Developers can grant the app any permission while it is in development and all features are active for Developers while it is in development. They have access to the app and all its technical settings that are needed to run, edit, and test the app. Developers can modify all technical settings through the App Dashboard. They can also see insights for the app.

### Tester

Testers can grant the app any permission while it is in development, and all features are active for Testers while it is in development. They cannot edit any app settings, give other people access to the app or access insights for the app. You may only add a person as a Tester to your app if they are your employee or you have an agreement with them which establishes that they are acting on your behalf as a tester of your app. For example, a Tester should be a part of your quality assurance team and be responsible for testing your app for bugs, errors or other issues that could have a negative influence on its general performance. If a person is no longer testing your app, you should remove them from this role.

### Consumer tester

A consumer tester is a Facebook user who doesn't have a role on your app but who you invite to test your app. Wwhile it is in development, the consumer tester can log in to your app with their Facebook credentials and grant your app permissions, and all features are active for consumer tester.

### Instructions for consumer testers

Once you send an invitation, the consumer tester can accept or decline an invitation and manage their role from their Facebook account [within **Settings & privacy > Your activity > Apps and Websites**](https://www.facebook.com/settings/?tab=applications) section.

1. Log in to your Facebook account and navigate to **Facebook Settings**.
2. Scroll down to the [**Apps and Websites**](https://www.facebook.com/settings/?tab=applications) section.
3. Scroll down to the **Requests** section to find the consumer tester invitation.
4. Review the consumer tester invitations that you have received.
5. Click **Accept** to become a consumer tester for an app or **Decline** to reject an invitation.
6. Click **Resign** to remove yourself as a consumer tester for an app you no longer need to test.

### Analytics user

Analytics Users can only access analytics for your app. They cannot edit any app settings, give other people access to the app or access insights for the app. do not have access to edit any of the app's settings.

## Role task reference

| Ability | Administrator | Developer | Tester | Analytics User |
| --- | --- | --- | --- | --- |
| Modify app settings | ✔ | ✔ |  |  |
| Reset app secret | ✔ |  |  |  |
| Remove app | ✔ |  |  |  |
| Modify app roles | ✔ |  |  |  |
| Test login permissions, features, and products | ✔ | ✔ | ✔ | ✔ |
| Create test apps, users, and pages | ✔ | ✔ |  |  |
| View app insights | ✔ | ✔ |  | ✔ |

## App Limitations

Developer and Administrator roles are subject to limits on the apps they manage.

## Learn more

- [Apps in development using Meta Technologies](https://developers.facebook.com/docs/development/build-and-test/app-modes#development-mode)
- [Additional App Limitations for developer and administator roles](https://developers.facebook.com/docs/development/create-an-app/#before-you-start)
- [Register as a Meta Developer](https://developers.facebook.com/docs/development/register)
