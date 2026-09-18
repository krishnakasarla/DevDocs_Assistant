> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

<!--
Tab options on this page. Append to the .md URL to filter:
  ?tabs=<id,...>   select specific tabs (e.g. ?tabs=nodejs,shell)
  ?allTabs=true    include every tab
  (no param)       default: one tab per tabset

Available tabs:
  other tabs: firstpass, second pass
-->

# Replica Set Data Synchronization

To maintain up-to-date copies of the shared data set, secondary members of a replica set [sync](/docs/manual/reference/glossary#std-term-sync) or replicate data from a source member. MongoDB uses two forms of data synchronization: initial sync to populate new members with the full data set, and replication to apply ongoing changes to the entire data set.

## Initial Sync

Initial sync copies all the data from the source member of the replica set to a destination member. See [Initial Sync Source Selection](/docs/manual/core/replica-set-sync#std-label-replica-set-initial-sync-source-selection) for more information on source member selection criteria.

The `local` database stores the [oplog](/docs/manual/reference/glossary#std-term-oplog) data that the initial sync process uses. Ensure the destination member has enough space in the `local` database to store the oplog data for the initial sync process to complete.

**Note:**

During the initial sync, MongoDB truncates the oplog on the destination member. This oplog truncation can impact processes such as [change streams](/docs/manual/changeStreams#std-label-changeStreams) and [Atlas Stream Processing checkpoints](https://www.mongodb.com/docs/atlas/atlas-stream-processing/architecture/#std-label-atlas-sp-checkpoints) that depend on oplog data.

You can specify the preferred initial sync source using the [`initialSyncSourceReadPreference`](/docs/manual/reference/parameters#mongodb-parameter-param.initialSyncSourceReadPreference) parameter. This parameter can only be specified when starting the [`mongod`.](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod)

Starting in MongoDB 5.2, initial syncs can be *logical* or *file copy
based*.

**Note: Cloud-based Initial Sync Disambiguation**

For self-managed deployments, initial sync is the process that MongoDB uses to add a new node to a replica set. This is different from [cloud-based initial syncs](https://www.mongodb.com/docs/atlas/scale-cluster/#std-label-cloud-based-initial-sync) available in MongoDB Atlas, which leverage your cloud provider's native capabilities to create a snapshot of the source node's data and restore it to the new node.

### Logical Initial Sync Process

When you perform a logical initial sync, MongoDB:

1. Clones all databases except the [local](/docs/manual/reference/local-database#std-label-replica-set-local-database) database. To clone, the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) scans every collection in each source member database and inserts all data into its own copies of these collections.

2. In parallel with the data clone, `mongod` builds all collection indexes as it copies all the documents for each collection.

3. Applies oplog records that buffered during the data copy.

4. Applies all changes to the data set. Using the oplog from the source member, the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) updates its data set to reflect the current state of the replica set.

**Important:**

- During steps 1 and 2, the `mongod` pulls newly added oplog records and stores them in a temporary collection in the `local` database. Ensure that the target member has enough disk space in the `local` database to temporarily store these oplog records for the duration of this data copy stage.

- During steps 3 and 4, the syncing node checks for continuity of operations against the source node. If a gap is found, restart the initial sync from the beginning. To avoid this, make sure that the size of the oplog provisioned provides enough of an oplog window to cover the time it takes for steps 3 and 4 to complete.

When the initial sync finishes, the member transitions from [`STARTUP2`](/docs/manual/reference/replica-states#mongodb-replstate-replstate.STARTUP2) to [`SECONDARY`.](/docs/manual/reference/replica-states#mongodb-replstate-replstate.SECONDARY)

To perform an initial sync, see [Resync a Member of a Self-Managed Replica Set.](/docs/manual/tutorial/resync-replica-set-member#std-label-resync-replica-member)

### File Copy Based Initial Sync

*Available in MongoDB Enterprise only.*

File copy based initial sync runs the initial sync process by copying and moving files on the file system. This sync method can be faster than [logical initial sync.](/docs/manual/core/replica-set-sync#std-label-replica-set-initial-sync-logical)

**Important: File copy based initial sync may cause inaccurate counts**

After file copy based initial sync completes, if you run the [`count()`](/docs/manual/reference/method/db.collection.count#mongodb-method-db.collection.count) method without a query predicate, the count of documents returned may be inaccurate.

A `count` method without a query predicate looks like this: `db.<collection>.count()`.

To learn more, see [Inaccurate Counts Without Query Predicate.](/docs/manual/reference/method/db.collection.count#std-label-count-method-behavior-query-predicate)

#### Enable File Copy Based Initial Sync

To enable file copy based initial sync, set the [`initialSyncMethod`](/docs/manual/reference/parameters#mongodb-parameter-param.initialSyncMethod) parameter to `fileCopyBased` on the destination member for the initial sync. This parameter can only be set at startup.

#### Behavior

File copy based initial sync replaces the `local` database of the destination member with the `local` database of the source member when syncing.

#### Limitations

- During a file copy based initial sync:

  - You cannot run backups on either the source member or the destination member.

  - You cannot write to the `local` database on the destination member.

- You can only run an initial sync from one source member at a time.

- When using the encrypted storage engine, MongoDB uses the source member key to encrypt the destination.

### Initial Sync on NVMe Clusters

You must perform an initial sync on clusters that use the local Non-Volatile Memory Express ([NVMe](/docs/manual/reference/glossary#std-term-NVMe)) SSD storage option, including if you're using Atlas [auto-scaling](https://www.mongodb.com/docs/atlas/cluster-autoscaling/#std-label-cluster-autoscaling). Atlas NVMe clusters auto-scale to the next higher tier when 90% of the storage space is full. An initial sync takes longer to complete compared to subsequent syncs, and reduces the performance of the [primary](/docs/manual/reference/glossary#std-term-primary) from which the data is read.

### Fault Tolerance

If a destination member performing initial sync encounters a persistent network error during the sync process, the destination member restarts the initial sync process from the beginning.

A destination member performing initial sync can attempt to resume the sync process if interrupted by a temporary network error, collection drop, or collection rename.

By default, the destination member tries to resume initial sync for 24 hours. You can use the [`initialSyncTransientErrorRetryPeriodSeconds`](/docs/manual/reference/parameters#mongodb-parameter-param.initialSyncTransientErrorRetryPeriodSeconds) server parameter to control the amount of time the destination member attempts to resume initial sync. If the destination member cannot successfully resume the initial sync process during the configured time period, it selects a new healthy source member from the replica set and restarts the initial synchronization process from the beginning.

The secondary attempts to restart the initial sync up to `10` times before returning a fatal error.

### Initial Sync Source Selection

Initial sync source selection depends on the value of the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) startup parameter [`initialSyncSourceReadPreference`:](/docs/manual/reference/parameters#mongodb-parameter-param.initialSyncSourceReadPreference)

- For [`initialSyncSourceReadPreference`](/docs/manual/reference/parameters#mongodb-parameter-param.initialSyncSourceReadPreference) set to [`primary`](/docs/manual/reference/glossary#std-term-primary) (default if [`chainingAllowed`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.settings.chainingAllowed) is disabled), select the [primary](/docs/manual/reference/glossary#std-term-primary) as the source member. If the primary is unavailable or unreachable, log an error and periodically check for primary availability.

- For [`initialSyncSourceReadPreference`](/docs/manual/reference/parameters#mongodb-parameter-param.initialSyncSourceReadPreference) set to [`primaryPreferred`](/docs/manual/core/read-preference#mongodb-readmode-primaryPreferred) (default for voting replica set members), attempt to select the [primary](/docs/manual/reference/glossary#std-term-primary) as the source member. If the primary is unavailable or unreachable, perform sync source member selection from the remaining replica set members.

- For all other supported read modes, perform sync source member selection from the destination members.

Members performing initial source member selection make two passes through the list of all replica set members:

### First Pass

The member applies the following criteria to each replica set member when making the first pass for selecting a initial source member:

- The source member *must* be in the [`PRIMARY`](/docs/manual/reference/replica-states#mongodb-replstate-replstate.PRIMARY) or [`SECONDARY`](/docs/manual/reference/replica-states#mongodb-replstate-replstate.SECONDARY) replication state.

- The source member *must* be online and reachable.

- If [`initialSyncSourceReadPreference`](/docs/manual/reference/parameters#mongodb-parameter-param.initialSyncSourceReadPreference) is [`secondary`](/docs/manual/reference/glossary#std-term-secondary) or [`secondaryPreferred`](/docs/manual/core/read-preference#mongodb-readmode-secondaryPreferred), the source member *must* be a [secondary.](/docs/manual/reference/glossary#std-term-secondary)

- The source member *must* be [`visible`.](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.members-n-.hidden)

- The source member *must* be within [`maxSyncSourceLagSecs`](/docs/manual/reference/parameters#mongodb-parameter-param.maxSyncSourceLagSecs) (default `30`) seconds of the newest oplog entry on the primary.

- If the member [`builds indexes`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.members-n-.buildIndexes), the source member *must* build indexes.

- If the member [`votes`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.members-n-.votes) in replica set elections, the source member *must* also vote.

- If the member is *not* a [`delayed member`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.members-n-.secondaryDelaySecs), the source member *must not* be delayed.

- If the member *is* a [`delayed member`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.members-n-.secondaryDelaySecs), the source member must have a shorter configured delay.

- The source member *must* be faster than the current best sync source.

If no candidate source member remains after the first pass, the member performs a second pass with relaxed criteria. See Sync Source Selection (Second Pass).

If the destination member cannot select a source member after two passes, it logs an error and waits `1` second before restarting the selection process. The secondary [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) can restart the initial sync source selection process up to `10` times before exiting with an error.

### Oplog Window

The [oplog window](/docs/manual/reference/glossary#std-term-oplog-window) must be long enough so that a destination member can fetch any new [oplog](/docs/manual/reference/glossary#std-term-oplog) entries that occur between the start and end of the [Logical Initial Sync Process](/docs/manual/core/replica-set-sync#std-label-replica-set-initial-sync-logical). If the window is too short, some entries may fall off the `oplog` before the destination member can apply them.

Size the `oplog` with additional time to accommodate changes that may occur during initial syncs.

For more information, see [Oplog Size.](/docs/manual/core/replica-set-oplog#std-label-replica-set-oplog-sizing)

## Replication

Destination members replicate data continuously after the initial sync. Destination members copy the [oplog](/docs/manual/core/replica-set-oplog#std-label-replica-set-oplog) from the source member and apply these operations in an asynchronous process.

Destination members automatically change their source member as needed based on changes in the ping time and state of other members' replication. See [Replication Sync Source Selection](/docs/manual/core/replica-set-sync#std-label-replica-set-replication-sync-source-selection) for more information on source member selection criteria.

### Streaming Replication

Source members send a continuous stream of [oplog](/docs/manual/core/replica-set-oplog#std-label-replica-set-oplog) entries to their destination members. Streaming replication mitigates replication lag in high-load and high-latency networks. It also:

- Reduces staleness for reads from secondaries.

- Reduces risk of losing write operations with [w: 1](/docs/manual/reference/write-concern#std-label-wc-w) due to primary failover.

- Reduces latency on write operations with [`w: "majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) and [w: >1](/docs/manual/reference/write-concern#std-label-wc-w) (that is, any write concern that requires waiting for replication).

Use the [`oplogFetcherUsesExhaust`](/docs/manual/reference/parameters#mongodb-parameter-param.oplogFetcherUsesExhaust) startup parameter to disable streaming replication and using the older replication behavior. Set the [`oplogFetcherUsesExhaust`](/docs/manual/reference/parameters#mongodb-parameter-param.oplogFetcherUsesExhaust) parameter to `false` only if there are any resource constraints on the source member or if you wish to limit MongoDB's usage of network bandwidth for replication.

### Multithreaded Replication

MongoDB applies write operations in batches using multiple threads to improve concurrency. MongoDB groups batches by document ID ([WiredTiger](/docs/manual/core/wiredtiger#std-label-storage-wiredtiger)) and simultaneously applies each group of operations using a different thread. MongoDB always applies write operations to a given document in their original write order.

Read operations that [target secondaries](/docs/manual/core/read-preference#std-label-replica-set-read-preference) and are configured with a [read concern](/docs/manual/reference/read-concern#std-label-read-concern) level of [`"local"`](/docs/manual/reference/read-concern-local#mongodb-readconcern-readconcern.-local-) or  [`"majority"`](/docs/manual/reference/read-concern-majority#mongodb-readconcern-readconcern.-majority-) read from a [WiredTiger](/docs/manual/core/wiredtiger#std-label-storage-wiredtiger) snapshot of the data if the read takes place on a secondary where replication batches are being applied.

Reading from a snapshot guarantees a consistent view of the data, and allows the read to occur simultaneously with the ongoing replication without the need for a lock. As a result, secondary reads requiring these read concern levels no longer need to wait for replication batches to be applied, and can be handled as they are received.

### Flow Control

Administrators can limit the rate at which the primary applies its writes with the goal of keeping the [`majority committed`](/docs/manual/reference/command/replSetGetStatus#mongodb-data-replSetGetStatus.optimes.lastCommittedOpTime) lag under a configurable maximum value [`flowControlTargetLagSeconds`.](/docs/manual/reference/parameters#mongodb-parameter-param.flowControlTargetLagSeconds)

By default, flow control is [`enabled`.](/docs/manual/reference/parameters#mongodb-parameter-param.enableFlowControl)

For more information, see [Flow Control.](/docs/manual/tutorial/troubleshoot-replica-sets#std-label-flow-control)

### Replication Sync Source Selection

Replication source member selection depends on the replica set [`chaining`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.settings.chainingAllowed) setting:

- With chaining enabled (default), perform source member selection from the destination members.

- With chaining disabled, select the [primary](/docs/manual/reference/glossary#std-term-primary) as the source member. If the primary is unavailable or unreachable, log an error and periodically check for primary availability.

Members performing replication source member selection make two passes through the list of all replica set members:

### First Pass

The member applies the following criteria to each replica set member when making the first pass for selecting a source member:

- The source member *must* be in the [`PRIMARY`](/docs/manual/reference/replica-states#mongodb-replstate-replstate.PRIMARY) or [`SECONDARY`](/docs/manual/reference/replica-states#mongodb-replstate-replstate.SECONDARY) replication state.

- The source member *must* be online and reachable.

- The source member *must* have newer oplog entries than the member. That is, the source member must be *ahead* of the member.

- The source member *must* be [`visible`.](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.members-n-.hidden)

- The source member *must* be within [`maxSyncSourceLagSecs`](/docs/manual/reference/parameters#mongodb-parameter-param.maxSyncSourceLagSecs) (default `30`) seconds of the newest oplog entry on the primary.

- If the member [`builds indexes`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.members-n-.buildIndexes), the source member *must* build indexes.

- If the member [`votes`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.members-n-.votes) in replica set elections, the source member *must* also vote.

- If the member is *not* a [`delayed member`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.members-n-.secondaryDelaySecs), the source member *must not* be delayed.

- If the member *is* a [`delayed member`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.members-n-.secondaryDelaySecs), the source member must have a shorter configured delay.

- The source member *must* be faster than the current best sync source.

If no candidate source members remain after the first pass, the member performs a second pass with relaxed criteria. See the Sync Source Selection (Second Pass).

If the member cannot select a sync source after two passes, it logs an error and waits `1` second before restarting the selection process.

The number of times a source member can be changed per hour is configurable by setting the [`maxNumSyncSourceChangesPerHour`](/docs/manual/reference/parameters#mongodb-parameter-param.maxNumSyncSourceChangesPerHour) parameter.

**Note:**

The startup parameter [`initialSyncSourceReadPreference`](/docs/manual/reference/parameters#mongodb-parameter-param.initialSyncSourceReadPreference) takes precedence over the replica set's [`settings.chainingAllowed`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.settings.chainingAllowed) setting when selecting an initial sync source member. After a replica set member successfully performs initial sync, it defers to the value of [`chainingAllowed`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.settings.chainingAllowed) when selecting a source member.

See [Initial Sync Source Selection](/docs/manual/core/replica-set-sync#std-label-replica-set-initial-sync-source-selection) for more information on initial sync source selection.
