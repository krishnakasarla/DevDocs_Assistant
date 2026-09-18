> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Queryable Encryption Reference

Queryable Encryption equality and range queries are fully supported in production. Prefix, suffix, and substring queries are only available in public preview in MongoDB 8.2. Do not enable these query types in production. GA functionality of prefix, suffix and substring query types will be incompatible with the preview feature. To learn more, see [Supported Query Types](https://www.mongodb.com/docs/manual/core/queryable-encryption/reference/supported-operations/).

Read the following sections to learn about components of Queryable Encryption:

- [Supported Operations for Queryable Encryption](/docs/manual/core/queryable-encryption/reference/supported-operations#std-label-qe-reference-automatic-encryption-supported-operations)

- [MongoClient Options for Queryable Encryption](/docs/manual/core/queryable-encryption/reference/qe-options-clients#std-label-qe-reference-mongo-client)

To learn about aggregation operators specific to Queryable Encryption enabled collections, refer to the following section of the MQL reference for aggregation operators:

- [Encrypted String Operators](/docs/manual/reference/mql/expressions#std-label-qe-aggregation-operators)
