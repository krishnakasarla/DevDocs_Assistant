> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Shard a Time Series Collection

Use this tutorial to shard a new or existing time series collection.

**Important:**

Before completing this tutorial, review the [sharding limitations](/docs/manual/core/timeseries/timeseries-limitations#std-label-time-series-limitations-sharding) for time series collections.

## Prerequisites

To shard a time series collection, you must [deploy a sharded cluster](/docs/manual/tutorial/deploy-shard-cluster#std-label-sharding-procedure-setup) to host the database that contains your time series collection.

**Note:**

Starting in MongoDB 8.0.10, you can reshard a time series collection. All shards in the time series collection must run version 8.0.10 or later to reshard.

## Procedures

### Create a Sharded Time Series Collection

1. Connect to your sharded cluster.

   Connect [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) to the [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) for your sharded cluster. Specify the `host` and `port` on which the `mongos` is running:

   ```javascript
   mongosh --host <hostname> --port <port>
   ```

2. Confirm that sharding is enabled on your database.

   Run [`sh.status()`](/docs/manual/reference/method/sh.status#mongodb-method-sh.status) to confirm that sharding is enabled on your database:

   ```javascript
   sh.status()
   ```

   The command returns the sharding information:

   ```javascript
   --- Sharding Status ---
      sharding version: {
         "_id" : 1,
         "minCompatibleVersion" : 5,
         "currentVersion" : 6,
   ...
   ```

3. Create the collection.

   Use the [`shardCollection()`](/docs/manual/reference/method/sh.shardCollection#mongodb-method-sh.shardCollection) method with the [timeseries](/docs/manual/reference/method/sh.shardCollection#std-label-method-sharded-time-series-collection-options) option.

   For example:

   ```javascript
   sh.shardCollection(
      "test.weather",
      { "metadata.sensorId": 1 },
      {
         timeseries: {
            timeField: "timestamp",
            metaField: "metadata",
            granularity: "hours"
         }
      }
   )
   ```

   In this example, [`sh.shardCollection()`:](/docs/manual/reference/method/sh.shardCollection#mongodb-method-sh.shardCollection)

   - Shards a new time series collection named `weather` on the `test` database.

   - Specifies the `metadata.sensorId` field as the [shard key.](/docs/manual/core/sharding-shard-key#std-label-shard-key)

   - Specifies a `granularity` of hours.

   The following document contains the appropriate metadata for the collection:

   ```javascript
   db.weather.insertOne( {
      "metadata": { "sensorId": 5578, "type": "temperature" },
      "timestamp": ISODate("2021-05-18T00:00:00.000Z"),
      "temp": 12
   } )
   ```

1) Connect to your sharded cluster.

   Connect [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) to the [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) for your sharded cluster. Specify the `host` and `port` on which the `mongos` is running:

   ```javascript
   mongosh --host <hostname> --port <port>
   ```

2) Confirm that sharding is enabled on your database.

   Run [`sh.status()`](/docs/manual/reference/method/sh.status#mongodb-method-sh.status) to confirm that sharding is enabled on your database:

   ```javascript
   sh.status()
   ```

   The command returns the sharding information:

   ```javascript
   --- Sharding Status ---
      sharding version: {
         "_id" : 1,
         "minCompatibleVersion" : 5,
         "currentVersion" : 6,
   ...
   ```

3) Create the collection.

   Use the [`shardCollection()`](/docs/manual/reference/method/sh.shardCollection#mongodb-method-sh.shardCollection) method with the [timeseries](/docs/manual/reference/method/sh.shardCollection#std-label-method-sharded-time-series-collection-options) option.

   For example:

   ```javascript
   sh.shardCollection(
      "test.weather",
      { "metadata.sensorId": 1 },
      {
         timeseries: {
            timeField: "timestamp",
            metaField: "metadata",
            granularity: "hours"
         }
      }
   )
   ```

   In this example, [`sh.shardCollection()`:](/docs/manual/reference/method/sh.shardCollection#mongodb-method-sh.shardCollection)

   - Shards a new time series collection named `weather` on the `test` database.

   - Specifies the `metadata.sensorId` field as the [shard key.](/docs/manual/core/sharding-shard-key#std-label-shard-key)

   - Specifies a `granularity` of hours.

   The following document contains the appropriate metadata for the collection:

   ```javascript
   db.weather.insertOne( {
      "metadata": { "sensorId": 5578, "type": "temperature" },
      "timestamp": ISODate("2021-05-18T00:00:00.000Z"),
      "temp": 12
   } )
   ```

### Shard an Existing Time Series Collection

1. Connect to your sharded cluster.

   Connect [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) to the [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) for your sharded cluster. Specify the `host` and `port` on which the `mongos` is running:

   ```javascript
   mongosh --host <hostname> --port <port>
   ```

2. Confirm that sharding is enabled on your database.

   Run [`sh.status()`](/docs/manual/reference/method/sh.status#mongodb-method-sh.status) to confirm that sharding is enabled on your database:

   ```javascript
   sh.status()
   ```

   The command returns the sharding information:

   ```javascript
   --- Sharding Status ---
      sharding version: {
         "_id" : 1,
         "minCompatibleVersion" : 5,
         "currentVersion" : 6,
   ...
   ```

3. Create a hashed index on your collection.

   Enable sharding on your collection by creating an index that supports the [shard key.](/docs/manual/core/sharding-shard-key#std-label-shard-key)

   Consider a time series collection with the following properties:

   ```javascript
   db.createCollection(
      "deliverySensor",
      {
         timeseries: {
            timeField: "timestamp",
            metaField: "metadata",
            granularity: "minutes"
         }
      }
   )
   ```

   A sample document from the collection resembles:

   ```javascript
   db.deliverySensor.insertOne( {
      "metadata": { "location": "USA", "vehicle": "truck" },
      "timestamp": ISODate("2021-08-21T00:00:10.000Z"),
      "speed": 50
   } )
   ```

   Run the following command to create a hashed index on the `metadata.location` field:

   ```javascript
   db.deliverySensor.createIndex( { "metadata.location" : "hashed" } )
   ```

4. Shard your collection.

   Use the [`shardCollection()`](/docs/manual/reference/method/sh.shardCollection#mongodb-method-sh.shardCollection) method to shard the collection.

   To shard the `deliverySensor` collection described in the preceding step, run the following command:

   ```javascript
   sh.shardCollection( "test.deliverySensor", { "metadata.location": "hashed" } )
   ```

   In this example, [`sh.shardCollection()`:](/docs/manual/reference/method/sh.shardCollection#mongodb-method-sh.shardCollection)

   - Shards an existing time series collection named `deliverySensor` on the `test` database.

   - Specifies the `metadata.location` field as the [shard key](/docs/manual/core/sharding-shard-key#std-label-shard-key). `location` is a sub-field of the collection's `metaField`.

   When the collection you specify to [`sh.shardCollection()`](/docs/manual/reference/method/sh.shardCollection#mongodb-method-sh.shardCollection) is a time series collection, you do not need to specify the [timeseries](/docs/manual/reference/method/sh.shardCollection#std-label-method-sharded-time-series-collection-options) option.

## Additional Information

- [Time Series Collections](/docs/manual/core/timeseries-collections#std-label-manual-timeseries-collection)

- [`sh.shardCollection()`](/docs/manual/reference/method/sh.shardCollection#mongodb-method-sh.shardCollection)

- [`shardCollection`](/docs/manual/reference/command/shardCollection#mongodb-dbcommand-dbcmd.shardCollection)
