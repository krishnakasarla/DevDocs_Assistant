> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Rolling Index Builds

Rolling index builds are an alternative to [the default index builds](/docs/manual/core/index-creation#std-label-index-operations). Rolling indexes build indexes on the applicable nodes sequentially and may reduce the performance impact of an index build if your deployment matches one of the following cases:

- If your average CPU utilization exceeds (N-1)/N-10% where N is the number of CPU threads available to mongod

- If the WiredTiger cache fill ratio regularly exceeds 90%

If your deployment does not meet this criteria, use the [default index build.](/docs/manual/core/index-creation#std-label-index-operations)

**Warning:**

Avoid performing rolling index and replicated index build processes concurrently as it might lead to unexpected issues, such as broken builds and crash loops.

## Considerations

- Rolling index builds hide at most one replica set member at a time, starting with the secondary members, and build the index on that member as a standalone.

- Rolling index builds require at least one replica set election.

- Rolling index builds lower the resiliency of your cluster and increases build duration.

**Note:**

For information about creating indexes in Atlas, refer to the [index management](https://www.mongodb.com/docs/atlas/atlas-ui/indexes/) page in the Atlas documentation.

## Tutorials

To create rolling index builds, use the following tutorials:

- [Create a Rolling Index Build on Replica Sets](/docs/manual/tutorial/build-indexes-on-replica-sets#std-label-index-building-replica-sets)

- [Create Rolling Index Builds on Sharded Clusters](/docs/manual/tutorial/build-indexes-on-sharded-clusters#std-label-index-build-on-sharded-clusters)
