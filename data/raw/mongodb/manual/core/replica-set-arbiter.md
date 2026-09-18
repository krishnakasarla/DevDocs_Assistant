> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Replica Set Arbiter

In some circumstances (such as when you have a primary and a secondary, but cost constraints prohibit adding another secondary), you may choose to add an arbiter to your replica set. An arbiter participates in [elections for primary](/docs/manual/core/replica-set-elections#std-label-replica-set-elections) but an arbiter does **not** have a copy of the data set and **cannot** become a primary.

An arbiter has exactly `1` election vote. By default an arbiter has priority `0`.

**Important:**

Do not run an arbiter on systems that also host the primary or the secondary members of the replica set.

**Warning:**

Using a [primary-secondary-arbiter (PSA)](/docs/manual/core/replica-set-architecture-three-members#std-label-rs-architecture-psa) architecture for shards in a sharded cluster can cause a loss of availability if a data-bearing secondary is unavailable. A PSA cluster differs from a typical replica set: In a sharded cluster, shards perform `w: majority` [write concern operations](/docs/manual/reference/write-concern) that cannot complete if the remaining cluster members required to confirm an operation have an arbiter.

To add an arbiter, see [Add an Arbiter to a Self-Managed Replica Set.](/docs/manual/tutorial/add-replica-set-arbiter)

## Performance Issues with PSA replica sets

If you are using a three-member primary-secondary-arbiter (PSA) architecture, consider the following:

- The write concern [`"majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) can cause performance issues if a secondary is unavailable or lagging. For advice on how to mitigate these issues, see [Mitigate Performance Issues in Self-Managed PSA Replica Sets.](/docs/manual/tutorial/mitigate-psa-performance-issues#std-label-performance-issues-psa)

- If you are using a global default [`"majority"`](/docs/manual/reference/read-concern-majority#mongodb-readconcern-readconcern.-majority-) and the write concern is less than the size of the majority, your queries may return stale (not fully replicated) data.

## Shard Keys, Transactions, and Arbiters

You cannot change a [shard key](/docs/manual/reference/glossary#std-term-shard-key) using a transaction if the replica set has an arbiter. Arbiters cannot participate in the data operations required for multi-shard transactions.

Transactions whose write operations span multiple shards will error and abort if any transaction operation reads from or writes to a shard that contains an arbiter.

## Concerns with Multiple Arbiters

Use a single arbiter to avoid problems with data consistency. Multiple arbiters prevent the reliable use of the majority write concern.

To ensure that a write will persist after the failure of a primary node, the majority write concern requires a majority of nodes to acknowledge a write operation. Arbiters do not store any data, but they do contribute to the number of nodes in a replica set. When a replica set has multiple arbiters it is less likely that a majority of data bearing nodes will be available after a node failure.

**Warning:**

If a secondary node falls behind the primary, and the cluster is [`reconfigured`](/docs/manual/reference/method/rs.reconfig#mongodb-method-rs.reconfig), votes from multiple arbiters can elect the node that had fallen behind. The new primary will not have the unreplicated writes even though the writes could have been majority committed by the old configuration. The result is data loss.

To avoid this scenario, use at most a single arbiter.

**New in version 5.3**

Starting in MongoDB 5.3, support for multiple arbiters in a replica set is disabled by default. If you attempt to add multiple arbiters to a replica set, the server returns an error:

```text
MongoServerError: Multiple arbiters are not allowed unless all nodes
were started with --setParameter 'allowMultipleArbiters=true'
```

To add multiple arbiters to a replica set using MongoDB 5.3 or later, start each node with the [`allowMultipleArbiters`](/docs/manual/reference/parameters#mongodb-parameter-param.allowMultipleArbiters) parameter set to `true`:

```bash
mongod --setParameter allowMultipleArbiters=true
```

## Security

### Authentication

When running with [`authorization`](/docs/manual/reference/configuration-options#mongodb-setting-security.authorization), arbiters exchange credentials with other members of the set to authenticate. MongoDB encrypts the authentication process, and the MongoDB authentication exchange is cryptographically secure.

Because arbiters do not store data, they do not possess the internal table of user and role mappings used for authentication.  Thus, the only way to log on to an arbiter with authorization active is to use the [localhost exception.](/docs/manual/core/localhost-exception#std-label-localhost-exception)

### Communication

The only communication between arbiters and other set members are: votes during elections, heartbeats, and configuration data. These exchanges are not encrypted.

**However**, if your MongoDB deployment uses TLS/SSL, MongoDB will encrypt *all* communication between replica set members. See [Configure MongoDB Instances for TLS/SSL Encryption](/docs/manual/tutorial/configure-ssl) for more information.

As with all MongoDB components, run arbiters in trusted network environments.

## Example

For example, in the following replica set with 2 data-bearing members (the primary and a secondary), an arbiter allows the set to have an odd number of votes to break a tie:

![Diagram of a replica set that consists of a primary, a secondary, and an arbiter.](/images/replica-set-primary-with-secondary-and-arbiter.bakedsvg.svg)
