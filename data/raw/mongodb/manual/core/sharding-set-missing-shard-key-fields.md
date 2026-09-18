> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Set Missing Shard Key Fields

## Chunk Range and Missing Shard Key Fields

Missing shard key fields fall within the same chunk range as shard keys with null values. For example, if the shard key is on the fields `{ x:
1, y: 1 }`, then:

| Document Missing Shard Key | Falls into Same Range As |
| --- | --- |
| `{ x: "hello" }` | `{ x: "hello", y: null }` |
| `{ y: "goodbye" }` | `{ x: null, y: "goodbye" }` |
| `{ z: "oops" }` | `{ x: null, y: null }` |

## Read/Write Operations and Missing Shard Key Fields

To target documents with missing shard key fields, you can use the [`{ $exists: false }`](/docs/manual/reference/operator/query/exists#mongodb-query-op.-exists) filter condition on the shard key fields. For example, if the shard key is on the fields `{ x: 1, y: 1
}`, you can find the documents with missing shard key fields by running this query:

```javascript
db.shardedcollection.find( { $or: [ { x: { $exists: false } }, { y: { $exists: false } } ] } )
```

If you specify a [null equality match](/docs/manual/tutorial/query-for-null-fields) filter condition (e.g. `{ x: null
}`), the filter matches both those documents with missing shard key fields and those with shard key fields set to `null`.

Some write operations, such as a write with an `upsert` specification, require an equality match on the shard key. In those cases, to target a document that is missing the shard key, include another filter condition in addition to the `null` equality match. For example:

```javascript
{ _id: <value>, <shardkeyfield>: null } // _id of the document missing shard key
```

## Set the Missing Shard Key Fields

If you have missing shard key fields, you can set the shard key field to `null`. If you want to set the missing shard key field to a non-`null` value, see [Change a Document's Shard Key Value.](/docs/manual/core/sharding-change-shard-key-value#std-label-update-shard-key)

To perform the update, you can use the following operations on a [`mongos`:](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos)

| Command | Method | Description |
| --- | --- | --- |
| [update](/docs/manual/reference/command/update#std-label-command-update-shard-key-modification) with`multi: true` | [db.collection.updateMany()](/docs/manual/reference/method/db.collection.updateMany#std-label-updateMany-sharded-collection) | Can be used to set the missing key value to `null` only.; Can be performed inside or outside a transaction.; Can be performed as a retryable write or not.; For additional requirements, refer to the specific command/method. |
| [update](/docs/manual/reference/command/update#std-label-command-update-shard-key-modification)  with`multi: false` | [db.collection.replaceOne()](/docs/manual/reference/method/db.collection.replaceOne#std-label-replaceOne-missing-shard-key)[db.collection.updateOne()](/docs/manual/reference/method/db.collection.updateOne#std-label-updateOne-missing-shard-key) | Can be used to set the missing key value to `null` or any other value.; The update to set missing shard key fields **must** meet one of the following requirements:the filter of the query contains an equality condition on the full shard key in the query; the filter of the query contains an exact match on _id; the update targets a single shard; To set to a non-`null` value, refer to [Change a Document's Shard Key Value.](/docs/manual/core/sharding-change-shard-key-value#std-label-update-shard-key); For additional requirements, refer to the specific command/method. |
| [findAndModify](/docs/manual/reference/command/findAndModify#std-label-cmd-findAndModify-missing-shard-key) | [db.collection.findOneAndReplace()](/docs/manual/reference/method/db.collection.findOneAndReplace#std-label-findOneAndReplace-missing-shard-key)[db.collection.findOneAndUpdate()](/docs/manual/reference/method/db.collection.findOneAndUpdate#std-label-findOneAndUpdate-missing-shard-key)[db.collection.findAndModify()](/docs/manual/reference/method/db.collection.findAndModify#std-label-method-findAndModify-missing-shard-key) | Can be used to set the missing key value to `null` or any other value.; When setting missing shard key fields with a method that explicitly updates only one document, the update **must** meet one of the following requirements:the filter of the query contains an equality condition on the full shard key in the query; the filter of the query contains an exact match on _id; the update targets a single shard; Missing key values are returned when matching on `null`. To avoid updating a key value that is `null`, include additional query conditions as appropriate.; To set to a non-`null` value, refer to [Change a Document's Shard Key Value.](/docs/manual/core/sharding-change-shard-key-value#std-label-update-shard-key); For additional requirements, refer to the specific command/method. |
|  | [`db.collection.bulkWrite()`](/docs/manual/reference/method/db.collection.bulkWrite#mongodb-method-db.collection.bulkWrite)[`Bulk.find.replaceOne()`](/docs/manual/reference/method/Bulk.find.replaceOne#mongodb-method-Bulk.find.replaceOne)[`Bulk.find.updateOne()`](/docs/manual/reference/method/Bulk.find.updateOne#mongodb-method-Bulk.find.updateOne)[`Bulk.find.update()`](/docs/manual/reference/method/Bulk.find.update#mongodb-method-Bulk.find.update) | To set to a `null` value,  you can specify multiple shard key modifications in the bulk operation.; When setting missing shard key fields with a method that explicitly updates only one document, the update **must** meet one of the following requirements:the filter of the query contains an equality condition on the full shard key in the query; the filter of the query contains an exact match on _id; the update targets a single shard; To set to a non-`null` value, refer to [Change a Document's Shard Key Value.](/docs/manual/core/sharding-change-shard-key-value#std-label-update-shard-key); For additional requirements, refer to the underlying command/method. |

## Example

Consider a `sales` collection which is sharded on the `location` field. Some documents in the collection have no `location` field. A missing field is considered the same as a null value for the field. To explicitly set these fields to `null`, run the following command:

```javascript
db.sales.updateOne(
  { _id: 12345, location: null },
  { $set: { location: null } }
)
```

When setting missing shard key fields with [`db.collection.updateOne()`](/docs/manual/reference/method/db.collection.updateOne#mongodb-method-db.collection.updateOne) or another method that explicitly updates only one document, the update **must** meet one of the following requirements:

- the filter of the query contains an equality condition on the full shard key in the query

- the filter of the query contains an exact match on \_id

- the update targets a single Shard
