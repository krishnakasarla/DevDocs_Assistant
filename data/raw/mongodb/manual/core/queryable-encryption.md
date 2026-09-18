> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Queryable Encryption

Queryable Encryption equality and range queries are fully supported in production. Prefix, suffix, and substring queries are only available in public preview in MongoDB 8.2. Do not enable these query types in production. GA functionality of prefix, suffix and substring query types will be incompatible with the preview feature. To learn more, see [Supported Query Types](https://www.mongodb.com/docs/manual/core/queryable-encryption/reference/supported-operations/).

## Introduction

Queryable Encryption lets you perform the following tasks:

- Encrypt sensitive data fields from the client-side.

- Store sensitive data fields as fully randomized encrypted data on the database server-side.

- Run expressive queries on the encrypted data.

The server has no knowledge of the data it processes.

Sensitive data is encrypted throughout its lifecycle: in-transit, at-rest, in-use, in logs, and in backups. Data is decrypted only on the client-side, since only you have access to the encryption keys.

Queryable Encryption introduces an industry-first, fast, searchable encryption scheme developed by the pioneers in encrypted search. The feature supports equality and range searches, with additional query types such as prefix, suffix, and substring available in Public Preview.

You can set up Queryable Encryption using the following mechanisms:

- Automatic Encryption: Enables you to perform encrypted read and write operations without adding explicit calls to encrypt and decrypt fields.

- Explicit Encryption: Enables you to perform encrypted read and write operations through your MongoDB driver's encryption library. You must specify the logic for encryption with this library throughout your application.

## Considerations

When implementing an application that uses Queryable Encryption, consider the points listed in [Security Considerations.](/docs/manual/core/queryable-encryption/about-qe-csfle#std-label-qe-csfle-security-considerations)

For limitations, see [Queryable Encryption limitations.](/docs/manual/core/queryable-encryption/reference/limitations#std-label-qe-reference-encryption-limits)

### Compatibility

To learn which MongoDB server products and drivers support Queryable Encryption, see [Compatibility.](/docs/manual/core/queryable-encryption/reference/compatibility#std-label-qe-compatibility-reference)

### MongoDB Support Limitations

Enabling Queryable Encryption on a collection redacts fields from some diagnostic commands and omits some operations from the query log. This limits the data available to MongoDB support engineers, especially when analyzing query performance. To measure the impact of operations against encrypted collections, use a third party application performance monitoring tool to collect metrics.

For details, see [Redaction.](/docs/manual/core/queryable-encryption/reference/limitations#std-label-qe-redaction)

## Features

To learn about the security benefits of Queryable Encryption for your applications, see the [Queryable Encryption Features](/docs/manual/core/queryable-encryption/features#std-label-qe-features) page.

## Installation

To learn what you must install to use Queryable Encryption, see the [Install a Queryable Encryption Compatible Driver and Dependencies](/docs/manual/core/queryable-encryption/install#std-label-qe-install) and [Install and Configure a Query Analysis Component](/docs/manual/core/queryable-encryption/install-library#std-label-qe-csfle-install-library) pages.

## Quick Start

To start using Queryable Encryption, see the [Queryable Encryption Quick Start.](/docs/manual/core/queryable-encryption/quick-start#std-label-qe-quick-start)

## Fundamentals

To learn about encryption key management, see [Encryption Keys and Key Vaults.](/docs/manual/core/queryable-encryption/fundamentals/keys-key-vaults#std-label-qe-reference-keys-key-vaults)

To learn how Queryable Encryption works, see the [Queryable Encryption Fundamentals](/docs/manual/core/queryable-encryption/fundamentals#std-label-qe-fundamentals) section, which contains the following pages:

- [Encrypted Fields and Enabled Queries](/docs/manual/core/queryable-encryption/fundamentals/encrypt-and-query#std-label-qe-fundamentals-encrypt-query)

- [Create an Encryption Schema](/docs/manual/core/queryable-encryption/qe-create-encryption-schema#std-label-qe-create-encryption-schema)

- [Encrypted Collections](/docs/manual/core/queryable-encryption/fundamentals/manage-collections#std-label-qe-fundamentals-collection-management)

- [Queryable Encryption with Explicit Encryption](/docs/manual/core/queryable-encryption/fundamentals/manual-encryption#std-label-qe-fundamentals-manual-encryption)

- [Rotate and Rewrap Encryption Keys](/docs/manual/core/queryable-encryption/fundamentals/manage-keys#std-label-qe-fundamentals-manage-keys)

## Tutorials

To learn how to perform specific tasks with Queryable Encryption, see the [Queryable Encryption Tutorials](/docs/manual/core/queryable-encryption/tutorials#std-label-qe-tutorials) section.

## Reference

For reference, see the [Queryable Encryption Reference](/docs/manual/core/queryable-encryption/reference#std-label-qe-reference) section.

The reference section contains the following pages:

- [Supported Operations for Queryable Encryption](/docs/manual/core/queryable-encryption/reference/supported-operations#std-label-qe-reference-automatic-encryption-supported-operations)

- [MongoClient Options for Queryable Encryption](/docs/manual/core/queryable-encryption/reference/qe-options-clients#std-label-qe-reference-mongo-client)
