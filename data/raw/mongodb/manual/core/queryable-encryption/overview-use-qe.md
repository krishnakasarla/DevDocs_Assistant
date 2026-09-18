> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Overview: Use Queryable Encryption

Queryable Encryption equality and range queries are fully supported in production. Prefix, suffix, and substring queries are only available in public preview in MongoDB 8.2. Do not enable these query types in production. GA functionality of prefix, suffix and substring query types will be incompatible with the preview feature. To learn more, see [Supported Query Types](https://www.mongodb.com/docs/manual/core/queryable-encryption/reference/supported-operations/).

This page summarizes the tasks required to create a Queryable Encryption-enabled collection, insert a document with encrypted fields, and query encrypted data.

## Enable Queryable Encryption

Before encrypting and querying data, you must install a Queryable Encryption-enabled driver and libraries, create a Customer Master Key, and create your application. See [Overview: Enable Queryable Encryption](/docs/manual/core/queryable-encryption/overview-enable-qe#std-label-qe-overview-enable-qe) for instructions.

## Use Queryable Encryption

1. Create an encrypted collection and insert a document with encrypted fields

   [Create an encrypted collection and insert documents](/docs/manual/core/queryable-encryption/qe-create-encrypted-collection#std-label-qe-create-encrypted-collection)

2. Query a document with encrypted fields

   [Query a document with encrypted fields](/docs/manual/core/queryable-encryption/qe-retrieve-encrypted-document#std-label-qe-query-encrypted-document)
