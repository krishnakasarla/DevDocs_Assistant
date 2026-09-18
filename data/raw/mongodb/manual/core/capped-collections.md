> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Capped Collections

Capped collections are fixed-size collections that insert and retrieve documents based on insertion order. Capped collections work similarly to circular buffers: once a collection fills its allocated space, it makes room for new documents by deleting the oldest documents in the collection.

## Restrictions

- Capped collections cannot be sharded.

- Capped collections are not supported in [Stable API](/docs/manual/reference/stable-api#std-label-stable-api) V1.

- You cannot write to capped collections in [transactions.](/docs/manual/core/transactions#std-label-transactions)

- The [`$out`](/docs/manual/reference/operator/aggregation/out#mongodb-pipeline-pipe.-out) aggregation pipeline stage cannot write results to a capped collection.

## Command Syntax

The following example creates a capped collection called `log` with a maximum size of 100,000 bytes.

```javascript
db.createCollection( "log", { capped: true, size: 100000 } )
```

For more information on creating capped collections, see [`createCollection()`](/docs/manual/reference/method/db.createCollection#mongodb-method-db.createCollection) or [`create`.](/docs/manual/reference/command/create#mongodb-dbcommand-dbcmd.create)

## Use Cases

Generally, [TTL (Time To Live) indexes](/docs/manual/core/index-ttl#std-label-index-feature-ttl) offer better performance and more flexibility than capped collections. TTL indexes expire and remove data from normal collections based on the value of a date-typed field and a TTL value for the index.

Capped collections serialize write operations and therefore have worse concurrent insert, update, and delete performance than non-capped collections. Before you create a capped collection, consider if you can use a TTL index instead.

The most common use case for a capped collection is to store log information. When the capped collection reaches its maximum size, old log entries are automatically overwritten with new entries.

## Get Started

To create and query capped collections, see these pages:

- [Create a Capped Collection](/docs/manual/core/capped-collections/create-capped-collection#std-label-capped-collections-create)

- [Query a Capped Collection](/docs/manual/core/capped-collections/query-capped-collection#std-label-capped-collections-query)

- [Check if a Collection is Capped](/docs/manual/core/capped-collections/check-if-collection-is-capped#std-label-capped-collections-check)

- [Convert a Collection to Capped](/docs/manual/core/capped-collections/convert-collection-to-capped#std-label-capped-collections-convert)

- [Change the Size of a Capped Collection](/docs/manual/core/capped-collections/change-size-capped-collection#std-label-capped-collections-change-size)

- [Change Maximum Documents in a Capped Collection](/docs/manual/core/capped-collections/change-max-docs-capped-collection#std-label-capped-collections-change-max-docs)

## Behavior

### Oplog Collection

The [oplog.rs](/docs/manual/reference/glossary#std-term-oplog) collection that stores a log of the operations in a [replica set](/docs/manual/reference/glossary#std-term-replica-set) uses a capped collection.

Unlike other capped collections, the oplog can grow past its configured size limit to avoid deleting the [`majority commit point`.](/docs/manual/reference/command/replSetGetStatus#mongodb-data-replSetGetStatus.optimes.lastCommittedOpTime)

**Note:**

MongoDB rounds the capped size of the oplog up to the nearest integer multiple of 256, in bytes.

### \_id Index

Capped collections have an `_id` field and an index on the `_id` field by default.

### Updates

Avoid updating data in a capped collection. Updates can expand your data beyond the collection's allocated space and cause unexpected behavior.

### Query Efficiency

Use [natural ordering](/docs/manual/reference/glossary#std-term-natural-order) to retrieve the most recently inserted elements from the collection efficiently. This is similar to using the `tail` command on a log file.

### Tailable Cursor

You can use a [tailable cursor](/docs/manual/reference/glossary#std-term-tailable-cursor) with capped collections. Similar to the Unix `tail -f` command, a tailable cursor continuously retrieves new documents from the end of a capped collection as they are inserted.

For information on creating a tailable cursor, see [Tailable Cursors.](/docs/manual/core/tailable-cursors#std-label-tailable-cursors-landing-page)

### Multiple Concurrent Writes

If there are concurrent writers to a capped collection, MongoDB does not guarantee that documents are returned in insertion order.

### Read Concern Snapshot

Starting in MongoDB 8.0, you can use read concern [`"snapshot"`](/docs/manual/reference/read-concern-snapshot#mongodb-readconcern-readconcern.-snapshot-) on [capped](/docs/manual/core/capped-collections#std-label-manual-capped-collection) collections.

## Learn More

- [TTL Indexes](/docs/manual/core/index-ttl#std-label-index-feature-ttl)

- [Index Properties](/docs/manual/core/indexes/index-properties#std-label-index-properties)

- [Indexing Strategies](/docs/manual/applications/indexes#std-label-indexing-strategies)
