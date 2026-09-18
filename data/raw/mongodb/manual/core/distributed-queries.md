> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Distributed Queries

Learn how MongoDB handles read and write operations in replica sets and sharded clusters. This page explains the importance of cluster architecture on query routing and data consistency.

## Read Operations to Replica Sets

By default, clients read from a replica set's [primary](/docs/manual/reference/glossary#std-term-primary). However, you can specify a [read preference](/docs/manual/core/read-preference) to direct read operations to other members. For example, configure read preferences to read from secondaries or from the nearest member to:

- Reduce latency in deployments with multiple data centers.

- Perform backup operations.

- Allow reads until a [new primary is elected.](/docs/manual/core/replica-set-high-availability#std-label-replica-set-failover)

![Read operations to a replica set showing default and \`\`nearest\`\` read preference routing.](/images/replica-set-read-preference.bakedsvg.svg)

Read operations from secondary members of replica sets may not reflect the current state of the primary. Read preferences that direct read operations to different servers may result in non-monotonic reads.

Clients can use [causally consistent](/docs/manual/core/read-isolation-consistency-recency#std-label-causal-consistency) sessions, which provides various guarantees including monotonic reads.

You can configure the read preference on a per-connection or per-operation basis. For more information on read preference or on the read preference modes, see [Read Preference](/docs/manual/core/read-preference) and [Read Preference Modes.](/docs/manual/core/read-preference#std-label-replica-set-read-preference-modes)

## Write Operations on Replica Sets

In [replica sets](/docs/manual/reference/glossary#std-term-replica-set), all write operations go to the set's [primary](/docs/manual/reference/glossary#std-term-primary). The primary applies the write operation and records the operations on the primary's operation log or [oplog](/docs/manual/reference/glossary#std-term-oplog). The oplog is a reproducible sequence of operations to the data set. [secondary](/docs/manual/reference/glossary#std-term-secondary) members of the set continuously replicate the oplog and apply the operations to themselves in an asynchronous process.

![Diagram of default routing of reads and writes to the primary.](/images/replica-set-read-write-operations-primary.bakedsvg.svg)

For more information on replica sets and write operations, see [Replication](/docs/manual/replication#std-label-replication) and [Write Concern.](/docs/manual/reference/write-concern)

## Read Operations to Sharded Clusters

[Sharded clusters](/docs/manual/reference/glossary#std-term-sharded-cluster) allow you to partition a data set among a cluster of [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instances in a way that is nearly transparent to the application. For an overview of sharded clusters, see the [Sharding](/docs/manual/sharding) section of this manual.

For a sharded cluster, applications issue operations to one of the [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instances associated with the cluster.

![Diagram of a sharded cluster.](/images/sharded-cluster.bakedsvg.svg)

Read operations on sharded clusters are most efficient when directed to a specific shard. Queries to sharded collections should include the collection's [shard key](/docs/manual/core/sharding-shard-key#std-label-sharding-shard-key). When a query includes a shard key, the [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) can use cluster metadata from the [config database](/docs/manual/core/sharded-cluster-config-servers#std-label-sharding-config-server) to route the queries to shards.

![Targeted read where \`\`mongos\`\` routes to specific shards based on the shard key in the query.](/images/sharded-cluster-targeted-query.bakedsvg.svg)

If a query does not include the shard key, the [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) must direct the query to *all* shards in the cluster. These *scatter
gather* queries can be inefficient. On larger clusters, scatter gather queries are unfeasible for routine operations.

![Read operations to a sharded cluster where \`\`mongos\`\` broadcasts the query to all shards.](/images/sharded-cluster-scatter-gather-query.bakedsvg.svg)

For replica set shards, read operations from secondary members of replica sets may not reflect the current state of the primary. Read preferences that direct read operations to different servers may result in non-monotonic reads.

**Note:**

- Clients can use [causally consistent](/docs/manual/core/read-isolation-consistency-recency#std-label-causal-consistency) sessions, which provides various guarantees, including monotonic reads.

- All members of a shard replica set, not just the primary, maintain the metadata regarding chunk metadata. This prevents reads from the secondaries from returning [orphaned data](/docs/manual/reference/glossary#std-term-orphaned-document) if not using read concern [`"available"`](/docs/manual/reference/read-concern-available#mongodb-readconcern-readconcern.-available-). In earlier versions, reads from secondaries, regardless of the read concern, could return orphaned documents.

For more information on read operations in sharded clusters, see the [Routing with mongos](/docs/manual/core/sharded-cluster-query-router) and [Shard Keys](/docs/manual/core/sharding-shard-key#std-label-sharding-shard-key) sections.

## Write Operations on Sharded Clusters

For sharded collections in a [sharded cluster](/docs/manual/reference/glossary#std-term-sharded-cluster), the [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) directs write operations from applications to the shards that are responsible for the specific *portion* of the data set. The [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) uses the cluster metadata from the [config database](/docs/manual/core/sharded-cluster-config-servers#std-label-sharding-config-server) to route the write operation to the appropriate shards.

![Diagram of a sharded cluster.](/images/sharded-cluster.bakedsvg.svg)

MongoDB partitions data in a sharded collection into *ranges* based on the values of the [shard key](/docs/manual/reference/glossary#std-term-shard-key). Then, MongoDB distributes these chunks to shards. The shard key determines the distribution of chunks to shards. This can affect the performance of write operations in the cluster.

![Diagram of the shard key value space segmented into smaller ranges or chunks.](/images/sharding-range-based.bakedsvg.svg)

**Important:**

Update operations that affect a *single* document **must** include the [shard key](/docs/manual/reference/glossary#std-term-shard-key) or the `_id` field. Updates that affect multiple documents are more efficient in some situations if they have the [shard key](/docs/manual/reference/glossary#std-term-shard-key), but can be broadcast to all shards.

If the value of the shard key increases or decreases with every insert, all insert operations target a single shard. As a result, the capacity of a single shard becomes the limit for the insert capacity of the sharded cluster.

For more information, see [Sharding](/docs/manual/sharding) and [Bulk Write Operations.](/docs/manual/core/bulk-write-operations)

**See also:**

[Retryable Writes](/docs/manual/core/retryable-writes#std-label-retryable-writes)

## Change Streams and Orphan Documents

Starting in MongoDB 5.3, during [range migration](/docs/manual/core/sharding-balancer-administration#std-label-range-migration-procedure), [change stream](/docs/manual/changeStreams#std-label-changeStreams) events are not generated for updates to [orphaned documents.](/docs/manual/reference/glossary#std-term-orphaned-document)
