> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Refine a Shard Key

Refining a collection's shard key allows for a more fine-grained data distribution and can address situations where the existing key has led to [jumbo chunks](/docs/manual/core/sharding-data-partitioning#std-label-jumbo-chunks) due to insufficient [cardinality.](/docs/manual/core/sharding-choose-a-shard-key#std-label-shard-key-cardinality)

**Warning:**

Do not modify the range or hashed type for any of the current shard key fields. It causes data inconsistencies. For example, do not modify a shard key from `{ customer_id: 1 }` to `{ customer_id:
    "hashed", order_id: 1 }`.

**Note:**

Starting in MongoDB 5.0, you can also [reshard your collection](/docs/manual/core/sharding-reshard-a-collection#std-label-sharding-resharding) by providing a new shard key for the collection. To learn whether you should reshard your collection or refine your shard key, see [Change a Shard Key.](/docs/manual/core/sharding-change-a-shard-key#std-label-change-a-shard-key)

To refine a collection's shard key, use the [`refineCollectionShardKey`](/docs/manual/reference/command/refineCollectionShardKey#mongodb-dbcommand-dbcmd.refineCollectionShardKey) command. The [`refineCollectionShardKey`](/docs/manual/reference/command/refineCollectionShardKey#mongodb-dbcommand-dbcmd.refineCollectionShardKey) adds a suffix field or fields to the existing key to create the new shard key.

For example, you may have an existing `orders` collection in a `test` database with the shard key `{ customer_id: 1 }`. You can use the [`refineCollectionShardKey`](/docs/manual/reference/command/refineCollectionShardKey#mongodb-dbcommand-dbcmd.refineCollectionShardKey) command to change the shard key to the new shard key `{ customer_id: 1, order_id: 1 }`:

```javascript
db.adminCommand( {
   refineCollectionShardKey: "test.orders",
   key: { customer_id: 1, order_id: 1 }
} )
```
