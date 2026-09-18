> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Unsharded Collections

Starting in MongoDB 8.0, you can unshard a sharded collection by using the [`unshardCollection`](/docs/manual/reference/command/unshardCollection#mongodb-dbcommand-dbcmd.unshardCollection) command. When you unshard a collection, MongoDB moves the collection data onto a single shard and updates the metadata to reflect the unsharded state.

## Command Syntax

To unshard a collection, use the [`unshardCollection`](/docs/manual/reference/command/unshardCollection#mongodb-dbcommand-dbcmd.unshardCollection) command:

```javascript
db.adminCommand({
   unshardCollection : "<database>.<collection>",
   toShard : "<recipient shard ID>"
})
```

## Use Cases

A user can unshard a collection if:

- You can store the collection entirely on a single shard.

- The collection requires resource isolation, and access patterns are better supported if the collection lives on a single shard. To meet the same requirements on a sharded collection, see [Zone Sharding.](/docs/manual/core/zone-sharding#std-label-zone-sharding)

- The collection was previously sharded but no longer needs to be sharded.

## Get Started

- [Unshard a Collection](/docs/manual/tutorial/unshard-collection#std-label-unshard-collection-task)

## Access Control

If your deployment has [access control](/docs/manual/core/authorization#std-label-authorization) enabled, the [`enableSharding`](/docs/manual/reference/built-in-roles#mongodb-authrole-enableSharding) role grants you access to run the `unshardCollection` command.

## Details

An unsharded collection's data only lives on one shard and the [shard key](/docs/manual/reference/glossary#std-term-shard-key) is removed. Collections that you manually unshard behave the same as newly created collections that were never sharded.

You can specify the destination shard with the optional `toShard` field. If you don't specify a destination shard, MongoDB automatically selects the shard with the least amount of data.

## Learn More

- [Moveable Collections](/docs/manual/core/moveable-collections#std-label-moveable-collections)

- [`unshardCollection`](/docs/manual/reference/command/unshardCollection#mongodb-dbcommand-dbcmd.unshardCollection)
