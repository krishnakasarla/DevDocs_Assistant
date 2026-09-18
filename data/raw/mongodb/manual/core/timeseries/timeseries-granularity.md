> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Set Granularity for Time Series Data

When you create a time series collection, MongoDB automatically groups incoming time series data into buckets. By setting granularity, you control how frequently data is bucketed based on the ingestion rate of your data.

Starting in MongoDB 6.3, you can use the custom bucketing parameters `bucketMaxSpanSeconds` and `bucketRoundingSeconds` to specify bucket boundaries and more accurately control how time series data is bucketed.

For more information on bucketing, see [About Time Series Data.](/docs/manual/core/timeseries/timeseries-bucketing#std-label-timeseries-bucketing)

**Note:**

You must be running MongoDB 5.0.1 or later in order to change a time series collection's granularity after the collection has been created.

## Retrieve the Current Bucketing Parameters

To retrieve current collection values, use the [`listCollections`](/docs/manual/reference/command/listCollections#mongodb-dbcommand-dbcmd.listCollections) command:

```javascript
db.runCommand( { listCollections: 1 } )
```

For time series collections, the output contains `granularity`, `bucketMaxSpanSeconds`, and `bucketRoundingSeconds` parameters, if present.

```javascript
{
    cursor: {
       id: <number>,
       ns: 'test.$cmd.listCollections',
       firstBatch: [
         {
            name: <string>,
            type: 'timeseries',
            options: {
               expireAfterSeconds: <number>,
               timeseries: {
                  timeField: <string>,
                  metaField: <string>,
                  granularity: <string>,
                  bucketMaxSpanSeconds: <number>,
                  bucketRoundingSeconds: <number>
               }
            },
            ...
         },
         ...
       ]
    }
 }
```

## Set the "granularity" Parameter

The following example sets the `granularity` of a `weather24h` collection to `minutes`:

```javascript
db.createCollection(
    "weather24h",
    {
       timeseries: {
          timeField: "timestamp",
          metaField: "metadata",
          granularity: "minutes"
       },
       expireAfterSeconds: 86400
    }
)
```

**See also:**

[Timing of Automatic Removal](/docs/manual/core/timeseries/timeseries-automatic-removal#std-label-timeseries-collection-delete-operations-timing)

## Using Custom Bucketing Parameters

In MongoDB 6.3 and later, instead of `granularity`, you can set bucket boundaries manually using the two custom bucketing parameters. Consider this approach if you expect to query data for fixed time intervals, such as every 4 hours starting at midnight. Ensuring buckets don't overlap between those periods optimizes for high query volume and [`insert`](/docs/manual/reference/command/insert#mongodb-dbcommand-dbcmd.insert) operations.

To use custom bucketing parameters, set both parameters to the same value, and do not set `granularity`:

- `bucketMaxSpanSeconds` sets the maximum time between timestamps in the same bucket. Possible values are 1-31536000.

- `bucketRoundingSeconds` sets the time interval that determines the starting timestamp for a new bucket. When a document requires a new bucket, MongoDB rounds down the document's timestamp value by this interval to set the minimum time for the bucket.

For the weather station example, if you generate summary reports every 4 hours, you could adjust bucketing by setting the custom bucketing parameters to 14400 seconds instead of using a `granularity` of `"minutes"`:

```javascript
db.createCollection(
   "weather24h",
   {
      timeseries: {
         timeField: "timestamp",
         metaField: "metadata",
         bucketMaxSpanSeconds: 14400,
         bucketRoundingSeconds: 14400
      }
   }
)
```

If a document with a time of `2023-03-27T16:24:35Z` does not fit an existing bucket, MongoDB creates a new bucket with a minimum time of `2023-03-27T16:00:00Z` and a maximum time of `2023-03-27T19:59:59Z`.

## Change Time Series Granularity

You can increase `timeseries.granularity` from a shorter unit of time to a longer one using a [`collMod`](/docs/manual/reference/command/collMod#mongodb-dbcommand-dbcmd.collMod) command.

```javascript
db.runCommand( {
   collMod: "weather24h",
   timeseries: { granularity: "seconds" | "minutes" | "hours" }
} )
```

If you are using the custom bucketing parameters `bucketRoundingSeconds` and `bucketMaxSpanSeconds` instead of `granularity`, include both custom parameters in the `collMod` command and set them to the same value:

```javascript
db.runCommand( {
   collMod: "weather24h",
   timeseries: {
      bucketRoundingSeconds: 86400,
      bucketMaxSpanSeconds: 86400
   }
} )
```

You cannot decrease the granularity interval or the custom bucketing values.

**Note:**

To modify the granularity of a **sharded** time series collection, you must be running MongoDB 6.0 or later.
