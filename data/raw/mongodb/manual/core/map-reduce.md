> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Map-Reduce

**Note: Aggregation Pipeline as Alternative**

Starting in MongoDB 5.0, [map-reduce](/docs/manual/core/map-reduce#std-label-map-reduce) is deprecated:

- Instead of [map-reduce](/docs/manual/core/map-reduce#std-label-map-reduce), you should use an [aggregation pipeline](/docs/manual/core/aggregation-pipeline#std-label-aggregation-pipeline). Aggregation pipelines provide better performance and usability than map-reduce.

- You can rewrite map-reduce operations using [aggregation pipeline stages](/docs/manual/reference/mql/aggregation-stages#std-label-aggregation-pipeline-operator-reference), such as [`$group`](/docs/manual/reference/operator/aggregation/group#mongodb-pipeline-pipe.-group), [`$merge`](/docs/manual/reference/operator/aggregation/merge#mongodb-pipeline-pipe.-merge), and others.

- For map-reduce operations that require custom functionality, you can use the [`$accumulator`](/docs/manual/reference/operator/aggregation/accumulator#mongodb-group-grp.-accumulator) and [`$function`](/docs/manual/reference/operator/aggregation/function#mongodb-expression-exp.-function) aggregation operators. You can use those operators to define custom aggregation expressions in JavaScript.

For examples of aggregation pipeline alternatives to map-reduce, see:

- [Map-Reduce to Aggregation Pipeline](/docs/manual/reference/map-reduce-to-aggregation-pipeline#std-label-map-reduce-to-agg-pipeline)

- [Map-Reduce Examples](/docs/manual/tutorial/map-reduce-examples#std-label-map-reduce-examples)

You can [run aggregation pipelines in the UI](https://www.mongodb.com/docs/atlas/atlas-ui/agg-pipeline/) for deployments hosted in [MongoDB Atlas.](https://www.mongodb.com/docs/atlas)

Map-reduce is a data processing paradigm for condensing large volumes of data into *aggregated* results. To perform map-reduce operations, MongoDB provides the [`mapReduce`](/docs/manual/reference/command/mapReduce#mongodb-dbcommand-dbcmd.mapReduce) database command.

Consider the following map-reduce operation:

![Diagram of the annotated map-reduce operation.](/images/map-reduce.bakedsvg.svg)

MongoDB applies the *map* phase to each input document (the documents in the collection that match the query condition). The map function emits key-value pairs. For keys that have multiple values, MongoDB applies the *reduce* phase, which collects and condenses the data, and then stores the results in a collection. The output of the reduce function can optionally pass through a *finalize* function to further process the results.

All map-reduce functions in MongoDB are JavaScript and run within the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) process. Map-reduce operations take a single [collection](/docs/manual/reference/glossary#std-term-collection) as input and can apply sorting and limiting before the map stage. [`mapReduce`](/docs/manual/reference/command/mapReduce#mongodb-dbcommand-dbcmd.mapReduce) can return results as a document or write them to a collection.

**Note:**

Map-reduce is unsupported for MongoDB Atlas Free and Flex clusters.

## Map-Reduce JavaScript Functions

Map-reduce operations use custom JavaScript functions to *map* values to a key. If a key has multiple values, the operation *reduces* them to a single object. A map function can emit multiple key-value pairs or none. An optional finalize function can make further modifications to the results.

## Map-Reduce Results

A map-reduce operation can write results to a collection or return them inline. If you write results to a collection, you can run subsequent map-reduce operations against the same input collection that replace, merge, or reduce new results with previous results. See [`mapReduce`](/docs/manual/reference/command/mapReduce#mongodb-dbcommand-dbcmd.mapReduce) and [Perform Incremental Map-Reduce](/docs/manual/tutorial/perform-incremental-map-reduce#std-label-incremental-map-reduce) for examples.

When returning results *inline*, the result documents must fit within the [BSON Document Size](/docs/manual/reference/limits#mongodb-limit-BSON-Document-Size) limit of 16 mebibytes. For more limits and restrictions, see [`mapReduce`.](/docs/manual/reference/command/mapReduce#mongodb-dbcommand-dbcmd.mapReduce)

## Sharded Collections

MongoDB supports map-reduce operations on [sharded collections.](/docs/manual/sharding#std-label-sharding-background)

## Views

[Views](/docs/manual/core/views#std-label-views-landing-page) do not support map-reduce operations.
