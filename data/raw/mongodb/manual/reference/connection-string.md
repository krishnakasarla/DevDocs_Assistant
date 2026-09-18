> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Connection Strings

You can use connection strings to define connections between MongoDB instances and the following destinations:

- Your applications when you connect using [drivers.](https://www.mongodb.com/docs/drivers/)

- Tools such as [MongoDB Compass](https://www.mongodb.com/docs/compass/current/) and [MongoDB Shell (mongosh).](https://www.mongodb.com/docs/mongodb-shell/)

To connect to your cluster, you can use one of these connection string formats:

- **SRV connection strings** use the `mongodb+srv://` prefix to simplify connecting to a cluster.  SRV connection strings automatically include all seed list hosts, which supports server rotation without client reconfiguration. When possible, use SRV connection strings over standard connection strings.

- **Standard connection strings** use the `mongodb://` prefix and require you to include all cluster members in replica sets and sharded clusters.

Use the selectors at the top of the page to choose your deployment type and connection string format. Complete the following steps to find your connection string.

## Find Your MongoDB Atlas Connection String

To find your MongoDB Atlas connection string using the [Atlas CLI](https://www.mongodb.com/docs/atlas/cli/current/), [install](https://www.mongodb.com/docs/atlas/cli/current/install-atlas-cli/) and [connect](https://www.mongodb.com/docs/atlas/cli/current/connect-atlas-cli/) from the Atlas CLI, then run the following command. Replace `<clusterName>` with the name of the MongoDB Atlas cluster and replace `<projectId>` with the project ID.

```text
atlas clusters connectionStrings describe <clusterName>
--projectId <projectId>
```

Your MongoDB Atlas connection string resembles the following example:

```bash
mongodb+srv://myDatabaseUser:D1fficultP%40ssw0rd@cluster0.example.mongodb.net/?retryWrites=true&w=majority
```

To learn more, see [atlas clusters connectionStrings describe.](https://www.mongodb.com/docs/atlas/cli/current/command/atlas-clusters-connectionStrings-describe/)

## Atlas Cluster that Authenticates with AWS IAM Credentials

The following example connects to an Atlas cluster that has been configured to support authentication via [AWS IAM credentials:](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html)

```bash
mongodb+srv://<aws access key id>:<aws secret access key>@cluster0.example.com/testdb?authSource=$external&authMechanism=MONGODB-AWS
```

Connecting to Atlas using AWS IAM credentials in this manner uses the `MONGODB-AWS` [`authentication mechanism`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.authMechanism) and the `$external` [`authSource`.](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.authSource)

If you use an [AWS session token](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html), specify an `AWS_SESSION_TOKEN` in the [`authMechanismProperties`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.authMechanismProperties) value, as shown in the following example:

```bash
mongodb+srv://<aws access key id>:<aws secret access key>@cluster0.example.com/testdb?authSource=$external&authMechanism=MONGODB-AWS&authMechanismProperties=AWS_SESSION_TOKEN:<aws session token>
```

**Note:**

If the AWS access key ID, the secret access key, or the session token include the following characters:

```none
$ : / ? # [ ] @
```

those characters must be converted using [percent encoding.](https://tools.ietf.org/html/rfc3986#section-2.1)

You can also set these credentials on your platform using standard [AWS IAM environment variables](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html#envvars-list). [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) checks for the following environment variables when you use the `MONGODB-AWS` [`authentication mechanism`:](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.authMechanism)

- `AWS_ACCESS_KEY_ID`

- `AWS_SECRET_ACCESS_KEY`

- `AWS_SESSION_TOKEN`

If set, these credentials do not need to be specified in the connection string.

The following example sets these environment variables in the `bash` shell:

```bash
export AWS_ACCESS_KEY_ID='<aws access key id>'
export AWS_SECRET_ACCESS_KEY='<aws secret access key>'
export AWS_SESSION_TOKEN='<aws session token>'
```

Syntax for setting environment variables in other shells will be different. Consult the documentation for your platform for more information.

To verify that these environment variables have been set, run the following command:

```none
env | grep AWS
```

Once set, the following example connects to an Atlas cluster using these environment variables:

```bash
mongodb+srv://cluster0.example.com/testdb?authSource=$external&authMechanism=MONGODB-AWS
```

## Find Your MongoDB Atlas Connection String

To find your MongoDB Atlas connection string in the Atlas UI, follow these steps:

1. In the MongoDB Atlas UI, go to the Clusters page for your project.

   If it's not already displayed, select the organization that contains your desired project from the  Organizations menu in the navigation bar.

   If it's not already displayed, select your project from the Projects menu in the navigation bar.

   In the sidebar, click Clusters under the Database heading.

   The [Clusters](https://cloud.mongodb.com/go?l=https%3A%2F%2Fcloud.mongodb.com%2Fv2%2F%3Cproject%3E%23%2Fclusters) page displays.

2. Open the Connection Method dialog.

   Click Connect for the cluster to which you want to connect.

   Click Choose a Connection Method. MongoDB Atlas selects Standard Connection by default. To connect using a [private endpoint](https://www.mongodb.com/docs/atlas/security-private-endpoint/), select Private Endpoint.

3. Choose a connection method.

   To connect to your application, click Drivers. To connect using tools, click the tool you want to use to access your data.

4. Follow instructions for the connection method you selected.

   If you selected Drivers, select your driver and version. If you selected a tool, download the tool.

   Select Connect To Cluster.

   Copy the connection string. Replace `<password>` and `<username>` in the connection string with the database user's credentials.

Your MongoDB Atlas connection string resembles the following example:

```bash
mongodb+srv://myDatabaseUser:D1fficultP%40ssw0rd@cluster0.example.mongodb.net/?retryWrites=true&w=majority
```

## Atlas Cluster that Authenticates with AWS IAM Credentials

The following example connects to an Atlas cluster that has been configured to support authentication via [AWS IAM credentials:](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html)

```bash
mongodb+srv://<aws access key id>:<aws secret access key>@cluster0.example.com/testdb?authSource=$external&authMechanism=MONGODB-AWS
```

Connecting to Atlas using AWS IAM credentials in this manner uses the `MONGODB-AWS` [`authentication mechanism`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.authMechanism) and the `$external` [`authSource`.](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.authSource)

If you use an [AWS session token](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html), specify an `AWS_SESSION_TOKEN` in the [`authMechanismProperties`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.authMechanismProperties) value, as shown in the following example:

```bash
mongodb+srv://<aws access key id>:<aws secret access key>@cluster0.example.com/testdb?authSource=$external&authMechanism=MONGODB-AWS&authMechanismProperties=AWS_SESSION_TOKEN:<aws session token>
```

**Note:**

If the AWS access key ID, the secret access key, or the session token include the following characters:

```none
$ : / ? # [ ] @
```

those characters must be converted using [percent encoding.](https://tools.ietf.org/html/rfc3986#section-2.1)

You can also set these credentials on your platform using standard [AWS IAM environment variables](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html#envvars-list). [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) checks for the following environment variables when you use the `MONGODB-AWS` [`authentication mechanism`:](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.authMechanism)

- `AWS_ACCESS_KEY_ID`

- `AWS_SECRET_ACCESS_KEY`

- `AWS_SESSION_TOKEN`

If set, these credentials do not need to be specified in the connection string.

The following example sets these environment variables in the `bash` shell:

```bash
export AWS_ACCESS_KEY_ID='<aws access key id>'
export AWS_SECRET_ACCESS_KEY='<aws secret access key>'
export AWS_SESSION_TOKEN='<aws session token>'
```

Syntax for setting environment variables in other shells will be different. Consult the documentation for your platform for more information.

To verify that these environment variables have been set, run the following command:

```none
env | grep AWS
```

Once set, the following example connects to an Atlas cluster using these environment variables:

```bash
mongodb+srv://cluster0.example.com/testdb?authSource=$external&authMechanism=MONGODB-AWS
```

## Find Your Self-Hosted Deployment's Connection String

If you are connected to your self-hosted MongoDB deployment, run [`db.getMongo()`](/docs/manual/reference/method/db.getMongo#mongodb-method-db.getMongo) method to return the connection string.

If you are not connected to your deployment, you can determine your connection string based on the connection string format and options you want to use.

The following replica set connection string includes these elements:

- The hostnames of the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instance(s) as listed in the replica set configuration.

- Authentication as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`.

```bash
mongodb+srv://myDatabaseUser:D1fficultP%40ssw0rd@mongodb0.example.com/?authSource=admin&replicaSet=myRepl
```

If the username or password includes the following characters, those characters must be converted using [percent encoding:](https://tools.ietf.org/html/rfc3986#section-2.1)

```none
$ : / ? # [ ] @
```

## Additional Connection String Examples

The following examples show connection strings for common connection targets.

### admin Database Running Locally

The following example connects and logs in to the `admin` database as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@localhost
```

### records Database Running Locally

The following example connects and logs in to the `records` database as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@localhost/records
```

### UNIX Domain Socket

When you connect to a UNIX domain socket, use a URL-encoded connection string.

The following example connects to a UNIX domain socket with file path `/tmp/mongodb-27017.sock` as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@%2Ftmp%2Fmongodb-27017.sock
```

### Replica Set with Members on Different Hosts

The following example connects to a [replica set](/docs/manual/reference/glossary#std-term-replica-set) with two members, one on `db1.example.net` and the other on `db2.example.net`, as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

**Note:**

For a replica set, specify the hostname(s) of the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instance(s) as listed in the replica set configuration.

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@db1.example.net,db2.example.com/?replicaSet=test
```

### Replica Set with Members on localhost

The following example connects to a replica set with three members running on `localhost` on ports `27017`, `27018`, and `27019` as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@localhost:27017,localhost:27018,localhost:27019/?replicaSet=myRepl
```

### Replica Set with Read Distribution

The following example connects to a replica set with three members and distributes reads to the [secondaries](/docs/manual/reference/glossary#std-term-secondary) as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@mongodb0.example.com:27017,mongodb1.example.com:27017,mongodb2.example.com:27017/?replicaSet=myRepl&readPreference=secondary
```

### Replica Set with a High Level of Write Concern

The following example connects to a replica set with write concern configured to wait for replication to succeed across a majority of the data-bearing voting members, with a two-second timeout. It authenticates as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`.

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@mongodb0.example.com:27017,mongodb1.example.com:27017,mongodb2.example.com:27017/?replicaSet=myRepl&w=majority&wtimeoutMS=2000
```

### Sharded Cluster

The following example connects to a sharded cluster with three [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instances as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@router1.example.com:27017,router2.example2.com:27017,router3.example3.com:27017/
```

## Find Your Self-Hosted Deployment's Connection String

If you are connected to your self-hosted MongoDB deployment, run [`db.getMongo()`](/docs/manual/reference/method/db.getMongo#mongodb-method-db.getMongo) method to return the connection string.

If you are not connected to your deployment, you can determine your connection string based on the connection string format and options you want to use.

The following replica set connection string includes these elements:

- The hostnames of the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instance(s) as listed in the replica set configuration.

- Authentication as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`.

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@mongodb0.example.com:27017,mongodb1.example.com:27017,mongodb2.example.com:27017/?authSource=admin&replicaSet=myRepl
```

If the username or password includes the following characters, those characters must be converted using [percent encoding:](https://tools.ietf.org/html/rfc3986#section-2.1)

```none
$ : / ? # [ ] @
```

## Additional Connection String Examples

The following examples show connection strings for common connection targets.

### admin Database Running Locally

The following example connects and logs in to the `admin` database as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@localhost
```

### records Database Running Locally

The following example connects and logs in to the `records` database as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@localhost/records
```

### UNIX Domain Socket

When you connect to a UNIX domain socket, use a URL-encoded connection string.

The following example connects to a UNIX domain socket with file path `/tmp/mongodb-27017.sock` as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@%2Ftmp%2Fmongodb-27017.sock
```

### Replica Set with Members on Different Hosts

The following example connects to a [replica set](/docs/manual/reference/glossary#std-term-replica-set) with two members, one on `db1.example.net` and the other on `db2.example.net`, as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

**Note:**

For a replica set, specify the hostname(s) of the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instance(s) as listed in the replica set configuration.

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@db1.example.net,db2.example.com/?replicaSet=test
```

### Replica Set with Members on localhost

The following example connects to a replica set with three members running on `localhost` on ports `27017`, `27018`, and `27019` as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@localhost:27017,localhost:27018,localhost:27019/?replicaSet=myRepl
```

### Replica Set with Read Distribution

The following example connects to a replica set with three members and distributes reads to the [secondaries](/docs/manual/reference/glossary#std-term-secondary) as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@mongodb0.example.com:27017,mongodb1.example.com:27017,mongodb2.example.com:27017/?replicaSet=myRepl&readPreference=secondary
```

### Replica Set with a High Level of Write Concern

The following example connects to a replica set with write concern configured to wait for replication to succeed across a majority of the data-bearing voting members, with a two-second timeout. It authenticates as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`.

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@mongodb0.example.com:27017,mongodb1.example.com:27017,mongodb2.example.com:27017/?replicaSet=myRepl&w=majority&wtimeoutMS=2000
```

### Sharded Cluster

The following example connects to a sharded cluster with three [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instances as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@router1.example.com:27017,router2.example2.com:27017,router3.example3.com:27017/
```

## Find Your Self-Hosted Deployment's Connection String

If you are connected to your self-hosted MongoDB deployment, run [`db.getMongo()`](/docs/manual/reference/method/db.getMongo#mongodb-method-db.getMongo) method to return the connection string.

If you are not connected to your deployment, you can determine your connection string based on the connection string format and options you want to use.

The following sharded cluster connection string includes these elements:

- The hostnames of the [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instances of the sharded cluster.

- Authentication as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`.

```bash
mongodb+srv://myDatabaseUser:D1fficultP%40ssw0rd@mongos0.example.com/?authSource=admin
```

If the username or password includes the following characters, those characters must be converted using [percent encoding:](https://tools.ietf.org/html/rfc3986#section-2.1)

```none
$ : / ? # [ ] @
```

## Additional Connection String Examples

The following examples show connection strings for common connection targets.

### admin Database Running Locally

The following example connects and logs in to the `admin` database as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@localhost
```

### records Database Running Locally

The following example connects and logs in to the `records` database as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@localhost/records
```

### UNIX Domain Socket

When you connect to a UNIX domain socket, use a URL-encoded connection string.

The following example connects to a UNIX domain socket with file path `/tmp/mongodb-27017.sock` as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@%2Ftmp%2Fmongodb-27017.sock
```

### Replica Set with Members on Different Hosts

The following example connects to a [replica set](/docs/manual/reference/glossary#std-term-replica-set) with two members, one on `db1.example.net` and the other on `db2.example.net`, as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

**Note:**

For a replica set, specify the hostname(s) of the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instance(s) as listed in the replica set configuration.

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@db1.example.net,db2.example.com/?replicaSet=test
```

### Replica Set with Members on localhost

The following example connects to a replica set with three members running on `localhost` on ports `27017`, `27018`, and `27019` as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@localhost:27017,localhost:27018,localhost:27019/?replicaSet=myRepl
```

### Replica Set with Read Distribution

The following example connects to a replica set with three members and distributes reads to the [secondaries](/docs/manual/reference/glossary#std-term-secondary) as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@mongodb0.example.com:27017,mongodb1.example.com:27017,mongodb2.example.com:27017/?replicaSet=myRepl&readPreference=secondary
```

### Replica Set with a High Level of Write Concern

The following example connects to a replica set with write concern configured to wait for replication to succeed across a majority of the data-bearing voting members, with a two-second timeout. It authenticates as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`.

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@mongodb0.example.com:27017,mongodb1.example.com:27017,mongodb2.example.com:27017/?replicaSet=myRepl&w=majority&wtimeoutMS=2000
```

### Sharded Cluster

The following example connects to a sharded cluster with three [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instances as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@router1.example.com:27017,router2.example2.com:27017,router3.example3.com:27017/
```

## Find Your Self-Hosted Deployment's Connection String

If you are connected to your self-hosted MongoDB deployment, run [`db.getMongo()`](/docs/manual/reference/method/db.getMongo#mongodb-method-db.getMongo) method to return the connection string.

If you are not connected to your deployment, you can determine your connection string based on the connection string format and options you want to use.

The following sharded cluster connection string includes these elements:

- The hostnames of the [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instances of the sharded cluster.

- Authentication as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`.

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@mongos0.example.com:27017,mongos1.example.com:27017,mongos2.example.com:27017/?authSource=admin
```

If the username or password includes the following characters, those characters must be converted using [percent encoding:](https://tools.ietf.org/html/rfc3986#section-2.1)

```none
$ : / ? # [ ] @
```

## Additional Connection String Examples

The following examples show connection strings for common connection targets.

### admin Database Running Locally

The following example connects and logs in to the `admin` database as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@localhost
```

### records Database Running Locally

The following example connects and logs in to the `records` database as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@localhost/records
```

### UNIX Domain Socket

When you connect to a UNIX domain socket, use a URL-encoded connection string.

The following example connects to a UNIX domain socket with file path `/tmp/mongodb-27017.sock` as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@%2Ftmp%2Fmongodb-27017.sock
```

### Replica Set with Members on Different Hosts

The following example connects to a [replica set](/docs/manual/reference/glossary#std-term-replica-set) with two members, one on `db1.example.net` and the other on `db2.example.net`, as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

**Note:**

For a replica set, specify the hostname(s) of the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instance(s) as listed in the replica set configuration.

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@db1.example.net,db2.example.com/?replicaSet=test
```

### Replica Set with Members on localhost

The following example connects to a replica set with three members running on `localhost` on ports `27017`, `27018`, and `27019` as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@localhost:27017,localhost:27018,localhost:27019/?replicaSet=myRepl
```

### Replica Set with Read Distribution

The following example connects to a replica set with three members and distributes reads to the [secondaries](/docs/manual/reference/glossary#std-term-secondary) as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@mongodb0.example.com:27017,mongodb1.example.com:27017,mongodb2.example.com:27017/?replicaSet=myRepl&readPreference=secondary
```

### Replica Set with a High Level of Write Concern

The following example connects to a replica set with write concern configured to wait for replication to succeed across a majority of the data-bearing voting members, with a two-second timeout. It authenticates as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`.

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@mongodb0.example.com:27017,mongodb1.example.com:27017,mongodb2.example.com:27017/?replicaSet=myRepl&w=majority&wtimeoutMS=2000
```

### Sharded Cluster

The following example connects to a sharded cluster with three [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instances as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@router1.example.com:27017,router2.example2.com:27017,router3.example3.com:27017/
```

## Find Your Self-Hosted Deployment's Connection String

If you are connected to your self-hosted MongoDB deployment, run [`db.getMongo()`](/docs/manual/reference/method/db.getMongo#mongodb-method-db.getMongo) method to return the connection string.

If you are not connected to your deployment, you can determine your connection string based on the connection string format and options you want to use.

The following connection string for a standalone node includes these elements:

- The hostname of the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instance.

- Authentication as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`.

```bash
mongodb+srv://myDatabaseUser:D1fficultP%40ssw0rd@mongodb0.example.com/?authSource=admin
```

If the username or password includes the following characters, those characters must be converted using [percent encoding:](https://tools.ietf.org/html/rfc3986#section-2.1)

```none
$ : / ? # [ ] @
```

## Additional Connection String Examples

The following examples show connection strings for common connection targets.

### admin Database Running Locally

The following example connects and logs in to the `admin` database as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@localhost
```

### records Database Running Locally

The following example connects and logs in to the `records` database as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@localhost/records
```

### UNIX Domain Socket

When you connect to a UNIX domain socket, use a URL-encoded connection string.

The following example connects to a UNIX domain socket with file path `/tmp/mongodb-27017.sock` as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@%2Ftmp%2Fmongodb-27017.sock
```

### Replica Set with Members on Different Hosts

The following example connects to a [replica set](/docs/manual/reference/glossary#std-term-replica-set) with two members, one on `db1.example.net` and the other on `db2.example.net`, as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

**Note:**

For a replica set, specify the hostname(s) of the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instance(s) as listed in the replica set configuration.

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@db1.example.net,db2.example.com/?replicaSet=test
```

### Replica Set with Members on localhost

The following example connects to a replica set with three members running on `localhost` on ports `27017`, `27018`, and `27019` as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@localhost:27017,localhost:27018,localhost:27019/?replicaSet=myRepl
```

### Replica Set with Read Distribution

The following example connects to a replica set with three members and distributes reads to the [secondaries](/docs/manual/reference/glossary#std-term-secondary) as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@mongodb0.example.com:27017,mongodb1.example.com:27017,mongodb2.example.com:27017/?replicaSet=myRepl&readPreference=secondary
```

### Replica Set with a High Level of Write Concern

The following example connects to a replica set with write concern configured to wait for replication to succeed across a majority of the data-bearing voting members, with a two-second timeout. It authenticates as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`.

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@mongodb0.example.com:27017,mongodb1.example.com:27017,mongodb2.example.com:27017/?replicaSet=myRepl&w=majority&wtimeoutMS=2000
```

### Sharded Cluster

The following example connects to a sharded cluster with three [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instances as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@router1.example.com:27017,router2.example2.com:27017,router3.example3.com:27017/
```

## Find Your Self-Hosted Deployment's Connection String

If you are connected to your self-hosted MongoDB deployment, run [`db.getMongo()`](/docs/manual/reference/method/db.getMongo#mongodb-method-db.getMongo) method to return the connection string.

If you are not connected to your deployment, you can determine your connection string based on the connection string format and options you want to use.

The following connection string for a standalone node includes these elements:

- The hostname of the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instance.

- Authentication as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`.

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@mongodb0.example.com:27017/?authSource=admin
```

If the username or password includes the following characters, those characters must be converted using [percent encoding:](https://tools.ietf.org/html/rfc3986#section-2.1)

```none
$ : / ? # [ ] @
```

## Additional Connection String Examples

The following examples show connection strings for common connection targets.

### admin Database Running Locally

The following example connects and logs in to the `admin` database as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@localhost
```

### records Database Running Locally

The following example connects and logs in to the `records` database as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@localhost/records
```

### UNIX Domain Socket

When you connect to a UNIX domain socket, use a URL-encoded connection string.

The following example connects to a UNIX domain socket with file path `/tmp/mongodb-27017.sock` as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@%2Ftmp%2Fmongodb-27017.sock
```

### Replica Set with Members on Different Hosts

The following example connects to a [replica set](/docs/manual/reference/glossary#std-term-replica-set) with two members, one on `db1.example.net` and the other on `db2.example.net`, as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

**Note:**

For a replica set, specify the hostname(s) of the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instance(s) as listed in the replica set configuration.

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@db1.example.net,db2.example.com/?replicaSet=test
```

### Replica Set with Members on localhost

The following example connects to a replica set with three members running on `localhost` on ports `27017`, `27018`, and `27019` as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@localhost:27017,localhost:27018,localhost:27019/?replicaSet=myRepl
```

### Replica Set with Read Distribution

The following example connects to a replica set with three members and distributes reads to the [secondaries](/docs/manual/reference/glossary#std-term-secondary) as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@mongodb0.example.com:27017,mongodb1.example.com:27017,mongodb2.example.com:27017/?replicaSet=myRepl&readPreference=secondary
```

### Replica Set with a High Level of Write Concern

The following example connects to a replica set with write concern configured to wait for replication to succeed across a majority of the data-bearing voting members, with a two-second timeout. It authenticates as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`.

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@mongodb0.example.com:27017,mongodb1.example.com:27017,mongodb2.example.com:27017/?replicaSet=myRepl&w=majority&wtimeoutMS=2000
```

### Sharded Cluster

The following example connects to a sharded cluster with three [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instances as user `myDatabaseUser` with the password `D1fficultP%40ssw0rd`:

```bash
mongodb://myDatabaseUser:D1fficultP%40ssw0rd@router1.example.com:27017,router2.example2.com:27017,router3.example3.com:27017/
```

## Learn More

For a full list of connection string options, see [Connection String Options.](/docs/manual/reference/connection-string-options#std-label-connections-connection-options)
