> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Replica Set High Availability

Replica sets use elections to support [high availability.](/docs/manual/reference/glossary#std-term-high-availability)

[Replica Set Elections](/docs/manual/core/replica-set-elections)

Elections occur when the primary becomes unavailable and the replica set members autonomously select a new primary.

[Rollbacks During Replica Set Failover](/docs/manual/core/replica-set-rollbacks)

A rollback reverts write operations on a former primary when the member rejoins the replica set after a failover.
