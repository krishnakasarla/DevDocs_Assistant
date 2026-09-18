> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Replica Set Primary

The primary is the only member in the replica set that receives write operations. MongoDB applies write operations on the [primary](/docs/manual/reference/glossary#std-term-primary) and then records the operations on the primary's [oplog](/docs/manual/core/replica-set-oplog). [Secondary](/docs/manual/core/replica-set-members#std-label-replica-set-secondary-members) members replicate this log and apply the operations to their data sets.

In the following three-member replica set, the primary accepts all write operations. Then the secondaries replicate the oplog to apply to their data sets.

![Diagram of default routing of reads and writes to the primary.](/images/replica-set-read-write-operations-primary.bakedsvg.svg)

All members of the replica set can accept read operations. However, by default, an application directs its read operations to the primary member. See [Read Preference](/docs/manual/core/read-preference) for details on changing the default read behavior.

The replica set can have at most one primary.  If the current primary becomes unavailable, an election determines the new primary. See [Replica Set Elections](/docs/manual/core/replica-set-elections) for more details.

In the following 3-member replica set, the primary becomes unavailable. This triggers an election which selects one of the remaining secondaries as the new primary.

![Election in a three-member replica set after the primary becomes unreachable; a secondary is elected.](/images/replica-set-trigger-election.bakedsvg.svg)

In [some circumstances](/docs/manual/core/read-preference-use-cases#std-label-edge-cases), two nodes in a replica set may *transiently* believe that they are the primary, but at most, one of them will be able to complete writes with [`{ w: "majority" }`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) write concern. The node that can complete [`{ w: "majority" }`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) writes is the current primary, and the other node is a former primary that has not yet recognized its demotion, typically due to a [network partition](/docs/manual/reference/glossary#std-term-network-partition). When this occurs, clients that connect to the former primary may observe stale data despite having requested read preference [`primary`](/docs/manual/reference/glossary#std-term-primary), and new writes to the former primary will eventually roll back.
