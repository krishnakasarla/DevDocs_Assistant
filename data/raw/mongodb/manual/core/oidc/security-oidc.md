> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Authentication and Authorization with OIDC/OAuth 2.0

MongoDB Enterprise supports OpenID Connect (OIDC) and OAuth 2.0 authentication and authorization for both human users and applications. These protocols enable Workforce and Workload Identity Federation, which streamline authentication and authorization by integrating with external IdPs. This lets you simplify your security management and enhance your system's scalability and flexibility.

**Important:**

OpenID Connect (OIDC) is only supported on Linux.

## Use Cases

Workload and Workforce Identity Federation use OIDC and OAuth 2.0 as follows:

- Workforce Identity Federation uses OIDC to enable human users to authenticate and get authorized using an external IdP.

- Workload Identity Federation uses OAuth 2.0 to enable your applications to access MongoDB using external programmatic identities such as Azure Service Principals, Azure Managed Identities, and Google Service Accounts.

## Behavior

To use Workforce and Workload Identity Federation, you must use MongoDB Enterprise and have MongoDB 7.0.11 or later.

To verify that you are using MongoDB Enterprise, pass the `--version` command line option to the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) or [`mongos`:](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos)

```bash
mongod --version
```

In the output from this command, look for the string `modules:
subscription` or `modules: enterprise` to confirm you are using the MongoDB Enterprise binaries.

## Get Started

Select an authentication method to get started:

| Authentication method | User type | Supported protocols |
| --- | --- | --- |
| [Workforce Identity Federation with OpenID Connect](/docs/manual/core/oidc/workforce#std-label-workforce) | Human users | OIDC |
| [Workload Identity Federation with OAuth 2.0](/docs/manual/core/oidc/workload#std-label-workload) | Programmatic users | OAuth 2.0 |
