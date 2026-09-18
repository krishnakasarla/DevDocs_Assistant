> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Start Defragmenting a Sharded Collection

To start defragmenting a sharded collection, use the [`configureCollectionBalancing`](/docs/manual/reference/command/configureCollectionBalancing#mongodb-dbcommand-dbcmd.configureCollectionBalancing) command with the `defragmentCollection` option set to `true`.

## About this Task

Fragmentation is where a sharded collection's data is broken up into an unnecessarily large number of small chunks. This can increase operation times of CRUD operations run on that collection. Defragmentation reduces the number of chunks by merging smaller chunks into larger ones, resulting in lower CRUD operation times.

If CRUD operation times are acceptable, you don't need to defragment collections.

The following table summarizes defragmentation information for various MongoDB versions.

| MongoDB Version | Description |
| --- | --- |
| MongoDB 7.0 and later | Chunks are automatically merged. Performance improvements from defragmenting a collection in MongoDB 7.0 are lower compared to MongoDB 6.0. Typically, you don't need to defragment collections starting in MongoDB 7.0. |
| MongoDB 6.0 and earlier than 7.0 | Defragment collections only if you experience CRUD operation delays when the balancer migrates chunks or a node starts. Starting in MongoDB 6.0, high write traffic should not cause fragmentation. Chunk migrations cause fragmentation. |
| Earlier than MongoDB 6.0 | Defragment collections only if you experience longer CRUD operation times during metadata updates. For MongoDB versions earlier than 6.0, a sharded collection becomes fragmented when the collection size grows significantly because of many insert or update operations. |

The procedure in this task uses an example sharded collection named `ordersShardedCollection` in a database named `test`.

You can use your own sharded collection and database in the procedure.

## Before you Begin

Connect to [`mongos`.](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos)

## Procedure

1. Start defragmenting the collection

   Run:

   ```javascript
   db.adminCommand(
      {
         configureCollectionBalancing: "test.ordersShardedCollection",
         defragmentCollection: true
      }
   )
   ```

2. Ensure defragmentation started

   Ensure `ok` is `1` in the command output, which indicates the command execution was successful:

   ```javascript
   {
      ok: 1,
      '$clusterTime': {
         clusterTime: Timestamp({ t: 1677616966, i: 8 }),
         signature: {
            hash: Binary(Buffer.from("0000000000000000000000000000000000000000", "hex"), 0),
            keyId: Long("0")
         }
      },
      operationTime: Timestamp({ t: 1677616966, i: 8 })
   }
   ```

## Next Steps

You can monitor the collection's defragmentation progress. For details, see [Monitor Defragmentation of a Sharded Collection.](/docs/manual/core/defragment-sharded-collections/monitor-defragmentation-sharded-collection#std-label-monitor-defragmentation-sharded-collection)

## Learn More

- Print shard status, see [`db.printShardingStatus()`](/docs/manual/reference/method/db.printShardingStatus#mongodb-method-db.printShardingStatus)

- Retrieve shard status details, see [`sh.status()`](/docs/manual/reference/method/sh.status#mongodb-method-sh.status)

- View shard status collection fields, see [Sharded Collection](/docs/manual/reference/method/sh.status#std-label-sharding-status-collection-fields)

- See active mongos instances, see [Active `mongos` Instances](/docs/manual/reference/method/sh.status#std-label-sharding-status-mongoses)

- Monitor shards using MongoDB Atlas, see [Review Sharded Clusters](https://www.mongodb.com/docs/atlas/review-sharded-cluster-metrics/#review-sharded-clusters/)
