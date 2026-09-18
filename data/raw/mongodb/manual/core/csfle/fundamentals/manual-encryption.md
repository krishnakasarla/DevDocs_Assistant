> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

<!--
Tab options on this page. Append to the .md URL to filter:
  ?tabs=<id,...>   select specific tabs (e.g. ?tabs=nodejs,shell)
  ?allTabs=true    include every tab
  (no param)       default: one tab per tabset

Available tabs:
  drivers: shell, csharp, go, java-sync, nodejs, python
-->

# CSFLE Explicit Encryption

## Overview

Explicit encryption provides fine-grained control over security, at the cost of increased complexity when configuring collections and writing code for MongoDB Drivers. With explicit encryption, you specify how to encrypt fields in your document for each operation you perform on the database, and you include this logic throughout your application.

Explicit encryption is available in the following MongoDB products:

- MongoDB Community Server

- MongoDB Enterprise Advanced

- MongoDB Atlas

## Use Explicit Encryption

To use explicit encryption you must perform the following actions in your CSFLE-enabled application:

- [Create a ClientEncryption Instance](/docs/manual/core/csfle/fundamentals/manual-encryption#std-label-csfle-fundamentals-manual-encryption-client-enc)

- [Encrypt Fields in Read and Write Operations](/docs/manual/core/csfle/fundamentals/manual-encryption#std-label-csfle-fundamentals-manual-encryption-update-operations)

- [Manually](/docs/manual/core/csfle/fundamentals/manual-encryption#std-label-csfle-fundamentals-manual-encryption-manual-decryption) or [Automatically](/docs/manual/core/csfle/fundamentals/manual-encryption#std-label-csfle-fundamentals-manual-encryption-automatic-decryption) Decrypt Fields in Your Documents

### Create a ClientEncryption Instance

To use explicit encryption, you must create a `ClientEncryption` instance. `ClientEncryption` is an abstraction used across drivers and [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) that encapsulates the Key Vault collection and KMS (Key Management System) operations involved in explicit encryption.

To create a `ClientEncryption` instance, you must specify the following information:

- A `MongoClient` instance with access to your Key Vault collection

- The namespace of your Key Vault collection

- A `kmsProviders` object configured with access to the KMS (Key Management System) provider hosting your Customer Master Key

For more `ClientEncryption` options, see [MongoClient Options for CSFLE.](/docs/manual/core/csfle/reference/csfle-options-clients#std-label-csfle-reference-mongo-client)

To view code snippets that show how to create a `ClientEncryption` instance, see the [Example](/docs/manual/core/csfle/fundamentals/manual-encryption#std-label-csfle-fundamentals-manual-encryption-example) section of this guide.

### Encrypt Fields in Read and Write Operations

You must update read and write operations throughout your application such that your application encrypts fields before performing read and write operations.

To encrypt fields, use the `encrypt` method of your `ClientEncryption` instance.

To view code snippets that show how to use the `encrypt` method, see the [Example](/docs/manual/core/csfle/fundamentals/manual-encryption#std-label-csfle-fundamentals-manual-encryption-example) section of this guide.

### Manual Decryption

You can decrypt your encrypted fields manually or automatically when using explicit encryption.

To decrypt your fields manually, use the `decrypt` method of your `ClientEncryption` instance.

To view code snippets that show how to use the `decrypt` method, see the [Example](/docs/manual/core/csfle/fundamentals/manual-encryption#std-label-csfle-fundamentals-manual-encryption-example) section of this guide.

### Automatic Decryption

To decrypt your fields automatically, configure your `MongoClient` instance as follows:

- Specify your Key Vault collection

- Specify a `kmsProviders` object

- If you use MongoDB Community Server, set the `bypassAutoEncryption` option to `True`

**Note: Automatic Decryption is Available in MongoDB Community Server**

Although automatic encryption requires MongoDB Enterprise or MongoDB Atlas, automatic decryption is available in the following MongoDB products:

- MongoDB Community Server

- MongoDB Enterprise Advanced

- MongoDB Atlas

To view a code snippet demonstrating how to enable automatic decryption, select the tab corresponding to your preferred language:

```java
MongoClientSettings clientSettings = MongoClientSettings.builder()
.applyConnectionString(new ConnectionString(connectionString))
.autoEncryptionSettings(AutoEncryptionSettings.builder()
        .keyVaultNamespace(keyVaultNamespace)
        .kmsProviders(kmsProviders).bypassAutoEncryption(true)
        .build())
.build();
MongoClient mongoClient = MongoClients.create(clientSettings);

```

```javascript
const client = new MongoClient(connectionString, {
  monitorCommands: true,
  autoEncryption: {
    keyVaultNamespace,
    kmsProviders,
    bypassAutoEncryption: true,
  },
});

```

```python
auto_encryption_opts = AutoEncryptionOpts(
    kms_providers=kms_providers,
    key_vault_namespace=key_vault_namespace,
    bypass_auto_encryption=True,
)
client = MongoClient(auto_encryption_opts=auto_encryption_opts)

```

```csharp
var clientSettings = MongoClientSettings.FromConnectionString(connectionString);
var autoEncryptionOptions = new AutoEncryptionOptions(
    keyVaultNamespace: keyVaultNamespace,
    kmsProviders: kmsProviders,
    bypassAutoEncryption: true);
clientSettings.AutoEncryptionOptions = autoEncryptionOptions;
var client = new MongoClient(clientSettings);

```

```go
autoEncryptionOpts := options.AutoEncryption().
	SetKmsProviders(kmsProviders).
	SetKeyVaultNamespace(KeyVaultNamespace).
	SetBypassAutoEncryption(true)
client, err := mongo.Connect(context.TODO(), options.Client().ApplyURI(URI).SetAutoEncryptionOptions(autoEncryptionOpts))
if err != nil {
	return fmt.Errorf("Connect error for encrypted client: %v", err)
}
defer func() {
	_ = client.Disconnect(context.TODO())
}()

```

```javascript
var autoEncryptionOpts = {
  keyVaultNamespace: keyVaultNamespace,
  kmsProviders: kmsProviders,
  bypassAutoEncryption: true,
};
var encryptedClient = Mongo(
  connectionString,
  autoEncryptionOpts
);

```

## Example

Assume you want to insert documents with the following structure into your MongoDB instance:

```json
{
  "name": "<name of person>",
  "age": <age of person>,
  "favorite-foods": ["<array of foods>"]
}

```

1. Create a MongoClient Instance

   In this example, you use the same `MongoClient` instance to access your Key Vault collection and to read and write encrypted data.

   The following code snippets show how to create a `MongoClient` instance:

   ### MongoDB Shell

   ```javascript
   const autoEncryptionOpts = {
     keyVaultNamespace: keyVaultNamespace,
     kmsProviders: kmsProviders,
   };
   const encryptedClient = Mongo(connectionString, autoEncryptionOpts);
   ```

2. Create a ClientEncryption Instance

   The following code snippets show how to create a `ClientEncryption` instance:

   ### MongoDB Shell

   ```javascript
   const clientEncryption = encryptedClient.getClientEncryption();
   ```

3. Encrypt Fields and Insert

   You want to encrypt the fields of your document using the following algorithms:

   | Field Name | Encryption Algorithm | BSON Type of Field |
   | --- | --- | --- |
   | `name` | Deterministic | String |
   | `age` | No encryption | Int |
   | `favorite-foods` | Random | Array |

   The following code snippets show how to manually encrypt the fields in your document and insert your document into MongoDB:

   ### MongoDB Shell

   **Note:**

   The `dataKeyId` variable in the following examples refers to a Data Encryption Key (DEK). To learn how to generate a DEK with your Local Key Provider, see the [Quick Start](/docs/manual/core/csfle/quick-start#std-label-csfle-quick-start-create-dek). To learn how to create a DEK with a specific Key Management System, see [CSFLE Tutorials.](/docs/manual/core/csfle/tutorials#std-label-csfle-tutorials)

   ```javascript
   const encName = clientEncryption.encrypt(
     dataKeyId,
     "Greg",
     "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic"
   );
   const encFoods = clientEncryption.encrypt(
     dataKeyId,
     ["Cheese", "Grapes"],
     "AEAD_AES_256_CBC_HMAC_SHA_512-Random"
   );
   db.getSiblingDB(database).getCollection(collection).insertOne({
     name: encName,
     foods: encFoods,
   });
   ```

4. Retrieve Document and Decrypt Fields

   The following code snippets show how to retrieve your inserted document and manually decrypt the encrypted fields:

   ### MongoDB Shell

   ```javascript
   const encNameQuery = clientEncryption.encrypt(
     dataKeyId,
     "Greg",
     "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic"
   );
   let doc = db.getSiblingDB(database).getCollection(collection).findOne({
     name: encNameQuery,
   });
   console.log(doc);
   doc.name = clientEncryption.decrypt(doc.name);
   doc.foods = clientEncryption.decrypt(doc.foods);
   console.log(doc);
   ```

## Server-Side Field Level Encryption Enforcement

MongoDB supports using [schema validation](/docs/manual/core/schema-validation#std-label-schema-validation-overview) to enforce encryption of specific fields in a collection.

A client performing Client-Side Field Level Encryption with the explicit encryption mechanism on a MongoDB instance configured to enforce encryption of certain fields must encrypt those fields as specified on the MongoDB instance.

To learn how to set up server-side CSFLE enforcement, see [CSFLE Server-Side Schema Enforcement.](/docs/manual/core/csfle/reference/server-side-schema#std-label-csfle-reference-server-side-schema)

## Learn More

To learn more about Key Vault collections, Data Encryption Keys, and Customer Master Keys, see [Encryption Keys and Key Vaults.](/docs/manual/core/queryable-encryption/fundamentals/keys-key-vaults#std-label-qe-reference-keys-key-vaults)

To learn more about KMS (Key Management System) providers and `kmsProviders` objects, see [KMS Providers.](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-fundamentals-kms-providers)

To view and download full runnable code examples for the topics covered above, select a programming language:

- [C#](https://github.com/mongodb/mongo-csharp-driver/blob/main/tests/MongoDB.Driver.Examples/ExplicitEncryptionExamples.cs)

- [Go](https://github.com/mongodb/mongo-go-driver/blob/master/internal/integration/client_side_encryption_test.go)

- [Java](https://github.com/mongodb/mongo-java-driver/blob/main/driver-sync/src/test/functional/com/mongodb/client/ClientSideEncryptionSessionTest.java)

- [Node.js](https://github.com/mongodb/node-mongodb-native/blob/main/test/integration/client-side-encryption/client_side_encryption.prose.22.range_explicit_encryption.test.ts)

- [Python](https://github.com/mongodb/mongo-python-driver/blob/master/test/test_encryption.py)
