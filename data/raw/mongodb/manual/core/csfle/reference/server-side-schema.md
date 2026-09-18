> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# CSFLE Server-Side Schema Enforcement

In Client-Side Field Level Encryption (CSFLE)-enabled client applications, you can use [schema validation](https://www.mongodb.com/docs/manual/core/schema-validation/) to have your MongoDB instance enforce encryption of specific fields. To specify which fields require encryption, use the [automatic encryption rule keywords](/docs/manual/core/csfle/reference/encryption-schemas#std-label-field-level-encryption-json-schema) with the [`$jsonSchema`](/docs/manual/reference/operator/query/jsonSchema#mongodb-query-op.-jsonSchema) validation object. The server rejects any write operations to that collection where the specified fields are not [`Binary (BinData)`](/docs/manual/reference/mongodb-extended-json#mongodb-bsontype-Binary) subtype 6 objects.

To learn how a CSFLE-enabled client configured to use automatic encryption behaves when it encounters a server-side schema, see [Server-Side Field Level Encryption Enforcement.](/docs/manual/core/csfle/fundamentals/automatic-encryption#std-label-field-level-encryption-automatic-remote-schema)

To learn how a CSFLE-enabled client configured to use explicit encryption behaves when it encounters a server-side schema, see [Server-Side Field Level Encryption Enforcement.](/docs/manual/core/csfle/fundamentals/manual-encryption#std-label-csfle-fundamentals-manual-encryption-server-side-schema)

## Example

Consider an `hr` database with an `employees` collection. Documents in the `employees` collection have the following form:

```json
{
  "name": "Jane Doe",
  "age": 51
}

```

You want to enforce the following behavior for client applications using your collection:

- When encrypting the `age` field, clients must follow these encryption rules:

  - Use the Data Encryption Key with an `_id` of `UUID("e114f7ad-ad7a-4a68-81a7-ebcb9ea0953a")`.

  - Use the [randomized](/docs/manual/core/csfle/fundamentals/encryption-algorithms#std-label-field-level-encryption-random) encryption algorithm.

  - The `age` field must be an integer.

- When encrypting the `name` field, clients must follow these encryption rules:

  - Use the Data Encryption Key with an `_id` of `UUID("33408ee9-e499-43f9-89fe-5f8533870617")`.

  - Use the [deterministic](/docs/manual/core/csfle/fundamentals/encryption-algorithms#std-label-field-level-encryption-deterministic) encryption algorithm.

  - The `name` field must be a string.

The following [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) code uses the [`collMod`](/docs/manual/reference/command/collMod#mongodb-dbcommand-dbcmd.collMod) command to update the `hr.employees` collection to include a `validator` to enforce the preceding behavior:

```javascript
db.getSiblingDB("hr").runCommand({
  collMod: "employees",
  validator: {
    $jsonSchema: {
      bsonType: "object",
      properties: {
        age: {
          encrypt: {
            keyId: [UUID("e114f7ad-ad7a-4a68-81a7-ebcb9ea0953a")],
            algorithm: "AEAD_AES_256_CBC_HMAC_SHA_512-Random",
            bsonType: "int",
          },
        },
        name: {
          encrypt: {
            keyId: [UUID("33408ee9-e499-43f9-89fe-5f8533870617")],
            algorithm: "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic",
            bsonType: "string",
          },
        },
      },
    },
  },
});

```

## Learn More

To learn more about the encryption algorithms CSFLE supports, see [Fields and Encryption Types.](/docs/manual/core/csfle/fundamentals/encryption-algorithms#std-label-csfle-reference-encryption-algorithms)

To learn more about encryption schemas and encryption rules, see [CSFLE Encryption Schemas.](/docs/manual/core/csfle/reference/encryption-schemas#std-label-csfle-reference-encryption-schemas)
