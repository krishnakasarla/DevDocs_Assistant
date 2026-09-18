> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Change a Shard Key

The ideal shard key allows MongoDB to distribute documents evenly throughout the cluster while facilitating common query patterns. A suboptimal shard key can lead to uneven data distribution and the following problems:

- [Jumbo chunks](/docs/manual/core/sharding-troubleshooting-shard-keys#std-label-sharding-troubleshooting-jumbo-chunks)

- [Uneven load distribution](/docs/manual/core/sharding-troubleshooting-shard-keys#std-label-sharding-troubleshooting-monotonicity)

- [Decreased query performance over time](/docs/manual/core/sharding-troubleshooting-shard-keys#std-label-sharding-troubleshooting-scatter-gather)

To address these issues, MongoDB allows you to change your shard key:

- You can [refine a shard key](/docs/manual/core/sharding-refine-a-shard-key#std-label-shard-key-refine) by adding a suffix field or fields to the existing shard key.

- You can change a collection's shard key entirely and [reshard a collection.](/docs/manual/core/sharding-reshard-a-collection#std-label-sharding-resharding)

Data distribution fixes are most effective when you reshard a collection. If you want to improve data distribution and your cluster meets the [criteria to reshard](/docs/manual/core/sharding-reshard-a-collection#std-label-reshard-requirements), you should reshard the collection instead of refining the shard key. If your cluster doesn't meet the criteria to reshard, you should refine the shard key.

For more information on common performance and scaling issues and advice on how to fix them, read [Troubleshoot Shard Keys.](/docs/manual/core/sharding-troubleshooting-shard-keys#std-label-shardkey-troubleshoot-shard-keys)
