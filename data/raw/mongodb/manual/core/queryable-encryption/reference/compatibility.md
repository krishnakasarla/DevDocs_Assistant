> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Compatibility

Queryable Encryption equality and range queries are fully supported in production. Prefix, suffix, and substring queries are only available in public preview in MongoDB 8.2. Do not enable these query types in production. GA functionality of prefix, suffix and substring query types will be incompatible with the preview feature. To learn more, see [Supported Query Types](https://www.mongodb.com/docs/manual/core/queryable-encryption/reference/supported-operations/).

This page describes the MongoDB Server editions and driver versions compatible with Queryable Encryption and Client-Side Field Level Encryption to help you determine whether your deployment supports each in-use encryption feature.

Select your encryption feature and driver to see compatibility requirements.

## MongoDB Compatibility

You can use Queryable Encryption on a MongoDB Server 7.0 or later replica set or sharded cluster, but not a standalone instance. The following table shows which MongoDB Server products support Queryable Encryption:

| Product Name | Minimum Version | Supports Queryable Encryption with Automatic Encryption | Supports Queryable Encryption with Explicit Encryption |
| --- | --- | --- | --- |
| MongoDB Atlas | 7.0 | Yes | Yes |
| MongoDB Enterprise Advanced | 7.0 | Yes | Yes |
| MongoDB Community Edition | 7.0 | No | Yes |

**Note:**

Queryable Encryption is compatible with MongoDB Atlas but not [MongoDB Search.](https://www.mongodb.com/docs/atlas/atlas-search/)

## Driver Compatibility

To use Queryable Encryption with the [C](https://www.mongodb.com/docs/drivers/c/) driver, install driver version 1.24.0 or later and [libmongocrypt](/docs/manual/core/queryable-encryption/install#std-label-qe-reference-libmongocrypt) version 1.8.0 or later.

**Important: Automatic Encryption Support**

To use Queryable Encryption with automatic encryption, you must install a query analysis component. To learn more, see [Install and Configure a Query Analysis Component.](/docs/manual/core/queryable-encryption/install-library#std-label-qe-csfle-install-library)

## MongoDB Support Limitations

Enabling Queryable Encryption on a collection redacts fields from some diagnostic commands and omits some operations from the query log. This limits the data available to MongoDB support engineers, especially when analyzing query performance. To measure the impact of operations against encrypted collections, use a third party application performance monitoring tool to collect metrics.

## MongoDB Compatibility

You can use Queryable Encryption on a MongoDB Server 7.0 or later replica set or sharded cluster, but not a standalone instance. The following table shows which MongoDB Server products support Queryable Encryption:

| Product Name | Minimum Version | Supports Queryable Encryption with Automatic Encryption | Supports Queryable Encryption with Explicit Encryption |
| --- | --- | --- | --- |
| MongoDB Atlas | 7.0 | Yes | Yes |
| MongoDB Enterprise Advanced | 7.0 | Yes | Yes |
| MongoDB Community Edition | 7.0 | No | Yes |

**Note:**

Queryable Encryption is compatible with MongoDB Atlas but not [MongoDB Search.](https://www.mongodb.com/docs/atlas/atlas-search/)

## Driver Compatibility

To use Queryable Encryption with the [C++](https://www.mongodb.com/docs/drivers/cxx/) driver, install driver version 3.8.0 or later and [libmongocrypt](/docs/manual/core/queryable-encryption/install#std-label-qe-reference-libmongocrypt) version 1.8.0 or later.

**Important: Automatic Encryption Support**

To use Queryable Encryption with automatic encryption, you must install a query analysis component. To learn more, see [Install and Configure a Query Analysis Component.](/docs/manual/core/queryable-encryption/install-library#std-label-qe-csfle-install-library)

## MongoDB Support Limitations

Enabling Queryable Encryption on a collection redacts fields from some diagnostic commands and omits some operations from the query log. This limits the data available to MongoDB support engineers, especially when analyzing query performance. To measure the impact of operations against encrypted collections, use a third party application performance monitoring tool to collect metrics.

## MongoDB Compatibility

You can use Queryable Encryption on a MongoDB Server 7.0 or later replica set or sharded cluster, but not a standalone instance. The following table shows which MongoDB Server products support Queryable Encryption:

| Product Name | Minimum Version | Supports Queryable Encryption with Automatic Encryption | Supports Queryable Encryption with Explicit Encryption |
| --- | --- | --- | --- |
| MongoDB Atlas | 7.0 | Yes | Yes |
| MongoDB Enterprise Advanced | 7.0 | Yes | Yes |
| MongoDB Community Edition | 7.0 | No | Yes |

**Note:**

Queryable Encryption is compatible with MongoDB Atlas but not [MongoDB Search.](https://www.mongodb.com/docs/atlas/atlas-search/)

## Driver Compatibility

To use Queryable Encryption with the [.NET/C#](https://www.mongodb.com/docs/drivers/csharp/) driver, install driver version 2.20.0 or later.

For driver version 3.0 or later:

- Install [MongoDB.Driver.Encryption](https://www.nuget.org/packages/MongoDB.Driver.Encryption) on all operating systems.

- If your application runs on Linux, also install [libmongocrypt](/docs/manual/core/queryable-encryption/install#std-label-qe-reference-libmongocrypt) version 1.8.0 or later.

**Important: Automatic Encryption Support**

To use Queryable Encryption with automatic encryption, you must install a query analysis component. To learn more, see [Install and Configure a Query Analysis Component.](/docs/manual/core/queryable-encryption/install-library#std-label-qe-csfle-install-library)

## MongoDB Support Limitations

Enabling Queryable Encryption on a collection redacts fields from some diagnostic commands and omits some operations from the query log. This limits the data available to MongoDB support engineers, especially when analyzing query performance. To measure the impact of operations against encrypted collections, use a third party application performance monitoring tool to collect metrics.

## MongoDB Compatibility

You can use Queryable Encryption on a MongoDB Server 7.0 or later replica set or sharded cluster, but not a standalone instance. The following table shows which MongoDB Server products support Queryable Encryption:

| Product Name | Minimum Version | Supports Queryable Encryption with Automatic Encryption | Supports Queryable Encryption with Explicit Encryption |
| --- | --- | --- | --- |
| MongoDB Atlas | 7.0 | Yes | Yes |
| MongoDB Enterprise Advanced | 7.0 | Yes | Yes |
| MongoDB Community Edition | 7.0 | No | Yes |

**Note:**

Queryable Encryption is compatible with MongoDB Atlas but not [MongoDB Search.](https://www.mongodb.com/docs/atlas/atlas-search/)

## Driver Compatibility

To use Queryable Encryption with the [Go](https://www.mongodb.com/docs/drivers/go/) driver, install driver version 1.12 or later and [libmongocrypt](/docs/manual/core/queryable-encryption/install#std-label-qe-reference-libmongocrypt) version 1.8.0 or later.

**Important: Automatic Encryption Support**

To use Queryable Encryption with automatic encryption, you must install a query analysis component. To learn more, see [Install and Configure a Query Analysis Component.](/docs/manual/core/queryable-encryption/install-library#std-label-qe-csfle-install-library)

## MongoDB Support Limitations

Enabling Queryable Encryption on a collection redacts fields from some diagnostic commands and omits some operations from the query log. This limits the data available to MongoDB support engineers, especially when analyzing query performance. To measure the impact of operations against encrypted collections, use a third party application performance monitoring tool to collect metrics.

## MongoDB Compatibility

You can use Queryable Encryption on a MongoDB Server 7.0 or later replica set or sharded cluster, but not a standalone instance. The following table shows which MongoDB Server products support Queryable Encryption:

| Product Name | Minimum Version | Supports Queryable Encryption with Automatic Encryption | Supports Queryable Encryption with Explicit Encryption |
| --- | --- | --- | --- |
| MongoDB Atlas | 7.0 | Yes | Yes |
| MongoDB Enterprise Advanced | 7.0 | Yes | Yes |
| MongoDB Community Edition | 7.0 | No | Yes |

**Note:**

Queryable Encryption is compatible with MongoDB Atlas but not [MongoDB Search.](https://www.mongodb.com/docs/atlas/atlas-search/)

## Driver Compatibility

To use Queryable Encryption with the [Java Sync](https://www.mongodb.com/docs/drivers/java/sync/) driver, install driver version 4.10.0 or later and [mongodb-crypt](https://mvnrepository.com/artifact/org.mongodb/mongodb-crypt) version 1.8.0 or later.

**Important: Automatic Encryption Support**

To use Queryable Encryption with automatic encryption, you must install a query analysis component. To learn more, see [Install and Configure a Query Analysis Component.](/docs/manual/core/queryable-encryption/install-library#std-label-qe-csfle-install-library)

## MongoDB Support Limitations

Enabling Queryable Encryption on a collection redacts fields from some diagnostic commands and omits some operations from the query log. This limits the data available to MongoDB support engineers, especially when analyzing query performance. To measure the impact of operations against encrypted collections, use a third party application performance monitoring tool to collect metrics.

## MongoDB Compatibility

You can use Queryable Encryption on a MongoDB Server 7.0 or later replica set or sharded cluster, but not a standalone instance. The following table shows which MongoDB Server products support Queryable Encryption:

| Product Name | Minimum Version | Supports Queryable Encryption with Automatic Encryption | Supports Queryable Encryption with Explicit Encryption |
| --- | --- | --- | --- |
| MongoDB Atlas | 7.0 | Yes | Yes |
| MongoDB Enterprise Advanced | 7.0 | Yes | Yes |
| MongoDB Community Edition | 7.0 | No | Yes |

**Note:**

Queryable Encryption is compatible with MongoDB Atlas but not [MongoDB Search.](https://www.mongodb.com/docs/atlas/atlas-search/)

## Driver Compatibility

To use Queryable Encryption with the [Java Reactive Streams](https://www.mongodb.com/docs/drivers/reactive-streams/) driver, install driver version 4.10.0 or later and [mongodb-crypt](https://mvnrepository.com/artifact/org.mongodb/mongodb-crypt) version 1.8.0 or later.

**Important: Automatic Encryption Support**

To use Queryable Encryption with automatic encryption, you must install a query analysis component. To learn more, see [Install and Configure a Query Analysis Component.](/docs/manual/core/queryable-encryption/install-library#std-label-qe-csfle-install-library)

## MongoDB Support Limitations

Enabling Queryable Encryption on a collection redacts fields from some diagnostic commands and omits some operations from the query log. This limits the data available to MongoDB support engineers, especially when analyzing query performance. To measure the impact of operations against encrypted collections, use a third party application performance monitoring tool to collect metrics.

## MongoDB Compatibility

You can use Queryable Encryption on a MongoDB Server 7.0 or later replica set or sharded cluster, but not a standalone instance. The following table shows which MongoDB Server products support Queryable Encryption:

| Product Name | Minimum Version | Supports Queryable Encryption with Automatic Encryption | Supports Queryable Encryption with Explicit Encryption |
| --- | --- | --- | --- |
| MongoDB Atlas | 7.0 | Yes | Yes |
| MongoDB Enterprise Advanced | 7.0 | Yes | Yes |
| MongoDB Community Edition | 7.0 | No | Yes |

**Note:**

Queryable Encryption is compatible with MongoDB Atlas but not [MongoDB Search.](https://www.mongodb.com/docs/atlas/atlas-search/)

## Driver Compatibility

To use Queryable Encryption with the [Node.js](https://www.mongodb.com/docs/drivers/node/current/) driver, install driver version 5.5.0 or later and [mongodb-client-encryption](https://www.npmjs.com/package/mongodb-client-encryption/) version 2.8.0 or later.

If you're using version 6.0 or later of the Node.js driver, you must also use version 6.0 or later of `mongodb-client-encryption`.

**Important: Automatic Encryption Support**

To use Queryable Encryption with automatic encryption, you must install a query analysis component. To learn more, see [Install and Configure a Query Analysis Component.](/docs/manual/core/queryable-encryption/install-library#std-label-qe-csfle-install-library)

## MongoDB Support Limitations

Enabling Queryable Encryption on a collection redacts fields from some diagnostic commands and omits some operations from the query log. This limits the data available to MongoDB support engineers, especially when analyzing query performance. To measure the impact of operations against encrypted collections, use a third party application performance monitoring tool to collect metrics.

## MongoDB Compatibility

You can use Queryable Encryption on a MongoDB Server 7.0 or later replica set or sharded cluster, but not a standalone instance. The following table shows which MongoDB Server products support Queryable Encryption:

| Product Name | Minimum Version | Supports Queryable Encryption with Automatic Encryption | Supports Queryable Encryption with Explicit Encryption |
| --- | --- | --- | --- |
| MongoDB Atlas | 7.0 | Yes | Yes |
| MongoDB Enterprise Advanced | 7.0 | Yes | Yes |
| MongoDB Community Edition | 7.0 | No | Yes |

**Note:**

Queryable Encryption is compatible with MongoDB Atlas but not [MongoDB Search.](https://www.mongodb.com/docs/atlas/atlas-search/)

## Driver Compatibility

To use Queryable Encryption with the [PHP](https://www.mongodb.com/docs/drivers/php/) driver, install driver version 1.16 or later. No additional dependencies are required.

**Important: Automatic Encryption Support**

To use Queryable Encryption with automatic encryption, you must install a query analysis component. To learn more, see [Install and Configure a Query Analysis Component.](/docs/manual/core/queryable-encryption/install-library#std-label-qe-csfle-install-library)

## MongoDB Support Limitations

Enabling Queryable Encryption on a collection redacts fields from some diagnostic commands and omits some operations from the query log. This limits the data available to MongoDB support engineers, especially when analyzing query performance. To measure the impact of operations against encrypted collections, use a third party application performance monitoring tool to collect metrics.

## MongoDB Compatibility

You can use Queryable Encryption on a MongoDB Server 7.0 or later replica set or sharded cluster, but not a standalone instance. The following table shows which MongoDB Server products support Queryable Encryption:

| Product Name | Minimum Version | Supports Queryable Encryption with Automatic Encryption | Supports Queryable Encryption with Explicit Encryption |
| --- | --- | --- | --- |
| MongoDB Atlas | 7.0 | Yes | Yes |
| MongoDB Enterprise Advanced | 7.0 | Yes | Yes |
| MongoDB Community Edition | 7.0 | No | Yes |

**Note:**

Queryable Encryption is compatible with MongoDB Atlas but not [MongoDB Search.](https://www.mongodb.com/docs/atlas/atlas-search/)

## Driver Compatibility

To use Queryable Encryption with [PyMongo](https://www.mongodb.com/docs/drivers/python/), install driver version 4.4 or later and [pymongocrypt](https://pypi.org/project/pymongocrypt/) version 1.6 or later.

**Important: Automatic Encryption Support**

To use Queryable Encryption with automatic encryption, you must install a query analysis component. To learn more, see [Install and Configure a Query Analysis Component.](/docs/manual/core/queryable-encryption/install-library#std-label-qe-csfle-install-library)

## MongoDB Support Limitations

Enabling Queryable Encryption on a collection redacts fields from some diagnostic commands and omits some operations from the query log. This limits the data available to MongoDB support engineers, especially when analyzing query performance. To measure the impact of operations against encrypted collections, use a third party application performance monitoring tool to collect metrics.

## MongoDB Compatibility

You can use Queryable Encryption on a MongoDB Server 7.0 or later replica set or sharded cluster, but not a standalone instance. The following table shows which MongoDB Server products support Queryable Encryption:

| Product Name | Minimum Version | Supports Queryable Encryption with Automatic Encryption | Supports Queryable Encryption with Explicit Encryption |
| --- | --- | --- | --- |
| MongoDB Atlas | 7.0 | Yes | Yes |
| MongoDB Enterprise Advanced | 7.0 | Yes | Yes |
| MongoDB Community Edition | 7.0 | No | Yes |

**Note:**

Queryable Encryption is compatible with MongoDB Atlas but not [MongoDB Search.](https://www.mongodb.com/docs/atlas/atlas-search/)

## Driver Compatibility

To use Queryable Encryption with the [Ruby](https://www.mongodb.com/docs/drivers/ruby/) driver, install driver version 2.19 or later and [libmongocrypt-helper](https://rubygems.org/gems/libmongocrypt-helper/) version 1.8.0 or later.

**Important: Automatic Encryption Support**

To use Queryable Encryption with automatic encryption, you must install a query analysis component. To learn more, see [Install and Configure a Query Analysis Component.](/docs/manual/core/queryable-encryption/install-library#std-label-qe-csfle-install-library)

## MongoDB Support Limitations

Enabling Queryable Encryption on a collection redacts fields from some diagnostic commands and omits some operations from the query log. This limits the data available to MongoDB support engineers, especially when analyzing query performance. To measure the impact of operations against encrypted collections, use a third party application performance monitoring tool to collect metrics.

## MongoDB Compatibility

You can use Queryable Encryption on a MongoDB Server 7.0 or later replica set or sharded cluster, but not a standalone instance. The following table shows which MongoDB Server products support Queryable Encryption:

| Product Name | Minimum Version | Supports Queryable Encryption with Automatic Encryption | Supports Queryable Encryption with Explicit Encryption |
| --- | --- | --- | --- |
| MongoDB Atlas | 7.0 | Yes | Yes |
| MongoDB Enterprise Advanced | 7.0 | Yes | Yes |
| MongoDB Community Edition | 7.0 | No | Yes |

**Note:**

Queryable Encryption is compatible with MongoDB Atlas but not [MongoDB Search.](https://www.mongodb.com/docs/atlas/atlas-search/)

## Driver Compatibility

To use Queryable Encryption with the [Rust](https://www.mongodb.com/docs/drivers/rust/) driver, install driver version 2.4.0 or later and [libmongocrypt](/docs/manual/core/queryable-encryption/install#std-label-qe-reference-libmongocrypt) version 1.8.0 or later.

**Important: Automatic Encryption Support**

To use Queryable Encryption with automatic encryption, you must install a query analysis component. To learn more, see [Install and Configure a Query Analysis Component.](/docs/manual/core/queryable-encryption/install-library#std-label-qe-csfle-install-library)

## MongoDB Support Limitations

Enabling Queryable Encryption on a collection redacts fields from some diagnostic commands and omits some operations from the query log. This limits the data available to MongoDB support engineers, especially when analyzing query performance. To measure the impact of operations against encrypted collections, use a third party application performance monitoring tool to collect metrics.

## MongoDB Compatibility

You can use Queryable Encryption on a MongoDB Server 7.0 or later replica set or sharded cluster, but not a standalone instance. The following table shows which MongoDB Server products support Queryable Encryption:

| Product Name | Minimum Version | Supports Queryable Encryption with Automatic Encryption | Supports Queryable Encryption with Explicit Encryption |
| --- | --- | --- | --- |
| MongoDB Atlas | 7.0 | Yes | Yes |
| MongoDB Enterprise Advanced | 7.0 | Yes | Yes |
| MongoDB Community Edition | 7.0 | No | Yes |

**Note:**

Queryable Encryption is compatible with MongoDB Atlas but not [MongoDB Search.](https://www.mongodb.com/docs/atlas/atlas-search/)

## Driver Compatibility

To use Queryable Encryption with the [Scala](https://www.mongodb.com/docs/drivers/scala/) driver, install driver version 4.10.0 or later and [mongodb-crypt](https://mvnrepository.com/artifact/org.mongodb/mongodb-crypt) version 1.8.0 or later.

**Important: Automatic Encryption Support**

To use Queryable Encryption with automatic encryption, you must install a query analysis component. To learn more, see [Install and Configure a Query Analysis Component.](/docs/manual/core/queryable-encryption/install-library#std-label-qe-csfle-install-library)

## MongoDB Support Limitations

Enabling Queryable Encryption on a collection redacts fields from some diagnostic commands and omits some operations from the query log. This limits the data available to MongoDB support engineers, especially when analyzing query performance. To measure the impact of operations against encrypted collections, use a third party application performance monitoring tool to collect metrics.

## MongoDB Compatibility

You can use Client-Side Field Level Encryption on a replica set or sharded cluster, but not a standalone instance. The following table shows which MongoDB Server products support Client-Side Field Level Encryption:

| Product Name | Minimum Version | Supports CSFLE with Automatic Encryption | Supports CSFLE with Explicit Encryption |
| --- | --- | --- | --- |
| MongoDB Atlas | [All supported MongoDB versions](https://www.mongodb.com/docs/atlas/reference/faq/database/#which-versions-of-mongodb-do-service-clusters-use-) | Yes | Yes |
| MongoDB Enterprise Advanced | 4.2 | Yes | Yes |
| MongoDB Community Edition | 4.2 | No | Yes |

## Driver Compatibility

To use Client-Side Field Level Encryption and the Key Rotation API with the [C](https://www.mongodb.com/docs/drivers/c/) driver, install driver version 1.17.5 or later.

To learn more about the Key Rotation API, see [Rotate and Rewrap Encryption Keys.](/docs/manual/core/queryable-encryption/fundamentals/manage-keys#std-label-qe-fundamentals-manage-keys)

**Important: Automatic Encryption Support**

To use Client-Side Field Level Encryption with automatic encryption, you must install a query analysis component. To learn more, see [Install and Configure a CSFLE Query Analysis Component.](/docs/manual/core/csfle/reference/install-library#std-label-csfle-reference-install-lib)

## MongoDB Compatibility

You can use Client-Side Field Level Encryption on a replica set or sharded cluster, but not a standalone instance. The following table shows which MongoDB Server products support Client-Side Field Level Encryption:

| Product Name | Minimum Version | Supports CSFLE with Automatic Encryption | Supports CSFLE with Explicit Encryption |
| --- | --- | --- | --- |
| MongoDB Atlas | [All supported MongoDB versions](https://www.mongodb.com/docs/atlas/reference/faq/database/#which-versions-of-mongodb-do-service-clusters-use-) | Yes | Yes |
| MongoDB Enterprise Advanced | 4.2 | Yes | Yes |
| MongoDB Community Edition | 4.2 | No | Yes |

## Driver Compatibility

To use Client-Side Field Level Encryption and the Key Rotation API with the [C++](https://www.mongodb.com/docs/drivers/cxx/) driver, install driver version 3.6.0 or later.

To learn more about the Key Rotation API, see [Rotate and Rewrap Encryption Keys.](/docs/manual/core/queryable-encryption/fundamentals/manage-keys#std-label-qe-fundamentals-manage-keys)

**Important: Automatic Encryption Support**

To use Client-Side Field Level Encryption with automatic encryption, you must install a query analysis component. To learn more, see [Install and Configure a CSFLE Query Analysis Component.](/docs/manual/core/csfle/reference/install-library#std-label-csfle-reference-install-lib)

## MongoDB Compatibility

You can use Client-Side Field Level Encryption on a replica set or sharded cluster, but not a standalone instance. The following table shows which MongoDB Server products support Client-Side Field Level Encryption:

| Product Name | Minimum Version | Supports CSFLE with Automatic Encryption | Supports CSFLE with Explicit Encryption |
| --- | --- | --- | --- |
| MongoDB Atlas | [All supported MongoDB versions](https://www.mongodb.com/docs/atlas/reference/faq/database/#which-versions-of-mongodb-do-service-clusters-use-) | Yes | Yes |
| MongoDB Enterprise Advanced | 4.2 | Yes | Yes |
| MongoDB Community Edition | 4.2 | No | Yes |

## Driver Compatibility

To use Client-Side Field Level Encryption with the [.NET/C#](https://www.mongodb.com/docs/drivers/csharp/) driver, install driver version 2.10.0 or later. To use the Key Rotation API, install driver version 2.17.1 or later.

If you're using driver version 3.0 or later:

- Install the [MongoDB.Driver.Encryption](https://www.nuget.org/packages/MongoDB.Driver.Encryption) package from NuGet. This package enables automatic encryption.

- If your application runs on Linux, [install libmongocrypt](/docs/manual/core/queryable-encryption/install#std-label-qe-reference-libmongocrypt) manually. Then, set the `LIBMONGOCRYPT_PATH` environment variable to the absolute path of the `libmongocrypt` file.

- If your application runs on 64-bit Linux and you're using driver version 3.4.3 or earlier, add the following XML to your `.csproj` file.

  Replace `<MongoDriverEncryptionVersion>` with the installed version of the `MongoDB.Driver.Encryption` package:

  ```xml
  <PropertyGroup>
      <!-- replace the version here with your package version -->
      <MongoDriverEncryptionVersion>3.4.2</MongoDriverEncryptionVersion>
      <MongoDriverEncryptionPath>$(NuGetPackageRoot)mongodb.driver.encryption\$(MongoDriverEncryptionVersion)</MongoDriverEncryptionPath>
  </PropertyGroup>
  <PropertyGroup>
      <!-- Suppresses the duplicate file error -->
      <ErrorOnDuplicatePublishOutputFiles>false</ErrorOnDuplicatePublishOutputFiles>
  </PropertyGroup>
  <!-- Ensures the correct library after build or publish -->
  <Target Name="EnsureCorrectMongoEncryption" AfterTargets="Build;Publish" Condition="'$(RuntimeIdentifier)' != ''">
      <!-- Determine paths based on current operation -->
      <PropertyGroup>
          <_TargetDir Condition="Exists('$(PublishDir)')">$(PublishDir)</_TargetDir>
          <_TargetDir Condition="'$(_TargetDir)' == ''">$(OutputPath)</_TargetDir>
      </PropertyGroup>
      <!-- Copy the correct library based on runtime identifier (RID) -->
      <ItemGroup>
          <_CorrectMongoLib Include="$(MongoDriverEncryptionPath)/runtimes/linux/native/x64/libmongocrypt.so"
                            Condition="'$(RuntimeIdentifier)' == 'linux-x64'" />
          <_CorrectMongoLib Include="$(MongoDriverEncryptionPath)/runtimes/linux/native/arm64/libmongocrypt.so"
                            Condition="'$(RuntimeIdentifier)' == 'linux-arm64'" />
          <_CorrectMongoLib Include="$(MongoDriverEncryptionPath)/runtimes/linux/native/alpine/libmongocrypt.so"
                            Condition="'$(RuntimeIdentifier)' == 'linux-musl-arm64'" />
      </ItemGroup>
      <!-- Copy with overwrite -->
      <Copy SourceFiles="@(_CorrectMongoLib)"
            DestinationFolder="$(_TargetDir)"
            Condition="'@(_CorrectMongoLib)' != ''"
            OverwriteReadOnlyFiles="true" />
      <Message Text="Fixed MongoDB encryption library for $(RuntimeIdentifier)"
                Condition="'@(_CorrectMongoLib)' != ''" />
  </Target>
  ```

To learn more about the Key Rotation API, see [Rotate and Rewrap Encryption Keys.](/docs/manual/core/queryable-encryption/fundamentals/manage-keys#std-label-qe-fundamentals-manage-keys)

**Important: Automatic Encryption Support**

To use Client-Side Field Level Encryption with automatic encryption, you must install a query analysis component. To learn more, see [Install and Configure a CSFLE Query Analysis Component.](/docs/manual/core/csfle/reference/install-library#std-label-csfle-reference-install-lib)

## MongoDB Compatibility

You can use Client-Side Field Level Encryption on a replica set or sharded cluster, but not a standalone instance. The following table shows which MongoDB Server products support Client-Side Field Level Encryption:

| Product Name | Minimum Version | Supports CSFLE with Automatic Encryption | Supports CSFLE with Explicit Encryption |
| --- | --- | --- | --- |
| MongoDB Atlas | [All supported MongoDB versions](https://www.mongodb.com/docs/atlas/reference/faq/database/#which-versions-of-mongodb-do-service-clusters-use-) | Yes | Yes |
| MongoDB Enterprise Advanced | 4.2 | Yes | Yes |
| MongoDB Community Edition | 4.2 | No | Yes |

## Driver Compatibility

To use Client-Side Field Level Encryption, Explicit Encryption, or the Key Rotation API with the [Go](https://www.mongodb.com/docs/drivers/go/) driver, install Go driver version 1.2 or later and install [libmongocrypt](/docs/manual/core/queryable-encryption/install#std-label-qe-reference-libmongocrypt) version 1.5.2 or later.

To learn more about the Key Rotation API, see [Rotate and Rewrap Encryption Keys.](/docs/manual/core/queryable-encryption/fundamentals/manage-keys#std-label-qe-fundamentals-manage-keys)

**Important: Automatic Encryption Support**

To use Client-Side Field Level Encryption with automatic encryption, you must install a query analysis component. To learn more, see [Install and Configure a CSFLE Query Analysis Component.](/docs/manual/core/csfle/reference/install-library#std-label-csfle-reference-install-lib)

## MongoDB Compatibility

You can use Client-Side Field Level Encryption on a replica set or sharded cluster, but not a standalone instance. The following table shows which MongoDB Server products support Client-Side Field Level Encryption:

| Product Name | Minimum Version | Supports CSFLE with Automatic Encryption | Supports CSFLE with Explicit Encryption |
| --- | --- | --- | --- |
| MongoDB Atlas | [All supported MongoDB versions](https://www.mongodb.com/docs/atlas/reference/faq/database/#which-versions-of-mongodb-do-service-clusters-use-) | Yes | Yes |
| MongoDB Enterprise Advanced | 4.2 | Yes | Yes |
| MongoDB Community Edition | 4.2 | No | Yes |

## Driver Compatibility

To use Client-Side Field Level Encryption with the [Java Sync](https://www.mongodb.com/docs/drivers/java/sync/) driver, install driver version 3.10.0 or later. To use the Key Rotation API, install `mongodb-crypt` version 1.7.3 or later.

To learn more about the Key Rotation API, see [Rotate and Rewrap Encryption Keys.](/docs/manual/core/queryable-encryption/fundamentals/manage-keys#std-label-qe-fundamentals-manage-keys)

**Important: Automatic Encryption Support**

To use Client-Side Field Level Encryption with automatic encryption, you must install a query analysis component. To learn more, see [Install and Configure a CSFLE Query Analysis Component.](/docs/manual/core/csfle/reference/install-library#std-label-csfle-reference-install-lib)

## MongoDB Compatibility

You can use Client-Side Field Level Encryption on a replica set or sharded cluster, but not a standalone instance. The following table shows which MongoDB Server products support Client-Side Field Level Encryption:

| Product Name | Minimum Version | Supports CSFLE with Automatic Encryption | Supports CSFLE with Explicit Encryption |
| --- | --- | --- | --- |
| MongoDB Atlas | [All supported MongoDB versions](https://www.mongodb.com/docs/atlas/reference/faq/database/#which-versions-of-mongodb-do-service-clusters-use-) | Yes | Yes |
| MongoDB Enterprise Advanced | 4.2 | Yes | Yes |
| MongoDB Community Edition | 4.2 | No | Yes |

## Driver Compatibility

To use Client-Side Field Level Encryption with the [Java Reactive Streams](https://www.mongodb.com/docs/drivers/reactive-streams/) driver, install driver version 1.12.0 or later. To use the Key Rotation API, install `mongodb-crypt` version 1.7.3 or later.

To learn more about the Key Rotation API, see [Rotate and Rewrap Encryption Keys.](/docs/manual/core/queryable-encryption/fundamentals/manage-keys#std-label-qe-fundamentals-manage-keys)

**Important: Automatic Encryption Support**

To use Client-Side Field Level Encryption with automatic encryption, you must install a query analysis component. To learn more, see [Install and Configure a CSFLE Query Analysis Component.](/docs/manual/core/csfle/reference/install-library#std-label-csfle-reference-install-lib)

## MongoDB Compatibility

You can use Client-Side Field Level Encryption on a replica set or sharded cluster, but not a standalone instance. The following table shows which MongoDB Server products support Client-Side Field Level Encryption:

| Product Name | Minimum Version | Supports CSFLE with Automatic Encryption | Supports CSFLE with Explicit Encryption |
| --- | --- | --- | --- |
| MongoDB Atlas | [All supported MongoDB versions](https://www.mongodb.com/docs/atlas/reference/faq/database/#which-versions-of-mongodb-do-service-clusters-use-) | Yes | Yes |
| MongoDB Enterprise Advanced | 4.2 | Yes | Yes |
| MongoDB Community Edition | 4.2 | No | Yes |

## Driver Compatibility

To use Client-Side Field Level Encryption with the [Node.js](https://www.mongodb.com/docs/drivers/node/current/) driver, install driver version 3.4.0 or later. To use the Key Rotation API, install [mongodb-client-encryption](https://www.npmjs.com/package/mongodb-client-encryption/) version 2.2.0 - 2.x.

If you're using version 6.0 or later of the Node.js driver, you must also use version 6.0 or later of `mongodb-client-encryption`.

To learn more about the Key Rotation API, see [Rotate and Rewrap Encryption Keys.](/docs/manual/core/queryable-encryption/fundamentals/manage-keys#std-label-qe-fundamentals-manage-keys)

**Important: Automatic Encryption Support**

To use Client-Side Field Level Encryption with automatic encryption, you must install a query analysis component. To learn more, see [Install and Configure a CSFLE Query Analysis Component.](/docs/manual/core/csfle/reference/install-library#std-label-csfle-reference-install-lib)

## MongoDB Compatibility

You can use Client-Side Field Level Encryption on a replica set or sharded cluster, but not a standalone instance. The following table shows which MongoDB Server products support Client-Side Field Level Encryption:

| Product Name | Minimum Version | Supports CSFLE with Automatic Encryption | Supports CSFLE with Explicit Encryption |
| --- | --- | --- | --- |
| MongoDB Atlas | [All supported MongoDB versions](https://www.mongodb.com/docs/atlas/reference/faq/database/#which-versions-of-mongodb-do-service-clusters-use-) | Yes | Yes |
| MongoDB Enterprise Advanced | 4.2 | Yes | Yes |
| MongoDB Community Edition | 4.2 | No | Yes |

## Driver Compatibility

To use Client-Side Field Level Encryption and the Key Rotation API with the [PHP](https://www.mongodb.com/docs/drivers/php/) driver, install driver version 1.6.0 or later.

To learn more about the Key Rotation API, see [Rotate and Rewrap Encryption Keys.](/docs/manual/core/queryable-encryption/fundamentals/manage-keys#std-label-qe-fundamentals-manage-keys)

**Important: Automatic Encryption Support**

To use Client-Side Field Level Encryption with automatic encryption, you must install a query analysis component. To learn more, see [Install and Configure a CSFLE Query Analysis Component.](/docs/manual/core/csfle/reference/install-library#std-label-csfle-reference-install-lib)

## MongoDB Compatibility

You can use Client-Side Field Level Encryption on a replica set or sharded cluster, but not a standalone instance. The following table shows which MongoDB Server products support Client-Side Field Level Encryption:

| Product Name | Minimum Version | Supports CSFLE with Automatic Encryption | Supports CSFLE with Explicit Encryption |
| --- | --- | --- | --- |
| MongoDB Atlas | [All supported MongoDB versions](https://www.mongodb.com/docs/atlas/reference/faq/database/#which-versions-of-mongodb-do-service-clusters-use-) | Yes | Yes |
| MongoDB Enterprise Advanced | 4.2 | Yes | Yes |
| MongoDB Community Edition | 4.2 | No | Yes |

## Driver Compatibility

To use Client-Side Field Level Encryption with [PyMongo](https://www.mongodb.com/docs/drivers/python/), install driver version 3.10.0 or later. To use the Key Rotation API, install [pymongocrypt](https://pypi.org/project/pymongocrypt/) version 1.3.1 or later.

To learn more about the Key Rotation API, see [Rotate and Rewrap Encryption Keys.](/docs/manual/core/queryable-encryption/fundamentals/manage-keys#std-label-qe-fundamentals-manage-keys)

**Important: Automatic Encryption Support**

To use Client-Side Field Level Encryption with automatic encryption, you must install a query analysis component. To learn more, see [Install and Configure a CSFLE Query Analysis Component.](/docs/manual/core/csfle/reference/install-library#std-label-csfle-reference-install-lib)

## MongoDB Compatibility

You can use Client-Side Field Level Encryption on a replica set or sharded cluster, but not a standalone instance. The following table shows which MongoDB Server products support Client-Side Field Level Encryption:

| Product Name | Minimum Version | Supports CSFLE with Automatic Encryption | Supports CSFLE with Explicit Encryption |
| --- | --- | --- | --- |
| MongoDB Atlas | [All supported MongoDB versions](https://www.mongodb.com/docs/atlas/reference/faq/database/#which-versions-of-mongodb-do-service-clusters-use-) | Yes | Yes |
| MongoDB Enterprise Advanced | 4.2 | Yes | Yes |
| MongoDB Community Edition | 4.2 | No | Yes |

## Driver Compatibility

To use Client-Side Field Level Encryption and the Key Rotation API with the [Ruby](https://www.mongodb.com/docs/drivers/ruby/) driver, install driver version 2.12.1 or later.

To learn more about the Key Rotation API, see [Rotate and Rewrap Encryption Keys.](/docs/manual/core/queryable-encryption/fundamentals/manage-keys#std-label-qe-fundamentals-manage-keys)

**Important: Automatic Encryption Support**

To use Client-Side Field Level Encryption with automatic encryption, you must install a query analysis component. To learn more, see [Install and Configure a CSFLE Query Analysis Component.](/docs/manual/core/csfle/reference/install-library#std-label-csfle-reference-install-lib)

## MongoDB Compatibility

You can use Client-Side Field Level Encryption on a replica set or sharded cluster, but not a standalone instance. The following table shows which MongoDB Server products support Client-Side Field Level Encryption:

| Product Name | Minimum Version | Supports CSFLE with Automatic Encryption | Supports CSFLE with Explicit Encryption |
| --- | --- | --- | --- |
| MongoDB Atlas | [All supported MongoDB versions](https://www.mongodb.com/docs/atlas/reference/faq/database/#which-versions-of-mongodb-do-service-clusters-use-) | Yes | Yes |
| MongoDB Enterprise Advanced | 4.2 | Yes | Yes |
| MongoDB Community Edition | 4.2 | No | Yes |

## Driver Compatibility

To use Client-Side Field Level Encryption with the [Rust](https://www.mongodb.com/docs/drivers/rust/) driver, install driver version 2.4.0 or later. To use the Key Rotation API, install [libmongocrypt](/docs/manual/core/queryable-encryption/install#std-label-qe-reference-libmongocrypt) version 1.8.0 or later.

To learn more about the Key Rotation API, see [Rotate and Rewrap Encryption Keys.](/docs/manual/core/queryable-encryption/fundamentals/manage-keys#std-label-qe-fundamentals-manage-keys)

**Important: Automatic Encryption Support**

To use Client-Side Field Level Encryption with automatic encryption, you must install a query analysis component. To learn more, see [Install and Configure a CSFLE Query Analysis Component.](/docs/manual/core/csfle/reference/install-library#std-label-csfle-reference-install-lib)

## MongoDB Compatibility

You can use Client-Side Field Level Encryption on a replica set or sharded cluster, but not a standalone instance. The following table shows which MongoDB Server products support Client-Side Field Level Encryption:

| Product Name | Minimum Version | Supports CSFLE with Automatic Encryption | Supports CSFLE with Explicit Encryption |
| --- | --- | --- | --- |
| MongoDB Atlas | [All supported MongoDB versions](https://www.mongodb.com/docs/atlas/reference/faq/database/#which-versions-of-mongodb-do-service-clusters-use-) | Yes | Yes |
| MongoDB Enterprise Advanced | 4.2 | Yes | Yes |
| MongoDB Community Edition | 4.2 | No | Yes |

## Driver Compatibility

To use Client-Side Field Level Encryption and the Key Rotation API with the [Scala](https://www.mongodb.com/docs/drivers/scala/) driver, install driver version 2.7.0 or later.

To learn more about the Key Rotation API, see [Rotate and Rewrap Encryption Keys.](/docs/manual/core/queryable-encryption/fundamentals/manage-keys#std-label-qe-fundamentals-manage-keys)

**Important: Automatic Encryption Support**

To use Client-Side Field Level Encryption with automatic encryption, you must install a query analysis component. To learn more, see [Install and Configure a CSFLE Query Analysis Component.](/docs/manual/core/csfle/reference/install-library#std-label-csfle-reference-install-lib)
