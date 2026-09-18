> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Dollar-Prefixed Field Names

This section summarizes how different insert and update operations handle dollar (`$`) prefixed field names. MongoDB discourages the use of dollar prefixed field names because some features aren't supported with these fields. See [General Restrictions](/docs/manual/core/dot-dollar-considerations#std-label-dot-dollar-general-restrictions) for more information.

## Insert Operations

Dollar (`$`) prefixed fields are permitted as top level and nested field names for inserts.

```javascript
db.sales.insertOne( {
   "$price": 50.00,
   "quantity": 30
} )
```

Dollar (`$`) prefixed fields are permitted on inserts using otherwise reserved words. Operator names like [`$inc`](/docs/manual/reference/operator/update/inc#mongodb-update-up.-inc) can be used as field names as well as words like `id`, `db`, and `ref`.

```javascript
db.books.insertOne( {
   "$id": "h1961-01",
   "location": {
      "$db": "novels",
      "$ref": "2007042768",
      "$inc": true
} } )
```

An update which creates a new document during an [upsert](/docs/manual/reference/glossary#std-term-upsert) is treated as an `insert` rather than an `update` for field name validation. [Upserts](/docs/manual/reference/glossary#std-term-upsert) can accept dollar (`$`) prefixed fields. However, [upserts](/docs/manual/reference/glossary#std-term-upsert) are a special case and similar update operations may cause an error if the `match` portion of the update selects an existing document.

This code sample has `upsert: true` so it will insert a new document if the collection doesn't already contain a document that matches the query term, `{ "date": "2021-07-07" }`. If this sample code matches an existing document, the update will fail since `$hotel` is dollar (`$`) prefixed.

```javascript
db.expenses.updateOne(
   { "date": "2021-07-07" },
   { $set: {
      "phone": 25.17,
      "$hotel": 320.10
   } },
   { upsert: true }
)
```

## Document Replacing Updates

Update operators either replace existing fields with new documents or else modify those fields. In cases where the update performs a replacement, dollar (`$`) prefixed fields are not permitted as top level field names.

Consider a document like

```javascript::
{
   "_id": "E123",
   "address": {
      "$number": 123,
      "$street": "Elm Road"
   },
   "$rooms": {
      "br": 2,
      "bath": 1
   }
}
```

You could use an update operator that replaces an existing document to modify the `address.$street` field but you could not update the `$rooms` field that way.

```text
db.housing.updateOne(
   { "_id": "E123" },
   { $set: { "address.$street": "Elm Ave" } }
)
```

Use [`$setField`](/docs/manual/reference/operator/aggregation/setField#mongodb-expression-exp.-setField) as part of an aggregation pipeline to [update top level](/docs/manual/core/dot-dollar-considerations/dollar-prefix#std-label-dotDollar-aggregate-update) dollar (`$`) prefixed fields like `$rooms`.

## Document Modifying Updates

When an update modifies, rather than replaces, existing document fields, dollar (`$`) prefixed fields can be top level field names. Subfields can be accessed directly, but you need a helper method to access the top level fields.

**See also:**

[`$getField`](/docs/manual/reference/operator/aggregation/getField#mongodb-expression-exp.-getField), [`$setField`](/docs/manual/reference/operator/aggregation/setField#mongodb-expression-exp.-setField), [`$literal`](/docs/manual/reference/operator/aggregation/literal#mongodb-expression-exp.-literal), [`$replaceWith`](/docs/manual/reference/operator/aggregation/replaceWith#mongodb-pipeline-pipe.-replaceWith)

Consider a collection with documents like this inventory record:

```text
{
   _id: ObjectId("610023ad7d58ecda39b8d161"),
   "part": "AB305",
   "$bin": 200,
   "quantity": 100,
   "pricing": { sale: true, "$discount": 60 }
}
```

The `pricing.$discount` subfield can be queried directly.

```text
db.inventory.findAndModify( {
    query: { "part": { $eq: "AB305" } },
    update: { $inc: { "pricing.$discount": 10 } }
} )
```

Use [`$getField`](/docs/manual/reference/operator/aggregation/getField#mongodb-expression-exp.-getField) and [`$literal`](/docs/manual/reference/operator/aggregation/literal#mongodb-expression-exp.-literal) to access the value of the top level `$bin` field.

```text
db.inventory.findAndModify( {
   query: { $expr: {
      $eq: [ { $getField: { $literal: "$bin" } }, 200 ]
   } },
   update: { $inc: { "quantity": 10 } }
} )
```

## Updates Using Aggregation Pipelines

Use [`$setField`](/docs/manual/reference/operator/aggregation/setField#mongodb-expression-exp.-setField), [`$getField`](/docs/manual/reference/operator/aggregation/getField#mongodb-expression-exp.-getField), and [`$literal`](/docs/manual/reference/operator/aggregation/literal#mongodb-expression-exp.-literal) in the [`$replaceWith`](/docs/manual/reference/operator/aggregation/replaceWith#mongodb-pipeline-pipe.-replaceWith) stage to modify dollar (`$`) prefixed fields in an aggregation [pipeline.](/docs/manual/reference/glossary#std-term-pipeline)

Consider a collection of school records like:

```javascript
db.school.insertOne (
{
   "_id": 100001,
   "$term": "fall",
   "registered": true,
   "grade": 4
} )
```

Create a new collection for the spring semester using a [pipeline](/docs/manual/reference/glossary#std-term-pipeline) to update the dollar (`$`) prefixed `$term` field.

```javascript
db.school.aggregate( [
   { $match: { "registered": true } },
   { $replaceWith: {
      $setField: {
         field: { $literal: "$term" },
         input: "$$ROOT",
         value: "spring"
   } } },
   { $out: "spring2022" }
] )
```
