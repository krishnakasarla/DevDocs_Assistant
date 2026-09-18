> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Specify Allowed Field Values

When you create a [JSON Schema](/docs/manual/core/schema-validation/specify-json-schema#std-label-schema-validation-json), you can specify what values are allowed in a particular field. Use this functionality to ensure that your field values belong to an expected set of values, such as a list of countries. Similarly, you can use this functionality to prevent human error, such as typos, when inserting data into a collection.

## Context

To specify a list of allowed values, use the `enum` keyword in your JSON schema. The `enum` keyword means "enumerate", and is used to list possible values of a field.

## Steps

Consider a clothing company that only ships products to France, the United Kingdom, and the United States. In the validator, you can list the allowed country values and reject documents that specify a different country.

1. Create a collection with validation containing `enum`.

   Create a `shipping` collection and use the [`$jsonSchema`](/docs/manual/reference/operator/query/jsonSchema#mongodb-query-op.-jsonSchema) operator to set schema validation rules:

   ```javascript
   db.createCollection("shipping", {
      validator: {
         $jsonSchema: {
            bsonType: "object",
            title: "Shipping Country Validation",
            properties: {
               country: {
                  enum: [ "France", "United Kingdom", "United States" ],
                  description: "Must be either France, United Kingdom, or United States"
               }
            }
         }
      }
   } )
   ```

   The `enum` field in the `country` object only allows documents where the `country` field is either `France`, `United
           Kingdom`, or `United States`.

2. Confirm that the validation prevents invalid documents.

   The following insert operation fails because `country` is `Germany`, which isn't in the list of allowed values.

   ```javascript
   db.shipping.insertOne( {
      item: "sweater",
      size: "medium",
      country: "Germany"
   } )
   ```

   The operation returns this error:

   ```javascript
   MongoServerError: Document failed validation
   Additional information: {
     failingDocumentId: ObjectId("630d1057931191850b40d0aa"),
     details: {
       operatorName: '$jsonSchema',
       title: 'Shipping Country Validation',
       schemaRulesNotSatisfied: [
         {
           operatorName: 'properties',
           propertiesNotSatisfied: [
             {
               propertyName: 'country',
               description: 'Must be either France, United Kingdom, or United States',
               details: [
                 {
                   operatorName: 'enum',
                   specifiedAs: {
                     enum: [ 'France', 'United Kingdom', 'United States' ]
                   },
                   reason: 'value was not found in enum',
                   consideredValue: 'Germany'
                 }
               ]
             }
           ]
         }
       ]
     }
   }
   ```

3. Insert a valid document.

   The insert succeeds after you change the `country` field to one of the allowed values:

   ```javascript
   db.shipping.insertOne( {
      item: "sweater",
      size: "medium",
      country: "France"
   } )
   ```

4. Query for the valid document.

   To confirm that the document was successfully inserted, query the `shipping` collection:

   ```javascript
   db.shipping.find()
   ```

   MongoDB returns the document:

   ```javascript
   [
     {
       _id: ObjectId("630d10d5931191850b40d0ab"),
       item: 'sweater',
       size: 'medium',
       country: 'France'
     }
   ]
   ```
