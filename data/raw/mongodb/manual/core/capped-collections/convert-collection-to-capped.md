> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Convert a Collection to Capped

To convert a non-capped collection to a [capped collection](/docs/manual/core/capped-collections#std-label-manual-capped-collection), use the [`convertToCapped`](/docs/manual/reference/command/convertToCapped#mongodb-dbcommand-dbcmd.convertToCapped) database command.

The `convertToCapped` command holds a database-exclusive lock for the duration of the operation. Other operations that lock the same database are blocked until the `convertToCapped` operation completes.

## About this Task

Generally, [TTL (Time To Live) indexes](/docs/manual/core/index-ttl#std-label-index-feature-ttl) offer better performance and more flexibility than capped collections. TTL indexes expire and remove data from normal collections based on the value of a date-typed field and a TTL value for the index.

Capped collections serialize write operations and therefore have worse concurrent insert, update, and delete performance than non-capped collections. Before you create a capped collection, consider if you can use a TTL index instead.

## Before you Begin

Create a non-capped collection called `log2`:

```javascript
db.createCollection("log2")
```

## Steps

1. Convert the collection to a capped collection

   To convert the `log2` collection to a capped collection, run the [`convertToCapped`](/docs/manual/reference/command/convertToCapped#mongodb-dbcommand-dbcmd.convertToCapped) command:

   ```javascript
   db.runCommand( {
      convertToCapped: "log2",
      size: 100000
   } )
   ```

   The `log2` collection has a maximum size of 100,000 bytes.

2. Confirm that the collection is capped

   To confirm that the `log2` collection is now capped, use the [`isCapped()`](/docs/manual/reference/method/db.collection.isCapped#mongodb-method-db.collection.isCapped) method:

   ```javascript
   db.log2.isCapped()
   ```

   **Output:**

   ```javascript
      true
   ```

## Learn More

- [Which administrative commands lock a database?](/docs/manual/faq/concurrency#std-label-faq-concurrency-database-lock)

- [Change the Size of a Capped Collection](/docs/manual/core/capped-collections/change-size-capped-collection#std-label-capped-collections-change-size)

- [Query a Capped Collection](/docs/manual/core/capped-collections/query-capped-collection#std-label-capped-collections-query)
