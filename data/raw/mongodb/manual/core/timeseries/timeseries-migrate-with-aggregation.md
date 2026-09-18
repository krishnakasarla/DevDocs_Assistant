> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Migrate Data into a Time Series Collection with Aggregation

Starting in MongoDB version 7.0, you can use the [`$out`](/docs/manual/reference/operator/aggregation/out#mongodb-pipeline-pipe.-out) aggregation stage to migrate data from an existing collection into a [time series collection.](/docs/manual/core/timeseries-collections#std-label-manual-timeseries-collection)

**Note:**

MongoDB does not guarantee output order when you use [`$out`](/docs/manual/reference/operator/aggregation/out#mongodb-pipeline-pipe.-out) to migrate data into a times series collection. To maintain order, sort your data before you migrate with an aggregation pipeline.

## Before you Begin

Consider a `weather_data` collection that contains time and metadata information:

```csharp
var sampleDocument = new BsonDocument("_id", new ObjectId("5553a998e4b02cf7151190b8"))
    .Add("st", "x+47600-047900")
    .Add("ts", new BsonDateTime(new DateTime(1984, 3, 5, 13, 0, 0, DateTimeKind.Utc)))
    .Add("position", new BsonDocument("type", "Point")
        .Add("coordinates", new BsonArray { -47.9, 47.6 }))
    .Add("elevation", 9999)
    .Add("callLetters", "VCSZ")
    .Add("qualityControlProcess", "V020")
    .Add("dataSource", "4")
    .Add("type", "FM-13")
    .Add("airTemperature", new BsonDocument("value", -3.1).Add("quality", "1"))
    .Add("dewPoint", new BsonDocument("value", 999.9).Add("quality", "9"))
    .Add("pressure", new BsonDocument("value", 1015.3).Add("quality", "1"))
    .Add("wind", new BsonDocument("direction",
            new BsonDocument("angle", 999)
                .Add("quality", "9"))
        .Add("type", "9")
        .Add("speed", new BsonDocument("rate", 999.9).Add("quality", "9")))
    .Add("visibility", new BsonDocument("distance", new BsonDocument("value", 999999).Add("quality", "9"))
        .Add("variability", new BsonDocument("value", "N").Add("quality", "9")))
    .Add("skyCondition", new BsonDocument("ceilingHeight", new BsonDocument("value", 99999)
            .Add("quality", "9").Add("determination", "9"))
        .Add("cavok", "N"))
    .Add("sections", new BsonArray { "AG1" })
    .Add("precipitationEstimatedObservation", new BsonDocument("discrepancy", "2")
        .Add("estimatedWaterDepth", 999));

await collection.InsertOneAsync(sampleDocument);

```

```java
timeseriesDb = mongoClient.getDatabase("mydatabase");

weatherDataColl = timeseriesDb.getCollection("weather_data");

Document sampleDocument = new Document("_id", new ObjectId("5553a998e4b02cf7151190b8"))
        .append("st", "x+47600-047900")
        .append("ts", new Date(447339600000L)) // 1984-03-05T13:00:00.000Z
        .append("position", new Document("type", "Point")
                .append("coordinates", Arrays.asList(-47.9, 47.6)))
        .append("elevation", 9999)
        .append("callLetters", "VCSZ")
        .append("qualityControlProcess", "V020")
        .append("dataSource", "4")
        .append("type", "FM-13")
        .append("airTemperature", new Document("value", -3.1).append("quality", "1"))
        .append("dewPoint", new Document("value", 999.9).append("quality", "9"))
        .append("pressure", new Document("value", 1015.3).append("quality", "1"))
        .append("wind", new Document("direction", new Document("angle", 999).append("quality", "9"))
                .append("type", "9")
                .append("speed", new Document("rate", 999.9).append("quality", "9")))
        .append("visibility", new Document("distance", new Document("value", 999999).append("quality", "9"))
                .append("variability", new Document("value", "N").append("quality", "9")))
        .append("skyCondition", new Document("ceilingHeight", new Document("value", 99999)
                .append("quality", "9").append("determination", "9"))
                .append("cavok", "N"))
        .append("sections", Arrays.asList("AG1"))
        .append("precipitationEstimatedObservation", new Document("discrepancy", "2")
                .append("estimatedWaterDepth", 999));

weatherDataColl.insertOne(sampleDocument);

```

```javascript
db.weather_data.insertOne(
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

```javascript
const timeseriesDb = client.db('mydatabase');
const weatherDataColl = timeseriesDb.collection('weather_data');

const sampleDocument = {
  _id: new ObjectId('5553a998e4b02cf7151190b8'),
  st: 'x+47600-047900',
  ts: new Date('1984-03-05T13:00:00.000Z'),
  position: {
    type: 'Point',
    coordinates: [-47.9, 47.6],
  },
  elevation: 9999,
  callLetters: 'VCSZ',
  qualityControlProcess: 'V020',
  dataSource: '4',
  type: 'FM-13',
  airTemperature: { value: -3.1, quality: '1' },
  dewPoint: { value: 999.9, quality: '9' },
  pressure: { value: 1015.3, quality: '1' },
  wind: {
    direction: { angle: 999, quality: '9' },
    type: '9',
    speed: { rate: 999.9, quality: '9' },
  },
  visibility: {
    distance: { value: 999999, quality: '9' },
    variability: { value: 'N', quality: '9' },
  },
  skyCondition: {
    ceilingHeight: { value: 99999, quality: '9', determination: '9' },
    cavok: 'N',
  },
  sections: ['AG1'],
  precipitationEstimatedObservation: {
    discrepancy: '2',
    estimatedWaterDepth: 999,
  },
};

await weatherDataColl.insertOne(sampleDocument);

```

```python
client = MongoClient(CONNECTION_STRING)

timeseries_db = client["mydatabase"]

weather_data_coll = timeseries_db["weather_data"]

sample_document = {
    "_id": ObjectId("5553a998e4b02cf7151190b8"),
    "st": "x+47600-047900",
    "ts": datetime(1984, 3, 5, 13, 0, 0),
    "position": {
        "type": "Point",
        "coordinates": [-47.9, 47.6]
    },
    "elevation": 9999,
    "callLetters": "VCSZ",
    "qualityControlProcess": "V020",
    "dataSource": "4",
    "type": "FM-13",
    "airTemperature": {"value": -3.1, "quality": "1"},
    "dewPoint": {"value": 999.9, "quality": "9"},
    "pressure": {"value": 1015.3, "quality": "1"},
    "wind": {
        "direction": {"angle": 999, "quality": "9"},
        "type": "9",
        "speed": {"rate": 999.9, "quality": "9"}
    },
    "visibility": {
        "distance": {"value": 999999, "quality": "9"},
        "variability": {"value": "N", "quality": "9"}
    },
    "skyCondition": {
        "ceilingHeight": {"value": 99999, "quality": "9", "determination": "9"},
        "cavok": "N"
    },
    "sections": ["AG1"],
    "precipitationEstimatedObservation": {
        "discrepancy": "2",
        "estimatedWaterDepth": 999
    }
}

weather_data_coll.insert_one(sample_document)

```

## Steps

1. Create a metadata field.

   If your collection doesn't include a field you can use to identify each series, transform your data to define one. In this example, we create a `metaData` field that will be used for the `metaField` property of the time series collection we will later create.

   **Note:**

   Choosing the right field as your time series `metaField` and `grandularity` optimizes both storage and query performance. For more information on field selection and best practices, see [metaField and Granularity Best Practices.](/docs/manual/core/timeseries/timeseries-best-practices#std-label-tsc-best-practice-optimize-query-performance)

   These aggregation stages perform the following operations:

   - Uses [`$set`](/docs/manual/reference/operator/aggregation/set#mongodb-pipeline-pipe.-set) to add a `metaData` field.

   - Uses [`$project`](/docs/manual/reference/operator/aggregation/project#mongodb-pipeline-pipe.-project) to include the remaining fields in the document.

   ```csharp
   var pipeline = new BsonDocument[]
   {
       new BsonDocument("$set", new BsonDocument("metaData", new BsonDocument
       {
           { "st", "$st" },
           { "position", "$position" },
           { "elevation", "$elevation" },
           { "callLetters", "$callLetters" },
           { "qualityControlProcess", "$qualityControlProcess" },
           { "type", "$type" }
       })),
       new BsonDocument("$project", new BsonDocument
       {
           { "_id", 0 },
           { "ts", 1 },
           { "metaData", 1 },
           { "dataSource", 1 },
           { "airTemperature", 1 },
           { "dewPoint", 1 },
           { "pressure", 1 },
           { "wind", 1 },
           { "visibility", 1 },
           { "skyCondition", 1 },
           { "sections", 1 },
           { "precipitationEstimatedObservation", 1 }
       })
   };

   ```

   **Note:**

   The `timeField` of a time series collection must be a [date](/docs/manual/reference/bson-types#std-label-document-bson-type-date) type.

2. Create your time series collection.

   Before you can output data to a time series collection, you must create the collection with the appropriate options. In this example, we create a `TimeSeriesOptions` object to define the time series options for the new collection, and then create the collection using those options:

   ```csharp
   var timeSeriesOptions = new TimeSeriesOptions(
       timeField: "ts",
       metaField: "metaData",
       granularity: TimeSeriesGranularity.Seconds
   );

   database.CreateCollection(weather_new,
       new CreateCollectionOptions { TimeSeriesOptions = timeSeriesOptions });

   ```

   Then, add an [`$out`](/docs/manual/reference/operator/aggregation/out#mongodb-pipeline-pipe.-out) aggregation stage to your pipeline that outputs to the new time series collection. Create the output, and then concatenate it to your existing aggregation pipeline:

   ```csharp
   var outPipeline = new BsonDocument("$out", new BsonDocument
   {
       { "db", "mydatabase" },
       { "coll", weather_new },
       {
           "timeseries", new BsonDocument
           {
               { "timeField", "ts" }, // Field representing the time data  
               { "metaField", "metaData" }, // Field containing meta information  
               { "granularity", "seconds" } // Granularity (or "seconds", "minutes", etc.)  
           }
       }
   });
   collection.Aggregate<BsonDocument>(pipeline.Concat(new[] { outPipeline }).ToArray());

   ```

   For a full explanation of the time series options, see the [Time Series Field Reference.](/docs/manual/core/timeseries/timeseries-procedures#std-label-time-series-fields)

3. Run your aggregation pipeline.

   To run the complete aggregation pipeline to migrate the data into the new time series collection, call one of the methods that implements `IEnumerable`, such as `ToList`, `ToArray`, or `ToEnumerable` on the pipeline object. The following example shows the complete aggregation pipeline, including this final step:

   ```csharp
   var pipeline = new BsonDocument[]
   {
       new BsonDocument("$set", new BsonDocument("metaData", new BsonDocument
       {
           { "st", "$st" },
           { "position", "$position" },
           { "elevation", "$elevation" },
           { "callLetters", "$callLetters" },
           { "qualityControlProcess", "$qualityControlProcess" },
           { "type", "$type" }
       })),
       new BsonDocument("$project", new BsonDocument
       {
           { "_id", 0 },
           { "ts", 1 },
           { "metaData", 1 },
           { "dataSource", 1 },
           { "airTemperature", 1 },
           { "dewPoint", 1 },
           { "pressure", 1 },
           { "wind", 1 },
           { "visibility", 1 },
           { "skyCondition", 1 },
           { "sections", 1 },
           { "precipitationEstimatedObservation", 1 }
       })
   };
   var outPipeline = new BsonDocument("$out", new BsonDocument
   {
       { "db", "mydatabase" },
       { "coll", weather_new },
       {
           "timeseries", new BsonDocument
           {
               { "timeField", "ts" }, // Field representing the time data  
               { "metaField", "metaData" }, // Field containing meta information  
               { "granularity", "seconds" } // Granularity (or "seconds", "minutes", etc.)  
           }
       }
   });
   collection.Aggregate<BsonDocument>(pipeline.Concat(new[] { outPipeline }).ToArray());

   ```

4. Review your data.

   After you run this aggregation pipeline, you can use the standard MongoDB query methods to review the data in your new time series collection. The following example shows how to use the `Find` and `ToList` methods to view a document in your `weather_new` time series collection:

   ```csharp
   var newCollection = database.GetCollection<BsonDocument>(weather_new);
   var result = newCollection.Find(_ => true).ToList();
   return result;

   ```

   **Output:**

   ```json
   {
     "ts" : {
       "$date" : "1984-03-05T13:00:00Z"
     },
     "metaData" : {
       "callLetters" : "VCSZ",
       "elevation" : 9999,
       "position" : {
         "coordinates" : [ -47.9, 47.6 ],
         "type" : "Point"
       },
       "qualityControlProcess" : "V020",
       "st" : "x+47600-047900",
       "type" : "FM-13"
     },
     "dewPoint" : {
       "value" : 999.9,
       "quality" : "9"
     },
     "wind" : {
       "direction" : {
         "angle" : 999,
         "quality" : "9"
       },
       "type" : "9",
       "speed" : {
         "rate" : 999.9,
         "quality" : "9"
       }
     },
     "skyCondition" : {
       "ceilingHeight" : {
         "value" : 99999,
         "quality" : "9",
         "determination" : "9"
       },
       "cavok" : "N"
     },
     "dataSource" : "4",
     "pressure" : {
       "value" : 1015.3,
       "quality" : "1"
     },
     "visibility" : {
       "distance" : {
         "value" : 999999,
         "quality" : "9"
       },
       "variability" : {
         "value" : "N",
         "quality" : "9"
       }
     },
     "airTemperature" : {
       "value" : -3.1,
       "quality" : "1"
     },
     "sections" : [ "AG1" ],
     "precipitationEstimatedObservation" : {
       "discrepancy" : "2",
       "estimatedWaterDepth" : 999
     }
   }
   ```

1) Create a metadata field.

   If your collection doesn't include a field you can use to identify each series, transform your data to define one. In this example, the `metaData` field becomes the `metaField` of the time series collection that you create.

   **Note:**

   Choosing the right field as your time series `metaField` and `grandularity` optimizes both storage and query performance. For more information on field selection and best practices, see [metaField and Granularity Best Practices.](/docs/manual/core/timeseries/timeseries-best-practices#std-label-tsc-best-practice-optimize-query-performance)

   These aggregation stages perform the following operations:

   - Uses [`$addFields`](/docs/manual/reference/operator/aggregation/addFields#mongodb-pipeline-pipe.-addFields) to add a `metaData` field to the `weather_data` collection.

   - Uses [`$project`](/docs/manual/reference/operator/aggregation/project#mongodb-pipeline-pipe.-project) to include or exclude the remaining fields in the document.

   ```java
   addFields(
           new Field<>("metaData", new Document("st", "$st")
                   .append("position", "$position")
                   .append("elevation", "$elevation")
                   .append("callLetters", "$callLetters")
                   .append("qualityControlProcess", "$qualityControlProcess")
                   .append("type", "$type"))),
   project(fields(
           include("_id", "ts", "metaData", "dataSource", "airTemperature",
                   "dewPoint", "pressure", "wind", "visibility",
                   "skyCondition", "sections", "precipitationEstimatedObservation"))),

   ```

2) Create your time series collection.

   Add an [`$out`](/docs/manual/reference/operator/aggregation/out#mongodb-pipeline-pipe.-out) aggregation stage to your pipeline to create a time series collection and insert your data into it. The pipeline below performs the following operations:

   - Uses [`$out`](/docs/manual/reference/operator/aggregation/out#mongodb-pipeline-pipe.-out) with the `timeseries` option to create a `weather_new` time series collection in the `mydatabase` database.

   - Defines the `metaData` field as the `metaField` of the `weather_new` collection.

   - Defines the `ts` field as the `timeField` of the `weather_new` collection.

     **Note:**

     The `timeField` of a time series collection must be a [date](/docs/manual/reference/bson-types#std-label-document-bson-type-date) type.

   ```java
   out(new Document("db", "mydatabase")
           .append("coll", "weather_new")
           .append("timeseries", new Document("timeField", "ts")
                   .append("metaField", "metaData")
                   .append("granularity", "seconds")))

   ```

   For the aggregation stage syntax, see [`$out`](/docs/manual/reference/operator/aggregation/out#mongodb-pipeline-pipe.-out). For a full explanation of the time series options, see the [Time Series Field Reference.](/docs/manual/core/timeseries/timeseries-procedures#std-label-time-series-fields)

3) Run your aggregation pipeline.

   Run the complete aggregation pipeline to migrate the data into the new time series collection.

   ```java
   List<Bson> pipeline = Arrays.asList(
           addFields(
                   new Field<>("metaData", new Document("st", "$st")
                           .append("position", "$position")
                           .append("elevation", "$elevation")
                           .append("callLetters", "$callLetters")
                           .append("qualityControlProcess", "$qualityControlProcess")
                           .append("type", "$type"))),
           project(fields(
                   include("_id", "ts", "metaData", "dataSource", "airTemperature",
                           "dewPoint", "pressure", "wind", "visibility",
                           "skyCondition", "sections", "precipitationEstimatedObservation"))),
           out(new Document("db", "mydatabase")
                   .append("coll", "weather_new")
                   .append("timeseries", new Document("timeField", "ts")
                           .append("metaField", "metaData")
                           .append("granularity", "seconds")))
   );

   weatherDataColl.aggregate(pipeline).toCollection();

   ```

4) Review your data.

   After you run this aggregation pipeline, you can use `find().first()` method to view a document in your `weather_new` time series collection:

   ```java
   MongoCollection<Document> weatherNewColl = timeseriesDb.getCollection("weather_new");
   Document result = weatherNewColl.find().first();

   ```

   **Output:**

   ```text
   {
       "_id": {"$oid": "5553a998e4b02cf7151190b8"},
       "ts": {"$date": "1984-03-05T13:00:00Z"},
       "metaData": {
           "st": "x+47600-047900",
           "position": {"type": "Point", "coordinates": [-47.9, 47.6]},
           "elevation": 9999,
           "callLetters": "VCSZ",
           "qualityControlProcess": "V020",
           "type": "FM-13"
       },
       "dataSource": "4",
       "airTemperature": {"value": -3.1, "quality": "1"},
       "dewPoint": {"value": 999.9, "quality": "9"},
       "pressure": {"value": 1015.3, "quality": "1"},
       "wind": {
           "direction": {"angle": 999, "quality": "9"},
           "type": "9",
           "speed": {"rate": 999.9, "quality": "9"}
       },
       "visibility": {
           "distance": {"value": 999999, "quality": "9"},
           "variability": {"value": "N", "quality": "9"}
       },
       "skyCondition": {
           "ceilingHeight": {"value": 99999, "quality": "9", "determination": "9"},
           "cavok": "N"
       },
       "sections": ["AG1"],
       "precipitationEstimatedObservation": {"discrepancy": "2", "estimatedWaterDepth": 999}
   }

   ```

1. Create a metadata field.

   If your collection doesn't include a field you can use to identify each series, transform your data to define one. In this example, the `metaData` field becomes the `metaField` of the time series collection that you create.

   **Note:**

   Choosing the right field as your time series `metaField` and `grandularity` optimizes both storage and query performance. For more information on field selection and best practices, see [metaField and Granularity Best Practices.](/docs/manual/core/timeseries/timeseries-best-practices#std-label-tsc-best-practice-optimize-query-performance)

   These aggregation stages perform the following operations:

   - Uses [`$addFields`](/docs/manual/reference/operator/aggregation/addFields#mongodb-pipeline-pipe.-addFields) to add a `metaData` field to the `weather_data` collection.

   - Uses [`$project`](/docs/manual/reference/operator/aggregation/project#mongodb-pipeline-pipe.-project) to include or exclude the remaining fields in the document.

   ```javascript
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
   },
   {
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
   },

   ```

2. Create your time series collection.

   Add an [`$out`](/docs/manual/reference/operator/aggregation/out#mongodb-pipeline-pipe.-out) aggregation stage to your pipeline to create a time series collection and insert your data into it. The pipeline below performs the following operations:

   - Uses [`$out`](/docs/manual/reference/operator/aggregation/out#mongodb-pipeline-pipe.-out) with the `timeseries` option to create a `weather_new` time series collection in the `mydatabase` database.

   - Defines the `metaData` field as the `metaField` of the `weather_new` collection.

   - Defines the `ts` field as the `timeField` of the `weather_new` collection.

     **Note:**

     The `timeField` of a time series collection must be a [date](/docs/manual/reference/bson-types#std-label-document-bson-type-date) type.

   ```javascript
   {
      $out: {
         db: "mydatabase",
         coll: "weather_new",
         timeseries: {
            timeField: "ts",
            metaField: "metaData",
            granularity: "seconds"
         }
      }
   }

   ```

   For the aggregation stage syntax, see [`$out`](/docs/manual/reference/operator/aggregation/out#mongodb-pipeline-pipe.-out). For a full explanation of the time series options, see the [Time Series Field Reference.](/docs/manual/core/timeseries/timeseries-procedures#std-label-time-series-fields)

3. Run your aggregation pipeline.

   Run the complete aggregation pipeline to migrate the data into the new time series collection.

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
   },
   {
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
   },
   {
      $out: {
         db: "mydatabase",
         coll: "weather_new",
         timeseries: {
            timeField: "ts",
            metaField: "metaData",
            granularity: "seconds"
         }
      }
   }
   ])

   ```

4. Review your data.

   After you run this aggregation pipeline, you can use [`findOne()`](/docs/manual/reference/method/db.collection.findOne#mongodb-method-db.collection.findOne) to view a document in your `weather_new` time series collection:

   ```javascript
   db.weather_new.findOne()

   ```

   **Output:**

   ```shell
   {
       _id: ObjectId("5553a998e4b02cf7151190b8"),
       ts: ISODate("1984-03-05T13:00:00Z"),
       metaData: {
           st: "x+47600-047900",
           position: {
           type: "Point",
           coordinates: [ -47.9, 47.6 ]
           },
           elevation: 9999,
           callLetters: "VCSZ",
           qualityControlProcess: "V020",
           type: "FM-13"
       },
       dataSource: "4",
       airTemperature: { value: -3.1, quality: "1" },
       dewPoint: { value: 999.9, quality: "9" },
       pressure: { value: 1015.3, quality: "1" },
       wind: {
           direction: { angle: 999, quality: "9" },
           type: "9",
           speed: { rate: 999.9, quality: "9" }
       },
       visibility: {
           distance: { value: 999999, quality: "9" },
           variability: { value: "N", quality: "9" }
       },
       skyCondition: {
           ceilingHeight: { value: 99999, quality: "9", determination: "9" },
           cavok: "N"
       },
       sections: [ "AG1" ],
       precipitationEstimatedObservation: { discrepancy: "2", estimatedWaterDepth: 999 }
   }

   ```

1) Create a metadata field.

   If your collection doesn't include a field you can use to identify each series, transform your data to define one. In this example, the `metaData` field becomes the `metaField` of the time series collection that you create.

   **Note:**

   Choosing the right field as your time series `metaField` and `grandularity` optimizes both storage and query performance. For more information on field selection and best practices, see [metaField and Granularity Best Practices.](/docs/manual/core/timeseries/timeseries-best-practices#std-label-tsc-best-practice-optimize-query-performance)

   These aggregation stages perform the following operations:

   - Uses [`$addFields`](/docs/manual/reference/operator/aggregation/addFields#mongodb-pipeline-pipe.-addFields) to add a `metaData` field to the `weather_data` collection.

   - Uses [`$project`](/docs/manual/reference/operator/aggregation/project#mongodb-pipeline-pipe.-project) to include or exclude the remaining fields in the document.

   ```javascript
   {
     $addFields: {
       metaData: {
         st: '$st',
         position: '$position',
         elevation: '$elevation',
         callLetters: '$callLetters',
         qualityControlProcess: '$qualityControlProcess',
         type: '$type',
       },
     },
   },
   {
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
       precipitationEstimatedObservation: 1,
     },
   },

   ```

2) Create your time series collection.

   Add an [`$out`](/docs/manual/reference/operator/aggregation/out#mongodb-pipeline-pipe.-out) aggregation stage to your pipeline to create a time series collection and insert your data into it. The pipeline below performs the following operations:

   - Uses [`$out`](/docs/manual/reference/operator/aggregation/out#mongodb-pipeline-pipe.-out) with the `timeseries` option to create a `weather_new` time series collection in the `mydatabase` database.

   - Defines the `metaData` field as the `metaField` of the `weather_new` collection.

   - Defines the `ts` field as the `timeField` of the `weather_new` collection.

     **Note:**

     The `timeField` of a time series collection must be a [date](/docs/manual/reference/bson-types#std-label-document-bson-type-date) type.

   ```javascript
   {
     $out: {
       db: 'mydatabase',
       coll: 'weather_new',
       timeseries: {
         timeField: 'ts',
         metaField: 'metaData',
         granularity: 'seconds',
       },
     },
   },

   ```

   For the aggregation stage syntax, see [`$out`](/docs/manual/reference/operator/aggregation/out#mongodb-pipeline-pipe.-out). For a full explanation of the time series options, see the [Time Series Field Reference.](/docs/manual/core/timeseries/timeseries-procedures#std-label-time-series-fields)

3) Run your aggregation pipeline.

   Run the complete aggregation pipeline to migrate the data into the new time series collection.

   ```javascript
   const timeseriesDb = client.db('mydatabase');
   const weatherDataColl = timeseriesDb.collection('weather_data');

   const pipeline = [
     {
       $addFields: {
         metaData: {
           st: '$st',
           position: '$position',
           elevation: '$elevation',
           callLetters: '$callLetters',
           qualityControlProcess: '$qualityControlProcess',
           type: '$type',
         },
       },
     },
     {
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
         precipitationEstimatedObservation: 1,
       },
     },
     {
       $out: {
         db: 'mydatabase',
         coll: 'weather_new',
         timeseries: {
           timeField: 'ts',
           metaField: 'metaData',
           granularity: 'seconds',
         },
       },
     },
   ];

   weatherDataColl.aggregate(pipeline);

   ```

4) Review your data.

   After you run this aggregation pipeline, you can use `findOne()` method to view a document in your `weather_new` time series collection:

   ```javascript
   const timeseriesDb = client.db('mydatabase');
   const weatherNewColl = timeseriesDb.collection('weather_new');

   const result = await weatherNewColl.findOne();

   ```

   **Output:**

   ```text
   {
       _id: new ObjectId('5553a998e4b02cf7151190b8'),
       ts: 1984-03-05T13:00:00.000Z,
       metaData: {
           st: 'x+47600-047900',
           position: { type: 'Point', coordinates: [ -47.9, 47.6 ] },
           elevation: 9999,
           callLetters: 'VCSZ',
           qualityControlProcess: 'V020',
           type: 'FM-13'
       },
       dataSource: '4',
       airTemperature: { value: -3.1, quality: '1' },
       dewPoint: { value: 999.9, quality: '9' },
       pressure: { value: 1015.3, quality: '1' },
       wind: {
           direction: { angle: 999, quality: '9' },
           type: '9',
           speed: { rate: 999.9, quality: '9' }
       },
       visibility: {
           distance: { value: 999999, quality: '9' },
           variability: { value: 'N', quality: '9' }
       },
       skyCondition: {
           ceilingHeight: { value: 99999, quality: '9', determination: '9' },
           cavok: 'N'
       },
       sections: [ 'AG1' ],
       precipitationEstimatedObservation: {
           discrepancy: '2',
           estimatedWaterDepth: 999
       }
   }
   ```

1. Create a metadata field.

   If your collection doesn't include a field you can use to identify each series, transform your data to define one. In this example, the `metaData` field becomes the `metaField` of the time series collection that you create.

   **Note:**

   Choosing the right field as your time series `metaField` and `grandularity` optimizes both storage and query performance. For more information on field selection and best practices, see [metaField and Granularity Best Practices.](/docs/manual/core/timeseries/timeseries-best-practices#std-label-tsc-best-practice-optimize-query-performance)

   These aggregation stages perform the following operations:

   - Uses [`$addFields`](/docs/manual/reference/operator/aggregation/addFields#mongodb-pipeline-pipe.-addFields) to add a `metaData` field to the `weather_data` collection.

   - Uses [`$project`](/docs/manual/reference/operator/aggregation/project#mongodb-pipeline-pipe.-project) to include or exclude the remaining fields in the document.

   ```python
   {
       "$addFields": {
           "metaData": {
               "st": "$st",
               "position": "$position",
               "elevation": "$elevation",
               "callLetters": "$callLetters",
               "qualityControlProcess": "$qualityControlProcess",
               "type": "$type"
           }
       }
   },
   {
       "$project": {
           "_id": 1,
           "ts": 1,
           "metaData": 1,
           "dataSource": 1,
           "airTemperature": 1,
           "dewPoint": 1,
           "pressure": 1,
           "wind": 1,
           "visibility": 1,
           "skyCondition": 1,
           "sections": 1,
           "precipitationEstimatedObservation": 1
       }
   },

   ```

2. Create your time series collection.

   Add an [`$out`](/docs/manual/reference/operator/aggregation/out#mongodb-pipeline-pipe.-out) aggregation stage to your pipeline to create a time series collection and insert your data into it. The pipeline below performs the following operations:

   - Uses [`$out`](/docs/manual/reference/operator/aggregation/out#mongodb-pipeline-pipe.-out) with the `timeseries` option to create a `weather_new` time series collection in the `mydatabase` database.

   - Defines the `metaData` field as the `metaField` of the `weather_new` collection.

   - Defines the `ts` field as the `timeField` of the `weather_new` collection.

     **Note:**

     The `timeField` of a time series collection must be a [date](/docs/manual/reference/bson-types#std-label-document-bson-type-date) type.

   ```python
   {
       "$out": {
           "db": "mydatabase",
           "coll": "weather_new",
           "timeseries": {
               "timeField": "ts",
               "metaField": "metaData",
               "granularity": "seconds"
           }
       }
   }

   ```

   For the aggregation stage syntax, see [`$out`](/docs/manual/reference/operator/aggregation/out#mongodb-pipeline-pipe.-out). For a full explanation of the time series options, see the [Time Series Field Reference.](/docs/manual/core/timeseries/timeseries-procedures#std-label-time-series-fields)

3. Run your aggregation pipeline.

   Run the complete aggregation pipeline to migrate the data into the new time series collection.

   ```python
   pipeline = [
       {
           "$addFields": {
               "metaData": {
                   "st": "$st",
                   "position": "$position",
                   "elevation": "$elevation",
                   "callLetters": "$callLetters",
                   "qualityControlProcess": "$qualityControlProcess",
                   "type": "$type"
               }
           }
       },
       {
           "$project": {
               "_id": 1,
               "ts": 1,
               "metaData": 1,
               "dataSource": 1,
               "airTemperature": 1,
               "dewPoint": 1,
               "pressure": 1,
               "wind": 1,
               "visibility": 1,
               "skyCondition": 1,
               "sections": 1,
               "precipitationEstimatedObservation": 1
           }
       },
       {
           "$out": {
               "db": "mydatabase",
               "coll": "weather_new",
               "timeseries": {
                   "timeField": "ts",
                   "metaField": "metaData",
                   "granularity": "seconds"
               }
           }
       }
   ]

   weather_data_coll.aggregate(pipeline)

   ```

4. Review your data.

   After you run this aggregation pipeline, you can use `find_one()` method to view a document in your `weather_new` time series collection:

   ```python
   weather_new_coll = timeseries_db["weather_new"]
   result = weather_new_coll.find_one()

   ```

   **Output:**

   ```text
   {'_id': ObjectId('5553a998e4b02cf7151190b8'),
    'ts': datetime.datetime(1984, 3, 5, 13, 0),
    'metaData': {'st': 'x+47600-047900',
                 'position': {'type': 'Point', 'coordinates': [-47.9, 47.6]},
                 'elevation': 9999,
                 'callLetters': 'VCSZ',
                 'qualityControlProcess': 'V020',
                 'type': 'FM-13'},
    'dataSource': '4',
    'airTemperature': {'value': -3.1, 'quality': '1'},
    'dewPoint': {'value': 999.9, 'quality': '9'},
    'pressure': {'value': 1015.3, 'quality': '1'},
    'wind': {'direction': {'angle': 999, 'quality': '9'},
             'type': '9',
             'speed': {'rate': 999.9, 'quality': '9'}},
    'visibility': {'distance': {'value': 999999, 'quality': '9'},
                   'variability': {'value': 'N', 'quality': '9'}},
    'skyCondition': {'ceilingHeight': {'value': 99999,
                                       'quality': '9',
                                       'determination': '9'},
                     'cavok': 'N'},
    'sections': ['AG1'],
    'precipitationEstimatedObservation': {'discrepancy': '2',
                                          'estimatedWaterDepth': 999}}

   ```

For more information on additional considerations for migrating your data, see [Best Practices for Time Series Collections.](/docs/manual/core/timeseries/timeseries-best-practices#std-label-timeseries-best-practices)

## Next Steps

If your original collection had secondary indexes, manually recreate them now.

If your time series collection includes `timeField` values before `1970-01-01T00:00:00.000Z` or after `2038-01-19T03:14:07.000Z`, MongoDB logs a warning and disables some query optimizations that make use of the [internal clustered index](/docs/manual/core/timeseries-collections#std-label-manual-timeseries-internal-index). To regain query performance and resolve the log warning, [create a secondary index](/docs/manual/core/timeseries/timeseries-secondary-index#std-label-timeseries-add-secondary-index) on the `timeField`.

**See also:**

[Add Secondary Indexes to Time Series Collections](/docs/manual/core/timeseries/timeseries-secondary-index#std-label-timeseries-add-secondary-index)
