> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Connection String Formats

You can specify the MongoDB connection string by using one of the following formats:

- [SRV Connection Format](/docs/manual/reference/connection-string-formats#std-label-connections-dns-seedlist): A connection string with a hostname that corresponds to a DNS SRV record. Your driver or [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) queries the record to determine which hosts are running the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) or [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instances.

- [Standard Connection String Format](/docs/manual/reference/connection-string-formats#std-label-connections-standard-connection-string-format): A connection string that specifies all hosts that are running the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) or [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instances.

MongoDB Atlas clusters use SRV connection format unless you connect to an [online archive.](https://www.mongodb.com/docs/atlas/online-archive/manage-online-archive/)

To connect directly to a host and port specified in a connection string, set the [`directConnection`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.directConnection) option to `true`. For full details about `directConnection` and the other connection string options, see [Connection String Options.](/docs/manual/reference/connection-string-options#std-label-connections-connection-options)

## SRV Connection Format

MongoDB supports a DNS (Domain Name Service)-constructed [seed list](/docs/manual/reference/glossary#std-term-seed-list). Using DNS to construct the available servers list allows more flexibility of deployment and the ability to change the servers in rotation without reconfiguring clients.

The SRV URI connection scheme has the following form:

```none
mongodb+srv://[username:password@]host[/[defaultauthdb][?options]]
```

### Connection String Components

A connection string includes the following components:

| Component | Description |
| --- | --- |
| `mongodb://` or `mongodb+srv://` | A required prefix to identify that this is a string in the standard connection format (`mongodb://`) or SRV connection format (`mongodb+srv://`). To learn more about each format, see [Standard Connection String Format](/docs/manual/reference/connection-string-formats#std-label-connections-standard-connection-string-format) and [SRV Connection Format.](/docs/manual/reference/connection-string-formats#std-label-connections-dns-seedlist) |
| `username:password@` | Optional. Authentication credentials. If specified, the client will attempt to authenticate the user to the [`authSource`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.authSource). If [`authSource`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.authSource) is unspecified, the client will attempt to authenticate the user to the `defaultauthdb`. And if the `defaultauthdb` is unspecified, to the `admin` database. If the username or password includes the following characters, those characters must be converted using [percent encoding:](https://tools.ietf.org/html/rfc3986#section-2.1) `$ : / ? # [ ] @` See also [`authSource`.](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.authSource) |
| `host[:port]` | The host (and optional port number) where the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instance (or [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instance for a sharded cluster) is running. You can specify a hostname, IP address, or UNIX domain socket. Specify as many hosts as appropriate for your deployment topology: For a standalone, specify the hostname of the standalone [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instance.; For a replica set, specify the hostname(s) of the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instance(s) as listed in the replica set configuration.; For a sharded cluster, specify the hostname(s) of the [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instance(s). If the port number is not specified, the default port `27017` is used. If you use the SRV URI connection format, you can specify only one host and no port. Otherwise, the driver or [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) raises a parse error and does not perform DNS resolution. |
| `/defaultauthdb` | Optional. The authentication database to use if the connection string includes `username:password@` authentication credentials but the [`authSource`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.authSource) option is unspecified. If both [`authSource`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.authSource) and `defaultauthdb` are unspecified, the client will attempt to authenticate the specified user to the `admin` database. For more information, see [`authSource`.](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.authSource) IMPORTANT: For Atlas deployments using the [SRV Connection Format](/docs/manual/reference/connection-string-formats#std-label-connections-dns-seedlist), `authSource` is automatically set to `admin` in the `TXT` DNS record. For more information about connecting to Atlas deployments, see [Connect to an Atlas Cluster.](https://www.mongodb.com/docs/atlas/connect-to-database-deployment/#std-label-atlas-connect-to-deployment) |
| `?<options>` | Optional. A query string that specifies connection specific options as `<name>=<value>` pairs. See [Connection String Options](/docs/manual/reference/connection-string-options#std-label-connections-connection-options) for a full description of these options. If the connection string does not specify a database/ you must specify a slash (`/`) between the last `host` and the question mark (`?`) that begins the string of options. |

To use the DNS seed list, use the [standard connection string](/docs/manual/reference/connection-string-formats#std-label-connections-standard-connection-string-format) syntax with a prefix of `mongodb+srv` instead of the standard `mongodb`. The `+srv` indicates to the client that the hostname that follows corresponds to a DNS SRV record. The driver or [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) queries the DNS for the record and uses the record to determine which hosts run the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) or [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instances.

**Note:**

The `+srv` connection string modifier automatically sets [`tls`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.tls), or the equivalent [`ssl`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.ssl) option, to `true`. To override this behavior, explicitly set [`tls`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.tls) or [`ssl`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.ssl) to `false` in the connection query string.

When using the `+srv` format, you must specify the `hostname`, `domain`, and `top-level domain (TLD)` in the following format: `<hostname>.<domain>.<TLD>.` This table shows how the placeholders correspond to example values:

| Placeholder | Example |
| --- | --- |
| `<hostname>` | `server` |
| `<domain>` | `example` |
| `<TLD>` | `com` |
| `<hostname>.<domain>.<TLD>` | `server.example.com` |

This example shows a DNS [seed list](/docs/manual/reference/glossary#std-term-seed-list) connection string that correctly uses the `<hostname>.<domain>.<TLD>` format. It authenticates as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

```none
mongodb+srv://myDatabaseUser:D1fficultP%40ssw0rd@server.example.com/
```

The corresponding DNS configuration resembles:

```none
Record                            TTL   Class    Priority Weight Port  Target
_mongodb._tcp.server.example.com. 86400 IN SRV   0        5      27317 mongodb1.example.com.
_mongodb._tcp.server.example.com. 86400 IN SRV   0        5      27017 mongodb2.example.com.
```

Individual SRV records must be in `_mongodb._tcp.<hostname>.<domain>.<TLD>` format.

When a client connects to a member of the [seed list](/docs/manual/reference/glossary#std-term-seed-list), the client retrieves a list of replica set members it can connect to. Clients often use DNS aliases in their seed lists, which means the host may return a server list that differs from the original seed list. If this happens, clients use the hostnames provided by the replica set rather than the hostnames listed in the seed list to ensure that replica set members can be reached via the hostnames in the resulting replica set config.

**Important:**

The hostnames returned in SRV records must share the same parent domain (in this example, `example.com`) as the given hostname. If the parent domains and hostname do not match, you can't connect.

Like the standard connection string, the DNS seed list connection string supports specifying options as a query string. With a DNS seed list connection string, you can also specify the following options via a TXT record:

- `replicaSet`

- `authSource`

You can only specify one TXT record per [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instance. If multiple TXT records appear in the DNS or if the TXT record contains an option other than `replicaSet` or `authSource`, the client returns an error.

The TXT record for the `server.example.com` DNS entry resembles the following example:

```none
Record              TTL   Class    Text
server.example.com. 86400 IN TXT   "replicaSet=mySet&authSource=authDB"
```

Taken together, the DNS SRV records and the options specified in the TXT record resolve to the following standard format connection string:

```none
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@mongodb1.example.com:27317,mongodb2.example.com:27017/?replicaSet=mySet&authSource=authDB
```

To override TXT record options, specify the option in the query string. The following example overrides the `authSource` option configured in the TXT record of the previous DNS entry:

```none
mongodb+srv://myDatabaseUser:D1fficultP%40ssw0rd@server.example.com/?connectTimeoutMS=300000&authSource=aDifferentAuthDB
```

Given the override for the `authSource`, the equivalent connection string in the standard format would resemble the following example:

```none
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@mongodb1.example.com:27317,mongodb2.example.com:27017/?connectTimeoutMS=300000&replicaSet=mySet&authSource=aDifferentAuthDB
```

**Note:**

The `mongodb+srv` option fails if there is no available DNS with records that correspond to the hostname identified in the connection string. If you use the `+srv` connection string modifier, the [`tls`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.tls) (or the equivalent [`ssl`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.ssl)) option is set to `true` for the connection. To override this behavior, explicitly set [`tls`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.tls) or [`ssl`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.ssl) to `false` in the connection query string.

To connect [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) to a replica set using the DNS seed list format, see [mongosh Connection Options.](https://www.mongodb.com/docs/mongodb-shell/reference/options/#std-label-example-connect-mongosh-using-srv)

## Standard Connection String Format

This section describes the standard format of the MongoDB connection URI used to connect to a self-hosted MongoDB standalone deployment, replica set, or sharded cluster.

The standard URI connection scheme has the form:

```none
mongodb://[username:password@]host1[:port1][,...hostN[:portN]][/[defaultauthdb][?options]]
```

### Connection String Database Options

You can specify an authentication database either in the [`authSource`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.authSource) connection option or in the `[/defaultauthdb]` field in the connection string. If you specify [`authSource`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.authSource), the client uses that database to verify your identity and credentials. If you do not specify [`authSource`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.authSource), the client uses `[/defaultauthdb]` as the authentication database. If both [`authSource`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.authSource) and `[/defaultauthdb]` are unspecified, the client authenticates against the `admin` database.

**Note:**

In [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh), `[/defaultauthdb]` also sets the default database. If you do not specify a default database in the connection string, [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) uses the `test` database as the default. Other MongoDB tools, such as the drivers, may handle this field differently. To learn about behavior for a specific driver, see [the drivers documentation.](https://www.mongodb.com/docs/drivers/)

The following example connection string sets the default database to `myDefaultDB` and the authentication database to `admin`:

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@mongodb0.example.com:27017/myDefaultDB?authSource=admin
```

### Connection String Components

A connection string includes the following components:

| Component | Description |
| --- | --- |
| `mongodb://` or `mongodb+srv://` | A required prefix to identify that this is a string in the standard connection format (`mongodb://`) or SRV connection format (`mongodb+srv://`). To learn more about each format, see [Standard Connection String Format](/docs/manual/reference/connection-string-formats#std-label-connections-standard-connection-string-format) and [SRV Connection Format.](/docs/manual/reference/connection-string-formats#std-label-connections-dns-seedlist) |
| `username:password@` | Optional. Authentication credentials. If specified, the client will attempt to authenticate the user to the [`authSource`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.authSource). If [`authSource`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.authSource) is unspecified, the client will attempt to authenticate the user to the `defaultauthdb`. And if the `defaultauthdb` is unspecified, to the `admin` database. If the username or password includes the following characters, those characters must be converted using [percent encoding:](https://tools.ietf.org/html/rfc3986#section-2.1) `$ : / ? # [ ] @` See also [`authSource`.](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.authSource) |
| `host[:port]` | The host (and optional port number) where the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instance (or [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instance for a sharded cluster) is running. You can specify a hostname, IP address, or UNIX domain socket. Specify as many hosts as appropriate for your deployment topology: For a standalone, specify the hostname of the standalone [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instance.; For a replica set, specify the hostname(s) of the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instance(s) as listed in the replica set configuration.; For a sharded cluster, specify the hostname(s) of the [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instance(s). If the port number is not specified, the default port `27017` is used. If you use the SRV URI connection format, you can specify only one host and no port. Otherwise, the driver or [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) raises a parse error and does not perform DNS resolution. |
| `/defaultauthdb` | Optional. The authentication database to use if the connection string includes `username:password@` authentication credentials but the [`authSource`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.authSource) option is unspecified. If both [`authSource`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.authSource) and `defaultauthdb` are unspecified, the client will attempt to authenticate the specified user to the `admin` database. For more information, see [`authSource`.](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.authSource) IMPORTANT: For Atlas deployments using the [SRV Connection Format](/docs/manual/reference/connection-string-formats#std-label-connections-dns-seedlist), `authSource` is automatically set to `admin` in the `TXT` DNS record. For more information about connecting to Atlas deployments, see [Connect to an Atlas Cluster.](https://www.mongodb.com/docs/atlas/connect-to-database-deployment/#std-label-atlas-connect-to-deployment) |
| `?<options>` | Optional. A query string that specifies connection specific options as `<name>=<value>` pairs. See [Connection String Options](/docs/manual/reference/connection-string-options#std-label-connections-connection-options) for a full description of these options. If the connection string does not specify a database/ you must specify a slash (`/`) between the last `host` and the question mark (`?`) that begins the string of options. |

## Learn More

For more connection string examples, see [Connection Strings.](/docs/manual/reference/connection-string#std-label-find-connection-string)
