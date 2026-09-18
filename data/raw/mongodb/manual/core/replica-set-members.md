> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Replica Set Members

A *replica set* in MongoDB is a group of [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) processes that provide redundancy and high availability. The members of a replica set are:

[Primary](/docs/manual/core/replica-set-members#std-label-replica-set-primary-member)

The primary receives all write operations.

[Secondaries](/docs/manual/core/replica-set-members#std-label-replica-set-secondary-members)

Secondaries replicate operations from the primary to maintain an identical data set. Secondaries may have additional configurations for special usage profiles. For example, secondaries may be [non-voting](/docs/manual/core/replica-set-elections#std-label-replica-set-non-voting-members) or [priority 0.](/docs/manual/core/replica-set-priority-0-member#std-label-replica-set-secondary-only-members)

The minimum recommended configuration for a replica set is a three member replica set with three data-bearing members: one [primary](/docs/manual/core/replica-set-members#std-label-replica-set-primary-member) and two [secondary](/docs/manual/core/replica-set-members#std-label-replica-set-secondary-members) members. In some circumstances (such as you have a primary and a secondary but cost constraints prohibit adding another secondary), you may choose to include an [arbiter](/docs/manual/core/replica-set-members#std-label-replica-set-arbiters). An arbiter participates in [elections](/docs/manual/core/replica-set-elections#std-label-replica-set-elections) but does not hold data (i.e. does not provide data redundancy).

A replica set can have up to 50 members but only 7 voting members.

**See also:**

- [`replSetGetStatus.votingMembersCount`](/docs/manual/reference/command/replSetGetStatus#mongodb-data-replSetGetStatus.votingMembersCount)

- [`replSetGetStatus.writableVotingMembersCount`](/docs/manual/reference/command/replSetGetStatus#mongodb-data-replSetGetStatus.writableVotingMembersCount)

## Primary

The primary is the only member in the replica set that receives write operations. MongoDB applies write operations on the [primary](/docs/manual/reference/glossary#std-term-primary) and then records the operations on the primary's [oplog](/docs/manual/core/replica-set-oplog). [Secondary](/docs/manual/core/replica-set-members#std-label-replica-set-secondary-members) members replicate this log and apply the operations to their data sets.

In the following three-member replica set, the primary accepts all write operations. Then the secondaries replicate the oplog to apply to their data sets.

![Diagram of default routing of reads and writes to the primary.](/images/replica-set-read-write-operations-primary.bakedsvg.svg)

All members of the replica set can accept read operations. However, by default, an application directs its read operations to the primary member. See [Read Preference](/docs/manual/core/read-preference) for details on changing the default read behavior.

The replica set can have at most one primary.  If the current primary becomes unavailable, an election determines the new primary. See [Replica Set Elections](/docs/manual/core/replica-set-elections) for more details.

## Secondaries

A secondary maintains a copy of the [primary's](/docs/manual/reference/glossary#std-term-primary) data set. To replicate data, a secondary applies operations from the primary's [oplog](/docs/manual/core/replica-set-oplog#std-label-replica-set-oplog) to its own data set in an asynchronous process.  A replica set can have one or more secondaries.

The following three-member replica set has two secondary members. The secondaries replicate the primary's oplog and apply the operations to their data sets.

![Diagram of a 3 member replica set that consists of a primary and two secondaries.](/images/replica-set-primary-with-two-secondaries.bakedsvg.svg)

Although clients cannot write data to secondaries, clients can read data from secondary members. See [Read Preference](/docs/manual/core/read-preference) for more information on how clients direct read operations to replica sets.

A secondary can become a primary. If the current primary becomes unavailable, the replica set holds an [election](/docs/manual/reference/glossary#std-term-election) to choose which of the secondaries becomes the new primary.

See [Replica Set Elections](/docs/manual/core/replica-set-elections) for more details.

You can configure a secondary member for a specific purpose. You can configure a secondary to:

- Prevent it from becoming a primary in an election, which allows it to reside in a secondary data center or to serve as a cold standby. See [Priority 0 Replica Set Members.](/docs/manual/core/replica-set-priority-0-member)

- Prevent applications from reading from it, which allows it to run applications that require separation from normal traffic. See [Hidden Replica Set Members.](/docs/manual/core/replica-set-hidden-member)

- Keep a running "historical" snapshot for use in recovery from certain errors, such as unintentionally deleted databases. See [Delayed Replica Set Members.](/docs/manual/core/replica-set-delayed-member)

Secondary members of a replica set now [log oplog entries](/docs/manual/core/replica-set-oplog#std-label-slow-oplog-application) that take longer than the slow operation threshold to apply. These slow oplog messages:

- Are logged for the secondaries in the [`diagnostic log`.](/docs/manual/reference/program/mongod#std-option-mongod.--logpath)

- Are logged under the [`REPL`](/docs/manual/reference/log-messages#mongodb-data-REPL) component with the text `applied op: <oplog entry> took <num>ms`.

- Do not depend on the log levels (either at the system or component level)

- Do not depend on the profiling level.

- Are affected by [`slowOpSampleRate`.](/docs/manual/reference/configuration-options#mongodb-setting-operationProfiling.slowOpSampleRate)

The profiler does not capture slow oplog entries.

## Arbiter

In some circumstances (such as when you have a primary and a secondary, but cost constraints prohibit adding another secondary), you may choose to add an arbiter to your replica set. An arbiter participates in [elections for primary](/docs/manual/core/replica-set-elections#std-label-replica-set-elections) but an arbiter does **not** have a copy of the data set and **cannot** become a primary.

An arbiter has exactly `1` election vote. By default an arbiter has priority `0`.

**Important:**

Do not run an arbiter on systems that also host the primary or the secondary members of the replica set.

**Warning:**

Using a [primary-secondary-arbiter (PSA)](/docs/manual/core/replica-set-architecture-three-members#std-label-rs-architecture-psa) architecture for shards in a sharded cluster can cause a loss of availability if a data-bearing secondary is unavailable. A PSA cluster differs from a typical replica set: In a sharded cluster, shards perform `w: majority` [write concern operations](/docs/manual/reference/write-concern) that cannot complete if the remaining cluster members required to confirm an operation have an arbiter.

To add an arbiter, see [Add an Arbiter to a Self-Managed Replica Set.](/docs/manual/tutorial/add-replica-set-arbiter)

For considerations when using an arbiter, see [Replica Set Arbiter.](/docs/manual/core/replica-set-arbiter)

In [some circumstances](/docs/manual/core/read-preference-use-cases#std-label-edge-cases), two nodes in a replica set may *transiently* believe that they are the primary, but at most, one of them will be able to complete writes with [`{ w: "majority" }`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) write concern. The node that can complete [`{ w: "majority" }`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) writes is the current primary, and the other node is a former primary that has not yet recognized its demotion, typically due to a [network partition](/docs/manual/reference/glossary#std-term-network-partition). When this occurs, clients that connect to the former primary may observe stale data despite having requested read preference [`primary`](/docs/manual/reference/glossary#std-term-primary), and new writes to the former primary will eventually roll back.
