> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

<!--
Tab options on this page. Append to the .md URL to filter:
  ?tabs=<id,...>   select specific tabs (e.g. ?tabs=nodejs,shell)
  ?allTabs=true    include every tab
  (no param)       default: one tab per tabset

Available tabs:
  other tabs: config file, command line, update internal auth, update command line internal auth
-->

# Configure MongoDB with Workload Identity Federation

Configure MongoDB with Workload Identity Federation to authenticate services across different platforms. This enhances security and simplifies service identity management.

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

- Configure your external IdP (Identity Provider). For more details, see [Configure Workload Identity Federation.](/docs/manual/core/oidc/workload/workload-external-provider#std-label-workload-external-provider)

## Steps

1. Configure the MongoDB server with OpenID Connect (OIDC)

   To configure the MongoDB server, enable the [MONGODB-OIDC](/docs/manual/core/oidc/security-oidc#std-label-authentication-oidc) authentication mechanism and use the [`oidcIdentityProviders`](/docs/manual/reference/parameters#mongodb-parameter-param.oidcIdentityProviders) to specify IdP configurations.

   **Note:**

   When configuring MongoDB for Workload Identity Federation, set the `supportsHumanFlows` field in [`oidcIdentityProviders`](/docs/manual/reference/parameters#mongodb-parameter-param.oidcIdentityProviders) to `false`.

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
             "supportsHumanFlows": false
           }
         ]
   ```

   To specify multiple IdPs, add additional objects to the `oidcIdentityProviders` array. For example:

   ```javascript
   setParameter:
      authenticationMechanisms: "MONGODB-OIDC,SCRAM-SHA-256"
      oidcIdentityProviders: |
         [
           {
             "issuer": "https://okta-test.okta.com",
             "audience": "example@kernel.mongodb.com",
             "authNamePrefix": "okta-issuer",
             "authorizationClaim": "groups",
             "supportsHumanFlows": false
           },
           {
             "issuer": "https://azure-test.azure.com",
             "audience": "example2@kernel.mongodb.com",
             "authNamePrefix": "azure-issuer",
             "authorizationClaim": "groups",
             "supportsHumanFlows": false
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
             "supportsHumanFlows": false
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
             "supportsHumanFlows": false
           },
           {
             "issuer": "https://azure-test.azure.com",
             "audience": "example2@kernel.mongodb.com",
             "authNamePrefix": "azure-issuer",
             "useAuthorizationClaim": false,
             "supportsHumanFlows": false
           }
         ]
   ```

   When you set `useAuthorizationClaim` to `false`, users who authenticate with the `MONGODB-OIDC` mechanism obtain their authorization rights from a user document in `$external`. The server searches for a user document with an `_id` matching the value of the `authNamePrefix/principalName` claim for every OIDC based authentication attempt for a user of your IdP.

3. *(Conditional)* CA Certificates for Internal X509 TLS

   For environments using X509 TLS certificates signed by an internal Certificate Authority (CA), you must add the CA certificate to the system CA certificate bundle so that [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) can communicate with the identity provider. This applies to user authentication and to workload authentication when using the callback method. Omitting this step might result in OIDC SSL Certificate or JWT Key Verification errors.

## Next Steps

- [Authorize Users with Workload Identity Federation](/docs/manual/core/oidc/workload/database-user-workload#std-label-database-user-workload)

## Learn More

- [OpenID Connect Authentication](/docs/manual/core/oidc/security-oidc#std-label-authentication-oidc)
