> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Queryable Encryption Quick Start

Queryable Encryption equality and range queries are fully supported in production. Prefix, suffix, and substring queries are only available in public preview in MongoDB 8.2. Do not enable these query types in production. GA functionality of prefix, suffix and substring query types will be incompatible with the preview feature. To learn more, see [Supported Query Types](https://www.mongodb.com/docs/manual/core/queryable-encryption/reference/supported-operations/).

This tutorial shows you how to build an application that implements the MongoDB Queryable Encryption feature to automatically encrypt and decrypt document fields.

The tutorial includes the following sections:

- **Set Up Your Project**: Install the driver and encryption dependencies, configure your environment variables, and create your project files with the required application variables.

- **Configure Encryption**: Create a Customer Master Key (CMK (Customer Master Key)), configure your KMS provider and automatic encryption settings, and create an encryption-enabled client and collection.

- **Perform Encrypted Operations**: Insert a document with encrypted fields, query on an encrypted field, and run the application to view the decrypted results.

Select your driver language in the drop-down menu to learn how to create an application that automatically encrypts and decrypts document fields.

**Important: Do Not Use this Sample Application In Production**

Because the instructions in this tutorial include storing an encryption key in an insecure environment, you should not use an unmodified version of this application in production. Using this application in production risks unauthorized access to the encryption key or loss of the key needed to decrypt your data. The purpose of this tutorial is to demonstrate how to use Queryable Encryption without needing to set up a Key Management System.

You can use a Key Management System to securely store your encryption key in a production environment. A KMS (Key Management System) is a remote service that securely stores and manages your encryption keys. To learn how to set up a Queryable Encryption enabled application that uses a KMS (Key Management System), see the [Queryable Encryption Tutorials.](/docs/manual/core/queryable-encryption/tutorials#std-label-qe-tutorial-automatic-encryption)

## Before You Begin

Before you begin this tutorial, complete the following prerequisite steps:

1. Download the Automatic Encryption Shared Library from the [MongoDB Download Center](https://www.mongodb.com/try/download/enterprise?tck=docs). Navigate to the MongoDB Enterprise Server Download section and select the following options:

   - In the Version dropdown, select the version marked as `"current"`.

   - In the Platform dropdown, select your platform.

   - In the Package dropdown, select `crypt_shared`.

   Extract the archive and save the path to the shared library file for future use.

   **Note: Query Analysis Component**

   The Automatic Encryption Shared Library is a preferred alternative to `mongocryptd` and does not require spawning a new process to perform automatic encryption. This tutorial uses the Automatic Encryption Shared Library.

2. Configure a MongoDB Atlas cluster or a local replica set deployment, and save your connection string for future use. To learn more, see the [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) tutorial.

   **Note:**

   MongoDB Community Edition [doesn't support](/docs/manual/core/queryable-encryption/reference/compatibility#std-label-qe-csfle-compatibility) Queryable Encryption with Automatic Encryption.

3. Ensure your database user has [`dbAdmin`](/docs/manual/reference/built-in-roles#mongodb-authrole-dbAdmin) permissions on the following namespaces:

   - `encryption.__keyVault`

   - `medicalRecords` database

### Full Application Code

[Complete mongosh Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/mongosh/)

To view the complete code for the sample application, see [Complete Node.js Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/node/)

**Tip: Driver Integration Tutorials**

To use the Mongoose library to implement Queryable Encryption, see [Tutorial: Queryable Encryption with Mongoose](https://www.mongodb.com/docs/drivers/node/current/integrations/mongoose/mongoose-qe/#std-label-node-mongoose-qe) in the Node.js driver documentation.

[Complete Python Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/python/)

**Tip: Driver Integration Tutorials**

To use Queryable Encryption in a Django application, see [Tutorial: Queryable Encryption with Django MongoDB Backend](https://www.mongodb.com/docs/languages/python/django-mongodb/current/queryable-encryption/#std-label-django-qe) in the Django MongoDB Backend documentation.

[Complete Java Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/java/)

[Complete Go Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/go/)

[Complete C# Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/csharp/)

[Complete Rust Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/rust/)

[Complete PHP Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/php/)

[Complete Ruby Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/ruby/)

## Procedure

### Set Up Your Project

Follow the steps in this section to create your project files and assign the required configuration variables.

1. Create your project directory.

   Create a directory named `shell-qe` to store your project files:

   ```bash
   mkdir shell-qe
   cd shell-qe
   ```

2. Set up your environment variables.

   In your `shell-qe` directory, create a `.envrc` file. The sample code in this tutorial references environment variables that you need to set in this `.envrc` file.

   Paste the following code into this file and replace the placeholder value with your own MongoDB deployment connection URI:

   ```bash

   export MONGODB_URI="<Your MongoDB URI>"

   ```

   After you create your `.envrc` file, run the following command to load the environment variables into your shell:

   ```bash
   source .envrc
   ```

   For more information on setting up environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/mongosh/README.md)  file included in the sample application on GitHub.

3. Create your main project file.

   In your `shell-qe` directory, create a file named `quickstart.js`. Paste the following starter code into this file. The placeholder comments indicate where you will add code in future steps of this tutorial:

   ```javascript
   const fs = require("fs");
   const crypto = require("crypto");

   async function runExample() {

     // Paste application variables below

     // Paste code to generate CMK below

     // Paste code to retrieve CMK and specify KMS provider settings below

     // Paste automatic encryption options code below

     // Paste client configuration code below

     // Paste schema below

     // Paste code to create an encrypted collection below

     // Paste code to insert a document below

     // Paste code to query the document below
   }

   runExample();
   ```

4. Assign your application variables.

   Declare the required application variables by pasting the following code into your `quickstart.js` file under the `// Paste application
               variables below` comment. For this tutorial, set the `kmsProviderName` variable to `"local"`.

   ```javascript
   const kmsProviderName = "<Your KMS Provider Name>";
   const uri = process.env.MONGODB_URI; // Your connection URI
   const keyVaultDatabaseName = "encryption";
   const keyVaultCollectionName = "__keyVault";
   const keyVaultNamespace = `${keyVaultDatabaseName}.${keyVaultCollectionName}`;
   const encryptedDatabaseName = "medicalRecords";
   const encryptedCollectionName = "patients";
   ```

   | Variable | Description |
   | --- | --- |
   | `kmsProviderName` | The KMS used to store your Customer Master Key. For this tutorial, set this variable to `"local"`. |
   | `uri` | Your MongoDB connection URI. Set with the `MONGODB_URI` environment variable. |
   | `keyVaultDatabaseName` | The database where DEKs are stored. Set to `"encryption"`. |
   | `keyVaultCollectionName` | The collection where DEKs are stored. Set to `"__keyVault"`. |
   | `keyVaultNamespace` | The namespace in MongoDB where your DEKs are stored. Set this variable to the values of the `keyVaultDatabaseName` and `keyVaultCollectionName` variables, separated by a period. |
   | `encryptedDatabaseName` | The database where encrypted data is stored. Set to `"medicalRecords"`. |
   | `encryptedCollectionName` | The collection where encrypted data is stored. Set to `"patients"`. |

### Configure Encryption

After you set up your project, follow the steps in this section to create an encryption key and configure your application for Queryable Encryption.

1. Create an encryption key.

   Paste the following code into your `quickstart.js` file under the `// Paste code to generate CMK below` comment. This code snippet creates a 96-byte Customer Master Key and saves it to your filesystem as the file `customer-master-key.txt`:

   ```javascript
   customerMasterKeyPath = "customer-master-key.txt";
   if (!fs.existsSync(customerMasterKeyPath)) {
     fs.writeFileSync(customerMasterKeyPath, crypto.randomBytes(96));
   }
   ```

   **Warning: Secure your Local Key File in Production**

   We recommend storing your Customer Master Keys in a remote [Key Management System](https://en.wikipedia.org/wiki/Key_management#Key_management_system) (KMS (Key Management System)). To learn how to use a remote KMS (Key Management System) in your Queryable Encryption implementation, see the [Queryable Encryption Tutorials](/docs/manual/core/queryable-encryption/tutorials#std-label-qe-tutorial-automatic-encryption) guide.

   If you choose to use a local key provider in production, exercise great caution and do not store it on the file system. Consider injecting the key into your client application using a sidecar process, or use another approach that keeps the key secure.

2. Retrieve the Customer Master Key and specify the KMS provider settings.

   Paste the following code into your `quickstart.js` file under the `// Paste code to retrieve CMK and specify KMS provider settings below` comment to retrieve the contents of the `customer-master-key.txt` file you generated in the previous step:

   ```javascript
   // WARNING: Do not use a local key file in a production application
   const localMasterKey = fs.readFileSync("./customer-master-key.txt");

   if (localMasterKey.length !== 96) {
     throw new Error(
       "Expected the customer master key file to be 96 bytes."
     );
   }

   kmsProviderCredentials = {
     local: {
       key: localMasterKey,
     },
   };
   ```

   This code sets the provider name to `local` to use a Local Key Provider and uses the CMK (Customer Master Key) value from your KMS provider settings.

3. Set your automatic encryption options.

   Add the following code under the `// Paste automatic encryption options code below` comment to create an `autoEncryptionOptions` object that contains the following options:

   - The namespace of your Key Vault collection

   - The `kmsProviders` object, defined in the previous step

   ```javascript
   const autoEncryptionOptions = {
     keyVaultNamespace: keyVaultNamespace,
     kmsProviders: kmsProviderCredentials,
   };
   ```

4. Create a client to set up an encrypted collection.

   Create a new client to encrypt and decrypt your collection. The client uses your connection URI and automatic encryption options. Paste the following code into your `quickstart.js` file, under the `// Paste client configuration code below` comment:

   ```javascript
   const encryptedClient = Mongo(uri, autoEncryptionOptions);
   ```

5. Specify fields to encrypt.

   To encrypt a field, add it to the encryption schema. To enable queries on a field, add the `queries` property. Paste the following code under the `// Paste schema below` comment:

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

   **Note:**

   In the previous code sample, both the `ssn` and `billing` fields are encrypted. However, only the `ssn` field can be queried because it contains the `queries` property.

6. Create your encrypted collection.

   Add the following code blocks to your `quickstart.js` file, under the `// Paste code to create an encrypted collection below` comment in the order shown.

   First, instantiate a `ClientEncryption` object to access the API for the encryption helper methods:

   ```javascript
   const clientEncryption = encryptedClient.getClientEncryption();
   ```

   Because you are using a local Customer Master Key, you don't need to provide Customer Master Key credentials. Create a variable containing an empty object to use in place of credentials when you create your encrypted collection.

   ```javascript
   customerMasterKeyCredentials = {};
   ```

   Create your encrypted collection by using the encryption helper method accessed through the `ClientEncryption` class. This method automatically generates data encryption keys for your encrypted fields and creates the encrypted collection:

   ```javascript
   await clientEncryption.createEncryptedCollection(
     encryptedDatabaseName,
     encryptedCollectionName,
     {
       provider: kmsProviderName,
       createCollectionOptions: collectionOpts,
       masterKey: customerMasterKeyCredentials,
     }
   );
   ```

### Perform Encrypted Operations

After you configure your application and database connection, you can insert and query encrypted documents.

1. Insert a document with encrypted fields.

   Paste the following code under the `// Paste code to insert a document below` comment to create a document that stores patient data and insert it into the `patients` collection:

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
     .getDB(encryptedDatabaseName)
     .getCollection(encryptedCollectionName);

   const insertResult = await encryptedCollection.insertOne(patientDocument);
   ```

2. Query on encrypted data.

   Add the following code to your `quickstart.js` file under the `// Paste code to query the document below` comment:

   ```javascript
   const findResult = await encryptedCollection.findOne({
     "patientRecord.ssn": "987-65-4320",
   });
   console.log(findResult);
   ```

3. Run your application.

   To start your application, run the following command from your project directory:

   ```bash
   mongosh -f quickstart.js
   ```

   **Note:**

   If your `mongosh` installation requires you to specify the path to your shared library, you can use the following command:

   ```bash
   mongosh --cryptSharedLibPath "<path-to-shared-library>" -f quickstart.js
   ```

   The output of the preceding code sample should look similar to the following:

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

### Set Up Your Project

Follow the steps in this section to create your project files and assign the required configuration variables.

1. Install dependencies.

   Create a directory named `nodeQE` to store your project files. Run the following commands to navigate into the directory, initialize your project, and install the required packages:

   ```bash
   cd nodeQE
   npm init -y
   npm install mongodb-client-encryption dotenv
   ```

   Then, open the generated `package.json` file. To use [ECMAScript modules](https://nodejs.org/api/esm.html#modules-ecmascript-modules), the standard format for packaging JavaScript code for reuse, replace the existing line that specifies the `"type"` field with the following line:

   ```json
   "type": "module"
   ```

2. Set up your environment variables.

   In your `nodeQE` directory, create a `.env` file. The sample code in this tutorial references environment variables that you need to set in this `.env` file. Paste the following code into this file:

   ```text

   MONGODB_URI="<Your MongoDB URI>"
   SHARED_LIB_PATH="<Full path to your Automatic Encryption Shared Library>"

   ```

   Replace the following placeholder values:

   - `<Your MongoDB URI>`: Your MongoDB deployment connection URI.

   - `<Full path to your Automatic Encryption Shared Library>`: The full path to your Automatic Encryption Shared Library, which resembles the following paths:

     - **macOS**: `/<crypt shared directory>/lib/mongo_crypt_v1.dylib`

     - **Linux**: `/<crypt shared directory>/lib/mongo_crypt_v1.so`

     - **Windows**: `C:\<crypt shared directory>\bin\mongo_crypt_v1.dll`

   For more information on setting up environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/node/README.md)  file included in the sample application on GitHub.

3. Create your main project file.

   In your `nodeQE` directory, create a file named `quickstart.js`. Paste the following starter code into this file. The placeholder comments indicate where you will add code in future steps of this tutorial:

   ```javascript
   import "dotenv/config";
   import { existsSync, writeFileSync, readFileSync } from "node:fs";
   import { randomBytes } from "node:crypto";
   import { MongoClient } from "mongodb";
   import { ClientEncryption } from "mongodb";

   async function runExample() {

     // Paste application variables below

     // Paste code to generate CMK below

     // Paste code to retrieve CMK and specify KMS provider settings below

     // Paste automatic encryption options code below

     // Paste client configuration code below

     // Paste schema below

     // Paste code to create an encrypted collection below

     // Paste code to insert a document below

     // Paste code to query the document below
   }

   runExample().catch(console.dir);
   ```

   **Note: Import ClientEncryption**

   When using the Node.js driver v6.0 and later, you must import `ClientEncryption` from `mongodb`.

   For earlier driver versions, import `ClientEncryption` from `mongodb-client-encryption`.

4. Assign your application variables.

   Declare the required application variables by pasting the following code into your `quickstart.js` file under the `// Paste application variables below` comment. For this tutorial, set the `kmsProviderName` variable to `"local"`.

   ```javascript
   const kmsProviderName = "<Your KMS Provider Name>";

   const uri = process.env.MONGODB_URI; // Your connection URI

   const keyVaultDatabaseName = "encryption";
   const keyVaultCollectionName = "__keyVault";
   const keyVaultNamespace = `${keyVaultDatabaseName}.${keyVaultCollectionName}`;
   const encryptedDatabaseName = "medicalRecords";
   const encryptedCollectionName = "patients";
   ```

   The following table describes each application variable in the code snippet:

   | Variable | Description |
   | --- | --- |
   | `kmsProviderName` | The KMS used to store your Customer Master Key. For this tutorial, set this variable to `"local"`. |
   | `uri` | Your MongoDB connection URI. Set with the `MONGODB_URI` environment variable. |
   | `keyVaultDatabaseName` | The database where DEKs are stored. Set to `"encryption"`. |
   | `keyVaultCollectionName` | The collection where DEKs are stored. Set to `"__keyVault"`. |
   | `keyVaultNamespace` | The namespace in MongoDB where your DEKs are stored. Set this variable to the values of the `keyVaultDatabaseName` and `keyVaultCollectionName` variables, separated by a period. |
   | `encryptedDatabaseName` | The database where encrypted data is stored. Set to `"medicalRecords"`. |
   | `encryptedCollectionName` | The collection where encrypted data is stored. Set to `"patients"`. |

### Configure Encryption

After you set up your project, follow the steps in this section to create an encryption key and configure your application for Queryable Encryption.

1. Create an encryption key.

   Paste the following code into your `quickstart.js` file under the `// Paste code to generate CMK below` comment. This code snippet creates a 96-byte Customer Master Key and saves it to your filesystem as the file `customer-master-key.txt`:

   ```javascript
   if (!existsSync("./customer-master-key.txt")) {
     try {
       writeFileSync("customer-master-key.txt", randomBytes(96));
     } catch (err) {
       throw new Error(
         `Unable to write Customer Master Key to file due to the following error: ${err}`
       );
     }
   }
   ```

   **Warning: Secure your Local Key File in Production**

   We recommend storing your Customer Master Keys in a remote [Key Management System](https://en.wikipedia.org/wiki/Key_management#Key_management_system) (KMS (Key Management System)). To learn how to use a remote KMS (Key Management System) in your Queryable Encryption implementation, see the [Queryable Encryption Tutorials](/docs/manual/core/queryable-encryption/tutorials#std-label-qe-tutorial-automatic-encryption) guide.

   If you choose to use a local key provider in production, exercise great caution and do not store it on the file system. Consider injecting the key into your client application using a sidecar process, or use another approach that keeps the key secure.

2. Retrieve the Customer Master Key and specify the KMS provider settings.

   Paste the following code into your `quickstart.js` file under the `// Paste code to retrieve CMK and specify KMS provider settings below` comment to retrieve the contents of the `customer-master-key.txt` file you generated in the previous step:

   ```javascript
   // WARNING: Do not use a local key file in a production application
   const localMasterKey = readFileSync("./customer-master-key.txt");

   if (localMasterKey.length !== 96) {
     throw new Error(
       "Expected the customer master key file to be 96 bytes."
     );
   }

   kmsProviders = {
     local: {
       key: localMasterKey,
     },
   };
   ```

   This code sets the provider name to `local` to use a Local Key Provider and uses the CMK (Customer Master Key) value from your KMS provider settings.

3. Set your automatic encryption options.

   Add the following code under the `// Paste automatic encryption options code below` comment to create an `autoEncryptionOptions` object that contains the following options:

   - The namespace of your Key Vault collection

   - The `kmsProviders` object, defined in the previous step

   - The `sharedLibraryPathOptions` object, which contains the path to your Automatic Encryption Shared Library

   ```javascript
   const extraOptions = {
     cryptSharedLibPath: process.env.SHARED_LIB_PATH, // Path to your Automatic Encryption Shared Library
   };

   const autoEncryptionOptions = {
     keyVaultNamespace,
     kmsProviders,
     extraOptions,
   };
   ```

4. Create a client to set up an encrypted collection.

   Create a new client to encrypt and decrypt your collection. The client uses your connection URI and automatic encryption options. Paste the following code into your `quickstart.js` file, under the `// Paste client configuration code below` comment:

   ```javascript
   const encryptedClient = new MongoClient(uri, {
     autoEncryption: autoEncryptionOptions,
   });
   ```

5. Specify fields to encrypt.

   To encrypt a field, add it to the encryption schema. To enable queries on a field, add the `queries` property. Paste the following code under the `// Paste schema below` comment:

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

   **Note:**

   The previous code sample encrypts both the `ssn` and `billing` fields. However, only the `ssn` field can be queried because it contains the `queries` property.

6. Create your encrypted collection.

   Add the following code blocks to your `quickstart.js` file, under the `// Paste code to create an encrypted collection below` comment in the order shown.

   First, instantiate a `ClientEncryption` object to access the API for the encryption helper methods:

   ```javascript
   const clientEncryption = new ClientEncryption(
     encryptedClient,
     autoEncryptionOptions
   );
   ```

   Because you are using a local Customer Master Key, you don't need to provide Customer Master Key credentials. Create a variable containing an empty object to use in place of credentials when you create your encrypted collection.

   ```javascript
   customerMasterKeyCredentials = {};
   ```

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

### Perform Encrypted Operations

After you configure your application and database connection, you can insert and query encrypted documents.

1. Insert a document with encrypted fields.

   Paste the following code under the `// Paste code to insert a document below` comment to create a document that stores patient data and insert it into the `patients` collection:

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

2. Query on encrypted data.

   Add the following code to your `quickstart.js` file under the `// Paste code to query the document below` comment:

   ```javascript
   const findResult = await encryptedCollection.findOne({
     "patientRecord.ssn": "987-65-4320",
   });
   console.log(findResult);
   ```

3. Run your application.

   To start your application, run the following command from your project directory:

   ```bash
   node quickstart.js
   ```

   The output of the preceding code sample should look similar to the following:

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

### Set Up Your Project

Follow the steps in this section to create your project files and assign the required configuration variables.

1. Install dependencies.

   Create a directory named `python-qe` to store your project files. Run the following commands to navigate into the directory and create a virtual environment:

   ```bash
   cd python-qe
   python3 -m venv venv
   source venv/bin/activate
   ```

   Then, install the required packages:

   ```bash
   python3 -m pip install pymongo pymongocrypt python-dotenv
   ```

2. Set up your environment variables.

   In your `python-qe` directory, create a `.env` file. The sample code in this tutorial references environment variables that you need to set in this `.env` file. Paste the following code into this file:

   ```text

   export MONGODB_URI="<Your MongoDB URI>"
   export SHARED_LIB_PATH="<Full path to your Automatic Encryption Shared Library>"

   ```

   Replace the following placeholder values:

   - `<Your MongoDB URI>`: Your MongoDB deployment connection URI.

   - `<Full path to your Automatic Encryption Shared Library>`: The full path to your Automatic Encryption Shared Library, which resembles the following paths:

     - **macOS**: `/<crypt shared directory>/lib/mongo_crypt_v1.dylib`

     - **Linux**: `/<crypt shared directory>/lib/mongo_crypt_v1.so`

     - **Windows**: `C:\<crypt shared directory>\bin\mongo_crypt_v1.dll`

   For more information on setting up environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/python/README.md)  file included in the sample application on GitHub.

3. Create your main project file.

   In your `python-qe` directory, create a file named `quickstart.py`. Paste the following starter code into this file. The placeholder comments indicate where you will add code in future steps of this tutorial:

   ```python
   import os
   from dotenv import load_dotenv
   from pymongo import MongoClient
   from pymongo.encryption import ClientEncryption
   from pymongo.encryption_options import AutoEncryptionOpts
   from bson.codec_options import CodecOptions
   from bson.binary import STANDARD

   load_dotenv()

   # Paste application variables below

   # Paste code to generate CMK below

   # Paste code to retrieve CMK and specify KMS provider settings below

   # Paste automatic encryption options code below

   # Paste client configuration code below

   # Paste schema below

   # Paste code to create an encrypted collection below

   # Paste code to insert a document below

   # Paste code to query the document below
   ```

4. Assign your application variables.

   Declare the required application variables by pasting the following code into your `quickstart.py` file under the `# Paste application variables below` comment. For this tutorial, set the `kms_provider_name` variable to `"local"`.

   ```python
   kms_provider_name = "<KMS provider name>"
   uri = os.environ.get("MONGODB_URI", "mongodb://127.0.0.1:27017")  # Your connection URI
   key_vault_database_name = "encryption"
   key_vault_collection_name = "__keyVault"
   key_vault_namespace = f"{key_vault_database_name}.{key_vault_collection_name}"
   encrypted_database_name = "medicalRecords"
   encrypted_collection_name = "patients"
   ```

   The following table describes each application variable in the code snippet:

   | Variable | Description |
   | --- | --- |
   | `kms_provider_name` | The KMS used to store your Customer Master Key. For this tutorial, set this variable to `"local"`. |
   | `uri` | Your MongoDB connection URI. Set with the `MONGODB_URI` environment variable. |
   | `key_vault_database_name` | The database where DEKs are stored. Set to `"encryption"`. |
   | `key_vault_collection_name` | The collection where DEKs are stored. Set to `"__keyVault"`. |
   | `key_vault_namespace` | The namespace in MongoDB where your DEKs are stored. Set this variable to the values of the `key_vault_database_name` and `key_vault_collection_name` variables, separated by a period. |
   | `encrypted_database_name` | The database where encrypted data is stored. Set to `"medicalRecords"`. |
   | `encrypted_collection_name` | The collection where encrypted data is stored. Set to `"patients"`. |

### Configure Encryption

After you set up your project, follow the steps in this section to create an encryption key and configure your application for Queryable Encryption.

1. Create an encryption key.

   Paste the following code into your `quickstart.py` file under the `# Paste code to generate CMK below` comment. This code snippet creates a 96-byte Customer Master Key and saves it to your filesystem as the file `customer-master-key.txt`:

   ```python
   path = "customer-master-key.txt"
   file_bytes = os.urandom(96)
   with open(path, "wb") as f:
       f.write(file_bytes)
   ```

   **Warning: Secure your Local Key File in Production**

   We recommend storing your Customer Master Keys in a remote [Key Management System](https://en.wikipedia.org/wiki/Key_management#Key_management_system) (KMS (Key Management System)). To learn how to use a remote KMS (Key Management System) in your Queryable Encryption implementation, see the [Queryable Encryption Tutorials](/docs/manual/core/queryable-encryption/tutorials#std-label-qe-tutorial-automatic-encryption) guide.

   If you choose to use a local key provider in production, exercise great caution and do not store it on the file system. Consider injecting the key into your client application using a sidecar process, or use another approach that keeps the key secure.

2. Retrieve the Customer Master Key and specify the KMS provider settings.

   Paste the following code into your `quickstart.py` file under the `# Paste code to retrieve CMK and specify KMS provider settings below` comment to retrieve the contents of the `customer-master-key.txt` file you generated in the previous step:

   ```python
   path = "./customer-master-key.txt"
   with open(path, "rb") as f:
       local_master_key = f.read()
       if len(local_master_key) != 96:
           raise Exception("Expected the customer master key file to be 96 bytes.")
       kms_provider_credentials = {
           "local": {
               "key": local_master_key
           },
       }
   ```

   This code sets the provider name to `local` to use a Local Key Provider and uses the CMK (Customer Master Key) value from your KMS provider settings.

3. Set your automatic encryption options.

   Add the following code under the `# Paste automatic encryption options code below` comment to create an `AutoEncryptionOpts` object that contains the following options:

   - The `kms_provider_credentials` object, defined in the previous step

   - The namespace of your Key Vault collection

   - The path to your Automatic Encryption Shared Library

   ```python
   auto_encryption_options = AutoEncryptionOpts(
       kms_provider_credentials,
       key_vault_namespace,
       crypt_shared_lib_path=os.environ['SHARED_LIB_PATH'] # Path to your Automatic Encryption Shared Library>
   )
   ```

4. Create a client to set up an encrypted collection.

   Create a new client to encrypt and decrypt your collection. The client uses your connection URI and automatic encryption options. Paste the following code into your `quickstart.py` file, under the `# Paste client configuration code below` comment:

   ```python
   encrypted_client = MongoClient(
       uri, auto_encryption_opts=auto_encryption_options)
   ```

5. Specify fields to encrypt.

   To encrypt a field, add it to the encryption schema. To enable queries on a field, add the `queries` property. Paste the following code under the `# Paste schema below` comment:

   ```python
   encrypted_fields = {
       "fields": [
           {
               "path": "patientRecord.ssn",
               "bsonType": "string",
               "queries": [{"queryType": "equality"}]
           },
           {
               "path": "patientRecord.billing",
               "bsonType": "object",
           }
       ]
   }
   ```

   **Note:**

   The previous code sample encrypts both the `ssn` and `billing` fields. However, only the `ssn` field can be queried because it contains the `queries` property.

6. Create your encrypted collection.

   Add the following code blocks to your `quickstart.py` file, under the `# Paste code to create an encrypted collection below` comment in the order shown.

   First, instantiate a `ClientEncryption` object to access the API for the encryption helper methods:

   ```python
   client_encryption = ClientEncryption(
       kms_providers=kms_provider_credentials,
       key_vault_namespace=key_vault_namespace,
       key_vault_client=encrypted_client,
       codec_options=CodecOptions(uuid_representation=STANDARD)
   )
   ```

   Because you are using a local Customer Master Key, you don't need to provide Customer Master Key credentials. Create a variable containing an empty object to use in place of credentials when you create your encrypted collection.

   ```python
   customer_master_key_credentials = {}
   ```

   Create your encrypted collection by using the encryption helper method accessed through the `ClientEncryption` class. This method automatically generates data encryption keys for your encrypted fields and creates the encrypted collection:

   ```python
   client_encryption.create_encrypted_collection(
       encrypted_client[encrypted_database_name],
       encrypted_collection_name,
       encrypted_fields,
       kms_provider_name,
       customer_master_key_credentials,
   )
   ```

### Perform Encrypted Operations

After you configure your application and database connection, you can insert and query encrypted documents.

1. Insert a document with encrypted fields.

   Paste the following code under the `# Paste code to insert a document below` comment to create a document that stores patient data and insert it into the `patients` collection:

   ```python
   patient_document = {
       "patientName": "Jon Doe",
       "patientId": 12345678,
       "patientRecord": {
           "ssn": "987-65-4320",
           "billing": {
               "type": "Visa",
               "number": "4111111111111111",
           },
           "billAmount": 1500,
       },
   }

   encrypted_collection = encrypted_client[encrypted_database_name][encrypted_collection_name]

   result = encrypted_collection.insert_one(patient_document)
   ```

2. Query on encrypted data.

   Add the following code to your `quickstart.py` file under the `# Paste code to query the document below` comment:

   ```python
   find_result = encrypted_collection.find_one({
       "patientRecord.ssn": "987-65-4320"
   })

   print(find_result)
   ```

3. Run your application.

   To start your application, run the following command from your project directory:

   ```bash
   python3 quickstart.py
   ```

   The output of the preceding code sample should look similar to the following:

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

### Set Up Your Project

Follow the steps in this section to create your project files and assign the required configuration variables.

1. Install dependencies.

   This tutorial uses Apache Maven to manage dependencies. In an Integrated Development Environment (IDE), create a new Maven project named `JavaQE`. Then, navigate to the `pom.xml` file and add the following dependencies:

   ```xml
   <project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
     <modelVersion>4.0.0</modelVersion>
     <groupId>com.mongodb.tutorials</groupId>
     <artifactId>queryable-encryption-tutorial</artifactId>
     <version>1.0-SNAPSHOT</version>

     <properties>
       <maven.compiler.source>11</maven.compiler.source>
       <maven.compiler.target>11</maven.compiler.target>
     </properties>

     <dependencies>

       <dependency>
         <groupId>org.mongodb</groupId>
         <artifactId>mongodb-driver-sync</artifactId>
         <version>4.10.1</version>
       </dependency>
       <dependency>
         <groupId>org.mongodb</groupId>
         <artifactId>mongodb-driver-core</artifactId>
         <version>4.10.1</version>
       </dependency>
       <dependency>
         <groupId>org.mongodb</groupId>
         <artifactId>bson</artifactId>
         <version>4.10.1</version>
       </dependency>

       <dependency>
         <groupId>org.mongodb</groupId>
         <artifactId>mongodb-crypt</artifactId>
         <version>1.8.0</version>
       </dependency>

       <dependency>
         <groupId>io.github.cdimascio</groupId>
         <artifactId>dotenv-java</artifactId>
         <version>3.0.0</version>
       </dependency>

     </dependencies>

     <build>
       <plugins>
         <plugin>
           <groupId>org.apache.maven.plugins</groupId>
           <artifactId>maven-assembly-plugin</artifactId>
           <version>3.6.0</version>
           <executions>
             <execution>
               <phase>package</phase>
               <goals>
                 <goal>single</goal>
               </goals>
             </execution>
           </executions>
           <configuration>
             <archive>
               <manifest>
                 <mainClass>com.mongodb.tutorials.qe.QueryableEncryptionTutorial</mainClass>
                 <addClasspath>true</addClasspath>
               </manifest>
             </archive>
             <descriptorRefs>
               <descriptorRef>jar-with-dependencies</descriptorRef>
             </descriptorRefs>
             <appendAssemblyId>false</appendAssemblyId>
             <finalName>${project.artifactId}</finalName>
           </configuration>
         </plugin>
       </plugins>
       <finalName>${project.artifactId}</finalName>
     </build>
   </project>

   ```

   This code installs the MongoDB Java Sync Driver and the `mongodb-crypt` package, which provides the necessary classes for Queryable Encryption. It also installs the `dotenv-java` package, which reads your credentials from a `.env` file.

2. Set up your environment variables.

   In your `JavaQE` directory, create a file named `.env`. The sample code in this tutorial reads its configuration from this file. Paste the following code into this file:

   ```bash
   # MongoDB connection uri and automatic encryption shared library path

   MONGODB_URI="<Your MongoDB URI>"
   SHARED_LIB_PATH="<Full path to your Automatic Encryption Shared Library>"

   ```

   Replace the following placeholder values:

   - `<Your MongoDB URI>`: Your MongoDB deployment connection URI.

   - `<Full path to your Automatic Encryption Shared Library>`: The full path to your Automatic Encryption Shared Library, which resembles the following paths:

     - **macOS**: `/<crypt shared directory>/lib/mongo_crypt_v1.dylib`

     - **Linux**: `/<crypt shared directory>/lib/mongo_crypt_v1.so`

     - **Windows**: `C:\<crypt shared directory>\bin\mongo_crypt_v1.dll`

   For more information on setting up your environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/java/README.md) file included in the sample application on GitHub.

3. Create your data model classes.

   This tutorial uses Plain Old Java Objects (POJOs) as data models to represent the document structure. In your `src/main/java/com/mongodb/tutorials/qe/models` directory, create a file named `Patient.java` and paste the following `Patient` class into the file:

   ```java
   package com.mongodb.tutorials.qe.models;

   import org.bson.types.ObjectId;

   public class Patient {
       public ObjectId id;
       public String patientName;

       public PatientRecord patientRecord;

       public Patient() {
       }

       public Patient(String name, PatientRecord patientRecord) {
           this.patientName = name;
           this.patientRecord = patientRecord;
       }

       public ObjectId getId() {
           return id;
       }

       public void setId(ObjectId id) {
           this.id = id;
       }

       public String getPatientName() {
           return patientName;
       }

       public void setPatientName(String name) {
           this.patientName = name;
       }

       public PatientRecord getPatientRecord() {
           return patientRecord;
       }

       public void setPatientRecord(PatientRecord patientRecord) {
           this.patientRecord = patientRecord;
       }

       @Override
       public String toString() {
           return "{" +
                   "id=" + id +
                   ", name='" + patientName + '\'' +
                   ", patientRecord=" + patientRecord +
                   '}';
       }
   }
   ```

   Then, create a file named `PatientRecord.java` and paste the following `PatientRecord` class into the file:

   ```java
   package com.mongodb.tutorials.qe.models;

   public class PatientRecord {
       public String ssn;
       public PatientBilling billing;
       public int billAmount;

       public PatientRecord() {
       }

       public PatientRecord(String ssn, PatientBilling billing, int billAmount) {
           this.ssn = ssn;
           this.billing = billing;
           this.billAmount = billAmount;
       }

       public String getSsn() {
           return ssn;
       }

       public void setSsn(String ssn) {
           this.ssn = ssn;
       }

       public PatientBilling getBilling() {
           return billing;
       }

       public void setBilling(PatientBilling billing) {
           this.billing = billing;
       }

       public int getBillAmount() {
           return billAmount;
       }

       public void setBillAmount(int billAmount) {
           this.billAmount = billAmount;
       }

       @Override
       public String toString() {
           return "{" +
                   "ssn='" + ssn + '\'' +
                   ", billing=" + billing +
                   ", billAmount=" + billAmount +
                   '}';
       }
   }
   ```

   Finally, create a file named `PatientBilling.java` and paste the following `PatientBilling` class into the file:

   ```java
   package com.mongodb.tutorials.qe.models;

   public class PatientBilling {
       public String cardType;
       public String cardNumber;

       public PatientBilling() {
       }

       public PatientBilling(String cardType, String cardNumber) {
           this.cardType = cardType;
           this.cardNumber = cardNumber;
       }

       public String getCardType() {
           return cardType;
       }

       public void setCardType(String cardType) {
           this.cardType = cardType;
       }

       public String getCardNumber() {
           return cardNumber;
       }

       public void setCardNumber(String cardNumber) {
           this.cardNumber = cardNumber;
       }

       @Override
       public String toString() {
           return "{" +
                   "cardType='" + cardType + '\'' +
                   ", cardNumber='" + cardNumber + '\'' +
                   '}';
       }
   }
   ```

   To learn more about Java POJOs, see the [Plain Old Java Object](https://en.wikipedia.org/wiki/Plain_old_Java_object) Wikipedia article.

4. Create your application file.

   In your `src/main/java/com/mongodb/tutorials/qe` directory, create a file named `QueryableEncryptionTutorial.java`. This file contains the main Queryable Encryption workflow. Paste the following starter code into this file. The placeholder comments indicate where you add code in later steps of this tutorial:

   ```java
   package com.mongodb.tutorials.qe;

   import com.mongodb.AutoEncryptionSettings;
   import com.mongodb.ClientEncryptionSettings;
   import com.mongodb.ConnectionString;
   import com.mongodb.MongoClientSettings;
   import com.mongodb.client.MongoClient;
   import com.mongodb.client.MongoClients;
   import com.mongodb.client.MongoCollection;
   import com.mongodb.client.MongoDatabase;
   import com.mongodb.client.model.CreateCollectionOptions;
   import com.mongodb.client.model.CreateEncryptedCollectionParams;
   import com.mongodb.client.result.InsertOneResult;
   import com.mongodb.client.vault.ClientEncryption;
   import com.mongodb.client.vault.ClientEncryptions;
   import com.mongodb.tutorials.qe.models.Patient;
   import com.mongodb.tutorials.qe.models.PatientBilling;
   import com.mongodb.tutorials.qe.models.PatientRecord;
   import io.github.cdimascio.dotenv.Dotenv;
   import org.bson.BsonArray;
   import org.bson.BsonDocument;
   import org.bson.BsonNull;
   import org.bson.BsonString;
   import org.bson.codecs.configuration.CodecProvider;
   import org.bson.codecs.configuration.CodecRegistry;
   import org.bson.codecs.pojo.PojoCodecProvider;

   import java.io.File;
   import java.io.FileInputStream;
   import java.io.FileOutputStream;
   import java.security.SecureRandom;
   import java.util.Arrays;
   import java.util.HashMap;
   import java.util.Map;

   import static com.mongodb.MongoClientSettings.getDefaultCodecRegistry;
   import static org.bson.codecs.configuration.CodecRegistries.fromProviders;
   import static org.bson.codecs.configuration.CodecRegistries.fromRegistries;

   public class QueryableEncryptionTutorial {

       // Loads values from your .env file
       // Later steps call getEnv() to read your configuration values
       static class QueryableEncryptionHelpers {
           private static final Dotenv dotEnv = Dotenv.configure()
                   .directory("./.env")
                   .load();

           public static String getEnv(String name) {
               return dotEnv.get(name);
           }
       }

       static String getEnv(String name) {
           return QueryableEncryptionHelpers.getEnv(name);
       }

       public static void main(String[] args) throws Exception {
           // Paste application variables below


           // Paste code to generate CMK below


           // Paste code to retrieve the CMK and specify KMS provider settings below


           // Paste automatic encryption options code below


           // Paste client settings code below


           try (MongoClient encryptedClient = MongoClients.create(clientSettings)) {

               // Paste schema below


               // Paste code to create an encrypted collection below


               // Paste code to insert a document below


               // Paste code to query the document below

           }
       }
   }
   ```

5. Assign your application variables.

   The code samples in this tutorial use the following variables to perform the Queryable Encryption workflow. Paste the following code into the `main()` method of `QueryableEncryptionTutorial.java`, under the `// Paste application variables below` comment. For this tutorial, set the `kmsProviderName` variable to `"local"`:

   ```java
   String kmsProviderName = "<KMS provider name>";
   String uri = QueryableEncryptionHelpers.getEnv("MONGODB_URI"); // Your connection URI
   String keyVaultDatabaseName = "encryption";
   String keyVaultCollectionName = "__keyVault";
   String keyVaultNamespace = keyVaultDatabaseName + "." + keyVaultCollectionName;
   String encryptedDatabaseName = "medicalRecords";
   String encryptedCollectionName = "patients";
   ```

   | Variable | Description |
   | --- | --- |
   | `kmsProviderName` | The KMS that stores your Customer Master Key. For this tutorial, set this variable to `"local"`. |
   | `uri` | Your MongoDB connection URI. Set with the `MONGODB_URI` environment variable in your `.env` file. |
   | `keyVaultDatabaseName` | The database that stores your DEKs. Set to `"encryption"`. |
   | `keyVaultCollectionName` | The collection that stores your DEKs. Set to `"__keyVault"`. |
   | `keyVaultNamespace` | The namespace in MongoDB that stores your DEKs. Set this variable to the values of the `keyVaultDatabaseName` and `keyVaultCollectionName` variables, separated by a period. |
   | `encryptedDatabaseName` | The database that stores your encrypted data. Set to `"medicalRecords"`. |
   | `encryptedCollectionName` | The collection that stores your encrypted data. Set to `"patients"`. |

### Configure Encryption

After you set up your project, follow the steps in this section to create an encryption key and configure your application for Queryable Encryption.

1. Create an encryption key.

   Paste the following code into your `QueryableEncryptionTutorial.java` file under the `// Paste code to generate CMK below` comment. This code creates a 96-byte Customer Master Key and saves it to your filesystem as the file `customer-master-key.txt`:

   ```java
   // Reuse the key from the customer-master-key.txt file if it exists
   if (!new File("./customer-master-key.txt").isFile()) {
       byte[] localCustomerMasterKey = new byte[96];
       new SecureRandom().nextBytes(localCustomerMasterKey);
       try (FileOutputStream stream = new FileOutputStream("customer-master-key.txt")) {
           stream.write(localCustomerMasterKey);
       } catch (Exception e) {
           throw new Exception("Unable to write Customer Master Key file due to the following error:" + e.getMessage());
       }
   }
   ```

   **Warning: Secure your Local Key File in Production**

   We recommend storing your Customer Master Keys in a remote [Key Management System](https://en.wikipedia.org/wiki/Key_management#Key_management_system) (KMS (Key Management System)). To learn how to use a remote KMS (Key Management System) in your Queryable Encryption implementation, see the [Queryable Encryption Tutorials](/docs/manual/core/queryable-encryption/tutorials#std-label-qe-tutorial-automatic-encryption) guide.

   If you choose to use a local key provider in production, exercise great caution and do not store it on the file system. Consider injecting the key into your client application using a sidecar process, or use another approach that keeps the key secure.

2. Retrieve the Customer Master Key and specify the KMS provider settings.

   Paste the following code under the `// Paste code to retrieve
               the CMK and specify KMS provider settings below` comment. This code retrieves the contents of the `customer-master-key.txt` file and uses the CMK (Customer Master Key) value in your KMS provider settings. Setting the provider name to `local` indicates that you are using a Local Key Provider:

   ```java
   byte[] localCustomerMasterKey = new byte[96];

   try (FileInputStream fis = new FileInputStream("customer-master-key.txt")) {
       if (fis.read(localCustomerMasterKey) != 96)
           throw new Exception("Expected the customer master key file to be 96 bytes.");
   } catch (Exception e) {
       throw new Exception("Unable to read the Customer Master Key due to the following error: " + e.getMessage());
   }
   Map<String, Object> keyMap = new HashMap<String, Object>();
   keyMap.put("key", localCustomerMasterKey);

   Map<String, Map<String, Object>> kmsProviderCredentials = new HashMap<String, Map<String, Object>>();
   kmsProviderCredentials.put("local", keyMap);
   ```

3. Set your automatic encryption options.

   Paste the following code under the `// Paste automatic
               encryption options code below` comment. This code creates an `AutoEncryptionSettings` object that contains the following options:

   - The namespace of your Key Vault collection

   - The `kmsProviderCredentials` object, defined in the previous step

   - The `extraOptions` object, which contains the path to your Automatic Encryption Shared Library

   ```java
   Map<String, Object> extraOptions = new HashMap<String, Object>();
   extraOptions.put("cryptSharedLibPath", getEnv("SHARED_LIB_PATH")); // Path to your Automatic Encryption Shared Library

   AutoEncryptionSettings autoEncryptionSettings = AutoEncryptionSettings.builder()
           .keyVaultNamespace(keyVaultNamespace)
           .kmsProviders(kmsProviderCredentials)
           .extraOptions(extraOptions)
           .build();
   ```

4. Create a client to set up an encrypted collection.

   To create a client that encrypts and decrypts data in your collection, paste the following code under the `// Paste client
               settings code below` comment. This code builds the `clientSettings` object from your connection URI and your automatic encryption options:

   ```java
   MongoClientSettings clientSettings = MongoClientSettings.builder()
           .applyConnectionString(new ConnectionString(uri))
           .autoEncryptionSettings(autoEncryptionSettings)
           .build();

   ```

   The `try` block in your starter code passes these settings to `MongoClients.create()` to instantiate the encrypted client.

5. Specify fields to encrypt.

   To encrypt a field, add it to the encryption schema. To enable queries on a field, add the `queries` property. Paste the following code under the `// Paste schema below` comment:

   ```java
   BsonDocument encryptedFields = new BsonDocument().append("fields",
           new BsonArray(Arrays.asList(
                   new BsonDocument()
                           .append("keyId", new BsonNull())
                           .append("path", new BsonString("patientRecord.ssn"))
                           .append("bsonType", new BsonString("string"))
                           .append("queries", new BsonDocument()
                                   .append("queryType", new BsonString("equality"))),
                   new BsonDocument()
                           .append("keyId", new BsonNull())
                           .append("path", new BsonString("patientRecord.billing"))
                           .append("bsonType", new BsonString("object")))));
   ```

   **Note:**

   The previous code sample encrypts both the `ssn` and `billing` fields. However, only the `ssn` field can be queried because it contains the `queries` property.

6. Create your encrypted collection.

   Add the following code blocks to your `QueryableEncryptionTutorial.java` file under the `// Paste
               code to create an encrypted collection below` comment in the order shown.

   First, instantiate a `ClientEncryption` object to access the API for the encryption helper methods:

   ```java
   ClientEncryptionSettings clientEncryptionSettings = ClientEncryptionSettings.builder()
           .keyVaultMongoClientSettings(MongoClientSettings.builder()
                   .applyConnectionString(new ConnectionString(uri))
                   .build())
           .keyVaultNamespace(keyVaultNamespace)
           .kmsProviders(kmsProviderCredentials)
           .build();
   ClientEncryption clientEncryption = ClientEncryptions.create(clientEncryptionSettings);
   ```

   Because you are using a local Customer Master Key, you don't need to provide Customer Master Key credentials. Create a variable containing an empty object to use in place of credentials when you create your encrypted collection:

   ```java
   BsonDocument customerMasterKeyCredentials = new BsonDocument();
   ```

   Create your encrypted collection by using the `createEncryptedCollection()` helper method accessed through the `ClientEncryption` class. This method automatically generates data encryption keys for your encrypted fields and creates the encrypted collection:

   ```java
   CreateCollectionOptions createCollectionOptions = new CreateCollectionOptions().encryptedFields(encryptedFields);

   CreateEncryptedCollectionParams encryptedCollectionParams = new CreateEncryptedCollectionParams(kmsProviderName);
   encryptedCollectionParams.masterKey(customerMasterKeyCredentials);

   try {
       clientEncryption.createEncryptedCollection(
               encryptedClient.getDatabase(encryptedDatabaseName),
               encryptedCollectionName,
               createCollectionOptions,
               encryptedCollectionParams);
   } 
   catch (Exception e) {
       throw new Exception("Unable to create encrypted collection due to the following error: " + e.getMessage());
   }
   ```

### Perform Encrypted Operations

After you configure your application and database connection, you can insert and query encrypted documents.

1. Insert a document with encrypted fields.

   Add the following code blocks under the `// Paste code to insert
               a document below` comment in the order shown.

   First, configure your application to use the POJO classes that you created:

   ```java
   CodecProvider pojoCodecProvider = PojoCodecProvider.builder().automatic(true).build();
   CodecRegistry pojoCodecRegistry = fromRegistries(getDefaultCodecRegistry(), fromProviders(pojoCodecProvider));
   ```

   Then, create an instance of a `Patient` that describes a patient's personal information and use the encrypted client to insert it into the `patients` collection:

   ```java
   MongoDatabase encryptedDb = encryptedClient.getDatabase(encryptedDatabaseName).withCodecRegistry(pojoCodecRegistry);
   MongoCollection<Patient> collection = encryptedDb.getCollection(encryptedCollectionName, Patient.class);

   PatientBilling patientBilling = new PatientBilling("Visa", "4111111111111111");
   PatientRecord patientRecord = new PatientRecord("987-65-4320", patientBilling, 1500);
   Patient patientDocument = new Patient("Jon Doe", patientRecord);

   InsertOneResult result = collection.insertOne(patientDocument);
   ```

2. Query on encrypted data.

   Paste the following code under the `// Paste code to query the
               document below` comment to execute a find query on an encrypted field and print the decrypted data:

   ```java
   Patient findResult = collection.find(
       new BsonDocument()
               .append("patientRecord.ssn", new BsonString("987-65-4320")))
               .first();
    
   System.out.println(findResult);
   ```

3. Compile and run your application.

   To compile and run your application, run the following commands from your `JavaQE` directory:

   ```bash
   mvn clean package
   java -jar target/queryable-encryption-tutorial.jar
   ```

   The driver decrypts the encrypted fields automatically when it returns the document. The output resembles the following:

   ```none
   {id=648b384a722cb9b8392df76a, name='Jon Doe', patientRecord={ssn='987-65-4320', billing={cardType='Visa', cardNumber='4111111111111111'}, billAmount=1500}}
   ```

   **Warning: Do not Modify the \_\_safeContent\_\_ Field**

   The `__safeContent__` field is essential to Queryable Encryption. Do not modify the contents of this field.

### Set Up Your Project

Follow the steps in this section to create your project files and assign the required configuration variables.

1. Install libmongocrypt 1.8.0 or later

   For instructions on how to install `libmongocrypt`, select your operating system and the Go driver on the [Install a Queryable Encryption Compatible Driver and Dependencies](/docs/manual/core/queryable-encryption/install#std-label-qe-install) page.

2. Install dependencies.

   Create a directory named `go-qe` to store your project files. Run the following commands to navigate into the directory, initialize your project, and install the required packages:

   ```bash
   cd go-qe
   go mod init go-qe
   go get go.mongodb.org/mongo-driver/v2/mongo
   go get github.com/joho/godotenv
   ```

3. Set up your environment variables.

   In your `go-qe` directory, create a `.env` file. The sample code in this tutorial references environment variables that you need to set in this `.env` file. Paste the following code into this file:

   ```bash
   # MongoDB replica set connection URI
   export MONGODB_URI="<Your MongoDB Connection URI>"

   # MongoDB Automatic Encryption Shared Library 
   export SHARED_LIB_PATH="<Full path to your Automatic Encryption Shared Library>"

   ```

   Replace the following placeholder values:

   - `<Your MongoDB URI>`: Your MongoDB deployment connection URI.

   - `<Full path to your Automatic Encryption Shared Library>`: The full path to your Automatic Encryption Shared Library, which resembles the following paths:

     - **macOS**: `/<crypt shared directory>/lib/mongo_crypt_v1.dylib`

     - **Linux**: `/<crypt shared directory>/lib/mongo_crypt_v1.so`

     - **Windows**: `C:\<crypt shared directory>\bin\mongo_crypt_v1.dll`

   For more information on setting up environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/go/README.md)  file included in the sample application on GitHub.

4. Create your data model file.

   This Go tutorial uses structs to represent the document structure. In your ] `go-qe` directory, create a file named `models.go` and paste the following code into this file:

   ```go
   package main

   /*
   	This file contains a sample data model you can use
   	to serialize data you store in MongoDB and deserialize
   	your retrieved data from MongoDB.
   */

   // start-patient-document
   type PatientDocument struct {
   	PatientName   string        `bson:"patientName"`
   	PatientID     int32         `bson:"patientId"`
   	PatientRecord PatientRecord `bson:"patientRecord"`
   }

   // end-patient-document

   // start-patient-record
   type PatientRecord struct {
   	SSN        string      `bson:"ssn"`
   	Billing    PaymentInfo `bson:"billing"`
   	BillAmount int         `bson:"billAmount"`
   }

   // end-patient-record

   // start-payment-info
   type PaymentInfo struct {
   	Type   string `bson:"type"`
   	Number string `bson:"number"`
   }

   // end-payment-info

   ```

5. Create your main project file.

   In your `go-qe` directory, create a file named `main.go`. Paste the following starter code into this file. The placeholder comments indicate where you will add code in future steps of this tutorial:

   ```go
   package main

   import (
       "context"
       "crypto/rand"
       "encoding/json"
       "fmt"
       "os"

       "github.com/joho/godotenv"
       "go.mongodb.org/mongo-driver/v2/bson"
       "go.mongodb.org/mongo-driver/v2/mongo"
       "go.mongodb.org/mongo-driver/v2/mongo/options"
   )

   func main() {

       if err := godotenv.Load(".env"); err != nil {
           panic("Error loading .env file")
       }

       // Paste application variables below

       // Paste code to generate CMK below

       // Paste code to retrieve CMK and specify KMS provider settings below

       // Paste automatic encryption options code below

       // Paste client configuration code below

       // Paste JSON schema below

       // Paste code to create an encrypted collection below

       // Paste code to insert a document below

       // Paste code to query the document below
   }
   ```

6. Assign your application variables.

   Declare the required application variables by pasting the following code into your `main.go` file under the `// Paste application variables
               below` comment. For this tutorial, set the `kmsProviderName` variable to `"local"`.

   ```go
   kmsProviderName := "<KMS provider name>"
   uri := os.Getenv("MONGODB_URI") // Your connection URI
   keyVaultDatabaseName := "encryption"
   keyVaultCollectionName := "__keyVault"
   keyVaultNamespace := keyVaultDatabaseName + "." + keyVaultCollectionName
   encryptedDatabaseName := "medicalRecords"
   encryptedCollectionName := "patients"
   ```

   | Variable | Description |
   | --- | --- |
   | `kmsProviderName` | The KMS that stores your Customer Master Key. For this tutorial, set this variable to `"local"`. |
   | `uri` | Your MongoDB connection URI. Set with the `MONGODB_URI` environment variable. |
   | `keyVaultDatabaseName` | The database that stores your DEKs. Set to `"encryption"`. |
   | `keyVaultCollectionName` | The collection that stores your DEKs. Set to `"__keyVault"`. |
   | `keyVaultNamespace` | The namespace in MongoDB that stores your DEKs. Set this variable to the values of the `keyVaultDatabaseName` and `keyVaultCollectionName` variables, separated by a period. |
   | `encryptedDatabaseName` | The database that stores your encrypted data. Set to `"medicalRecords"`. |
   | `encryptedCollectionName` | The collection that stores your encrypted data. Set to `"patients"`. |

### Configure Encryption

After you set up your project, follow the steps in this section to create an encryption key and configure your application for Queryable Encryption.

1. Create an encryption key.

   Paste the following code into your `main.go` file under the `// Paste code to generate CMK below` comment. This code snippet creates a 96-byte Customer Master Key and saves it to your filesystem as the file `customer-master-key.txt`:

   ```go
   key := make([]byte, 96)
   if _, err := rand.Read(key); err != nil {
   	panic(fmt.Sprintf("Unable to create a random 96 byte data key: %v\n", err))
   }
   if err := os.WriteFile("customer-master-key.txt", key, 0644); err != nil {
   	panic(fmt.Sprintf("Unable to write key to file: %v\n", err))
   }
   ```

   **Warning: Secure your Local Key File in Production**

   We recommend storing your Customer Master Keys in a remote [Key Management System](https://en.wikipedia.org/wiki/Key_management#Key_management_system) (KMS (Key Management System)). To learn how to use a remote KMS (Key Management System) in your Queryable Encryption implementation, see the [Queryable Encryption Tutorials](/docs/manual/core/queryable-encryption/tutorials#std-label-qe-tutorial-automatic-encryption) guide.

   If you choose to use a local key provider in production, exercise great caution and do not store it on the file system. Consider injecting the key into your client application using a sidecar process, or use another approach that keeps the key secure.

2. Retrieve the Customer Master Key and specify the KMS provider settings.

   Paste the following code into your `main.go` file under the `// Paste code to retrieve CMK and specify KMS provider settings below` comment to retrieve the contents of the `customer-master-key.txt` file:

   ```go
   key, err := os.ReadFile("customer-master-key.txt")
   if err != nil {
   	panic(fmt.Sprintf("Could not read the Customer Master Key: %v", err))
   }
   if len(key) != 96 {
   	panic(fmt.Sprintf("Expected the customer master key file to be 96 bytes."))
   }
   kmsProviderCredentials := map[string]map[string]interface{}{"local": {"key": key}}
   ```

   This code sets the provider name to `local` to use a Local Key Provider and uses the CMK (Customer Master Key) value from your KMS provider settings.

3. Set your automatic encryption options.

   Add the following code under the `// Paste automatic encryption options code below` comment to create an `AutoEncryption` object that contains the following options:

   - The namespace of your Key Vault collection

   - The `kmsProviderCredentials` object, defined in the previous step

   - The `cryptSharedLibraryPath` object, which contains the path to your Automatic Encryption Shared Library

   ```go
   cryptSharedLibraryPath := map[string]interface{}{
   	"cryptSharedLibPath": os.Getenv("SHARED_LIB_PATH"), // Path to your Automatic Encryption Shared Library
   }

   autoEncryptionOptions := options.AutoEncryption().
   	SetKeyVaultNamespace(keyVaultNamespace).
   	SetKmsProviders(kmsProviderCredentials).
   	SetExtraOptions(cryptSharedLibraryPath)
   ```

4. Create a client to set up an encrypted collection.

   Create a new client to encrypt and decrypt your collection. The client uses your connection URI and automatic encryption options. Paste the following code into your `main.go` file, under the `// Paste client configuration code below` comment:

   ```go
   opts := options.Client().
   	ApplyURI(uri).
   	SetAutoEncryptionOptions(autoEncryptionOptions)
   encryptedClient, err := mongo.Connect(opts)

   if err != nil {
   	panic(fmt.Sprintf("Unable to connect to MongoDB: %v\n", err))
   }
   defer func() {
   	_ = encryptedClient.Disconnect(context.TODO())
   }()
   ```

5. Specify fields to encrypt.

   To encrypt a field, add it to the encryption schema. To enable queries on a field, add the `queries` property. Paste the following code under the `// Paste JSON schema below` comment:

   ```go
   encryptedFields := bson.M{
   	"fields": []bson.M{
   		bson.M{
   			"keyId":    nil,
   			"path":     "patientRecord.ssn",
   			"bsonType": "string",
   			"queries": []bson.M{
   				{
   					"queryType": "equality",
   				},
   			},
   		},
   		bson.M{
   			"keyId":    nil,
   			"path":     "patientRecord.billing",
   			"bsonType": "object",
   		},
   	},
   }
   ```

   **Note:**

   The previous code sample encrypts both the `ssn` and `billing` fields. However, only the `ssn` field can be queried because it contains the `queries` property.

6. Create your encrypted collection.

   Add the following code blocks to your `main.go` file, under the `// Paste code to create an encrypted collection below` comment in the order shown.

   First, instantiate a `ClientEncryption` object to access the API for the encryption helper methods:

   ```go
   clientEncryptionOpts := options.ClientEncryption().
   	SetKeyVaultNamespace(keyVaultNamespace).
   	SetKmsProviders(kmsProviderCredentials)

   clientEncryption, err := mongo.NewClientEncryption(encryptedClient, clientEncryptionOpts)
   if err != nil {
   	panic(fmt.Sprintf("Unable to create a ClientEncryption instance due to the following error: %s\n", err))
   }
   ```

   Because you are using a local Customer Master Key, you don't need to provide Customer Master Key credentials. Create a variable containing an empty object to use in place of credentials when you create your encrypted collection:

   ```go
   customerMasterKey := map[string]string{}
   ```

   To create your encrypted collection, use the `ClientEncryption` object's `CreateEncryptedCollection()` helper method. This method automatically generates data encryption keys for your encrypted fields and creates the encrypted collection:

   ```go
   createCollectionOptions := options.CreateCollection().SetEncryptedFields(encryptedFields)
   _, _, err =
   	clientEncryption.CreateEncryptedCollection(
   		context.TODO(),
   		encryptedClient.Database(encryptedDatabaseName),
   		encryptedCollectionName,
   		createCollectionOptions,
   		kmsProviderName,
   		customerMasterKey,
   	)
   ```

### Perform Encrypted Operations

After you configure your application and database connection, you can insert and query encrypted documents.

1. Insert a document with encrypted fields.

   Paste the following code under the `// Paste code to insert a document below` comment to create a document that stores patient data and insert it into the `patients` collection:

   ```go
   patientDocument := &PatientDocument{
   	PatientName: "Jon Doe",
   	PatientID:   12345678,
   	PatientRecord: PatientRecord{
   		SSN: "987-65-4320",
   		Billing: PaymentInfo{
   			Type:   "Visa",
   			Number: "4111111111111111",
   		},
   		BillAmount: 1500,
   	},
   }

   coll := encryptedClient.Database(encryptedDatabaseName).Collection(encryptedCollectionName)

   _, err = coll.InsertOne(context.TODO(), patientDocument)
   if err != nil {
   	panic(fmt.Sprintf("Unable to insert the patientDocument: %s", err))
   }
   ```

2. Query on encrypted data.

   Add the following code to your `main.go` file under the `// Paste code to query the document below` comment:

   ```go
   var findResult PatientDocument
   err = coll.FindOne(
   	context.TODO(),
   	bson.M{"patientRecord.ssn": "987-65-4320"},
   ).Decode(&findResult)
   if err != nil {
   	fmt.Print("Unable to find the document\n")
   } else {
   	output, _ := json.MarshalIndent(findResult, "", "    ")
   	fmt.Printf("%s\n", output)
   }
   ```

3. Compile and run your application.

   To compile and run your application, run the following commands from your project directory:

   ```bash
   go build -tags cse
   ./go-qe
   ```

   The output of the preceding code sample should look similar to the following:

   ```json
   {
       "PatientName": "Jon Doe",
       "PatientID": 12345678,
       "PatientRecord": {
           "SSN": "987-65-4320",
           "Billing": {
               "Type": "Visa",
               "Number": "4111111111111111"
           },
           "BillAmount": 1500
       }
   }
   ```

   **Warning: Do not Modify the \_\_safeContent\_\_ Field**

   The `__safeContent__` field is essential to Queryable Encryption. Do not modify the contents of this field.

### Set Up Your Project

Follow the steps in this section to create your project files and assign the required configuration variables.

1. Create your .NET console project.

   Run the following commands to create a new .NET console project in a directory named `CSharpQE`:

   ```bash
   mkdir CSharpQE && cd CSharpQE
   dotnet new console
   ```

2. Install dependencies.

   From your `CSharpQE` directory, run the following commands to install the MongoDB .NET/C# Driver and required packages:

   ```bash
   dotnet add package MongoDB.Driver
   dotnet add package MongoDB.Driver.Encryption
   dotnet add package Microsoft.Extensions.Configuration.Json
   ```

3. Configure your application settings.

   In your `CSharpQE` directory, create a file named `appsettings.json`. The sample code in this tutorial reads its configuration from this file. Paste the following code into this file:

   ```json
   {
       "MongoDbUri": "<Your MongoDB URI>",
       "CryptSharedLibPath": "<Full path to your Automatic Encryption Shared Library>"
   }
   ```

   Replace the following placeholder values:

   - `<Your MongoDB URI>`: Your MongoDB deployment connection URI.

   - `<Full path to your Automatic Encryption Shared Library>`: The full path to your Automatic Encryption Shared Library, which resembles the following paths:

     - **macOS**: `/<crypt shared directory>/lib/mongo_crypt_v1.dylib`

     - **Linux**: `/<crypt shared directory>/lib/mongo_crypt_v1.so`

     - **Windows**: `C:\<crypt shared directory>\bin\mongo_crypt_v1.dll`

   **Tip: appsettings.json Location**

   When you run the application, the `appsettings.json` file must be in the same directory as the compiled executable. Add the following `ItemGroup` to your `.csproj` file so that the `CopyToOutputDirectory` setting automatically copies `appsettings.json` to the output `bin` directory when you build:

   ```xml
   <ItemGroup>
     <None Update="appsettings.json">
       <CopyToOutputDirectory>PreserveNewest</CopyToOutputDirectory>
     </None>
   </ItemGroup>
   ```

   For more information on setting up your configuration, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/csharp/README.md) file included in the sample application on GitHub.

4. Create your data model classes.

   This tutorial uses separate classes as data models to represent the document structure. In your `CSharpQE` directory, create a file named `Patient.cs` and paste the following `Patient` class into the file:

   ```csharp
   using MongoDB.Bson;
   using MongoDB.Bson.Serialization.Attributes;

   [BsonIgnoreExtraElements]
   public class Patient
   {
       public ObjectId Id { get; set; }
       public string PatientName { get; set; }
       public PatientRecord PatientRecord { get; set; }
   }
   ```

   Then, create a file named `PatientRecord.cs` and paste the following `PatientRecord` class into the file:

   ```csharp
   public class PatientRecord
   {
       public string Ssn { get; set; }
       public PatientBilling Billing { get; set; }
       public int BillAmount { get; set; }
   }
   ```

   Finally, create a file named `PatientBilling.cs` and paste the following `PatientBilling` class into the file:

   ```csharp
   public class PatientBilling
   {
       public string CardType { get; set; }
       public long CardNumber { get; set; }
   }
   ```

5. Create your main project file.

   Replace the contents of the `Program.cs` file that was generated in your `CSharpQE` directory with the following code:

   ```csharp
   ﻿namespace QueryableEncryption;

   public class Program
   {
       public static async Task Main(string[] args)
       {
           await QueryableEncryptionTutorial.RunExample();
       }
   }
   ```

   The `Program.cs` file contains your main method, which calls the code in your other project files to generate encryption keys and perform encrypted operations.

6. Create your application file.

   In your `CSharpQE` directory, create a file named `QueryableEncryptionTutorial.cs`. This file contains the main Queryable Encryption workflow. Paste the following starter code into this file:

   ```csharp
   using Microsoft.Extensions.Configuration;
   using MongoDB.Bson;
   using MongoDB.Bson.IO;
   using MongoDB.Bson.Serialization.Conventions;
   using MongoDB.Driver;
   using MongoDB.Driver.Encryption;
   using System.Security.Cryptography;

   namespace QueryableEncryption;

   public static class QueryableEncryptionTutorial
   {
      public static async Task RunExample()
      {
         var camelCaseConvention = new ConventionPack { new CamelCaseElementNameConvention() };
         ConventionRegistry.Register("CamelCase", camelCaseConvention, type => true);

         // Paste application variables below


         // The helper code snippets you paste below read configuration
         // from this alias of your appSettings variable
         var _appSettings = appSettings;

         // Paste code to generate CMK below


         // Paste code to retrieve the CMK and specify KMS provider settings below


         // Paste automatic encryption options code below


         // Paste client configuration code below


         // Paste schema below


         // Paste code to create an encrypted collection below


         // Paste code to insert a document below


         // Paste code to query the document below

      }
   }
   ```

   The placeholder comments indicate where you add code in later steps of this tutorial.

7. Assign your application variables.

   The code samples in this tutorial use the following variables to perform the Queryable Encryption workflow. Paste the following code into the `RunExample()` method of `QueryableEncryptionTutorial.cs`, under the `// Paste application variables below` comment. For this tutorial, set the `kmsProviderName` variable to `"local"`.

   ```csharp
   const string kmsProviderName = "<your KMS provider name>";
   const string keyVaultDatabaseName = "encryption";
   const string keyVaultCollectionName = "__keyVault";
   var keyVaultNamespace =
       CollectionNamespace.FromFullName($"{keyVaultDatabaseName}.{keyVaultCollectionName}");
   const string encryptedDatabaseName = "medicalRecords";
   const string encryptedCollectionName = "patients";
   var appSettings = new ConfigurationBuilder().AddJsonFile("appsettings.json").Build();
   var uri = appSettings["MongoDbUri"];
   ```

   | Variable | Description |
   | --- | --- |
   | `kmsProviderName` | The KMS that stores your Customer Master Key. For this tutorial, set this variable to `"local"`. |
   | `keyVaultDatabaseName` | The database that stores your DEKs. Set to `"encryption"`. |
   | `keyVaultCollectionName` | The collection that stores your DEKs. Set to `"__keyVault"`. |
   | `keyVaultNamespace` | The namespace in MongoDB that stores your DEKs. Set this variable to a new `CollectionNamespace` object whose name is the values of the `keyVaultDatabaseName` and `keyVaultCollectionName` variables, separated by a period. |
   | `encryptedDatabaseName` | The database that stores your encrypted data. Set to `"medicalRecords"`. |
   | `encryptedCollectionName` | The collection that stores your encrypted data. Set to `"patients"`. |
   | `uri` | Your MongoDB connection URI. Set with the `MongoDbUri` value in your `appsettings.json` file. |

### Configure Encryption

After you set up your project, follow the steps in this section to create an encryption key and configure your application for Queryable Encryption.

1. Create an encryption key.

   Paste the following code into your `QueryableEncryptionTutorial.cs` file under the `// Paste code to generate CMK below` comment. This code creates a 96-byte Customer Master Key and saves it to your filesystem as the file `customer-master-key.txt`:

   ```csharp
   using var randomNumberGenerator = RandomNumberGenerator.Create();
   try
   {
       var bytes = new byte[96];
       randomNumberGenerator.GetBytes(bytes);
       File.WriteAllBytes("customer-master-key.txt", bytes);
   }
   catch (Exception e)
   {
       throw new Exception("Unable to write Customer Master Key file due to the following error: " + e.Message);
   }
   ```

   **Warning: Secure your Local Key File in Production**

   We recommend storing your Customer Master Keys in a remote [Key Management System](https://en.wikipedia.org/wiki/Key_management#Key_management_system) (KMS (Key Management System)). To learn how to use a remote KMS (Key Management System) in your Queryable Encryption implementation, see the [Queryable Encryption Tutorials](/docs/manual/core/queryable-encryption/tutorials#std-label-qe-tutorial-automatic-encryption) guide.

   If you choose to use a local key provider in production, exercise great caution and do not store it on the file system. Consider injecting the key into your client application using a sidecar process, or use another approach that keeps the key secure.

2. Retrieve the Customer Master Key and specify the KMS provider settings.

   Paste the following code under the `// Paste code to retrieve the CMK and
               specify KMS provider settings below` comment. This code retrieves the contents of the `customer-master-key.txt` file:

   ```csharp
   // WARNING: Do not use a local key file in a production application
   var kmsProviderCredentials = new Dictionary<string, IReadOnlyDictionary<string, object>>();
   try
   {
       var localCustomerMasterKeyBytes = File.ReadAllBytes("customer-master-key.txt");

       if (localCustomerMasterKeyBytes.Length != 96)
       {
           throw new Exception("Expected the customer master key file to be 96 bytes.");
       }

       var localOptions = new Dictionary<string, object>
       {
           { "key", localCustomerMasterKeyBytes }
       };

       kmsProviderCredentials.Add("local", localOptions);
   }
   catch (Exception e)
   {
       throw new Exception("Unable to read the Customer Master Key due to the following error: " + e.Message);
   }
   ```

3. Set your automatic encryption options.

   Paste the following code under the `// Paste automatic encryption options
               code below` comment. This code snippet creates an `AutoEncryptionOptions` object that contains the following options:

   - The namespace of your Key Vault collection

   - The `kmsProviderCredentials` object, defined in the previous step

   - The `extraOptions` object, which contains the path to your Automatic Encryption Shared Library

   ```csharp
   var extraOptions = new Dictionary<string, object>
   {
       { "cryptSharedLibPath", _appSettings["CryptSharedLibPath"] } // Path to your Automatic Encryption Shared Library
   };

   var autoEncryptionOptions = new AutoEncryptionOptions(
       keyVaultNamespace,
       kmsProviderCredentials,
       extraOptions: extraOptions);
   ```

4. Create a client to set up an encrypted collection.

   Paste the following code under the `// Paste client configuration code
               below` comment.

   IMPORTANT: If you are using the .NET/C# driver version 3.0 or later, you must add the following code to your application before you instantiate a new `MongoClient`:

   ```csharp
   MongoClientSettings.Extensions.AddAutoEncryption(); // .NET/C# Driver v3.0 or later only
   ```

   Then, instantiate a new `MongoClient`:

   ```csharp
   var clientSettings = MongoClientSettings.FromConnectionString(uri);
   clientSettings.AutoEncryptionOptions = autoEncryptionOptions;

   var encryptedClient = new MongoClient(clientSettings);
   ```

5. Specify fields to encrypt.

   To encrypt a field, add the field to the encryption schema. To enable queries on a field, add the `queries` property. Paste the following code under the `// Paste schema below` comment:

   ```csharp
   var encryptedFields = new BsonDocument
   {
       {
           "fields", new BsonArray
           {
               new BsonDocument
               {
                   { "keyId", BsonNull.Value },
                   { "path", "patientRecord.ssn" },
                   { "bsonType", "string" },
                   { "queries", new BsonDocument("queryType", "equality") }
               },
               new BsonDocument
               {
                   { "keyId", BsonNull.Value },
                   { "path", "patientRecord.billing" },
                   { "bsonType", "object" }
               }
           }
       }
   };
   ```

   **Note:**

   The previous code sample encrypts both the `ssn` and `billing` fields. However, only the `ssn` field can be queried because it contains the `queries` property.

6. Create your encrypted collection.

   Add the following code blocks to your `QueryableEncryptionTutorial.cs` file under the `// Paste code to create an encrypted collection below` comment in the order shown.

   First, instantiate a `ClientEncryption` object to access the API for the encryption helper methods:

   ```csharp
   var clientEncryptionOptions = new ClientEncryptionOptions(
      keyVaultClient: encryptedClient,
      keyVaultNamespace: keyVaultNamespace,
      kmsProviders: kmsProviderCredentials
   );
   var clientEncryption = new ClientEncryption(clientEncryptionOptions);
   ```

   Because you are using a local Customer Master Key, you don't need to provide Customer Master Key credentials. Create a variable containing an empty object to use in place of credentials when you create your encrypted collection:

   ```csharp
   var customerMasterKeyCredentials = new BsonDocument();
   ```

   To create your encrypted collection, use the `ClientEncryption` object's `CreateEncryptedCollection()` helper method. This method automatically generates data encryption keys for your encrypted fields and creates the encrypted collection:

   ```csharp
   var patientDatabase = encryptedClient.GetDatabase(encryptedDatabaseName);
   patientDatabase.DropCollection(encryptedCollectionName); // Ensure the collection is dropped before creating a new one
   try
   {
       var createCollectionOptions = new CreateCollectionOptions<Patient>
       {
           EncryptedFields = encryptedFields
       };

       clientEncryption.CreateEncryptedCollection(patientDatabase,
           encryptedCollectionName,
           createCollectionOptions,
           kmsProviderName,
           customerMasterKeyCredentials);
   }
   catch (Exception e)
   {
       throw new Exception("Unable to create encrypted collection due to the following error: " + e.Message);
   }
   ```

### Perform Encrypted Operations

After you configure your application and database connection, you can insert and query encrypted documents.

1. Insert a document with encrypted fields.

   To create a document that stores patient data and insert it into the `patients` collection, paste the following code under the `// Paste code to insert a document below` comment:

   ```csharp
   var patient = new Patient
   {
       PatientName = "Jon Doe",
       Id = new ObjectId(),
       PatientRecord = new PatientRecord
       {
           Ssn = "987-65-4320",
           Billing = new PatientBilling
           {
               CardType = "Visa",
               CardNumber = 4111111111111111,
           },
           BillAmount = 1500
       }
   };

   var encryptedCollection = encryptedClient.GetDatabase(encryptedDatabaseName).
       GetCollection<Patient>(encryptedCollectionName);

   await encryptedCollection.InsertOneAsync(patient);
   ```

2. Query on encrypted data.

   Paste the following code under the `// Paste code to query the document
               below` comment to retrieve an encrypted field value and print the decrypted data:

   ```csharp
   var ssnFilter = Builders<Patient>.Filter.Eq("patientRecord.ssn", patient.PatientRecord.Ssn);
   var findResult = await encryptedCollection.Find(ssnFilter).FirstOrDefaultAsync();

   Console.WriteLine(findResult.ToJson(new JsonWriterSettings { Indent = true }));
   ```

3. Run your application.

   To run the application, run the following command from your `CSharpQE` project directory:

   ```bash
   dotnet run
   ```

   The output of the preceding code sample should look similar to the following:

   ```json
   {
     "_id": {
       "$oid": "6a6281b43201828e23bbe897"
     },
     "patientName": "Jon Doe",
     "patientRecord": {
       "ssn": "987-65-4320",
       "billing": {
         "cardType": "Visa",
         "cardNumber": 4111111111111111
       },
       "billAmount": 1500
     }
   }
   ```

   **Warning: Do not Modify the \_\_safeContent\_\_ Field**

   The `__safeContent__` field is essential to Queryable Encryption. Do not modify the contents of this field.

### Set Up Your Project

Follow the steps in this section to create your project files and assign the required configuration variables.

1. Install libmongocrypt.

   To install `libmongocrypt`, see the [Install a Queryable Encryption Compatible Driver and Dependencies](/docs/manual/core/queryable-encryption/install#std-label-qe-install) page. In the drop-down menus, select your operating system and the Rust driver.

2. Create a project directory.

   In your shell, run the following command to create a directory called `rust_qe` for this project:

   ```bash
   cargo new rust_qe
   ```

   This command creates a `Cargo.toml` file and a `src/main.rs` file in your `rust_qe` directory.

   Run the following command to navigate into the project directory:

   ```bash
   cd rust_qe
   ```

3. Install dependencies.

   To add the necessary crates, paste the following code into your project's `Cargo.toml` file.

   ```toml
   [package]
   name = "rust-qe"
   version = "0.1.0"
   edition = "2024"

   # See more keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html

   [[bin]]
   name = "queryable_encryption_tutorial"
   path = "src/queryable_encryption_tutorial.rs"

   [dependencies]
   serde = "1.0.188"
   futures = "0.3.28"
   tokio = {version = "1.32.0", features = ["full"]}
   rand = "0.9.3"
   dotenv = "0.15.0"

   [dependencies.mongodb]
   features = ["in-use-encryption"]
   version = "3.7"

   ```

   This code declares the MongoDB Rust driver with the `in-use-encryption` feature flag, which provides the encryption functionality required for Queryable Encryption, and the `dotenv` crate that reads your credentials from a `.env` file.

4. Set up your environment variables.

   In your `rust_qe` directory, create a `.env` file. The sample code in this tutorial references environment variables that you need to set in this `.env` file. Paste the following code into this file:

   ```bash
   # MongoDB connection uri and automatic encryption shared library path

   MONGODB_URI="<Your MongoDB URI>"
   SHARED_LIB_PATH="<Full path to your Automatic Encryption Shared Library>"

   ```

   Replace the following placeholder values:

   - `<Your MongoDB URI>`: Your MongoDB deployment connection URI.

   - `<Full path to your Automatic Encryption Shared Library>`: The full path to your Automatic Encryption Shared Library, which resembles the following paths:

     - **macOS**: `/<crypt shared directory>/lib/mongo_crypt_v1.dylib`

     - **Linux**: `/<crypt shared directory>/lib/mongo_crypt_v1.so`

     - **Windows**: `C:\<crypt shared directory>\bin\mongo_crypt_v1.dll`

   To learn more about setting up environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/rust/README.md) file included in the sample application on GitHub.

5. Create your main project file.

   In the `rust_qe/src` directory, rename your `main.rs` file to `queryable_encryption_tutorial.rs` and paste the following starter code into this file. The placeholder comments indicate where you will add code in future steps of this tutorial:

   ```rust
   use mongodb::{
       bson::{doc, spec::BinarySubtype, Binary, Bson, Document},
       client_encryption::{ClientEncryption, LocalMasterKey, MasterKey},
       mongocrypt::ctx::KmsProvider,
       options::ClientOptions,
       Client, Collection, Namespace,
   };
   use dotenv::dotenv;
   use rand::RngCore;
   use std::env;
   use std::fs::{self, OpenOptions};
   use std::io::{Read, Write};
   use std::path::Path;

   #[tokio::main]
   async fn main() -> mongodb::error::Result<()> {
       dotenv().ok();

       // Paste application variables below

       // Paste code to generate CMK below

       // Paste code to retrieve CMK and specify KMS provider settings below

       // Paste automatic encryption options code below

       // Paste client configuration code below

       // Paste schema below

       // Paste code to create an encrypted collection below

       // Paste code to insert a document below

       // Paste code to query the document below

       return Ok(());
   }
   ```

6. Assign your application variables.

   Declare the required application variables by pasting the following code into your `queryable_encryption_tutorial.rs` file under the `// Paste application variables below` comment. For this tutorial, set the `kms_provider_name` variable to `"local"`.

   ```rust
   let kms_provider_name = "<KMS provider name>";
   let uri = env::var("MONGODB_URI").expect("Set MONGODB_URI environment variable to your connection string");
   let key_vault_database_name = "encryption";
   let key_vault_collection_name = "__keyVault";
   let key_vault_namespace = Namespace::new(key_vault_database_name, key_vault_collection_name);
   let encrypted_database_name = "medicalRecords";
   let encrypted_collection_name = "patients";
   ```

   The following table describes each application variable in the code snippet:

   | Variable | Description |
   | --- | --- |
   | `kms_provider_name` | The KMS used to store your Customer Master Key. |
   | `uri` | Your MongoDB connection URI. Set with the `MONGODB_URI` environment variable. |
   | `key_vault_database_name` | The database where DEKs are stored. Set to `"encryption"`. |
   | `key_vault_collection_name` | The collection where DEKs are stored. Set to `"__keyVault"`. |
   | `key_vault_namespace` | The namespace in MongoDB where your DEKs are stored. Set this variable to a `Namespace` struct that takes the values of the `key_vault_database_name` and `key_vault_collection_name` variables. |
   | `encrypted_database_name` | The database where encrypted data is stored. Set to `"medicalRecords"`. |
   | `encrypted_collection_name` | The collection where encrypted data is stored. Set to `"patients"`. |

### Configure Encryption

After you set up your project, follow the steps in this section to create an encryption key and configure your application for Queryable Encryption.

1. Create an encryption key.

   Paste the following code into your `queryable_encryption_tutorial.rs` file under the `// Paste
               code to generate CMK below` comment. This code snippet creates a 96-byte Customer Master Key and saves it to your filesystem as the file `customer-master-key.txt`:

   ```rust
   let key_file_path = "customer-master-key.txt";
   let mut local_key = Vec::new();

   if !Path::new(key_file_path).exists() {
       let mut key = [0u8; 96];
       rand::rng().fill_bytes(&mut key);

       // Write the key to the file
       match OpenOptions::new().write(true).create(true).open(key_file_path) {
           Ok(mut file) => {
               if let Err(err) = file.write_all(&key) {
                   panic!("Unable to write Customer Master Key to file: {}", err);
               }
           }
           Err(err) => panic!("Unable to create Customer Master Key file: {}", err),
       }
       local_key = key.to_vec();
   } 
   ```

   **Warning: Secure your Local Key File in Production**

   We recommend storing your Customer Master Keys in a remote [Key Management System](https://en.wikipedia.org/wiki/Key_management#Key_management_system) (KMS (Key Management System)). To learn how to use a remote KMS (Key Management System) in your Queryable Encryption implementation, see the [Queryable Encryption Tutorials](/docs/manual/core/queryable-encryption/tutorials#std-label-qe-tutorial-automatic-encryption) guide.

   If you choose to use a local key provider in production, exercise great caution and do not store it on the file system. Consider injecting the key into your client application using a sidecar process, or use another approach that keeps the key secure.

2. Retrieve the Customer Master Key and specify the KMS provider settings.

   Paste the following code into your `queryable_encryption_tutorial.rs` file under the `// Paste
               code to retrieve CMK and specify KMS provider settings below` comment to retrieve the contents of the `customer-master-key.txt` file you generated in the previous step:

   ```rust
   else
   {
       // WARNING: Do not use a local key file in a production application
       match fs::File::open(key_file_path) {
           Ok(mut file) => {
               if let Err(err) = file.read_to_end(&mut local_key) {
                   panic!("Unable to read Customer Master Key file: {}", err);
               }
           }
           Err(err) => panic!("Unable to open Customer Master Key file: {}", err),
       }

       if local_key.len() != 96 {
           panic!("Expected the customer master key file to be 96 bytes.");
       }
   }
   let binary_key = Binary {
       subtype: BinarySubtype::Generic,
       bytes: local_key,
   };
   kms_providers = vec![(
       KmsProvider::local(),
       doc! {
           "key": binary_key,
       },
       None,
   )];
   ```

   This code sets the provider name to `local` to use a Local Key Provider and uses the CMK (Customer Master Key) value from your KMS provider settings.

3. Set your automatic encryption options.

   Add the following code under the `// Paste automatic encryption
               options code below` comment to create an `EncryptedClientBuilder` that contains the following options:

   - A `ClientOptions` struct

   - The namespace of your Key Vault collection

   - The `kms_providers` vector, defined in the previous step

   ```rust
   let client_options = ClientOptions::parse(uri).await.expect("Unable to parse MONGODB_URI");

   let encrypted_client_builder = Client::encrypted_builder(
       client_options,
       key_vault_namespace.clone(),
       kms_providers.clone()
   ).expect("");
   ```

4. Create a client to set up an encrypted collection.

   Create a new client to encrypt and decrypt your collection. The client uses your connection URI and the path to your Automatic Encryption Shared Library. Paste the following code into your `queryable_encryption_tutorial.rs` file, under the `// Paste
               client configuration code below` comment:

   ```rust
   let encrypted_client = encrypted_client_builder
       .extra_options(Some(doc!{
           "cryptSharedLibPath": env::var("SHARED_LIB_PATH").expect("Set SHARED_LIB_PATH environment variable to path to crypt_shared library")
       }))
       .key_vault_client(Client::with_uri_str(uri).await.unwrap())
       .build()
       .await
       .unwrap();
   ```

5. Specify fields to encrypt.

   To encrypt a field, add it to the encryption schema. To enable queries on a field, add the `queries` property. Paste the following code under the `// Paste schema below` comment:

   ```rust
   let encrypted_fields = doc! {
       "fields": [
           {
               "path":     "patientRecord.ssn",
               "bsonType": "string",
               "keyId":    Bson::Null,
               "queries": { "queryType": "equality" },
           },
           {
               "path":     "patientRecord.billing",
               "bsonType": "object",
               "keyId":    Bson::Null,
           },
       ]
   };
   ```

   **Note:**

   The previous code sample encrypts both the `ssn` and `billing` fields. However, only the `ssn` field can be queried because it contains the `queries` property.

6. Create your encrypted collection.

   Add the following code blocks to your `queryable_encryption_tutorial.rs` file, under the `// Paste
               code to create an encrypted collection below` comment in the order shown.

   First, instantiate a `ClientEncryption` struct to access the API for the encryption helper methods:

   ```rust
   let client_encryption = ClientEncryption::new(
       encrypted_client.clone(),
       key_vault_namespace.clone(),
       kms_providers.clone(),
   )
   .unwrap();
   ```

   Because you are using a local Customer Master Key, you don't need to provide Customer Master Key credentials. Create an empty `LocalMasterKey` and wrap it in a `MasterKey::Local` variant to use in place of credentials when you create your encrypted collection:

   ```rust
   let local_master_key = LocalMasterKey::builder().build();
   let customer_master_key_credentials = MasterKey::Local(local_master_key);
   ```

   Create your encrypted collection by using the `create_encrypted_collection()` helper method accessed through the `ClientEncryption` struct. This method automatically generates data encryption keys for your encrypted fields and creates the encrypted collection:

   ```rust
   client_encryption.create_encrypted_collection(
       &encrypted_client.database(encrypted_database_name), 
       encrypted_collection_name,
       customer_master_key_credentials
   )
   .encrypted_fields(encrypted_fields)
   .await
   .1?;
   ```

   The method that creates the encrypted collection requires a reference to a database *object* rather than the database *name*. To obtain this reference, use the `database()` method on your client object.

### Perform Encrypted Operations

After you configure your application and database connection, you can insert and query encrypted documents.

1. Insert a document with encrypted fields.

   Paste the following code under the `// Paste code to insert a
               document below` comment to create a document that stores patient data and insert it into the `patients` collection:

   ```rust
   let patient_document = doc! {
       "patientName": "Jon Doe",
       "patientId": 12345678,
       "patientRecord": {
           "ssn": "987-65-4320",
           "billing": {
               "type": "Visa",
               "number": "4111111111111111",
           },
           "billAmount": 1500,
       }
   };

   let encrypted_coll: Collection<Document>  = encrypted_client
       .database(encrypted_database_name)
       .collection(encrypted_collection_name);

   let insert_result = encrypted_coll.insert_one(patient_document).await?;
   ```

2. Query on encrypted data.

   Add the following code to your `queryable_encryption_tutorial.rs` file under the `// Paste
               code to query the document below` comment:

   ```rust
   let find_result = encrypted_coll.find_one(doc! {"patientRecord.ssn": "987-65-4320"}).await?;

   match find_result {
       Some(document) => println!("{:?}", document),
       None => println!("Document not found"),
   }
   ```

3. Run your application.

   To set the path to your `libmongocrypt` library, run the following command from your project directory:

   ```bash
   export MONGOCRYPT_LIB_DIR=/path/to/libmongocrypt/
   ```

   Then, run the following command to start your application:

   ```bash
   cargo run --bin queryable_encryption_tutorial
   ```

   The driver decrypts the encrypted fields automatically when it returns the document. The output of the preceding code sample should resemble the following:

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

### Set Up Your Project

Follow the steps in this section to create your project files and assign the required configuration variables.

1. Install dependencies.

   Create a directory named `php-qe` to store your project files. Run the following commands to navigate into the directory and install the required packages:

   ```bash
   cd php-qe
   composer require mongodb/mongodb
   composer require symfony/dotenv
   ```

2. Set up your environment variables.

   In your `php-qe` directory, create a `.env` file. The sample code in this tutorial references environment variables that you need to set in this `.env` file. Paste the following code into this file:

   ```bash

   MONGODB_URI="<Your MongoDB URI>"
   KMS_PROVIDER="<Your KMS provider name>"
   SHARED_LIB_PATH="<Full path to your Automatic Encryption Shared Library>"

   ```

   Replace the following placeholder values:

   - `<Your MongoDB URI>`: Your MongoDB deployment connection URI.

   - `<Your KMS provider name>`: The KMS provider name. Set this value to `local` for this tutorial.

   - `<Full path to your Automatic Encryption Shared Library>`: The full path to your Automatic Encryption Shared Library, which resembles the following paths:

     - **macOS**: `/<crypt shared directory>/lib/mongo_crypt_v1.dylib`

     - **Linux**: `/<crypt shared directory>/lib/mongo_crypt_v1.so`

     - **Windows**: `C:\<crypt shared directory>\bin\mongo_crypt_v1.dll`

   For more information on setting up environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/php/README.md)  file included in the sample application on GitHub.

3. Create your main project file.

   In your `php-qe` directory, create a file named `quickstart.php`. Paste the following starter code into this file. The placeholder comments indicate where you will add code in future steps of this tutorial:

   ```php
   <?php

   use Symfony\Component\Dotenv\Dotenv;

   require __DIR__.'/vendor/autoload.php';

   (new Dotenv())->usePutenv()->loadEnv(__DIR__.'/.env');

   // Paste application variables below

   // Paste code to generate CMK below

   // Paste code to retrieve CMK and specify KMS provider settings below

   // Paste automatic encryption options code below

   // Paste client configuration code below

   // Paste schema below

   // Paste code to create an encrypted collection below

   // Paste code to insert a document below

   // Paste code to query the document below
   ```

4. Assign your application variables.

   Declare the required application variables by pasting the following code into your `quickstart.php` file under the `// Paste application variables below` comment:

   ```php
   $kmsProviderName = getenv('KMS_PROVIDER');
   $uri = getenv('MONGODB_URI'); // Your connection URI
   $keyVaultDatabaseName = 'encryption';
   $keyVaultCollectionName = '__keyVault';
   $keyVaultNamespace = $keyVaultDatabaseName . '.' . $keyVaultCollectionName;
   $encryptedDatabaseName = 'medicalRecords';
   $encryptedCollectionName = 'patients';
   ```

   The following table describes each application variable in the code snippet:

   | Variable | Description |
   | --- | --- |
   | `kmsProviderName` | The KMS used to store your Customer Master Key. Set this environment variable to `"local"` in your `.env` file. |
   | `uri` | Your MongoDB connection URI. Set with the `MONGODB_URI` environment variable. |
   | `keyVaultDatabaseName` | The database where DEKs are stored. Set to `"encryption"`. |
   | `keyVaultCollectionName` | The collection where DEKs are stored. Set to `"__keyVault"`. |
   | `keyVaultNamespace` | The namespace in MongoDB where your DEKs are stored. Set this variable to the values of the `keyVaultDatabaseName` and `keyVaultCollectionName` variables, separated by a period. |
   | `encryptedDatabaseName` | The database where encrypted data is stored. Set to `"medicalRecords"`. |
   | `encryptedCollectionName` | The collection where encrypted data is stored. Set to `"patients"`. |

### Configure Encryption

After you set up your project, follow the steps in this section to create an encryption key and configure your application for Queryable Encryption.

1. Create an encryption key.

   Paste the following code into your `quickstart.php` file under the `// Paste code to generate CMK below` comment. This code snippet creates a 96-byte Customer Master Key and saves it to your filesystem as the file `customer-master-key.txt`:

   ```php
   if (!file_exists('./customer-master-key.txt')) {
       file_put_contents('./customer-master-key.txt', random_bytes(96));
   }
   ```

   **Warning: Secure your Local Key File in Production**

   We recommend storing your Customer Master Keys in a remote [Key Management System](https://en.wikipedia.org/wiki/Key_management#Key_management_system) (KMS (Key Management System)). To learn how to use a remote KMS (Key Management System) in your Queryable Encryption implementation, see the [Queryable Encryption Tutorials](/docs/manual/core/queryable-encryption/tutorials#std-label-qe-tutorial-automatic-encryption) guide.

   If you choose to use a local key provider in production, exercise great caution and do not store it on the file system. Consider injecting the key into your client application using a sidecar process, or use another approach that keeps the key secure.

2. Retrieve the Customer Master Key and specify the KMS provider settings.

   Paste the following code into your `quickstart.php` file under the `// Paste code to retrieve CMK and specify KMS provider settings below` comment to retrieve the contents of the `customer-master-key.txt` file you generated in the previous step:

   ```php
   // WARNING: Do not use a local key file in a production application
   $localMasterKey = file_get_contents('./customer-master-key.txt');
   $kmsProviders = [
       'local' => [
           'key' => new \MongoDB\BSON\Binary($localMasterKey),
       ],
   ];
   ```

   This code sets the provider name to `local` to use a Local Key Provider and uses the CMK (Customer Master Key) value from your KMS provider settings.

3. Set your automatic encryption options.

   Add the following code under the `// Paste automatic encryption options code below` comment to create an `$autoEncryptionOptions` array that contains the following options:

   - The namespace of your Key Vault collection

   - The `$kmsProviders` array, defined in the previous step

   - The path to your Automatic Encryption Shared Library

   ```php
   $autoEncryptionOptions = [
       'keyVaultNamespace' => $keyVaultNamespace,
       'kmsProviders' => $kmsProviders,
       'extraOptions' => [
           'cryptSharedLibPath' => getenv('SHARED_LIB_PATH'), // Path to your Automatic Encryption Shared Library
       ],
   ];
   ```

4. Create a client to set up an encrypted collection.

   Create a new client to encrypt and decrypt your collection. The client uses your connection URI and automatic encryption options. Paste the following code into your `quickstart.php` file, under the `// Paste client configuration code below` comment:

   ```php
   $encryptedClient = new \MongoDB\Client($uri, [], [
       'autoEncryption' => $autoEncryptionOptions,
   ]);
   ```

5. Specify fields to encrypt.

   To encrypt a field, add it to the encryption schema. To enable queries on a field, add the `queries` property. Paste the following code under the `// Paste schema below` comment:

   ```php
   $collectionOpts = [
       'encryptedFields' => [
           'fields' => [
               [
                   'path' => 'patientRecord.ssn',
                   'bsonType' => 'string',
                   'queries' => ['queryType' => 'equality'],
                   'keyId' => null,
               ],
               [
                   'path' => 'patientRecord.billing',
                   'bsonType' => 'object',
                   'keyId' => null,
               ],
           ],
       ],
   ];
   ```

   **Note:**

   The previous code sample encrypts both the `ssn` and `billing` fields. However, only the `ssn` field can be queried because it contains the `queries` property.

6. Create your encrypted collection.

   Add the following code blocks to your `quickstart.php` file, under the `// Paste code to create an encrypted collection below` comment in the order shown.

   First, instantiate a `ClientEncryption` object to access the API for the encryption helper methods:

   ```php
   $clientEncryption = $encryptedClient->createClientEncryption($autoEncryptionOptions);
   ```

   Because you are using a local Customer Master Key, you don't need to provide Customer Master Key credentials. Create a variable containing an empty array to use in place of credentials when you create your encrypted collection.

   ```php
   $customerMasterKeyCredentials = [];
   ```

   Create your encrypted collection by using the encryption helper method. This method automatically generates data encryption keys for your encrypted fields and creates the encrypted collection:

   ```php
   $encryptedClient->getDatabase($encryptedDatabaseName)->createEncryptedCollection(
       $encryptedCollectionName,
       $clientEncryption,
       $kmsProviderName,
       $customerMasterKeyCredentials,
       $collectionOpts,
   );
   ```

### Perform Encrypted Operations

After you configure your application and database connection, you can insert and query encrypted documents.

1. Insert a document with encrypted fields.

   Paste the following code under the `// Paste code to insert a document below` comment to create a document that stores patient data and insert it into the `patients` collection:

   ```php
   $patientDocument = [
       'patientName' => 'Jon Doe',
       'patientId' => 12345678,
       'patientRecord' => [
           'ssn' => '987-65-4320',
           'billing' => [
               'type' => 'Visa',
               'number' => '4111111111111111',
           ],
           'billAmount' => 1500,
       ],
   ];

   $encryptedCollection = $encryptedClient
       ->getDatabase($encryptedDatabaseName)
       ->getCollection($encryptedCollectionName);

   $result = $encryptedCollection->insertOne($patientDocument);
   ```

2. Query on encrypted data.

   Add the following code to your `quickstart.php` file under the `// Paste code to query the document below` comment:

   ```php
   $findResult = $encryptedCollection->findOne([
       'patientRecord.ssn' => '987-65-4320',
   ]);

   print(json_encode($findResult, JSON_PRETTY_PRINT));
   ```

3. Run your application.

   To start your application, run the following command from your project directory:

   ```bash
   php quickstart.php
   ```

   The output of the preceding code sample should look similar to the following:

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

### Set Up Your Project

Follow the steps in this section to create your project files and assign the required configuration variables.

1. Install dependencies.

   Create a directory named `ruby-qe` to store your project files. In this directory, create a file named `Gemfile` and paste the following code into the file:

   ```ruby
   # frozen_string_literal: true

   source "https://rubygems.org"

   gem "mongo"
   gem "dotenv"
   gem "bigdecimal"
   gem "logger"
   gem "ffi"
   gem "libmongocrypt-helper"

   ```

   This code declares the MongoDB Ruby driver, the `libmongocrypt-helper` gem that provides the encryption libraries required for Queryable Encryption, and the `dotenv` gem that reads your credentials from a `.env` file.

   Then, run the following commands to navigate into the directory and install the gems:

   ```bash
   cd ruby-qe
   bundle install
   ```

2. Set up your environment variables.

   In your `ruby-qe` directory, create a `.env` file. The sample code in this tutorial references environment variables that you need to set in this `.env` file. Paste the following code into this file:

   ```bash
   # MongoDB connection uri and automatic encryption shared library path

   MONGODB_URI="<Your MongoDB URI>"
   SHARED_LIB_PATH="<Full path to your Automatic Encryption Shared Library>"

   # KMS Provider (local, aws, azure, gcp, or kmip)

   KMS_PROVIDER="local"

   ```

   Replace the following placeholder values:

   - `<Your MongoDB URI>`: Your MongoDB deployment connection URI.

   - `<Full path to your Automatic Encryption Shared Library>`: The full path to your Automatic Encryption Shared Library, which resembles the following paths:

     - **macOS**: `/<crypt shared directory>/lib/mongo_crypt_v1.dylib`

     - **Linux**: `/<crypt shared directory>/lib/mongo_crypt_v1.so`

     - **Windows**: `C:\<crypt shared directory>\bin\mongo_crypt_v1.dll`

   For more information on setting up environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/ruby/README.md) file included in the sample application on GitHub.

3. Create your main project file.

   In your `ruby-qe` directory, create a file named `quickstart.rb`. Paste the following starter code into this file. The placeholder comments indicate where you will add code in future steps of this tutorial:

   ```ruby
   # frozen_string_literal: true

   require "dotenv/load"
   require "mongo"
   require "securerandom"

   # Paste application variables below

   # Paste code to generate CMK below

   # Paste code to retrieve CMK and specify KMS provider settings below

   # Paste automatic encryption options code below

   # Paste client configuration code below

   # Paste schema below

   # Paste code to create an encrypted collection below

   # Paste code to insert a document below

   # Paste code to query the document below

   encrypted_client.close
   ```

4. Assign your application variables.

   Declare the required application variables by pasting the following code into your `quickstart.rb` file under the `# Paste application variables below` comment:

   ```ruby
   kms_provider_name = ENV["KMS_PROVIDER"]
   uri = ENV["MONGODB_URI"] # Your connection URI
   key_vault_database_name = "encryption"
   key_vault_collection_name = "__keyVault"
   key_vault_namespace = "#{key_vault_database_name}.#{key_vault_collection_name}"
   encrypted_database_name = "medicalRecords"
   encrypted_collection_name = "patients"
   ```

   The following table describes each application variable in the code snippet:

   | Variable | Description |
   | --- | --- |
   | `kms_provider_name` | The KMS used to store your Customer Master Key. Set with the `KMS_PROVIDER` environment variable. |
   | `uri` | Your MongoDB connection URI. Set with the `MONGODB_URI` environment variable. |
   | `key_vault_database_name` | The database where DEKs are stored. Set to `"encryption"`. |
   | `key_vault_collection_name` | The collection where DEKs are stored. Set to `"__keyVault"`. |
   | `key_vault_namespace` | The namespace in MongoDB where your DEKs are stored. Set this variable to the values of the `key_vault_database_name` and `key_vault_collection_name` variables, separated by a period. |
   | `encrypted_database_name` | The database where encrypted data is stored. Set to `"medicalRecords"`. |
   | `encrypted_collection_name` | The collection where encrypted data is stored. Set to `"patients"`. |

### Configure Encryption

After you set up your project, follow the steps in this section to create an encryption key and configure your application for Queryable Encryption.

1. Create an encryption key.

   Paste the following code into your `quickstart.rb` file under the `# Paste code to generate CMK below` comment. This code snippet creates a 96-byte Customer Master Key and saves it to your filesystem as the file `customer-master-key.txt`:

   ```ruby
   unless File.exist?("./customer-master-key.txt")
     File.binwrite("./customer-master-key.txt", SecureRandom.random_bytes(96))
   end
   ```

   **Warning: Secure your Local Key File in Production**

   We recommend storing your Customer Master Keys in a remote [Key Management System](https://en.wikipedia.org/wiki/Key_management#Key_management_system) (KMS (Key Management System)). To learn how to use a remote KMS (Key Management System) in your Queryable Encryption implementation, see the [Queryable Encryption Tutorials](/docs/manual/core/queryable-encryption/tutorials#std-label-qe-tutorial-automatic-encryption) guide.

   If you choose to use a local key provider in production, exercise great caution and do not store it on the file system. Consider injecting the key into your client application using a sidecar process, or use another approach that keeps the key secure.

2. Retrieve the Customer Master Key and specify the KMS provider settings.

   Paste the following code into your `quickstart.rb` file under the `# Paste code to retrieve CMK and specify KMS provider
               settings below` comment to retrieve the contents of the `customer-master-key.txt` file you generated in the previous step:

   ```ruby
   # WARNING: Do not use a local key file in a production application
   local_master_key = File.binread("./customer-master-key.txt")

   raise "Expected the customer master key file to be 96 bytes." unless local_master_key.bytesize == 96

   kms_providers = {
     local: {
       key: local_master_key
     }
   }
   ```

   This code sets the provider name to `local` to use a Local Key Provider and uses the CMK (Customer Master Key) value from your KMS provider settings.

3. Set your automatic encryption options.

   Add the following code under the `# Paste automatic encryption
               options code below` comment to create an `auto_encryption_options` hash that contains the following options:

   - The namespace of your Key Vault collection

   - The `kms_providers` hash, defined in the previous step

   - The `extra_options` hash, which contains the path to your Automatic Encryption Shared Library

   ```ruby
   auto_encryption_options = {
     key_vault_namespace: key_vault_namespace,
     kms_providers: kms_providers,
     extra_options: {
       crypt_shared_lib_path: ENV["SHARED_LIB_PATH"] # Path to your Automatic Encryption Shared Library
     }
   }
   ```

4. Create a client to set up an encrypted collection.

   Create a new client to encrypt and decrypt your collection. The client uses your connection URI and automatic encryption options. Paste the following code into your `quickstart.rb` file, under the `# Paste client configuration code below` comment:

   ```ruby
   encrypted_client = Mongo::Client.new(uri, auto_encryption_options: auto_encryption_options)
   ```

5. Specify fields to encrypt.

   To encrypt a field, add it to the encryption schema. To enable queries on a field, add the `queries` property. Paste the following code under the `# Paste schema below` comment:

   ```ruby
   collection_opts = {
     encrypted_fields: {
       fields: [
         {
           path: "patientRecord.ssn",
           bsonType: "string",
           queries: { queryType: "equality" },
           keyId: nil
         },
         {
           path: "patientRecord.billing",
           bsonType: "object",
           keyId: nil
         }
       ]
     }
   }
   ```

   **Note:**

   The previous code sample encrypts both the `ssn` and `billing` fields. However, only the `ssn` field can be queried because it contains the `queries` property.

6. Create your encrypted collection.

   Add the following code blocks to your `quickstart.rb` file, under the `# Paste code to create an encrypted collection below` comment in the order shown.

   First, instantiate a `Mongo::ClientEncryption` object to access the API for the encryption helper methods:

   ```ruby
   client_encryption = Mongo::ClientEncryption.new(
     encrypted_client,
     key_vault_namespace: auto_encryption_options[:key_vault_namespace],
     kms_providers: auto_encryption_options[:kms_providers]
   )
   ```

   Because you are using a local Customer Master Key, you don't need to provide Customer Master Key credentials. Create a variable containing an empty hash to use in place of credentials when you create your encrypted collection:

   ```ruby
   customer_master_key_credentials = {}
   ```

   Create your encrypted collection by using the `create_encrypted_collection()` helper method accessed through the `Mongo::ClientEncryption` class. This method automatically generates data encryption keys for your encrypted fields and creates the encrypted collection:

   ```ruby
   client_encryption.create_encrypted_collection(
     encrypted_client.use(encrypted_database_name).database,
     encrypted_collection_name,
     collection_opts,
     kms_provider_name,
     customer_master_key_credentials
   )
   ```

### Perform Encrypted Operations

After you configure your application and database connection, you can insert and query encrypted documents.

1. Insert a document with encrypted fields.

   Paste the following code under the `# Paste code to insert a
               document below` comment to create a document that stores patient data and insert it into the `patients` collection:

   ```ruby
   patient_document = {
     patientName: "Jon Doe",
     patientId: 12345678,
     patientRecord: {
       ssn: "987-65-4320",
       billing: {
         type: "Visa",
         number: "4111111111111111"
       },
       billAmount: 1500
     }
   }

   encrypted_collection = encrypted_client
     .use(encrypted_database_name)[encrypted_collection_name]

   result = encrypted_collection.insert_one(patient_document)
   ```

2. Query on encrypted data.

   Add the following code to your `quickstart.rb` file under the `# Paste code to query the document below` comment:

   ```ruby
   find_result = encrypted_collection.find("patientRecord.ssn" => "987-65-4320").first
   puts find_result.inspect
   ```

3. Run your application.

   To start your application, run the following command from your project directory:

   ```bash
   bundle exec ruby quickstart.rb
   ```

   The driver decrypts the encrypted fields automatically when it returns the document. The output of the preceding code sample should look similar to the following:

   ```none
   {"_id" => BSON::ObjectId('6a8611235f1548b277869df7'),
   "patientName" => "Jon Doe", "patientId" => 12345678,
   "patientRecord" => {"ssn" => "987-65-4320", "billing" =>
   {"type" => "Visa", "number" => "4111111111111111"}, "billAmount" => 1500},
   "__safeContent__" => [<BSON::Binary:0x744 type=generic data=0xc464ecc34a383129...>]}
   ```

   **Warning: Do not Modify the \_\_safeContent\_\_ Field**

   The `__safeContent__` field is essential to Queryable Encryption. Do not modify the contents of this field.

In this tutorial, you created an application that automatically encrypts and decrypts the `ssn` and `billing` fields in your `patients` collection. Because your application uses an encrypted client, the query returns the decrypted field values. A client that is not configured with your encryption keys would see the encrypted values for those fields instead.

## Learn More

To view a tutorial on production-ready Queryable Encryption with a remote KMS, see [Queryable Encryption Tutorials.](/docs/manual/core/queryable-encryption/tutorials#std-label-qe-tutorial-automatic-encryption)

To learn how Queryable Encryption works, see [Queryable Encryption Fundamentals.](/docs/manual/core/queryable-encryption/fundamentals#std-label-qe-fundamentals)

To learn more about the topics mentioned in this guide, see the following links:

- Learn more about Queryable Encryption components on the [Reference](/docs/manual/core/queryable-encryption/reference#std-label-qe-reference) page.

- Learn how Customer Master Keys and Data Encryption Keys work on the [Encryption Keys and Key Vaults](/docs/manual/core/queryable-encryption/fundamentals/keys-key-vaults#std-label-qe-reference-keys-key-vaults) page.

- See how KMS Providers manage your Queryable Encryption keys on the [KMS Providers](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-fundamentals-kms-providers) page.
