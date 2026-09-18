> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Create an Index on an Embedded Document

You can create indexes on embedded documents as a whole. However, only queries that specify the **entire** embedded document use the index. Queries on a specific field within the document do not use the index.

## About this Task

- To utilize an index on an embedded document, your query must specify the entire embedded document. This can lead to unexpected behaviors if your schema model changes and you add or remove fields from your indexed document.

- When you query embedded documents, the order that you specify fields in the query matters. The embedded documents in your query and returned document must match exactly. To see examples of queries on embedded documents, see [Query on Embedded/Nested Documents.](/docs/manual/tutorial/query-embedded-documents#std-label-read-operations-subdocuments)

- Before you create an index on an embedded document, consider if you should instead index specific fields in that document, or use a [wildcard index](/docs/manual/core/indexes/index-types/index-wildcard#std-label-wildcard-index-core) to index all of the document's subfields.

## Before you Begin

Create a `students` collection that contains the following documents:

```javascript
db.students.insertMany( [
   {
      "name": "Alice",
      "gpa": 3.6,
      "location": { city: "Sacramento", state: "California" }
   },
   {
      "name": "Bob",
      "gpa": 3.2,
      "location": { city: "Albany", state: "New York" }
   }
] )
```

## Steps

Create an index on the `location` field:

```javascript
db.students.createIndex( { location: 1 } )
```

## Results

The following query uses the index on the `location` field:

```javascript
db.students.find( { location: { city: "Sacramento", state: "California" } } )
```

The following queries *do not* use the index on the `location` field because they query on specific fields within the embedded document:

```javascript
db.students.find( { "location.city": "Sacramento" } )

db.students.find( { "location.state": "New York" } )
```

In order for a [dot notation](/docs/manual/reference/glossary#std-term-dot-notation) query to use an index, you must create an index on the specific embedded field you are querying, not the entire embedded object. For an example, see [Create an Index on an Embedded Field.](/docs/manual/core/indexes/index-types/index-single/create-single-field-index#std-label-index-embedded-fields)

The following query returns no results because the embedded fields in the query predicate are specified in a different order than they appear in the document:

```javascript
db.students.find( { location: { state: "California", city: "Sacramento" } } )
```

## Learn More

- [Single Field Indexes](/docs/manual/core/indexes/index-types/index-single#std-label-indexes-single-field)

- [Analyze Query Performance](/docs/manual/tutorial/evaluate-operation-performance#std-label-server-diagnose-queries)

- [Query Optimization](/docs/manual/core/query-optimization#std-label-optimize-query-performance)
