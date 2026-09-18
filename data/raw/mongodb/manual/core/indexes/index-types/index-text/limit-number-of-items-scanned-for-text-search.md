> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Limit Text Index Entries Scanned on Self-Managed Deployments

**Note:**

MongoDB offers an improved full-text search solution, [MongoDB Search](https://www.mongodb.com/docs/atlas/atlas-search/), and vector search solution, [MongoDB Vector Search](https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-overview/). We recommend using [MongoDB Search indexes](https://www.mongodb.com/docs/search/indexes/manage-indexes/#std-label-fts-manage-indexes) or [MongoDB Vector Search indexes](https://www.mongodb.com/docs/vector-search/indexes/vector-search-type/#std-label-avs-types-vector-search)  instead of text indexes.

If you run `$text` queries on a large dataset, a single-field text index may scan a large number of entries to return results, which can result in slow queries.

To improve query performance, you can create a [compound text index](/docs/manual/core/indexes/index-types/index-text/create-text-index#std-label-compound-text-index-example) and include an equality match in your `$text` queries. If the compound index contains the field used in your equality match, the index scans fewer entries and returns results faster.

## About this Task

In this example, a store manager queries an `inventory` collection that contains these documents:

```javascript
db.inventory.insertMany( [
   { _id: 1, department: "tech", description: "lime green computer" },
   { _id: 2, department: "tech", description: "wireless red mouse" },
   { _id: 3, department: "kitchen", description: "green placemat" },
   { _id: 4, department: "kitchen", description: "red peeler" },
   { _id: 5, department: "food", description: "green apple" },
   { _id: 6, department: "food", description: "red potato" }
] )
```

The manager performs `$text` queries for items within a specific department.

A compound text index on the `department` and `description` fields limits the index keys scanned to only documents within the specified `department`. The compound text index provides improved performance compared to a single-field text index on the `description` field.

## Procedure

Create a compound index on the `inventory` collection that contains the following fields:

- An ascending or descending index key on the `department` field

- A `text` index key on the `description` field

```javascript
db.inventory.createIndex(
   {
     department: 1,
     description: "text"
   }
)
```

## Results

After you create the compound index, `$text` queries only scan documents that match a specified equality condition on the `department` field.

For example, the following query scans documents with `department` equal to `kitchen` where the `description` field contains the string `green`:

```javascript
db.inventory.find( { department: "kitchen", $text: { $search: "green" } } )
```

Output:

```javascript
[ { _id: 3, department: 'kitchen', description: 'green placemat' } ]
```

### View Number of Documents Examined

To see how many documents were scanned to return the query, view the query's [`executionStats`:](/docs/manual/reference/explain-results#std-label-executionStats)

```javascript
db.inventory.find(
   {
      department: "kitchen", $text: { $search: "green" }
   }
).explain("executionStats")
```

The number of index keys examined is indicated in the [`totalKeysExamined`](/docs/manual/reference/explain-results#mongodb-data-explain.executionStats.totalKeysExamined) field. Queries that examine more index keys generally take longer to complete.

With the compound index on `department` and `description`, the query only examines **one** index key. There is only one document in the collection where `department` is `kitchen` and the `description` contains the string `green`.

However, if the query used a single-field text index only on the `description` field, the query would examine **three** index keys. There are three documents in the collection where the `description` field contains the string `green`.

In a small collection like the one used in the preceding example, there isn't a noticeable difference in performance between single-field and compound text indexes. However, in larger collections, increased index entry scans can noticeably hinder performance. For best performance, create text indexes that limit the number of index entries scanned to best fit your equality matches.

## Learn More

- [Compound text index restrictions](/docs/manual/core/indexes/index-types/index-text/text-index-restrictions#std-label-text-index-compound-restrictions)

- [Assign Weights to $text Query Results on Self-Managed Deployments](/docs/manual/core/indexes/index-types/index-text/control-text-search-results#std-label-specify-weights)

- [Text Index Properties on Self-Managed Deployments](/docs/manual/core/indexes/index-types/index-text/text-index-properties#std-label-text-index-properties)
