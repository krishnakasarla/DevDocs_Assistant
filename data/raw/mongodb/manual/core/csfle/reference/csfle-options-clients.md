> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

<!--
Tab options on this page. Append to the .md URL to filter:
  ?tabs=<id,...>   select specific tabs (e.g. ?tabs=nodejs,shell)
  ?allTabs=true    include every tab
  (no param)       default: one tab per tabset

Available tabs:
  drivers: shell, csharp, go, java-sync, nodejs, python
-->

# MongoClient Options for CSFLE

## Overview

View information about the Client-Side Field Level Encryption (CSFLE)-specific configuration options for `MongoClient` instances.

## AutoEncryptionOpts

Pass an `autoEncryptionOpts` object to your `MongoClient` instance to specify CSFLE-specific options.

The following table describes the structure of an `autoEncryptionOpts` object:

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `keyVaultClient` | `MongoClient` | No | A `MongoClient` instance configured to connect to the MongoDB instance hosting your Key Vault collection. If you omit the `keyVaultClient` option, the MongoDB instance specified to your `MongoClient` instance containing the `autoEncryptionOpts` configuration is used as the host of your Key Vault collection. To learn more about Key Vault collections, see [Encryption Keys and Key Vaults.](/docs/manual/core/queryable-encryption/fundamentals/keys-key-vaults#std-label-qe-reference-keys-key-vaults) |
| `keyVaultNamespace` | String | Yes | The full [namespace](/docs/manual/reference/glossary#std-term-namespace) of the Key Vault collection. |
| `kmsProviders` | Object | Yes | The Key Management System (KMS) used by Client-Side Field Level Encryption for managing your Customer Master Keys (CMKs). To learn more about `kmsProviders` objects, see [KMS Providers.](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-fundamentals-kms-providers) To learn more about Customer Master Keys, see [Encryption Keys and Key Vaults.](/docs/manual/core/queryable-encryption/fundamentals/keys-key-vaults#std-label-qe-reference-keys-key-vaults) |
| `tlsOptions` | Object | No | An object that maps Key Management System provider names to TLS configuration options. To learn more about TLS options see: [TLS Options.](/docs/manual/reference/program/mongod#std-label-tls-mongod-options) To learn more about TLS see: [TLS/SSL (Transport Encryption).](/docs/manual/core/security-transport-encryption#std-label-transport-encryption) |
| `schemaMap` | Object | No | An encryption schema. To learn how to construct an encryption schema, see [Encryption Schemas.](/docs/manual/core/csfle/fundamentals/create-schema#std-label-csfle-fundamentals-create-schema) For complete documentation of encryption schemas, see [CSFLE Encryption Schemas.](/docs/manual/core/csfle/reference/encryption-schemas#std-label-csfle-reference-encryption-schemas) |
| `bypassAutoEncryption` | Boolean | No | Specify `true` to bypass automatic Client-Side Field Level Encryption rules and perform explicit encryption. `bypassAutoEncryption` does not disable automatic decryption. To learn more about this option, see [Automatic Decryption.](/docs/manual/core/csfle/fundamentals/manual-encryption#std-label-csfle-fundamentals-manual-encryption-automatic-decryption) |

## Example

To view a code-snippet demonstrating how to use `autoEncryptionOpts` to configure your `MongoClient` instance, select the tab corresponding to your driver:

### Node.js

```javascript
const secureClient = new MongoClient(connectionString, {
  monitorCommands: true,
  autoEncryption: {
    keyVaultNamespace,
    kmsProviders,
    schemaMap: patientSchema,
    extraOptions: extraOptions,
  },
});

```
