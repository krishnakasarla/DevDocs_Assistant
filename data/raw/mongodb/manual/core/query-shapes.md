> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Query Shapes

**Changed in version 8.0**

A query shape is a set of specifications that group similar queries together. Specifications can include filters, sorts, projections, aggregation pipeline stages, a namespace, and others. Queries that have similar specifications have the same query shape.

**Note:**

Starting in MongoDB 8.0, the pre-existing query shape is renamed to the **plan cache query shape**, and the `queryHash` field is renamed `planCacheShapeHash`. For the components of a command that differentiate plan cache query shapes, see the [plan cache query shape](/docs/manual/reference/glossary#std-term-plan-cache-query-shape) definition. MongoDB 8.0 uses the new query shape and the existing plan cache query shape as shown on this page.

In MongoDB 8.0 and earlier versions, the existing plan cache query shape supports:

- query planning in [plan cache](/docs/manual/core/query-plans#std-label-cache-entry-state) scenarios.

- deprecated [index filters](/docs/manual/core/query-plans#std-label-index-filters). (Starting in MongoDB 8.0, use the new query settings for the new query shape.)

- a subset of the [Aggregation Pipeline.](/docs/manual/core/aggregation-pipeline#std-label-aggregation-pipeline)

Starting in MongoDB 8.0, the new query shape supports:

- query settings, which you can add with [`setQuerySettings`](/docs/manual/reference/command/setQuerySettings#mongodb-dbcommand-dbcmd.setQuerySettings). (As you'll see later on this page, query settings specify indexes and execution settings for a query shape.)

- [$queryStats query shape statistics.](/docs/manual/reference/operator/aggregation/queryStats#std-label-queryStats-queryShape)

- the fields and operations also supported by the plan cache query shape. Examples: `filter`, `sort`, and `projection`.

- the majority of the fields and operands available for the [`find`](/docs/manual/reference/command/find#mongodb-dbcommand-dbcmd.find), [`distinct`](/docs/manual/reference/command/distinct#mongodb-dbcommand-dbcmd.distinct), and [`aggregate`](/docs/manual/reference/command/aggregate#mongodb-dbcommand-dbcmd.aggregate) commands. To view the fields and operands for the commands, see the Syntax sections on each command page.

- the overall structure of the `find`, `aggregation`, and `distinct` commands, which support a wider range of query shapes than the existing plan cache query shape.

- [operation rejection filters](/docs/manual/tutorial/operation-rejection-filters#std-label-operation-rejection-filters) to block `find`, `aggregation`, and `distinct` commands that have a specified query shape.

- the entire aggregation pipeline.

Starting in MongoDB 8.0, you can use a [`$querySettings`](/docs/manual/reference/operator/aggregation/querySettings#mongodb-pipeline-pipe.-querySettings) pipeline stage to return query settings specified for each query shape.

## Examples

The following sections show examples with query shapes for the following example `pizzaOrders` collection:

```javascript
db.pizzaOrders.insertMany( [
   { _id: 0, type: "pepperoni", size: "small", price: 19,
     totalNumber: 10, orderDate: ISODate( "2023-03-13T08:14:30Z" ) },
   { _id: 1, type: "pepperoni", size: "medium", price: 20,
     totalNumber: 20, orderDate: ISODate( "2023-03-13T09:13:24Z" ) },
   { _id: 2, type: "pepperoni", size: "large", price: 21,
     totalNumber: 30, orderDate: ISODate( "2023-03-17T09:22:12Z" ) },
   { _id: 3, type: "cheese", size: "small", price: 12,
     totalNumber: 15, orderDate: ISODate( "2023-03-13T11:21:39.736Z" ) }
] )
```

### Matching Query Shapes

The following example query shape shows specifications for a `find` command on the `pizzaOrders` collection in the default `test` database:

```javascript
find: "pizzaOrders",
filter: {
   orderDate: { $gt: ISODate( "2023-01-20T00:00:00Z" ) }
},
sort: {
   totalNumber: 1
},
$db: "test"
```

The example filter limits the documents to those with an order date greater than the specified date. The example has an ascending sort on the total number of pizzas ordered.

To view the MongoDB 8.0 `queryShapeHash` and `planCacheShapeHash` hexadecimal strings, you can use the [`explain`](/docs/manual/reference/command/explain#mongodb-dbcommand-dbcmd.explain) command.

The following `explain` examples contain queries with the same query shape:

```javascript
db.pizzaOrders.explain().find(
   { orderDate: { $gt: ISODate( "2024-05-10T05:15:35Z" ) } } ).
   sort( { totalNumber: 1 }
)

db.pizzaOrders.explain().find(
   { orderDate: { $gt: ISODate( "2024-02-05T07:07:16Z" ) } } ).
   sort( { totalNumber: 1 }
)

db.pizzaOrders.explain().find(
   { orderDate: { $gt: ISODate( "2023-03-08T08:12:25Z" ) } } ).
   sort( { totalNumber: 1 }
)
```

Because the query shapes are the same, the `explain` output has the same `queryShapeHash` for each of the examples, and the same `planCacheShapeHash` for each. For example:

```javascript
queryShapeHash: 'AB8ECADEE8F0EB0F447A30744EB4813AE7E0BFEF523B0870CA10FCBC87F5D8F1'
planCacheShapeHash: '48E51110'
```

### Different Query Shape

A query has a different shape if the query has different specifications. For example, if a query has a different filter, sort, projection, namespace, or aggregation pipeline stages.

In the example in the previous section, the example sorts by the `totalNumber` field. If you change the query sort from `totalNumber` to a different field, the query has a different query shape.

For example, sorting by pizza `price` changes the query shape:

```javascript
db.pizzaOrders.explain().find(
   { orderDate: { $gt: ISODate( "2023-01-20T00:00:00Z" ) } } ).
   sort( { price: 1 }
)
```

Because the query shape is different from the shape in the previous section, the `explain` output has a different `queryShapeHash` from the previous example, and a different `planCacheShapeHash`. For example:

```javascript
queryShapeHash: 'AC1ECADBE8F1EB0F417A30741AB4813BE7E0BFEF523B0870CA11FCBC87F1A8B2'
planCacheShapeHash: '31A52130'
```

## Behavior

Starting in MongoDB 8.0, add query settings for query shapes instead of [index filters](/docs/manual/core/query-plans#std-label-index-filters) for collections. Index filters are deprecated starting in MongoDB 8.0. Query settings have more functionality than index filters, and index filters aren't persistent after cluster shutdown.

Query settings allow you to use an index for all executions of a query shape in a cluster. Also, to prevent an operation from causing excessive cluster workload, you can reject all operations associated with a query shape using an operation rejection filter.

The [query optimizer](/docs/manual/reference/glossary#std-term-query-optimizer) uses the query settings as an additional input during query planning. The query settings affect the plan selected to run a query that has a matching query shape.

## Get Started

- To add query settings for a query shape, use [`setQuerySettings`.](/docs/manual/reference/command/setQuerySettings#mongodb-dbcommand-dbcmd.setQuerySettings)

- To delete query settings, use [`removeQuerySettings`.](/docs/manual/reference/command/removeQuerySettings#mongodb-dbcommand-dbcmd.removeQuerySettings)

- To retrieve query settings, use a [`$querySettings`](/docs/manual/reference/operator/aggregation/querySettings#mongodb-pipeline-pipe.-querySettings) stage in an aggregation pipeline.

- To block a query shape, use an [operation rejection filter.](/docs/manual/tutorial/operation-rejection-filters#std-label-operation-rejection-filters)

## Learn More

- [Query Plans](/docs/manual/core/query-plans#std-label-query-plans-query-optimization)

- [Query shape statistics](/docs/manual/reference/operator/aggregation/queryStats#std-label-queryStats-queryShape)

- [Indexes](/docs/manual/indexes#std-label-indexes)

- [Aggregation Pipeline](/docs/manual/core/aggregation-pipeline#std-label-aggregation-pipeline)
