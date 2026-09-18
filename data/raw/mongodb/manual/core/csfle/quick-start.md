> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# CSFLE Quick Start

## Overview

In this tutorial, you can learn how to use automatic Client-Side Field Level Encryption (CSFLE) and a MongoDB driver to encrypt a document.

The tutorial includes the following sections:

- **Set Up Your Project**: Set up your project files and assign required variables.

- **Configure Encryption**: Create an encryption key and configure your application for Client-Side Field Level Encryption.

- **Perform Encrypted Operations**: Insert and query encrypted documents.

**Important: Do Not Use this Application In Production**

Since this example application stores an encryption key on your application's filesystem, you risk unauthorized access to the key or loss of the key to decrypt your data.

To view a tutorial that demonstrates how to create a production-ready CSFLE-enabled application, see [CSFLE Tutorials.](/docs/manual/core/csfle/tutorials#std-label-csfle-tutorial-automatic-encryption)

### Prerequisites

Before you begin this tutorial, complete the following prerequisite steps:

1. Download the Automatic Encryption Shared Library from the [MongoDB Download Center](https://www.mongodb.com/try/download/enterprise?tck=docs). Navigate to the MongoDB Enterprise Server Download section and select the follow options:

   - In the Version dropdown, select the version marked as `"current"`.

   - In the Platform dropdown, select your platform.

   - In the Package dropdown, select `crypt_shared`.

   Extract the archive and save the path to the shared library file for future use.

   **Note: Query Analysis Component**

   The Automatic Encryption Shared Library is a preferred alternative to `mongocryptd` and does not require spawning a new process to perform automatic encryption. This tutorial uses the Automatic Encryption Shared Library, but `mongocryptd` is still supported.

2. Configure a MongoDB Atlas cluster or a local replica set deployment, and save your connection string for future use. To learn more, see the [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) tutorial.

### Full Application Code

[Complete Java Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/csfle/java/src/main/java/com/mongodb/csfle/)

[Complete Node.js Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/csfle/nodejs/)

[Complete Python Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/csfle/python/)

[Complete C# Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/csfle/csharp/)

[Complete Go Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/csfle/go/)

[Complete Ruby Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/csfle/ruby/)

## Tutorial

### Set Up Your Project

Follow the steps in this section to create your project files and assign the required configuration variables.

1. Install the dependencies.

   In an Integrated Development Environment (IDE), create a new Maven project named `JavaCSFLE`. Then, navigate to the `pom.xml` file and add the following dependencies:

   ```xml
   <dependencies>
      <dependency>
         <groupId>org.mongodb</groupId>
         <artifactId>mongodb-driver-sync</artifactId>
         <version>5.6.0</version>
      </dependency>
      <dependency>
         <groupId>org.mongodb</groupId>
         <artifactId>mongodb-crypt</artifactId>
         <version>5.6.0</version>
      </dependency>
   </dependencies>
   ```

   This code installs the MongoDB Java Sync Driver and the `mongodb-crypt` package, which provides the necessary classes for Client-Side Field Level Encryption and Queryable Encryption operations.

2. Create your main project file.

   In your `JavaCSFLE` project, navigate to the `Main.java` file and replace its contents with the following code:

   ```java
   package com.mongodb.csfle;

   public class Main {
       public static void main(String[] args) throws Exception {
           System.out.println("=".repeat(60));
           System.out.println("Running MakeDataKey...");
           System.out.println("=".repeat(60));
           MakeDataKey.main(new String[]{});
           System.out.println("=".repeat(60));
           System.out.println("Running InsertEncryptedDocument...");
           System.out.println("=".repeat(60));
           InsertEncryptedDocument.main(new String[]{});
           System.out.println("=".repeat(60));
           System.out.println("All scripts completed successfully!");
           System.out.println("=".repeat(60));
       }
   }

   ```

   The `Main.java` file contains your main method, which runs the code from the other project files. In this tutorial, the file is in the `com/mongodb/csfle` base package directory, but you can use a different directory and replace the package name in the code.

3. Create your data key file.

   To generate a Customer Master Key and Data Encryption Key, create a file named `MakeDataKey.java` in your project's base package directory. Then, paste the following code into the file:

   ```java
   package com.mongodb.csfle;

   import java.io.*;
   import java.nio.file.*;
   import java.security.SecureRandom;
   import java.util.*;
   import java.util.Base64;

   import org.bson.BsonBinary;
   import org.bson.BsonBoolean;
   import org.bson.BsonDocument;
   import org.bson.BsonInt32;
   import com.mongodb.ClientEncryptionSettings;
   import com.mongodb.ConnectionString;
   import com.mongodb.MongoClientSettings;
   import com.mongodb.client.MongoClient;
   import com.mongodb.client.MongoClients;
   import com.mongodb.client.model.IndexOptions;
   import com.mongodb.client.model.vault.DataKeyOptions;
   import com.mongodb.client.vault.ClientEncryption;
   import com.mongodb.client.vault.ClientEncryptions;

   public class MakeDataKey {
       public static void main(String[] args) throws Exception {
           // Paste CMK generation code below

           // Paste index creation code below

           // Paste DEK generation code below
       }
   }
   ```

   In future steps, you will add code to this file under each corresponding comment.

4. Create your encrypted operations file.

   Next, create a file named `InsertEncryptedDocument.java` in your base package directory and paste the following code:

   ```java
   package com.mongodb.csfle;

   import java.nio.file.*;
   import java.util.*;

   import static com.mongodb.client.model.Filters.eq;

   import com.mongodb.AutoEncryptionSettings;
   import com.mongodb.ConnectionString;
   import com.mongodb.MongoClientSettings;
   import com.mongodb.client.MongoClient;
   import com.mongodb.client.MongoClients;
   import org.bson.BsonDocument;
   import org.bson.Document;

   public class InsertEncryptedDocument {
       public static void main(String[] args) throws Exception {
           Map<String, Map<String, Object>> kmsProviders =
               Config.getKmsProviders();

           // Paste JSON schema below

           // Paste client configuration code below

           // Paste code to insert a document below

           // Paste code to query the document below
       }
   }
   ```

   In future steps, you will add code that inserts and queries encrypted documents under each corresponding comment.

5. Assign your configuration variables.

   Each of your project files use variables from a configuration class. Create a file named `Config.java` in your base package directory and paste the following code:

   ```java
   package com.mongodb.csfle;

   import java.io.FileInputStream;
   import java.util.HashMap;
   import java.util.Map;

   public class Config {
       public static final String CONNECTION_STRING = "<connection string>";
       public static final String KEY_VAULT_DB = "encryption";
       public static final String KEY_VAULT_COLL = "__keyVault";
       public static final String KEY_VAULT_NAMESPACE =
           KEY_VAULT_DB + "." + KEY_VAULT_COLL;
       public static final String MASTER_KEY_PATH = "master-key.txt";
       public static final String DEK_ID_PATH = "dek_id.txt";
       public static final String CRYPT_SHARED_LIB_PATH =
           "<Automatic Encryption Shared Library path>";

       public static Map<String, Map<String, Object>> getKmsProviders()
               throws Exception {
           byte[] localMasterKey = new byte[96];
           try (FileInputStream fis = new FileInputStream(MASTER_KEY_PATH)) {
               if (fis.read(localMasterKey) < 96) {
                   throw new Exception(
                       "Expected 96 bytes from master key file");
               }
           }
           Map<String, Object> keyMap = new HashMap<>();
           keyMap.put("key", localMasterKey);
           Map<String, Map<String, Object>> kmsProviders = new HashMap<>();
           kmsProviders.put("local", keyMap);
           return kmsProviders;
       }
   }

   ```

   Then, replace the following placeholder values:

   - `<connection string>`: Your MongoDB [connection string](/docs/manual/reference/connection-string#std-label-mongodb-uri)

   - `<Automatic Encryption Shared Library path>`: The full path to your Automatic Encryption Shared Library, which resembles the following paths:

     - **macOS**: `/<crypt shared directory>/lib/mongo_crypt_v1.dylib`

     - **Linux**: `/<crypt shared directory>/lib/mongo_crypt_v1.so`

     - **Windows**: `C:\<crypt shared directory>\bin\mongo_crypt_v1.dll`

   The `Config.java` class instructs your application to store data encryption keys in the `encryption.__keyVault` namespace.

### Configure Encryption

After setting up your project, follow the steps in this section to create an encryption key and configure your application for CSFLE.

1. Create a Customer Master Key.

   Paste the following code into your `MakeDataKey.java` file under the `// Paste CMK generation code below` comment to generate a 96-byte Customer Master Key (CMK (Customer Master Key)) and save it to your filesystem when you run the application:

   ```java
   byte[] localMasterKey = new byte[96];
   new SecureRandom().nextBytes(localMasterKey);
   try (FileOutputStream fos =
           new FileOutputStream(Config.MASTER_KEY_PATH)) {
       fos.write(localMasterKey);
   }
   ```

   **Warning: Secure your Local Key File in Production**

   We recommend storing your Customer Master Keys in a remote [Key Management System](https://en.wikipedia.org/wiki/Key_management#Key_management_system) (KMS (Key Management System)). To learn how to use a remote KMS (Key Management System) in your Queryable Encryption implementation, see the [Queryable Encryption Tutorials](/docs/manual/core/queryable-encryption/tutorials#std-label-qe-tutorial-automatic-encryption) guide.

   If you choose to use a local key provider in production, exercise great caution and do not store it on the file system. Consider injecting the key into your client application using a sidecar process, or use another approach that keeps the key secure.

2. Create a unique index on your Key Vault collection.

   Client-Side Field Level Encryption depends on server-enforced uniqueness of key alternate names, so you must create a unique index on the `keyAltNames` field in your Key Vault collection.

   Add the following code to your `MakeDataKey.java` file under the `// Paste index creation code below` comment to connect to MongoDB and create a partial unique index on the `keyAltNames` field:

   ```java
   try (MongoClient keyVaultClient =
           MongoClients.create(Config.CONNECTION_STRING)) {
       keyVaultClient.getDatabase(Config.KEY_VAULT_DB)
           .getCollection(Config.KEY_VAULT_COLL).drop();
       keyVaultClient.getDatabase("medicalRecords")
           .getCollection("patients").drop();
       IndexOptions indexOpts = new IndexOptions()
           .partialFilterExpression(new BsonDocument("keyAltNames",
               new BsonDocument("$exists", new BsonBoolean(true))))
           .unique(true);
       keyVaultClient.getDatabase(Config.KEY_VAULT_DB)
           .getCollection(Config.KEY_VAULT_COLL)
           .createIndex(new BsonDocument("keyAltNames",
               new BsonInt32(1)), indexOpts);
   }
   ```

3. Create a Data Encryption Key.

   Add the following code to your `MakeDataKey.java` file under the `// Paste DEK generation code below` comment to configure a `ClientEncryption` instance and generate a Data Encryption Key:

   ```java
   Map<String, Map<String, Object>> kmsProviders =
       Config.getKmsProviders();
   ClientEncryptionSettings encryptionSettings =
       ClientEncryptionSettings.builder()
           .keyVaultMongoClientSettings(MongoClientSettings.builder()
               .applyConnectionString(
                   new ConnectionString(Config.CONNECTION_STRING))
               .build())
           .keyVaultNamespace(Config.KEY_VAULT_NAMESPACE)
           .kmsProviders(kmsProviders)
           .build();
   try (ClientEncryption clientEncryption =
           ClientEncryptions.create(encryptionSettings)) {
       BsonBinary dataKeyId = clientEncryption.createDataKey(
           "local", new DataKeyOptions());
       String base64DataKeyId = Base64.getEncoder()
           .encodeToString(dataKeyId.getData());
       System.out.println("DataKeyId [base64]: " + base64DataKeyId);
       Files.write(Paths.get(Config.DEK_ID_PATH),
           base64DataKeyId.getBytes());
   }
   ```

   The `ClientEncryption` instance uses your KMS provider credentials, key vault namespace, and your connection settings to manage encryption keys. Once configured, the code calls `createDataKey()` to generate a Data Encryption Key and writes the key ID to a file.

4. Define a JSON schema.

   Add the following code to your `InsertEncryptedDocument.java` file under the `// Paste JSON schema below` comment to define an encryption schema:

   ```java
   String dekId = new String(
       Files.readAllBytes(Paths.get(Config.DEK_ID_PATH))).trim();
   Document jsonSchema = new Document()
       .append("bsonType", "object")
       .append("encryptMetadata", new Document()
           .append("keyId", new ArrayList<>(Arrays.asList(
               new Document()
                   .append("$binary", new Document()
                       .append("base64", dekId)
                       .append("subType", "04"))))))
       .append("properties", new Document()
           .append("ssn", new Document()
               .append("encrypt", new Document()
                   .append("bsonType", "int")
                   .append("algorithm",
                       "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic")))
           .append("bloodType", new Document()
               .append("encrypt", new Document()
                   .append("bsonType", "string")
                   .append("algorithm",
                       "AEAD_AES_256_CBC_HMAC_SHA_512-Random")))
           .append("medicalRecords", new Document()
               .append("encrypt", new Document()
                   .append("bsonType", "array")
                   .append("algorithm",
                       "AEAD_AES_256_CBC_HMAC_SHA_512-Random")))
           .append("insurance", new Document()
               .append("bsonType", "object")
               .append("properties", new Document()
                   .append("policyNumber", new Document()
                       .append("encrypt", new Document()
                           .append("bsonType", "int")
                           .append("algorithm",
                               "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic"))))));
   Map<String, BsonDocument> schemaMap = new HashMap<>();
   schemaMap.put("medicalRecords.patients",
       BsonDocument.parse(jsonSchema.toJson()));
   ```

   The code reads your DEK (Data Encryption Key) ID and uses it to encrypt the following fields in the `medicalRecords.patients` collection:

   - `insurance.policyNumber`: Encrypted with deterministic encryption

   - `ssn`: Encrypted with deterministic encryption

   - `bloodType`: Encrypted with random encryption

   - `medicalRecords`: Encrypted with random encryption

   Deterministic encryption allows you to perform equality queries on the encrypted fields. Random encryption provides stronger security for fields that you don't need to query, because this algorithm does not support read operations on the encrypted fields.

5. Create a standard and a CSFLE-enabled client.

   Paste the following code into your `InsertEncryptedDocument.java` file under the `// Paste client configuration code below` comment to create two MongoDB clients:

   ```java
   Map<String, Object> extraOptions = new HashMap<>();
   extraOptions.put("cryptSharedLibPath", Config.CRYPT_SHARED_LIB_PATH);
   MongoClientSettings clientSettings = MongoClientSettings.builder()
       .applyConnectionString(
           new ConnectionString(Config.CONNECTION_STRING))
       .autoEncryptionSettings(AutoEncryptionSettings.builder()
           .keyVaultNamespace(Config.KEY_VAULT_NAMESPACE)
           .kmsProviders(kmsProviders)
           .schemaMap(schemaMap)
           .extraOptions(extraOptions)
           .build())
       .build();
   MongoClient mongoClientRegular = MongoClients.create(Config.CONNECTION_STRING);
   MongoClient mongoClientSecure = MongoClients.create(clientSettings);
   ```

   This code creates a `MongoClient` instance with `AutoEncryptionSettings` that specify your KMS provider credentials, key vault namespace, encryption schema, and the location of your Automatic Encryption Shared Library. The code also creates a standard `MongoClient` instance without automatic encryption. In a future step, you will compare the output of both clients.

   **Note: Automatic Encryption Options**

   The automatic encryption options provide configuration information to the Automatic Encryption Shared Library, which modifies the application's behavior when accessing encrypted fields.

   To learn more about the Automatic Encryption Shared Library, see the [Install and Configure a CSFLE Query Analysis Component](/docs/manual/core/csfle/reference/install-library#std-label-csfle-reference-shared-library) page.

### Perform Encrypted Operations

After configuring your application and database connection, follow the steps in this section to insert and query encrypted documents.

1. Insert a document with encrypted fields.

   Add the following code to your `InsertEncryptedDocument.java` file under the `// Paste code to insert a document below` comment to insert a document into the `medicalRecords.patients` collection:

   ```java
   ArrayList<Document> medicalRecords = new ArrayList<>();
   medicalRecords.add(new Document().append("weight", 180));
   medicalRecords.add(
       new Document().append("bloodPressure", "120/80"));
   Document insurance = new Document()
       .append("policyNumber", 123142)
       .append("provider", "MaestCare");
   Document patient = new Document()
       .append("name", "Jon Doe")
       .append("ssn", 241014209)
       .append("bloodType", "AB+")
       .append("medicalRecords", medicalRecords)
       .append("insurance", insurance);
   mongoClientSecure.getDatabase("medicalRecords")
       .getCollection("patients").insertOne(patient);
   ```

   When you insert the document, your CSFLE-enabled client automatically encrypts the specified fields. The stored document resembles the following JSON:

   ```json
   {
     "_id": { "$oid": "<_id of your document>" },
     "name": "Jon Doe",
     "ssn": {
       "$binary": "<cipher-text>",
       "$type": "6"
     },
     "bloodType": {
       "$binary": "<cipher-text>",
       "$type": "6"
     },
     "medicalRecords": {
       "$binary": "<cipher-text>",
       "$type": "6"
     },
     "insurance": {
       "provider": "MaestCare",
       "policyNumber": {
         "$binary": "<cipher-text>",
         "$type": "6"
       }
     }
   }

   ```

2. Query encrypted data.

   Add the following code to your `InsertEncryptedDocument.java` file under the `// Paste code to query the document below` comment to retrieve the document with both a CSFLE-enabled client and a standard client:

   ```java
   System.out.println(
       "Finding a document with the regular (non-encrypted) client:");
   Document docRegular = mongoClientRegular
       .getDatabase("medicalRecords").getCollection("patients")
       .find(eq("name", "Jon Doe")).first();
   System.out.println(docRegular.toJson());
   System.out.println(
       "Finding a document with the encrypted client:");
   Document docSecure = mongoClientSecure
       .getDatabase("medicalRecords").getCollection("patients")
       .find(eq("name", "Jon Doe")).first();
   System.out.println(docSecure.toJson());
   ```

   The CSFLE-enabled client automatically decrypts the encrypted fields when it retrieves the document. The standard client returns the encrypted binary values.

3. Run the application.

   Start the application by running the `Main.java` file in your IDE.

   If successful, your output resembles the following example:

   ```none
   ============================================================
   Running MakeDataKey...
   ============================================================
   DataKeyId [base64]: ...

   ============================================================
   Running InsertEncryptedDocument...
   ============================================================
   Finding a document with the regular (non-encrypted) client:
   {"_id": {"$oid": "..."}, "name": "Jon Doe", "ssn": {"$binary":
   {"base64": "ARYntz2D/ENqpAa9E1JcGi8QBX2oPBS6MfdE16XiOvjs7ZrUZtTFzlCHr4zeujm2FnDNDJynNRZfCFbHBAOnXNCU8Ey92IFQZtaQIoc4lcPWhg==", "subType": "06"}},
   "bloodType": {"$binary": {"base64": "AhYntz2D/ENqpAa9E1JcGi8CMgflFgLG6FIAQEhXlxrreDUVFVl5h68KFcet0ANaFUfclf7aN200NGzw/lxUom53jSiYD95iI8rbjm/LlGcN+w==", "subType": "06"}},
   "medicalRecords": {"$binary": {"base64": "AhYntz2D/ENqpAa9E1JcGi8EFRrvY5sDeZc0lOxk7yQj7GK7hUAd2iSFq+uF3F6zt2toE4nNw3nTIDUzX/9W2H+YLGvucHaTk6Z7L9FPpsluNXGY65hPlr6OfVJWcfF/a1gGqDCfS1P02WVDbJQ9PPyHPXEAYzC6Z+DTPNMTU1CSsA==", "subType": "06"}},
   "insurance": {"policyNumber": {"$binary": {"base64": "ARYntz2D/ENqpAa9E1JcGi8Qveejc6QQdkMIX28awKMugoZdO5fLJeMsflTzOl1eOHlorQ/arY5gXWqa+Gvsrj/aWe4l22V0jM5RSwIw8/sVEQ==", "subType": "06"}},
   "provider": "MaestCare"}}
   Finding a document with the encrypted client:
   {"_id": {"$oid": "..."}, "name": "Jon Doe", "ssn": 241014209, "bloodType": "AB+", "medicalRecords":
   [{"weight": 180}, {"bloodPressure": "120/80"}], "insurance": {"policyNumber": 123142, "provider": "MaestCare"}}

   ============================================================
   All scripts completed successfully!
   ============================================================
   ```

   The output includes your DEK (Data Encryption Key) ID, the encrypted document as stored in your database, and the decrypted document retrieved with your CSFLE-enabled client.

### Set Up Your Project

Follow the steps in this section to create your project files and assign the required configuration variables.

1. Install the dependencies.

   Create a directory named `nodeCSFLE` to store your project files. From this directory, run the following commands to initialize your project and install the required packages:

   ```bash
   npm init -y
   npm install mongodb mongodb-client-encryption
   ```

   Then, open the generated `package.json` file. To use [ECMAScript modules](https://nodejs.org/api/esm.html#modules-ecmascript-modules), the standard format for packaging JavaScript code for reuse, replace the existing line that specifies the `"type"` field with the following line:

   ```json
   "type": "module"
   ```

2. Create your main project file.

   Add a file named `main.js` to your `nodeCSFLE` directory. Paste the following code into this file:

   ```javascript
   import { makeKey } from "./makeDataKey.js";
   import { insert } from "./insertEncryptedDocument.js";

   const separator = "=".repeat(60);

   async function main() {
     console.log(separator);
     console.log("Running makeDataKey.js...");
     console.log(separator);
     await makeKey();

     console.log(separator);
     console.log("Running insertEncryptedDocument.js...");
     console.log(separator);
     await insert();

     console.log(separator);
     console.log("All scripts completed successfully!");
     console.log(separator);
   }

   main().catch((err) => {
     console.error(err);
     process.exit(1);
   });

   ```

   The `main.js` file contains your main function, which imports and runs the code from the other project files.

3. Create your data key file.

   To generate a Customer Master Key and Data Encryption Key, create a file named `makeDataKey.js` in your `nodeCSFLE` directory and paste the following code:

   ```javascript
   import { MongoClient, ClientEncryption } from "mongodb";
   import fs from "fs";
   import crypto from "crypto";
   import * as config from "./config.js";

   // Paste CMK generation code below

   async function makeKey() {
     // Paste index creation code below

     // Paste DEK creation code below
   }

   export { makeKey };
   ```

   In future steps, you will add code to this file under each corresponding comment.

4. Create your encrypted operations file.

   Next, create a file named `insertEncryptedDocument.js` in your `nodeCSFLE` directory and paste the following code:

   ```javascript
   import { MongoClient, Binary } from "mongodb";
   import fs from "fs";
   import * as config from "./config.js";

   async function insert() {
     // Paste JSON schema below

     // Paste client configuration code below

     // Paste code to insert a document below

     // Paste code to query the document below
   }

   export { insert };
   ```

   In future steps, you will add code that inserts and queries encrypted documents under each corresponding comment.

5. Assign your configuration variables.

   Each of your project files imports variables from a configuration file. Create a file named `config.js` in your `nodeCSFLE` directory and paste the following code:

   ```javascript
   import fs from "fs";

   const connectionString = "<connection string>";
   const keyVaultDb = "encryption";
   const keyVaultColl = "__keyVault";
   const keyVaultNamespace = `${keyVaultDb}.${keyVaultColl}`;
   const masterKeyPath = "./master-key.txt";
   const dekIdPath = "./dek_id.txt";
   const cryptSharedLibPath = "<Automatic Encryption Shared Library path>";

   function getKmsProviders() {
     const localMasterKey = fs.readFileSync(masterKeyPath);
     return { local: { key: localMasterKey } };
   }

   export {
     connectionString,
     keyVaultNamespace,
     masterKeyPath,
     dekIdPath,
     cryptSharedLibPath,
     getKmsProviders,
   };

   ```

   Then, replace the following placeholder values:

   - `<connection string>`: Your MongoDB connection string

   - `<Automatic Encryption Shared Library path>`: The full path to your Automatic Encryption Shared Library, which resembles the following paths:

     - **macOS**: `/<crypt shared directory>/lib/mongo_crypt_v1.dylib`

     - **Linux**: `/<crypt shared directory>/lib/mongo_crypt_v1.so`

     - **Windows**: `C:\<crypt shared directory>\bin\mongo_crypt_v1.dll`

   The `config.js` file instructs your application to store data encryption keys in the `encryption.__keyVault` namespace.

### Configure Encryption

After setting up your project, follow the steps in this section to create an encryption key and configure your application for CSFLE.

1. Create a Customer Master Key.

   Paste the following code into your `makeDataKey.js` file under the `// Paste CMK generation code below` comment. This code generates a 96-byte Customer Master Key (CMK (Customer Master Key)) and saves it to your filesystem:

   ```javascript
   fs.writeFileSync(config.masterKeyPath, crypto.randomBytes(96));
   ```

   **Warning: Secure your Local Key File in Production**

   We recommend storing your Customer Master Keys in a remote [Key Management System](https://en.wikipedia.org/wiki/Key_management#Key_management_system) (KMS (Key Management System)). To learn how to use a remote KMS (Key Management System) in your Queryable Encryption implementation, see the [Queryable Encryption Tutorials](/docs/manual/core/queryable-encryption/tutorials#std-label-qe-tutorial-automatic-encryption) guide.

   If you choose to use a local key provider in production, exercise great caution and do not store it on the file system. Consider injecting the key into your client application using a sidecar process, or use another approach that keeps the key secure.

2. Create a unique index on your Key Vault collection.

   Client-Side Field Level Encryption depends on server-enforced uniqueness of key alternate names, so you must create a unique index on the `keyAltNames` field in your Key Vault collection.

   Add the following code to your `makeDataKey.js` file under the `// Paste index creation code below` comment to connect to MongoDB and create a partial unique index on the `keyAltNames` field:

   ```javascript
   const keyVaultClient = new MongoClient(config.connectionString);
   await keyVaultClient.connect();
   const keyVaultDb = keyVaultClient.db("encryption");
   await keyVaultDb.dropDatabase();
   await keyVaultClient.db("medicalRecords").dropDatabase();
   const keyVaultColl = keyVaultDb.collection("__keyVault");
   await keyVaultColl.createIndex(
     { keyAltNames: 1 },
     {
       unique: true,
       partialFilterExpression: { keyAltNames: { $exists: true } },
     }
   );
   await keyVaultClient.close();
   ```

3. Create a Data Encryption Key.

   Add the following code to your `makeDataKey.js` file under the `// Paste DEK creation code below` comment to configure a `ClientEncryption` instance and generate a Data Encryption Key:

   ```javascript
   const client = new MongoClient(config.connectionString);
   await client.connect();
   const encryption = new ClientEncryption(client, {
     keyVaultNamespace: config.keyVaultNamespace,
     kmsProviders: config.getKmsProviders(),
   });
   const key = await encryption.createDataKey("local");
   const base64DekId = key.toString("base64");
   console.log("DataKeyId [base64]: ", base64DekId);
   fs.writeFileSync(config.dekIdPath, base64DekId);
   await client.close();
   ```

   The `ClientEncryption` instance uses your KMS provider credentials, key vault namespace, and your client to manage encryption keys. Once configured, the code calls the `createDataKey()` method to generate a Data Encryption Key and writes it to a separate file.

4. Define an encryption schema.

   Add the following code to your `insertEncryptedDocument.js` file under the `// Paste JSON schema below` comment to define an encryption schema:

   ```javascript
   const dekId = fs.readFileSync(config.dekIdPath, "utf8");
   const schema = {
     bsonType: "object",
     encryptMetadata: {
       keyId: [new Binary(Buffer.from(dekId, "base64"), 4)],
     },
     properties: {
       insurance: {
         bsonType: "object",
         properties: {
           policyNumber: {
             encrypt: {
               bsonType: "int",
               algorithm: "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic",
             },
           },
         },
       },
       medicalRecords: {
         encrypt: {
           bsonType: "array",
           algorithm: "AEAD_AES_256_CBC_HMAC_SHA_512-Random",
         },
       },
       bloodType: {
         encrypt: {
           bsonType: "string",
           algorithm: "AEAD_AES_256_CBC_HMAC_SHA_512-Random",
         },
       },
       ssn: {
         encrypt: {
           bsonType: "int",
           algorithm: "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic",
         },
       },
     },
   };

   const patientSchema = { "medicalRecords.patients": schema };
   ```

   The code reads your DEK (Data Encryption Key) ID and uses it to encrypt the following fields in the `medicalRecords.patients` collection:

   - `insurance.policyNumber`: Encrypted with deterministic encryption

   - `ssn`: Encrypted with deterministic encryption

   - `bloodType`: Encrypted with random encryption

   - `medicalRecords`: Encrypted with random encryption

   Deterministic encryption allows you to perform equality queries on the encrypted fields. Random encryption provides stronger security for fields that do not require querying.

5. Create a standard and a CSFLE-enabled client.

   Paste the following code into your `insertEncryptedDocument.js` file under the `// Paste client configuration code below` comment to create two MongoDB clients:

   ```javascript
   const secureClient = new MongoClient(config.connectionString, {
     autoEncryption: {
       keyVaultNamespace: config.keyVaultNamespace,
       kmsProviders: config.getKmsProviders(),
       schemaMap: patientSchema,
       extraOptions: {
         cryptSharedLibPath: config.cryptSharedLibPath,
       },
     },
   });
   const regularClient = new MongoClient(config.connectionString);
   ```

   This code creates a `MongoClient` instance with an `autoEncryption` object that specifies your KMS provider credentials, key vault namespace, encryption schema, and the location of your Automatic Encryption Shared Library. The code also creates a standard `MongoClient` instance without automatic encryption. In a future step, you will compare the output of both clients.

   **Note: Automatic Encryption Options**

   The automatic encryption options provide configuration information to the Automatic Encryption Shared Library, which modifies the application's behavior when accessing encrypted fields.

   To learn more about the Automatic Encryption Shared Library, see the [Install and Configure a CSFLE Query Analysis Component](/docs/manual/core/csfle/reference/install-library#std-label-csfle-reference-shared-library) page.

### Perform Encrypted Operations

After configuring your application and database connection, follow the steps in this section to insert and query encrypted documents.

1. Insert a document with encrypted fields.

   Add the following code to your `insertEncryptedDocument.js` file under the `// Paste code to insert a document below` comment to insert a document into the `medicalRecords.patients` collection:

   ```javascript
   await secureClient.connect();
   const collection = secureClient
     .db("medicalRecords")
     .collection("patients");
   await collection.insertOne({
     name: "Jon Doe",
     ssn: 241014209,
     bloodType: "AB+",
     medicalRecords: [{ weight: 180, bloodPressure: "120/80" }],
     insurance: {
       policyNumber: 123142,
       provider: "MaestCare",
     },
   });
   ```

   When you insert the document, your CSFLE-enabled client automatically encrypts the specified fields. The stored document resembles the following JSON:

   ```json
   {
     "_id": { "$oid": "<_id of your document>" },
     "name": "Jon Doe",
     "ssn": {
       "$binary": "<cipher-text>",
       "$type": "6"
     },
     "bloodType": {
       "$binary": "<cipher-text>",
       "$type": "6"
     },
     "medicalRecords": {
       "$binary": "<cipher-text>",
       "$type": "6"
     },
     "insurance": {
       "provider": "MaestCare",
       "policyNumber": {
         "$binary": "<cipher-text>",
         "$type": "6"
       }
     }
   }

   ```

2. Query encrypted data.

   Add the following code to your `insertEncryptedDocument.js` file under the `// Paste code to query the document below` comment to retrieve the document with both a CSFLE-enabled client and a standard client:

   ```javascript
   await regularClient.connect();

   console.log(
     "Finding a document with the regular (non-encrypted) client:"
   );
   console.log(
     await regularClient
       .db("medicalRecords")
       .collection("patients")
       .findOne({ name: "Jon Doe" })
   );

   console.log("\nFinding a document with the encrypted client:");
   console.log(
     await secureClient
       .db("medicalRecords")
       .collection("patients")
       .findOne({ name: "Jon Doe" })
   );

   await regularClient.close();
   await secureClient.close();
   ```

   The CSFLE-enabled client automatically decrypts the encrypted fields when it retrieves the document. The standard client returns the encrypted binary values.

3. Run the application.

   To start the application, run the following command from your project directory:

   ```bash
   node main.js
   ```

   If successful, your output resembles the following example:

   ```none
   ============================================================
   Running makeDataKey.js...
   ============================================================
   DataKeyId [base64]:  ...

   ============================================================
   Running insertEncryptedDocument.js...
   ============================================================
   Finding a document with the regular (non-encrypted) client:
   {
      _id: new ObjectId('...'),
      name: 'Jon Doe',
      ssn: Binary.createFromBase64('AbOZ3SnfHUt0rXzbnMDZQUoQlAGa8Spse/0TtNt6H1HdSKmHx4Hvqa0GpadZ9r0WKueVLD7/sslIn6EgBP2NbLw6DgZy9Jeo7Ze9b4IAfmXtVA==', 6),
      bloodType: Binary.createFromBase64('ArOZ3SnfHUt0rXzbnMDZQUoCmoaHVdpLs9dZF927WGGiinrtIU2lcuM9Oh6tsqh1Cvh9s7lxEzoBjLIT2TwmQ74ZVqi2Anogj0KmEtsOrlmrYQ==', 6),
      medicalRecords: Binary.createFromBase64('ArOZ3SnfHUt0rXzbnMDZQUoEfL3BP3IahNwrClkFuN1WJG/Ldfjf+KU/vpD7I9jqjXxNl61ABctZkdJyZU1Mbi7cO+RSAvaGoYQhEeBUubRKiAe6pRyhZS7BijiF1D2BaqZmk4gDlMggdGzstpVlPeaN/W2NRWH0l0w222Pn33fsvQ==', 6),
      insurance: {
         policyNumber: Binary.createFromBase64('AbOZ3SnfHUt0rXzbnMDZQUoQr99GZNZ/FDEVkGek0B3NhQpJZNnfp8lWVkg/Vl2uMd+Lc8q7wt70+TCk6x1XxiKGGZi/EsWm1nE8FfuBASjBiA==', 6),
         provider: 'MaestCare'
      }
   }

   Finding a document with the encrypted client:
   {
      _id: new ObjectId('...'),
      name: 'Jon Doe',
      ssn: 241014209,
      bloodType: 'AB+',
      medicalRecords: [ { weight: 180, bloodPressure: '120/80' } ],
      insurance: { policyNumber: 123142, provider: 'MaestCare' }
   }
   ============================================================
   All scripts completed successfully!
   ============================================================
   ```

   The output includes your DEK (Data Encryption Key) ID, the encrypted document as stored in your database, and the decrypted document retrieved with your CSFLE-enabled client.

### Set Up Your Project

Follow the steps in this section to create your project files and assign the required configuration variables.

1. Install the dependencies.

   First, ensure that you have the following dependencies installed in your development environment:

   - [Python3 version 3.8 or later](https://www.python.org/downloads/)

   - [pip](https://pip.pypa.io/en/stable/installation/)

   Then, create a directory named `python-csfle` to store your project files. From this directory, start a [virtual environment](https://docs.python.org/3/library/venv.html) and install the PyMongo driver:

   ```bash
   python3 -m pip install pymongo
   ```

2. Create your main project file.

   Add a file named `main.py` to your `python-csfle` directory. Paste the following code into this file:

   ```python
   """
   Main script to run the CSFLE example.
   First generates a data encryption key, then inserts an encrypted document.
   """

   import subprocess
   import sys

   def run_script(script_name):
       """Run a Python script and exit if it fails."""
       print(f"\n{'='*60}")
       print(f"Running {script_name}...")
       print('='*60)
       result = subprocess.run([sys.executable, script_name])
       if result.returncode != 0:
           print(f"\nError: {script_name} failed with exit code {result.returncode}")
           sys.exit(result.returncode)

   if __name__ == "__main__":
       run_script("make_data_key.py")
       run_script("insert_encrypted_document.py")
       print("\n" + "="*60)
       print("All scripts completed successfully!")
       print("="*60)

   ```

   The `main.py` file contains your main function, which imports and runs the code from the other project files.

3. Create your data key file.

   To generate a Customer Master Key and Data Encryption Key, create a file named `make_data_key.py` in your `python-csfle` directory and paste the following code:

   ```python
   from pymongo import MongoClient, ASCENDING
   from pymongo.encryption_options import AutoEncryptionOpts
   from pymongo.encryption import ClientEncryption
   import base64
   import os
   from bson.codec_options import CodecOptions
   from bson.binary import STANDARD, UUID
   import config

   kms_providers = config.get_kms_providers()

   # Paste CMK generation code below

   # Paste index creation code below

   # Paste Client and DEK generation code below
   ```

   In future steps, you will add code to this file under each corresponding comment.

4. Create your encrypted operations file.

   Next, create a file named `insert_encrypted_document.py` in your `python-csfle` directory and paste the following code:

   ```python&#xA;
   from pymongo import MongoClient
   from pymongo.encryption_options import AutoEncryptionOpts
   from pymongo.encryption import ClientEncryption
   import base64
   import os
   from bson.codec_options import CodecOptions
   from bson.binary import STANDARD, UUID, Binary, UUID_SUBTYPE
   import pprint
   import config

   kms_providers = config.get_kms_providers()

   # Paste JSON schema below

   # Paste client configuration code below

   # Paste code to insert a document below

   # Paste code to query the document below
   ```

   In future steps, you will add code that inserts and queries encrypted documents under each corresponding comment.

5. Assign your configuration variables.

   Each of your project files imports variables from a configuration file. Create a file named `config.py` in your `python-csfle` directory and paste the following code:

   ```python
   """
   Shared configuration for CSFLE example scripts.
   """

   # MongoDB connection string
   connection_string = "<connection string>"

   # Database that contains the key vault collection
   key_vault_db = "encryption"

   # Collection that stores your data encryption keys
   key_vault_coll = "__keyVault"

   # Namespace that stores your data encryption keys
   key_vault_namespace = f"{key_vault_db}.{key_vault_coll}"

   # File path for your local Customer Master Key
   master_key_path = "master-key.txt"

   # File path for your data encryption key
   dek_id_path = "dek_id.txt"

   # Shared library path for CSFLE
   crypt_shared_lib_path = "<Automatic Encryption Shared Library path>"

   def get_kms_providers():
       """Load and return KMS providers with the local master key."""
       import os
       with open(master_key_path, "rb") as f:
           local_master_key = f.read()
       return {
           "local": {
               "key": local_master_key
           },
       }

   ```

   Then, replace the following placeholder values:

   - `<connection string>`: Your MongoDB connection string

   - `<Automatic Encryption Shared Library path>`: The full path to your Automatic Encryption Shared Library, which resembles the following paths:

     - **macOS**: `/<crypt shared directory>/lib/mongo_crypt_v1.dylib`

     - **Linux**: `/<crypt shared directory>/lib/mongo_crypt_v1.so`

     - **Windows**: `C:\<crypt shared directory>\bin\mongo_crypt_v1.dll`

   The `config.py` file instructs your application to store data encryption keys in the `encryption.__keyVault` namespace.

### Configure Encryption

After setting up your project, follow the steps in this section to create an encryption key and configure your application for CSFLE.

1. Create a Customer Master Key.

   Paste the following code into your `make_data_key.py` file under the `# Paste CMK generation code below` comment to generate a 96-byte Customer Master Key (CMK (Customer Master Key)) and save it to your filesystem:

   ```python
   file_bytes = os.urandom(96)
   with open(config.master_key_path, "wb") as f:
       f.write(file_bytes)
   ```

   **Warning: Secure your Local Key File in Production**

   We recommend storing your Customer Master Keys in a remote [Key Management System](https://en.wikipedia.org/wiki/Key_management#Key_management_system) (KMS (Key Management System)). To learn how to use a remote KMS (Key Management System) in your Queryable Encryption implementation, see the [Queryable Encryption Tutorials](/docs/manual/core/queryable-encryption/tutorials#std-label-qe-tutorial-automatic-encryption) guide.

   If you choose to use a local key provider in production, exercise great caution and do not store it on the file system. Consider injecting the key into your client application using a sidecar process, or use another approach that keeps the key secure.

2. Create a unique index on your Key Vault collection.

   Client-Side Field Level Encryption depends on server-enforced uniqueness of key alternate names, so you must create a unique index on the `keyAltNames` field in your Key Vault collection.

   Add the following code to your `make_data_key.py` file under the `# Paste index creation code below` comment to connect to MongoDB and create a partial unique index on the `keyAltNames` field:

   ```python
   key_vault_client = MongoClient(config.connection_string)
   # Drops the Key Vault collection and database if they already exist
   key_vault_client.drop_database(config.key_vault_db)
   key_vault_client["medicalRecords"].drop_collection("patients")
   key_vault_client[config.key_vault_db][config.key_vault_coll].create_index(
       [("keyAltNames", ASCENDING)],
       unique=True,
       partialFilterExpression={"keyAltNames": {"$exists": True}},
   )
   ```

3. Create a Data Encryption Key.

   Add the following code to your `make_data_key.py` file under the `# Paste Client and DEK generation code below` comment to configure a `ClientEncryption` instance and generate a Data Encryption Key:

   ```python
   client = MongoClient(config.connection_string)
   client_encryption = ClientEncryption(
       kms_providers,
       config.key_vault_namespace,
       client,
       CodecOptions(uuid_representation=STANDARD),
   )

   data_key_id = client_encryption.create_data_key("local")

   base_64_data_key_id = base64.b64encode(data_key_id)
   print("DataKeyId [base64]: ", base_64_data_key_id)

   # Writes the key ID to a file for use by other scripts
   with open(config.dek_id_path, "wb") as f:
       f.write(base_64_data_key_id)
   ```

   The `ClientEncryption` instance uses your KMS provider credentials, key vault namespace, and your client to manage encryption keys. Once configured, the code calls the the `create_data_key()` method to generate a Data Encryption Key and writes it to a separate file.

4. Define an encryption schema.

   Add the following code to your `insert_encrypted_document.py` file under the `# Paste encryption schema code below` comment to define an encryption schema:

   ```python
   with open(config.dek_id_path, "rb") as f:
       dek_id = f.read()

   json_schema = {
       "bsonType": "object",
       "encryptMetadata": {"keyId": [Binary(base64.b64decode(dek_id), UUID_SUBTYPE)]},
       "properties": {
           "insurance": {
               "bsonType": "object",
               "properties": {
                   "policyNumber": {
                       "encrypt": {
                           "bsonType": "int",
                           "algorithm": "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic",
                       }
                   }
               },
           },
           "medicalRecords": {
               "encrypt": {
                   "bsonType": "array",
                   "algorithm": "AEAD_AES_256_CBC_HMAC_SHA_512-Random",
               }
           },
           "bloodType": {
               "encrypt": {
                   "bsonType": "string",
                   "algorithm": "AEAD_AES_256_CBC_HMAC_SHA_512-Random",
               }
           },
           "ssn": {
               "encrypt": {
                   "bsonType": "int",
                   "algorithm": "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic",
               }
           },
       },
   }

   patient_schema = {"medicalRecords.patients": json_schema}
   ```

   The code reads your DEK (Data Encryption Key) ID and uses it to encrypt the following fields in the `medicalRecords.patients` collection:

   - `insurance.policyNumber`: Encrypted with deterministic encryption

   - `ssn`: Encrypted with deterministic encryption

   - `bloodType`: Encrypted with random encryption

   - `medicalRecords`: Encrypted with random encryption

   Deterministic encryption allows you to perform equality queries on the encrypted fields. Random encryption provides stronger security for fields that you don't need to query, because this algorithm does not support read operations on the encrypted fields.

5. Create standard and CSFLE-enabled clients.

   Paste the following code into your `insert_encrypted_document.py` file under the `# Paste client configuration code below` comment to create two MongoDB clients:

   ```python
   extra_options = {
       "crypt_shared_lib_path": config.crypt_shared_lib_path
   }

   fle_opts = AutoEncryptionOpts(
       kms_providers, config.key_vault_namespace, schema_map=patient_schema, **extra_options
   )
   secureClient = MongoClient(config.connection_string, auto_encryption_opts=fle_opts)
   regularClient = MongoClient(config.connection_string)
   ```

   This code creates a `MongoClient` instance with an `AutoEncryptionOpts` object that specifies your KMS provider credentials, key vault namespace, encryption schema, and the location of your Automatic Encryption Shared Library. The code also creates a standard `MongoClient` instance without automatic encryption. In a future step, you will compare the output of both clients.

   **Note: Automatic Encryption Options**

   The automatic encryption options provide configuration information to the Automatic Encryption Shared Library, which modifies the application's behavior when accessing encrypted fields.

   To learn more about the Automatic Encryption Shared Library, see the [Install and Configure a CSFLE Query Analysis Component](/docs/manual/core/csfle/reference/install-library#std-label-csfle-reference-shared-library) page.

### Perform Encrypted Operations

After configuring your application and database connection, follow the steps in this section to insert and query encrypted documents.

1. Insert a document with encrypted fields.

   Add the following code to your `insert_encrypted_document.py` file under the `# Paste document insertion code below` comment to insert a document into the `medicalRecords.patients` collection:

   ```python
   collection = secureClient.medicalRecords.patients
   collection.insert_one({
       "name": "Jon Doe",
       "ssn": 241014209,
       "bloodType": "AB+",
       "medicalRecords": [{"weight": 180, "bloodPressure": "120/80"}],
       "insurance": {"policyNumber": 123142, "provider": "MaestCare"},
   })
   ```

   When you insert the document, your CSFLE-enabled client automatically encrypts the specified fields. The stored document resembles the following code:

   ```json
   {
     "_id": { "$oid": "<_id of your document>" },
     "name": "Jon Doe",
     "ssn": {
       "$binary": "<cipher-text>",
       "$type": "6"
     },
     "bloodType": {
       "$binary": "<cipher-text>",
       "$type": "6"
     },
     "medicalRecords": {
       "$binary": "<cipher-text>",
       "$type": "6"
     },
     "insurance": {
       "provider": "MaestCare",
       "policyNumber": {
         "$binary": "<cipher-text>",
         "$type": "6"
       }
     }
   }

   ```

2. Query encrypted data.

   Add the following code to your `insert_encrypted_document.py` file under the `# Paste document query code below` comment to retrieve the document with both a CSFLE-enabled client and a standard client:

   ```python
   print("Finding a document with the regular (non-encrypted) client:")
   pprint.pprint(regularClient.medicalRecords.patients.find_one({"name": "Jon Doe"}))

   print("\nFinding a document with the encrypted client:")
   pprint.pprint(secureClient.medicalRecords.patients.find_one({"name": "Jon Doe"}))
   ```

   The CSFLE-enabled client automatically decrypts the encrypted fields when it retrieves the document. The standard client returns the encrypted binary values.

3. Run the application.

   To start the application, run the following command from your project directory:

   ```bash
   python main.py
   ```

   If successful, your output resembles the following example:

   ```none
   ============================================================
   Running make_data_key.py...
   ============================================================
   DataKeyId [base64]:  ...

   ============================================================
   Running insert_encrypted_document.py...
   ============================================================
   Finding a document with the regular (non-encrypted) client:
   {'_id': ObjectId('...'),
   'bloodType': Binary(b'\x02\x87\x83\xa9*\x8a\xa1D\x8b\xba\xe0i\x92\xb4\xa5\xe5\x80\x02\xacb\xbdI\xd5\xa7\xed\xf1\x8d\xda\x84\xd6\x1e\xf0\xa1\xa4\x142\x0b\x05\xd0\xed\x96rW\xc6+1|a"8U\xfa\xcd\xd5\x05>\xbd19\\\x8c\xba\xddUr\x87a\x9f\xb91I\xbdu\x823\x14\xbd\xa0m\xeb+\x9c', 6),
   'insurance': {'policyNumber': Binary(b'\x01\x87\x83\xa9*\x8a\xa1D\x8b\xba\xe0i\x92\xb4\xa5\xe5\x80\x104\x04\xeb\xbc7\xa7\xaf\x849\xcd\xe0\xa1}ji\x0e`\xd6\x10\x00\x19\xc0\x92\x03\xfe\x9c\x97\xbd1\xf2\xb6I\x99/\xa0\xb5\x07\xfe\xdd\x08\xf5\x11\x101\xb7q\xd0\xadK\x9bH7\x9f\xe8]=2G\x15\x1dCD\n/', 6),
              'provider': 'MaestCare'},
   'medicalRecords': Binary(b'\x02\x87\x83\xa9*\x8a\xa1D\x8b\xba\xe0i\x92\xb4\xa5\xe5\x80\x04`hP\xa3\x84\xe1\xa5\xc9\xba0\x84\xa3i\x1e\x1e;{9"\x90\xab\xc9\xdbS\xcc\x1a/\xfcgT-\x17G\xddg\x02\x8ce\xb8\xe00gX\xc7\xcc\xb9\x1b5\x0c\x00\x7f\xa3\x1d\xda}\xc2\x99\\\x1c0b\xd2\xa1\xd7\xf8%\x86\xc1\xda\xfa\xa2\x8fV\xf9\xc9\xcb\x8a.{\xecC\xc78#\xa6HX\xe9\xc44!\\S\xb9d\xe5\x9c\xf3\xe7\xb1+\xa55AC]\x9e2\xe6\xf5<\xf2', 6),
   'name': 'Jon Doe',
   'ssn': Binary(b'\x01\x87\x83\xa9*\x8a\xa1D\x8b\xba\xe0i\x92\xb4\xa5\xe5\x80\x10\xc8\xacE\xcdpT\r\x07\x11\xc3h\x0f\x93<\x92\xcc\xb4\xd3\x97q\x1a\x0eF\x8d8\x1c.\xc9\xe1\xce\x07\x1eGX\x1e\xee\x8a>\xf8\xc7\xf36\xdeF@j\xda\x8b\xde\xc6\x92$X\x8d\xbe\xce\x83\x00E\x08Lp\xbd\xe8', 6)}

   Finding a document with the encrypted client:
   {'_id': ObjectId('...'),
   'bloodType': 'AB+',
   'insurance': {'policyNumber': 123142, 'provider': 'MaestCare'},
   'medicalRecords': [{'bloodPressure': '120/80', 'weight': 180}],
   'name': 'Jon Doe',
   'ssn': 241014209}

   ============================================================
   All scripts completed successfully!
   ============================================================
   ```

   The output includes your DEK (Data Encryption Key) ID, the encrypted document as stored in your database, and the decrypted document retrieved with your CSFLE-enabled client.

### Set Up Your Project

Follow the steps in this section to create your project files and assign the required configuration variables.

1. Create your .NET console project.

   Run the following commands to create a new .NET console project in a directory named `CSharpCSFLE`:

   ```bash
   mkdir CSharpCSFLE && cd CSharpCSFLE
   dotnet new console
   ```

2. Install the dependencies.

   From your `CSharpCSFLE` directory, run the following commands to install the MongoDB .NET/C# Driver and the `MongoDB.Driver.Encryption` package:

   ```bash
   dotnet add package MongoDB.Driver
   dotnet add package MongoDB.Driver.Encryption
   ```

3. Create your main project file.

   Replace the contents of the `Program.cs` file that was generated in your `CSharpCSFLE` directory with the following code:

   ```csharp
   using System;

   namespace CsfleTutorial;

   class Program
   {
       static void Main(string[] args)
       {
           Console.WriteLine(new string('=', 60));
           Console.WriteLine("Running MakeDataKey...");
           Console.WriteLine(new string('=', 60));
           MakeDataKey.MakeKey();

           Console.WriteLine(new string('=', 60));
           Console.WriteLine("Running InsertEncryptedDocument...");
           Console.WriteLine(new string('=', 60));
           InsertEncryptedDocument.Insert();

           Console.WriteLine(new string('=', 60));
           Console.WriteLine("All scripts completed successfully!");
           Console.WriteLine(new string('=', 60));
       }
   }

   ```

   The `Program.cs` file contains your main method, which calls the code in your other project files to generate encryption keys and perform encrypted operations.

4. Create your data key file.

   To generate a Customer Master Key and Data Encryption Key, create a file named `MakeDataKey.cs` in your `CSharpCSFLE` directory and paste the following code:

   ```csharp
   using MongoDB.Driver;
   using MongoDB.Bson;
   using MongoDB.Driver.Encryption;

   namespace CsfleTutorial;

   public static class MakeDataKey
   {
       public static void MakeKey()
       {
           // Paste CMK generation code below

           // Paste index creation code below

           // Paste DEK creation code below
       }
   }
   ```

   In future steps, you will add code to this file under each corresponding comment.

5. Create your encrypted operations file.

   Next, create a file named `InsertEncryptedDocument.cs` in your `CSharpCSFLE` directory and paste the following code:

   ```csharp
   using MongoDB.Driver;
   using MongoDB.Bson;
   using MongoDB.Driver.Encryption;

   namespace CsfleTutorial;

   public static class InsertEncryptedDocument
   {
       public static void Insert()
       {
           var db = "medicalRecords";
           var coll = "patients";
           var dbNamespace = $"{db}.{coll}";

           // Paste encryption schema below

           // Paste client configuration code below

           // Paste code to insert a document below

           // Paste code to query the document below
       }
   }
   ```

   In future steps, you will add code that inserts and queries encrypted documents under each corresponding comment.

6. Assign your configuration variables.

   Each of your project files uses variables from a configuration class. Create a file named `Config.cs` in your `CSharpCSFLE` directory and paste the following code:

   ```csharp
   using System.Collections.Generic;
   using System.IO;

   namespace CsfleTutorial;

   public static class Config
   {
       public const string ConnectionString = "<connection string>";
       public const string KeyVaultDb = "encryption";
       public const string KeyVaultColl = "__keyVault";
       public const string KeyVaultNamespace = KeyVaultDb + "." + KeyVaultColl;
       public const string MasterKeyPath = "master-key.txt";
       public const string DekIdPath = "dek_id.txt";
       public const string CryptSharedLibPath =
           "<Automatic Encryption Shared Library path>";

       public static Dictionary<string, IReadOnlyDictionary<string, object>>
           GetKmsProviders()
       {
           var localMasterKeyBytes = File.ReadAllBytes(MasterKeyPath);
           var localOptions = new Dictionary<string, object>
           {
               { "key", localMasterKeyBytes }
           };
           return new Dictionary<string, IReadOnlyDictionary<string, object>>
           {
               { "local", localOptions }
           };
       }
   }

   ```

   Then, replace the following placeholder values:

   - `<connection string>`: Your MongoDB connection string

   - `<Automatic Encryption Shared Library path>`: The full path to your Automatic Encryption Shared Library, which resembles the following paths:

     - **macOS**: `/<crypt shared directory>/lib/mongo_crypt_v1.dylib`

     - **Linux**: `/<crypt shared directory>/lib/mongo_crypt_v1.so`

     - **Windows**: `C:\<crypt shared directory>\bin\mongo_crypt_v1.dll`

   The `Config.cs` file instructs your application to store data encryption keys in the `encryption.__keyVault` namespace.

### Configure Encryption

After setting up your project, follow the steps in this section to create an encryption key and configure your project for CSFLE.

1. Create a Customer Master Key.

   Paste the following code into your `MakeDataKey.cs` file inside the `MakeKey()` method, below the `// Paste CMK generation code below` comment, to generate a 96-byte Customer Master Key (CMK (Customer Master Key)) and save it to your filesystem:

   ```csharp
   using (var rng =
       System.Security.Cryptography.RandomNumberGenerator.Create())
   {
       var bytes = new byte[96];
       rng.GetBytes(bytes);
       File.WriteAllBytes(Config.MasterKeyPath, bytes);
   }
   ```

   **Warning: Secure your Local Key File in Production**

   We recommend storing your Customer Master Keys in a remote [Key Management System](https://en.wikipedia.org/wiki/Key_management#Key_management_system) (KMS (Key Management System)). To learn how to use a remote KMS (Key Management System) in your Queryable Encryption implementation, see the [Queryable Encryption Tutorials](/docs/manual/core/queryable-encryption/tutorials#std-label-qe-tutorial-automatic-encryption) guide.

   If you choose to use a local key provider in production, exercise great caution and do not store it on the file system. Consider injecting the key into your client application using a sidecar process, or use another approach that keeps the key secure.

2. Create a unique index on your Key Vault collection.

   Client-Side Field Level Encryption depends on server-enforced uniqueness of key alternate names, so you must create a unique index on the `keyAltNames` field in your Key Vault collection.

   Add the following code to your `MakeDataKey.cs` file below the `// Paste index creation code below` comment to connect to MongoDB and create a partial unique index on the `keyAltNames` field:

   ```csharp
   var keyVaultNamespace =
       CollectionNamespace.FromFullName(Config.KeyVaultNamespace);
   var keyVaultClient = new MongoClient(Config.ConnectionString);
   var keyVaultDatabase = keyVaultClient
       .GetDatabase(keyVaultNamespace.DatabaseNamespace.ToString());
   keyVaultDatabase.DropCollection(keyVaultNamespace.CollectionName);
   // Drop the patients collection to make the tutorial re-runnable.
   keyVaultClient.GetDatabase("medicalRecords").DropCollection("patients");
   var keyVaultCollection = keyVaultDatabase
       .GetCollection<BsonDocument>(keyVaultNamespace.CollectionName);
   var indexOptions = new CreateIndexOptions<BsonDocument>
   {
       Unique = true,
       PartialFilterExpression = new BsonDocument
       {
           {
               "keyAltNames",
               new BsonDocument { { "$exists", new BsonBoolean(true) } }
           }
       }
   };
   var indexKeysDocument =
       Builders<BsonDocument>.IndexKeys.Ascending("keyAltNames");
   var indexModel =
       new CreateIndexModel<BsonDocument>(indexKeysDocument, indexOptions);
   keyVaultCollection.Indexes.CreateOne(indexModel);
   ```

3. Create a Data Encryption Key.

   Add the following code to your `MakeDataKey.cs` file below the `// Paste DEK creation code below` comment to configure a `ClientEncryption` instance and generate a Data Encryption Key:

   ```csharp
   var kmsProviders = Config.GetKmsProviders();
   var clientEncryptionOptions = new ClientEncryptionOptions(
       keyVaultClient: keyVaultClient,
       keyVaultNamespace: keyVaultNamespace,
       kmsProviders: kmsProviders);
   var clientEncryption = new ClientEncryption(clientEncryptionOptions);
   var dataKeyOptions = new DataKeyOptions();
   var dataKeyId = clientEncryption.CreateDataKey(
       "local", dataKeyOptions, CancellationToken.None);
   var base64DekId = Convert.ToBase64String(
       GuidConverter.ToBytes(dataKeyId, GuidRepresentation.Standard));
   Console.WriteLine($"DataKeyId [base64]: {base64DekId}");
   File.WriteAllText(Config.DekIdPath, base64DekId);
   ```

   The `ClientEncryption` instance uses your KMS provider settings, key vault namespace, and client to manage encryption keys. Once configured, the code calls the `CreateDataKey()` method to generate a Data Encryption Key and writes it to a separate file.

4. Define an encryption schema.

   Add the following code to your `InsertEncryptedDocument.cs` file below the `// Paste encryption schema below` comment to define an encryption schema:

   ```csharp
   var dekId = File.ReadAllText(Config.DekIdPath);
   var schema = new BsonDocument
   {
       { "bsonType", "object" },
       {
           "encryptMetadata",
           new BsonDocument("keyId", new BsonArray(new[]
           {
               new BsonBinaryData(
                   Convert.FromBase64String(dekId),
                   BsonBinarySubType.UuidStandard)
           }))
       },
       {
           "properties", new BsonDocument
           {
               {
                   "ssn", new BsonDocument
                   {
                       {
                           "encrypt", new BsonDocument
                           {
                               { "bsonType", "int" },
                               {
                                   "algorithm",
                                   "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic"
                               }
                           }
                       }
                   }
               },
               {
                   "bloodType", new BsonDocument
                   {
                       {
                           "encrypt", new BsonDocument
                           {
                               { "bsonType", "string" },
                               {
                                   "algorithm",
                                   "AEAD_AES_256_CBC_HMAC_SHA_512-Random"
                               }
                           }
                       }
                   }
               },
               {
                   "medicalRecords", new BsonDocument
                   {
                       {
                           "encrypt", new BsonDocument
                           {
                               { "bsonType", "array" },
                               {
                                   "algorithm",
                                   "AEAD_AES_256_CBC_HMAC_SHA_512-Random"
                               }
                           }
                       }
                   }
               },
               {
                   "insurance", new BsonDocument
                   {
                       { "bsonType", "object" },
                       {
                           "properties", new BsonDocument
                           {
                               {
                                   "policyNumber", new BsonDocument
                                   {
                                       {
                                           "encrypt", new BsonDocument
                                           {
                                               { "bsonType", "int" },
                                               {
                                                   "algorithm",
                                                   "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic"
                                               }
                                           }
                                       }
                                   }
                               }
                           }
                       }
                   }
               }
           }
       }
   };
   var schemaMap = new Dictionary<string, BsonDocument>
   {
       { dbNamespace, schema }
   };
   ```

   The code reads your DEK (Data Encryption Key) ID and uses it to encrypt the following fields in the `medicalRecords.patients` collection:

   - `insurance.policyNumber`: Encrypted with deterministic encryption

   - `ssn`: Encrypted with deterministic encryption

   - `bloodType`: Encrypted with random encryption

   - `medicalRecords`: Encrypted with random encryption

   Deterministic encryption allows you to perform equality queries on encrypted fields. Random encryption provides stronger security but does not support read operations on the encrypted fields.

5. Create standard and CSFLE-enabled clients.

   Paste the following code into your `InsertEncryptedDocument.cs` file below the `// Paste client configuration code below` comment to create two MongoDB clients:

   ```csharp
   var keyVaultNamespace =
       CollectionNamespace.FromFullName(Config.KeyVaultNamespace);
   var kmsProviders = Config.GetKmsProviders();
   var extraOptions = new Dictionary<string, object>
   {
       { "cryptSharedLibPath", Config.CryptSharedLibPath }
   };
   MongoClientSettings.Extensions.AddAutoEncryption();
   var clientSettings =
       MongoClientSettings.FromConnectionString(Config.ConnectionString);
   var autoEncryptionOptions = new AutoEncryptionOptions(
       keyVaultNamespace: keyVaultNamespace,
       kmsProviders: kmsProviders,
       schemaMap: schemaMap,
       extraOptions: extraOptions);
   clientSettings.AutoEncryptionOptions = autoEncryptionOptions;
   var secureClient = new MongoClient(clientSettings);
   var regularClient = new MongoClient(Config.ConnectionString);
   ```

   This code creates a `MongoClient` instance with an `AutoEncryptionOptions` object that specifies your KMS provider settings, key vault namespace, encryption schema, and the location of your Automatic Encryption Shared Library. The code also creates a standard `MongoClient` instance without automatic encryption. In a future step, you will compare the output of both clients.

   **Note: Automatic Encryption Options**

   The automatic encryption options provide configuration information to the Automatic Encryption Shared Library, which modifies the application's behavior when accessing encrypted fields.

   To learn more about the Automatic Encryption Shared Library, see the [Install and Configure a CSFLE Query Analysis Component](/docs/manual/core/csfle/reference/install-library#std-label-csfle-reference-shared-library) page.

### Perform Encrypted Operations

After configuring your project and database connection, follow the steps in this section to insert and query encrypted documents.

1. Insert a document with encrypted fields.

   Add the following code to your `InsertEncryptedDocument.cs` file below the `// Paste code to insert a document below` comment to insert a document into the `medicalRecords.patients` collection:

   ```csharp
   var secureCollection = secureClient
       .GetDatabase(db).GetCollection<BsonDocument>(coll);
   var sampleDoc = new BsonDocument
   {
       { "name", "Jon Doe" },
       { "ssn", 241014209 },
       { "bloodType", "AB+" },
       {
           "medicalRecords", new BsonArray
           {
               new BsonDocument
               {
                   { "weight", 180 },
                   { "bloodPressure", "120/80" }
               }
           }
       },
       {
           "insurance", new BsonDocument
           {
               { "policyNumber", 123142 },
               { "provider", "MaestCare" }
           }
       }
   };
   secureCollection.InsertOne(sampleDoc);
   ```

   When you insert the document, your CSFLE-enabled client automatically encrypts the specified fields. The stored document resembles the following code:

   ```json
   {
     "_id": { "$oid": "<_id of your document>" },
     "name": "Jon Doe",
     "ssn": {
       "$binary": "<cipher-text>",
       "$type": "6"
     },
     "bloodType": {
       "$binary": "<cipher-text>",
       "$type": "6"
     },
     "medicalRecords": {
       "$binary": "<cipher-text>",
       "$type": "6"
     },
     "insurance": {
       "provider": "MaestCare",
       "policyNumber": {
         "$binary": "<cipher-text>",
         "$type": "6"
       }
     }
   }

   ```

2. Query encrypted data.

   Add the following code to your `InsertEncryptedDocument.cs` file below the `// Paste code to query the document below` comment to retrieve the document with both a CSFLE-enabled client and a standard client:

   ```csharp
   var regularCollection = regularClient
       .GetDatabase(db).GetCollection<BsonDocument>(coll);

   Console.WriteLine(
       "Finding a document with the regular (non-encrypted) client:");
   var filter = Builders<BsonDocument>.Filter.Eq("name", "Jon Doe");
   var regularResult = regularCollection.Find(filter).First();
   Console.WriteLine($"\n{regularResult}\n");

   Console.WriteLine("Finding a document with the encrypted client:");
   var secureResult = secureCollection.Find(filter).First();
   Console.WriteLine($"\n{secureResult}\n");
   ```

   The CSFLE-enabled client automatically decrypts the encrypted fields when it retrieves the document. The standard client returns the encrypted binary values.

3. Run the application.

   To start the application, run the following command from your project directory:

   ```bash
   dotnet run
   ```

   If successful, your output resembles the following example:

   ```none
   ============================================================
   Running MakeDataKey...
   ============================================================
   DataKeyId [base64]: ...

   ============================================================
   Running InsertEncryptedDocument...
   ============================================================
   Finding a document with the regular (non-encrypted) client:

   { "_id" : { "$oid" : "..." }, "name" : "Jon Doe",
   "ssn" : { "$binary" : { "base64" : "...", "subType" : "06" } },
   "bloodType" : { "$binary" : { "base64" : "...", "subType" : "06" } },
   "medicalRecords" : { "$binary" : { "base64" : "...", "subType" : "06" } },
   "insurance" : { "policyNumber" : { "$binary" : { "base64" : "...",
   "subType" : "06" } }, "provider" : "MaestCare" } }

   Finding a document with the encrypted client:

   { "_id" : { "$oid" : "..." }, "name" : "Jon Doe", "ssn" : 241014209,
   "bloodType" : "AB+", "medicalRecords" :
   [{ "weight" : 180, "bloodPressure" : "120/80" }],
   "insurance" : { "policyNumber" : 123142,
   "provider" : "MaestCare" } }

   ============================================================
   All scripts completed successfully!
   ============================================================
   ```

   The output includes your DEK (Data Encryption Key) ID, the encrypted document as stored in your database, and the decrypted document retrieved with your CSFLE-enabled client.

### Set Up Your Project

Follow the steps in this section to create your project files and assign the required configuration variables.

1. Install the dependencies.

   Create and navigate to a directory named `go-csfle`, and then initialize a Go module:

   ```bash
   mkdir go-csfle && cd go-csfle
   go mod init go-csfle
   ```

   Then, add the MongoDB Go Driver to your project by running the following command:

   ```bash
   go get go.mongodb.org/mongo-driver/v2/mongo
   ```

2. Create your main project file.

   Add a file named `main.go` to your `go-csfle` directory and paste the following code:

   ```go
   package main

   import (
   	"fmt"
   	"log"
   	"strings"
   )

   func main() {
   	separator := strings.Repeat("=", 60)
   	fmt.Println(separator)
   	fmt.Println("Running make_data_key...")
   	fmt.Println(separator)
   	if err := MakeKey(); err != nil {
   		log.Fatalf("MakeKey failed: %v", err)
   	}
   	fmt.Println(separator)
   	fmt.Println("Running insert_encrypted_document...")
   	fmt.Println(separator)
   	if err := Insert(); err != nil {
   		log.Fatalf("Insert failed: %v", err)
   	}
   	fmt.Println(separator)
   	fmt.Println("All scripts completed successfully!")
   	fmt.Println(separator)
   }

   ```

   The `main.go` file contains your main function, which calls the functions from your other project files in sequence.

3. Create your data key file.

   To generate a Customer Master Key and Data Encryption Key, create a file named `make_data_key.go` in your `go-csfle` directory and paste the following code:

   ```go
   package main

   import (
      "context"
      "crypto/rand"
      "encoding/base64"
      "fmt"
      "os"

      "go.mongodb.org/mongo-driver/v2/bson"
      "go.mongodb.org/mongo-driver/v2/mongo"
      "go.mongodb.org/mongo-driver/v2/mongo/options"
   )

   func MakeKey() error {
      // Paste CMK generation code below

      // Paste index creation code below

      // Paste DEK creation code below

      return nil
   }
   ```

   In future steps, you will add code to this file under each corresponding comment.

4. Create your encrypted operations file.

   Next, create a file named `insert_encrypted_document.go` in your `go-csfle` directory and paste the following code:

   ```go
   package main

   import (
      "context"
      "fmt"
      "os"
      "strings"

      "go.mongodb.org/mongo-driver/v2/bson"
      "go.mongodb.org/mongo-driver/v2/mongo"
      "go.mongodb.org/mongo-driver/v2/mongo/options"
   )

   func Insert() error {
      // Paste JSON schema below

      // Paste client configuration code below

      // Paste code to insert a document below

      // Paste code to query the document below

      return nil
   }
   ```

   In future steps, you will add code that inserts and queries encrypted documents under each corresponding comment.

5. Assign your configuration variables.

   Each of your project files uses variables from a configuration file. Create a file named `config.go` in your `go-csfle` directory and paste the following code:

   ```go
   // Shared configuration for CSFLE example files.
   package main

   import (
   	"fmt"
   	"os"
   )

   // MongoDB connection string
   const connectionString = "<connection string>"

   // Database that contains the key vault collection
   const keyVaultDb = "encryption"

   // Collection that stores your data encryption keys
   const keyVaultColl = "__keyVault"

   // Namespace that stores your data encryption keys
   const keyVaultNamespace = keyVaultDb + "." + keyVaultColl

   // File path for your local Customer Master Key
   const masterKeyPath = "master-key.txt"

   // File path for your data encryption key
   const dekIdPath = "dek_id.txt"

   // Shared library path for CSFLE
   const cryptSharedLibPath = "<Automatic Encryption Shared Library path>"

   // getKmsProviders loads and returns KMS providers with the local master key.
   func getKmsProviders() (map[string]map[string]any, error) {
   	key, err := os.ReadFile(masterKeyPath)
   	if err != nil {
   		return nil, fmt.Errorf("could not read master key: %v", err)
   	}
   	return map[string]map[string]any{"local": {"key": key}}, nil
   }

   ```

   Then, replace the following placeholder values:

   - `<connection string>`: Your MongoDB connection string

   - `<Automatic Encryption Shared Library path>`: The full path to your Automatic Encryption Shared Library, which resembles the following paths:

     - **macOS**: `/<crypt shared directory>/lib/mongo_crypt_v1.dylib`

     - **Linux**: `/<crypt shared directory>/lib/mongo_crypt_v1.so`

     - **Windows**: `C:\<crypt shared directory>\bin\mongo_crypt_v1.dll`

   The `config.go` file instructs your application to store data encryption keys in the `encryption.__keyVault` namespace.

### Configure Encryption

After setting up your project, follow the steps in this section to create an encryption key and configure your app for CSFLE.

1. Create a Customer Master Key.

   Paste the following code into your `make_data_key.go` file under the `// Paste CMK generation code below` comment to generate a 96-byte Customer Master Key (CMK (Customer Master Key)) and save it to your filesystem:

   ```go
   key := make([]byte, 96)
   if _, err := rand.Read(key); err != nil {
   	return fmt.Errorf("could not generate random key: %v", err)
   }
   if err := os.WriteFile(masterKeyPath, key, 0644); err != nil {
   	return fmt.Errorf("could not write master key to file: %v", err)
   }
   ```

   **Warning: Secure your Local Key File in Production**

   We recommend storing your Customer Master Keys in a remote [Key Management System](https://en.wikipedia.org/wiki/Key_management#Key_management_system) (KMS (Key Management System)). To learn how to use a remote KMS (Key Management System) in your Queryable Encryption implementation, see the [Queryable Encryption Tutorials](/docs/manual/core/queryable-encryption/tutorials#std-label-qe-tutorial-automatic-encryption) guide.

   If you choose to use a local key provider in production, exercise great caution and do not store it on the file system. Consider injecting the key into your client application using a sidecar process, or use another approach that keeps the key secure.

2. Create a unique index on your Key Vault collection.

   Client-Side Field Level Encryption depends on server-enforced uniqueness of key alternate names, so you must create a unique index on the `keyAltNames` field in your Key Vault collection.

   Add the following code to your `make_data_key.go` file under the `// Paste index creation code below` comment to connect to MongoDB and create a partial unique index on the `keyAltNames` field:

   ```go
   keyVaultClient, err := mongo.Connect(options.Client().ApplyURI(connectionString))
   if err != nil {
   	return fmt.Errorf("connect error for key vault client: %v", err)
   }
   defer func() {
   	_ = keyVaultClient.Disconnect(context.TODO())
   }()

   // Drops the key vault collection and database if they already exist
   if err = keyVaultClient.Database(keyVaultDb).Collection(keyVaultColl).Drop(context.TODO()); err != nil {
   	return fmt.Errorf("collection drop error: %v", err)
   }
   if err = keyVaultClient.Database("medicalRecords").Collection("patients").Drop(context.TODO()); err != nil {
   	return fmt.Errorf("collection drop error: %v", err)
   }
   keyVaultIndex := mongo.IndexModel{
   	Keys: bson.D{{Key: "keyAltNames", Value: 1}},
   	Options: options.Index().
   		SetUnique(true).
   		SetPartialFilterExpression(bson.D{
   			{Key: "keyAltNames", Value: bson.D{
   				{Key: "$exists", Value: true},
   			}},
   		}),
   }
   _, err = keyVaultClient.Database(keyVaultDb).Collection(keyVaultColl).Indexes().CreateOne(context.TODO(), keyVaultIndex)
   if err != nil {
   	return fmt.Errorf("index create error: %v", err)
   }
   ```

3. Create a Data Encryption Key.

   Add the following code to your `make_data_key.go` file under the `// Paste DEK creation code below` comment to configure a `ClientEncryption` instance and generate a Data Encryption Key:

   ```go
   kmsProviders, err := getKmsProviders()
   if err != nil {
   	return err
   }
   clientEncryptionOpts := options.ClientEncryption().
   	SetKeyVaultNamespace(keyVaultNamespace).
   	SetKmsProviders(kmsProviders)
   clientEnc, err := mongo.NewClientEncryption(keyVaultClient, clientEncryptionOpts)
   if err != nil {
   	return fmt.Errorf("NewClientEncryption error: %v", err)
   }
   defer func() {
   	_ = clientEnc.Close(context.TODO())
   }()

   dataKeyID, err := clientEnc.CreateDataKey(context.TODO(), "local", options.DataKey())
   if err != nil {
   	return fmt.Errorf("create data key error: %v", err)
   }

   base64DekId := base64.StdEncoding.EncodeToString(dataKeyID.Data)
   fmt.Printf("DataKeyId [base64]: %s\n", base64DekId)
   // Writes the key ID to a file for use by other files
   if err := os.WriteFile(dekIdPath, []byte(base64DekId), 0644); err != nil {
   	return fmt.Errorf("write dek_id.txt error: %v", err)
   }
   ```

   The `ClientEncryption` instance uses your KMS provider credentials, key vault namespace, and client to manage encryption keys. Once configured, the code calls `CreateDataKey` to generate a Data Encryption Key and writes it to a separate file.

4. Define an encryption schema.

   Add the following code to your `insert_encrypted_document.go` file under the `// Paste JSON schema below` comment to define an encryption schema:

   ```go
   dekIdBytes, err := os.ReadFile(dekIdPath)
   if err != nil {
   	return fmt.Errorf("read dek_id.txt error: %v", err)
   }
   dekId := strings.TrimSpace(string(dekIdBytes))
   schemaTemplate := `{
   	"bsonType": "object",
   	"encryptMetadata": {
   		"keyId": [
   			{
   				"$binary": {
   					"base64": "%s",
   					"subType": "04"
   				}
   			}
   		]
   	},
   	"properties": {
   		"insurance": {
   			"bsonType": "object",
   			"properties": {
   				"policyNumber": {
   					"encrypt": {
   						"bsonType": "int",
   						"algorithm": "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic"
   					}
   				}
   			}
   		},
   		"medicalRecords": {
   			"encrypt": {
   				"bsonType": "array",
   				"algorithm": "AEAD_AES_256_CBC_HMAC_SHA_512-Random"
   			}
   		},
   		"bloodType": {
   			"encrypt": {
   				"bsonType": "string",
   				"algorithm": "AEAD_AES_256_CBC_HMAC_SHA_512-Random"
   			}
   		},
   		"ssn": {
   			"encrypt": {
   				"bsonType": "int",
   				"algorithm": "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic"
   			}
   		}
   	}
   }`
   schema := fmt.Sprintf(schemaTemplate, dekId)
   var schemaDoc bson.Raw
   if err := bson.UnmarshalExtJSON([]byte(schema), true, &schemaDoc); err != nil {
   	return fmt.Errorf("UnmarshalExtJSON error: %v", err)
   }
   schemaMap := map[string]any{
   	"medicalRecords.patients": schemaDoc,
   }
   ```

   The code reads your DEK (Data Encryption Key) ID and uses it to encrypt the following fields in the `medicalRecords.patients` collection:

   - `insurance.policyNumber`: Deterministically encrypted

   - `ssn`: Deterministically encrypted

   - `bloodType`: Randomly encrypted

   - `medicalRecords`: Randomly encrypted

   Deterministic encryption allows you to perform equality queries on the encrypted fields. Random encryption provides stronger security for fields that you don't need to query, because this algorithm does not support read operations on the encrypted fields.

5. Create a CSFLE-enabled client.

   Paste the following code into your `insert_encrypted_document.go` file under the `// Paste client configuration code below` comment to create two MongoDB clients:

   ```go
   kmsProviders, err := getKmsProviders()
   if err != nil {
   	return err
   }
   extraOptions := map[string]any{
   	"cryptSharedLibPath": cryptSharedLibPath,
   }
   autoEncryptionOpts := options.AutoEncryption().
   	SetKmsProviders(kmsProviders).
   	SetKeyVaultNamespace(keyVaultNamespace).
   	SetSchemaMap(schemaMap).
   	SetExtraOptions(extraOptions)
   secureClient, err := mongo.Connect(
   	options.Client().ApplyURI(connectionString).SetAutoEncryptionOptions(autoEncryptionOpts),
   )
   if err != nil {
   	return fmt.Errorf("connect error for encrypted client: %v", err)
   }
   defer func() {
   	_ = secureClient.Disconnect(context.TODO())
   }()
   regularClient, err := mongo.Connect(options.Client().ApplyURI(connectionString))
   if err != nil {
   	return fmt.Errorf("connect error for regular client: %v", err)
   }
   defer func() {
   	_ = regularClient.Disconnect(context.TODO())
   }()
   ```

   This code creates a `MongoClient` instance that uses `AutoEncryptionOptions`. The options specify your KMS provider credentials, key vault namespace, encryption schema, and the location of your Automatic Encryption Shared Library. The code also creates a standard `MongoClient` instance without automatic encryption. In a future step, you will compare the output of both clients.

   **Note: Automatic Encryption Options**

   The automatic encryption options provide configuration information to the Automatic Encryption Shared Library, which modifies the application's behavior when accessing encrypted fields.

   To learn more about the Automatic Encryption Shared Library, see the [Install and Configure a CSFLE Query Analysis Component](/docs/manual/core/csfle/reference/install-library#std-label-csfle-reference-shared-library) page.

### Perform Encrypted Operations

After configuring your app and database connection, follow the steps in this section to insert and query encrypted documents.

1. Insert a document with encrypted fields.

   Add the following code to your `insert_encrypted_document.go` file under the `// Paste code to insert a document below` comment to insert a document into the `medicalRecords.patients` collection:

   ```go
   secureCollection := secureClient.Database("medicalRecords").Collection("patients")
   if _, err := secureCollection.InsertOne(context.TODO(), map[string]any{
   	"name":      "Jon Doe",
   	"ssn":       241014209,
   	"bloodType": "AB+",
   	"medicalRecords": []map[string]any{{
   		"weight":        180,
   		"bloodPressure": "120/80",
   	}},
   	"insurance": map[string]any{
   		"provider":     "MaestCare",
   		"policyNumber": 123142,
   	},
   }); err != nil {
   	return fmt.Errorf("InsertOne error: %v", err)
   }
   ```

   When you insert the document, your CSFLE-enabled client automatically encrypts the specified fields. The stored document resembles the following:

   ```json
   {
     "_id": { "$oid": "<_id of your document>" },
     "name": "Jon Doe",
     "ssn": {
       "$binary": "<cipher-text>",
       "$type": "6"
     },
     "bloodType": {
       "$binary": "<cipher-text>",
       "$type": "6"
     },
     "medicalRecords": {
       "$binary": "<cipher-text>",
       "$type": "6"
     },
     "insurance": {
       "provider": "MaestCare",
       "policyNumber": {
         "$binary": "<cipher-text>",
         "$type": "6"
       }
     }
   }

   ```

2. Query encrypted data.

   Add the following code to your `insert_encrypted_document.go` file under the `// Paste code to query the document below` comment to retrieve the document with both a CSFLE-enabled client and a standard client:

   ```go
   fmt.Println("Finding a document with the regular (non-encrypted) client:")
   var resultRegular bson.M
   regularCollection := regularClient.Database("medicalRecords").Collection("patients")
   err = regularCollection.FindOne(context.TODO(), bson.D{{Key: "name", Value: "Jon Doe"}}).Decode(&resultRegular)
   if err != nil {
   	return fmt.Errorf("FindOne error (regular client): %v", err)
   }
   outputRegular, err := bson.MarshalExtJSONIndent(resultRegular, false, false, "", "    ")
   if err != nil {
   	return fmt.Errorf("MarshalExtJSONIndent error: %v", err)
   }
   fmt.Printf("%s\n", outputRegular)

   fmt.Println("Finding a document with the encrypted client:")
   var resultSecure bson.M
   err = secureCollection.FindOne(context.TODO(), bson.D{{Key: "name", Value: "Jon Doe"}}).Decode(&resultSecure)
   if err != nil {
   	return fmt.Errorf("FindOne error (encrypted client): %v", err)
   }
   outputSecure, err := bson.MarshalExtJSONIndent(resultSecure, false, false, "", "    ")
   if err != nil {
   	return fmt.Errorf("MarshalExtJSONIndent error: %v", err)
   }
   fmt.Printf("%s\n", outputSecure)
   ```

   The CSFLE-enabled client automatically decrypts the encrypted fields when it retrieves the document. The standard client returns the encrypted binary values.

3. Run the application.

   To install required dependencies, run the following command from your project directory:

   ```bash
   go mod tidy
   ```

   Then start the application:

   ```bash
   go run -tags cse .
   ```

   **Note:**

   Go CSFLE applications require the `-tags cse` build flag to run.

   If successful, your output resembles the following example:

   ```none
   ============================================================
   Running make_data_key...
   ============================================================
   DataKeyId [base64]: <dataKeyId>

   ============================================================
   Running insert_encrypted_document...
   ============================================================
   Finding a document with the regular (non-encrypted) client:
   {
       "_id": {
           "$oid": "..."
       },
       "name": "Jon Doe",
       "ssn": {
           "$binary": {
               "base64": "...",
               "subType": "06"
           }
       },
       "bloodType": {
           "$binary": {
               "base64": "...",
               "subType": "06"
           }
       },
       "medicalRecords": {
           "$binary": {
               "base64": "...",
               "subType": "06"
           }
       },
       "insurance": {
           "provider": "MaestCare",
           "policyNumber": {
               "$binary": {
                   "base64": "...",
                   "subType": "06"
               }
           }
       }
   }

   Finding a document with the encrypted client:
   {
       "_id": {
           "$oid": "..."
       },
       "name": "Jon Doe",
       "ssn": 241014209,
       "bloodType": "AB+",
       "medicalRecords": [
           {
               "bloodPressure": "120/80",
               "weight": 180
           }
       ],
       "insurance": {
           "provider": "MaestCare",
           "policyNumber": 123142
       }
   }

   ============================================================
   All scripts completed successfully!
   ============================================================
   ```

   The output includes your DEK (Data Encryption Key) ID, the encrypted document as stored in your database, and the decrypted document retrieved with your CSFLE-enabled client.

### Set Up Your Project

Follow the steps in this section to create your project files and assign the required configuration variables.

1. Create your main project file.

   Create a directory named `ruby-csfle` to store your project files, and then add a file named `main.rb` to this directory. Paste the following code into this file:

   ```ruby
   require_relative 'make_data_key'
   require_relative 'insert_encrypted_document'

   SEPARATOR = '=' * 60

   puts SEPARATOR
   puts 'Running make_data_key.rb...'
   puts SEPARATOR
   make_key

   puts SEPARATOR
   puts 'Running insert_encrypted_document.rb...'
   puts SEPARATOR
   insert

   puts SEPARATOR
   puts 'All scripts completed successfully!'
   puts SEPARATOR

   ```

   The `main.rb` file contains your main script, which imports and runs the code from the other project files.

2. Create your data key file.

   To generate a Customer Master Key and Data Encryption Key, create a file named `make_data_key.rb` in your `ruby-csfle` directory and paste the following code:

   ```ruby
   require 'mongo'
   require 'base64'
   require 'securerandom'
   require_relative 'config'

   # Paste CMK generation code below

   def make_key
     # Paste index creation code below

     # Paste DEK creation code below
   end
   ```

   In future steps, you will add code to this file following each corresponding comment.

3. Create your encrypted operations file.

   Next, create a file named `insert_encrypted_document.rb` in your `ruby-csfle` directory and paste the following code:

   ```ruby
   require 'mongo'
   require 'base64'
   require_relative 'config'

   def insert
     # Paste JSON schema below

     # Paste client configuration code below

     # Paste code to insert a document below

     # Paste code to query the document below
   end
   ```

   In future steps, you will add code that inserts and queries encrypted documents under each corresponding comment.

4. Assign your configuration variables.

   Each of your project files imports variables from a configuration file. Create a file named `config.rb` in your `ruby-csfle` directory and paste the following code:

   ```ruby
   require 'mongo'
   require 'base64'

   CONNECTION_STRING = '<connection string>'
   KEY_VAULT_DB = 'encryption'
   KEY_VAULT_COLL = '__keyVault'
   KEY_VAULT_NAMESPACE = "#{KEY_VAULT_DB}.#{KEY_VAULT_COLL}"
   MASTER_KEY_PATH = 'master-key.txt'
   DEK_ID_PATH = 'dek_id.txt'
   CRYPT_SHARED_LIB_PATH = '<Automatic Encryption Shared Library path>'

   def get_kms_providers
     local_master_key = File.binread(MASTER_KEY_PATH)
     { local: { key: local_master_key } }
   end

   ```

   Then, replace the following placeholder values:

   - `<connection string>`: Your MongoDB connection string

   - `<Automatic Encryption Shared Library path>`: The full path to your Automatic Encryption Shared Library, which resembles `/<crypt shared directory>/lib/mongo_crypt_v1.dylib` on macOS and `/<crypt shared directory>/lib/mongo_crypt_v1.so` on Linux

   The `config.rb` file instructs your application to store data encryption keys in the `encryption.__keyVault` namespace.

### Configure Encryption

After setting up your project, follow the steps in this section to create an encryption key and configure your application for CSFLE.

1. Create a Customer Master Key.

   Paste the following code into your `make_data_key.rb` file under the `# Paste CMK generation code below` comment to generate a 96-byte Customer Master Key (CMK (Customer Master Key)) and save it to your filesystem when you run the application:

   ```ruby
   File.binwrite(MASTER_KEY_PATH, SecureRandom.random_bytes(96))
   ```

   **Warning: Secure your Local Key File in Production**

   We recommend storing your Customer Master Keys in a remote [Key Management System](https://en.wikipedia.org/wiki/Key_management#Key_management_system) (KMS (Key Management System)). To learn how to use a remote KMS (Key Management System) in your Queryable Encryption implementation, see the [Queryable Encryption Tutorials](/docs/manual/core/queryable-encryption/tutorials#std-label-qe-tutorial-automatic-encryption) guide.

   If you choose to use a local key provider in production, exercise great caution and do not store it on the file system. Consider injecting the key into your client application using a sidecar process, or use another approach that keeps the key secure.

2. Create a unique index on your Key Vault collection.

   Client-Side Field Level Encryption depends on server-enforced uniqueness of key alternate names, so you must create a unique index on the `keyAltNames` field in your Key Vault collection.

   Add the following code to your `make_data_key.rb` file under the `# Paste index creation code below` comment to connect to MongoDB and create a partial unique index on the `keyAltNames` field:

   ```ruby
   key_vault_client = Mongo::Client.new(CONNECTION_STRING)
   key_vault_client.use(KEY_VAULT_DB).database.drop
   key_vault_client.use('medicalRecords').database.drop
   key_vault_client.use(KEY_VAULT_DB)[KEY_VAULT_COLL].indexes.create_one(
     { 'keyAltNames' => 1 },
     unique: true,
     partial_filter_expression: { 'keyAltNames' => { '$exists' => true } }
   )
   key_vault_client.close
   ```

3. Create a Data Encryption Key.

   Add the following code to your `make_data_key.rb` file under the `# Paste DEK creation code below` comment to configure a `Mongo::ClientEncryption` instance and generate a Data Encryption Key:

   ```ruby
   client = Mongo::Client.new(CONNECTION_STRING)
   client_encryption = Mongo::ClientEncryption.new(
     client,
     key_vault_namespace: KEY_VAULT_NAMESPACE,
     kms_providers: get_kms_providers
   )
   dek_id = client_encryption.create_data_key('local')
   base64_dek_id = Base64.strict_encode64(dek_id.data)
   puts "DataKeyId [base64]: #{base64_dek_id}"
   File.write(DEK_ID_PATH, base64_dek_id)
   client.close
   ```

   The `Mongo::ClientEncryption` instance uses your KMS provider credentials, key vault namespace, and your client to manage encryption keys. Once configured, the code calls the `create_data_key` method to generate a Data Encryption Key and writes it to a separate file.

4. Define an encryption schema.

   Add the following code to your `insert_encrypted_document.rb` file under the `# Paste JSON schema below` comment to define an encryption schema:

   ```ruby
   dek_id = BSON::Binary.new(
     Base64.strict_decode64(File.read(DEK_ID_PATH)),
     :uuid
   )
   patient_schema = {
     'medicalRecords.patients' => {
       bsonType: 'object',
       encryptMetadata: {
         keyId: [dek_id]
       },
       properties: {
         insurance: {
           bsonType: 'object',
           properties: {
             policyNumber: {
               encrypt: {
                 bsonType: 'int',
                 algorithm: 'AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic'
               }
             }
           }
         },
         medicalRecords: {
           encrypt: {
             bsonType: 'array',
             algorithm: 'AEAD_AES_256_CBC_HMAC_SHA_512-Random'
           }
         },
         bloodType: {
           encrypt: {
             bsonType: 'string',
             algorithm: 'AEAD_AES_256_CBC_HMAC_SHA_512-Random'
           }
         },
         ssn: {
           encrypt: {
             bsonType: 'int',
             algorithm: 'AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic'
           }
         }
       }
     }
   }
   ```

   The code reads your DEK (Data Encryption Key) ID and uses it to encrypt the following fields in the `medicalRecords.patients` collection:

   - `insurance.policyNumber`: Deterministically encrypted

   - `ssn`: Deterministically encrypted

   - `bloodType`: Randomly encrypted

   - `medicalRecords`: Randomly encrypted

   Deterministic encryption allows you to perform equality queries on the encrypted fields. Random encryption provides stronger security for fields that you don't need to query, because this algorithm does not support read operations on the encrypted fields.

5. Create a standard and a CSFLE-enabled client.

   Paste the following code into your `insert_encrypted_document.rb` file under the `# Paste client configuration code below` comment to create two MongoDB clients:

   ```ruby
   secure_client = Mongo::Client.new(
     CONNECTION_STRING,
     auto_encryption_options: {
       key_vault_namespace: KEY_VAULT_NAMESPACE,
       kms_providers: get_kms_providers,
       schema_map: patient_schema,
       extra_options: {
         crypt_shared_lib_path: CRYPT_SHARED_LIB_PATH
       }
     }
   )
   regular_client = Mongo::Client.new(CONNECTION_STRING)
   ```

   This code creates a `Mongo::Client` instance with an `auto_encryption_options` hash that specifies your KMS provider credentials, key vault namespace, encryption schema, and the location of your Automatic Encryption Shared Library. The code also creates a standard `Mongo::Client` instance without automatic encryption. In a future step, you will compare the output of both clients.

   **Note: Automatic Encryption Options**

   The automatic encryption options provide configuration information to the Automatic Encryption Shared Library, which modifies the application's behavior when accessing encrypted fields.

   To learn more about the Automatic Encryption Shared Library, see the [Install and Configure a CSFLE Query Analysis Component](/docs/manual/core/csfle/reference/install-library#std-label-csfle-reference-shared-library) page.

### Perform Encrypted Operations

After configuring your application and database connection, follow the steps in this section to insert and query encrypted documents.

1. Insert a document with encrypted fields.

   Add the following code to your `insert_encrypted_document.rb` file under the `# Paste code to insert a document below` comment to insert a document into the `medicalRecords.patients` collection:

   ```ruby
   collection = secure_client.use('medicalRecords')['patients']
   collection.insert_one(
     name: 'Jon Doe',
     ssn: 241014209,
     bloodType: 'AB+',
     medicalRecords: [{ weight: 180, bloodPressure: '120/80' }],
     insurance: {
       policyNumber: 123142,
       provider: 'MaestCare'
     }
   )
   ```

   When you insert the document, your CSFLE-enabled client automatically encrypts the specified fields. The stored document resembles the following code:

   ```json
   {
     "_id": { "$oid": "<_id of your document>" },
     "name": "Jon Doe",
     "ssn": {
       "$binary": "<cipher-text>",
       "$type": "6"
     },
     "bloodType": {
       "$binary": "<cipher-text>",
       "$type": "6"
     },
     "medicalRecords": {
       "$binary": "<cipher-text>",
       "$type": "6"
     },
     "insurance": {
       "provider": "MaestCare",
       "policyNumber": {
         "$binary": "<cipher-text>",
         "$type": "6"
       }
     }
   }

   ```

2. Query encrypted data.

   Add the following code to your `insert_encrypted_document.rb` file under the `# Paste code to query the document below` comment to retrieve the document by using both a CSFLE-enabled client and a standard client:

   ```ruby
   puts 'Finding a document with the regular (non-encrypted) client:'
   p regular_client.use('medicalRecords')['patients']
     .find(name: 'Jon Doe').first

   puts "\nFinding a document with the encrypted client:"
   p secure_client.use('medicalRecords')['patients']
     .find(name: 'Jon Doe').first

   regular_client.close
   secure_client.close
   ```

   The CSFLE-enabled client automatically decrypts the encrypted fields when it retrieves the document. The standard client returns the encrypted binary values.

3. Run the application.

   To start the application, run the following command from your project directory:

   ```bash
   ruby main.rb
   ```

   If successful, your output resembles the following example:

   ```none
   ============================================================
   Running make_data_key.rb...
   ============================================================
   DataKeyId [base64]: ...

   ============================================================
   Running insert_encrypted_document.rb...
   ============================================================
   Finding a document with the regular (non-encrypted) client:
   {"_id" => BSON::ObjectId('...'), "name" => "Jon Doe", "ssn" =>
   <BSON::Binary:0x688 type=ciphertext data=0x0114bccfbe8e954f...>,
   "bloodType" => <BSON::Binary:0x696 type=ciphertext data=0x0214bccfbe8e954f...>,
   "medicalRecords" => <BSON::Binary:0x704 type=ciphertext data=0x0214bccfbe8e954f...>,
   "insurance" => {"policyNumber" => <BSON::Binary:0x712 type=ciphertext data=0x0114bccfbe8e954f...>,
   "provider" => "MaestCare"}}

   Finding a document with the encrypted client:
   {"_id" => BSON::ObjectId('...'), "name" => "Jon Doe", "ssn" => 241014209,
   "bloodType" => "AB+", "medicalRecords" => [{"weight" => 180, "bloodPressure" => "120/80"}],
   "insurance" => {"policyNumber" => 123142, "provider" => "MaestCare"}}

   ============================================================
   All scripts completed successfully!
   ============================================================
   ```

   The output includes your DEK (Data Encryption Key) ID, the encrypted document as stored in your database, and the decrypted document retrieved with your CSFLE-enabled client.

## Learn More

To learn how to create a production-ready CSFLE with a remote KMS, see the [CSFLE Tutorials.](/docs/manual/core/csfle/tutorials#std-label-csfle-tutorial-automatic-encryption)

To learn how CSFLE works, see [CSFLE Fundamentals.](/docs/manual/core/csfle/fundamentals#std-label-csfle-fundamentals)

To learn more about the topics mentioned in this guide, see the following resources:

- [Customer Master Keys](/docs/manual/core/queryable-encryption/fundamentals/keys-key-vaults#std-label-qe-reference-keys-key-vaults)

- [Key Management System providers](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-fundamentals-kms-providers)

- [Data Encryption Keys](/docs/manual/core/queryable-encryption/fundamentals/keys-key-vaults#std-label-qe-reference-keys-key-vaults)

- [Key Vault collections](/docs/manual/core/queryable-encryption/fundamentals/keys-key-vaults#std-label-qe-reference-keys-key-vaults)

- [Encryption Schemas](/docs/manual/core/csfle/reference/encryption-schemas#std-label-csfle-reference-encryption-schemas)

- [mongocryptd](/docs/manual/core/csfle/reference/install-library#std-label-csfle-reference-mongocryptd)

- [CSFLE-specific MongoClient settings](/docs/manual/core/csfle/reference/csfle-options-clients#std-label-csfle-reference-mongo-client)

- [Automatic CSFLE Writes](/docs/manual/core/csfle/fundamentals/automatic-encryption#std-label-csfle-fundamentals-automatic-encryption)
