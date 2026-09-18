> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Multi-tenant Architecture with Moveable Collections

**New in version 8.0**

In a multi-tenant architecture, a single instance of an application serves multiple users. Multi-tenant users share resources, and generally data belonging to the same tenant is kept on a single shard.

If your multi-tenant configuration has a single tenant per database and the majority of its workload takes place on a single shard, you can move frequently-accessed collections to other shards for more even workload distribution. This reduces the number of collections on the original shard and improves performance system-wide.

**Note: Non-Sharded Clusters**

If your multi-tenant deployment is a replica set, you can convert it to a sharded cluster and add additional shards to more evenly distribute your workload. For more information, see either:

- [Modify a Cluster](https://www.mongodb.com/docs/atlas/scale-cluster/) for MongoDB Atlas deployments

- [Convert a Self-Managed Replica Set to a Sharded Cluster](/docs/manual/tutorial/convert-replica-set-to-replicated-shard-cluster#std-label-manual-convert-replica-set-to-sharded-cluster)

## Considerations

- Moving collections has operational overhead. Before you move collections, review the [`sh.moveCollection()`](/docs/manual/reference/method/sh.moveCollection#mongodb-method-sh.moveCollection) documentation for performance considerations.

- The optimal multi-tenant configuration depends on your workload and application needs. Moving collections to new shards is not as scalable as [multi-tenancy in a single database with shared collections](https://www.mongodb.com/docs/atlas/build-multi-tenant-arch/#std-label-all-tenants-single). However, having each database correspond to a single tenant allows for more customizable security and access patterns.

- To optimize performance for cross-collection operations (like [`$lookup`](/docs/manual/reference/operator/aggregation/lookup#mongodb-pipeline-pipe.-lookup) or transactions that access multiple collections), place all collections for a given tenant on the same shard.

## Learn More

- [Move a Collection](/docs/manual/tutorial/move-a-collection#std-label-task-move-a-collection)

- [Build a Multi-Tenant Architecture](https://www.mongodb.com/docs/atlas/build-multi-tenant-arch/)
