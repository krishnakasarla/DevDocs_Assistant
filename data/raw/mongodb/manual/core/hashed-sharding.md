> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Hashed Sharding

Hashed sharding uses either a [single field hashed index](/docs/manual/core/indexes/index-types/index-hashed#std-label-index-hashed-index) or a [compound hashed index](/docs/manual/core/indexes/index-types/index-hashed/create#std-label-index-type-compound-hashed) as the shard key to partition data across your sharded cluster.

Sharding on a Single Field Hashed Index

Hashed sharding provides a more even data distribution across the sharded cluster at the cost of reducing [Targeted Operations vs. Broadcast Operations](/docs/manual/core/sharded-cluster-query-router#std-label-sharding-query-isolation). Post-hash, documents with "close" shard key values are unlikely to be on the same chunk or shard - the [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) is more likely to perform [Broadcast Operations](/docs/manual/core/sharded-cluster-query-router#std-label-sharding-mongos-broadcast) to fulfill a given ranged query. [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) can target queries with equality matches to a single shard.

![Diagram of the hashed based segmentation.](/images/sharding-hash-based.bakedsvg.svg)

Hashed indexes compute the hash value of a single field as the index value; this value is used as your shard key.&#x20;

Sharding on a Compound Hashed Index

MongoDB includes support for creating compound indexes with a single [hashed field](/docs/manual/core/indexes/index-types/index-hashed#std-label-index-type-hashed). To create a compound hashed index, specify `hashed` as the value of any single index key when creating the index.

Compound hashed index compute the hash value of a single field in the compound index; this value is used along with the other fields in the index as your shard key.

Compound hashed sharding supports features like [zone sharding](/docs/manual/core/zone-sharding#std-label-zone-sharding), where the prefix (i.e. first) non-hashed field or fields support zone ranges while the hashed field supports more even distribution of the sharded data. Compound hashed sharding also supports shard keys with a hashed prefix for resolving data distribution issues related to [monotonically increasing fields.](/docs/manual/core/sharding-choose-a-shard-key#std-label-shard-key-monotonic)

**Tip:**

MongoDB automatically computes the hashes when resolving queries using hashed indexes.  Applications do **not** need to compute hashes.

**Warning:**

MongoDB `hashed` indexes truncate floating point numbers to 64-bit integers before hashing. For example, a `hashed` index would store the same value for a field that held a value of `2.3`, `2.2`, and `2.9`. To prevent collisions, do not use a `hashed` index for floating point numbers that cannot be reliably converted to 64-bit integers (and then back to floating point). MongoDB `hashed` indexes do not support floating point values larger than 2 53.

To see what the hashed value would be for a key, see [`convertShardKeyToHashed()`.](/docs/manual/reference/method/convertShardKeyToHashed#mongodb-method-convertShardKeyToHashed)

[`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) provides the  [`convertShardKeyToHashed()`](/docs/manual/reference/method/convertShardKeyToHashed#mongodb-method-convertShardKeyToHashed) method. This method uses the same hashing function as the hashed index and can be used to see what the hashed value would be for a key.

## Hashed Sharding Shard Key

The field you choose as your hashed shard key should have a good [cardinality](/docs/manual/core/sharding-choose-a-shard-key#std-label-shard-key-range), or large number of different values. Hashed keys are ideal for shard keys with fields that change [monotonically](/docs/manual/core/sharding-choose-a-shard-key#std-label-shard-key-monotonic) like [ObjectId](/docs/manual/reference/glossary#std-term-ObjectId) values or timestamps. A good example of this is the default `_id` field, assuming it only contains [ObjectId](/docs/manual/reference/glossary#std-term-ObjectId) values.

To shard a collection using a hashed shard key, see [Shard a Collection.](/docs/manual/tutorial/deploy-shard-cluster#std-label-deploy-hashed-sharded-cluster-shard-collection)

## Hashed vs Ranged Sharding

Given a collection using a monotonically increasing value `X` as the shard key, using ranged sharding results in a distribution of incoming inserts similar to the following:

![Diagram of poor shard key distribution due to monotonically increasing or decreasing shard key](/images/sharded-cluster-monotonic-distribution.bakedsvg.svg)

Since the value of `X` is always increasing, the chunk with an upper bound of [`MaxKey`](/docs/manual/reference/mongodb-extended-json#mongodb-bsontype-MaxKey) receives the majority incoming writes. This restricts insert operations to the single shard containing this chunk, which reduces or removes the advantage of distributed writes in a sharded cluster.

By using a hashed index on `X`, the distribution of inserts is similar to the following:

![Diagram of hashed shard key distribution](/images/sharded-cluster-hashed-distribution.bakedsvg.svg)

Since the data is now distributed more evenly, inserts are efficiently distributed throughout the cluster.

## Shard the Collection

Use the [`sh.shardCollection()`](/docs/manual/reference/method/sh.shardCollection#mongodb-method-sh.shardCollection) method, specifying the full namespace of the collection and the target [hashed index](/docs/manual/core/indexes/index-types/index-hashed#std-label-index-type-hashed) to use as the [shard key.](/docs/manual/reference/glossary#std-term-shard-key)

```javascript
sh.shardCollection( "database.collection", { <field> : "hashed" } )
```

To shard a collection on a [compound hashed index](/docs/manual/core/indexes/index-types/index-hashed/create#std-label-index-type-compound-hashed), specify the full namespace of the collection and the target compound hashed index to use as the [shard key:](/docs/manual/reference/glossary#std-term-shard-key)

```javascript
sh.shardCollection(
  "database.collection",
  { "fieldA" : 1, "fieldB" : 1, "fieldC" : "hashed" }
)
```

**Important:**

- Starting in MongoDB 5.0, you can [reshard a collection](/docs/manual/core/sharding-reshard-a-collection#std-label-sharding-resharding) by changing a collection's shard key.

- You can [refine a shard key](/docs/manual/core/sharding-refine-a-shard-key#std-label-shard-key-refine) by adding a suffix field or fields to the existing shard key.

### Shard a Populated Collection

If you shard a populated collection using a hashed shard key:

- The sharding operation creates an initial chunk to cover all of the shard key values.

- After the initial chunk creation, the balancer moves ranges of the initial chunk when it needs to balance data.

### Shard an Empty Collection

The shard collection operation can perform an initial chunk creation and distribution for empty or non-existing collections if [zones and zone ranges](/docs/manual/core/zone-sharding) have been defined for the collection. Initial creation and distribution of chunk allows for faster setup of zoned sharding. After the initial distribution, the balancer manages the chunk distribution going forward per usual.

Sharding Empty Collection on Single Field Hashed Shard Key

- With no [zones and zone ranges](/docs/manual/core/zone-sharding#std-label-zones-sharding) specified for the empty or non-existing collection:

  - The sharding operation creates an empty chunk to cover the entire range of the shard key values. Starting in version 8.0, the operation creates 1 chunk per shard by default and migrates across the cluster. This initial creation and distribution of chunks allows for faster setup of sharding.

  - After the initial distribution, the balancer manages the chunk distribution going forward.

- With zones and zone ranges specified for the empty or a non-existing collection:

  - The sharding operation creates empty chunks for the defined zone ranges as well as any additional chunks to cover the entire range of the shard key values and performs an initial chunk distribution based on the zone ranges. This initial creation and distribution of chunks allows for faster setup of zoned sharding.

  - After the initial distribution, the balancer manages the chunk distribution going forward.

Sharding Empty Collection on Compound Hashed Shard Key with Hashed Field Prefix

If the compound hashed shard key has the hashed field as the prefix (the hashed field is the first field in the shard key):

- With no zones and zone ranges specified for the empty or non-existing collection:

  - The sharding operation creates empty chunks to cover the entire range of the shard key values and performs an initial chunk distribution. The value of all non-hashed fields is [`MinKey`](/docs/manual/reference/mongodb-extended-json#mongodb-bsontype-MinKey) at each split point. Starting in version 8.0, the operation creates 1 chunk per shard by default and migrates across the cluster. This initial creation and distribution of chunks allows for faster setup of sharding.

  - After the initial distribution, the balancer manages the chunk distribution going forward.

- With a *single* zone with a range from `MinKey` to `MaxKey` specified for the empty or a non-existing collection *and* the `presplitHashedZones` option specified to [`sh.shardCollection()`:](/docs/manual/reference/method/sh.shardCollection#mongodb-method-sh.shardCollection)

  - The sharding operation creates empty chunks for the defined zone range as well as any additional chunks to cover the entire range of the shard key values and performs an initial chunk distribution based on the zone ranges. This initial creation and distribution of chunks allows for faster setup of zoned sharding.

  - After the initial distribution, the balancer manages the chunk distribution going forward.

Sharding Empty Collection on Compound Hashed Shard Key with Non-Hashed Prefix

If the compound hashed shard key has one or more non-hashed fields as the prefix (i.e. the hashed field is *not* the first field in the shard key):

- With no zones and zone ranges specified for the empty or non-existing collection *and* [preSplitHashedZones](/docs/manual/reference/method/sh.shardCollection#std-label-method-shard-collection-presplitHashedZones) is `false` or omitted, MongoDB does not perform any initial chunk creation or distribution when sharding the collection.

- With no zones and zone ranges specified for the empty or non-existing collection *and* [preSplitHashedZones](/docs/manual/reference/method/sh.shardCollection#std-label-method-shard-collection-presplitHashedZones), [`sh.shardCollection()`](/docs/manual/reference/method/sh.shardCollection#mongodb-method-sh.shardCollection) / [`shardCollection`](/docs/manual/reference/command/shardCollection#mongodb-dbcommand-dbcmd.shardCollection) returns an error.

- With zones and zone ranges specified for the empty or a non-existing collection *and* the [preSplitHashedZones](/docs/manual/reference/method/sh.shardCollection#std-label-method-shard-collection-presplitHashedZones) option specified to [`sh.shardCollection()`:](/docs/manual/reference/method/sh.shardCollection#mongodb-method-sh.shardCollection)

  - The sharding operation creates empty chunks for the defined zone ranges as well as any additional chunks to cover the entire range of the shard key values.

  - The sharding operation further subdivides the initial chunk for each range, such that each shard in the zone is allocated an equal number of chunks.

  - This initial creation and distribution of chunks allows for faster setup of zoned sharding. After the initial distribution, the balancer manages the chunk distribution going forward.

  The defined ranges for each zone *must* meet certain requirements. For a description of the requirements and a complete example, see [Pre-Define Zones and Zone Ranges for an Empty or Non-Existing Collection.](/docs/manual/reference/method/sh.updateZoneKeyRange#std-label-pre-define-zone-range-hashed-example)

### Drop a Hashed Shard Key Index

Starting in MongoDB 7.0.3 (and 6.0.12 and 5.0.22), you can drop the index for a hashed shard key.

This can speed up data insertion for collections sharded with a hashed shard key.

For details, see [Drop a Hashed Shard Key Index.](/docs/manual/tutorial/drop-a-hashed-shard-key-index#std-label-drop-a-hashed-shard-key-index)

**See also:**

To learn how to deploy a sharded cluster and implement hashed sharding, see [Deploy a Self-Managed Sharded Cluster.](/docs/manual/tutorial/deploy-shard-cluster#std-label-sharding-procedure-setup)
