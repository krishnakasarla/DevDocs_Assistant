> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Change a Document's Shard Key Value

You can update a document's shard key value unless the shard key field is the immutable `_id` field.

**Important: When updating the shard key value**

- You **must** be on a [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos). Do **not** issue the operation directly on the shard.

- You **must** run either in a [transaction](/docs/manual/core/transactions) or as a [retryable write.](/docs/manual/core/retryable-writes)

- You **must** include an equality condition on the full shard key in the query filter. For example, consider a `messages` collection that uses `{ activityid: 1, userid : 1 }` as the shard key. To update the shard key value for a document, you must include `activityid: <value>, userid: <value>` in the query filter. You can include additional fields in the query as appropriate.

See also the specific write command/methods for additional operation-specific requirements when run against a sharded collection.

To update a shard key value, use the following operations:

| Command | Method |
| --- | --- |
| [update](/docs/manual/reference/command/update#std-label-command-update-shard-key-modification) with `multi: false` | [db.collection.replaceOne()](/docs/manual/reference/method/db.collection.replaceOne#std-label-replaceOne-shard-key-modification)[db.collection.updateOne()](/docs/manual/reference/method/db.collection.updateOne#std-label-updateOne-shard-key-modification) To set to a non-`null` value, the update must be performed either inside a transaction or as a retryable write. |
| [findAndModify](/docs/manual/reference/command/findAndModify#std-label-cmd-findAndModify-sharded-collection) | [db.collection.findOneAndReplace()](/docs/manual/reference/method/db.collection.findOneAndReplace#std-label-findOneAndReplace-shard-key-modification)[db.collection.findOneAndUpdate()](/docs/manual/reference/method/db.collection.findOneAndUpdate#std-label-findOneAndUpdate-shard-key-modification)[db.collection.findAndModify()](/docs/manual/reference/method/db.collection.findAndModify#std-label-method-findAndModify-sharded-collection) To set to a non-`null` value, the update must be performed either inside a transaction or as a retryable write. |
|  | [`db.collection.bulkWrite()`](/docs/manual/reference/method/db.collection.bulkWrite#mongodb-method-db.collection.bulkWrite)[`Bulk.find.updateOne()`](/docs/manual/reference/method/Bulk.find.updateOne#mongodb-method-Bulk.find.updateOne) If the shard key modification results in moving the document to another shard, you cannot specify more than one shard key modification in the bulk operation; the batch size has to be 1. If the shard key modification does not result in moving the document to another shard, you can specify multiple shard key modification in the bulk operation. To set to a non-`null` value, the operation must be performed either inside a transaction or as a retryable write. |

**Warning:**

Documents in sharded collections can be missing the shard key fields. Take precaution to avoid accidentally removing the shard key when changing a document's shard key value.

## Example

Consider a `sales` collection which is sharded on the `location` field. The collection contains a document with the `_id` `12345` and the `location` `""`. To update the field value for this document, you can run the following command:

```javascript
db.sales.updateOne(
  { _id: 12345, location: "" },
  { $set: { location: "New York"} }
)
```

**See also:**

[Set Missing Shard Key Fields](/docs/manual/core/sharding-set-missing-shard-key-fields#std-label-shard-key-missing-set)
