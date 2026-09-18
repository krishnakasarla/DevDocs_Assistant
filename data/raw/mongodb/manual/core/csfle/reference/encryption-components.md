> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# CSFLE Encryption Components

## Diagram

The following diagram illustrates the relationships between a MongoDB driver or [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) and each component of Client-Side Field Level Encryption (CSFLE):

![Diagram of relationships between driver and encryption components](/images/client-side-field-level-encryption-diagram.svg)

## Components

The following sections discuss the individual components of the preceding diagram.

### libmongocrypt

`libmongocrypt` is the [Apache-licensed open-source](https://github.com/mongodb/libmongocrypt) core cryptography library used by the official MongoDB drivers and [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) to power Client-Side Field Level Encryption. Some drivers may require specific integration steps to install or link the library.

To view steps for installing `libmongocrypt`, see the [libmongocrypt reference page.](/docs/manual/core/csfle/reference/libmongocrypt#std-label-csfle-reference-libmongocrypt)

### mongocryptd

`mongocryptd` supports automatic encryption and is only available with MongoDB Enterprise. `mongocryptd` does not perform cryptographic functions.

To learn more about `mongocryptd`, see [Install and Configure a CSFLE Query Analysis Component.](/docs/manual/core/csfle/reference/install-library#std-label-csfle-reference-mongocryptd)

### Key Vault collection

The Key Vault collection is a standard MongoDB collection that stores all Data Encryption Keys used to encrypt application data. Data Encryption Keys are themselves encrypted using a Customer Master Key (CMK (Customer Master Key)) prior to storage in the Key Vault collection. You can host your Key Vault collection on a different MongoDB cluster than the cluster storing your encrypted application data.

To learn more about the Key Vault collection, see [Encryption Keys and Key Vaults.](/docs/manual/core/queryable-encryption/fundamentals/keys-key-vaults#std-label-qe-reference-keys-key-vaults)

### Key Management System

The Key Management System (KMS (Key Management System)) stores the Customer Master Key (CMK (Customer Master Key)) used to encrypt Data Encryption Keys.

To view a list of all KMS (Key Management System) providers MongoDB supports, see [KMS Providers.](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-fundamentals-kms-providers)

### MongoDB Cluster

The MongoDB cluster which stores the encrypted data may also enforce Client-Side Field Level Encryption. For more information on server-side schema enforcement, see [CSFLE Server-Side Schema Enforcement.](/docs/manual/core/csfle/reference/server-side-schema#std-label-csfle-reference-server-side-schema)
