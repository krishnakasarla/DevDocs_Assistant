> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Clustered Collections

**New in version 5.3**

Clustered collections store documents in index order rather than the natural order typical of traditional collections. Clustered collections store documents in one [WiredTiger](/docs/manual/core/wiredtiger#std-label-storage-wiredtiger) file ordered according to the index specification, instead of requiring a separate index file for the default `_id` index.

Storing the collection's documents in index order can provide benefits for storage and performance compared to traditional collections and their related regular indexes.

Clustered collections are created with a [clustered index](/docs/manual/reference/method/db.createCollection#std-label-db.createCollection.clusteredIndex). The clustered index specifies the order in which documents are stored.

To create a clustered collection, see [Examples.](/docs/manual/core/clustered-collections#std-label-clustered-collections-examples)

**Important: Backward-Incompatible Feature**

You must drop clustered collections before you can downgrade to a version of MongoDB earlier than 5.3.

## Benefits

Clustered collections have the following benefits compared to non-clustered collections:

- Faster queries on clustered collections without needing a secondary index, such as queries with range scans and equality comparisons on the clustered index key.

- Clustered collections have a lower storage size, which improves performance for queries and bulk inserts.

- Clustered collections can eliminate the need for a secondary [TTL (Time To Live) index.](/docs/manual/core/indexes/index-properties#std-label-ttl-index)

  - A clustered index is also a TTL index if you specify the [expireAfterSeconds](/docs/manual/reference/method/db.createCollection#std-label-db.createCollection.expireAfterSeconds) field.

  - To be used as a TTL index, the `_id` field must be a supported date type. See [TTL Indexes.](/docs/manual/core/index-ttl#std-label-index-feature-ttl)

  - If you use a clustered index as a TTL index, it improves document delete performance and reduces the clustered collection storage size.

- Clustered collections have additional performance improvements for inserts, updates, deletes, and queries.

  - All collections have an [\_id index.](/docs/manual/indexes#std-label-index-type-id)

  - A non-clustered collection stores the `_id` index separately from the documents. This requires two writes for inserts, updates, and deletes, and two reads for queries.

  - A clustered collection stores the index and the documents together in `_id` value order. This requires one write for inserts, updates, and deletes, and one read for queries.

## Behavior

Clustered collections store documents ordered by the [clustered index](/docs/manual/reference/method/db.createCollection#std-label-db.createCollection.clusteredIndex) key value. The clustered index key must be `{ _id: 1 }`.

You can only have one clustered index in a collection because the documents can be stored in only one order. Only collections with a clustered index store the data in sorted order.

You can have a clustered index and add [secondary indexes](/docs/manual/reference/glossary#std-term-secondary-index) to a clustered collection. Clustered indexes differ from secondary indexes:

- A clustered index can only be created when you create the collection.

- The clustered index keys are stored with the collection. The collection size returned by the [`collStats`](/docs/manual/reference/command/collStats#mongodb-dbcommand-dbcmd.collStats) command includes the clustered index size.

Starting in MongoDB 6.0.7, if a usable clustered index exists, the MongoDB query planner evaluates the clustered index against secondary indexes in the query planning process. When a query uses a clustered index, MongoDB performs a [bounded collection scan.](/docs/manual/reference/glossary#std-term-bounded-collection-scan)

Prior to MongoDB 6.0.7, if a [secondary index](/docs/manual/reference/glossary#std-term-secondary-index) existed on a clustered collection and the secondary index was usable by your query, the query planner selected the secondary index instead of the clustered index by default. In MongoDB 6.1 and prior, to use the clustered index, you must provide a hint because the [query optimizer](/docs/manual/core/query-plans#std-label-query-plans-query-optimization) does not automatically select the clustered index.

### Index Size

In clustered collections with only a default index on the `_ìd` field (no secondary indexes), the index size appears as zero because the collection does not require a separate index file.

## Limitations

- The clustered index key must be `{ _id: 1 }`.

- You cannot transform a non-clustered collection to a clustered collection, or the reverse. Instead, you can:

  - Read documents from one collection and write them to another collection using an [aggregation pipeline](/docs/manual/aggregation#std-label-aggregation-pipeline-intro) with an [`$out`](/docs/manual/reference/operator/aggregation/out#mongodb-pipeline-pipe.-out) stage or a [`$merge`](/docs/manual/reference/operator/aggregation/merge#mongodb-pipeline-pipe.-merge) stage.

  - Export collection data with [`mongodump`](https://www.mongodb.com/docs/database-tools/mongodump/#mongodb-binary-bin.mongodump) and import the data into another collection with [`mongorestore`.](https://www.mongodb.com/docs/database-tools/mongorestore/#mongodb-binary-bin.mongorestore)

- You cannot hide a clustered index. See [Hidden indexes.](/docs/manual/core/index-hidden)

- If there are secondary indexes for the clustered collection, the collection has a larger storage size. This is because secondary indexes on a clustered collection with large clustered index keys may have a larger storage size than secondary indexes on a non-clustered collection.

- Clustered collections may not be [capped collections.](/docs/manual/core/capped-collections#std-label-manual-capped-collection)

## Set Your Own Clustered Index Key Values

By default, the [clustered index](/docs/manual/reference/method/db.createCollection#std-label-db.createCollection.clusteredIndex) key values are the unique document [object identifiers.](/docs/manual/reference/bson-types#std-label-objectid)

You can set your own clustered index key values, which must follow the standard constraints of [the \_id field.](/docs/manual/core/document#std-label-document-id-field)

To optimize performance:

- Use sequentially increasing key values to improve insert performance.

- Set your index keys to be as small in size as possible.

  - A clustered index supports keys up to 8 MB in size, but a much smaller clustered index key is best.

  - Large keys increase the storage size of the clustered collection and its secondary indexes which decreases clustered collection performance.

**Warning:**

Randomly generated key values may decrease a clustered collection's performance.

## Examples

### `Create` Example

The following [`create`](/docs/manual/reference/command/create#mongodb-dbcommand-dbcmd.create) example adds a [clustered collection](/docs/manual/core/clustered-collections#std-label-clustered-collections) named `products`:

```javascript
db.runCommand( {
   create: "products",
   clusteredIndex: { "key": { _id: 1 }, "unique": true, "name": "products clustered key" }
} )

```

In the example, [clusteredIndex](/docs/manual/reference/command/create#std-label-create.clusteredIndex) specifies:

- `"key": { _id: 1 }`, which sets the clustered index key to the `_id` field.

- `"unique": true`, which indicates the clustered index key value must be unique.

- `"name": "orders clustered key"`, which sets the clustered index name.

### `db.createCollection` Example

The following [`db.createCollection()`](/docs/manual/reference/method/db.createCollection#mongodb-method-db.createCollection) example adds a [clustered collection](/docs/manual/core/clustered-collections#std-label-clustered-collections) named `stocks`:

```javascript
db.createCollection(
   "stocks",
   { clusteredIndex: { "key": { _id: 1 }, "unique": true, "name": "stocks clustered key" } }
)

```

In the example, [clusteredIndex](/docs/manual/reference/method/db.createCollection#std-label-db.createCollection.clusteredIndex) specifies:

- `"key": { _id: 1 }`, which sets the clustered index key to the `_id` field.

- `"unique": true`, which indicates the clustered index key value must be unique.

- `"name": "orders clustered key"`, which sets the clustered index name.

### Date Clustered Index Key Example

The following [`create`](/docs/manual/reference/command/create#mongodb-dbcommand-dbcmd.create) example adds a clustered collection named `orders`:

```javascript
db.createCollection(
   "orders",
   { clusteredIndex: { "key": { _id: 1 }, "unique": true, "name": "orders clustered key" } }
)

```

In the example, [clusteredIndex](/docs/manual/reference/method/db.createCollection#std-label-db.createCollection.clusteredIndex) specifies:

- `"key": { _id: 1 }`, which sets the clustered index key to the `_id` field.

- `"unique": true`, which indicates the clustered index key value must be unique.

- `"name": "orders clustered key"`, which sets the clustered index name.

The following example adds documents to the `orders` collection:

```javascript
db.orders.insertMany( [
   { _id: ISODate( "2022-03-18T12:45:20Z" ), "quantity": 50, "totalOrderPrice": 500 },
   { _id: ISODate( "2022-03-18T12:47:00Z" ), "quantity": 5, "totalOrderPrice": 50 },
   { _id: ISODate( "2022-03-18T12:50:00Z" ), "quantity": 1, "totalOrderPrice": 10 }
] )

```

The `_id` [clusteredIndex](/docs/manual/reference/command/create#std-label-create.clusteredIndex) key stores the order date.

If you use the `_id` field in a range query, performance is improved. For example, the following query uses `_id` and [`$gt`](/docs/manual/reference/operator/aggregation/gt#mongodb-expression-exp.-gt) to return the orders where the order date is greater than the supplied date:

```javascript
db.orders.find( { _id: { $gt: ISODate( "2022-03-18T12:47:00.000Z" ) } } )

```

Example output:

```javascript
[
   {
      _id: ISODate( "2022-03-18T12:50:00.000Z" ),
      quantity: 1,
      totalOrderPrice: 10
   }
]
```

### Determine if a Collection is Clustered

To determine if a collection is clustered, use the [`listCollections`](/docs/manual/reference/command/listCollections#mongodb-dbcommand-dbcmd.listCollections) command:

```javascript
db.runCommand( { listCollections: 1 } )
```

For clustered collections, the output includes the [clusteredIndex](/docs/manual/reference/command/create#std-label-create.clusteredIndex) details. For example, the following output shows the details for the `orders` clustered collection:

```javascript
...
name: 'orders',
type: 'collection',
options: {
   clusteredIndex: {
      v: 2,
      key: { _id: 1 },
      name: 'orders clustered key',
      unique: true
   }
},
...
```

`v` is the index version.
