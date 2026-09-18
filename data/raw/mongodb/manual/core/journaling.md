> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Journaling

To provide durability in the event of a failure, MongoDB uses *write
ahead logging* to on-disk [journal](/docs/manual/reference/glossary#std-term-journal) files.

## Journaling and the WiredTiger Storage Engine

**Important:**

The *log* mentioned in this section refers to the WiredTiger write-ahead log (i.e. the journal) and not the MongoDB log file.

[WiredTiger](/docs/manual/core/wiredtiger#std-label-storage-wiredtiger) uses [checkpoints](/docs/manual/core/wiredtiger#std-label-storage-wiredtiger-checkpoints) to provide a consistent view of data on disk and allow MongoDB to recover from the last checkpoint. However, if MongoDB exits unexpectedly in between checkpoints, journaling is required to recover information that occurred after the last checkpoint.

**Note:**

Starting in MongoDB 6.1, journaling is always enabled. As a result, MongoDB removes the `storage.journal.enabled` option and the corresponding `--journal` and `--nojournal` command-line options.

With journaling, the recovery process:

1. Looks in the data files to find the identifier of the last checkpoint.

2. Searches in the journal files for the record that matches the identifier of the last checkpoint.

3. Apply the operations in the journal files since the last checkpoint.

### Journaling Process

With journaling, WiredTiger creates one journal record for each client initiated write operation. The journal record includes any internal write operations caused by the initial write. For example, an update to a document in a collection may result in modifications to the indexes; WiredTiger creates a single journal record that includes both the update operation and its associated index modifications.

MongoDB configures WiredTiger to use in-memory buffering for storing the journal records. Threads coordinate to allocate and copy into their portion of the buffer. All journal records up to 128 kB are buffered.

WiredTiger syncs the buffered journal records to disk upon any of the following conditions:

- For replica set members (primary and secondary members):

  - If a write operation includes or implies a write concern of [`j: true`.](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.j)

  - Additionally for secondary members, after every batch application of the oplog entries.

  **Note:**

  Write concern [`"majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) implies `j: true` if the [`writeConcernMajorityJournalDefault`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.writeConcernMajorityJournalDefault) is true.

- At every 100 milliseconds (See [`storage.journal.commitIntervalMs`](/docs/manual/reference/configuration-options#mongodb-setting-storage.journal.commitIntervalMs)).

- When WiredTiger creates a new journal file. Because MongoDB uses a journal file size limit of 100 MB, WiredTiger creates a new journal file approximately every 100 MB of data.

**Important:**

In between write operations, while the journal records remain in the WiredTiger buffers, updates can be lost following a hard shutdown of [`mongod`.](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod)

**See also:**

The [`serverStatus`](/docs/manual/reference/command/serverStatus#mongodb-dbcommand-dbcmd.serverStatus) command returns information on the WiredTiger journal statistics in the [`wiredTiger.log`](/docs/manual/reference/command/serverStatus#mongodb-serverstatus-serverstatus.wiredTiger.log) field.

### Journal Files

For the journal files, MongoDB creates a subdirectory named `journal` under the [`dbPath`](/docs/manual/reference/configuration-options#mongodb-setting-storage.dbPath) directory. WiredTiger journal files have names with the following format `WiredTigerLog.<sequence>` where `<sequence>` is a zero-padded number starting from `0000000001`.

#### Journal Records

Journal files contain a record per each client initiated write operation

- The journal record includes any internal write operations caused by the initial write. For example, an update to a document in a collection may result in modifications to the indexes; WiredTiger creates a single journal record that includes both the update operation and its associated index modifications.

- Each record has a unique identifier.

- The minimum journal record size for WiredTiger is 128 bytes.

#### Compression

By default, MongoDB configures WiredTiger to use snappy compression for its journaling data. To specify a different compression algorithm or no compression, use the [`storage.wiredTiger.engineConfig.journalCompressor`](/docs/manual/reference/configuration-options#mongodb-setting-storage.wiredTiger.engineConfig.journalCompressor) setting. For details, see [Change WiredTiger Journal Compressor.](/docs/manual/tutorial/manage-journaling#std-label-manage-journaling-change-wt-journal-compressor)

**Note:**

If a log record is less than or equal to 128 bytes, which is the minimum [log record size for WiredTiger](/docs/manual/core/journaling#std-label-wt-jouraling-record), WiredTiger does not compress that record.

#### Journal File Size Limit

WiredTiger journal files have a maximum size limit of approximately 100 MB. Once the file exceeds that limit, WiredTiger creates a new journal file.

WiredTiger automatically removes old journal files and maintains only the files needed to recover from the last checkpoint.  To determine how much disk space to set aside for journal files, consider the following:

- The default maximum size for a checkpoint is 2 GB

- Additional space may be required for MongoDB to write new journal files while recovering from a checkpoint

- MongoDB compresses journal files

- The time it takes to restore a checkpoint is specific to your use case

- If you override the maximum checkpoint size or disable compression, your calculations may be significantly different

For these reasons, it is difficult to calculate exactly how much additional space you need. Over-estimating disk space is always a safer approach.

**Important:**

If you do not set aside enough disk space for your journal files, the MongoDB server will crash.

#### Pre-Allocation

WiredTiger pre-allocates journal files.

## Journaling and the In-Memory Storage Engine

In MongoDB Enterprise, the [In-Memory Storage Engine](/docs/manual/core/inmemory) is part of general availability (GA). Because its data is kept in memory, there is no separate journal. Write operations with a write concern of [`j: true`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.j) are immediately acknowledged.

If any voting member of a replica set uses the [in-memory storage engine](/docs/manual/core/inmemory#std-label-storage-inmemory), you must set [`writeConcernMajorityJournalDefault`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.writeConcernMajorityJournalDefault) to `false`.

**Note:**

Starting in version 4.2 (and 4.0.13 and 3.6.14 ), if a replica set member uses the [in-memory storage engine](/docs/manual/core/inmemory#std-label-storage-inmemory) (voting or non-voting) but the replica set has [`writeConcernMajorityJournalDefault`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.writeConcernMajorityJournalDefault) set to true, the replica set member logs a startup warning.

With [`writeConcernMajorityJournalDefault`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.writeConcernMajorityJournalDefault) set to `false`, MongoDB does not wait for [`w: "majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) writes to be written to the on-disk journal before acknowledging the writes. As such, [`"majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) write operations could possibly roll back in the event of a transient loss (e.g. crash and restart) of a majority of nodes in a given replica set.

**See also:**

[In-Memory Storage Engine: Durability](/docs/manual/core/inmemory#std-label-inmemory-durability)
