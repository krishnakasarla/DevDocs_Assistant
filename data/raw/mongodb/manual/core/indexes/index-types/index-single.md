> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Single Field Indexes

Single field indexes store information from a single field in a collection. By default, all collections have an index on the [\_id field](/docs/manual/indexes#std-label-index-type-id). You can add additional indexes to speed up important queries and operations.

You can create an index on any field in a document, including top-level fields, embedded fields, or fields inside embedded documents. When you create an index, specify the field and the sort order (`1` for ascending, `-1` for descending).

To create a single-field index, use the following prototype:

```javascript
db.<collection>.createIndex( { <field>: <sort-order> } )
```

This image shows an ascending index on a single field, `score`:

![Diagram of an index on the \`\`score\`\` field (ascending).](/images/index-ascending.bakedsvg.svg)

In this example, each document in the collection that has a value for the `score` field is added to the index in ascending order.

You can [create and manage single field indexes in the UI](https://www.mongodb.com/docs/atlas/atlas-ui/indexes/) for deployments hosted in [MongoDB Atlas.](https://www.mongodb.com/docs/atlas)

## Use Cases

If your application repeatedly runs queries on the same field, you can create an index on that field to improve performance. For example, your human resources department often needs to look up employees by employee ID. You can create an index on the employee ID field to improve the performance of that query.

## Get Started

To create an index on a single field, see these examples:

- [Create an Index on a Single Field](/docs/manual/core/indexes/index-types/index-single/create-single-field-index#std-label-index-create-ascending-single-field)

- [Create an Index on an Embedded Field](/docs/manual/core/indexes/index-types/index-single/create-single-field-index#std-label-index-embedded-fields)

- [Create an Index on an Embedded Document](/docs/manual/core/indexes/index-types/index-single/create-embedded-object-index#std-label-index-embedded-documents)
