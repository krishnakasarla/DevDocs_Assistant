> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Workforce Identity Federation with OpenID Connect

Workforce Identity Federation uses OpenID Connect (OIDC) to enable human users to authenticate and get authorized using an external IdP (Identity Provider). You can use Workforce Identity Federation to enhance security and simplify user management.

## Use Cases

With Workforce Identity Federation, you can:

- Manage your workforce access to MongoDB deployments through your existing IdP.

- Enforce security policies such as password complexity, credential rotation, and multi-factor authentication within your IdP.

- Grant access for a group of users or a single user.

## Behavior

You must use MongoDB Enterprise and have MongoDB 7.0.11 or later.

To verify that you are using MongoDB Enterprise, pass the `--version` command line option to the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) or [`mongos`:](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos)

```bash
mongod --version
```

In the output from this command, look for the string `modules:
subscription` or `modules: enterprise` to confirm you are using the MongoDB Enterprise binaries.

## Get Started

To configure and use Workforce Identity Federation, you must perform the following tasks:

1. [Configure OIDC for Workforce Authentication](/docs/manual/core/oidc/workforce/workforce-external-provider#std-label-workforce-external-provider)

   Register your OIDC application with an IdP that supports the OIDC standard, such as Microsoft Entra ID, Okta, or Ping Identity.

2. [Configure MongoDB with Workforce Identity Federation](/docs/manual/core/oidc/workforce/configure-oidc#std-label-configure-oidc)

   Configure your MongoDB server to use Workforce Identity Federation with OIDC.

3. [Authorize Users with Workforce Identity Federation](/docs/manual/core/oidc/workforce/database-user-workforce#std-label-database-user-workforce)

   Specify privileges for workforce identity principals by adding roles to MongoDB (for OIDC, external authorization, or both) or adding database users to MongoDB (for database-managed authorization).
