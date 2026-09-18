> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Bypass Schema Validation

In some situations, you may need to bypass a collection's schema validation rules. For example, if you are restoring potentially invalid data from a backup to a collection that has validation rules. In this scenario, older documents may not meet new validation requirements.

## Context

Bypassing schema validation is done on a per-operation basis. If you bypass schema validation to insert an invalid document, any future updates to the invalid document must either:

- Also bypass schema validation

- Result in a valid document

## Supported Operations

You can use the following commands and methods to bypass validation on a per-operation basis:

- [`applyOps`](/docs/manual/reference/command/applyOps#mongodb-dbcommand-dbcmd.applyOps) command

- [`findAndModify`](/docs/manual/reference/command/findAndModify#mongodb-dbcommand-dbcmd.findAndModify) command and [`db.collection.findAndModify()`](/docs/manual/reference/method/db.collection.findAndModify#mongodb-method-db.collection.findAndModify) method

- [`mapReduce`](/docs/manual/reference/command/mapReduce#mongodb-dbcommand-dbcmd.mapReduce) command and [`db.collection.mapReduce()`](/docs/manual/reference/method/db.collection.mapReduce#mongodb-method-db.collection.mapReduce) method

- [`insert`](/docs/manual/reference/command/insert#mongodb-dbcommand-dbcmd.insert) command

- [`update`](/docs/manual/reference/command/update#mongodb-dbcommand-dbcmd.update) command

- [`$out`](/docs/manual/reference/operator/aggregation/out#mongodb-pipeline-pipe.-out) and [`$merge`](/docs/manual/reference/operator/aggregation/merge#mongodb-pipeline-pipe.-merge) stages for the [`aggregate`](/docs/manual/reference/command/aggregate#mongodb-dbcommand-dbcmd.aggregate) command and [`db.collection.aggregate()`](/docs/manual/reference/method/db.collection.aggregate#mongodb-method-db.collection.aggregate) method

## Prerequisite

For deployments that have enabled access control, to bypass document validation, the authenticated user must have [`bypassDocumentValidation`](/docs/manual/reference/privilege-actions#mongodb-authaction-bypassDocumentValidation) action. The built-in roles [`dbAdmin`](/docs/manual/reference/built-in-roles#mongodb-authrole-dbAdmin) and [`restore`](/docs/manual/reference/built-in-roles#mongodb-authrole-restore) provide this action.

## Steps

The following example creates a collection with schema validation, and then inserts an invalid document by bypassing the validation rules.

1. Create a collection with validation rules

   Create a `students` collection and use the [`$jsonSchema`](/docs/manual/reference/operator/query/jsonSchema#mongodb-query-op.-jsonSchema) operator to set schema validation rules:

   ```javascript
   db.createCollection("students", {
      validator: {
         $jsonSchema: {
            bsonType: "object",
            required: [ "name", "year", "major", "address" ],
            properties: {
               name: {
                  bsonType: "string",
                  description: "must be a string and is required"
               },
               year: {
                  bsonType: "int",
                  minimum: 2017,
                  maximum: 3017,
                  description: "must be an integer in [ 2017, 3017 ] and is required"
               }
            }
         }
      }
   } )
   ```

2. Bypass the validation to insert an invalid document

   The following document is invalid because the `year` field is outside of the allowed bounds (`2017`-`3017`):

   ```javascript
   {
      name: "Alice",
      year: Int32( 2016 ),
      major: "History",
      gpa: Double(3.0),
      address: {
         city: "NYC",
         street: "33rd Street"
      }
   }
   ```

   To bypass the validation rules and insert the invalid document, run the following `insert` command, which sets the `bypassDocumentValidation` option to `true`:

   ```javascript
   db.runCommand( {
      insert: "students",
      documents: [
         {
            name: "Alice",
            year: Int32( 2016 ),
            major: "History",
            gpa: Double(3.0),
            address: {
               city: "NYC",
               street: "33rd Street"
            }
         }
      ],
      bypassDocumentValidation: true
   } )
   ```

## Results

To confirm that the document was successfully inserted, query the `students` collection:

```javascript
db.students.find()
```

MongoDB returns the inserted document:

```javascript
[
   {
      _id: ObjectId("62bcb4db3f7991ea4fc6830e"),
      name: 'Alice',
      year: 2016,
      major: 'History',
      gpa: 3,
      address: { city: 'NYC', street: '33rd Street' }
   }
]
```

## Learn More

- [Query for and Modify Valid or Invalid Documents](/docs/manual/core/schema-validation/use-json-schema-query-conditions#std-label-use-json-schema-query-conditions)

- [Specify Validation Level for Existing Documents](/docs/manual/core/schema-validation/specify-validation-level#std-label-schema-specify-validation-level)
