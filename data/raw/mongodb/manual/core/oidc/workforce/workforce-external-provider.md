> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

<!--
Tab options on this page. Append to the .md URL to filter:
  ?tabs=<id,...>   select specific tabs (e.g. ?tabs=nodejs,shell)
  ?allTabs=true    include every tab
  (no param)       default: one tab per tabset

Available tabs:
  other tabs: azure, okta, generic
-->

# Configure OIDC for Workforce Authentication

To configure Workforce Identity Federation with OIDC (OpenID Connect), register your OIDC application with an external IdP (Identity Provider), such as Okta or Microsoft Entra ID. This ensures secure authentication and facilitates user management.

## About this Task

Workforce Identity Federation uses OIDC. You can use any external IdP that supports the OIDC standard.

You can configure your OIDC application for the following grant types:

- Authorization Code Flow with PKCE (Proof Key of Code Exchange)

- Device Authorization Flow

MongoDB recommends that you use Authorization Code Flow with PKCE for increased security. Use Device Authorization Flow only if your users need to access the database from machines with no browser.

**Note:**

Workforce Identity Federation supports only JWT (JSON Web Token) for authentication. It doesn't support opaque access tokens.

The following procedures provide detailed configuration instructions for Microsoft Entra ID and Okta, and generic configuration instructions for other external IdPs.

## Before you Begin

- To use Okta as an IdP, you must have an [Okta account.](https://www.okta.com/)

- To use Microsoft Entra ID as an IdP, you must have a [Microsoft Azure account.](https://azure.microsoft.com/en-us/get-started/azure-portal)

## Steps

### Microsoft Entra ID

1. Register an application

   1. Navigate to App registrations.

      1. In your [Azure portal](https://portal.azure.com/) account, search and click Microsoft Entra ID.

      2. In the Manage section of the left navigation, click App registrations.

   2. Click New registration.

   3. Apply the following values.

      | Field | Value |
      | --- | --- |
      | Name | MongoDB - Workforce |
      | Supported Account Types | Accounts in this organizational directory only (single tenant) |
      | Redirect URI | - Public client/native (mobile & desktop)- To access clusters using [MongoDB Compass](https://www.mongodb.com/docs/compass/current/) and [MongoDB Shell](https://www.mongodb.com/docs/mongodb-shell/), set the Redirect URI to `http://localhost:27097/redirect`. |

   4. Click Register.

   To learn more about registering an application, see [Azure Documentation.](https://learn.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app#register-an-application)

2. Add a group claim

   1. Navigate to Token Configuration.

      In the Manage section of the left navigation, click Token Configuration.

   2. Click Add groups claim.

   3. In the Edit groups claim modal, select Security.

      What groups you select depend on the type of groups you configured in your Azure environment. You may need to select a different type of group to send the appropriate group information.

   4. In the Customize token properties by type section, only select Group ID.

   5. Click Add.

   To learn more about adding a group claim, see [Azure Documentation.](https://docs.microsoft.com/en-us/azure/active-directory/hybrid/connect/how-to-connect-fed-group-claims)

3. Add a user identifier claim to the access token

   1. Click Add optional claim.

   2. In the Add optional claim modal, select Access.

   3. Select a claim that carries a user identifier that you can refer to in MongoDB access logs such as an email.

      You can use the UPN (UserPrincipalName) claim to identify users with their email address.

   4. Click Add.

   5. In the Microsoft Graph Permissions note, check the box, and click Add.

   To learn more, see [Azure Documentation.](https://docs.microsoft.com/en-us/azure/active-directory/develop/optional-claims)

4. Update the manifest

   1. In the Manage section of the left navigation, click Manifest.

   2. Update the requestedAccessTokenVersion from `null` to `2`.

      The number `2` represents Version 2 of Microsoft's access tokens. Other applications can use this as a signed attestation of the Active Directory-managed user's identity. Version 2 ensures that the token is a JSON Web Token that MongoDB understands.

   3. Click Save.

   To learn more about adding an optional claim, see [Azure Documentation.](https://docs.microsoft.com/en-us/azure/active-directory/develop/reference-app-manifest)

5. Remember metadata

   1. In the left navigation, click Overview.

      Copy the Application (client) ID value.

   2. In the top navigation, click Endpoints.

      Copy the OpenID Connect metadata document value without the `/.well-known/openid-configuration` part.

      You can also get this value by copying the value for `issuer` in the OpenID Connect metadata document URL.

   The following table shows what these Microsoft Entra ID UI values map to in the MongoDB [`oidcIdentityProviders`](/docs/manual/reference/parameters#mongodb-parameter-param.oidcIdentityProviders) parameter:

   | Microsoft Entra ID UI | MongoDB `oidcIdentityProviders` Parameter Field |
   | --- | --- |
   | Application (client) ID | `clientID``audience` |
   | OpenID Connect metadata document (without /.well-known/openid-configuration) | `issuer` |

## Next Steps

- [Configure MongoDB with Workforce Identity Federation](/docs/manual/core/oidc/workforce/configure-oidc#std-label-configure-oidc)

- [Authorize Users with Workforce Identity Federation](/docs/manual/core/oidc/workforce/database-user-workforce#std-label-database-user-workforce)

## Learn More

- [Okta account](https://www.okta.com/)

- [Microsoft Azure](https://azure.microsoft.com/en-us/get-started/azure-portal)
