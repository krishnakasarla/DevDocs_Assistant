> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Replica Set Secondary Members

A secondary maintains a copy of the [primary's](/docs/manual/reference/glossary#std-term-primary) data set. To replicate data, a secondary applies operations from the primary's [oplog](/docs/manual/core/replica-set-oplog#std-label-replica-set-oplog) to its own data set in an asynchronous process.  A replica set can have one or more secondaries.

The following three-member replica set has two secondary members. The secondaries replicate the primary's oplog and apply the operations to their data sets.

![Diagram of a 3 member replica set that consists of a primary and two secondaries.](/images/replica-set-primary-with-two-secondaries.bakedsvg.svg)

Although clients cannot write data to secondaries, clients can read data from secondary members. See [Read Preference](/docs/manual/core/read-preference) for more information on how clients direct read operations to replica sets.

A secondary can become a primary. If the current primary becomes unavailable, the replica set holds an [election](/docs/manual/reference/glossary#std-term-election) to choose which of the secondaries becomes the new primary.

In the following three-member replica set, the primary becomes unavailable. This triggers an election where one of the remaining secondaries becomes the new primary.

![Election in a three-member replica set after the primary becomes unreachable; a secondary is elected.](/images/replica-set-trigger-election.bakedsvg.svg)

See [Replica Set Elections](/docs/manual/core/replica-set-elections) for more details.

You can configure a secondary member for a specific purpose. You can configure a secondary to:

- Prevent it from becoming a primary in an election, which allows it to reside in a secondary data center or to serve as a cold standby. See [Priority 0 Replica Set Members.](/docs/manual/core/replica-set-priority-0-member)

- Prevent applications from reading from it, which allows it to run applications that require separation from normal traffic. See [Hidden Replica Set Members.](/docs/manual/core/replica-set-hidden-member)

- Keep a running "historical" snapshot for use in recovery from certain errors, such as unintentionally deleted databases. See [Delayed Replica Set Members.](/docs/manual/core/replica-set-delayed-member)

Secondary members of a replica set now [log oplog entries](/docs/manual/core/replica-set-oplog#std-label-slow-oplog-application) that take longer than the slow operation threshold to apply. These slow oplog messages:

- Are logged for the secondaries in the [`diagnostic log`.](/docs/manual/reference/program/mongod#std-option-mongod.--logpath)

- Are logged under the [`REPL`](/docs/manual/reference/log-messages#mongodb-data-REPL) component with the text `applied op: <oplog entry> took <num>ms`.

- Do not depend on the log levels (either at the system or component level)

- Do not depend on the profiling level.

- Are affected by [`slowOpSampleRate`.](/docs/manual/reference/configuration-options#mongodb-setting-operationProfiling.slowOpSampleRate)

The profiler does not capture slow oplog entries.
