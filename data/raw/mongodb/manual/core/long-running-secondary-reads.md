> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Long-Running Secondary Reads in Sharded Clusters

Starting in MongoDB 8.2, secondary reads in sharded clusters might automatically terminate if there is a risk of missing documents due to [chunk migrations.](/docs/manual/core/sharding-data-partitioning#std-label-sharding-chunk-migration)

To support this new behavior, MongoDB 8.2 introduces the following changes:

- Adds [`terminateSecondaryReadsOnOrphanCleanup`](/docs/manual/reference/parameters#mongodb-parameter-param.terminateSecondaryReadsOnOrphanCleanup) parameter (default: `true`)

  **Note:**

  If `terminateSecondaryReadsOnOrphanCleanup` is set to `false`, the server does not terminate reads and might miss documents in sharded collections due to chunk migrations. This is the default behavior in MongoDB 8.1 or earlier. To learn more, see [Disable Secondary Read Termination.](/docs/manual/core/long-running-secondary-reads#std-label-secondary-reads-disable-termination)

- Increases [`orphanCleanupDelaySecs`](/docs/manual/reference/parameters#mongodb-parameter-param.orphanCleanupDelaySecs) default value from `900` seconds to `3600` seconds (1 hour)

## Behavior

By default, a sharded cluster performs the following operations when a chunk migration commits:

1. The source shard initiates an orphan cleanup process to delete documents that migrated to a different shard.

   The shard waits for any pre-existing reads on the primary to complete.

   The shard waits an additional `orphanCleanupDelaySecs` seconds (default: 1 hour).

   The shard deletes [orphaned documents.](/docs/manual/reference/glossary#std-term-orphaned-document)

2. Secondaries terminate reads that started before the migration completed.

3. Secondaries replicate orphaned document deletions.

![Lifecycle of a long-running secondary read terminated by a chunk migration.](/images/long-running-secondary-reads.svg)

Terminating secondary reads before deleting orphaned documents ensures that long-running secondary reads do not miss any documents deleted by the cleanup process.

### Monitoring

You can monitor terminated secondary reads due to orphan cleanup in the following ways:

- Check the server status of your secondary node with the following [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) command:

  `db.serverStatus().metrics.operation.killedDueToRangeDeletion`

- Review your `mongod` logs. Each termination results in a log entry like the following example:

```javascript
{
   "t": {
         "$date": "2025-06-11T12:11:43.361+02:00"
   },
   "s": "I",
   "c": "SHARDING",
   "id": 10016300,
   "svc": "S",
   "ctx": "conn93",
   "msg": "Read has been terminated due to orphan range cleanup",
   "attr": {
         "type": "command",
         ...
         "workingMillis": 0,
         "durationMillis": 0,
         "orphanCleanupDelaySecs": 3600
   }
}
```

## Managing Long-Running Secondary Reads

If your application performs secondary reads that exceed 1 hour on sharded clusters that perform chunk migrations, you might encounter `QueryPlanKilled` errors (error code [`175`](/docs/manual/reference/error-codes#mongodb-error-175)) due to terminated reads.

The recommended method to manage long-running secondary reads is to [implement a resume mechanism](/docs/manual/core/long-running-secondary-reads#std-label-secondary-reads-resume-mechanism) in your application.

You can also manage long-running secondary reads with the following alternative strategies:

- [Increase orphanCleanupDelaySecs](/docs/manual/core/long-running-secondary-reads#std-label-secondary-reads-cleanup-delay)

- [Disable Secondary Read Termination](/docs/manual/core/long-running-secondary-reads#std-label-secondary-reads-disable-termination)

- [Disable the Balancer](/docs/manual/core/long-running-secondary-reads#std-label-secondary-reads-disable-balancer)

### Implement Resume Mechanism

A resume mechanism allows your application to create a new read operation that starts where your previous read operation terminates.

To implement an effective resume mechanism, your application must use a consistent sort order for your query results. Consider the following factors when selecting a sort order for your resume mechanism:

- The sort operation should utilize an indexed field for efficient query execution.

- The sort field should contain unique values.

  - If the sort field values are not unique, your application must implement additional logic to handle documents that share the same sort value.

#### Example

Consider a `cities` database containing a `zipcodes` collection with the following structure:

```javascript
{
        "state": "NY",
        "city": "NEW YORK",
        "zipcode": "00501"
}
```

For this example, assume the `zipcode` field values are unique.

The following JavaScript code performs a secondary read operation to retrieve all documents where the `state` is `NY` and implements a resume mechanism to handle `QueryPlanKilled` errors:

```javascript
let readDoc;
let latestZip;

let cursor = db.getSiblingDB("cities").zipcodes.find({
   state: "NY"
})
.sort({zipcode: 1})
.readPref("secondary");

while(cursor.hasNext()) {
   try {
      readDoc = cursor.next();
      // process `readDoc` here
      latestZip = readDoc.zipcode;
   } catch (err) {
      if (err.code === 175 &&
         err.errmsg.includes("Read has been terminated due to orphan range cleanup")) {
         console.log("Query terminated, resuming from zipcode:", latestZip);

         cursor = db.getSiblingDB("cities").zipcodes.find({
               state: "NY",
               zipcode: {$gt: latestZip}
         })
         .sort({zipcode: 1})
         .readPref("secondary");
      } else {
         throw err; // Rethrow non-termination errors
      }
   }
}
```

When reviewing the example database and application logic, consider the following:

- The example code handles `QueryPlanKilled` errors with a resume mechanism that sorts by `zipcode`. Sorting on the `zipcode` field ensures a consistent order and a unique sort value for each document. This allows the application to resume the read operation precisely where it was terminated.

- The `cities.zipcodes` collection implements a `{state: 1, zipcode: 1}` compound index to ensure the efficiency of the resume mechanism queries. Implementing this compound index prevents both collection scans and in-memory sorts, and supports filter and sort operations. To learn more about creating effective indexes, see [The ESR (Equality, Sort, Range) Guideline.](/docs/manual/tutorial/equality-sort-range-guideline#std-label-esr-indexing-guideline)

- The `QueryPlanKilled` error (error code `175`) can occur for reasons other than terminated secondary reads. To accurately handle `QueryPlanKilled` errors, you must parse the `errmsg` field. MongoDB returns the following error message when it terminates a secondary read:

```javascript
{
   code: 175,
   name: QueryPlanKilled,
   categories: [CursorInvalidatedError],
   errmsg: "Read has been terminated due to orphan range cleanup"
}
```

- When the application encounters a `QueryPlanKilled` error due to orphan range cleanup, it uses the last successfully processed zipcode as a starting point for the resumed query. The [`$gt`](/docs/manual/reference/operator/aggregation/gt#mongodb-expression-exp.-gt) operator ensures the application does not process duplicate documents.

Test your resume mechanisms in a test environment and monitor your production cluster to understand how often secondary reads are terminated. If terminations occur frequently, you might need to adjust your query patterns, or consider alternative data access approaches. To learn how to monitor your cluster for these errors, see [Monitoring.](/docs/manual/core/long-running-secondary-reads#std-label-secondary-reads-error-monitoring)

### Increase orphanCleanupDelaySecs

The [`orphanCleanupDelaySecs`](/docs/manual/reference/parameters#mongodb-parameter-param.orphanCleanupDelaySecs) server parameter controls the time MongoDB waits before deleting a migrated chunk from the source shard.

Increasing `orphanCleanupDelaySecs` allows secondary read operations to run for a longer period of time. You can set the `orphanCleanupDelaySecs` at both startup and runtime.

The following command sets `orphanCleanupDelaySecs` to 2 hours:

```javascript
db.adminCommand({
        setParameter: 1,
        orphanCleanupDelaySecs: 7200
})
```

**Important:**

Increasing `orphanCleanupDelaySecs` means that orphaned documents remain on nodes for a longer period of time. If you increase this value, executing a query that uses an index but does not include the shard key might result in degraded performance as the query must filter more orphaned documents before returning results.

### Disable Secondary Read Termination

**Note:**

In MongoDB 8.1 or earlier, sharded clusters do not automatically terminate long-running secondary reads. To match this behavior in MongoDB 8.2 or later, disable secondary read termination.

The [`terminateSecondaryReadsOnOrphanCleanup`](/docs/manual/reference/parameters#mongodb-parameter-param.terminateSecondaryReadsOnOrphanCleanup) server parameter controls whether long-running secondary reads automatically terminate before orphaned document deletion.

You can disable secondary read termination by setting `terminateSecondaryReadsOnOrphanCleanup` to `false`. You can set this parameter at startup or runtime.

The following command sets `terminateSecondaryReadsOnOrphanCleanup` to `false`:

```javascript
db.adminCommand({
        setParameter: 1,
        terminateSecondaryReadsOnOrphanCleanup: false
})
```

**Warning:**

If this feature is disabled and chunk migrations affect the targeted collection, your secondary reads might fail to return all documents.

### Disable the Balancer

You can avoid automatically terminating long-running secondary reads by disabling the balancer and not performing any [manual migrations.](/docs/manual/tutorial/migrate-chunks-in-sharded-cluster#std-label-migrate-ranges-sharded-cluster)

To disable the balancer for specific collections, use the [`configureCollectionBalancing`](/docs/manual/reference/command/configureCollectionBalancing#mongodb-dbcommand-dbcmd.configureCollectionBalancing) command's `enableBalancing` field.

To restrict balancer operations to specific times, see [Schedule the Balancing Window.](/docs/manual/tutorial/manage-sharded-cluster-balancer#std-label-sharding-schedule-balancing-window)

**Warning:**

Disabling the balancer for extended periods of time can lead to unbalanced shards which degrade cluster performance. Only disable the balancer if it is necessary for your use case.

## Learn More

- [Sharded Cluster Balancer](/docs/manual/core/sharding-balancer-administration#std-label-sharding-balancing)

- [Migrate Ranges in a Sharded Cluster](/docs/manual/tutorial/migrate-chunks-in-sharded-cluster#std-label-migrate-ranges-sharded-cluster)

- [`terminateSecondaryReadsOnOrphanCleanup`](/docs/manual/reference/parameters#mongodb-parameter-param.terminateSecondaryReadsOnOrphanCleanup)
