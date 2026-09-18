> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Auditing

**Note: Auditing in MongoDB Atlas**

MongoDB Atlas supports auditing for `M10` and larger clusters. To learn more, see [Set Up Database Auditing](https://www.mongodb.com/docs/atlas/database-auditing/#std-label-set-up-database-auditing) in the MongoDB Atlas documentation.

MongoDB Enterprise includes an auditing facility for [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) and [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instances. The facility allows administrators and users to track system activity for deployments with multiple users and applications.

## Enable and Configure Audit Output

The auditing facility can write audit events to the console, the [syslog](/docs/manual/reference/glossary#std-term-syslog), a JSON file, or a BSON file. To enable auditing in MongoDB Enterprise, set an audit output destination with [`--auditDestination`](/docs/manual/reference/program/mongod#std-option-mongod.--auditDestination). For details, see [Configure Auditing.](/docs/manual/tutorial/configure-auditing)

For information on the audit log messages, see [System Event Audit Messages.](/docs/manual/reference/audit-message)

## Audit Events and Filter

Once enabled, the auditing system can record the following operations :

- schema (DDL),

- replica set and sharded cluster,

- authentication and authorization, and

- CRUD operations (requires [`auditAuthorizationSuccess`](/docs/manual/reference/parameters#mongodb-parameter-param.auditAuthorizationSuccess) set to `true`).

**Note:**

Starting in MongoDB 5.0, [secondaries](/docs/manual/reference/glossary#std-term-secondary) do not log DDL audit events for replicated changes. DDL audit events are still logged for DDL operations that modify the [local database](/docs/manual/reference/local-database#std-label-replica-set-local-database) and the [`system.profile`](/docs/manual/reference/system-collections#mongodb-data--database-.system.profile) collection.

For details on audited actions, see [System Event Audit Messages.](/docs/manual/reference/audit-message#std-label-audit-message-format)

Use [filters](/docs/manual/tutorial/configure-audit-filters#std-label-audit-filter) to restrict captured events. See [Configure Audit Filters](/docs/manual/tutorial/configure-audit-filters#std-label-audit-filter) for details.

Operations in an aborted transaction still generate audit events. However, there is no audit event that indicates that the transaction aborted.

## Audit Guarantee

The auditing system writes every audit event  to an in-memory buffer. MongoDB writes this buffer to disk periodically.

Events from a single connection are ordered: if MongoDB writes one event to disk, it has written all prior events for that connection.

If an audit event corresponds to an operation that affects the durable state of the database, such as a modification to data, MongoDB writes the audit event to disk *before* writing to the [journal](/docs/manual/reference/glossary#std-term-journal) for that entry. Before adding an operation to the journal, MongoDB writes all audit events on that connection, up to and including the entry for that operation.

**Warning:**

MongoDB may lose events **if** the server terminates before it commits the events to the audit log. The client may receive confirmation of the event before MongoDB commits to the audit log. For example, while auditing an aggregation operation, the server might terminate after returning the result but before the audit log flushes.

In addition, if the server cannot write to the audit log at the [`audit destination`](/docs/manual/reference/program/mongod#std-option-mongod.--auditDestination), the server terminates.

Audit configuration can include a [filter](/docs/manual/tutorial/configure-audit-filters#std-label-audit-filter) to limit events to audit.
