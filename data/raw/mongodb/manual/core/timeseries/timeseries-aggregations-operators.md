> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Aggregation and Operator Considerations

Some aggregation stages and operators require special considerations when you use them with [time series collections.](/docs/manual/core/timeseries-collections#std-label-manual-timeseries-landing)

## $geoNear

Time series collections only support the [`$geoNear`](/docs/manual/reference/operator/aggregation/geoNear#mongodb-pipeline-pipe.-geoNear) aggregation stage for sorting [geospatial data](/docs/manual/geospatial-queries) from queries against [2dsphere](/docs/manual/core/indexes/index-types/geospatial/2dsphere#std-label-2dsphere-index) indexes. You can't use the [`$near`](/docs/manual/reference/operator/query/near#mongodb-query-op.-near) and [`$nearSphere`](/docs/manual/reference/operator/query/nearSphere#mongodb-query-op.-nearSphere) operators on time series collections.

You can't use the `query` field for `$geoNear` on a [time series collection.](/docs/manual/core/timeseries-collections#std-label-manual-timeseries-landing)

You must specify the `key` field for `$geoNear` on a time series collection.

## $merge

You cannot use the [`$merge`](/docs/manual/reference/operator/aggregation/merge#mongodb-pipeline-pipe.-merge) aggregation stage to add data from another collection to a time series collection.

## $out

Starting in MongoDB 7.0, you can use the [`$out`](/docs/manual/reference/operator/aggregation/out#mongodb-pipeline-pipe.-out) aggregation stage to write documents to a time series collection. For more information, see [Migrate Data into a Time Series Collection.](/docs/manual/core/timeseries/timeseries-migrate-data-into-timeseries-collection#std-label-migrate-data-into-a-timeseries-collection)

## Frequently Used Operations

The following aggregation pipeline operators and stages are often used to analyze time series data:

- [`$dateAdd`](/docs/manual/reference/operator/aggregation/dateAdd#mongodb-expression-exp.-dateAdd): Adds a specified amount of time to a Date object.

- [`$dateDiff`](/docs/manual/reference/operator/aggregation/dateDiff#mongodb-expression-exp.-dateDiff): Returns the time difference between two dates.

- [`$dateTrunc`](/docs/manual/reference/operator/aggregation/dateTrunc#mongodb-expression-exp.-dateTrunc): Returns a date that has been truncated to the specific unit.

- [`$setWindowFields`](/docs/manual/reference/operator/aggregation/setWindowFields#mongodb-pipeline-pipe.-setWindowFields): Runs calculations on documents in a given window.

## Examples

### Calculate Average Price per Month

Consider a `dowJonesTickerData` collection that contains documents with the following structure:

```javascript
{
   date: ISODate("2020-01-03T05:00:00.000Z"),
   symbol: 'AAPL',
   volume: 146322800,
   open: 74.287498,
   adjClose: 73.486023,
   high: 75.144997,
   low: 74.125,
   close: 74.357498
}
```

This aggregation pipeline performs the following actions:

- Uses [`$dateTrunc`](/docs/manual/reference/operator/aggregation/dateTrunc#mongodb-expression-exp.-dateTrunc) to truncate each document's `date` to the appropriate month.

- Uses [`$group`](/docs/manual/reference/operator/aggregation/group#mongodb-pipeline-pipe.-group) to group the documents by month and symbol.

- Uses [`$avg`](/docs/manual/reference/operator/aggregation/avg#mongodb-group-grp.-avg) to calculate the average price per month.

```javascript
db.dowJonesTickerData.aggregate( [ {
   $group: {
      _id: {
         firstDayOfMonth: {
            $dateTrunc: {
               date: "$date",
               unit: "month"
            }
         },
         symbol: "$symbol"
      },
      avgMonthClose: {
         $avg: "$close"
      }
   }
} ] )
```

The pipeline returns a set of documents where each document contains the average closing price per month for a particular stock.

```javascript
{
   _id: {
      firstDayOfMonth: ISODate("2020-06-01T00:00:00.000Z"),
      symbol: 'GOOG'
   },
   avgMonthClose: 1431.0477184545455
},
{
   _id: {
      firstDayOfMonth: ISODate("2021-07-01T00:00:00.000Z"),
      symbol: 'MDB'
   },
   avgMonthClose: 352.7314293333333
},
{
   _id: {
      firstDayOfMonth: ISODate("2021-06-01T00:00:00.000Z"),
      symbol: 'MSFT'
   },
   avgMonthClose: 259.01818086363636
}
```

### Calculate a Rolling Average Over 30 Days

Consider a `dowJonesTickerData` collection that contains documents with the following structure:

```javascript
{
   date: ISODate("2020-01-03T05:00:00.000Z"),
   symbol: 'AAPL',
   volume: 146322800,
   open: 74.287498,
   adjClose: 73.486023,
   high: 75.144997,
   low: 74.125,
   close: 74.357498
}
```

This aggregation pipeline performs the following operations:

- Uses [`$setWindowFields`](/docs/manual/reference/operator/aggregation/setWindowFields#mongodb-pipeline-pipe.-setWindowFields) to specify a window of 30 days.

- Calculates a rolling average of the closing price over the last 30 days for each stock.

```javascript
db.dowJonesTickerData.aggregate( [
   { $setWindowFields: {
      partitionBy: { symbol : "$symbol" } ,
      sortBy: { date: 1 },
      output: {
         averageMonthClosingPrice: {
            $avg : "$close",
            window : { range : [-1, "current"], unit : "month" }

         }
      }
   } }
] )
```

The pipeline returns a set of documents where each document includes a `$averageMonthClosingPrice` field that contains the average of the previous month's closing price for that stock symbol.

```javascript
{
   date: ISODate("2020-01-29T05:00:00.000Z"),
   symbol: 'AAPL',
   volume: 216229200,
   adjClose: 80.014801,
   low: 80.345001,
   high: 81.962502,
   open: 81.112503,
   close: 81.084999,
   averageMonthClosingPrice: 77.63137520000001
}
```

Each of the following examples uses a `dowJonesTickerData` collection that contains documents with the following structure:

```csharp
new Stocks()
{
    Symbol = "MDB",
    Date = DateTime.Parse("2021-12-18T15:59:00Z"),
    Close = 252.47,
    Volume = 55046.0
}

```

### Calculate Average Price per Month

This example aggregation pipeline performs the following actions:

- Uses [`$dateTrunc`](/docs/manual/reference/operator/aggregation/dateTrunc#mongodb-expression-exp.-dateTrunc) to truncate each document's `date` to the appropriate month.

- Uses [`$group`](/docs/manual/reference/operator/aggregation/group#mongodb-pipeline-pipe.-group) to group the documents by month and symbol.

- Uses [`$avg`](/docs/manual/reference/operator/aggregation/avg#mongodb-group-grp.-avg) to calculate the average price per month.

The pipeline returns a set of documents where each document contains the average closing price per month for a particular stock.

```csharp
var pipeline = new BsonDocument[]
{
    new("$group",
        new BsonDocument
        {
            {
                "_id",
                new BsonDocument
                {
                    {
                        "firstDayOfMonth",
                        new BsonDocument("$dateTrunc",
                            new BsonDocument
                            {
                                { "date", "$date" },
                                { "unit", "month" }
                            })
                    },
                    { "symbol", "$symbol" }
                }
            },
            {
                "avgMonthClose", new BsonDocument("$avg", "$close")
            }
        })
};
var pipelineDefinition = PipelineDefinition<Stocks, BsonDocument>.Create(pipeline);
var result = await _stocks?.Aggregate(pipelineDefinition).ToListAsync()!;

```

**Output:**

```json
[
  {
    "_id": {
      "firstDayOfMonth": {
        "$date": "2021-12-01T00:00:00Z"
      },
      "symbol": "GOOG"
    },
    "avgMonthClose": 253.62
  },
  {
    "_id": {
      "firstDayOfMonth": {
        "$date": "2021-12-01T00:00:00Z"
      },
      "symbol": "MSFT"
    },
    "avgMonthClose": 253.82999999999998
  },
  {
    "_id": {
      "firstDayOfMonth": {
        "$date": "2021-12-01T00:00:00Z"
      },
      "symbol": "MDB"
    },
    "avgMonthClose": 252.70499999999998
  }
]
```

### Calculate a Rolling Average Over 30 Days

The next example aggregation pipeline performs the following operations:

- Uses [`$setWindowFields`](/docs/manual/reference/operator/aggregation/setWindowFields#mongodb-pipeline-pipe.-setWindowFields) to specify a window of 30 days.

- Calculates a rolling average of the closing price over the last 30 days for each stock.

The pipeline returns a set of documents where each document includes a `$averageMonthClosingPrice` field that contains the average of the previous month's closing price for that stock symbol.

```csharp
var pipeline = new BsonDocument[]
{
    new("$setWindowFields",
        new BsonDocument
        {
            { "partitionBy", new BsonDocument("symbol", "$symbol") },
            { "sortBy", new BsonDocument("date", 1) },
            { "output", new BsonDocument("averageMonthClosingPrice",
                new BsonDocument
                {
                    { "$avg", "$close" },
                    { "window", new BsonDocument
                        {
                            { "range", new BsonArray { -1, "current" } },
                            { "unit", "month" }
                        }
                    }
                })
            }
        })
};

var pipelineDefinition = PipelineDefinition<Stocks, BsonDocument>.Create(pipeline);
var result = await _stocks?.Aggregate(pipelineDefinition).ToListAsync()!;

```

**Output:**

```json
[
  {
    "date": {
      "$date": "2021-12-18T15:57:00Z"
    },
    "close": 253.62,
    "volume": 40182,
    "symbol": "GOOG",
    "_id": {
      "$oid": "6971140eef74a5a9bec56820"
    },
    "averageMonthClosingPrice": 253.62
  },
  {
    "date": {
      "$date": "2021-12-18T15:58:00Z"
    },
    "close": 252.94,
    "volume": 44042,
    "symbol": "MDB",
    "_id": {
      "$oid": "6971140eef74a5a9bec5681f"
    },
    "averageMonthClosingPrice": 252.94
  },
  {
    "date": {
      "$date": "2021-12-18T15:59:00Z"
    },
    "close": 252.47,
    "volume": 55046,
    "symbol": "MDB",
    "_id": {
      "$oid": "6971140eef74a5a9bec5681e"
    },
    "averageMonthClosingPrice": 252.70499999999998
  },
  {
    "date": {
      "$date": "2021-12-18T15:55:00Z"
    },
    "close": 254.03,
    "volume": 40270,
    "symbol": "MSFT",
    "_id": {
      "$oid": "6971140eef74a5a9bec56822"
    },
    "averageMonthClosingPrice": 254.03
  },
  {
    "date": {
      "$date": "2021-12-18T15:56:00Z"
    },
    "close": 253.63,
    "volume": 27890,
    "symbol": "MSFT",
    "_id": {
      "$oid": "6971140eef74a5a9bec56821"
    },
    "averageMonthClosingPrice": 253.82999999999998
  }
]
```

Each of the following examples uses a `dowJonesTickerData` collection that contains documents with the following structure:

```python
"symbol": "MDB",
"date": datetime(2021, 12, 18, 15, 59, 0, 0),
"close": 252.47,
"volume": 55046.00,

```

### Calculate Average Price per Month

This example aggregation pipeline performs the following actions:

- Uses [`$dateTrunc`](/docs/manual/reference/operator/aggregation/dateTrunc#mongodb-expression-exp.-dateTrunc) to truncate each document's `date` to the appropriate month.

- Uses [`$group`](/docs/manual/reference/operator/aggregation/group#mongodb-pipeline-pipe.-group) to group the documents by month and symbol.

- Uses [`$avg`](/docs/manual/reference/operator/aggregation/avg#mongodb-group-grp.-avg) to calculate the average price per month.

The pipeline returns a set of documents where each document contains the average closing price per month for a particular stock.

```python
pipeline_results = stocks_coll.aggregate(
    [
        {
            "$group": {
                "_id": {
                    "firstDayOfMonth": {
                        "$dateTrunc": {
                            "date": "$date",
                            "unit": "month"
                        }
                    },
                    "symbol": "$symbol"
                },
                "avgMonthClose": {"$avg": "$close"}
            }
        }
    ]
)

```

**Output:**

```json
[
  {
    "_id": {
      "firstDayOfMonth": datetime.datetime(2021, 12, 1, 0, 0),
      "symbol": "GOOG"
    },
    "avgMonthClose": 253.82999999999998
  },
  {
    "_id": {
      "firstDayOfMonth": datetime.datetime(2021, 12, 1, 0, 0),
      "symbol": "APPL"
    },
    "avgMonthClose": 253.61
  },
  {
    "_id": {
      "firstDayOfMonth": datetime.datetime(2021, 12, 1, 0, 0),
      "symbol": "MDB"
    },
    "avgMonthClose": 252.7
  }
]

```

### Calculate a Rolling Average Over 30 Days

The next example aggregation pipeline performs the following operations:

- Uses [`$setWindowFields`](/docs/manual/reference/operator/aggregation/setWindowFields#mongodb-pipeline-pipe.-setWindowFields) to specify a window of 30 days.

- Calculates a rolling average of the closing price over the last 30 days for each stock.

The pipeline returns a set of documents where each document includes a `$averageMonthClosingPrice` field that contains the average of the previous month's closing price for that stock symbol.

```python
pipeline_results = stocks_coll.aggregate(
    [
        {
            "$setWindowFields": {
                "partitionBy": "$symbol",
                "sortBy": {"date": 1},
                "output": {
                    "averageMonthClosingPrice": {
                        "$avg": "$close",
                        "window": {"range": [-1, 0], "unit": "month"}
                    }
                }
            }
        }
    ]
)

```

**Output:**

```json
[
 {
    "date": datetime.datetime(2021, 12, 18, 15, 57),
    "symbol": "APPL",
    "volume": 40182,
    "_id": ObjectId("69716feb98032974560c2699"),
    "close": 253.61,
    "averageMonthClosingPrice": 253.61
  },
  {
    "date": datetime.datetime(2021, 12, 18, 15, 55),
    "symbol": "GOOG",
    "_id": ObjectId("69716feb98032974560c269b"),
    "close": 254.03,
    "volume": 40270,
    "averageMonthClosingPrice": 254.03
  },
  {
    "date": datetime.datetime(2021, 12, 18, 15, 56),
    "symbol": "GOOG",
    "_id": ObjectId("69716feb98032974560c269a"),
    "close": 253.63,
    "volume": 27890,
    "averageMonthClosingPrice": 253.82999999999998
  },
  {
    "date": datetime.datetime(2021, 12, 18, 15, 58),
    "symbol": "MDB",
    "_id": ObjectId("69716feb98032974560c2698"),
    "close": 252.93,
    "volume": 44042,
    "averageMonthClosingPrice": 252.93
  },
  {
    "date": datetime.datetime(2021, 12, 18, 15, 59),
    "symbol": "MDB",
    "_id": ObjectId("69716feb98032974560c2697"),
    "close": 252.47,
    "volume": 55046,
    "averageMonthClosingPrice": 252.7
  }
]

```

Each of the following examples uses a `dowJonesTickerData` collection that contains documents with the following structure:

```java
new Document("symbol", "MDB")
        .append("date", Date.from(Instant.parse("2021-12-18T15:59:00Z")))
        .append("close", 252.47)
        .append("volume", 55046.0),

```

### Calculate Average Price per Month

This example aggregation pipeline performs the following actions:

- Uses [`$dateTrunc`](/docs/manual/reference/operator/aggregation/dateTrunc#mongodb-expression-exp.-dateTrunc) to truncate each document's `date` to the appropriate month.

- Uses [`$group`](/docs/manual/reference/operator/aggregation/group#mongodb-pipeline-pipe.-group) to group the documents by month and symbol.

- Uses [`$avg`](/docs/manual/reference/operator/aggregation/avg#mongodb-group-grp.-avg) to calculate the average price per month.

The pipeline returns a set of documents where each document contains the average closing price per month for a particular stock.

```java
// Create the compound _id with $dateTrunc and symbol
Document groupId = new Document("firstDayOfMonth",
        new Document("$dateTrunc",
                new Document("date", "$date")
                        .append("unit", "month")))
        .append("symbol", "$symbol");

// Create the $group stage
Bson groupStage = Aggregates.group(
        groupId,
        Accumulators.avg("avgMonthClose", "$close")
);

// Run the aggregation
List<Document> result = stocks.aggregate(List.of(groupStage))
        .into(new ArrayList<>());

```

**Output:**

```json
{"_id": {"firstDayOfMonth": {"$date": "2021-12-01T00:00:00Z"},"symbol": "MDB"},"avgMonthClose": 252.7}
{"_id": {"firstDayOfMonth": {"$date": "2021-12-01T00:00:00Z"},"symbol": "APPL"},"avgMonthClose": 253.61}
{"_id": {"firstDayOfMonth": {"$date": "2021-12-01T00:00:00Z"},"symbol": "GOOG"},"avgMonthClose": 253.82999999999998}

```

### Calculate a Rolling Average Over 30 Days

The next example aggregation pipeline performs the following operations:

- Uses [`$setWindowFields`](/docs/manual/reference/operator/aggregation/setWindowFields#mongodb-pipeline-pipe.-setWindowFields) to specify a window of 30 days.

- Calculates a rolling average of the closing price over the last 30 days for each stock.

The pipeline returns a set of documents where each document includes a `$averageMonthClosingPrice` field that contains the average of the previous month's closing price for that stock symbol.

```java
// Use $setWindowFields to specify the 30-day window
List<Document> pipeline = List.of(
        new Document("$setWindowFields",
                new Document("partitionBy", new Document("symbol", "$symbol"))
                        .append("sortBy", new Document("date", 1))
                        .append("output", new Document("averageMonthClosingPrice",
                                new Document("$avg", "$close")
                                        .append("window", new Document("range", Arrays.asList(-1, "current"))
                                                .append("unit", "month")))))
);
// Run the aggregation
List<Document> result = stocks.aggregate(pipeline)
        .into(new ArrayList<>());

```

**Output:**

```json
{"date": {"$date": {"$date": "2021-12-18T15:57:00Z"}}, "symbol": "APPL", "_id": "6972b12a1ef3a1e5ce994fa0", "close": 253.61, "volume": 40182.0, "averageMonthClosingPrice": 253.61}
{"date": {"$date": {"$date": "2021-12-18T15:55:00Z"}}, "symbol": "GOOG", "_id": "6972b12a1ef3a1e5ce994fa2", "close": 254.03, "volume": 40270.0, "averageMonthClosingPrice": 254.03}
{"date": {"$date": {"$date": "2021-12-18T15:56:00Z"}}, "symbol": "GOOG", "_id": "6972b12a1ef3a1e5ce994fa1", "close": 253.63, "volume": 27890.0, "averageMonthClosingPrice": 253.82999999999998}
{"date": {"$date": {"$date": "2021-12-18T15:58:00Z"}}, "symbol": "MDB", "_id": "6972b12a1ef3a1e5ce994f9f", "close": 252.93, "volume": 44042.0, "averageMonthClosingPrice": 252.93}
{"date": {"$date": {"$date": "2021-12-18T15:59:00Z"}}, "symbol": "MDB", "_id": "6972b12a1ef3a1e5ce994f9e", "close": 252.47, "volume": 55046.0, "averageMonthClosingPrice": 252.7}

```

Each of the following examples uses a `dowJonesTickerData` collection that contains documents with the following structure:

```javascript
{
  symbol: 'MDB',
  date: new Date('2021-12-18T15:59:00Z'),
  close: 252.47,
  volume: 55046.0,
},

```

### Calculate Average Price per Month

This example aggregation pipeline performs the following actions:

- Uses [`$dateTrunc`](/docs/manual/reference/operator/aggregation/dateTrunc#mongodb-expression-exp.-dateTrunc) to truncate each document's `date` to the appropriate month.

- Uses [`$group`](/docs/manual/reference/operator/aggregation/group#mongodb-pipeline-pipe.-group) to group the documents by month and symbol.

- Uses [`$avg`](/docs/manual/reference/operator/aggregation/avg#mongodb-group-grp.-avg) to calculate the average price per month.

The pipeline returns a set of documents where each document contains the average closing price per month for a particular stock.

```javascript
const pipeline = [
  {
    $group: {
      _id: {
        firstDayOfMonth: {
          $dateTrunc: {
            date: '$date',
            unit: 'month',
          },
        },
        symbol: '$symbol',
      },
      avgMonthClose: { $avg: '$close' },
    },
  },
];
const result = await stocksCollection.aggregate(pipeline).toArray();
return result;

```

**Output:**

```json
[
  {
    "_id": { "firstDayOfMonth": "2021-12-01T00:00:00.000Z", "symbol": "GOOG" },
    "avgMonthClose": 253.62
  },
  {
    "_id": { "firstDayOfMonth": "2021-12-01T00:00:00.000Z", "symbol": "MDB" },
    "avgMonthClose": 252.70499999999998
  },
  {
    "_id": { "firstDayOfMonth": "2021-12-01T00:00:00.000Z", "symbol": "MSFT" },
    "avgMonthClose": 253.82999999999998
  }
]

```

### Calculate a Rolling Average Over 30 Days

The next example aggregation pipeline performs the following operations:

- Uses [`$setWindowFields`](/docs/manual/reference/operator/aggregation/setWindowFields#mongodb-pipeline-pipe.-setWindowFields) to specify a window of 30 days.

- Calculates a rolling average of the closing price over the last 30 days for each stock.

The pipeline returns a set of documents where each document includes a `$averageMonthClosingPrice` field that contains the average of the previous month's closing price for that stock symbol.

```javascript
try {
  const pipeline = [
    {
      $setWindowFields: {
        partitionBy: { symbol: '$symbol' },
        sortBy: { date: 1 },
        output: {
          averageMonthClosingPrice: {
            $avg: '$close',
            window: {
              range: [-1, 'current'],
              unit: 'month',
            },
          },
        },
      },
    },
  ];

  const result = await stocksCollection.aggregate(pipeline).toArray();
  return result;

```

**Output:**

```json
[
  {
    "_id": "6973b6508c09e14b2552a939",
    "symbol": "GOOG",
    "date": "2021-12-18T15:57:00.000Z",
    "close": 253.62,
    "volume": 40182,
    "averageMonthClosingPrice": 253.62
  },
  {
    "_id": "6973b6508c09e14b2552a938",
    "symbol": "MDB",
    "date": "2021-12-18T15:58:00.000Z",
    "close": 252.94,
    "volume": 44042,
    "averageMonthClosingPrice": 252.94
  },
  {
    "_id": "6973b6508c09e14b2552a937",
    "symbol": "MDB",
    "date": "2021-12-18T15:59:00.000Z",
    "close": 252.47,
    "volume": 55046,
    "averageMonthClosingPrice": 252.70499999999998
  },
  {
    "_id": "6973b6508c09e14b2552a93b",
    "symbol": "MSFT",
    "date": "2021-12-18T15:55:00.000Z",
    "close": 254.03,
    "volume": 40270,
    "averageMonthClosingPrice": 254.03
  },
  {
    "_id": "6973b6508c09e14b2552a93a",
    "symbol": "MSFT",
    "date": "2021-12-18T15:56:00.000Z",
    "close": 253.63,
    "volume": 27890,
    "averageMonthClosingPrice": 253.82999999999998
  }
]

```
