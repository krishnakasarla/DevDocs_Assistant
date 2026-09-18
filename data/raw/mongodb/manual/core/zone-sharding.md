> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Zones

In sharded clusters, you can create [zones](/docs/manual/reference/glossary#std-term-zone) of sharded data based on the [shard key](/docs/manual/reference/glossary#std-term-shard-key). You can associate each zone with one or more shards in the cluster. A shard can associate with any number of zones. In a balanced cluster, MongoDB migrates [chunks](/docs/manual/reference/glossary#std-term-chunk) covered by a zone only to those shards associated with the zone.

Some common deployment patterns where zones can be applied are as follows:

- Isolate a specific subset of data on a specific set of shards.

- Ensure that the most relevant data reside on shards that are geographically closest to the application servers.

- Route data to shards based on the hardware / performance of the shard hardware.

The following image illustrates a sharded cluster with three shards and two zones. The `A` zone represents a range with a lower boundary of `1` and an upper bound of `10`. The `B` zone represents a range with a lower boundary of `10` and an upper boundary of `20`. Shards `Alpha` and `Beta` have the `A` zone. Shard `Beta` also has the `B` zone. Shard `Charlie` has no zones associated with it. The cluster is in a steady state and no chunks violate any of the zones.

![Diagram of data distribution based on zones in a sharded cluster](/images/sharded-cluster-zones.bakedsvg.svg)

## Behavior and Operations

### Ranges

Each zone covers one or more ranges of [shard key](/docs/manual/reference/glossary#std-term-shard-key) values for a collection. Each range a zone covers is always inclusive of its lower boundary and exclusive of its upper boundary. Zones cannot share ranges, nor can they have overlapping ranges.

For example, consider a shard key on `{"x": 1}`. The cluster has the following zone ranges:

```javascript
{ "x" : 5 } --> { "x" : 10 } // Zone A
{ "x" : 10} --> { "x" : 20 } // Zone B
```

- A document with a shard key value of `7` is routed to zone A.

- A document with shard key value of `10` is routed to zone B.

### Hashed Shard Keys and Zone Ranges

For collections whose shard key includes a hashed field, zone ranges and data distribution on that field are on hashed values. The zone contains documents whose *hashed* shard key value falls into the defined range. A zone range on a hashed field does not have the same predictable document routing behavior as a zone range on an unhashed field.

For example, consider a shard key on `{"x" : "hashed"}`. The following range represents the *hashed* range between `5` and `10`:

```javascript
{ "x": Long("4470791281878691347") } --> { "x": Long("7766103514953448109") } // Zone A
```

- A document with a shard key value of `1` is routed to Zone A since the *hashed* value of `1` falls into the defined range.

- A document with a shard key value of `15` is routed to Zone A since the *hashed* value of `15` falls into the defined range.

- A document with a shard key value of `8` is not routed to Zone A since the *hashed* value of `8` does not fall into the defined range.

[`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) provides the [`convertShardKeyToHashed()`](/docs/manual/reference/method/convertShardKeyToHashed#mongodb-method-convertShardKeyToHashed) for computing the post-hash value of the specified parameter.

One valid use of zone ranges on a hashed field is to restrict the data for a collection to the shard or shards in a single zone. Create a zone range that covers the entire range of possible hashed shard key values using [`MinKey`](/docs/manual/reference/mongodb-extended-json#mongodb-bsontype-MinKey) as the lower bound and [`MaxKey`](/docs/manual/reference/mongodb-extended-json#mongodb-bsontype-MaxKey) as the upper bound.

To define ranges, MongoDB provides the [`updateZoneKeyRange`](/docs/manual/reference/command/updateZoneKeyRange#mongodb-dbcommand-dbcmd.updateZoneKeyRange) command and the associated helper methods [`sh.updateZoneKeyRange()`](/docs/manual/reference/method/sh.updateZoneKeyRange#mongodb-method-sh.updateZoneKeyRange) and [`sh.addShardTag()`.](/docs/manual/reference/method/sh.addShardTag#mongodb-method-sh.addShardTag)

You can run [`updateZoneKeyRange`](/docs/manual/reference/command/updateZoneKeyRange#mongodb-dbcommand-dbcmd.updateZoneKeyRange) database command and its helpers [`sh.updateZoneKeyRange()`](/docs/manual/reference/method/sh.updateZoneKeyRange#mongodb-method-sh.updateZoneKeyRange) and [`sh.addTagRange()`](/docs/manual/reference/method/sh.addTagRange#mongodb-method-sh.addTagRange) on an unsharded collection or a non-existing collection.

Dropping a collection deletes its associated zone/tag ranges.

### Initial Chunk Distribution

By defining the zones and the zone ranges *before* sharding an empty or a non-existing collection, the shard collection operation creates chunks for the defined zone ranges as well as any additional chunks to cover the entire range of the shard key values and performs an initial chunk distribution based on the zone ranges. This initial creation and distribution of chunks allows for faster setup of zoned sharding. After the initial distribution, the balancer manages the chunk distribution going forward.

MongoDB supports sharding collections on [compound hashed indexes](/docs/manual/core/indexes/index-types/index-hashed/create#std-label-index-type-compound-hashed). When sharding an empty or non-existing collection using a compound hashed shard key, additional requirements apply in order for MongoDB to perform initial chunk creation and distribution.

See [Pre-Define Zones and Zone Ranges for an Empty or Non-Existing Collection](/docs/manual/reference/method/sh.updateZoneKeyRange#std-label-pre-define-zone-range-hashed-example) for for an example.

**See also:**

[`sh.balancerCollectionStatus()`](/docs/manual/reference/method/sh.balancerCollectionStatus#mongodb-method-sh.balancerCollectionStatus)

### Balancer

The [balancer](/docs/manual/reference/glossary#std-term-balancer) attempts to evenly distribute a sharded collection's chunks across all shards in the cluster.

For each [chunk](/docs/manual/reference/glossary#std-term-chunk) marked for migration, the balancer checks each possible destination shard for any configured zones. If the chunk range falls into a zone, the balancer migrates the chunk into a shard inside that zone. Chunks that do not fall into a zone can exist on *any* shard in the cluster and are migrated normally.

During balancing rounds, if the balancer detects that any chunks violate the configured zones for a given shard, the balancer migrates those chunks to a shard where no conflict exists.

After associating a zone with a shard or shards and configuring the zone with a shard key range for a sharded collection, the cluster may take some time to migrate the affected data for the sharded collection. This depends on the division of chunks and the current distribution of data in the cluster. When balancing is complete, reads and writes for documents in a given zone are routed only to the shard or shards inside that zone.

Once configured, the balancer respects zones during future [balancing rounds.](/docs/manual/core/sharding-balancer-administration#std-label-sharding-internals-balancing)

**See also:**

[`sh.balancerCollectionStatus()`](/docs/manual/reference/method/sh.balancerCollectionStatus#mongodb-method-sh.balancerCollectionStatus)

### Shard Key

You must use fields contained in the [shard key](/docs/manual/reference/glossary#std-term-shard-key) when defining a new range for a zone to cover. If using a [compound](/docs/manual/reference/glossary#std-term-compound-index) shard key, the range must include the prefix of the shard key.

For example, given a shard key `{ a : 1, b : 1, c : 1 }`, creating or updating a range to cover values of `b` requires including `a` as the prefix. Creating or updating a range to covers values of `c` requires including `a` and `b` as the prefix.

You cannot create ranges using fields not included in the shard key. For example, if you wanted to use zones to partition data based on geographic location, the shard key would need the first field to contain geographic data.

When choosing a shard key for a collection, consider what fields you might want to use for configuring zones. See [Choose a Shard Key](/docs/manual/core/sharding-choose-a-shard-key#std-label-sharding-internals-choose-shard-key) for considerations in choosing a shard key.

### Shard Zone Boundaries

Zone ranges are always inclusive of the lower boundary and exclusive of the upper boundary.

**See also:**

[Manage Shard Zones](/docs/manual/tutorial/manage-shard-zone)

### Time Series Collections

Zone sharding does not support time series collections. The balancer always distributes data in sharded time series collections evenly across all shards in the cluster.
