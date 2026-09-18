> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Add Secondary Indexes to Time Series Collections

To improve query performance for [time series collections](/docs/manual/reference/glossary#std-term-time-series-collection), add one or more [secondary indexes](/docs/manual/reference/glossary#std-term-secondary-index) to support common time series query patterns. Starting in MongoDB 6.3, MongoDB automatically creates a [compound index](/docs/manual/core/indexes/index-types/index-compound#std-label-index-type-compound) on the `metaField` and `timeField` fields for new collections.

**Note:**

Not all index types are supported. For a list of unsupported index types, see [Limitations for Secondary Indexes on Time Series Collections.](/docs/manual/core/timeseries/timeseries-limitations#std-label-timeseries-limitations-secondary-indexes)

## Use Secondary Indexes to Improve Sort Performance

Consider a weather data collection with the following configuration:

```csharp
var createCollectionOptions = new CreateCollectionOptions
{
    TimeSeriesOptions = new TimeSeriesOptions(
        timeField: "timestamp",
        metaField: "metadata"),
    ExpireAfter = TimeSpan.FromHours(24)
};

```

In each weather data document, the `metadata` field value is a subdocument with fields for the weather sensor's ID, type, and location:

```csharp
"metadata", new BsonDocument
{
    { "sensorId", 5578 },
    { "type", "omni" },
    { "location", new BsonDocument
        {
            { "type", "Point" },
            { "coordinates", new BsonArray { -77.40711, 39.03335 } }
        }
    }
}

```

The default compound index for the collection indexes the entire `metadata` subdocument, so the index is only used with [`$eq`](/docs/manual/reference/operator/aggregation/eq#mongodb-expression-exp.-eq) queries. By indexing specific `metadata` fields, you improve query performance for other query types.

For example, this [`$in`](/docs/manual/reference/operator/aggregation/in#mongodb-expression-exp.-in) query benefits from a secondary index on `metadata.type`:

```csharp
var filter = Builders<BsonDocument>.Filter
    .In("metadata.type", new[] { "temperature", "pressure" });

```

Sort operations on time series collections can use secondary indexes on the `timeField` field. Under certain conditions, sort operations can also use compound secondary indexes on the `metaField` and `timeField` fields.

The aggregation pipeline uses the [`$match`](/docs/manual/reference/operator/aggregation/match#mongodb-pipeline-pipe.-match) and [`$sort`](/docs/manual/reference/operator/aggregation/sort#mongodb-pipeline-pipe.-sort) stages to determine which indexes a time series collection can use. An index can be used in the following scenarios:

- A sort on `{ <timeField>: ±1 }` uses a secondary index on `<timeField>`.

- A sort on `{ <metaField>: ±1, timeField: ±1 }` uses the default compound index on `{ <metaField>: ±1, timeField: ±1 }`.

- A sort on `{ <timeField>: ±1 }` uses a secondary index on `{ metaField: ±1, timeField: ±1 }` when there is a point predicate on `<metaField>`.

For example, the following `sensorData` collection contains measurements from weather sensors:

```csharp
var sampleDocuments = new List<BsonDocument>
{
    new BsonDocument
    {

            "metadata", new BsonDocument
            {
                { "sensorId", 5578 },
                { "type", "omni" },
                { "location", new BsonDocument
                    {
                        { "type", "Point" },
                        { "coordinates", new BsonArray { -77.40711, 39.03335 } }
                    }
                }
            }
        }

        ,
        { "timestamp", new DateTime(2045, 1, 15, 0, 0, 0, DateTimeKind.Utc) } ,
        { "currentConditions", new BsonDocument
            {
                { "windDirection", 127.0 },
                { "tempF", 71.0 },
                { "windSpeed", 2.0 },
                { "cloudCover", BsonNull.Value },
                { "precip", 0.1 },
                { "humidity", 94.0 }
            }
        }
    },
    new BsonDocument
    {
        { "metadata", new BsonDocument
            {
                { "sensorId", 5578 },
                { "type", "omni" },
                { "location", new BsonDocument
                    {
                        { "type", "Point" },
                        { "coordinates", new BsonArray { -77.40711, 39.03335 } }
                    }
                }
            }
        },
        { "timestamp", new DateTime(2045, 1, 15, 0, 1, 0, DateTimeKind.Utc) },
        { "currentConditions", new BsonDocument
            {
                { "windDirection", 128.0 },
                { "tempF", 69.8 },
                { "windSpeed", 2.2 },
                { "cloudCover", BsonNull.Value },
                { "precip", 0.1 },
                { "humidity", 94.3 }
            }
        }
    },
    new BsonDocument
    {
        { "metadata", new BsonDocument
            {
                { "sensorId", 5579 },
                { "type", "omni" },
                { "location", new BsonDocument
                    {
                        { "type", "Point" },
                        { "coordinates", new BsonArray { -80.19773, 25.77481 } }
                    }
                }
            }
        },
        { "timestamp", new DateTime(2045, 1, 15, 0, 1, 0, DateTimeKind.Utc) },
        { "currentConditions", new BsonDocument
            {
                { "windDirection", 115.0 },
                { "tempF", 88.0 },
                { "windSpeed", 1.0 },
                { "cloudCover", BsonNull.Value },
                { "precip", 0.0 },
                { "humidity", 99.0 }
            }
        }
    }
};

```

Create a secondary single-field index on the `timestamp` field:

```csharp
await _collection?.Indexes.CreateOneAsync(new CreateIndexModel<BsonDocument>(
    Builders<BsonDocument>.IndexKeys.Ascending("timestamp")))!;

```

The following sort operation on the `timestamp` field uses the Secondary Index to improve performance:

```csharp
var matchStage = Builders<BsonDocument>.Filter.Gte("timestamp",
    new DateTime(2045, 1, 15, 0, 0, 0, DateTimeKind.Utc));

var pipeline = new EmptyPipelineDefinition<BsonDocument>()
    .Match(matchStage)
    .Sort(new BsonDocument("timestamp", 1));

var result = _collection?.Aggregate(pipeline).ToList();

```

To confirm that the sort operation used the Secondary Index, run the operation again with the `explain` option:

```csharp
var renderedPipeline = pipeline.Render(new RenderArgs<BsonDocument>(
    BsonDocumentSerializer.Instance, BsonSerializer.SerializerRegistry));

var explainCommand = new BsonDocument
{
    {
        "explain", new BsonDocument
        {
            { "aggregate", collectionName },
            { "pipeline", new BsonArray(renderedPipeline.Documents) },
            { "cursor", new BsonDocument() }
        }
    },
    { "verbosity", "executionStats" }
};

var explainResult = _database?.RunCommand<BsonDocument>(explainCommand);

```

### Last Point Queries on Time Series Collections

In time series data, a last point query returns the data point with the latest timestamp for a given field. For time series collections, a last point query fetches the latest measurement for each unique metadata value. For example, you may want to get the latest temperature reading from all sensors. Improve performance on last point queries by creating any of the following indexes:

```csharp
// Indexes on ``timeField`` descending are more performant because they 
// enable ``DISTINCT_SCAN`` optimizations.
var indexes = new List<CreateIndexModel<BsonDocument>>
{
    new CreateIndexModel<BsonDocument>(
        Builders<BsonDocument>.IndexKeys
            .Ascending("metadata.sensorId")
            .Ascending("timestamp")),
    new CreateIndexModel<BsonDocument>(
        Builders<BsonDocument>.IndexKeys
            .Ascending("metadata.sensorId")
            .Descending("timestamp")),
    new CreateIndexModel<BsonDocument>(
        Builders<BsonDocument>.IndexKeys
            .Descending("metadata.sensorId")
            .Ascending("timestamp")),
    new CreateIndexModel<BsonDocument>(
        Builders<BsonDocument>.IndexKeys
            .Descending("metadata.sensorId")
            .Descending("timestamp"))
};

```

**Note:**

Last point queries are most performant when they use the [DISTINCT\_SCAN optimization](/docs/manual/reference/explain-results#std-label-explain-results). This optimization is only available when an index on `timeField` is descending.

The following command creates a compound secondary index on `metaField` (ascending) and `timeField` (descending):

```csharp
_collection?.Indexes.CreateOne(
    new CreateIndexModel<BsonDocument>(
        Builders<BsonDocument>.IndexKeys
            .Ascending("metadata.type")
            .Descending("timestamp")));

```

The following last point query example uses the descending `timeField` compound secondary index created above:

```csharp
var pipeline = new EmptyPipelineDefinition<BsonDocument>()
    .Sort(new BsonDocument
    {
        { "metadata.sensorId", 1 },
        { "timestamp", -1 }
    })
    .Group(new BsonDocument
    {
        { "_id", "$metadata.sensorId" },
        { "ts", new BsonDocument("$first", "$timestamp") },
        { "temperatureF", new BsonDocument("$first", "$currentConditions.tempF") }
    });

var result = _collection?.Aggregate(pipeline).ToList();

```

To confirm that the last point query used the secondary index, run the operation again using `explain`:

```csharp
var renderedPipeline = pipeline.Render(new RenderArgs<BsonDocument>(
    BsonDocumentSerializer.Instance, BsonSerializer.SerializerRegistry));

var explainCommand = new BsonDocument
{
    {
        "explain", new BsonDocument
        {
            { "aggregate", collectionName },
            { "pipeline", new BsonArray(renderedPipeline.Documents) },
            { "cursor", new BsonDocument() }
        }
    },
    { "verbosity", "executionStats" }
};

var explainResult = _database?.RunCommand<BsonDocument>(explainCommand);

```

**Output:**

```text
{
  "explainVersion": "1",
  "stages": [
    {
      "$cursor": {
        "queryPlanner": {
          "namespace": "timeseries.system.buckets.sensorData",
          ...
          "winningPlan": {
            "isCached": false,
            "stage": "CLUSTERED_IXSCAN",
            ...
          },
        }
      }
    }
  ]
}
```

If the `queryPlanner.winningPlan.inputStage.stage` is either `CLUSTERED_IXSCAN` or `IXSCAN`, the index was used. For more information on the explain plan output, see [Explain Results.](/docs/manual/reference/explain-results#std-label-explain-results)

### Specify Index Hints for Time Series Collections

Index hints cause MongoDB to use a specific index for a query. Some operations on time series collections can only take advantage of an index if that index is specified in a hint.

For example, the following query causes MongoDB to use the index we just created:

```csharp
var hintOptions = new AggregateOptions
{
    Hint = new BsonDocument
    {
        { "metadata.sensorId", 1 },
        { "timestamp", -1 }
    }
};
var hintResult = _collection?.Aggregate(pipeline, hintOptions).ToList();

```

On a time series collection, you can specify hints using either the index name or the index key pattern. To get the names of the indexes on a collection, use the [`db.collection.getIndexes()`](/docs/manual/reference/method/db.collection.getIndexes#mongodb-method-db.collection.getIndexes) method.

### Create 2dsphere Indexes

Starting in version 6.0 you can create 2dsphere indexes on the `timeField`, `metaField`, or measurement fields. For example, the following operation creates a 2dsphere index on the `location` field:

```csharp
_collection?.Indexes.CreateOne(new CreateIndexModel<BsonDocument>(
    Builders<BsonDocument>.IndexKeys.Geo2DSphere("metadata.location")));

```

**Note:**

If there are [secondary indexes](/docs/manual/reference/glossary#std-term-secondary-index) on [time series collections](/docs/manual/core/timeseries-collections#std-label-manual-timeseries-collection) and you need to downgrade the feature compatibility version (FCV), you must first drop any secondary indexes that are incompatible with the downgraded FCV. For more information, see [`setFeatureCompatibilityVersion`.](/docs/manual/reference/command/setFeatureCompatibilityVersion#mongodb-dbcommand-dbcmd.setFeatureCompatibilityVersion)

## Use Secondary Indexes to Improve Sort Performance

Consider a weather data collection with the following configuration:

```java
CreateCollectionOptions createCollectionOptions = new CreateCollectionOptions()
        .timeSeriesOptions(
                new TimeSeriesOptions("timestamp")
                        .metaField("metadata"))
        .expireAfter(24, TimeUnit.HOURS);

```

In each weather data document, the `metadata` field value is a subdocument with fields for the weather sensor's ID, type, and location:

```java
.append("metadata", new Document()
        .append("sensorId", 5578)
        .append("type", "omni")
        .append("location", new Document()
                .append("type", "Point")
                .append("coordinates", Arrays.asList(-77.40711, 39.03335))))

```

The default compound index for the collection indexes the entire `metadata` subdocument, so the index is only used with [`$eq`](/docs/manual/reference/operator/aggregation/eq#mongodb-expression-exp.-eq) queries. By indexing specific `metadata` fields, you improve query performance for other query types.

For example, this [`$in`](/docs/manual/reference/operator/aggregation/in#mongodb-expression-exp.-in) query benefits from a secondary index on `metadata.type`:

```java
var filter = Filters.in("metadata.type", "temperature", "pressure");

```

Sort operations on time series collections can use secondary indexes on the `timeField` field. Under certain conditions, sort operations can also use compound secondary indexes on the `metaField` and `timeField` fields.

The aggregation pipeline uses the [`$match`](/docs/manual/reference/operator/aggregation/match#mongodb-pipeline-pipe.-match) and [`$sort`](/docs/manual/reference/operator/aggregation/sort#mongodb-pipeline-pipe.-sort) stages to determine which indexes a time series collection can use. An index can be used in the following scenarios:

- A sort on `{ <timeField>: ±1 }` uses a secondary index on `<timeField>`.

- A sort on `{ <metaField>: ±1, timeField: ±1 }` uses the default compound index on `{ <metaField>: ±1, timeField: ±1 }`.

- A sort on `{ <timeField>: ±1 }` uses a secondary index on `{ metaField: ±1, timeField: ±1 }` when there is a point predicate on `<metaField>`.

For example, the following `sensorData` collection contains measurements from weather sensors:

```java
List<Document> sampleDocuments = Arrays.asList(
        new Document()
                .append("metadata", new Document()
                        .append("sensorId", 5578)
                        .append("type", "omni")
                        .append("location", new Document()
                                .append("type", "Point")
                                .append("coordinates", Arrays.asList(-77.40711, 39.03335))))
                .append("timestamp", Date.from(Instant.parse("2022-01-15T00:00:00Z")))
                .append("currentConditions", new Document()
                        .append("windDirection", 127.0)
                        .append("tempF", 71.0)
                        .append("windSpeed", 2.0)
                        .append("cloudCover", null)
                        .append("precip", 0.1)
                        .append("humidity", 94.0)),
        new Document()
                .append("metadata", new Document()
                        .append("sensorId", 5578)
                        .append("type", "omni")
                        .append("location", new Document()
                                .append("type", "Point")
                                .append("coordinates", Arrays.asList(-77.40711, 39.03335))))
                .append("timestamp", Date.from(Instant.parse("2022-01-15T00:01:00Z")))
                .append("currentConditions", new Document()
                        .append("windDirection", 128.0)
                        .append("tempF", 69.8)
                        .append("windSpeed", 2.2)
                        .append("cloudCover", null)
                        .append("precip", 0.1)
                        .append("humidity", 94.3)),
        new Document()
                .append("metadata", new Document()
                        .append("sensorId", 5579)
                        .append("type", "omni")
                        .append("location", new Document()
                                .append("type", "Point")
                                .append("coordinates", Arrays.asList(-80.19773, 25.77481))))
                .append("timestamp", Date.from(Instant.parse("2022-01-15T00:01:00Z")))
                .append("currentConditions", new Document()
                        .append("windDirection", 115.0)
                        .append("tempF", 88.0)
                        .append("windSpeed", 1.0)
                        .append("cloudCover", null)
                        .append("precip", 0.0)
                        .append("humidity", 99.0))
);

```

Create a secondary single-field index on the `timestamp` field:

```java
collection.createIndex(Indexes.ascending("timestamp"));

```

The following sort operation on the `timestamp` field uses the Secondary Index to improve performance:

```java
var matchFilter = Filters.gte("timestamp",
        Date.from(Instant.parse("2022-01-15T00:00:00Z")));

var pipeline = Arrays.asList(
        new Document("$match", new Document("timestamp",
                new Document("$gte", Date.from(Instant.parse("2022-01-15T00:00:00Z"))))),
        new Document("$sort", new Document("timestamp", 1))
);

List<Document> result = collection.aggregate(pipeline).into(new ArrayList<>());

```

To confirm that the sort operation used the Secondary Index, run the operation again with the `explain` option:

```java
var explainCommand = new Document("explain", new Document()
        .append("aggregate", collectionName)
        .append("pipeline", pipeline)
        .append("cursor", new Document()))
        .append("verbosity", "executionStats");

Document explainResult = database.runCommand(explainCommand);

```

### Last Point Queries on Time Series Collections

In time series data, a last point query returns the data point with the latest timestamp for a given field. For time series collections, a last point query fetches the latest measurement for each unique metadata value. For example, you may want to get the latest temperature reading from all sensors. Improve performance on last point queries by creating any of the following indexes:

```java
// Indexes on ``timeField`` descending are more performant because they
// enable ``DISTINCT_SCAN`` optimizations.
List<String> indexes = Arrays.asList(
        collection.createIndex(Indexes.compoundIndex(
                Indexes.ascending("metadata.sensorId"),
                Indexes.ascending("timestamp"))),
        collection.createIndex(Indexes.compoundIndex(
                Indexes.ascending("metadata.sensorId"),
                Indexes.descending("timestamp"))),
        collection.createIndex(Indexes.compoundIndex(
                Indexes.descending("metadata.sensorId"),
                Indexes.ascending("timestamp"))),
        collection.createIndex(Indexes.compoundIndex(
                Indexes.descending("metadata.sensorId"),
                Indexes.descending("timestamp")))
);

```

**Note:**

Last point queries are most performant when they use the [DISTINCT\_SCAN optimization](/docs/manual/reference/explain-results#std-label-explain-results). This optimization is only available when an index on `timeField` is descending.

The following command creates a compound secondary index on `metaField` (ascending) and `timeField` (descending):

```java
collection.createIndex(Indexes.compoundIndex(
        Indexes.ascending("metadata.type"),
        Indexes.descending("timestamp")));

```

The following last point query example uses the descending `timeField` compound secondary index created above:

```java
var pipeline = Arrays.asList(
        new Document("$sort", new Document()
                .append("metadata.sensorId", 1)
                .append("timestamp", -1)),
        new Document("$group", new Document()
                .append("_id", "$metadata.sensorId")
                .append("ts", new Document("$first", "$timestamp"))
                .append("temperatureF", new Document("$first", "$currentConditions.tempF")))
);

List<Document> result = collection.aggregate(pipeline).into(new ArrayList<>());

```

To confirm that the last point query used the secondary index, run the operation again using `explain`:

```java
var explainCommand = new Document("explain", new Document()
        .append("aggregate", collectionName)
        .append("pipeline", pipeline)
        .append("cursor", new Document()))
        .append("verbosity", "executionStats");

Document explainResult = database.runCommand(explainCommand);

```

**Output:**

```text
{
  "explainVersion": "1",
  "stages": [
    {
      "$cursor": {
        "queryPlanner": {
          "namespace": "timeseries.system.buckets.sensorData",
          ...
          "winningPlan": {
            "isCached": false,
            "stage": "CLUSTERED_IXSCAN",
            ...
          },
        }
      }
    }
  ]
}

```

If the `queryPlanner.winningPlan.inputStage.stage` is either `CLUSTERED_IXSCAN` or `IXSCAN`, the index was used. For more information on the explain plan output, see [Explain Results.](/docs/manual/reference/explain-results#std-label-explain-results)

### Specify Index Hints for Time Series Collections

Index hints cause MongoDB to use a specific index for a query. Some operations on time series collections can only take advantage of an index if that index is specified in a hint.

For example, the following query causes MongoDB to use the index we just created:

```java
var hintPipeline = Arrays.asList(
        new Document("$sort", new Document()
                .append("metadata.sensorId", 1)
                .append("timestamp", -1)),
        new Document("$group", new Document()
                .append("_id", "$metadata.sensorId")
                .append("ts", new Document("$first", "$timestamp"))
                .append("temperatureF", new Document("$first", "$currentConditions.tempF")))
);

List<Document> hintResult = collection.aggregate(hintPipeline)
        .hint(new Document()
                .append("metadata.sensorId", 1)
                .append("timestamp", -1))
        .into(new ArrayList<>());

```

On a time series collection, you can specify hints using either the index name or the index key pattern. To get the names of the indexes on a collection, use the [`db.collection.getIndexes()`](/docs/manual/reference/method/db.collection.getIndexes#mongodb-method-db.collection.getIndexes) method.

### Create 2dsphere Indexes

Starting in version 6.0 you can create 2dsphere indexes on the `timeField`, `metaField`, or measurement fields. For example, the following operation creates a 2dsphere index on the `location` field:

```java
collection.createIndex(Indexes.geo2dsphere("metadata.location"));

```

**Note:**

If there are [secondary indexes](/docs/manual/reference/glossary#std-term-secondary-index) on [time series collections](/docs/manual/core/timeseries-collections#std-label-manual-timeseries-collection) and you need to downgrade the feature compatibility version (FCV), you must first drop any secondary indexes that are incompatible with the downgraded FCV. For more information, see [`setFeatureCompatibilityVersion`.](/docs/manual/reference/command/setFeatureCompatibilityVersion#mongodb-dbcommand-dbcmd.setFeatureCompatibilityVersion)

You may wish to create additional secondary indexes. Consider a weather data collection with the configuration:

```javascript
db.createCollection(
"weather",
{
   timeseries: {
      timeField: "timestamp",
      metaField: "metadata"
}})
```

In each weather data document, the `metadata` field value is a subdocument with fields for the weather sensor ID and type:

```javascript
{
    "timestamp": ISODate("2021-05-18T00:00:00.000Z"),
    "metadata": {
    "sensorId": 5578,
    "type": "temperature"
    },
    "temp": 12
}
```

The default compound index for the collection indexes the entire `metadata` subdocument, so the index is only used with [`$eq`](/docs/manual/reference/operator/aggregation/eq#mongodb-expression-exp.-eq) queries. By indexing specific `metadata` fields, you improve query performance for other query types.

For example, this [`$in`](/docs/manual/reference/operator/aggregation/in#mongodb-expression-exp.-in) query benefits from a secondary index on `metadata.type`:

```javascript
{ metadata.type:{ $in: ["temperature", "pressure"] }}
```

## Use Secondary Indexes to Improve Sort Performance

Sort operations on time series collections can use secondary indexes on the `timeField` field. Under certain conditions, sort operations can also use compound secondary indexes on the `metaField` and `timeField` fields.

The aggregation pipeline stages [`$match`](/docs/manual/reference/operator/aggregation/match#mongodb-pipeline-pipe.-match) and [`$sort`](/docs/manual/reference/operator/aggregation/sort#mongodb-pipeline-pipe.-sort) determine which indexes a time series collection can use. An index can be used in the following scenarios:

- Sort on `{ <timeField>: ±1 }` uses a secondary index on

  `<timeField>`

- Sort on `{ <metaField>: ±1, timeField: ±1 }` uses the default

  compound index on `{ <metaField>: ±1, timeField: ±1 }`

- Sort on `{ <timeField>: ±1 }` uses a secondary index on

  `{ metaField: ±1, timeField: ±1 }` when there is a point predicate on `<metaField>`

For example, the following `sensorData` collection contains measurements from weather sensors:

```javascript
db.sensorData.insertMany( [ {
    "metadata": {
        "sensorId": 5578,
        "type": "omni",
        "location": {
            type: "Point",
            coordinates: [-77.40711, 39.03335]
        }
    },
    "timestamp": ISODate("2022-01-15T00:00:00.000Z"),
    "currentConditions": {
        "windDirection": 127.0,
        "tempF": 71.0,
        "windSpeed": 2.0,
        "cloudCover": null,
        "precip": 0.1,
        "humidity": 94.0,
    }
    },
    {
    "metadata": {
        "sensorId": 5578,
        "type": "omni",
        "location": {
            type: "Point",
            coordinates: [-77.40711, 39.03335]
        }
    },
    "timestamp": ISODate("2022-01-15T00:01:00.000Z"),
    "currentConditions": {
        "windDirection": 128.0,
        "tempF": 69.8,
        "windSpeed": 2.2,
        "cloudCover": null,
        "precip": 0.1,
        "humidity": 94.3,
    }
    },
    {
    "metadata": {
        "sensorId": 5579,
        "type": "omni",
        "location": {
            type: "Point",
            coordinates: [-80.19773, 25.77481]
        }
    },
    "timestamp": ISODate("2022-01-15T00:01:00.000Z"),
    "currentConditions": {
        "windDirection": 115.0,
        "tempF": 88.0,
        "windSpeed": 1.0,
        "cloudCover": null,
        "precip": 0.0,
        "humidity": 99.0,
    }
    }
]
)
```

Create a secondary single-field index on the `timestamp` field:

```javascript
db.sensorData.createIndex( { "timestamp": 1 } )
```

The following sort operation on the `timestamp` field uses the Secondary Index to improve performance:

```javascript
db.sensorData.aggregate( [
    { $match: { "timestamp" : { $gte: ISODate("2022-01-15T00:00:00.000Z") } } },
    { $sort: { "timestamp": 1 } }
] )
```

To confirm that the sort operation used the Secondary Index, run the operation again with the `.explain( "executionStats" )` option:

```javascript
db.sensorData.explain( "executionStats" ).aggregate( [
    { $match: { "timestamp": { $gte: ISODate("2022-01-15T00:00:00.000Z") } } },
    { $sort: { "timestamp": 1 } }
] )
```

### Last Point Queries on Time Series Collections

In time series data, a last point query returns the data point with the latest timestamp for a given field. For time series collections, a last point query fetches the latest measurement for each unique metadata value. For example, you may want to get the latest temperature reading from all sensors. Improve performance on last point queries by creating any of the following indexes:

```javascript
{ "metadata.sensorId": 1,  "timestamp": 1 }
{ "metadata.sensorId": 1,  "timestamp": -1 }
{ "metadata.sensorId": -1, "timestamp": 1 }
{ "metadata.sensorId": -1, "timestamp": -1 }
```

**Note:**

Last point queries are most performant when they use the [DISTINCT\_SCAN optimization](/docs/manual/reference/explain-results#std-label-explain-results). This optimization is only available when an index on `timeField` is descending.

The following command creates a compound secondary index on `metaField` (ascending) and `timeField` (descending):

```javascript
db.sensorData.createIndex( { "metadata.sensorId": 1,  "timestamp": -1 } )
```

The following last point query example uses the descending `timeField` compound secondary index created above:

```javascript
db.sensorData.aggregate( [
    {
        $sort: { "metadata.sensorId": 1, "timestamp": -1 }
    },
    {
        $group: {
            _id: "$metadata.sensorId",
            ts: { $first: "$timestamp" },
            temperatureF: { $first: "$currentConditions.tempF" }
        }
    }
] )
```

To confirm that the last point query used the secondary index, run the operation again using `.explain( "executionStats" )`:

```javascript
db.getCollection( 'sensorData' ).explain( "executionStats" ).aggregate( [
    {
        $sort: { "metadata.sensorId": 1, "timestamp": -1 }
    },
    {
        $group: {
            _id: "$metadata.sensorId",
            ts: { $first: "$timestamp" },
            temperatureF: { $first: "$currentConditions.tempF" }
        }
    }
] )
```

The `winningPlan.queryPlan.inputStage.stage` is `DISTINCT_SCAN`, which indicates that the index was used. For more information on the explain plan output, see [Explain Results.](/docs/manual/reference/explain-results#std-label-explain-results)

### Specify Index Hints for Time Series Collections

Index hints cause MongoDB to use a specific index for a query. Some operations on time series collections can only take advantage of an index if that index is specified in a hint.

For example, the following query causes MongoDB to use the `timestamp_1_metadata.sensorId_1` index:

```javascript
db.sensorData.find( { "metadata.sensorId": 5578 } ).hint( "timestamp_1_metadata.sensorId_1" )
```

On a time series collection, you can specify hints using either the index name or the index key pattern. To get the names of the indexes on a collection, use `GetIndexes()`.

### Create 2dsphere Indexes

Starting in version 6.0 you can create `2dsphere` indexes. For example, the following operation creates a 2dsphere index on the `location` field:

**Example:**

```javascript
db.sensorData.createIndex({ "metadata.location": "2dsphere" })
```

**Note:**

If there are [secondary indexes](/docs/manual/reference/glossary#std-term-secondary-index) on [time series collections](/docs/manual/core/timeseries-collections#std-label-manual-timeseries-collection) and you need to downgrade the feature compatibility version (FCV), you must first drop any secondary indexes that are incompatible with the downgraded FCV. For more information, see [`setFeatureCompatibilityVersion`.](/docs/manual/reference/command/setFeatureCompatibilityVersion#mongodb-dbcommand-dbcmd.setFeatureCompatibilityVersion)

## Use Secondary Indexes to Improve Sort Performance

Consider a weather data collection with the following configuration:

```javascript
const createCollectionOptions = {
  timeseries: {
    timeField: 'timestamp',
    metaField: 'metadata',
  },
  expireAfterSeconds: 86400,
};

```

In each weather data document, the `metadata` field value is a subdocument with fields for the weather sensor's ID, type, and location:

```javascript
metadata: {
  sensorId: 5578,
  type: 'omni',
  location: {
    type: 'Point',
    coordinates: [-77.40711, 39.03335],
  },
},

```

The default compound index for the collection indexes the entire `metadata` subdocument, so the index is only used with [`$eq`](/docs/manual/reference/operator/aggregation/eq#mongodb-expression-exp.-eq) queries. By indexing specific `metadata` fields, you improve query performance for other query types.

For example, this [`$in`](/docs/manual/reference/operator/aggregation/in#mongodb-expression-exp.-in) query benefits from a secondary index on `metadata.type`:

```javascript
const filter = { 'metadata.type': { $in: ['temperature', 'pressure'] } };

```

Sort operations on time series collections can use secondary indexes on the `timeField` field. Under certain conditions, sort operations can also use compound secondary indexes on the `metaField` and `timeField` fields.

The aggregation pipeline uses the [`$match`](/docs/manual/reference/operator/aggregation/match#mongodb-pipeline-pipe.-match) and [`$sort`](/docs/manual/reference/operator/aggregation/sort#mongodb-pipeline-pipe.-sort) stages to determine which indexes a time series collection can use. An index can be used in the following scenarios:

- A sort on `{ <timeField>: ±1 }` uses a secondary index on `<timeField>`.

- A sort on `{ <metaField>: ±1, timeField: ±1 }` uses the default compound index on `{ <metaField>: ±1, timeField: ±1 }`.

- A sort on `{ <timeField>: ±1 }` uses a secondary index on `{ metaField: ±1, timeField: ±1 }` when there is a point predicate on `<metaField>`.

For example, the following `sensorData` collection contains measurements from weather sensors:

```javascript
const sampleDocuments = [
  {
    metadata: {
      sensorId: 5578,
      type: 'omni',
      location: {
        type: 'Point',
        coordinates: [-77.40711, 39.03335],
      },
    },
    timestamp: new Date('2022-01-15T00:00:00.000Z'),
    currentConditions: {
      windDirection: 127.0,
      tempF: 71.0,
      windSpeed: 2.0,
      cloudCover: null,
      precip: 0.1,
      humidity: 94.0,
    },
  },
  {
    metadata: {
      sensorId: 5578,
      type: 'omni',
      location: {
        type: 'Point',
        coordinates: [-77.40711, 39.03335],
      },
    },
    timestamp: new Date('2022-01-15T00:01:00.000Z'),
    currentConditions: {
      windDirection: 128.0,
      tempF: 69.8,
      windSpeed: 2.2,
      cloudCover: null,
      precip: 0.1,
      humidity: 94.3,
    },
  },
  {
    metadata: {
      sensorId: 5579,
      type: 'omni',
      location: {
        type: 'Point',
        coordinates: [-80.19773, 25.77481],
      },
    },
    timestamp: new Date('2022-01-15T00:01:00.000Z'),
    currentConditions: {
      windDirection: 115.0,
      tempF: 88.0,
      windSpeed: 1.0,
      cloudCover: null,
      precip: 0.0,
      humidity: 99.0,
    },
  },
];

```

Create a secondary single-field index on the `timestamp` field:

```javascript
await collection.createIndex({ timestamp: 1 });

```

The following sort operation on the `timestamp` field uses the Secondary Index to improve performance:

```javascript
const matchStage = {
  $match: { timestamp: { $gte: new Date('2022-01-15T00:00:00.000Z') } },
};
const sortStage = { $sort: { timestamp: 1 } };

const pipeline = [matchStage, sortStage];

const result = await collection.aggregate(pipeline).toArray();

```

To confirm that the sort operation used the Secondary Index, run the operation again with the `explain` option:

```javascript
const explainResult = await database.command({
  explain: {
    aggregate: collectionName,
    pipeline: pipeline,
    cursor: {},
  },
  verbosity: 'executionStats',
});

```

### Last Point Queries on Time Series Collections

In time series data, a last point query returns the data point with the latest timestamp for a given field. For time series collections, a last point query fetches the latest measurement for each unique metadata value. For example, you may want to get the latest temperature reading from all sensors. Improve performance on last point queries by creating any of the following indexes:

```javascript
// Indexes on ``timeField`` descending are more performant because they
// enable ``DISTINCT_SCAN`` optimizations.
const indexes = [
  { key: { 'metadata.sensorId': 1, timestamp: 1 } },
  { key: { 'metadata.sensorId': 1, timestamp: -1 } },
  { key: { 'metadata.sensorId': -1, timestamp: 1 } },
  { key: { 'metadata.sensorId': -1, timestamp: -1 } },
];

```

**Note:**

Last point queries are most performant when they use the [DISTINCT\_SCAN optimization](/docs/manual/reference/explain-results#std-label-explain-results). This optimization is only available when an index on `timeField` is descending.

The following command creates a compound secondary index on `metaField` (ascending) and `timeField` (descending):

```javascript
await collection.createIndex({ 'metadata.type': 1, timestamp: -1 });

```

The following last point query example uses the descending `timeField` compound secondary index created above:

```javascript
const pipeline = [
  { $sort: { 'metadata.sensorId': 1, timestamp: -1 } },
  {
    $group: {
      _id: '$metadata.sensorId',
      ts: { $first: '$timestamp' },
      temperatureF: { $first: '$currentConditions.tempF' },
    },
  },
];

const result = await collection.aggregate(pipeline).toArray();

```

To confirm that the last point query used the secondary index, run the operation again using `explain`:

```javascript
const explainResult = await database.command({
  explain: {
    aggregate: collectionName,
    pipeline: pipeline,
    cursor: {},
  },
  verbosity: 'executionStats',
});

```

**Output:**

```text
{
  "explainVersion": "1",
  "stages": [
    {
      "$cursor": {
        "queryPlanner": {
          "namespace": "timeseries.system.buckets.sensorData",
          ...
          "winningPlan": {
            "isCached": false,
            "stage": "CLUSTERED_IXSCAN",
            ...
          },
        }
      }
    }
  ]
}


```

If the `queryPlanner.winningPlan.inputStage.stage` is either `CLUSTERED_IXSCAN` or `IXSCAN`, the index was used. For more information on the explain plan output, see [Explain Results.](/docs/manual/reference/explain-results#std-label-explain-results)

### Specify Index Hints for Time Series Collections

Index hints cause MongoDB to use a specific index for a query. Some operations on time series collections can only take advantage of an index if that index is specified in a hint.

For example, the following query causes MongoDB to use the index we just created:

```javascript
const hintPipeline = [
  { $sort: { 'metadata.sensorId': 1, timestamp: -1 } },
  {
    $group: {
      _id: '$metadata.sensorId',
      ts: { $first: '$timestamp' },
      temperatureF: { $first: '$currentConditions.tempF' },
    },
  },
];

const hintResult = await collection
  .aggregate(hintPipeline, {
    hint: { 'metadata.sensorId': 1, timestamp: -1 },
  })
  .toArray();

```

On a time series collection, you can specify hints using either the index name or the index key pattern. To get the names of the indexes on a collection, use the [`db.collection.getIndexes()`](/docs/manual/reference/method/db.collection.getIndexes#mongodb-method-db.collection.getIndexes) method.

### Create 2dsphere Indexes

Starting in version 6.0 you can create 2dsphere indexes on the `timeField`, `metaField`, or measurement fields. For example, the following operation creates a 2dsphere index on the `location` field:

```javascript
await collection.createIndex({ 'metadata.location': '2dsphere' });

```

**Note:**

If there are [secondary indexes](/docs/manual/reference/glossary#std-term-secondary-index) on [time series collections](/docs/manual/core/timeseries-collections#std-label-manual-timeseries-collection) and you need to downgrade the feature compatibility version (FCV), you must first drop any secondary indexes that are incompatible with the downgraded FCV. For more information, see [`setFeatureCompatibilityVersion`.](/docs/manual/reference/command/setFeatureCompatibilityVersion#mongodb-dbcommand-dbcmd.setFeatureCompatibilityVersion)

## Use Secondary Indexes to Improve Sort Performance

Consider a weather data collection with the following configuration:

```python
database.create_collection(
    sensorData,
    timeseries={
        "timeField": "timestamp",
        "metaField": "metadata",
    },
    expireAfterSeconds=86400  # 24 hours
)

```

In each weather data document, the `metadata` field value is a subdocument with fields for the weather sensor's ID, type, and location:

```python
"metadata": {
    "sensorId": 5578,
    "type": "omni",
    "location": {
        "type": "Point",
        "coordinates": [-77.40711, 39.03335]
    }
},

```

The default compound index for the collection indexes the entire `metadata` subdocument, so the index is only used with [`$eq`](/docs/manual/reference/operator/aggregation/eq#mongodb-expression-exp.-eq) queries. By indexing specific `metadata` fields, you improve query performance for other query types.

For example, this [`$in`](/docs/manual/reference/operator/aggregation/in#mongodb-expression-exp.-in) query benefits from a secondary index on `metadata.type`:

```python
filter_query = {"metadata.type": {"$in": ["temperature", "pressure"]}}

```

Sort operations on time series collections can use secondary indexes on the `timeField` field. Under certain conditions, sort operations can also use compound secondary indexes on the `metaField` and `timeField` fields.

The aggregation pipeline uses the [`$match`](/docs/manual/reference/operator/aggregation/match#mongodb-pipeline-pipe.-match) and [`$sort`](/docs/manual/reference/operator/aggregation/sort#mongodb-pipeline-pipe.-sort) stages to determine which indexes a time series collection can use. An index can be used in the following scenarios:

- A sort on `{ <timeField>: ±1 }` uses a secondary index on `<timeField>`.

- A sort on `{ <metaField>: ±1, timeField: ±1 }` uses the default compound index on `{ <metaField>: ±1, timeField: ±1 }`.

- A sort on `{ <timeField>: ±1 }` uses a secondary index on `{ metaField: ±1, timeField: ±1 }` when there is a point predicate on `<metaField>`.

For example, the following `sensorData` collection contains measurements from weather sensors:

```python
sample_documents = [
    {
        "metadata": {
            "sensorId": 5578,
            "type": "omni",
            "location": {
                "type": "Point",
                "coordinates": [-77.40711, 39.03335]
            }
        },
        "timestamp": datetime(2022, 1, 15, 0, 0, 0, tzinfo=timezone.utc),
        "currentConditions": {
            "windDirection": 127.0,
            "tempF": 71.0,
            "windSpeed": 2.0,
            "cloudCover": None,
            "precip": 0.1,
            "humidity": 94.0
        }
    },
    {
        "metadata": {
            "sensorId": 5578,
            "type": "omni",
            "location": {
                "type": "Point",
                "coordinates": [-77.40711, 39.03335]
            }
        },
        "timestamp": datetime(2022, 1, 15, 0, 1, 0, tzinfo=timezone.utc),
        "currentConditions": {
            "windDirection": 128.0,
            "tempF": 69.8,
            "windSpeed": 2.2,
            "cloudCover": None,
            "precip": 0.1,
            "humidity": 94.3
        }
    },
    {
        "metadata": {
            "sensorId": 5579,
            "type": "omni",
            "location": {
                "type": "Point",
                "coordinates": [-80.19773, 25.77481]
            }
        },
        "timestamp": datetime(2022, 1, 15, 0, 1, 0, tzinfo=timezone.utc),
        "currentConditions": {
            "windDirection": 115.0,
            "tempF": 88.0,
            "windSpeed": 1.0,
            "cloudCover": None,
            "precip": 0.0,
            "humidity": 99.0
        }
    }
]

```

Create a secondary single-field index on the `timestamp` field:

```python
collection.create_index([("timestamp", ASCENDING)])

```

The following sort operation on the `timestamp` field uses the Secondary Index to improve performance:

```python
match_stage = {"$match": {"timestamp": {"$gte": datetime(2022, 1, 15, 0, 0, 0, tzinfo=timezone.utc)}}}
sort_stage = {"$sort": {"timestamp": 1}}

pipeline = [match_stage, sort_stage]

result = list(collection.aggregate(pipeline))

```

To confirm that the sort operation used the Secondary Index, run the operation again with the `explain` option:

```python
explain_result = database.command(
    "explain",
    {
        "aggregate": sensorData,
        "pipeline": pipeline,
        "cursor": {}
    },
    verbosity="executionStats"
)

```

### Last Point Queries on Time Series Collections

In time series data, a last point query returns the data point with the latest timestamp for a given field. For time series collections, a last point query fetches the latest measurement for each unique metadata value. For example, you may want to get the latest temperature reading from all sensors. Improve performance on last point queries by creating any of the following indexes:

```python
# Indexes on ``timeField`` descending are more performant because they 
# enable ``DISTINCT_SCAN`` optimizations.
indexes = [
    [("metadata.sensorId", ASCENDING), ("timestamp", ASCENDING)],
    [("metadata.sensorId", ASCENDING), ("timestamp", DESCENDING)],
    [("metadata.sensorId", DESCENDING), ("timestamp", ASCENDING)],
    [("metadata.sensorId", DESCENDING), ("timestamp", DESCENDING)],
]

```

**Note:**

Last point queries are most performant when they use the [DISTINCT\_SCAN optimization](/docs/manual/reference/explain-results#std-label-explain-results). This optimization is only available when an index on `timeField` is descending.

The following command creates a compound secondary index on `metaField` (ascending) and `timeField` (descending):

```python
collection.create_index([("metadata.type", ASCENDING), ("timestamp", DESCENDING)])

```

The following last point query example uses the descending `timeField` compound secondary index created above:

```python
pipeline = [
    {"$sort": {"metadata.sensorId": 1, "timestamp": -1}},
    {"$group": {
        "_id": "$metadata.sensorId",
        "ts": {"$first": "$timestamp"},
        "temperatureF": {"$first": "$currentConditions.tempF"}
    }}
]

result = list(collection.aggregate(pipeline))

```

To confirm that the last point query used the secondary index, run the operation again using `explain`:

```python
explain_result = database.command(
    "explain",
    {
        "aggregate": sensorData,
        "pipeline": pipeline,
        "cursor": {}
    },
    verbosity="executionStats"
)

```

**Output:**

```text
{
  "explainVersion": "1",
  "stages": [
    {
      "$cursor": {
        ...,
        "queryPlanner": {
          "namespace": "timeseries.system.buckets.sensorData",
          ...,
          "winningPlan": {
            "isCached": false,
            "stage": "CLUSTERED_IXSCAN"
          }
        }
      }
    }
  ]
}

```

If the `queryPlanner.winningPlan.inputStage.stage` is either `CLUSTERED_IXSCAN` or `IXSCAN`, the index was used. For more information on the explain plan output, see [Explain Results.](/docs/manual/reference/explain-results#std-label-explain-results)

### Specify Index Hints for Time Series Collections

Index hints cause MongoDB to use a specific index for a query. Some operations on time series collections can only take advantage of an index if that index is specified in a hint.

For example, the following query causes MongoDB to use the index we just created:

```python
hint_result = list(collection.aggregate(
    pipeline,
    hint={"metadata.sensorId": 1, "timestamp": -1}
))

```

On a time series collection, you can specify hints using either the index name or the index key pattern. To get the names of the indexes on a collection, use the [`db.collection.getIndexes()`](/docs/manual/reference/method/db.collection.getIndexes#mongodb-method-db.collection.getIndexes) method.

### Create 2dsphere Indexes

Starting in version 6.0, you can create 2dsphere indexes on the `timeField`, `metaField`, or measurement fields. For example, the following operation creates a 2dsphere index on the `location` field:

```python
collection.create_index([("metadata.location", GEOSPHERE)])

```

**Note:**

If there are [secondary indexes](/docs/manual/reference/glossary#std-term-secondary-index) on [time series collections](/docs/manual/core/timeseries-collections#std-label-manual-timeseries-collection) and you need to downgrade the feature compatibility version (FCV), you must first drop any secondary indexes that are incompatible with the downgraded FCV. For more information, see [`setFeatureCompatibilityVersion`.](/docs/manual/reference/command/setFeatureCompatibilityVersion#mongodb-dbcommand-dbcmd.setFeatureCompatibilityVersion)
