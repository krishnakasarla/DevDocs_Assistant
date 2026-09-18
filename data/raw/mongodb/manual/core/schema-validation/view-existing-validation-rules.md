> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# View Existing Validation Rules

You can view a collection's validation rules to determine what restrictions are imposed on documents and how MongoDB handles invalid documents when they occur.

To view a collection's validation rules, use the [`db.getCollectionInfos()`](/docs/manual/reference/method/db.getCollectionInfos#mongodb-method-db.getCollectionInfos) method or [`listCollections`](/docs/manual/reference/command/listCollections#mongodb-dbcommand-dbcmd.listCollections) database command.

Both commands return the same information, but the output format differs between each command.

## Prerequisite

To run the examples on this page, create a `students` collection with validation rules. For more information, see [Specify JSON Schema Validation.](/docs/manual/core/schema-validation/specify-json-schema#std-label-schema-validation-json)

## Example: `db.getCollectionInfos()` Syntax

The following command uses [`db.getCollectionInfos()`](/docs/manual/reference/method/db.getCollectionInfos#mongodb-method-db.getCollectionInfos) to return the validation rules for the `students` collection:

```javascript
db.getCollectionInfos( { name: "students" } )[0].options.validator
```

The output resembles the following validation object:

```javascript
{
  '$jsonSchema': {
    bsonType: 'object',
    required: [ 'name', 'year', 'major', 'address' ],
    properties: {
      name: {
        bsonType: 'string',
        description: 'must be a string and is required'
      },
      year: {
        bsonType: 'int',
        minimum: 2017,
        maximum: 3017,
        description: 'must be an integer in [ 2017, 3017 ] and is required'
      },
      gpa: {
        bsonType: [ 'double' ],
        description: 'must be a double if the field exists'
      }
    }
  }
}
```

**Note: Validation Action and Level Not Included by Default**

If `validationAction` and `validationLevel` are not explicitly set, [`db.getCollectionInfos()`](/docs/manual/reference/method/db.getCollectionInfos#mongodb-method-db.getCollectionInfos) does not include those fields in its output.

## Example: `listCollections` Syntax

The following command uses [`listCollections`](/docs/manual/reference/command/listCollections#mongodb-dbcommand-dbcmd.listCollections) to return the validation rules for the `students` collection:

```javascript
db.runCommand ( { listCollections: 1, filter: { name: "students" } } )
```

The output resembles the following object:

```javascript
{
  cursor: {
    id: Long("0"),
    ns: 'test.$cmd.listCollections',
    firstBatch: [
      {
        name: 'students',
        type: 'collection',
        options: {
          validator: {
            '$jsonSchema': {
              bsonType: 'object',
              required: [ 'name', 'year', 'major', 'address' ],
              properties: {
                name: {
                  bsonType: 'string',
                  description: 'must be a string and is required'
                },
                gpa: {
                  bsonType: [ 'double' ],
                  description: 'must be a double if the field exists'
                }
              }
            },
            validationAction: 'warn'
          }
        },
        info: {
          readOnly: false,
          uuid: UUID("bf560865-5879-4ec1-b389-f77a03abbc5a")
        },
        idIndex: { v: 2, key: { _id: 1 }, name: '_id_' }
      }
    ]
  },
  ok: 1
}
```

## Learn More

- [Query for and Modify Valid or Invalid Documents](/docs/manual/core/schema-validation/use-json-schema-query-conditions#std-label-use-json-schema-query-conditions)

- [Choose How to Handle Invalid Documents](/docs/manual/core/schema-validation/handle-invalid-documents#std-label-schema-validation-handle-invalid-docs)
