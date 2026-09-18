> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Read Preference `maxStalenessSeconds`

Replica set members can lag behind the [primary](/docs/manual/reference/glossary#std-term-primary) due to network congestion, low disk throughput, long-running operations, etc. The read preference `maxStalenessSeconds` option lets you specify a maximum replication lag, or "staleness", for reads from [secondaries](/docs/manual/reference/glossary#std-term-secondary). When a secondary's estimated staleness exceeds `maxStalenessSeconds`, the client stops using it for read operations.

**Important:**

The `maxStalenessSeconds` read preference option is intended for applications that read from secondaries and want to avoid reading from a secondary that has fallen overly far behind in replicating the primary's writes. For example, a secondary might stop replicating due to a network outage between itself and the primary. In that case, the client should stop reading from the secondary until an administrator resolves the outage and the secondary catches up.

**Note:**

[Flow control](/docs/manual/replication#std-label-replication-flow-control) limits the rate at which the primary applies its writes with the goal of keeping [`majority committed`](/docs/manual/reference/command/replSetGetStatus#mongodb-data-replSetGetStatus.optimes.lastCommittedOpTime) lag under a specified maximum value.

You can specify `maxStalenessSeconds` with the following read preference modes:

- [`primaryPreferred`](/docs/manual/core/read-preference#mongodb-readmode-primaryPreferred)

- [`secondary`](/docs/manual/reference/glossary#std-term-secondary)

- [`secondaryPreferred`](/docs/manual/core/read-preference#mongodb-readmode-secondaryPreferred)

- [`nearest`](/docs/manual/core/read-preference#mongodb-readmode-nearest)

Max staleness is not compatible with mode [`primary`](/docs/manual/reference/glossary#std-term-primary) and only applies when [selecting](/docs/manual/core/read-preference-mechanics#std-label-replica-set-read-preference-behavior-member-selection) a [secondary](/docs/manual/reference/glossary#std-term-secondary) member of a set for a read operation.

When selecting a server for a read operation with `maxStalenessSeconds`, clients estimate how stale each secondary is by comparing the secondary's last write to that of the primary. The client will then direct the read operation to a secondary whose estimated lag is less than or equal to `maxStalenessSeconds`.

If there is no primary, the client uses the secondary with the most recent write for the comparison.

By default, there is no maximum staleness and clients will not consider a secondary's lag when choosing where to direct a read operation.

You must specify a `maxStalenessSeconds` value of 90 seconds or longer: specifying a smaller `maxStalenessSeconds` value will raise an error. Clients estimate secondaries' staleness by periodically checking the latest write date of each replica set member. Since these checks are infrequent, the staleness estimate is coarse. Thus, clients cannot enforce a `maxStalenessSeconds` value of less than 90 seconds.
