> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Display a Shard Key

Every sharded collection has a [shard key](/docs/manual/core/sharding-shard-key#std-label-sharding-shard-key). To display the shard key, connect to a [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instance and run the [`db.printShardingStatus()`](/docs/manual/reference/method/db.printShardingStatus#mongodb-method-db.printShardingStatus) method:

```javascript
db.printShardingStatus()
```

The output resembles:

```javascript
<dbname>.<collection>
   shard key: { <shard key> : <1 or hashed> }
   unique: <boolean>
   balancing: <boolean>
   allowMigrations: <boolean>
   chunks:
      <shard name1> <number of chunks>
      <shard name2> <number of chunks>
      ...
   { <shard key>: <min range1> } -->> { <shard key> : <max range1> } on : <shard name> <last modified timestamp>
   { <shard key>: <min range2> } -->> { <shard key> : <max range2> } on : <shard name> <last modified timestamp>
   ...
   tag: <tag1>  { <shard key> : <min range1> } -->> { <shard key> : <max range1> }
   ...
```

For more details on the `db.printShardingStatus()` output, see the [sharded collection section](/docs/manual/reference/method/sh.status#std-label-sharded-collection-output-reference) on the [`sh.status()`](/docs/manual/reference/method/sh.status#mongodb-method-sh.status) page.
