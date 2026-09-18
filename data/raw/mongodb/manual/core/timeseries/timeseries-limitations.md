> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Time Series Collection Limitations

[Time series collections](/docs/manual/core/timeseries-collections#std-label-manual-timeseries-collection) generally behave like regular collections with several limitations.

## Unsupported Features

MongoDB does not support the following features with time series collections:

- [MongoDB Search](https://www.mongodb.com/docs/atlas/atlas-search/)

- [Change streams](/docs/manual/changeStreams#std-label-changeStreams)

- [Client-Side Field Level Encryption](/docs/manual/core/csfle#std-label-manual-csfle-feature)

- [Database Triggers](https://www.mongodb.com/docs/atlas/atlas-ui/triggers/database-triggers/)

- [Schema validation rules](/docs/manual/core/schema-validation#std-label-schema-validation-overview)

- [`reIndex`](/docs/manual/reference/command/reIndex#mongodb-dbcommand-dbcmd.reIndex)

- [`renameCollection`](/docs/manual/reference/command/renameCollection#mongodb-dbcommand-dbcmd.renameCollection)

**Note:**

You cannot use [time series collections](/docs/manual/core/timeseries-collections#std-label-manual-timeseries-collection) as a source for [Atlas Stream Processing](https://www.mongodb.com/docs/atlas/atlas-stream-processing/#std-label-atlas-sp). Time series collections do not support [change streams.](/docs/manual/changeStreams#std-label-changeStreams)

## Aggregation $merge

You cannot use the [`$merge`](/docs/manual/reference/operator/aggregation/merge#mongodb-pipeline-pipe.-merge) aggregation stage to add data from another collection to a time series collection. Use the [`$out`](/docs/manual/reference/operator/aggregation/out#mongodb-pipeline-pipe.-out) aggregation stage to write documents to a time series collection.

You can use [`$merge`](/docs/manual/reference/operator/aggregation/merge#mongodb-pipeline-pipe.-merge) to move data from a time series collection to another collection.

## distinct Command

Due to the unique data structure of time series collections, MongoDB can't efficiently index them for distinct values. Avoid using the [`distinct`](/docs/manual/reference/command/distinct#mongodb-dbcommand-dbcmd.distinct) command or [`db.collection.distinct()`](/docs/manual/reference/method/db.collection.distinct#mongodb-method-db.collection.distinct) helper method on time series collections. Instead, use a [`$group`](/docs/manual/reference/operator/aggregation/group#mongodb-pipeline-pipe.-group) aggregation to group documents by distinct values, as shown in the following example:

```javascript
db.foo.createIndex({"meta.project":1, "meta.type":1})
db.foo.aggregate([{$match: {"meta.project": 10}},
                  {$group: {_id: "$meta.type"}}])
```

This works as follows:

1. Creating a [compound index](/docs/manual/core/indexes/index-types/index-compound#std-label-index-type-compound) on `meta.project` and `meta.type` and supports the aggregation.

2. The [`$match`](/docs/manual/reference/operator/aggregation/match#mongodb-pipeline-pipe.-match) stage filters for documents where `meta.project = 10`.

3. The [`$group`](/docs/manual/reference/operator/aggregation/group#mongodb-pipeline-pipe.-group) stage uses `meta.type` as the group key to output one document per unique value.

Due to the unique data structure of time series collections, MongoDB can't efficiently index them for distinct values. Avoid using the [`distinct`](/docs/manual/reference/command/distinct#mongodb-dbcommand-dbcmd.distinct) command or [`db.collection.distinct()`](/docs/manual/reference/method/db.collection.distinct#mongodb-method-db.collection.distinct) helper method on time series collections. Instead, use a [`$group`](/docs/manual/reference/operator/aggregation/group#mongodb-pipeline-pipe.-group) aggregation to group documents by distinct values, as shown in the following example:

```csharp
var indexModel = new CreateIndexModel<BsonDocument>(
    Builders<BsonDocument>.IndexKeys
        .Ascending("meta.project")
        .Ascending("meta.type"));

_collection?.Indexes.CreateOne(indexModel);

var matchStage = Builders<BsonDocument>.Filter.Eq("meta.project", 10);
var pipeline = new EmptyPipelineDefinition<BsonDocument>()
    .Match(matchStage)
    .Group(new BsonDocument("_id", "$meta.type"));

var result = _collection?.Aggregate(pipeline).ToList();

```

This works as follows:

1. Creating a [compound index](/docs/manual/core/indexes/index-types/index-compound#std-label-index-type-compound) on `meta.project` and `meta.type` and supports the aggregation.

2. The [`$match`](/docs/manual/reference/operator/aggregation/match#mongodb-pipeline-pipe.-match) stage filters for documents where `meta.project = 10`.

3. The [`$group`](/docs/manual/reference/operator/aggregation/group#mongodb-pipeline-pipe.-group) stage uses `meta.type` as the group key to output one document per unique value.

Due to the unique data structure of time series collections, MongoDB can't efficiently index them for distinct values. Avoid using the [`distinct`](/docs/manual/reference/command/distinct#mongodb-dbcommand-dbcmd.distinct) command or [`db.collection.distinct()`](/docs/manual/reference/method/db.collection.distinct#mongodb-method-db.collection.distinct) helper method on time series collections. Instead, use a [`$group`](/docs/manual/reference/operator/aggregation/group#mongodb-pipeline-pipe.-group) aggregation to group documents by distinct values, as shown in the following example:

```python
collection.create_index([("meta.project", 1), ("meta.type", 1)])

pipeline = [
    {"$match": {"meta.project": 10}},
    {"$group": {"_id": "$meta.type"}},
]

result = list(collection.aggregate(pipeline))

```

This works as follows:

1. Creating a [compound index](/docs/manual/core/indexes/index-types/index-compound#std-label-index-type-compound) on `meta.project` and `meta.type` and supports the aggregation.

2. The [`$match`](/docs/manual/reference/operator/aggregation/match#mongodb-pipeline-pipe.-match) stage filters for documents where `meta.project = 10`.

3. The [`$group`](/docs/manual/reference/operator/aggregation/group#mongodb-pipeline-pipe.-group) stage uses `meta.type` as the group key to output one document per unique value.

Due to the unique data structure of time series collections, MongoDB can't efficiently index them for distinct values. Avoid using the [`distinct`](/docs/manual/reference/command/distinct#mongodb-dbcommand-dbcmd.distinct) command or [`db.collection.distinct()`](/docs/manual/reference/method/db.collection.distinct#mongodb-method-db.collection.distinct) helper method on time series collections. Instead, use a [`$group`](/docs/manual/reference/operator/aggregation/group#mongodb-pipeline-pipe.-group) aggregation to group documents by distinct values, as shown in the following example:

```javascript
await collection.createIndex({ 'meta.project': 1, 'meta.type': 1 });

const pipeline = [
  { $match: { 'meta.project': 10 } },
  { $group: { _id: '$meta.type' } },
];

const result = await collection.aggregate(pipeline).toArray();

```

This works as follows:

1. Creating a [compound index](/docs/manual/core/indexes/index-types/index-compound#std-label-index-type-compound) on `meta.project` and `meta.type` and supports the aggregation.

2. The [`$match`](/docs/manual/reference/operator/aggregation/match#mongodb-pipeline-pipe.-match) stage filters for documents where `meta.project = 10`.

3. The [`$group`](/docs/manual/reference/operator/aggregation/group#mongodb-pipeline-pipe.-group) stage uses `meta.type` as the group key to output one document per unique value.

Due to the unique data structure of time series collections, MongoDB can't efficiently index them for distinct values. Avoid using the [`distinct`](/docs/manual/reference/command/distinct#mongodb-dbcommand-dbcmd.distinct) command or [`db.collection.distinct()`](/docs/manual/reference/method/db.collection.distinct#mongodb-method-db.collection.distinct) helper method on time series collections. Instead, use a [`$group`](/docs/manual/reference/operator/aggregation/group#mongodb-pipeline-pipe.-group) aggregation to group documents by distinct values, as shown in the following example:

```java
collection.createIndex(Indexes.compoundIndex(
        Indexes.ascending("meta.project"),
        Indexes.ascending("meta.type")
));

var pipeline = Arrays.asList(
        Aggregates.match(Filters.eq("meta.project", 10)),
        Aggregates.group("$meta.type")
);
List<Document> result = collection.aggregate(pipeline).into(new ArrayList<>());

```

This works as follows:

1. Creating a [compound index](/docs/manual/core/indexes/index-types/index-compound#std-label-index-type-compound) on `meta.project` and `meta.type` and supports the aggregation.

2. The [`$match`](/docs/manual/reference/operator/aggregation/match#mongodb-pipeline-pipe.-match) stage filters for documents where `meta.project = 10`.

3. The [`$group`](/docs/manual/reference/operator/aggregation/group#mongodb-pipeline-pipe.-group) stage uses `meta.type` as the group key to output one document per unique value.

## Geospatial Queries

Time series collections only support the [`$geoNear`](/docs/manual/reference/operator/aggregation/geoNear#mongodb-pipeline-pipe.-geoNear) aggregation stage for sorting [geospatial data](/docs/manual/geospatial-queries) from queries against [2dsphere](/docs/manual/core/indexes/index-types/geospatial/2dsphere#std-label-2dsphere-index) indexes. You can't use [`$near`](/docs/manual/reference/operator/query/near#mongodb-query-op.-near) and [`$nearSphere`](/docs/manual/reference/operator/query/nearSphere#mongodb-query-op.-nearSphere) operators on time series collections.

### $geoNear

You can't use the `query` field for `$geoNear` on a [time series collection.](/docs/manual/core/timeseries-collections#std-label-manual-timeseries-landing)

You must specify the `key` field for `$geoNear` on a time series collection.

## Document Size

The maximum size for documents within a time series collection is 4 MB.

## Extended Date Range

If your time series collection contains  documents with `timeField` timestamps before `1970-01-01T00:00:00.000Z` or after `2038-01-19T03:14:07.000Z`, create an index on the `timeField` to optimize queries.

## Updates

Update commands must meet the following requirements:

- You can only match on the `metaField` field value.

- You can only modify the `metaField` field value.

- Your update document can only contain [update operator](/docs/manual/reference/mql/update#std-label-update-operators) expressions.

- Your update command must not limit the number of documents to be updated. Set `multi: true` or use the [`updateMany()`](/docs/manual/reference/method/db.collection.updateMany#mongodb-method-db.collection.updateMany) method.

- Your update command must not set [upsert: true.](/docs/manual/reference/method/db.collection.update#std-label-update-upsert)

To automatically delete old data, [set up automatic removal (TTL).](/docs/manual/core/timeseries/timeseries-automatic-removal#std-label-set-up-automatic-removal)

## Indexes

### Default Index

MongoDB does not create an index on the `_id` field when you create a time series collection. This differs from regular collections which have an index on the `_id` field by default. Commands that specify a hint on the `_id` field on time series collections return an error unless you manually create an index on the `_id` field.

### Hint on "\_id\_" Index

Starting in MongoDB 8.3, creating an index with the name of `"_id_"` or specifying a hint of `"_id_"` on time series collections returns an error.

### Time Series Secondary Indexes

MongoDB partially supports the following indexes on time series collections:

- You can only create [multikey indexes](/docs/manual/core/indexes/index-types/index-multikey#std-label-index-type-multikey) on the `metaField`.

- You can only create [2d indexes](/docs/manual/core/indexes/index-types/geospatial/2d#std-label-2d-index) on the `metaField`.

- You can only create [sparse indexes](/docs/manual/core/index-sparse#std-label-index-type-sparse) on the `metaField`.

MongoDB doesn't support the following index types on time series collections:

- [Text indexes](/docs/manual/core/indexes/index-types/index-text#std-label-index-type-text)

- [Unique indexes](/docs/manual/core/index-unique#std-label-index-type-unique)

If there are [secondary indexes](/docs/manual/reference/glossary#std-term-secondary-index) on [time series collections](/docs/manual/core/timeseries-collections#std-label-manual-timeseries-collection) and you need to downgrade the feature compatibility version (FCV), you must first drop any secondary indexes that are incompatible with the downgraded FCV. For more information, see [`setFeatureCompatibilityVersion`.](/docs/manual/reference/command/setFeatureCompatibilityVersion#mongodb-dbcommand-dbcmd.setFeatureCompatibilityVersion)

## Capped Collections

You cannot create a time series collection as a [capped collection.](/docs/manual/core/capped-collections#std-label-manual-capped-collection)

## Modification of Collection Type

You can only set the collection type when you create a collection:

- You cannot convert an existing collection into a time series collection.

- You cannot convert a time series collection into a different collection type.

To move data from an existing collection to a time series collection, [migrate data into a time series collection.](/docs/manual/core/timeseries/timeseries-migrate-data-into-timeseries-collection#std-label-migrate-data-into-a-timeseries-collection)

## timeField and metaField

Starting in MongoDB 8.3, you cannot create a `timeField` that starts with a `$` character.

You can only set a collection's `timeField` and `metaField` parameters when you create the collection. You cannot modify these parameters later.

## Granularity

### Bucket Size

For any configuration of granularity parameters, the maximum size of a bucket is 1000 measurements or 125KB of data, whichever is lower. MongoDB may also enforce a lower maximum size for high cardinality data with many unique values, so that the working set of buckets fits within the [WiredTiger cache.](/docs/manual/core/wiredtiger#std-label-storage-wiredtiger)

#### Modifying Bucket Parameters

Once you set a collection's `granularity` or the custom bucketing parameters `bucketMaxSpanSeconds` and `bucketRoundingSeconds`, you can increase the time span covered by a bucket, but not decrease it. Use the [`collMod`](/docs/manual/reference/command/collMod#mongodb-dbcommand-dbcmd.collMod) command to modify the parameters.

For more information on modifying time series intervals, see [Change Time Series Granularity.](/docs/manual/core/timeseries/timeseries-granularity#std-label-change-granularity)

**Note:**

`bucketMaxSpanSeconds` and `bucketRoundingSeconds` must be equal. If you modify one parameter, you must also set the other to the same value.

## Sharding

Time series collections are subject to several sharding limitations.

### Sharding Administration Commands

You cannot run sharding administration commands on sharded time series collections.

### Shard Key Fields

When sharding time series collections, you can only specify the following fields in the shard key:

- The `metaField`

- Sub-fields of `metaField`

- The `timeField`

You may specify combinations of these fields in the shard key. No other fields, including `_id`, are allowed in the shard key pattern.

When you specify the shard key:

- `metaField` can be either a:

  - [Hashed shard key](/docs/manual/core/hashed-sharding#std-label-sharding-hashed-sharding)

  - [Ranged shard key](/docs/manual/core/ranged-sharding#std-label-sharding-ranged)

- `timeField` must be:

  - A [ranged shard key](/docs/manual/core/ranged-sharding#std-label-sharding-ranged)

  - At the end of the shard key pattern

**Tip:**

Avoid specifying **only** the `timeField` as the shard key. Since the `timeField` [increases monotonically](/docs/manual/core/sharding-choose-a-shard-key#std-label-shard-key-monotonic), it may result in all writes appearing on a single chunk within the cluster. Ideally, data is evenly distributed across chunks.

To learn how to best choose a shard key, see:

- [Choose a Shard Key](/docs/manual/core/sharding-choose-a-shard-key#std-label-sharding-shard-key-requirements)

- [MongoDB Blog: On Selecting a Shard Key for MongoDB.](https://www.mongodb.com/blog/post/on-selecting-a-shard-key-for-mongodb)

**Warning:**

Starting in MongoDB 8.0, shard keys containing the `timeField` are deprecated for time series collections.

### Resharding

Starting in MongoDB 8.0.10, you can reshard a time series collection. All shards in the time series collection must run version 8.0.10 or later to reshard.

For more information, see [Reshard a Collection.](/docs/manual/core/sharding-reshard-a-collection#std-label-sharding-resharding)

### Zone Sharding

Zone sharding does not support time series collections. The balancer always distributes data in sharded time series collections evenly across all shards in the cluster.

## Transactions

You cannot write to time series collections in [transactions.](/docs/manual/core/transactions#std-label-transactions)

**Note:**

MongoDB supports reads from time series collections in transactions.

## Views

Time series collections are writable non-materialized [views](/docs/manual/core/views#std-label-views-landing-page). Limitations for views apply to time series collections.

## Snapshot Isolation

Read operations on time series collections with read concern `"snapshot"` guarantee snapshot isolation only in the absence of concurrent drop or rename operations on collections in the read operation. Re-creating a time series collection on the same namespace with different granularity setting does not yield full snapshot isolation.
