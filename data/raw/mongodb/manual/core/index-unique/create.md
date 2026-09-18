> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Create a Single-Field Unique Index

Unique indexes ensure that a value appears at most once for a given field.

To create a unique index in the MongoDB Shell, use the [`db.collection.createIndex()`](/docs/manual/reference/method/db.collection.createIndex#mongodb-method-db.collection.createIndex) method with the `unique` option set to `true`.

```javascript
db.collection.createIndex(
   { <field>: <sortOrder> },
   { unique: true }
 )
```

## About this Task

This example adds a unique index on the `user_id` field of a `members` collection to ensure that there are no duplicate values in the `user_id` field.

## Steps

To create a unique index on the `user_id` field of the `members` collection, run the following command in [`mongosh`:](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh)

```javascript
db.members.createIndex( { "user_id": 1 }, { unique: true } )
```

## Learn More

- [Create a Compound Unique Index](/docs/manual/core/index-unique/create-compound#std-label-index-unique-compound-index)

- [Convert an Existing Index to a Unique Index](/docs/manual/core/index-unique/convert-to-unique#std-label-index-convert-to-unique)
