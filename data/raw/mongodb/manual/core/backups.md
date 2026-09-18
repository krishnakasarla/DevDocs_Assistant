> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Backup Methods for a Self-Managed Deployment

When deploying MongoDB in production, have a backup and restore strategy to protect against data loss.

This page covers backup methods for [self-managed](/docs/manual/reference/glossary#std-term-self-managed) deployments.

To learn more about Backup Methods for deployments hosted in MongoDB Atlas, see [Back Up, Restore, and Archive Data](https://www.mongodb.com/docs/atlas/backup-restore-cluster/).

## Back Up with MongoDB Cloud Manager or Ops Manager

MongoDB Cloud Manager is a hosted backup, monitoring, and automation service for MongoDB. [MongoDB Cloud Manager](https://www.mongodb.com/products/tools/cloud-manager) supports backing up and restoring [replica sets](/docs/manual/reference/glossary#std-term-replica-set) and [sharded clusters](/docs/manual/reference/glossary#std-term-sharded-cluster) from a graphical user interface.

### MongoDB Cloud Manager

**Important:**

To back up your replica sets and sharded clusters using MongoDB Cloud Manager, you must be using MongoDB Enterprise Server. For more information, see [Install MongoDB Enterprise.](/docs/manual/administration/install-enterprise#std-label-install-mdb-enterprise)

MongoDB Cloud Manager backs up replica sets and sharded clusters by reading [oplog](/docs/manual/reference/glossary#std-term-oplog) data from your MongoDB deployment. MongoDB Cloud Manager creates snapshots at set intervals and offers point-in-time recovery.

**Tip:**

Sharded cluster snapshots are difficult to achieve with other MongoDB backup methods.

To get started with MongoDB Cloud Manager Backup, sign up for [MongoDB Cloud Manager](https://www.mongodb.com/products/tools/cloud-manager). For documentation on MongoDB Cloud Manager, see the [MongoDB Cloud Manager documentation](https://www.mongodb.com/docs/cloud-manager/).

### Ops Manager

With Ops Manager, MongoDB subscribers can install and run the same backup software as MongoDB Cloud Manager on their own infrastructure. Ops Manager is available with Enterprise Advanced subscriptions.

For more information about Ops Manager, see the [MongoDB Enterprise Advanced](https://www.mongodb.com/products/mongodb-enterprise-advanced) page and the [Ops Manager Manual.](https://www.mongodb.com/docs/ops-manager/current/)

## Back Up by Copying Underlying Data Files

**Note: Considerations for Encrypted Storage Engines using AES256-GCM**

For [encrypted storage engines](/docs/manual/core/security-encryption-at-rest#std-label-encrypted-storage-engine) that use `AES256-GCM` encryption mode, `AES256-GCM` requires that every process use a unique counter block value with the key.

For [encrypted storage engine](/docs/manual/core/security-encryption-at-rest#std-label-encrypted-storage-engine) configured with `AES256-GCM` cipher:

- Restoring from Hot Backup

  If you restore from files taken through "hot" backup while the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) is running, MongoDB detects "dirty" keys on startup and automatically rolls over the database key to avoid IV (Initialization Vector) reuse.

- Restoring from Cold Backup

  However, if you restore from files taken through "cold" backup while the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) is not running, MongoDB does not detect "dirty" keys on startup, and reuse of IV voids confidentiality and integrity guarantees.

  To avoid the reuse of the keys after restoring from a cold filesystem snapshot, MongoDB adds a new command-line option [`--eseDatabaseKeyRollover`](/docs/manual/reference/program/mongod#std-option-mongod.--eseDatabaseKeyRollover). When started with the [`--eseDatabaseKeyRollover`](/docs/manual/reference/program/mongod#std-option-mongod.--eseDatabaseKeyRollover) option, the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instance rolls over the database keys configured with `AES256-GCM` cipher and exits.

If using filesystem-based backups for MongoDB Enterprise, use the "hot" backup feature.

### Back Up with Filesystem Snapshots

If the volume where MongoDB stores its data files supports point-in-time snapshots, use those snapshots to create backups at an exact moment in time. File system snapshots are an operating system volume manager feature and are not specific to MongoDB. The operating system takes a snapshot of the volume to use as a baseline for backup. The mechanics of snapshots depend on the underlying storage system. For example, on Linux, the Logical Volume Manager (LVM) can create snapshots. Similarly, Amazon's EBS storage system for EC2 supports snapshots.

To get a correct snapshot of a running [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) process, you must have journaling enabled and the journal must reside on the same logical volume as the other MongoDB data files.

To get a consistent snapshot of a [sharded cluster](/docs/manual/reference/glossary#std-term-sharded-cluster), you must disable the balancer and capture a snapshot from every shard as well as a config server at approximately the same moment in time. To backup sharded clusters, see [Back Up a Self-Managed Sharded Cluster with a Database Dump.](/docs/manual/tutorial/backup-sharded-cluster-with-database-dumps#std-label-backup-sharded-dumps)

For more information, see the [Back Up a Self-Managed Deployment with Filesystem Snapshots](/docs/manual/tutorial/backup-with-filesystem-snapshots) and [Back Up a Sharded Cluster with File System Snapshots](/docs/manual/tutorial/backup-sharded-cluster-with-filesystem-snapshots) for complete instructions on using LVM to create snapshots.

### Back Up with `cp` or `rsync`

If your storage system does not support snapshots, you can copy the files directly using `cp`, `rsync`, or a similar tool. Since copying multiple files is not an atomic operation, you must stop all writes to the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) before copying the files.

Backups produced by copying the underlying data do not support point in time recovery for [replica sets](/docs/manual/reference/glossary#std-term-replica-set) and are difficult to manage for larger sharded clusters. Additionally, these backups are larger because they include the indexes and duplicate underlying storage padding and fragmentation. [`mongodump`](https://www.mongodb.com/docs/database-tools/mongodump/#mongodb-binary-bin.mongodump), by contrast, creates smaller backups.

## Back Up with `mongodump`

[`mongodump`](https://www.mongodb.com/docs/database-tools/mongodump/#mongodb-binary-bin.mongodump) and [`mongorestore`](https://www.mongodb.com/docs/database-tools/mongorestore/#mongodb-binary-bin.mongorestore) are tools for backing up and restoring small MongoDB deployments. To learn more, see [Back Up and Restore with MongoDB Tools.](/docs/manual/tutorial/backup-and-restore-tools#std-label-manual-tutorial-backup-and-restore)

To backup sharded clusters, see [Back Up a Self-Managed Sharded Cluster with a Database Dump.](/docs/manual/tutorial/backup-sharded-cluster-with-database-dumps#std-label-backup-sharded-dumps)

## Compare Backup Methods

The following table compares backup methods for on-premises deployments.

| Backup Considerations | Cloud Manager/Ops Manager | Filesystem Snapshot | [`mongodump`/](https://www.mongodb.com/docs/database-tools/mongodump/#mongodb-binary-bin.mongodump)[`mongorestore`](https://www.mongodb.com/docs/database-tools/mongorestore/#mongodb-binary-bin.mongorestore) |
| --- | --- | --- | --- |
| Backup RTO (recovery time objective) | Low/depends on [snapshot store type](https://www.mongodb.com/docs/ops-manager/current/core/backup-preparations/#snapshot-frequency-and-retention-policy) | Low | High |
| Backup RPO (recovery point objective) | Low | High | High |
| Backup storage cost | Low/depends on snapshot store type | Medium | High |
| Staff Time to Manage Backups | None/depends on snapshot store type | High | High |
| Continually Point-in-Time backup and restore | Yes | No | No |
| Complexity of the restore | Low if deployment is under automation | High for a sharded cluster | Low |
| Complexity of a sharded cluster backup | Low | High, requires extra steps | High, requires extra steps |
| Impact of the backup to the source sharded cluster deployment | Low | High, requires write lock | High, requires write lock |
| Consistencies in the sharded cluster backup | Guaranteed | Not guaranteed, use [`fsync`](/docs/manual/reference/command/fsync#mongodb-dbcommand-dbcmd.fsync) or [`db.fsyncLock()`](/docs/manual/reference/method/db.fsyncLock#mongodb-method-db.fsyncLock) to reduce inconsistencies | Not guaranteed, use [`fsync`](/docs/manual/reference/command/fsync#mongodb-dbcommand-dbcmd.fsync) or [`db.fsyncLock()`](/docs/manual/reference/method/db.fsyncLock#mongodb-method-db.fsyncLock) to reduce inconsistencies |
| Incremental backup | Yes, daily incremental backup and weekly full backup | Depends on storage and tool | No |
| Define scope of backups | Yes, with [namespace filtering](https://www.mongodb.com/docs/ops-manager/current/core/backup-preparations/#namespaces-filter) | No | Yes |
