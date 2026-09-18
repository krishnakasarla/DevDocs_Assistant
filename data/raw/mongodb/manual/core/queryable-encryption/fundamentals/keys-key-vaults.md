> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Encryption Keys and Key Vaults

Queryable Encryption equality and range queries are fully supported in production. Prefix, suffix, and substring queries are only available in public preview in MongoDB 8.2. Do not enable these query types in production. GA functionality of prefix, suffix and substring query types will be incompatible with the preview feature. To learn more, see [Supported Query Types](https://www.mongodb.com/docs/manual/core/queryable-encryption/reference/supported-operations/).

## Overview

In this guide, you can learn details about the following components of In-Use Encryption:

- Data Encryption Keys (DEK (Data Encryption Key))s

- Customer Master Keys (CMK (Customer Master Key))s

- Key Vault collections

- Key Management System (KMS (Key Management System))

To view step by step guides demonstrating how to use the preceding components to set up a Queryable Encryption or Client-Side Field Level Encryption enabled client, see the following resources:

- [Queryable Encryption Quick Start](/docs/manual/core/queryable-encryption/quick-start#std-label-qe-quick-start)

- [Queryable Encryption Automatic Encryption Tutorial](/docs/manual/core/queryable-encryption/tutorials#std-label-qe-tutorial-automatic-encryption)

- [CSFLE Quick Start](/docs/manual/core/csfle/quick-start#std-label-csfle-quick-start)

- [CSFLE Automatic Encryption Tutorial](/docs/manual/core/csfle/tutorials#std-label-csfle-tutorial-automatic-encryption)

## Data Encryption Keys and the Customer Master Key

In-use encryption uses a multi-level key hierarchy to protect your data, often called "[envelope encryption](/docs/manual/reference/glossary#std-term-envelope-encryption)" or "wrapping keys".

A Customer Master Key (CMK (Customer Master Key)), sometimes called a Key Management System (KMS (Key Management System)) key, is the top-level key you create in your customer provisioned key provider, such as a cloud KMS. The CMK (Customer Master Key) encrypts Data Encryption Keys (DEK (Data Encryption Key)), which in turn encrypt the fields in your documents. Without access to a CMK (Customer Master Key), your client application cannot decrypt the associated DEKs.

MongoDB stores DEKs, encrypted with your CMK (Customer Master Key), in the Key Vault collection as BSON documents. MongoDB can never decrypt the DEKs, as key management is client-side and customer controlled.

If you delete a DEK (Data Encryption Key), all fields encrypted with that DEK (Data Encryption Key) become permanently unreadable. If you delete a CMK (Customer Master Key), all fields encrypted with a DEK (Data Encryption Key) using that CMK (Customer Master Key) become permanently unreadable.

**Warning:**

The Customer Master Key is the most sensitive key in Queryable Encryption. If your CMK (Customer Master Key) is compromised, all of your encrypted data can be decrypted. Use a remote Key Management System to store your CMK (Customer Master Key).

**Important: Use a Remote Key Management Service Provider**

Store your Customer Master Key on a remote Key Management System (KMS (Key Management System)).

To learn more about why you should use a remote KMS (Key Management System), see [Reasons to Use a Remote Key Management System.](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-reasons-to-use-remote-kms)

To view a list of all supported KMS (Key Management System) providers, see the [KMS Providers](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-fundamentals-kms-providers) page.

### Key Rotation

You rotate your CMK (Customer Master Key) either manually or automatically on your provisioned key provider. MongoDB has no visibility into this process. Once you rotate the CMK (Customer Master Key), MongoDB uses it to wrap all new DEKs. It does not re-wrap existing encrypted DEKs. These are still wrapped with the prior CMK (Customer Master Key).

To rotate some or all of the encrypted DEKs in your key vault, use the [`KeyVault.rewrapManyDataKey()`](/docs/manual/reference/method/KeyVault.rewrapManyDataKey#mongodb-method-KeyVault.rewrapManyDataKey) method. It seamlessly re-wraps keys with the new CMK (Customer Master Key) specified, without interrupting your application. The DEKs themselves are left unchanged after re-wrapping them with the new CMK (Customer Master Key).

For details on rotating keys, see [Rotate Encryption Keys.](/docs/manual/core/queryable-encryption/fundamentals/manage-keys#std-label-qe-fundamentals-manage-keys)

## Key Vault Collections

Your Key Vault collection is the MongoDB collection you use to store encrypted Data Encryption Key (DEK (Data Encryption Key)) documents. DEK (Data Encryption Key) documents are BSON documents that contain DEKs and have the following structure:

```json
{
  "_id" : UUID(<string>),
  "status" : <int>,
  "masterKey" : {<object>},
  "updateDate" : ISODate(<string>),
  "keyMaterial" : BinData(0,<string>),
  "creationDate" : ISODate(<string>),
  "keyAltNames" : <array>
}

```

You create your Key Vault collection as you would a standard MongoDB collection. Your Key Vault collection must have a [unique index](/docs/manual/core/index-unique#std-label-index-type-unique) on the `keyAltNames` field. To check if the unique index exists, run the [`listIndexes`](/docs/manual/reference/command/listIndexes#mongodb-dbcommand-dbcmd.listIndexes) command against the Key Vault collection:

```json
db.runCommand({
   listIndexes: "__keyVault",
});
```

**Output:**

```text
{
   cursor: {
      id: Long("0"),
      ns: 'encryption.__keyVault',
      firstBatch: [
         { v: 2, key: { _id: 1 }, name: '_id_' }
         ]
   },
   ok: 1,
}
```

If the unique index does not exist, your application must create it before performing DEK (Data Encryption Key) management.

To learn how to create a MongoDB collection, see [Databases and Collections.](/docs/manual/core/databases-and-collections#std-label-collections)

**Tip: mongosh Feature**

The [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) method [`KeyVault.createKey()`](/docs/manual/reference/method/KeyVault.createKey#mongodb-method-KeyVault.createKey) automatically creates a unique index on the `keyAltNames` field if one does not exist.

To view diagrams detailing how your DEK (Data Encryption Key), CMK (Customer Master Key), and Key Vault collection interact in all supported KMS (Key Management System) provider architectures, see [KMS Providers.](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-fundamentals-kms-providers)

### Key Vault collection Name

You may use any non-admin [namespace](/docs/manual/reference/glossary#std-term-namespace) to store your Key Vault collection. By convention, the examples throughout this documentation use the  `encryption.__keyVault` [namespace.](/docs/manual/reference/glossary#std-term-namespace)

**Warning:**

Do not use the `admin` database to store encryption-related collections. If you use the admin database for this collection, your MongoDB client may not be able to access or decrypt your data due to lack of permissions.

### Permissions

Applications with [`read`](/docs/manual/reference/built-in-roles#mongodb-authrole-read) access to the Key Vault collection can retrieve encrypted Data Encryption Key (DEK (Data Encryption Key))s by querying the collection. However, only applications with access to the Customer Master Key (CMK (Customer Master Key)) used to encrypt a DEK (Data Encryption Key) can use that DEK (Data Encryption Key) for encryption or decryption. You must grant your application access to both the Key Vault collection  and your CMK (Customer Master Key) to encrypt and decrypt documents with a DEK (Data Encryption Key).

To learn how to grant access to a MongoDB collection, see [Manage Users and Roles](https://www.mongodb.com/docs/manual/tutorial/manage-users-and-roles/) in the MongoDB manual.

To learn how to grant your application access to your Customer Master Key, see the [Queryable Encryption Automatic Encryption Tutorial](/docs/manual/core/queryable-encryption/tutorials#std-label-qe-tutorial-automatic-encryption) or [CSFLE Automatic Encryption Tutorial.](/docs/manual/core/csfle/tutorials#std-label-csfle-tutorial-automatic-encryption)

### Key Vault Cluster

By default, MongoDB stores the Key Vault collection on the connected cluster. MongoDB also supports hosting the Key Vault collection on a different MongoDB deployment than the connected cluster. Applications must have access to both the cluster that hosts your Key Vault collection and the connection cluster to perform Queryable Encryption operations.

To specify the cluster that hosts your Key Vault collection, use the `keyVaultClient` field of your client's `MongoClient` object. To learn more about the specific configuration options in your client's `MongoClient` object, see the [MongoClient Options for Queryable Encryption](/docs/manual/core/queryable-encryption/reference/qe-options-clients#std-label-qe-reference-mongo-client) or [MongoClient Options for CSFLE.](/docs/manual/core/csfle/reference/csfle-options-clients#std-label-csfle-reference-mongo-client)

### Update a Key Vault Collection

To add a DEK (Data Encryption Key) to your Key Vault collection, use the `createKey` method of a `ClientEncryption` object.

To delete or update a DEK (Data Encryption Key), use one of the following mechanisms:

- The `rewrapManyDataKey` method

- Standard [CRUD](/docs/manual/crud#std-label-crud) operations

To learn more about the `rewrapManyDataKey` method, see the documentation of the method for your client or driver:

- [MongoDB Shell](/docs/manual/reference/method/KeyVault.rewrapManyDataKey#std-label-server-keyvault-rewrap-manydatakey-method)

- [PyMongo](https://pymongo.readthedocs.io/en/stable/api/pymongo/encryption.html#pymongo.encryption.ClientEncryption.rewrap_many_data_key)

- [MongoDB Node.js driver](https://github.com/mongodb/libmongocrypt/tree/master/bindings/node#RewrapManyDataKeyResult)

- [MongoDB .NET/C# driver](https://mongodb.github.io/mongo-csharp-driver/3.10.0/api/MongoDB.Driver.Encryption/MongoDB.Driver.Encryption.ClientEncryption.RewrapManyDataKey.html)

- [MongoDB Java driver](https://mongodb.github.io/mongo-java-driver/5.6/apidocs/driver-sync/com/mongodb/client/vault/ClientEncryption.html#rewrapManyDataKey\(org.bson.conversions.Bson\))

- [MongoDB Go driver](https://pkg.go.dev/go.mongodb.org/mongo-driver/v2/mongo#ClientEncryption.RewrapManyDataKey)

**Tip: mongosh Specific Features**

[`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) provides the following additional methods for working with your Key Vault collection:

- [`getKeyVault()`](/docs/manual/reference/method/getKeyVault#mongodb-method-getKeyVault)

- [`KeyVault.getKey()`](/docs/manual/reference/method/KeyVault.getKey#mongodb-method-KeyVault.getKey)

- [`KeyVault.getKeys()`](/docs/manual/reference/method/KeyVault.getKeys#mongodb-method-KeyVault.getKeys)

- [`KeyVault.getKeyByAltName()`](/docs/manual/reference/method/KeyVault.getKeyByAltName#mongodb-method-KeyVault.getKeyByAltName)

- [`KeyVault.createKey()`](/docs/manual/reference/method/KeyVault.createKey#mongodb-method-KeyVault.createKey)

- [`KeyVault.rewrapManyDataKey()`](/docs/manual/reference/method/KeyVault.rewrapManyDataKey#mongodb-method-KeyVault.rewrapManyDataKey)

- [`KeyVault.addKeyAlternateName()`](/docs/manual/reference/method/KeyVault.addKeyAlternateName#mongodb-method-KeyVault.addKeyAlternateName)

- [`KeyVault.removeKeyAlternateName()`](/docs/manual/reference/method/KeyVault.removeKeyAlternateName#mongodb-method-KeyVault.removeKeyAlternateName)

To view a tutorial that shows how to create a Data Encryption Key, see the [Queryable Encryption Quick Start](/docs/manual/core/queryable-encryption/quick-start#std-label-qe-quick-start) or the [CSFLE Quick Start.](/docs/manual/core/csfle/quick-start#std-label-csfle-local-create-dek)
