> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Migrate Data into a Time Series Collection with Database Tools

Use the following steps to migrate data from an existing collection to a time series collection with [`mongodump`](https://www.mongodb.com/docs/database-tools/mongodump/#mongodb-binary-bin.mongodump) and [`mongorestore`.](https://www.mongodb.com/docs/database-tools/mongorestore/#mongodb-binary-bin.mongorestore)

## Steps

1. Create a new time series collection.

   To create a new [time series collection](/docs/manual/core/timeseries-collections#std-label-manual-timeseries-collection), issue the following command in the [`mongosh`:](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh)

   ```javascript
   db.createCollection(
      "weathernew", {
         timeseries: {
            timeField: "ts",
            metaField: "metaData",
            granularity: "hours"
         }
      }
   )
   ```

   This example uses sample data for the `timeField`, `metaField`, and `granularity`. For more information on the preceeding command, see [Create a Time Series Collection.](/docs/manual/core/timeseries/timeseries-procedures#std-label-manual-timeseries-collection-create)

2. (Optional) Transform your data.

   Time series collections support [secondary indexes](/docs/manual/core/timeseries/timeseries-secondary-index#std-label-timeseries-add-secondary-index) on the field specified as the `metaField`. If the data model of your time series data does not have a designated field for your metadata, you can transform your data to create one. To transform the data in your existing collection, use [`$out`](/docs/manual/reference/operator/aggregation/out#mongodb-pipeline-pipe.-out) to create a temporary collection with your time series data.

   Consider a collection with weather data of the following format:

   ```javascript
   db.weatherdata.insertOne(
      {
         _id: ObjectId("5553a998e4b02cf7151190b8"),
         st: "x+47600-047900",
         ts: ISODate("1984-03-05T13:00:00Z"),
         position: {
            type: "Point",
            coordinates: [ -47.9, 47.6 ]
         },
         elevation: 9999,
         callLetters: "VCSZ",
         qualityControlProcess: "V020",
         dataSource: "4",
         type: "FM-13",
         airTemperature: { value: -3.1, quality: "1" },
         dewPoint: { value: 999.9, quality : "9" },
         pressure: { value: 1015.3, quality: "1" },
         wind: {
            direction: { angle: 999, quality: "9" },
            type: "9",
            speed: { rate: 999.9, quality: "9" }
         },
         visibility: {
            distance: { value: 999999, quality : "9" },
            variability: { value: "N", quality: "9" }
         },
         skyCondition: {
            ceilingHeight: { value: 99999, quality: "9", determination: "9" },
            cavok: "N"
         },
         sections: [ "AG1" ],
         precipitationEstimatedObservation: {
            discrepancy: "2",
            estimatedWaterDepth: 999
         }
      }
   )
   ```

   **Note:**

   Choosing the right field as your time series `metaField` and `grandularity` optimizes both storage and query performance. For more information on field selection and best practices, see [metaField and Granularity Best Practices.](/docs/manual/core/timeseries/timeseries-best-practices#std-label-tsc-best-practice-optimize-query-performance)

   The pipline below performs the following operations:

   - Uses [`$addFields`](/docs/manual/reference/operator/aggregation/addFields#mongodb-pipeline-pipe.-addFields) to add a `metaData` field to the `weather_data` collection.

   - Uses [`$project`](/docs/manual/reference/operator/aggregation/project#mongodb-pipeline-pipe.-project) to include or exclude the remaining fields in the document.

   - Uses [`$out`](/docs/manual/reference/operator/aggregation/out#mongodb-pipeline-pipe.-out) to create a temporary collection called `temporarytimeseries`.

   ```javascript
   db.weather_data.aggregate([
   {
      $addFields: {
         metaData: {
            "st": "$st",
            "position": "$position",
            "elevation": "$elevation",
            "callLetters": "$callLetters",
            "qualityControlProcess": "$qualityControlProcess",
            "type": "$type"
         }
      },
   }, {
      $project: {
         _id: 1,
         ts: 1,
         metaData: 1,
         dataSource: 1,
         airTemperature: 1,
         dewPoint: 1,
         pressure: 1,
         wind: 1,
         visibility: 1,
         skyCondition: 1,
         sections: 1,
         precipitationEstimatedObservation: 1
      }
   }, {
      $out: "temporarytimeseries"
   }
   ])
   ```

   After you run this command, you have an intermediary `temporarytimeseries` collection:

   ```javascript
   db.temporarytimeseries.findOne()
   {
      "_id" : ObjectId("5553a998e4b02cf7151190b8"),
      "ts" : ISODate("1984-03-05T13:00:00Z"),
      "dataSource" : "4",
      "airTemperature" : { "value" : -3.1, "quality" : "1" },
      "dewPoint" : { "value" : 999.9, "quality" : "9" },
      "pressure" : { "value" : 1015.3, "quality" : "1" },
      "wind" : {
      "direction" : { "angle" : 999, "quality" : "9" },
      "type" : "9",
      "speed" : { "rate" : 999.9, "quality" : "9" }
      },
      "visibility" : {
      "distance" : { "value" : 999999, "quality" : "9" },
      "variability" : { "value" : "N", "quality" : "9" }
      },
      "skyCondition" : {
      "ceilingHeight" : { "value" : 99999, "quality" : "9", "determination" : "9" },
      "cavok" : "N"
      },
      "sections" : [ "AG1" ],
      "precipitationEstimatedObservation" : { "discrepancy" : "2", "estimatedWaterDepth" : 999 },
      "metaData" : {
      "st" : "x+47600-047900",
      "position" : {
         "type" : "Point",
         "coordinates" : [ -47.9, 47.6 ]
      },
      "elevation" : 9999,
      "callLetters" : "VCSZ",
      "qualityControlProcess" : "V020",
      "type" : "FM-13"
      }
   }
   ```

3. Export your original collection.

   To export your data from an existing collection that is not of type `timeseries` use [`mongodump`.](https://www.mongodb.com/docs/database-tools/mongodump/#mongodb-binary-bin.mongodump)

   **Warning:**

   When migrating or backfilling into a time series collection, always insert the documents in order, from oldest to newest. In this case, [`mongodump`](https://www.mongodb.com/docs/database-tools/mongodump/#mongodb-binary-bin.mongodump) exports documents in natural order and the `--maintainInsertionOrder` option for [`mongorestore`](https://www.mongodb.com/docs/database-tools/mongorestore/#mongodb-binary-bin.mongorestore) guarantees the same insertion order for documents.

   For example, to export the `temporarytimeseries` collection, issue the following command:

   ```javascript
   mongodump
      --uri="mongodb://mongodb0.example.com:27017,mongodb1.example.com:27017,mongodb2.example.com:27017/weather" \
      --collection=temporarytimeseries --out=timeseries
   ```

   The command returns the following output:

   ```javascript
   2021-06-01T16:48:39.980+0200  writing weather.temporarytimeseries to timeseries/weather/temporarytimeseries.bson
   2021-06-01T16:48:40.056+0200  done dumping weather.temporarytimeseries
   (10000 documents)
   ```

4. Import your collection.

   To import your data into a timeseries collection, use [`mongorestore`.](https://www.mongodb.com/docs/database-tools/mongorestore/#mongodb-binary-bin.mongorestore)

   **Important:**

   Ensure that you run the `mongorestore` command with the [`--noIndexRestore`](https://www.mongodb.com/docs/database-tools/mongorestore/#std-option-mongorestore.--noIndexRestore) option. `mongorestore` cannot create indexes on time series collections.

   The following operation imports `timeseries/weather/temporarytimeseries.bson` into the new collection `weathernew`:

   ```javascript
   mongorestore
      --uri="mongodb://mongodb0.example.com:27017,mongodb1.example.com:27017,mongodb2.example.com:27017/weather" \
      --collection=weathernew --noIndexRestore \
      --maintainInsertionOrder \
      timeseries/weather/temporarytimeseries.bson
   ```

   The command returns the following output:

   ```javascript
   2021-06-01T16:50:56.639+0200  checking for collection data in timeseries/weather/temporarytimeseries.bson
   2021-06-01T16:50:56.640+0200  restoring to existing collection weather.weathernew without dropping
   2021-06-01T16:50:56.640+0200  reading metadata for weather.weathernew from timeseries/weather/temporarytimeseries.metadata.json
   2021-06-01T16:50:56.640+0200  restoring weather.weathernew from timeseries/weather/temporarytimeseries.bson
   2021-06-01T16:51:01.229+0200  no indexes to restore
   2021-06-01T16:51:01.229+0200  finished restoring weather.weathernew (10000 documents, 0 failures)
   2021-06-01T16:51:01.229+0200  10000 document(s) restored successfully. 0 document(s) failed to restore.
   ```

   If your original collection had secondary indexes, manually recreate them now. If your collection includes `timeField` values before `1970-01-01T00:00:00.000Z` or after `2038-01-19T03:14:07.000Z`, MongoDB logs a warning and disables some query optimizations that make use of the [internal clustered index](/docs/manual/core/timeseries-collections#std-label-manual-timeseries-internal-index). [Create a secondary index](/docs/manual/core/timeseries/timeseries-secondary-index#std-label-timeseries-add-secondary-index) on the `timeField` to regain query performance and resolve the log warning.

**See also:**

[Add Secondary Indexes to Time Series Collections](/docs/manual/core/timeseries/timeseries-secondary-index#std-label-timeseries-add-secondary-index)

If you insert a document into a collection with a `timeField` value before `1970-01-01T00:00:00.000Z` or after `2038-01-19T03:14:07.000Z`, MongoDB logs a warning and prevents some query optimizations from using the internal index. [Create a secondary index](/docs/manual/core/timeseries/timeseries-secondary-index#std-label-timeseries-add-secondary-index) on the `timeField` to regain query performance and resolve the log warning.
