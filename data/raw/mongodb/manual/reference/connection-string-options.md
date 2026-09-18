> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Connection String Options

This page lists all connection options to connect to your database using SRV connection strings and standard connection strings.

Connection options are pairs in the following form: `name=value`.

- The option `name` is case insensitive when using a driver.

- The option `name` is case insensitive when using [`mongosh`.](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh)

- The `value` is always case sensitive.

Separate options with the ampersand (`&`) character `name1=value1&name2=value2`. In the following example, a connection includes the [`replicaSet`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.replicaSet) and [`connectTimeoutMS`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.connectTimeoutMS) options:

```none
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@db1.example.net:27017,db2.example.net:2500/?replicaSet=test&connectTimeoutMS=300000
```

**Note: Semi-colon separator for connection string arguments**

To provide backwards compatibility, drivers accept semi-colons (`;`) as option separators.

## Replica Set Option

The following connection string connects to a replica set named `myRepl` with members running on the specified hosts. It authenticates as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@db0.example.com:27017,db1.example.com:27017,db2.example.com:27017/?replicaSet=myRepl
```

| Connection Option | Description |
| --- | --- |
|  | Specifies the name of the [replica set](/docs/manual/reference/glossary#std-term-replica-set), if the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) is a member of a replica set. Set the `replicaSet` connection option to ensure consistent behavior across drivers. When connecting to a replica set, provide a [seed list](/docs/manual/reference/glossary#std-term-seed-list) of the replica set members in the `host[:port]` component. See your [driver](https://www.mongodb.com/docs/drivers/) documentation for details. |
|  | Specifies whether the client connects directly to the `host[:port]` in the connection URI: `true`: The client sends operations only to the specified host and does not attempt to discover other replica set members.; `false`: The client attempts to discover all servers in the replica set, and sends operations to the primary member. This is the default value. IMPORTANT: When a replica set runs in Docker, it might expose only one MongoDB endpoint. In this case, the replica set is not discoverable, and specifying `directConnection=false` can prevent your application from connecting to it. In a test or development environment, you can connect to the replica set by specifying `directConnection=true` in your connection URI. In a production environment, we recommend configuring the cluster to make each MongoDB instance accessible outside of the Docker virtual network. |

## Connection Options

### TLS Options

The following connection string to a replica set includes [`tls=true`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.tls) option. It authenticates as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`.

```none
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@db0.example.com,db1.example.com,db2.example.com/?replicaSet=myRepl&tls=true
```

You can also use the equivalent [`ssl=true`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.ssl) option:

```none
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@db0.example.com,db1.example.com,db2.example.com/?replicaSet=myRepl&ssl=true
```

