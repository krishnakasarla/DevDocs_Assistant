> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

<!--
Tab options on this page. Append to the .md URL to filter:
  ?tabs=<id,...>   select specific tabs (e.g. ?tabs=nodejs,shell)
  ?allTabs=true    include every tab
  (no param)       default: one tab per tabset

Available tabs:
  drivers: shell, csharp, go, java-sync, nodejs, php, python, ruby, rust
-->

# Create an Encrypted Collection and Insert Documents

Queryable Encryption equality and range queries are fully supported in production. Prefix, suffix, and substring queries are only available in public preview in MongoDB 8.2. Do not enable these query types in production. GA functionality of prefix, suffix and substring query types will be incompatible with the preview feature. To learn more, see [Supported Query Types](https://www.mongodb.com/docs/manual/core/queryable-encryption/reference/supported-operations/).

## Overview

This guide shows you how to create a Queryable Encryption-enabled collection and insert a document with encrypted fields.

After you complete the steps in this guide, you should be able to create an encrypted collection and insert a document with fields that are encrypted with your Customer Master Key.

## Before You Start

[Create your Queryable Encryption-enabled application](/docs/manual/core/queryable-encryption/qe-create-application#std-label-qe-create-application) before creating an encrypted collection.

If you are using [explicit encryption](/docs/manual/core/queryable-encryption/fundamentals/manual-encryption#std-label-qe-fundamentals-manual-encryption), you must also create a unique Data Encryption Key for each encrypted field in advance. For more information, see [Encryption Keys and Key Vaults.](/docs/manual/core/queryable-encryption/fundamentals/keys-key-vaults#std-label-qe-reference-keys-key-vaults)

## Procedure

1. Specify fields to encrypt

   To encrypt a field, add it to the encryption schema. To enable queries on a field, add the `queries` property. You can enable fields to be queryable by the following types of queries:

   - Equality

   - Range

   - Prefix, suffix, or substring

   The following steps demonstrate how to specify fields to encrypt with each query type.

   Specify fields for equality queries

   To enable equality queries on a field, add the field to the encryption schema with a `queryType` of `"equality"`. The following code sample encrypts both the `ssn` and `billing` fields, but only the `ssn` field is queryable:

   ### Node.js

   ```javascript
   const collectionOpts = {
     encryptedFields: {
       fields: [
         {
           path: "patientRecord.ssn",
           bsonType: "string",
           queries: { queryType: "equality" },
         },
         {
           path: "patientRecord.billing",
           bsonType: "object",
         },
       ],
     },
   };
   ```

   Specify fields for range queries

   To enable range queries on a field, add the field to the encryption schema with a `queryType` of `"range"`. The following example adds the `billAmount` field to the encryption schema created in the preceding step and enables range queries on it:

   ### Node.js

   ```javascript
   const collectionOpts = {
     encryptedFields: {
       fields: [
         {
           path: "patientRecord.ssn",
           bsonType: "string",
           queries: { queryType: "equality" },
         },
         {
           path: "patientRecord.billing",
           bsonType: "object",
         },
         {
           path: "patientRecord.billAmount",
           bsonType: "int",
           queries: {
             queryType: "range",
             sparsity: 1,
             trimFactor: 4,
             min: 100,
             max: 2000,
           },
         },
       ],
     },
   };
   ```

   Specify fields for prefix, suffix, or substring queries

   ### Node.js

   To enable prefix, suffix, or substring queries on a field, add the field to the encryption schema with a `queryType` of `"prefixPreview"`, `"suffixPreview"`, or `"substringPreview"` and the [associated options](/docs/manual/core/queryable-encryption/fundamentals/encrypt-and-query#std-label-qe-substring-parameters). The following example enables prefix queries on the `patientRecord.ssn` field:

   ```javascript
   const collectionOpts = {
     encryptedFields: {
       fields: [
         {
           keyId: dek,
           path: "patientRecord.ssn",
           bsonType: "string",
           queries: { 
             queryType: "prefixPreview",
             strMinQueryLength: 3,
             strMaxQueryLength: 10,
             caseSensitive: true,
             diacriticSensitive: true,
           },
         },
       ],
     },
   };
   ```

   **Tip: Suffix Query**

   To enable suffix queries on a field, change the `queryType` option to `"suffix"` in the preceding code example.

   The following example enables substring queries on the `patientRecord.ssn` field:

   ```javascript
   const collectionOpts = {
     encryptedFields: {
       fields: [
         {
           keyId: dek,
           path: "patientRecord.ssn",
           bsonType: "string",
           queries: { 
             queryType: "substringPreview",
             strMaxLength: 12,
             strMinQueryLength: 3,
             strMaxQueryLength: 10,
             caseSensitive: true,
             diacriticSensitive: true,
           },
         },
       ],
     },
   };
   ```

   For extended versions of these steps, see [Create an Encryption Schema.](/docs/manual/core/queryable-encryption/qe-create-encryption-schema#std-label-qe-create-encryption-schema)

2. Instantiate a client encryption object to access the API for the encryption helper methods

   ### Node.js

   ```javascript
   const clientEncryption = new ClientEncryption(
     encryptedClient,
     autoEncryptionOptions
   );
   ```

3. Create the collection

   **Important:**

   Explicitly create your collection, rather than creating it implicitly with an insert operation. When you create a collection using `createCollection()`, MongoDB creates an index on the encrypted fields. Without this index, queries on encrypted fields may run slowly.

   ### Node.js

   **Note: Import ClientEncryption**

   When using the Node.js driver v6.0 and later, you must import `ClientEncryption` from `mongodb`.

   For earlier driver versions, import `ClientEncryption` from `mongodb-client-encryption`.

   Create your encrypted collection by using the encryption helper method accessed through the `ClientEncryption` class. This method automatically generates data encryption keys for your encrypted fields and creates the encrypted collection:

   ```javascript
   await clientEncryption.createEncryptedCollection(
     encryptedDatabase,
     encryptedCollectionName,
     {
       provider: kmsProviderName,
       createCollectionOptions: collectionOpts,
       masterKey: customerMasterKeyCredentials,
     }
   );
   ```

   **Tip: Database vs. Database Name**

   The method that creates the encrypted collection requires a reference to a database *object* rather than the database *name*.

   For additional information, see [Enable Queryable Encryption when Creating a Collection.](/docs/manual/core/queryable-encryption/fundamentals/enable-qe#std-label-qe-fundamentals-enable-qe)

4. Insert a document with encrypted fields

   ### Node.js

   Create a sample document that describes a patient's personal information. Use the encrypted client to insert it into the `patients` collection, as shown in the following example:

   ```javascript
   const patientDocument = {
     patientName: "Jon Doe",
     patientId: 12345678,
     patientRecord: {
       ssn: "987-65-4320",
       billing: {
         type: "Visa",
         number: "4111111111111111",
       },
       billAmount: 1500,
     },
   };

   const encryptedCollection = encryptedClient
     .db(encryptedDatabaseName)
     .collection(encryptedCollectionName);

   const result = await encryptedCollection.insertOne(patientDocument);
   ```

## Next Steps

After creating a Queryable Encryption-enabled collection, you can [query the encrypted fields.](/docs/manual/core/queryable-encryption/qe-retrieve-encrypted-document#std-label-qe-query-encrypted-document)
