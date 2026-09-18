> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Retryable Writes

Retryable writes let drivers retry specific write operations once after network errors or if they cannot find a healthy [primary](/docs/manual/reference/glossary#std-term-primary) in the [replica set](/docs/manual/replication#std-label-replication) or [sharded cluster.](/docs/manual/sharding#std-label-sharding-introduction)

## Compatibility

Retryable writes require:

Deployment Topologies

A [replica set](/docs/manual/replication#std-label-replication) or [sharded cluster](/docs/manual/sharding#std-label-sharding-introduction). Not supported on [standalone instances.](/docs/manual/reference/glossary#std-term-standalone)

Storage Engine

A storage engine with document-level locking, such as [WiredTiger](/docs/manual/core/wiredtiger#std-label-storage-wiredtiger) or [in-memory.](/docs/manual/core/inmemory#std-label-storage-inmemory)

MongoDB Drivers

Drivers compatible with MongoDB 3.6+.

| Java 3.6+ Python 3.6+ C 1.9+ Go 1.8+ | C# 2.5+ Node 3.0+ Ruby 2.5+ Rust 2.1+ Swift 1.2+ | Perl 2.0+ PHPC 1.4+ Scala 2.2+ C++ 3.6.6+ |
| --- | --- | --- |

MongoDB Version

MongoDB 3.6+ and `featureCompatibilityVersion` 3.6+ on all nodes. See [`setFeatureCompatibilityVersion`.](/docs/manual/reference/command/setFeatureCompatibilityVersion#mongodb-dbcommand-dbcmd.setFeatureCompatibilityVersion)

Write Acknowledgment

Writes with [Write Concern](/docs/manual/reference/write-concern) `0` are not retryable.

## Behaviors

### Retryable Writes and Multi-Document Transactions

[Transaction commit and abort operations](/docs/manual/core/transactions-in-applications#std-label-transactions-retry) are retryable. Drivers retry these operations once on error, even if [`retryWrites`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.retryWrites) is `false`.

Writes inside a transaction are not individually retryable, regardless of value of [`retryWrites`.](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.retryWrites)

For more information on transactions, see [Transactions.](/docs/manual/core/transactions)

### Enabling Retryable Writes

MongoDB Drivers

Drivers compatible with MongoDB 4.2 and higher enable [Retryable Writes](/docs/manual/core/retryable-writes#std-label-retryable-writes) by default. Earlier drivers require the [`retryWrites=true`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.retryWrites) option. The [`retryWrites=true`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.retryWrites) option can be omitted in applications that use drivers compatible with MongoDB 4.2 and higher.

To disable retryable writes, applications that use drivers compatible with MongoDB 4.2 and higher must include [`retryWrites=false`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.retryWrites) in the connection string.

[`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh)

[`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) enables retryable writes by default. To disable, use [`--retryWrites=false`:](https://www.mongodb.com/docs/mongodb-shell/reference/options/#std-option-mongosh.--retryWrites)

```bash
mongosh --retryWrites=false
```

### Retryable Write Operations

MongoDB retries the following operations if they have acknowledged write concern (for example, [Write Concern](/docs/manual/reference/write-concern) cannot be [`{w: 0}`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-number-)):

**Note:**

Writes inside [transactions](/docs/manual/core/transactions) are not individually retryable.

| Methods | Descriptions |
| --- | --- |
| [`db.collection.insertOne()`](/docs/manual/reference/method/db.collection.insertOne#mongodb-method-db.collection.insertOne)[`db.collection.insertMany()`](/docs/manual/reference/method/db.collection.insertMany#mongodb-method-db.collection.insertMany) | Inserts |
| [`db.collection.updateOne()`](/docs/manual/reference/method/db.collection.updateOne#mongodb-method-db.collection.updateOne)[`db.collection.replaceOne()`](/docs/manual/reference/method/db.collection.replaceOne#mongodb-method-db.collection.replaceOne) | Single-document updates |
| [`db.collection.deleteOne()`](/docs/manual/reference/method/db.collection.deleteOne#mongodb-method-db.collection.deleteOne)[`db.collection.remove()`](/docs/manual/reference/method/db.collection.remove#mongodb-method-db.collection.remove) where `justOne` is `true` | Single-document deletes |
| [`db.collection.findAndModify()`](/docs/manual/reference/method/db.collection.findAndModify#mongodb-method-db.collection.findAndModify)[`db.collection.findOneAndDelete()`](/docs/manual/reference/method/db.collection.findOneAndDelete#mongodb-method-db.collection.findOneAndDelete)[`db.collection.findOneAndReplace()`](/docs/manual/reference/method/db.collection.findOneAndReplace#mongodb-method-db.collection.findOneAndReplace)[`db.collection.findOneAndUpdate()`](/docs/manual/reference/method/db.collection.findOneAndUpdate#mongodb-method-db.collection.findOneAndUpdate) | `findAndModify` operations (always single-document). |
| [`db.collection.bulkWrite()`](/docs/manual/reference/method/db.collection.bulkWrite#mongodb-method-db.collection.bulkWrite) with the following write operations: [insertOne](/docs/manual/reference/method/db.collection.bulkWrite#std-label-bulkwrite-write-operations-insertOne); [updateOne](/docs/manual/reference/method/db.collection.bulkWrite#std-label-bulkwrite-write-operations-updateOneMany); [replaceOne](/docs/manual/reference/method/db.collection.bulkWrite#std-label-bulkwrite-write-operations-replaceOne); [deleteOne](/docs/manual/reference/method/db.collection.bulkWrite#std-label-bulkwrite-write-operations-deleteOneMany) | Bulk write operations that only consist of the single-document write operations. A retryable bulk operation can include any combination of the specified write operations but cannot include any multi-document write operations, such as `updateMany`. |
| [`Bulk`](/docs/manual/reference/method/Bulk#mongodb-method-Bulk) operations for: [`Bulk.find.removeOne()`](/docs/manual/reference/method/Bulk.find.removeOne#mongodb-method-Bulk.find.removeOne); [`Bulk.find.replaceOne()`](/docs/manual/reference/method/Bulk.find.replaceOne#mongodb-method-Bulk.find.replaceOne); [`Bulk.find.updateOne()`](/docs/manual/reference/method/Bulk.find.updateOne#mongodb-method-Bulk.find.updateOne) | Bulk write operations that only consist of the single-document write operations. A retryable bulk operation can include any combination of the specified write operations but cannot include any multi-document write operations, such as `update` which specifies `true` for the `multi` option. |

### Persistent Network Errors

By default, MongoDB retries writes **once**. One retry attempts to address transient network errors and [replica set elections](/docs/manual/core/replica-set-elections#std-label-replica-set-elections), but not persistent network errors.

If you set `timeoutMS`, MongoDB may retry writes multiple times. Retries continue until one of the following conditions is true:

- The operation succeeds.

- The operation fails with a non-retryable error.

- The timeout expires.

### Failover Period

Drivers wait [`serverSelectionTimeoutMS`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.serverSelectionTimeoutMS) to find a new primary before retrying. Retryable writes fail if failover takes longer than this timeout.

**Warning:**

If a client is unresponsive for longer than [`localLogicalSessionTimeoutMinutes`](/docs/manual/reference/parameters#mongodb-parameter-param.localLogicalSessionTimeoutMinutes), the write might retry and apply again when the client recovers.

### Diagnostics

[`serverStatus`](/docs/manual/reference/command/serverStatus#mongodb-dbcommand-dbcmd.serverStatus) includes retryable write statistics in the [`transactions`](/docs/manual/reference/command/serverStatus#mongodb-serverstatus-serverstatus.transactions) section.

### Retryable Writes Against `local` Database

Official drivers enable retryable writes by default. Writes to the `local` [database](/docs/manual/reference/local-database#std-label-replica-set-local-database) fail unless you disable retryable writes.

To disable, set [`retryWrites=false`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.retryWrites) in the [connection string.](/docs/manual/reference/connection-string#std-label-mongodb-uri)

### Error Handling

Starting in MongoDB 6.1, if both the first and second attempt of a retryable write fail without a single write being performed, MongoDB returns an error with the `NoWritesPerformed` label.

The `NoWritesPerformed` label differentiates the results of batch operations like [`insertMany()`](/docs/manual/reference/method/db.collection.insertMany#mongodb-method-db.collection.insertMany). In an `insertMany` operation, one of the following outcomes can occur:

| Outcome | MongoDB Output |
| --- | --- |
| No documents are inserted. | Error returned with `NoWritesPerformed` label. |
| Partial work done. (At least one document is inserted, but not all.) | Error returned without `NoWritesPerformed` label. |
| All documents are inserted. | Success returned. |

Applications can use the `NoWritesPerformed` label to definitively determine that no documents were inserted. This error reporting lets the application maintain an accurate state of the database when handling retryable writes.

In previous versions of MongoDB, an error is returned when both the first and second attempts of a retryable write fail. However, there is no distinction made to indicate that no writes were performed.

## Learn More

[Retryable Reads](/docs/manual/core/retryable-reads#std-label-retryable-reads)