| Connection Option | Description |
| --- | --- |
|  | Enables or disables TLS/SSL for the connection: `true`: Initiates the connection with TLS/SSL. Default for [SRV Connection Format.](/docs/manual/reference/connection-string-formats#std-label-connections-dns-seedlist); `false`: Initiates the connection without TLS/SSL. Default for [Standard Connection String Format.](/docs/manual/reference/connection-string-formats#std-label-connections-standard-connection-string-format) The [`tls`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.tls) option is equivalent to [`ssl`.](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.ssl) If the [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) shell specifies additional [tls/ssl](https://www.mongodb.com/docs/mongodb-shell/reference/options/#std-label-mongosh-ssl) options from the command-line, use the `--tls` command-line option instead. |
|  | Enables or disables TLS/SSL for the connection: `true`: Initiates the connection with TLS/SSL. Default for [SRV Connection Format.](/docs/manual/reference/connection-string-formats#std-label-connections-dns-seedlist); `false`: Initiates the connection without TLS/SSL. Default for [Standard Connection String Format.](/docs/manual/reference/connection-string-formats#std-label-connections-standard-connection-string-format) The [`ssl`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.ssl) option is equivalent to the [`tls`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.tls) option. If the [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) shell specifies additional [tls/ssl](https://www.mongodb.com/docs/mongodb-shell/reference/options/#std-label-mongosh-ssl) options from the command-line, use the `--ssl` command-line option instead. |
|  | Specifies the location of a local `.pem` file that contains either the client's TLS/SSL X.509 certificate or the client's TLS/SSL certificate and key. The client presents this file to the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) / [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instance. [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) / [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) logs a warning on connection if the presented X.509 certificate expires within `30` days of the `mongod/mongos` host system time. This option is not supported by all drivers. Refer to the [Drivers](https://www.mongodb.com/docs/drivers/) documentation. This connection string option is not available for the `mongo` shell. Use the command-line option instead. |
|  | Specifies the password to decrypt the [`tlsCertificateKeyFile`.](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.tlsCertificateKeyFile) This option is not supported by all drivers. Refer to the [Drivers](https://www.mongodb.com/docs/drivers/) documentation. This connection string option is not available for the `mongo` shell. Use the command-line option instead. |
|  | Specifies the path to a local `.pem` file that contains the root certificate chain from the Certificate Authority. The client uses this file to validate the certificate presented by the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) / [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instance. This option is not supported by all drivers. Refer to the [Drivers](https://www.mongodb.com/docs/drivers/) documentation. This connection string option is not available for the `mongo` shell. Use the command-line option instead. |
|  | Bypasses validation of the certificates presented by the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) / [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instance Set to `true` to connect to MongoDB instances even if the server's present invalid certificates. This option is not supported by all drivers. Refer to the [Drivers](https://www.mongodb.com/docs/drivers/) documentation. This connection string option is not available for the `mongo` shell. Use the command-line option instead. WARNING: Disabling certificate validation creates a vulnerability. |
|  | Disables hostname validation of the certificate presented by the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) / [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instance. Set to `true` to connect to MongoDB instances even if the hostname in the server certificates do not match the server's host. This option is not supported by all drivers. Refer to the [Drivers](https://www.mongodb.com/docs/drivers/) documentation. This connection string option is not available for the `mongo` shell. Use the command-line option instead. WARNING: Disabling certificate validation creates a vulnerability. |
|  | Disables various certificate validations. Set to `true` to disable certificate validations. The exact validatations disabled vary by drivers. Refer to the [Drivers](https://www.mongodb.com/docs/drivers/) documentation. This connection string option is not available for the `mongo` shell. Use the command-line option instead. WARNING: Disabling certificate validation creates a vulnerability. |

### Timeout Options

| Connection Option | Description |
| --- | --- |
|  | The time in milliseconds to attempt an operation before timing out. The timeout applies to all steps in an operation, including server selection, connection checkout, and server-side execution. `timeoutMS` has no default value. If you do not specify a value, the driver applies individual timeout options, such as [`socketTimeoutMS`.](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.socketTimeoutMS) If you set `timeoutMS` in the connection string, the driver ignores other timeout options, and the timeout applies to every operation in the client. You can override `timeoutMS` at a more specific level, but you cannot unset the value. To learn more about timeout inheritence, see [Limit Server Execution Time.](https://www.mongodb.com/docs/drivers/node/current/connect/connection-options/csot/#std-label-node-csot) IMPORTANT: `timeoutMS` is not yet supported by all official drivers. For availability, see the [driver](https://www.mongodb.com/docs/drivers/) documentation. |
|  | The time in milliseconds to attempt a connection before timing out. The default is 10,000 milliseconds, but specific drivers might have a different default. For details, see the [driver](https://www.mongodb.com/docs/drivers/) documentation. |
|  | The time in milliseconds to attempt a send or receive on a socket before the attempt times out. The default is no timeout, though different drivers might vary. See the [driver](https://www.mongodb.com/docs/drivers/) documentation. |

### Compression Options

| Connection Option | Description |
| --- | --- |
|  | Comma-delimited string of compressors to enable network compression for communication between this client and a [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) / [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instance. You can specify the following compressors: [snappy](/docs/manual/reference/glossary#std-term-snappy); [zlib](/docs/manual/reference/glossary#std-term-zlib); [zstd](/docs/manual/reference/glossary#std-term-zstd) If you specify multiple compressors, then the order in which you list the compressors matter as well as the communication initiator. For example, if the client specifies the following network compressors `"zlib,snappy"` and the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) specifies `"snappy,zlib"`, messages between the client and the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) uses `zlib`. Messages are compressed only when both parties enable network compression and share a common compressor. Otherwise, messages between the parties are uncompressed. [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) supports the uri connection string option [`compressors`.](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.compressors) |
|  | An integer that specifies the compression level if using [zlib](/docs/manual/reference/glossary#std-term-zlib) for [`network compression`.](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.compressors) You can specify an integer value ranging from `-1` to `9`: ValueNotes`-1`Default compression level, usually level `6` compression.`0`No compression`1` - `9`Increasing level of compression but at the cost of speed, with:`1` providing the best speed but least compression, and; `9` providing the best compression but at the slowest speed. Supported by [`mongosh`.](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) |

## Connection Pool Options

Most drivers implement some kind of connection pool handling. Some drivers do not support connection pools. See your [driver](https://www.mongodb.com/docs/drivers/) documentation for more information on the connection pooling implementation. These options allow applications to configure the connection pool when connecting to the MongoDB deployment.

| Connection Option | Description |
| --- | --- |
|  | The maximum number of connections in the connection pool. The default value is `100`. |
|  | The minimum number of connections in the connection pool. The default value is `0`. The [`minPoolSize`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.minPoolSize) option is not supported by all drivers. For information on your driver, see the [Drivers](https://www.mongodb.com/docs/drivers/) documentation. |
|  | Maximum number of connections a pool can establish concurrently. The default value is `2`. `maxConnecting` is supported for all drivers **except** the [Rust Driver.](https://www.mongodb.com/docs/drivers/rust/current/) Raising the value of `maxConnecting` allows the client to establish connection to the server faster, but increases the chance of [connection storms](/docs/manual/reference/glossary#std-term-connection-storm). If the value of `maxConnecting` is too low, your connection pool may experience heavy throttling and increased tail latency for clients checking out connections. |
|  | The maximum number of milliseconds that a connection can remain idle in the pool before being removed and closed. This option is not supported by all drivers. |
|  | A number that the driver multiplies the [`maxPoolSize`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.maxPoolSize) value by, to provide the maximum number of threads allowed to wait for a connection to become available from the pool. For default values, see the [driver](https://www.mongodb.com/docs/drivers/) documentation. This option is not supported by all drivers. |
|  | The maximum time in milliseconds that a thread can wait for a connection to become available. For default values, see the [driver](https://www.mongodb.com/docs/drivers/) documentation. This option is not supported by all drivers. |

## Write Concern Options

[Write concern](/docs/manual/reference/write-concern#std-label-write-concern) describes the level of acknowledgment requested from MongoDB. These options are supported by:

- MongoDB drivers

- [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh)

- [`mongofiles`](https://www.mongodb.com/docs/database-tools/mongofiles/#mongodb-binary-bin.mongofiles)

- [`mongoimport`](https://www.mongodb.com/docs/database-tools/mongoimport/#mongodb-binary-bin.mongoimport)

- [`mongorestore`](https://www.mongodb.com/docs/database-tools/mongorestore/#mongodb-binary-bin.mongorestore)

You can specify write concern both in the connection string and as a parameter to methods like `insert` or `update`. If specified in both places, the method parameter overrides the connection string.

MongoDB Atlas deployment connection strings use [`"majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) by default. If you don't specify write concern for an MongoDB Atlas deployment, MongoDB Atlas enforces [`"majority"`.](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-)

The following connection string to a replica set specifies [`"majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) write concern and a 5 second timeout using the [`wtimeoutMS`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.wtimeoutMS) write concern parameter:

```none
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@db0.example.com,db1.example.com,db2.example.com/?replicaSet=myRepl&w=majority&wtimeoutMS=5000
```

| Connection Option | Description |
| --- | --- |
|  | Corresponds to the write concern [`w` Option](/docs/manual/reference/write-concern#std-label-wc-w). The `w` option requests acknowledgment that the write operation has propagated to a specified number of [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instances or to [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instances with specified tags. You can specify a [`number`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-number-), the string [`majority`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-), or a [`tag set`.](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-custom-write-concern-name-) For details, see [`w` Option.](/docs/manual/reference/write-concern#std-label-wc-w) |
|  | IMPORTANT: The [`wtimeoutMS`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.wtimeoutMS) option is deprecated. Set [`timeoutMS`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.timeoutMS) instead. [`timeoutMS`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.timeoutMS) overrides [`wtimeoutMS`.](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.wtimeoutMS) Corresponds to the write concern [`wtimeout`](/docs/manual/reference/write-concern#std-label-wc-wtimeout). [`wtimeoutMS`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.wtimeoutMS) specifies a time limit, in milliseconds, for the write concern. When `wtimeoutMS` is `0`, write operations never time out. For more information, see [`wtimeout`.](/docs/manual/reference/write-concern#std-label-wc-wtimeout) |
|  | Corresponds to the write concern [`j` Option](/docs/manual/reference/write-concern#std-label-wc-j) option. The [`journal`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.journal) option requests acknowledgment from MongoDB that the write operation has been written to the [journal](/docs/manual/core/journaling#std-label-journaling-internals). For details, see [`j` Option.](/docs/manual/reference/write-concern#std-label-wc-j) If you set [`journal`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.journal) to `true`, and specify a [`w`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.w) value less than 1, [`journal`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.journal) prevails. |

For more information, see [Write Concern.](/docs/manual/reference/write-concern#std-label-write-concern)

## readConcern Options

For the WiredTiger storage engine, MongoDB introduces the `readConcern` option for replica sets and replica set shards.

[Read Concern](/docs/manual/reference/read-concern) allows clients to choose a level of isolation for their reads from replica sets.

The following connection string to a replica set specifies [`readConcernLevel=majority`:](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.readConcernLevel)

```none
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@db0.example.com,db1.example.com,db2.example.com/?replicaSet=myRepl&readConcernLevel=majority
```

| Connection Option | Description |
| --- | --- |
|  | The level of isolation. Accepts one of the following values: [`local`](/docs/manual/reference/read-concern-local#mongodb-readconcern-readconcern.-local-); [`majority`](/docs/manual/reference/read-concern-majority#mongodb-readconcern-readconcern.-majority-); [`linearizable`](/docs/manual/reference/read-concern-linearizable#mongodb-readconcern-readconcern.-linearizable-); [`available`](/docs/manual/reference/read-concern-available#mongodb-readconcern-readconcern.-available-) This connection string option is not available for [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh). Specify the read concern as an [option to the specific operation.](/docs/manual/reference/read-concern#std-label-read-concern-operations) |

For more information, see [Read Concern.](/docs/manual/reference/read-concern)

## Read Preference Options

[Read preferences](/docs/manual/core/read-preference#std-label-read-preference) describe the behavior of read operations with regards to [replica sets](/docs/manual/reference/glossary#std-term-replica-set). These parameters allow you to specify read preferences on a per-connection basis in the connection string.

For example:

- The following connection string to a replica set specifies [`secondary`](/docs/manual/reference/glossary#std-term-secondary) read preference mode and a [`maxStalenessSeconds`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.maxStalenessSeconds) value of 120 seconds:

  ```none
  mongodb://myDatabaseUser:D1fficultP%40ssw0rd@db0.example.com,db1.example.com,db2.example.com/?replicaSet=myRepl&readPreference=secondary&maxStalenessSeconds=120
  ```

- The following connection string to a sharded cluster specifies [`secondary`](/docs/manual/reference/glossary#std-term-secondary) read preference mode and a [`maxStalenessSeconds`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.maxStalenessSeconds) value of 120 seconds:

  ```none
  mongodb://myDatabaseUser:D1fficultP%40ssw0rd@mongos1.example.com,mongos2.example.com/?readPreference=secondary&maxStalenessSeconds=120
  ```

- The following connection string to a sharded cluster specifies [`secondary`](/docs/manual/reference/glossary#std-term-secondary) read preference mode and three [`readPreferenceTags`:](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.readPreferenceTags)

  ```none
  mongodb://myDatabaseUser:D1fficultP%40ssw0rd@mongos1.example.com,mongos2.example.com/?readPreference=secondary&readPreferenceTags=dc:ny,rack:r1&readPreferenceTags=dc:ny&readPreferenceTags=
  ```

Order matters when using multiple `readPreferenceTags`. The `readPreferenceTags` are tried in order until a match is found. Once found, that specification is used to find all eligible matching members and any remaining `readPreferenceTags`  are ignored. For details, see [Order of Tag Matching.](/docs/manual/core/read-preference-tags#std-label-read-preference-tag-order-matching)

| Connection Option | Description |
| --- | --- |
|  | Specifies the [read preferences](/docs/manual/core/read-preference#std-label-read-preference) for this connection. Possible values are: [`primary`](/docs/manual/reference/glossary#std-term-primary) (*Default*); [`primaryPreferred`](/docs/manual/core/read-preference#mongodb-readmode-primaryPreferred); [`secondary`](/docs/manual/reference/glossary#std-term-secondary); [`secondaryPreferred`](/docs/manual/core/read-preference#mongodb-readmode-secondaryPreferred); [`nearest`](/docs/manual/core/read-preference#mongodb-readmode-nearest) [Transactions](/docs/manual/core/transactions#std-label-transactions) that contain read operations must use read preference [`primary`](/docs/manual/reference/glossary#std-term-primary). All operations in a given transaction must route to the same member. This connection string option is not available for the [`mongo`](/docs/manual/reference/mongo#mongodb-binary-bin.mongo) shell. See [`cursor.readPref()`](/docs/manual/reference/method/cursor.readPref#mongodb-method-cursor.readPref) and [`Mongo.setReadPref()`](/docs/manual/reference/method/Mongo.setReadPref#mongodb-method-Mongo.setReadPref) instead. |
|  | Specifies, in seconds, how stale a secondary can be before the client stops using it for read operations. For details, see [Read Preference `maxStalenessSeconds`.](/docs/manual/core/read-preference-staleness#std-label-replica-set-read-preference-max-staleness) By default, there is no maximum staleness and clients do not consider a secondary's lag when choosing where to direct a read operation. The minimum [`maxStalenessSeconds`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.maxStalenessSeconds) value is 90 seconds. Specifying a value between 0 and 90 seconds produces an error. MongoDB drivers treat a `maxStalenessSeconds` value of `-1` as "no max staleness", the same as if `maxStalenessSeconds` is omitted. |
|  | Specifies the [tags document](/docs/manual/core/read-preference-tags#std-label-replica-set-read-preference-tag-sets) as a comma-separated list of colon-separated key-value pairs. For example, To specify the tags document `{ "dc": "ny", "rack": "r1" }`, use `readPreferenceTags=dc:ny,rack:r1` in the connection string.; To specify an empty tags document `{ }`, use `readPreferenceTags=` without setting the value. To specify a *list* of tag documents, use multiple `readPreferenceTags`. For example, `readPreferenceTags=dc:ny,rack:r1&readPreferenceTags=`. Order matters when using multiple `readPreferenceTags`. The `readPreferenceTags` are tried in order until a match is found. For details, see [Order of Tag Matching.](/docs/manual/core/read-preference-tags#std-label-read-preference-tag-order-matching) This connection string option is not available for the [`mongo`](/docs/manual/reference/mongo#mongodb-binary-bin.mongo) shell. See [`cursor.readPref()`](/docs/manual/reference/method/cursor.readPref#mongodb-method-cursor.readPref) and [`Mongo.setReadPref()`](/docs/manual/reference/method/Mongo.setReadPref#mongodb-method-Mongo.setReadPref) instead. |

For more information, see [Read preferences.](/docs/manual/core/read-preference#std-label-read-preference)

## Authentication Options

The following connection string to a replica set specifies the [`authSource`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.authSource) to the `admin` database. That is, the user credentials are authenticated against the `admin` database.

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@mongodb0.example.com:27017,mongodb1.example.com:27017,mongodb2.example.com:27017/?replicaSet=myRepl&authSource=admin
```

If the username or password includes the following characters, those characters must be converted using [percent encoding:](https://tools.ietf.org/html/rfc3986#section-2.1)

```none
$ : / ? # [ ] @
```

| Connection Option | Description |
| --- | --- |
|  | Database name associated with the user's credentials. Defaults to `defaultauthdb` if specified, otherwise defaults to `admin`. The `PLAIN`, `GSSAPI`, and `MONGODB-AWS` mechanisms require [`authSource`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.authSource) to be set to `$external`, as they delegate credential storage to external services. MongoDB ignores [`authSource`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.authSource) if no username is provided in the connection string or via `--username`. |
| Default: SCRAM-SHA-256 | Authentication mechanism for the connection. Without an explicit `authMechanism`, MongoDB tries SCRAM-SHA-256 and falls back to SCRAM-SHA-1 if that fails. [SCRAM-SHA-1](/docs/manual/core/security-scram#std-label-authentication-scram-sha-1); [SCRAM-SHA-256](/docs/manual/core/security-scram#std-label-authentication-scram-sha-256); [MONGODB-X509](/docs/manual/core/security-x.509#std-label-security-auth-x509); `MONGODB-AWS`; [GSSAPI](/docs/manual/core/authentication#std-label-security-auth-kerberos) (Kerberos); [PLAIN](/docs/manual/core/authentication#std-label-security-auth-ldap) (LDAP SASL); `MONGODB-OIDC` (OpenID Connect OIDC). To use `MONGODB-OIDC`, you must either:Set the [`authMechanismProperties`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.authMechanismProperties) `ENVIRONMENT` variable.; Provide an OIDC callback to the client constructor. Only MongoDB Enterprise [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) and [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instances provide `GSSAPI` (Kerberos) and `PLAIN` (LDAP) mechanisms. To use `MONGODB-X509`, you must have TLS/SSL Enabled. To use `MONGODB-AWS`, you must connect to a [MongoDB Atlas](https://www.mongodb.com/atlas/database) cluster configured to support authentication via [AWS IAM credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html) (an AWS access key ID and a secret access key, and optionally an [AWS session token](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html)). The `MONGODB-AWS` authentication mechanism requires that the [`authSource`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.authSource) be set to `$external`. If the AWS access key ID, secret access key, or session token are defined on your platform by using their respective [AWS IAM environment variables](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html#envvars-list), [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) uses these environment variable values to authenticate automatically. You do not need to specify them in the connection string. There are other methods to provide AWS credentials depending on your deployment environment and security requirements. For example usage of the `MONGODB-AWS` authentication mechanism, see [Connection Strings.](/docs/manual/reference/connection-string#std-label-find-connection-string) See [Authentication on Self-Managed Deployments](/docs/manual/core/authentication) for more information about the authentication system in MongoDB. Also consider [Use X.509 to Authenticate Clients on Self-Managed MongoDB](/docs/manual/tutorial/configure-x509-client-authentication) for more information on x509 authentication. |
|  | Specify properties for the specified [`authMechanism`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.authMechanism) as a comma-separated list of colon-separated key-value pairs. Possible key-value pairs are: `SERVICE_NAME:<string>`Set the Kerberos service name when connecting to Kerberized MongoDB instances. This value must match the service name set on MongoDB instances to which you are connecting. Only valid when using the [GSSAPI](/docs/manual/core/authentication#std-label-security-auth-kerberos) authentication mechanism.`SERVICE_NAME` defaults to `mongodb` for all clients and MongoDB instances. If you change the [`saslServiceName`](/docs/manual/reference/parameters#mongodb-parameter-param.saslServiceName) setting on a MongoDB instance, you must set `SERVICE_NAME` to match that setting. Only valid when using the [GSSAPI](/docs/manual/core/authentication#std-label-security-auth-kerberos) authentication mechanism.`CANONICALIZE_HOST_NAME:true|false`Canonicalize the hostname of the client host machine when connecting to the Kerberos server. This may be required when hosts report different hostnames than what is in the Kerberos database. Defaults to `false`. Only valid when using the [GSSAPI](/docs/manual/core/authentication#std-label-security-auth-kerberos) authentication mechanism.`SERVICE_REALM:<string>`Set the Kerberos realm for the MongoDB service. This may be necessary to support cross-realm authentication where the user exists in one realm and the service in another. Only valid when using the [GSSAPI](/docs/manual/core/authentication#std-label-security-auth-kerberos) authentication mechanism.`AWS_SESSION_TOKEN:<security_token>`Set the AWS session token for authentication with temporary credentials when using an [AssumeRole](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html) request, or when working with AWS resources that specify this value such as Lambda. Only valid when using the `MONGODB-AWS` authentication mechanism. You must have an AWS access key ID and a secret access key as well. For example usage, see [Connection Strings.](/docs/manual/reference/connection-string#std-label-find-connection-string)`ENVIRONMENT:<string>`Set the OpenID Connect (OIDC) environment. For:Microsoft Azure, set `ENVIRONMENT:azure`; Google Cloud Platform, set `ENVIRONMENT:gcp`You must also set [`authMechanism`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.authMechanism) to `MONGODB-OIDC`. |
|  | Set the Kerberos service name when connecting to Kerberized MongoDB instances. This value must match the service name set on MongoDB instances to which you are connecting. [`gssapiServiceName`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.gssapiServiceName) defaults to `mongodb` for all clients and MongoDB instances. If you change [`saslServiceName`](/docs/manual/reference/parameters#mongodb-parameter-param.saslServiceName) setting on a MongoDB instance, you must set [`gssapiServiceName`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.gssapiServiceName) to match that setting. [`gssapiServiceName`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.gssapiServiceName) is a deprecated aliases for [`authMechanismProperties=SERVICE_NAME:mongodb`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.authMechanismProperties). For more information on which options your driver supports and their relative priority to each other, reference the documentation for your preferred driver version. |

## Server Selection and Discovery Options

MongoDB provides the following options to configure how MongoDB drivers and [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instances select a server to which to direct read or write operations.

| Connection Option | Description |
| --- | --- |
|  | The size (in milliseconds) of the latency window for selecting among multiple suitable MongoDB instances. *Default*: 15 milliseconds. All drivers use [`localThresholdMS`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.localThresholdMS). Use the `localThreshold` alias when specifying the latency window size to [`mongos`.](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) |
|  | Specifies how long (in milliseconds) to block for server selection before throwing an exception. *Default*: 30,000 milliseconds. |
|  | **Single-threaded drivers only**. When `true`, the driver scans the MongoDB deployment exactly once after server selection fails and then either selects a server or raises an error. When `false`, the driver blocks and searches for a server up to the [`serverSelectionTimeoutMS`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.serverSelectionTimeoutMS) value. *Default*: `true`. Multi-threaded drivers and [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) do not support [`serverSelectionTryOnce`.](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.serverSelectionTryOnce) |
|  | [`heartbeatFrequencyMS`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.heartbeatFrequencyMS) controls when the driver checks the state of the MongoDB deployment. Specify the interval (in milliseconds) between checks, counted from the end of the previous check until the beginning of the next one. *Default*: Single-threaded drivers: 60 seconds.; Multi-threaded drivers: 10 seconds. [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) does not support changing the frequency of the heartbeat checks. |
|  | **Single-threaded clients only**. Controls how often the client checks the state of the TCP connection to the MongoDB deployment. If you specify a lower value, the client detects network issues faster but uses more CPU. *Default*: 5 seconds. This option is not supported by all drivers. Refer to the [Drivers](https://www.mongodb.com/docs/drivers/) documentation. |

## Miscellaneous Configuration

| Connection Option | Description |
| --- | --- |
|  | Specify a custom app name. The app name appears in: [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) and [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) [logs](/docs/manual/reference/log-messages#std-label-log-messages-ref); the [`currentOp.appName`](/docs/manual/reference/command/currentOp#mongodb-data-currentOp.appName) field in the [`currentOp`](/docs/manual/reference/command/currentOp#mongodb-dbcommand-dbcmd.currentOp) command and [`db.currentOp()`](/docs/manual/reference/method/db.currentOp#mongodb-method-db.currentOp) method output; the [`system.profile.appName`](/docs/manual/reference/database-profiler#mongodb-data-system.profile.appName) field in the [database profiler](/docs/manual/reference/database-profiler#std-label-profiler) output The [`appName`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.appName) connection option is available for: [MongoDB Drivers](https://www.mongodb.com/docs/drivers/); [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) starting in `mongosh` 1.1.9; [MongoDB Compass](https://www.mongodb.com/docs/compass/current/) starting in Compass 1.28.4 |
|  | Enables [retryable reads.](/docs/manual/core/retryable-reads#std-label-retryable-reads) Possible values are: `true`. Enables retryable reads for the connection.Official MongoDB drivers default to `true`.; `false`. Disables retryable reads for the connection. [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) does not support retryable reads. |
|  | Enable [retryable writes.](/docs/manual/core/retryable-writes#std-label-retryable-writes) Possible values are: `true`. Enables retryable writes for the connection.Official MongoDB drivers default to `true`.; `false`. Disables retryable writes for the connection. MongoDB drivers retry [transaction commit and abort operations](/docs/manual/core/transactions-in-applications#std-label-transactions-retry) regardless of the value of [`retryWrites`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.retryWrites). For more information on transaction retryability, see [Transaction Error Handling.](/docs/manual/core/transactions-in-applications#std-label-transactions-retry) |
|  | Possible values are: `standard`The standard binary representation.`csharpLegacy`The default representation for the .NET/C# driver.`javaLegacy`The default representation for the Java driver.`pythonLegacy`The default representation for the Python driver. For the default, see the [Drivers](https://www.mongodb.com/docs/drivers/) documentation for your driver. Not all drivers support the [`uuidRepresentation`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.uuidRepresentation) option. For information on your driver, see the [drivers](https://www.mongodb.com/docs/drivers/) documentation. |
|  | Specifies whether the client is connecting to a load balancer. This option is `false` by default. You can set this option to `true` only if you meet the following requirements: You specify only one host name.; You aren't connecting to a replica set.; The [`srvMaxHosts`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.srvMaxHosts) option is unset or has a value of `0`.; The [`directConnection`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.directConnection) option is unset or has a value of `false`. |
|  | Specifies the number of [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) connections that can be created for sharded topologies. Set this option to a non-negative integer. `0` is the default value and means there is no limit on the number of [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) connections. |
