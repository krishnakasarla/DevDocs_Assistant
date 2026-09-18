> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Specify Validation With Query Operators

You can specify validation using query operators such as [`$eq`](/docs/manual/reference/operator/query/eq#mongodb-query-op.-eq) and [`$gt`](/docs/manual/reference/operator/query/gt#mongodb-query-op.-gt) to compare fields.

A common use case for schema validation with query operators is when you want to create dynamic validation rules that compare multiple field values at runtime. For example, if you have a field that depends on the value of another field and need to ensure that those values are correctly proportional to each other.

## Restrictions

- You can't specify the following [query operators](/docs/manual/reference/mql/query-predicates#std-label-query-selectors) in a `validator` object:

  - [`$expr`](/docs/manual/reference/operator/query/expr#mongodb-query-op.-expr) with [`$function`](/docs/manual/reference/operator/aggregation/function#mongodb-expression-exp.-function) expressions

  - [`$near`](/docs/manual/reference/operator/query/near#mongodb-query-op.-near)

  - [`$nearSphere`](/docs/manual/reference/operator/query/nearSphere#mongodb-query-op.-nearSphere)

  - [`$text`](/docs/manual/reference/operator/query/text#mongodb-query-op.-text)

  - [`$where`](/docs/manual/reference/operator/query/where#mongodb-query-op.-where)

- You can't specify schema validation for:

  - Collections in the `admin`, `local`, and `config` databases

  - [System collections](/docs/manual/reference/system-collections#std-label-metadata-system-collections)

## Context

Consider an application that tracks customer orders. The orders have a base price and a VAT (Value Added Tax). The `orders` collection contains these fields to track total price:

- `price`

- `VAT`

- `totalWithVAT`

## Steps

The following procedure creates a schema validation with query operators to ensure that `totalWithVAT` matches the expected combination of `price` and `VAT`.

1. Create a collection with validation.

   Create an `orders` collection with schema validation:

   ```javascript
   db.createCollection( "orders",
      {
         validator: {
            $expr:
               {
                  $eq: [
                     "$totalWithVAT",
                     { $multiply: [ "$total", { $sum:[ 1, "$VAT" ] } ] }
                  ]
               }
         }
      }
   )
   ```

   With this validation, you can only insert documents if the `totalWithVAT` field equals `total * (1 + VAT)`.

2. Confirm that the validation prevents invalid documents.

   The following operation fails because the `totalWithVAT` field does not equal the correct value:

   ```javascript
   db.orders.insertOne( {
      total: Decimal128("141"),
      VAT: Decimal128("0.20"),
      totalWithVAT: Decimal128("169")
   } )
   ```

   141 \* (1 + 0.20) equals 169.2, so the value of the `totalWithVAT` field must be 169.2.

   The operation returns this error:

   ```javascript
   MongoServerError: Document failed validation
   Additional information: {
     failingDocumentId: ObjectId("62bcc9b073c105dde9231293"),
     details: {
       operatorName: '$expr',
       specifiedAs: {
         '$expr': {
           '$eq': [
             '$totalWithVAT',
             {
               '$multiply': [ '$total', { '$sum': [ 1, '$VAT' ] } ]
             }
           ]
         }
       },
       reason: 'expression did not match',
       expressionResult: false
     }
   }
   ```

3. Make the document valid and insert it.

   After updating the document to have the correct `totalWithVAT` value, the operation succeeds:

   ```javascript
   db.orders.insertOne( {
      total: Decimal128("141"),
      VAT: Decimal128("0.20"),
      totalWithVAT: Decimal128("169.2")
   } )
   ```

   MongoDB returns the following output, indicating that the insert was successful:

   ```javascript
   {
     acknowledged: true,
     insertedId: ObjectId("6304f4651e52f124b84479ba")
   }
   ```

## Additional Information

You can combine query operator validation with [JSON Schema validation.](/docs/manual/core/schema-validation/specify-json-schema#std-label-schema-validation-json)

For example, consider a `sales` collection with this schema validation:

```javascript
 db.createCollection("sales", {
   validator: {
     "$and": [
       // Validation with query operators
       {
         "$expr": {
           "$lt": ["$lineItems.discountedPrice", "$lineItems.price"]
         }
       },
       // Validation with JSON Schema
       {
         "$jsonSchema": {
           "properties": {
             "items": { "bsonType": "array" }
           }
          }
        }
      ]
    }
  }
)
```

The preceding validation enforces these rules for documents in the `sales` collection:

- `lineItems.discountedPrice` must be less than `lineItems.price`. This rule uses the [`$lt`](/docs/manual/reference/operator/aggregation/lt#mongodb-expression-exp.-lt) operator.

- The `items` field must be an array. This rule uses [`$jsonSchema`.](/docs/manual/reference/operator/query/jsonSchema#mongodb-query-op.-jsonSchema)

## Learn More

- To see all query operators available in MongoDB, see [Query Predicates.](/docs/manual/reference/mql/query-predicates#std-label-query-selectors)

- To learn more about the `$expr` operator, which allows the use of aggregation expressions within the query language, see [`$expr`.](/docs/manual/reference/operator/query/expr#mongodb-query-op.-expr)
