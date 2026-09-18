> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Hidden Replica Set Members

A hidden member maintains a copy of the [primary's](/docs/manual/reference/glossary#std-term-primary) data set but is **invisible** to client applications. Hidden members are good for workloads with different usage patterns from the other members in the [replica set](/docs/manual/reference/glossary#std-term-replica-set). Hidden members must always be [priority 0 members](/docs/manual/core/replica-set-priority-0-member#std-label-replica-set-secondary-only-members) and so **cannot become primary**. The [`db.hello()`](/docs/manual/reference/method/db.hello#mongodb-method-db.hello) method does not display hidden members. Hidden members, however, **may vote** in [elections.](/docs/manual/core/replica-set-elections#std-label-replica-set-elections)

## Behavior

### Read Operations

You can only read from a hidden member if you directly connect to the node. If you connect to a cluster without directly connecting to the hidden node, you cannot run queries on the hidden node. As a result, these members receive no traffic other than basic replication. Use hidden members for dedicated tasks such as reporting and backups.

**Important:**

If your replica set contains [delayed members](/docs/manual/core/replica-set-delayed-member) ensure that the delayed members are hidden and non-voting.

Hiding delayed replica set members prevents applications from seeing and querying delayed data without a direct connection to that member. Making delayed replica set members non-voting means they will not count towards acknowledging write operations with write concern [`"majority"`.](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-)

If you do not hide delayed members and one or more nodes become unavailable, the replica set has to wait for the delayed member and the commit point lags. A lagged commit point can lead to performance issues.

For example, consider a Primary-Secondary-Delayed replica set configuration where the delayed secondary is voting with a 10 minute delay.

With one non-delayed secondary unavailable, the degraded configuration of Primary-Delayed must wait at least 10 minutes to acknowledge a write operation with [`"majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-). The majority commit point will take longer to advance, leading to cache pressure similar performance issues with a [Primary with a Secondary and an Arbiter](/docs/manual/core/replica-set-architecture-three-members#std-label-rs-architecture-psa) (PSA) replica set.

For more information on the majority commit point, see [Causal Consistency and Read and Write Concerns](/docs/manual/core/causal-consistency-read-write-concerns). For additional details on resolving performance issues see the [replica set maintenance tutorial.](/docs/manual/tutorial/mitigate-psa-performance-issues#std-label-performance-issues-psa)

In sharded clusters, you cannot access hidden nodes through [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos). Directly connecting to these nodes to read data can result in data inconsistency or loss. Instead, to achieve workload isolation, use [tag-based read preferences.](/docs/manual/core/read-preference-tags#std-label-replica-set-read-preference-tag-sets)

**Note:**

Starting in MongoDB 8.0, you can only run [certain commands](/docs/manual/reference/supported-shard-direct-commands#std-label-node-direct-commands) on nodes in sharded clusters. If you attempt to connect directly to a node and run an unsupported command, MongoDB returns an error:

```none
"You are connecting to a sharded cluster improperly by connecting directly
to a shard. Please connect to the cluster via a router (mongos)."
```

### Voting

Hidden members *may* vote in replica set elections. If you stop a voting hidden member, ensure that the set has an active majority or the [primary](/docs/manual/reference/glossary#std-term-primary) will step down.

For the purposes of backups,

- [`db.fsyncLock()`](/docs/manual/reference/method/db.fsyncLock#mongodb-method-db.fsyncLock) ensures that the data files are safe to copy using low-level backup utilities such as `cp`, `scp`, or `tar`. A [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) started using the copied files contains user-written data that is indistinguishable from the user-written data on the locked [`mongod`.](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod)

  The data files of a locked [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) may change due to operations such as [journaling syncs](/docs/manual/core/journaling#std-label-journal-process) or [WiredTiger snapshots](/docs/manual/core/wiredtiger#std-label-storage-wiredtiger-checkpoints).  While this has no effect on the logical data (e.g. data accessed by clients), some backup utilities may detect these changes and emit warnings or fail with errors. For more information on MongoDB- recommended backup utilities and procedures, see [Backup Methods for a Self-Managed Deployment.](/docs/manual/core/backups/)

### Write Concern

Hidden replica set members can acknowledge write operations issued with [`w: <number>`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-number-). For write operations issued with [`w : "majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-), however, hidden members must also be voting members (i.e. [`members[n].votes`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.members-n-.votes) greater than `0`) to acknowledge the `"majority"` write operation. Non-voting replica set members (i.e. [`members[n].votes`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.members-n-.votes) is `0`) cannot contribute to acknowledging write operations with `majority` write concern.

## Further Reading

For more information about backing up MongoDB databases, see [Backup Methods for a Self-Managed Deployment](/docs/manual/core/backups). To configure a hidden member, see [Configure a Hidden Self-Managed Replica Set Member.](/docs/manual/tutorial/configure-a-hidden-replica-set-member)
