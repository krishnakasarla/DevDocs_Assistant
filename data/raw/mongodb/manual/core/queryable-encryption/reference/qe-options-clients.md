> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

<!--
Tab options on this page. Append to the .md URL to filter:
  ?tabs=<id,...>   select specific tabs (e.g. ?tabs=nodejs,shell)
  ?allTabs=true    include every tab
  (no param)       default: one tab per tabset

Available tabs:
  drivers: shell, csharp, go, java-sync, nodejs, python
-->

# MongoClient Options for Queryable Encryption

Queryable Encryption equality and range queries are fully supported in production. Prefix, suffix, and substring queries are only available in public preview in MongoDB 8.2. Do not enable these query types in production. GA functionality of prefix, suffix and substring query types will be incompatible with the preview feature. To learn more, see [Supported Query Types](https://www.mongodb.com/docs/manual/core/queryable-encryption/reference/supported-operations/).

## Overview

On this page, you can learn about the Queryable Encryption-specific configuration options for `MongoClient` instances.

## Automatic Encryption Options

### Node.js

The following table describes the structure of an `AutoEncryptionOptions` object:

| Property | Data Type | Required? | Description |
| --- | --- | --- | --- |
| `keyVaultNamespace` | `String` | Yes | The full [namespace](/docs/manual/reference/glossary#std-term-namespace) of the Key Vault collection. |
| `kmsProviders` | `Object` | Yes | The Key Management System (KMS) used by Queryable Encryption for managing your Customer Master Keys (CMKs). To learn more about `kmsProviders` objects, see [KMS Providers.](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-fundamentals-kms-providers) To learn more about Customer Master Keys, see [Encryption Keys and Key Vaults.](/docs/manual/core/queryable-encryption/fundamentals/keys-key-vaults#std-label-qe-reference-keys-key-vaults) |
| `bypassAutoEncryption` | `Boolean` | No | Specify `true` to bypass automatic encryption rules and perform explicit (manual) per-field encryption. |
| `bypassQueryAnalysis` | `Boolean` | No | Disables automatic analysis of outgoing commands. Specify `true` to use explicit encryption without the Automatic Encryption Shared Library. Defaults to `false` if not specified. |
| `encryptedFieldsMap` | `Object` | No | A schema that specifies which fields to automatically encrypt and the types of queries allowed on those fields. To learn how to construct an encryption schema, see [Encrypted Fields and Enabled Queries.](/docs/manual/core/queryable-encryption/fundamentals/encrypt-and-query#std-label-qe-fundamentals-encrypt-query) |
| `extraOptions` | `Object` | No | Configuration options for the encryption library. To use the Automatic Encryption Shared Library instead of `mongocryptd`, specify the full absolute or relative file path to the library file in the `cryptSharedLibPath` property of this object. If the driver can't load the Automatic Encryption Shared Library from this path, creating the `MongoClient` will fail. |
| `keyVaultClient` | `MongoClient` | No | Specifies the `MongoClient` that should connect to the MongoDB instance hosting your Key Vault collection. If you omit this option, the driver uses the current `MongoClient` instance. To learn more about Key Vault collections, see [Key Vault Collections.](/docs/manual/core/queryable-encryption/fundamentals/keys-key-vaults#std-label-qe-reference-key-vault) |
| `tlsOptions` | `Object` | No | The TLS options to use when connecting to the KMS provider. |

**Note: API Documentation**

For more information on these automatic encryption options, see the API documentation for the [AutoEncryptionOptions](https://mongodb.github.io/node-mongodb-native/5.7/interfaces/AutoEncryptionOptions.html) interface.
