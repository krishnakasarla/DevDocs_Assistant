> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Migrate Data into a Time Series Collection

If your collection stores data that you want to compare across time intervals, use a time series collection to improve performance and storage. For more information on the benefits of time series collections, see [Time Series Collections.](/docs/manual/core/timeseries-collections#std-label-manual-timeseries-collection)

You can use the following methods to migrate data from an existing collection into a [time series collection:](/docs/manual/core/timeseries-collections#std-label-manual-timeseries-collection)

- [Migrate with an Aggregation Pipeline](/docs/manual/core/timeseries/timeseries-migrate-with-aggregation#std-label-migrate-data-into-a-timeseries-collection-with-aggregation)

- [Migrate with Database Tools](/docs/manual/core/timeseries/timeseries-migrate-with-tools#std-label-migrate-data-into-a-timeseries-collection-with-tools)

- [Migrate with Relational Migrator](https://www.mongodb.com/docs/relational-migrator/mapping-rules/mapping-rule-options/time-series/)

## Considerations

If you use MongoDB 7.0 or greater and already have your data in a MongoDB database, migrate with an [aggregation pipeline.](/docs/manual/core/timeseries/timeseries-migrate-with-aggregation#std-label-migrate-data-into-a-timeseries-collection-with-aggregation)

If your data is in a relational database, use [Relational Migrator](https://www.mongodb.com/docs/relational-migrator/mapping-rules/mapping-rule-options/time-series/) to migrate your data into a time series collection.

If your deployment is not in one of those cases, use [Database Tools](/docs/manual/core/timeseries/timeseries-migrate-with-tools#std-label-migrate-data-into-a-timeseries-collection-with-tools) to migrate your data.
