> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Three Member Replica Sets

The minimum number of replica set members needed to obtain the benefits of a replica set is three members. A three member replica set can have either three data-bearing members (Primary-Secondary-Secondary) (*Recommended*) or if circumstances (such as cost) prohibit adding a third data bearing member, two data-bearing members and an arbiter (Primary-Secondary-Arbiter).&#x20;

For considerations when using an arbiter, see [Replica Set Arbiter.](/docs/manual/core/replica-set-arbiter)

## Primary with Two Secondary Members (P-S-S)

A replica set with three members that store data has:

- One [primary.](/docs/manual/core/replica-set-primary#std-label-replica-set-primary)

- Two [secondary](/docs/manual/core/replica-set-secondary#std-label-replica-set-secondary-members-ref) members. Both secondaries can become the primary in an [election.](/docs/manual/core/replica-set-elections#std-label-replica-set-election-internals)

![Diagram of a 3 member replica set that consists of a primary and two secondaries.](/images/replica-set-primary-with-two-secondaries.bakedsvg.svg)

These deployments provide two complete copies of the data set at all times in addition to the primary. These replica sets provide additional fault tolerance and [high availability](/docs/manual/core/replica-set-high-availability#std-label-replica-set-failover). If the primary is unavailable, the replica set elects a secondary to be primary and continues normal operation. The old primary rejoins the set when available.

![Election in a three-member replica set after the primary becomes unreachable; a secondary is elected.](/images/replica-set-trigger-election.bakedsvg.svg)

## Primary with a Secondary and an Arbiter (PSA)

**Note:**

For considerations when using an arbiter, see [Replica Set Arbiter.](/docs/manual/core/replica-set-arbiter)

A three member replica set with a two members that store data has:

- One [primary.](/docs/manual/core/replica-set-primary#std-label-replica-set-primary)

- One [secondary](/docs/manual/core/replica-set-secondary#std-label-replica-set-secondary-members-ref) member. The secondary can become primary in an [election.](/docs/manual/core/replica-set-elections#std-label-replica-set-election-internals)

- One [arbiter](/docs/manual/core/replica-set-arbiter#std-label-replica-set-arbiter-configuration). The arbiter only votes in elections.

![Diagram of a replica set that consists of a primary, a secondary, and an arbiter.](/images/replica-set-primary-with-secondary-and-arbiter.bakedsvg.svg)

Since the arbiter does not hold a copy of the data, these deployments provides only one complete copy of the data. Arbiters require fewer resources, but at the expense of more limited redundancy and fault tolerance.

However, a deployment with a primary, secondary, and an arbiter ensures that a replica set remains available if the primary *or* the secondary is unavailable. If the primary is unavailable, the replica set will elect the secondary to be primary.

![Election in a three-member replica set with an arbiter; the secondary becomes primary.](/images/replica-set-w-arbiter-trigger-election.bakedsvg.svg)

**See also:**

[Deploy a Self-Managed Replica Set](/docs/manual/tutorial/deploy-replica-set)
