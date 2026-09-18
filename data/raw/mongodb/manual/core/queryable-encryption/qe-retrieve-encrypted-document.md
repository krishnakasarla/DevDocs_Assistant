> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

<!--
Tab options on this page. Append to the .md URL to filter:
  ?tabs=<id,...>   select specific tabs (e.g. ?tabs=nodejs,shell)
  ?allTabs=true    include every tab
  (no param)       default: one tab per tabset

Available tabs:
  drivers: shell, csharp, go, java-sync, nodejs, php, python, ruby, rust
-->

# Query a Document with Encrypted Fields

Queryable Encryption equality and range queries are fully supported in production. Prefix, suffix, and substring queries are only available in public preview in MongoDB 8.2. Do not enable these query types in production. GA functionality of prefix, suffix and substring query types will be incompatible with the preview feature. To learn more, see [Supported Query Types](https://www.mongodb.com/docs/manual/core/queryable-encryption/reference/supported-operations/).

## Overview

This guide shows you how to use a Queryable Encryption-enabled application to retrieve a document that has encrypted fields.

After you complete the steps in this guide, you should be able to use your application to query data in encrypted fields, and to decrypt those fields as an authorized user.

## Before You Start

[Create an encrypted collection and insert documents](/docs/manual/core/queryable-encryption/qe-create-encrypted-collection#std-label-qe-create-encrypted-collection) before continuing.

## Procedure

1. Query an encrypted field with equality

   If you enabled equality queries on an encrypted field, you can retrieve documents that have a specified value in that field.

   The following example performs an equality query on an encrypted field and prints the decrypted data:

   ### Node.js

   ```javascript
   const findResult = await encryptedCollection.findOne({
     "patientRecord.ssn": "987-65-4320",
   });
   console.log(findResult);
   ```

2. Query an encrypted field with range

   If you enabled range queries on an encrypted field, you can retrieve documents where the value of that field is within the range that you specify.

   The following example performs a range query on an encrypted field and prints the decrypted data:

   ### Node.js

   ```javascript
   const findResult = await encryptedCollection.findOne({
     "patientRecord.billAmount": { $gt: 1000, $lt: 2000 },
   });
   console.log(findResult);
   ```

3. Query an encrypted field for a prefix, suffix, or substring match

   ### Node.js

   If you enabled prefix, suffix, or substring queries on an encrypted field, you can retrieve documents where the value of that field includes the string specified in your search criteria.

   The following example performs a prefix query on an encrypted field and prints the decrypted data:

   ```javascript
   const findResult = await encryptedCollection.findOne(
     { $expr: { $encStrStartsWith: 
       { input: "$patientRecord.ssn", prefix: "987" } 
     } 
   })
   ```

   To perform a suffix query, replace `$encStrStartsWith` with `$encStrEndsWith`. Then, replace the `prefix` option with the `suffix` option.

   To perform a substring query, use the `$encStrContains` operator, as shown in the following example:

   ```javascript
   const findResult = await encryptedCollection.findOne(
     { $expr: { $encStrContains: 
       { input: "$patientRecord.ssn", substring: "-65-432" } 
     } 
   })
   ```

   ##### Query Result

   The output of the preceding code examples should look similar to the following:

   ```json
   {
     "_id": {
       "$oid": "648b384a722cb9b8392df76a"
     },
     "name": "Jon Doe",
     "record": {
       "ssn": "987-65-4320",
       "billing": {
         "type": "Visa",
         "number": "4111111111111111"
       },
       "billAmount": 1500
     },
     "__safeContent__": [
       {
         "$binary": {
           "base64": "L1NsYItk0Sg+oL66DBj6IYHbX7tveANQyrU2cvMzD9Y=",
           "subType": "00"
         }
       }
     ]
   }

   ```

   **Warning: Do not Modify the \_\_safeContent\_\_ Field**

   The `__safeContent__` field is essential to Queryable Encryption. Do not modify the contents of this field.
