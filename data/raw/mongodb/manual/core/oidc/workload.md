> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Workload Identity Federation with OAuth 2.0

Workload Identity Federation uses OAuth 2.0 to enable your applications to access MongoDB using external programmatic identities such as Azure Service Principals, Azure Managed Identities, and Google Service Accounts.

**Important:**

OpenID Connect (OIDC) is only supported on Linux.

## Use Cases

With Workload Identity Federation, you can:

- Manage your application's access to MongoDB deployments through your existing cloud provider or IdP (Identity Provider).

- Enforce security policies such as role-based access control, credential rotation, and workload-specific permissions.

- Grant access to specific applications, containers, or virtual machines without managing individual service accounts.

## Behavior

- To use Workload Identity Federation, you must use MongoDB Enterprise and have MongoDB 7.0.11 or later.

  To verify that you are using MongoDB Enterprise, pass the `--version` command line option to the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) or [`mongos`:](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos)

  ```bash
  mongod --version
  ```

  In the output from this command, look for the string `modules:
  subscription` or `modules: enterprise` to confirm you are using the MongoDB Enterprise binaries.

- Workload Identity Federation allows your applications to access MongoDB clusters with OAuth 2.0 access tokens. The access tokens can be issued by any external IdP, including Azure Entra ID and Google Cloud Platform.

- MongoDB stores user identifiers and privileges, but not secrets.

## Get Started

To configure and use Workload Identity Federation, perform the following tasks:

1. [Configure Workload Identity Federation](/docs/manual/core/oidc/workload/workload-external-provider#std-label-workload-external-provider)

   Register your OAuth 2.0 application with an IdP that supports the OAuth 2.0 standard, such as Azure Service Principals, Azure Managed Identities and Google Service Accounts.

2. [Configure MongoDB with Workload Identity Federation](/docs/manual/core/oidc/workload/configure-mongodb-workload#std-label-configure-mongodb-workload)

   Configure your MongoDB server to use Workload Identity Federation with OAuth 2.0.

3. [Authorize Users with Workload Identity Federation](/docs/manual/core/oidc/workload/database-user-workload#std-label-database-user-workload)

   Specify privileges for workload identity principals by adding roles to MongoDB (for OAuth, external authorization, or both) or adding database users to MongoDB (for database-managed authorization).

## Details

MongoDB Drivers support two types of authentication flow for Workload Identity Federation: Built-in Authentication and Callback Authentication.

### Built-in Authentication

You can use built-in authentication if you deploy your application on a supported infrastructure with a supported principal type. Your application can access MongoDB clusters without supplying a password or manually requesting a JSON Web Tokens (JWT) from your cloud provider's metadata service. Instead, your chosen MongoDB driver uses your existing principal identifier to request a JWT access token under the hood, which is then passed to the Atlas cluster automatically when your application connects.

For more implementation details, see your chosen [Driver's documentation.](https://www.mongodb.com/docs/drivers/)

#### Built-in Authentication Supported Infrastructure and Principal Types

| Cloud Provider | Infrastructure Type | Principal Type |
| --- | --- | --- |
| Google Cloud Provider (GCP) | Compute Engine | GCP Service Accounts |
|  | App Engine Standard Environment | |
|  | App Engine Flexible Environment | |
|  | Cloud Functions | |
|  | Google Run | |
|  | Google Kubernetes Engine | |
|  | Cloud Build | |
| Azure | Azure VM | Azure Managed Identities (User and System assigned) |

### Callback Authentication

You can use callback authentication with any service supporting OAuth 2.0 access tokens. Workload Identity Federation calls a callback method, in which you can request the required JWT from your authorization server or cloud provider that you must pass when your application connects to MongoDB with Workload Identity Federation.

Review your chosen [driver's documentation](https://www.mongodb.com/docs/drivers/) for more  implementation details.
