> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Read Isolation, Consistency, and Recency

## Isolation Guarantees

### Read Uncommitted

Depending on the read concern, clients can see the results of writes before the writes are [durable:](/docs/manual/reference/glossary#std-term-durable)

- Regardless of a write's [write concern](/docs/manual/reference/write-concern#std-label-write-concern), other clients using [`"local"`](/docs/manual/reference/read-concern-local#mongodb-readconcern-readconcern.-local-) or [`"available"`](/docs/manual/reference/read-concern-available#mongodb-readconcern-readconcern.-available-) read concern can see the result of a write operation before the write operation is acknowledged to the issuing client.

- Clients using [`"local"`](/docs/manual/reference/read-concern-local#mongodb-readconcern-readconcern.-local-) or [`"available"`](/docs/manual/reference/read-concern-available#mongodb-readconcern-readconcern.-available-) read concern can read data which may be subsequently [rolled back](/docs/manual/core/replica-set-rollbacks) during replica set failovers.

For operations in a [multi-document transaction](/docs/manual/core/transactions), when a transaction commits, all data changes made in the transaction are saved and visible outside the transaction. That is, a transaction will not commit some of its changes while rolling back others.

Until a transaction commits, the data changes made in the transaction are not visible outside the transaction.

However, when a transaction writes to multiple shards, not all outside read operations need to wait for the result of the committed transaction to be visible across the shards. For example, if a transaction is committed and write 1 is visible on shard A but write 2 is not yet visible on shard B, an outside read at read concern [`"local"`](/docs/manual/reference/read-concern-local#mongodb-readconcern-readconcern.-local-) can read the results of write 1 without seeing write 2.

Read uncommitted is the default isolation level and applies to [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) standalone instances, replica sets, and sharded clusters.

### Read Uncommitted And Single Document Atomicity

Write operations are atomic with respect to a single document; i.e. if a write is updating multiple fields in the document, a read operation will never see the document with only some of the fields updated. However, although a client may not see a *partially* updated document, read uncommitted means that concurrent read operations may still see the updated document before the changes are made [durable.](/docs/manual/reference/glossary#std-term-durable)

With a standalone [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instance, a set of read and write operations to a single document is serializable. With a replica set, a set of read and write operations to a single document is serializable *only* in the absence of a rollback.

### Read Uncommitted And Multiple Document Write

When a single write operation (e.g. [`db.collection.updateMany()`](/docs/manual/reference/method/db.collection.updateMany#mongodb-method-db.collection.updateMany)) modifies multiple documents, the modification of each document is atomic, but the operation as a whole is not atomic.

When performing multi-document write operations, whether through a single write operation or multiple write operations, other operations may interleave.

For situations that require atomicity of reads and writes to multiple documents (in a single or multiple collections), MongoDB supports distributed transactions, including transactions on replica sets and sharded clusters.

For more information, see [Transactions.](/docs/manual/core/transactions#std-label-transactions)

**Important:**

In most cases, a distributed transaction incurs a greater performance cost over single document writes, and the availability of distributed transactions should not be a replacement for effective schema design. For many scenarios, the [denormalized data model (embedded documents and arrays)](/docs/manual/data-modeling/embedding#std-label-data-modeling-embedding) will continue to be optimal for your data and use cases. That is, for many scenarios, modeling your data appropriately will minimize the need for distributed transactions.

For additional transactions usage considerations (such as runtime limit and oplog size limit), see also [Production Considerations.](/docs/manual/core/transactions-production-consideration#std-label-production-considerations)

Without isolating the multi-document write operations, MongoDB exhibits the following behavior:

1. Non-point-in-time read operations. Suppose a read operation begins at time *t* 1 and starts reading documents. A write operation then commits an update to one of the documents at some later time *t* 2. The reader may see the updated version of the document, and therefore does not see a point-in-time snapshot of the data.

2. Non-serializable operations. Suppose a read operation reads a document *d* 1 at time *t* 1 and a write operation updates *d* 1 at some later time *t* 3. This introduces a read-write dependency such that, if the operations were to be serialized, the read operation must precede the write operation. But also suppose that the write operation updates document *d* 2 at time *t* 2 and the read operation subsequently reads *d* 2 at some later time *t* 4. This introduces a write-read dependency which would instead require the read operation to come *after* the write operation in a serializable schedule. There is a dependency cycle which makes serializability impossible.

3. Reads may miss matching documents that are updated during the course of the read operation.

### Cursor Snapshot

MongoDB cursors can return the same document more than once in some situations. As a cursor returns documents, other operations may interleave with the query. If one of these operations changes the indexed field on the index used by the query, then the cursor could return the same document more than once.

Queries that use [unique indexes](/docs/manual/core/index-unique#std-label-index-type-unique) can, in some cases, return duplicate values. If a cursor using a unique index interleaves with a delete and insert of documents sharing the same unique value, the cursor may return the same unique value twice from different documents.

Use read isolation to improve consistency. To learn more, see [Read Concern `"snapshot"`.](/docs/manual/reference/read-concern-snapshot#std-label-read-concern-snapshot)

## Monotonic Writes

MongoDB provides monotonic write guarantees, by default, for standalone [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instances and replica sets.

For monotonic writes and sharded clusters, see [Causal Consistency.](/docs/manual/core/read-isolation-consistency-recency#std-label-causal-consistency)

Writes that don't modify any documents are known as no-operation [noop](/docs/manual/reference/glossary#std-term-noop) writes. No-operation writes:

- Occur if the filter for the write doesn't match any documents, or the matched documents are unchanged after applying the write.

- Don't increase the [optime](/docs/manual/reference/glossary#std-term-optime) value.

- Return [`WriteResult.nModified`](/docs/manual/reference/method/WriteResult#mongodb-data-WriteResult.nModified) equal to `0`, which indicates that the write operation didn't modify any documents.

To ensure monotonicity with no-operation writes, use [causal consistency guarantees](/docs/manual/core/read-isolation-consistency-recency#std-label-causal-consistency-guarantees). For all other writes, the following sections describe the monotonicity guarantees.

## Real Time Order

For read and write operations on the primary, issuing [`"linearizable"`](/docs/manual/reference/read-concern-linearizable#mongodb-readconcern-readconcern.-linearizable-) read concern for reads and [`"majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) write concern for writes enables multiple threads to read and write a single document as if a single thread performed these operations in real time. The resulting schedule for these reads and writes is linearizable.

**See also:**

[Causal Consistency](/docs/manual/core/read-isolation-consistency-recency#std-label-causal-consistency)

## Causal Consistency

Operations that logically depend on a preceding operation have a causal relationship. For example, a write that deletes all documents matching a specified condition and a subsequent read that verifies the delete operation have a causal relationship.

With causally consistent sessions, MongoDB executes causal operations in an order that respects their causal relationships. Clients observe results consistent with those relationships.

### Client Sessions and Causal Consistency Guarantees

MongoDB enables causal consistency through client sessions. A causally consistent session ensures that read operations with [`"majority"`](/docs/manual/reference/read-concern-majority#mongodb-readconcern-readconcern.-majority-) read concern and write operations with [`"majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) write concern have a causal relationship reflected in their ordering. Applications must ensure that only one thread at a time executes
these operations in a client session.

For causally related operations:

1. A client starts a client session.

   **Important:**

   Client sessions only guarantee causal consistency for:

   - Read operations with [`"majority"`](/docs/manual/reference/read-concern-majority#mongodb-readconcern-readconcern.-majority-) read concern. The return data has been acknowledged by a majority of the replica set members and is durable.

   - Write operations with [`"majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) write concern. These operations request acknowledgment that the write has been applied to a majority of the replica set's voting members.

   For more information on causal consistency and various read and write concerns, see [Causal Consistency and Read and Write Concerns.](/docs/manual/core/causal-consistency-read-write-concerns)

2. As the client issues read operations with [`"majority"`](/docs/manual/reference/read-concern-majority#mongodb-readconcern-readconcern.-majority-) read concern and write operations with [`"majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) write concern, the client includes session information with each operation.

3. For each read operation with [`"majority"`](/docs/manual/reference/read-concern-majority#mongodb-readconcern-readconcern.-majority-) read concern and write operation with [`"majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) write concern associated with the session, MongoDB returns the operation time and the cluster time, even if the operation errors. The client session tracks the operation time and the cluster time.

   **Note:**

   MongoDB does not return the operation time and the cluster time for *unacknowledged* (`w: 0`) write operations. Unacknowledged writes do not imply any causal relationship.

   MongoDB returns the operation time and the cluster time for read operations and acknowledged write operations in a client session. Only read operations with [`"majority"`](/docs/manual/reference/read-concern-majority#mongodb-readconcern-readconcern.-majority-) read concern and write operations with [`"majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) write concern guarantee causal consistency. For details, see [Causal Consistency and Read and Write Concerns.](/docs/manual/core/causal-consistency-read-write-concerns)

4. The associated client session tracks these two time fields.

   **Note:**

   Operations can be causally consistent across different sessions. MongoDB drivers and [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) provide methods to advance the operation time and the cluster time for a client session. A client can advance the cluster time and the operation time of one client session to be consistent with the operations of another client session.

#### Causal Consistency Guarantees

The following table describes the causal consistency guarantees for causally consistent sessions that use [`"majority"`](/docs/manual/reference/read-concern-majority#mongodb-readconcern-readconcern.-majority-) read concern for read operations and [`"majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) write concern for write operations.

| Guarantees | Description |
| --- | --- |
| Read your writes | Read operations reflect the results of write operations that precede them. |
| Monotonic reads | Read operations do not return results that correspond to an earlier state of the data than a preceding read operation. For example, if in a session: write 1 precedes write 2,; read 1 precedes read 2, and; read 1 returns results that reflect write 2 then read 2 cannot return results of write 1. |
| Monotonic writes | Write operations that must precede other writes are executed before those other writes. For example, if write 1 must precede write 2 in a session, the state of the data at the time of write 2 must reflect the state of the data post write 1. Other writes can interleave between write 1 and write write 2, but write 2 cannot occur before write 1. |
| Writes follow reads | Write operations that must occur after read operations are executed after those read operations. That is, the state of the data at the time of the write must incorporate the state of the data of the preceding read operations. |

#### Read Preference

These guarantees hold across all members of the MongoDB deployment. For example, in a causally consistent session, if you issue a write with [`"majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) write concern followed by a read from a secondary with read preference [`secondary`](/docs/manual/reference/glossary#std-term-secondary) and [`"majority"`](/docs/manual/reference/read-concern-majority#mongodb-readconcern-readconcern.-majority-) read concern, the read operation reflects the state of the database after the write operation.

#### Isolation

Operations within a causally consistent session are not isolated from operations outside the session. If a concurrent write operation interleaves between the session's write and read operations, the session's read operation may return results that reflect a write operation that occurred *after* the session's write operation.

### MongoDB Drivers

**Tip:**

Applications must ensure that only one thread at a time executes these operations in a client session.

Clients require MongoDB drivers updated for MongoDB 3.6 or later:

| Java 3.6+ Python 3.6+ C 1.9+ Go 1.8+ | C# 2.5+ Node 3.0+ Ruby 2.5+ Rust 2.1+ Swift 1.2+ | Perl 2.0+ PHPC 1.4+ Scala 2.2+ C++ 3.6.6+ |
| --- | --- | --- |

### Examples

**Important:**

Causally consistent sessions only guarantee causal consistency for reads with [`"majority"`](/docs/manual/reference/read-concern-majority#mongodb-readconcern-readconcern.-majority-) read concern and writes with [`"majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) write concern.

Consider a collection `items` that maintains current and historical data for various items. Only historical data has a non-null `end` date. If the `sku` value for an item changes, update the document with the old `sku` value to add the `end` date, then insert a new document with the current `sku` value. Use a causally consistent session to ensure that the update occurs before the insert.

Use the language selector to set the language of this example.

```python
with client.start_session(causal_consistency=True) as s1:
    current_date = datetime.datetime.today()
    items = client.get_database(
        "test",
        read_concern=ReadConcern("majority"),
        write_concern=WriteConcern("majority", wtimeout=1000),
    ).items
    items.update_one(
        {"sku": "111", "end": None}, {"$set": {"end": current_date}}, session=s1
    )
    items.insert_one(
        {"sku": "nuts-111", "name": "Pecans", "start": current_date}, session=s1
    )
```

```java
// Example 1: Use a causally consistent session to ensure that the update occurs before the insert.
ClientSession session1 = client.startSession(ClientSessionOptions.builder().causallyConsistent(true).build());
Date currentDate = new Date();
MongoCollection<Document> items = client.getDatabase("test")
        .withReadConcern(ReadConcern.MAJORITY)
        .withWriteConcern(WriteConcern.MAJORITY.withWTimeout(1000, TimeUnit.MILLISECONDS))
        .getCollection("test");

items.updateOne(session1, eq("sku", "111"), set("end", currentDate));

Document document = new Document("sku", "nuts-111")
        .append("name", "Pecans")
        .append("start", currentDate);
items.insertOne(session1, document);
```

```php
$items = $client->selectDatabase(
    'test',
    [
        'readConcern' => new \MongoDB\Driver\ReadConcern(\MongoDB\Driver\ReadConcern::MAJORITY),
        'writeConcern' => new \MongoDB\Driver\WriteConcern(\MongoDB\Driver\WriteConcern::MAJORITY, 1000),
    ],
)->items;

$s1 = $client->startSession(
    ['causalConsistency' => true],
);

$currentDate = new \MongoDB\BSON\UTCDateTime();

$items->updateOne(
    ['sku' => '111', 'end' => ['$exists' => false]],
    ['$set' => ['end' => $currentDate]],
    ['session' => $s1],
);
$items->insertOne(
    ['sku' => '111-nuts', 'name' => 'Pecans', 'start' => $currentDate],
    ['session' => $s1],
);
```

```csharp
using (var session1 = client.StartSession(new ClientSessionOptions { CausalConsistency = true }))
{
    var currentDate = DateTime.UtcNow.Date;
    var items = client.GetDatabase(
        "test",
        new MongoDatabaseSettings
        {
            ReadConcern = ReadConcern.Majority,
            WriteConcern = new WriteConcern(
                    WriteConcern.WMode.Majority,
                    TimeSpan.FromMilliseconds(1000))
        })
        .GetCollection<BsonDocument>("items");

    items.UpdateOne(session1,
        Builders<BsonDocument>.Filter.And(
            Builders<BsonDocument>.Filter.Eq("sku", "111"),
            Builders<BsonDocument>.Filter.Eq("end", BsonNull.Value)),
        Builders<BsonDocument>.Update.Set("end", currentDate));

    items.InsertOne(session1, new BsonDocument
    {
        {"sku", "nuts-111"},
        {"name", "Pecans"},
        {"start", currentDate}
    });
}
```

```c

 /* Use a causally-consistent session to run some operations. */

 wc = mongoc_write_concern_new ();
 mongoc_write_concern_set_wmajority (wc, 1000);
 mongoc_collection_set_write_concern (coll, wc);

 rc = mongoc_read_concern_new ();
 mongoc_read_concern_set_level (rc, MONGOC_READ_CONCERN_LEVEL_MAJORITY);
 mongoc_collection_set_read_concern (coll, rc);

 session_opts = mongoc_session_opts_new ();
 mongoc_session_opts_set_causal_consistency (session_opts, true);

 session1 = mongoc_client_start_session (client, session_opts, &error);
 if (!session1) {
    fprintf (stderr, "couldn't start session: %s\n", error.message);
    goto cleanup;
 }

 /* Run an update_one with our causally-consistent session. */
 update_opts = bson_new ();
 res = mongoc_client_session_append (session1, update_opts, &error);
 if (!res) {
    fprintf (stderr, "couldn't add session to opts: %s\n", error.message);
    goto cleanup;
 }

 query = BCON_NEW ("sku", "111");
 update = BCON_NEW ("$set", "{", "end",
      BCON_DATE_TIME (bson_get_monotonic_time ()), "}");
 res = mongoc_collection_update_one (coll,
		       query,
		       update,
		       update_opts,
		       NULL, /* reply */
		       &error);

 if (!res) {
    fprintf (stderr, "update failed: %s\n", error.message);
    goto cleanup;
 }

 /* Run an insert with our causally-consistent session */
 insert_opts = bson_new ();
 res = mongoc_client_session_append (session1, insert_opts, &error);
 if (!res) {
    fprintf (stderr, "couldn't add session to opts: %s\n", error.message);
    goto cleanup;
 }

 insert = BCON_NEW ("sku", "nuts-111", "name", "Pecans",
      "start", BCON_DATE_TIME (bson_get_monotonic_time ()));
 res = mongoc_collection_insert_one (coll, insert, insert_opts, NULL, &error);
 if (!res) {
    fprintf (stderr, "insert failed: %s\n", error.message);
    goto cleanup;
 }

```

```python
  async with await client.start_session(causal_consistency=True) as s1:
      current_date = datetime.datetime.today()
      items = client.get_database(
          "test",
          read_concern=ReadConcern("majority"),
          write_concern=WriteConcern("majority", wtimeout=1000),
      ).items
      await items.update_one(
          {"sku": "111", "end": None}, {"$set": {"end": current_date}}, session=s1
      )
      await items.insert_one(
          {"sku": "nuts-111", "name": "Pecans", "start": current_date}, session=s1
      )
```

```swift
let s1 = client1.startSession(options: ClientSessionOptions(causalConsistency: true))
let currentDate = Date()
var dbOptions = MongoDatabaseOptions(
    readConcern: .majority,
    writeConcern: try .majority(wtimeoutMS: 1000)
)
let items = client1.db("test", options: dbOptions).collection("items")
try items.updateOne(
    filter: ["sku": "111", "end": .null],
    update: ["$set": ["end": .datetime(currentDate)]],
    session: s1
)
try items.insertOne(["sku": "nuts-111", "name": "Pecans", "start": .datetime(currentDate)], session: s1)
```

```swift
let s1 = client1.startSession(options: ClientSessionOptions(causalConsistency: true))
let currentDate = Date()
var dbOptions = MongoDatabaseOptions(
    readConcern: .majority,
    writeConcern: try .majority(wtimeoutMS: 1000)
)
let items = client1.db("test", options: dbOptions).collection("items")
let result1 = items.updateOne(
    filter: ["sku": "111", "end": .null],
    update: ["$set": ["end": .datetime(currentDate)]],
    session: s1
).flatMap { _ in
    items.insertOne(["sku": "nuts-111", "name": "Pecans", "start": .datetime(currentDate)], session: s1)
}
```

To read all current `sku` values from another client, advance the cluster time and the operation time to match the other session. This ensures that the client is causally consistent with the other session and reads after the two writes:

```python
with client.start_session(causal_consistency=True) as s2:
    s2.advance_cluster_time(s1.cluster_time)
    s2.advance_operation_time(s1.operation_time)

    items = client.get_database(
        "test",
        read_preference=ReadPreference.SECONDARY,
        read_concern=ReadConcern("majority"),
        write_concern=WriteConcern("majority", wtimeout=1000),
    ).items
    for item in items.find({"end": None}, session=s2):
        print(item)
```

```java
// Example 2: Advance the cluster time and the operation time to that of the other session to ensure that
// this client is causally consistent with the other session and read after the two writes.
ClientSession session2 = client.startSession(ClientSessionOptions.builder().causallyConsistent(true).build());
session2.advanceClusterTime(session1.getClusterTime());
session2.advanceOperationTime(session1.getOperationTime());

items = client.getDatabase("test")
        .withReadPreference(ReadPreference.secondary())
        .withReadConcern(ReadConcern.MAJORITY)
        .withWriteConcern(WriteConcern.MAJORITY.withWTimeout(1000, TimeUnit.MILLISECONDS))
        .getCollection("items");

for (Document item: items.find(session2, eq("end", BsonNull.VALUE))) {
    System.out.println(item);
}
```

```php
$s2 = $client->startSession(
    ['causalConsistency' => true],
);
$s2->advanceClusterTime($s1->getClusterTime());
$s2->advanceOperationTime($s1->getOperationTime());

$items = $client->selectDatabase(
    'test',
    [
        'readPreference' => new \MongoDB\Driver\ReadPreference(\MongoDB\Driver\ReadPreference::SECONDARY),
        'readConcern' => new \MongoDB\Driver\ReadConcern(\MongoDB\Driver\ReadConcern::MAJORITY),
        'writeConcern' => new \MongoDB\Driver\WriteConcern(\MongoDB\Driver\WriteConcern::MAJORITY, 1000),
    ],
)->items;

$result = $items->find(
    ['end' => ['$exists' => false]],
    ['session' => $s2],
);
foreach ($result as $item) {
    var_dump($item);
}

```

```csharp
using (var session2 = client.StartSession(new ClientSessionOptions { CausalConsistency = true }))
{
    session2.AdvanceClusterTime(session1.ClusterTime);
    session2.AdvanceOperationTime(session1.OperationTime);

    var items = client.GetDatabase(
        "test",
        new MongoDatabaseSettings
        {
            ReadPreference = ReadPreference.Secondary,
            ReadConcern = ReadConcern.Majority,
            WriteConcern = new WriteConcern(WriteConcern.WMode.Majority, TimeSpan.FromMilliseconds(1000))
        })
        .GetCollection<BsonDocument>("items");

    var filter = Builders<BsonDocument>.Filter.Eq("end", BsonNull.Value);
    foreach (var item in items.Find(session2, filter).ToEnumerable())
    {
        // process item
    }
}
```

```c

 /* Make a new session, session2, and make it causally-consistent
  * with session1, so that session2 will read session1's writes. */
 session2 = mongoc_client_start_session (client, session_opts, &error);
 if (!session2) {
    fprintf (stderr, "couldn't start session: %s\n", error.message);
    goto cleanup;
 }

 /* Set the cluster time for session2 to session1's cluster time */
 cluster_time = mongoc_client_session_get_cluster_time (session1);
 mongoc_client_session_advance_cluster_time (session2, cluster_time);

 /* Set the operation time for session2 to session2's operation time */
 mongoc_client_session_get_operation_time (session1, &timestamp, &increment);
 mongoc_client_session_advance_operation_time (session2,
				 timestamp,
				 increment);

 /* Run a find on session2, which should now find all writes done
  * inside of session1 */
 find_opts = bson_new ();
 res = mongoc_client_session_append (session2, find_opts, &error);
 if (!res) {
    fprintf (stderr, "couldn't add session to opts: %s\n", error.message);
    goto cleanup;
 }

 find_query = BCON_NEW ("end", BCON_NULL);
 read_prefs = mongoc_read_prefs_new (MONGOC_READ_SECONDARY);
 cursor = mongoc_collection_find_with_opts (coll,
			      query,
			      find_opts,
			      read_prefs);

 while (mongoc_cursor_next (cursor, &result)) {
    json = bson_as_relaxed_extended_json (result, NULL);
    fprintf (stdout, "Document: %s\n", json);
    bson_free (json);
 }

 if (mongoc_cursor_error (cursor, &error)) {
    fprintf (stderr, "cursor failure: %s\n", error.message);
    goto cleanup;
 }

```

```python
  async with await client.start_session(causal_consistency=True) as s2:
      s2.advance_cluster_time(s1.cluster_time)
      s2.advance_operation_time(s1.operation_time)

      items = client.get_database(
          "test",
          read_preference=ReadPreference.SECONDARY,
          read_concern=ReadConcern("majority"),
          write_concern=WriteConcern("majority", wtimeout=1000),
      ).items
      async for item in items.find({"end": None}, session=s2):
          print(item)
```

```swift
try client2.withSession(options: ClientSessionOptions(causalConsistency: true)) { s2 in
    // The cluster and operation times are guaranteed to be non-nil since we already used s1 for operations above.
    s2.advanceClusterTime(to: s1.clusterTime!)
    s2.advanceOperationTime(to: s1.operationTime!)

    dbOptions.readPreference = .secondary
    let items2 = client2.db("test", options: dbOptions).collection("items")
    for item in try items2.find(["end": .null], session: s2) {
        print(item)
    }
}
```

```swift
let options = ClientSessionOptions(causalConsistency: true)
let result2: EventLoopFuture<Void> = client2.withSession(options: options) { s2 in
    // The cluster and operation times are guaranteed to be non-nil since we already used s1 for operations above.
    s2.advanceClusterTime(to: s1.clusterTime!)
    s2.advanceOperationTime(to: s1.operationTime!)

    dbOptions.readPreference = .secondary
    let items2 = client2.db("test", options: dbOptions).collection("items")

    return items2.find(["end": .null], session: s2).flatMap { cursor in
        cursor.forEach { item in
            print(item)
        }
    }
}
```

### Limitations

The following operations build in-memory structures and are not causally consistent:

| Operation | Notes |
| --- | --- |
| [`collStats`](/docs/manual/reference/command/collStats#mongodb-dbcommand-dbcmd.collStats) | |
| [`$collStats`](/docs/manual/reference/operator/aggregation/collStats#mongodb-pipeline-pipe.-collStats) with `latencyStats` option. | |
| [`$currentOp`](/docs/manual/reference/operator/aggregation/currentOp#mongodb-pipeline-pipe.-currentOp) | Returns an error if the operation is associated with a causally consistent client session. |
| [`createIndexes`](/docs/manual/reference/command/createIndexes#mongodb-dbcommand-dbcmd.createIndexes) | |
| [`dbHash`](/docs/manual/reference/command/dbHash#mongodb-dbcommand-dbcmd.dbHash) | |
| [`dbStats`](/docs/manual/reference/command/dbStats#mongodb-dbcommand-dbcmd.dbStats) | |
| [`getMore`](/docs/manual/reference/command/getMore#mongodb-dbcommand-dbcmd.getMore) | Returns an error if the operation is associated with a causally consistent client session. |
| [`$indexStats`](/docs/manual/reference/operator/aggregation/indexStats#mongodb-pipeline-pipe.-indexStats) | |
| [`mapReduce`](/docs/manual/reference/command/mapReduce#mongodb-dbcommand-dbcmd.mapReduce) | |
| [`ping`](/docs/manual/reference/command/ping#mongodb-dbcommand-dbcmd.ping) | Returns an error if the operation is associated with a causally consistent client session. |
| [`serverStatus`](/docs/manual/reference/command/serverStatus#mongodb-dbcommand-dbcmd.serverStatus) | Returns an error if the operation is associated with a causally consistent client session. |
| [`validate`](/docs/manual/reference/command/validate#mongodb-dbcommand-dbcmd.validate) | |
