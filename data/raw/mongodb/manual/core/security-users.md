> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Users in Self-Managed Deployments

To authenticate a client in MongoDB, you must add a corresponding user to MongoDB.

## User Management

You can add a user with the [`db.createUser()`](/docs/manual/reference/method/db.createUser#mongodb-method-db.createUser) method using [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh). The first user you create must have privileges to create other users. The [`userAdmin`](/docs/manual/reference/built-in-roles#mongodb-authrole-userAdmin) or [`userAdminAnyDatabase`](/docs/manual/reference/built-in-roles#mongodb-authrole-userAdminAnyDatabase) role both confer the privilege to create other users.

**See also:**

[Create a User on Self-Managed Deployments](/docs/manual/tutorial/create-users)

You can grant a user privileges by assigning [roles](/docs/manual/core/authorization) to the user when you create the user. You can also grant or revoke roles and update passwords by updating existing users. For a full list of user management methods, see [User Management.](/docs/manual/reference/method#std-label-user-management-methods)

**See also:**

[Manage Users and Roles on Self-Managed Deployments](/docs/manual/tutorial/manage-users-and-roles)

## Authentication Database

The database where you add a user is its authentication database.

A user's privileges are not limited to their authentication database and can span multiple databases. For more information on roles, see [Role-Based Access Control in Self-Managed Deployments.](/docs/manual/core/authorization)

A user's name and authentication database serve as a unique identifier for that user. MongoDB associates a user with a unique `userId` upon creation in MongoDB. However, [LDAP managed users](/docs/manual/core/security-ldap#std-label-security-ldap) created on an LDAP server do not have an associated document in the [system.users](/docs/manual/reference/system-users-collection#std-label-system-users) collection, and therefore don't have a [`userId`](/docs/manual/reference/system-users-collection#mongodb-data-admin.system.users.userId) field associated with them.

If two users have the same name but are created in different databases, they are two separate users. If you want to have a single user with permissions on multiple databases, create a single user with a role for each applicable database.

## Centralized User Data

MongoDB stores all user information, including [`name`](/docs/manual/reference/system-users-collection#mongodb-data-admin.system.users.user), [`password`](/docs/manual/reference/system-users-collection#mongodb-data-admin.system.users.credentials), and the user's [`authentication database`](/docs/manual/reference/system-users-collection#mongodb-data-admin.system.users.db), in the [system.users](/docs/manual/reference/system-users-collection) collection in the `admin` database.

Do not modify this collection directly. To manage users, use the designated [user management commands.](/docs/manual/reference/command#std-label-user-management-commands)

## Sharded Cluster Users

To create users for a sharded cluster, connect to a [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instance and add the users. To authenticate as a user created on a [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instance, you must authenticate through a [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instance.

In sharded clusters, MongoDB stores user configuration data in the `admin` database of the [config servers.](/docs/manual/reference/glossary#std-term-config-server)

### Shard Local Users

Some maintenance operations, such as [`compact`](/docs/manual/reference/command/compact#mongodb-dbcommand-dbcmd.compact) or [`rs.reconfig()`](/docs/manual/reference/method/rs.reconfig#mongodb-method-rs.reconfig), require direct connections to specific shards in a sharded cluster. To perform these operations, you must connect directly to the shard and authenticate as a *shard local* administrative user.

To create a *shard local* administrative user, connect directly to the primary of the shard and create the user. For instructions on how to create a shard local user administrator see the [Keyfile Authentication for Self-Managed Sharded Clusters](/docs/manual/tutorial/deploy-sharded-cluster-with-keyfile-access-control) tutorial.

MongoDB stores *shard local* users in the `admin` database of the shard itself. These *shard local* users are independent from the users added to the sharded cluster through a [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos). *Shard local* users are local to the shard and are inaccessible by [`mongos`.](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos)

Starting in MongoDB 8.0, you can use the [`directShardOperations`](/docs/manual/reference/built-in-roles#mongodb-authrole-directShardOperations) role to perform maintenance operations that require you to execute commands directly against a shard.

Direct connections to a shard should only be used for shard-specific maintenance and configuration. In general, clients must connect to the sharded cluster through the [`mongos`.](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos)

**Warning:**

Running commands using the `directShardOperations` role can cause your cluster to stop working correctly and may cause data corruption. Only use the `directShardOperations` role for maintenance purposes or under the guidance of MongoDB support. Stop using the `directShardOperations` role when you finish performing maintenance operations.
