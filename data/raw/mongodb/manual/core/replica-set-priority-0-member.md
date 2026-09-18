> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Priority 0 Replica Set Members

A [`priority 0`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.members-n-.priority) member is a member that **cannot** become [primary](/docs/manual/reference/glossary#std-term-primary) and **cannot** trigger [elections](/docs/manual/reference/glossary#std-term-election). Priority 0 members can acknowledge write operations issued with [write concern](/docs/manual/reference/write-concern#std-label-write-concern) of `w : <number>`. For `"majority"` write concern, the priority 0 member must also be a voting member (i.e. [`members[n].votes`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.members-n-.votes) is greater than `0`) to acknowledge the write. Non-voting replica set members (i.e. [`members[n].votes`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.members-n-.votes) is `0`) cannot contribute to acknowledging write operations with `"majority"` write concern.

Other than the aforementioned restrictions, secondaries that have [`priority 0`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.members-n-.priority) function as normal secondaries: they maintain a copy of the data set, accept read operations, and vote in elections.

Configuring a replica set member with [`priority 0`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.members-n-.priority) might be desired if the particular member is deployed in a data center that is distant from the main deployment and therefore has higher latency. It may serve local read requests well, but might not be an ideal candidate to perform the duties of a primary due to its latency.

For this situation, the following diagram shows a data center on the left which hosts the primary and a secondary, and a data center on the right which hosts a secondary that has been configured to have *priority 0* to prevent it from becoming primary. Because of this setting, only the members in the left data center are eligible to become primary in an election.

![Three-member replica set across two data centers including a priority 0 member.](/images/replica-set-three-members-geographically-distributed.bakedsvg.svg)

Compare this to the default priority for replica set members, [`priority 1`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.members-n-.priority), where either of the secondaries in this scenario would be eligible to serve as primary. See [Replica Sets Distributed Across Two or More Data Centers](/docs/manual/core/replica-set-architecture-geographically-distributed) for more information.

## Priority 0 Members as Standbys

A secondary with [`priority 0`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.members-n-.priority) can function as a standby. In some replica sets, it might not be possible to add a new member in a reasonable amount of time. A standby member keeps a current copy of the data to be able to replace an unavailable member.

In many cases, you need not set standby to *priority 0*. However, in replica sets with varied hardware or [geographic distribution](/docs/manual/core/replica-set-architecture-geographically-distributed#std-label-replica-set-geographical-distribution), a *priority 0* standby ensures that only certain members become primary.

A *priority 0* standby may also be valuable for some members of a set with different hardware or workload profiles. In these cases, deploy a member with *priority 0* so it can't become primary. Also consider using a [hidden member](/docs/manual/core/replica-set-hidden-member#std-label-replica-set-hidden-members) for this purpose.

If your set already has seven voting members, also configure the member as [non-voting.](/docs/manual/core/replica-set-elections#std-label-replica-set-non-voting-members)

## Failover Considerations

When configuring a secondary to have [`priority 0`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.members-n-.priority), consider potential failover patterns, including all possible network partitions. Always ensure that your main data center contains both a quorum of voting members and members that are eligible to be primary.

## Example

To configure a secondary to have [`priority 0`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.members-n-.priority), see [Prevent a Self-Managed Secondary from Becoming Primary.](/docs/manual/tutorial/configure-secondary-only-replica-set-member)
