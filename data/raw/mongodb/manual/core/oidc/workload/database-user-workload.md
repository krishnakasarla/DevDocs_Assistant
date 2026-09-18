> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

<!--
Tab options on this page. Append to the .md URL to filter:
  ?tabs=<id,...>   select specific tabs (e.g. ?tabs=nodejs,shell)
  ?allTabs=true    include every tab
  (no param)       default: one tab per tabset

Available tabs:
  other tabs: add-idp-groups, add-user-id
-->

# Authorize Users with Workload Identity Federation

You can add a database user to MongoDB using Workload Identity Federation. This approach enables your organization’s IdP to manage user access, ensuring secure, centralized authentication for database operations.

## Before you Begin

- You must [Configure Workload Identity Federation.](/docs/manual/core/oidc/workload/workload-external-provider#std-label-workload-external-provider)

- You must [Configure MongoDB with Workload Identity Federation.](/docs/manual/core/oidc/workload/configure-mongodb-workload#std-label-configure-mongodb-workload)

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

You can connect an application to MongoDB using Workload Identity Federation with the following supported drivers:

- [Java](https://www.mongodb.com/docs/drivers/java/sync/current/fundamentals/enterprise-auth/#std-label-mongodb-oidc)

- [Kotlin](https://www.mongodb.com/docs/drivers/kotlin/coroutine/upcoming/fundamentals/enterprise-auth/#std-label-kotlin-oidc)

- [Node.js](https://www.mongodb.com/docs/drivers/node/current/fundamentals/authentication/enterprise-mechanisms/#mongodb-oidc)

- [PyMongo](https://www.mongodb.com/docs/languages/python/pymongo-driver/security/enterprise-authentication/#mongodb-oidc)

- [TypeScript](https://www.mongodb.com/docs/drivers/typescript/)

- [C#](https://www.mongodb.com/docs/drivers/csharp/current/fundamentals/enterprise-authentication/#std-label-csharp-mongodb-oidc)

- [Go](https://www.mongodb.com/docs/drivers/go/current/fundamentals/enterprise-auth/#mongodb-oidc)

- [Rust](https://www.mongodb.com/docs/drivers/rust/current/security/authentication/oidc/#std-label-rust-authentication-oidc)

- [Scala](https://www.mongodb.com/docs/languages/scala/scala-driver/?tck=docs)

## Learn More

- [Workload Identity Federation with OAuth 2.0](/docs/manual/core/oidc/workload#std-label-workload)

- [Workforce Identity Federation with OpenID Connect](/docs/manual/core/oidc/workforce#std-label-workforce)
