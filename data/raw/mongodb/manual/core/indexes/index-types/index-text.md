> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Text Indexes on Self-Managed Deployments

**Note:**

MongoDB offers an improved full-text search solution, [MongoDB Search](https://www.mongodb.com/docs/atlas/atlas-search/), and vector search solution, [MongoDB Vector Search](https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-overview/). We recommend using [MongoDB Search indexes](https://www.mongodb.com/docs/search/indexes/manage-indexes/#std-label-fts-manage-indexes) or [MongoDB Vector Search indexes](https://www.mongodb.com/docs/vector-search/indexes/vector-search-type/#std-label-avs-types-vector-search)  instead of text indexes.

Text indexes support [`$text`](/docs/manual/reference/operator/query/text#mongodb-query-op.-text) [queries](/docs/manual/text-search#std-label-text-query) on fields that contain string content. They also support [aggregation expressions](/docs/manual/reference/mql/expressions#std-label-qe-aggregation-operators) for encrypted string fields in [Queryable Encryption](/docs/manual/core/queryable-encryption#std-label-qe-manual-feature-qe) enabled collections. Text indexes improve performance when you search for specific words or strings within string content.

A collection can have only **one** text index, but that index may include multiple fields.

To create a text index, use the following prototype:

```javascript
db.<collection>.createIndex(
   {
      <field1>: "text",
      <field2>: "text",
      ...
   }
)
```

## Support for the $text Operator

Text indexes support [`$text`](/docs/manual/reference/operator/query/text#mongodb-query-op.-text) query operations on on-premises deployments. To use `$text`, you must create a text index.

## $encStr Support

Text indexes support [aggregation expressions](/docs/manual/reference/mql/expressions#std-label-qe-aggregation-operators) for fields in Queryable Encryption collections with prefix, suffix, or substring queries enabled. A text index is required to use the [`$encStrNormalizedEq`](/docs/manual/reference/operator/aggregation/encStrNormalizedEq#mongodb-expression-exp.-encStrNormalizedEq) expression.

## Use Cases

An online shop's `clothing` collection has a `description` field that contains a string of text describing each item. To find clothes made of `"silk"`, create a text index on `description` and run a `$text` query for `"silk"`. The search returns all documents mentioning `"silk"` in `description`.

## Get Started

To learn how to create and use text indexes, see:

- [Create a Text Index on Self-Managed Deployments](/docs/manual/core/indexes/index-types/index-text/create-text-index#std-label-create-text-index)

- [Create a Wildcard Text Index on Self-Managed Deployments](/docs/manual/core/indexes/index-types/index-text/create-wildcard-text-index#std-label-create-wildcard-text-index)

- [Specify Language for Text Indexes on Self-Managed MongoDB](/docs/manual/core/indexes/index-types/index-text/specify-text-index-language#std-label-specify-default-text-index-language)

- [Limit Text Index Entries Scanned on Self-Managed Deployments](/docs/manual/core/indexes/index-types/index-text/limit-number-of-items-scanned-for-text-search#std-label-limit-entries-scanned)

## Details

This section describes text index details.

### Compound Text Indexes

In a compound index with a text index key and other key types, only the text index field determines whether the index references a document. Other keys do not affect document references.

### Covered Queries

Text indexes can't [cover a query.](/docs/manual/core/query-optimization#std-label-covered-queries)

### `sparse` Property

Text indexes are always [sparse](/docs/manual/core/index-sparse#std-label-index-type-sparse). MongoDB ignores the `sparse` option when creating text indexes.

MongoDB does not add a text index entry for documents that lack the text index field, have null values, or have empty arrays.

### Storage Requirements and Performance Costs

Text indexes have these storage and performance characteristics:

- Text indexes can consume significant RAM. They contain one index entry for each unique stemmed word in each indexed field for each document.

- Building a text index is similar to building a large [multikey index](/docs/manual/core/indexes/index-types/index-multikey#std-label-index-type-multi-key) but takes longer than building an ordered (scalar) index on the same data.

- When building large text indexes, ensure sufficient file descriptor limits. See [recommended settings.](/docs/manual/reference/ulimit#std-label-ulimit)

- Text indexes impact write performance because MongoDB must add an index entry for each unique stemmed word in each indexed field of new documents.

- Text indexes store individual words, not multi-word strings or word proximity information. Queries with multiple words run faster when the entire collection fits in RAM.

## Learn More

- To learn more about text indexes, see:

  - [Assign Weights to $text Query Results on Self-Managed Deployments](/docs/manual/core/indexes/index-types/index-text/control-text-search-results#std-label-control-text-search-results)

  - [Text Index Properties on Self-Managed Deployments](/docs/manual/core/indexes/index-types/index-text/text-index-properties#std-label-text-index-properties)

  - [Text Index Restrictions on Self-Managed Deployments](/docs/manual/core/indexes/index-types/index-text/text-index-restrictions#std-label-text-index-restrictions)

  - [Text Index Versions on Self-Managed Deployments](/docs/manual/core/indexes/index-types/index-text/text-index-versions#std-label-text-index-versions)

- For `$text` query examples, see the [`$text reference page`.](/docs/manual/reference/operator/query/text#mongodb-query-op.-text)

- For sample `$text` operations in aggregation pipelines, see [$text in the Aggregation Pipeline.](/docs/manual/tutorial/text-search-in-aggregation#std-label-text-agg)
