> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Supported Operations for Queryable Encryption

Queryable Encryption equality and range queries are fully supported in production. Prefix, suffix, and substring queries are only available in public preview in MongoDB 8.2. Do not enable these query types in production. GA functionality of prefix, suffix and substring query types will be incompatible with the preview feature. To learn more, see [Supported Query Types](https://www.mongodb.com/docs/manual/core/queryable-encryption/reference/supported-operations/).

This page documents the specific data types, commands, query operators, update operators, aggregation stages, and aggregation expressions supported for Queryable Encryption compatible drivers. It outlines the behavior for operations using automatic encryption, and operations using explicit encryption.

**Note: Enterprise Feature**

Automatic encryption is available in MongoDB Enterprise and MongoDB Atlas

## Operations Using `BinData`

MongoDB stores Queryable Encryption encrypted fields as a [`BinData`](/docs/manual/reference/mongodb-extended-json-v1#mongodb-bsontype-data_binary) blob. Read and write operations issued against the encrypted `BinData` value may have unexpected or incorrect behavior as compared to issuing that same operation against the decrypted value. Certain operations have strict BSON type support where issuing them against a `BinData` value returns an error.

Official drivers compatible with Queryable Encryption parse read and write operations for operators or expressions that don't support `BinData` values.

## Supported and Unsupported BSON Types

Queryable Encryption supports [configuring](/docs/manual/core/queryable-encryption/qe-create-encryption-schema#std-label-qe-create-encryption-schema) the equality query type `queryType: "equality"` for all [BSON types](/docs/manual/reference/bson-types#std-label-bson-types) **except** the following:

- `array`

- `decimal`: Decimal (IEEE 754 Decimal128)

- `double`: Double (IEEE 754 Binary64)

- `object`

Queryable Encryption supports [configuring](/docs/manual/core/queryable-encryption/qe-create-encryption-schema#std-label-qe-create-encryption-schema) the range query type `queryType: "range"` for the following [BSON types:](/docs/manual/reference/bson-types#std-label-bson-types)

- `date`: UTC DateTime (Int64)

- `decimal`: Decimal (IEEE 754 Decimal128)

- `double`: Double (IEEE 754 Binary64)

- `int`: 32-bit integer

- `long`: 64-bit integer

**Note:**

The query type is the [configuration](/docs/manual/core/queryable-encryption/qe-create-encryption-schema#std-label-qe-create-encryption-schema) of the encrypted index, not the set of query operators by itself. In particular, `decimal` and `double` support the range query type `queryType: "range"`, and MongoDB evaluates equality queries on these fields using the range index.

## CRUD

- Queryable Encryption doesn't support multi-document update or delete operations. [`db.collection.updateMany()`](/docs/manual/reference/method/db.collection.updateMany#mongodb-method-db.collection.updateMany) and [`db.collection.bulkWrite()`](/docs/manual/reference/method/db.collection.bulkWrite#mongodb-method-db.collection.bulkWrite) with more than one update or delete operation aren't supported.

- Queryable Encryption bulk write operations can target only one namespace. If a [`bulkWrite`](/docs/manual/reference/command/bulkWrite#mongodb-dbcommand-dbcmd.bulkWrite) command specifies more than one namespace in `nsInfo`, the operation returns an error.

- Queryable Encryption limits [`db.collection.findAndModify()`](/docs/manual/reference/method/db.collection.findAndModify#mongodb-method-db.collection.findAndModify) arguments.

  - `fields` is not allowed

  - `new` must be false

- When performing an upsert operation, any encrypted fields in the filter are excluded from the insert.

## Supported Read and Write Commands

Queryable Encryption compatible drivers support automatic encryption with the following commands:

- [`aggregate`](/docs/manual/reference/command/aggregate#mongodb-dbcommand-dbcmd.aggregate)

- [`bulkWrite`](/docs/manual/reference/command/bulkWrite#mongodb-dbcommand-dbcmd.bulkWrite)

- [`count`](/docs/manual/reference/command/count#mongodb-dbcommand-dbcmd.count)

- [`delete`](/docs/manual/reference/command/delete#mongodb-dbcommand-dbcmd.delete)

- [`explain`](/docs/manual/reference/command/explain#mongodb-dbcommand-dbcmd.explain)

- [`find`](/docs/manual/reference/command/find#mongodb-dbcommand-dbcmd.find)

- [`findAndModify`](/docs/manual/reference/command/findAndModify#mongodb-dbcommand-dbcmd.findAndModify)

- [`insert`](/docs/manual/reference/command/insert#mongodb-dbcommand-dbcmd.insert)

- [`update`](/docs/manual/reference/command/update#mongodb-dbcommand-dbcmd.update)

For any supported command, the drivers return an error if the command uses an unsupported operator, aggregation stage, or aggregation expression. For a complete list of the supported operators, stages, and expressions, see the following sections:

- [Supported Query Operators](/docs/manual/core/queryable-encryption/reference/supported-operations#std-label-qe-supported-query-operators)

- [Supported Update Operators](/docs/manual/core/queryable-encryption/reference/supported-operations#std-label-qe-supported-update-operators)

- [Supported Aggregation Stages](/docs/manual/core/queryable-encryption/reference/supported-operations#std-label-qe-supported-aggregation-stages)

- [Supported Aggregation Expressions](/docs/manual/core/queryable-encryption/reference/supported-operations#std-label-qe-supported-aggregation-expressions)

The following commands do not require automatic encryption. Official drivers configured for automatic encryption pass these commands directly to the [`mongod`:](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod)

- [`getMore`](/docs/manual/reference/command/getMore#mongodb-dbcommand-dbcmd.getMore)&#x20;

- [`authenticate`](/docs/manual/reference/command/authenticate#mongodb-dbcommand-dbcmd.authenticate)

- [`hello`](/docs/manual/reference/command/hello#mongodb-dbcommand-dbcmd.hello)

- [`logout`](/docs/manual/reference/command/logout#mongodb-dbcommand-dbcmd.logout)

- [`abortTransaction`](/docs/manual/reference/command/abortTransaction#mongodb-dbcommand-dbcmd.abortTransaction)

- [`commitTransaction`](/docs/manual/reference/command/commitTransaction#mongodb-dbcommand-dbcmd.commitTransaction)

- [`endSessions`](/docs/manual/reference/command/endSessions#mongodb-dbcommand-dbcmd.endSessions)

- [`startSession`](/docs/manual/reference/command/startSession#mongodb-dbcommand-dbcmd.startSession)

- [`create`](/docs/manual/reference/command/create#mongodb-dbcommand-dbcmd.create)

- [`createIndexes`](/docs/manual/reference/command/createIndexes#mongodb-dbcommand-dbcmd.createIndexes)

- [`drop`](/docs/manual/reference/command/drop#mongodb-dbcommand-dbcmd.drop)

- [`dropDatabase`](/docs/manual/reference/command/dropDatabase#mongodb-dbcommand-dbcmd.dropDatabase)

- [`dropIndexes`](/docs/manual/reference/command/dropIndexes#mongodb-dbcommand-dbcmd.dropIndexes)

- [`killCursors`](/docs/manual/reference/command/killCursors#mongodb-dbcommand-dbcmd.killCursors)

- [`listCollections`](/docs/manual/reference/command/listCollections#mongodb-dbcommand-dbcmd.listCollections)

- [`listDatabases`](/docs/manual/reference/command/listDatabases#mongodb-dbcommand-dbcmd.listDatabases)

- [`listIndexes`](/docs/manual/reference/command/listIndexes#mongodb-dbcommand-dbcmd.listIndexes)

- [`renameCollection`](/docs/manual/reference/command/renameCollection#mongodb-dbcommand-dbcmd.renameCollection)

- [`ping`](/docs/manual/reference/command/ping#mongodb-dbcommand-dbcmd.ping)

Issuing any other command through a compatible driver configured for automatic encryption returns an error.

While automatic encryption does not encrypt the getMore command, the response to the command may contain encrypted field values.

- Applications configured with the correct Queryable Encryption options automatically decrypt those values.

- Applications without the correct encryption options see the encrypted values.

## Supported Query Types & Operators

Drivers configured for automatic encryption support a limited set of query operators when issued against an encrypted queryable field.

Querying non-encrypted fields or encrypted fields with a supported query type returns encrypted data that is then decrypted at the client.

Queryable Encryption currently supports the following query types:

- `none`

- `equality`

- `range`

- `prefix`

- `suffix`

- `substring`

If the query type is unspecified, it defaults to `none`. If the query type is `none`, MongoDB encrypts the field, and clients can't query it.

**Important: Comparison Support**

Comparison of an encrypted field to a plaintext value is supported.

```json
{$expr: {$eq: ["$encrypted1", "plaintext_value"]}}
```

Comparison of one encrypted field to another encrypted field will fail.

```json
{$expr: {$eq: ["$encrypted1", "$encrypted2"]}}
```

Fields configured for `queryType: "equality"` support the following expressions:

- [`$eq`](/docs/manual/reference/operator/query/eq#mongodb-query-op.-eq)

- [`$ne`](/docs/manual/reference/operator/query/ne#mongodb-query-op.-ne)

- [`$in`](/docs/manual/reference/operator/query/in#mongodb-query-op.-in)

- [`$nin`](/docs/manual/reference/operator/query/nin#mongodb-query-op.-nin)

- [`$and`](/docs/manual/reference/operator/query/and#mongodb-query-op.-and)

- [`$or`](/docs/manual/reference/operator/query/or#mongodb-query-op.-or)

- [`$not`](/docs/manual/reference/operator/query/not#mongodb-query-op.-not)

- [`$nor`](/docs/manual/reference/operator/query/nor#mongodb-query-op.-nor)

- [`$expr`](/docs/manual/reference/operator/query/expr#mongodb-query-op.-expr)

- [`$exists`](/docs/manual/reference/operator/query/exists#mongodb-query-op.-exists)

Range queries implicitly convert equality queries to [`$lte`](/docs/manual/reference/operator/query/lte#mongodb-query-op.-lte) and [`$gte`](/docs/manual/reference/operator/query/gte#mongodb-query-op.-gte). Thus, fields configured for `queryType: "range"` support all expressions above, as well as the following expressions:

- [`$lt`](/docs/manual/reference/operator/query/lt#mongodb-query-op.-lt)

- [`$lte`](/docs/manual/reference/operator/query/lte#mongodb-query-op.-lte)

- [`$gt`](/docs/manual/reference/operator/query/gt#mongodb-query-op.-gt)

- [`$gte`](/docs/manual/reference/operator/query/gte#mongodb-query-op.-gte)

Queries specifying any other query operator against an encrypted field return an error.

### Unsupported Queries

Queries that compare an encrypted field to `null` or a regular expression always throw an error, even if using a supported query operator.

When using a MongoClient configured for Queryable Encryption, the following query operators throw an error, even if issued against an unencrypted field:

- [`$text`](/docs/manual/reference/operator/query/text#mongodb-query-op.-text)

- [`$where`](/docs/manual/reference/operator/query/where#mongodb-query-op.-where)

- [`$jsonSchema`](/docs/manual/reference/operator/query/jsonSchema#mongodb-query-op.-jsonSchema)

## Supported Update Operators

Drivers configured for automatic encryption support the following update operators when issued against encrypted fields:

- [`$set`](/docs/manual/reference/operator/update/set#mongodb-update-up.-set)

- [`$unset`](/docs/manual/reference/operator/update/unset#mongodb-update-up.-unset)

Updates specifying any other update operator against an encrypted field return an error.

Update operations with the following behavior throw an error, even if using a supported operator:

- The update operation produces an array inside of an encrypted path.

- The update operation uses aggregation expression syntax.

For update operations specifying a [query filter](/docs/manual/reference/command/update#std-label-update-command-q) on encrypted fields, the query filter must use only [supported operators](/docs/manual/core/csfle/reference/supported-operations#std-label-csfle-supported-query-operators) on those fields.

## Replacement-style Updates

Replacement-style updates are supported, however, if the replacement document contains a `Timestamp(0,0)` inside a top-level encrypted field, Queryable Encryption will error. The `(0,0)` value indicates that the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) should generate the Timestamp.  [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) cannot generate encrypted fields.

## Unsupported Insert Operations

Compatible drivers configured for automatic encryption do not support insert commands with the following behavior:

- Inserting a document with `Timestamp(0,0)` associated to an encrypted field. The `(0,0)` value indicates that the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) should generate the Timestamp. Since the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) cannot generate encrypted fields, the resulting timestamp would be unencrypted.

## Unsupported Aggregation Stages

Automatic encryption will not support aggregation stages that read from or write to additional collections. These stages are:

- [`$out`](/docs/manual/reference/operator/aggregation/out#mongodb-pipeline-pipe.-out)

- [`$merge`](/docs/manual/reference/operator/aggregation/merge#mongodb-pipeline-pipe.-merge)

## Supported Aggregation Stages

Compatible drivers configured for automatic encryption support the following aggregation pipeline stages:

- [`$addFields`](/docs/manual/reference/operator/aggregation/addFields#mongodb-pipeline-pipe.-addFields)

- [`$bucket`](/docs/manual/reference/operator/aggregation/bucket#mongodb-pipeline-pipe.-bucket)

- [`$bucketAuto`](/docs/manual/reference/operator/aggregation/bucketAuto#mongodb-pipeline-pipe.-bucketAuto)

- [`$collStats`](/docs/manual/reference/operator/aggregation/collStats#mongodb-pipeline-pipe.-collStats)

- [`$count`](/docs/manual/reference/operator/aggregation/count#mongodb-pipeline-pipe.-count)

- [`$geoNear`](/docs/manual/reference/operator/aggregation/geoNear#mongodb-pipeline-pipe.-geoNear)

- [`$graphLookup`](/docs/manual/reference/operator/aggregation/graphLookup#mongodb-pipeline-pipe.-graphLookup) (For usage requirements, see [`$lookup` and `$graphLookup` Behavior)](/docs/manual/core/queryable-encryption/reference/supported-operations#std-label-qe-lookup-graphLookup-behavior)

- [`$group`](/docs/manual/reference/operator/aggregation/group#mongodb-pipeline-pipe.-group) on unencrypted fields

- [`$indexStats`](/docs/manual/reference/operator/aggregation/indexStats#mongodb-pipeline-pipe.-indexStats)

- [`$limit`](/docs/manual/reference/operator/aggregation/limit#mongodb-pipeline-pipe.-limit)

- [`$lookup`](/docs/manual/reference/operator/aggregation/lookup#mongodb-pipeline-pipe.-lookup) (For usage requirements, see [`$lookup` and `$graphLookup` Behavior)](/docs/manual/core/queryable-encryption/reference/supported-operations#std-label-qe-lookup-graphLookup-behavior)

- [`$match`](/docs/manual/reference/operator/aggregation/match#mongodb-pipeline-pipe.-match)

- [`$project`](/docs/manual/reference/operator/aggregation/project#mongodb-pipeline-pipe.-project)

- [`$redact`](/docs/manual/reference/operator/aggregation/redact#mongodb-pipeline-pipe.-redact)

- [`$replaceRoot`](/docs/manual/reference/operator/aggregation/replaceRoot#mongodb-pipeline-pipe.-replaceRoot)

- [`$sample`](/docs/manual/reference/operator/aggregation/sample#mongodb-pipeline-pipe.-sample)

- [`$skip`](/docs/manual/reference/operator/aggregation/skip#mongodb-pipeline-pipe.-skip)

- [`$sort`](/docs/manual/reference/operator/aggregation/sort#mongodb-pipeline-pipe.-sort)

- [`$sortByCount`](/docs/manual/reference/operator/aggregation/sortByCount#mongodb-pipeline-pipe.-sortByCount)

- [`$unwind`](/docs/manual/reference/operator/aggregation/unwind#mongodb-pipeline-pipe.-unwind)

Aggregation pipelines operating on collections configured for automatic encryption that specify any other stage return an error.

For each supported pipeline stage, MongoDB tracks fields that *must* be encrypted as they pass through the supported pipelines and marks them for encryption.

Each supported stage must specify only supported [query operators](/docs/manual/core/queryable-encryption/reference/supported-operations#std-label-qe-supported-query-operators) and [aggregation expressions.](/docs/manual/core/queryable-encryption/reference/supported-operations#std-label-qe-supported-aggregation-expressions)

### `$lookup` and `$graphLookup` Behavior

Starting in MongoDB 8.1, you can reference multiple encrypted collections in a [`$lookup`](/docs/manual/reference/operator/aggregation/lookup#mongodb-pipeline-pipe.-lookup) stage. However, `$lookup` does not support:

- Using an encrypted field as the join field in the `localField` or `foreignField`.

- Using any field in an encrypted array. An array is considered as encrypted if it contains any encrypted elements.

  - For example, you can't use any field within the resulting [as](/docs/manual/reference/operator/aggregation/lookup#std-label-lookup-subquery-as) array of the `$lookup` operation.

Automatic encryption supports [`$graphLookup`](/docs/manual/reference/operator/aggregation/graphLookup#mongodb-pipeline-pipe.-graphLookup) *only if* the `from` collection matches the collection the aggregation runs against. `$graphLookup` stages that reference a different `from` collection return an error.

Automatic encryption does not support "connectionless" aggregation metadata sources, which read metadata that doesn't pertain to a particular collection, such as:

- [`$currentOp`](/docs/manual/reference/operator/aggregation/currentOp#mongodb-pipeline-pipe.-currentOp)

- [MongoDB Change Streams](/docs/manual/changeStreams#std-label-changeStreams) for watching a database or the whole cluster

- [`$listSessions`](/docs/manual/reference/operator/aggregation/listSessions#mongodb-pipeline-pipe.-listSessions)

- [`$listLocalSessions`](/docs/manual/reference/operator/aggregation/listLocalSessions#mongodb-pipeline-pipe.-listLocalSessions)

Automatic encryption does not support the [`$planCacheStats`](/docs/manual/reference/operator/aggregation/planCacheStats#mongodb-pipeline-pipe.-planCacheStats) stage as the result may contain sensitive information.

## Supported Aggregation Expressions

Compatible drivers configured for automatic encryption support the following expressions against encrypted fields configured for equality queries:

- [`$cond`](/docs/manual/reference/operator/aggregation/cond#mongodb-expression-exp.-cond)

- [`$eq`](/docs/manual/reference/operator/aggregation/eq#mongodb-expression-exp.-eq)

- [`$ifNull`](/docs/manual/reference/operator/aggregation/ifNull#mongodb-expression-exp.-ifNull)

- [`$in`](/docs/manual/reference/operator/aggregation/in#mongodb-expression-exp.-in)

- [`$let`](/docs/manual/reference/operator/aggregation/let#mongodb-expression-exp.-let)

- [`$literal`](/docs/manual/reference/operator/aggregation/literal#mongodb-expression-exp.-literal)

- [`$ne`](/docs/manual/reference/operator/aggregation/ne#mongodb-expression-exp.-ne)

- [`$switch`](/docs/manual/reference/operator/aggregation/switch#mongodb-expression-exp.-switch)

Compatible drivers configured for automatic encryption support the following expressions against encrypted fields configured for `prefix`, `suffix`, or `substring` queries:

- [`$encStrStartsWith`](/docs/manual/reference/operator/aggregation/encStrStartsWith#mongodb-expression-exp.-encStrStartsWith)

- [`$encStrEndsWith`](/docs/manual/reference/operator/aggregation/encStrEndsWith#mongodb-expression-exp.-encStrEndsWith)

- [`$encStrContains`](/docs/manual/reference/operator/aggregation/encStrContains#mongodb-expression-exp.-encStrContains)

- [`$encStrNormalizedEq`](/docs/manual/reference/operator/aggregation/encStrNormalizedEq#mongodb-expression-exp.-encStrNormalizedEq)

All other aggregation expressions return an error if issued against encrypted fields.

Aggregation stages with the following behavior return an error, even if using a supported aggregation expression:

| Expressions | Rejected Behavior | Example |
| --- | --- | --- |
| [`$cond`](/docs/manual/reference/operator/aggregation/cond#mongodb-expression-exp.-cond) [`$switch`](/docs/manual/reference/operator/aggregation/switch#mongodb-expression-exp.-switch) | The expression specifies a field whose encryption properties cannot be known until runtime *and* a subsequent aggregation stage includes an expression referencing that field. | `$addFields : {
  "valueWithUnknownEncryption" : {
    $cond : {
      if : { "$encryptedField" : "value" },
      then : "$encryptedField",
      else: "unencryptedValue"
    }
  }
},
{
  $match : {
    "valueWithUnknownEncryption" : "someNewValue"
  }
}` |
| [`$eq`](/docs/manual/reference/operator/aggregation/eq#mongodb-expression-exp.-eq) [`$ne`](/docs/manual/reference/operator/aggregation/ne#mongodb-expression-exp.-ne) | The expression creates a new field that references an encrypted field *and* operates on that new field in the same expression. | `{
  $eq : [
    {"newField" : "$encryptedField"},
    {"newField" : "value"
  ]
}` |
| [`$eq`](/docs/manual/reference/operator/aggregation/eq#mongodb-expression-exp.-eq) [`$ne`](/docs/manual/reference/operator/aggregation/ne#mongodb-expression-exp.-ne) | The expression references the prefix of an encrypted field within the comparison expression. | `{ $eq : [ "$prefixOfEncryptedField" , "value"] }` |
| [`$eq`](/docs/manual/reference/operator/aggregation/eq#mongodb-expression-exp.-eq) [`$ne`](/docs/manual/reference/operator/aggregation/ne#mongodb-expression-exp.-ne) | The result of the expression is compared to an encrypted field. | `{
  $eq : [
      "$encryptedField" ,
      { $ne : [ "field", "value" ] }
  ]
}` |
| [`$let`](/docs/manual/reference/operator/aggregation/let#mongodb-expression-exp.-let) | The expression binds a variable to an encrypted field or attempts to rebind [`$$CURRENT`.](/docs/manual/reference/aggregation-variables#mongodb-variable-variable.CURRENT) | `{
  $let: {
    "vars" : {
      "newVariable" : "$encryptedField"
    }
  }
}` |
| [`$in`](/docs/manual/reference/operator/aggregation/in#mongodb-expression-exp.-in) | The first argument to the expression *is* an encrypted field, *and* The second argument to the expression is *not* an array literal*-OR-*; The second argument to the expression is an encrypted field. | `{
  $in : [
    "$encryptedField" ,
    "$otherEncryptedField"
  ]
}` |

## Unsupported Field Types

Drivers configured for automatic encryption do not support any read or write operation that requires encrypting the following value types, because Queryable Encryption doesn't adequately hide the type information for these values:

- [`MaxKey`](/docs/manual/reference/mongodb-extended-json#mongodb-bsontype-MaxKey)

- [`MinKey`](/docs/manual/reference/mongodb-extended-json#mongodb-bsontype-MinKey)

- `null`

- `undefined`

Queryable Encryption supports automatic and explicit encryption of array fields if the query type is `none`. You can encrypt an array, but not the fields within it, and you can't query an encrypted array.

Queryable Encryption does not support read or write operations on an encrypted field where the operation compares the encrypted field to the following value types:

- `array`

- `object`
