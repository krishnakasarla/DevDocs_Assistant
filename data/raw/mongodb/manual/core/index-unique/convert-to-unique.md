> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Convert an Existing Index to a Unique Index

To convert a non-unique index to a [unique index](/docs/manual/core/index-unique#std-label-index-type-unique), use the [`collMod`](/docs/manual/reference/command/collMod#mongodb-dbcommand-dbcmd.collMod) command. The `collMod` command provides options to verify that your indexed field contains unique values before you complete the conversion.

## Before you Begin

1. Populate sample data

   Create the `apples` collection:

   ```javascript
   db.apples.insertMany( [
      { type: "Delicious", quantity: 12 },
      { type: "Macintosh", quantity: 13 },
      { type: "Delicious", quantity: 13 },
      { type: "Fuji", quantity: 15 },
      { type: "Washington", quantity: 10 }
   ] )
   ```

2. Create a single field index

   Add a single field index on the `type` field:

   ```javascript
   db.apples.createIndex( { type: 1 } )
   ```

## Steps

1. Prepare the index to be converted to a unique index

   Run `collMod` on the `type` field index and set `prepareUnique` to `true`:

   ```javascript
   db.runCommand( {
      collMod: "apples",
      index: {
         keyPattern: { type: 1 },
         prepareUnique: true
      }
   } )
   ```

   After `prepareUnique` is set, you cannot insert new documents that duplicate an index key entry. For example, the following insert operation results in an error:

   ```javascript
   db.apples.insertOne( { type: "Delicious", quantity: 20 } )
   ```

   **Output:**

   ```javascript
   MongoServerError: E11000 duplicate key error collection:
   test.apples index: type_1 dup key: { type: "Delicious" }
   ```

2. Check for unique key violations

   To see if there are any documents that violate the unique constraint on the `type` field, run `collMod` with `unique: true` and `dryRun:
           true`:

   ```javascript
   db.runCommand( {
      collMod: "apples",
      index: {
         keyPattern: { type: 1 },
         unique: true
      },
      dryRun: true
   } )
   ```

   **Output:**

   ```javascript
   MongoServerError: Cannot convert the index to unique. Please resolve conflicting documents before running collMod again.

   Violations: [
      {
         ids: [
            ObjectId("660489d24cabd75abebadbd0"),
            ObjectId("660489d24cabd75abebadbd2")
         ]
      }
   ]
   ```

3. Resolve duplicate key conflicts

   To complete the conversion, modify the duplicate entries to remove any conflicts. For example:

   ```javascript
   db.apples.deleteOne(
      { _id: ObjectId("660489d24cabd75abebadbd2") }
   )
   ```

4. Confirm that all conflicts are resolved

   To confirm that the index can be converted, re-run the `collMod()` command with `dryRun: true`:

   ```javascript
   db.runCommand( {
      collMod: "apples",
      index: {
         keyPattern: { type: 1 },
         unique: true
      },
      dryRun: true
   } )
   ```

   **Output:**

   ```javascript
   { ok: 1 }
   ```

5. Finalize the index conversion

   To finalize the conversion to a unique index, run the `collMod` command with `unique: true` and remove the `dryRun` flag:

   ```javascript
   db.runCommand( {
      collMod: "apples",
      index: {
         keyPattern: { type: 1 },
         unique: true
      }
   } )
   ```

   **Output:**

   ```javascript
   { unique_new: true, ok: 1 }
   ```

## Learn More

- [Manage Indexes](/docs/manual/tutorial/manage-indexes#std-label-manage-indexes)

- [Index Properties](/docs/manual/core/indexes/index-properties#std-label-index-properties)

- [Indexing Strategies](/docs/manual/applications/indexes#std-label-indexing-strategies)
