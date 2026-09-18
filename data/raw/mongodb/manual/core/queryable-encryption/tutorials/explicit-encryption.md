> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

<!--
Tab options on this page. Append to the .md URL to filter:
  ?tabs=<id,...>   select specific tabs (e.g. ?tabs=nodejs,shell)
  ?allTabs=true    include every tab
  (no param)       default: one tab per tabset

Available tabs:
  drivers: csharp, go, java, nodejs, python, java-sync
-->

# Use Explicit Encryption

Queryable Encryption equality and range queries are fully supported in production. Prefix, suffix, and substring queries are only available in public preview in MongoDB 8.2. Do not enable these query types in production. GA functionality of prefix, suffix and substring query types will be incompatible with the preview feature. To learn more, see [Supported Query Types](https://www.mongodb.com/docs/manual/core/queryable-encryption/reference/supported-operations/).

## Overview

This guide shows you how to encrypt a document with explicit encryption and a MongoDB driver.

After completing this guide, you should be able to configure a driver to encrypt fields in a document using explicit encryption. With this knowledge, you should be able to create a client application that uses explicit encryption. with automatic decryption.

**Important: Do Not Use this Sample Application In Production**

Because the instructions in this tutorial include storing an encryption key in an insecure environment, you should not use an unmodified version of this application in production. Using this application in production risks unauthorized access to the encryption key or loss of the key needed to decrypt your data. The purpose of this tutorial is to demonstrate how to use Queryable Encryption without needing to set up a Key Management System.

You can use a Key Management System to securely store your encryption key in a production environment. A KMS (Key Management System) is a remote service that securely stores and manages your encryption keys. To learn how to set up a Queryable Encryption enabled application that uses a KMS (Key Management System), see the [Queryable Encryption Tutorials.](/docs/manual/core/queryable-encryption/tutorials#std-label-qe-tutorial-automatic-encryption)

## Before You Get Started

To complete and run the code in this guide, you need to set up your development environment as shown in the [Install a Queryable Encryption Compatible Driver and Dependencies](/docs/manual/core/queryable-encryption/install#std-label-qe-install) page.

### Full Application Code

To see the complete code for the sample application, select your programming language in the language selector.

### Node.js

[Complete Node.js Application](https://github.com/mongodb-university/docs-in-use-encryption-examples/tree/main/queryable-encryption/node/exp/reader/)

## Procedure

1. Create a Customer Master Key

   You must create a Customer Master Key (CMK (Customer Master Key)) to perform Queryable Encryption.

   Create a 96-byte Customer Master Key and save it to the file `master-key.txt`:

   ### Node.js

   ```javascript
   const fs = require("fs");
   const crypto = require("crypto");
   try {
     fs.writeFileSync("master-key.txt", crypto.randomBytes(96));
   } catch (err) {
     console.error(err);
   }
   ```

   **Warning: Secure your Local Key File in Production**

   We recommend storing your Customer Master Keys in a remote [Key Management System](https://en.wikipedia.org/wiki/Key_management#Key_management_system) (KMS (Key Management System)). To learn how to use a remote KMS (Key Management System) in your Queryable Encryption implementation, see the [Queryable Encryption Tutorials](/docs/manual/core/queryable-encryption/tutorials#std-label-qe-tutorial-automatic-encryption) guide.

   If you choose to use a local key provider in production, exercise great caution and do not store it on the file system. Consider injecting the key into your client application using a sidecar process, or use another approach that keeps the key secure.

   **Tip: Generate a CMK from the Command Line**

   Use the following command to generate a CMK (Customer Master Key) from a Unix shell or PowerShell:

   - Unix/macOS shell:

     ```sh
     echo $(head -c 96 /dev/urandom | tr -d '\n')
     ```

   - PowerShell:

     ```none
     $r=[byte[]]::new(96);$g=[System.Security.Cryptography.RandomNumberGenerator]::Create();$g.GetBytes($r);$r
     ```

   Save the output of the preceding command to a file named `customer-master-key.txt`.

   **See also: Complete Code**

   ### Node.js

   To view the complete code for making a Customer Master Key, see [the Queryable Encryption sample application repository.](https://github.com/mongodb-university/docs-in-use-encryption-examples/tree/main/queryable-encryption/node/exp/reader/make_data_key.js)

2. Create a Unique Index on your Key Vault collection

   Create a unique index on the `keyAltNames` field in your `encryption.__keyVault` namespace.

   Select the tab corresponding to your preferred MongoDB driver:

   ### Node.js

   ```javascript
   const uri = "<Your Connection String>";
   const keyVaultClient = new MongoClient(uri);
   await keyVaultClient.connect();
   const keyVaultDB = keyVaultClient.db(keyVaultDatabase);
   // Drop the Key Vault Collection in case you created this collection
   // in a previous run of this application.
   await keyVaultDB.dropDatabase();
   const keyVaultColl = keyVaultDB.collection(keyVaultCollection);
   await keyVaultColl.createIndex(
     { keyAltNames: 1 },
     {
       unique: true,
       partialFilterExpression: { keyAltNames: { $exists: true } },
     }
   );
   ```

3. Create your Data Encryption Keys and Encrypted Collection

   Read the Customer Master Key and Specify KMS Provider Settings

   Retrieve the contents of the Customer Master Key file that you generated in the [Create a Customer Master Key](/docs/manual/core/queryable-encryption/tutorials/explicit-encryption#std-label-qe-manual-enc-create-master-key) step of this guide.

   Use the CMK (Customer Master Key) value in your KMS provider settings. The client uses these settings to discover the CMK (Customer Master Key). Set the provider name to `local` to indicate that you are using a Local Key Provider.

   Select the tab corresponding to your preferred MongoDB driver:

   ### Node.js

   ```javascript
   const provider = "local";
   const path = "./master-key.txt";
   // WARNING: Do not use a local key file in a production application
   const localMasterKey = fs.readFileSync(path);
   const kmsProviders = {
     local: {
       key: localMasterKey,
     },
   };
   ```

   Create your Data Encryption Keys

   Construct a client with your MongoDB connection string and Key Vault collection namespace, and create the Data Encryption Keys:

   **Note: Key Vault Collection Namespace Permissions**

   To complete this tutorial, the database user your application uses to connect to MongoDB must have [`dbAdmin`](/docs/manual/reference/built-in-roles#mongodb-authrole-dbAdmin) permissions on the following namespaces:

   - `encryption.__keyVault`

   - `medicalRecords` database

   ### Node.js

   ```javascript
   const clientEnc = new ClientEncryption(keyVaultClient, {
     keyVaultNamespace: keyVaultNamespace,
     kmsProviders: kmsProviders,
   });
   const dek1 = await clientEnc.createDataKey(provider, {
     keyAltNames: ["dataKey1"],
   });
   const dek2 = await clientEnc.createDataKey(provider, {
     keyAltNames: ["dataKey2"],
   });
   ```

   Create Your Encrypted Collection

   Use a Queryable Encryption enabled `MongoClient` instance to specify what fields you must encrypt and create your encrypted collection:

   ### Node.js

   ```javascript
   const encryptedFieldsMap = {
     [`${secretDB}.${secretCollection}`]: {
       fields: [
         {
           keyId: dek1,
           path: "patientId",
           bsonType: "int",
           queries: { queryType: "equality" },
         },
         {
           keyId: dek2,
           path: "medications",
           bsonType: "array",
         },
       ],
     },
   };
   const extraOptions = {
     cryptSharedLibPath: "<path to FLE Shared Library>",
   };
   const encClient = new MongoClient(uri, {
     autoEncryption: {
       keyVaultNamespace,
       kmsProviders,
       extraOptions,
       encryptedFieldsMap,
     },
   });
   await encClient.connect();
   const newEncDB = encClient.db(secretDB);
   // Drop the encrypted collection in case you created this collection
   // in a previous run of this application.
   await newEncDB.dropDatabase();
   await newEncDB.createCollection(secretCollection);
   console.log("Created encrypted collection!");
   ```

   The output from the code in this section should resemble the following:

   ```text
   Created encrypted collection!

   ```

   **See also: Complete Code**

   ### Node.js

   To view the complete code for making a Data Encryption Key, see [the Queryable Encryption sample application repository.](https://github.com/mongodb-university/docs-in-use-encryption-examples/tree/main/queryable-encryption/node/exp/reader/make_data_key.js)

4. Configure your MongoClient for Encrypted Reads and Writes

   Specify the Key Vault Collection Namespace

   Specify `encryption.__keyVault` as the Key Vault collection namespace.

   ### Node.js

   ```javascript
   const eDB = "encryption";
   const eKV = "__keyVault";
   const keyVaultNamespace = `${eDB}.${eKV}`;
   const secretDB = "medicalRecords";
   const secretCollection = "patients";
   ```

   Specify the Customer Master Key

   Specify the KMS provider and specify your Customer Master Key inline:

   ### Node.js

   ```javascript
   const fs = require("fs");
   const path = "./master-key.txt";
   // WARNING: Do not use a local key file in a production application
   const localMasterKey = fs.readFileSync(path);
   const kmsProviders = {
     local: {
       key: localMasterKey,
     },
   };
   ```

   Retrieve Data Encryption Keys

   Retrieve the Data Encryption Keys created in the [Create a Data Encryption Key](/docs/manual/core/queryable-encryption/tutorials/explicit-encryption#std-label-qe-manual-encryption-tutorial-data-key-create) step of this guide:

   ### Node.js

   ```javascript
   const uri = "<Your MongoDB URI>";
   const unencryptedClient = new MongoClient(uri);
   await unencryptedClient.connect();
   const keyVaultClient = unencryptedClient.db(eDB).collection(eKV);
   const dek1 = await keyVaultClient.findOne({ keyAltNames: "dataKey1" });
   const dek2 = await keyVaultClient.findOne({ keyAltNames: "dataKey2" });
   ```

   Specify the Path of the Automatic Encryption Shared Library

   ### Node.js

   ```javascript
   const extraOptions = {
     cryptSharedLibPath: "<path to crypt_shared library>",
   };
   ```

   **Tip: Learn More**

   To learn more about the library referenced by this path, see the [Automatic Encryption Shared Library](/docs/manual/core/queryable-encryption/install-library#std-label-qe-reference-shared-library) page.

   Create a MongoClient Object

   Instantiate a `MongoClient` object with the following automatic encryption settings:

   ### Node.js

   ```javascript
   const encryptedClient = new MongoClient(uri, {
     autoEncryption: {
       kmsProviders: kmsProviders,
       keyVaultNamespace: keyVaultNamespace,
       bypassQueryAnalysis: true,
       keyVaultClient: unencryptedClient,
       extraOptions: extraOptions,
     },
   });
   await encryptedClient.connect();
   ```

   **Note: Automatic Decryption**

   We use a `MongoClient` instance with automatic encryption enabled to perform automatic decryption.

   To learn more about explicit encryption with automatic decryption, see the [Fundamentals](/docs/manual/core/queryable-encryption/fundamentals#std-label-qe-fundamentals) section.

   Create a ClientEncryption Object

   Instantiate a `ClientEncryption` object as follows:

   ### Node.js

   ```javascript
   const encryption = new ClientEncryption(unencryptedClient, {
     keyVaultNamespace,
     kmsProviders,
   });
   ```

   **Note: Indexed and Unindexed Algorithms**

   To learn more about the indexed and unindexed algorithms in explicit encryption, see [Algorithms and QueryTypes.](/docs/manual/core/queryable-encryption/fundamentals/manual-encryption#std-label-qe-fundamentals-man-enc-algorithm-choice)

5. Insert a Document with Encrypted Fields

   Use your Queryable Encryption enabled `MongoClient` instance to insert a document with encrypted fields into the `medicalRecords.patients` namespace using the following code snippet:

   ### Node.js

   ```javascript
   const patientId = 12345678;
   const medications = ["Atorvastatin", "Levothyroxine"];

   const indexedInsertPayload = await encryption.encrypt(patientId, {
     algorithm: "Indexed",
     keyId: dek1._id,
     contentionFactor: 8,
   });
   const unindexedInsertPayload = await encryption.encrypt(medications, {
     algorithm: "Unindexed",
     keyId: dek2._id,
   });
   const encryptedColl = encryptedClient
     .db(secretDB)
     .collection(secretCollection);
   await encryptedColl.insertOne({
     firstName: "Jon",
     patientId: indexedInsertPayload,
     medications: unindexedInsertPayload,
   });
   ```

   When you insert a document, your Queryable Encryption enabled client encrypts the fields of your document such that it resembles the following:

   ```json
   {
     "_id": {
       "$oid": "6303e36053cc7ec2e6a630bd"
     },
     "firstName": "Jon",
     "patientId": {
       "$binary": {
         "base64": "BxLJUBmg703civqMz8ASsD4QEYeSneOGiiYHfLE77ELEkp1EC/fXPrKCNRQl2mAFddszqDJ0P3znKrq0DVMEvJoU6wa0Ra+U+JjNVr8NtJE+TpTLCannY5Av6iGfLAaiHbM/E8Ftz1YCQsArQwuNp3wIV/GJPLa2662xsyk0wz7F6IRGC3FlnxpN4UIFaHE1M7Y6kEnx3tEy5uJBvU4Sex7I2H0kqHthClH77Q6xHIHc8H9d6upvgnEbkKBCnmc24A2pSG/xZ7LBsV3j5aOboPISuN/lvg==",
         "subType": "06"
       }
     },
     "medications": {
       "$binary": {
         "base64": "BvOsveapfUxiuQxCMSM2fYIEyRlQaSqR+0NxlMarwurBflvoMz1FrSjSGgCVCpK8X+YrilP6Bac99kkaUmRJfjo4savxcjpOfEnUj5bHciPyfQBYmYF4PMLDtTTzGZpPilb9d5KgpIMBXxHi+dIcog==",
         "subType": "06"
       }
     },
     "__safeContent__": [
       {
         "$binary": {
           "base64": "ZLPIpgxzXpHUGrvdIHetwmMagR+mqvuUj5nzXNGf/WM=",
           "subType": "00"
         }
       }
     ]
   }

   ```

   **Warning: Do not Modify the \_\_safeContent\_\_ Field**

   The `__safeContent__` field is essential to Queryable Encryption. Do not modify the contents of this field.

   **See also: Complete Code**

   ### Node.js

   To view the complete code to insert a document encrypted with explicit encryption, see [the Queryable Encryption sample application repository.](https://github.com/mongodb-university/docs-in-use-encryption-examples/tree/main/queryable-encryption/node/exp/reader/insert_encrypted_document.js)

6. Retrieve Your Document with Encrypted Fields

   Retrieve the document with encrypted fields you inserted in the [Insert a Document with Encrypted Fields](/docs/manual/core/queryable-encryption/tutorials/explicit-encryption#std-label-qe-tutorials-manual-enc-insert) step of this guide through a query on an encrypted field:

   ### Node.js

   ```javascript
   const findPayload = await encryption.encrypt(patientId, {
     algorithm: "Indexed",
     keyId: dek1._id,
     queryType: "equality",
     contentionFactor: 8,
   });

   console.log("Finding a document with manually encrypted field:");
   console.log(await encryptedColl.findOne({ patientId: findPayload }));
   ```

   The output of the preceding code snippet should contain the following document:

   ```json
   {
     "__safeContent__": [
       {
         "Subtype": 0,
         "Data": "LfaIuWm9o30MIGrK7GGUoStJMSNOjRgbxy5q2TPiDes="
       }
     ],
     "_id": "6303a770857952ca5e363fd2",
     "firstName": "Jon",
     "medications": ["Atorvastatin", "Levothyroxine"],
     "patientId": 12345678
   }

   ```

   **See also: Complete Code**

   ### Node.js

   To view the code to retrieve your document with encrypted fields, see [the Queryable Encryption sample application repository.](https://github.com/mongodb-university/docs-in-use-encryption-examples/tree/main/queryable-encryption/node/exp/reader/insert_encrypted_document.js)

## Learn More

To view a tutorial on using Queryable Encryption with a remote KMS, see [Queryable Encryption Tutorials.](/docs/manual/core/queryable-encryption/tutorials#std-label-qe-tutorial-automatic-encryption)

To learn how Queryable Encryption works, see [Queryable Encryption with Explicit Encryption.](/docs/manual/core/queryable-encryption/fundamentals/manual-encryption#std-label-qe-fundamentals-manual-encryption)

To learn more about the topics mentioned in this guide, see the following links:

- [Encryption Keys and Key Vaults](/docs/manual/core/queryable-encryption/fundamentals/keys-key-vaults#std-label-qe-reference-keys-key-vaults)

- [KMS Providers](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-fundamentals-kms-providers)
