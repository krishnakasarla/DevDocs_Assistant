> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Encrypted Fields and Enabled Queries

Queryable Encryption equality and range queries are fully supported in production. Prefix, suffix, and substring queries are only available in public preview in MongoDB 8.2. Do not enable these query types in production. GA functionality of prefix, suffix and substring query types will be incompatible with the preview feature. To learn more, see [Supported Query Types](https://www.mongodb.com/docs/manual/core/queryable-encryption/reference/supported-operations/).

When you use Queryable Encryption, you define encrypted fields at the collection level using an encryption schema. Encrypting a field and enabling queries increases storage requirements and impacts query performance. You can configure an encrypted field for either equality or range queries, but not both. Configure fields for the expected query type.

For instructions on creating an encryption schema and configuring querying, see [Create an Encryption Schema.](/docs/manual/core/queryable-encryption/qe-create-encryption-schema#std-label-qe-create-encryption-schema)

## Supported Query Types and Behavior

For a list of supported query operators and behavior with encrypted fields, see [Supported Query Types & Operators.](/docs/manual/core/queryable-encryption/reference/supported-operations#std-label-qe-supported-query-operators)

## Schema Validation

Queryable Encryption requires a server-side encryption schema to enforce encryption of specific fields in a collection. Clients using automatic Queryable Encryption behave differently depending on the database connection configuration:

- At minimum, local rules must encrypt the same fields as the remote schema on the server.

- If the connection `encryptedFieldsMap` object contains a key for the specified collection, the client uses that object to perform automatic Queryable Encryption, rather than using the remote schema.

- If the connection `encryptedFieldsMap` object doesn't contain a key for the specified collection, the client downloads the remote schema for the collection and uses it instead.

  **Important: Remote Schema Behavior**

  When using a remote schema:

  - The client trusts that the server has a valid schema

  - The client uses the remote schema to perform automatic Queryable Encryption only. The client does not enforce any other validation rules specified in the schema.

## Considerations when Enabling Querying

Decide which fields should be encrypted and/or queryable prior to creating your collection. Changing which fields are encrypted or queryable requires rebuilding the collection's encryption schema and re-creating the collection.

If you don't need to query an encrypted field, you may not need to enable querying on that field. You can still retrieve the document by querying other fields that are queryable or unencrypted.

For every encrypted collection, MongoDB creates [two metadata collections](/docs/manual/core/queryable-encryption/fundamentals/manage-collections#std-label-qe-metadata-collections), increasing storage space. MongoDB creates an index for each encrypted field, which increases the duration of write operations on that field. When a write operation updates an indexed field, MongoDB updates the related index.

## Configure Encrypted Fields for Optimal Search and Storage

MongoDB provides the following parameters to facilitate debugging and performance tuning:

*Query Type*: `range`

*Type*: Must match the field's `bsonType`.

Required if `bsonType` is `decimal` or `double`. Optional but highly recommended if it is `int`, `long`, or `date`. Defaults to the `bsonType` min and max values.

Specify minimum and maximum (inclusive) queryable values for a field when possible, as smaller bounds improve query efficiency. If querying values outside of these bounds, MongoDB returns an error.

### Substring Parameters

**Warning: Prefix, Suffix, and Substring Queries are in Public Preview**

Queryable Encryption prefix, suffix, and substring queries are available in public preview in MongoDB 8.2. Do not enable these query types in production. Public preview functionality will be incompatible with the GA feature, and you will have to drop any collections that enable these queries.

*Query Type*: `substringPreview`

*Type*: Integer from 1-60, inclusive.

The maximum allowed length for a substring-indexed field. Attempting to insert a longer string returns an error.

**Important:**

You can override the character limit by setting [`fleDisableSubstringPreviewParameterLimits`](/docs/manual/reference/cluster-parameters/fleDisableSubstringPreviewParameterLimits#mongodb-parameter-param.fleDisableSubstringPreviewParameterLimits), but running substring queries against longer strings has a significant impact on performance.

*Query Type*: `prefixPreview`, `suffixPreview`, `substringPreview`

*Type*: Positive integer.

- Must be >= 1 for `prefixPreview` or `suffixPreview` queries.

- Must be >= 2 for `substringPreview` queries.

The minimum allowed prefix/suffix/substring length to query. Attempting to query a shorter string returns an error.

*Query Type*: `prefixPreview`, `suffixPreview`, `substringPreview`

*Type*: Positive integer - Must be >=1 for `prefixPreview` or `suffixPreview` queries. - Must 2-10 inclusive for `substringPreview` queries.

The maximum allowed prefix/suffix/substring length to query. Attempting to query a longer string returns an error.

**Important:**

This setting strongly impacts query performance. Limit the maximum query length whenever possible.

*Query Type*: `prefixPreview`, `suffixPreview`, `substringPreview`

*Type*: Boolean

Optional. Defaults to `true`.

Whether prefix/suffix/substring queries are case-sensitive. Set to `false` for case-insensitive matching.

*Query Type*: `prefixPreview`, `suffixPreview`, `substringPreview`

*Type*: Boolean

Optional. Defaults to `true`.

Whether prefix/suffix/substring queries must match diacritical marks. Set to `false` for diacritic-insensitive matching.

### Advanced Query Parameters

**Warning:**

These parameters are intended for advanced users only. The default values are suitable for the majority of use cases, and should only be modified if your use case requires it.

*Query Type*: `range`

*Type*: Integer from 1-8.

Optional. Defaults to 2.

Affects how thoroughly MongoDB indexes range values. Low sparsity (dense indexing) improves query performance, but stores more documents in the encrypted metadata collections for each insert or update operation, causing greater storage overhead. High sparsity does the opposite.

**Changed in version 8.2**

Maximum value changed from 4 to 8.

*Query Type*: `range`

*Type*: Integer.

Optional. Allowed only if `bsonType` is `double` or `decimal`. If unset, MongoDB uses the same maximum precision as the `bsonType`, either `double` or `decimal`.

Limits how many digits after the decimal point are taken into account when querying a `double` or `decimal` field. Additional digits are dropped, not rounded. For example, a `precision` of 1 treats `10.18` as `10.1` for queries. The encrypted value is still stored as `10.18`.

Specify `precision` and limit it when possible. Every digit increases storage overhead and has a high impact on searchable range and index generation.

*Query Type*: `range`

*Type*: Integer.

Optional. Defaults to 6.

The `trimFactor` controls the throughput of concurrent inserts and updates. A higher `trimFactor` increases the throughput of concurrent insert and updates at the cost of slowing down some range read operations. A lower `trimFactor` does the opposite.

*Query Type*: `equality`, `range`, `prefixPreview`, `suffixPreview`, `substringPreview`

*Type*: Integer.

Optional. Defaults to 8.

Concurrent write operations, such as inserting the same field/value pair into multiple documents in close succession, can cause contention: conflicts that delay operations.

With Queryable Encryption, MongoDB tracks the occurrences of each field/value pair in an encrypted collection using an internal counter. The [contention factor](/docs/manual/reference/glossary#std-term-contention-factor) partitions this counter, similar to an array. This minimizes issues with incrementing the counter when using `insert`, `update`, or `findAndModify` to add or modify an encrypted field with the same field/value pair in close succession. `contention = 0` creates an array with one element at index 0. `contention = 4` creates an array with 5 elements at indexes 0-4. MongoDB increments a random array element during insert.

When unset, `contention` defaults to `8`, which provides high performance for most workloads. Higher contention improves the performance of insert and update operations on low cardinality fields, but decreases find performance.

You can optionally include `contention` on queryable fields to change the value from its default of 8.

For more thorough information on contention factor and its cryptographic implications, see "Section 9: Guidelines" in MongoDB's [Queryable Encryption Technical Paper](https://www.mongodb.com/resources/products/capabilities/queryable-encryption-technical-paper).
