> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Bulk Write Operations

## Overview

MongoDB provides clients the ability to perform write operations in bulk. Starting in MongoDB 8.0, you can perform bulk write operations across multiple databases and collections. If you are using a version earlier than MongoDB 8.0, you can perform bulk write operations on a single collection.

To perform bulk write operations across multiple databases and collections in MongoDB 8.0, use the [`bulkWrite`](/docs/manual/reference/command/bulkWrite#mongodb-dbcommand-dbcmd.bulkWrite) database command or the [`Mongo.bulkWrite()`](/docs/manual/reference/method/Mongo.bulkWrite#mongodb-method-Mongo.bulkWrite) `mongosh` method.

To perform bulk write operations on a single collection, use the [`db.collection.bulkWrite()`](/docs/manual/reference/method/db.collection.bulkWrite#mongodb-method-db.collection.bulkWrite) `mongosh` method. If you are running MongoDB 8.0 or later, you can also use [`bulkWrite`](/docs/manual/reference/command/bulkWrite#mongodb-dbcommand-dbcmd.bulkWrite) or [`Mongo.bulkWrite()`](/docs/manual/reference/method/Mongo.bulkWrite#mongodb-method-Mongo.bulkWrite) to write to a single collection.

## Ordered vs Unordered Operations

Bulk write operations execute either serially (*ordered*) or in any order (*unordered*). By default, operations are ordered and stop on the first error. Unordered operations continue despite errors and may execute in parallel, making them typically faster for sharded collections.

For detailed information on execution behavior and error handling, see [`db.collection.bulkWrite()`](/docs/manual/reference/method/db.collection.bulkWrite#mongodb-method-db.collection.bulkWrite) or [`Mongo.bulkWrite()`.](/docs/manual/reference/method/Mongo.bulkWrite#mongodb-method-Mongo.bulkWrite)

## Supported Operations

Bulk write operations support: Insert One, Update One, Update Many, Replace One, Delete One, and Delete Many.

## Strategies for Bulk Inserts to a Sharded Collection

Large bulk insert operations can impact [sharded cluster](/docs/manual/reference/glossary#std-term-sharded-cluster) performance. To optimize bulk writes on sharded collections:

### Pre-Split the Collection

If your sharded collection is empty and you are not using hashed sharding for the first key of your shard key, then your collection has only one initial [chunk](/docs/manual/reference/glossary#std-term-chunk), which resides on a single shard. MongoDB must then take time to receive data and distribute chunks to the available shards. To avoid this performance cost, pre-split the collection by [creating ranges in a sharded cluster.](/docs/manual/tutorial/create-chunks-in-sharded-cluster#std-label-create-ranges-in-a-sharded-cluster)

### Unordered Writes to `mongos`

To improve write performance to sharded clusters, perform an unordered bulk write by setting `ordered` to `false` when you perform a bulk write. [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) attempts to send the writes to multiple shards simultaneously. For *empty* collections, first pre-split the collection as described in [Split Chunks in a Sharded Cluster.](/docs/manual/tutorial/split-chunks-in-sharded-cluster)

### Avoid Monotonic Throttling

If your shard key increases monotonically during an insert, then all inserted data goes to the last chunk in the collection, which will always end up on a single shard. Therefore, the insert capacity of the cluster will never exceed the insert capacity of that single shard.

If your insert volume is larger than what a single shard can process, and if you cannot avoid a monotonically increasing shard key, then consider the following modifications to your application:

- Reverse the binary bits of the shard key. This preserves the information and avoids correlating insertion order with increasing sequence of values.

- Swap the first and last 16-bit words to "shuffle" the inserts.

**Example:**

The following example, in C++, swaps the leading and trailing 16-bit word of [BSON](/docs/manual/reference/glossary#std-term-BSON) [ObjectIds](/docs/manual/reference/glossary#std-term-ObjectId) generated so they are no longer monotonically increasing.

```cpp
using namespace mongo;
OID make_an_id() {
  OID x = OID::gen();
  const unsigned char *p = x.getData();
  swap( (unsigned short&) p[0], (unsigned short&) p[10] );
  return x;
}

void foo() {
  // create an object
  BSONObj o = BSON( "_id" << make_an_id() << "x" << 3 << "name" << "jane" );
  // now we may insert o into a sharded collection
}
```
