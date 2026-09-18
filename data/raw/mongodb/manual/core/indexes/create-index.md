> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

<!--
Tab options on this page. Append to the .md URL to filter:
  ?tabs=<id,...>   select specific tabs (e.g. ?tabs=nodejs,shell)
  ?allTabs=true    include every tab
  (no param)       default: one tab per tabset

Available tabs:
  drivers: shell, csharp, java-async, java-sync, kotlin-coroutine, motor, nodejs, perl, php, python, ruby, scala
-->

# Create an Index

If your application repeatedly runs queries on the same fields, create an index on those fields to improve performance.

To create an index, use the [`createIndex()`](/docs/manual/reference/method/db.collection.createIndex#mongodb-method-db.collection.createIndex) shell method or equivalent method for your driver. This page shows examples for the MongoDB Shell and drivers.

## About this Task

When you run a create index command in the MongoDB Shell or a driver, MongoDB only creates the index if an index of the same specification does not exist.

Although indexes improve query performance, adding an index has negative performance impact for write operations. For collections with a high write-to-read ratio, indexes are expensive because each insert and update must also update any indexes.

**Warning:**

Do not create indexes on encrypted fields. Creating indexes on encrypted fields that use Queryable Encryption negatively affect performance. Instead, you can create an index on the `__safeContent__` field to support queries on encrypted fields.

## Procedure

***

➤ To set the language of the examples on this page, use the **Select your language** drop-down menu in the right navigation pane.

***

### Node.js

To create an index using the [Node.JS driver](https://www.mongodb.com/docs/drivers/node/current/), use `createIndex()`.

```javascript
collection.createIndex( { <key and index type specification> }, function(err, result) {
   console.log(result);
   callback(result);
} )
```

## Example

### Node.js

This example creates a single key ascending index on the `name` field:

```javascript
 collection.createIndex( { name : 1 }, function(err, result) {
   console.log(result);
   callback(result);
} )
```

## Results

Use [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) to monitor index creation.

To see what indexes exist on your collection, including indexes that are currently being built, run the [`db.collection.getIndexes()`](/docs/manual/reference/method/db.collection.getIndexes#mongodb-method-db.collection.getIndexes) method:

```javascript
db.collection.getIndexes()
```

**Output:**

```javascript
[
   { v: 2, key: { _id: 1 }, name: '_id_' },
   { v: 2, key: { name: -1 }, name: 'name_-1' }
]
```

To check whether your index is building, use [`$currentOp`](/docs/manual/reference/operator/aggregation/currentOp#mongodb-pipeline-pipe.-currentOp) with [`db.aggregate()`](/docs/manual/reference/method/db.aggregate#mongodb-method-db.aggregate) on the `admin` database.

The following aggregation pipeline uses the [`$match`](/docs/manual/reference/operator/aggregation/match#mongodb-pipeline-pipe.-match) stage to show an active operation building a descending index on the `name` field:

```javascript
db.getSiblingDB("admin").aggregate( [
   { $currentOp : { idleConnections: true } },
   { $match : {"command.createIndexes": { $exists: true } } }
] )
```

**Output:**

```javascript
[
   {
      type: 'op',
      host: 'mongodb.example.net:27017',
      desc: 'conn584',
      connectionId: 584,
      client: '104.30.134.189:12077',
      appName: 'mongosh 2.3.4',
      clientMetadata: {
         ...
      },
      active: true,
      currentOpTime: '2024-12-05T16:13:35.571+00:00',
      effectiveUsers: [ { user: jane-doe, db: 'admin' } ],
      isFromUserConnection: true,
      threaded: true,
      opid: ...,
      lsid: {
         ...
      },
      secs_running: Long('3'),
      microsecs_running: Long('3920881'),
      op: 'command',
      ns: 'example_db.collection',
      redacted: false,
      command: {
         createIndexes: 'collection',
         indexes: [ { name: 'name_-1', key: { name: -1 } } ],
         apiVersion: '1',
         lsid: { id: UUID('570931be-c692-4963-b9e2-1e279efd9702') },
         '$clusterTime': {
         clusterTime: Timestamp({ t: 1733415063, i: 32 }),
         signature: {
            hash: Binary.createFromBase64('z0zaUHJ5SfhNQyvQLhocsKRFNbo=', 0),
            keyId: Long('7444956895695077380')
         }
         },
         '$db': 'example_db'
      },
      numYields: 0,
      queues: {
         ...
      },
      currentQueue: null,
      locks: {},
      waitingForLock: false,
      lockStats: { ... },
      waitingForFlowControl: false,
      flowControlStats: { acquireCount: Long('3') }
   }, ...
]
```

MongoDB marks index builds in various stages, including waiting on commit quorum, as an idle connection by setting the `active` field to `false`. The `idleConnections: true` setting includes these idle connections in the `$currentOp` output.

To view information on existing indexes using a driver, refer to your [driver's documentation.](https://www.mongodb.com/docs/drivers/)

## Learn More

- To learn how to create indexes in MongoDB Compass, see [Manage Indexes](https://www.mongodb.com/docs/compass/current/indexes/#std-label-compass-indexes) in the Compass documentation.

- To see how often your indexes are used, see [Measure Index Use.](/docs/manual/tutorial/measure-index-use#std-label-index-measure-index-use)

- To learn how to specify the name of your index, see [Specify an Index Name.](/docs/manual/core/indexes/create-index/specify-index-name#std-label-specify-index-name)

- To learn how MongoDB builds indexes, see [Index Build Process.](/docs/manual/core/index-creation#std-label-index-build-process)
