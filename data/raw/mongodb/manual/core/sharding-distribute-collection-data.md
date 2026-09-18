> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Distribute Collection Data

Sharding a collection distributes its documents across multiple shards in your MongoDB cluster. MongoDB uses your specified shard key to determine precisely where each document belongs. Choosing an effective shard key is critical, ensuring even data distribution and workload balancing across all available shards. This approach becomes essential when collections grow too large for a single shard to handle efficiently. Once sharded, MongoDB automatically distributes the collection across all available shards according to your chosen sharding strategy.

## When to Consider Sharding

You should consider sharding a collection when you approach certain resource limits or performance thresholds.

### High Resource Utilization

If a collection’s [working set](/docs/manual/reference/glossary#std-term-working-set) fits in RAM, MongoDB serves queries from memory, which provides the fastest query response times. When the working set grows beyond available memory, query latencies grow longer due to increased disk access. Sharding a collection improves query performance by distributing the data across multiple shards, where each shard maintains its own data indexes.

### Large Data Size

If your collection contains 3TB of data or more, you should consider sharding it to optimize performance.

## Distribution Options

When sharding a collection in MongoDB, you can choose from the following distribution options:

| Option | Description |
| --- | --- |
| [Ranged Sharding](/docs/manual/core/ranged-sharding#std-label-sharding-ranged) | Ranged sharding uses one or more document fields to determine data placement. Data with similar shard key values is stored on the same shard, optimizing range-based queries. This approach works best when your access patterns include range operations. |
| [Hashed Sharding](/docs/manual/core/hashed-sharding#std-label-sharding-hashed) | Hashed sharding computes a hash value from your specified field and distributes data randomly across shards. While useful for write scalability, this approach can impact performance for range-based queries since logically adjacent data may reside on different shards. |
| [Zone Sharding](/docs/manual/core/zone-sharding#std-label-zone-sharding) | Zone sharding distributes collections across a specific subset of shards rather than the entire cluster. This approach is ideal when collections exceed single-shard capacity but require strategic placement—whether for geographic proximity to users, optimizing for distinct access patterns with specialized hardware, or maintaining regulatory compliance by controlling data location. |

## Behavior

When sharding a collection, you must:

- Choose a shard key. Use the [`analyzeShardKey`](/docs/manual/reference/command/analyzeShardKey#mongodb-dbcommand-dbcmd.analyzeShardKey) database command to facilitate this choice.

- Select a sharding method:

  - [Sharded Cluster Balancer](/docs/manual/core/sharding-balancer-administration#std-label-sharding-balancing) for automatic data migration

  - [Reshard to shard](/docs/manual/tutorial/resharding-back-to-same-key#std-label-resharding-a-collection-back-to-same-key) for complete redistribution

## Learn More

- [Shard a Collection](/docs/manual/core/sharding-shard-key#std-label-sharding-shard-key-creation)
