> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Routing with mongos

MongoDB [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instances route queries and write operations to [shards](/docs/manual/reference/glossary#std-term-shard) in a sharded cluster. `mongos` provides the only interface to a sharded cluster from the perspective of applications. Applications never connect or communicate directly with the shards.

The `mongos` tracks what data is on which shard by caching the metadata from the [config servers](/docs/manual/core/sharded-cluster-config-servers#std-label-sharded-cluster-config-server). The `mongos` uses the metadata to route operations from applications and clients to the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instances. A `mongos` has no *persistent* state and consumes minimal system resources.

The most common practice is to run `mongos` instances on the same systems as your application servers, but you can maintain `mongos` instances on the shards or on other dedicated resources.  See also [Number of `mongos` and Distribution.](/docs/manual/core/sharded-cluster-components#std-label-sharded-cluster-components-distribution)

## Routing And Results Process

A [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instance routes a query to a [cluster](/docs/manual/reference/glossary#std-term-sharded-cluster) by:

1. Determining the list of [shards](/docs/manual/reference/glossary#std-term-shard) that must receive the query.

2. Establishing a cursor on all targeted shards.

The `mongos` then merges the data from each of the targeted shards and returns the result document. Certain query modifiers, such as [sorting](/docs/manual/core/sharded-cluster-query-router#std-label-sharding-mongos-sort), are performed on each shard before `mongos` retrieves the results.

[Aggregation operations](/docs/manual/core/aggregation-pipeline#std-label-aggregation-pipeline) running on multiple shards may route results back to the [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) to merge results if they don't need to run on the database's [primary shard.](/docs/manual/reference/glossary#std-term-primary-shard)

There are two cases in which a pipeline is ineligible to run on [`mongos`.](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos)

The first case occurs when the merge part of the split pipeline contains a stage which *must* run on a specific shard. For instance, if `$lookup` requires access to an unsharded collection in the same database as the sharded collection on which the aggregation is running, the merge runs on the shard that hosts the unsharded collection.

The second case occurs when the merge part of the split pipeline contains a stage which may write temporary data to disk, such as `$group`, and the client has specified `allowDiskUse:true`. In this case, assuming that there are no other stages in the merge pipeline which require the primary shard, the merge runs on a randomly-selected shard in the set of shards targeted by the aggregation.

For more information on how the work of aggregation is split among components of a sharded cluster query, use `explain:true` as a parameter to the [`aggregate()`](/docs/manual/reference/method/db.collection.aggregate#mongodb-method-db.collection.aggregate) call. The return includes three JSON objects:

- `mergeType` shows where the stage of the merge happens ("anyShard", "specificShard", or "router"). When `mergeType` is `specificShard`, the aggregate output includes a `mergeShard` property that contains the shard ID of the merging shard.

- `splitPipeline` shows which operations in your pipeline have run on individual shards.

- `shards` shows the work each shard has done.

In some cases, when the [shard key](/docs/manual/reference/glossary#std-term-shard-key) or a prefix of the shard key is a part of the query, the [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) performs a [targeted operation](/docs/manual/core/sharded-cluster-query-router#std-label-sharding-mongos-targeted), routing queries to a subset of shards in the cluster.

`mongos` performs a [broadcast operation](/docs/manual/core/sharded-cluster-query-router#std-label-sharding-mongos-broadcast) for queries that do *not* include the [shard key](/docs/manual/reference/glossary#std-term-shard-key), routing queries to *all* shards in the cluster. Some queries that do include the shard key may still result in a broadcast operation depending on the distribution of data in the cluster and the selectivity of the query.

See [Targeted Operations vs. Broadcast Operations](/docs/manual/core/sharded-cluster-query-router#std-label-sharding-query-isolation) for more on targeted and broadcast operations.

## How `mongos` Handles Query Modifiers

### Sorting

If the result of the query is not sorted, the [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instance opens a result cursor that "round robins" results from all cursors on the shards.

### Limits

If the query limits the size of the result set using the [`limit()`](/docs/manual/reference/method/cursor.limit#mongodb-method-cursor.limit) cursor method, the [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instance passes that limit to the shards and then re-applies the limit to the result before returning the result to the client.

### Skips

If the query specifies a number of records to *skip* using the [`skip()`](/docs/manual/reference/method/cursor.skip#mongodb-method-cursor.skip) cursor method, the [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) *cannot* pass the skip to the shards, but rather retrieves unskipped results from the shards and skips the appropriate number of documents when assembling the complete result.

When used in conjunction with a [`limit()`](/docs/manual/reference/method/cursor.limit#mongodb-method-cursor.limit), the [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) passes the *limit* plus the value of the [`skip()`](/docs/manual/reference/method/cursor.skip#mongodb-method-cursor.skip) to the shards to improve the efficiency of these operations.

## Read Preference and Shards

For sharded clusters, [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) applies the [read preference](/docs/manual/core/read-preference) when reading from the shards. The member selected is governed by both the [read preference](/docs/manual/core/read-preference) and [`replication.localPingThresholdMs`](/docs/manual/reference/configuration-options#mongodb-setting-replication.localPingThresholdMs) settings, and is re-evaluated for each operation.

For details on read preference and sharded clusters, see [Read Preference and Shards.](/docs/manual/core/read-preference-mechanics#std-label-read-preference-mechanics-sharded-cluster)

## Targeting Behavior Under Overload

When you enable the ingress request rate limiter, a `mongod` or `mongos` node can reject operations if the rate of incoming requests exceeds the configured limit. In this case, the server returns an error that includes the `SystemOverloadedError` error label.

When the [`overloadAwareServerSelectionEnabled`](/docs/manual/reference/parameters#mongodb-parameter-param.overloadAwareServerSelectionEnabled) is set to `true`, if a target server responds with an error labeled `SystemOverloadedError`, the router deprioritizes that server in later targeting decisions for retries of that request. By default, `overloadAwareServerSelectionEnabled` is set to `false`.

For example, when the [`primaryPreferred`](/docs/manual/core/read-preference#mongodb-readmode-primaryPreferred) read preference is in use and the primary is overloaded, the router can re‑target the read to an appropriate secondary instead of continuing to send traffic to the overloaded primary.

Overload‑aware targeting helps the cluster maintain availability during overload conditions by routing work away from servers that are actively shedding load, while still honoring read preference rules.

## Confirm Connection to `mongos` Instances

To detect if the MongoDB instance that your client is connected to is [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos), use the [`hello`](/docs/manual/reference/command/hello#mongodb-dbcommand-dbcmd.hello) command. When a client connects to a [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos), [`hello`](/docs/manual/reference/command/hello#mongodb-dbcommand-dbcmd.hello) returns a document with a `msg` field that holds the string `isdbgrid`. For example:

```javascript
{
   "isWritablePrimary" : true,
   "msg" : "isdbgrid",
   "maxBsonObjectSize" : 16777216,
   "ok" : 1,
   ...
}
```

If the application is instead connected to a [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod), the returned document does not include the `isdbgrid` string.

## Targeted Operations vs. Broadcast Operations

Generally, the fastest queries in a sharded environment are those that [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) route to a single shard, using the [shard key](/docs/manual/reference/glossary#std-term-shard-key) and the cluster meta data from the [config server](/docs/manual/core/sharded-cluster-config-servers#std-label-sharding-config-server). These [targeted operations](/docs/manual/core/sharded-cluster-query-router#std-label-sharding-mongos-targeted) use the shard key value to locate the shard or subset of shards that satisfy the query document.

For queries that don't include the shard key, [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) must query all shards, wait for their responses and then return the result to the application. These "scatter/gather" queries can be long running operations.

### Broadcast Operations

[`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instances broadcast queries to all shards for the collection **unless** the [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) can determine which shard or subset of shards stores this data.

![Read operations to a sharded cluster where \`\`mongos\`\` broadcasts the query to all shards.](/images/sharded-cluster-scatter-gather-query.bakedsvg.svg)

After the [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) receives responses from all shards, it merges the data and returns the result document. The performance of a broadcast operation depends on the overall load of the cluster, as well as variables like network latency, individual shard load, and number of documents returned per shard. Whenever possible, favor operations that result in [targeted operation](/docs/manual/core/sharded-cluster-query-router#std-label-sharding-mongos-targeted) over those that result in a broadcast operation.

Multi-update operations are always broadcast operations.

The [`updateMany()`](/docs/manual/reference/method/db.collection.updateMany#mongodb-method-db.collection.updateMany) and [`deleteMany()`](/docs/manual/reference/method/db.collection.deleteMany#mongodb-method-db.collection.deleteMany) methods are broadcast operations, unless the query document specifies the shard key in full.

### Targeted Operations

[`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) can route queries that include the shard key or the prefix of a [compound](/docs/manual/reference/glossary#std-term-compound-index) shard key a specific shard or set of shards. [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) uses the shard key value to locate the [chunk](/docs/manual/reference/glossary#std-term-chunk) whose range includes the shard key value and directs the query at the [shard](/docs/manual/reference/glossary#std-term-shard) containing that chunk.

![Targeted read where \`\`mongos\`\` routes to specific shards based on the shard key in the query.](/images/sharded-cluster-targeted-query.bakedsvg.svg)

For example, if the shard key is:

```javascript
{ a: 1, b: 1, c: 1 }
```

The [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) program *can* route queries that include the full shard key or either of the following shard key prefixes at a specific shard or set of shards:

```javascript
{ a: 1 }
{ a: 1, b: 1 }
```

All [`insertOne()`](/docs/manual/reference/method/db.collection.insertOne#mongodb-method-db.collection.insertOne) operations target to one shard. Each document in the [`insertMany()`](/docs/manual/reference/method/db.collection.insertMany#mongodb-method-db.collection.insertMany) array targets to a single shard, but there is no guarantee all documents in the array insert into a single shard.

All [`updateOne()`](/docs/manual/reference/method/db.collection.updateOne#mongodb-method-db.collection.updateOne), [`replaceOne()`](/docs/manual/reference/method/db.collection.replaceOne#mongodb-method-db.collection.replaceOne) and [`deleteOne()`](/docs/manual/reference/method/db.collection.deleteOne#mongodb-method-db.collection.deleteOne) operations *must* include the [shard key](/docs/manual/reference/glossary#std-term-shard-key) or `_id` in the query document. MongoDB returns an error if these methods are used without the shard key or `_id`.

Depending on the distribution of data in the cluster and the selectivity of the query, [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) may still perform a [broadcast operation](/docs/manual/core/sharded-cluster-query-router#std-label-sharding-mongos-broadcast) to fulfill these queries.

### Index Use

When a shard receives a query, it uses the most efficient index available to fulfill that query. The index used may be either the [shard key index](/docs/manual/core/sharding-shard-key-indexes#std-label-sharding-shard-key-indexes) or another eligible index present on the shard.

## Sharded Cluster Security

Use [Self-Managed Internal/Membership Authentication](/docs/manual/core/security-internal-authentication) to enforce intra-cluster security and prevent unauthorized cluster components from accessing the cluster. You must start each [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) or [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) in the cluster with the appropriate security settings in order to enforce internal authentication.

Starting in MongoDB 5.3, [SCRAM-SHA-1](/docs/manual/core/security-scram#std-label-authentication-scram-sha-1) cannot be used for intra-cluster authentication. Only [SCRAM-SHA-256](/docs/manual/core/security-scram#std-label-authentication-scram-sha-256) is supported.

In previous MongoDB versions, SCRAM-SHA-1 and SCRAM-SHA-256 can both be used for intra-cluster authentication, even if SCRAM is not explicitly enabled.

See [Keyfile Authentication for Self-Managed Sharded Clusters](/docs/manual/tutorial/deploy-sharded-cluster-with-keyfile-access-control) for a tutorial on deploying a secured sharded cluster.

### Cluster Users

Sharded clusters support [Role-Based Access Control in Self-Managed Deployments](/docs/manual/core/authorization) *(RBAC)* for restricting unauthorized access to cluster data and operations. You must start each [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) in the cluster, including the [config servers](/docs/manual/reference/glossary#std-term-config-server), with the [`--auth`](/docs/manual/reference/program/mongod#std-option-mongod.--auth) option in order to enforce RBAC. Alternatively, enforcing [Self-Managed Internal/Membership Authentication](/docs/manual/core/security-internal-authentication) for inter-cluster security also enables user access controls via RBAC.

With RBAC enforced, clients must specify a [`--username`](https://www.mongodb.com/docs/mongodb-shell/reference/options/#std-option-mongosh.--username), [`--password`](https://www.mongodb.com/docs/mongodb-shell/reference/options/#std-option-mongosh.--password), and [`--authenticationDatabase`](https://www.mongodb.com/docs/mongodb-shell/reference/options/#std-option-mongosh.--authenticationDatabase) when connecting to the [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) in order to access cluster resources.

Each cluster has its own cluster users. These users cannot be used to access individual shards.

See [Enable Access Control on Self-Managed Deployments](/docs/manual/tutorial/enable-authentication) for a tutorial on enabling adding users to an RBAC-enabled MongoDB deployment.

## Metadata Operations

[`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) uses [`"majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) write concern for the following operations that affect the sharded cluster metadata:

| Command | Method |
| --- | --- |
| [`addShard`](/docs/manual/reference/command/addShard#mongodb-dbcommand-dbcmd.addShard) | [`sh.addShard()`](/docs/manual/reference/method/sh.addShard#mongodb-method-sh.addShard) |
| [`create`](/docs/manual/reference/command/create#mongodb-dbcommand-dbcmd.create) | [`db.createCollection()`](/docs/manual/reference/method/db.createCollection#mongodb-method-db.createCollection) |
| [`drop`](/docs/manual/reference/command/drop#mongodb-dbcommand-dbcmd.drop) | [`db.collection.drop()`](/docs/manual/reference/method/db.collection.drop#mongodb-method-db.collection.drop) |
| [`dropDatabase`](/docs/manual/reference/command/dropDatabase#mongodb-dbcommand-dbcmd.dropDatabase) | [`db.dropDatabase()`](/docs/manual/reference/method/db.dropDatabase#mongodb-method-db.dropDatabase) |
| [`enableSharding`](/docs/manual/reference/command/enableSharding#mongodb-dbcommand-dbcmd.enableSharding) | [`sh.enableSharding()`](/docs/manual/reference/method/sh.enableSharding#mongodb-method-sh.enableSharding) |
| [`movePrimary`](/docs/manual/reference/command/movePrimary#mongodb-dbcommand-dbcmd.movePrimary) | |
| [`renameCollection`](/docs/manual/reference/command/renameCollection#mongodb-dbcommand-dbcmd.renameCollection) | [`db.collection.renameCollection()`](/docs/manual/reference/method/db.collection.renameCollection#mongodb-method-db.collection.renameCollection) |
| [`shardCollection`](/docs/manual/reference/command/shardCollection#mongodb-dbcommand-dbcmd.shardCollection) | [`sh.shardCollection()`](/docs/manual/reference/method/sh.shardCollection#mongodb-method-sh.shardCollection) |
| [`removeShard`](/docs/manual/reference/command/removeShard#mongodb-dbcommand-dbcmd.removeShard) | |
| [`setFeatureCompatibilityVersion`](/docs/manual/reference/command/setFeatureCompatibilityVersion#mongodb-dbcommand-dbcmd.setFeatureCompatibilityVersion) | |

## Additional Information

### FCV Compatibility

The [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) binary cannot connect to [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instances whose [feature compatibility version (FCV)](/docs/manual/reference/command/setFeatureCompatibilityVersion#std-label-view-fcv) is greater than that of the [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos). For example, you cannot connect a MongoDB 4.0 version [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) to a 4.2 sharded cluster with [FCV](/docs/manual/reference/command/setFeatureCompatibilityVersion#std-label-view-fcv) set to 4.2. You can, however, connect a MongoDB 4.0 version [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) to a 4.2 sharded cluster with [FCV](/docs/manual/reference/command/setFeatureCompatibilityVersion#std-label-view-fcv) set to 4.0.

### Full Time Diagnostic Data Capture Requirements

[`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) includes a [Full Time Diagnostic Data Capture](/docs/manual/administration/full-time-diagnostic-data-capture#std-label-ftdc-stub) mechanism to assist MongoDB engineers with troubleshooting deployments. If this thread fails, it terminates the originating process. To avoid the most common failures, confirm that the user running the process has permissions to create the FTDC `diagnostic.data` directory. For `mongod` the directory is within [`storage.dbPath`](/docs/manual/reference/configuration-options#mongodb-setting-storage.dbPath). For `mongos` it is parallel to [`systemLog.path`.](/docs/manual/reference/configuration-options#mongodb-setting-systemLog.path)

### Connection Pools

Starting in MongoDB 4.2, MongoDB adds the parameter [`ShardingTaskExecutorPoolReplicaSetMatching`](/docs/manual/reference/parameters#mongodb-parameter-param.ShardingTaskExecutorPoolReplicaSetMatching). This parameter determines the minimum size of the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) / [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instance's connection pool to each member of the sharded cluster. This value can vary during runtime.

[`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) and [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) maintain connection pools to each replica set secondary for every replica set in the sharded cluster. By default, these pools have a number of connections that is at least the number of connections to the primary.

To modify, see [`ShardingTaskExecutorPoolReplicaSetMatching`.](/docs/manual/reference/parameters#mongodb-parameter-param.ShardingTaskExecutorPoolReplicaSetMatching)

### Using Aggregation Pipelines with Clusters

For more information on how sharding works with [aggregations](/docs/manual/core/aggregation-pipeline#std-label-aggregation-pipeline), read the sharding chapter in the [Practical MongoDB Aggregations](https://www.practical-mongodb-aggregations.com/guides/sharding.html) e-book.
