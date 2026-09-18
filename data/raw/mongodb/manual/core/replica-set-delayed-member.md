> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Delayed Replica Set Members

Delayed members contain copies of a [replica set's](/docs/manual/reference/glossary#std-term-replica-set) data set. However, a delayed member's data set reflects an earlier, or delayed, state of the set. For example, if the current time is 09:52 and a member has a delay of an hour, the delayed member has no operation more recent than 08:52.

Because delayed members are a "rolling backup" or a running "historical" snapshot of the data set, they may help you recover from various kinds of human error. For example, a delayed member can make it possible to recover from unsuccessful application upgrades and operator errors including dropped databases and collections.

## Considerations

### Requirements

Delayed members:

- **Must be** [priority 0](/docs/manual/core/replica-set-priority-0-member#std-label-replica-set-secondary-only-members) members. Set the priority to 0 to prevent a delayed member from becoming primary.

- **Must be** [hidden](/docs/manual/core/replica-set-hidden-member#std-label-replica-set-hidden-members) members. Always prevent applications from seeing and querying delayed members.

- *Do* vote in [elections](/docs/manual/reference/glossary#std-term-election) for primary, if [`members[n].votes`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.members-n-.votes) is set to 1. Ensuring that delayed members are non-voting by setting [`members[n].votes`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.members-n-.votes) to 0 can help improve performance.

**Important:**

If your replica set contains [delayed members](/docs/manual/core/replica-set-delayed-member) ensure that the delayed members are hidden and non-voting.

Hiding delayed replica set members prevents applications from seeing and querying delayed data without a direct connection to that member. Making delayed replica set members non-voting means they will not count towards acknowledging write operations with write concern [`"majority"`.](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-)

If you do not hide delayed members and one or more nodes become unavailable, the replica set has to wait for the delayed member and the commit point lags. A lagged commit point can lead to performance issues.

For example, consider a Primary-Secondary-Delayed replica set configuration where the delayed secondary is voting with a 10 minute delay.

With one non-delayed secondary unavailable, the degraded configuration of Primary-Delayed must wait at least 10 minutes to acknowledge a write operation with [`"majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-). The majority commit point will take longer to advance, leading to cache pressure similar performance issues with a [Primary with a Secondary and an Arbiter](/docs/manual/core/replica-set-architecture-three-members#std-label-rs-architecture-psa) (PSA) replica set.

For more information on the majority commit point, see [Causal Consistency and Read and Write Concerns](/docs/manual/core/causal-consistency-read-write-concerns). For additional details on resolving performance issues see the [replica set maintenance tutorial.](/docs/manual/tutorial/mitigate-psa-performance-issues#std-label-performance-issues-psa)

### Behavior

Delayed members copy and apply operations from the source [oplog](/docs/manual/reference/glossary#std-term-oplog) on a delay. When choosing the amount of delay, consider that the amount of delay:

- must be equal to or greater than your expected maintenance window durations.

- must be *smaller* than the capacity of the oplog. For more information on oplog size, see [Oplog Size.](/docs/manual/core/replica-set-oplog#std-label-replica-set-oplog-sizing)

### Write Concern

Delayed replica set members can acknowledge write operations issued with either:

- [`w: <number>`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-number-). In this case, delayed members can acknowledge write operations even if they are non-voting members.

- [`w : "majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-). In this case, delayed members must be voting members (that is, [`members[n].votes`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.members-n-.votes) greater than `0`) to acknowledge the write operation. Non-voting replica set members (that is, [`members[n].votes`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.members-n-.votes) is `0`) cannot contribute to acknowledging write operations with `majority` write concern.

Delayed secondaries can return write acknowledgment no earlier than the configured [`secondaryDelaySecs`.](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.members-n-.secondaryDelaySecs)

For more information, refer to the [write concern "w" Option.](/docs/manual/reference/write-concern#std-label-wc-w)

### Sharding

In sharded clusters, delayed members have limited utility when the [balancer](/docs/manual/reference/glossary#std-term-balancer) is enabled. Because delayed members replicate chunk migrations with a delay, the state of delayed members in a sharded cluster are not useful for recovering to a previous state of the sharded cluster if any migrations occur during the delay window.

## Example

In the following 5-member replica set, the primary and all secondaries have copies of the data set. One member applies operations with a delay of 3600 seconds (one hour). This delayed member is also *hidden* and is a *priority 0 member*.

![Diagram of a 5 member replica set with a hidden delayed priority 0 member.](/images/replica-set-delayed-member.bakedsvg.svg)

## Configuration

A delayed member has its [`members[n].priority`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.members-n-.priority) equal to `0`, [`members[n].hidden`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.members-n-.hidden) equal to `true`, and its [`members[n].secondaryDelaySecs`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.members-n-.secondaryDelaySecs) equal to the number of seconds of delay:

```javascript
{
   "_id" : <num>,
   "host" : <hostname:port>,
   "priority" : 0,
   "secondaryDelaySecs" : <seconds>,
   "hidden" : true
}
```

To configure a delayed member, see [Configure a Delayed Self-Managed Replica Set Member.](/docs/manual/tutorial/configure-a-delayed-replica-set-member)
