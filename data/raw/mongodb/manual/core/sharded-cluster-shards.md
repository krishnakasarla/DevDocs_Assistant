> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Shards

A [shard](/docs/manual/reference/glossary#std-term-shard) contains a subset of sharded data for a [sharded cluster](/docs/manual/reference/glossary#std-term-sharded-cluster). Together, the cluster's shards hold the entire data set for the cluster.

Shards must be deployed as a [replica set](/docs/manual/reference/glossary#std-term-replica-set) to provide redundancy and high availability.

**Important:**

Sharded clusters use the write concern `"majority"` for a lot of internal operations. Using an arbiter in a sharded cluster is discouraged due to [Performance Issues with PSA replica sets.](/docs/manual/core/replica-set-arbiter#std-label-replica-set-arbiter-performance-psa)

**Warning:**

**Typically, do not perform operations directly on a shard because
they might cause data corruption or data loss.** Users, clients, or applications should only directly connect to a shard to perform local administrative or maintenance operations.

Performing queries on a single shard only returns a subset of data. Connect to the [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) to perform cluster level operations, including read or write operations.

**Important:**

MongoDB does not guarantee that any two contiguous [chunks](/docs/manual/reference/glossary#std-term-chunk) reside on a single shard.

## Primary Shard

Each database in a sharded cluster has a primary shard. It is the default shard for all unsharded collections in the database. All unsharded collections for a database are created on the database primary shard by default. Starting in MongoDB 8.0, you can move unsharded collections to another shard using [`moveCollection`](/docs/manual/reference/command/moveCollection#mongodb-dbcommand-dbcmd.moveCollection). The primary shard has no relation to the primary in a replica set.

The [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) selects the primary shard when creating a new database by picking the shard in the cluster that has the least amount of data. [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) uses the `totalSize` field returned by the [`listDatabases`](/docs/manual/reference/command/listDatabases#mongodb-dbcommand-dbcmd.listDatabases) command as a part of the selection criteria.

![Primary shard (Shard A) with non-sharded collections and chunks of sharded collection documents.](/images/sharded-cluster-primary-shard.bakedsvg.svg)

To change the primary shard for a database, use the [`movePrimary`](/docs/manual/reference/command/movePrimary#mongodb-dbcommand-dbcmd.movePrimary) command. The process of migrating the primary shard may take significant time to complete, and you should not access the collections associated to the database until it completes. Depending on the amount of data being migrated, the migration may affect overall cluster operations. Consider the impact to cluster operations and network load before attempting to change the primary shard.

When you deploy a new [sharded cluster](/docs/manual/reference/glossary#std-term-sharded-cluster) with shards that were previously used as replica sets, all existing databases continue to reside on their original replica sets. Databases created subsequently may reside on any shard in the cluster.

## Shard Status

Use the [`sh.status()`](/docs/manual/reference/method/sh.status#mongodb-method-sh.status) method in [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) to see an overview of the cluster. This reports includes which shard is primary for the database and the [chunk](/docs/manual/reference/glossary#std-term-chunk) distribution across the shards. See [`sh.status()`](/docs/manual/reference/method/sh.status#mongodb-method-sh.status) method for more details.

## Sharded Cluster Security

Use [Self-Managed Internal/Membership Authentication](/docs/manual/core/security-internal-authentication) to enforce intra-cluster security and prevent unauthorized cluster components from accessing the cluster. You must start each [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) in the cluster with the appropriate security settings in order to enforce internal authentication.

Starting in MongoDB 5.3, [SCRAM-SHA-1](/docs/manual/core/security-scram#std-label-authentication-scram-sha-1) cannot be used for intra-cluster authentication. Only [SCRAM-SHA-256](/docs/manual/core/security-scram#std-label-authentication-scram-sha-256) is supported.

In previous MongoDB versions, SCRAM-SHA-1 and SCRAM-SHA-256 can both be used for intra-cluster authentication, even if SCRAM is not explicitly enabled.

See [Keyfile Authentication for Self-Managed Sharded Clusters](/docs/manual/tutorial/deploy-sharded-cluster-with-keyfile-access-control) for a tutorial on deploying a secured sharded cluster.

### Shard Local Users

Each shard supports [Role-Based Access Control in Self-Managed Deployments](/docs/manual/core/authorization) *(RBAC)* for restricting unauthorized access to shard data and operations. Start each [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) in the replica set with the [`--auth`](/docs/manual/reference/program/mongod#std-option-mongod.--auth) option to enforce RBAC. Alternatively, enforcing [Self-Managed Internal/Membership Authentication](/docs/manual/core/security-internal-authentication) for intra-cluster security also enables user access controls via RBAC.

Starting in MongoDB 5.3, [SCRAM-SHA-1](/docs/manual/core/security-scram#std-label-authentication-scram-sha-1) cannot be used for intra-cluster authentication. Only [SCRAM-SHA-256](/docs/manual/core/security-scram#std-label-authentication-scram-sha-256) is supported.

In previous MongoDB versions, SCRAM-SHA-1 and SCRAM-SHA-256 can both be used for intra-cluster authentication, even if SCRAM is not explicitly enabled.

Each shard has its own shard-local users. These users cannot be used on other shards, nor can they be used for connecting to the cluster via a [`mongos`.](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos)

See [Enable Access Control on Self-Managed Deployments](/docs/manual/tutorial/enable-authentication) for a tutorial on enabling adding users to an RBAC-enabled MongoDB deployment.
