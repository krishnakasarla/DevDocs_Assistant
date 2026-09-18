> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Choosing an In-Use Encryption Approach

Queryable Encryption equality and range queries are fully supported in production. Prefix, suffix, and substring queries are only available in public preview in MongoDB 8.2. Do not enable these query types in production. GA functionality of prefix, suffix and substring query types will be incompatible with the preview feature. To learn more, see [Supported Query Types](https://www.mongodb.com/docs/manual/core/queryable-encryption/reference/supported-operations/).

MongoDB provides two approaches to [In-Use Encryption](/docs/manual/reference/glossary#std-term-In-Use-Encryption): [Queryable Encryption](/docs/manual/core/queryable-encryption#std-label-qe-manual-feature-qe) and [Client-Side Field Level Encryption](/docs/manual/core/csfle#std-label-manual-csfle-feature) (CSFLE). When using either approach, you can also choose between automatic and explicit encryption.

## About Queryable Encryption and CSFLE

Both Queryable Encryption and Client-Side Field Level Encryption (CSFLE) enable a client application to encrypt data before transporting it over the network. Sensitive data is transparently encrypted and decrypted by the client and only communicated to and from the server in encrypted form.

To compare features in detail, see [Queryable Encryption Features](/docs/manual/core/queryable-encryption/features#std-label-qe-features) and [CSFLE Features.](/docs/manual/core/csfle/features#std-label-csfle-features)

## Considerations

When implementing an application that uses Queryable Encryption or CSFLE, review the security considerations in this section.

For the limitations of each approach, see [Queryable Encryption limitations](/docs/manual/core/queryable-encryption/reference/limitations#std-label-qe-reference-encryption-limits) or [CSFLE limitations.](/docs/manual/core/csfle/reference/limitations#std-label-csfle-reference-encryption-limits)

For MongoDB server and driver version compatibility, see [Compatibility.](/docs/manual/core/queryable-encryption/reference/compatibility#std-label-qe-csfle-compatibility)

### Security Considerations

- CSFLE and Queryable Encryption do not provide any guarantees against adversaries with access to your Customer Master Key and Data Encryption Keys.

- CSFLE and Queryable Encryption do not provide any guarantees against adversaries with arbitrary write access to collections containing encrypted data.

- MongoDB uses [schema validation](/docs/manual/core/schema-validation#std-label-schema-validation-overview) to enforce encryption of specific fields in a collection. Without a client-side schema, the client downloads the server-side schema for the collection to determine which fields to encrypt. To avoid this issue, use client-side schema validation.

  Because CSFLE and Queryable Encryption do not provide a mechanism to verify the integrity of a schema, relying on a server-side schema means trusting that the server's schema has not been tampered with. If an adversary compromises the server, they can modify the schema so that a previously encrypted field is no longer labeled for encryption. This causes the client to send plaintext values for that field.

  For an example of CSFLE configuration for client and server-side schemas, see [CSFLE Server-Side Field Level Encryption Enforcement.](/docs/manual/core/csfle/fundamentals/automatic-encryption#std-label-field-level-encryption-automatic-remote-schema)

## Using Queryable Encryption and CSFLE

You can use Queryable Encryption, Client-Side Field Level Encryption, or both in your application. However, you can't use both approaches in the same collection.

Consider using Queryable Encryption in the following scenarios:

- You are developing a new application and want to use the latest cryptographic advancements from MongoDB.

- You expect users to run ranged, prefix, suffix, or substring queries against encrypted data.

- Your application can use a single key for a given field, rather than requiring separate keys on a per-user or per-tenant basis.

There are situations where CSFLE may be a preferable solution:

- Your application already uses CSFLE.

- You need to use different keys for the same field. This is commonly encountered when separating tenants or using user-specific keys.

- You need to be flexible with your data schema and potentially add more encrypted fields. Adding encrypted fields for Queryable Encryption requires rebuilding metadata collections and indexes.

### Querying Encrypted Fields

Queryable Encryption supports equality and range queries on encrypted numeric or date fields.

Support for prefix, suffix, and substring queries on encrypted string fields is in Public Preview. You can configure these queries for diacritic folding or case insensitivity to ensure different representations of the same string match.

Client-Side Field Level Encryption supports equality queries on deterministically encrypted fields.

For more information about supported query operators, see [Supported Query Operators for Queryable Encryption](/docs/manual/core/queryable-encryption/reference/supported-operations#std-label-qe-supported-query-operators) and [Supported Query Operators for CSFLE](/docs/manual/core/csfle/reference/supported-operations#std-label-csfle-supported-query-operators). For the full list of MongoDB query operators, see [Query Predicates.](/docs/manual/reference/mql/query-predicates#std-label-query-projection-operators-top)

### Encryption Algorithms

Both Queryable Encryption and Client-Side Field Level Encryption use the [AEAD](https://en.wikipedia.org/wiki/Authenticated_encryption#Authenticated_encryption_with_associated_data) AES-256-CBC encryption algorithm in authenticated mode to perform encryption. See [Cryptographic Primitives](/docs/manual/core/csfle/reference/cryptographic-primitives#std-label-qe-cryptographic-primitives) for more information.

The encryption algorithm for Queryable Encryption uses randomized encryption based on structured encryption, which produces different encrypted output values from the same input.

For detailed information on MongoDB's approach to Queryable Encryption, see the [Overview of Queryable Encryption](https://cdn.bfldr.com/2URK6TO/as/64kp46t53v34xw37gkngbrg/An_Overview_of_Queryable_Encryption) and [Design and Analysis of a Stateless Document Database Encryption Scheme](https://cdn.bfldr.com/2URK6TO/as/jkwp857q2zr8fj5vqs24f5/Design__Analysis_Stateless_Document_Database_Encryption_Scheme) whitepapers.

The CSFLE encryption algorithm supports both randomized encryption and [deterministic encryption](/docs/manual/core/csfle/fundamentals/encryption-algorithms#std-label-csfle-deterministic-encryption). However, it only supports **querying** fields that are encrypted deterministically. With deterministic encryption, a given input value always encrypts to the same output value.

### Private Querying

MongoDB encrypts queries for both Queryable Encryption and Client-Side Field Level Encryption so that the server has no information on cleartext document or query values. With Queryable Encryption, private querying goes a step further and redacts logs and metadata to scrub information around the query's existence. This ensures stronger privacy and confidentiality.

## Choosing Between Automatic and Explicit Encryption

### Using Automatic Encryption

We recommend automatic encryption in most situations, as it streamlines the process of writing your client application. With automatic encryption, MongoDB automatically encrypts and decrypts fields in read and write operations.

### Using Explicit Encryption

Explicit encryption provides fine-grained control over security, at the cost of increased complexity when configuring collections and writing code for MongoDB Drivers. With explicit encryption, you specify how to encrypt fields in your document for each operation you perform on the database, and you include this logic throughout your application.

For details, see [Explicit Encryption with Queryable Encryption](/docs/manual/core/queryable-encryption/fundamentals/manual-encryption#std-label-qe-fundamentals-manual-encryption) or [Explicit Encryption with CSFLE.](/docs/manual/core/csfle/fundamentals/manual-encryption#std-label-csfle-fundamentals-manual-encryption)
