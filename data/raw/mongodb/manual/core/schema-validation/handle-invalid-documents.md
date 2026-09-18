> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Choose How to Handle Invalid Documents

You can specify how MongoDB handles documents that violate validation rules. When an operation would result in an invalid document, MongoDB can either:

- Reject any insert or update that violates the validation criteria. This is the default behavior.

- Allow the operation to proceed, but record the violation in the MongoDB log.

Rejecting invalid documents ensures that your schema stays consistent. However, in certain scenarios you may want to allow invalid documents, such as a data migration containing documents from before a schema was established.

## Context

Your schema's `validationAction` option determines how MongoDB handles invalid documents:

| Validation Action | Behavior |
| --- | --- |
| `error` | (*Default*) MongoDB rejects any insert or update that violates the validation criteria. |
| `warn` | MongoDB allows the operation to proceed, but records the violation in the MongoDB log. |
| `errorAndLog` | MongoDB rejects any insert or update that violates validation criteria and logs the error to the `mongod` log file. **New in version 8.1** |

**Note:**

If you use an `errorAndLog` validation action on a collection, MongoDB cannot downgrade until you drop the collection, or if you change the validation action for the collection to one supported in older versions. To change the validation action on a collection, use the [`collMod`](/docs/manual/reference/command/collMod#mongodb-dbcommand-dbcmd.collMod) command.

## Option 1: Reject Invalid Documents

The following procedure shows how to create a schema validation that rejects invalid documents.

1. Create a collection with `validationAction: "error"`.

   Create a `contacts` collection with a JSON schema validator that has `validationAction: "error"`:

   ```javascript
   db.createCollection( "contacts", {
      validator: { $jsonSchema: {
         bsonType: "object",
         required: [ "phone" ],
         properties: {
            phone: {
               bsonType: "string",
               description: "must be a string and is required"
            },
            email: {
               bsonType : "string",
               pattern : "@mongodb\\.com$",
               description: "must be a string and end with '@mongodb.com'"
            }
         }
      } },
      validationAction: "error"
   } )
   ```

   The `error` `validationAction` causes MongoDB to reject any invalid documents and prevent them from being inserted into the collection.

2. Attempt to insert an invalid document.

   Attempt to insert the following document:

   ```javascript
   db.contacts.insertOne(
      { name: "Amanda", email: "amanda@xyz.com" }
   )
   ```

   The document violates the validation rule because:

   - The `email` field does not match the regular expression pattern. The `email` field must end in `@mongodb.com`.

   - It is missing the required `phone` field.

   The operation fails with the following error:

   ```javascript
   MongoServerError: Document failed validation
   Additional information: {
     failingDocumentId: ObjectId("6377cca4aac957f2b77ea955"),
     details: {
       operatorName: '$jsonSchema',
       schemaRulesNotSatisfied: [
         {
           operatorName: 'properties',
           propertiesNotSatisfied: [
             {
               propertyName: 'email',
               description: "must be a string and end with '@mongodb.com'",
               details: [
                 {
                   operatorName: 'pattern',
                   specifiedAs: { pattern: '@mongodb\\.com$' },
                   reason: 'regular expression did not match',
                   consideredValue: 'amanda@xyz.com'
                 }
               ]
             }
           ]
         },
         {
           operatorName: 'required',
           specifiedAs: { required: [ 'phone' ] },
           missingProperties: [ 'phone' ]
         }
       ]
     }
   }
   ```

## Option 2: Allow Invalid Documents, but Record Them in the Log

The following procedure shows how to create a schema validation that allows invalid documents, but records invalid documents in the MongoDB log.

1. Create a collection with `validationAction: "warn"`.

   Create a `contacts2` collection with a JSON schema validator that has `validationAction: "warn"`:

   ```javascript
   db.createCollection( "contacts2", {
      validator: { $jsonSchema: {
         bsonType: "object",
         required: [ "phone" ],
         properties: {
            phone: {
               bsonType: "string",
               description: "must be a string and is required"
            },
            email: {
               bsonType : "string",
               pattern : "@mongodb\\.com$",
               description: "must be a string and end with '@mongodb.com'"
            }
         }
      } },
      validationAction: "warn"
   } )
   ```

   The `warn` `validationAction` allows invalid documents to be inserted into the collection. Invalid documents are recorded in the MongoDB log.

2. Attempt to insert an invalid document.

   Attempt to insert the following document:

   ```javascript
   db.contacts2.insertOne(
      { name: "Amanda", email: "amanda@xyz.com" }
   )
   ```

   The document violates the validation rule because:

   - The `email` field does not match the regular expression pattern. The `email` field must end in `@mongodb.com`.

   - It is missing the required `phone` field.

3. Check the logs for the invalid document.

   To view the MongoDB logs in a readable format, run the following command:

   ```javascript
   db.adminCommand(
      { getLog:'global'} ).log.forEach(x => { print(x) }
   )
   ```

   The MongoDB log includes an entry similar to the following object:

   ```bash
   {
      "t": {
         "$date": "2022-11-18T13:30:43.607-05:00"
      },
      "s": "W",
      "c": "STORAGE",
      "id": 20294,
      "ctx": "conn2",
      "msg": "Document would fail validation",
      "attr": {
         "namespace": "test.contacts2",
         "document": {
            "_id": {
               "$oid": "6377cf53d59841355cac1cd0"
            },
            "name": "Amanda",
            "email": "amanda@xyz.com"
         },
         "errInfo": {
            "failingDocumentId": {
               "$oid": "6377cf53d59841355cac1cd0"
            },
            "details": {
               "operatorName": "$jsonSchema",
               "schemaRulesNotSatisfied": [{
                  "operatorName": "properties",
                  "propertiesNotSatisfied": [{
                     "propertyName": "email",
                     "description": "must be a string and end with '@mongodb.com'",
                     "details": [{
                        "operatorName": "pattern",
                        "specifiedAs": {
                           "pattern": "@mongodb\\.com$"
                        },
                        "reason": "regular expression did not match",
                        "consideredValue": "amanda@xyz.com"
                     }]
                  }]
               }, {
                  "operatorName": "required",
                  "specifiedAs": {
                     "required": ["phone"]
                  },
                  "missingProperties": ["phone"]
               }]
            }
         }
      }
   }
   ```

## Learn More

- [Log Messages](/docs/manual/reference/log-messages#std-label-log-messages-ref)

- [Specify Validation Level for Existing Documents](/docs/manual/core/schema-validation/specify-validation-level#std-label-schema-specify-validation-level)
