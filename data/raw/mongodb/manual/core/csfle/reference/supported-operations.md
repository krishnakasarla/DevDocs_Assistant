> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Supported Operations for Automatic Encryption

This page documents the specific commands, query operators, update operators, aggregation stages, and aggregation expressions supported by drivers configured for automatic Client-Side Field Level Encryption.

## Supported Read and Write Commands

Drivers using automatic Client-Side Field Level Encryption support the following commands:

- [`aggregate`](/docs/manual/reference/command/aggregate#mongodb-dbcommand-dbcmd.aggregate)

- [`count`](/docs/manual/reference/command/count#mongodb-dbcommand-dbcmd.count)

- [`delete`](/docs/manual/reference/command/delete#mongodb-dbcommand-dbcmd.delete)

- [`distinct`](/docs/manual/reference/command/distinct#mongodb-dbcommand-dbcmd.distinct)

- [`explain`](/docs/manual/reference/command/explain#mongodb-dbcommand-dbcmd.explain)

- [`find`](/docs/manual/reference/command/find#mongodb-dbcommand-dbcmd.find)

- [`findAndModify`](/docs/manual/reference/command/findAndModify#mongodb-dbcommand-dbcmd.findAndModify)

- [`insert`](/docs/manual/reference/command/insert#mongodb-dbcommand-dbcmd.insert)

- [`update`](/docs/manual/reference/command/update#mongodb-dbcommand-dbcmd.update)

For any supported command, drivers return an error if the command uses an unsupported operator, aggregation stage, or aggregation expression. For a complete list of the supported operators, stages, and expressions, see the following sections of this page:

- [Supported Query Operators](/docs/manual/core/csfle/reference/supported-operations#std-label-csfle-supported-query-operators)

- [Supported Update Operators](/docs/manual/core/csfle/reference/supported-operations#std-label-csfle-supported-update-operators)

- [Supported Aggregation Stages](/docs/manual/core/csfle/reference/supported-operations#std-label-csfle-supported-aggregation-stages)

- [Supported Aggregation Expressions](/docs/manual/core/csfle/reference/supported-operations#std-label-csfle-supported-aggregation-expressions)

The following commands do not require automatic encryption. Drivers configured for automatic Client-Side Field Level Encryption pass these commands directly to the [`mongod`:](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod)

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

Issuing any other [command](/docs/manual/reference/command#std-label-database-commands) through a driver configured for automatic Client-Side Field Level Encryption returns an error.

While automatic Client-Side Field Level Encryption (CSFLE) does not encrypt the [`getMore`](/docs/manual/reference/command/getMore#mongodb-dbcommand-dbcmd.getMore) command, the response to the command may contain encrypted field values.

- Applications configured with the correct CSFLE options automatically decrypt those values.

- Applications without the correct CSFLE options only see the encrypted values.

## Supported Query Operators

Drivers configured for automatic Client-Side Field Level Encryption allow the following query operators when issued against [deterministically encrypted](/docs/manual/core/csfle/fundamentals/encryption-algorithms#std-label-csfle-deterministic-encryption) fields:

- [`$eq`](/docs/manual/reference/operator/query/eq#mongodb-query-op.-eq)

- [`$ne`](/docs/manual/reference/operator/query/ne#mongodb-query-op.-ne)

- [`$in`](/docs/manual/reference/operator/query/in#mongodb-query-op.-in)

- [`$nin`](/docs/manual/reference/operator/query/nin#mongodb-query-op.-nin)

- [`$and`](/docs/manual/reference/operator/query/and#mongodb-query-op.-and)

- [`$or`](/docs/manual/reference/operator/query/or#mongodb-query-op.-or)

- [`$not`](/docs/manual/reference/operator/query/not#mongodb-query-op.-not)

- [`$nor`](/docs/manual/reference/operator/query/nor#mongodb-query-op.-nor)

Queries that compare an encrypted field to `null` or a regular expression always return an error even when using a supported query operator. Queries issuing these operators against a [randomly encrypted](/docs/manual/core/csfle/fundamentals/encryption-algorithms#std-label-csfle-random-encryption) field return an error.

The [`$exists`](/docs/manual/reference/operator/query/exists#mongodb-query-op.-exists) operator has normal behavior when issued against both deterministically and randomly encrypted fields.

Queries specifying any other query operator against an encrypted field return an error.

The following query operators return an error *even if* not issued against an encrypted field:

- [`$text`](/docs/manual/reference/operator/query/text#mongodb-query-op.-text)

- [`$where`](/docs/manual/reference/operator/query/where#mongodb-query-op.-where)

- [`$jsonSchema`](/docs/manual/reference/operator/query/jsonSchema#mongodb-query-op.-jsonSchema)

**Warning: Unexpected Behavior with BinData**

MongoDB stores client-side field level encrypted fields as a [`BinData`](/docs/manual/reference/mongodb-extended-json-v1#mongodb-bsontype-data_binary) blob. Read and write operations issued against the encrypted `BinData` value may have unexpected or incorrect behavior as compared to issuing that same operation against the decrypted value. Certain operations have strict BSON type support where issuing them against a `BinData` value returns an error.

- Drivers using automatic Client-Side Field Level Encryption parse read and write operations for operators or expressions that do not support `BinData` values *or* that have unexpected behavior when issued against `BinData` values.

- Applications using explicit (manual) Client-Side Field Level Encryption *may* use this page as guidance for issuing read and write operations against encrypted fields.

## Unsupported Insert Operations

Drivers configured for automatic Client-Side Field Level Encryption do *not* support insert commands with the following behavior:

- Inserting a document with `Timestamp(0,0)` associated to an encrypted field. The `(0,0)` value indicates that the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) should generate the Timestamp. When the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) cannot generated encrypted fields, the resulting timestamp is unencrypted.

- Inserting a document without an encrypted `_id` *if* the configured automatic schema specifies an encrypted `_id` field. When the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) automatically generates an unencrypted [ObjectId](/docs/manual/reference/bson-types#std-label-objectid), omitting `_id` from documents results in documents that do not conform to the automatic encryption rules.

- Inserting a document with an array associated to a [deterministically encrypted](/docs/manual/core/csfle/fundamentals/encryption-algorithms#std-label-csfle-deterministic-encryption) field. Automatic Client-Side Field Level Encryption does not support deterministically encrypting arrays.

## Supported Update Operators

Drivers configured for automatic Client-Side Field Level Encryption allow the following update operators when issued against [deterministically encrypted](/docs/manual/core/csfle/fundamentals/encryption-algorithms#std-label-csfle-deterministic-encryption) fields:

- [`$set`](/docs/manual/reference/operator/update/set#mongodb-update-up.-set)

- [`$unset`](/docs/manual/reference/operator/update/unset#mongodb-update-up.-unset)

- [`$rename`](/docs/manual/reference/operator/update/rename#mongodb-update-up.-rename)

When you use the [`$rename`](/docs/manual/reference/operator/update/rename#mongodb-update-up.-rename) operator on encrypted fields, the automatic JSON schema must specify the same encryption metadata for the source and target field names.

Updates specifying any other update operator against an encrypted field return an error.

Update operations with the following behavior return an error *even if* using a supported operator:

- The update operation produces an array inside of an encrypted path.

- The update operation uses aggregation expression syntax.

For update operations specifying a [query filter](/docs/manual/reference/command/update#std-label-update-command-q) on deterministically encrypted fields, the query filter must use only [supported operators](/docs/manual/core/csfle/reference/supported-operations#std-label-csfle-supported-query-operators) on those fields.

## Supported Aggregation Stages

Drivers configured for automatic Client-Side Field Level Encryption support the following aggregation pipeline stages:

- [`$addFields`](/docs/manual/reference/operator/aggregation/addFields#mongodb-pipeline-pipe.-addFields)

- [`$bucket`](/docs/manual/reference/operator/aggregation/bucket#mongodb-pipeline-pipe.-bucket)

- [`$bucketAuto`](/docs/manual/reference/operator/aggregation/bucketAuto#mongodb-pipeline-pipe.-bucketAuto)

- [`$collStats`](/docs/manual/reference/operator/aggregation/collStats#mongodb-pipeline-pipe.-collStats)

- [`$count`](/docs/manual/reference/operator/aggregation/count#mongodb-pipeline-pipe.-count)

- [`$geoNear`](/docs/manual/reference/operator/aggregation/geoNear#mongodb-pipeline-pipe.-geoNear)

- [`$graphLookup`](/docs/manual/reference/operator/aggregation/graphLookup#mongodb-pipeline-pipe.-graphLookup) (For usage requirements, see [`$lookup` and `$graphLookup` Behavior)](/docs/manual/core/csfle/reference/supported-operations#std-label-csfle-lookup-graphLookup-behavior)

- [`$group`](/docs/manual/reference/operator/aggregation/group#mongodb-pipeline-pipe.-group) (For usage requirements, see [`$group` Behavior)](/docs/manual/core/csfle/reference/supported-operations#std-label-csfle-group-behavior)

- [`$indexStats`](/docs/manual/reference/operator/aggregation/indexStats#mongodb-pipeline-pipe.-indexStats)

- [`$limit`](/docs/manual/reference/operator/aggregation/limit#mongodb-pipeline-pipe.-limit)

- [`$lookup`](/docs/manual/reference/operator/aggregation/lookup#mongodb-pipeline-pipe.-lookup) (For usage requirements, see [`$lookup` and `$graphLookup` Behavior)](/docs/manual/core/csfle/reference/supported-operations#std-label-csfle-lookup-graphLookup-behavior)

- [`$match`](/docs/manual/reference/operator/aggregation/match#mongodb-pipeline-pipe.-match)

- [`$project`](/docs/manual/reference/operator/aggregation/project#mongodb-pipeline-pipe.-project)

- [`$redact`](/docs/manual/reference/operator/aggregation/redact#mongodb-pipeline-pipe.-redact)

- [`$replaceRoot`](/docs/manual/reference/operator/aggregation/replaceRoot#mongodb-pipeline-pipe.-replaceRoot)

- [`$sample`](/docs/manual/reference/operator/aggregation/sample#mongodb-pipeline-pipe.-sample)

- [`$skip`](/docs/manual/reference/operator/aggregation/skip#mongodb-pipeline-pipe.-skip)

- [`$sort`](/docs/manual/reference/operator/aggregation/sort#mongodb-pipeline-pipe.-sort)

- [`$sortByCount`](/docs/manual/reference/operator/aggregation/sortByCount#mongodb-pipeline-pipe.-sortByCount)

- [`$unwind`](/docs/manual/reference/operator/aggregation/unwind#mongodb-pipeline-pipe.-unwind)

Pipelines operating on collections configured for automatic encryption that specify any other stage return an error.

For each supported pipeline stage, MongoDB tracks fields that *must* be encrypted as they pass through the supported pipelines and marks them for encryption.

Each supported stage must specify only supported [query operators](/docs/manual/core/csfle/reference/supported-operations#std-label-csfle-supported-query-operators) and [aggregation expressions.](/docs/manual/core/csfle/reference/supported-operations#std-label-csfle-supported-aggregation-expressions)

### `$group` Behavior

[`$group`](/docs/manual/reference/operator/aggregation/group#mongodb-pipeline-pipe.-group) has the following behaviors specific to Client-Side Field Level Encryption:

[`$group`](/docs/manual/reference/operator/aggregation/group#mongodb-pipeline-pipe.-group) supports:

- Grouping on deterministically encrypted fields.

- Using [`$addToSet`](/docs/manual/reference/operator/aggregation/addToSet#mongodb-group-grp.-addToSet) and [`$push`](/docs/manual/reference/operator/aggregation/push#mongodb-group-grp.-push) accumulators on encrypted fields.

$group does not support:

- Matching on the array returned by  [`$addToSet`](/docs/manual/reference/operator/aggregation/addToSet#mongodb-group-grp.-addToSet) and [`$push`](/docs/manual/reference/operator/aggregation/push#mongodb-group-grp.-push) accumulators.

- Arithmetic accumulators on encrypted fields.

### `$lookup` and `$graphLookup` Behavior

Starting in MongoDB 8.1, you can reference multiple encrypted collections in a [`$lookup`](/docs/manual/reference/operator/aggregation/lookup#mongodb-pipeline-pipe.-lookup) stage. However, `$lookup` does not support:

- Using an encrypted field as the join field in the `localField` or `foreignField` unless you are performing a self-join operation.

- Using any field in an encrypted array. An array is considered as encrypted if it contains any encrypted elements.

  - For example, you can't use any field within the resulting [as](/docs/manual/reference/operator/aggregation/lookup#std-label-lookup-subquery-as) array of the `$lookup` operation unless you [`$unwind`](/docs/manual/reference/operator/aggregation/unwind#mongodb-pipeline-pipe.-unwind) the `as` field.

Automatic Client-Side Field Level Encryption supports the [`$graphLookup`](/docs/manual/reference/operator/aggregation/graphLookup#mongodb-pipeline-pipe.-graphLookup) stage *only if* the `from` collection matches the collection on which the aggregation runs against (specifically, self-lookup operations). [`$graphLookup`](/docs/manual/reference/operator/aggregation/graphLookup#mongodb-pipeline-pipe.-graphLookup) stages that reference a different `from` collection return an error.

### Supported Aggregation Expressions

Drivers configured for automatic Client-Side Field Level Encryption allow aggregation stages using the following expressions against [deterministically encrypted](/docs/manual/core/csfle/fundamentals/encryption-algorithms#std-label-csfle-deterministic-encryption) fields:

- [`$cond`](/docs/manual/reference/operator/aggregation/cond#mongodb-expression-exp.-cond)

- [`$eq`](/docs/manual/reference/operator/aggregation/eq#mongodb-expression-exp.-eq)

- [`$ifNull`](/docs/manual/reference/operator/aggregation/ifNull#mongodb-expression-exp.-ifNull)

- [`$in`](/docs/manual/reference/operator/aggregation/in#mongodb-expression-exp.-in)

- [`$let`](/docs/manual/reference/operator/aggregation/let#mongodb-expression-exp.-let)

- [`$literal`](/docs/manual/reference/operator/aggregation/literal#mongodb-expression-exp.-literal)

- [`$ne`](/docs/manual/reference/operator/aggregation/ne#mongodb-expression-exp.-ne)

- [`$switch`](/docs/manual/reference/operator/aggregation/switch#mongodb-expression-exp.-switch)

All other aggregation expressions return an error if issued against encrypted fields.

Aggregation stages with the following behavior return an error *even if* using a supported aggregation expression:

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

Drivers configured for automatic Client-Side Field Level Encryption (CSFLE) do *not* support any read or write operation that requires encrypting the following value types:

- [`MaxKey`](/docs/manual/reference/mongodb-extended-json#mongodb-bsontype-MaxKey)

- [`MinKey`](/docs/manual/reference/mongodb-extended-json#mongodb-bsontype-MinKey)

- `null`

- `undefined`

Encryption does not adequately hide the type information for these values.

CSFLE does not support automatic encryption on fields within an array of documents.

Automatic CSFLE *also* does not support read or write operations on a deterministically encrypted field where the operation compares the encrypted field to the following value types:

- `array`

- `bool`

- `decimal128`

- `double`

- `object`
