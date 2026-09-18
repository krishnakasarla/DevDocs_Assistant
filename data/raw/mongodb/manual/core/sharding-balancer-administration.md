> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Sharded Cluster Balancer

The MongoDB balancer is a background process that monitors the amount of data on each [shard](/docs/manual/reference/glossary#std-term-shard) for each sharded collection. When the amount of data for a sharded collection on a given shard reaches specific [migration thresholds](/docs/manual/core/sharding-balancer-administration#std-label-sharding-migration-thresholds), the balancer attempts to automatically migrate data between shards and reach an even amount of data per shard while respecting the [zones](/docs/manual/core/zone-sharding#std-label-zone-sharding). By default, the balancer process is always enabled.

The balancing procedure for [sharded clusters](/docs/manual/reference/glossary#std-term-sharded-cluster) is entirely transparent to the user and application layer, though there may be some performance impact while the procedure takes place.

![Collection distributed across 3 shards triggers a chunk migration after reaching threshold of 2.](/images/sharding-migrating.bakedsvg.svg)

The balancer runs on the primary of the config server replica set (CSRS).

To configure collection balancing for a single collection, see [`configureCollectionBalancing`.](/docs/manual/reference/command/configureCollectionBalancing#mongodb-dbcommand-dbcmd.configureCollectionBalancing)

To manage the sharded cluster balancer, see [Manage Sharded Cluster Balancer.](/docs/manual/tutorial/manage-sharded-cluster-balancer#std-label-sharded-cluster-balancer)

## Balancer Internals

Range migrations carry some overhead in terms of bandwidth and workload, both of which can impact database performance. The [balancer](/docs/manual/reference/glossary#std-term-balancer) attempts to minimize the impact by:

- Restricting a shard to at most one migration at any given time. Specifically, a shard cannot participate in multiple data migrations at the same time. The balancer migrates ranges one at a time.

  MongoDB can perform parallel data migrations, but a shard can participate in at most one migration at a time. For a sharded cluster with *n* shards, MongoDB can perform at most *n/2* (rounded down) simultaneous migrations.

  See also [Asynchronous Range Migration Cleanup.](/docs/manual/core/sharding-balancer-administration#std-label-range-migration-queuing)

- Starting a balancing round only when the **difference in the amount
  of data** between the shard with the most data for a sharded collection and the shard with the least data for that collection reaches the [migration threshold.](/docs/manual/core/sharding-balancer-administration#std-label-sharding-migration-thresholds)

You can disable the balancer temporarily for maintenance, but leaving the balancer disabled for extended periods of time can degrade cluster performance. For more information, see [Disable the Balancer.](/docs/manual/tutorial/manage-sharded-cluster-balancer#std-label-sharding-balancing-disable-temporally)

You can also limit the window during which the balancer runs to prevent it from impacting production traffic. See [Schedule the Balancing Window](/docs/manual/tutorial/manage-sharded-cluster-balancer#std-label-sharding-schedule-balancing-window) for details.

**Note:**

The specification of the balancing window is relative to the local time zone of the primary of the config server replica set.

**See also:**

[Manage Sharded Cluster Balancer](/docs/manual/tutorial/manage-sharded-cluster-balancer#std-label-sharded-cluster-balancer)

### Adding and Removing Shards from the Cluster

Adding a shard to a cluster creates an imbalance, since the new shard has no data. While MongoDB begins migrating data to the new shard immediately, it can take some time before the cluster balances. See the [Add Shards to a Cluster](/docs/manual/tutorial/add-shards-to-shard-cluster#std-label-sharding-procedure-add-shard) tutorial for instructions on adding a shard to a cluster.

**Tip:**

Starting in MongoDB 8.0, you can reshard to the same key to move data. If your application meets the [resharding requirements](/docs/manual/core/sharding-reshard-a-collection#std-label-reshard-requirements), you can use the [`reshardCollection`](/docs/manual/reference/command/reshardCollection#mongodb-dbcommand-dbcmd.reshardCollection) command to redistribute data across the cluster to include the new shards. For more information, see [Reshard to the Same Shard Key](/docs/manual/core/reshard-to-same-key#std-label-reshard-to-same-key). This process is much faster than the alternative [Range Migration Procedure.](/docs/manual/core/sharding-balancer-administration#std-label-range-migration-procedure)

Removing a shard from a cluster creates a similar imbalance, since data residing on that shard must be redistributed throughout the cluster. While MongoDB begins draining a removed shard immediately, it can take some time before the cluster balances. *Do not* shutdown the servers associated to the removed shard during this process.

When you remove a shard in a cluster with an uneven chunk distribution, the balancer first removes the chunks from the draining shard and then balances the remaining uneven chunk distribution.

See the [Remove Shards from a Cluster](/docs/manual/tutorial/remove-shards-from-cluster#std-label-remove-shards-from-cluster-tutorial) tutorial for instructions on safely removing a shard from a cluster.

**See also:**

[`sh.balancerCollectionStatus()`](/docs/manual/reference/method/sh.balancerCollectionStatus#mongodb-method-sh.balancerCollectionStatus)

## Range Migration Procedure

All range migrations use the following procedure:

1. The balancer process sends the [`moveRange`](/docs/manual/reference/command/moveRange#mongodb-dbcommand-dbcmd.moveRange) command to the source shard.

2. The source starts the move when it receives an internal [`moveRange`](/docs/manual/reference/command/moveRange#mongodb-dbcommand-dbcmd.moveRange) command. During the migration process, operations to the range are sent to the source shard. The source shard is responsible for incoming write operations for the range.

3. The destination shard builds any indexes required by the source that do not exist on the destination.

4. The destination shard begins requesting documents in the range and starts receiving copies of the data. See also [Range Migration and Replication.](/docs/manual/core/sharding-balancer-administration#std-label-range-migration-replication)

5. After receiving the final document in the range, the destination shard starts a synchronization process to ensure that it has the changes to the migrated documents that occurred during the migration.

6. When fully synchronized, the source shard connects to the [config database](/docs/manual/reference/glossary#std-term-config-database) and updates the cluster metadata with the new location for the range.

7. After the source shard completes the update of the metadata, and once there are no open cursors on the range, the source shard deletes its copy of the documents.

   **Note:**

   If the balancer needs to perform additional chunk migrations from the source shard, the balancer can start the next chunk migration without waiting for the current migration process to finish this deletion step. See [Asynchronous Range Migration Cleanup.](/docs/manual/core/sharding-balancer-administration#std-label-chunk-migration-queuing)

**Warning:**

Starting in MongoDB version 8.2, long-running secondary reads in a sharded cluster may automatically terminate before orphaned document deletion following a chunk migration.

The [`terminateSecondaryReadsOnOrphanCleanup`](/docs/manual/reference/parameters#mongodb-parameter-param.terminateSecondaryReadsOnOrphanCleanup) parameter controls this behavior. To learn more about handling long-running secondary reads, see [Long-Running Secondary Reads in Sharded Clusters.](/docs/manual/core/long-running-secondary-reads#std-label-long-running-secondary-reads)

**See also:**

[`shardingStatistics.countDonorMoveChunkLockTimeout`](/docs/manual/reference/command/serverStatus#mongodb-serverstatus-serverstatus.shardingStatistics.countDonorMoveChunkLockTimeout)

### Migration Thresholds

To minimize the impact of balancing on the cluster, the [balancer](/docs/manual/reference/glossary#std-term-balancer) only begins balancing after the distribution of data for a sharded collection has reached certain thresholds.

A collection is considered balanced if the difference in data between shards (for that collection) is less than three times the configured [range size](/docs/manual/tutorial/modify-chunk-size-in-sharded-cluster#std-label-tutorial-modifying-range-size) for the collection. For the default range size of `128MB`, two shards must have a data size difference for a given collection of at least `384MB` for a migration to occur.

**See also:**

[`sh.balancerCollectionStatus()`](/docs/manual/reference/method/sh.balancerCollectionStatus#mongodb-method-sh.balancerCollectionStatus)

### Asynchronous Range Migration Cleanup

To migrate data from a shard, the balancer migrates the data one range at a time. However, the balancer does not wait for the current migration's delete phase to complete before starting the next range migration. See [Range Migration](/docs/manual/core/sharding-data-partitioning#std-label-sharding-range-migration) for the range migration process and the delete phase.

This queuing behavior allows shards to unload data more quickly in cases of heavily imbalanced cluster, such as when performing initial data loads without pre-splitting and when adding new shards.

This behavior also affects the [`moveRange`](/docs/manual/reference/command/moveRange#mongodb-dbcommand-dbcmd.moveRange) command, and migration scripts that use the [`moveRange`](/docs/manual/reference/command/moveRange#mongodb-dbcommand-dbcmd.moveRange) command may proceed more quickly.

In some cases, the delete phases may persist longer. Range migrations are enhanced to be more resilient in the event of a failover during the delete phase. Orphaned documents are cleaned up even if a replica set's primary crashes or restarts during this phase.

**Important:**

When the `_waitForDelete` field is set to `true`, MongoDB does not wait on the [`orphanCleanupDelaySecs`](/docs/manual/reference/parameters#mongodb-parameter-param.orphanCleanupDelaySecs) delay before performing the range deletion. If you use the `_waitForDelete` parameter and have any read operations occurring on secondaries, the read might terminate due to the migration's delete phase. To learn more, see [`terminateSecondaryReadsOnOrphanCleanup`.](/docs/manual/reference/parameters#mongodb-parameter-param.terminateSecondaryReadsOnOrphanCleanup)

For more information, see [Wait for Delete.](/docs/manual/tutorial/manage-sharded-cluster-balancer#std-label-wait-for-delete-setting)

**Note:**

Range deletion is a resource intensive operation that can result in significant cache and I/O stress as the cluster deletes the documents.

In cases where you plan to move a large amount of data, such as when adding shards to a cluster or during the initial distribution of a sharded collection across multiple shards, consider resharding the collection instead. Resharding operations don't require range cleanup, which makes them much less stressful on the cluster.

For more information, see [Reshard a Collection.](/docs/manual/core/sharding-reshard-a-collection#std-label-sharding-resharding)

### Range Migration and Replication

During range migration, the `_secondaryThrottle` value determines when the migration proceeds with next document in the range.

In the [`config.settings`](/docs/manual/reference/config-database#mongodb-data-config.settings) collection:

- If the `_secondaryThrottle` setting for the balancer is set to a [write concern](/docs/manual/reference/glossary#std-term-write-concern), each document moved during range migration must receive the requested acknowledgment before proceeding with the next document.

- If the `_secondaryThrottle` setting is unset, the migration process does not wait for replication to a secondary and instead continues with the next document.

To update the `_secondaryThrottle` parameter for the balancer, see [Secondary Throttle](/docs/manual/tutorial/manage-sharded-cluster-balancer#std-label-sharded-cluster-config-secondary-throttle) for an example.

Independent of any `_secondaryThrottle` setting, certain phases of the range migration have the following replication policy:

- MongoDB briefly pauses all application reads and writes to the collection being migrated to on the source shard before updating the config servers with the range location. MongoDB resumes application reads and writes after the update. The range move requires all writes to be acknowledged by majority of the members of the replica set both before and after committing the range move to config servers.

- When an outgoing migration finishes and cleanup occurs, all writes must be replicated to a majority of servers before further cleanup (from other outgoing migrations) or new incoming migrations can proceed.

To update the `_secondaryThrottle` setting in the [`config.settings`](/docs/manual/reference/config-database#mongodb-data-config.settings) collection, see [Secondary Throttle](/docs/manual/tutorial/manage-sharded-cluster-balancer#std-label-sharded-cluster-config-secondary-throttle) for an example.

### Maximum Number of Documents Per Range to Migrate

By default, MongoDB cannot move a range if the number of documents in the range is greater than 2 times the result of dividing the configured [range size](/docs/manual/core/sharding-data-partitioning#std-label-sharding-range-size) by the average document size. If MongoDB can move a sub-range of a chunk and reduce the size to less than that, the balancer does so by migrating a range. [`db.collection.stats()`](/docs/manual/reference/method/db.collection.stats#mongodb-method-db.collection.stats) includes the `avgObjSize` field, which represents the average document size in the collection.

For chunks that are [too large to migrate:](/docs/manual/core/sharding-balancer-administration#std-label-migration-chunk-size-limit)

- The balancer setting `attemptToBalanceJumboChunks` allows the balancer to migrate chunks too large to move as long as the chunks are not labeled [jumbo](/docs/manual/core/sharding-data-partitioning#std-label-jumbo-chunk). See [Balance Ranges that Exceed Size Limit](/docs/manual/tutorial/manage-sharded-cluster-balancer#std-label-balance-chunks-that-exceed-size-limit) for details.

  When issuing [`moveRange`](/docs/manual/reference/command/moveRange#mongodb-dbcommand-dbcmd.moveRange) and [`moveChunk`](/docs/manual/reference/command/moveChunk#mongodb-dbcommand-dbcmd.moveChunk) commands, it's possible to specify the [forceJumbo](/docs/manual/reference/command/moveRange#std-label-moverange-forceJumbo) option to allow for the migration of ranges that are too large to move. The ranges may or may not be labeled [jumbo.](/docs/manual/core/sharding-data-partitioning#std-label-jumbo-chunk)

### Range Deletion Performance Tuning

You can tune the performance impact of range deletions with [`rangeDeleterBatchSize`](/docs/manual/reference/parameters#mongodb-parameter-param.rangeDeleterBatchSize) and [`rangeDeleterBatchDelayMS`.](/docs/manual/reference/parameters#mongodb-parameter-param.rangeDeleterBatchDelayMS)

For example:

- To limit the number of documents deleted per batch, you can set [`rangeDeleterBatchSize`](/docs/manual/reference/parameters#mongodb-parameter-param.rangeDeleterBatchSize) to a small value such as `32`.

- To add an additional delay between batch deletions, you can set [`rangeDeleterBatchDelayMS`](/docs/manual/reference/parameters#mongodb-parameter-param.rangeDeleterBatchDelayMS) above the current default of `20` milliseconds.

**Note:**

If there are ongoing read operations or open cursors on the collection targeted for deletes, range deletion processes may not proceed.

### Change Streams and Orphan Documents

Starting in MongoDB 5.3, during [range migration](/docs/manual/core/sharding-balancer-administration#std-label-range-migration-procedure), [change stream](/docs/manual/changeStreams#std-label-changeStreams) events are not generated for updates to [orphaned documents.](/docs/manual/reference/glossary#std-term-orphaned-document)

## Shard Size

By default, MongoDB attempts to fill all available disk space with data on every shard as the data set grows. To ensure that the cluster always has the capacity to handle data growth, monitor disk usage as well as other performance metrics.

## Chunk Size and Balancing

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

For details about defragmenting sharded collections, see [Defragment Sharded Collections.](/docs/manual/core/defragment-sharded-collections#std-label-defragment-sharded-collections)

## Reshard to Balance

When you run the [`sh.shardCollection()`](/docs/manual/reference/method/sh.shardCollection#mongodb-method-sh.shardCollection) method, the balancer begins distributing the collection data to other shards in the cluster. A single shard can only participate in one chunk migration at a time. When MongoDB succeeds in copying a range of data from one shard to another, the range on the donor shard is marked for removal by the range deleter. This process is slow and resource intensive.

Starting in MongoDB 8.0, if your deployment meets the [resource requirements](/docs/manual/core/reshard-to-same-key#std-label-reshard-to-same-key-req), it's recommended that you use the [`sh.shardAndDistributeCollection()`](/docs/manual/reference/method/sh.shardAndDistributeCollection#mongodb-method-sh.shardAndDistributeCollection) method to shard the collection. This method wraps the [`shardCollection`](/docs/manual/reference/command/shardCollection#mongodb-dbcommand-dbcmd.shardCollection) and [`reshardCollection`](/docs/manual/reference/command/reshardCollection#mongodb-dbcommand-dbcmd.reshardCollection) commands to shard the collection and immediately reshard it to the same key. This causes MongoDB to rebalance data across the shards without waiting on the balancer.

For more information, see [Reshard to the Same Shard Key.](/docs/manual/core/reshard-to-same-key#std-label-reshard-to-same-key)
