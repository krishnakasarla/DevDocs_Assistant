> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Aggregation Pipeline

An aggregation pipeline consists of one or more [stages](/docs/manual/reference/mql/aggregation-stages#std-label-aggregation-pipeline-operator-reference) that process documents. These documents can come from a collection, a view, or a specially designed stage.

Each stage performs an operation on the input documents. For example, a stage can [`$filter`](/docs/manual/reference/operator/aggregation/filter#mongodb-expression-exp.-filter) documents, [`$group`](/docs/manual/reference/operator/aggregation/group#mongodb-pipeline-pipe.-group) documents, and calculate values. The documents that a stage outputs are then passed to the next stage in the pipeline.

An aggregation pipeline can return results for groups of documents. You can also update documents with an aggregation pipeline using the stages shown in [Updates with Aggregation Pipeline.](/docs/manual/tutorial/update-documents-with-aggregation-pipeline#std-label-updates-agg-pipeline)

**Note:**

Aggregation pipelines run with the [`db.collection.aggregate()`](/docs/manual/reference/method/db.collection.aggregate#mongodb-method-db.collection.aggregate) method do not modify documents in a collection, unless the pipeline contains a [`$merge`](/docs/manual/reference/operator/aggregation/merge#mongodb-pipeline-pipe.-merge) or [`$out`](/docs/manual/reference/operator/aggregation/out#mongodb-pipeline-pipe.-out) stage.

You can [run aggregation pipelines in the UI](https://www.mongodb.com/docs/atlas/atlas-ui/agg-pipeline/) for deployments hosted in [MongoDB Atlas.](https://www.mongodb.com/docs/atlas)

When you run aggregation pipelines on MongoDB Atlas deployments in the MongoDB Atlas UI, you can preview the results at each stage.

## Complete Aggregation Pipeline Examples

The [Complete Aggregation Pipeline Tutorials](/docs/manual/tutorial/aggregation-complete-examples#std-label-aggregation-complete-examples) section contains step-by-step tutorials for common aggregation tasks, with examples for MongoDB Shell and each of the [official MongoDB drivers.](https://www.mongodb.com/docs/drivers/)

## Run an Aggregation Pipeline

To run an aggregation pipeline, use:

- [`db.collection.aggregate()`](/docs/manual/reference/method/db.collection.aggregate#mongodb-method-db.collection.aggregate) or

- [`aggregate`](/docs/manual/reference/command/aggregate#mongodb-dbcommand-dbcmd.aggregate)

## Additional Aggregation Pipeline Stage Details

An aggregation pipeline consists of one or more [stages](/docs/manual/reference/mql/aggregation-stages#std-label-aggregation-pipeline-operator-reference) that process documents:

- A stage does not need to output one document for every input document. Some stages produce new documents or filter documents out.

- The same stage can appear multiple times in a pipeline, except for [`$out`](/docs/manual/reference/operator/aggregation/out#mongodb-pipeline-pipe.-out), [`$merge`](/docs/manual/reference/operator/aggregation/merge#mongodb-pipeline-pipe.-merge), and [`$geoNear`.](/docs/manual/reference/operator/aggregation/geoNear#mongodb-pipeline-pipe.-geoNear)

For all aggregation stages, see [Aggregation Stages.](/docs/manual/reference/mql/aggregation-stages#std-label-aggregation-pipeline-operator-reference)

### Expressions and Operators

In aggregation pipelines, expressions define how the stage processes each input document in the pipeline. For example, expressions can define which documents to include, how to reshape fields, or how to compute new values.

Some aggregation pipeline stages accept [expressions](/docs/manual/reference/glossary#std-term-expression). Operators calculate values based on input expressions.

In the MongoDB Query Language, you can build expressions from the following components:

| Component | Example |
| --- | --- |
| Constants | `3` |
| Operators | [`$add`](/docs/manual/reference/operator/aggregation/add#mongodb-expression-exp.-add) |
| Field path expressions | `"$<path.to.field>"` |

For example, `{ $add: [ 3, "$inventory.total" ] }` is an expression that consists of the `$add` operator and two operands:

- The constant `3`

- The [field path expression](/docs/manual/core/aggregation-pipeline#std-label-agg-quick-ref-field-paths) `"$inventory.total"`

The expression returns the result of adding 3 to the value at path `inventory.total` of the input document.

**Note: Accessing Array Element Indexes in $map, $filter, and $reduce**

MongoDB 8.3 improves access to array element indexes in [`$map`](/docs/manual/reference/operator/aggregation/map#mongodb-expression-exp.-map), [`$filter`](/docs/manual/reference/operator/aggregation/filter#mongodb-expression-exp.-filter), and [`$reduce`](/docs/manual/reference/operator/aggregation/reduce#mongodb-expression-exp.-reduce) aggregation expressions. You can use the new `arrayIndexAs` field to set a variable to store the index of an array element. You can also use the new [`$$IDX`](/docs/manual/reference/aggregation-variables#mongodb-variable-variable.IDX) aggregation system variable to access the index of the current array element if you omit `arrayIndexAs`.

### Field Paths

[Field path](/docs/manual/reference/glossary#std-term-field-path) expressions access fields in input documents. Prefix the field name with a dollar sign `$`. For example, `"$user"` references the `user` field, and `"$user.name"` references the embedded `user.name` field.

For more examples, see [Field Paths.](/docs/manual/core/field-paths#std-label-agg-field-paths)

## Update Documents Using an Aggregation Pipeline

To update documents with an aggregation pipeline, use:

| Command | `mongosh` Methods |
| --- | --- |
| [`findAndModify`](/docs/manual/reference/command/findAndModify#mongodb-dbcommand-dbcmd.findAndModify) | [db.collection.findOneAndUpdate()](/docs/manual/reference/method/db.collection.findOneAndUpdate#std-label-findOneAndUpdate-agg-pipeline)[db.collection.findAndModify()](/docs/manual/reference/method/db.collection.findAndModify#std-label-findAndModify-agg-pipeline) |
| [`update`](/docs/manual/reference/command/update#mongodb-dbcommand-dbcmd.update) | [db.collection.updateOne()](/docs/manual/reference/method/db.collection.updateOne#std-label-updateOne-example-agg)[db.collection.updateMany()](/docs/manual/reference/method/db.collection.updateMany#std-label-updateMany-example-agg) [Bulk.find.update()](/docs/manual/reference/method/Bulk.find.update#std-label-example-bulk-find-update-agg)[Bulk.find.updateOne()](/docs/manual/reference/method/Bulk.find.updateOne#std-label-example-bulk-find-update-one-agg)[Bulk.find.upsert()](/docs/manual/reference/method/Bulk.find.upsert#std-label-bulk-find-upsert-update-agg-example) |

## Other Considerations

### Aggregation Pipeline Limitations

For limits on value types and result size, see [Aggregation Pipeline Limits.](/docs/manual/core/aggregation-pipeline-limits#std-label-agg-pipeline-limits)

### Aggregation Pipelines and Sharded Collections

Aggregation pipelines support operations on sharded collections. See [Aggregation Pipeline and Sharded Collections.](/docs/manual/core/aggregation-pipeline-sharded-collections#std-label-aggregation-pipeline-sharded-collection)

**Important: Aggregation Pipelines as an Alternative to Map-Reduce**

Starting in MongoDB 5.0, [map-reduce](/docs/manual/core/map-reduce#std-label-map-reduce) is deprecated.

For examples of aggregation pipeline alternatives to map-reduce, see:

- [Map-Reduce to Aggregation Pipeline](/docs/manual/reference/map-reduce-to-aggregation-pipeline#std-label-map-reduce-to-agg-pipeline)

- [Map-Reduce Examples](/docs/manual/tutorial/map-reduce-examples#std-label-map-reduce-examples)

## Learn More

To learn more about aggregation pipelines, see:

- [Expressions](/docs/manual/reference/mql/expressions#std-label-aggregation-expression-operators)

- [Aggregation Stages](/docs/manual/reference/mql/aggregation-stages#std-label-aggregation-pipeline-operator-reference)
