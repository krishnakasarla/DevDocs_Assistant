> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Compound Wildcard Indexes

**New in version 7.0**

MongoDB supports creating wildcard indexes on a field or a set of fields. A compound index has multiple index terms. A compound wildcard index has one wildcard term and one or more additional index terms.

**Important:**

Wildcard indexes do not replace workload-based index planning.

For more information on creating indexes that support your workload, see [Create Indexes to Support Your Queries.](/docs/manual/data-modeling/schema-design-process/create-indexes#std-label-create-indexes-to-support-queries)

## Use Cases

### Search Using the Attribute Pattern

The [attribute pattern](https://www.mongodb.com/blog/post/building-with-patterns-the-attribute-pattern) is a useful technique for searching documents that share common characteristics.

Unfortunately, it is expensive to create a lot of individual indexes to cover all of the possible queries. A wildcard index is a good alternative to creating a large number of individual indexes because one wildcard index can efficiently cover many potential queries.

Consider a schema like:

```javascript
{
     tenantId: <Number>,
     tenantRegion: <Number>,
     customFields: {
                     addr: <String>,
                     name: <String>,
                     blockId: <Number>,
                     ...
     }
    dateOpened: <Date>
 }
```

You might want to query aspects of the `customFields` field for tenants that have a particular `tenantId`. You could create a series of individual indexes:

```javascript
{ tenantId: 1, "customFields.addr": 1 }
{ tenantId: 1, "customFields.name": 1 }
{ tenantId: 1, "customFields.blockId": 1 }
...
```

This approach is difficult to maintain and you are likely to reach the maximum number of indexes per collection (64).

Use a compound wildcard index instead. The compound wildcard index is easier to write, easier to maintain, and is unlikely to reach the 64 index collection limit.

This example creates a compound wildcard index on the `salesData` collection:

```javascript
db.runCommand(
   {
       createIndexes: "salesData",
       indexes: [
          {
             key: {
                tenantId: 1,
                "customFields.$**": 1
             },
             name: "tenant_customFields"
          }
       ]
   }
)
```

The wildcard, `"customFields.$**"`, specifies all of the sub-fields in the `customFields` field. The other index term, `tenantId`, is not a wildcard specification; it is a standard field specification.

## Behavior

To create wildcard indexes, use a standard index creation command:

- [`createIndexes`](/docs/manual/reference/command/createIndexes#mongodb-dbcommand-dbcmd.createIndexes)

- [`createIndex()`](/docs/manual/reference/method/db.collection.createIndex#mongodb-method-db.collection.createIndex)

- [`createIndexes()`](/docs/manual/reference/method/db.collection.createIndexes#mongodb-method-db.collection.createIndexes)

### General Considerations for Wildcard Indexes

- Wildcard indexes omit the `_id` field by default. To include the `_id` field in a wildcard index, you must explicitly include it in the `wildcardProjection` document.

  ```javascript
  db.salesData.createIndex(
     { "$**" : 1 },
     { "wildcardProjection" :
        { "_id": 1, "customers.lastName": 1, "customers.FirstName": 1, }
     }
  )
  ```

- You can create more than one wildcard index on a collection.

- A wildcard index may cover the same fields as other indexes in the collection.

- Wildcard indexes are [sparse](/docs/manual/core/index-sparse#std-label-index-type-sparse). They only include entries for documents that contain the indexed field.

  The document is not indexed if all of the fields in the compound wildcard index are missing.

### Compound Wildcard Index Considerations

- Compound wildcard indexes are sparse indexes.

- Documents are included in the index if they are missing the wildcard field but have one of the compound fields.

- Index fields, including wildcard fields, can be sorted in ascending (`1`) or descending (`-1`) order.

## Get Started

### Filter Fields with a `wildcardProjection`

You can use a `wildcardProjection` to specify individual sub-fields.

```javascript
db.runCommand(
   {
       createIndexes: "salesData",
       indexes: [
          {
             key: {
                tenantId: 1,
                "$**": 1
             },
             name: "tenant_customFields_projection",
             wildcardProjection: {
                "customFields.addr": 1,
                "customFields.name": 1
             }
          }
       ]
   }
)
```

The wildcard index term, `"$**"`, specifies every field in the collection. The `wildcardProjection` limits the index to the specified fields, `"customFields.addr"` and `"customFields.name"`.

You can only use a `wildcardProjection` when the wildcard term is `$**`.

### Use a Helper Method to Create a Wildcard Index

MongoDB provides [shell helper methods](/docs/manual/reference/method#std-label-js-administrative-methods) for most [database commands](/docs/manual/reference/command#std-label-database-commands). These shell methods offer a simplified syntax and are functionally equivalent to the database commands.

The shell helper for the [first example](/docs/manual/core/indexes/index-types/index-wildcard/index-wildcard-compound#std-label-wc-ex-first) is:

```javascript
db.salesData.createIndex(
   { tenantId: 1, "customFields.$**": 1 },
   {
      name: "tenant_customFields_shellHelper"
   }
)
```

The shell helper for the [second example](/docs/manual/core/indexes/index-types/index-wildcard/index-wildcard-compound#std-label-wc-ex-second) is:

```javascript
db.salesData.createIndex(
  { tenantId: 1, "$**": 1 },
  { "wildcardProjection": {
        "customFields.addr": 1,
        "customFields.name": 1
     },
     name: "tenant_customFields_projection_helper"
  }
)
```

If you want to compare the shell commands and the database commands, you must drop the indexes between command invocations. You cannot create the same index twice, even with different names.

To drop an index, insert the index name and run [db.collection.dropIndex().](/docs/manual/reference/method/db.collection.dropIndex#std-label-collection-drop-index)

```javascript
db.salesData.dropIndex( "tenant_customFields" )
```

The preceding command removes the `"tenant_customFields"` index from the `salesData` database.

### Create a Partial Compound Wildcard Index

To create a [partial](/docs/manual/core/index-partial#std-label-index-type-partial) compound wildcard index, you can use the `partialFilterExpression` option to specify a filter expression so that the index only includes documents that match the filter condition. `partialFilterExpression` can cover fields included or not included in the index.

The following example creates a partial compound wildcard index on the `tenantId` field and on all the sub-fields in the `customFields` field, only on documents with a `tenantRegion` of `1`.

```javascript
db.runCommand(
   {
      createIndexes: "salesData",
      indexes: [
         {
            key: {
               tenantId: 1,
               "customFields.$**": 1
            },
            name: "tenant_customFields_partial",
            partialFilterExpression: { tenantRegion: 1 }
         }
      ]
   }
)
```

## Learn More

- [Behavioral details for wildcard indexes](/docs/manual/core/indexes/index-types/index-wildcard#std-label-wildcard-index-details)

- [Single wildcard indexes](/docs/manual/core/indexes/index-types/index-wildcard/create-wildcard-index-single-field#std-label-wildcard-index-single)

- [Wildcard text indexes](/docs/manual/core/indexes/index-types/index-text/create-wildcard-text-index#std-label-create-wildcard-text-index)
