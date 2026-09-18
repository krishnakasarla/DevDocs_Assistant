> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Enabling Queryable Encryption when Creating Collections

Queryable Encryption equality and range queries are fully supported in production. Prefix, suffix, and substring queries are only available in public preview in MongoDB 8.2. Do not enable these query types in production. GA functionality of prefix, suffix and substring query types will be incompatible with the preview feature. To learn more, see [Supported Query Types](https://www.mongodb.com/docs/manual/core/queryable-encryption/reference/supported-operations/).

## Overview

Enable Queryable Encryption at collection creation. You can't encrypt fields on documents that are already in a collection.

**Important:**

Explicitly create your collection, rather than creating it implicitly with an insert operation. When you create a collection using `createCollection()`, MongoDB creates an index on the encrypted fields. Without this index, queries on encrypted fields may run slowly.

## Enable Queryable Encryption on a Collection

You can enable Queryable Encryption on fields in one of two ways. The following examples use Node.js to enable Queryable Encryption:

- Pass the encryption schema, represented by the `encryptedFieldsObject` constant, to the client that the application uses to create the collection:

  ```javascript
  const client = new MongoClient(uri, {
     autoEncryption: {
        keyVaultNameSpace: "<your keyvault namespace>",
        kmsProviders: "<your kms provider>",
        extraOptions: {
           cryptSharedLibPath: "<path to Automatic Encryption Shared Library>"
        },
        encryptedFieldsMap: {
           "<databaseName.collectionName>": { encryptedFieldsObject }
        }
     }

     ...

     await client.db("<database name>").createEncryptedCollection("<collection name>");
  }
  ```

  For more information on `autoEncryption` configuration options, see the section on [MongoClient Options for Queryable Encryption.](/docs/manual/core/queryable-encryption/reference/qe-options-clients#std-label-qe-reference-mongo-client)

- Pass the encryption schema `encryptedFieldsObject` to `createEncryptedCollection()`:

  ```javascript
  await encryptedDB.createEncryptedCollection("<collection name>", {
     encryptedFields: encryptedFieldsObject
  });
  ```

  **Tip:**

  Specify the `encryptedFieldsObject` when you create the collection, and also when you create a client to access the collection. For more information about the security considerations of not defining the `encryptedFieldsObject`, see [Security Considerations.](/docs/manual/core/queryable-encryption/about-qe-csfle#std-label-qe-csfle-security-considerations)
