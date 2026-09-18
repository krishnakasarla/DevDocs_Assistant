> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Shard Key Indexes

Sharded collections require an index that supports the [shard key](/docs/manual/reference/glossary#std-term-shard-key). The index can be an index on the shard key or a [compound index](/docs/manual/reference/glossary#std-term-compound-index) where the shard key is a [prefix](/docs/manual/core/indexes/index-types/index-compound#std-label-compound-index-prefix) of the index.

- If the collection is empty, [`sh.shardCollection()`](/docs/manual/reference/method/sh.shardCollection#mongodb-method-sh.shardCollection) creates the index on the shard key if such an index does not already exists.

- If the collection is not empty, you must create the index first before using [`sh.shardCollection()`.](/docs/manual/reference/method/sh.shardCollection#mongodb-method-sh.shardCollection)

- If you reshard a collection using [`sh.reshardCollection()`](/docs/manual/reference/method/sh.reshardCollection#mongodb-method-sh.reshardCollection), you do not need to create the index on the new shard key beforehand. The resharding operation builds the required indexes automatically. To learn more, see the [Reshard a Collection procedure.](/docs/manual/core/sharding-reshard-a-collection#std-label-resharding_process)

You cannot [drop](/docs/manual/reference/method/db.collection.dropIndex#std-label-collection-drop-index) or [hide](/docs/manual/reference/method/db.collection.hideIndex#std-label-collection-hide-index) an index if it is the only non-hidden index that supports the shard key.

Starting in MongoDB 7.0.3, 6.0.12, and 5.0.22, you can drop the index for a [hashed shard key](/docs/manual/core/hashed-sharding#std-label-sharding-hashed-sharding). For details, see [Drop a Hashed Shard Key Index.](/docs/manual/tutorial/drop-a-hashed-shard-key-index#std-label-drop-a-hashed-shard-key-index)

## Unique Indexes

MongoDB can enforce a uniqueness constraint on a ranged shard key index. Using a unique index on the shard key enforces uniqueness on the entire key combination and not individual components of the shard key.

For a ranged sharded collection, only the following indexes can be [unique:](/docs/manual/core/index-unique#std-label-index-type-unique)

- The index on the shard key

- A [compound index](/docs/manual/reference/glossary#std-term-compound-index) where the shard key is a [prefix](/docs/manual/core/indexes/index-types/index-compound#std-label-compound-index-prefix)

- The default `_id` index; however, the `_id` index only enforces the uniqueness constraint **per shard** if the `_id` field is not the shard key.

**Important:**

Sharded clusters do not enforce the uniqueness constraint on `_id` fields across the cluster when the `_id` field is not the shard key.

If the `_id` field is not the shard key, the uniqueness constraint only applies to the shard that stores the document. This means that two or more documents can have the same `_id` value, provided they occur on different shards.

For example, consider a sharded collection with shard key `{x:
    1}` that spans two shards A and B. Because the `_id` key is not the shard key, the collection could have a document with `_id` value `1` in shard A and another document with `_id` value `1` in shard B.

In cases where the `_id` field is not the shard key, MongoDB expects applications to ensure the uniqueness of `_id` values across the shards, for example, by using a unique identifier to populate the `_id` field.

The unique index constraints mean that:

- For a to-be-sharded collection, you cannot shard the collection if the collection has multiple unique indexes unless the shard key is the prefix for all the unique indexes.

- For an already-sharded collection, you cannot create unique indexes on other fields unless the shard key is included as the prefix.

- A unique index stores a null value for a document missing the indexed field; that is a missing index field is treated as another instance of a `null` index key value. For more information, see [Missing Document Field in a Unique Single-Field Index.](/docs/manual/core/index-unique#std-label-unique-index-and-missing-field)

To enforce uniqueness on the shard key values, pass the `unique` parameter as `true` to the [`sh.shardCollection()`](/docs/manual/reference/method/sh.shardCollection#mongodb-method-sh.shardCollection) method:

- If the collection is empty, [`sh.shardCollection()`](/docs/manual/reference/method/sh.shardCollection#mongodb-method-sh.shardCollection) creates the unique index on the shard key if such an index does not already exist.

- If the collection is not empty, you must create the index first before using [`sh.shardCollection()`.](/docs/manual/reference/method/sh.shardCollection#mongodb-method-sh.shardCollection)

Although you can have a unique [compound index](/docs/manual/reference/glossary#std-term-compound-index) where the shard key is a [prefix](/docs/manual/core/indexes/index-types/index-compound#std-label-compound-index-prefix), if using `unique` parameter, the collection must have a unique index that is on the shard key.

You cannot specify a unique constraint on a [hashed index.](/docs/manual/core/indexes/index-types/index-hashed#std-label-index-type-hashed)

To maintain uniqueness on a field that is not your shard key, see [Unique Constraints on Arbitrary Fields.](/docs/manual/tutorial/unique-constraints-on-arbitrary-fields#std-label-shard-key-arbitrary-uniqueness)
