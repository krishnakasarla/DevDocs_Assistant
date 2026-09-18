> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Field Names with Periods

This section summarizes how to insert, query, and update documents with field names that contain a period. MongoDB discourages the use of field names that contain a period because some features aren't supported with these fields. See [General Restrictions](/docs/manual/core/dot-dollar-considerations#std-label-dot-dollar-general-restrictions) for more information.

**Note:**

Limit the number of words separated by periods in field names to less than 255. If you attempt to use more, MongoDB returns an error.

## Insert a Field Name with a Period

To insert a document that contains a field name with a period, put the field name in quotes.

The following command inserts a document that contains a field name `price.usd`:

```javascript
db.inventory.insertOne(
   {
      "item" : "sweatshirt",
      "price.usd": 45.99,
      "quantity": 20
   }
)
```

## Query a Field that has a Period

To query for a field that has a period, use the [`$getField`](/docs/manual/reference/operator/aggregation/getField#mongodb-expression-exp.-getField) operator.

The following query returns documents where the `price.usd` field is greater than `40`:

```javascript
db.inventory.find(
   {
      $expr:
         {
            $gt: [ { $getField: "price.usd" }, 40 ]
         }
   }
)
```

**Output:**

```javascript
[
   {
      _id: ObjectId("66145f9bcb1d4abffd2f1b50"),
      item: 'sweatshirt',
      'price.usd': 45.99,
      quantity: 20
   }
]
```

If you don't use `$getField`, MongoDB treats the field name with a period as an embedded object. For example, the following query matches documents where a `usd` field inside of a `price` field is greater than `40`:

```javascript
db.inventory.find( {
   "price.usd": { $gt: 40 }
} )
```

The preceding query would match this document:

```javascript
{
   "item" : "sweatshirt",
   "price": {
      "usd": 45.99
   },
   "quantity": 20
}
```

## Update a Field that has a Period

To update a field that has a period, use an aggregation pipeline with the [`$setField`](/docs/manual/reference/operator/aggregation/setField#mongodb-expression-exp.-setField) operator.

The following operation sets the `price.usd` field to `29.99`:

```javascript
db.inventory.updateOne(
   { "item": "sweatshirt" },
   [
      {
         $replaceWith: {
            $setField: {
               field: "price.usd",
               input: "$$ROOT",
               value: 29.99
            }
         }
      }
   ]
)
```

If you don't use `$setField`, MongoDB treats the field name with a period as an embedded object. For example, the following operation does not update the existing `price.usd` field, and instead inserts a new field `usd`, embedded inside of a `price` field:

```javascript
db.inventory.updateOne(
   { "item": "sweatshirt" },
   { $set: { "price.usd": 29.99 } }
)
```

Resulting document:

```javascript
[
   {
      _id: ObjectId("66145f9bcb1d4abffd2f1b50"),
      item: 'sweatshirt',
      'price.usd': 45.99
      quantity: 20,
      price: { usd: 29.99 }
   }
]
```

For more examples of updates with aggregation pipelines, see [Updates with Aggregation Pipeline.](/docs/manual/tutorial/update-documents-with-aggregation-pipeline#std-label-updates-agg-pipeline)

## Learn More

- [`$getField`](/docs/manual/reference/operator/aggregation/getField#mongodb-expression-exp.-getField)

- [`$setField`](/docs/manual/reference/operator/aggregation/setField#mongodb-expression-exp.-setField)

- [`$literal`](/docs/manual/reference/operator/aggregation/literal#mongodb-expression-exp.-literal)

- [Dollar-Prefixed Field Names](/docs/manual/core/dot-dollar-considerations/dollar-prefix#std-label-dollar-prefix-field-names)
