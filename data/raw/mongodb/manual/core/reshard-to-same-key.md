> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Reshard to the Same Shard Key

Starting in MongoDB 8.0, you can reshard to the same shard key to move data with no downtime or impact on workload. This enables you to:

- Use the [Reshard to Shard](/docs/manual/core/reshard-to-same-key#std-label-reshard-to-shard-def) technique to shard a collection and distribute its data across all relevant shards

- Add new shards faster

- Remove shards faster

- Rewrite collections to reclaim disk space

Starting in MongoDB 8.0, resharding reads data using natural order scan. Resharding first clones all the data and then builds relevant indexes, resulting in orders of magnitude speed improvement of the resharding process.

## Command Syntax

You can reshard to the same key using the `reshardCollection` command with `forceRedistribution` set to `true`.

The `reshardCollection` command has the following syntax:

```javascript
db.adminCommand(
   {
     reshardCollection: "<database>.<collection>",
     key: { "<shardkey>" },
     unique: <boolean>,
     numInitialChunks: <integer>,
     numSamplesPerChunk: <integer>,  // New in MongoDB 8.0.20
     collation: { locale: "simple" },
     zones: [
         {
             min: { "<document with same shape as shardkey>" },
             max: { "<document with same shape as shardkey>" },
             zone: <string> | null
         },
     ],
     forceRedistribution: <bool>
   }
)
```

**Note:**

Resharding operations ignore the `numInitialChunks` setting when the shard key contains a hashed prefix. Instead, MongoDB deterministically splits the hashed key space among recipients, using the same approach as initial chunk creation for empty hashed collections.

For details, see [`reshardCollection`.](/docs/manual/reference/command/reshardCollection#mongodb-dbcommand-dbcmd.reshardCollection)

## Use Cases

Resharding is a strategy to move data with no downtime or impact on workload. Use the [Reshard to Shard](/docs/manual/core/reshard-to-same-key#std-label-reshard-to-shard-def) technique to shard a collection and distribute data across all shards.

Use resharding to distribute your collections across all relevant shards faster than [chunk migrations](/docs/manual/tutorial/migrate-chunks-in-sharded-cluster#std-label-migrate-chunks-sharded-cluster). Resharding writes to all shards in parallel while each shard can only participate in one chunk migration at a time. Resharding drops the old collection at the end of the process. There are no orphan documents at the end of resharding.

### Reshard to Shard

The **Reshard to Shard** technique lets you use resharding to shard a collection and distribute the data to all of the shards in a cluster.

Consider using **Reshard to Shard** when you are initially sharding a collection of any size across any number of shards. If your deployment meets the [resource requirements](/docs/manual/core/reshard-to-same-key#std-label-reshard-to-same-key-behavior), use **Reshard to Shard** no matter how large the collection you want to shard.

## Behavior

### Storage

Calculate the required storage space for the resharding operation by adding your collection size and index size, assuming a minimum oplog window of 24 hours by using this formula:

```none
Available storage required on each shard = [(collection size + index size) *2 ] / number of shards the collection will be distributed across.
```

For example, a 2TB collection and 400GB of indexes distributed across 4 shards will need a minimum of 1.2TB of available storage per shard:

```none
[ (2 TB + 400GB) * 2 ] / 4 shards = 1.2 TB / shard
```

You must confirm that you have the available storage space in your cluster.

If there is insufficient space or I/O headroom available, you must increase the storage size. If there is insufficient CPU headroom, you must scale up the cluster by selecting a higher instance size.

**Tip:**

If your MongoDB cluster is hosted on Atlas, you can use the Atlas UI to review storage, CPU, and I/O headroom metrics.

### Latency

You must ensure that your application can tolerate two seconds where the collection being resharded blocks writes. When writes are blocked, your application experiences an increase in latency. If your workload cannot tolerate this requirement, use chunk migrations to balance your cluster.

### Reshard Limitations

- If the collection uses [Atlas Search](https://www.mongodb.com/docs/search/#std-label-atlas-search), the search index becomes unavailable after the operation completes. To restore it, manually rebuild the search index.

- Collections that use queryable encryption are not supported.

### Additional Resource Requirements

Your cluster must meet these additional requirements:

- A minimum oplog window of 24 hours.

- I/O capacity below 50%.

- CPU load below 80%.

## Get Started

- [Reshard a Collection back to the Same Shard Key](/docs/manual/tutorial/resharding-back-to-same-key#std-label-resharding-a-collection-back-to-same-key)

- [Resharding for Adding and Removing Shards](/docs/manual/tutorial/resharding-for-adding-and-removing-shards#std-label-resharding-for-adding-and-removing-shards-tutorial)

## Learn More

- [`sh.reshardCollection()`](/docs/manual/reference/method/sh.reshardCollection#mongodb-method-sh.reshardCollection)

- [Reshard a Collection](/docs/manual/core/sharding-reshard-a-collection#std-label-sharding-resharding)
