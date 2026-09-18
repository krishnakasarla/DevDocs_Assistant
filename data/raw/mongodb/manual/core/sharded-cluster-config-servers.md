> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Config Servers

Config servers store the metadata for a [sharded cluster](/docs/manual/reference/glossary#std-term-sharded-cluster). The metadata reflects state and organization for all data and components within the sharded cluster. The metadata includes the list of chunks on every shard and the ranges that define the chunks.

The [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instances cache this data and use it to route read and write operations to the correct shards. [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) updates the cache when there are metadata changes for the cluster, such as [adding a shard](/docs/manual/tutorial/add-shards-to-shard-cluster#std-label-sharding-procedure-add-shard). Shards also read chunk metadata from the config servers.

The config servers also store [Authentication on Self-Managed Deployments](/docs/manual/core/authentication#std-label-authentication) configuration information such as [Role-Based Access Control](/docs/manual/core/authorization#std-label-authorization) or [internal authentication](/docs/manual/core/security-internal-authentication#std-label-replica-set-security) settings for the cluster.

MongoDB also uses the config servers to manage distributed locks.

Each sharded cluster must have its own config servers. Do not use the same config servers for different sharded clusters.

**Warning:**

Administrative operations conducted on config servers may have significant impact on sharded cluster performance and availability. Depending on the number of config servers impacted, the cluster may be read-only or offline for a period of time.

Starting in MongoDB 8.0, you can configure a config server to store application data in addition to the usual sharded cluster metadata. The config server is then known as a *config shard*. You'll learn more later on this page in the [Config Shards](/docs/manual/core/sharded-cluster-config-servers#std-label-sharded-cluster-config-server-config-shards) section.

## Replica Set Config Servers

The following restrictions apply to a replica set configuration when used for config servers:

- Must have zero [arbiters.](/docs/manual/core/replica-set-arbiter#std-label-replica-set-arbiter-configuration)

- Must have no [delayed members.](/docs/manual/core/replica-set-delayed-member)

- Must build indexes (i.e. no member should have [`members[n].buildIndexes`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.members-n-.buildIndexes) setting set to false).

## Read and Write Operations on Config Servers

The `admin` database and the `config` database exist on the config servers.

### Writes to Config Servers

The `admin` database contains the collections related to the authentication and authorization as well as the other [system.\* collections](/docs/manual/reference/system-collections#std-label-metadata-system-collections) for internal use.

The `config` database contains the collections that contain the sharded cluster metadata. MongoDB writes data to the `config` database when the metadata changes, such as after a [chunk migration](/docs/manual/core/sharding-balancer-administration#std-label-sharding-balancing) or a [chunk split.](/docs/manual/core/sharding-data-partitioning#std-label-sharding-data-partitioning)

Users should avoid writing directly to the config database in the course of normal operation or maintenance.

When writing to the config servers, MongoDB uses a [write concern](/docs/manual/reference/write-concern#std-label-wc-w) of `"majority"`.

### Reads from Config Servers

MongoDB reads from the `admin` database for authentication and authorization data and other internal uses.

MongoDB reads from the `config` database when a [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) starts or after a change in the metadata, such as after a chunk migration. Shards also read chunk metadata from the config servers.

When reading from the replica set config servers, MongoDB uses a [Read Concern](/docs/manual/reference/read-concern#std-label-read-concern) level of [`"majority"`.](/docs/manual/reference/read-concern-majority#mongodb-readconcern-readconcern.-majority-)

### Metadata Views Must be Up-to-Date

For an operation to succeed, the view of the metadata on the specific shard member must be up-to-date. The shard and the router issuing the request must have the same version of the chunks metadata.

If the metadata is not up-to-date, the operation fails with the `StaleConfig` error and the metadata refresh process is triggered. Refreshing the metadata can introduce additional operational latency.

On a secondary, a metadata refresh can take a long time if there is significant replication lag. For secondary reads, set `maxStalenessSeconds` to minimize the impact of replication lag.

## Config Server Availability

If the config server replica set loses its primary and cannot elect a primary, the cluster's metadata becomes *read only*. You can still read and write data from the shards, but no chunk migration or chunk splits will occur until the replica set can elect a primary.

In a sharded cluster, [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) and [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instances monitor the replica sets in the sharded cluster (e.g. shard replica sets, config server replica set).

If all config servers become unavailable, the cluster can become inoperable. To ensure that the config servers remain available and intact, backups of config servers are critical. The data on the config server is small compared to the data stored in a cluster, and the config server has a relatively low activity load.

See [A Config Server Replica Set Member Become Unavailable](/docs/manual/tutorial/troubleshoot-sharded-clusters#std-label-sharding-config-servers-and-availability) for more information.

## Sharded Cluster Metadata

Config servers store metadata in the `config` database.

**Important:**

Always back up the `config` database before doing any maintenance on the config server.

To access the `config` database, issue the following command in [`mongosh`:](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh)

```javascript
use config
```

In general, you should *never* edit the content of the `config` database directly. The `config` database contains the following collections:

- [`changelog`](/docs/manual/reference/config-database#mongodb-data-config.changelog)

- [`chunks`](/docs/manual/reference/config-database#mongodb-data-config.chunks)

- [`collections`](/docs/manual/reference/config-database#mongodb-data-config.collections)

- [`databases`](/docs/manual/reference/config-database#mongodb-data-config.databases)

- [`mongos`](/docs/manual/reference/config-database#mongodb-data-config.mongos)

- [`placementHistory`](/docs/manual/reference/config-database#mongodb-data-config.placementHistory)

- [`settings`](/docs/manual/reference/config-database#mongodb-data-config.settings)

- [`shards`](/docs/manual/reference/config-database#mongodb-data-config.shards)

- [`version`](/docs/manual/reference/config-database#mongodb-data-config.version)

For more information on these collections and their role in sharded clusters, see [Config Database](/docs/manual/reference/config-database#std-label-config-database). See [Read and Write Operations on Config Servers](/docs/manual/core/sharded-cluster-config-servers#std-label-config-server-read-write-ops) for more information about reads and updates to the metadata.

## Sharded Cluster Security

Use [Self-Managed Internal/Membership Authentication](/docs/manual/core/security-internal-authentication#std-label-inter-process-auth) to enforce intra-cluster security and prevent unauthorized cluster components from accessing the cluster. You must start each [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) in the cluster with the appropriate security settings in order to enforce internal authentication.

Starting in MongoDB 5.3, [SCRAM-SHA-1](/docs/manual/core/security-scram#std-label-authentication-scram-sha-1) cannot be used for intra-cluster authentication. Only [SCRAM-SHA-256](/docs/manual/core/security-scram#std-label-authentication-scram-sha-256) is supported.

In previous MongoDB versions, SCRAM-SHA-1 and SCRAM-SHA-256 can both be used for intra-cluster authentication, even if SCRAM is not explicitly enabled.

See [Keyfile Authentication for Self-Managed Sharded Clusters](/docs/manual/tutorial/deploy-sharded-cluster-with-keyfile-access-control#std-label-deploy-cluster-with-keyfile-auth) for a tutorial on deploying a secured sharded cluster.

## Config Shards

**New in version 8.0**

Starting in MongoDB 8.0, you can:

- Configure a config server to store your application data in addition to the usual [sharded cluster](/docs/manual/reference/glossary#std-term-sharded-cluster) metadata. A config server that stores application data is called a *config shard*.

- Transition a config server between being a config shard and a dedicated config server.

A cluster requires a config server, but it can be a config shard instead of a dedicated config server. Using a config shard reduces the number of nodes required and can simplify your deployment.

A config shard costs less than a dedicated config server because a dedicated config server runs as its own replica set. A config shard combines the config server role into an existing shard's replica set, so your cluster needs one replica set instead of two. Using a config shard has no measurable performance impact at low shard counts. A dedicated config server isolates cluster metadata from application data, which certain features require. To learn which deployment fits your cluster, see [Config Shard Use Cases.](/docs/manual/core/config-shard#std-label-config-shard-use-cases)

You cannot use the same config shard for multiple sharded clusters.

### Commands

To configure a dedicated config server to run as a config shard, run the [`transitionFromDedicatedConfigServer`](/docs/manual/reference/command/transitionFromDedicatedConfigServer#mongodb-dbcommand-dbcmd.transitionFromDedicatedConfigServer) command.

To configure a config shard to run as a dedicated config server, run the [`transitionToDedicatedConfigServer`](/docs/manual/reference/command/transitionToDedicatedConfigServer#mongodb-dbcommand-dbcmd.transitionToDedicatedConfigServer) command.

### Users

A user created on a config shard has the same behavior as a user created on a dedicated config server.

### Confirm use of Config Shard

You can confirm that a sharded cluster uses a config shard by using one of the following methods:

- Run the [`sh.isConfigShardEnabled()`](/docs/manual/reference/method/sh.isConfigShardEnabled#mongodb-method-sh.isConfigShardEnabled) method in `mongosh`. If the `sh.isConfigShardEnabled()` output contains `enabled: true`, the cluster uses a config shard. If the output contains `enabled: false`, the cluster does not use a config shard.

- Run the [`listShards`](/docs/manual/reference/command/listShards#mongodb-dbcommand-dbcmd.listShards) command against the `admin` database while connected to a [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) and inspect the output for a document where `_id` is set to `"config"`. If the `listShards` output does not contain a document where `_id` is set to `"config"`, the cluster does not use a config shard.

The following example runs the `listShards` command and tries to find a document where `_id` is set to `"config"`.

```javascript
db.adminCommand({ listShards: 1 })["shards"].find(element => element._id === "config")
```

In this example, the returned document has `_id` set to `"config"` which confirms that this cluster uses a config shard.

```javascript
{
  _id: "config",
  host: "configRepl/localhost:27018",
  state: 1,
  topologyTime: Timestamp({ t: 1732218671, i: 13 }),
  replSetConfigVersion: Long('-1')
}
```

### Downgrade Feature Compatibility Version

If your cluster has a config shard and you need to downgrade the [feature compatibility version](/docs/manual/reference/command/setFeatureCompatibilityVersion#std-label-view-fcv) to earlier than 8.0, connect to `mongos` and perform this procedure:

1. Configure a config shard to run as a dedicated config server.

   To begin configuring a config shard to run as a dedicated config server, run [`transitionToDedicatedConfigServer`:](/docs/manual/reference/command/transitionToDedicatedConfigServer#mongodb-dbcommand-dbcmd.transitionToDedicatedConfigServer)

   ```javascript
   db.adminCommand( {
      transitionToDedicatedConfigServer: 1
   } )
   ```

2. List all of the databases and collections in the cluster.

   To list all the databases in the cluster, run [`listDatabases`:](/docs/manual/reference/command/listDatabases#mongodb-dbcommand-dbcmd.listDatabases)

   ```javascript
   db.adminCommand( { listDatabases: 1, nameOnly: true } )
   ```

   Exclude `admin` and `config` databases.

   For each database, list all of the collections in the database.

   To list all of the collections in the database, run [`listCollections`.](/docs/manual/reference/command/listCollections#mongodb-dbcommand-dbcmd.listCollections)

   ```javascript
   db.adminCommand(
      {
         listCollections: 1,
         nameOnly: true,
         filter: { type: { $ne: "view" } }
      }
   )
   ```

   Exclude collections starting with `system`.

3. For each non-system collection, move the collection to a new shard.

   To move the collection to a new shard, run [`moveCollection`:](/docs/manual/reference/command/moveCollection#mongodb-dbcommand-dbcmd.moveCollection)

   ```javascript
   db.adminCommand(
      {
         moveCollection: "<database>.<collection>",
         toShard: "<new shard>",
      }
      )
   ```

4. Wait for balancer to move sharded collection data off config server.

   To verify the balancer has moved sharded collection data off the config server, run `transitionToDedicatedConfigServer` again:

   ```javascript
   db.adminCommand( {
      transitionToDedicatedConfigServer: 1
   } )
   ```

   The response after a successful data move contains `state:
           "completed"`. If the response contains `state: "pendingDataCleanup"`, wait a moment then continue calling `transitionToDedicatedConfigServer` until the command response contains `state: "completed"`. For full response details, see [`removeShard`.](/docs/manual/reference/command/removeShard#mongodb-dbcommand-dbcmd.removeShard)

5. Set the feature compatibility version.

   To set the feature compatibility version, run [`setFeatureCompatibilityVersion`:](/docs/manual/reference/command/setFeatureCompatibilityVersion#mongodb-dbcommand-dbcmd.setFeatureCompatibilityVersion)

   ```javascript
   db.adminCommand( { setFeatureCompatibilityVersion: "7.0" } )
   ```
