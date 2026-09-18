> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Query Optimization

Query optimization improves the efficiency of read operations by reducing the amount of data that query operations need to process. Use indexes, projections, and query limits to enhance query performance and reduce resource consumption.

Query optimization can occur both during development and later as your data usage and demand changes. As collections grow, a periodic review of query performance can help determine when clusters need to scale up or scale out.

## Create Indexes to Support Queries

[Indexes](/docs/manual/indexes#std-label-indexes) store values from individual fields or sets of fields from a collection in a separate data structure. In read operations, they allow MongoDB to search in the index to identify relevant documents instead of the entire collection. In write operations, MongoDB must both write the change to the collection and update the index.

Create indexes for commonly issued queries. If a query searches multiple fields, create a [compound index.](/docs/manual/core/indexes/index-types/index-compound#std-label-index-type-compound)

For example, consider the following query on the `rated` field in the `movies` collection:

```javascript
let ratingValue = <someUserInput>;
db.movies.find( { rated: ratingValue } );
```

To improve performance for this query, add an index to the `movies` collection on the `rated` field.  In [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh), create indexes using the [`db.collection.createIndex()`](/docs/manual/reference/method/db.collection.createIndex#mongodb-method-db.collection.createIndex) method:

```javascript
db.movies.createIndex( { rated: 1 } )

```

To analyze query performance, see [Interpret Explain Plan Results.](/docs/manual/tutorial/analyze-query-plan)

For single-field indexes, the order of the index doesn't matter. For compound indexes, the field order impacts what queries the index supports. For details, see [Compound Index Sort Order.](/docs/manual/core/indexes/index-types/index-compound/sort-order#std-label-index-ascending-and-descending)

## Create Selective Queries

Query selectivity refers to how well the query predicate filters out documents in a collection. Query selectivity determines whether queries can use indexes effectively.

More selective queries match a smaller percentage of documents. For instance, an equality match on the unique `_id` field is highly selective as it can match at most one document.

Less selective queries match a larger percentage of documents and can't use indexes effectively.

For instance, the inequality operators [`$nin`](/docs/manual/reference/operator/query/nin#mongodb-query-op.-nin) and [`$ne`](/docs/manual/reference/operator/query/ne#mongodb-query-op.-ne) are *not* very selective since they often match a large portion of the index. As a result, in many cases, a [`$nin`](/docs/manual/reference/operator/query/nin#mongodb-query-op.-nin) or [`$ne`](/docs/manual/reference/operator/query/ne#mongodb-query-op.-ne) query with an index may perform no better than a [`$nin`](/docs/manual/reference/operator/query/nin#mongodb-query-op.-nin) or [`$ne`](/docs/manual/reference/operator/query/ne#mongodb-query-op.-ne) query that must scan all documents in a collection.

The selectivity of [`regular expressions`](/docs/manual/reference/operator/query/regex#mongodb-query-op.-regex) depends on the expressions themselves. For details, see [regular expression and index use.](/docs/manual/reference/operator/query/regex#std-label-regex-index-use)

## Project Only Necessary Data

When you need a subset of fields from documents, you can improve performance by returning only the fields you need. Projections reduce network traffic and processing time.

For example, if your query to the `movies` collection needs only the `year`, `title`, `directors`, and `plot` fields, specify those fields in the projection:

```javascript
db.movies.find(
   {},
   { year: 1, title: 1, directors: 1 }
).sort( { year: -1 } ).limit(3)

```

When you use a [`$project`](/docs/manual/reference/operator/aggregation/project#mongodb-pipeline-pipe.-project) aggregation stage it should typically be the last stage in your pipeline, used to specify which fields to return to the client.

Using a `$project` stage at the beginning or middle of a pipeline to reduce the number of fields passed to subsequent pipeline stages is unlikely to improve performance, because the database performs this optimization automatically.

For more information on using projections, see [Project Fields to Return from Query.](/docs/manual/tutorial/project-fields-from-query-results#std-label-read-operations-projection)

### Example

To achieve a covered query, you must index projected fields. The [ESR (Equality, Sort, Range) rule](/docs/manual/tutorial/equality-sort-range-guideline#std-label-esr-indexing-guideline) applies to the order of fields in the index.

For example, consider the following index on a `movies` collection:

```javascript
db.movies.createIndex(
   { rated: 1, _id: 1, "imdb.rating": 1, title: 1, released: 1 }
)

```

The preceding index, while technically correct, isn't structured to optimize query performance.

The following query uses the ESR (Equality, Sort, Range) rule to structure a more efficient aggregation pipeline and improve query response times.

```javascript
db.movies.aggregate( [
   { $match: { rated: "PG",
     released: { $gt: ISODate("2000-01-01T00:00:00Z") } } },
   { $sort: { title: 1 } },
   { $limit: 5 },
   { $project: { _id: 1, "imdb.rating": 1 } }
] )

```

The index and query follow the ESR rule:

- `rated` is used for an equality match (E), so it is the first field in the index.

- `title` is used for sorting (S), so it is after `rated` in the index.

- `released` is used for a range query (R), so it is the last field in the index.

## Limit Query Results

MongoDB [cursors](/docs/manual/reference/glossary#std-term-cursor) return results in batches. If you know the number of results you want, specify that value in the [`limit()`](/docs/manual/reference/method/cursor.limit#mongodb-method-cursor.limit) method. Limiting results reduces the demand on network resources.

Sort results before applying a limit to ensure that the query returns the expected documents. For example, if you need only 10 results from your query to the `movies` collection, run the following query:

```javascript
db.movies.find(
   {},
   { title: 1, year: 1 }
).sort( { year: -1 } ).limit(10)

```

For more information on limiting results, see [`limit()`.](/docs/manual/reference/method/cursor.limit#mongodb-method-cursor.limit)

## Use Index Hints

The [query optimizer](/docs/manual/core/query-plans#std-label-read-operations-query-optimization) typically selects the optimal index for a specific operation. However, you can force MongoDB to use a specific index using the [`hint()`](/docs/manual/reference/method/cursor.hint#mongodb-method-cursor.hint) method. Use [`hint()`](/docs/manual/reference/method/cursor.hint#mongodb-method-cursor.hint) to support performance testing or when you are querying a field that appears in several indexes to ensure that MongoDB uses the correct index.

## Use Server-Side Operations

Use the [`$inc`](/docs/manual/reference/operator/update/inc#mongodb-update-up.-inc) operator to increment or decrement values in documents. The operator increments the value of the field on the server side, as an alternative to selecting a document, making changes in the client code, and then writing the entire document to the server. The [`$inc`](/docs/manual/reference/operator/update/inc#mongodb-update-up.-inc) operator can also help avoid race conditions that occur when two application instances query for a document, manually increment a field, and save the entire document back at the same time.

## Run Covered Queries

A covered query is a query that can be satisfied entirely using an index and doesn't have to examine any documents. An index covers a query when all of the following apply:

- All the fields in the query (both as specified by the application and as needed internally such as for sharding purposes) are part of an index.

- All the fields returned in the results are in the same index.

- No fields in the query are equal to `null`. For example, the following query predicates can't result in covered queries:

  - `{ "field": null }`

  - `{ "field": { $eq: null } }`

### Example

A `movies` collection has the following index on the `rated` and `title` fields:

```javascript
db.movies.createIndex( { rated: 1, title: 1 } )

```

The index covers the following operation which queries on the `rated` and `title` fields and returns only the `title` field:

```javascript
db.movies.find(
   { rated: "PG", title: /^T/ },
   { title: 1, _id: 0 }
).limit(3)

```

For the specified index to cover the query, the projection document must explicitly specify `_id: 0` to exclude the `_id` field from the result since the index doesn't include the `_id` field.

### Embedded Documents

An index can cover a query on fields within embedded documents.

For example, consider the `theaters` collection from the [sample\_mflix](https://www.mongodb.com/docs/atlas/sample-data/sample-mflix/) dataset, which has documents with the following structure:

```javascript
{
  theaterId: <num>,
  location: {
    address: {
      street1: "<address>",
      city: "<city>",
      state: "<state>",
      zipcode: "<zip>"
    },
    geo: { ... }
  }
}
```

The collection has the following index:

```javascript
db.theaters.createIndex( { "location.address.city": 1 } )

```

The `{ "location.address.city": 1 }` index covers the following query:

```javascript
db.theaters.find(
   { "location.address.city": "Portland" },
   { "location.address.city": 1, _id: 0 }
).limit(1)

```

**Note:**

To index fields in embedded documents, use [dot notation](/docs/manual/reference/glossary#std-term-dot-notation). See [Create an Index on an Embedded Field.](/docs/manual/core/indexes/index-types/index-single/create-single-field-index#std-label-index-embedded-fields)

### Multikey Covering

Multikey indexes can cover queries over the non-array fields if the index tracks which field or fields cause the index to be multikey.

[Multikey indexes](/docs/manual/core/indexes/index-types/index-multikey#std-label-index-type-multikey) cannot cover queries over array fields.

For an example of a covered query with a multikey index, see [Covered Queries](/docs/manual/core/indexes/index-types/index-multikey#std-label-multikey-covered-queries) on the multikey indexes page.

### Performance

Because the index contains all fields required by the query, MongoDB can both match the [query conditions](/docs/manual/tutorial/query-documents#std-label-read-operations-query-document) and return the results using only the index.

Querying *only* the index can be much faster than querying documents outside of the index. Index keys are typically smaller than the documents they catalog, and indexes are typically available in RAM or located sequentially on disk.

### Limitations

#### Index Types

Not all [index types](/docs/manual/core/indexes/index-types#std-label-index-types) can cover queries. For details on covered index support, refer to the documentation page for the corresponding index type.

#### Sharded Collections

When run on [`mongos`](/docs/manual/reference/program/mongos#std-program-mongos), indexes can only cover queries on [sharded](/docs/manual/reference/glossary#std-term-shard) collections if the index contains the shard key.

### Explain Results

To determine whether a query is a covered query, use the [`db.collection.explain()`](/docs/manual/reference/method/db.collection.explain#mongodb-method-db.collection.explain) or the [`explain()`](/docs/manual/reference/method/cursor.explain#mongodb-method-cursor.explain) method. See [Covered Queries.](/docs/manual/reference/explain-results#std-label-explain-output-covered-queries)
