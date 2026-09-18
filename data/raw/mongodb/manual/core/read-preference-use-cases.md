> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Read Preference Use Cases

The following document explains common use cases for various [read preference](/docs/manual/core/read-preference#std-label-read-preference) modes, as well as [counter-indications](/docs/manual/core/read-preference-use-cases#std-label-read-preference-counter-indications) outlining when you should not change the read preference from the default [`primary`.](/docs/manual/reference/glossary#std-term-primary)

## Read Preference Modes

| Read Preference Mode | Description |
| --- | --- |
| [`primary`](/docs/manual/reference/glossary#std-term-primary) | Default mode. All operations read from the current replica set [primary.](/docs/manual/reference/glossary#std-term-primary) [Transactions](/docs/manual/core/transactions#std-label-transactions) that contain read operations must use read preference [`primary`](/docs/manual/reference/glossary#std-term-primary). All operations in a given transaction must route to the same member. |
| [`primaryPreferred`](/docs/manual/core/read-preference#mongodb-readmode-primaryPreferred) | In most situations, operations read from the [primary](/docs/manual/reference/glossary#std-term-primary) but if it is unavailable, operations read from [secondary](/docs/manual/reference/glossary#std-term-secondary) members. |
| [`secondary`](/docs/manual/reference/glossary#std-term-secondary) | All operations read from the [secondary](/docs/manual/reference/glossary#std-term-secondary) members of the replica set. |
| [`secondaryPreferred`](/docs/manual/core/read-preference#mongodb-readmode-secondaryPreferred) | Operations typically read data from [secondary](/docs/manual/reference/glossary#std-term-secondary) members of the replica set. If the replica set has only one single [primary](/docs/manual/reference/glossary#std-term-primary) member and no other members, operations read data from the primary member. |
| [`nearest`](/docs/manual/core/read-preference#mongodb-readmode-nearest) | Operations read from a random eligible [replica set](/docs/manual/reference/glossary#std-term-replica-set) member, irrespective of whether that member is a [primary](/docs/manual/reference/glossary#std-term-primary) or [secondary](/docs/manual/reference/glossary#std-term-secondary), based on a specified latency threshold. The operation considers the following when calculating latency: The [`localThresholdMS`](/docs/manual/reference/connection-string-options#mongodb-urioption-urioption.localThresholdMS) connection string option; The [maxStalenessSeconds](/docs/manual/core/read-preference-staleness#std-label-replica-set-read-preference-max-staleness) read preference option; Any specified [tag set lists](/docs/manual/tutorial/configure-replica-set-tag-sets) |

## Indications to Use Non-Primary Read Preference

The following are common use cases for using non-[`primary`](/docs/manual/reference/glossary#std-term-primary) read preference modes:

- Running systems operations that do not affect the front-end application.

  **Note:**

  Read preferences aren't relevant to direct connections to a single [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instance. However, in order to perform read operations on a direct connection to a secondary member of a replica set, you must set a read preference, such as [secondary.](/docs/manual/reference/glossary#std-term-secondary)

- Providing local reads for geographically distributed applications.

  If you have application servers in multiple data centers, you may consider having a [geographically distributed replica set](/docs/manual/core/replica-set-architecture-geographically-distributed#std-label-replica-set-geographical-distribution) and using a non primary or [`nearest`](/docs/manual/core/read-preference#mongodb-readmode-nearest) read preference. This allows the client to read from the lowest-latency members, rather than always reading from the primary.

- Maintaining availability during a failover.

  Use [`primaryPreferred`](/docs/manual/core/read-preference#mongodb-readmode-primaryPreferred) if you want an application to read from the primary under normal circumstances, but to allow [stale reads](/docs/manual/reference/glossary#std-term-stale-read) from secondaries when the primary is unavailable.

## Counter-Indications for Non-Primary Read Preference

In general, do *not* use [`secondary`](/docs/manual/reference/glossary#std-term-secondary) and [`secondaryPreferred`](/docs/manual/core/read-preference#mongodb-readmode-secondaryPreferred) to provide extra capacity for reads, because:

- All members of a replica have roughly equivalent write traffic; as a result, secondaries will service reads at roughly the same rate as the primary.

- Replication is asynchronous and there is some amount of delay between a successful write operation and its replication to secondaries. Reading from a secondary can return stale data; reading from different secondaries may result in non-monotonic reads.

  **Note:**

  Clients can use [Client Sessions and Causal Consistency Guarantees](/docs/manual/core/read-isolation-consistency-recency#std-label-sessions) to ensure monotonic reads.

- Distributing read operations to secondaries can compromise availability if *any* members of the set become unavailable because the remaining members of the set will need to be able to handle all application requests.

[Sharding](/docs/manual/sharding#std-label-sharding-background) increases read and write capacity by distributing read and write operations across a group of machines, and is often a better strategy for adding capacity.

See [Server Selection Algorithm](/docs/manual/core/read-preference-mechanics) for more information about the internal application of read preferences.

## Maximize Consistency

To avoid *stale* reads, use [`primary`](/docs/manual/reference/glossary#std-term-primary) read preference and [`"majority"`](/docs/manual/reference/read-concern-majority#mongodb-readconcern-readconcern.-majority-) `readConcern`. If the primary is unavailable, e.g. during elections or when a majority of the replica set is not accessible, read operations using [`primary`](/docs/manual/reference/glossary#std-term-primary) read preference produce an error or throw an exception.

In some circumstances, it may be possible for a replica set to temporarily have two primaries; however, only one primary will be capable of confirming writes with the [`"majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) write concern.

- A partial [network partition](/docs/manual/reference/glossary#std-term-network-partition) may segregate a primary (`P` old) into a partition with a minority of the nodes, while the other side of the partition contains a majority of nodes. The partition with the majority will elect a new primary (`P` new), but for a brief period, the old primary (`P` old) may still continue to serve reads and writes, as it has not yet detected that it can only see a minority of nodes in the replica set. During this period, if the old primary (`P` old) is still visible to clients as a primary, reads from this primary may reflect stale data.

- A primary (`P` old) may become unresponsive, which will trigger an election and a new primary (`P` new) can be elected, serving reads and writes. If the unresponsive primary (`P` old) starts responding again, two primaries will be visible for a brief period. The brief period will end when `P` old steps down. However, during the brief period, clients might read from the old primary `P` old, which can provide stale data.

To increase consistency, you can disable automatic [failover](/docs/manual/reference/glossary#std-term-failover); however, disabling automatic failover sacrifices availability.

## Maximize Availability

To permit read operations when possible, use [`primaryPreferred`](/docs/manual/core/read-preference#mongodb-readmode-primaryPreferred). When there's a primary you will get consistent reads , but if there is no primary you can still query [secondaries](/docs/manual/reference/glossary#std-term-secondary). However, when using this read mode, consider the situation described in [`secondary` vs `secondaryPreferred`.](/docs/manual/core/read-preference-use-cases#std-label-caveat-secondaryPreferred)

In [some circumstances](/docs/manual/core/read-preference-use-cases#std-label-edge-cases), two nodes in a replica set may *transiently* believe that they are the primary, but at most, one of them will be able to complete writes with [`{ w: "majority" }`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) write concern. The node that can complete [`{ w: "majority" }`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) writes is the current primary, and the other node is a former primary that has not yet recognized its demotion, typically due to a [network partition](/docs/manual/reference/glossary#std-term-network-partition). When this occurs, clients that connect to the former primary may observe stale data despite having requested read preference [`primary`](/docs/manual/reference/glossary#std-term-primary), and new writes to the former primary will eventually roll back.

## Minimize Latency

To always read from a low-latency node, use [`nearest`](/docs/manual/core/read-preference#mongodb-readmode-nearest). The driver or [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) will read from the nearest member and those no more than 15 milliseconds  further away than the nearest member.

[`nearest`](/docs/manual/core/read-preference#mongodb-readmode-nearest) does *not* guarantee consistency. If the nearest member to your application server is a secondary with some replication lag, queries could return stale data. [`nearest`](/docs/manual/core/read-preference#mongodb-readmode-nearest) only reflects network distance and does not reflect I/O or CPU load.

This threshold is configurable. See [`localPingThresholdMs`](/docs/manual/reference/configuration-options#mongodb-setting-replication.localPingThresholdMs) for [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) or your driver documentation for the appropriate setting.

## Query From Geographically Distributed Members

If the members of a replica set are geographically distributed, you can create replica tags based that reflect the location of the instance and then configure your application to query the members nearby.

For example, if members in "east" and "west" data centers are [tagged](/docs/manual/tutorial/configure-replica-set-tag-sets#std-label-replica-set-configuration-tag-sets) `{'dc': 'east'}` and `{'dc': 'west'}`, your application servers in the east data center can read from nearby members with the following read preference:

```javascript
db.collection.find().readPref('nearest', [ { 'dc': 'east' } ])
```

Although [`nearest`](/docs/manual/core/read-preference#mongodb-readmode-nearest) already favors members with low network latency, including the tag makes the choice more predictable.

## `secondary` vs `secondaryPreferred`

For specific dedicated queries (e.g. ETL, reporting), you may shift the read load from the primary by using the [`secondary`](/docs/manual/reference/glossary#std-term-secondary) read preference mode. For this use case, the [`secondary`](/docs/manual/reference/glossary#std-term-secondary) mode is preferable to the [`secondaryPreferred`](/docs/manual/core/read-preference#mongodb-readmode-secondaryPreferred) mode because [`secondaryPreferred`](/docs/manual/core/read-preference#mongodb-readmode-secondaryPreferred) risks the following situation: if all secondaries are unavailable and your replica set has enough [arbiters](/docs/manual/reference/glossary#std-term-arbiter)  to prevent the primary from stepping down, then the primary will receive all traffic from the clients. If the primary is unable to handle this load, the queries will compete with the writes. For this reason, use read preference [`secondary`](/docs/manual/reference/glossary#std-term-secondary) to distribute these specific dedicated queries instead of [`secondaryPreferred`.](/docs/manual/core/read-preference#mongodb-readmode-secondaryPreferred)

In general, avoid deploying arbiters in replica sets and use an odd number of data-bearing nodes instead. If you must deploy arbiters, avoid deploying more than one arbiter per replica set.
