> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Client-Side Field Level Encryption

## Introduction

Client-Side Field Level Encryption (CSFLE) enables you to encrypt data in your application before you send it over the network to MongoDB. With CSFLE enabled, no MongoDB product has access to your data in an unencrypted form.

You can set up CSFLE using the following mechanisms:

- Automatic Encryption: Enables you to perform encrypted read and write operations without adding explicit calls to encrypt and decrypt fields.

- Explicit Encryption: Enables you to perform encrypted read and write operations through your MongoDB driver's encryption library. You must specify the logic for encryption with this library throughout your application.

## Considerations

When implementing an application that uses Client-Side Field Level Encryption, consider the points listed in [Security Considerations.](/docs/manual/core/queryable-encryption/about-qe-csfle#std-label-qe-csfle-security-considerations)

For limitations, see [CSFLE limitations.](/docs/manual/core/csfle/reference/limitations#std-label-csfle-reference-encryption-limits)

### Compatibility

To learn which MongoDB server products and drivers support CSFLE, see [Compatibility.](/docs/manual/core/queryable-encryption/reference/compatibility#std-label-csfle-compatibility-reference)

## Features

To learn about the security benefits of CSFLE for your applications, see the [CSFLE Features](/docs/manual/core/csfle/features#std-label-csfle-features) page.

## Installation

To learn what you must install to use CSFLE, see the [Installation Requirements](/docs/manual/core/csfle/install#std-label-csfle-install) page.

## Quick Start

To start using CSFLE, see the [CSFLE Quick Start.](/docs/manual/core/csfle/quick-start#std-label-csfle-quick-start)

Throughout this guide, code examples use placeholder text. Before you run the examples, substitute your own values for these placeholders.

For example:

```go
dek_id := "<Your Base64 DEK ID>"
```

You would replace everything between quotes with your DEK (Data Encryption Key) ID.

```go
dek_id := "abc123"
```

## Fundamentals

To learn how CSFLE works and how to set it up, see the [CSFLE Fundamentals](/docs/manual/core/csfle/fundamentals#std-label-csfle-fundamentals) section.

The fundamentals section contains the following pages:

- [Automatic Encryption](/docs/manual/core/csfle/fundamentals/automatic-encryption#std-label-csfle-fundamentals-automatic-encryption)

- [CSFLE Explicit Encryption](/docs/manual/core/csfle/fundamentals/manual-encryption#std-label-csfle-fundamentals-manual-encryption)

- [Encryption Schemas](/docs/manual/core/csfle/fundamentals/create-schema#std-label-csfle-fundamentals-create-schema)

- [Encryption Key Management](/docs/manual/core/csfle/fundamentals/manage-keys#std-label-csfle-fundamentals-manage-keys)

- [Fields and Encryption Types](/docs/manual/core/csfle/fundamentals/encryption-algorithms#std-label-csfle-reference-encryption-algorithms)

## Tutorials

To learn how to perform specific tasks with CSFLE, see the [CSFLE Tutorials](/docs/manual/core/csfle/tutorials#std-label-csfle-tutorials) section.

## Reference

To learn about encryption key management, see [Encryption Keys and Key Vaults.](/docs/manual/core/queryable-encryption/fundamentals/keys-key-vaults#std-label-qe-reference-keys-key-vaults)

For reference on CSFLE-enabled applications, see the [CSFLE Reference](/docs/manual/core/csfle/reference#std-label-csfle-reference) section:

- [CSFLE Encryption Schemas](/docs/manual/core/csfle/reference/encryption-schemas#std-label-csfle-reference-encryption-schemas)

- [CSFLE Server-Side Schema Enforcement](/docs/manual/core/csfle/reference/server-side-schema#std-label-csfle-reference-server-side-schema)

- [Supported Operations for Automatic Encryption](/docs/manual/core/csfle/reference/supported-operations#std-label-csfle-reference-automatic-encryption-supported-operations)

- [MongoClient Options for CSFLE](/docs/manual/core/csfle/reference/csfle-options-clients#std-label-csfle-reference-mongo-client)

- [CSFLE Encryption Components](/docs/manual/core/csfle/reference/encryption-components#std-label-csfle-reference-encryption-components)

- [How CSFLE Decrypts Documents](/docs/manual/core/csfle/reference/decryption#std-label-csfle-reference-decryption)

- [Cryptographic Primitives](/docs/manual/core/csfle/reference/cryptographic-primitives#std-label-csfle-reference-cryptographic-primitives)

- [Install and Configure a CSFLE Query Analysis Component](/docs/manual/core/csfle/reference/install-library#std-label-csfle-reference-mongocryptd)

- [Install libmongocrypt for CSFLE](/docs/manual/core/csfle/reference/libmongocrypt#std-label-csfle-reference-libmongocrypt)
