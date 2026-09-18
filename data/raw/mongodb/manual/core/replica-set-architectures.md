> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Replica Set Deployment Architectures

The architecture of a [replica set](/docs/manual/reference/glossary#std-term-replica-set) affects the set's capacity and capability. This document provides strategies for replica set deployments and describes common architectures.

The standard replica set deployment for a production system is a three-member replica set. These sets provide redundancy and fault tolerance. Avoid complexity when possible, but let your application requirements dictate the architecture.

**Note:**

Outside of a rolling upgrade, all [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) members of a [replica set](/docs/manual/reference/glossary#std-term-replica-set) should use the same major version of MongoDB.

## Strategies

### Determine the Number of Members

Add members in a replica set according to these strategies.

#### Maximum Number of Voting Members

A replica set can have up to [50 members](/docs/manual/reference/limits#mongodb-limit-Number-of-Members-of-a-Replica-Set), but only [7 voting members](/docs/manual/reference/limits#mongodb-limit-Number-of-Voting-Members-of-a-Replica-Set). If the replica set already has 7 voting members, additional members must be [non-voting members.](/docs/manual/core/replica-set-elections#std-label-replica-set-non-voting-members)

#### Deploy an Odd Number of Members

Ensure that the replica set has an odd number of voting members. A replica set can have up to 7 voting members. If you have an *even* number of voting members, deploy another data bearing voting member or, if constraints prohibit against another data bearing voting member, an [arbiter.](/docs/manual/core/replica-set-members#std-label-replica-set-arbiters)

An [arbiter](/docs/manual/reference/glossary#std-term-arbiter) does not store a copy of the data and requires fewer resources. As a result, you may run an arbiter on an application server or other shared resource. With no copy of the data, it may be possible to place an arbiter into environments that you would not place other members of the replica set. Consult your security policies.

**Warning:**

Avoid deploying more than one [arbiter](/docs/manual/reference/glossary#std-term-arbiter) in a [replica set](/docs/manual/reference/glossary#std-term-replica-set). See [Concerns with Multiple Arbiters.](/docs/manual/core/replica-set-arbiter#std-label-rollbacks-multi-arbiters)

To add an arbiter to an existing replica set:

- Typically, if there are two or fewer data-bearing members in the replica set, you might need to first set the [cluster wide write concern](/docs/manual/reference/command/setDefaultRWConcern#std-label-set_global_default_write_concern) for the replica set.

- See [cluster wide write concern](/docs/manual/reference/command/setDefaultRWConcern#std-label-set_global_default_write_concern) for more information on why you might need to set the cluster wide write concern.

You do not need to change the cluster wide write concern before starting a new replica set with an arbiter.

**See also:**

[Default write concern formula](/docs/manual/reference/mongodb-defaults#std-label-default-wc-formula)

#### Consider Fault Tolerance

*Fault tolerance* for a replica set is the number of members that can become unavailable and still leave enough members in the set to elect a primary. In other words, it is the difference between the number of members in the set and the [`majority`](/docs/manual/reference/command/replSetGetStatus#mongodb-data-replSetGetStatus.majorityVoteCount) of voting members needed to elect a primary. Without a primary, a replica set cannot accept write operations. Fault tolerance is an effect of replica set size, but the relationship is not direct. See the following table:

| Number of Members | Majority Required to Elect a New Primary | Fault Tolerance |
| --- | --- | --- |
| 3 | 2 | 1 |
| 4 | 3 | 1 |
| 5 | 3 | 2 |
| 6 | 4 | 2 |

Adding a member to the replica set does not *always* increase the fault tolerance. However, in these cases, additional members can provide support for dedicated functions, such as backups or reporting.

[`rs.status()`](/docs/manual/reference/method/rs.status#mongodb-method-rs.status) returns [`majorityVoteCount`](/docs/manual/reference/command/replSetGetStatus#mongodb-data-replSetGetStatus.majorityVoteCount) for the replica set.

#### Use Hidden and Delayed Members for Dedicated Functions

Add [hidden](/docs/manual/core/replica-set-hidden-member#std-label-replica-set-hidden-members) or [delayed](/docs/manual/core/replica-set-delayed-member#std-label-replica-set-delayed-members) members to support dedicated functions, such as backup or reporting.

#### Read-Heavy Applications

A replica set is designed for high availability and redundancy. In most cases secondary members operate under similar loads as the primary. You should not direct reads to secondaries.

If you have a read-heavy application, consider using [Mongosync](https://www.mongodb.com/docs/cluster-to-cluster-sync/current/#std-label-c2c-index) to replicate data to another cluster for reading.

For more information on secondary read modes, see: [`secondary`](/docs/manual/reference/glossary#std-term-secondary) and [`secondaryPreferred`.](/docs/manual/core/read-preference#mongodb-readmode-secondaryPreferred)

#### Add Capacity Ahead of Demand

The existing members of a replica set must have spare capacity to support adding a new member. Always add new members before the current demand saturates the capacity of the set.

### Distribute Members Geographically

To protect your data in case of a data center failure, keep at least one member in an alternate data center. If possible, use an odd number of data centers, and choose a distribution of members that maximizes the likelihood that even with a loss of a data center, the remaining replica set members can form a majority or at minimum, provide a copy of your data.

**Note:**

For production deployments, we recommend deplying config server and shard replica sets on at least three data centers. This configuration provides high availability in case a single data center goes down.

To ensure that the members in your main data center be elected primary before the members in the alternate data center, set the [`members[n].priority`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.members-n-.priority) of the members in the alternate data center to be lower than that of the members in the primary data center.

For more information, see [Replica Sets Distributed Across Two or More Data Centers](/docs/manual/core/replica-set-architecture-geographically-distributed)

### Target Operations with Tag Sets

Use [replica set tag sets](/docs/manual/tutorial/configure-replica-set-tag-sets#std-label-replica-set-configuration-tag-sets) to target read operations to specific members or to customize write concern to request acknowledgment from specific members.

**See also:**

- [Data Center Awareness](/docs/manual/data-center-awareness#std-label-data-center-awareness)

- [Workload Isolation in MongoDB Deployments](/docs/manual/core/workload-isolation)

### Use Journaling to Protect Against Power Failures

MongoDB enables [journaling](/docs/manual/core/journaling#std-label-journaling-internals) by default. Journaling protects against data loss in the event of service interruptions, such as power failures and unexpected reboots.

### Hostnames

**Important:**

To avoid configuration updates due to IP address changes, use DNS hostnames instead of IP addresses. It is particularly important to use a DNS hostname instead of an IP address when configuring replica set members or sharded cluster members.

Use hostnames instead of IP addresses to configure clusters across a split network horizon. Starting in MongoDB 5.0, nodes that are only configured with an IP address fail startup validation and do not start.

## Replica Set Naming

If your application connects to more than one replica set, each set must have a distinct name. Some drivers group replica set connections by replica set name.

## Deployment Patterns

The following documents describe common replica set deployment patterns. Other patterns are possible and effective depending on the application's requirements. If needed, combine features of each architecture in your own deployment:

[Three Member Replica Sets](/docs/manual/core/replica-set-architecture-three-members)

Three-member replica sets provide the minimum recommended architecture for a replica set.

[Replica Sets Distributed Across Two or More Data Centers](/docs/manual/core/replica-set-architecture-geographically-distributed)

Geographically distributed sets include members in multiple locations to protect against facility-specific failures, such as power outages.
