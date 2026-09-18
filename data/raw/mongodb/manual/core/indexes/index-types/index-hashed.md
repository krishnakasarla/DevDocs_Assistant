> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Hashed Indexes

Hashed indexes collect and store hashes of the values of the indexed field.

Hashed indexes support [sharding](/docs/manual/sharding#std-label-sharding-background) using hashed shard keys. [Hashed based sharding](/docs/manual/core/hashed-sharding#std-label-sharding-hashed-sharding) uses a hashed index of a field as the shard key to partition data across your sharded cluster.

## Use Cases

Hashed indexing is ideal for shard keys with fields that change [monotonically](/docs/manual/core/sharding-choose-a-shard-key#std-label-shard-key-monotonic) like [ObjectId](/docs/manual/reference/glossary#std-term-ObjectId) values or timestamps. When you use [ranged sharding](/docs/manual/core/ranged-sharding#std-label-sharding-ranged) with a monotonically increasing shard key value, the chunk with an upper bound of [`MaxKey`](/docs/manual/reference/mongodb-extended-json#mongodb-bsontype-MaxKey) receives the majority incoming writes. This behavior restricts insert operations to a single shard, which removes the advantage of distributed writes in a sharded cluster.

For more information on choosing the best sharding approach for your application, see [Hashed vs Ranged Sharding](/docs/manual/core/hashed-sharding#std-label-hashed-versus-ranged-sharding)

## Behavior

### Floating-Point Numbers

Hashed indexes truncate floating-point numbers to 64-bit integers before hashing. For example, a hashed index uses the same hash to store the values `2.3`, `2.2`, and `2.9`. This is a **collision**, where multiple values are assigned to a single hash key. Collisions may negatively impact query performance.

To prevent collisions, do not use a hashed index for floating-point numbers that cannot be reliably converted to 64-bit integers and then back to floating point.

Hashed indexes do not support floating-point numbers larger than 2 53.

### Limitations

Hashed indexes have limitations for array fields and the unique property.

#### Array Fields

The hashing function does not support [multikey indexes:](/docs/manual/core/indexes/index-types/index-multikey#std-label-index-type-multikey)

- You cannot create a hashed index on a field that contains an array *or* insert an array into a hashed indexed field.

- If any field in a compound index is an array, no field in that index can use a hashed index. This includes non-array fields.

- You cannot use hashed indexes in a compound index that becomes a multikey index.

#### Covered Queries

Hashed indexes can't [cover a query.](/docs/manual/core/query-optimization#std-label-covered-queries)

#### Unique Constraint

You cannot specify a [unique constraint](/docs/manual/core/index-unique#std-label-index-type-unique) on a hashed index. Instead, you can create an additional non-hashed index with the unique constraint. MongoDB can use that non-hashed index to enforce uniqueness on the chosen field.

## Get Started

To create a hashed index, see [Create a Hashed Index.](/docs/manual/core/indexes/index-types/index-hashed/create#std-label-hashed-index-create)

## Details

This section describes technical details for hashed indexes.

### Hashing Function

**Important:**

When MongoDB uses a hashed index to resolve a query, it uses a hashing function to automatically compute the hash values. Applications do **not** need to compute hashes.

To see what the hashed value would be for a key, use the [`convertShardKeyToHashed()`](/docs/manual/reference/method/convertShardKeyToHashed#mongodb-method-convertShardKeyToHashed) method. This method uses the same hashing function as the hashed index.

### Embedded Documents

The hashing function collapses embedded documents and computes the hash for the entire value.

## Learn More

- [Sharding](/docs/manual/sharding#std-label-sharding-background)

- [Hashed Sharding](/docs/manual/core/hashed-sharding#std-label-sharding-hashed-sharding)

- [Hashed vs Ranged Sharding](/docs/manual/core/hashed-sharding#std-label-hashed-versus-ranged-sharding)
