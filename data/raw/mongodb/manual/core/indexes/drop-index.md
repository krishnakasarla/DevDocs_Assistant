> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Drop an Index

You can remove a specific index from a collection. You may need to drop an index if you see a negative performance impact, want to replace it with a new index, or no longer need the index.

To drop an index, use one of the following shell methods:

| Method | Description |
| --- | --- |
| [`db.collection.dropIndex()`](/docs/manual/reference/method/db.collection.dropIndex#mongodb-method-db.collection.dropIndex) | Drops a specific index from the collection. |
| [`db.collection.dropIndexes()`](/docs/manual/reference/method/db.collection.dropIndexes#mongodb-method-db.collection.dropIndexes) | Drops all removable indexes from the collection or an array of indexes, if specified. |

## About this Task

You can drop any index except the default index on the `_id` field. To drop the `_id` index, you must drop the entire collection.

If you drop an index that's actively used in production, you may experience performance degradation. Before you drop an index, consider [hiding the index](/docs/manual/core/index-hidden#std-label-index-type-hidden) to evaluate the potential impact of the drop.

## Before You Begin

To drop an index, you need its name. To get all index names for a collection, run the [`getIndexes()`](/docs/manual/reference/method/db.collection.getIndexes#mongodb-method-db.collection.getIndexes) method:

```javascript
db.<collection>.getIndexes()
```

## Procedures

After you identify which indexes to drop, use one of the following drop methods for the specified collection:

### Drop a Single Index

To drop a specific index, use the [`dropIndex()`](/docs/manual/reference/method/db.collection.dropIndex#mongodb-method-db.collection.dropIndex) method and specify the index name:

```javascript
db.<collection>.dropIndex("<indexName>")
```

### Drop Multiple Indexes

To drop multiple indexes, use the [`dropIndexes()`](/docs/manual/reference/method/db.collection.dropIndexes#mongodb-method-db.collection.dropIndexes) method and specify an array of index names:

```javascript
db.<collection>.dropIndexes( [ "<index1>", "<index2>", "<index3>" ] )
```

### Drop All Indexes Except the `_id` Index

To drop all indexes except the `_id` index, use the [`dropIndexes()`](/docs/manual/reference/method/db.collection.dropIndexes#mongodb-method-db.collection.dropIndexes) method:

```javascript
db.<collection>.dropIndexes()
```

## Results

After you drop an index, the system returns information about the status of the operation.

Example output:

```javascript
...
{ "nIndexesWas" : 3, "ok" : 1 }
...
```

The value of `nIndexesWas` reflects the number of indexes before removing an index.

To confirm that the index was dropped, run the [`db.collection.getIndexes()`](/docs/manual/reference/method/db.collection.getIndexes#mongodb-method-db.collection.getIndexes) method:

```javascript
db.<collection>.getIndexes()
```

The dropped index no longer appears in the `getIndexes()` output.

## Learn More

- To learn more about managing your existing indexes, see [Manage Indexes.](/docs/manual/tutorial/manage-indexes#std-label-manage-indexes)

- To learn how to remove an index in MongoDB Compass, see [Manage Indexes in Compass.](https://www.mongodb.com/docs/compass/current/indexes/)
