> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Best Practices for Time Series Collections

This page describes best practices to improve performance and data usage for time series collections.

## Compression Best Practices

To optimize data compression for time series collections, perform the following actions:

### Omit Fields Containing Empty Objects and Arrays from Documents

If your data contains empty objects, arrays, or strings, omit the empty fields from your documents to optimize compression.

For example, consider the following documents:

```javascript
{
   timestamp: ISODate("2020-01-23T00:00:00.441Z"),
   coordinates: [1.0, 2.0]
},
{
   timestamp: ISODate("2020-01-23T00:00:10.441Z"),
   coordinates: []
},
{
   timestamp: ISODate("2020-01-23T00:00:20.441Z"),
   coordinates: [3.0, 5.0]
}
```

`coordinates` fields with populated values and `coordinates` fields with an empty array result in a schema change for the compressor. The schema change causes the second and third documents in the sequence to remain uncompressed.

Optimize compression by omitting the fields with empty values, as shown in the following documents:

```javascript
{
   timestamp: ISODate("2020-01-23T00:00:00.441Z"),
   coordinates: [1.0, 2.0]
},
{
   timestamp: ISODate("2020-01-23T00:00:10.441Z")
},
{
   timestamp: ISODate("2020-01-23T00:00:20.441Z"),
   coordinates: [3.0, 5.0]
}
```

### Round Numeric Data to Few Decimal Places

Round numeric data to the precision that your application requires. Rounding numeric data to fewer decimal places improves the compression ratio.

### Use Standard Embedded Fields Best Practices

