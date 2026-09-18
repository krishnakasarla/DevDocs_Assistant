> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Query Plans

For any given query, the MongoDB query planner chooses and caches an efficient query plan given the available indexes. The planner can use either the classic multi-planner or the cost-based ranker (CBR) to select a plan.

## Query Plan Options

In the classic multi-planner, the winning plan is the query plan that produces the most results during the trial period while performing the least amount of work.

Starting in MongoDB 8.3, multi-planning with a cost-based ranker backup is the default plan selection mechanism for eligible queries. For a short trial period, the multi-planner attempts to find a plan capable of returning a result within the timeframe.

If the attempt is unsuccessful, MongoDB applies a set of rules to decide whether the multi-planner should continue or if CBR should evaluate the plans to determine the optimal solution. CBR evaluates each node in a plan based on a cost function and its cardinality estimations. MongoDB selects the plan with the lowest overall cost as the winning plan. Currently, MongoDB only invokes the CBR for a small amount of queries.

Both ranking mechanisms store the chosen plan in the **query plan cache** and reuse it for subsequent queries with the same [plan cache query shape](/docs/manual/reference/glossary#std-term-plan-cache-query-shape). The rest of this page describes plan cache behavior and related concepts that apply to both mechanisms.

The following diagram illustrates the query planner logic:

![A diagram of MongoDB's query planner logic.](/images/general-query-planner-logic.svg)

**Note:**

Using `explain` ignores all existing plan cache entries and prevents the MongoDB query planner from creating a new plan cache entry.

### Plan Cache Entry State

Each plan cache query shape is associated with one of three states in the cache:

| State | Description |
| --- | --- |
| [Missing](/docs/manual/core/query-plans#std-label-cache-entry-missing) | No entry for this shape exists in the cache. For a query, if the cache entry state for a plan cache query shape is [Missing:](/docs/manual/core/query-plans#std-label-cache-entry-missing) Candidate plans are evaluated and a winning plan is selected.; The cache creates an entry for the plan cache query shape in state [Inactive](/docs/manual/core/query-plans#std-label-cache-entry-inactive) with a value that quantifies the amount of work required by the plan. |
| [Inactive](/docs/manual/core/query-plans#std-label-cache-entry-inactive) | The entry in the cache is a placeholder entry for this shape. That is, the planner has seen the shape, calculated a value that quantifies the amount of work required by the plan and stored the shape placeholder entry but the plan cache query shape is **not** used to generate query plans. For a query, if the cache entry state for a shape is [Inactive:](/docs/manual/core/query-plans#std-label-cache-entry-inactive) Candidate plans are evaluated and a winning plan is selected.; The selected plan's value that quantifies the amount of work required by the plan is compared to the [Inactive](/docs/manual/core/query-plans#std-label-cache-entry-inactive) entry's. If the selected plan's value is:Less than or equal to the [Inactive](/docs/manual/core/query-plans#std-label-cache-entry-inactive) entry's:The selected plan replaces the placeholder [Inactive](/docs/manual/core/query-plans#std-label-cache-entry-inactive) entry and has an [Active](/docs/manual/core/query-plans#std-label-cache-entry-active) state.If before the replacement happens, the [Inactive](/docs/manual/core/query-plans#std-label-cache-entry-inactive) entry becomes [Active](/docs/manual/core/query-plans#std-label-cache-entry-active) (for example, due to another query operation), the newly active entry will only be replaced if its value that quantifies the amount of work required by the plan is greater than the selected plan.; Greater than the [Inactive](/docs/manual/core/query-plans#std-label-cache-entry-inactive) entry's:The [Inactive](/docs/manual/core/query-plans#std-label-cache-entry-inactive) entry remains but its value that quantifies the amount of work required by the plan is incremented. |
| [Active](/docs/manual/core/query-plans#std-label-cache-entry-active) | The entry in the cache is for the winning plan. The planner can use this entry to generate query plans. For a query, if the cache entry state for a shape is [Active:](/docs/manual/core/query-plans#std-label-cache-entry-active) The active entry is used to generate query plans. The planner also evaluates the entry's performance and if its value that quantifies the amount of work required by the plan no longer meets the selection criterion, it will transition to [Inactive](/docs/manual/core/query-plans#std-label-cache-entry-inactive) state. |

See [Plan Cache Flushes](/docs/manual/core/query-plans#std-label-query-plans-plan-cache-flushes) for additional scenarios that trigger changes to the plan cache.

### Query Plan and Cache Information

To view the query plan information for a given query, you can use [`db.collection.explain()`](/docs/manual/reference/method/db.collection.explain#mongodb-method-db.collection.explain) or the [`cursor.explain()`](/docs/manual/reference/method/cursor.explain#mongodb-method-cursor.explain) .

To view plan cache information for a collection, you can use the [`$planCacheStats`](/docs/manual/reference/operator/aggregation/planCacheStats#mongodb-pipeline-pipe.-planCacheStats) aggregation stage.

### Plan Cache Flushes

The query plan cache does not persist if a [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) restarts or shuts down. In addition:

- Any DDL event clears the plan cache for the relevant collection. Example DDL events include dropping a collection, and creating, deleting, or hiding an index.

- Least recently used (LRU) cache replacement mechanism clears the least recently accessed cache entry, regardless of state.

Users can also:

- Manually clear the entire plan cache using the [`PlanCache.clear()`](/docs/manual/reference/method/PlanCache.clear#mongodb-method-PlanCache.clear) method.

- Manually clear specific plan cache entries using the [`PlanCache.clearPlansByQuery()`](/docs/manual/reference/method/PlanCache.clearPlansByQuery#mongodb-method-PlanCache.clearPlansByQuery) method.

**See also:**

[planCacheShapeHash and planCacheKey](/docs/manual/core/query-plans#std-label-query-hash-plan-cache-key)

### Plan Cache Debug Info Size Limit

Starting in MongoDB 5.0, the [plan cache](/docs/manual/core/query-plans#std-label-query-plans-query-optimization) will save full `plan cache` entries only if the cumulative size of the `plan caches` for all collections is lower than 0.5 GB. When the cumulative size of the `plan caches` for all collections exceeds this threshold, additional `plan cache` entries are stored without the following debug information:

- [createdFromQuery](/docs/manual/reference/operator/aggregation/planCacheStats#std-label-plancachestats-createdFromQuery)

- [cachedPlan](/docs/manual/reference/operator/aggregation/planCacheStats#std-label-plancachestats-cachedPlan)

- [creationExecStats](/docs/manual/reference/operator/aggregation/planCacheStats#std-label-plancachestats-creationExecStats)

- [candidatePlanScores](/docs/manual/reference/operator/aggregation/planCacheStats#std-label-plancachestats-candidatePlanScores)

The estimated size in bytes of a `plan cache` entry is available in the output of [`$planCacheStats`.](/docs/manual/reference/operator/aggregation/planCacheStats#mongodb-pipeline-pipe.-planCacheStats)

### planCacheShapeHash and planCacheKey

## planCacheShapeHash

To help identify slow queries with the same [plan cache query shape](/docs/manual/reference/glossary#std-term-plan-cache-query-shape), each plan cache query shape is associated with a query hash. The plan cache query shape hash is a hexadecimal string that represents a hash of the query shape and is dependent only on the query shape.

**Note:**

As with any hash function, two different query shapes may result in the same hash value. However, the occurrence of hash collisions between different query shapes is unlikely.

Starting in MongoDB 8.0, the existing `queryHash` field is duplicated in a new field named `planCacheShapeHash`. If you're using an earlier MongoDB version, you'll only see the `queryHash` field. Future MongoDB versions will remove the deprecated `queryHash` field, and you'll need to use the `planCacheShapeHash` field instead.

## planCacheKey

To provide more insight into the [query plan cache](/docs/manual/core/query-plans), MongoDB offers the `planCacheKey`.

`planCacheKey` is a hash of the [plan cache query shape](/docs/manual/reference/glossary#std-term-plan-cache-query-shape), further distinguished by any available indexes for the shape.

**Note:**

Unlike `planCacheShapeHash`, `planCacheKey` is a function of both the query shape and the currently available indexes for the shape. That is, if indexes that can support the query shape are added/dropped, the `planCacheKey` value may change whereas the `planCacheShapeHash` value would not change.

Starting in MongoDB 8.0, the existing `queryHash` field is duplicated in a new field named `planCacheShapeHash`. If you're using an earlier MongoDB version, you'll only see the `queryHash` field. Future MongoDB versions will remove the deprecated `queryHash` field, and you'll need to use the `planCacheShapeHash` field instead.

For example, consider a collection `foo` with the following indexes:

```javascript
db.foo.createIndex( { x: 1 } )
db.foo.createIndex( { x: 1, y: 1 } )
db.foo.createIndex( { x: 1, z: 1 }, { partialFilterExpression: { x: { $gt: 10 } } } )
```

The following queries on the collection have the same shape:

```javascript
db.foo.explain().find( { x: { $gt: 5 } } )  // Query Operation 1
db.foo.explain().find( { x: { $gt: 20 } } ) // Query Operation 2
```

Given these queries, the index with the [partial filter expression](/docs/manual/core/index-partial#std-label-partial-index-query-coverage) can support query operation 2 but *not* support query operation 1. Since the indexes available to support query operation 1 differs from query operation 2, the two queries have different `planCacheKey`.

If one of the indexes were dropped, or if a new index `{ x: 1, a: 1
}` were added, the `planCacheKey` for both query operations will change.

## Availability

The `planCacheShapeHash` and `planCacheKey` are available in:

- [explain() output](/docs/manual/reference/explain-results#std-label-explain-results) fields:

  - [`queryPlanner.planCacheShapeHash`](/docs/manual/reference/explain-results#mongodb-data-explain.queryPlanner.planCacheShapeHash)

  - [`queryPlanner.planCacheKey`](/docs/manual/reference/explain-results#mongodb-data-explain.queryPlanner.planCacheKey)

  Starting in MongoDB 8.0, the existing `queryHash` field is duplicated in a new field named `planCacheShapeHash`. If you're using an earlier MongoDB version, you'll only see the `queryHash` field. Future MongoDB versions will remove the deprecated `queryHash` field, and you'll need to use the `planCacheShapeHash` field instead.

- [profiler log messages](/docs/manual/tutorial/manage-the-database-profiler#std-label-database-profiler) and [diagnostic log messages (i.e. mongod/mongos log messages)](/docs/manual/reference/log-messages#std-label-log-messages-ref) when logging slow queries.

- [`$planCacheStats`](/docs/manual/reference/operator/aggregation/planCacheStats#mongodb-pipeline-pipe.-planCacheStats) aggregation stage

- `PlanCache.listQueryShapes()` method/`planCacheListQueryShapes` command

- `PlanCache.getPlansByQuery()` method/`planCacheListPlans` command

### Index Filters

Index filters are set with the [`planCacheSetFilter`](/docs/manual/reference/command/planCacheSetFilter#mongodb-dbcommand-dbcmd.planCacheSetFilter) command and determine which indexes the planner evaluates for a [query shape](/docs/manual/reference/glossary#std-term-query-shape). A plan cache query shape consists of a combination of query, sort, and projection specifications. If an index filter exists for a given query shape, the planner only considers those indexes specified in the filter.

When an index filter exists for the plan cache query shape, MongoDB ignores the [`hint()`](/docs/manual/reference/method/cursor.hint#mongodb-method-cursor.hint). To see whether MongoDB applied an index filter for a query shape, check the [`indexFilterSet`](/docs/manual/reference/explain-results#mongodb-data-explain.queryPlanner.indexFilterSet) field of either the [`db.collection.explain()`](/docs/manual/reference/method/db.collection.explain#mongodb-method-db.collection.explain) or the [`cursor.explain()`](/docs/manual/reference/method/cursor.explain#mongodb-method-cursor.explain) method.

Index filters only affect which indexes the planner evaluates; the planner may still select the collection scan as the winning plan for a given plan cache query shape.

Index filters exist for the duration of the server process and do not persist after shutdown. MongoDB also provides a command to manually remove filters.

Because index filters override the expected behavior of the planner as well as the [`hint()`](/docs/manual/reference/method/cursor.hint#mongodb-method-cursor.hint) method, use index filters sparingly.

Starting in MongoDB 6.0, an index filter uses the [collation](/docs/manual/reference/collation#std-label-collation) previously set using the [`planCacheSetFilter`](/docs/manual/reference/command/planCacheSetFilter#mongodb-dbcommand-dbcmd.planCacheSetFilter) command.

Starting in MongoDB 8.0, use query settings instead of adding [index filters](/docs/manual/core/query-plans#std-label-index-filters). Index filters are deprecated starting in MongoDB 8.0.

Query settings have more functionality than index filters. Also, index filters aren't persistent and you cannot easily create index filters for all cluster nodes. To add query settings and explore examples, see [`setQuerySettings`.](/docs/manual/reference/command/setQuerySettings#mongodb-dbcommand-dbcmd.setQuerySettings)

**See also:**

- [`planCacheListFilters`](/docs/manual/reference/command/planCacheListFilters#mongodb-dbcommand-dbcmd.planCacheListFilters)

- [`planCacheClearFilters`](/docs/manual/reference/command/planCacheClearFilters#mongodb-dbcommand-dbcmd.planCacheClearFilters)

- [`planCacheSetFilter`](/docs/manual/reference/command/planCacheSetFilter#mongodb-dbcommand-dbcmd.planCacheSetFilter)

- [Indexing Strategies](/docs/manual/applications/indexes)
