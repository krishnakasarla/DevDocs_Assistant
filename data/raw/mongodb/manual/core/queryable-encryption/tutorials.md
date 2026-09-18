> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Queryable Encryption Tutorials

Queryable Encryption equality and range queries are fully supported in production. Prefix, suffix, and substring queries are only available in public preview in MongoDB 8.2. Do not enable these query types in production. GA functionality of prefix, suffix and substring query types will be incompatible with the preview feature. To learn more, see [Supported Query Types](https://www.mongodb.com/docs/manual/core/queryable-encryption/reference/supported-operations/).

Read the [Overview: Enable Queryable Encryption](/docs/manual/core/queryable-encryption/overview-enable-qe#std-label-qe-overview-enable-qe) section to set up your development environment and data keys, then the [Overview: Use Queryable Encryption](/docs/manual/core/queryable-encryption/overview-use-qe#std-label-qe-overview-use-qe) section to learn how to use Queryable Encryption with your preferred Key Management System.

To learn how to use Queryable Encryption with a local key (not for production), see the [Queryable Encryption Quick Start.](/docs/manual/core/queryable-encryption/quick-start#std-label-qe-quick-start)

To learn how to use explicit encryption with Queryable Encryption, read [Use Explicit Encryption.](/docs/manual/core/queryable-encryption/tutorials/explicit-encryption#std-label-qe-tutorials-manual-encryption)

Each tutorial provides a sample application in multiple languages for each supported Key Management System.

Code samples for specific language drivers:

- [Python](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/python/)

- [Node.js](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/node/)

- [Java](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/java/)

- [Go](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/go/)

- [C#/.NET](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/csharp/)

- [Rust](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/rust/)

- [PHP](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/php/)

**Tip: Driver Integration Tutorials**

Some driver documentation sets include queryable encryption tutorials for specific driver integrations and frameworks. To view the tutorials, visit the following documentation:

- [Tutorial: Queryable Encryption with Mongoose](https://www.mongodb.com/docs/drivers/node/current/integrations/mongoose/mongoose-qe/#std-label-node-mongoose-qe) in the Node.js driver documentation

- [Tutorial: Queryable Encryption with Django MongoDB Backend](https://www.mongodb.com/docs/languages/python/django-mongodb/current/queryable-encryption/#std-label-django-qe) in the Django MongoDB Backend documentation
