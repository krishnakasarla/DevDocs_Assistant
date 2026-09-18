> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Index Types

This page describes the types of indexes you can create in MongoDB. Different index types support different types of data and queries.

## Single Field Index

Single field indexes collect and sort data from a single field in each document in a collection.

This image shows an index on a single field, `score`:

![Diagram of an index on the \`\`score\`\` field (ascending).](/images/index-ascending.bakedsvg.svg)

To learn more, see [Single Field Indexes.](/docs/manual/core/indexes/index-types/index-single#std-label-indexes-single-field)

## Compound Index

Compound indexes collect and sort data from multiple field values from each document in a collection. You can use the compound index to query the first field or any prefix fields of the index. The order of fields in a compound index is very important. The B-tree created by a compound index stores the sorted data in the order that the index specifies the fields.

For example, the following image shows a compound index where documents are first sorted by `userid` in ascending order (alphabetically). Then, the `scores` for each `userid` are sorted in descending order:

![Diagram of a compound index on userid (ascending) and score (descending), sorted by userid first.](/images/index-compound-key.bakedsvg.svg)

To learn more, see [Compound Indexes.](/docs/manual/core/indexes/index-types/index-compound#std-label-index-type-compound)

## Multikey Index

Multikey indexes collect and sort data stored in arrays.

This image shows a multikey index on the `addr.zip` field:

![Diagram of a multikey index on addr.zip where addr is an array containing the zip field.](/images/index-multikey.bakedsvg.svg)

To learn more, see [Multikey Indexes.](/docs/manual/core/indexes/index-types/index-multikey#std-label-index-type-multikey)

## Wildcard Index

Wildcard indexes apply to collections with flexible schemas, where document field names may differ. Use wildcard indexes to support queries against arbitrary or unknown field names.

To learn more, see [Wildcard Indexes.](/docs/manual/core/indexes/index-types/index-wildcard#std-label-wildcard-index-core)

## Geospatial Index

Geospatial indexes improve performance for queries on geospatial coordinate data. To learn more, see [Geospatial Indexes.](/docs/manual/core/indexes/index-types/index-geospatial#std-label-geospatial-index)

## Hashed Index

Hashed indexes support [hashed sharding](/docs/manual/core/hashed-sharding#std-label-sharding-hashed-sharding). Hashed indexes index the hash of a field's value.

To learn more, see [Hashed Indexes.](/docs/manual/core/indexes/index-types/index-hashed#std-label-index-type-hashed)

## Text Index

Text indexes support `$text` queries on fields containing string content.

To learn more, see [Text Indexes on Self-Managed Deployments.](/docs/manual/core/indexes/index-types/index-text#std-label-index-type-text)

**Note: Use MongoDB Search or MongoDB Vector Search**

MongoDB also offers the following text search solutions:

- [MongoDB Search](https://www.mongodb.com/docs/atlas/atlas-search/) provides improved performance and functionality compared to on-premises text search.

- [MongoDB Vector Search](https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-overview/) provides vector search capabilities to perform semantic, hybrid, and generative search.

## Clustered Index

Clustered indexes specify the order in which [clustered collections](/docs/manual/core/clustered-collections#std-label-clustered-collections) store data. Collections created with a clustered index are called clustered collections.

To learn how to create a collection with a clustered index, see [Date Clustered Index Key Example.](/docs/manual/core/clustered-collections#std-label-clustered-collections-index-example)
