> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Schema Validation

Schema validation lets you create validation rules for your fields, such as allowed data types and value ranges.

MongoDB uses a flexible schema model. By default, documents in a collection don't need the same fields or data types. After you establish an application schema, use schema validation to prevent unintended schema changes and data type errors.

You can [implement schema validation in the UI](https://www.mongodb.com/docs/atlas/performance-advisor/schema-suggestions/) for deployments hosted in [MongoDB Atlas.](https://www.mongodb.com/docs/atlas)

## When to Use Schema Validation

Your schema validation needs depend on how your application organizes data. Schema validation is most useful for an established application with a defined data structure.

**Note:**

Schema validation rules are also flexible, so they don't need to cover every field in a document, unless your application requires that they do.

You can use schema validation in the following scenarios:

- For an `events` collection, ensure that the `start_date` field stores only a date, not a string. Consistent types prevent unexpected values in connecting applications.

- For a `store` collection, ensure that the `accepted_credit_cards` field contains only accepted card types, such as `["Visa", "MasterCard", "American Express"]`. This rule prevents users from entering unsupported values.

- For a `students` collection, ensure that the `gpa` field is always a positive floating-point number. This rule prevents data entry errors.

## When MongoDB Checks Validation

After you add schema validation rules to a collection:

- All document inserts must match the rules.

- The validation level determines how rules apply to existing documents and updates. To learn more, see [Specify Validation Level for Existing Documents.](/docs/manual/core/schema-validation/specify-validation-level#std-label-schema-specify-validation-level)

To find documents in a collection that don't match the schema validation rules, see [Find Documents that Don't Match the Schema.](/docs/manual/core/schema-validation/use-json-schema-query-conditions#std-label-use-json-schema-query-conditions-find-documents)

## What Happens When a Document Fails Validation

By default, MongoDB rejects any insert or update operation that would produce an invalid document.

Alternatively, you can configure MongoDB to allow invalid documents and log a warning when a schema violation occurs.

To learn more, see [Choose How to Handle Invalid Documents.](/docs/manual/core/schema-validation/handle-invalid-documents#std-label-schema-validation-handle-invalid-docs)

## Get Started

For schema validation tasks, see the following pages:

- [Specify JSON Schema Validation](/docs/manual/core/schema-validation/specify-json-schema#std-label-schema-validation-json)

- [Specify Validation for Polymorphic Collections](/docs/manual/core/schema-validation/specify-validation-polymorphic-collections#std-label-schema-validation-polymorphic-collections)

- [Specify Validation With Query Operators](/docs/manual/core/schema-validation/specify-query-expression-rules#std-label-schema-validation-query-expression)

- [Specify Allowed Field Values](/docs/manual/core/schema-validation/specify-json-schema/specify-allowed-field-values#std-label-schema-allowed-field-values)

- [View Existing Validation Rules](/docs/manual/core/schema-validation/view-existing-validation-rules#std-label-schema-view-validation-rules)

- [Modify Schema Validation](/docs/manual/core/schema-validation/update-schema-validation#std-label-schema-update-validation)

- [Query for and Modify Valid or Invalid Documents](/docs/manual/core/schema-validation/use-json-schema-query-conditions#std-label-use-json-schema-query-conditions)

- [Bypass Schema Validation](/docs/manual/core/schema-validation/bypass-document-validation#std-label-schema-bypass-document-validation)

## Learn More

To learn about MongoDB's flexible schema model, see [Data Modeling in MongoDB.](/docs/manual/data-modeling#std-label-manual-data-modeling-intro)
