> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Assign Weights to $text Query Results on Self-Managed Deployments

**Note:**

[MongoDB Search](https://www.mongodb.com/docs/atlas/atlas-search/) offers advanced full-text search capabilities, including improved [relevance scoring](https://www.mongodb.com/docs/search/query/score/customize-score/#std-label-fts-customize-score) and [score boosting](https://www.mongodb.com/docs/search/query/score/modify-score/#std-label-scoring-boost). We recommend using the [`$search`](https://www.mongodb.com/docs/search/query/aggregation-stages/search/#mongodb-pipeline-pipe.-search) stage with the `score` field, instead of the [`$text`](/docs/manual/reference/operator/query/text#mongodb-query-op.-text) operator, to assign and sort text search results based on relevance scores.

When MongoDB returns results for `$text` queries, it assigns a **score** to each returned document. The score indicates the relevance of the document to a given search query. You can sort returned documents by score to have the most relevant documents appear first in the result set.

If you have a [compound index](/docs/manual/core/indexes/index-types/index-compound#std-label-index-type-compound) with multiple text index keys, you can specify different **weights** for each indexed field. The weight of an indexed field indicates the significance of the field relative to the other indexed fields, with higher weights resulting in higher scores.

For example, you can emphasize search matches on a `title` field if you know users are likely to search for titles, or if `title` contains more relevant search terms compared to other document fields.

The default weight for indexed fields is 1. To adjust the weights for the indexed fields, include the weights option in the [`db.collection.createIndex()`](/docs/manual/reference/method/db.collection.createIndex#mongodb-method-db.collection.createIndex) method, as seen in this example:

```javascript
db.<collection>.createIndex(
   {
     <field1>: "text",
     <field2>: "text",
     ...
   },
   {
     weights: {
       <field1>: <weight>,
       <field2>: <weight>,
       ...
     },
     name: <indexName>
   }
 )
```

**Important:**

If you change the weights in your index after it is created, MongoDB needs to reindex the collection. Reindexing can negatively impact performance, especially on large collections. For more information, see [Index Builds on Populated Collections.](/docs/manual/core/index-creation#std-label-index-creation-background)

## About this Task

You have a `blog` collection that contains documents for individual blog posts. Each document contains:

- The content of the post.

- The topic that the post covers.

- A list of keywords related to the post.

You want to create a text index so users can perform `$text` queries on blog posts. Your application supports searches on content, topics, and keywords.

You want to prioritize matches on the `content` field over other document fields. Use index weights to assign greater importance to matches on `content` and sort query results so `content` matches appear first.

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

Create a `text` index with different weights for each indexed field:

```javascript
db.blog.createIndex(
   {
     content: "text",
     keywords: "text",
     about: "text"
   },
   {
     weights: {
       content: 10,
       keywords: 5
     },
     name: "BlogTextIndex"
   }
 )
```

The `text` index has the following fields and weights:

- `content` has a weight of 10.

- `keywords` has a weight of 5.

- `about` has the default weight of 1.

These weights indicate the relative significance of the indexed fields to each other.

## Results

The following examples show how different weights for indexed fields affect result scores. Each example sorts results based on the `textScore` of each document. To access documents' `textScore` attributes, use the [`$meta`](/docs/manual/reference/operator/aggregation/meta#mongodb-expression-exp.-meta) operator.

### Matches in `content` and `about` Fields

The following query searches documents in the `blog` collection for the string `ice cream`:

```javascript
db.blog.find(
   {
      $text: { $search: "ice cream" }
   },
   {
      score: { $meta: "textScore" }
   }
).sort( { score: { $meta: "textScore" } } )
```

Output:

```javascript
[
  {
    _id: 2,
    content: 'Who likes chocolate ice cream for dessert?',
    about: 'food',
    keywords: [ 'food', 'poll' ],
    score: 12
  },
  {
    _id: 3,
    content: 'My favorite flavors are strawberry and coffee',
    about: 'ice cream',
    keywords: [ 'food', 'dessert' ],
    score: 1.5
  }
]
```

The search string `ice cream` matches:

- The `content` field in the document with `_id: 2`.

- The `about` field in the document with `_id: 3`.

A term match in the `content` field has `10` times the impact (`10:1` weight) as a term match in the `keywords` field.

### Matches in `keywords` and `about` Fields

The following query searches documents in the `blog` collection for the string `food`:

```javascript
db.blog.find(
   {
      $text: { $search: "food" }
   },
   {
      score: { $meta: "textScore" }
   }
).sort( { score: { $meta: "textScore" } } )
```

Output:

```javascript
[
  {
    _id: 3,
    content: 'My favorite flavors are strawberry and coffee',
    about: 'ice cream',
    keywords: [ 'food', 'dessert' ],
    score: 5.5
  },
  {
    _id: 2,
    content: "Who likes chocolate ice cream for dessert?",
    about: 'food',
    keywords: [ 'poll' ],
    score: 1.1
  }
]
```

The search string `food` matches:

- The `keywords` field in the document with `_id: 3`.

- The `about` field in the document with `_id: 2`.

A term match in the `keywords` field has `5` times  the impact (`5:1` weight) as a term match in the `about` field.

### Multiple Matches in a Single Document

The following query searches documents in the `blog` collection for the string `coffee`:

```javascript
db.blog.find(
   {
      $text: { $search: "coffee" }
   },
   {
      score: { $meta: "textScore" }
   }
).sort( { score: { $meta: "textScore" } } )
```

Output:

```javascript
[
  {
    _id: 1,
    content: 'This morning I had a cup of coffee.',
    about: 'beverage',
    keywords: [ 'coffee' ],
    score: 11.666666666666666
  },
  {
    _id: 3,
    content: 'My favorite cake flavors are strawberry and coffee',
    about: 'ice cream',
    keywords: [ 'food', 'dessert' ],
    score: 6
  }
]
```

The search string `coffee` matches:

- The `content` and `keywords` fields in the document with `_id:
  1`.

- The `content` field in the document with `_id: 3`.

To calculate the `score` when a search string matches multiple fields, MongoDB multiplies the number of matches by the weight for the corresponding field and sums the results.

## Learn More

To learn more about `$text` queries in MongoDB, see:

- [$text Queries](/docs/manual/core/text-search/on-prem#std-label-perform-text-search-onprem)

- [$text Query Operators](/docs/manual/core/text-search-operators#std-label-text-search-operators-onprem)

- [$text Query Languages on Self-Managed Deployments](/docs/manual/reference/text-search-languages#std-label-text-search-languages)

- [`$meta`](/docs/manual/reference/operator/aggregation/meta#mongodb-expression-exp.-meta)

**Note: MongoDB Search**

For data hosted on MongoDB, [MongoDB Search](https://www.mongodb.com/docs/atlas/atlas-search/) provides more robust custom scoring than `text` indexes. To learn more, see the MongoDB Search [Scoring](https://www.mongodb.com/docs/atlas/reference/atlas-search/scoring/) documentation.
