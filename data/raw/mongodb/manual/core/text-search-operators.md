> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# $text Query Operators

**Note:**

MongoDB offers an improved full-text search solution, [MongoDB Search](https://www.mongodb.com/docs/atlas/atlas-search/), and semantic search solution, [MongoDB Vector Search](https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-overview/). We recommend using the [`$search`](https://www.mongodb.com/docs/search/query/aggregation-stages/search/#mongodb-pipeline-pipe.-search), [`$searchMeta`](https://www.mongodb.com/docs/search/query/aggregation-stages/searchMeta/#mongodb-pipeline-pipe.-searchMeta), or [`$vectorSearch`](/docs/manual/reference/operator/aggregation/vectorSearch#mongodb-expression-exp.-vectorSearch) stages, instead of the `$text` operator.

## Query Framework

You can use the [`$text`](/docs/manual/reference/operator/query/text#mongodb-query-op.-text) operator on a collection with a [text index.](/docs/manual/core/indexes/index-types/index-text#std-label-index-type-text)

`$text` tokenizes the search string using whitespace and most punctuation as delimiters, and performs a logical `OR` of all such tokens in the search string.

For example, you could use the following query to find all stores containing any terms from the list "coffee", "shop", and "java" in the `stores` [collection:](/docs/manual/core/text-search/on-prem#std-label-text-index-eg)

```javascript
db.stores.find( { $text: { $search: "java coffee shop" } } )
```

Use the [`$meta`](/docs/manual/reference/operator/aggregation/meta#mongodb-expression-exp.-meta) query operator to obtain and sort by the relevance score of each matching document. For example, to order a list of coffee shops in order of relevance, run the following:

```javascript
db.stores.find(
   { $text: { $search: "coffee shop cake" } },
   { score: { $meta: "textScore" } }
).sort( { score: { $meta: "textScore" } } )
```

For more information on the [`$text`](/docs/manual/reference/operator/query/text#mongodb-query-op.-text) and [`$meta`](/docs/manual/reference/operator/aggregation/meta#mongodb-expression-exp.-meta) operators, including restrictions and behavior, see:

- [`$text Reference Page`](/docs/manual/reference/operator/query/text#mongodb-query-op.-text)

- [$text Query Examples](/docs/manual/reference/operator/query/text#std-label-text-query-examples)

- [$meta as a projection operator](/docs/manual/reference/operator/aggregation/meta#std-label-meta-projection-usage)

## Aggregation Pipeline

When working with [aggregation](/docs/manual/aggregation#std-label-aggregation) pipelines, use [`$match`](/docs/manual/reference/operator/aggregation/match#mongodb-pipeline-pipe.-match) with a `$text` expression. To sort the results in order of relevance score, use the [`$meta`](/docs/manual/reference/operator/aggregation/meta#mongodb-expression-exp.-meta) aggregation operator in the [`$sort`](/docs/manual/reference/operator/aggregation/sort#mongodb-pipeline-pipe.-sort) stage.

For more information and examples, see [$text in the Aggregation Pipeline.](/docs/manual/tutorial/text-search-in-aggregation#std-label-text-agg)

[MongoDB Search](https://www.mongodb.com/docs/atlas/atlas-search/) provides the [$search](https://www.mongodb.com/docs/atlas/reference/atlas-search/query-syntax/) aggregation stage to perform full-text search on your collections.
