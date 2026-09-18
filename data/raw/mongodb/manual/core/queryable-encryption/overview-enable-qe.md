> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Overview: Enable Queryable Encryption

Queryable Encryption equality and range queries are fully supported in production. Prefix, suffix, and substring queries are only available in public preview in MongoDB 8.2. Do not enable these query types in production. GA functionality of prefix, suffix and substring query types will be incompatible with the preview feature. To learn more, see [Supported Query Types](https://www.mongodb.com/docs/manual/core/queryable-encryption/reference/supported-operations/).

This page summarizes the tasks required to set up your MongoDB deployment and your development environment for Queryable Encryption.

## Enable Queryable Encryption

1. Install a compatible MongoDB driver and dependencies

   [Install a Queryable Encryption compatible driver and dependencies](/docs/manual/core/queryable-encryption/install#std-label-qe-install)

2. Install and configure a Queryable Encryption library

   [Install and configure a query analysis component](/docs/manual/core/queryable-encryption/install-library#std-label-qe-csfle-install-library)

3. Create a Customer Master Key

   [Create a Customer Master Key](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-create-cmk)

4. Create your Queryable Encryption enabled application

   [Create a Queryable Encryption enabled application](/docs/manual/core/queryable-encryption/qe-create-application#std-label-qe-create-application)

## Use Queryable Encryption

After you install a Queryable Encryption driver and libraries, create a Customer Master Key, and create your application, you can start encrypting and querying data. See [Overview: Use Queryable Encryption](/docs/manual/core/queryable-encryption/overview-use-qe#std-label-qe-overview-use-qe) for instructions.
