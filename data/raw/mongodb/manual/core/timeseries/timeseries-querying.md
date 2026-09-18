> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# About Querying Time Series Data

MongoDB groups documents with matching [metaFields](/docs/manual/core/timeseries-collections#std-label-timeseries-collections-metafield) to optimize the storage and query latency of time series data. Your choice of `metaField` has the biggest impact on optimizing queries in your application.

## Querying the metaField

You query a time series collection the same way you query a standard MongoDB collection. For an example query and example aggregation pipeline, see [Query a Time Series Collection](/docs/manual/core/timeseries/timeseries-procedures#std-label-timeseries-query-example). For a list of querying best practices, see [Query Best Practices.](/docs/manual/core/timeseries/timeseries-best-practices#std-label-tsc-best-practice-optimize-query-performance)

Queries against time series data typically focus on a single time series in the collection. For example, consider a time series collection that tracks stock data using the following schema:

```javascript
{
   _id: 573a1397f29313caabce8347,

   "ticker": "MDB",
   "timestamp": ISODate("2024-07-24T13:45:00.000Z"),
   "price": 248.21,
   "volume": 6930
}
```

The collection has the following settings:

```javascript
timeseries: {
   timeField: "timestamp",
   metaField: "ticker",
   granularity: "seconds"
}
```

MongoDB groups documents with matching `ticker` values. Instead of having to check for matches across all fields in all documents, the server only has to check against the `metaField`, in this case `ticker`, to narrow down the search range to a unique time series. This fits the expected use case, which is searching for activity on a single stock. A user searching for information on MongoDB stock (MDB) doesn't need to consider results for Amazon (AMZN).

## Querying the timeField

The second major dimension for querying time series data is time. Since MongoDB groups documents that have both an identical `metaField` value and close `timeField` values, this further narrows the scope of a query to a range of buckets. Recent transactions are kept in memory, so it's easy to stream data in real time.

## Block Processing

Starting in version 8.0, MongoDB may execute certain time series queries using block processing. This performance improvement processes queries in "blocks" of data, rather than individual values. Block processing improves query execution speed and throughput when working with time series collections.

Block processing significantly improves performance and reduces overhead for long running aggregation pipelines that begin with the following stages:

- [`$match`](/docs/manual/reference/operator/aggregation/match#mongodb-pipeline-pipe.-match)

- [`$sort`](/docs/manual/reference/operator/aggregation/sort#mongodb-pipeline-pipe.-sort), if used on the `timeField`

- [`$group`](/docs/manual/reference/operator/aggregation/group#mongodb-pipeline-pipe.-group)

Compared to time series queries run on MongoDB 7.0 or earlier, block processing for time series data in MongoDB 8.0 may handle higher volumes of data and improve throughput in some cases by more than 200% for [`$group`](/docs/manual/reference/operator/aggregation/group#mongodb-pipeline-pipe.-group) operations and analytical queries. To learn more about performance improvements in MongoDB 8.0, see [Performance Improvements.](/docs/manual/release-notes/8.0#std-label-8.0-performance-improvements)

**Note:**

The amount of performance improvement can vary depending on the configuration of your workloads and database instances.

MongoDB automatically enables block processing for eligible time series queries. You cannot manually specify whether a query uses block processing. To see if your time series query uses block processing, see [`stages`](/docs/manual/reference/explain-results#mongodb-data-explain.queryPlanner.winningPlan.slotBasedPlan.stages) in the explain plan output.
