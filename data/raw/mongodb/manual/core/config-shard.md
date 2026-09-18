> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Config Shard

Starting in MongoDB 8.0, you can configure a config server to store your application data in addition to the usual sharded cluster metadata. A [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) node that provides both config server and shard server functionality is called a config shard. A `mongod` node that runs as a standalone [`--configsvr`](/docs/manual/reference/program/mongod#std-option-mongod.--configsvr) without shard server functionality is called a dedicated [config server.](/docs/manual/core/sharded-cluster-config-servers#std-label-sharded-cluster-config-server)

A sharded cluster must have a config server, but it can be either a config shard (embedded config server) or a dedicated config server. Using a config shard reduces the number of nodes required and can simplify your deployment. A config shard cluster is also called an embedded config server cluster. You cannot use the same config server for multiple sharded clusters.

## Use Cases

A config shard costs less than a dedicated config server because a dedicated config server runs as its own replica set. A config shard combines the config server role into an existing shard's replica set, so your cluster needs one replica set instead of two. Using a config shard has no measurable performance impact at low shard counts. A dedicated config server isolates cluster metadata from application data, which certain features require.

Use a dedicated config server if you use one or more of the following features:

- [Queryable Encryption](/docs/manual/core/queryable-encryption#std-label-qe-manual-feature-qe) collections

- [Queryable backups](https://www.mongodb.com/docs/ops-manager/current/tutorial/query-backup/) (on-prem)

On MongoDB Atlas, a cluster automatically transitions from a config shard to a dedicated config server when the cluster has more than five [shards.](/docs/manual/sharding#std-label-sharding-sharded-cluster)

## Behavior

In an embedded config server cluster, a config shard will be used to store cluster metadata and user data. It helps reduce the complexity of a sharded cluster deployment.

You can store sharded and unsharded collection data in your config shard. It has all the properties of a shard as well as acting as the config server.

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

### Commands

To configure a dedicated config server to run as a config shard, run the [`transitionFromDedicatedConfigServer`](/docs/manual/reference/command/transitionFromDedicatedConfigServer#mongodb-dbcommand-dbcmd.transitionFromDedicatedConfigServer) command.

To configure a config shard to run as a dedicated config server, run the [`transitionToDedicatedConfigServer`](/docs/manual/reference/command/transitionToDedicatedConfigServer#mongodb-dbcommand-dbcmd.transitionToDedicatedConfigServer) command.

## Get Started

- [Convert Replica Set to an Embedded Config Shard](/docs/manual/tutorial/convert-replica-set-to-embedded-config-server#std-label-convert-replica-set-to-embedded-config-server)

- [Start a Sharded Cluster with a Config Shard](/docs/manual/tutorial/start-a-sharded-cluster-with-config-shard#std-label-start-a-sharded-cluster-with-config-shard)

## Learn More

- [Config Shards](/docs/manual/core/sharded-cluster-config-servers#std-label-sharded-cluster-config-server-config-shards)

- [`transitionFromDedicatedConfigServer`](/docs/manual/reference/command/transitionFromDedicatedConfigServer#mongodb-dbcommand-dbcmd.transitionFromDedicatedConfigServer)

- [`transitionToDedicatedConfigServer`](/docs/manual/reference/command/transitionToDedicatedConfigServer#mongodb-dbcommand-dbcmd.transitionToDedicatedConfigServer)
