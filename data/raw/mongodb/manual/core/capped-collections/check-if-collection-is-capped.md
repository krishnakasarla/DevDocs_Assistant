> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Check if a Collection is Capped

To check if a collection is capped, use the [`isCapped()`](/docs/manual/reference/method/db.collection.isCapped#mongodb-method-db.collection.isCapped) method.

## About this Task

Generally, [TTL (Time To Live) indexes](/docs/manual/core/index-ttl#std-label-index-feature-ttl) offer better performance and more flexibility than capped collections. TTL indexes expire and remove data from normal collections based on the value of a date-typed field and a TTL value for the index.

Capped collections serialize write operations and therefore have worse concurrent insert, update, and delete performance than non-capped collections. Before you create a capped collection, consider if you can use a TTL index instead.

## Before you Begin

Create a non-capped collection and a capped collection:

```javascript
db.createCollection("nonCappedCollection1")

db.createCollection("cappedCollection1", { capped: true, size: 100000 } )
```

## Steps

To check if the collections are capped, use the [`isCapped()`](/docs/manual/reference/method/db.collection.isCapped#mongodb-method-db.collection.isCapped) method:

```javascript
db.nonCappedCollection1.isCapped()

db.cappedCollection1.isCapped()
```

**Output:**

```javascript
false
true
```

## Learn More

- [Create a Capped Collection](/docs/manual/core/capped-collections/create-capped-collection#std-label-capped-collections-create)

- [Convert a Collection to Capped](/docs/manual/core/capped-collections/convert-collection-to-capped#std-label-capped-collections-convert)

- [`$collStats`](/docs/manual/reference/operator/aggregation/collStats#mongodb-pipeline-pipe.-collStats)
