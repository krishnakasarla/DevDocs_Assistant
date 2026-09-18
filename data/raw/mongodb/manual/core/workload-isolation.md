> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Workload Isolation in MongoDB Deployments

## Operational Overview

MongoDB includes a number of features that allow database administrators and developers to isolate workload by functional or geographical groupings.

This capability provides "data center awareness," which allows applications to target MongoDB deployments with consideration of the physical location of the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instances. MongoDB supports segmentation of operations across different dimensions, which may include multiple data centers and geographical regions in multi-data center deployments, racks, networks, or power circuits in single data center deployments.

MongoDB also supports workload isolation based on functional or operational parameters, to ensure that certain [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instances are only used for reporting workloads or that certain high-frequency portions of a sharded collection only exist on specific shards.

Specifically, with MongoDB, you can:

- ensure write operations propagate to specific members of a replica set, or to specific members of replica sets.

- ensure that specific members of a replica set respond to queries.

- ensure that specific ranges of your [shard key](/docs/manual/reference/glossary#std-term-shard-key) balance onto and reside on specific [shards.](/docs/manual/reference/glossary#std-term-shard)

- combine the above features in a single distributed deployment, on a per-operation (for read and write operations) and collection (for chunk distribution in sharded clusters distribution) basis.

For full documentation of these features, see the following documentation in the MongoDB Manual:

- [Read Preferences](/docs/manual/core/read-preference#std-label-read-preference), which controls how drivers help applications target read operations to members of a replica set.

- [Write Concerns](/docs/manual/reference/write-concern#std-label-write-concern), which controls how MongoDB ensures that write operations propagate to members of a replica set.

- [Replica Set Tags](/docs/manual/tutorial/configure-replica-set-tag-sets#std-label-replica-set-configuration-tag-sets), which control how applications create and interact with custom groupings of replica set members to create custom application-specific read preferences and write concerns.

- [Zones](/docs/manual/core/zone-sharding#std-label-zone-sharding) in sharded clusters, which allows MongoDB administrators to create [zones](/docs/manual/reference/glossary#std-term-zone) that represent a group of shards and associate one or more ranges of [shard key](/docs/manual/reference/glossary#std-term-shard-key) values to these zones. You can associate each zone with one or more shards in the cluster. A shard can associate with any number of zones. In a balanced cluster, MongoDB directs reads and writes covered by a zone only to the shards inside the zone.

**See also:**

Before adding workload isolation features to your application and MongoDB deployment, become familiar with all documentation of [replication](/docs/manual/replication#std-label-replication), and [sharding.](/docs/manual/sharding#std-label-sharding-background)
