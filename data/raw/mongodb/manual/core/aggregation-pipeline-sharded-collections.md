> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Aggregation Pipeline and Sharded Collections

The aggregation pipeline supports operations on [sharded](/docs/manual/reference/glossary#std-term-sharded-cluster) collections. This section describes behaviors specific to the [aggregation pipeline](/docs/manual/core/aggregation-pipeline#std-label-aggregation-pipeline) and sharded collections.

## Behavior

If the pipeline starts with an exact [`$match`](/docs/manual/reference/operator/aggregation/match#mongodb-pipeline-pipe.-match) on a [shard key](/docs/manual/reference/glossary#std-term-shard-key), and the pipeline does not contain [`$out`](/docs/manual/reference/operator/aggregation/out#mongodb-pipeline-pipe.-out) or [`$lookup`](/docs/manual/reference/operator/aggregation/lookup#mongodb-pipeline-pipe.-lookup) stages, the entire pipeline runs on the matching shard only.

When aggregation operations run on multiple shards, the results are routed to the [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) to be merged, except in the following cases:

- If the pipeline includes the [`$out`](/docs/manual/reference/operator/aggregation/out#mongodb-pipeline-pipe.-out) stage, the merge runs on the shard where the output collection lives.

- If the pipeline includes the [`$lookup`](/docs/manual/reference/operator/aggregation/lookup#mongodb-pipeline-pipe.-lookup) stage that references an unsharded collection, the merge runs on the shard where the unsharded collection lives.

- If the pipeline includes a sorting or grouping stage, and the [allowDiskUse](/docs/manual/reference/command/aggregate#std-label-aggregate-cmd-allowDiskUse) setting is enabled, the merge runs on a randomly-selected shard.

## Optimization

When splitting the aggregation pipeline into two parts, the pipeline is split to ensure that the shards perform as many stages as possible with consideration for optimization.

To see how the pipeline was split, include the [`explain`](/docs/manual/reference/method/db.collection.aggregate#mongodb-method-db.collection.aggregate) option in the [`db.collection.aggregate()`](/docs/manual/reference/method/db.collection.aggregate#mongodb-method-db.collection.aggregate) method.

Optimizations are subject to change between releases.
