> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Create an Encryption Schema

Queryable Encryption equality and range queries are fully supported in production. Prefix, suffix, and substring queries are only available in public preview in MongoDB 8.2. Do not enable these query types in production. GA functionality of prefix, suffix and substring query types will be incompatible with the preview feature. To learn more, see [Supported Query Types](https://www.mongodb.com/docs/manual/core/queryable-encryption/reference/supported-operations/).

## About this Task

To make encrypted fields queryable, create an [encryption schema](/docs/manual/reference/glossary#std-term-encryption-schema). This schema defines which fields are queryable, and which query types are permitted. For more information, see [Encrypted Fields and Enabled Queries.](/docs/manual/core/queryable-encryption/fundamentals/encrypt-and-query#std-label-qe-fundamentals-encrypt-query)

**Important:**

Queryable Encryption supports equality and range queries. You can configure a field for only one query type.

## Before you Begin

When you make encrypted fields queryable, consider performance and security. For details on how each configuration option affects these, see [Configure Encrypted Fields for Optimal Search and Storage.](/docs/manual/core/queryable-encryption/fundamentals/encrypt-and-query#std-label-qe-field-configuration)

To use the Public Preview prefix, suffix, or substring queries with [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh), you must separately download the [Automatic Encryption Shared Library](https://www.mongodb.com/docs/manual/core/queryable-encryption/install-library/) 8.2 or higher, then specify the library path to `mongosh` using the [--cryptSharedLibPath](https://www.mongodb.com/docs/mongodb-shell/reference/options/) option.

## Field Reference

You can configure encryption for each field in the `fields` array of your `encryptedFieldsObject`. The following table describes the available subfields:

| Field | Type | Description |
| --- | --- | --- |
| `path` | String | **Required.** The dot-notation path to the field to encrypt, such as `"patientInfo.ssn"`. You can specify any field except the `_id` field. |
| `bsonType` | String | **Required.** The [BSON type](/docs/manual/reference/bson-types#std-label-bson-types) of the field to encrypt. For a complete list of supported types, see [Supported and Unsupported BSON Types.](/docs/manual/core/queryable-encryption/reference/supported-operations#std-label-qe-commands-supported-bson-types) |
| `keyId` | UUID | *Optional.* The UUID of the DEK (Data Encryption Key) to use for encrypting this field. The UUID is a BSON [binary data](http://bsonspec.org/spec.html) element of subtype `4`. Key IDs must be unique. Specifying a `keyId` that is already in use returns an error. If omitted, you can use the `createEncryptedCollection()` helper method to create keys automatically. |
| `queries` | Object | *Optional.* Enables querying on this encrypted field. If omitted, the field is encrypted but not queryable. To learn more about query options, see [Configure Encrypted Fields for Optimal Search and Storage.](/docs/manual/core/queryable-encryption/fundamentals/encrypt-and-query#std-label-qe-field-configuration) |

## Steps

1. Create the encryption schema.

   Include an `encryptedFieldsObject` with a nested `fields` array:

   ```javascript
   const encryptedFieldsObject = {
      fields: []
   }
   ```

2. Specify fields to encrypt.

   Add the `path` and `bsonType` strings to a document within the fields array:

   ```javascript
   const encryptedFieldsObject = {
      fields: [
         {
            path: "myDocumentField",
            bsonType: "int"
         }
      ]
   }
   ```

   **Important:**

   You can specify any field for encryption except the `_id` field.

   Optionally, set a `keyId` field with the DEK (Data Encryption Key) ID.

   **Important:**

   Key IDs must be unique, otherwise the server returns an error.

   By configuring `AutoEncryptionSettings` on the client, you can use the `createEncryptedCollection` helper method to create keys automatically.

   ```javascript
   {
      path: "myDocumentField",
      bsonType: "int",
      keyId: "<unique data encryption key>"
   }
   ```

3. Enable equality queries on desired fields.

   This enables querying with the [`$eq`](/docs/manual/reference/operator/query/eq#mongodb-query-op.-eq), [`$ne`](/docs/manual/reference/operator/query/ne#mongodb-query-op.-ne), [`$in`](/docs/manual/reference/operator/query/in#mongodb-query-op.-in), and [`$nin`](/docs/manual/reference/operator/query/nin#mongodb-query-op.-nin) operators.

   Add the `queries` object and set `queryType` to `"equality"`:

   ```javascript
   {
      path: "myDocumentField",
      bsonType: "int",
      queries: { queryType: "equality" }
   }
   ```

4. Enable range queries on desired fields.

   This enables querying with the [`$lt`](/docs/manual/reference/operator/query/lt#mongodb-query-op.-lt), [`$lte`](/docs/manual/reference/operator/query/lte#mongodb-query-op.-lte), [`$gt`](/docs/manual/reference/operator/query/gt#mongodb-query-op.-gt), and [`$gte`](/docs/manual/reference/operator/query/gte#mongodb-query-op.-gte) operators.

   For details on how the following options affect security and performance, see [Configure Encrypted Fields for Optimal Search and Storage.](/docs/manual/core/queryable-encryption/fundamentals/encrypt-and-query#std-label-qe-field-configuration)

   Add the `queries` object and set `queryType` to `"range"`:

   ```javascript
   {
      path: "myDocumentRangeField",
      bsonType: "int",
      queries: { queryType: "range" }
   }
   ```

   Set the following fields:

   | Field | Type | Description |
   | --- | --- | --- |
   | [min and max](/docs/manual/core/queryable-encryption/fundamentals/encrypt-and-query#std-label-qe-field-min-max) | Same as field `bsonType` | Required if `bsonType` is `decimal` or `double`. Optional but highly recommended if it is `int`, `long`, or `date`. Defaults to the minimum and maximum values of the `bsonType`. When possible, specifying bounds on a query improves performance. If querying values outside of these inclusive bounds, MongoDB returns an error. |

   ```javascript
   {
      path: "myDocumentRangeField",
      bsonType: "int",
      queries: { queryType: "range",
                 min: 0,
                 max: 1200
      }
   }
   ```

5. Enable prefix, suffix, or substring queries on desired fields.

   These query types are for `string` fields only. You can enable both `prefixPreview` and `suffixPreview` on the same field, but can't enable either if using `substringPreview`.

   **Warning: Prefix, Suffix, and Substring Queries are in Public Preview**

   Queryable Encryption prefix, suffix, and substring queries are available in public preview in MongoDB 8.2. Do not enable these query types in production. Public preview functionality will be incompatible with the GA feature, and you will have to drop any collections that enable these queries.

   - `prefixPreview` queries enable the [`$encStrStartsWith`](/docs/manual/reference/operator/aggregation/encStrStartsWith#mongodb-expression-exp.-encStrStartsWith) and [`$encStrNormalizedEq`](/docs/manual/reference/operator/aggregation/encStrNormalizedEq#mongodb-expression-exp.-encStrNormalizedEq) aggregation expressions.

   - `suffixPreview` queries enable the [`$encStrEndsWith`](/docs/manual/reference/operator/aggregation/encStrEndsWith#mongodb-expression-exp.-encStrEndsWith) and [`$encStrNormalizedEq`](/docs/manual/reference/operator/aggregation/encStrNormalizedEq#mongodb-expression-exp.-encStrNormalizedEq) aggregation expressions.

   - `substringPreview` queries enable the [`$encStrContains`](/docs/manual/reference/operator/aggregation/encStrContains#mongodb-expression-exp.-encStrContains) and [`$encStrNormalizedEq`](/docs/manual/reference/operator/aggregation/encStrNormalizedEq#mongodb-expression-exp.-encStrNormalizedEq) aggregation expressions.

   Add the `queries` object and set `queryType` to `"prefixPreview"`, `"suffixPreview"`, or `"substringPreview"`:

   ```javascript
   {
      path: "myDocumentStringField",
      bsonType: "string",
      queries: { queryType: "substringPreview" }
   }
   ```

   Set the following fields.

   For details on how they affect security and performance, see [Configure Encrypted Fields for Optimal Search and Storage.](/docs/manual/core/queryable-encryption/fundamentals/encrypt-and-query#std-label-qe-field-configuration)

   | Field | Type | Description |
   | --- | --- | --- |
   | [`strMaxLength`](/docs/manual/core/queryable-encryption/fundamentals/encrypt-and-query#mongodb-parameter-param.strMaxLength) | integer | `substringPreview` queries only. The maximum allowed length for a substring-indexed field. |
   | [`strMinQueryLength`](/docs/manual/core/queryable-encryption/fundamentals/encrypt-and-query#mongodb-parameter-param.strMinQueryLength) | integer | The minimum allowed prefix/suffix/substring length to query. |
   | [`strMaxQueryLength`](/docs/manual/core/queryable-encryption/fundamentals/encrypt-and-query#mongodb-parameter-param.strMaxQueryLength) | integer | The maximum allowed prefix/suffix/substring length to query. IMPORTANT: This setting strongly impacts query performance. Limit it whenever possible. |
   | [`caseSensitive`](/docs/manual/core/queryable-encryption/fundamentals/encrypt-and-query#mongodb-parameter-param.caseSensitive) | Boolean | Optional. Whether queries are case-sensitive. Defaults to `true`. |
   | [`diacriticSensitive`](/docs/manual/core/queryable-encryption/fundamentals/encrypt-and-query#mongodb-parameter-param.diacriticSensitive) | Boolean | Optional. Whether queries are diacritic-sensitive. Defaults to `true`. |

   ```javascript
   {
      path: "myDocumentStringField",
      bsonType: "string",
      queries: {
         "queryType": "substringPreview",
         "strMaxLength": 30,
         "strMinQueryLength": 1,
         "strMaxQueryLength": 20,
         "caseSensitive": false
      }
   }
   ```

## Example

This example shows how to create an encryption schema for hospital data.

Consider the following document that contains personally identifiable information (PII), credit card information, and sensitive medical information:

```json
{
   "firstName": "Jon",
   "lastName": "Snow",
   "patientId": 12345187,
   "address": "123 Cherry Ave",
   "medications": [
      "Adderall",
      "Lipitor"
   ],
   "patientInfo": {
      "ssn": "921-12-1234",
      "billing": {
            "type": "visa",
            "number": "1234-1234-1234-1234"
      }
   }
}
```

To ensure the PII and sensitive medical information stays secure, this encryption schema adds the relevant fields:

```javascript
const encryptedFieldsObject = {
   fields: [
      {
         path: "patientId",
         bsonType: "int"
      },
      {
         path: "patientInfo.ssn",
         bsonType: "string"
      },
      {
         path: "medications",
         bsonType: "array"
      },
      {
         path: "patientInfo.billing",
         bsonType: "object"
      }
   ]
}
```

Adding the `queries` property makes the `patientId` and `patientInfo.ssn` fields queryable. This example enables equality queries:

```javascript
const encryptedFieldsObject = {
   fields: [
      {
         path: "patientId",
         bsonType: "int",
         queries: { queryType: "equality" }
      },
      {
         path: "patientInfo.ssn",
         bsonType: "string",
         queries: { queryType: "equality" }
      },
      {
         path: "medications",
         bsonType: "array"
      },
      {
         path: "patientInfo.billing",
         bsonType: "object"
      },
   ]
}
```
