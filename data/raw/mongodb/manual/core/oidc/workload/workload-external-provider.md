> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

<!--
Tab options on this page. Append to the .md URL to filter:
  ?tabs=<id,...>   select specific tabs (e.g. ?tabs=nodejs,shell)
  ?allTabs=true    include every tab
  (no param)       default: one tab per tabset

Available tabs:
  other tabs: azure-oauth, gcp-oauth
-->

# Configure Workload Identity Federation

To configure Workload Identity Federation using OAuth 2.0, register your OAuth 2.0 application with an external IdP like Microsoft Azure or Google Cloud Platform (GCP). This enables secure authentication and streamlines user management.

## About this Task

Workload Identity Federation uses OAuth2.0 access tokens. These tokens can be issued by any external IdP.

The following procedures configure Microsoft Azure Entra ID and Google Cloud Platform as external IdPs for MongoDB.

## Before you Begin

- To use Microsoft Azure as an IdP, you must have a [Microsoft Azure account.](https://azure.microsoft.com/en-us/get-started/azure-portal)

- To use Google Cloud as an IdP, you must have a [Google Cloud account.](https://cloud.google.com)

## Steps

### Azure

In order to access self-managed MongoDB instances with Azure Managed Identities or Azure Service Principals, you need to register an Azure Entra ID application. If you have an existing application registration for [Workforce](/docs/manual/core/oidc/workforce/workforce-external-provider#std-label-workforce-external-provider) (human user) access, we recommended that you register a separate application for Workload access.

1. Register an application

   1. Navigate to App registrations.

      In your [Azure portal](https://portal.azure.com/) account, search and click Microsoft Entra ID.

      In the Manage section of the left navigation, click App registrations.

   2. Click New registration.

   3. Apply the following values.

      | Field | Value |
      | --- | --- |
      | Name | MongoDB - Workload |
      | Supported Account Types | Accounts in this organizational directory only (single tenant) |
      | Redirect URI | Web |

2. (Optional) Add groups claim

   For application access, it is a best practice to use service principal identifiers as MongoDB user identifiers while defining access rights in self-managed MongoDB deployments. If you plan to use this common approach, skip this step. However, if you prefer to use group identifiers such as Azure AD Security Group identifier instead, you can set groups claim in your application registration with below steps.

   1. Navigate to Token Configuration.

      In the Manage section of the left navigation, click Token Configuration.

   2. Click Add groups claim.

   3. In the Edit groups claim modal, select Security.

      What groups you select depend on the type of groups you configured in your Azure environment. You may need to select a different type of group to send the appropriate group information.

   4. In the Customize token properties by type section, ensure that you only select Group ID.

      When you select Group ID, Azure sends the security group's Object ID.

   5. Click Add.

      To learn more about adding a group claim, see [Azure Documentation.](https://learn.microsoft.com/en-us/azure/active-directory/hybrid/connect/how-to-connect-fed-group-claims)

3. Enable an Application ID URI

   1. Navigate to Expose an API in the left sidebar and enable Application ID URI.

   2. Enable an Application ID URI.

      Keep the default Application ID URI assigned by Azure, which is `<application_client_id>`. Copy and store this value, as self-managed MongoDB deployments and all MongoDB drivers require this value for Workload Identity Federation configuration.

4. Update the manifest

   1. In the Manage section of the left navigation, click Manifest.

   2. Update the requestedAccessTokenVersion from `null` to `2`.

      The number `2` represents Version 2 of Microsoft's access tokens. Other applications can use this as proof of the Active Directory-managed user's identity. Version 2 ensures that the token is a JSON Web Token that MongoDB understands.

   3. Click Save.

   To learn more about adding an optional claim, see [Azure Documentation.](https://learn.microsoft.com/en-us/azure/active-directory/develop/reference-app-manifest)

5. Remember metadata

   1. In the left navigation, click Overview.

   2. In the top navigation, click Endpoints.

      Copy the OpenID Connect metadata document value, excluding `/.well-known/openid-configuration`.

      You can also retrieve this value by following the OpenID Connect metadata document URL and copying the value for `issuer`.

   The following table shows what these Microsoft Entra ID UI values map to in the MongoDB [`oidcIdentityProviders`](/docs/manual/reference/parameters#mongodb-parameter-param.oidcIdentityProviders) parameter:

   | Microsoft Entra ID UI | MongoDB `oidcIdentityProviders` Parameter Field |
   | --- | --- |
   | OpenID Connect metadata document (without /.well-known/openid-configuration) | `issuer` |
   | Application ID URI | `audience` |
