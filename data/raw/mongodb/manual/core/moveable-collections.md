> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Moveable Collections

**New in version 8.0**

Starting in MongoDB 8.0, you can move an unsharded collection to a different shard using the [`moveCollection`](/docs/manual/reference/command/moveCollection#mongodb-dbcommand-dbcmd.moveCollection) command.

## Use Cases

Moving unsharded collections to any shard can:

- Optimize performance on larger, complex workloads.

- Achieve better resource utilization.

- More evenly distribute data across shards.

Consider the following scenarios:

- A company runs an e-commerce platform with several unsharded collections, such as `products`, `orders`, and `users` on a single shard. The `orders` collection begins to grow significantly larger than the others, which causes performance issues on the shard. To improve performance and balance the load across the cluster, the administrator can use the `moveCollection` command to move the smaller `products` and `users` collections to a different shard.

- A global application stores user data in three separate unsharded collections for users located in North America, Europe, and Asia on one shard. To reduce latency for users, an administrator can move these collections to a shard located in each respective region in the same cluster.

- An application frequently performs [`$lookup`](/docs/manual/reference/operator/aggregation/lookup#mongodb-pipeline-pipe.-lookup) operations between two unsharded collections, `orders` and `customers`, that reside on different shards. To improve query performance, a database administrator can move both collections to the same shard.

## Get Started

- [Move a Collection](/docs/manual/tutorial/move-a-collection#std-label-task-move-a-collection)

- [Stop Moving a Collection](/docs/manual/tutorial/stop-moving-a-collection#std-label-task-stop-moving-a-collection)

## Access Control

To move unsharded collections on a deployment that enforces authentication, you must authenticate as a user with at least the [`enableSharding`](/docs/manual/reference/built-in-roles#mongodb-authrole-enableSharding) role.

## Learn More

- [Primary Shard](/docs/manual/core/sharded-cluster-shards#std-label-primary-shard)

- [Sharded and Non-Sharded Collections](/docs/manual/sharding#std-label-sharded-vs-non-sharded-collections)
