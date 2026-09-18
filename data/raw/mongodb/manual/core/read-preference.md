> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Read Preference

Read preference describes how MongoDB clients route read operations to the members of a [replica set.](/docs/manual/reference/glossary#std-term-replica-set)

![Read operations to a replica set showing default and \`\`nearest\`\` read preference routing.](/images/replica-set-read-preference.bakedsvg.svg)

By default, an application directs its read operations to the [primary](/docs/manual/reference/glossary#std-term-primary) member in a [replica set](/docs/manual/reference/glossary#std-term-replica-set) (that is, read preference mode "primary"). But, clients can specify a read preference to send read operations to secondaries.

Read preference consists of the [read preference mode](/docs/manual/core/read-preference#std-label-read-pref-modes-summary) and optionally, a [tag set list](/docs/manual/core/read-preference-tags#std-label-replica-set-read-preference-tag-sets), and the [maxStalenessSeconds](/docs/manual/core/read-preference-staleness#std-label-replica-set-read-preference-max-staleness) option.

## Read Preference Modes

The following table summarizes the read preference modes:

| Read Preference Mode | Description |
| --- | --- |
| [`primary`](/docs/manual/reference/glossary#std-term-primary) | Default mode. All operations read from the current replica set [primary.](/docs/manual/reference/glossary#std-term-primary) [Transactions](/docs/manual/core/transactions#std-label-transactions) that contain read operations must use read preference [`primary`](/docs/manual/reference/glossary#std-term-primary). All operations in a given transaction must route to the same member. |
| [`primaryPreferred`](/docs/manual/core/read-preference#mongodb-readmode-primaryPreferred) | In most situations, operations read from the [primary](/docs/manual/reference/glossary#std-term-primary) but if it is unavailable, operations read from [secondary](/docs/manual/reference/glossary#std-term-secondary) members. |
| [`secondary`](/docs/manual/reference/glossary#std-term-secondary) | All operations read from the [secondary](/docs/manual/reference/glossary#std-term-secondary) members of the replica set. |
| [`secondaryPreferred`](/docs/manual/core/read-preference#mongodb-readmode-secondaryPreferred) | Operations typically read data from [secondary](/docs/manual/reference/glossary#std-term-secondary) members of the replica set. If the replica set has only one single [primary](/docs/manual/reference/glossary#std-term-primary) member and no other members, operations read data from the primary member. |
| [`nearest`](/docs/manual/core/read-preference#mongodb-readmode-nearest) | Operations read from a random eligible [replica set](/docs/manual/reference/glossary#std-term-replica-set) member, irrespective of whether that member is a [primary](/docs/manual/reference/glossary#std-term-primary) or [secondary](/docs/manual/reference/glossary#std-term-secondary), based on a specified latency threshold. The operation considers the following when calculating latency: The [`localThresholdMS`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.localThresholdMS) connection string option; The [maxStalenessSeconds](/docs/manual/core/read-preference-staleness#std-label-replica-set-read-preference-max-staleness) read preference option; Any specified [tag set lists](/docs/manual/tutorial/configure-replica-set-tag-sets) |

For detailed description of the read preference modes, see [Read Preference Modes.](/docs/manual/core/read-preference#std-label-replica-set-read-preference-modes)

**See also:**

- [Read Preference Tag Set Lists](/docs/manual/core/read-preference-tags#std-label-replica-set-read-preference-tag-sets)

- [Read Preference `maxStalenessSeconds`](/docs/manual/core/read-preference-staleness#std-label-replica-set-read-preference-max-staleness)

## Behavior

- All read preference modes except [`primary`](/docs/manual/reference/glossary#std-term-primary) may return stale data because [secondaries](/docs/manual/reference/glossary#std-term-secondary) replicate operations from the primary in an asynchronous process.  Ensure that your application can tolerate stale data if you choose to use a non-[`primary`](/docs/manual/reference/glossary#std-term-primary) mode.

- Read preference does not affect the visibility of data. Clients can see the results of writes before they are acknowledged or have propagated to a majority of replica set members. For details, see [Read Isolation, Consistency, and Recency.](/docs/manual/core/read-isolation-consistency-recency)

- Read preference does not affect [causal consistency](/docs/manual/core/read-isolation-consistency-recency#std-label-causal-consistency). The [causal consistency guarantees](/docs/manual/core/read-isolation-consistency-recency#std-label-sessions) provided by causally consistent sessions for read operations with [`"majority"`](/docs/manual/reference/read-concern-majority#mongodb-readconcern-readconcern.-majority-) read concern and write      operations with [`"majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) write concern hold across all members of the MongoDB deployment.

**Warning:**

Starting in MongoDB version 8.2, long-running secondary reads in a sharded cluster may automatically terminate before orphaned document deletion following a chunk migration.

The [`terminateSecondaryReadsOnOrphanCleanup`](/docs/manual/reference/parameters#mongodb-parameter-param.terminateSecondaryReadsOnOrphanCleanup) parameter controls this behavior. To learn more about handling long-running secondary reads, see [Long-Running Secondary Reads in Sharded Clusters.](/docs/manual/core/long-running-secondary-reads#std-label-long-running-secondary-reads)

## Read Preference Modes

All read operations use only the current replica set [primary](/docs/manual/reference/glossary#std-term-primary).  This is the default read mode. If the primary is unavailable, read operations produce an error or throw an exception.

The [`primary`](/docs/manual/reference/glossary#std-term-primary) read preference mode is not compatible with read preference modes that use [tag set lists](/docs/manual/core/read-preference-tags#std-label-replica-set-read-preference-tag-sets) or [maxStalenessSeconds](/docs/manual/core/read-preference-staleness#std-label-replica-set-read-preference-max-staleness). If you specify tag set lists or a `maxStalenessSeconds` value with [`primary`](/docs/manual/reference/glossary#std-term-primary), the driver will produce an error.

[Transactions](/docs/manual/core/transactions#std-label-transactions) that contain read operations must use read preference [`primary`](/docs/manual/reference/glossary#std-term-primary). All operations in a given transaction must route to the same member.

In most situations, operations read from the [primary](/docs/manual/reference/glossary#std-term-primary) member of the set. However, if the primary is unavailable, as is the case during [failover](/docs/manual/reference/glossary#std-term-failover) situations, operations read from [secondary](/docs/manual/reference/glossary#std-term-secondary) members that satisfy the read preference's `maxStalenessSeconds` and tag set lists.

When the [`primaryPreferred`](/docs/manual/core/read-preference#mongodb-readmode-primaryPreferred) read preference includes a [maxStalenessSeconds value](/docs/manual/core/read-preference-staleness#std-label-replica-set-read-preference-max-staleness) and there is no primary from which to read, the client estimates how stale each secondary is by comparing the secondary's last write to that of the secondary with the most recent write. The client then directs the read operation to a secondary whose estimated lag is less than or equal to `maxStalenessSeconds`.

When the read preference includes a [tag set list (an array of tag sets)](/docs/manual/core/read-preference-tags#std-label-replica-set-read-preference-tag-sets) and there is no primary from which to read, the client attempts to find secondary members with matching tags (trying the tag sets in order until a match is found). If matching secondaries are found, the client selects a random secondary from the [nearest group](/docs/manual/core/read-preference-mechanics#std-label-replica-set-read-preference-behavior-nearest) of matching secondaries. If no secondaries have matching tags, the read operation produces an error.

When the read preference includes a `maxStalenessSeconds` value **and** a tag set list, the client filters by staleness first and then by the specified tags.

Read operations using the [`primaryPreferred`](/docs/manual/core/read-preference#mongodb-readmode-primaryPreferred) mode may return stale data. Use the `maxStalenessSeconds` option to avoid reading from secondaries that the client estimates are overly stale.

In sharded clusters that enable the ingress request rate limiter, shard nodes that are shedding load can return errors labeled `SystemOverloadedError`.

For clusters that have [`overloadAwareServerSelectionEnabled`](/docs/manual/reference/parameters#mongodb-parameter-param.overloadAwareServerSelectionEnabled) set to `true`, when a primary responds with a retryable error labeled with `SystemOverloadedError`, the router may temporarily route reads to eligible secondaries instead of the overloaded server. This applies to any read preference that can select multiple servers. By default, `overloadAwareServerSelectionEnabled` is set to `false`.

Operations read *only* from the [secondary](/docs/manual/reference/glossary#std-term-secondary) members of the set. If no secondaries are available, then this read operation produces an error or exception.

Most replica sets have at least one secondary, but there are situations where there may be no available secondary. For example, a replica set with a [primary](/docs/manual/reference/glossary#std-term-primary), a secondary, and an [arbiter](/docs/manual/reference/glossary#std-term-arbiter) may not have any secondaries if a member is in recovering state or unavailable.

When the [`secondary`](/docs/manual/reference/glossary#std-term-secondary) read preference includes a [maxStalenessSeconds value](/docs/manual/core/read-preference-staleness#std-label-replica-set-read-preference-max-staleness), the client estimates how stale each secondary is by comparing the secondary's last write to that of the primary. The client then directs the read operation to a secondary whose estimated lag is less than or equal to `maxStalenessSeconds`. If there is no primary, the client uses the secondary with the most recent write for the comparison.

When the read preference includes a [tag set list (an array of tag sets)](/docs/manual/core/read-preference-tags#std-label-replica-set-read-preference-tag-sets), the client attempts to find secondary members with matching tags (trying the tag sets in order until a match is found). If matching secondaries are found, the client selects a random secondary from the [nearest group](/docs/manual/core/read-preference-mechanics#std-label-replica-set-read-preference-behavior-nearest) of matching secondaries. If no secondaries have matching tags, the read operation produces an error.

When the read preference includes a `maxStalenessSeconds` value **and** a tag set list, the client filters by staleness first and then by the specified tags.

Read operations using the [`secondary`](/docs/manual/reference/glossary#std-term-secondary) mode may return stale data. Use the `maxStalenessSeconds` option to avoid reading from secondaries that the client estimates are overly stale.

Operations typically read data from [secondary](/docs/manual/reference/glossary#std-term-secondary) members of the replica set. If the replica set has only one single [primary](/docs/manual/reference/glossary#std-term-primary) member and no other members, operations read data from the primary member.

When the [`secondaryPreferred`](/docs/manual/core/read-preference#mongodb-readmode-secondaryPreferred) read preference includes a [maxStalenessSeconds value](/docs/manual/core/read-preference-staleness#std-label-replica-set-read-preference-max-staleness), the client estimates how stale each secondary is by comparing the secondary's last write to that of the primary. The client then directs the read operation to a secondary whose estimated lag is less than or equal to `maxStalenessSeconds`. If there is no primary, the client uses the secondary with the most recent write for the comparison. If there are no secondaries with estimated lag less than or equal to `maxStalenessSeconds`, the client directs the read operation to the replica set's primary.

When the read preference includes a [tag set list (an array of tag sets)](/docs/manual/core/read-preference-tags#std-label-replica-set-read-preference-tag-sets), the client attempts to find secondary members with matching tags (trying the tag sets in order until a match is found). If matching secondaries are found, the client selects a random secondary from the [nearest group](/docs/manual/core/read-preference-mechanics#std-label-replica-set-read-preference-behavior-nearest) of matching secondaries. If no secondaries have matching tags, the client ignores tags and reads from the primary.

When the read preference includes a `maxStalenessSeconds` value **and** a tag set list, the client filters by staleness first and then by the specified tags.

Read operations using the [`secondaryPreferred`](/docs/manual/core/read-preference#mongodb-readmode-secondaryPreferred) mode may return stale data. Use the `maxStalenessSeconds` option to avoid reading from secondaries that the client estimates are overly stale.

The driver reads from a member whose network latency falls within the acceptable latency window. Reads in the [`nearest`](/docs/manual/core/read-preference#mongodb-readmode-nearest) mode do not consider whether a member is a [primary](/docs/manual/reference/glossary#std-term-primary) or [secondary](/docs/manual/reference/glossary#std-term-secondary) when routing read operations: primaries and secondaries are treated equivalently.

Set this mode to minimize the effect of network latency on read operations without preference for current or stale data.

When the read preference includes a [maxStalenessSeconds value](/docs/manual/core/read-preference-staleness#std-label-replica-set-read-preference-max-staleness), the client estimates how stale each secondary is by comparing the secondary's last write to that of the primary, if available, or to the secondary with the most recent write if there is no primary. The client will then filter out any secondary whose estimated lag is greater than `maxStalenessSeconds` and randomly direct the read to a remaining member (primary or secondary) whose network latency falls within the [acceptable latency window.](/docs/manual/core/read-preference-mechanics#std-label-replica-set-read-preference-behavior-nearest)

If you specify a [tag set list](/docs/manual/core/read-preference-tags#std-label-replica-set-read-preference-tag-sets), the client attempts to find a replica set member that matches the specified tag set lists and directs reads to an arbitrary member from among the [nearest group.](/docs/manual/core/read-preference-mechanics#std-label-replica-set-read-preference-behavior-nearest)

When the read preference includes a `maxStalenessSeconds` value **and** a tag set list, the client filters by staleness first and then by the specified tags. From the remaining [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instances, the client then randomly directs the read to an instance that falls within the acceptable latency window. The read preference [member selection](/docs/manual/core/read-preference-mechanics#std-label-replica-set-read-preference-behavior-nearest) documentation describes the process in detail.

Read operations using the [`nearest`](/docs/manual/core/read-preference#mongodb-readmode-nearest) mode may return stale data. Use the `maxStalenessSeconds` option to avoid reading from secondaries that the client estimates are overly stale.

**See also:**

To learn about use cases for specific read preference settings, see [Read Preference Use Cases.](/docs/manual/core/read-preference-use-cases#std-label-read-preference-use-cases)

## Configure Read Preference

When using a MongoDB driver, you can specify the read preference using the driver's read preference API. See the driver [API documentation](https://www.mongodb.com/docs/drivers/). You can also set the read preference when [connecting to the replica set or sharded cluster](/docs/manual/reference/connection-string-options#std-label-connections-read-preference). For an example, see [connection string.](/docs/manual/reference/connection-string-options#std-label-connections-read-preference)

For a given read preference, the MongoDB drivers use the same [member selection logic.](/docs/manual/core/read-preference-mechanics#std-label-replica-set-read-preference-behavior-member-selection)

When using [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh), see [`cursor.readPref()`](/docs/manual/reference/method/cursor.readPref#mongodb-method-cursor.readPref) and [`Mongo.setReadPref()`.](/docs/manual/reference/method/Mongo.setReadPref#mongodb-method-Mongo.setReadPref)

## Read Preference and Transactions

[Transactions](/docs/manual/core/transactions#std-label-transactions) that contain read operations must use read preference [`primary`](/docs/manual/reference/glossary#std-term-primary). All operations in a given transaction must route to the same member.

## Additional Considerations

Consider the following points when using [`$merge`](/docs/manual/reference/operator/aggregation/merge#mongodb-pipeline-pipe.-merge) or [`$out`](/docs/manual/reference/operator/aggregation/out#mongodb-pipeline-pipe.-out) stages in an [aggregation pipeline:](/docs/manual/core/aggregation-pipeline#std-label-aggregation-pipeline)

- Starting in MongoDB 5.0, pipelines with a `$merge` stage can run on replica set [secondary](/docs/manual/reference/glossary#std-term-secondary) nodes if all the nodes in the cluster have the [featureCompatibilityVersion](/docs/manual/reference/command/setFeatureCompatibilityVersion#std-label-view-fcv) set to `5.0` or higher and the [read preference](/docs/manual/core/read-preference#std-label-read-preference) allows secondary reads.

  - `$merge` and `$out` stages run on secondary nodes, but write operations are sent to the [primary](/docs/manual/reference/glossary#std-term-primary) node.

  - Not all driver versions support `$merge` operations sent to the secondary nodes. For details, see the [driver](https://www.mongodb.com/docs/drivers/) documentation.

- In earlier MongoDB versions, pipelines with `$out` or `$merge` stages always run on the primary node and read preference isn't considered.

For [`mapReduce`](/docs/manual/reference/command/mapReduce#mongodb-dbcommand-dbcmd.mapReduce) operations, only "inline" [`mapReduce`](/docs/manual/reference/command/mapReduce#mongodb-dbcommand-dbcmd.mapReduce) operations that do not write data support read preference. Otherwise, [`mapReduce`](/docs/manual/reference/command/mapReduce#mongodb-dbcommand-dbcmd.mapReduce) operations run on the [primary](/docs/manual/reference/glossary#std-term-primary) member.

In [some circumstances](/docs/manual/core/read-preference-use-cases#std-label-edge-cases), two nodes in a replica set may *transiently* believe that they are the primary, but at most, one of them will be able to complete writes with [`{ w: "majority" }`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) write concern. The node that can complete [`{ w: "majority" }`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) writes is the current primary, and the other node is a former primary that has not yet recognized its demotion, typically due to a [network partition](/docs/manual/reference/glossary#std-term-network-partition). When this occurs, clients that connect to the former primary may observe stale data despite having requested read preference [`primary`](/docs/manual/reference/glossary#std-term-primary), and new writes to the former primary will eventually roll back.
