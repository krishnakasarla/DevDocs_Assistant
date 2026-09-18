> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

<!--
Tab options on this page. Append to the .md URL to filter:
  ?tabs=<id,...>   select specific tabs (e.g. ?tabs=nodejs,shell)
  ?allTabs=true    include every tab
  (no param)       default: one tab per tabset

Available tabs:
  other tabs: add-idp-groups, add-user-id
-->

# Authorize Users with Workforce Identity Federation

You can add a database user to MongoDB using Workforce authentication. This process allows your organization’s IdP (Identity Provider) to manage user access, ensuring secure and centralized authentication for database operations.

## Before you Begin

- You must [Configure OIDC for Workforce Authentication.](/docs/manual/core/oidc/workforce/workforce-external-provider#std-label-workforce-external-provider)

- You must [Configure MongoDB with Workforce Identity Federation.](/docs/manual/core/oidc/workforce/configure-oidc#std-label-configure-oidc)

**Note:**

Your [`oidcIdentityProviders`](/docs/manual/reference/parameters#mongodb-parameter-param.oidcIdentityProviders) configuration determines the approach you must take to authorize users:

- If the `useAuthorizationClaim` field is set to `false` to enable internal authorization, authorize users with user IDs.

- If the field is set to `true`, authorize users with IdP groups.

## Steps

### Authorize Users with IdP Groups

1. Create MongoDB roles

   In the `admin` database, use the [`db.createRole()`](/docs/manual/reference/method/db.createRole#mongodb-method-db.createRole) method to create roles that map the IdP group roles to MongoDB roles.

   Use the following format to create roles:

   ```text
   <authNamePrefix>/<authorizationClaim>
   ```

   The [`oidcIdentityProviders`](/docs/manual/reference/parameters#mongodb-parameter-param.oidcIdentityProviders) parameter provides the `authNamePrefix` field and the `authorizationClaim` field. For example:

   ```javascript
   db.createRole( {
      role: "okta/Everyone",
      privileges: [ ],
      roles: [ "readWriteAnyDatabase" ]
   } )
   ```

## Next Steps

You can connect an application to MongoDB using Workforce Identity Federation in the following ways:

- [Compass](https://www.mongodb.com/docs/compass/current/connect/#connect-with-openid-connect)

- [MongoDB Shell](https://www.mongodb.com/docs/mongodb-shell/connect/#connect-with-openid-connect)

  For more details on MongoDB Shell OIDC options, see [Authentication Options](https://www.mongodb.com/docs/mongodb-shell/reference/options/#std-option-mongosh.--oidcFlows)

## Learn More

- [Workforce Identity Federation with OpenID Connect](/docs/manual/core/oidc/workforce#std-label-workforce)

- [Workload Identity Federation with OAuth 2.0](/docs/manual/core/oidc/workload#std-label-workload)
