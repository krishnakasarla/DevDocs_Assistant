> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Hidden Indexes

Hidden indexes are not visible to the [query planner](/docs/manual/core/query-plans) and cannot be used to support a query.

By hiding an index from the planner, you can evaluate the potential impact of dropping an index without actually dropping the index. If the impact is negative, you can unhide the index instead of having to recreate a dropped index.

## Behavior

Apart from being hidden from the planner, hidden indexes behave like unhidden indexes. For example:

- If a hidden index is a [unique index](/docs/manual/core/index-unique#std-label-index-type-unique), the index still applies its unique constraint to the documents.

- If a hidden index is a [TTL index](/docs/manual/core/index-ttl#std-label-index-feature-ttl), the index still expires documents.

- Hidden indexes are included in [`listIndexes`](/docs/manual/reference/command/listIndexes#mongodb-dbcommand-dbcmd.listIndexes) and [`db.collection.getIndexes()`](/docs/manual/reference/method/db.collection.getIndexes#mongodb-method-db.collection.getIndexes) results.

- Hidden indexes are updated upon write operations to the collection and continue to consume disk space and memory. As such, they are included in various statistics operations, such as [`db.collection.stats()`](/docs/manual/reference/method/db.collection.stats#mongodb-method-db.collection.stats) and [`$indexStats`.](/docs/manual/reference/operator/aggregation/indexStats#mongodb-pipeline-pipe.-indexStats)

- Hiding an unhidden index or unhiding a hidden index resets its [`$indexStats`](/docs/manual/reference/operator/aggregation/indexStats#mongodb-pipeline-pipe.-indexStats). Hiding an already hidden index or unhiding an already unhidden index does not reset the [`$indexStats`.](/docs/manual/reference/operator/aggregation/indexStats#mongodb-pipeline-pipe.-indexStats)

## Restrictions

- To hide an index, you must have [featureCompatibilityVersion](/docs/manual/reference/command/setFeatureCompatibilityVersion#std-label-view-fcv) set to `6.0` or greater.

- You cannot hide the `_id` index.

- You cannot [`cursor.hint()`](/docs/manual/reference/method/cursor.hint#mongodb-method-cursor.hint) a hidden index.

## Examples

### Create a Hidden Index

To create a `hidden` index, use the [`db.collection.createIndex()`](/docs/manual/reference/method/db.collection.createIndex#mongodb-method-db.collection.createIndex) method with the [hidden](/docs/manual/reference/method/db.collection.createIndex#std-label-method-createIndex-hidden) option set to `true`.

**Note:**

To use the `hidden` option with [`db.collection.createIndex()`](/docs/manual/reference/method/db.collection.createIndex#mongodb-method-db.collection.createIndex), you must have [featureCompatibilityVersion](/docs/manual/reference/command/setFeatureCompatibilityVersion#std-label-view-fcv) set to `6.0` or greater.

For example, the following operation creates a hidden ascending index on the `borough` field:

```javascript
db.addresses.createIndex(
   { borough: 1 },
   { hidden: true }
);
```

To verify, run [`db.collection.getIndexes()`](/docs/manual/reference/method/db.collection.getIndexes#mongodb-method-db.collection.getIndexes) on the `addresses` collection:

```javascript
db.addresses.getIndexes()
```

The operation returns the following information:

```javascript
[
   {
      "v" : 2,
      "key" : {
         "_id" : 1
      },
      "name" : "_id_"
   },
   {
      "v" : 2,
      "key" : {
         "borough" : 1
      },
      "name" : "borough_1",
      "hidden" : true
   }
]
```

The index option `hidden` is only returned if the value is `true`.

### Hide an Existing Index

**Note:**

- To hide an index, you must have [featureCompatibilityVersion](/docs/manual/reference/command/setFeatureCompatibilityVersion#std-label-view-fcv) set to `6.0` or greater.

- You cannot hide the `_id` index.

To hide an existing index, you can use the [`collMod`](/docs/manual/reference/command/collMod#mongodb-dbcommand-dbcmd.collMod) command or [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) helper [`db.collection.hideIndex()`.](/docs/manual/reference/method/db.collection.hideIndex#mongodb-method-db.collection.hideIndex)

For example, create an index without hiding:

```javascript
db.restaurants.createIndex( { borough: 1, ratings: 1 } );
```

To hide the index, you can specify either:

- the index key specification document to the [`db.collection.hideIndex()`](/docs/manual/reference/method/db.collection.hideIndex#mongodb-method-db.collection.hideIndex) method:

  ```javascript
  db.restaurants.hideIndex( { borough: 1, ratings: 1 } ); // Specify the index key specification document
  ```

- the index name to the [`db.collection.hideIndex()`](/docs/manual/reference/method/db.collection.hideIndex#mongodb-method-db.collection.hideIndex) method:

  ```javascript
  db.restaurants.hideIndex( "borough_1_ratings_1" );  // Specify the index name
  ```

To verify, run [`db.collection.getIndexes()`](/docs/manual/reference/method/db.collection.getIndexes#mongodb-method-db.collection.getIndexes) on the `restaurants` collection:

```javascript
db.restaurants.getIndexes()
```

The operation returns the following information:

```javascript
[
   {
      "v" : 2,
      "key" : {
         "_id" : 1
      },
      "name" : "_id_"
   },
   {
      "v" : 2,
      "key" : {
         "borough" : 1,
         "ratings" : 1
      },
      "name" : "borough_1_ratings_1",
      "hidden" : true
   }
]
```

The index option `hidden` is only returned if the value is `true`.

### Unhide an Existing Index

To unhide a hidden index, you can use the [`collMod`](/docs/manual/reference/command/collMod#mongodb-dbcommand-dbcmd.collMod) command or [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) helper [`db.collection.unhideIndex()`](/docs/manual/reference/method/db.collection.unhideIndex#mongodb-method-db.collection.unhideIndex). You can specify either:

- the index key specification document to the [`db.collection.unhideIndex()`](/docs/manual/reference/method/db.collection.unhideIndex#mongodb-method-db.collection.unhideIndex) method:

  ```javascript
  db.restaurants.unhideIndex( { borough: 1, city: 1 } );  // Specify the index key specification document
  ```

- the index name to the [`db.collection.unhideIndex()`](/docs/manual/reference/method/db.collection.unhideIndex#mongodb-method-db.collection.unhideIndex) method:

  ```javascript
  db.restaurants.unhideIndex( "borough_1_ratings_1" );    // Specify the index name
  ```

To verify, run [`db.collection.getIndexes()`](/docs/manual/reference/method/db.collection.getIndexes#mongodb-method-db.collection.getIndexes) on the `restaurants` collection:

```javascript
db.restaurants.getIndexes()
```

The operation returns the following information:

```javascript
[
   {
      "v" : 2,
      "key" : {
         "_id" : 1
      },
      "name" : "_id_"
   },
   {
      "v" : 2,
      "key" : {
         "borough" : 1,
         "ratings" : 1
      },
      "name" : "borough_1_ratings_1"
   }
]
```

The index option `hidden` no longer appears as part of the `borough_1_ratings_1` index since the field is only returned if the value is `true`.

Because indexes are fully maintained while hidden, the index is immediately available for use once unhidden.
