> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Multikey Indexes

Multikey indexes collect and sort data from fields containing array values. These indexes improve performance for queries on array fields.

You do not need to explicitly specify an index as multikey. If you create an index on a field that contains an array value, MongoDB automatically creates the index as a multikey index.

For each distinct value in the array, MongoDB creates a separate entry in the index, and each entry points back to the same document. As a result, a single document can have multiple entries in a multikey index. If an array contains multiple instances of the same value, the index only includes one entry for the value.

MongoDB can create multikey indexes over arrays that hold both scalar values (for example, strings and numbers) and embedded documents.

To create a multikey index, use the following prototype:

```javascript
db.<collection>.createIndex( { <arrayField>: <sortOrder> } )
```

This image shows a multikey index on the `addr.zip` field:

![Diagram of a multikey index on addr.zip where addr is an array containing the zip field.](/images/index-multikey.bakedsvg.svg)

You can [create and manage multikey indexes in the UI](https://www.mongodb.com/docs/atlas/atlas-ui/indexes/) for deployments hosted in [MongoDB Atlas.](https://www.mongodb.com/docs/atlas)

## Use Cases

If your application frequently queries a field that contains an array value, a multikey index improves performance for those queries.

For example, documents in a `movies` collection contain a `genres` field: an array of genres associated with each movie. You regularly query movies that have specific genres, such as finding all movies that are both `Drama` and `Action`.

You can create an index on the `genres` field to improve performance for this query. Because `genres` contains an array value, MongoDB stores the index as a multikey index.

## Get Started

To create a multikey index, see:

- [Create an Index on an Array Field](/docs/manual/core/indexes/index-types/index-multikey/create-multikey-index-basic#std-label-index-create-multikey-scalar)

- [Create an Index on an Embedded Field in an Array](/docs/manual/core/indexes/index-types/index-multikey/create-multikey-index-embedded#std-label-index-create-multikey-embedded)

## Details

This section describes technical details and limitations for multikey indexes.

The examples on this page use data from the [sample\_mflix sample dataset](/docs/manual/sample-data/sample-mflix#std-label-sample-mflix). For details on how to load this dataset into your self-managed MongoDB deployment, see [Load the sample dataset](/docs/manual/sample-data/load-sample-data-local#std-label-sample-dataset-local). If you made any modifications to the sample databases, you may need to drop and recreate the databases to run the examples on this page.

### Index Bounds

The bounds of an index scan define the parts of an index to search during a query. The computation of multikey index bounds follows special rules. For details, see [Multikey Index Bounds.](/docs/manual/core/indexes/index-types/index-multikey/multikey-index-bounds#std-label-indexes-multikey-bounds)

### Unique Multikey Indexes

In a [unique](/docs/manual/core/index-unique#std-label-index-type-unique) multikey index, a document may have array elements that result in repeating index key values as long as the index key values for that document do not duplicate those of another document.

To learn more and see an example of this behavior, see [Unique Constraint Across Separate Documents.](/docs/manual/core/index-unique#std-label-unique-separate-documents)

### Compound Multikey Indexes

In a [compound](/docs/manual/core/indexes/index-types/index-compound#std-label-index-type-compound) multikey index, each indexed document can have *at most* one indexed field whose value is an array. Specifically:

- You cannot create a compound multikey index if more than one field in the index specification is an array.

- If a compound multikey index already exists, you cannot insert a document that would violate this restriction.

For example, you can create a compound multikey index `{ genres: 1, year: 1
}` on the `movies` collection because for each document, only one field indexed by the compound multikey index is an array. No document contains array values for both `genres` and `year` fields.

However, after you create the compound multikey index, if you attempt to insert a document where both `genres` and `year` fields are arrays, the insert fails.

### Sorting

When you sort based on an array field that is indexed with a [multikey index](/docs/manual/core/indexes/index-types/index-multikey#std-label-index-type-multikey), the query plan includes an [in-memory sort](/docs/manual/reference/glossary#std-term-in-memory-sort) stage unless both of the following are true:

- The index [boundaries](/docs/manual/core/indexes/index-types/index-multikey/multikey-index-bounds#std-label-multikey-index-bounds-intersecting) for all sort fields are `[MinKey, MaxKey]`.

- No boundaries for any multikey-indexed field have the same path prefix as the sort pattern.

### Shard Keys

You cannot specify a multikey index as a shard key index.

However, if the shard key index is a [prefix](/docs/manual/core/indexes/index-types/index-compound#std-label-compound-index-prefix) of a compound index, the compound index may become a compound *multikey* index if one of the trailing keys (that are not part of the shard key) indexes an array.

### Hashed Indexes

[Hashed indexes](/docs/manual/core/indexes/index-types/index-hashed#std-label-index-type-hashed) cannot be multikey.

### Covered Queries

Multikey indexes can cover queries when these conditions are met:

- The query does not return the array field (meaning the array is not included in the query projection). This means that to cover a query, the multikey index must be [compound.](/docs/manual/core/indexes/index-types/index-multikey#std-label-compound_multikey_indexes)

- The query does not include [`$elemMatch`.](/docs/manual/reference/operator/query/elemMatch#mongodb-query-op.-elemMatch)

- The query meets all other [covered query requirements.](/docs/manual/core/query-optimization#std-label-covered-queries)

For example, the following operation creates a compound multikey index on the `movies` collection on the `genres` and `title` fields:

```javascript
db.movies.createIndex( { genres: 1, title: 1 } )
```

The preceding index is multikey because the `genres` field contains array values.

The index covers these queries:

```javascript
db.movies.find(
   { genres: 'Drama' },
   { _id: 0, title: 1 }
).sort({ genres: 1 }).limit(5)
```

```javascript
db.movies.find(
   { title: 'The Ace of Hearts', genres: 'Drama' },
   { _id: 0, title: 1 }
)

```

The index does not cover the following query because the projection contains the `genres` array field:

```javascript
db.movies.find(
   { genres: 'Drama' },
   { _id: 0, genres: 1 }
).limit(5)
```

### Query on an Array Field as a Whole

When a query specifies an [exact match for an array as a whole](/docs/manual/tutorial/query-arrays#std-label-array-match-exact), MongoDB uses the multikey index to locate documents that contain the first element of that array. However, it cannot match the entire array using the index alone. MongoDB then fetches the candidate documents and filters them to return only those whose array exactly matches the query array.

For example, the following operation creates a multikey index on the `movies` collection on the `genres` field:

```javascript
db.movies.createIndex( { genres: 1 } )
```

The following query looks for documents where the `genres` field is the array `[ "Drama" ]`:

```javascript
db.movies.find( { genres: 'Drama' }, { title: 1, genres: 1 } ).limit(5)
```

MongoDB can use the multikey index to find documents that have `"Drama"` at any position in the `genres` array. Then, MongoDB retrieves these documents and filters for documents whose `genres` array equals the query array `[ "Drama" ]`.

### $expr

The [`$expr`](/docs/manual/reference/operator/query/expr#mongodb-query-op.-expr) operator does not support multikey indexes.

## Learn More

- To learn how MongoDB combines multikey index bounds to improve performance, see [Multikey Index Bounds.](/docs/manual/core/indexes/index-types/index-multikey/multikey-index-bounds#std-label-indexes-multikey-bounds)

- To learn how to query array fields, see:

  - [Query an Array](/docs/manual/tutorial/query-arrays#std-label-read-operations-arrays)

  - [Query an Array of Embedded Documents](/docs/manual/tutorial/query-array-of-documents#std-label-array-match-embedded-documents)
