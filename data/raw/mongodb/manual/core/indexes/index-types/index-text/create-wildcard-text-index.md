> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Create a Wildcard Text Index on Self-Managed Deployments

**Note:**

[MongoDB Search](https://www.mongodb.com/docs/atlas/atlas-search/) offers advanced full-text search capabilities, including [configurable dynamic indexing](https://www.mongodb.com/docs/search/indexes/define-field-mappings/#std-label-fts-configure-dynamic-mappings). We recommend using [MongoDB Search indexes](https://www.mongodb.com/docs/search/indexes/manage-indexes/#std-label-fts-manage-indexes) instead of text indexes.

You can create a text index that contains every document field with string data in a collection. These text indexes are called **wildcard
text indexes**. Wildcard text indexes support [`$text`](/docs/manual/reference/operator/query/text#mongodb-query-op.-text) [queries](/docs/manual/core/text-search/on-prem#std-label-text-search-on-prem) on unknown, arbitrary, or dynamically generated fields.

To create a wildcard text index, set the index key to the wildcard specifier (`$**`) and set the index value to `text`:

```javascript
db.<collection>.createIndex( { "$**": "text" } )
```

## About this Task

Wildcard text indexes are distinct from [wildcard indexes](/docs/manual/core/indexes/index-types/index-wildcard#std-label-wildcard-index-core). Wildcard text indexes support queries that use the [`$text`](/docs/manual/reference/operator/query/text#mongodb-query-op.-text) operator, while wildcard indexes do not.

**Note:**

`$text` provides text query capabilities for self-managed (non-Atlas) deployments. For data hosted on MongoDB, MongoDB also offers an improved full-text query solution, [MongoDB Search.](https://www.mongodb.com/docs/atlas/atlas-search/)

After you create a wildcard text index, when you insert or update documents, the index updates to include any new string field values. As a result, wildcard text indexes negatively impact performance for inserts and updates.

Only use wildcard text indexes when the fields you want to index are unknown or may change. Wildcard text indexes don't perform as well as targeted text indexes on specific fields. If your collection contains arbitrary field names that prevent targeted indexes, consider remodeling your schema to have consistent field names. To learn more about targeted indexes, see [Create Indexes to Support Your Queries.](/docs/manual/data-modeling/schema-design-process/create-indexes#std-label-create-indexes-to-support-queries)

## Before You Begin

Create a `blog` collection with the following documents:

```javascript
db.blog.insertMany( [
   {
     _id: 1,
     content: "This morning I had a cup of coffee.",
     about: "beverage",
     keywords: [ "coffee" ]
   },
   {
     _id: 2,
     content: "Who likes chocolate ice cream for dessert?",
     about: "food",
     keywords: [ "poll" ]
   },
   {
     _id: 3,
     content: "My favorite flavors are strawberry and coffee",
     about: "ice cream",
     keywords: [ "food", "dessert" ]
   }
] )
```

## Procedure

Create a wildcard text index on the `blog` collection:

```javascript
db.blog.createIndex( { "$**": "text" } )
```

## Results

The wildcard text index supports `$text` queries on all fields in the collection. Consider the following queries:

### Search for a Single Word

Query the `blog` collection for the string `coffee`:

```javascript
db.blog.find( { $text: { $search: "coffee" } } )
```

Output:

```javascript
[
  {
    _id: 1,
    content: 'This morning I had a cup of coffee.',
    about: 'beverage',
    keywords: [ 'coffee' ]
  },
  {
    _id: 3,
    content: 'My favorite flavors are strawberry and coffee',
    about: 'ice cream',
    keywords: [ 'food', 'dessert' ]
  }
]
```

The preceding query returns all documents that contain the string `coffee` in any field.

### Search for Multiple Terms

Query the `blog` collection for documents that contain the string `poll` **or** `coffee`:

```javascript
db.blog.find( { $text: { $search: "poll coffee" } } )
```

Output:

```javascript
[
  {
    _id: 1,
    content: 'This morning I had a cup of coffee.',
    about: 'beverage',
    keywords: [ 'coffee' ]
  },
  {
    _id: 3,
    content: 'My favorite flavors are strawberry and coffee',
    about: 'ice cream',
    keywords: [ 'food', 'dessert' ]
  },
  {
    _id: 2,
    content: 'Who likes chocolate ice cream for dessert?',
    about: 'food',
    keywords: [ 'poll' ]
  }
]
```

The preceding query returns documents that contain the string `poll` or `coffee` in any field.

### Search for an Exact String

Query the `blog` collection for documents that contain the exact string `chocolate ice cream`:

```javascript
db.blog.find( { $text: { $search: "\"chocolate ice cream\"" } } )
```

Output:

```javascript
[
  {
    _id: 2,
    content: 'Who likes chocolate ice cream for dessert?',
    about: 'food',
    keywords: [ 'poll' ]
  }
]
```

The preceding query returns documents that contain the exact string `chocolate ice cream` in any field.

## Learn More

- To learn how to control the ranking of `$text` query results, see [Assign Weights to $text Query Results on Self-Managed Deployments.](/docs/manual/core/indexes/index-types/index-text/control-text-search-results#std-label-specify-weights)

- You can include a wildcard text index as part of a compound text index. To learn more about compound text indexes, see [Create a Compound Text Index.](/docs/manual/core/indexes/index-types/index-text/create-text-index#std-label-compound-text-index-example)

- To see examples of `$text` queries, see [`$text`.](/docs/manual/reference/operator/query/text#mongodb-query-op.-text)

  **Note:**

  `$text` provides text query capabilities for self-managed (non-Atlas) deployments. For data hosted on MongoDB, MongoDB also offers an improved full-text query solution, [MongoDB Search.](https://www.mongodb.com/docs/atlas/atlas-search/)

- To learn about text index properties such as case sensitivity, see [Text Index Properties on Self-Managed Deployments.](/docs/manual/core/indexes/index-types/index-text/text-index-properties#std-label-text-index-properties)
