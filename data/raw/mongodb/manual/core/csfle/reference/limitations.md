> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# CSFLE Limitations

## Overview

Consider these limitations and restrictions before you enable CSFLE. Some operations are unsupported, and others behave differently.

For compatibility limitations, see [Compatibility.](/docs/manual/core/queryable-encryption/reference/compatibility#std-label-qe-csfle-compatibility)

## Read and Write Operation Support

The [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) only stores encrypted [`BinData`](/docs/manual/reference/mongodb-extended-json-v1#mongodb-bsontype-data_binary) and applies any aggregation expression or query operator specifying an encrypted field against the `BinData` value. While the expression or operator may support `BinData` fields, the resulting value may be incorrect or unexpected when compared to issuing that same expression or operator against the decrypted value. The `mongod` throws an error if the expression or operator does not support `BinData` values.

For example, consider a deterministically encrypted integer `Salary`. A query filters for documents where `Salary` is greater than `100000`. The application explicitly (manually) encrypts the query value using deterministic encryption prior to issuing the query. The `mongod` compares the *encrypted* `BinData` value of `100000` to the *encrypted* `BinData` values stored in each document. While the operation returns successfully, the comparison of the `BinData` values may return a different result than the comparison of the decrypted integer values.

Automatic Client-Side Field Level Encryption rejects read or write operations which would return incorrect or unexpected results when issued against an encrypted field. For complete documentation, see [Supported Operations for Automatic Encryption.](/docs/manual/core/csfle/reference/supported-operations#std-label-csfle-reference-automatic-encryption-supported-operations)

Applications performing explicit (manual) encryption may reference the linked page as guidance for issuing read/write operations against encrypted fields.

## Arrays

CSFLE does not support automatic encryption on fields within an array of documents.

## Views

Queries against [views](/docs/manual/core/views#std-label-views-landing-page) on collections containing values encrypted with Client-Side Field Level Encryption may return unexpected or incorrect results if either the underlying view aggregation pipeline *or* the query references encrypted fields. If creating a view on a collection containing values encrypted with Client-Side Field Level Encryption, avoid operating on encrypted fields to mitigate the risk of unexpected or incorrect results.

While 4.2+ compatible drivers configured for automatic Client-Side Field Level Encryption have [supported operations for automatic encryption](/docs/manual/core/csfle/reference/supported-operations#std-label-csfle-reference-automatic-encryption-supported-operations), for unsupported read and write operations, the underlying support library cannot introspect the view catalog to identify a given collection as a view. Applications therefore cannot rely on the automatic Client-Side Field Level Encryption validation to prevent unsupported queries against views on collections with encrypted fields.

For applications using explicit (manual) encryption to query a view on a collection containing encrypted values, consider constructing the query using *only* query operators with known [normal behavior](/docs/manual/core/csfle/reference/supported-operations#std-label-csfle-supported-query-operators) when issued against encrypted fields.

## Collation

Client-Side Field Level Encryption does not respect user-specified collations or collection default [collations](/docs/manual/reference/collation#std-label-collation-document-fields). Field level encryption obscures the field value and prevents normal collation behavior. Collation-sensitive queries against encrypted fields may return unexpected or incorrect results.

While 4.2+ compatible drivers configured for automatic Client-Side Field Level Encryption have [supported operations for automatic encryption](/docs/manual/core/csfle/reference/supported-operations#std-label-csfle-reference-automatic-encryption-supported-operations), for unsupported read and write operations the underlying support library cannot introspect the collection catalog to identify the default collation. Applications therefore cannot rely on the Client-Side Field Level Encryption validation to prevent querying on encrypted fields with collation defaults.

## Unique Indexes

[Unique indexes](/docs/manual/core/index-unique#std-label-index-type-unique) *cannot* guarantee uniqueness if the index key specifies any [randomly encrypted](/docs/manual/core/csfle/fundamentals/encryption-algorithms#std-label-csfle-random-encryption) fields.

Fields encrypted using the random algorithm *always* produce a different encrypted value given a specific input. The server considers each encrypted value unique even though the decrypted value itself is not unique. The collection can therefore contain multiple documents with duplicate decrypted values for a field with an index-enforced unique constraint.

While 4.2+ compatible drivers configured for automatic Client-Side Field Level Encryption have [supported operations for automatic encryption](/docs/manual/core/csfle/reference/supported-operations#std-label-csfle-reference-automatic-encryption-supported-operations) for unsupported read and write operations, the underlying support library cannot introspect the index catalog to identify a given field as unique. Applications therefore cannot rely on the automatic Client-Side Field Level Encryption validation to prevent unique constraint violations on randomly-encrypted fields.

## Shard Key

Specifying a [shard key](/docs/manual/core/sharding-shard-key#std-label-shard-key) on encrypted fields *or* encrypting fields of an existing shard key may result in unexpected or incorrect sharding behavior.

While 4.2+ compatible drivers configured for automatic Client-Side Field Level Encryption have [supported operations for automatic encryption](/docs/manual/core/csfle/reference/supported-operations#std-label-csfle-reference-automatic-encryption-supported-operations), for unsupported read and write operations, the underlying support library cannot introspect the sharding catalog metadata to identify shard key fields. Applications therefore cannot rely on the automatic field level encryption validation to prevent encryption of shard key fields.

## Read/Write Query Support

Automatic Client-Side Field Level Encryption supports a subset of commands, query operators, update operators, aggregation stages, and aggregation expressions. For complete documentation, see [Supported Operations for Automatic Encryption.](/docs/manual/core/csfle/reference/supported-operations#std-label-csfle-reference-automatic-encryption-supported-operations)
