> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# $text Queries

**Note:**

MongoDB offers an improved full-text search solution, [MongoDB Search](https://www.mongodb.com/docs/atlas/atlas-search/), and semantic search solution, [MongoDB Vector Search](https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-overview/). We recommend using the [`$search`](https://www.mongodb.com/docs/search/query/aggregation-stages/search/#mongodb-pipeline-pipe.-search), [`$searchMeta`](https://www.mongodb.com/docs/search/query/aggregation-stages/searchMeta/#mongodb-pipeline-pipe.-searchMeta), or [`$vectorSearch`](/docs/manual/reference/operator/aggregation/vectorSearch#mongodb-expression-exp.-vectorSearch) stages, instead of the `$text` operator.

To run `$text` queries, you must have a [text index](/docs/manual/core/indexes/index-types/index-text#std-label-index-feature-text) on your collection. MongoDB provides text indexes to support `$text` queries on string content. Text indexes can include any field whose value is a string or an array of string elements. A collection can only have **one** text index, but that index can cover multiple fields.

See the [Text Indexes on Self-Managed Deployments](/docs/manual/core/indexes/index-types/index-text#std-label-index-type-text) section for a full reference on text indexes, including behavior, tokenization, and properties.

## Examples

This example demonstrates how to build a text index and use it to find coffee shops, given only text fields.

### Create a Collection

Create a collection `stores` with the following documents:

```javascript
db.stores.insertMany(
   [
     { _id: 1, name: "Java Hut", description: "Coffee and cakes" },
     { _id: 2, name: "Burger Buns", description: "Gourmet hamburgers" },
     { _id: 3, name: "Coffee Shop", description: "Just coffee" },
     { _id: 4, name: "Clothes Clothes Clothes", description: "Discount clothing" },
     { _id: 5, name: "Java Shopping", description: "Indonesian goods" },
     { _id: 6, name: "NYC_Coffee Shop", description: "local NYC coffee" }
   ]
)
```

### Create a Text Index

Run the following in [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) to allow `$text` queries over the `name` and `description` fields:

```javascript
db.stores.createIndex( { name: "text", description: "text" } )
```

### Search for an Exact String

You can search for exact multi-word strings by wrapping them in double-quotes. `$text` queries only match documents that include the whole string.

For example, the following query finds all documents that contain the string "coffee shop":

```javascript
db.stores.find( { $text: { $search: "\"coffee shop\"" } } )
```

This query returns the following documents:

```javascript
[
   { _id: 3, name: 'Coffee Shop', description: 'Just coffee' },
   { _id: 6, name: 'NYC_Coffee Shop', description: 'local NYC coffee' }
]
```

Unless specified, exact string search is not case sensitive or diacritic sensitive. For example, the following query returns the same results as the previous query:

```javascript
db.stores.find( { $text: { $search: "\"COFFEé SHOP\"" } } )
```

Exact string search does not handle stemming or stop words.

### Exclude a Term

To exclude a word, you can prepend a "`-`" character. For example, to find all stores containing "java" or "shop" but not "coffee", use the following:

```javascript
db.stores.find( { $text: { $search: "java shop -coffee" } } )
```

### Sort the Results

MongoDB returns its results in unsorted order by default. However, `$text` queries compute a relevance score for each document that specifies how well a document matches the query.

To sort the results in order of relevance score, you must explicitly project the [`$meta`](/docs/manual/reference/operator/aggregation/meta#mongodb-expression-exp.-meta) `textScore` field and sort on it:

```javascript
db.stores.find(
   { $text: { $search: "java coffee shop" } },
   { score: { $meta: "textScore" } }
).sort( { score: { $meta: "textScore" } } )
```

`$text` is also available in the aggregation pipeline.
