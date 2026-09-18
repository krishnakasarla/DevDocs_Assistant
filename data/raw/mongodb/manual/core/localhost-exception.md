> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Localhost Exception in Self-Managed Deployments

**Important:**

On a [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instance, the localhost exception only applies when there are **no users or roles** created in the MongoDB instance.

The localhost exception allows you to create the first user or role in the system after enabling access control. You can also use it to initiate a replica set.

## Initiating a Replica Set

You can use the localhost exception to initiate a replica set, following the steps in [Deploy a Self-Managed Replica Set](/docs/manual/tutorial/deploy-replica-set#std-label-server-replica-set-deploy). You must wait until the replica set elects a primary before you can add the first user.

## Creating the First User or Role

**Warning:**

Connections using the localhost exception have access to create *only* the **first user OR role**. Only create a role first if you are authorizing users with LDAP. See [LDAP Authorization](/docs/manual/core/security-ldap-external#std-label-security-ldap-external) for more information.

After you enable access control, connect to the localhost interface and [create the first user](/docs/manual/tutorial/configure-scram-client-authentication#std-label-create-user-admin) in the `admin` database. The first user must have privileges to create other users. The [`userAdmin`](/docs/manual/reference/built-in-roles#mongodb-authrole-userAdmin) or [`userAdminAnyDatabase`](/docs/manual/reference/built-in-roles#mongodb-authrole-userAdminAnyDatabase) role both confer the privilege to create other users.

### Localhost Exception for Sharded Clusters

**Important:**

- On a [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos), the localhost exception only applies when there are no [sharded cluster users](/docs/manual/core/security-users#std-label-sharding-localhost) or roles created.

- In a sharded cluster, the localhost exception applies to each shard individually as well as to the cluster as a whole.

Once you create a sharded cluster and add a [user administrator](/docs/manual/tutorial/configure-scram-client-authentication#std-label-create-user-admin) through the [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instance, you **must** still prevent unauthorized access to the individual shards. To prevent unauthorized access to individual shards, follow one of the following steps for each shard in your cluster:

- [Create a user administrator](/docs/manual/tutorial/configure-scram-client-authentication#std-label-create-user-admin) on the shard's primary.

- Disable the localhost exception at startup. To disable the localhost exception, set the [`enableLocalhostAuthBypass`](/docs/manual/reference/parameters#mongodb-parameter-param.enableLocalhostAuthBypass) parameter to `0`.

## All Localhost Exception Permissions

While the localhost exception applies, you can:

- Run the [`createUser`](/docs/manual/reference/command/createUser#mongodb-dbcommand-dbcmd.createUser) command or [`db.createUser()`](/docs/manual/reference/method/db.createUser#mongodb-method-db.createUser) method. This ends the localhost exception.

- Run the [`createRole`](/docs/manual/reference/command/createRole#mongodb-dbcommand-dbcmd.createRole) command or [`db.createRole()`](/docs/manual/reference/method/db.createRole#mongodb-method-db.createRole) method. This ends the localhost exception.

- Use the [`grantRole`](/docs/manual/reference/privilege-actions#mongodb-authaction-grantRole) action to grant a role to a user on an external authentication system, such as LDAP.

- Run [`replSetInitiate`](/docs/manual/reference/command/replSetInitiate#mongodb-dbcommand-dbcmd.replSetInitiate) to initiate a new replica set

- Run [`replSetGetStatus`](/docs/manual/reference/command/replSetGetStatus#mongodb-dbcommand-dbcmd.replSetGetStatus) to get the status of the current member's replica set

- Run [`replSetReconfig`](/docs/manual/reference/command/replSetReconfig#mongodb-dbcommand-dbcmd.replSetReconfig) on the primary member to modify replica set configuration.

- On a [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instance, if the cluster is hosted on `localhost`, you can run [`addShard`](/docs/manual/reference/command/addShard#mongodb-dbcommand-dbcmd.addShard) to add a shard to the cluster.
