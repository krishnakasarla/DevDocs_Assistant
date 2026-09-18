> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

<!--
Tab options on this page. Append to the .md URL to filter:
  ?tabs=<id,...>   select specific tabs (e.g. ?tabs=nodejs,shell)
  ?allTabs=true    include every tab
  (no param)       default: one tab per tabset

Available tabs:
  other tabs: csharp-v3, csharp-v2
-->

# Use Automatic Client-Side Field Level Encryption with Azure

## Overview

This guide shows you how to build a Client-Side Field Level Encryption (CSFLE)-enabled application using Azure Key Vault.

After you complete the steps in this guide, you should have:

- A Customer Master Key hosted on an Azure Key Vault instance.

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

Select the programming language for which you want to see code examples for from the Select your language dropdown menu on the right side of the page.

### Full Application Code

To see the complete code for the sample application, select your programming language in the language selector.

[Complete Java Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/java/azure/reader/)

[Complete Node.js Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/node/azure/reader/)

[Complete Python Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/python/azure/reader/)

[Complete C# Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/dotnet/azure/reader/CSFLE/)

[Complete Go Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/go/azure/reader/)

## Set Up the KMS

1. Register your Application with Azure

   Log in to [Azure.](https://azure.microsoft.com/en-us/features/azure-portal/)

   Register your Application with Azure Active Directory

   To register an application on Azure Active Directory, follow Microsoft's official [Register an application with the Microsoft identity platform](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app) Quick Start.

   **Important: Record your Credentials**

   Ensure you record the following credentials:

   - **Tenant ID**

   - **Client ID**

   - **Client secret**

   You need these credentials to construct your `kmsProviders` object later in this tutorial. You can also authenticate by using an access token or automatic credential fetching. To learn about all available credential forms for Azure, see [kmsProviders Object.](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-kms-provider-object-azure)

2. Create the Customer Master Key

   Create your Azure Key Vault and Customer Master Key

   To create a new Azure Key Vault instance and Customer Master Key, follow Microsoft's official [Set and retrieve a key from Azure Key Vault using the Azure portal](https://docs.microsoft.com/en-us/azure/key-vault/keys/quick-create-portal) Quick Start.

   **Note:**

   The Customer Master Key should have an RSA key size of 2048 or 4096 bits.

   **Important: Record your Credentials**

   Ensure you record the following credentials:

   - **Key Name**

   - **Key Identifier** (referred to as `keyVaultEndpoint` later in this guide)

   - **Key Version**

   You will need them to construct your `dataKeyOpts` object later in this tutorial.

   Grant Permissions

## Create the Application

1. Create a Unique Index on your Key Vault collection

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

2. Create a New Data Encryption Key

   Add your Azure Key Vault Credentials

   Add the service account credentials to your CSFLE-enabled client code.

   ```java
   String kmsProvider = "azure";
   Map<String, Map<String, Object>> kmsProviderDetails = new HashMap<String, Map<String, Object>>();
   Map<String, Object> providerDetails = new HashMap<>();
   providerDetails.put("tenantId", "<Azure account organization>");
   providerDetails.put("clientId", "<Azure client ID>");
   providerDetails.put("clientSecret", "<Azure client secret>");
   kmsProviderDetails.put(kmsProvider, providerDetails);
   ```

   You can also provide a custom name for your KMS provider by passing in a string that includes the name of the KMS provider, followed by a colon and the custom name. Providing a unique name for a KMS provider allows you to specify multiple KMS providers of the same type.

   For example, you can name your Azure KMS provider "my\_azure\_provider" in your KMS credentials variable as shown in the following code:

   ```java
   Map<String, Object> kmsProviderDetails = new HashMap<>();
   kmsProviderDetails.put("tenantId", getEnv("AZURE_TENANT_ID")); // Your Azure tenant ID
   kmsProviderDetails.put("clientId", getEnv("AZURE_CLIENT_ID")); // Your Azure client ID
   kmsProviderDetails.put("clientSecret", getEnv("AZURE_CLIENT_SECRET")); // Your Azure client secret

   Map<String, Map<String, Object>> kmsProviderCredentials = new HashMap<String, Map<String, Object>>();
   kmsProviderCredentials.put("azure:my_azure_provider", kmsProviderDetails);
   ```

   **Tip: Azure Virtual Machine Managed Identities**

   If your client runs on an Azure Virtual Machine (VM), you can allow the VM to use its Managed Identity to authenticate to your key vault.

   To allow the Azure VM to automatically provide your credentials, assign an empty map instead of one that contains your Azure credentials as shown in the following code:

   ```java
   String kmsProvider = "azure";
   Map<String, Map<String, Object>> kmsProviders = new HashMap<String, Map<String, Object>>();
   Map<String, Object> providerDetails = new HashMap<>();
   kmsProviders.put(kmsProvider, providerDetails);
   ```

   Add Your Key Information

   Update the following code to specify your Customer Master Key:

   **Tip:**

   You recorded your Customer Master Key's ARN (Amazon Resource Name) and Region in the [Create a Customer Master Key](/docs/manual/core/csfle/tutorials/azure/azure-automatic#std-label-aws-create-master-key) step of this guide.

   ```java
   BsonDocument masterKeyProperties = new BsonDocument();
   masterKeyProperties.put("provider", new BsonString(kmsProvider));
   masterKeyProperties.put("keyName", new BsonString("<Azure key name>"));
   masterKeyProperties.put("keyVaultEndpoint", new BsonString("<Azure key vault endpoint"));
   ```

   Generate your Data Encryption Key

   Generate your Data Encryption Key using the variables declared in [step one](/docs/manual/core/csfle/tutorials/azure/azure-automatic#std-label-csfle-azure-create-index) of this tutorial.

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

   **Tip: Learn More**

   To view a diagram showing how your client application creates your Data Encryption Key when using an Azure Key Vault, see [Architecture.](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-fundamentals-kms-providers-azure-architecture)

   To learn more about the options for creating a Data Encryption Key encrypted with a Customer Master Key hosted in Azure Key Vault, see [kmsProviders Object](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-kms-provider-object-azure) and [dataKeyOpts Object.](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-kms-datakeyopts-azure)

   **See also: Complete Code**

   To view the complete code for making a Data Encryption Key, see [our Github repository.](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/java/azure/reader/src/main/java/com/mongodb/csfle/MakeDataKey.java)

3. Configure the MongoClient

   **Tip:**

   Follow the remaining steps in this tutorial in a separate file from the one created in the previous steps.

   To view the complete code for this file, see [our Github repository.](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/java/azure/reader/src/main/java/com/mongodb/csfle/InsertEncryptedDocument.java)

   Specify the Key Vault Collection Namespace

   Specify `encryption.__keyVault` as the Key Vault collection namespace.

   ```java
   String keyVaultNamespace = "encryption.__keyVault";
   ```

   Specify your Azure Credentials

   Specify the `azure` KMS provider and your Azure credentials:

   ```java
   String kmsProvider = "azure";
   Map<String, Map<String, Object>> kmsProviders = new HashMap<String, Map<String, Object>>();
   Map<String, Object> providerDetails = new HashMap<>();
   providerDetails.put("tenantId", "<Azure account organization>");
   providerDetails.put("clientId", "<Azure client ID>");
   providerDetails.put("clientSecret", "<Azure client secret>");
   kmsProviders.put(kmsProvider, providerDetails);
   ```

   **Tip: Azure Virtual Machine Managed Identities**

   If your client runs on an Azure Virtual Machine (VM), you can allow the VM to use its Managed Identity to authenticate to your key vault.

   To allow the Azure VM to automatically provide your credentials, assign an empty map instead of one that contains your Azure credentials as shown in the following code:

   ```java
   String kmsProvider = "azure";
   Map<String, Map<String, Object>> kmsProviders = new HashMap<String, Map<String, Object>>();
   Map<String, Object> providerDetails = new HashMap<>();
   kmsProviders.put(kmsProvider, providerDetails);
   ```

   Create an Encryption Schema For Your Collection

   **Tip: Add Your Data Encryption Key Base64 ID**

   Make sure to update the following code to include your Base64 DEK (Data Encryption Key) ID. You received this value in the [Generate your Data Encryption Key](/docs/manual/core/csfle/tutorials/azure/azure-automatic#std-label-csfle-azure-create-dek) step of this guide.

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

   To view the complete code for inserting a document with encrypted fields, see [our Github repository.](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/java/azure/reader/src/main/java/com/mongodb/csfle/InsertEncryptedDocument.java)

5. Retrieve Your Document with Encrypted Fields

   Retrieve the document with encrypted fields you inserted in the [Insert a Document with Encrypted Fields](/docs/manual/core/csfle/tutorials/azure/azure-automatic#std-label-csfle-azure-insert) step of this guide.

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

   To view the complete code for finding a document with encrypted fields, see [our Github repository.](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/java/azure/reader/src/main/java/com/mongodb/csfle/InsertEncryptedDocument.java)

1) Create a Unique Index on your Key Vault collection

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

2) Create a New Data Encryption Key

   Add your Azure Key Vault Credentials

   Add the service account credentials to your CSFLE-enabled client code.

   ```javascript
   const provider = "azure";
   const kmsProviderCredentials = {
     azure: {
       tenantId: "<Your Tenant ID>",
       clientId: "<Your Client ID>",
       clientSecret: "<Your Client Secret>",
     },
   };
   ```

   You can also provide a custom name for your KMS provider by passing in a string that includes the name of the KMS provider, followed by a colon and the custom name. Providing a unique name for a KMS provider allows you to specify multiple KMS providers of the same type.

   For example, you can name your Azure KMS provider "my\_azure\_provider" in your KMS credentials variable as shown in the following code:

   ```javascript
   kmsProviderCredentials = {
     "azure:my_azure_provider": {
       tenantId: process.env.AZURE_TENANT_ID, // Your Azure tenant ID
       clientId: process.env.AZURE_CLIENT_ID, // Your Azure client ID
       clientSecret: process.env.AZURE_CLIENT_SECRET, // Your Azure client secret
     },
   };

   ```

   Add Your Key Information

   Update the following code to specify your Customer Master Key:

   **Tip:**

   You recorded your Customer Master Key's ARN (Amazon Resource Name) and Region in the [Create a Customer Master Key](/docs/manual/core/csfle/tutorials/azure/azure-automatic#std-label-aws-create-master-key) step of this guide.

   ```javascript
   const masterKey = {
     keyVaultEndpoint: "<Your Key Vault Endpoint>",
     keyName: "<Your Key Name>",
   };
   ```

   Generate your Data Encryption Key

   Generate your Data Encryption Key using the variables declared in [step one](/docs/manual/core/csfle/tutorials/azure/azure-automatic#std-label-csfle-azure-create-index) of this tutorial.

   ```javascript
   const client = new MongoClient(uri);
   await client.connect();

   const encryption = new ClientEncryption(client, {
     keyVaultNamespace,
     kmsProviderCredentials,
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

   **Tip: Learn More**

   To view a diagram showing how your client application creates your Data Encryption Key when using an Azure Key Vault, see [Architecture.](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-fundamentals-kms-providers-azure-architecture)

   To learn more about the options for creating a Data Encryption Key encrypted with a Customer Master Key hosted in Azure Key Vault, see [kmsProviders Object](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-kms-provider-object-azure) and [dataKeyOpts Object.](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-kms-datakeyopts-azure)

   **See also: Complete Code**

   To view the complete code for making a Data Encryption Key, see [our Github repository.](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/node/azure/reader/make_data_key.js)

3) Configure the MongoClient

   **Tip:**

   Follow the remaining steps in this tutorial in a separate file from the one created in the previous steps.

   To view the complete code for this file, see [our Github repository.](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/node/azure/reader/insert_encrypted_document.js)

   Specify the Key Vault Collection Namespace

   Specify `encryption.__keyVault` as the Key Vault collection namespace.

   ```javascript
   const keyVaultNamespace = "encryption.__keyVault";
   ```

   Specify your Azure Credentials

   Specify the `azure` KMS provider and your Azure credentials:

   ```javascript
   const kmsProviders = {
     azure: {
       tenantId: "<Your Tenant ID>",
       clientId: "<Your Client ID>",
       clientSecret: "<Your Client Secret>",
     },
   };
   ```

   Create an Encryption Schema For Your Collection

   **Tip: Add Your Data Encryption Key Base64 ID**

   Make sure to update the following code to include your Base64 DEK (Data Encryption Key) ID. You received this value in the [Generate your Data Encryption Key](/docs/manual/core/csfle/tutorials/azure/azure-automatic#std-label-csfle-azure-create-dek) step of this guide.

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
     },
   });
   ```

4) Insert a Document with Encrypted Fields

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

   To view the complete code for inserting a document with encrypted fields, see [our Github repository.](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/node/azure/reader/insert_encrypted_document.js)

5) Retrieve Your Document with Encrypted Fields

   Retrieve the document with encrypted fields you inserted in the [Insert a Document with Encrypted Fields](/docs/manual/core/csfle/tutorials/azure/azure-automatic#std-label-csfle-azure-insert) step of this guide.

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

   To view the complete code for finding a document with encrypted fields, see [our Github repository.](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/node/azure/reader/insert_encrypted_document.js)

1. Create a Unique Index on your Key Vault collection

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

2. Create a New Data Encryption Key

   Add your Azure Key Vault Credentials

   Add the service account credentials to your CSFLE-enabled client code.

   ```python
   provider = "azure"
   kms_provider_credentials = {
       provider: {
           "tenantId": "<Azure account organization>",
           "clientId": "<Azure client ID>",
           "clientSecret": "<Azure client secret>",
       }
   }
   ```

   You can also provide a custom name for your KMS provider by passing in a string that includes the name of the KMS provider, followed by a colon and the custom name. Providing a unique name for a KMS provider allows you to specify multiple KMS providers of the same type.

   For example, you can name your Azure KMS provider "my\_azure\_provider" in your KMS credentials variable as shown in the following code:

   ```python
   kms_provider_credentials = {
       "azure:my_azure_provider": {
           "tenantId": os.environ['AZURE_TENANT_ID'], # Your Azure tenant ID
           "clientId": os.environ['AZURE_CLIENT_ID'], # Your Azure client ID
           "clientSecret": os.environ['AZURE_CLIENT_SECRET'] # Your Azure client secret
       }
   }
   ```

   Add Your Key Information

   Update the following code to specify your Customer Master Key:

   **Tip:**

   You recorded your Customer Master Key's ARN (Amazon Resource Name) and Region in the [Create a Customer Master Key](/docs/manual/core/csfle/tutorials/azure/azure-automatic#std-label-aws-create-master-key) step of this guide.

   ```python
   master_key = {
       "keyName": "<Azure key name>",
       "keyVersion": "<Azure key version>",
       "keyVaultEndpoint": "<Azure key vault endpoint/key identifier>",
   }
   ```

   Generate your Data Encryption Key

   Generate your Data Encryption Key using the variables declared in [step one](/docs/manual/core/csfle/tutorials/azure/azure-automatic#std-label-csfle-azure-create-index) of this tutorial.

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
   )
   data_key_id = client_encryption.create_data_key(provider, master_key)

   base_64_data_key_id = base64.b64encode(data_key_id)
   print("DataKeyId [base64]: ", base_64_data_key_id)
   ```

   **Tip: Learn More**

   To view a diagram showing how your client application creates your Data Encryption Key when using an Azure Key Vault, see [Architecture.](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-fundamentals-kms-providers-azure-architecture)

   To learn more about the options for creating a Data Encryption Key encrypted with a Customer Master Key hosted in Azure Key Vault, see [kmsProviders Object](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-kms-provider-object-azure) and [dataKeyOpts Object.](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-kms-datakeyopts-azure)

   **See also: Complete Code**

   To view the complete code for making a Data Encryption Key, see [our Github repository.](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/python/azure/reader/make_data_key.py)

3. Configure the MongoClient

   **Tip:**

   Follow the remaining steps in this tutorial in a separate file from the one created in the previous steps.

   To view the complete code for this file, see [our Github repository.](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/python/azure/reader/insert_encrypted_document.py)

   Specify the Key Vault Collection Namespace

   Specify `encryption.__keyVault` as the Key Vault collection namespace.

   ```python
   key_vault_namespace = "encryption.__keyVault"
   ```

   Specify your Azure Credentials

   Specify the `azure` KMS provider and your Azure credentials:

   ```python
   provider = "azure"
   kms_providers = {
       "azure": {
           "tenantId": "<Azure account organization>",
           "clientId": "<Azure client ID>",
           "clientSecret": "<Azure client secret>",
       }
   }
   ```

   Create an Encryption Schema For Your Collection

   **Tip: Add Your Data Encryption Key Base64 ID**

   Make sure to update the following code to include your Base64 DEK (Data Encryption Key) ID. You received this value in the [Generate your Data Encryption Key](/docs/manual/core/csfle/tutorials/azure/azure-automatic#std-label-csfle-azure-create-dek) step of this guide.

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
       kms_providers, key_vault_namespace, schema_map=patient_schema, **extra_options
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

   To view the complete code for inserting a document with encrypted fields, see [our Github repository.](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/python/azure/reader/insert_encrypted_document.py)

5. Retrieve Your Document with Encrypted Fields

   Retrieve the document with encrypted fields you inserted in the [Insert a Document with Encrypted Fields](/docs/manual/core/csfle/tutorials/azure/azure-automatic#std-label-csfle-azure-insert) step of this guide.

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

   To view the complete code for finding a document with encrypted fields, see [our Github repository.](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/python/azure/reader/insert_encrypted_document.py)

1) Create a Unique Index on your Key Vault collection

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

2) Create a New Data Encryption Key

   Add your Azure Key Vault Credentials

   Add the service account credentials to your CSFLE-enabled client code.

   ```csharp
   var kmsProviderCredentials = new Dictionary<string, IReadOnlyDictionary<string, object>>();
   var provider = "azure";
   var azureKmsOptions = new Dictionary<string, object>
   {
      { "tenantId", "<Your Azure Tenant ID>" },
      { "clientId", "<Your Azure Client ID>" },
      { "clientSecret", "<Your Azure Client Secret>" },
   };
   ```

   You can also provide a custom name for your KMS provider by passing in a string that includes the name of the KMS provider, followed by a colon and the custom name. Providing a unique name for a KMS provider allows you to specify multiple KMS providers of the same type.

   For example, you can name your Azure KMS provider "my\_azure\_provider" in your KMS credentials variable as shown in the following code:

   ```csharp
   var kmsProviderCredentials = new Dictionary<string, IReadOnlyDictionary<string, object>>();
   var kmsOptions = new Dictionary<string, object>
   {
       { "tenantId", _appSettings["Azure:TenantId"] }, // Your Azure tenant ID
       { "clientId", _appSettings["Azure:ClientId"] }, // Your Azure client ID
       { "clientSecret", _appSettings["Azure:ClientSecret"] } // Your Azure client secret
   };
   kmsProviderCredentials.Add("azure:my_azure_provider", kmsOptions);
   ```

   Add Your Key Information

   Update the following code to specify your Customer Master Key:

   **Tip:**

   You recorded your Customer Master Key's ARN (Amazon Resource Name) and Region in the [Create a Customer Master Key](/docs/manual/core/csfle/tutorials/azure/azure-automatic#std-label-aws-create-master-key) step of this guide.

   ```csharp
   kmsProviderCredentials.Add(provider, azureKmsOptions);
   var dataKeyOptions = new DataKeyOptions(
   masterKey: new BsonDocument
   {
      { "keyName", "<Your Azure Key Name>" },
      { "keyVaultEndpoint", "<Your Azure Key Vault Endpoint>" },
   });
   ```

   Generate your Data Encryption Key

   Generate your Data Encryption Key using the variables declared in [step one](/docs/manual/core/csfle/tutorials/azure/azure-automatic#std-label-csfle-azure-create-index) of this tutorial.

   ```csharp
   var clientEncryptionOptions = new ClientEncryptionOptions(
       keyVaultClient: keyVaultClient,
       keyVaultNamespace: keyVaultNamespace,
       kmsProviders: kmsProviderCredentials
       );

   var clientEncryption = new ClientEncryption(clientEncryptionOptions);
   var dataKeyId = clientEncryption.CreateDataKey(provider, dataKeyOptions, CancellationToken.None);
   var dataKeyIdBase64 = Convert.ToBase64String(GuidConverter.ToBytes(dataKeyId, GuidRepresentation.Standard));
   Console.WriteLine($"DataKeyId [base64]: {dataKeyIdBase64}");
   ```

   **Tip: Learn More**

   To view a diagram showing how your client application creates your Data Encryption Key when using an Azure Key Vault, see [Architecture.](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-fundamentals-kms-providers-azure-architecture)

   To learn more about the options for creating a Data Encryption Key encrypted with a Customer Master Key hosted in Azure Key Vault, see [kmsProviders Object](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-kms-provider-object-azure) and [dataKeyOpts Object.](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-kms-datakeyopts-azure)

   **See also: Complete Code**

   To view the complete code for making a Data Encryption Key, see [our Github repository](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/dotnet/azure/reader/CSFLE/MakeDataKey.cs)

3) Configure the MongoClient

   **Tip:**

   Follow the remaining steps in this tutorial in a separate file from the one created in the previous steps.

   To view the complete code for this file, see [our Github repository](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/dotnet/azure/reader/CSFLE/InsertEncryptedDocument.cs)

   Specify the Key Vault Collection Namespace

   Specify `encryption.__keyVault` as the Key Vault collection namespace.

   ```csharp
   var keyVaultNamespace = CollectionNamespace.FromFullName("encryption.__keyVault");
   ```

   Specify your Azure Credentials

   Specify the `azure` KMS provider and your Azure credentials:

   ```csharp
   var kmsProviders = new Dictionary<string, IReadOnlyDictionary<string, object>>();
   var provider = "azure";
   var azureKmsOptions = new Dictionary<string, object>
   {
      { "tenantId", "<Your Azure Tenant ID>" },
      { "clientId", "<Your Azure Client ID>" },
      { "clientSecret", "<Your Azure Client Secret>" },
   };
   kmsProviders.Add(provider, azureKmsOptions);
   ```

   Create an Encryption Schema For Your Collection

   **Tip: Add Your Data Encryption Key Base64 ID**

   Make sure to update the following code to include your Base64 DEK (Data Encryption Key) ID. You received this value in the [Generate your Data Encryption Key](/docs/manual/core/csfle/tutorials/azure/azure-automatic#std-label-csfle-azure-create-dek) step of this guide.

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
       extraOptions: extraOptions
       );
   clientSettings.AutoEncryptionOptions = autoEncryptionOptions;
   var secureClient = new MongoClient(clientSettings);
   ```

4) Insert a Document with Encrypted Fields

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

   To view the complete code for inserting a document with encrypted fields, see [our Github repository](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/dotnet/azure/reader/CSFLE/InsertEncryptedDocument.cs)

5) Retrieve Your Document with Encrypted Fields

   Retrieve the document with encrypted fields you inserted in the [Insert a Document with Encrypted Fields](/docs/manual/core/csfle/tutorials/azure/azure-automatic#std-label-csfle-azure-insert) step of this guide.

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

   To view the complete code for finding a document with encrypted fields, see [our Github repository](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/dotnet/azure/reader/CSFLE/InsertEncryptedDocument.cs)

1. Create a Unique Index on your Key Vault collection

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

2. Create a New Data Encryption Key

   Add your Azure Key Vault Credentials

   Add the service account credentials to your CSFLE-enabled client code.

   ```go
   provider := "azure"
   kmsProviders := map[string]map[string]interface{}{
   	provider: {
   		"tenantId":     "<Your Azure Tenant ID>",
   		"clientId":     "<Your Azure Client ID>",
   		"clientSecret": "<Your Azure Client Secret>",
   	},
   }
   ```

   Add Your Key Information

   Update the following code to specify your Customer Master Key:

   **Tip:**

   You recorded your Customer Master Key's ARN (Amazon Resource Name) and Region in the [Create a Customer Master Key](/docs/manual/core/csfle/tutorials/azure/azure-automatic#std-label-aws-create-master-key) step of this guide.

   ```go
   masterKey := map[string]interface{}{
   	"keyVaultEndpoint": "<Your Azure Key Vault Endpoint>",
   	"keyName":          "<Your Azure Key Name>",
   }
   ```

   Generate your Data Encryption Key

   Generate your Data Encryption Key using the variables declared in [step one](/docs/manual/core/csfle/tutorials/azure/azure-automatic#std-label-csfle-azure-create-index) of this tutorial.

   ```go
   clientEncryptionOpts := options.ClientEncryption().SetKeyVaultNamespace(keyVaultNamespace).
   	SetKmsProviders(kmsProviders)
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

   **Tip: Learn More**

   To view a diagram showing how your client application creates your Data Encryption Key when using an Azure Key Vault, see [Architecture.](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-fundamentals-kms-providers-azure-architecture)

   To learn more about the options for creating a Data Encryption Key encrypted with a Customer Master Key hosted in Azure Key Vault, see [kmsProviders Object](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-kms-provider-object-azure) and [dataKeyOpts Object.](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-kms-datakeyopts-azure)

   **See also: Complete Code**

   To view the complete code for making a Data Encryption Key, see [our Github repository.](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/go/azure/reader/make-data-key.go)

3. Configure the MongoClient

   **Tip:**

   Follow the remaining steps in this tutorial in a separate file from the one created in the previous steps.

   To view the complete code for this file, see [our Github repository.](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/go/azure/reader/insert-encrypted-document.go)

   Specify the Key Vault Collection Namespace

   Specify `encryption.__keyVault` as the Key Vault collection namespace.

   ```go
   keyVaultNamespace := "encryption.__keyVault"
   ```

   Specify your Azure Credentials

   Specify the `azure` KMS provider and your Azure credentials:

   ```go
   kmsProviders := map[string]map[string]interface{}{
   	"azure": {
   		"tenantId":     "<Your Azure Tenant ID>",
   		"clientId":     "<Your Azure Client ID>",
   		"clientSecret": "<Your Azure Client Secret>",
   	},
   }
   ```

   Create an Encryption Schema For Your Collection

   **Tip: Add Your Data Encryption Key Base64 ID**

   Make sure to update the following code to include your Base64 DEK (Data Encryption Key) ID. You received this value in the [Generate your Data Encryption Key](/docs/manual/core/csfle/tutorials/azure/azure-automatic#std-label-csfle-azure-create-dek) step of this guide.

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
   	SetExtraOptions(extraOptions)
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

   To view the complete code for inserting a document with encrypted fields, see [our Github repository.](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/go/azure/reader/insert-encrypted-document.go)

5. Retrieve Your Document with Encrypted Fields

   Retrieve the document with encrypted fields you inserted in the [Insert a Document with Encrypted Fields](/docs/manual/core/csfle/tutorials/azure/azure-automatic#std-label-csfle-azure-insert) step of this guide.

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

   To view the complete code for finding a document with encrypted fields, see [our Github repository.](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/generated/in-use-encryption/csfle/go/azure/reader/insert-encrypted-document.go)

## Learn More

To learn how CSFLE works, see [CSFLE Fundamentals.](/docs/manual/core/csfle/fundamentals#std-label-csfle-fundamentals)

To learn more about the topics mentioned in this guide, see the following links:

- Learn more about CSFLE components on the [Reference](/docs/manual/core/csfle/reference#std-label-csfle-reference) page.

- Learn how Customer Master Keys and Data Encryption Keys work on the [Encryption Keys and Key Vaults](/docs/manual/core/queryable-encryption/fundamentals/keys-key-vaults#std-label-qe-reference-keys-key-vaults) page

- See how KMS Providers manage your CSFLE keys on the [KMS Providers](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-fundamentals-kms-providers) page.
