> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Manage Unsharded Collections

Collections on the same replica set can encounter performance bottlenecks when competing for resources. As your data grows beyond the available memory, increased disk I/O introduces latency and strains system resources, degrading overall application performance. Isolating collections on dedicated shards within your cluster reduces these resource constraints while maintaining a single connection point for your application.

Benefits of Collection Isolation:

- Workload Separation – Prevent resource contention by assigning collections to specific shards.

- Hardware Optimization – Configure [asymmetric shards](https://www.mongodb.com/docs/atlas/cluster-autoscaling/#std-label-independently-scaling-shards) with hardware tailored to specific collection requirements.

- Independent Scaling –  Scale collections individually based on workload growth.

- Improved Resilience – Reduce recovery time by isolating potential failures.

## When to Use `moveCollection`

Moving collections on dedicated shards is particularly beneficial when your collection requirements vary in the following ways:

| Requirement | Description |
| --- | --- |
| Access Patterns | Some of your collections are read-heavy, while others are write-heavy. |
| Performance | Certain collections require more RAM, CPU, or disk throughput than others. |
| Scalability Demands | Collections that have rapid or unpredictable growth patterns require dedicated hardware. |

Assigning collections to shards with the necessary hardware to meet their specific requirements optimizes performance while maintaining operational simplicity.

## When to Move Unsharded Collections

Starting in MongoDB 8.0, [movable collections](/docs/manual/core/moveable-collections#std-label-moveable-collections) allow you to strategically place any unsharded collection on any shard within the cluster. Previously, unsharded collections were restricted to the primary shard of their database, leading to resource bottlenecks. [Moving a collection](/docs/manual/tutorial/move-a-collection#std-label-task-move-a-collection) simplifies horizontal scaling by allowing you to relocate unsharded collections without disrupting workloads.

While not every collection needs to be sharded, deploying a sharded cluster provides horizontal scaling advantages even for unsharded collections. This approach maintains a single connection point for all data access, simplifying application architecture.

The following scenarios benefit from moving unsharded collections across shards:

### Workload Isolation

When multiple collections serve different workloads within the same cluster, moving unsharded collections across different shards helps prevent resource contention. This separation eliminates issues where one workload's performance negatively impacts others.

### Multi-Tenant Architecture

In environments hosting collections for different tenants, MongoDB's [`moveCollection`](/docs/manual/reference/command/moveCollection#mongodb-dbcommand-dbcmd.moveCollection) command enables seamless distribution of collections across shards without downtime. This flexibility optimizes resource allocation based on each tenant's specific needs.

### Geographic Data Distribution

Organizations may need to store user data in specific geographic regions to comply with data sovereignty regulations. With moveCollection, you can place unsharded collections on shards in different regions and relocate them as regulatory requirements evolve.

### Cost Optimization

Before MongoDB 8.0, all unsharded collections within a database were restricted to the primary shard. This limitation often forced upgrades to larger, more expensive instance tiers. MongoDB 8.0 removes this constraint, allowing movement of unsharded collections across all available shards in the cluster.

Moving unsharded collections across [asymmetric shard](https://www.mongodb.com/docs/atlas/cluster-autoscaling/#std-label-cluster-autoscaling) hardware delivers significant benefits for resource optimization, allowing you to place specific collections on hardware tailored to their requirements. By matching collections to appropriate hardware resources, you can scale different workloads independently based on their actual demands. This targeted approach improves performance while avoiding the cost of over-provisioning resources across the entire cluster.

### Reduced Collection Density

While MongoDB has no hard limit on collection count per instance, performance degrades when a node manages too many collections and indexes. To learn more about these limits, see [MongoDB Atlas Collection and Index Limits.](/docs/manual/reference/limits#std-label-limits-atlas-collection-and-index)

By distributing unsharded collections across different shards, you can reduce collection density on any single node while maintaining a unified access point for applications.

### Strategic co-location

Consider co-locating unsharded collections on the same shard to minimize distributed operations, such as cross-collection transactions or join operations ([`$lookup`](/docs/manual/reference/operator/aggregation/lookup#mongodb-pipeline-pipe.-lookup)). Keeping related operations confined to a single shard eliminates network overhead, reduces latency, and improves overall performance. This approach is particularly effective for collections that are frequently joined or accessed together in the same transaction.

## Command Syntax

```javascript
sh.moveCollection("database.collection", "shardName")
```

The following example moves four unsharded collection between two shards for equal distribution of collections:

```javascript
db.adminCommand({moveCollection:"E", toShard: "shard1"})
```

![Unsharded collections moving to a specified shard to distribute across two shards evenly.](/images/sharding-move-unsharded-collection.bakedsvg.svg)

## When to avoid using `moveCollection`

While `moveCollection` offers significant flexibility, there are a few specific scenarios where it may not be the optimal solution:

### Large Collections

Don't use `moveCollection` when a collection is too large for a single shard. Consider sharding a collection when it is approaching 3 TB in size.

### Collections with MongoDB Search Indexes

If a specific collection uses [MongoDB Search](https://www.mongodb.com/docs/atlas/atlas-search/), be aware that `moveCollection` uses [resharding](/docs/manual/core/sharding-reshard-a-collection#std-label-sharding-resharding) to rewrite the collection on a different shard. After moving the collection, you will need to manually rebuild its MongoDB Search index. Until the indexes are fully rebuilt, MongoDB Search functionality will be unavailable for this specific collection, though the rest of your application will function normally.

Before using `moveCollection`, evaluate these limitations against your application requirements to determine if it's the appropriate solution.

## Learn More

- [Move a Collection](/docs/manual/tutorial/move-a-collection#std-label-task-move-a-collection)
