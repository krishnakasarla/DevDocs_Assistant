> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Time Series Collections Considerations

Time series collections generally behave like normal collections, but with additional exceptions. For information on time series collection behavior and structure, see [Time Series Collections.](/docs/manual/core/timeseries-collections#std-label-manual-timeseries-collection)

## metaField Considerations

A `metaField` should rarely change and can be any data type. A `metaField` can be an object and can contain subfields. Once you define a field as the `metaField`, you can change the value of the `metaField` but you cannot redefine the `metaField` as another field. For example, if you create time series documents with the `metaField` defined as field `A`, you cannot later convert a field `B` to be the `metaField`. However, if the value of `A` is an object, you can add new subfields to `A`.

**Note:**

Using an array as a `metaField` may cause unexpected collection behavior because array equality depends on specific order.

MongoDB uses the `metaField` to partition data for efficient organization and retrieval. When you create a time series collection, MongoDB groups documents into buckets. Documents within a bucket share an identical `metaField` value and have `timeField` values that are close together.

The number of buckets in a time series collection depends on the number of unique `metaField` values. Collections with fine-grained or dynamic `metaField` values may generate more, sparsely packed, short-lived buckets than collections with simple `metaField` values that rarely or never change. Fine-grained and dynamic `metaField` values typically decrease storage and query effiency.

### `metaField` Best Practices

- Select fields that rarely or never change as part of your metaField.

- If possible, select identifiers or other stable values that are common in filter expressions as part of your metaField.

- Avoid selecting fields that are not used for filtering as part of your metaField. Instead, use those fields as measurements.

## Storage and Cardinality

When you insert data into a time series collection, the internal collection automatically organizes the data into an optimized storage format using [buckets](/docs/manual/core/timeseries/timeseries-bucketing#std-label-timeseries-bucketing-specifics). If a suitable bucket exists, MongoDB inserts new data into that bucket. If a suitable bucket does not exist, MongoDB creates a new bucket. To optimize storage, choose a `metaField` that rarely changes to create time series collections with fewer, more densely packed buckets.

Collections with fine-grained or changing `metaField` values generate many sparsely packed, short-lived buckets, increasing the cardinality of your collection. Increasing cardinality leads to decreased storage and query efficiency.

## Granularity

You can use the `granularity` parameter to specify how frequently MongoDB buckets your time series data based on the data ingestion rate. The following table shows the maximum time interval included in one bucket of data when using a given `granularity` value:

| `granularity` | `granularity` bucket limit |
| --- | --- |
| `seconds` | 1 hour |
| `minutes` | 24 hours |
| `hours` | 30 days |

By default, `granularity` is set to `seconds`. You can improve performance by setting the `granularity` value to the closest match to the time span between incoming measurements from the same data source. For example, if you are recording weather data from thousands of sensors but only record data from each sensor once per 5 minutes, set `granularity` to `"minutes"`. The less frequently you append new documents, the greater the storage and performance benefits of coarser granularity.

Setting the `granularity` to `hours` groups up to a month's worth of data ingest events into a single bucket, resulting in longer traversal times and slower queries. Setting it to `seconds` leads to multiple buckets per polling interval, many of which might contain only a single document.

You should also consider typical queries when choosing the `granularity` value. For example, if you expect your queries to fetch 1 day of data at a time, use "minutes". A finer granularity, like "seconds", creates buckets that cover one hour. This requires more buckets to represent the same data, which negatively affects storage and query performance. A coarser granularity, like "hours" (which has a 30-day bucket span), requires queries to fetch 30 days of data at a time and then filter out most of it.

For examples, see [Set Granularity for Time Series Data.](/docs/manual/core/timeseries/timeseries-granularity#std-label-timeseries-granularity)

## Compression and Hardware

All time series collection use a compressed bucket format when you append data into opened or reopened buckets. Compressing time series data in the cache supports high [cardinality](/docs/manual/reference/glossary#std-term-cardinality) workloads while preserving efficient query performance.

## Zone Sharding

Zone sharding does not support time series collections. The balancer always distributes data in sharded time series collections evenly across all shards in the cluster.
