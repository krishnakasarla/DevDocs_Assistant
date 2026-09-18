> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Wildcard Index Restrictions

This page describes limitations for wildcard indexes such as incompatible properties and unsupported query patterns.

## Compound Wildcard Index Restrictions

[Compound wildcard indexes](/docs/manual/core/indexes/index-types/index-wildcard/index-wildcard-compound#std-label-wildcard-index-compound) have the following restrictions:

- A compound wildcard index can only have one wildcard term.

  For example, you cannot specify the following index:

  ```javascript
  { userID: 1, "object1.$**": 1, "object2.$**": 1 }
  ```

- The non-wildcard terms in a compound wildcard index must be single key terms. [Multikey](/docs/manual/core/indexes/index-types/index-multikey#std-label-index-type-multikey) index terms are not permitted.

- You can only specify the `wildcardProjection` option when the wildcard field is `$**`. You cannot use `wildcardProjection` when you specify a field path for the wildcard index term.

  This is a valid definition:

  ```javascript
  {
     key: { "$**": 1 },
     name: "index_all_with_projection",
     wildcardProjection: {
        "someFields.name": 1,
        "otherFields.values": 1
     }
  }
  ```

  This is an invalid definition:

  ```javascript
  {
     key: { "someFields.$**": 1 },
     name: "invalid_index",
     wildcardProjection: {
        "someFields.name": 1,
        "otherFields.values": 1
     }
  }
  ```

- The `_id` field is omitted by default. If you need the `_id` field:

  - Specify a wildcard index as `$**`.

  - Include the `_id` field in the `wildcardProjection` with `_id:
    1`.

  ```javascript
  db.studentGrades.createIndex(
     {
        "$**": 1,
     },
     {
        wildcardProjection: {
           _id: 1,
           exams: 1,
           extraCredit: 1
        }
     }
  )
  ```

- You cannot include the same field in the wildcard fields and the regular fields. To exclude fields from the wildcard pattern, use a `wildcardProjection` with exclusion rules.

  ```javascript
  db.studentGrades.createIndex(
     {
        exams: 1,
        "$**": 1,
        homeworks: 1
     },
     {
        wildcardProjection: {
           exams: 0,
           homeworks: 0
        }
     }
  )
  ```

### wildcardProjection Validation Rules

Starting in MongoDB 8.3 (and 8.2.4, 8.0.18, 7.0.29), stricter validation rules apply to `wildcardProjection` in compound wildcard indexes to prevent invalid configurations.

Existing indexes that do not meet the new validation requirements continue to function, but you cannot create new indexes that don't meet these requirements.

When using `wildcardProjection` with compound wildcard indexes, the following rules apply:

| Rule | Valid Example | Invalid Example |
| --- | --- | --- |
| If you specify a `wildcardProjection`, it cannot be empty. | `{ productId: 1, "$**": 1 },
{
  wildcardProjection: {
    attributes: 1
  }
}` | `{ productId: 1, "$**": 1 },
{
  wildcardProjection: { }
}` |
| You can only combine inclusions and exclusions in a `wildcardProjection` if the included or excluded field is `_id`. You can exclude `_id` in inclusion projections or include `_id` in exclusion projections. | `{ "$**": 1, category: 1 },
{
  wildcardProjection: {
    _id: 0,
    attributes: 1
  }
}` `{ "$**": 1, category: 1 },
{
  wildcardProjection: {
    _id: 1,
    metadata: 0
  }
}` | `{ "$**": 1, category: 1 },
{
  wildcardProjection: {
    _id: 0,
    price: 0,
    stock: 1
  }
}` |
| The fields included in the `wildcardProjection` must not overlap with any regular (non-wildcard) index fields. | `{ userId: 1, "$**": 1 },
{
  wildcardProjection: {
    preferences: 1
  }
}` | `{ userId: 1, "$**": 1 },
{
  wildcardProjection: {
    userId: 1
  }
}` |
| You can only specify an `_id`-only exclusion if the regular index field is also `_id`. | `{ _id: 1, "$**": 1 },
{
  wildcardProjection: {
    _id: 0
  }
}` | `{ productId: 1, "$**": 1 },
{
  wildcardProjection: {
    _id: 0
  }
}` |
| If the `wildcardProjection` is an exclusion, it must exclude all regular index fields. | `{
  userId: 1,
  category: 1,
  "$**": 1
},
{
  wildcardProjection: {
    userId: 0,
    category: 0
  }
}` | `{
  userId: 1,
  category: 1,
  "$**": 1
},
{
  wildcardProjection: {
    userId: 0
  }
}` |

## Incompatible Index Properties

Wildcard indexes do not support:

- [2d (Geospatial) indexes](/docs/manual/core/indexes/index-types/geospatial/2d/internals#std-label-2d-index-internals)

- [2dsphere (Geospatial) indexes](/docs/manual/core/indexes/index-types/geospatial/2dsphere#std-label-2dsphere-index)

- [Hashed indexes](/docs/manual/core/indexes/index-types/index-hashed#std-label-index-type-hashed)

- [Time to Live (TTL) indexes](/docs/manual/core/index-ttl#std-label-index-feature-ttl)

- [Text indexes](/docs/manual/core/indexes/index-types/index-text#std-label-index-feature-text)

- [Unique indexes](/docs/manual/core/index-unique#std-label-index-type-unique)

Wildcard indexes are [sparse](/docs/manual/core/index-sparse#std-label-index-type-sparse) indexes. They do not support queries when an indexed field does not exist. A wildcard index will index the document if the wildcard field has a `null` value.

Starting in MongoDB 7.0, wildcard indexes support ascending (`1`) and descending (`-1`) sort order. Earlier versions only supported ascending order.

## Incompatible Index Types

You cannot create the following index types using wildcard syntax (`$.**`):

- [2d (Geospatial)](/docs/manual/core/indexes/index-types/geospatial/2d#std-label-2d-index)

- [2dsphere (Geospatial)](/docs/manual/core/indexes/index-types/geospatial/2dsphere#std-label-2dsphere-index)

- [Hashed](/docs/manual/core/indexes/index-types/index-hashed#std-label-index-type-hashed)

**Note: Disambiguation**

Wildcard Indexes are distinct from and incompatible with [Create a Wildcard Text Index on Self-Managed Deployments](/docs/manual/core/indexes/index-types/index-text/create-wildcard-text-index#std-label-create-wildcard-text-index). Wildcard indexes cannot support queries using the [`$text`](/docs/manual/reference/operator/query/text#mongodb-query-op.-text) operator.

## Shard Key

You cannot use a wildcard index as a [shard key index.](/docs/manual/core/sharding-shard-key-indexes#std-label-sharding-shard-key-indexes)

## \_id Fields

Wildcard indexes omit the `_id` field by default. To include the `_id` field in the wildcard index, you must explicitly include it in the `wildcardProjection` document:

```javascript
{
    "wildcardProjection": {
      "_id": 1,
      "<field>": 0|1
    }
}
```

All of the statements in the `wildcardProjection` document must be either inclusion or exclusion statements. You can also include the `_id` field with exclusion statements. This is the only exception to the rule.

## Unsupported Query Patterns

Wildcard indexes cannot support the following query patterns:

### Array Field is Not Equal to `null`

If a given field is an array in any document in the collection, wildcard indexes cannot support queries for documents where that field is not equal to `null`.

For example, consider an `inventory` collection with a wildcard index on `product_attributes`. The wildcard index **cannot** support the following queries if `product_attributes.tags` is an array in any document in the collection:

```javascript
db.inventory.find( { $ne : [ "product_attributes.tags", null ] } )

db.inventory.aggregate( [
   {
      $match : { $ne : [ "product_attributes.tags", null ] }
   }
] )
```

### Equality Matches on Documents and Arrays

Wildcard indexes store entries for the contents of a document or array, not the document or array itself. Therefore, wildcard indexes cannot support exact equality matches on documents or arrays.

For example, consider an `inventory` collection with a wildcard index on `product_attributes`. The wildcard index cannot support the following queries:

```javascript
db.inventory.find(
   {
      "product_attributes" : { "price" : 29.99 }
   }
)

db.inventory.find(
   {
      "product_attributes.tags" : [ "waterproof", "fireproof" ]
   }
)
```

**Note:**

Wildcard indexes **can** support queries where the field equals an empty document `{}`.

Similarly, wildcard indexes cannot support exact **inequality** matches on documents and arrays. For example, a wildcard index on `product_attributes` cannot support the following queries:

```javascript
db.inventory.aggregate( [
   {
      $match : {
         $ne : [ "product_attributes", { "price" : 29.99 } ]
      }
   }
] )

db.inventory.aggregate( [
   {
      $match : {
         $ne : [ "product_attributes.tags", [ "waterproof", "fireproof" ] ]
      }
   }
] )
```

### Field Does Not Exist

Wildcard indexes are [sparse](/docs/manual/core/index-sparse#std-label-index-type-sparse) and do not index empty fields. Therefore, wildcard indexes cannot support queries for documents where a field does not exist.

For example, consider an `inventory` collection with a wildcard index on `product_attributes`. The wildcard index cannot support the following queries:

```javascript
db.inventory.find(
   {
      "product_attributes" : { $exists : false }
   }
)

db.inventory.aggregate( [
  {
     $match : {
        "product_attributes" : { $exists : false }
     }
  }
] )
```

### Multi-Field Query Predicates

In the case that a single wildcard index could support multiple query fields, MongoDB can only use the wildcard index to support one of the query fields.

For example, consider an `inventory` collection with a wildcard index on `product_attributes`. The wildcard index cannot support all of the predicates in the following query:

```javascript
db.inventory.find(
   {
      "product_attributes.price": { $gt: 20 },
      "product_attributes.material": "silk",
      "product_attributes.size": "large"
   }
)
```

Instead, MongoDB uses the wildcard index to support only one of the query predicates. MongoDB automatically chooses which predicate to support based on relevant wildcard index paths. The unsupported query predicates are shown in the [`rejectedPlans`](/docs/manual/reference/explain-results#mongodb-data-explain.queryPlanner.rejectedPlans) of the [explain results.](/docs/manual/reference/explain-results#std-label-explain-results)

This is also true for compound wildcard indexes. The wildcard term of a compound index can only support one query predicate, although the non-wildcard terms can support the remaining predicates.

**Note: $or Behavior**

MongoDB may use the same wildcard index to support each independent argument of the query [`$or`](/docs/manual/reference/operator/query/or#mongodb-query-op.-or) or aggregation [`$or`](/docs/manual/reference/operator/aggregation/or#mongodb-expression-exp.-or) operators.

### Queries with Sort

MongoDB can use a wildcard index for satisfying the [`sort()`](/docs/manual/reference/method/cursor.sort#mongodb-method-cursor.sort) **only if** all of the following are true:

- The query planner selects the wildcard index for satisfying the query predicate.

- The [`sort()`](/docs/manual/reference/method/cursor.sort#mongodb-method-cursor.sort) specifies **only** the query predicate field.

- The specified field is never an array.

If the above conditions are not met, MongoDB cannot use the wildcard index for the sort. MongoDB does not support [`sort()`](/docs/manual/reference/method/cursor.sort#mongodb-method-cursor.sort) operations that require a different index from that of the query predicate.

Consider the following wildcard index on the `products` collection:

```javascript
db.products.createIndex( { "product_attributes.$**" : 1 } )
```

The following operation queries for a single field `product_attributes.price` and sorts on that same field:

```javascript
db.products.find(
  { "product_attributes.price" : { $gt : 10.00 } },
).sort(
  { "product_attributes.price" : 1 }
)
```

Assuming that the specified `price` is never an array, MongoDB can use the `product_attributes.$**` wildcard index for satisfying both the [`find()`](/docs/manual/reference/method/db.collection.find#mongodb-method-db.collection.find) and [`sort()`.](/docs/manual/reference/method/cursor.sort#mongodb-method-cursor.sort)
