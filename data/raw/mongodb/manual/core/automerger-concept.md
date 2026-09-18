> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# The AutoMerger

Starting in MongoDB 7.0, the balancer can automatically merge chunks that meet the [mergeability requirements.](/docs/manual/core/automerger-concept#std-label-mergeability-concept)

## Behavior

The AutoMerger runs in the background as part of balancing operations. For most use cases, the default settings perform well. For details on which settings to customize for your deployment, see [AutoMerger Policy.](/docs/manual/core/automerger-concept#std-label-automerge-policy-settings)

When the AutoMerger runs, it squashes together all sequences of mergeable chunks for each shard of each collection.

### AutoMerger Policy

Unless explicitly disabled, the AutoMerger starts the first time the balancer is enabled and pauses for the next [`autoMergerIntervalSecs`](/docs/manual/reference/parameters#mongodb-parameter-param.autoMergerIntervalSecs) after the routine drains.

When AutoMerger is enabled, automerging happens every [`autoMergerIntervalSecs`](/docs/manual/reference/parameters#mongodb-parameter-param.autoMergerIntervalSecs) seconds.

For a given collection, AutoMerger guarantees that subsequent merges are delayed at least the amount specified by [`autoMergerThrottlingMS`.](/docs/manual/reference/parameters#mongodb-parameter-param.autoMergerThrottlingMS)

If a [balancing window](/docs/manual/tutorial/manage-sharded-cluster-balancer#std-label-sharding-schedule-balancing-window) is set, AutoMerger only runs during the window.

### Balancing Settings Precedence

Automerging happens as part of balancing operations. In order to decide if and when to execute automerger, the settings are taken into account in this order:

1. Global [balancing settings](/docs/manual/reference/parameters#std-label-balancer-sharding-params)

2. Per-collection balancing settings (configured by [`configureCollectionBalancing`)](/docs/manual/reference/command/configureCollectionBalancing#mongodb-dbcommand-dbcmd.configureCollectionBalancing)

3. Global [AutoMerger settings](/docs/manual/reference/parameters#std-label-automerger-params)

4. Per-collection AutoMerger settings (configured by [`configureCollectionBalancing`)](/docs/manual/reference/command/configureCollectionBalancing#mongodb-dbcommand-dbcmd.configureCollectionBalancing)

## Details

`mergeAllChunksOnShard` finds and merges all mergeable chunks for a collection on the same shard. Two or more contiguous chunks in the same collection are **mergeable** when they meet all of these conditions:

- They are owned by the same shard.

- They are not [jumbo](/docs/manual/core/sharding-data-partitioning#std-label-jumbo-chunk) chunks. `jumbo` chunks are not mergeable because they cannot participate in migrations.

- Their history can be purged safely, without breaking transactions and snapshot reads:

  - The last migration involving the chunk happened at least as many seconds ago as the value of [`minSnapshotHistoryWindowInSeconds`.](/docs/manual/reference/parameters#mongodb-parameter-param.minSnapshotHistoryWindowInSeconds)

  - The last migration involving the chunk happened at least as many seconds ago as the value of [`transactionLifetimeLimitSeconds`.](/docs/manual/reference/parameters#mongodb-parameter-param.transactionLifetimeLimitSeconds)

## Example

This example assumes that history is empty for all chunks and all chunks are non-jumbo. Since both conditions are true, all contiguous intervals on the same shard are [mergeable.](/docs/manual/reference/command/mergeAllChunksOnShard#std-label-mergeability)

### Setup

These chunks belong to a collection named `coll` with shard key `x`. There are nine chunks in total.

| Chunk ID | Min | Max | Shard |
| --- | --- | --- | --- |
| A | `x: 0` | `x: 10` | Shard0 |
| B | `x: 10` | `x: 20` | Shard0 |
| C | `x: 20` | `x: 30` | Shard0 |
| D | `x: 30` | `x: 40` | Shard0 |
| E | `x: 40` | `x: 50` | Shard1 |
| F | `x: 50` | `x: 60` | Shard1 |
| G | `x: 60` | `x: 70` | Shard0 |
| H | `x: 70` | `x: 80` | Shard0 |
| I | `x: 80` | `x: 90` | Shard1 |

### Steps

1. Merge All Mergeable Chunks on Shard0

   ```javascript
   db.adminCommand( { mergeAllChunksOnShard: "db.coll", shard: "Shard0" } )
   ```

   This command merges the contiguous sequences of chunks:

   - A-B-C-D

   - G-H

2. Merge All Mergeable Chunks on Shard1

   ```javascript
   db.adminCommand( { mergeAllChunksOnShard: "db.coll", shard: "Shard1" } )
   ```

   This command merges the contiguous sequences of chunks E-F.

### Result

After these commands have completed, the contiguous chunks have been merged. There are four total chunks instead of the original nine.

| Chunk ID | Min | Max | Shard |
| --- | --- | --- | --- |
| A-B-C-D | `x: 0` | `x: 40` | Shard0 |
| E-F | `x: 40` | `x: 60` | Shard1 |
| G-H | `x: 60` | `x: 80` | Shard0 |
| I | `x: 80` | `x: 90` | Shard1 |
