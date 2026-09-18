> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Queryable Encryption with Explicit Encryption

Queryable Encryption equality and range queries are fully supported in production. Prefix, suffix, and substring queries are only available in public preview in MongoDB 8.2. Do not enable these query types in production. GA functionality of prefix, suffix and substring query types will be incompatible with the preview feature. To learn more, see [Supported Query Types](https://www.mongodb.com/docs/manual/core/queryable-encryption/reference/supported-operations/).

## Overview

Explicit encryption provides fine-grained control over security, at the cost of increased complexity when configuring collections and writing code for MongoDB Drivers. With explicit encryption, you specify how to encrypt fields in your document for each operation you perform on the database, and you include this logic throughout your application.

Explicit encryption is available in the following MongoDB products:

- MongoDB Community Server

- MongoDB Enterprise Advanced

- MongoDB Atlas

## Use Explicit Encryption

### Create a ClientEncryption Instance

`ClientEncryption` is an abstraction used across drivers and [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) that encapsulates the Key Vault collection and KMS (Key Management System) operations involved in explicit encryption.

To create a `ClientEncryption` instance, specify:

- A `kmsProviders` object configured with access to the KMS (Key Management System) provider hosting your Customer Master Key

- The namespace of your Key Vault collection

- If you use MongoDB Community Server, set the `bypassQueryAnalysis` option to `True`

- A `MongoClient` instance with access to your Key Vault collection

For more `ClientEncryption` options, see [MongoClient Options for Queryable Encryption.](/docs/manual/core/queryable-encryption/reference/qe-options-clients#std-label-qe-reference-mongo-client)

### Encrypt Fields in Read and Write Operations

You must update read and write operations throughout your application such that your application encrypts fields before performing read and write operations.

To encrypt fields, use the `encrypt` method of your `ClientEncryption` instance. Specify the following:

- The value to be encrypted

- The ID of the Data Encryption Key

- The algorithm

  - `unindexed`: for non-queryable encrypted fields.

  - `indexed`: supports equality queries.

  - `range`: supports range queries.

  - `text`: supports prefixPreview, suffixPreview, and substringPreview queries.

- For read operations on queryable encrypted fields, specify the [queryType](/docs/manual/core/queryable-encryption/fundamentals/encrypt-and-query#std-label-qe-query-types). All algorithms below require an index on the server, which is created when you specify the `encryptedFields` option during [`db.createCollection()`.](/docs/manual/reference/method/db.createCollection#mongodb-method-db.createCollection)

- For read operations on queryable encrypted fields, specify any additional options, such as the minimum and maximum queryable values for range fields.

#### Algorithms and QueryTypes

| algorithm | queryType | Additional Parameters |
| --- | --- | --- |
| `indexed` | `equality` | [contention factor.](/docs/manual/core/queryable-encryption/fundamentals/encrypt-and-query#std-label-qe-contention) |
| `range` | `range` | [min and max](/docs/manual/core/queryable-encryption/fundamentals/encrypt-and-query#std-label-qe-field-min-max) queryable values.; [contention factor.](/docs/manual/core/queryable-encryption/fundamentals/encrypt-and-query#std-label-qe-contention) |
| `text` | `prefixPreview`, `suffixPreview`, or `substringPreview` | [strMinQueryLength, strMaxQueryLength, caseSensitive, diacriticSensitive.](/docs/manual/core/queryable-encryption/fundamentals/encrypt-and-query#std-label-qe-substring-parameters); [contention factor.](/docs/manual/core/queryable-encryption/fundamentals/encrypt-and-query#std-label-qe-contention); `substringPreview` only: [strMaxLength](/docs/manual/core/queryable-encryption/fundamentals/encrypt-and-query#std-label-qe-substring-parameters) |

**Note:**

Starting in MongoDB 8.0, the `rangePreview` Queryable Encryption algorithm is deprecated and removed. Use the `range` algorithm instead.

### Automatic Decryption

To decrypt fields automatically, configure your `MongoClient` instance as follows:

- Specify a `kmsProviders` object

- Specify your Key Vault collection

- If you use MongoDB Community Server, set the `bypassQueryAnalysis` option to `True`

**Note: Automatic Decryption in MongoDB Community Server**

Automatic decryption is available in MongoDB Community Server. Automatic encryption requires MongoDB Enterprise or MongoDB Atlas.

## Server-Side Field Level Encryption Enforcement

[Steps](/docs/manual/core/queryable-encryption/qe-create-encryption-schema#std-label-qe-specify-fields-for-encryption) to enforce encryption of specific fields in a collection.

`Indexed` and `Range` fields require an index on the server. The index is created by specifying the `encryptedFields` option in [`db.createCollection()`.](/docs/manual/reference/method/db.createCollection#mongodb-method-db.createCollection)

If your MongoDB instance enforces the encryption of specific fields, any client performing Queryable Encryption with explicit encryption must encrypt those fields as specified. To learn how to set up server-side Queryable Encryption enforcement, see [Encrypted Fields and Enabled Queries.](/docs/manual/core/queryable-encryption/fundamentals/encrypt-and-query#std-label-qe-fundamentals-encrypt-query)

## Learn More

To learn more about Key Vault collections, Data Encryption Keys, and Customer Master Keys, see [Encryption Keys and Key Vaults.](/docs/manual/core/queryable-encryption/fundamentals/keys-key-vaults#std-label-qe-reference-keys-key-vaults)

To learn more about KMS (Key Management System) providers and `kmsProviders` objects, see [KMS Providers.](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-fundamentals-kms-providers)
