> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Create a Hashed Index

To enable sharding for a collection that already contains data, you must create an index that supports the shard key. To enable sharding for an empty collection, you can instead specify the shard key index when you [shard the collection.](/docs/manual/core/sharding-shard-key#std-label-sharding-shard-key-creation)

Hashed indexes support [hashed sharding](/docs/manual/core/hashed-sharding#std-label-sharding-hashed), where data is distributed across shards based on the hashes of shard key values.

To create a single-field hashed index, specify `hashed` as the value of the index key:

```javascript
db.<collection>.createIndex(
   {
      <field>: "hashed"
   }
)
```

To create a hashed index that contains multiple fields (a compound hashed index), specify `hashed` as the value of a *single* index key. For other index keys, specify the sort order (`1` or `-1`):

```javascript
db.<collection>.createIndex(
   {
      <field1>: "hashed",
      <field2>: "<sort order>",
      <field3>: "<sort order>",
      ...
   }
)
```

## About this Task

Hashed indexing is ideal for shard keys with fields that change [monotonically](/docs/manual/core/sharding-choose-a-shard-key#std-label-shard-key-monotonic) like [ObjectId](/docs/manual/reference/glossary#std-term-ObjectId) values or timestamps. When you use [ranged sharding](/docs/manual/core/ranged-sharding#std-label-sharding-ranged) with a monotonically increasing shard key value, the chunk with an upper bound of [`MaxKey`](/docs/manual/reference/mongodb-extended-json#mongodb-bsontype-MaxKey) receives the majority incoming writes. This behavior restricts insert operations to a single shard, which removes the advantage of distributed writes in a sharded cluster.

For more information on choosing the best sharding approach for your application, see [Hashed vs Ranged Sharding](/docs/manual/core/hashed-sharding#std-label-hashed-versus-ranged-sharding)

### Choose a Hashed Shard Key

Consider the following guidelines for your hashed shard key:

- The field you choose for your hashed shard key should have a high [cardinality](/docs/manual/core/sharding-choose-a-shard-key#std-label-shard-key-range), meaning a large number of different values.

- If your data model does not contain a single field with high cardinality, consider creating a [compound hashed index](/docs/manual/core/indexes/index-types/index-hashed/create#std-label-compound-hashed-index-example). A compound hashed index provides more unique indexed values and can increase cardinality.

- Your shard key should support common query patterns. Range queries (like [`$gt`](/docs/manual/reference/operator/query/gt#mongodb-query-op.-gt) and [`$lt`](/docs/manual/reference/operator/query/lt#mongodb-query-op.-lt)) cannot use a hashed index. If your application often performs range queries on the fields included in your shard key, consider range-based sharding instead.

A hashed index can contain up to 32 fields.

## Before You Begin

To implement hashed sharding, you must [deploy a sharded cluster.](/docs/manual/tutorial/deploy-shard-cluster#std-label-sharding-procedure-setup)

## Examples

The following examples show you how to:

- [Create a Single-Field Hashed Index](/docs/manual/core/indexes/index-types/index-hashed/create#std-label-single-hashed-index-example)

- [Create a Compound Hashed Index](/docs/manual/core/indexes/index-types/index-hashed/create#std-label-compound-hashed-index-example)

### Create a Single-Field Hashed Index

Consider an `orders` collection that already contains data. Create a hashed index in the `orders` collection on the `_id` field:

```javascript
db.orders.createIndex( { _id: "hashed" } )
```

The `_id` field increases monotonically, which makes it a good candidate for a hashed index key. Although `_id` values incrementally increase, when MongoDB generates a hash for individual `_id` values, those hashed values are unlikely to be on the same [chunk.](/docs/manual/reference/glossary#std-term-chunk)

After you create the index, you can shard the `orders` collection:

```javascript
sh.shardCollection(
   "<database>.orders",
   { _id: "hashed" }
)
```

### Create a Compound Hashed Index

Consider a `customers` collection that already contains data. Create a compound hashed index in the `customers` collection on the `name`, `address`, and `birthday` fields:

```javascript
db.customers.createIndex(
   {
      "name" : 1
      "address" : "hashed",
      "birthday" : -1
   }
)
```

When you create a compound hashed index, you must specify `hashed` as the value of a *single* index key. For other index keys, specify the sort order (`1` or `-1`). In the preceding index, `address` is the hashed field.

After you create the index, you can shard the `customers` collection:

```javascript
sh.shardCollection(
   "<database>.customers",
   {
      "name" : 1
      "address" : "hashed",
      "birthday" : -1
   }
)
```

## Learn More

- [Hashed Sharding](/docs/manual/core/hashed-sharding#std-label-sharding-hashed)

- [Choose a Shard Key](/docs/manual/core/sharding-choose-a-shard-key#std-label-sharding-shard-key-selection)

- [Hashed vs Ranged Sharding](/docs/manual/core/hashed-sharding#std-label-hashed-versus-ranged-sharding)

- [Deploy a Self-Managed Sharded Cluster](/docs/manual/tutorial/deploy-shard-cluster#std-label-sharding-procedure-setup)
