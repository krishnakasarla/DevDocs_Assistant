> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Geospatial Indexes

Geospatial indexes support queries on data stored as [GeoJSON](/docs/manual/geospatial-queries#std-label-geospatial-geojson) objects or [legacy coordinate pairs](/docs/manual/geospatial-queries#std-label-geospatial-legacy). You can use geospatial indexes to improve performance for queries on geospatial data or to run certain geospatial queries.

MongoDB provides two types of geospatial indexes:

- [2dsphere Indexes](/docs/manual/core/indexes/index-types/geospatial/2dsphere#std-label-2dsphere-index), which support queries that interpret geometry on a sphere.

- [2d Indexes](/docs/manual/core/indexes/index-types/geospatial/2d#std-label-2d-index), which support queries that interpret geometry on a flat surface.

To learn more about geospatial data and query operations, see [Geospatial Queries.](/docs/manual/geospatial-queries)

## Use Cases

If your application frequently queries a field that contains geospatial data, you can create a geospatial index to improve performance for those queries.

Certain query operations require a geospatial index. If you want to query with the [`$near`](/docs/manual/reference/operator/query/near#mongodb-query-op.-near) or [`$nearSphere`](/docs/manual/reference/operator/query/nearSphere#mongodb-query-op.-nearSphere) operators or the [`$geoNear`](/docs/manual/reference/operator/aggregation/geoNear#mongodb-pipeline-pipe.-geoNear) aggregation stage, you must create a geospatial index. For details, see [Geospatial Query Operators](/docs/manual/geospatial-queries#std-label-geospatial-operators) and [Geospatial Aggregation Stage.](/docs/manual/geospatial-queries#std-label-geospatial-aggregation)

For example, consider a `subway` collection with documents containing a `location` field, which specifies the coordinates of subway stations in a city. You often run queries with the [`$geoWithin`](/docs/manual/reference/operator/query/geoWithin#mongodb-query-op.-geoWithin) operator to return a list of stations within a specific area. To improve performance for this query, you can create a geospatial index on the `location` field. After creating the index, you can query using the [`$near`](/docs/manual/reference/operator/query/near#mongodb-query-op.-near) operator to return a list of nearby stations, sorted from nearest to farthest.

## Get Started

To create a geospatial index and run geospatial queries, see:

- [Create a 2dsphere Index](/docs/manual/core/indexes/index-types/geospatial/2dsphere/create#std-label-2dsphere-index-create)

- [Query a 2dsphere Index](/docs/manual/core/indexes/index-types/geospatial/2dsphere/query#std-label-2dsphere-index-query)

- [Create a 2d Index](/docs/manual/core/indexes/index-types/geospatial/2d/create#std-label-2d-index-create)

- [Query a 2d Index](/docs/manual/core/indexes/index-types/geospatial/2d/query#std-label-2d-index-query)

## Details

This section describes details about geospatial indexes.

### Sharded Collections

You can't use a geospatial index as a [shard key](/docs/manual/reference/glossary#std-term-shard-key) when sharding a collection. However, you can create a geospatial index on a sharded collection using a different field as the shard key.

You can use geospatial [query operators](/docs/manual/geospatial-queries#std-label-geospatial-operators) and [aggregation stages](/docs/manual/geospatial-queries#std-label-geospatial-aggregation) to query for geospatial data on sharded collections.

### Covered Queries

Geospatial indexes can't [cover a query.](/docs/manual/core/query-optimization#std-label-covered-queries)

### Spherical Queries

Using a `2d` index for queries on spherical data can return incorrect results or an error. For example, `2d` indexes don't support spherical queries that wrap around the poles.

However, you can use the `2dsphere` index for both spherical queries *and* two-dimensional queries. For two-dimensional queries, the `2dsphere` index converts data stored as legacy coordinate pairs to the [GeoJSON Point](/docs/manual/reference/geojson#std-label-geojson-point) type.

## Learn More

For sample geospatial query operations, see [Geospatial Query Examples.](/docs/manual/geospatial-queries#std-label-geospatial-query-examples)
