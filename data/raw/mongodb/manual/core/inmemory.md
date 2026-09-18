> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# In-Memory Storage Engine for Self-Managed Deployments

The in-memory storage engine is included in MongoDB Enterprise. It is not available for MongoDB Community Edition.

Other than some metadata and diagnostic data, the in-memory storage engine does not maintain any on-disk data, including configuration data, indexes, user credentials, etc. By avoiding disk I/O, the in-memory storage engine allows for more predictable latency of database operations.

## Specify In-Memory Storage Engine

To select the in-memory storage engine, specify:

- `inMemory` for the [`--storageEngine`](/docs/manual/reference/program/mongod#std-option-mongod.--storageEngine) option, or the [`storage.engine`](/docs/manual/reference/configuration-options#mongodb-setting-storage.engine) setting if using a configuration file.

- `--dbpath`, or [`storage.dbPath`](/docs/manual/reference/configuration-options#mongodb-setting-storage.dbPath) if using a configuration file. Although the in-memory storage engine does not write data to the filesystem, it maintains in the `--dbpath` small metadata files and diagnostic data as well temporary files for building large indexes.

For example, from the command line:

```bash
mongod --storageEngine inMemory --dbpath <path>
```

Or, if using the [YAML configuration file format:](/docs/manual/reference/configuration-options)

```yaml
storage:
   engine: inMemory
   dbPath: <path>
```

See [inMemory Options](/docs/manual/reference/program/mongod#std-label-cli-mongod-inmemory) for configuration options specific to this storage engine. Most [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) configuration options are available for use with in-memory storage engine except for those options that are related to data persistence, such as journaling or encryption at rest configuration.

**Warning: The in-memory storage engine does not persist data after process shutdown.**

## Transaction (Read and Write) Concurrency

Starting in version 7.0, MongoDB uses a default algorithm to dynamically adjust the maximum number of concurrent storage engine transactions, or read and write tickets. The dynamic concurrent storage engine transaction algorithm optimizes database throughput during cluster overload.

**Note:**

The dynamic algorithm also results in lower overall ticket usage, even under normal conditions, because the algorithm starts with a much lower baseline number of available tickets. As a result, when upgrading to MongoDB 7.0, you may observe a significant drop in ticket usage, which is expected behavior.

The maximum number of concurrent storage engine transactions, or read and write tickets, never exceeds 128 read tickets and 128 write tickets and may differ across nodes in a cluster. The maximum number of read tickets and write tickets within a single node are always equal.

To specify a maximum number of read and write transactions, or read and write tickets, that the dynamic maximum can not exceed, use [`storageEngineConcurrentReadTransactions`](/docs/manual/reference/parameters#mongodb-parameter-param.storageEngineConcurrentReadTransactions) and [`storageEngineConcurrentWriteTransactions`.](/docs/manual/reference/parameters#mongodb-parameter-param.storageEngineConcurrentWriteTransactions)

If you want to disable the dynamic concurrent storage engine transactions algorithm, file a support request to work with a MongoDB Technical Services Engineer.

## Document Level Concurrency

The in-memory storage engine uses *document-level* concurrency control for write operations. As a result, multiple clients can modify different documents of a collection at the same time.

## Memory Use

In-memory storage engine requires that all its data (including indexes, oplog if [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instance is part of a replica set, etc.) must fit into the specified [`--inMemorySizeGB`](/docs/manual/reference/program/mongod#std-option-mongod.--inMemorySizeGB) command-line option or [`storage.inMemory.engineConfig.inMemorySizeGB`](/docs/manual/reference/configuration-options#mongodb-setting-storage.inMemory.engineConfig.inMemorySizeGB) setting in the [YAML configuration file.](/docs/manual/reference/configuration-options#std-label-configuration-options)

By default, the in-memory storage engine uses 50% of physical RAM minus 1 GB.

If a write operation would cause the data to exceed the specified memory size, MongoDB returns with the error:

```bash
"WT_CACHE_FULL: operation would overflow cache"
```

To specify a new size, use the [`storage.inMemory.engineConfig.inMemorySizeGB`](/docs/manual/reference/configuration-options#mongodb-setting-storage.inMemory.engineConfig.inMemorySizeGB) setting in the [YAML configuration file format:](/docs/manual/reference/configuration-options)

```yaml
storage:
   engine: inMemory
   dbPath: <path>
   inMemory:
      engineConfig:
         inMemorySizeGB: <newSize>
```

Or use the command-line option [`--inMemorySizeGB`:](/docs/manual/reference/program/mongod#std-option-mongod.--inMemorySizeGB)

```bash
mongod --storageEngine inMemory --dbpath <path> --inMemorySizeGB <newSize>
```

## Durability

The in-memory storage engine is non-persistent and does not write data to a persistent storage. Non-persisted data includes application data and system data, such as users, permissions, indexes, replica set configuration, sharded cluster configuration, etc.

As such, the concept of [journal](/docs/manual/reference/glossary#std-term-journal) or waiting for data to become [durable](/docs/manual/reference/glossary#std-term-durable) does not apply to the in-memory storage engine.

If any voting member of a replica set uses the [in-memory storage engine](/docs/manual/core/inmemory#std-label-storage-inmemory), you must set [`writeConcernMajorityJournalDefault`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.writeConcernMajorityJournalDefault) to `false`.

**Note:**

Starting in version 4.2 (and 4.0.13 and 3.6.14 ), if a replica set member uses the [in-memory storage engine](/docs/manual/core/inmemory#std-label-storage-inmemory) (voting or non-voting) but the replica set has [`writeConcernMajorityJournalDefault`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.writeConcernMajorityJournalDefault) set to true, the replica set member logs a startup warning.

With [`writeConcernMajorityJournalDefault`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.writeConcernMajorityJournalDefault) set to `false`, MongoDB does not wait for [`w: "majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) writes to be written to the on-disk journal before acknowledging the writes. As such, [`"majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) write operations could possibly roll back in the event of a transient loss (e.g. crash and restart) of a majority of nodes in a given replica set.

Write operations that specify a write concern [`journaled`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.j) are acknowledged immediately. When an [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instance shuts down, either as result of the [`shutdown`](/docs/manual/reference/command/shutdown#mongodb-dbcommand-dbcmd.shutdown) command or due to a system error, recovery of in-memory data is impossible.

## Transactions

Transactions are supported on replica sets and sharded clusters where:

- the primary uses the [WiredTiger](/docs/manual/core/wiredtiger#std-label-storage-wiredtiger) storage engine, and

- the secondary members use either the WiredTiger storage engine or the [in-memory](/docs/manual/core/inmemory#std-label-storage-inmemory) storage engines.

**Note:**

You cannot run transactions on a sharded cluster that has a shard with [`writeConcernMajorityJournalDefault`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.writeConcernMajorityJournalDefault) set to `false`, such as a shard with a voting member that uses the [in-memory storage engine.](/docs/manual/core/inmemory#std-label-storage-inmemory)

## Deployment Architectures

In addition to running as standalones, [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instances that use in-memory storage engine can run as part of a replica set or part of a sharded cluster.

### Replica Set

You can deploy [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instances that use in-memory storage engine as part of a replica set. For example, as part of a three-member replica set, you could have:

- two [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instances run with in-memory storage engine.

- one [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instance run with [WiredTiger](/docs/manual/core/wiredtiger) storage engine. Configure the WiredTiger member as a hidden member (i.e. [`hidden: true`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.members-n-.hidden) and [`priority: 0`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.members-n-.priority)).

With this deployment model, only the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instances running with the in-memory storage engine can become the primary. Clients connect only to the in-memory storage engine [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instances. Even if both [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instances running in-memory storage engine crash and restart, they can sync from the member running WiredTiger. The hidden [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instance running with WiredTiger persists the data to disk, including the user data, indexes, and replication configuration information.

**Note:**

In-memory storage engine requires that all its data (including oplog if [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) is part of replica set, etc.) fit into the specified [`--inMemorySizeGB`](/docs/manual/reference/program/mongod#std-option-mongod.--inMemorySizeGB) command-line option or [`storage.inMemory.engineConfig.inMemorySizeGB`](/docs/manual/reference/configuration-options#mongodb-setting-storage.inMemory.engineConfig.inMemorySizeGB) setting. See [Memory Use.](/docs/manual/core/inmemory#std-label-inmemory-memory-use)

### Sharded Cluster

You can deploy [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instances that use an in-memory storage engine as part of a [sharded cluster](/docs/manual/reference/glossary#std-term-sharded-cluster). The in-memory storage engine avoids disk I/O to allow for more predictable database operation latency. In a sharded cluster, a [shard](/docs/manual/reference/glossary#std-term-shard) can consist of a single [`mongod`](/docs/manual/reference/program/mongod#std-program-mongod) instance or a [replica set](/docs/manual/reference/glossary#std-term-replica-set). For example, you could have one shard that consists of the following replica set:

- two [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instances run with in-memory storage engine

- one [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instance run with [WiredTiger](/docs/manual/core/wiredtiger) storage engine. Configure the WiredTiger member as a hidden member (i.e. [`hidden: true`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.members-n-.hidden) and [`priority: 0`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.members-n-.priority)).

To this shard, add the [`tag`](/docs/manual/reference/method/sh.addShardTag#mongodb-method-sh.addShardTag) `inmem`. For example, if this shard has the name `shardC`, connect to the [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) and run [`sh.addShardTag()`.](/docs/manual/reference/method/sh.addShardTag#mongodb-method-sh.addShardTag)

For example,

```javascript
sh.addShardTag("shardC", "inmem")
```

To the other shards, add a separate tag `persisted` .

```javascript
sh.addShardTag("shardA", "persisted")
sh.addShardTag("shardB", "persisted")
```

For each sharded collection that should reside on the `inmem` shard, [`assign to the entire chunk range`](/docs/manual/reference/method/sh.addTagRange#mongodb-method-sh.addTagRange) the tag `inmem`:

```javascript
sh.addTagRange("test.analytics", { shardKey: MinKey }, { shardKey: MaxKey }, "inmem")
```

For each sharded collection that should reside across the `persisted` shards, [`assign to the entire chunk range`](/docs/manual/reference/method/sh.addTagRange#mongodb-method-sh.addTagRange) the tag `persisted`:

```javascript
sh.addTagRange("salesdb.orders", { shardKey: MinKey }, { shardKey: MaxKey }, "persisted")
```

For the `inmem` shard, create a database or move the database.

**Note:**

Read concern level [`"snapshot"`](/docs/manual/reference/read-concern-snapshot#mongodb-readconcern-readconcern.-snapshot-) is not officially supported with the in-memory storage engine.
