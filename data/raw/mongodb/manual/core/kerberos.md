> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Kerberos Authentication on Self-Managed Deployments

## Overview

MongoDB Enterprise provides support for Kerberos authentication of MongoDB clients to [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) and [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instances. Kerberos is an industry standard authentication protocol for large client/server systems. Kerberos allows MongoDB and applications to take advantage of existing authentication infrastructure and processes. MongoDB Enterprise only supports the [MIT implementation](https://kerberos.org/) of Kerberos.

## Kerberos Components and MongoDB

### Principals

In a Kerberos-based system, every participant in the authenticated communication is known as a "principal", and every principal must have a unique name.

Principals belong to administrative units called *realms*. For each realm, the Kerberos Key Distribution Center (KDC) maintains a database of the realm's principal and the principals' associated "secret keys".

For a client-server authentication, the client requests from the KDC a "ticket" for access to a specific asset. KDC uses the client's secret and the server's secret to construct the ticket which allows the client and server to mutually authenticate each other, while keeping the secrets hidden.

For the configuration of MongoDB for Kerberos support, two kinds of principal names are of interest: [user principals](/docs/manual/core/kerberos#std-label-kerberos-user-principal) and [service principals.](/docs/manual/core/kerberos#std-label-kerberos-service-principal)

#### User Principal

To authenticate using Kerberos, you must add the Kerberos user principals to MongoDB to the `$external` database. User principal names have the form:

```none
<username>@<KERBEROS REALM>
```

For every user you want to authenticate using Kerberos, you must create a corresponding user in MongoDB in the `$external` database.

To use [Client Sessions and Causal Consistency Guarantees](/docs/manual/core/read-isolation-consistency-recency#std-label-sessions) with `$external` authentication users (Kerberos, LDAP, or X.509 users), usernames cannot be greater than 10k bytes.

For examples of adding a user to MongoDB as well as authenticating as that user, see [Configure MongoDB with Kerberos Authentication on Linux](/docs/manual/tutorial/control-access-to-mongodb-with-kerberos-authentication) and [Configure MongoDB with Kerberos Authentication on Windows.](/docs/manual/tutorial/control-access-to-mongodb-windows-with-kerberos-authentication)

**See also:**

[Manage Users and Roles on Self-Managed Deployments](/docs/manual/tutorial/manage-users-and-roles) for general information regarding creating and managing users in MongoDB.

#### Service Principal

Every MongoDB [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) and [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instance (or [`mongod.exe`](/docs/manual/reference/program/mongod.exe#mongodb-binary-bin.mongod.exe) or [`mongos.exe`](/docs/manual/reference/program/mongos.exe#mongodb-binary-bin.mongos.exe) on Windows) must have an associated service principal. Service principal names have the form:

```none
<service>/<fully qualified domain name>@<KERBEROS REALM>
```

For MongoDB, the `<service>` defaults to `mongodb`. For example, if `m1.example.com` is a MongoDB server, and `example.com` maintains the `EXAMPLE.COM` Kerberos realm, then `m1` should have the service principal name `mongodb/m1.example.com@EXAMPLE.COM`.

To specify a different value for `<service>`, use [`serviceName`](/docs/manual/reference/configuration-options#mongodb-setting-security.sasl.serviceName) during the start up of [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) or [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) (or [`mongod.exe`](/docs/manual/reference/program/mongod.exe#mongodb-binary-bin.mongod.exe) or [`mongos.exe`](/docs/manual/reference/program/mongos.exe#mongodb-binary-bin.mongos.exe)). [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) or other clients may also specify a different service principal name using [`serviceName`.](/docs/manual/reference/configuration-options#mongodb-setting-security.sasl.serviceName)

Service principal names must be reachable over the network using the fully qualified domain name (FQDN) part of its service principal name.

By default, Kerberos attempts to identify hosts using the `/etc/krb5.conf` file before using DNS to resolve hosts.

On Windows, if running MongoDB as a service, see [Assign Service Principal Name to MongoDB Windows Service.](/docs/manual/tutorial/control-access-to-mongodb-windows-with-kerberos-authentication#std-label-assign-service-principal-name)

### Linux Keytab Files

Linux systems can store Kerberos authentication keys for a [service principal](/docs/manual/core/kerberos#std-label-kerberos-service-principal) in *keytab* files. Each Kerberized [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) and [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instance running on Linux must have access to a keytab file containing keys for its [service principal.](/docs/manual/core/kerberos#std-label-kerberos-service-principal)

To keep keytab files secure, use file permissions that restrict access to only the user that runs the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) or [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) process.

### Tickets

On Linux, MongoDB clients can use Kerberos's `kinit` program to initialize a credential cache for authenticating the user principal to servers.

### Windows Active Directory

Unlike on Linux systems, [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) and [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instances running on Windows do not require access to keytab files. Instead, the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) and [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instances read their server credentials from a credential store specific to the operating system.

However, from the Windows Active Directory, you can export a keytab file for use on Linux systems. See [Ktpass](http://technet.microsoft.com/en-us/library/cc753771.aspx) for more information.

### Authenticate With Kerberos

To configure MongoDB for Kerberos support and authenticate, see [Configure MongoDB with Kerberos Authentication on Linux](/docs/manual/tutorial/control-access-to-mongodb-with-kerberos-authentication) and [Configure MongoDB with Kerberos Authentication on Windows.](/docs/manual/tutorial/control-access-to-mongodb-windows-with-kerberos-authentication)

## Operational Considerations

### DNS

Each host that runs a [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) or [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instance must have both `A` and `PTR` DNS records to provide forward and reverse lookup.

Without `A` and `PTR` DNS records, the host cannot resolve the components of the Kerberos domain or the Key Distribution Center (KDC).

### System Time Synchronization

To successfully authenticate, the system time for each [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) and [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instance must be within 5 minutes of the system time of the other hosts in the Kerberos infrastructure.

## Kerberized MongoDB Environments

### Driver Support

The following MongoDB drivers support Kerberos authentication:

- [C](https://www.mongodb.com/docs/drivers/c/)

- [C++](https://www.mongodb.com/docs/drivers/cpp/)

- [Java](https://www.mongodb.com/docs/drivers/java/)

- [C#](https://www.mongodb.com/docs/drivers/csharp/)

- [Go](https://www.mongodb.com/docs/drivers/go/)

- [Node.js](https://www.mongodb.com/docs/drivers/javascript/)

- [Perl](https://metacpan.org/pod/MongoDB::MongoClient#GSSAPI-\(for-Kerberos\))

- [PHP](https://www.mongodb.com/docs/drivers/php/)

- [Python](https://www.mongodb.com/docs/drivers/python/)

- [Ruby](https://www.mongodb.com/docs/drivers/ruby/)

- [Rust](https://www.mongodb.com/docs/drivers/rust/)

- [Scala](https://www.mongodb.com/docs/drivers/scala/)

- [Swift](https://mongodb.github.io/mongo-swift-driver/docs/current/)

### Use with Additional MongoDB Authentication Mechanism

Although MongoDB supports the use of Kerberos authentication with other authentication mechanisms, only add the other mechanisms as necessary. See the `Incorporate Additional Authentication Mechanisms` section in [Configure MongoDB with Kerberos Authentication on Linux](/docs/manual/tutorial/control-access-to-mongodb-with-kerberos-authentication) and [Configure MongoDB with Kerberos Authentication on Windows](/docs/manual/tutorial/control-access-to-mongodb-windows-with-kerberos-authentication) for details.

## Testing and Verification

The [`mongokerberos`](/docs/manual/reference/program/mongokerberos#mongodb-binary-bin.mongokerberos) program provides a convenient method to verify your platform's Kerberos configuration for use with MongoDB, and to test that Kerberos authentication from a MongoDB client works as expected. See the [`mongokerberos`](/docs/manual/reference/program/mongokerberos#mongodb-binary-bin.mongokerberos) documentation for more information.

[`mongokerberos`](/docs/manual/reference/program/mongokerberos#mongodb-binary-bin.mongokerberos) is available in MongoDB Enterprise only.
