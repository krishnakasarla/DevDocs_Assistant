> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Operational Restrictions in Sharded Clusters

## Sharding Operational Restrictions

### Operations Unavailable in Sharded Environments

[`$where`](/docs/manual/reference/operator/query/where#mongodb-query-op.-where) does not permit references to the `db` object from the [`$where`](/docs/manual/reference/operator/query/where#mongodb-query-op.-where) function. This is uncommon in un-sharded collections.

### Single Document Modification Operations in Sharded Collections

To use [`updateOne()`](/docs/manual/reference/method/db.collection.updateOne#mongodb-method-db.collection.updateOne)
and [`deleteOne()`](/docs/manual/reference/method/db.collection.deleteOne#mongodb-method-db.collection.deleteOne) operations for a sharded collection that specify the `multi: false` or `justOne` option:

- If you only target one shard, you can use a partial shard key in the query specification or,

- You can provide the [shard key](/docs/manual/reference/glossary#std-term-shard-key) or the `_id` field in the query specification.

To use [`findOneAndUpdate()`](/docs/manual/reference/method/db.collection.findOneAndUpdate#mongodb-method-db.collection.findOneAndUpdate) with a sharded collection, your query filter must include an equality condition on the [shard key](/docs/manual/reference/glossary#std-term-shard-key) to compare the key and value in either of these formats:

```javascript
{ key: value }
{ key: { $eq: value } }
```

### Unique Indexes in Sharded Collections

MongoDB does not support unique indexes across shards, except when the unique index contains the full shard key as a prefix of the index. In these situations MongoDB will enforce uniqueness across the full key, not a single field.

**See also:**

[Unique Constraints on Arbitrary Fields](/docs/manual/tutorial/unique-constraints-on-arbitrary-fields#std-label-shard-key-arbitrary-uniqueness) for an alternate approach.

### Consistent Indexes

MongoDB does not guarantee consistent indexes across shards.  Index creation during [`addShard`](/docs/manual/reference/command/addShard#mongodb-dbcommand-dbcmd.addShard) operations or chunk migrations may not propagate to new shards.

To check a sharded cluster for consistent indexes, use the [`checkMetadataConsistency`](/docs/manual/reference/command/checkMetadataConsistency#mongodb-dbcommand-dbcmd.checkMetadataConsistency) command:

```javascript
db.runCommand( {
   checkMetadataConsistency: 1,
   checkIndexes: true
} )
```

### Write Concern for DDL Operations

On a sharded cluster, [DDL (Data Definition Language) operations](/docs/manual/reference/ddl-operations#std-label-ddl-operations) run with write concern [`"majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-). If you specify a different write concern, the operation overrides the provided write concern with `"majority"`.
