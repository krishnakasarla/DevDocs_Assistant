> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Defragment Sharded Collections

Fragmentation is where a sharded collection's data is broken up into an unnecessarily large number of small chunks. This can increase operation times of CRUD operations run on that collection. Defragmentation reduces the number of chunks by merging smaller chunks into larger ones, resulting in lower CRUD operation times.

If CRUD operation times are acceptable, you don't need to defragment collections.

The following table summarizes defragmentation information for various MongoDB versions.

| MongoDB Version | Description |
| --- | --- |
| MongoDB 7.0 and later | Chunks are automatically merged. Performance improvements from defragmenting a collection in MongoDB 7.0 are lower compared to MongoDB 6.0. Typically, you don't need to defragment collections starting in MongoDB 7.0. |
| MongoDB 6.0 and earlier than 7.0 | Defragment collections only if you experience CRUD operation delays when the balancer migrates chunks or a node starts. Starting in MongoDB 6.0, high write traffic should not cause fragmentation. Chunk migrations cause fragmentation. |
| Earlier than MongoDB 6.0 | Defragment collections only if you experience longer CRUD operation times during metadata updates. For MongoDB versions earlier than 6.0, a sharded collection becomes fragmented when the collection size grows significantly because of many insert or update operations. |

To defragment a sharded collection, use the [`configureCollectionBalancing`](/docs/manual/reference/command/configureCollectionBalancing#mongodb-dbcommand-dbcmd.configureCollectionBalancing) command's `defragmentCollection` option. The option is available starting in MongoDB 6.0.

## Before you Begin

Consider these issues before you defragment collections:

- Defragmentation might cause many metadata updates on the shards. If your CRUD operations are already taking longer than usual during migrations, you should only run defragmentation during a [shard balancing window](/docs/manual/tutorial/manage-sharded-cluster-balancer#std-label-sharding-schedule-balancing-window) to reduce the system workload.

- If defragmentation is impacting workload and CRUD latency on the cluster, you can reduce the impact using the [`chunkDefragmentationThrottlingMS`](/docs/manual/reference/parameters#mongodb-parameter-param.chunkDefragmentationThrottlingMS) parameter.

- Merged chunks lose their placement history.

  - This means that while defragmentation is running, snapshot reads and indirectly, transactions, could fail with stale chunk history errors.

  - Placement history records the shards that a chunk was stored on. Defragmentation erases the placement history and some operations could fail, but will typically resolve after around five minutes.

- Defragmentation affects the locality of the documents in a collection by moving data between shards. If a collection has ranges of data that are frequently accessed, after defragmenting the collection it is possible that the frequently accessed data will be on one shard. This might decrease the performance of CRUD operations by placing the workload on one shard instead of multiple shards.

## Tasks

- [Manually start defragmenting a sharded collection](/docs/manual/core/defragment-sharded-collections/start-defragmenting-sharded-collection#std-label-start-defragmenting-sharded-collection)

- [Monitor defragmentation of a sharded collection](/docs/manual/core/defragment-sharded-collections/monitor-defragmentation-sharded-collection#std-label-monitor-defragmentation-sharded-collection)

- [Manually stop defragmenting a sharded collection](/docs/manual/core/defragment-sharded-collections/stop-defragmenting-sharded-collection#std-label-stop-defragmenting-sharded-collection)

**Note:**

Typically, you should use a [shard balancing window](/docs/manual/tutorial/manage-sharded-cluster-balancer#std-label-sharding-schedule-balancing-window) to specify when the balancer runs instead of manually starting and stopping defragmentation.

## Details

This section describes additional details related to defragmenting sharded collections.

### Configure Collection Balancing Status

The `defragmentCollection` field returned by the [`configureCollectionBalancing`](/docs/manual/reference/command/configureCollectionBalancing#mongodb-dbcommand-dbcmd.configureCollectionBalancing) command is only `true` when defragmentation is running.

After defragmentation automatically ends or you manually stop defragmentation, the `defragmentCollection` field is removed from the returned document.

### Operations

Secondary node reads are permitted during defragmentation, but might take longer to complete until metadata updates on the primary node are replicated to the secondary nodes.

### Chunk Size, Balancing, and Defragmentation

For details about the MongoDB balancer, see [Sharded Cluster Balancer.](/docs/manual/core/sharding-balancer-administration#std-label-sharding-balancing)

For an introduction to `chunkSize`, see [Modify Range Size in a Sharded Cluster.](/docs/manual/tutorial/modify-chunk-size-in-sharded-cluster#std-label-tutorial-modifying-chunk-size)

When the collection data shared between two shards differs by three or more times the configured `chunkSize` setting, the balancer migrates chunks between the shards.

For example, if `chunkSize` is 128 MB and the collection data differs by 384 MB or more, the balancer migrates chunks between the shards.

When chunks are moved, split, or merged, the shard metadata is updated after the chunk operation is committed by a [config server](/docs/manual/core/sharded-cluster-config-servers#std-label-sharding-config-server). Shards not involved in the chunk operation are also updated with new metadata.

The time for the shard metadata update is proportional to the size of the routing table. CRUD operations on the collection are temporarily blocked while the shard metadata is updated, and a smaller routing table means shorter CRUD operation delays.

Defragmenting a collection reduces the number of chunks and the time to update the chunk metadata.

To reduce the system workload, configure the balancer to run only at a specific time using a [shard balancing window](/docs/manual/tutorial/manage-sharded-cluster-balancer#std-label-sharding-schedule-balancing-window). Defragmentation runs during the balancing window time period.

You can use the [`chunkDefragmentationThrottlingMS`](/docs/manual/reference/parameters#mongodb-parameter-param.chunkDefragmentationThrottlingMS) parameter to limit the rate of split and merge commands run by the balancer.

You can start and stop defragmentation at any time.

You can also set a [shard zone](/docs/manual/core/zone-sharding#std-label-zone-sharding). A shard zone is based on the shard key, and you can associate each zone with one or more shards in a cluster.

A sharded cluster only splits chunks when chunks must be migrated. This means the chunk size may exceed `chunkSize`. Larger chunks reduce the number of chunks on a shard and improve performance because the time to update the shard metadata is reduced. For example, you might see a 1 TB chunk on a shard even though you have set `chunkSize` to 256 MB.

`chunkSize` affects the following:

- Maximum amount of data the balancer attempts to migrate between two shards in a single chunk migration operation.

- Amount of data migrated during defragmentation.

## Learn More

- Introduction to sharding, see [Sharding](/docs/manual/sharding#std-label-sharding-introduction)

- Partition data with chunks, see [Data Partitioning with Chunks](/docs/manual/core/sharding-data-partitioning#std-label-sharding-data-partitioning)

- Configure collection balancing, see [`configureCollectionBalancing`](/docs/manual/reference/command/configureCollectionBalancing#mongodb-dbcommand-dbcmd.configureCollectionBalancing)

- Examine balancer collection status, see [`balancerCollectionStatus`](/docs/manual/reference/command/balancerCollectionStatus#mongodb-dbcommand-dbcmd.balancerCollectionStatus)

- Configure shard balancing windows, see [Schedule the Balancing Window](/docs/manual/tutorial/manage-sharded-cluster-balancer#std-label-sharding-schedule-balancing-window)

- Monitor shards using MongoDB Atlas, see [Review Sharded Clusters](https://www.mongodb.com/docs/atlas/review-sharded-cluster-metrics/#review-sharded-clusters/)