If an [embedded data model](/docs/manual/data-modeling/embedding#std-label-data-modeling-embedding) supports your application's needs, use nested fields. The behavior of nested fields does not differ between regular collections and time series collections.

For example, consider a time series collection that contains weather documents similar to the following example:

```javascript
{
   timestamp: ISODate("2024-06-17T10:00:00Z"),
   stationId: "ALPHA123",
   atmosphere: {
      temperature: 21.5,
      humidity: 68,
      pressure: 1013.25
   },
   wind: {
      speed: 7.2,
      direction: "NW"
   },
   precipitation: 0.5,
   visibility: 10
}
```

MongoDB uses column compression on each nested field individually, which provides the same compression quality as flattening the fields to the top level. The resulting compression is identical to the compression that would result from flattening all of the nested fields to top level fields.

**Important:**

Column compression requires a consistent nested field order. However, if you use a driver to interact with your data, there may be additional ordering considerations. For example, see [BSON Types](https://www.mongodb.com/docs/drivers/go/current/data-formats/bson/) for ordered representation considerations for the Go driver. Refer to [driver documentation](https://www.mongodb.com/docs/drivers/) for more information.

If your workload has high cardinality, flattening nested objects may improve performance. For example, the following document contains the same data as the previous document but in a flattened format:

```javascript
{
   timestamp: ISODate("2024-06-17T10:00:00Z"),
   stationId: "ALPHA123",
   atmosphere_temperature: 21.5,
   atmosphere_humidity: 68,
   atmosphere_pressure: 1013.25
   wind_speed: 7.2,
   wind_direction: "NW"
   precipitation: 0.5,
   visibility: 10
}
```

**Note:**

Use a data model that is most natural for your application. MongoDB only recommends flattening documents if a nested structure causes significant performance issues.

## Inserts Best Practices

To optimize insert performance for time series collections, perform the following actions:

### Batch Document Writes

When inserting multiple documents:

- To avoid network roundtrips, use a single [`insertMany()`](/docs/manual/reference/method/db.collection.insertMany#mongodb-method-db.collection.insertMany) statement as opposed to multiple [`insertOne()`](/docs/manual/reference/method/db.collection.insertOne#mongodb-method-db.collection.insertOne) statements.

- If possible, insert data that contains identical `metaField` values in the same batches.

- Set the `ordered` parameter to `false`.

For example, if you have two sensors that correspond to two `metaField` values, `sensor A` and `sensor B`, a batch that contains multiple measurements from a single sensor incurs the cost of one insert, rather than one insert per measurement.

The following operation inserts six documents, but only incurs the cost of two inserts (one per `metaField` value), because the documents are ordered by sensor. The `ordered` parameter is set to `false` to improve performance:

```javascript
db.temperatures.insertMany(
   [
      {
         metaField: {
            sensor: "sensorA"
         },
         timestamp: ISODate("2021-05-18T00:00:00.000Z"),
         temperature: 10
      },
      {
         metaField: {
            sensor: "sensorA"
         },
         timestamp: ISODate("2021-05-19T00:00:00.000Z"),
         temperature: 12
      },
      {
         metaField: {
            sensor: "sensorA"
         },
         timestamp: ISODate("2021-05-20T00:00:00.000Z"),
         temperature: 13
      },
      {
         metaField: {
            sensor: "sensorB"
         },
         timestamp: ISODate("2021-05-18T00:00:00.000Z"),
         temperature: 20
      },
      {
         metaField: {
            sensor: "sensorB"
         },
         timestamp: ISODate("2021-05-19T00:00:00.000Z"),
         temperature: 25
      },
      {
         metadField: {
            sensor: "sensorB"
         },
         timestamp: ISODate("2021-05-20T00:00:00.000Z"),
         temperature: 26
      }
   ],
   { "ordered": false }
)
```

### Use Consistent Field Order in Documents

Using a consistent field order in your documents improves insert and compression performance.

**Note:**

Compression requires consistent nested field order. For more information on compression with nested fields, see [Nested Fields Best Practices.](/docs/manual/core/timeseries/timeseries-best-practices#std-label-tsc-best-practice-embedded-fields)

For example, inserting the following documents, all of which have the same field order, results in optimal performance.

```javascript
{
   _id: ObjectId("6250a0ef02a1877734a9df57"),
   timestamp: ISODate("2020-01-23T00:00:00.441Z"),
   name: "sensor1",
   range: 1
},
{
   _id: ObjectId("6560a0ef02a1877734a9df66"),
   timestamp: ISODate("2020-01-23T01:00:00.441Z"),
   name: "sensor1",
   range: 5
}
```

In contrast, the following documents *do not* achieve optimal performance, because their field orders differ:

```javascript
{
   range: 1,
   _id: ObjectId("6250a0ef02a1877734a9df57"),
   name: "sensor1",
   timestamp: ISODate("2020-01-23T00:00:00.441Z")
},
{
   _id: ObjectId("6560a0ef02a1877734a9df66"),
   name: "sensor1",
   timestamp: ISODate("2020-01-23T01:00:00.441Z"),
   range: 5
}
```

### Increase the Number of Clients

Increasing the number of clients that write data to your collections can improve performance.

## Sharding Best Practices

To optimize sharding on your time series collection, perform the following action:

### Use the `metaField` as your Shard Key

Using the `metaField` to shard your collection provides sufficienct cardinality as a shard key for time series collections.

**Note:**

Starting in MongoDB 8.0, the use of the `timeField` as a shard key in time series collections is deprecated.

## Query Best Practices

To optimize queries on your time series collection, perform the following actions:

### Set a Strategic `metaField` When Creating the Collection

Your choice of `metaField` has the biggest impact on optimizing queries in your application.

- Select fields that rarely or never change as part of your metaField.

- If possible, select identifiers or other stable values that are common in filter expressions as part of your metaField.

- Avoid selecting fields that are not used for filtering as part of your metaField. Instead, use those fields as measurements.

For more information, see [metaField Considerations.](/docs/manual/core/timeseries/timeseries-considerations#std-label-timeseries-metafield-considerations)

### Set Appropriate Bucket Granularity

When you create a time series collection, MongoDB groups incoming time series data into buckets. By accurately setting granularity, you control how frequently data is bucketed based on the ingestion rate of your data.

Starting in MongoDB 6.3, you can use the custom bucketing parameters `bucketMaxSpanSeconds` and `bucketRoundingSeconds` to specify bucket boundaries and more precisely control how time series data is bucketed.

You can improve performance by setting the `granularity` or custom bucketing parameters to the best match for the time span between incoming measurements from the same data source. For example, if you are recording weather data from thousands of sensors but only record data from each sensor once per 5 minutes, you can either set `granularity` to `"minutes"` or set the custom bucketing parameters to `300` (seconds).

In this case, setting the `granularity` to `hours` groups up to a month's worth of data ingest events into a single bucket, resulting in longer traversal times and slower queries. Setting it to `seconds` leads to multiple buckets per polling interval, many of which might contain only a single document.

The following table shows the maximum time interval included in one bucket of data when using a given `granularity` value:

| `granularity` | `granularity` bucket limit |
| --- | --- |
| `seconds` | 1 hour |
| `minutes` | 24 hours |
| `hours` | 30 days |

**See also:**

[Timing of Automatic Removal](/docs/manual/core/timeseries/timeseries-automatic-removal#std-label-timeseries-collection-delete-operations-timing)

### Create Secondary Indexes

To improve query performance, [create one or more secondary indexes](/docs/manual/core/timeseries/timeseries-secondary-index#std-label-timeseries-add-secondary-index) on your `timeField` and `metaField` to support common query  patterns. In versions 6.3 and higher, MongoDB creates a secondary index on the `timeField` and `metaField` automatically.

### Additional Index Best Practices

- Use the metaField index for filtering and equality.

- Use the timeField and other indexed fields for range queries.

- General indexing strategies also apply to time series collections. For more information, see [Indexing Strategies.](/docs/manual/applications/indexes#std-label-indexing-strategies)

### Query the `metaField` on Sub-Fields

MongoDB reorders the `metaField` of time-series collections, which may cause servers to store data in a different field order than applications. If a `metaField` is an object, queries on the `metaField` may produce inconsistent results because `metaField` order may vary between servers and applications. To optimize queries on a time-series `metaField`, query the `metaField` on scalar sub-fields rather than the entire `metaField`.

The following example creates a time series collection:

```javascript
db.weather.insertMany( [
   {
      metaField: { sensorId: 5578, type: "temperature" },
      timestamp: ISODate( "2021-05-18T00:00:00.000Z" ),
      temp: 12
   },
   {
      metaField: { sensorId: 5578, type: "temperature" },
      timestamp: ISODate( "2021-05-18T04:00:00.000Z" ),
      temp: 11
   }
] )
```

The following query on the `sensorId` and `type` scalar sub-fields returns the first document that matches the query criteria:

```javascript
db.weather.findOne( {
   "metaField.sensorId": 5578,
   "metaField.type": "temperature"
} )
```

Example output:

```javascript
{
  _id: ObjectId("6572371964eb5ad43054d572"),
  metaField: { sensorId: 5578, type: 'temperature' },
  timestamp: ISODate( "2021-05-18T00:00:00.000Z" ),
  temp: 12
}
```

### Use $group Instead of Distinct()

Due to the unique data structure of time series collections, MongoDB can't efficiently index them for distinct values. Avoid using the [`distinct`](/docs/manual/reference/command/distinct#mongodb-dbcommand-dbcmd.distinct) command or [`db.collection.distinct()`](/docs/manual/reference/method/db.collection.distinct#mongodb-method-db.collection.distinct) helper method on time series collections. Instead, use a [`$group`](/docs/manual/reference/operator/aggregation/group#mongodb-pipeline-pipe.-group) aggregation to group documents by distinct values, as shown in the following example:

```javascript
db.foo.createIndex({"meta.project":1, "meta.type":1})
db.foo.aggregate([{$match: {"meta.project": 10}},
                  {$group: {_id: "$meta.type"}}])
```

This works as follows:

1. Creating a [compound index](/docs/manual/core/indexes/index-types/index-compound#std-label-index-type-compound) on `meta.project` and `meta.type` and supports the aggregation.

2. The [`$match`](/docs/manual/reference/operator/aggregation/match#mongodb-pipeline-pipe.-match) stage filters for documents where `meta.project = 10`.

3. The [`$group`](/docs/manual/reference/operator/aggregation/group#mongodb-pipeline-pipe.-group) stage uses `meta.type` as the group key to output one document per unique value.
