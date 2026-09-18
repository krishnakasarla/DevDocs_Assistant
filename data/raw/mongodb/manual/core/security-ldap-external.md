> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# LDAP Authorization on Self-Managed Deployments

**Note:**

Starting in MongoDB 8.0, LDAP authentication and authorization is deprecated. LDAP is available and will continue to operate without changes throughout the lifetime of MongoDB 8. LDAP will be removed in a future major release.

For details, see [LDAP Deprecation.](/docs/manual/core/LDAP-deprecation#std-label-ldap-deprecation)

[MongoDB Enterprise](http://www.mongodb.com/products/mongodb-enterprise-advanced) supports querying an LDAP server for the LDAP groups to which the authenticated user belongs. MongoDB maps the distinguished names (DN) of each returned group to [roles](/docs/manual/core/authorization#std-label-roles) on the `admin` database. MongoDB authorizes the user based on the mapped roles and their associated privileges.

The LDAP Authorization process is summarized below:

1. A client connects to MongoDB and performs authentication with any [authentication](/docs/manual/core/authentication#std-label-authentication) mechanism that [supports external authentication.](/docs/manual/core/security-ldap-external#std-label-security-ldap-external-compatibility)

   To use [Client Sessions and Causal Consistency Guarantees](/docs/manual/core/read-isolation-consistency-recency#std-label-sessions) with `$external` authentication users (Kerberos, LDAP, or X.509 users), usernames cannot be greater than 10k bytes.

2. MongoDB binds to the LDAP server specified with [`security.ldap.servers`](/docs/manual/reference/configuration-options#mongodb-setting-security.ldap.servers) using the credentials specified with [`security.ldap.bind.queryUser`](/docs/manual/reference/configuration-options#mongodb-setting-security.ldap.bind.queryUser) and [`security.ldap.bind.queryPassword`.](/docs/manual/reference/configuration-options#mongodb-setting-security.ldap.bind.queryPassword)

   MongoDB uses simple binding by default, but can use `sasl` binding instead if configured in [`security.ldap.bind.method`](/docs/manual/reference/configuration-options#mongodb-setting-security.ldap.bind.method) and [`security.ldap.bind.saslMechanisms`.](/docs/manual/reference/configuration-options#mongodb-setting-security.ldap.bind.saslMechanisms)

3. MongoDB constructs an LDAP query using the [`security.ldap.authz.queryTemplate`](/docs/manual/reference/configuration-options#mongodb-setting-security.ldap.authz.queryTemplate) and queries the LDAP server for the authenticated user's group membership.

   MongoDB can use the [`security.ldap.userToDNMapping`](/docs/manual/reference/configuration-options#mongodb-setting-security.ldap.userToDNMapping) option to transform the username for supporting the query template.

4. The LDAP server evaluates the query and returns the list of groups to which the authenticated user belongs.

5. MongoDB authorizes the user to perform actions on the server by mapping each returned group's Distinguished Name (DN) into a [role](/docs/manual/core/authorization#std-label-authorization) on the `admin` database. If a returned group DN exactly matches the name of an existing role on the `admin` database, MongoDB grants the user the roles and privileges assigned to that role. See [MongoDB Roles for LDAP Authorization](/docs/manual/core/security-ldap-external#std-label-security-ldap-external-roles) for more information.

6. The client can perform actions on the MongoDB server which require the roles or privileges granted to the authenticated user.

7. At an interval defined by [`ldapUserCacheInvalidationInterval`](/docs/manual/reference/parameters#mongodb-parameter-param.ldapUserCacheInvalidationInterval), MongoDB flushes the `$external` cache. Prior to executing subsequent operations performed by externally authorized users, MongoDB re-acquires their group membership from the LDAP server.

## Considerations

A full description of LDAP is beyond the scope of this documentation. This page assumes prior knowledge of LDAP.

This documentation only describes MongoDB LDAP authorization, and does not replace other resources on LDAP. We encourage you to thoroughly familiarize yourself with LDAP and its related subject matter before configuring LDAP authentication.

MongoDB can provide [professional services](https://www.mongodb.com/products/consulting) for optimal configuration of LDAP authorization for your MongoDB deployment.

### Compatible Authentication Mechanism

MongoDB supports LDAP authorization with the following authentication methods:

- [Self-Managed LDAP Proxy Authentication](/docs/manual/core/security-ldap#std-label-security-ldap)

- [Kerberos Authentication on Self-Managed Deployments](/docs/manual/core/kerberos#std-label-security-kerberos)

- [x.509](/docs/manual/core/security-x.509#std-label-security-auth-x509)

With this configuration, MongoDB uses LDAP, X.509, or Kerberos authorization to authenticate client connections.

### Connection Pool

When connecting to the LDAP server for authentication/authorization, MongoDB, by default:

- Uses connection pooling if run:

  - on Windows or

  - on Linux where MongoDB Enterprise binaries are linked against [libldap\_r.](/docs/manual/core/security-ldap#std-label-libldap-vs-libldap_r)

- Does not use connection pooling if run:

  - on Linux where MongoDB Enterprise binaries are linked against [libldap.](/docs/manual/core/security-ldap#std-label-libldap-vs-libldap_r)

To change the connection pooling behavior, update the [`ldapUseConnectionPool`](/docs/manual/reference/parameters#mongodb-parameter-param.ldapUseConnectionPool) parameter.

### `libldap` and `libldap_r`

For MongoDB 4.2 Enterprise binaries linked against `libldap` (such as when running on RHEL), access to the `libldap` is synchronized, incurring some performance/latency costs.

For MongoDB 4.2 Enterprise binaries linked against `libldap_r`, there is no change in behavior from earlier MongoDB versions.

### User Management

With LDAP authorization, user creation and management occurs on the LDAP server. MongoDB requires creation of [roles](/docs/manual/core/authorization#std-label-roles) on the `admin` database, with the name of each role exactly matching a LDAP group Distinguished Name (DN). This is in contrast to MongoDB managed authorization, which requires creating users on the `$external` database.

To manage roles on the MongoDB server, authenticate as a user whose group membership corresponds to a `admin` database role with role administration privileges, such as those provided by [`userAdmin`](/docs/manual/reference/built-in-roles#mongodb-authrole-userAdmin). Create or update roles corresponding to LDAP group DNs such that users with membership in that group receive the appropriate roles and privileges.

For example, an LDAP group for database administrators might have a role with administrative roles and privileges. An LDAP group for marketing or analytics users may have a role with only have read privileges on certain databases.

**Important:**

When configuring a role for a corresponding LDAP Group, remember that *all* users with membership in that group can receive the configured roles and privileges. Consider applying the principle of least privilege when configuring MongoDB roles, LDAP groups, or group membership.

If no role with role administration privileges exists *AND* no non-`$external` user with these privileges exists, you effectively cannot perform user management, as no new or existing roles can be altered to reflect additions or changes to groups or group membership on the LDAP server.

To remedy a scenario where you cannot manage roles on the MongoDB server, perform the following procedure:

1. Restart the MongoDB server without authentication and LDAP authorization

2. Create a role on the `admin` database whose name corresponds to the appropriate LDAP group Distinguished Name. When choosing a group DN, consider which group is most appropriate for database administration.

3. Restart the MongoDB server with authentication and LDAP authorization

4. Authenticate as a user with membership in the group corresponding to the created administrative role.

### Existing Users

A MongoDB server using LDAP for authorization makes any existing users on the `$external` database inaccessible. If there are existing users in `$external` database, you must meet the following requirements for each user on the `$external` database to ensure continued access:

- User has a corresponding user object on the LDAP server

- User object has membership in the appropriate LDAP groups

- MongoDB has roles on the `admin` database named for the user's LDAP groups, such that the granted roles and privileges are identical to those granted to the non-`$external` user.

If you want to continue allowing access by users *not* on the `$external` database, ensure the [`authenticationMechanisms`](/docs/manual/reference/parameters#mongodb-parameter-param.authenticationMechanisms) parameter includes `SCRAM-SHA-1` and/or `SCRAM-SHA-256` as appropriate. Alternatively, apply the requirements listed above for transitioning those users to LDAP authorization.

### Replica Sets

For [replica sets](/docs/manual/reference/glossary#std-term-replica-set), configure LDAP authorization on the [secondary](/docs/manual/reference/glossary#std-term-secondary) and [arbiter](/docs/manual/reference/glossary#std-term-arbiter) members first before configuring the [primary](/docs/manual/reference/glossary#std-term-primary). This also applies to [shard replica sets](/docs/manual/core/sharded-cluster-shards#std-label-shards-concepts), or [config server replica sets](/docs/manual/core/sharded-cluster-config-servers#std-label-csrs). Configure one replica set member at a time to maintain a majority of members for write availability.

### Sharded Clusters

In [sharded clusters](/docs/manual/reference/glossary#std-term-sharded-cluster), you must configure LDAP authorization on the [config servers](/docs/manual/reference/glossary#std-term-config-server) for cluster-level users. You can optionally configure LDAP authorization on each [shard](/docs/manual/reference/glossary#std-term-shard) for shard-local users.

## Configuration

You must configure the following settings to use LDAP Authorization:

To use LDAP for authorization via operating system libraries, specify the following settings as a part of your [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) or [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) configuration file:

| Option | Description | Required |
| --- | --- | --- |
| [`security.ldap.servers`](/docs/manual/reference/configuration-options#mongodb-setting-security.ldap.servers) | Quote-enclosed comma-separated list of LDAP servers in `host[:port]` format. You can prefix LDAP servers with `srv:` and `srv_raw:`. If your connection string specifies `"srv:<DNS_NAME>"`, [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) verifies that `"_ldap._tcp.gc._msdcs.<DNS_NAME>"` exists for SRV to support Active Directory. If not found, [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) verifies that `"_ldap._tcp.<DNS_NAME>"` exists for SRV. If an SRV record cannot be found, [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) warns you to use `"srv_raw:<DNS_NAME>"` instead. If your connection string specifies `"srv_raw:<DNS_NAME>"`, [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) performs an SRV record lookup for `"<DNS NAME>"`. | **YES** |
| [`security.ldap.authz.queryTemplate`](/docs/manual/reference/configuration-options#mongodb-setting-security.ldap.authz.queryTemplate) | An [RFC4515](https://tools.ietf.org/html/rfc4515) and [RFC4516](https://tools.ietf.org/html/rfc4516) LDAP formatted query URL template executed by MongoDB to obtain the LDAP groups to which the user belongs to. The query is relative to the host or hosts specified in [`servers`.](/docs/manual/reference/configuration-options#mongodb-setting-security.ldap.servers) You can use the following tokens in the template: `{USER}`Substitutes the authenticated username, or the [`transformed`](/docs/manual/reference/configuration-options#mongodb-setting-security.ldap.userToDNMapping) username, into the LDAP query.; `{PROVIDED_USER}`Substitutes the supplied username, i.e. before either authentication or LDAP transformation, into the LDAP query. Only [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) supports this parameter. [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) defers to this setting as configured on its [config servers](/docs/manual/reference/glossary#std-term-config-server) | **YES** |
| [`security.ldap.bind.queryUser`](/docs/manual/reference/configuration-options#mongodb-setting-security.ldap.bind.queryUser) | The identity the MongoDB server binds as when connecting to and executing operations and queries on an LDAP server. Use with [`queryPassword`.](/docs/manual/reference/configuration-options#mongodb-setting-security.ldap.bind.queryPassword) The user specified must have the appropriate privileges to support the LDAP queries generated from the configured [`queryTemplate`.](/docs/manual/reference/configuration-options#mongodb-setting-security.ldap.authz.queryTemplate) | **YES** |
| [`security.ldap.bind.queryPassword`](/docs/manual/reference/configuration-options#mongodb-setting-security.ldap.bind.queryPassword) | The password used to bind to an LDAP server when using [`queryUser`.](/docs/manual/reference/configuration-options#mongodb-setting-security.ldap.bind.queryUser) | **YES** |
| [`security.ldap.bind.method`](/docs/manual/reference/configuration-options#mongodb-setting-security.ldap.bind.method) | Used to specify the method the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) or [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) uses to authenticate, or bind, to the LDAP server. Specify `sasl` to use one of the SASL protocols defined in [`security.ldap.bind.saslMechanisms`.](/docs/manual/reference/configuration-options#mongodb-setting-security.ldap.bind.saslMechanisms) Defaults to `simple`. | **NO**, unless using `sasl` for binding to the LDAP server. |
| [`security.ldap.bind.saslMechanisms`](/docs/manual/reference/configuration-options#mongodb-setting-security.ldap.bind.saslMechanisms) | Used to specify the SASL mechanisms [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) or [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) can use when authenticating or binding to the LDAP server. MongoDB and the LDAP server must agree on at least one SASL mechanism. Defaults to `DIGEST-MD5`. | **NO**, unless setting [`method`](/docs/manual/reference/configuration-options#mongodb-setting-security.ldap.bind.method) to `sasl`, and you need different or additional SASL mechanisms. |
| [`security.ldap.bind.useOSDefaults`](/docs/manual/reference/configuration-options#mongodb-setting-security.ldap.bind.useOSDefaults) | Windows MongoDB deployments can use the operating system credentials in place of [`queryUser`](/docs/manual/reference/configuration-options#mongodb-setting-security.ldap.bind.queryUser) and [`queryPassword`](/docs/manual/reference/configuration-options#mongodb-setting-security.ldap.bind.queryPassword) for authenticating or binding as when connecting to the LDAP server. | **NO**, unless replacing [`queryUser`](/docs/manual/reference/configuration-options#mongodb-setting-security.ldap.bind.queryUser) and [`queryPassword`.](/docs/manual/reference/configuration-options#mongodb-setting-security.ldap.bind.queryPassword) |
| [`security.ldap.userToDNMapping`](/docs/manual/reference/configuration-options#mongodb-setting-security.ldap.userToDNMapping) | Depending on your [`queryTemplate`](/docs/manual/reference/configuration-options#mongodb-setting-security.ldap.authz.queryTemplate), the authenticated client username may require transformation to support the LDAP query URL. [`userToDNMapping`](/docs/manual/reference/configuration-options#mongodb-setting-security.ldap.userToDNMapping) allows MongoDB to transform incoming usernames. | **NO**, unless client usernames require transformation into LDAP DNs. |

When you have configured LDAP authorization, restart [`mongod`](/docs/manual/reference/program/mongod#std-program-mongod) or [`mongos`](/docs/manual/reference/program/mongos#std-program-mongos). The server now uses LDAP authorization with X.509, Kerberos, or LDAP to authenticate client connections.

### LDAP Query Template

MongoDB uses the [`security.ldap.authz.queryTemplate`](/docs/manual/reference/configuration-options#mongodb-setting-security.ldap.authz.queryTemplate) to create an [RFC4516](https://tools.ietf.org/html/rfc4516) formatted LDAP query URL. In the template, you can use either:

- `{USER}` placeholder to substitute the authenticated username into the LDAP query URL. If MongoDB transformed the username using [`userToDNMapping`](/docs/manual/reference/configuration-options#mongodb-setting-security.ldap.userToDNMapping), MongoDB replaces the `{USER}` token with the transformed username when constructing the LDAP query URL.

- `{PROVIDED_USER}` placeholder to substitute the supplied username, i.e. before either authentication or LDAP transformation, into the LDAP query.

Design the query template to retrieve the user's groups.

**Example:**

The following query template returns any groups listed in the LDAP user object's `memberOf` attribute. This query assumes the `memberOf` attribute exists - your specific LDAP deployment may use a different attribute or methodology for tracking group membership. This query also assumes the user authenticates using their full LDAP DN as their username.

```bash
"{USER}?memberOf?base"
```

The LDAP query URL must conform to the format defined in [RFC4516](https://tools.ietf.org/html/rfc4516):

```text
[ dn  [ ? [attributes] [ ? [scope] [ ? [filter] [ ? [Extensions] ] ] ] ] ]
```

Consider the definition of each component, as quoted from RFC4516:

> The `dn` is an LDAP Distinguished Name using the string format described in [RFC4514](https://tools.ietf.org/html/rfc4514). It identifies the base object of the LDAP search or the target of a non-search operation.
>
> The `attributes` construct is used to indicate which attributes should be returned from the entry or entries.
>
> The `scope` construct is used to specify the scope of the search to perform in the given LDAP server. The allowable scopes are "base" for a base object search, "one" for a one-level search, or "sub" for a subtree search.
>
> The `filter` is used to specify the search filter to apply to entries within the specified scope during the search. It has the format specified in \[RFC4515].
>
> The `extensions` construct provides the LDAP URL with an extensibility mechanism, allowing the capabilities of the URL to be extended in the future.

If the query includes an `attribute`, MongoDB assumes the query retrieves a the DNs which this entity is member of.

If the query does not include an attribute, MongoDB assumes the query retrieves all entities for which the user is member of.

MongoDB currently ignores any extensions specified in the LDAP query.

**Important:**

A full description of RFC4516 or LDAP query URL construction is out of scope for this documentation.

## Tutorials

The following tutorials contain procedures for connecting to an LDAP server via the Operating System LDAP libraries:

- [Authenticate Using Active Directory with Native LDAP](/docs/manual/tutorial/authenticate-nativeldap-activedirectory)

- [Configure Kerberos and Active Directory Authorization](/docs/manual/tutorial/kerberos-auth-activedirectory-authz)

## Connecting to a MongoDB server using LDAP Authorization

When using LDAP for authorization, users connecting via [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) must:

- set [`--authenticationDatabase`](https://www.mongodb.com/docs/mongodb-shell/reference/options/#std-option-mongosh.--authenticationDatabase) to `$external`.

- set [`--authenticationMechanism`](https://www.mongodb.com/docs/mongodb-shell/reference/options/#std-option-mongosh.--authenticationMechanism) to the appropriate authentication mechanism.

  If using [LDAP authentication](/docs/manual/core/security-ldap#std-label-security-ldap), set this to `PLAIN`.

  If using [Kerberos authentication](/docs/manual/core/kerberos#std-label-security-kerberos), set this to `GSSAPI`.

  If using [X.509](/docs/manual/core/security-x.509#std-label-security-auth-x509), set this to `MONGODB-X.509`.

- set [`--username`](https://www.mongodb.com/docs/mongodb-shell/reference/options/#std-option-mongosh.--username) to a username that respects the [`security.ldap.authz.queryTemplate`](/docs/manual/reference/configuration-options#mongodb-setting-security.ldap.authz.queryTemplate), or any configured [`security.ldap.userToDNMapping`](/docs/manual/reference/configuration-options#mongodb-setting-security.ldap.userToDNMapping) template.

- set [`--password`](https://www.mongodb.com/docs/mongodb-shell/reference/options/#std-option-mongosh.--password) to the appropriate password.

Include the [`--host`](https://www.mongodb.com/docs/mongodb-shell/reference/options/#std-option-mongosh.--host) and [`--port`](https://www.mongodb.com/docs/mongodb-shell/reference/options/#std-option-mongosh.--port) of the MongoDB server, along with any other options relevant to your deployment.

For example, the following operation authenticates to a MongoDB server running with LDAP authentication and authorization:

```bash
mongosh --username alice@dba.example.com --password  --authenticationDatabase '$external' --authenticationMechanism "PLAIN"  --host "mongodb.example.com" --port 27017
```

If you do not specify the password to the [`--password`](https://www.mongodb.com/docs/mongodb-shell/reference/options/#std-option-mongosh.--password) command-line option, [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) prompts for the password.

**Important:**

The `$external` argument must be placed in single quotes, not double quotes, to prevent the shell from interpreting `$external` as a variable.

## MongoDB Roles for LDAP Authorization

MongoDB maps each returned group distinguished name (DN) returned by the LDAP [`query`](/docs/manual/reference/configuration-options#mongodb-setting-security.ldap.authz.queryTemplate) to a [role](/docs/manual/core/authorization#std-label-authorization) on the `admin` database.

If MongoDB acquires a group whose DN **exactly** matches the name of an existing role, MongoDB grants the authenticated user roles and [privileges](/docs/manual/core/authorization#std-label-privileges) associated with that role. If MongoDB cannot map any of the returned groups to a role, MongoDB grants no privileges to the user.

**Note:**

[LDAP](/docs/manual/core/security-ldap#std-label-security-ldap) and [kerberos](/docs/manual/core/kerberos#std-label-security-kerberos) authentication normally require creating users in the `$external` database. If you also use LDAP for authorization, you do *not* need to create users in the `$external` database. You only need to create the appropriate roles in the `admin` database. Users still authenticate against the `$external` database.

**Important:**

If you are using LDAP for authorization and your LDAP group DNs contain [RFC4514](https://tools.ietf.org/html/rfc4514) escaped sequences, the roles you create in the `admin` database must also be escaped following RFC4514.

**Example:**

A database has the following roles configured on the `admin` database:

```javascript
{
    role: "CN=dba,CN=Users,DC=example,DC=com",
    privileges: [],
    roles: [ "dbAdminAnyDatabase", "clusterAdmin" ]
}
{
   role: "CN=analytics,CN=Users,DC=example,DC=com"
   privileges: [],
   roles: [
         { role : "read", db : "web_statistics" },
         { role : "read", db : "user_statistics" }
       ]
}
```

After authenticating a user `alice@dba.example.com` against the `$external` database, the MongoDB server performs a query derived from the configured [`query template`](/docs/manual/reference/configuration-options#mongodb-setting-security.ldap.authz.queryTemplate) to retrieve the groups which include the authenticated user as a member. In this example, the MongoDB server retrieves the following group DNs for the user:

```text
dn:CN=dba,CN=Users,dc=example,dc=com
dn:CN=admin,CN=Users,dc=example,dc=com
```

MongoDB maps these group DNs to roles on the `admin` database. The first group DN matches the first role, and MongoDB grants the authenticated user its roles and privileges. The second group DN does not match to any role on the server, so MongoDB grants no additional permissions.

A new user `bob@analytics.example.com` authenticates against the `$external` database. The MongoDB server repeats the query process, using the provided username in the query template. In this example, the MongoDB server retrieves the following group DNs for the user:

```text
dn:cn=analytics,CN=Users,dc=example,dc=com
```

MongoDB maps these group DNs to roles on the `admin` database and grants the authenticated user the roles and privileges of the second role.

A new user `workstation@guest.example.com` authenticates against the `$external` database. The MongoDB server repeats the query process, using the provided username in the query template. In this example, the MongoDB server retrieves the following group DNs for the user:

```text
dn:cn=guest,CN=Users,dc=example,dc=com
```

MongoDB maps the group to a role on the `admin` database and, because no matching roles exist, grants the user no additional permissions.

## Use LDAP Authorization with Other Authentication Mechanisms

When LDAP authorization is enabled, MongoDB can have different authorization behavior based on your authentication mechanism.

The following mechanisms always use LDAP authorization if enabled:

- X.509

- Kerberos

- LDAP

- OIDC (when the `useAuthorizationClaim` field in [`oidcIdentityProviders`](/docs/manual/reference/parameters#mongodb-parameter-param.oidcIdentityProviders) is `false`)

The following mechanisms use internal authorization, whether LDAP authorization is enabled or not:

- SCRAM

- OIDC (when the `useAuthorizationClaim` field in [`oidcIdentityProviders`](/docs/manual/reference/parameters#mongodb-parameter-param.oidcIdentityProviders) is `true`)
