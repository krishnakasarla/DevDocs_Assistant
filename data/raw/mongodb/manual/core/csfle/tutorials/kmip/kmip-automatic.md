> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

<!--
Tab options on this page. Append to the .md URL to filter:
  ?tabs=<id,...>   select specific tabs (e.g. ?tabs=nodejs,shell)
  ?allTabs=true    include every tab
  (no param)       default: one tab per tabset

Available tabs:
  other tabs: csharp-v3, csharp-v2
-->

# Use Automatic Client-Side Field Level Encryption with KMIP

## Overview

This guide shows you how to build a Client-Side Field Level Encryption (CSFLE)-enabled application using a Key Management Interoperability Protocol (KMIP)-compliant key provider.

After you complete the steps in this guide, you should have:

- A Customer Master Key hosted on a KMIP (Key Management Interoperability Protocol)-compliant key provider.

- A working client application that inserts documents with encrypted fields using your Customer Master Key.

## Before You Get Started

Before you begin this tutorial, complete the following prerequisite steps:

1. Download the Automatic Encryption Shared Library from the [MongoDB Download Center](https://www.mongodb.com/try/download/enterprise?tck=docs). Navigate to the MongoDB Enterprise Server Download section and select the follow options:

   - In the Version dropdown, select the version marked as `"current"`.

   - In the Platform dropdown, select your platform.

   - In the Package dropdown, select `crypt_shared`.

   Extract the archive and save the path to the shared library file for future use.

   **Note: Query Analysis Component**

   The Automatic Encryption Shared Library is a preferred alternative to `mongocryptd` and does not require spawning a new process to perform automatic encryption. This tutorial uses the Automatic Encryption Shared Library, but `mongocryptd` is still supported.

2. Configure a MongoDB Atlas cluster or a local replica set deployment, and save your connection string for future use. To learn more, see the [Get Started](https://www.mongodb.com/docs/get-started/#std-label-unified-get-started) tutorial.

Throughout this guide, code examples use placeholder text. Before you run the examples, substitute your own values for these placeholders.

For example:

```go
dek_id := "<Your Base64 DEK ID>"
```

You would replace everything between quotes with your DEK (Data Encryption Key) ID.

```go
dek_id := "abc123"
```

Select the programming language for which you want to see code examples for from the dropdown menu below.

### Full Application Code

[Complete Java Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/java/kmip/reader/)

[Complete Node.js Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/node/kmip/reader/)

[Complete Python Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/python/kmip/reader/)

[Complete C# Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/dotnet/kmip/reader/CSFLE/)

[Complete Go Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/go/kmip/reader/)

### Set Up the KMS

**Note:**

`mongod` reads the KMIP configuration at startup. By default, the server uses KMIP protocol version 1.2.

To connect to a version 1.0 or 1.1 KMIP server, use the [`useLegacyProtocol`](/docs/manual/reference/configuration-options#mongodb-setting-security.kmip.useLegacyProtocol) setting.

1. Configure your KMIP-compliant key provider

   To connect a MongoDB driver client to your KMIP (Key Management Interoperability Protocol)-compliant key provider, you must configure your KMIP (Key Management Interoperability Protocol)-compliant key provider such that it accepts your client's TLS certificate.

   Consult the documentation for your KMIP (Key Management Interoperability Protocol)-compliant key provider for information on how to accept your client certificate.

2. Specify your Certificates

   Your client must connect to your KMIP (Key Management Interoperability Protocol)-compliant key provider through TLS and present a client certificate that your KMIP (Key Management Interoperability Protocol)-compliant key provider accepts:

   ```javascript
   const tlsOptions = {
     kmip: {
       tlsCAFile:
         "<path to file containing your Certificate Authority certificate>",
       tlsCertificateKeyFile: "<path to your client certificate file>",
     },
   };
   ```

#### Create the Application

1. Create a Unique Index on Your Key Vault Collection

   Create a unique index on the `keyAltNames` field in your `encryption.__keyVault` namespace.

   Select the tab corresponding to your preferred MongoDB driver:

   ```javascript
   const uri = "<Your Connection String>";
   const keyVaultDatabase = "encryption";
   const keyVaultCollection = "__keyVault";
   const keyVaultNamespace = `${keyVaultDatabase}.${keyVaultCollection}`;
   const keyVaultClient = new MongoClient(uri);
   await keyVaultClient.connect();
   const keyVaultDB = keyVaultClient.db(keyVaultDatabase);
   // Drop the Key Vault Collection in case you created this collection
   // in a previous run of this application.
   await keyVaultDB.dropDatabase();
   // Drop the database storing your encrypted fields as all
   // the DEKs encrypting those fields were deleted in the preceding line.
   await keyVaultClient.db("medicalRecords").dropDatabase();
   const keyVaultColl = keyVaultDB.collection(keyVaultCollection);
   await keyVaultColl.createIndex(
     { keyAltNames: 1 },
     {
       unique: true,
       partialFilterExpression: { keyAltNames: { $exists: true } },
     }
   );
   ```

2. Create a Data Encryption Key

   Add your Endpoint

   Specify the URI endpoint of your KMIP (Key Management Interoperability Protocol)-compliant key provider:

   ```javascript
   const provider = "kmip";
   const kmsProviderCredentials = {
     kmip: {
       endpoint: "<endpoint for your KMIP-compliant key provider>",
     },
   };
   ```

   You can also provide a custom name for your KMS provider by passing in a string that includes the name of the KMS provider, followed by a colon and the custom name. Providing a unique name for a KMS provider allows you to specify multiple KMS providers of the same type.

   For example, you can name your KMIP KMS provider "my\_kmip\_provider" in your KMS credentials variable as shown in the following code:

   Add Your Key Information

   The following code prompts your KMIP (Key Management Interoperability Protocol)-compliant key provider to automatically generate a Customer Master Key:

   ```javascript
   const masterKey = {}; // an empty key object prompts your KMIP-compliant key provider to generate a new Customer Master Key
   ```

   Generate your Data Encryption Key

   Generate your Data Encryption Key using the variables declared in [step one](/docs/manual/core/csfle/tutorials/kmip/kmip-automatic#std-label-csfle-kmip-create-index) of this tutorial.

   ```javascript
   const client = new MongoClient(uri);
   await client.connect();

   const encryption = new ClientEncryption(client, {
     keyVaultNamespace,
     kmsProviderCredentials,
     tlsOptions,
   });
   const key = await encryption.createDataKey(provider, {
     masterKey: masterKey,
   });
   console.log("DataKeyId [base64]: ", key.toString("base64"));
   await keyVaultClient.close();
   await client.close();
   ```

   **Note: Import ClientEncryption**

   When using the Node.js driver v6.0 and later, you must import `ClientEncryption` from `mongodb`.

   For earlier driver versions, import `ClientEncryption` from `mongodb-client-encryption`.

   **See also: Complete Code**

   To view the complete code for making a Data Encryption Key, see [our Github repository.](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/node/kmip/reader/make_data_key.js)

3. Configure the MongoClient

   **Tip:**

   Follow the remaining steps in this tutorial in a separate file from the one created in the previous steps.

   To view the complete code for this file, see [our Github repository.](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/node/kmip/reader/insert_encrypted_document.js)

   Specify the Key Vault Collection Namespace

   Specify `encryption.__keyVault` as the Key Vault collection namespace.

   ```javascript
   const keyVaultNamespace = "encryption.__keyVault";
   ```

   Specify your KMIP Endpoint

   Specify `kmip` in your `kmsProviders` object and enter the URI endpoint of your KMIP (Key Management Interoperability Protocol)-compliant key provider:

   ```javascript
   const provider = "kmip";
   const kmsProviders = {
     kmip: {
       endpoint: "<endpoint for your KMIP-compliant key provider>",
     },
   };
   ```

   Create an Encryption Schema For Your Collection

   Create an encryption schema that specifies how your client application encrypts your documents' fields:

   **Tip: Add Your Data Encryption Key Base64 ID**

   Make sure to update the following code to include your Base64 DEK (Data Encryption Key) ID. You received this value in the [Generate your Data Encryption Key](/docs/manual/core/csfle/tutorials/kmip/kmip-automatic#std-label-csfle-kmip-create-dek) step of this guide.

   ```javascript
   dataKey = "<Your base64 DEK ID>";
   const schema = {
     bsonType: "object",
     encryptMetadata: {
       keyId: [new Binary(Buffer.from(dataKey, "base64"), 4)],
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

   var patientSchema = {};
   patientSchema[namespace] = schema;
   ```

   **Tip: Further Reading on Schemas**

   To view an in-depth description of how to construct the schema you use in this step, see the [Encryption Schemas](/docs/manual/core/csfle/fundamentals/create-schema#std-label-csfle-fundamentals-create-schema) guide.

   To view a list of all supported encryption rules for your encryption schemas, see the [CSFLE Encryption Schemas](/docs/manual/core/csfle/reference/encryption-schemas#std-label-csfle-reference-encryption-schemas) guide.

   Specify the Location of the Automatic Encryption Shared Library

   ```javascript
   const extraOptions = {
     cryptSharedLibPath: "<Full path to your Automatic Encryption Shared Library>",
   };
   ```

   **Note: Automatic Encryption Options**

   The automatic encryption options provide configuration information to the Automatic Encryption Shared Library, which modifies the application's behavior when accessing encrypted fields.

   To learn more about the Automatic Encryption Shared Library, see the [Install and Configure a CSFLE Query Analysis Component](/docs/manual/core/csfle/reference/install-library#std-label-csfle-reference-shared-library) page.

   Create the MongoClient

   Instantiate a MongoDB client object with the following automatic encryption settings that use the variables declared in the previous steps:

   ```javascript
   const secureClient = new MongoClient(connectionString, {
     autoEncryption: {
       keyVaultNamespace,
       kmsProviders,
       schemaMap: patientSchema,
       extraOptions: extraOptions,
       tlsOptions,
     },
   });
   ```

4. Insert a Document with Encrypted Fields

   Use your CSFLE-enabled `MongoClient` instance to insert a document with encrypted fields into the `medicalRecords.patients` namespace using the following code snippet:

   ```javascript
   try {
     const writeResult = await secureClient
       .db(db)
       .collection(coll)
       .insertOne({
         name: "Jon Doe",
         ssn: 241014209,
         bloodType: "AB+",
         medicalRecords: [{ weight: 180, bloodPressure: "120/80" }],
         insurance: {
           policyNumber: 123142,
           provider: "MaestCare",
         },
       });
   } catch (writeError) {
     console.error("writeError occurred:", writeError);
   }
   ```

   When you insert a document, your CSFLE-enabled client encrypts the fields of your document such that it resembles the following:

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

   **See also: Complete Code**

   To view the complete code for inserting a document with encrypted fields, see [our Github repository.](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/node/kmip/reader/insert_encrypted_document.js)

5. Retrieve Your Document with Encrypted Fields

   Retrieve the document with encrypted fields you inserted in the [Insert a Document with Encrypted Fields](/docs/manual/core/csfle/tutorials/kmip/kmip-automatic#std-label-csfle-kmip-insert) step of this guide.

   To show the functionality of CSFLE, the following code snippet queries for your document with a client configured for automatic CSFLE as well as a client that is not configured for automatic CSFLE.

   ```javascript
   console.log("Finding a document with regular (non-encrypted) client.");
   console.log(
     await regularClient.db(db).collection(coll).findOne({ name: /Jon/ })
   );

   console.log("Finding a document with encrypted client");
   console.log(
     await secureClient.db(db).collection(coll).findOne({ name: /Jon/ })
   );
   ```

   The output of the preceding code snippet should look like this:

   ```json
   Finding a document with regular (non-encrypted) client.

   {
     _id: new ObjectId("629a452e0861b3130887103a"),
     name: 'Jon Doe',
     ssn: new Binary(Buffer.from("0217482732d8014cdd9ffdd6e2966e5e7910c20697e5f4fa95710aafc9153f0a3dc769c8a132a604b468732ff1f4d8349ded3244b59cbfb41444a210f28b21ea1b6c737508d9d30e8baa30c1d8070c4d5e26", "hex"), 6),
     bloodType: new Binary(Buffer.from("0217482732d8014cdd9ffdd6e2966e5e79022e238536dfd8caadb4d7751ac940e0f195addd7e5c67b61022d02faa90283ab69e02303c7e4001d1996128428bf037dea8bbf59fbb20c583cbcff2bf3e2519b4", "hex"), 6),
     'key-id': 'demo-data-key',
     medicalRecords: new Binary(Buffer.from("0217482732d8014cdd9ffdd6e2966e5e790405163a3207cff175455106f57eef14e5610c49a99bcbd14a7db9c5284e45e3ee30c149354015f941440bf54725d6492fb3b8704bc7c411cff6c868e4e13c58233c3d5ed9593eca4e4d027d76d3705b6d1f3b3c9e2ceee195fd944b553eb27eee69e5e67c338f146f8445995664980bf0", "hex"), 6),
     insurance: {
       policyNumber: new Binary(Buffer.from("0217482732d8014cdd9ffdd6e2966e5e79108decd85c05be3fec099e015f9d26d9234605dc959cc1a19b63072f7ffda99db38c7b487de0572a03b2139ac3ee163bcc40c8508f366ce92a5dd36e38b3c742f7", "hex"), 6),
       provider: 'MaestCare'
     }
   }

   Finding a document with encrypted client

   {
     _id: new ObjectId("629a452e0861b3130887103a"),
     name: 'Jon Doe',
     ssn: 241014209,
     bloodType: 'AB+',
     'key-id': 'demo-data-key',
     medicalRecords: [ { weight: 180, bloodPressure: '120/80' } ],
     insurance: { policyNumber: 123142, provider: 'MaestCare' }
   }

   ```

   **See also: Complete Code**

   To view the complete code for inserting a document with encrypted fields, see [our Github repository.](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/node/kmip/reader/insert_encrypted_document.js)

1) Configure your KMIP-compliant key provider

   To connect a MongoDB driver client to your KMIP (Key Management Interoperability Protocol)-compliant key provider, you must configure your KMIP (Key Management Interoperability Protocol)-compliant key provider such that it accepts your client's TLS certificate.

   Consult the documentation for your KMIP (Key Management Interoperability Protocol)-compliant key provider for information on how to accept your client certificate.

2) Specify your Certificates

   Your client must connect to your KMIP (Key Management Interoperability Protocol)-compliant key provider through TLS and present a client certificate that your KMIP (Key Management Interoperability Protocol)-compliant key provider accepts:

   Specify the following Java system properties to configure your client's TLS connection:

   ```shell
   -Djavax.net.ssl.keyStoreType=pkcs12
   -Djavax.net.ssl.keyStore=<path to pkcs12 KeyStore containing your client certificate>
   -Djavax.net.ssl.keyStorePassword=<KeyStore password>
   ```

   **Note: Configure Client With SSLContext**

   If you would rather configure your client application using an SSL context, use the [kmsProviderSslContextMap](https://mongodb.github.io/mongo-java-driver/5.6/apidocs/driver-core/com/mongodb/ClientEncryptionSettings.Builder.html#kmsProviderSslContextMap\(java.util.Map\)) method.

#### Create the Application

1. Create a Unique Index on Your Key Vault Collection

   Create a unique index on the `keyAltNames` field in your `encryption.__keyVault` namespace.

   Select the tab corresponding to your preferred MongoDB driver:

   ```java
   String connectionString = "<Your MongoDB URI>";
   String keyVaultDb = "encryption";
   String keyVaultColl = "__keyVault";
   String keyVaultNamespace = keyVaultDb + "." + keyVaultColl;
   MongoClient keyVaultClient = MongoClients.create(connectionString);

   // Drop the Key Vault Collection in case you created this collection
   // in a previous run of this application.
   keyVaultClient.getDatabase(keyVaultDb).getCollection(keyVaultColl).drop();
   // Drop the database storing your encrypted fields as all
   // the DEKs encrypting those fields were deleted in the preceding line.
   keyVaultClient.getDatabase("medicalRecords").getCollection("patients").drop();


   MongoCollection keyVaultCollection = keyVaultClient.getDatabase(keyVaultDb).getCollection(keyVaultColl);
   IndexOptions indexOpts = new IndexOptions().partialFilterExpression(new BsonDocument("keyAltNames", new BsonDocument("$exists", new BsonBoolean(true) ))).unique(true);
   keyVaultCollection.createIndex(new BsonDocument("keyAltNames", new BsonInt32(1)), indexOpts);
   keyVaultClient.close();
   ```

2. Create a Data Encryption Key

   Add your Endpoint

   Specify the URI endpoint of your KMIP (Key Management Interoperability Protocol)-compliant key provider:

   ```java
   String kmsProvider = "kmip";
   Map<String, Map<String, Object>> kmsProviderDetails = new HashMap<String, Map<String, Object>>();
   Map<String, Object> providerDetails = new HashMap<>();
   providerDetails.put("endpoint", "<endpoint for your KMIP-compliant key provider>");
   kmsProviderDetails.put(kmsProvider, providerDetails);
   ```

   You can also provide a custom name for your KMS provider by passing in a string that includes the name of the KMS provider, followed by a colon and the custom name. Providing a unique name for a KMS provider allows you to specify multiple KMS providers of the same type.

   For example, you can name your KMIP KMS provider "my\_kmip\_provider" in your KMS credentials variable as shown in the following code:

   ```java
   Map<String, Object> kmsProviderDetails = new HashMap<>();
   kmsProviderDetails.put("endpoint", getEnv("KMIP_KMS_ENDPOINT")); // Your KMIP KMS endpoint

   Map<String, Map<String, Object>> kmsProviderCredentials = new HashMap<String, Map<String, Object>>();
   kmsProviderCredentials.put("kmip:my_kmip_provider", kmsProviderDetails);
   ```

   Add Your Key Information

   The following code prompts your KMIP (Key Management Interoperability Protocol)-compliant key provider to automatically generate a Customer Master Key:

   ```java
   BsonDocument masterKeyProperties = new BsonDocument(); // an empty key object prompts your KMIP-compliant key provider to generate a new Customer Master Key
   ```

   Generate your Data Encryption Key

   Generate your Data Encryption Key using the variables declared in [step one](/docs/manual/core/csfle/tutorials/kmip/kmip-automatic#std-label-csfle-kmip-create-index) of this tutorial.

   ```java
   ClientEncryptionSettings clientEncryptionSettings = ClientEncryptionSettings.builder()
           .keyVaultMongoClientSettings(MongoClientSettings.builder()
                   .applyConnectionString(new ConnectionString(connectionString))
                   .build())
           .keyVaultNamespace(keyVaultNamespace)
           .kmsProviders(kmsProviderDetails)
           .build();

   MongoClient regularClient = MongoClients.create(connectionString);

   ClientEncryption clientEncryption = ClientEncryptions.create(clientEncryptionSettings);
   BsonBinary dataKeyId = clientEncryption.createDataKey(kmsProvider, new DataKeyOptions().masterKey(masterKeyProperties));
   String base64DataKeyId = Base64.getEncoder().encodeToString(dataKeyId.getData());
   System.out.println("DataKeyId [base64]: " + base64DataKeyId);
   clientEncryption.close();
   ```

   **See also: Complete Code**

   To view the complete code for making a Data Encryption Key, see [our Github repository.](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/java/kmip/reader/src/main/java/com/mongodb/csfle/MakeDataKey.java)

3. Configure the MongoClient

   **Tip:**

   Follow the remaining steps in this tutorial in a separate file from the one created in the previous steps.

   To view the complete code for this file, see [our Github repository.](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/java/kmip/reader/src/main/java/com/mongodb/csfle/InsertEncryptedDocument.java)

   Specify the Key Vault Collection Namespace

   Specify `encryption.__keyVault` as the Key Vault collection namespace.

   ```java
   String keyVaultNamespace = "encryption.__keyVault";
   ```

   Specify your KMIP Endpoint

   Specify `kmip` in your `kmsProviders` object and enter the URI endpoint of your KMIP (Key Management Interoperability Protocol)-compliant key provider:

   ```java
   String kmsProvider = "kmip";
   Map<String, Map<String, Object>> kmsProviders = new HashMap<String, Map<String, Object>>();
   Map<String, Object> providerDetails = new HashMap<>();
   providerDetails.put("endpoint", "<endpoint for your KMIP-compliant key provider>");
   kmsProviders.put(kmsProvider, providerDetails);
   ```

   Create an Encryption Schema For Your Collection

   Create an encryption schema that specifies how your client application encrypts your documents' fields:

   **Tip: Add Your Data Encryption Key Base64 ID**

   Make sure to update the following code to include your Base64 DEK (Data Encryption Key) ID. You received this value in the [Generate your Data Encryption Key](/docs/manual/core/csfle/tutorials/kmip/kmip-automatic#std-label-csfle-kmip-create-dek) step of this guide.

   ```java
   String dekId = "<paste-base-64-encoded-data-encryption-key-id>>";
   Document jsonSchema = new Document().append("bsonType", "object").append("encryptMetadata",
           new Document().append("keyId", new ArrayList<>((Arrays.asList(new Document().append("$binary", new Document()
                   .append("base64", dekId)
                   .append("subType", "04")))))))
           .append("properties", new Document()
                   .append("ssn", new Document().append("encrypt", new Document()
                           .append("bsonType", "int")
                           .append("algorithm", "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic")))
                   .append("bloodType", new Document().append("encrypt", new Document()
                           .append("bsonType", "string")
                           .append("algorithm", "AEAD_AES_256_CBC_HMAC_SHA_512-Random")))
                   .append("medicalRecords", new Document().append("encrypt", new Document()
                           .append("bsonType", "array")
                           .append("algorithm", "AEAD_AES_256_CBC_HMAC_SHA_512-Random")))
                   .append("insurance", new Document()
                           .append("bsonType", "object")
                           .append("properties",
                                   new Document().append("policyNumber", new Document().append("encrypt", new Document()
                                           .append("bsonType", "int")
                                           .append("algorithm", "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic"))))));
   HashMap<String, BsonDocument> schemaMap = new HashMap<String, BsonDocument>();
   schemaMap.put("medicalRecords.patients", BsonDocument.parse(jsonSchema.toJson()));
   ```

   **Tip: Further Reading on Schemas**

   To view an in-depth description of how to construct the schema you use in this step, see the [Encryption Schemas](/docs/manual/core/csfle/fundamentals/create-schema#std-label-csfle-fundamentals-create-schema) guide.

   To view a list of all supported encryption rules for your encryption schemas, see the [CSFLE Encryption Schemas](/docs/manual/core/csfle/reference/encryption-schemas#std-label-csfle-reference-encryption-schemas) guide.

   Specify the Location of the Automatic Encryption Shared Library

   ```java
   Map<String, Object> extraOptions = new HashMap<String, Object>();
   extraOptions.put("cryptSharedLibPath", "<Full path to your Automatic Encryption Shared Library>"));
   ```

   **Note: Automatic Encryption Options**

   The automatic encryption options provide configuration information to the Automatic Encryption Shared Library, which modifies the application's behavior when accessing encrypted fields.

   To learn more about the Automatic Encryption Shared Library, see the [Install and Configure a CSFLE Query Analysis Component](/docs/manual/core/csfle/reference/install-library#std-label-csfle-reference-shared-library) page.

   Create the MongoClient

   Instantiate a MongoDB client object with the following automatic encryption settings that use the variables declared in the previous steps:

   ```java
   MongoClientSettings clientSettings = MongoClientSettings.builder()
       .applyConnectionString(new ConnectionString(connectionString))
       .autoEncryptionSettings(AutoEncryptionSettings.builder()
           .keyVaultNamespace(keyVaultNamespace)
           .kmsProviders(kmsProviders)
           .schemaMap(schemaMap)
           .extraOptions(extraOptions)
           .build())
       .build();

   MongoClient mongoClientSecure = MongoClients.create(clientSettings);
   ```

4. Insert a Document with Encrypted Fields

   Use your CSFLE-enabled `MongoClient` instance to insert a document with encrypted fields into the `medicalRecords.patients` namespace using the following code snippet:

   ```java
   ArrayList<Document> medicalRecords = new ArrayList<>();
   medicalRecords.add(new Document().append("weight", "180"));
   medicalRecords.add(new Document().append("bloodPressure", "120/80"));

   Document insurance = new Document()
   .append("policyNumber", 123142)
   .append("provider",  "MaestCare");

   Document patient = new Document()
       .append("name", "Jon Doe")
       .append("ssn", 241014209)
       .append("bloodType", "AB+")
       .append("medicalRecords", medicalRecords)
       .append("insurance", insurance);
   mongoClientSecure.getDatabase(recordsDb).getCollection(recordsColl).insertOne(patient);
   ```

   When you insert a document, your CSFLE-enabled client encrypts the fields of your document such that it resembles the following:

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

   **See also: Complete Code**

   To view the complete code for inserting a document with encrypted fields, see [our Github repository.](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/java/kmip/reader/src/main/java/com/mongodb/csfle/InsertEncryptedDocument.java)

5. Retrieve Your Document with Encrypted Fields

   Retrieve the document with encrypted fields you inserted in the [Insert a Document with Encrypted Fields](/docs/manual/core/csfle/tutorials/kmip/kmip-automatic#std-label-csfle-kmip-insert) step of this guide.

   To show the functionality of CSFLE, the following code snippet queries for your document with a client configured for automatic CSFLE as well as a client that is not configured for automatic CSFLE.

   ```java
   System.out.println("Finding a document with regular (non-encrypted) client.");
   Document docRegular = mongoClientRegular.getDatabase(recordsDb).getCollection(recordsColl).find(eq("name", "Jon Doe")).first();
   System.out.println(docRegular.toJson());

   System.out.println("Finding a document with encrypted client");
   Document docSecure = mongoClientSecure.getDatabase(recordsDb).getCollection(recordsColl).find(eq("name", "Jon Doe")).first();
   System.out.println(docSecure.toJson());
   ```

   The output of the preceding code snippet should look like this:

   ```json
   Finding a document with regular (non-encrypted) client.

   {
     _id: new ObjectId("629a452e0861b3130887103a"),
     name: 'Jon Doe',
     ssn: new Binary(Buffer.from("0217482732d8014cdd9ffdd6e2966e5e7910c20697e5f4fa95710aafc9153f0a3dc769c8a132a604b468732ff1f4d8349ded3244b59cbfb41444a210f28b21ea1b6c737508d9d30e8baa30c1d8070c4d5e26", "hex"), 6),
     bloodType: new Binary(Buffer.from("0217482732d8014cdd9ffdd6e2966e5e79022e238536dfd8caadb4d7751ac940e0f195addd7e5c67b61022d02faa90283ab69e02303c7e4001d1996128428bf037dea8bbf59fbb20c583cbcff2bf3e2519b4", "hex"), 6),
     'key-id': 'demo-data-key',
     medicalRecords: new Binary(Buffer.from("0217482732d8014cdd9ffdd6e2966e5e790405163a3207cff175455106f57eef14e5610c49a99bcbd14a7db9c5284e45e3ee30c149354015f941440bf54725d6492fb3b8704bc7c411cff6c868e4e13c58233c3d5ed9593eca4e4d027d76d3705b6d1f3b3c9e2ceee195fd944b553eb27eee69e5e67c338f146f8445995664980bf0", "hex"), 6),
     insurance: {
       policyNumber: new Binary(Buffer.from("0217482732d8014cdd9ffdd6e2966e5e79108decd85c05be3fec099e015f9d26d9234605dc959cc1a19b63072f7ffda99db38c7b487de0572a03b2139ac3ee163bcc40c8508f366ce92a5dd36e38b3c742f7", "hex"), 6),
       provider: 'MaestCare'
     }
   }

   Finding a document with encrypted client

   {
     _id: new ObjectId("629a452e0861b3130887103a"),
     name: 'Jon Doe',
     ssn: 241014209,
     bloodType: 'AB+',
     'key-id': 'demo-data-key',
     medicalRecords: [ { weight: 180, bloodPressure: '120/80' } ],
     insurance: { policyNumber: 123142, provider: 'MaestCare' }
   }

   ```

   **See also: Complete Code**

   To view the complete code for inserting a document with encrypted fields, see [our Github repository.](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/java/kmip/reader/src/main/java/com/mongodb/csfle/InsertEncryptedDocument.java)

1) Configure your KMIP-compliant key provider

   To connect a MongoDB driver client to your KMIP (Key Management Interoperability Protocol)-compliant key provider, you must configure your KMIP (Key Management Interoperability Protocol)-compliant key provider such that it accepts your client's TLS certificate.

   Consult the documentation for your KMIP (Key Management Interoperability Protocol)-compliant key provider for information on how to accept your client certificate.

2) Specify your Certificates

   ```python
   tls_options = {
       "kmip": {
           "tlsCAFile": "<path to file containing your Certificate Authority certificate>",
           "tlsCertificateKeyFile": "<path to your client certificate file>",
       }
   }
   ```

#### Create the Application

1. Create a Unique Index on Your Key Vault Collection

   Create a unique index on the `keyAltNames` field in your `encryption.__keyVault` namespace.

   Select the tab corresponding to your preferred MongoDB driver:

   ```python
   connection_string = "<your connection string here>"

   key_vault_coll = "__keyVault"
   key_vault_db = "encryption"
   key_vault_namespace = f"{key_vault_db}.{key_vault_coll}"
   key_vault_client = MongoClient(connection_string)
   # Drop the Key Vault Collection in case you created this collection
   # in a previous run of this application.
   key_vault_client.drop_database(key_vault_db)
   # Drop the database storing your encrypted fields as all
   # the DEKs encrypting those fields were deleted in the preceding line.
   key_vault_client["medicalRecords"].drop_collection("patients")
   key_vault_client[key_vault_db][key_vault_coll].create_index(
       [("keyAltNames", ASCENDING)],
       unique=True,
       partialFilterExpression={"keyAltNames": {"$exists": True}},
   )
   ```

2. Create a Data Encryption Key

   Add your Endpoint

   Specify the URI endpoint of your KMIP (Key Management Interoperability Protocol)-compliant key provider:

   ```python
   provider = "kmip"
   kms_provider_credentials = {
       provider: {"endpoint": "<endpoint for your KMIP-compliant key provider>"}
   }
   ```

   You can also provide a custom name for your KMS provider by passing in a string that includes the name of the KMS provider, followed by a colon and the custom name. Providing a unique name for a KMS provider allows you to specify multiple KMS providers of the same type.

   For example, you can name your KMIP KMS provider "my\_kmip\_provider" in your KMS credentials variable as shown in the following code:

   ```python
   kms_provider_credentials = {
       "kmip:my_kmip_provider": {
           "endpoint": os.environ['KMIP_KMS_ENDPOINT'] # Your KMIP KMS endpoint
       }
   }
   ```

   Add Your Key Information

   The following code prompts your KMIP (Key Management Interoperability Protocol)-compliant key provider to automatically generate a Customer Master Key:

   ```python
   master_key = (
       {}
   )  # an empty key object prompts your KMIP-compliant key provider to generate a new Customer Master Key
   ```

   Generate your Data Encryption Key

   Generate your Data Encryption Key using the variables declared in [step one](/docs/manual/core/csfle/tutorials/kmip/kmip-automatic#std-label-csfle-kmip-create-index) of this tutorial.

   ```python
   key_vault_database = "encryption"
   key_vault_collection = "__keyVault"
   key_vault_namespace = f"{key_vault_database}.{key_vault_collection}"

   client = MongoClient(connection_string)
   client_encryption = ClientEncryption(
       kms_provider_credentials,  # pass in the kms_provider_credentials variable from the previous step
       key_vault_namespace,
       client,
       CodecOptions(uuid_representation=STANDARD),
       kms_tls_options=tls_options,
   )
   data_key_id = client_encryption.create_data_key(provider, master_key)

   base_64_data_key_id = base64.b64encode(data_key_id)
   print("DataKeyId [base64]: ", base_64_data_key_id)
   ```

   **See also: Complete Code**

   To view the complete code for making a Data Encryption Key, see [our Github repository.](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/python/kmip/reader/make_data_key.py)

3. Configure the MongoClient

   **Tip:**

   Follow the remaining steps in this tutorial in a separate file from the one created in the previous steps.

   To view the complete code for this file, see [our Github repository.](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/python/kmip/reader/insert_encrypted_document.py)

   Specify the Key Vault Collection Namespace

   Specify `encryption.__keyVault` as the Key Vault collection namespace.

   ```python
   key_vault_namespace = "encryption.__keyVault"
   ```

   Specify your KMIP Endpoint

   Specify `kmip` in your `kmsProviders` object and enter the URI endpoint of your KMIP (Key Management Interoperability Protocol)-compliant key provider:

   ```python
   provider = "kmip"
   kms_providers = {
       provider: {"endpoint": "<endpoint for your KMIP-compliant key provider>"}
   }
   ```

   Create an Encryption Schema For Your Collection

   Create an encryption schema that specifies how your client application encrypts your documents' fields:

   **Tip: Add Your Data Encryption Key Base64 ID**

   Make sure to update the following code to include your Base64 DEK (Data Encryption Key) ID. You received this value in the [Generate your Data Encryption Key](/docs/manual/core/csfle/tutorials/kmip/kmip-automatic#std-label-csfle-kmip-create-dek) step of this guide.

   ```python
   dek_id = b"<paste-base-64-encoded-data-encryption-key-id>"
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

   **Tip: Further Reading on Schemas**

   To view an in-depth description of how to construct the schema you use in this step, see the [Encryption Schemas](/docs/manual/core/csfle/fundamentals/create-schema#std-label-csfle-fundamentals-create-schema) guide.

   To view a list of all supported encryption rules for your encryption schemas, see the [CSFLE Encryption Schemas](/docs/manual/core/csfle/reference/encryption-schemas#std-label-csfle-reference-encryption-schemas) guide.

   Specify the Location of the Automatic Encryption Shared Library

   ```python
   extra_options = {
       "cryptSharedLibPath": "<Full path to your Automatic Encryption Shared Library>"
   }
   ```

   **Note: Automatic Encryption Options**

   The automatic encryption options provide configuration information to the Automatic Encryption Shared Library, which modifies the application's behavior when accessing encrypted fields.

   To learn more about the Automatic Encryption Shared Library, see the [Install and Configure a CSFLE Query Analysis Component](/docs/manual/core/csfle/reference/install-library#std-label-csfle-reference-shared-library) page.

   Create the MongoClient

   Instantiate a MongoDB client object with the following automatic encryption settings that use the variables declared in the previous steps:

   ```python
   fle_opts = AutoEncryptionOpts(
       kms_providers,
       key_vault_namespace,
       schema_map=patient_schema,
       kms_tls_options=tls_options,
       **extra_options
   )
   secureClient = MongoClient(connection_string, auto_encryption_opts=fle_opts)
   ```

4. Insert a Document with Encrypted Fields

   Use your CSFLE-enabled `MongoClient` instance to insert a document with encrypted fields into the `medicalRecords.patients` namespace using the following code snippet:

   ```python
   def insert_patient(
       collection, name, ssn, blood_type, medical_records, policy_number, provider
   ):
       insurance = {"policyNumber": policy_number, "provider": provider}
       doc = {
           "name": name,
           "ssn": ssn,
           "bloodType": blood_type,
           "medicalRecords": medical_records,
           "insurance": insurance,
       }
       collection.insert_one(doc)


   medical_record = [{"weight": 180, "bloodPressure": "120/80"}]
   insert_patient(
       secureClient.medicalRecords.patients,
       "Jon Doe",
       241014209,
       "AB+",
       medical_record,
       123142,
       "MaestCare",
   )
   ```

   When you insert a document, your CSFLE-enabled client encrypts the fields of your document such that it resembles the following:

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

   **See also: Complete Code**

   To view the complete code for inserting a document with encrypted fields, see [our Github repository.](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/python/kmip/reader/insert_encrypted_document.py)

5. Retrieve Your Document with Encrypted Fields

   Retrieve the document with encrypted fields you inserted in the [Insert a Document with Encrypted Fields](/docs/manual/core/csfle/tutorials/kmip/kmip-automatic#std-label-csfle-kmip-insert) step of this guide.

   To show the functionality of CSFLE, the following code snippet queries for your document with a client configured for automatic CSFLE as well as a client that is not configured for automatic CSFLE.

   ```python
   print("Finding a document with regular (non-encrypted) client.")
   result = regularClient.medicalRecords.patients.find_one({"name": "Jon Doe"})
   pprint.pprint(result)

   print("Finding a document with encrypted client")
   pprint.pprint(secureClient.medicalRecords.patients.find_one({"name": "Jon Doe"}))
   ```

   The output of the preceding code snippet should look like this:

   ```json
   Finding a document with regular (non-encrypted) client.

   {
     _id: new ObjectId("629a452e0861b3130887103a"),
     name: 'Jon Doe',
     ssn: new Binary(Buffer.from("0217482732d8014cdd9ffdd6e2966e5e7910c20697e5f4fa95710aafc9153f0a3dc769c8a132a604b468732ff1f4d8349ded3244b59cbfb41444a210f28b21ea1b6c737508d9d30e8baa30c1d8070c4d5e26", "hex"), 6),
     bloodType: new Binary(Buffer.from("0217482732d8014cdd9ffdd6e2966e5e79022e238536dfd8caadb4d7751ac940e0f195addd7e5c67b61022d02faa90283ab69e02303c7e4001d1996128428bf037dea8bbf59fbb20c583cbcff2bf3e2519b4", "hex"), 6),
     'key-id': 'demo-data-key',
     medicalRecords: new Binary(Buffer.from("0217482732d8014cdd9ffdd6e2966e5e790405163a3207cff175455106f57eef14e5610c49a99bcbd14a7db9c5284e45e3ee30c149354015f941440bf54725d6492fb3b8704bc7c411cff6c868e4e13c58233c3d5ed9593eca4e4d027d76d3705b6d1f3b3c9e2ceee195fd944b553eb27eee69e5e67c338f146f8445995664980bf0", "hex"), 6),
     insurance: {
       policyNumber: new Binary(Buffer.from("0217482732d8014cdd9ffdd6e2966e5e79108decd85c05be3fec099e015f9d26d9234605dc959cc1a19b63072f7ffda99db38c7b487de0572a03b2139ac3ee163bcc40c8508f366ce92a5dd36e38b3c742f7", "hex"), 6),
       provider: 'MaestCare'
     }
   }

   Finding a document with encrypted client

   {
     _id: new ObjectId("629a452e0861b3130887103a"),
     name: 'Jon Doe',
     ssn: 241014209,
     bloodType: 'AB+',
     'key-id': 'demo-data-key',
     medicalRecords: [ { weight: 180, bloodPressure: '120/80' } ],
     insurance: { policyNumber: 123142, provider: 'MaestCare' }
   }

   ```

   **See also: Complete Code**

   To view the complete code for inserting a document with encrypted fields, see [our Github repository.](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/python/kmip/reader/insert_encrypted_document.py)

1) Configure your KMIP-compliant key provider

   To connect a MongoDB driver client to your KMIP (Key Management Interoperability Protocol)-compliant key provider, you must configure your KMIP (Key Management Interoperability Protocol)-compliant key provider such that it accepts your client's TLS certificate.

   Consult the documentation for your KMIP (Key Management Interoperability Protocol)-compliant key provider for information on how to accept your client certificate.

2) Specify your Certificates

   ```csharp
   var tlsOptions = new Dictionary<string, SslSettings>();
   var sslSettings = new SslSettings();
   var clientCertificate = new X509Certificate2("<path to your pkcs12 client certificate file>");
   sslSettings.ClientCertificates = new List<X509Certificate>() {
       clientCertificate,
    };
   tlsOptions.Add(provider, sslSettings);
   ```

   **Important:**

   Your client certificate must be in pkcs12 format. You can convert your certificate using your certificate using [OpenSSL](https://docs.openssl.org/master/) with the following command:

   ```shell
   openssl pkcs12 -export -out "<new pkcs12 certificate>" -in "<certificate to convert>" \
   -name "<new certificate name>" -password "<new certificate
   password>"
   ```

#### Create the Application

1. Create a Unique Index on Your Key Vault Collection

   Create a unique index on the `keyAltNames` field in your `encryption.__keyVault` namespace.

   Select the tab corresponding to your preferred MongoDB driver:

   ```csharp
   var connectionString = "<Your MongoDB URI>";
   var keyVaultNamespace = CollectionNamespace.FromFullName("encryption.__keyVault");
   var keyVaultClient = new MongoClient(connectionString);
   var indexOptions = new CreateIndexOptions<BsonDocument>();
   indexOptions.Unique = true;
   indexOptions.PartialFilterExpression = new BsonDocument { { "keyAltNames", new BsonDocument { { "$exists", new BsonBoolean(true) } } } };
   var builder = Builders<BsonDocument>.IndexKeys;
   var indexKeysDocument = builder.Ascending("keyAltNames");
   var indexModel = new CreateIndexModel<BsonDocument>(indexKeysDocument, indexOptions);
   var keyVaultDatabase = keyVaultClient.GetDatabase(keyVaultNamespace.DatabaseNamespace.ToString());
   // Drop the Key Vault Collection in case you created this collection
   // in a previous run of this application.  
   keyVaultDatabase.DropCollection(keyVaultNamespace.CollectionName);
   // Drop the database storing your encrypted fields as all
   // the DEKs encrypting those fields were deleted in the preceding line.
   keyVaultClient.GetDatabase("medicalRecords").DropCollection("patients");
   var keyVaultCollection = keyVaultDatabase.GetCollection<BsonDocument>(keyVaultNamespace.CollectionName.ToString());
   keyVaultCollection.Indexes.CreateOne(indexModel);
   ```

2. Create a Data Encryption Key

   Add your Endpoint

   Specify the URI endpoint of your KMIP (Key Management Interoperability Protocol)-compliant key provider:

   ```csharp
   var kmsProviderCredentials = new Dictionary<string, IReadOnlyDictionary<string, object>>();
   var provider = "kmip";
   var kmipKmsOptions = new Dictionary<string, object>
   {
      { "endpoint", "<endpoint for your KMIP-compliant key provider>" },
   };
   kmsProviderCredentials.Add(provider, kmipKmsOptions);
   ```

   You can also provide a custom name for your KMS provider by passing in a string that includes the name of the KMS provider, followed by a colon and the custom name. Providing a unique name for a KMS provider allows you to specify multiple KMS providers of the same type.

   For example, you can name your KMIP KMS provider "my\_kmip\_provider" in your KMS credentials variable as shown in the following code:

   ```csharp
   var kmsProviderCredentials = new Dictionary<string, IReadOnlyDictionary<string, object>>();
   var kmsOptions = new Dictionary<string, object>
   {
       { "endpoint", _appSettings["Kmip:KmsEndpoint"] } // Your KMIP KMS endpoint
   };
   kmsProviderCredentials.Add("kmip:my_kmip_provider", kmsOptions);
   ```

   Add Your Key Information

   The following code prompts your KMIP (Key Management Interoperability Protocol)-compliant key provider to automatically generate a Customer Master Key:

   ```csharp
   var dataKeyOptions = new DataKeyOptions(
       masterKey: new BsonDocument { } // an empty key object prompts your KMIP-compliant key provider to generate a new Customer Master Key
   );
   ```

   Generate your Data Encryption Key

   Generate your Data Encryption Key using the variables declared in [step one](/docs/manual/core/csfle/tutorials/kmip/kmip-automatic#std-label-csfle-kmip-create-index) of this tutorial.

   ```csharp
   var clientEncryptionOptions = new ClientEncryptionOptions(
       keyVaultClient: keyVaultClient,
       keyVaultNamespace: keyVaultNamespace,
       kmsProviders: kmsProviderCredentials,
       tlsOptions: tlsOptions
       );

   var clientEncryption = new ClientEncryption(clientEncryptionOptions);
   var dataKeyId = clientEncryption.CreateDataKey(provider, dataKeyOptions, CancellationToken.None);
   var dataKeyIdBase64 = Convert.ToBase64String(GuidConverter.ToBytes(dataKeyId, GuidRepresentation.Standard));
   Console.WriteLine($"DataKeyId [base64]: {dataKeyIdBase64}");
   ```

   **See also: Complete Code**

   To view the complete code for making a Data Encryption Key, see [our Github repository.](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/dotnet/kmip/reader/CSFLE/MakeDataKey.cs)

3. Configure the MongoClient

   **Tip:**

   Follow the remaining steps in this tutorial in a separate file from the one created in the previous steps.

   To view the complete code for this file, see [our Github repository](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/dotnet/kmip/reader/CSFLE/InsertEncryptedDocument.cs)

   Specify the Key Vault Collection Namespace

   Specify `encryption.__keyVault` as the Key Vault collection namespace.

   ```csharp
   var keyVaultNamespace = CollectionNamespace.FromFullName("encryption.__keyVault");
   ```

   Specify your KMIP Endpoint

   Specify `kmip` in your `kmsProviders` object and enter the URI endpoint of your KMIP (Key Management Interoperability Protocol)-compliant key provider:

   ```csharp
   var kmsProviders = new Dictionary<string, IReadOnlyDictionary<string, object>>();
   var provider = "kmip";
   var kmipKmsOptions = new Dictionary<string, object>
   {
      { "endpoint", "<endpoint for your KMIP-compliant key provider>" },
   };
   kmsProviders.Add(provider, kmipKmsOptions);
   ```

   Create an Encryption Schema For Your Collection

   Create an encryption schema that specifies how your client application encrypts your documents' fields:

   **Tip: Add Your Data Encryption Key Base64 ID**

   Make sure to update the following code to include your Base64 DEK (Data Encryption Key) ID. You received this value in the [Generate your Data Encryption Key](/docs/manual/core/csfle/tutorials/kmip/kmip-automatic#std-label-csfle-kmip-create-dek) step of this guide.

   ```csharp
   var keyId = "<Your base64 DEK ID here>";
   var schema = new BsonDocument
   {
      { "bsonType", "object" },
      {
          "encryptMetadata",
          new BsonDocument("keyId", new BsonArray(new[] { new BsonBinaryData(Convert.FromBase64String(keyId), BsonBinarySubType.UuidStandard) }))
      },
      {
          "properties",
          new BsonDocument
          {
              {
                  "ssn", new BsonDocument
                  {
                      {
                          "encrypt", new BsonDocument
                          {
                              { "bsonType", "int" },
                              { "algorithm", "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic" }
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
                              { "algorithm", "AEAD_AES_256_CBC_HMAC_SHA_512-Random" }
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
                              { "algorithm", "AEAD_AES_256_CBC_HMAC_SHA_512-Random" }
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
                                              { "algorithm", "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic" }
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
   var schemaMap = new Dictionary<string, BsonDocument>();
   schemaMap.Add(dbNamespace, schema);
   ```

   **Tip: Further Reading on Schemas**

   To view an in-depth description of how to construct the schema you use in this step, see the [Encryption Schemas](/docs/manual/core/csfle/fundamentals/create-schema#std-label-csfle-fundamentals-create-schema) guide.

   To view a list of all supported encryption rules for your encryption schemas, see the [CSFLE Encryption Schemas](/docs/manual/core/csfle/reference/encryption-schemas#std-label-csfle-reference-encryption-schemas) guide.

   Specify the Location of the Automatic Encryption Shared Library

   ```csharp
   var mongoBinariesPath = "<Full path to your Automatic Encryption Shared Library>";
   var extraOptions = new Dictionary<string, object>()
   {
      { "cryptSharedLibPath", mongoBinariesPath },
   };
   ```

   **Note: Automatic Encryption Options**

   The automatic encryption options provide configuration information to the Automatic Encryption Shared Library, which modifies the application's behavior when accessing encrypted fields.

   To learn more about the Automatic Encryption Shared Library, see the [Install and Configure a CSFLE Query Analysis Component](/docs/manual/core/csfle/reference/install-library#std-label-csfle-reference-shared-library) page.

   Create the MongoClient

   Instantiate a MongoDB client object with the following automatic encryption settings that use the variables declared in the previous steps:

   ### .NET/C# Driver v3.0+

   ```csharp
   MongoClientSettings.Extensions.AddAutoEncryption(); // .NET/C# Driver v3.0 or later only
   var clientSettings = MongoClientSettings.FromConnectionString(connectionString);
   var autoEncryptionOptions = new AutoEncryptionOptions(
       keyVaultNamespace: keyVaultNamespace,
       kmsProviders: kmsProviders,
       schemaMap: schemaMap,
       extraOptions: extraOptions,
       tlsOptions: tlsOptions
       );
   clientSettings.AutoEncryptionOptions = autoEncryptionOptions;
   var secureClient = new MongoClient(clientSettings);
   ```

4. Insert a Document with Encrypted Fields

   Use your CSFLE-enabled `MongoClient` instance to insert a document with encrypted fields into the `medicalRecords.patients` namespace using the following code snippet:

   ```csharp
   var sampleDocFields = new BsonDocument
   {
       { "name", "Jon Doe" },
       { "ssn", 145014000 },
       { "bloodType", "AB-" },
       {
           "medicalRecords", new BsonArray
           {
               new BsonDocument("weight", 180),
               new BsonDocument("bloodPressure", "120/80")
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

   // Construct an auto-encrypting client
   var secureCollection = secureClient.GetDatabase(db).GetCollection<BsonDocument>(coll);

   // Insert a document into the collection
   secureCollection.InsertOne(sampleDocFields);
   ```

   When you insert a document, your CSFLE-enabled client encrypts the fields of your document such that it resembles the following:

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

   **See also: Complete Code**

   To view the complete code for inserting a document with encrypted fields, see [our Github repository](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/dotnet/kmip/reader/CSFLE/InsertEncryptedDocument.cs)

5. Retrieve Your Document with Encrypted Fields

   Retrieve the document with encrypted fields you inserted in the [Insert a Document with Encrypted Fields](/docs/manual/core/csfle/tutorials/kmip/kmip-automatic#std-label-csfle-kmip-insert) step of this guide.

   To show the functionality of CSFLE, the following code snippet queries for your document with a client configured for automatic CSFLE as well as a client that is not configured for automatic CSFLE.

   ```csharp
   Console.WriteLine("Finding a document with regular (non-encrypted) client.");
   var filter = Builders<BsonDocument>.Filter.Eq("name", "Jon Doe");
   var regularResult = regularCollection.Find(filter).Limit(1).ToList()[0];
   Console.WriteLine($"\n{regularResult}\n");

   Console.WriteLine("Finding a document with encrypted client");
   var ssnFilter = Builders<BsonDocument>.Filter.Eq("name", "Jon Doe");
   var secureResult = secureCollection.Find(ssnFilter).Limit(1).First();
   Console.WriteLine($"\n{secureResult}\n");
   ```

   The output of the preceding code snippet should look like this:

   ```json
   Finding a document with regular (non-encrypted) client.

   {
     _id: new ObjectId("629a452e0861b3130887103a"),
     name: 'Jon Doe',
     ssn: new Binary(Buffer.from("0217482732d8014cdd9ffdd6e2966e5e7910c20697e5f4fa95710aafc9153f0a3dc769c8a132a604b468732ff1f4d8349ded3244b59cbfb41444a210f28b21ea1b6c737508d9d30e8baa30c1d8070c4d5e26", "hex"), 6),
     bloodType: new Binary(Buffer.from("0217482732d8014cdd9ffdd6e2966e5e79022e238536dfd8caadb4d7751ac940e0f195addd7e5c67b61022d02faa90283ab69e02303c7e4001d1996128428bf037dea8bbf59fbb20c583cbcff2bf3e2519b4", "hex"), 6),
     'key-id': 'demo-data-key',
     medicalRecords: new Binary(Buffer.from("0217482732d8014cdd9ffdd6e2966e5e790405163a3207cff175455106f57eef14e5610c49a99bcbd14a7db9c5284e45e3ee30c149354015f941440bf54725d6492fb3b8704bc7c411cff6c868e4e13c58233c3d5ed9593eca4e4d027d76d3705b6d1f3b3c9e2ceee195fd944b553eb27eee69e5e67c338f146f8445995664980bf0", "hex"), 6),
     insurance: {
       policyNumber: new Binary(Buffer.from("0217482732d8014cdd9ffdd6e2966e5e79108decd85c05be3fec099e015f9d26d9234605dc959cc1a19b63072f7ffda99db38c7b487de0572a03b2139ac3ee163bcc40c8508f366ce92a5dd36e38b3c742f7", "hex"), 6),
       provider: 'MaestCare'
     }
   }

   Finding a document with encrypted client

   {
     _id: new ObjectId("629a452e0861b3130887103a"),
     name: 'Jon Doe',
     ssn: 241014209,
     bloodType: 'AB+',
     'key-id': 'demo-data-key',
     medicalRecords: [ { weight: 180, bloodPressure: '120/80' } ],
     insurance: { policyNumber: 123142, provider: 'MaestCare' }
   }

   ```

   **See also: Complete Code**

   To view the complete code for inserting a document with encrypted fields, see [our Github repository.](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/python/kmip/reader/insert_encrypted_document.py)

**Important:**

When building or running the Golang code in this guide using `go build` or `go run`, always include the `cse` build constraint to enable CSFLE. See the following shell command for an example of including the build constraint:

```bash
go run -tags cse insert-encrypted-document.go
```

1. Configure your KMIP-compliant key provider

   To connect a MongoDB driver client to your KMIP (Key Management Interoperability Protocol)-compliant key provider, you must configure your KMIP (Key Management Interoperability Protocol)-compliant key provider such that it accepts your client's TLS certificate.

   Consult the documentation for your KMIP (Key Management Interoperability Protocol)-compliant key provider for information on how to accept your client certificate.

2. Specify your Certificates

   ```go
   tlsConfig := make(map[string]*tls.Config)
   tlsOpts := map[string]interface{}{
   	"tlsCertificateKeyFile": "<path to your client certificate file>",
   	"tlsCAFile":             "<path to file containing your Certificate Authority certificate>",
   }
   kmipConfig, err := options.BuildTLSConfig(tlsOpts)
   tlsConfig["kmip"] = kmipConfig
   ```

   **Important:**

   You must use certificates with [ECDSA keys](https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm) when using the Go driver.

#### Create the Application

1. Create a Unique Index on Your Key Vault Collection

   Create a unique index on the `keyAltNames` field in your `encryption.__keyVault` namespace.

   Select the tab corresponding to your preferred MongoDB driver:

   ```go
   uri := "<Your MongoDB URI>"
   keyVaultClient, err := mongo.Connect(options.Client().ApplyURI(uri))
   if err != nil {
   	return fmt.Errorf("Connect error for regular client: %v", err)
   }
   defer func() {
   	_ = keyVaultClient.Disconnect(context.TODO())
   }()

   keyVaultColl := "__keyVault"
   keyVaultDb := "encryption"
   keyVaultNamespace := keyVaultDb + "." + keyVaultColl
   keyVaultIndex := mongo.IndexModel{
   	Keys: bson.D{{"keyAltNames", 1}},
   	Options: options.Index().
   		SetUnique(true).
   		SetPartialFilterExpression(bson.D{
   			{"keyAltNames", bson.D{
   				{"$exists", true},
   			}},
   		}),
   }
   // Drop the Key Vault Collection in case you created this collection
   // in a previous run of this application.
   if err = keyVaultClient.Database(keyVaultDb).Collection(keyVaultColl).Drop(context.TODO()); err != nil {
   	log.Fatalf("Collection.Drop error: %v", err)
   }
   // Drop the database storing your encrypted fields as all
   // the DEKs encrypting those fields were deleted in the preceding line.
   if err = keyVaultClient.Database("medicalRecords").Collection("patients").Drop(context.TODO()); err != nil {
   	log.Fatalf("Collection.Drop error: %v", err)
   }
   _, err = keyVaultClient.Database(keyVaultDb).Collection(keyVaultColl).Indexes().CreateOne(context.TODO(), keyVaultIndex)
   if err != nil {
   	panic(err)
   }
   ```

2. Create a Data Encryption Key

   Add your Endpoint

   Specify the URI endpoint of your KMIP (Key Management Interoperability Protocol)-compliant key provider:

   ```go
   provider := "kmip"
   kmsProviders := map[string]map[string]interface{}{
   	provider: {
   		"endpoint": "<endpoint for your KMIP-compliant key provider>",
   	},
   }
   ```

   Add Your Key Information

   The following code prompts your KMIP (Key Management Interoperability Protocol)-compliant key provider to automatically generate a Customer Master Key:

   ```go
   masterKey := map[string]interface{}{} // an empty key object prompts your KMIP-compliant key provider to generate a new Customer Master Key
   ```

   Generate your Data Encryption Key

   Generate your Data Encryption Key using the variables declared in [step one](/docs/manual/core/csfle/tutorials/kmip/kmip-automatic#std-label-csfle-kmip-create-index) of this tutorial.

   ```go
   clientEncryptionOpts := options.ClientEncryption().SetKeyVaultNamespace(keyVaultNamespace).
   	SetKmsProviders(kmsProviders).SetTLSConfig(tlsConfig)
   clientEnc, err := mongo.NewClientEncryption(keyVaultClient, clientEncryptionOpts)
   if err != nil {
   	return fmt.Errorf("NewClientEncryption error %v", err)
   }
   defer func() {
   	_ = clientEnc.Close(context.TODO())
   }()
   dataKeyOpts := options.DataKey().
   	SetMasterKey(masterKey)

   dataKeyID, err := clientEnc.CreateDataKey(context.TODO(), provider, dataKeyOpts)
   if err != nil {
   	return fmt.Errorf("create data key error %v", err)
   }

   fmt.Printf("DataKeyId [base64]: %s\n", base64.StdEncoding.EncodeToString(dataKeyID.Data))
   ```

   **See also: Complete Code**

   To view the complete code for making a Data Encryption Key, see [our Github repository.](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/go/kmip/reader/make-data-key.go)

3. Configure the MongoClient

   **Tip:**

   Follow the remaining steps in this tutorial in a separate file from the one created in the previous steps.

   To view the complete code for this file, see [our Github repository.](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/go/kmip/reader/insert-encrypted-document.go)

   Specify the Key Vault Collection Namespace

   Specify `encryption.__keyVault` as the Key Vault collection namespace.

   ```go
   keyVaultNamespace := "encryption.__keyVault"
   ```

   Specify your KMIP Endpoint

   Specify `kmip` in your `kmsProviders` object and enter the URI endpoint of your KMIP (Key Management Interoperability Protocol)-compliant key provider:

   ```go
   provider := "kmip"
   kmsProviders := map[string]map[string]interface{}{
   	provider: {
   		"endpoint": "<endpoint for your KMIP-compliant key provider>",
   	},
   }
   ```

   Create an Encryption Schema For Your Collection

   Create an encryption schema that specifies how your client application encrypts your documents' fields:

   **Tip: Add Your Data Encryption Key Base64 ID**

   Make sure to update the following code to include your Base64 DEK (Data Encryption Key) ID. You received this value in the [Generate your Data Encryption Key](/docs/manual/core/csfle/tutorials/kmip/kmip-automatic#std-label-csfle-kmip-create-dek) step of this guide.

   ```go
   dek_id := "<Your Base64 DEK ID>"
   schema_template := `{
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
   schema := fmt.Sprintf(schema_template, dek_id)
   var schemaDoc bson.Raw
   if err := bson.UnmarshalExtJSON([]byte(schema), true, &schemaDoc); err != nil {
   	return fmt.Errorf("UnmarshalExtJSON error: %v", err)
   }
   schemaMap := map[string]interface{}{
   	dbName + "." + collName: schemaDoc,
   }
   ```

   **Tip: Further Reading on Schemas**

   To view an in-depth description of how to construct the schema you use in this step, see the [Encryption Schemas](/docs/manual/core/csfle/fundamentals/create-schema#std-label-csfle-fundamentals-create-schema) guide.

   To view a list of all supported encryption rules for your encryption schemas, see the [CSFLE Encryption Schemas](/docs/manual/core/csfle/reference/encryption-schemas#std-label-csfle-reference-encryption-schemas) guide.

   Specify the Location of the Automatic Encryption Shared Library

   ```go
   extraOptions := map[string]interface{}{
   	"cryptSharedLibPath": "<Full path to your Automatic Encryption Shared Library>",
   }
   ```

   **Note: Automatic Encryption Options**

   The automatic encryption options provide configuration information to the Automatic Encryption Shared Library, which modifies the application's behavior when accessing encrypted fields.

   To learn more about the Automatic Encryption Shared Library, see the [Install and Configure a CSFLE Query Analysis Component](/docs/manual/core/csfle/reference/install-library#std-label-csfle-reference-shared-library) page.

   Create the MongoClient

   Instantiate a MongoDB client object with the following automatic encryption settings that use the variables declared in the previous steps:

   ```go
   autoEncryptionOpts := options.AutoEncryption().
   	SetKmsProviders(kmsProviders).
   	SetKeyVaultNamespace(keyVaultNamespace).
   	SetSchemaMap(schemaMap).
   	SetExtraOptions(extraOptions).SetTLSConfig(tlsConfig)
   secureClient, err := mongo.Connect(context.TODO(), options.Client().ApplyURI(uri).SetAutoEncryptionOptions(autoEncryptionOpts))
   if err != nil {
   	return fmt.Errorf("Connect error for encrypted client: %v", err)
   }
   defer func() {
   	_ = secureClient.Disconnect(context.TODO())
   }()
   ```

4. Insert a Document with Encrypted Fields

   Use your CSFLE-enabled `MongoClient` instance to insert a document with encrypted fields into the `medicalRecords.patients` namespace using the following code snippet:

   ```go
   test_patient := map[string]interface{}{
   	"name":      "Jon Doe",
   	"ssn":       241014209,
   	"bloodType": "AB+",
   	"medicalRecords": []map[string]interface{}{{
   		"weight":        180,
   		"bloodPressure": "120/80",
   	}},
   	"insurance": map[string]interface{}{
   		"provider":     "MaestCare",
   		"policyNumber": 123142,
   	},
   }
   if _, err := secureClient.Database(dbName).Collection(collName).InsertOne(context.TODO(), test_patient); err != nil {
   	return fmt.Errorf("InsertOne error: %v", err)
   }
   ```

   **Note:**

   Rather than creating a raw BSON document, you can pass a struct with `bson` tags directly to the driver for encoding.

   When you insert a document, your CSFLE-enabled client encrypts the fields of your document such that it resembles the following:

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

   **See also: Complete Code**

   To view the complete code for inserting a document with encrypted fields, see [our Github repository.](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/go/kmip/reader/insert-encrypted-document.go)

5. Retrieve Your Document with Encrypted Fields

   Retrieve the document with encrypted fields you inserted in the [Insert a Document with Encrypted Fields](/docs/manual/core/csfle/tutorials/kmip/kmip-automatic#std-label-csfle-kmip-insert) step of this guide.

   To show the functionality of CSFLE, the following code snippet queries for your document with a client configured for automatic CSFLE as well as a client that is not configured for automatic CSFLE.

   ```go
   fmt.Println("Finding a document with regular (non-encrypted) client.")
   var resultRegular bson.M
   err = regularClient.Database(dbName).Collection(collName).FindOne(context.TODO(), bson.D{{"name", "Jon Doe"}}).Decode(&resultRegular)
   if err != nil {
   	panic(err)
   }
   outputRegular, err := json.MarshalIndent(resultRegular, "", "    ")
   if err != nil {
   	panic(err)
   }
   fmt.Printf("%s\n", outputRegular)

   fmt.Println("Finding a document with encrypted client")
   var resultSecure bson.M
   err = secureClient.Database(dbName).Collection(collName).FindOne(context.TODO(), bson.D{{"name", "Jon Doe"}}).Decode(&resultSecure)
   if err != nil {
   	panic(err)
   }
   outputSecure, err := json.MarshalIndent(resultSecure, "", "    ")
   if err != nil {
   	panic(err)
   }
   fmt.Printf("%s\n", outputSecure)
   ```

   The output of the preceding code snippet should look like this:

   ```json
   Finding a document with regular (non-encrypted) client.

   {
     _id: new ObjectId("629a452e0861b3130887103a"),
     name: 'Jon Doe',
     ssn: new Binary(Buffer.from("0217482732d8014cdd9ffdd6e2966e5e7910c20697e5f4fa95710aafc9153f0a3dc769c8a132a604b468732ff1f4d8349ded3244b59cbfb41444a210f28b21ea1b6c737508d9d30e8baa30c1d8070c4d5e26", "hex"), 6),
     bloodType: new Binary(Buffer.from("0217482732d8014cdd9ffdd6e2966e5e79022e238536dfd8caadb4d7751ac940e0f195addd7e5c67b61022d02faa90283ab69e02303c7e4001d1996128428bf037dea8bbf59fbb20c583cbcff2bf3e2519b4", "hex"), 6),
     'key-id': 'demo-data-key',
     medicalRecords: new Binary(Buffer.from("0217482732d8014cdd9ffdd6e2966e5e790405163a3207cff175455106f57eef14e5610c49a99bcbd14a7db9c5284e45e3ee30c149354015f941440bf54725d6492fb3b8704bc7c411cff6c868e4e13c58233c3d5ed9593eca4e4d027d76d3705b6d1f3b3c9e2ceee195fd944b553eb27eee69e5e67c338f146f8445995664980bf0", "hex"), 6),
     insurance: {
       policyNumber: new Binary(Buffer.from("0217482732d8014cdd9ffdd6e2966e5e79108decd85c05be3fec099e015f9d26d9234605dc959cc1a19b63072f7ffda99db38c7b487de0572a03b2139ac3ee163bcc40c8508f366ce92a5dd36e38b3c742f7", "hex"), 6),
       provider: 'MaestCare'
     }
   }

   Finding a document with encrypted client

   {
     _id: new ObjectId("629a452e0861b3130887103a"),
     name: 'Jon Doe',
     ssn: 241014209,
     bloodType: 'AB+',
     'key-id': 'demo-data-key',
     medicalRecords: [ { weight: 180, bloodPressure: '120/80' } ],
     insurance: { policyNumber: 123142, provider: 'MaestCare' }
   }

   ```

   **See also: Complete Code**

   To view the complete code for inserting a document with encrypted fields, see [our Github repository.](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/go/kmip/reader/insert-encrypted-document.go)

## Learn More

To learn how CSFLE works, see [CSFLE Fundamentals.](/docs/manual/core/csfle/fundamentals#std-label-csfle-fundamentals)

To learn more about the topics mentioned in this guide, see the following links:

- Learn more about CSFLE components on the [Reference](/docs/manual/core/csfle/reference#std-label-csfle-reference) page.

- Learn how Customer Master Keys and Data Encryption Keys work on the [Encryption Keys and Key Vaults](/docs/manual/core/queryable-encryption/fundamentals/keys-key-vaults#std-label-qe-reference-keys-key-vaults) page.

- See how KMS Providers manage your CSFLE keys on the [KMS Providers](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-fundamentals-kms-providers) page.
