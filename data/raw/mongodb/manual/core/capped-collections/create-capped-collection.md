> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Create a Capped Collection

To create a [capped collection](/docs/manual/core/capped-collections#std-label-manual-capped-collection), specify the `capped` option to either the [`db.createCollection()`](/docs/manual/reference/method/db.createCollection#mongodb-method-db.createCollection) method or the [`create`](/docs/manual/reference/command/create#mongodb-dbcommand-dbcmd.create) command.

You must create capped collections explicitly. You cannot create a capped collection implicitly by inserting data into a non-existing collection.

When you create a capped collection you must specify the maximum size of the collection. MongoDB pre-allocates the specified storage for the collection. The size of the capped collection includes a small amount of space for internal overhead.

You can optionally specify a maximum number of documents for the collection. MongoDB removes older documents if the collection reaches the maximum size limit before it reaches the maximum document count.

## About this Task

Generally, [TTL (Time To Live) indexes](/docs/manual/core/index-ttl#std-label-index-feature-ttl) offer better performance and more flexibility than capped collections. TTL indexes expire and remove data from normal collections based on the value of a date-typed field and a TTL value for the index.

Capped collections serialize write operations and therefore have worse concurrent insert, update, and delete performance than non-capped collections. Before you create a capped collection, consider if you can use a TTL index instead.

## Steps

The following examples show you how to:

- [Create a Capped Collection with a Maximum Size](/docs/manual/core/capped-collections/create-capped-collection#std-label-create-capped-collection-max-size)

- [Create a Capped Collection with a Maximum Number of Documents](/docs/manual/core/capped-collections/create-capped-collection#std-label-create-capped-collection-max-docs)

### Create a Capped Collection with a Maximum Size

Create a capped collection called `log` that has a maximum size of 100,000 bytes:

```javascript
db.createCollection( "log", { capped: true, size: 100000 } )
```

**Note:**

The value that you provide for the `size` field must be greater than `0` and less than or equal to `1024^5` (1 PB (petabyte)). MongoDB rounds the `size` of all capped collections up to the nearest integer multiple of 256, in bytes.

### Create a Capped Collection with a Maximum Number of Documents

Create a capped collection called `log2` that has a maximum size of 5,242,880 bytes and can store a maximum of 5,000 documents:

```javascript
db.createCollection(
   "log2",
   {
      capped: true,
      size: 5242880,
      max: 5000
   }
)
```

**Important:**

The `size` field is always required, even when you specify the `max` number of documents.

## Learn More

- [`db.createCollection()`](/docs/manual/reference/method/db.createCollection#mongodb-method-db.createCollection)

- [Query a Capped Collection](/docs/manual/core/capped-collections/query-capped-collection#std-label-capped-collections-query)

- [Check if a Collection is Capped](/docs/manual/core/capped-collections/check-if-collection-is-capped#std-label-capped-collections-check)
