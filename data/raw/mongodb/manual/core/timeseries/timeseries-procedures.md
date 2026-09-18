> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Create and Query a Time Series Collection

This page shows how to create and query a time series collection. The code examples provided create and work with sample weather data that contains time, temperature, and sensor information.

**Important: Feature Compatibility Version Requirement**

You can only create time series collections on a system with [featureCompatibilityVersion](/docs/manual/reference/command/setFeatureCompatibilityVersion#std-label-view-fcv) set to 5.0 or greater.

## Create a Time Series Collection

Configure the settings for your time series collection:

```csharp
var timeSeriesOptions = new TimeSeriesOptions(
    timeField: "timestamp", // Required: The field containing the date/time
    metaField: "sensorId", // Optional: The field containing metadata
    granularity: TimeSeriesGranularity.Hours // or 'seconds' | 'minutes' | 'hours'
);

```

The steps below outline how to effectively configure a time series collection's settings.

### Configure a Time Series Collection

1. Define the `timeField` as the field that contains time data and the `metaField` as the field that contains metadata.

   In the example above, `timestamp` is the name of the `timeField` and `sensorId` is the name of the `metaField`. The value of the `timeField` field must be a [date](/docs/manual/reference/bson-types#std-label-document-bson-type-date) type.

   **Important:**

   Choosing the right `metaField` for your collection optimizes both storage and query performance. For more information on `metaField` selection and best practices, see [metaFields.](/docs/manual/core/timeseries-collections#std-label-timeseries-collections-metafield)

2. Define the time interval for each [bucket](/docs/manual/core/timeseries/timeseries-bucketing#std-label-timeseries-bucketing-specifics) of data.

   You can either use **manual bucketing** by defining a `granularity` field or **interval bucketing** by defining both `bucketMaxSpanSeconds` and `bucketRoundingSeconds` fields:

   - Define a `granularity` field, as shown above.

     For more detailed information on selecting a `granularity` value, see [Granularity Considerations.](/docs/manual/core/timeseries/timeseries-considerations#std-label-timeseries-granularity-considerations)

   **OR**

   - In MongoDB 6.3 and later, you can define `bucketMaxSpanSeconds` and `bucketRoundingSeconds` fields.

     Both values must be the same. If one is defined, the other must be as well:

     ```csharp
     var timeSeriesOptions = new TimeSeriesOptions(
         timeField: "date",
         metaField: "ticker",
         bucketMaxSpanSeconds: 3600,
         bucketRoundingSeconds: 3600
     );

     var options = new CreateCollectionOptions
     {
         TimeSeriesOptions = timeSeriesOptions
     };

     ```

   **Important: Changing Time Series Intervals**

   After creation, you can modify granularity or bucket definitions by using the .NET/C# driver `RunCommand()` method to run the [`collMod`](/docs/manual/reference/command/collMod#mongodb-dbcommand-dbcmd.collMod) database command. However, you can only increase the time span covered by each bucket.

   For more information on running database commands from the C# Driver, refer to the [Run a Database Command](https://www.mongodb.com/docs/drivers/csharp/current/run-command/) page in the Node.js Driver documentation.

   For more information on modifying time series intervals, see [Change Time Series Granularity.](/docs/manual/core/timeseries/timeseries-granularity#std-label-change-granularity)

3. Optionally, set `ExpireAfter` to expire documents when the value of the `timeField` reaches the specified interval. Expired documents are automatically deleted:

   ```csharp
   // Define CreateCollectionOptions with TimeSeriesOptions
   var createCollectionOptions = new CreateCollectionOptions
   {
       TimeSeriesOptions = timeSeriesOptions,
       ExpireAfter = TimeSpan.FromHours(24) // Optional: Expire documents after a specified time period.
   };

   ```

4. Create the collection in a database using the `CreateCollection()` method.

   The following example creates a database named `timeseries` and stores a reference to it under `timeSeriesDB`. It then create a timeseries collection named `weather` in that database and stores a reference to it under the same name:

   ```csharp
   var database = client.GetDatabase("timeseries");
   database.CreateCollection("weather", createCollectionOptions);

   ```

You must first configure the settings for your time series collection:

### Configure a Time Series Collection

1. Create and Configure a `TimeSeriesOptions` object

   ```java
   TimeSeriesOptions timeSeriesOptions = new TimeSeriesOptions("time")
           .metaField("sensor")
           .granularity(TimeSeriesGranularity.HOURS); // '.SECONDS' | '.MINUTES' | '.HOURS'

   ```

   Define the `timeField` and `metaField`.

   The `timefield` contains the time data and the `metaField` contains the metadata. The `TimeSeriesOptions` object stores the `timeField`.

   In the example above, `time` is the name of the `timeField` and `sensor` is the name of the `metaField`. The value of the `timeField` field must be a [date](/docs/manual/reference/bson-types#std-label-document-bson-type-date) type.

   **Important:**

   Choosing the right `metaField` for your collection optimizes both storage and query performance. For more information on `metaField` selection and best practices, see [metaFields.](/docs/manual/core/timeseries-collections#std-label-timeseries-collections-metafield)

   Define the time interval for each [bucket](/docs/manual/core/timeseries/timeseries-bucketing#std-label-timeseries-bucketing-specifics) of data.

   You can either use **manual bucketing** by defining a `granularity` field or **interval bucketing** by defining both the `bucketMaxSpan` and `bucketRounding` fields:

   - Define a `granularity` field, as shown above.

     For more detailed information on selecting a `granularity` value, see [Granularity Considerations.](/docs/manual/core/timeseries/timeseries-considerations#std-label-timeseries-granularity-considerations)

   **OR**

   - In MongoDB 6.3 and later, you can define the `bucketMaxSpan` and `bucketRounding` fields.

     Both values must be the same, and you must specify the unit of time you are using. If one is defined, the other must be as well:

     ```java
     TimeSeriesOptions timeSeriesOptions = new TimeSeriesOptions("time")
             .metaField("sensor")
             .bucketMaxSpan( (long) 3600, TimeUnit.SECONDS)
             .bucketRounding( (long) 3600, TimeUnit.SECONDS);

     ```

   **Important: Changing Time Series Intervals**

   After creation, you can modify granularity or bucket definitions by using the Java Driver `runCommand()` method to run the [`collMod`](/docs/manual/reference/command/collMod#mongodb-dbcommand-dbcmd.collMod) database command. However, you can only increase the time span covered by each bucket.

   For more information on running database commands from the Java Driver, refer to the [Run a Database Command](https://www.mongodb.com/docs/drivers/java/sync/current/command/) page in the Java Driver documentation.

   For more information on modifying time series intervals, see [Change Time Series Granularity.](/docs/manual/core/timeseries/timeseries-granularity#std-label-change-granularity)

2. Create and Configure a `CreateCollectionOptions` object

   ```java
   CreateCollectionOptions collectionOptions = new CreateCollectionOptions()
           .timeSeriesOptions(timeSeriesOptions)
           .expireAfter(86400, TimeUnit.SECONDS); // optional

   ```

   Set the `timeSeriesOptions` field to the `TimeSeriesOptions` object you created in the previous step.

   Optionally, set `expireAfter` to expire documents when the value of the `timeField` reaches the specified interval. Expired documents are automatically deleted.

You then create your collection with the configured settings using the `db.createCollection()` method.

The following example uses a database named `timeseries` and stores a reference to it under `timeSeriesDB`. It then create a timeseries collection named `weather` in that database and stores a reference to it under the same name:

```java
MongoDatabase timeSeriesDB = mongoClient.getDatabase("timeseries");
timeSeriesDB.createCollection("weather", collectionOptions);

```

Configure the settings for your time series collection:

```javascript
const settings = {
  timeseries: {
    timeField: 'time',
    metaField: 'sensor',
    granularity: 'hours', // 'seconds' | 'minutes' | 'hours'
  },
  expireAfterSeconds: 86400, // optional
};

```

The steps below outline how to effectively configure a time series collection's settings.

### Configure a Time Series Collection

1. Define the `timeField` as the field that contains time data and the `metaField` as the field that contains metadata.

   In the example above, `time` is the name of the `timeField` and `sensor` is the name of the `metaField`. The value of the `timeField` field must be a [date](/docs/manual/reference/bson-types#std-label-document-bson-type-date) type.

   **Important:**

   Choosing the right `metaField` for your collection optimizes both storage and query performance. For more information on `metaField` selection and best practices, see [metaFields.](/docs/manual/core/timeseries-collections#std-label-timeseries-collections-metafield)

2. Define the time interval for each [bucket](/docs/manual/core/timeseries/timeseries-bucketing#std-label-timeseries-bucketing-specifics) of data.

   You can either use **manual bucketing** by defining a `granularity` field or **interval bucketing** by defining both `bucketMaxSpanSeconds` and `bucketRoundingSeconds` fields:

   - Define a `granularity` field, as shown above.

     For more detailed information on selecting a `granularity` value, see [Granularity Considerations.](/docs/manual/core/timeseries/timeseries-considerations#std-label-timeseries-granularity-considerations)

   **OR**

   - In MongoDB 6.3 and later, you can define `bucketMaxSpanSeconds` and `bucketRoundingSeconds` fields.

     Both values must be the same. If one is defined, the other must be as well:

     ```javascript
     const settings = {
       timeseries: {
         timeField: 'time',
         metaField: 'sensor',
         bucketMaxSpanSeconds: 3600,
         bucketRoundingSeconds: 3600,
       },
       expireAfterSeconds: 86400, // optional
     };

     ```

   **Important: Changing Time Series Intervals**

   After creation, you can modify granularity or bucket definitions by using the Node.js Driver `command()` method to run the [`collMod`](/docs/manual/reference/command/collMod#mongodb-dbcommand-dbcmd.collMod) database command. However, you can only increase the time span covered by each bucket.

   For more information on running database commands from the Node.js Driver, refer to the [Run a Database Command](https://www.mongodb.com/docs/drivers/node/current/run-command/) page in the Node.js Driver documentation.

   For more information on modifying time series intervals, see [Change Time Series Granularity.](/docs/manual/core/timeseries/timeseries-granularity#std-label-change-granularity)

3. Optionally, set `expireAfterSeconds` to expire documents when the value of the `timeField` reaches the specified interval. Expired documents are automatically deleted.

4. Create the collection in a database using the `Db.createCollection()` method.

   The following example creates a database named `timeseries` and stores a reference to it under `timeSeriesDB`. It then create a timeseries collection named `weather` in that database and stores a reference to it under the same name:

   ```javascript
   const timeSeriesDB = client.db('timeseries');
   const weather = await timeSeriesDB.createCollection('weather', settings);

   ```

You must first configure the settings for your time series collection:

### Configure a Time Series Collection

1. Create and Configure a `timeseries` dictionary

   ```python
   time_series_options = {
       "timeField": "time",
       "metaField": "sensor",
       "granularity": "hours",
   }
   expire_after_seconds = 86400 # optional

   ```

   Define the `timeField` and `metaField`.

   The `timefield` contains the time data and the `metaField` contains the metadata.

   In the example above, `time` is the name of the `timeField` and `sensor` is the name of the `metaField`. The value of the `timeField` field must be a [date](/docs/manual/reference/bson-types#std-label-document-bson-type-date) type.

   **Important:**

   Choosing the right `metaField` for your collection optimizes both storage and query performance. For more information on `metaField` selection and best practices, see [metaFields.](/docs/manual/core/timeseries-collections#std-label-timeseries-collections-metafield)

   Define the time interval for each [bucket](/docs/manual/core/timeseries/timeseries-bucketing#std-label-timeseries-bucketing-specifics) of data.

   You can either use **manual bucketing** by defining a `granularity` field or **interval bucketing** by defining both the `bucketMaxSpanSeconds` and `bucketRoundingSeconds` fields:

   - Define a `granularity` field, as shown above.

     For more detailed information on selecting a `granularity` value, see [Granularity Considerations.](/docs/manual/core/timeseries/timeseries-considerations#std-label-timeseries-granularity-considerations)

   **OR**

   - As an alternative to `granularity`, you can define the `bucketMaxSpanSeconds` and `bucketRoundingSeconds` fields.

     Both values must be the same, and you must specify the unit of time you are using. If one is defined, the other must be as well:

     ```python
     time_series_options = {
         "timeField": "time",
         "metaField": "sensor",
         "bucketMaxSpanSeconds": 3600,
         "bucketRoundingSeconds": 3600
     }
     expire_after_seconds = 86400  # optional

     ```

   **Important: Changing Time Series Intervals**

   After creation, you can modify granularity or bucket definitions by using the PyMongo Driver `command()` method to run the [`collMod`](/docs/manual/reference/command/collMod#mongodb-dbcommand-dbcmd.collMod) database command. However, you can only increase the time span covered by each bucket.

   For more information on running database commands from the Java Driver, refer to the [Run a Database Command](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/run-command/) page in the PyMongo Driver documentation.

   For more information on modifying time series intervals, see [Change Time Series Granularity.](/docs/manual/core/timeseries/timeseries-granularity#std-label-change-granularity)

2. Create the collection

   You then create your collection with the configured settings using the `db.create_collection()` method.

   The following example uses a database named `timeseries` and stores a reference to it under `timeseries_db`. It then create a timeseries collection named `weather` in that database:

   ```python
   timeseries_db = client["timeseries"]
   timeseries_db.create_collection("weather", timeseries=time_series_options, expireAfterSeconds=expire_after_seconds)

   ```

   Optionally, set `expireAfterSeconds` to expire documents when the value of the `timeField` reaches the specified interval. Expired documents are automatically deleted.

Create your collection with your desired time series settings using the [`db.createCollection()`](/docs/manual/reference/method/db.createCollection#mongodb-method-db.createCollection) method.

The following example creates a collection named `weather`:

```javascript
db.createCollection(
  "weather",
  {
    timeseries: { 
      timeField: "time", 
      metaField: "sensor", 
      granularity: "seconds" 
    },
    expireAfterSeconds: 86400
  }
)

```

For more information on running database commands see the [Run Commands](https://www.mongodb.com/docs/mongodb-shell/run-commands/) page.

The steps below outline how to effectively configure a time series collection's settings.

### Configure a Time Series Collection

1. Define the `timeField` as the field that contains time data and the `metaField` as the field that contains metadata.

   In the example above, `time` is the name of the `timeField` and `sensor` is the name of the `metaField`. The value of the `timeField` field must be a [date](/docs/manual/reference/bson-types#std-label-document-bson-type-date) type.

   **Important:**

   Choosing the right `metaField` for your collection optimizes both storage and query performance. For more information on `metaField` selection and best practices, see [metaFields.](/docs/manual/core/timeseries-collections#std-label-timeseries-collections-metafield)

2. Define the time interval for each [bucket](/docs/manual/core/timeseries/timeseries-bucketing#std-label-timeseries-bucketing-specifics) of data.

   You can either use **manual bucketing** by defining a `granularity` field or **interval bucketing** by defining both `bucketMaxSpanSeconds` and `bucketRoundingSeconds` fields:

   - Define a `granularity` field, as shown above.

     For more detailed information on selecting a `granularity` value, see [Granularity Considerations.](/docs/manual/core/timeseries/timeseries-considerations#std-label-timeseries-granularity-considerations)

   **OR**

   - In MongoDB 6.3 and later, you can define `bucketMaxSpanSeconds` and `bucketRoundingSeconds` fields.

     Both values must be the same. If one is defined, the other must be as well:

     ```javascript
     db.createCollection(
       "weather",
       {
         timeseries: { 
           timeField: "time", 
           metaField: "sensor", 
           bucketMaxSpanSeconds: 3600,
           bucketRoundingSeconds: 3600,
         },
         expireAfterSeconds: 86400,
       }
     )

     ```

   **Important: Changing Time Series Intervals**

   After creation, you can modify granularity or bucket definitions by using the [`collMod`](/docs/manual/reference/command/collMod#mongodb-dbcommand-dbcmd.collMod) database command. However, you can only increase the time span covered by each bucket.

   For more information on modifying time series intervals, see [Change Time Series Granularity.](/docs/manual/core/timeseries/timeseries-granularity#std-label-change-granularity)

3. Optionally, set `expireAfterSeconds` to expire documents when the value of the `timeField` reaches the specified interval. Expired documents are automatically deleted.

### Time Series Field Reference

A time series collection includes the following fields:

| Field | Type | Description |
| --- | --- | --- |
| `timeseries.timeField` | string | Required. The name of the field which contains the date in each time series document. Documents in a time series collection must have a valid BSON date as the value for the `timeField`. |
| `timeseries.metaField` | string | Optional. The name of the field which contains metadata in each time series document. The metadata in the specified field should be data that is used to label a unique series of documents. The metadata should rarely, if ever, change The name of the specified field may not be `_id` or the same as the `timeseries.timeField`. The field can be of any data type. Although the `metaField` field is optional, using metadata can improve query optimization. For example, MongoDB automatically [creates a compound index](/docs/manual/core/timeseries/timeseries-secondary-index#std-label-timeseries-add-secondary-index) on the `metaField` and `timeField` fields for new collections. If you do not provide a value for this field, the data is bucketed solely based on time. |
| `timeseries.granularity` | integer | Optional. Do not use if setting `bucketRoundingSeconds` and `bucketMaxSpanSeconds`. Possible values are `seconds` (default), `minutes`, and `hours`. Set `granularity` to the value that most closely matches the time between consecutive incoming timestamps. This improves performance by optimizing how MongoDB stores data in the collection. For more information on granularity and bucket intervals, see [Set Granularity for Time Series Data.](/docs/manual/core/timeseries/timeseries-granularity#std-label-timeseries-granularity) |
| `timeseries.bucketMaxSpanSeconds` | integer | Optional. Use with `bucketRoundingSeconds` as an alternative to `granularity`. Sets the maximum time between timestamps in the same bucket. Possible values are 1-31536000. **New in version 6.3** |
| `timeseries.bucketRoundingSeconds` | integer | Optional. Use with `bucketMaxSpanSeconds` as an alternative to `granularity`. Must be equal to `bucketMaxSpanSeconds`. When a document requires a new bucket, MongoDB rounds down the document's timestamp value by this interval to set the minimum time for the bucket. **New in version 6.3** |
| `expireAfterSeconds` | integer | Optional. Enable the automatic deletion of documents in a time series collection by specifying the number of seconds after which documents expire. MongoDB deletes expired documents automatically. See [Set up Automatic Removal for Time Series Collections (TTL)](/docs/manual/core/timeseries/timeseries-automatic-removal#std-label-manual-timeseries-automatic-removal) for more information. |

Other allowed options that are not specific to time series collections are:

- `storageEngine`

- `indexOptionDefaults`

- `collation`

- `writeConcern`

- `comment`

## Insert Measurements into a Time Series Collection

Each document you insert should contain a single measurement. To insert multiple documents at once, use the `InsertMany()` method:

```csharp
var uri = "<connection string>";
var client = new MongoClient(uri);
var database = client.GetDatabase("timeseries");
var collection = database.GetCollection<SensorReading>("weather");

var sampleDocuments = new List<SensorReading>()
{
    new SensorReading(
        new Sensor(5578, "temperature"),
        temp: 45.2,
        timestamp: new DateTime(2045, 11, 18, 0, 0, 0, 0)),
    new SensorReading(
        new Sensor(5578, "temperature"),
        47.3,
        new DateTime(2045, 11, 18, 6, 0, 0, 0)),
    new SensorReading(
        new Sensor(5578, "temperature"),
        48.8,
        new DateTime(2045, 11, 18, 18, 0, 0, 0)),
    new SensorReading(
        new Sensor(5578, "temperature"),
        43.3,
        new DateTime(2045, 11, 19, 0, 0, 0, 0)),
    new SensorReading(
        new Sensor(5578, "temperature"),
        47.2,
        new DateTime(2045, 11, 19, 6, 0, 0, 0)),
    new SensorReading(
        new Sensor(5578, "temperature"),
        51.5,
        new DateTime(2045, 11, 19, 12, 0, 0, 0)),
    new SensorReading(
        new Sensor(5578, "temperature"),
        48.2,
        new DateTime(2045, 11, 19, 18, 0, 0, 0)),
};

try
{
    collection.InsertMany(sampleDocuments);
}
catch (Exception ex)
{
    Console.WriteLine(ex.Message);
}

```

To insert a single document, use the `InsertOne()` method.

For more information on inserting documents, see [Insert Operations.](https://www.mongodb.com/docs/drivers/csharp/sync/current/crud/insert/)

**Tip: Optimize Insert Performance**

To learn how to optimize inserts for large operations, see [Inserts Best Practices.](/docs/manual/core/timeseries/timeseries-best-practices#std-label-tsc-best-practice-optimize-inserts)

Each document you insert should contain a single measurement. To insert multiple documents at once, use the `insertMany()` method:

```java
weather = timeSeriesDB.getCollection("weather");

weather.insertMany(
    Arrays.asList(
        new Document("sensor", new Document("sensorId", 5578).append("type", "temperature"))
                .append("time", Date.from(Instant.parse("2045-11-18T00:00:00Z")))
                .append("temp", 45.2),
        new Document("sensor", new Document("sensorId", 5578).append("type", "temperature"))
                .append("time", Date.from(Instant.parse("2045-11-18T06:00:00Z")))
                .append("temp", 47.3),
        new Document("sensor", new Document("sensorId", 5578).append("type", "temperature"))
                .append("time", Date.from(Instant.parse("2045-11-18T12:00:00Z")))
                .append("temp", 49.1),
        new Document("sensor", new Document("sensorId", 5578).append("type", "temperature"))
                .append("time", Date.from(Instant.parse("2045-11-18T18:00:00Z")))
                .append("temp", 48.8),
        new Document("sensor", new Document("sensorId", 5578).append("type", "temperature"))
                .append("time", Date.from(Instant.parse("2045-11-19T00:00:00Z")))
                .append("temp", 43.3),
        new Document("sensor", new Document("sensorId", 5578).append("type", "temperature"))
                .append("time", Date.from(Instant.parse("2045-11-19T06:00:00Z")))
                .append("temp", 47.2),
        new Document("sensor", new Document("sensorId", 5578).append("type", "temperature"))
                .append("time", Date.from(Instant.parse("2045-11-19T12:00:00Z")))
                .append("temp", 51.5),
        new Document("sensor", new Document("sensorId", 5578).append("type", "temperature"))
                .append("time", Date.from(Instant.parse("2045-11-19T18:00:00Z")))
                .append("temp", 48.2)
    )
);

```

To insert a single document, use the `insertOne()` method.

For more information on inserting documents, see [Insert Operations.](https://www.mongodb.com/docs/drivers/java/sync/current/crud/insert/)

**Tip: Optimize Insert Performance**

To learn how to optimize inserts for large operations, see [Inserts Best Practices.](/docs/manual/core/timeseries/timeseries-best-practices#std-label-tsc-best-practice-optimize-inserts)

Each document you insert should contain a single measurement. To insert multiple documents at once, use the `insertMany()` method:

```javascript
const sampleDocuments = [
  {
    sensor: { sensorId: 5578, type: 'temperature' },
    time: new Date(2045, 11, 18, 0, 0, 0, 0),
    temp: 45.2,
  },
  {
    sensor: { sensorId: 5578, type: 'temperature' },
    time: new Date(2045, 11, 18, 6, 0, 0, 0),
    temp: 47.3,
  },
  {
    sensor: { sensorId: 5578, type: 'temperature' },
    time: new Date(2045, 11, 18, 12, 0, 0, 0),
    temp: 49.1,
  },
  {
    sensor: { sensorId: 5578, type: 'temperature' },
    time: new Date(2045, 11, 18, 18, 0, 0, 0),
    temp: 48.8,
  },
  {
    sensor: { sensorId: 5578, type: 'temperature' },
    time: new Date(2045, 11, 19, 0, 0, 0, 0),
    temp: 43.3,
  },
  {
    sensor: { sensorId: 5578, type: 'temperature' },
    time: new Date(2045, 11, 19, 6, 0, 0, 0),
    temp: 47.2,
  },
  {
    sensor: { sensorId: 5578, type: 'temperature' },
    time: new Date(2045, 11, 19, 12, 0, 0, 0),
    temp: 51.5,
  },
  {
    sensor: { sensorId: 5578, type: 'temperature' },
    time: new Date(2045, 11, 19, 18, 0, 0, 0),
    temp: 48.2,
  },
];

await weather.insertMany(sampleDocuments);

```

To insert a single document, use the `insertOne()` method.

**Tip: Optimize Insert Performance**

To learn how to optimize inserts for large operations, see [Inserts Best Practices.](/docs/manual/core/timeseries/timeseries-best-practices#std-label-tsc-best-practice-optimize-inserts)

Each document you insert should contain a single measurement. To insert multiple documents at once, use the `insert_many()` method:

```python
sample_documents = [
    {
        "sensor": {"sensorId": 5578, "type": "temperature"},
        "time": datetime(2045, 12, 18, 0, 0, 0),
        "temp": 45.2,
    },
    {
        "sensor": {"sensorId": 5578, "type": "temperature"},
        "time": datetime(2045, 12, 18, 6, 0, 0),
        "temp": 47.3,
    },
    {
        "sensor": {"sensorId": 5578, "type": "temperature"},
        "time": datetime(2045, 12, 18, 12, 0, 0),
        "temp": 49.1,
    },
    {
        "sensor": {"sensorId": 5578, "type": "temperature"},
        "time": datetime(2045, 12, 18, 18, 0, 0),
        "temp": 48.8,
    },
    {
        "sensor": {"sensorId": 5578, "type": "temperature"},
        "time": datetime(2045, 12, 19, 0, 0, 0),
        "temp": 43.3,
    },
    {
        "sensor": {"sensorId": 5578, "type": "temperature"},
        "time": datetime(2045, 12, 19, 6, 0, 0),
        "temp": 47.2,
    },
    {
        "sensor": {"sensorId": 5578, "type": "temperature"},
        "time": datetime(2045, 12, 19, 12, 0, 0),
        "temp": 51.5,
    },
    {
        "sensor": {"sensorId": 5578, "type": "temperature"},
        "time": datetime(2045, 12, 19, 18, 0, 0),
        "temp": 48.2,
    },
]

weather_coll.insert_many(sample_documents)

```

To insert a single document, use the `insert_one()` method.

For more information on inserting documents, see [Insert Operations.](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/insert/)

**Tip: Optimize Insert Performance**

To learn how to optimize inserts for large operations, see [Inserts Best Practices.](/docs/manual/core/timeseries/timeseries-best-practices#std-label-tsc-best-practice-optimize-inserts)

Each document you insert should contain a single measurement. To insert multiple documents at once, use the [`db.collection.insertMany()`](/docs/manual/reference/method/db.collection.insertMany#mongodb-method-db.collection.insertMany) method:

```javascript
db.weather.insertMany([
  {
    sensor: { sensorId: 5578, type: "temperature" },
    time: new Date(2045, 11, 18, 0, 0, 0, 0),
    temp: 45.2,
  },
  {
    sensor: { sensorId: 5578, type: "temperature" },
    time: new Date(2045, 11, 18, 6, 0, 0, 0),
    temp: 47.3,
  },
  {
    sensor: { sensorId: 5578, type: "temperature" },
    time: new Date(2045, 11, 18, 12, 0, 0, 0),
    temp: 49.1,
  },
  {
    sensor: { sensorId: 5578, type: "temperature" },
    time: new Date(2045, 11, 18, 18, 0, 0, 0),
    temp: 48.8,
  },
  {
    sensor: { sensorId: 5578, type: "temperature" },
    time: new Date(2045, 11, 19, 0, 0, 0, 0),
    temp: 43.3,
  },
  {
    sensor: { sensorId: 5578, type: "temperature" },
    time: new Date(2045, 11, 19, 6, 0, 0, 0),
    temp: 47.2,
  },
  {
    sensor: { sensorId: 5578, type: "temperature" },
    time: new Date(2045, 11, 19, 12, 0, 0, 0),
    temp: 51.5,
  },
  {
    sensor: { sensorId: 5578, type: "temperature" },
    time: new Date(2045, 11, 19, 18, 0, 0, 0),
    temp: 48.2,
  },
])

```

To insert a single document, use the [`db.collection.insertOne()`](/docs/manual/reference/method/db.collection.insertOne#mongodb-method-db.collection.insertOne) method.

**Tip: Optimize Insert Performance**

To learn how to optimize inserts for large operations, see [Inserts Best Practices.](/docs/manual/core/timeseries/timeseries-best-practices#std-label-tsc-best-practice-optimize-inserts)

## Query a Time Series Collection

You query a time series collection the same way you query a standard MongoDB collection.

To return one document from a time series collection, you use a [FilterDefinitionBuilder\<TDocument>](|api-root|/MongoDB.Driver/MongoDB.Driver.FilterDefinitionBuilder-1.html) to create a filter to match a document. You pass the filter to the `Find()` method of the `IMongoCollection<TDocument>` class.  The following example creates a FilterDefinition and also uses a ProjectionDefinition to omit the `_id` field from the results. It returns a `List<BsonDocument>`.

```csharp
var query =
    Builders<SensorReading>.Filter.Where
        (s => s.Timestamp == new DateTime(2045, 11, 19, 0, 0, 0, 0));

var projection = Builders<SensorReading>.Projection
    .Exclude(s => s.Id); // Exclude the _id field

var result = await collection.Find(query).Project(projection).ToListAsync();

```

**Output:**

```text
{
  "time": {
    "$date": "2045-11-19T18:00:00Z"
  },
  "sensor": {
    "sensorId": 5578,
    "type": "temperature"
  },
  "temp": 48.2
}

```

For more information on querying your collection, see [MongoDB .NET/C# Driver documentation.](https://www.mongodb.com/docs/drivers/csharp/sync/current/crud/query-documents/find/)

**Tip: Optimize Query Performance**

To learn how to optimize queries on your time series collection, see [Query Best Practices.](/docs/manual/core/timeseries/timeseries-best-practices#std-label-tsc-best-practice-optimize-query-performance)

You query a time series collection the same way you query a standard MongoDB collection.

To return one document from a time series collection, you can use the `findOne()` method. This returns a [cursor.](/docs/manual/core/cursors#std-label-cursors)

The following example uses the `projection` field in the query to omit the `_id` field from the results:

```java
Date target = Date.from(Instant.parse("2045-11-19T18:00:00Z"));

FindIterable<Document> findResults = weather.find(new Document("time", target))
        .projection(new Document("_id", 0));

```

You can then use the cursor to access the resulting document:

```java
for  (Document document : findResults) {
    System.out.println(document.toJson());
}

```

**Output:**

```text
{"time": {"$date": "2045-11-19T18:00:00Z"}, "sensor": {"sensorId": 5578, "type": "temperature"}, "temp": 48.2}

```

For more information on querying your collection, see [MongoDB Java Driver documentation.](https://www.mongodb.com/docs/drivers/java/sync/current/crud/query-documents/find/)

**Tip: Optimize Query Performance**

To learn how to optimize queries on your time series collection, see [Query Best Practices.](/docs/manual/core/timeseries/timeseries-best-practices#std-label-tsc-best-practice-optimize-query-performance)

You query a time series collection the same way you query a standard MongoDB collection.

To return one document from a time series collection, you can use the `findOne()` method. The following example uses the `projection` field in the query to omit the `_id` field from the returned documents:

```javascript
const result = await weather.findOne(
  { time: new Date(2045, 11, 19, 18, 0, 0, 0) },
  { projection: { _id: 0 } }
);

```

**Output:**

```shell
{
  time: 2045-12-19T18:00:00.000Z,
  sensor: { sensorId: 5578, type: 'temperature' },
  temp: 48.2
}
```

For more information on time series queries, see [Query Best Practices.](/docs/manual/core/timeseries/timeseries-best-practices#std-label-tsc-best-practice-optimize-query-performance)

You query a time series collection the same way you query a standard MongoDB collection.

To return one document from a time series collection, you can use the `find_one()` method. This returns a [cursor.](/docs/manual/core/cursors#std-label-cursors)

The following example uses `"_id": 0` in the query to omit the `_id` field from the results:

```python
result = weather_coll.find_one(
    {"time": datetime(2045, 12, 19, 18, 0, 0)},
    {"_id": 0}
)

```

The `find_one()` method returns a single document that matches the query:

```text
{'time': datetime.datetime(2045, 12, 19, 18, 0), 'sensor': {'sensorId': 5578, 'type': 'temperature'}, 'temp': 48.2}
```

For more information on querying your collection, see [MongoDB PyMongo Driver documentation.](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/query/)

**Tip: Optimize Query Performance**

To learn how to optimize queries on your time series collection, see [Query Best Practices.](/docs/manual/core/timeseries/timeseries-best-practices#std-label-tsc-best-practice-optimize-query-performance)

You query a time series collection the same way you query a standard MongoDB collection.

To return one document from a time series collection, you can use the [`db.collection.findOne()`](/docs/manual/reference/method/db.collection.findOne#mongodb-method-db.collection.findOne) method. The following example uses the `projection` field in the query to omit the `_id` field from the returned documents:

```javascript
db.weather.findOne(
  { time: new Date(2045, 11, 19, 18, 0, 0, 0) },
  { projection: { _id: 0 } }
)

```

**Output:**

```shell
{
  time: ISODate("2045-12-19T18:00:00.000Z"),
  sensor: { sensorId: 5578, type: "temperature" },
  temp: 48.2
}

```

For more information on time series queries, see [Query Best Practices.](/docs/manual/core/timeseries/timeseries-best-practices#std-label-tsc-best-practice-optimize-query-performance)

## Run Aggregations on a Time Series Collection

For additional query functionality, you can use the `Aggregate()` method to run an [aggregation pipeline.](/docs/manual/core/aggregation-pipeline#std-label-aggregation-pipeline)

For more information on aggregations, see [Aggregation and Operator Considerations.](/docs/manual/core/timeseries/timeseries-aggregations-operators#std-label-manual-timeseries-aggregations-operators)

This example creates an aggregation pipeline that:

- Matches all documents with a `sensor.sensor_id` of "5578"

- Groups those documents by the date of the measurement

- Calculates the average of all temperature measurements that day in a new property called `avgTemp`

- Returns a `List<BsonDocument>`

```csharp

var pipeline = new BsonDocument[]
{
    new("$match",
        new BsonDocument
            {
                { "sensor.sensor_id", 5578 },
                { "sensor.type", "temperature" }
            }
        ),
    new("$group",
        new BsonDocument
        {
            {
                "_id",
                new BsonDocument("date",
                    new BsonDocument("$dateTrunc",
                        new BsonDocument
                        {
                            { "date", "$time" },
                            { "unit", "day" }
                        }))
            },
            {
                "avgTemp", new BsonDocument("$avg", "$temp")
            }
        }),
    new("$sort", new BsonDocument("avgTemp", -1))
};

var pipelineDefinition = PipelineDefinition<SensorReading, BsonDocument>.Create(pipeline);

var client = new MongoClient(Uri);
var database = client.GetDatabase("timeseries");
var collection = database.GetCollection<SensorReading>("weather");

var result = await collection.Aggregate(pipelineDefinition).ToListAsync();

```

**Output:**

```text
{"_id": {"$date": "2021-11-18T00:00:00Z"}, "avgTemp": 47.6}
{"_id": {"$date": "2021-11-19T00:00:00Z"}, "avgTemp": 47.55}
```

For more information on running aggregations using the .NET/C# driver, see [.NET/C# Driver Aggregations.](https://www.mongodb.com/docs/drivers/csharp/sync/current/aggregation/)

For more information on how to access data from a cursor, see [Access Data From a Cursor.](https://www.mongodb.com/docs/drivers/csharp/sync/current/crud/query-documents/cursor/)

For additional query functionality, you can use the `aggregate()` method to run an [aggregation pipeline.](/docs/manual/core/aggregation-pipeline#std-label-aggregation-pipeline)

For more information on aggregations, see [Aggregation and Operator Considerations.](/docs/manual/core/timeseries/timeseries-aggregations-operators#std-label-manual-timeseries-aggregations-operators)

This example:

- Groups all documents by the date of the measurement

- Calculates the average of all temperature measurements that day

- Returns a [cursor](/docs/manual/core/cursors#std-label-cursors)

```java
// Create an aggregation pipeline
List<Document> pipeline = Arrays.asList(
        new Document("$match", new Document("sensor.sensorId", 5578).append("sensor.type", "temperature")),
        new Document("$group", new Document("_id", new Document("$dateTrunc", new Document("date", "$time").append("unit", "day")))
                .append("avgTemp", new Document("$avg", "$temp"))),
        new Document("$sort", new Document("avgTemp", -1))
);

// Run the aggregation
AggregateIterable<Document> aggregationResults = weather.aggregate(pipeline);

```

You can then use the cursor to iterate through the resulting documents:

```java
for  (Document document : aggregationResults) {
    System.out.println(document.toJson());
}

```

**Output:**

```text
{"_id": {"$date": "2045-11-18T00:00:00Z"}, "avgTemp": 47.6}
{"_id": {"$date": "2045-11-19T00:00:00Z"}, "avgTemp": 47.55}

```

For more information on running aggregations using the Java Driver, see [Java Driver Aggregations.](https://www.mongodb.com/docs/drivers/java/sync/current/aggregation/)

For more information on how to access data from a cursor, see [Access Data From a Cursor.](https://www.mongodb.com/docs/drivers/java/sync/current/crud/query-documents/cursor/)

For additional query functionality, you can use the `aggregate()` method to run an [aggregation pipeline.](/docs/manual/core/aggregation-pipeline#std-label-aggregation-pipeline)

For more information on aggregations, see [Aggregation and Operator Considerations.](/docs/manual/core/timeseries/timeseries-aggregations-operators#std-label-manual-timeseries-aggregations-operators)

This example groups all documents by the date of the measurement, then calculates the average of all temperature measurements that day and returns a [cursor:](/docs/manual/core/cursors#std-label-cursors)

```javascript
const pipeline = [
  { $match: { 'sensor.sensorId': 5578, 'sensor.type': 'temperature' } },
  {
    $group: {
      _id: { $dateTrunc: { date: '$time', unit: 'day' } },
      avgTemp: { $avg: '$temp' },
    },
  },
  { $sort: { avgTemp: -1 } },
];

const cursor = weather.aggregate(pipeline);

```

You can then iterate through the resulting documents:

```javascript
for await (const document of cursor) {
  console.log(document);
}

```

**Output:**

```shell
{ _id: 2045-12-18T00:00:00.000Z, avgTemp: 47.6 }
{ _id: 2045-12-19T00:00:00.000Z, avgTemp: 47.55 }
```

For more information on how to access data from a cursor, see [Access Data From a Cursor.](https://www.mongodb.com/docs/drivers/node/current/crud/query/cursor/)

For additional query functionality, you can use the `aggregate()` method to run an [aggregation pipeline.](/docs/manual/core/aggregation-pipeline#std-label-aggregation-pipeline)

For more information on aggregations, see [Aggregation and Operator Considerations.](/docs/manual/core/timeseries/timeseries-aggregations-operators#std-label-manual-timeseries-aggregations-operators)

This example:

- Finds all documents where the sensor ID is 5578

- Groups all documents by the date of the measurement

- Calculates the average of all temperature measurements that day

- Sorts the results by the average temperature in descending order

```python
pipeline = [
    {"$match": {"sensor.sensorId": 5578, "sensor.type": "temperature"}},
    {
        "$group": {
            "_id": {"$dateTrunc": {"date": "$time", "unit": "day"}},
            "avgTemp": {"$avg": "$temp"},
        }
    },
    {"$sort": {"avgTemp": -1}},
]

cursor = weather_coll.aggregate(pipeline)

```

The example returns a [cursor](/docs/manual/core/cursors#std-label-cursors). You can use the cursor to iterate through the resulting documents:

```python
for doc in cursor:
    print(doc)

```

**Output:**

```text
{'_id': datetime.datetime(2045, 12, 18, 0, 0), 'avgTemp': 47.6}
{'_id': datetime.datetime(2045, 12, 19, 0, 0), 'avgTemp': 47.55}
```

For more information on running aggregations using the PyMongo Driver, see [PyMongo Driver Aggregation.](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/aggregation/)

For more information on how to access data from a cursor, see [Access Data From a Cursor.](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/query/cursors/)

For additional query functionality, you can use the [`db.collection.aggregate()`](/docs/manual/reference/method/db.collection.aggregate#mongodb-method-db.collection.aggregate) method to run an [aggregation pipeline.](/docs/manual/core/aggregation-pipeline#std-label-aggregation-pipeline)

For more information on aggregations, see [Aggregation and Operator Considerations.](/docs/manual/core/timeseries/timeseries-aggregations-operators#std-label-manual-timeseries-aggregations-operators)

This example:

- Groups all documents by the date of the measurement

- Calculates the average of all temperature measurements that day

- Returns a [cursor](/docs/manual/core/cursors#std-label-cursors) that can be used to iterate through the resulting documents

```javascript
db.weather.aggregate( [
   { $match: { 'sensor.sensorId': 5578, 'sensor.type': 'temperature' } },
   {
      $group: {
         _id: { $dateTrunc: { date: "$time", unit: "day" } },
         avgTemp: { $avg: "$temp" },
      },
   },
   { $sort: { avgTemp: -1 } }
] )
```

**Output:**

```shell
[
  {
     _id: ISODate("2045-12-18T00:00:00.000Z"),
     avgTemp: 47.6
  },
  {
     _id: ISODate("2045-12-19T00:00:00.000Z"),
     avgTemp: 47.55
  }
]

```

For more information on how to access data from a cursor, see:

- [Iterate a Cursor in mongosh](/docs/manual/tutorial/iterate-a-cursor#std-label-read-operations-cursors)

- [Cursors](/docs/manual/reference/method#std-label-doc-cursor-methods)
