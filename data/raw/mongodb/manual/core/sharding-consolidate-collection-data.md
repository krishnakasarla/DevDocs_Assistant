> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Consolidate Collection Data

Prior to MongoDB v8.0, sharding a collection was an irreversible action. Starting in v8.0, you can unshard a collection to the shard of your choice.

## When to Unshard a Collection

The following scenarios benefit from moving unsharded collections across shards.

### Correcting unintentional sharding of a collection

If you discover that sharding was unnecessary or causing performance issues, you can use the\`\`unshardCollection\`\` command to rewrite the entire collection as an unsharded collection.

### Simplifying zone-based isolation

If you use [zones](/docs/manual/core/zone-sharding#std-label-zone-sharding) to keep a sharded collection on a single shard, you can now unshard the collection to reduce the complexity in your cluster.

### Consolidating previously sharded small collections

If you sharded small collections to efficiently utilize resources on multiple shards, you can unshard and move the collections to a shard of your choice. Doing so reduces the complexity of a deployment while maintaining appropriate resource allocation.

## Command Syntax

```javascript
sh.unshardCollection("database.collection", "shardName")
```

The following example unshards the `riders` collection in the `taxi` database and moves the collection to `shard1`.

```javascript
db.adminCommand({unshardCollection:"taxi.riders", toShard: "shard1"})
```

![Unsharded rider collection gets moved to shard1.](/images/sharding-unshard-collection.bakedsvg.svg)

## Learn More

- [Unshard a Collection](/docs/manual/tutorial/unshard-collection#std-label-unshard-collection-task)
