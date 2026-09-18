> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

<!--
Tab options on this page. Append to the .md URL to filter:
  ?tabs=<id,...>   select specific tabs (e.g. ?tabs=nodejs,shell)
  ?allTabs=true    include every tab
  (no param)       default: one tab per tabset

Available tabs:
  other tabs: config file, command line, update internal auth, update command line internal auth
-->

# Configure MongoDB with Workforce Identity Federation

Configure MongoDB with Workforce Identity Federation to authenticate users across different platforms using a single set of credentials. This enhances security and simplifies user management.

**Important:**

OpenID Connect (OIDC) is only supported on Linux.

## Before you Begin

- Ensure that you are on MongoDB Enterprise.

  To verify that you are using MongoDB Enterprise, pass the `--version` command line option to the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) or [`mongos`:](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos)

  ```bash
  mongod --version
  ```

  In the output from this command, look for the string `modules:
  subscription` or `modules: enterprise` to confirm you are using the MongoDB Enterprise binaries.

- Configure your external IdP (Identity Provider). For more details, see [Configure OIDC for Workforce Authentication.](/docs/manual/core/oidc/workforce/workforce-external-provider#std-label-workforce-external-provider)

## Steps

1. Configure the MongoDB server with OpenID Connect (OIDC)

   **Note:**

   When configuring MongoDB for Workforce Identity Federation, omit the `supportsHumanFlows` field in [`oidcIdentityProviders`.](/docs/manual/reference/parameters#mongodb-parameter-param.oidcIdentityProviders)

   You can configure the MongoDB server using your configuration file or command line.

   ### Configuration file

   To use your configuration file, specify these parameters in the file:

   ```yaml
   setParameter:
      authenticationMechanisms: "MONGODB-OIDC,SCRAM-SHA-256"
      oidcIdentityProviders: |
         [
           {
             "issuer": "https://okta-test.okta.com",
             "audience": "example@kernel.mongodb.com",
             "authNamePrefix": "okta-issuer",
             "authorizationClaim": "groups",
             "clientId": "0zzw3ggfd2ase33"
           }
         ]
   ```

   To specify multiple IdPs, add additional objects to the `oidcIdentityProviders` array. When you specify multiple IdPs, you must specify a `matchPattern` for each provider. For example:

   ```yaml
   setParameter:
      authenticationMechanisms: "MONGODB-OIDC,SCRAM-SHA-256"
      oidcIdentityProviders: |
         [
           {
             "issuer": "https://okta-test.okta.com",
             "audience": "example@kernel.mongodb.com",
             "authNamePrefix": "okta-issuer",
             "authorizationClaim": "groups",
             "matchPattern": "@okta.com$",
             "clientId": "0zzw3ggfd2ase33"
           },
           {
             "issuer": "https://azure-test.azure.com",
             "audience": "example2@kernel.mongodb.com",
             "authNamePrefix": "azure-issuer",
             "authorizationClaim": "groups",
             "matchPattern": "@azure.com$",
             "clientId": "1zzw3ggfd2ase33"
           }
         ]
   ```

2. *(Optional)* Enable internal authorization

   To enable internal authorization, set the `useAuthorizationClaim` field of the `oidcIdentityProviders` parameter to `false`. This setting enables more flexible user management by relying on user documents rather than authorization claims from the IdP.

   **Important:**

   If `useAuthorizationClaim` is set to `false`, **do not** include the `authorizationClaim` field.

   ### Configuration file

   ```yaml
   setParameter:
      authenticationMechanisms: "MONGODB-OIDC,SCRAM-SHA-256"
      oidcIdentityProviders: |
         [
           {
             "issuer": "https://okta-test.okta.com",
             "audience": "example@kernel.mongodb.com",
             "authNamePrefix": "okta-issuer",
             "useAuthorizationClaim": false,
             "clientId": "0zzw3ggfd2ase33"
           }
         ]
   ```

   To specify multiple IdPs, add additional objects to the `oidcIdentityProviders` array. For example:

   ```yaml
   setParameter:
      authenticationMechanisms: "MONGODB-OIDC,SCRAM-SHA-256"
      oidcIdentityProviders: |
         [
           {
             "issuer": "https://okta-test.okta.com",
             "audience": "example@kernel.mongodb.com",
             "authNamePrefix": "okta-issuer",
             "useAuthorizationClaim": false,
             "clientId": "0zzw3ggfd2ase33"
           },
           {
             "issuer": "https://azure-test.azure.com",
             "audience": "example2@kernel.mongodb.com",
             "authNamePrefix": "azure-issuer",
             "useAuthorizationClaim": false,
             "clientId": "1zzw3ggfd2ase33"
           }
         ]
   ```

   When you set `useAuthorizationClaim` to `false`, users who authenticate with the `MONGODB-OIDC` mechanism obtain their authorization rights from a user document in `$external`. The server searches for a user document with an `_id` matching the value of the `authNamePrefix/principalName` claim for every OIDC based authentication attempt for a user of your IdP.

3. *(Conditional)* CA Certificates for Internal X509 TLS

   For environments using X509 TLS certificates signed by an internal Certificate Authority (CA), you must add the CA certificate to the system CA certificate bundle so that [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) can communicate with the identity provider. This applies to user authentication and to workload authentication when using the callback method. Omitting this step might result in OIDC SSL Certificate or JWT Key Verification errors.

## oidcIdentityProviders for Sharded Clusters

In a sharded cluster, configure [`oidcIdentityProviders`](/docs/manual/reference/parameters#mongodb-parameter-param.oidcIdentityProviders) on every [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instance. Clients authenticate through `mongos`, which requires this configuration to verify IdP tokens. If clients connect directly to config servers or shard [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instances, you must also configure `oidcIdentityProviders` on those instances.

Apply the steps in this tutorial to each `mongos` instance in your deployment. To configure database users for Workforce Identity Federation, see [Authorize Users with Workforce Identity Federation.](/docs/manual/core/oidc/workforce/database-user-workforce#std-label-database-user-workforce)
