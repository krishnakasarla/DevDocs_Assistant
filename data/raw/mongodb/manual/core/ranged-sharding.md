> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Ranged Sharding

Range-based sharding involves dividing data into contiguous ranges determined by the shard key values. In this model, documents with "close" shard key values are likely to be in the same [chunk](/docs/manual/reference/glossary#std-term-chunk) or [shard](/docs/manual/reference/glossary#std-term-shard). This allows for efficient queries where reads target documents within a contiguous range. However, both read and write performance may decrease with poor shard key selection. See [Shard Key Selection.](/docs/manual/core/ranged-sharding#std-label-sharding-ranged-shard-key)

![Diagram of the shard key value space segmented into smaller ranges or chunks.](/images/sharding-range-based.bakedsvg.svg)

Range-based sharding is the default sharding methodology if no other options such as those required for [Hashed Sharding](/docs/manual/core/hashed-sharding) or [zones](/docs/manual/core/zone-sharding#std-label-zone-sharding) are configured.

## Shard Key Selection

Ranged sharding is most efficient when the shard key displays the following traits:

- Large [Shard Key Cardinality](/docs/manual/core/sharding-choose-a-shard-key#std-label-shard-key-range)

- Low [Shard Key Frequency](/docs/manual/core/sharding-choose-a-shard-key#std-label-shard-key-frequency)

- Non-[Monotonically Changing Shard Keys](/docs/manual/core/sharding-choose-a-shard-key#std-label-shard-key-monotonic)

The following image illustrates a sharded cluster using the field `X` as the shard key. If the values for `X` have a large range, low frequency, and change at a non-monotonic rate, the distribution of inserts may look similar to the following:

![Diagram of good shard key distribution](/images/sharded-cluster-ranged-distribution-good.bakedsvg.svg)

## Shard a Collection

Use the [`sh.shardCollection()`](/docs/manual/reference/method/sh.shardCollection#mongodb-method-sh.shardCollection) method, specifying the full namespace of the collection and the target [index](/docs/manual/reference/command/collMod#mongodb-collflag-index) or [compound index](/docs/manual/reference/glossary#std-term-compound-index) to use as the [shard key.](/docs/manual/reference/glossary#std-term-shard-key)

```javascript
sh.shardCollection( "database.collection", { <shard key> } )
```

**Important:**

- Starting in MongoDB 5.0, you can [reshard a collection](/docs/manual/core/sharding-reshard-a-collection#std-label-sharding-resharding) by changing a collection's shard key.

- You can [refine a shard key](/docs/manual/core/sharding-refine-a-shard-key#std-label-shard-key-refine) by adding a suffix field or fields to the existing shard key.

### Shard a Populated Collection

If you shard a populated collection, only one chunk is created initially. The balancer then migrates ranges from that chunk if necessary according to the configured range size.

### Shard an Empty Collection

If you shard an empty collection:

- With no [zones and zone ranges](/docs/manual/core/zone-sharding#std-label-zone-sharding) specified for the empty or non-existing collection:

  - The sharding operation creates a single empty chunk to cover the entire range of the shard key values.

  - After the initial chunk creation, the balancer migrates the initial chunk across the shards as appropriate as well as manages the chunk distribution going forward.

- With zones and zone ranges specified for the empty or a non-existing collections:

  - The sharding operation creates empty chunks for the defined zone ranges as well as any additional chunks to cover the entire range of the shard key values and performs an initial chunk distribution based on the zone ranges. This initial creation and distribution of chunks allows for faster setup of zoned sharding.

  - After the initial distribution, the balancer manages the chunk distribution going forward.

**See also:**

To learn how to deploy a sharded cluster and implement ranged sharding, see [Deploy a Self-Managed Sharded Cluster.](/docs/manual/tutorial/deploy-shard-cluster#std-label-sharding-procedure-setup)
