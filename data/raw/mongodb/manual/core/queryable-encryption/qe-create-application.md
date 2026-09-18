> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Create your Queryable Encryption Enabled Application

Queryable Encryption equality and range queries are fully supported in production. Prefix, suffix, and substring queries are only available in public preview in MongoDB 8.2. Do not enable these query types in production. GA functionality of prefix, suffix and substring query types will be incompatible with the preview feature. To learn more, see [Supported Query Types](https://www.mongodb.com/docs/manual/core/queryable-encryption/reference/supported-operations/).

## Overview

This guide shows you how to build an application that implements Queryable Encryption to automatically encrypt and decrypt document fields.

After you complete the steps in this guide, you should have a working client application that is ready for inserting documents with fields encrypted with your Customer Master Key.

## Before You Start

Ensure you have completed the following prerequisite tasks before creating your application:

1. [Install a Queryable Encryption compatible driver and dependencies](/docs/manual/core/queryable-encryption/install#std-label-qe-install)

2. [Install and configure a query analysis component](/docs/manual/core/queryable-encryption/install-library#std-label-qe-csfle-install-library)

3. [Create a Customer Master Key](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-create-cmk)

If you are using `mongocryptd`, your application requires write permissions on the working directory to create the `mongocryptd.pid` file.

## Procedure

### Full Application Code

To see the complete code for the sample application, select your programming language in the language selector.

[Complete mongosh Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/mongosh/)

Each sample application repository includes a `README.md` file that you can use to learn how to set up your environment and run the application.

1. Assign application variables

   The code samples in this tutorial use the following variables to perform the Queryable Encryption workflow:

   - **kmsProviderName** - The KMS you use to store your Customer Master Key. Set this to your key provider: `"aws"`, `"azure"`, `"gcp"`, or `"kmip"`.

   - **uri** - Your MongoDB deployment connection URI. Set your connection URI in the `MONGODB_URI` environment variable or replace the value directly.

   - **keyVaultDatabaseName** - The MongoDB database where your data encryption keys (DEKs) will be stored. Set this to `"encryption"`.

   - **keyVaultCollectionName** - The collection in MongoDB where your DEKs will be stored. Set this to `"__keyVault"`.

   - **keyVaultNamespace** - The namespace in MongoDB where your DEKs will be stored. Set this to the values of the `keyVaultDatabaseName` and `keyVaultCollectionName` variables, separated by a period.

   - **encryptedDatabaseName** - The MongoDB database where your encrypted data will be stored. Set this to `"medicalRecords"`.

   - **encryptedCollectionName** - The collection in MongoDB where your encrypted data will be stored. Set this to `"patients"`.

   You can declare these variables by using the following code:

   ```javascript
   const kmsProviderName = "<Your KMS Provider Name>";
   const uri = process.env.MONGODB_URI; // Your connection URI
   const keyVaultDatabaseName = "encryption";
   const keyVaultCollectionName = "__keyVault";
   const keyVaultNamespace = `${keyVaultDatabaseName}.${keyVaultCollectionName}`;
   const encryptedDatabaseName = "medicalRecords";
   const encryptedCollectionName = "patients";
   ```

   **Important: Key Vault Collection Namespace Permissions**

   The Key Vault collection is in the `encryption.__keyVault` namespace. Ensure that the database user your application uses to connect to MongoDB has [ReadWrite](/docs/manual/reference/built-in-roles#std-label-manual-reference-role-read-write) permissions on this namespace.

   **Tip: Environment Variables**

   The sample code in this tutorial references environment variables that you need to set. Alternatively, you can replace the values directly in the code.

   To learn how you can setup these environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/node/README.md) file included in the sample application on GitHub.

2. Add your KMS credentials

   Create a variable containing your KMS credentials with the following structure. Use the Access Key ID and Secret Access Key you used in step 2.2 when you [created an AWS IAM user.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-create-aws-iam-user)

   ```javascript
   kmsProviderCredentials = {
     aws: {
       accessKeyId: process.env["AWS_ACCESS_KEY_ID"], // Your AWS access key ID
       secretAccessKey: process.env["AWS_SECRET_ACCESS_KEY"], // Your AWS secret access key
     },
   };
   ```

   You can also provide a custom name for your KMS provider by passing in a string that includes the name of the KMS provider, followed by a colon and the custom name. Providing a unique name for a KMS provider allows you to specify multiple KMS providers of the same type.

   For example, you can name your AWS KMS provider "my\_aws\_provider" in your KMS credentials variable as shown in the following code:

   ```javascript
   kmsProviderCredentials = {
     "aws:my_aws_provider": {
       accessKeyId: process.env["AWS_ACCESS_KEY_ID"], // Your AWS access key ID
       secretAccessKey: process.env["AWS_SECRET_ACCESS_KEY"], // Your AWS secret access key
     },
   };

   ```

   NOTE: The remaining steps in this tutorial use the default KMS provider string, `"aws"`.

   **Important: Reminder: Authenticate with IAM Roles in Production**

   To use an IAM (Identity and Access Management) role instead of an IAM (Identity and Access Management) user to authenticate your application, specify an empty object for your credentials in your KMS provider object. This instructs the driver to automatically retrieve the credentials from the environment:

   ```javascript
   kmsProviders = {
     aws: { }
   };
   ```

   You cannot automatically retrieve credentials if you are using a named KMS provider.

3. Add your CMK credentials

   Create a variable containing your Customer Master Key credentials with the following structure. Use the ARN (Amazon Resource Name) and Region you recorded in step 1.3 when you [created a CMK.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-create-cmk-aws)

   ```javascript
   customerMasterKeyCredentials = {
     key: process.env["AWS_KEY_ARN"], // Your AWS Key ARN
     region: process.env["AWS_KEY_REGION"], // Your AWS Key Region
   };
   ```

4. Set automatic encryption options

   **Note: Automatic Encryption Options**

   The automatic encryption options provide configuration information to the Automatic Encryption Shared Library, which modifies the application's behavior when accessing encrypted fields.

   To learn more about the Automatic Encryption Shared Library, see the [Automatic Encryption Shared Library](/docs/manual/core/queryable-encryption/install-library#std-label-qe-reference-shared-library) page.

   Create an `autoEncryptionOptions` object with the following options:

   - The namespace of your Key Vault collection

   - The `kmsProviderCredentials` object, which contains your AWS KMS credentials

   ```javascript
   const autoEncryptionOptions = {
     keyVaultNamespace: keyVaultNamespace,
     kmsProviders: kmsProviderCredentials,
   };
   ```

5. Create a Client to Set Up an Encrypted Collection

   To create a client used to encrypt and decrypt data in your collection, instantiate a new `MongoClient` by using your connection URI and your automatic encryption options.

   ```javascript
   const encryptedClient = Mongo(uri, autoEncryptionOptions);
   ```

### Full Application Code

To see the complete code for the sample application, select your programming language in the language selector.

[Complete Node.js Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/node/)

Each sample application repository includes a `README.md` file that you can use to learn how to set up your environment and run the application.

1. Assign application variables

   The code samples in this tutorial use the following variables to perform the Queryable Encryption workflow:

   - **kmsProviderName** - The KMS you use to store your Customer Master Key. Set this to your key provider: `"aws"`, `"azure"`, `"gcp"`, or `"kmip"`.

   - **uri** - Your MongoDB deployment connection URI. Set your connection URI in the `MONGODB_URI` environment variable or replace the value directly.

   - **keyVaultDatabaseName** - The MongoDB database where your data encryption keys (DEKs) will be stored. Set this to `"encryption"`.

   - **keyVaultCollectionName** - The collection in MongoDB where your DEKs will be stored. Set this to `"__keyVault"`.

   - **keyVaultNamespace** - The namespace in MongoDB where your DEKs will be stored. Set this to the values of the `keyVaultDatabaseName` and `keyVaultCollectionName` variables, separated by a period.

   - **encryptedDatabaseName** - The MongoDB database where your encrypted data will be stored. Set this to `"medicalRecords"`.

   - **encryptedCollectionName** - The collection in MongoDB where your encrypted data will be stored. Set this to `"patients"`.

   You can declare these variables by using the following code:

   ```javascript
   const kmsProviderName = "<Your KMS Provider Name>";

   const uri = process.env.MONGODB_URI; // Your connection URI

   const keyVaultDatabaseName = "encryption";
   const keyVaultCollectionName = "__keyVault";
   const keyVaultNamespace = `${keyVaultDatabaseName}.${keyVaultCollectionName}`;
   const encryptedDatabaseName = "medicalRecords";
   const encryptedCollectionName = "patients";
   ```

   **Important: Key Vault Collection Namespace Permissions**

   The Key Vault collection is in the `encryption.__keyVault` namespace. Ensure that the database user your application uses to connect to MongoDB has [ReadWrite](/docs/manual/reference/built-in-roles#std-label-manual-reference-role-read-write) permissions on this namespace.

   **Tip: Environment Variables**

   The sample code in this tutorial references environment variables that you need to set. Alternatively, you can replace the values directly in the code.

   To learn how you can setup these environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/node/README.md) file included in the sample application on GitHub.

2. Add your KMS credentials

   Create a variable containing your KMS credentials with the following structure. Use the Access Key ID and Secret Access Key you used in step 2.2 when you [created an AWS IAM user.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-create-aws-iam-user)

   ```javascript
   kmsProviders = {
     aws: {
       accessKeyId: process.env.AWS_ACCESS_KEY_ID, // Your AWS access key ID
       secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY, // Your AWS secret access key
     },
   };
   ```

   You can also provide a custom name for your KMS provider by passing in a string that includes the name of the KMS provider, followed by a colon and the custom name. Providing a unique name for a KMS provider allows you to specify multiple KMS providers of the same type.

   For example, you can name your AWS KMS provider "my\_aws\_provider" in your KMS credentials variable as shown in the following code:

   ```javascript
   kmsProviderCredentials = {
     "aws:my_aws_provider": {
       accessKeyId: process.env["AWS_ACCESS_KEY_ID"], // Your AWS access key ID
       secretAccessKey: process.env["AWS_SECRET_ACCESS_KEY"], // Your AWS secret access key
     },
   };

   ```

   NOTE: The remaining steps in this tutorial use the default KMS provider string, `"aws"`.

   **Important: Reminder: Authenticate with IAM Roles in Production**

   To use an IAM (Identity and Access Management) role instead of an IAM (Identity and Access Management) user to authenticate your application, specify an empty object for your credentials in your KMS provider object. This instructs the driver to automatically retrieve the credentials from the environment:

   ```javascript
   kmsProviders = {
     aws: { }
   };
   ```

   You cannot automatically retrieve credentials if you are using a named KMS provider.

3. Add your CMK credentials

   Create a variable containing your Customer Master Key credentials with the following structure. Use the ARN (Amazon Resource Name) and Region you recorded in step 1.3 when you [created a CMK.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-create-cmk-aws)

   ```javascript
   customerMasterKeyCredentials = {
     key: process.env.AWS_KEY_ARN, // Your AWS Key ARN
     region: process.env.AWS_KEY_REGION, // Your AWS Key Region
   };
   ```

4. Set automatic encryption options

   **Note: Automatic Encryption Options**

   The automatic encryption options provide configuration information to the Automatic Encryption Shared Library, which modifies the application's behavior when accessing encrypted fields.

   To learn more about the Automatic Encryption Shared Library, see the [Automatic Encryption Shared Library](/docs/manual/core/queryable-encryption/install-library#std-label-qe-reference-shared-library) page.

   Create an `autoEncryptionOptions` object with the following options:

   - The namespace of your Key Vault collection

   - The `kmsProviders` object, which contains your AWS KMS credentials

   - The `sharedLibraryPathOptions` object, which contains the path to your Automatic Encryption Shared Library

   ```javascript
   const extraOptions = {
     cryptSharedLibPath: process.env.SHARED_LIB_PATH, // Path to your Automatic Encryption Shared Library
   };

   const autoEncryptionOptions = {
     keyVaultNamespace,
     kmsProviders,
     extraOptions,
   };
   ```

5. Create a Client to Set Up an Encrypted Collection

   To create a client used to encrypt and decrypt data in your collection, instantiate a new `MongoClient` by using your connection URI and your automatic encryption options.

   ```javascript
   const encryptedClient = new MongoClient(uri, {
     autoEncryption: autoEncryptionOptions,
   });
   ```

### Full Application Code

To see the complete code for the sample application, select your programming language in the language selector.

[Complete Python Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/python/)

Each sample application repository includes a `README.md` file that you can use to learn how to set up your environment and run the application.

1. Assign application variables

   The code samples in this tutorial use the following variables to perform the Queryable Encryption workflow:

   - **kms\_provider\_name** - The KMS you use to store your Customer Master Key. Set this to your key provider: `"aws"`, `"azure"`, `"gcp"`, or `"kmip"`.

   - **uri** - Your MongoDB deployment connection URI. Set your connection URI in the `MONGODB_URI` environment variable or replace the value directly.

   - **key\_vault\_database\_name** - The MongoDB database where your data encryption keys (DEKs) will be stored. Set this to `"encryption"`.

   - **key\_vault\_collection\_name** - The collection in MongoDB where your DEKs will be stored. Set this to `"__keyVault"`.

   - **key\_vault\_namespace** - The namespace in MongoDB where your DEKs will be stored. Set this to the values of the `key_vault_database_name` and `key_vault_collection_name` variables, separated by a period.

   - **encrypted\_database\_name** - The MongoDB database where your encrypted data will be stored. Set this to `"medicalRecords"`.

   - **encrypted\_collection\_name** - The collection in MongoDB where your encrypted data will be stored. Set this to `"patients"`.

   You can declare these variables by using the following code:

   ```python
   kms_provider_name = "<KMS provider name>"
   uri = os.environ.get("MONGODB_URI", "mongodb://127.0.0.1:27017")  # Your connection URI
   key_vault_database_name = "encryption"
   key_vault_collection_name = "__keyVault"
   key_vault_namespace = f"{key_vault_database_name}.{key_vault_collection_name}"
   encrypted_database_name = "medicalRecords"
   encrypted_collection_name = "patients"
   ```

   **Important: Key Vault Collection Namespace Permissions**

   The Key Vault collection is in the `encryption.__keyVault` namespace. Ensure that the database user your application uses to connect to MongoDB has [ReadWrite](/docs/manual/reference/built-in-roles#std-label-manual-reference-role-read-write) permissions on this namespace.

   **Tip: Environment Variables**

   The sample code in this tutorial references environment variables that you need to set. Alternatively, you can replace the values directly in the code.

   To learn how you can setup these environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/python/README.md) file included in the sample application on GitHub.

2. Add your KMS credentials

   Create a variable containing your KMS credentials with the following structure. Use the Access Key ID and Secret Access Key you used in step 2.2 when you [created an AWS IAM user.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-create-aws-iam-user)

   ```python
   kms_provider_credentials = {
       "aws": {
           "accessKeyId": os.environ['AWS_ACCESS_KEY_ID'], # Your AWS access key ID
           "secretAccessKey": os.environ['AWS_SECRET_ACCESS_KEY'] # Your AWS secret access key
       }
   }
   ```

   You can also provide a custom name for your KMS provider by passing in a string that includes the name of the KMS provider, followed by a colon and the custom name. Providing a unique name for a KMS provider allows you to specify multiple KMS providers of the same type.

   For example, you can name your AWS KMS provider "my\_aws\_provider" in your KMS credentials variable as shown in the following code:

   ```python
   kms_provider_credentials = {
       "aws:my_aws_provider": {
       "accessKeyId": os.environ['AWS_ACCESS_KEY_ID'], # Your AWS access key ID
       "secretAccessKey": os.environ['AWS_SECRET_ACCESS_KEY'] # Your AWS secret access key
       }
   }
   ```

   NOTE: The remaining steps in this tutorial use the default KMS provider string, `"aws"`.

   **Important: Reminder: Authenticate with IAM Roles in Production**

   To use an IAM (Identity and Access Management) role instead of an IAM (Identity and Access Management) user to authenticate your application, specify an empty object for your credentials in your KMS provider object. This instructs the driver to automatically retrieve the credentials from the environment:

   ```python
   kms_provider_credentials = {
     "aws": { }
   }
   ```

   You cannot automatically retrieve credentials if you are using a named KMS provider.

3. Add your CMK credentials

   Create a variable containing your Customer Master Key credentials with the following structure. Use the ARN (Amazon Resource Name) and Region you recorded in step 1.3 when you [created a CMK.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-create-cmk-aws)

   ```python
   customer_master_key_credentials = {
       "key": os.environ['AWS_KEY_ARN'],  # Your AWS Key ARN
       "region": os.environ['AWS_KEY_REGION'] # Your AWS Key Region
   }
   ```

4. Set automatic encryption options

   **Note: Automatic Encryption Options**

   The automatic encryption options provide configuration information to the Automatic Encryption Shared Library, which modifies the application's behavior when accessing encrypted fields.

   To learn more about the Automatic Encryption Shared Library, see the [Automatic Encryption Shared Library](/docs/manual/core/queryable-encryption/install-library#std-label-qe-reference-shared-library) page.

   Create an `AutoEncryptionOpts` object with the following options:

   - The `kms_provider_credentials` object, which contains your AWS KMS credentials

   - The namespace of your Key Vault collection

   - The path to your Automatic Encryption Shared Library

   ```python
   auto_encryption_options = AutoEncryptionOpts(
       kms_provider_credentials,
       key_vault_namespace,
       crypt_shared_lib_path=os.environ['SHARED_LIB_PATH'] # Path to your Automatic Encryption Shared Library>
   )
   ```

5. Create a Client to Set Up an Encrypted Collection

   To create a client used to encrypt and decrypt data in your collection, instantiate a new `MongoClient` by using your connection URI and your automatic encryption options.

   ```python
   encrypted_client = MongoClient(
       uri, auto_encryption_opts=auto_encryption_options)
   ```

### Full Application Code

To see the complete code for the sample application, select your programming language in the language selector.

[Complete Java Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/java/)

Each sample application repository includes a `README.md` file that you can use to learn how to set up your environment and run the application.

1. Assign application variables

   The code samples in this tutorial use the following variables to perform the Queryable Encryption workflow:

   - **kmsProviderName** - The KMS you use to store your Customer Master Key. Set this to your key provider: `"aws"`, `"azure"`, `"gcp"`, or `"kmip"`.

   - **uri** - Your MongoDB deployment connection URI. Set your connection URI in the `MONGODB_URI` environment variable or replace the value directly.

   - **keyVaultDatabaseName** - The MongoDB database where your data encryption keys (DEKs) will be stored. Set this to `"encryption"`.

   - **keyVaultCollectionName** - The collection in MongoDB where your DEKs will be stored. Set this to `"__keyVault"`.

   - **keyVaultNamespace** - The namespace in MongoDB where your DEKs will be stored. Set this to the values of the `keyVaultDatabaseName` and `keyVaultCollectionName` variables, separated by a period.

   - **encryptedDatabaseName** - The MongoDB database where your encrypted data will be stored. Set this to `"medicalRecords"`.

   - **encryptedCollectionName** - The collection in MongoDB where your encrypted data will be stored. Set this to `"patients"`.

   You can declare these variables by using the following code:

   ```java
   String kmsProviderName = "<KMS provider name>";
   String uri = QueryableEncryptionHelpers.getEnv("MONGODB_URI"); // Your connection URI
   String keyVaultDatabaseName = "encryption";
   String keyVaultCollectionName = "__keyVault";
   String keyVaultNamespace = keyVaultDatabaseName + "." + keyVaultCollectionName;
   String encryptedDatabaseName = "medicalRecords";
   String encryptedCollectionName = "patients";
   ```

   **Important: Key Vault Collection Namespace Permissions**

   The Key Vault collection is in the `encryption.__keyVault` namespace. Ensure that the database user your application uses to connect to MongoDB has [ReadWrite](/docs/manual/reference/built-in-roles#std-label-manual-reference-role-read-write) permissions on this namespace.

   **Tip: Environment Variables**

   The sample code in this tutorial references environment variables that you need to set. Alternatively, you can replace the values directly in the code.

   To learn how you can setup these environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/java/README.md) file included in the sample application on GitHub.

2. Add your KMS credentials

   Create a variable containing your KMS credentials with the following structure. Use the Access Key ID and Secret Access Key you used in step 2.2 when you [created an AWS IAM user.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-create-aws-iam-user)

   ```java
   Map<String, Object> kmsProviderDetails = new HashMap<>();
   kmsProviderDetails.put("accessKeyId", getEnv("AWS_ACCESS_KEY_ID")); // Your AWS access key ID
   kmsProviderDetails.put("secretAccessKey", getEnv("AWS_SECRET_ACCESS_KEY")); // Your AWS secret access key

   Map<String, Map<String, Object>> kmsProviderCredentials = new HashMap<String, Map<String, Object>>();
   kmsProviderCredentials.put("aws", kmsProviderDetails);
   ```

   You can also provide a custom name for your KMS provider by passing in a string that includes the name of the KMS provider, followed by a colon and the custom name. Providing a unique name for a KMS provider allows you to specify multiple KMS providers of the same type.

   For example, you can name your AWS KMS provider "my\_aws\_provider" in your KMS credentials variable as shown in the following code:

   ```java
   Map<String, Object> kmsProviderDetails = new HashMap<>();
   kmsProviderDetails.put("accessKeyId", getEnv("AWS_ACCESS_KEY_ID")); // Your AWS access key ID
   kmsProviderDetails.put("secretAccessKey", getEnv("AWS_SECRET_ACCESS_KEY")); // Your AWS secret access key

   Map<String, Map<String, Object>> kmsProviderCredentials = new HashMap<String, Map<String, Object>>();
   kmsProviderCredentials.put("aws:my_aws_provider", kmsProviderDetails);
   ```

   NOTE: The remaining steps in this tutorial use the default KMS provider string, `"aws"`.

   **Important: Reminder: Authenticate with IAM Roles in Production**

   To use an IAM (Identity and Access Management) role instead of an IAM (Identity and Access Management) user to authenticate your application, specify an empty object for your credentials in your KMS provider object. This instructs the driver to automatically retrieve the credentials from the environment:

   ```java
   kmsProviderCredentials.put("aws", new HashMap<>());
   ```

   You cannot automatically retrieve credentials if you are using a named KMS provider.

3. Add your CMK credentials

   Create a variable containing your Customer Master Key credentials with the following structure. Use the ARN (Amazon Resource Name) and Region you recorded in step 1.3 when you [created a CMK.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-create-cmk-aws)

   ```java
   BsonDocument customerMasterKeyCredentials = new BsonDocument();
   customerMasterKeyCredentials.put("provider", new BsonString(kmsProviderName));
   customerMasterKeyCredentials.put("key", new BsonString(getEnv("AWS_KEY_ARN"))); // Your AWS Key ARN
   customerMasterKeyCredentials.put("region", new BsonString(getEnv("AWS_KEY_REGION"))); // Your AWS Key Region
   ```

4. Set automatic encryption options

   **Note: Automatic Encryption Options**

   The automatic encryption options provide configuration information to the Automatic Encryption Shared Library, which modifies the application's behavior when accessing encrypted fields.

   To learn more about the Automatic Encryption Shared Library, see the [Automatic Encryption Shared Library](/docs/manual/core/queryable-encryption/install-library#std-label-qe-reference-shared-library) page.

   Create an `AutoEncryptionSettings` object with the following options:

   - The namespace of your Key Vault collection

   - The `kmsProviderCredentials` object, which contains your AWS KMS credentials

   - The `extraOptions` object, which contains the path to your Automatic Encryption Shared Library

   ```java
   Map<String, Object> extraOptions = new HashMap<String, Object>();
   extraOptions.put("cryptSharedLibPath", getEnv("SHARED_LIB_PATH")); // Path to your Automatic Encryption Shared Library

   AutoEncryptionSettings autoEncryptionSettings = AutoEncryptionSettings.builder()
           .keyVaultNamespace(keyVaultNamespace)
           .kmsProviders(kmsProviderCredentials)
           .extraOptions(extraOptions)
           .build();
   ```

   If you omit `keyVaultClient` or set `bypassAutomaticEncryption` to false in your `AutoEncryptionSettings` object, the driver creates a separate, internal `MongoClient`. The internal `MongoClient` configuration differs from the parent `MongoClient` by setting the `minPoolSize` to  0 and omitting the `AutoEncryptionSettings`.

5. Create a Client to Set Up an Encrypted Collection

   To create a client used to encrypt and decrypt data in your collection, instantiate a new `MongoClient` by using your connection URI and your automatic encryption options.

   ```java
   MongoClientSettings clientSettings = MongoClientSettings.builder()
           .applyConnectionString(new ConnectionString(uri))
           .autoEncryptionSettings(autoEncryptionSettings)
           .build();

   try (MongoClient encryptedClient = MongoClients.create(clientSettings)) {
   ```

### Full Application Code

To see the complete code for the sample application, select your programming language in the language selector.

[Complete Go Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/go/)

Each sample application repository includes a `README.md` file that you can use to learn how to set up your environment and run the application.

1. Assign application variables

   The code samples in this tutorial use the following variables to perform the Queryable Encryption workflow:

   - **kmsProviderName** - The KMS you use to store your Customer Master Key. Set this to your key provider: `"aws"`, `"azure"`, `"gcp"`, or `"kmip"`.

   - **uri** - Your MongoDB deployment connection URI. Set your connection URI in the `MONGODB_URI` environment variable or replace the value directly.

   - **keyVaultDatabaseName** - The MongoDB database where your data encryption keys (DEKs) will be stored. Set this to `"encryption"`.

   - **keyVaultCollectionName** - The collection in MongoDB where your DEKs will be stored. Set this to `"__keyVault"`.

   - **keyVaultNamespace** - The namespace in MongoDB where your DEKs will be stored. Set this to the values of the `keyVaultDatabaseName` and `keyVaultCollectionName` variables, separated by a period.

   - **encryptedDatabaseName** - The MongoDB database where your encrypted data will be stored. Set this to `"medicalRecords"`.

   - **encryptedCollectionName** - The collection in MongoDB where your encrypted data will be stored. Set this to `"patients"`.

   You can declare these variables by using the following code:

   ```go
   kmsProviderName := "<KMS provider name>"
   uri := os.Getenv("MONGODB_URI") // Your connection URI
   keyVaultDatabaseName := "encryption"
   keyVaultCollectionName := "__keyVault"
   keyVaultNamespace := keyVaultDatabaseName + "." + keyVaultCollectionName
   encryptedDatabaseName := "medicalRecords"
   encryptedCollectionName := "patients"
   ```

   **Important: Key Vault Collection Namespace Permissions**

   The Key Vault collection is in the `encryption.__keyVault` namespace. Ensure that the database user your application uses to connect to MongoDB has [ReadWrite](/docs/manual/reference/built-in-roles#std-label-manual-reference-role-read-write) permissions on this namespace.

   **Tip: Environment Variables**

   The sample code in this tutorial references environment variables that you need to set. Alternatively, you can replace the values directly in the code.

   To learn how you can setup these environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/go/README.md) file included in the sample application on GitHub.

2. Add your KMS credentials

   Create a variable containing your KMS credentials with the following structure. Use the Access Key ID and Secret Access Key you used in step 2.2 when you [created an AWS IAM user.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-create-aws-iam-user)

   ```go
   kmsProviderCredentials := map[string]map[string]interface{}{
   	"aws": {
   		"accessKeyId":     os.Getenv("AWS_ACCESS_KEY_ID"),     // AWS access key ID
   		"secretAccessKey": os.Getenv("AWS_SECRET_ACCESS_KEY"), // AWS secret access key
   	},
   }
   ```

   **Important: Reminder: Authenticate with IAM Roles in Production**

   To use an IAM (Identity and Access Management) role instead of an IAM (Identity and Access Management) user to authenticate your application, specify an empty object for your credentials in your KMS provider object. This instructs the driver to automatically retrieve the credentials from the environment:

   ```go
   kmsProviderCredentials := map[string]map[string]interface{}{
     "aws": { },
   }
   ```

   You cannot automatically retrieve credentials if you are using a named KMS provider.

3. Add your CMK credentials

   Create a variable containing your Customer Master Key credentials with the following structure. Use the ARN (Amazon Resource Name) and Region you recorded in step 1.3 when you [created a CMK.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-create-cmk-aws)

   ```go
   customerMasterKeyCredentials := map[string]string{
   	"key":    os.Getenv("AWS_KEY_ARN"),    // Your AWS Key ARN
   	"region": os.Getenv("AWS_KEY_REGION"), // Your AWS Key Region
   }
   ```

4. Set automatic encryption options

   **Note: Automatic Encryption Options**

   The automatic encryption options provide configuration information to the Automatic Encryption Shared Library, which modifies the application's behavior when accessing encrypted fields.

   To learn more about the Automatic Encryption Shared Library, see the [Automatic Encryption Shared Library](/docs/manual/core/queryable-encryption/install-library#std-label-qe-reference-shared-library) page.

   Create an `AutoEncryption` object with the following options:

   - The namespace of your Key Vault collection

   - The `kmsProviderCredentials` object, which contains your AWS KMS credentials

   - The `cryptSharedLibraryPath` object, which contains the path to your Automatic Encryption Shared Library

   ```go
   cryptSharedLibraryPath := map[string]interface{}{
   	"cryptSharedLibPath": os.Getenv("SHARED_LIB_PATH"), // Path to your Automatic Encryption Shared Library
   }

   autoEncryptionOptions := options.AutoEncryption().
   	SetKeyVaultNamespace(keyVaultNamespace).
   	SetKmsProviders(kmsProviderCredentials).
   	SetExtraOptions(cryptSharedLibraryPath)
   ```

5. Create a Client to Set Up an Encrypted Collection

   To create a client used to encrypt and decrypt data in your collection, instantiate a new `MongoClient` by using your connection URI and your automatic encryption options.

   ```go
   opts := options.Client().
   	ApplyURI(uri).
   	SetAutoEncryptionOptions(autoEncryptionOptions)
   encryptedClient, err := mongo.Connect(opts)

   if err != nil {
   	panic(fmt.Sprintf("Unable to connect to MongoDB: %v\n", err))
   }
   defer func() {
   	_ = encryptedClient.Disconnect(context.TODO())
   }()
   ```

### Full Application Code

To see the complete code for the sample application, select your programming language in the language selector.

[Complete C# Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/csharp/)

Each sample application repository includes a `README.md` file that you can use to learn how to set up your environment and run the application.

1. Assign application variables

   The code samples in this tutorial use the following variables to perform the Queryable Encryption workflow:

   - **kmsProviderName** - The KMS you use to store your Customer Master Key. Set this to your key provider: `"aws"`, `"azure"`, `"gcp"`, or `"kmip"`.

   - **keyVaultDatabaseName** - The MongoDB database where your data encryption keys (DEKs) will be stored. Set `keyVaultDatabaseName` to `"encryption"`.

   - **keyVaultCollectionName** - The collection in MongoDB where your DEKs will be stored. Set `keyVaultCollectionName` to `"__keyVault"`.

   - **keyVaultNamespace** - The namespace in MongoDB where your DEKs will be stored. Set `keyVaultNamespace` to a new `CollectionNamespace` object whose name is the values of the `keyVaultDatabaseName` and `keyVaultCollectionName` variables, separated by a period.

   - **encryptedDatabaseName** - The MongoDB database where your encrypted data will be stored. Set `encryptedDatabaseName` to `"medicalRecords"`.

   - **encryptedCollectionName** - The collection in MongoDB where your encrypted data will be stored. Set `encryptedCollectionName` to `"patients"`.

   - **uri** - Your MongoDB deployment connection URI. Set your connection URI in the `appsettings.json` file or replace the value directly.

   You can declare these variables by using the following code:

   ```csharp
   const string kmsProviderName = "<your KMS provider name>";
   const string keyVaultDatabaseName = "encryption";
   const string keyVaultCollectionName = "__keyVault";
   var keyVaultNamespace =
       CollectionNamespace.FromFullName($"{keyVaultDatabaseName}.{keyVaultCollectionName}");
   const string encryptedDatabaseName = "medicalRecords";
   const string encryptedCollectionName = "patients";
   var appSettings = new ConfigurationBuilder().AddJsonFile("appsettings.json").Build();
   var uri = appSettings["MongoDbUri"];
   ```

   **Important: Key Vault Collection Namespace Permissions**

   The Key Vault collection is in the `encryption.__keyVault` namespace. Ensure that the database user your application uses to connect to MongoDB has [ReadWrite](/docs/manual/reference/built-in-roles#std-label-manual-reference-role-read-write) permissions on this namespace.

   **Tip: Environment Variables**

   The sample code in this tutorial references environment variables that you need to set. Alternatively, you can replace the values directly in the code.

   To learn how you can setup these environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/csharp/README.md) file included in the sample application on GitHub.

2. Add your KMS credentials

   Create a variable containing your KMS credentials with the following structure. Use the Access Key ID and Secret Access Key you used in step 2.2 when you [created an AWS IAM user.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-create-aws-iam-user)

   ```csharp
   var kmsProviderCredentials = new Dictionary<string, IReadOnlyDictionary<string, object>>();
   var kmsOptions = new Dictionary<string, object>
   {
       { "accessKeyId", _appSettings["Aws:AccessKeyId"] }, // Your AWS access key ID
       { "secretAccessKey", _appSettings["Aws:SecretAccessKey"] } // Your AWS secret access key
   };
   kmsProviderCredentials.Add("aws", kmsOptions);
   ```

   You can also provide a custom name for your KMS provider by passing in a string that includes the name of the KMS provider, followed by a colon and the custom name. Providing a unique name for a KMS provider allows you to specify multiple KMS providers of the same type.

   For example, you can name your AWS KMS provider "my\_aws\_provider" in your KMS credentials variable as shown in the following code:

   ```csharp
   var kmsProviderCredentials = new Dictionary<string, IReadOnlyDictionary<string, object>>();
   var kmsOptions = new Dictionary<string, object>
       {
           { "accessKeyId", _appSettings["Aws:AccessKeyId"] }, // Your AWS access key ID
           { "secretAccessKey", _appSettings["Aws:SecretAccessKey"] } // Your AWS secret access key
       };
   kmsProviderCredentials.Add("aws:my_aws_provider", kmsOptions);
   ```

   NOTE: The remaining steps in this tutorial use the default KMS provider string, `"aws"`.

   **Important: Reminder: Authenticate with IAM Roles in Production**

   To use an IAM (Identity and Access Management) role instead of an IAM (Identity and Access Management) user to authenticate your application, specify an empty object for your credentials in your KMS provider object. This instructs the driver to automatically retrieve the credentials from the environment:

   ```csharp
   kmsProviderCredentials.Add("aws", new Dictionary<string, object>);
   ```

   You cannot automatically retrieve credentials if you are using a named KMS provider.

3. Add your CMK credentials

   Create a variable containing your Customer Master Key credentials with the following structure. Use the ARN (Amazon Resource Name) and Region you recorded in step 1.3 when you [created a CMK.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-create-cmk-aws)

   ```csharp
   var customerMasterKeyCredentials = new BsonDocument
   {
       { "key", _appSettings["Aws:KeyArn"] }, // Your AWS Key ARN
       { "region", _appSettings["Aws:KeyRegion"] } // Your AWS Key Region
   };
   ```

4. Set automatic encryption options

   **Note: Automatic Encryption Options**

   The automatic encryption options provide configuration information to the Automatic Encryption Shared Library, which modifies the application's behavior when accessing encrypted fields.

   To learn more about the Automatic Encryption Shared Library, see the [Automatic Encryption Shared Library](/docs/manual/core/queryable-encryption/install-library#std-label-qe-reference-shared-library) page.

   Create an `AutoEncryptionOptions` object with the following options:

   - The namespace of your Key Vault collection

   - The `kmsProviderCredentials` object, which contains your AWS KMS credentials

   - The `extraOptions` object, which contains the path to your Automatic Encryption Shared Library

   ```csharp
   var extraOptions = new Dictionary<string, object>
   {
       { "cryptSharedLibPath", _appSettings["CryptSharedLibPath"] } // Path to your Automatic Encryption Shared Library
   };

   var autoEncryptionOptions = new AutoEncryptionOptions(
       keyVaultNamespace,
       kmsProviderCredentials,
       extraOptions: extraOptions);
   ```

5. Create a Client to Set Up an Encrypted Collection

   To create a client used to encrypt and decrypt data in your collection, instantiate a new `MongoClient` by using your connection URI and your automatic encryption options.

   IMPORTANT: If you are using the .NET/C# driver version 3.0 or later, you must add the following code to your application before instantiating a new `MongoClient`:

   ```csharp
   MongoClientSettings.Extensions.AddAutoEncryption(); // .NET/C# Driver v3.0 or later only
   ```

   Instantiate a new `MongoClient` by using your connection URI and automatic encryption options:

   ```csharp
   var clientSettings = MongoClientSettings.FromConnectionString(uri);
   clientSettings.AutoEncryptionOptions = qeHelpers.GetAutoEncryptionOptions(
       keyVaultNamespace,
       kmsProviderCredentials);

   var encryptedClient = new MongoClient(clientSettings);
   ```

### Full Application Code

To see the complete code for the sample application, select your programming language in the language selector.

[Complete Rust Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/rust/)

Each sample application repository includes a `README.md` file that you can use to learn how to set up your environment and run the application.

1. Assign application variables

   The code samples in this tutorial use the following variables to perform the Queryable Encryption workflow:

   - **kms\_provider\_name** - The KMS you're using to store your Customer Master Key. Set this variable to `"local"` for this tutorial.

   - **uri** - Your MongoDB deployment connection URI. Set your connection URI in the `MONGODB_URI` environment variable.

   - **key\_vault\_database\_name** - The database in MongoDB where your data encryption keys (DEKs) will be stored. Set this variable to `"encryption"`.

   - **key\_vault\_collection\_name** - The collection in MongoDB where your DEKs will be stored. Set this variable to `"__keyVault"`, which is the convention to help prevent mistaking it for a user collection.

   - **key\_vault\_namespace** - The namespace in MongoDB where your DEKs will be stored. Set this variable to a `Namespace` struct and pass the values of the `key_vault_database_name` and `key_vault_collection_name` variables.

   - **encrypted\_database\_name** - The database in MongoDB where your encrypted data will be stored. Set this variable to `"medicalRecords"`.

   - **encrypted\_collection\_name** - The collection in MongoDB where your encrypted data will be stored. Set this variable to `"patients"`.

   You can declare these variables by using the following code:

   ```rust
   let kms_provider_name = "<KMS provider name>";
   let uri = env::var("MONGODB_URI").expect("Set MONGODB_URI environment variable to your connection string");
   let key_vault_database_name = "encryption";
   let key_vault_collection_name = "__keyVault";
   let key_vault_namespace = Namespace::new(key_vault_database_name, key_vault_collection_name);
   let encrypted_database_name = "medicalRecords";
   let encrypted_collection_name = "patients";
   ```

   **Important: Key Vault Collection Namespace Permissions**

   The Key Vault collection is in the `encryption.__keyVault` namespace. Ensure that the database user your application uses to connect to MongoDB has [ReadWrite](/docs/manual/reference/built-in-roles#std-label-manual-reference-role-read-write) permissions on this namespace.

   **Tip: Environment Variables**

   The sample code in this tutorial references environment variables that you need to set. Alternatively, you can replace the values directly in the code.

   To learn how you can setup these environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/rust/README.md) file included in the sample application on GitHub.

2. Add your KMS credentials

   Create a variable containing your KMS credentials with the following structure. Use the Access Key ID and Secret Access Key you used in step 2.2 when you [created an AWS IAM user.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-create-aws-iam-user)

   ```rust
   kms_providers = vec![(
       KmsProvider::aws(),
       doc! {
           "accessKeyId": env::var("AWS_ACCESS_KEY_ID").expect("Set AWS_ACCESS_KEY_ID environment variable"),
           "secretAccessKey": env::var("AWS_SECRET_ACCESS_KEY").expect("Set AWS_SECRET_ACCESS_KEY environment variable"),
       },
       None,
   )];
   ```

   You can also provide a custom name for your KMS provider by passing the name as a string to the `with_name()` function. Providing a unique name for a KMS provider allows you to specify multiple KMS providers of the same type.

   For example, you can name your AWS KMS provider "my\_aws\_provider" in your KMS credentials variable as shown in the following code:

   ```rust
   kms_providers = vec![(
       KmsProvider::aws().with_name("my_aws_provider"),
       doc! {
           "accessKeyId": env::var("AWS_ACCESS_KEY_ID").expect("Set AWS_ACCESS_KEY_ID environment variable"),
           "secretAccessKey": env::var("AWS_SECRET_ACCESS_KEY").expect("Set AWS_SECRET_ACCESS_KEY environment variable"),
       },
       None,
   )];
   ```

   NOTE: The remaining steps in this tutorial use the default KMS provider string, `"aws"`.

   **Important: Reminder: Authenticate with IAM Roles in Production**

   To use an IAM (Identity and Access Management) role instead of an IAM (Identity and Access Management) user to authenticate your application, specify an empty object for your credentials in your KMS provider object. This instructs the driver to automatically retrieve the credentials from the environment:

   ```rust
   kms_providers = vec![(
       KmsProvider::aws(),
       doc! {},
       None,
   )];
   ```

   You cannot automatically retrieve credentials if you are using a named KMS provider.

3. Add your CMK credentials

   Create a variable containing your Customer Master Key credentials with the following structure. Use the ARN (Amazon Resource Name) and Region you recorded in step 1.3 when you [created a CMK.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-create-cmk-aws)

   ```rust
   let aws_master_key = AwsMasterKey::builder()
       .key(env::var("AWS_KEY_ARN").expect("Set the AWS_KEY_ARN environment variable"))
       .region(env::var("AWS_KEY_REGION").expect("Set the AWS_KEY_REGION environment variable"))
       .build();
   ```

4. Set automatic encryption options

   **Note: Automatic Encryption Options**

   The automatic encryption options provide configuration information to the Automatic Encryption Shared Library, which modifies the application's behavior when accessing encrypted fields.

   To learn more about the Automatic Encryption Shared Library, see the [Automatic Encryption Shared Library](/docs/manual/core/queryable-encryption/install-library#std-label-qe-reference-shared-library) page.

   Create an `EncryptedClientBuilder` object that contains the following options:

   - A `ClientOptions` object

   - The namespace of your Key Vault collection

   - The `kms_providers` object, which contains your AWS KMS credentials

   ```rust
   let client_options = ClientOptions::parse(uri).await.expect("Unable to parse MONGODB_URI");

   let encrypted_client_builder = Client::encrypted_builder(
       client_options,
       key_vault_namespace.clone(),
       kms_providers.clone()
   ).expect("");
   ```

5. Create a Client to Set Up an Encrypted Collection

   To create a client used to encrypt and decrypt data in your collection, instantiate a new `MongoClient` by using your connection URI and your automatic encryption options.

   ```rust
   let encrypted_client = encrypted_client_builder
       .extra_options(Some(doc!{
           "cryptSharedLibPath": env::var("SHARED_LIB_PATH").expect("Set SHARED_LIB_PATH environment variable to path to crypt_shared library")
       }))
       .key_vault_client(Client::with_uri_str(uri).await.unwrap())
       .build()
       .await
       .unwrap();
   ```

### Full Application Code

To see the complete code for the sample application, select your programming language in the language selector.

[Complete PHP Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/php/)

Each sample application repository includes a `README.md` file that you can use to learn how to set up your environment and run the application.

1. Assign application variables

   The code samples in this tutorial use the following variables to perform the Queryable Encryption workflow:

   - **$kmsProviderName** - The KMS you're using to store your Customer Master Key. Set the `KMS_PROVIDER` environment variable to your key provider: `'aws'`, `'azure'`, `'gcp'`, or `'kmip'`.

   - **$uri** - Your MongoDB deployment connection URI. Set your connection URI in the `MONGODB_URI` environment variable.

   - **$keyVaultDatabaseName** - The database in MongoDB where your data encryption keys (DEKs) will be stored. Set the value of `$keyVaultDatabaseName` to `'encryption'`.

   - **$keyVaultCollectionName** - The collection in MongoDB where your DEKs will be stored. Set this variable to `'__keyVault'`, which is the convention to help prevent mistaking it for a user collection.

   - **$keyVaultNamespace** - The namespace in MongoDB where your DEKs will be stored. Set this variable to the values of the `$keyVaultDatabaseName` and `$keyVaultCollectionName` variables, separated by a period.

   - **$encryptedDatabaseName** - The database in MongoDB where your encrypted data will be stored. Set this variable to `'medicalRecords'`.

   - **$encryptedCollectionName** - The collection in MongoDB where your encrypted data will be stored. Set this variable to `'patients'`.

   You can declare these variables by using the following code:

   ```php
   $kmsProviderName = getenv('KMS_PROVIDER');
   $uri = getenv('MONGODB_URI'); // Your connection URI
   $keyVaultDatabaseName = 'encryption';
   $keyVaultCollectionName = '__keyVault';
   $keyVaultNamespace = $keyVaultDatabaseName . '.' . $keyVaultCollectionName;
   $encryptedDatabaseName = 'medicalRecords';
   $encryptedCollectionName = 'patients';
   ```

   **Important: Key Vault Collection Namespace Permissions**

   The Key Vault collection is in the `encryption.__keyVault` namespace. Ensure that the database user your application uses to connect to MongoDB has [ReadWrite](/docs/manual/reference/built-in-roles#std-label-manual-reference-role-read-write) permissions on this namespace.

   **Tip: Environment Variables**

   The sample code in this tutorial references environment variables that you need to set. Alternatively, you can replace the values directly in the code.

   To learn how you can setup these environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/php/README.md) file included in the sample application on GitHub.

2. Add your KMS credentials

   Create a variable containing your KMS credentials with the following structure. Use the Access Key ID and Secret Access Key you used in step 2.2 when you [created an AWS IAM user.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-create-aws-iam-user)

   ```php
   $kmsProviders = [
       'aws' => [
           'accessKeyId' => getenv('AWS_ACCESS_KEY_ID'), // Your AWS access key ID
           'secretAccessKey' => getenv('AWS_SECRET_ACCESS_KEY'), // Your AWS secret access key
       ],
   ];
   ```

   You can also provide a custom name for your KMS provider by passing in a string that includes the name of the KMS provider, followed by a colon and the custom name. Providing a unique name for a KMS provider allows you to specify multiple KMS providers of the same type.

   For example, you can name your AWS KMS provider 'my\_aws\_provider' in your KMS credentials variable as shown in the following code:

   ```php
   $kmsProviders = [
       'aws:my_aws_provider' => [
           'accessKeyId' => getenv('AWS_ACCESS_KEY_ID'), // Your AWS access key ID
           'secretAccessKey' => getenv('AWS_SECRET_ACCESS_KEY'), // Your AWS secret access key
       ],
   ];
   ```

   NOTE: The remaining steps in this tutorial use the default KMS provider string, `"aws"`.

   **Important: Reminder: Authenticate with IAM Roles in Production**

   To use an IAM (Identity and Access Management) role instead of an IAM (Identity and Access Management) user to authenticate your application, specify an empty object for your credentials in your KMS provider object. This instructs the driver to automatically retrieve the credentials from the environment:

   ```php
   $kmsProviders = [
      'aws' => [],
   ];
   ```

   You cannot automatically retrieve credentials if you are using a named KMS provider.

3. Add your CMK credentials

   Create a variable containing your Customer Master Key credentials with the following structure. Use the ARN (Amazon Resource Name) and Region you recorded in step 1.3 when you [created a CMK.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-create-cmk-aws)

   ```php
   $customerMasterKeyCredentials = [
       'key' => getenv('AWS_KEY_ARN'), // Your AWS key ARN
       'region' => getenv('AWS_REGION'), // Your AWS region
   ];
   ```

4. Set automatic encryption options

   **Note: Automatic Encryption Options**

   The automatic encryption options provide configuration information to the Automatic Encryption Shared Library, which modifies the application's behavior when accessing encrypted fields.

   To learn more about the Automatic Encryption Shared Library, see the [Automatic Encryption Shared Library](/docs/manual/core/queryable-encryption/install-library#std-label-qe-reference-shared-library) page.

   Create an `$autoEncryptionOptions` object that contains the following options:

   - The namespace of your Key Vault collection

   - The `$kmsProviders` object, defined in the previous step

   - The path to your Automatic Encryption Shared Library

   ```php
   $autoEncryptionOptions = [
       'keyVaultNamespace' => $keyVaultNamespace,
       'kmsProviders' => $kmsProviders,
       'extraOptions' => [
           'cryptSharedLibPath' => getenv('SHARED_LIB_PATH'), // Path to your Automatic Encryption Shared Library
       ],
   ];
   ```

5. Create a Client to Set Up an Encrypted Collection

   To create a client used to encrypt and decrypt data in your collection, instantiate a new `MongoClient` by using your connection URI and your automatic encryption options.

   ```php
   $encryptedClient = new \MongoDB\Client($uri, [], [
       'autoEncryption' => $autoEncryptionOptions,
   ]);
   ```

### Full Application Code

To see the complete code for the sample application, select your programming language in the language selector.

[Complete Ruby Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/ruby/)

Each sample application repository includes a `README.md` file that you can use to learn how to set up your environment and run the application.

1. Assign application variables

   The code samples in this tutorial use the following variables to perform the Queryable Encryption workflow:

   - **kms\_provider\_name** - The KMS you use to store your Customer Master Key. Set this to your key provider: `"aws"`, `"azure"`, `"gcp"`, or `"kmip"`.

   - **uri** - Your MongoDB deployment connection URI. Set your connection URI in the `MONGODB_URI` environment variable or replace the value directly.

   - **key\_vault\_database\_name** - The MongoDB database where your data encryption keys (DEKs) will be stored. Set this to `"encryption"`.

   - **key\_vault\_collection\_name** - The collection in MongoDB where your DEKs will be stored. Set this to `"__keyVault"`, which is the convention to help prevent mistaking it for a user collection.

   - **key\_vault\_namespace** - The namespace in MongoDB where your DEKs will be stored. Set this to the values of the `key_vault_database_name` and `key_vault_collection_name` variables separated by a period, in the format `"#{key_vault_database_name}.#{key_vault_collection_name}"`.

   - **encrypted\_database\_name** - The MongoDB database where your encrypted data will be stored. Set this to `"medicalRecords"`.

   - **encrypted\_collection\_name** - The collection in MongoDB where your encrypted data will be stored. Set this to `"patients"`.

   You can declare these variables by using the following code:

   ```ruby
   kms_provider_name = ENV["KMS_PROVIDER"]
   uri = ENV["MONGODB_URI"] # Your connection URI
   key_vault_database_name = "encryption"
   key_vault_collection_name = "__keyVault"
   key_vault_namespace = "#{key_vault_database_name}.#{key_vault_collection_name}"
   encrypted_database_name = "medicalRecords"
   encrypted_collection_name = "patients"
   ```

   **Important: Key Vault Collection Namespace Permissions**

   The Key Vault collection is in the `encryption.__keyVault` namespace. Ensure that the database user your application uses to connect to MongoDB has [ReadWrite](/docs/manual/reference/built-in-roles#std-label-manual-reference-role-read-write) permissions on this namespace.

   **Tip: Environment Variables**

   The sample code in this tutorial references environment variables that you need to set. Alternatively, you can replace the values directly in the code.

   To learn how you can setup these environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/ruby/README.md) file included in the sample application on GitHub.

2. Add your KMS credentials

   Create a variable containing your KMS credentials with the following structure. Use the Access Key ID and Secret Access Key that you used in step 2.2 when you [created an AWS IAM user.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-create-aws-iam-user)

   ```ruby
   kms_providers = {
     aws: {
       accessKeyId: ENV["AWS_ACCESS_KEY_ID"], # Your AWS access key ID
       secretAccessKey: ENV["AWS_SECRET_ACCESS_KEY"] # Your AWS secret access key
     }
   }
   ```

   **Important: Reminder: Authenticate with IAM Roles in Production**

   To use an IAM (Identity and Access Management) role instead of an IAM (Identity and Access Management) user to authenticate your application, specify an empty hash for your credentials in your KMS provider hash. This instructs the driver to automatically retrieve the credentials from the environment:

   ```ruby
   kms_provider_credentials = {
     aws: {}
   }
   ```

   You cannot automatically retrieve credentials if you are using a named KMS provider.

3. Add your CMK credentials

   Create a variable containing your Customer Master Key credentials with the following structure. Use the ARN (Amazon Resource Name) and Region you recorded in step 1.3 when you [created a CMK.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-create-cmk-aws)

   ```ruby
   customer_master_key_credentials = {
     key: ENV["AWS_KEY_ARN"], # Your AWS Key ARN
     region: ENV["AWS_KEY_REGION"] # Your AWS Key Region
   }
   ```

4. Set automatic encryption options

   **Note: Automatic Encryption Options**

   The automatic encryption options provide configuration information to the Automatic Encryption Shared Library, which modifies the application's behavior when accessing encrypted fields.

   To learn more about the Automatic Encryption Shared Library, see the [Automatic Encryption Shared Library](/docs/manual/core/queryable-encryption/install-library#std-label-qe-reference-shared-library) page.

   Create an `auto_encryption_options` hash that contains the following options:

   - The namespace of your Key Vault collection

   - The `kms_providers` hash, which contains your AWS KMS credentials

   - The path to your Automatic Encryption Shared Library

   ```ruby
   auto_encryption_options = {
     key_vault_namespace: key_vault_namespace,
     kms_providers: kms_providers,
     extra_options: {
       crypt_shared_lib_path: ENV["SHARED_LIB_PATH"] # Path to your Automatic Encryption Shared Library
     }
   }
   ```

5. Create a Client to Set Up an Encrypted Collection

   To create a client used to encrypt and decrypt data in your collection, instantiate a new `Mongo::Client` by using your connection URI and your automatic encryption options.

   ```ruby
   encrypted_client = Mongo::Client.new(uri, auto_encryption_options: auto_encryption_options)
   ```

### Full Application Code

To see the complete code for the sample application, select your programming language in the language selector.

[Complete mongosh Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/mongosh/)

Each sample application repository includes a `README.md` file that you can use to learn how to set up your environment and run the application.

1. Assign application variables

   The code samples in this tutorial use the following variables to perform the Queryable Encryption workflow:

   - **kmsProviderName** - The KMS you use to store your Customer Master Key. Set this to your key provider: `"aws"`, `"azure"`, `"gcp"`, or `"kmip"`.

   - **uri** - Your MongoDB deployment connection URI. Set your connection URI in the `MONGODB_URI` environment variable or replace the value directly.

   - **keyVaultDatabaseName** - The MongoDB database where your data encryption keys (DEKs) will be stored. Set this to `"encryption"`.

   - **keyVaultCollectionName** - The collection in MongoDB where your DEKs will be stored. Set this to `"__keyVault"`.

   - **keyVaultNamespace** - The namespace in MongoDB where your DEKs will be stored. Set this to the values of the `keyVaultDatabaseName` and `keyVaultCollectionName` variables, separated by a period.

   - **encryptedDatabaseName** - The MongoDB database where your encrypted data will be stored. Set this to `"medicalRecords"`.

   - **encryptedCollectionName** - The collection in MongoDB where your encrypted data will be stored. Set this to `"patients"`.

   You can declare these variables by using the following code:

   ```javascript
   const kmsProviderName = "<Your KMS Provider Name>";
   const uri = process.env.MONGODB_URI; // Your connection URI
   const keyVaultDatabaseName = "encryption";
   const keyVaultCollectionName = "__keyVault";
   const keyVaultNamespace = `${keyVaultDatabaseName}.${keyVaultCollectionName}`;
   const encryptedDatabaseName = "medicalRecords";
   const encryptedCollectionName = "patients";
   ```

   **Important: Key Vault Collection Namespace Permissions**

   The Key Vault collection is in the `encryption.__keyVault` namespace. Ensure that the database user your application uses to connect to MongoDB has [ReadWrite](/docs/manual/reference/built-in-roles#std-label-manual-reference-role-read-write) permissions on this namespace.

   **Tip: Environment Variables**

   The sample code in this tutorial references environment variables that you need to set. Alternatively, you can replace the values directly in the code.

   To learn how you can setup these environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/node/README.md) file included in the sample application on GitHub.

2. Add your KMS credentials

   Create a variable containing your KMS credentials with the following structure. Use the Azure Key Vault credentials you recorded when you [registered your application with Azure.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-register-cmk-azure)

   ```javascript
   kmsProviderCredentials = {
     azure: {
       tenantId: process.env["AZURE_TENANT_ID"], // Your Azure tenant ID
       clientId: process.env["AZURE_CLIENT_ID"], // Your Azure client ID
       clientSecret: process.env["AZURE_CLIENT_SECRET"], // Your Azure client secret
     },
   };
   ```

   You can also provide a custom name for your KMS provider by passing in a string that includes the name of the KMS provider, followed by a colon and the custom name. Providing a unique name for a KMS provider allows you to specify multiple KMS providers of the same type.

   For example, you can name your Azure KMS provider "my\_azure\_provider" in your KMS credentials variable as shown in the following code:

   ```javascript
   kmsProviderCredentials = {
     "azure:my_azure_provider": {
       tenantId: process.env["AZURE_TENANT_ID"], // Your Azure tenant ID
       clientId: process.env["AZURE_CLIENT_ID"], // Your Azure client ID
       clientSecret: process.env["AZURE_CLIENT_SECRET"], // Your Azure client secret
     },
   };

   ```

   NOTE: The remaining steps in this tutorial use the default KMS provider string, `"azure"`.

3. Add your CMK credentials

   Create a variable containing your Customer Master Key credentials with the following structure. Use the CMK details you recorded when you [created a CMK.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-create-cmk-azure)

   ```javascript
   customerMasterKeyCredentials = {
     keyVaultEndpoint: process.env["AZURE_KEY_VAULT_ENDPOINT"], // Your Azure Key Vault Endpoint
     keyName: process.env["AZURE_KEY_NAME"], // Your Azure Key Name
   };
   ```

4. Create an encryption client

   To create a client for encrypting and decrypting data in encrypted collections, instantiate a new `MongoClient` using your connection URI and automatic encryption options.

   ```javascript
   const encryptedClient = Mongo(uri, autoEncryptionOptions);
   ```

### Full Application Code

To see the complete code for the sample application, select your programming language in the language selector.

[Complete Node.js Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/node/)

Each sample application repository includes a `README.md` file that you can use to learn how to set up your environment and run the application.

1. Assign application variables

   The code samples in this tutorial use the following variables to perform the Queryable Encryption workflow:

   - **kmsProviderName** - The KMS you use to store your Customer Master Key. Set this to your key provider: `"aws"`, `"azure"`, `"gcp"`, or `"kmip"`.

   - **uri** - Your MongoDB deployment connection URI. Set your connection URI in the `MONGODB_URI` environment variable or replace the value directly.

   - **keyVaultDatabaseName** - The MongoDB database where your data encryption keys (DEKs) will be stored. Set this to `"encryption"`.

   - **keyVaultCollectionName** - The collection in MongoDB where your DEKs will be stored. Set this to `"__keyVault"`.

   - **keyVaultNamespace** - The namespace in MongoDB where your DEKs will be stored. Set this to the values of the `keyVaultDatabaseName` and `keyVaultCollectionName` variables, separated by a period.

   - **encryptedDatabaseName** - The MongoDB database where your encrypted data will be stored. Set this to `"medicalRecords"`.

   - **encryptedCollectionName** - The collection in MongoDB where your encrypted data will be stored. Set this to `"patients"`.

   You can declare these variables by using the following code:

   ```javascript
   const kmsProviderName = "<Your KMS Provider Name>";

   const uri = process.env.MONGODB_URI; // Your connection URI

   const keyVaultDatabaseName = "encryption";
   const keyVaultCollectionName = "__keyVault";
   const keyVaultNamespace = `${keyVaultDatabaseName}.${keyVaultCollectionName}`;
   const encryptedDatabaseName = "medicalRecords";
   const encryptedCollectionName = "patients";
   ```

   **Important: Key Vault Collection Namespace Permissions**

   The Key Vault collection is in the `encryption.__keyVault` namespace. Ensure that the database user your application uses to connect to MongoDB has [ReadWrite](/docs/manual/reference/built-in-roles#std-label-manual-reference-role-read-write) permissions on this namespace.

   **Tip: Environment Variables**

   The sample code in this tutorial references environment variables that you need to set. Alternatively, you can replace the values directly in the code.

   To learn how you can setup these environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/node/README.md) file included in the sample application on GitHub.

2. Add your KMS credentials

   Create a variable containing your KMS credentials with the following structure. Use the Azure Key Vault credentials you recorded when you [registered your application with Azure.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-register-cmk-azure)

   ```javascript
   kmsProviders = {
     azure: {
       tenantId: process.env.AZURE_TENANT_ID, // Your Azure tenant ID
       clientId: process.env.AZURE_CLIENT_ID, // Your Azure client ID
       clientSecret: process.env.AZURE_CLIENT_SECRET, // Your Azure client secret
     },
   };
   ```

   You can also provide a custom name for your KMS provider by passing in a string that includes the name of the KMS provider, followed by a colon and the custom name. Providing a unique name for a KMS provider allows you to specify multiple KMS providers of the same type.

   For example, you can name your Azure KMS provider "my\_azure\_provider" in your KMS credentials variable as shown in the following code:

   ```javascript
   kmsProviderCredentials = {
     "azure:my_azure_provider": {
       tenantId: process.env.AZURE_TENANT_ID, // Your Azure tenant ID
       clientId: process.env.AZURE_CLIENT_ID, // Your Azure client ID
       clientSecret: process.env.AZURE_CLIENT_SECRET, // Your Azure client secret
     },
   };

   ```

   NOTE: The remaining steps in this tutorial use the default KMS provider string, `"azure"`.

3. Add your CMK credentials

   Create a variable containing your Customer Master Key credentials with the following structure. Use the CMK details you recorded when you [created a CMK.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-create-cmk-azure)

   ```javascript
   customerMasterKeyCredentials = {
     keyVaultEndpoint: process.env.AZURE_KEY_VAULT_ENDPOINT, // Your Azure Key Vault Endpoint
     keyName: process.env.AZURE_KEY_NAME, // Your Azure Key Name
   };
   ```

4. Create an encryption client

   To create a client for encrypting and decrypting data in encrypted collections, instantiate a new `MongoClient` using your connection URI and automatic encryption options.

   ```javascript
   const encryptedClient = new MongoClient(uri, {
     autoEncryption: autoEncryptionOptions,
   });
   ```

### Full Application Code

To see the complete code for the sample application, select your programming language in the language selector.

[Complete Python Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/python/)

Each sample application repository includes a `README.md` file that you can use to learn how to set up your environment and run the application.

1. Assign application variables

   The code samples in this tutorial use the following variables to perform the Queryable Encryption workflow:

   - **kms\_provider\_name** - The KMS you use to store your Customer Master Key. Set this to your key provider: `"aws"`, `"azure"`, `"gcp"`, or `"kmip"`.

   - **uri** - Your MongoDB deployment connection URI. Set your connection URI in the `MONGODB_URI` environment variable or replace the value directly.

   - **key\_vault\_database\_name** - The MongoDB database where your data encryption keys (DEKs) will be stored. Set this to `"encryption"`.

   - **key\_vault\_collection\_name** - The collection in MongoDB where your DEKs will be stored. Set this to `"__keyVault"`.

   - **key\_vault\_namespace** - The namespace in MongoDB where your DEKs will be stored. Set this to the values of the `key_vault_database_name` and `key_vault_collection_name` variables, separated by a period.

   - **encrypted\_database\_name** - The MongoDB database where your encrypted data will be stored. Set this to `"medicalRecords"`.

   - **encrypted\_collection\_name** - The collection in MongoDB where your encrypted data will be stored. Set this to `"patients"`.

   You can declare these variables by using the following code:

   ```python
   kms_provider_name = "<KMS provider name>"
   uri = os.environ.get("MONGODB_URI", "mongodb://127.0.0.1:27017")  # Your connection URI
   key_vault_database_name = "encryption"
   key_vault_collection_name = "__keyVault"
   key_vault_namespace = f"{key_vault_database_name}.{key_vault_collection_name}"
   encrypted_database_name = "medicalRecords"
   encrypted_collection_name = "patients"
   ```

   **Important: Key Vault Collection Namespace Permissions**

   The Key Vault collection is in the `encryption.__keyVault` namespace. Ensure that the database user your application uses to connect to MongoDB has [ReadWrite](/docs/manual/reference/built-in-roles#std-label-manual-reference-role-read-write) permissions on this namespace.

   **Tip: Environment Variables**

   The sample code in this tutorial references environment variables that you need to set. Alternatively, you can replace the values directly in the code.

   To learn how you can setup these environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/python/README.md) file included in the sample application on GitHub.

2. Add your KMS credentials

   Create a variable containing your KMS credentials with the following structure. Use the Azure Key Vault credentials you recorded when you [registered your application with Azure.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-register-cmk-azure)

   ```python
   kms_provider_credentials = {
       "azure": {
           "tenantId": os.environ['AZURE_TENANT_ID'], # Your Azure tenant ID
           "clientId": os.environ['AZURE_CLIENT_ID'], # Your Azure client ID
           "clientSecret": os.environ['AZURE_CLIENT_SECRET'] # Your Azure client secret
       }
   }
   ```

   You can also provide a custom name for your KMS provider by passing in a string that includes the name of the KMS provider, followed by a colon and the custom name. Providing a unique name for a KMS provider allows you to specify multiple KMS providers of the same type.

   For example, you can name your Azure KMS provider "my\_azure\_provider" in your KMS credentials variable as shown in the following code:

   ```python
   kms_provider_credentials = {
       "azure:my_azure_provider": {
           "tenantId": os.environ['AZURE_TENANT_ID'], # Your Azure tenant ID
           "clientId": os.environ['AZURE_CLIENT_ID'], # Your Azure client ID
           "clientSecret": os.environ['AZURE_CLIENT_SECRET'] # Your Azure client secret
       }
   }
   ```

   NOTE: The remaining steps in this tutorial use the default KMS provider string, `"azure"`.

3. Add your CMK credentials

   Create a variable containing your Customer Master Key credentials with the following structure. Use the CMK details you recorded when you [created a CMK.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-create-cmk-azure)

   ```python
   customer_master_key_credentials = {
       "keyName": os.environ['AZURE_KEY_NAME'], # Your Azure key name
       "keyVaultEndpoint": os.environ['AZURE_KEY_VAULT_ENDPOINT'] # Your Azure key vault endpoint
   }
   ```

4. Create an encryption client

   To create a client for encrypting and decrypting data in encrypted collections, instantiate a new `MongoClient` using your connection URI and automatic encryption options.

   ```python
   encrypted_client = MongoClient(
       uri, auto_encryption_opts=auto_encryption_options)
   ```

### Full Application Code

To see the complete code for the sample application, select your programming language in the language selector.

[Complete Java Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/java/)

Each sample application repository includes a `README.md` file that you can use to learn how to set up your environment and run the application.

1. Assign application variables

   The code samples in this tutorial use the following variables to perform the Queryable Encryption workflow:

   - **kmsProviderName** - The KMS you use to store your Customer Master Key. Set this to your key provider: `"aws"`, `"azure"`, `"gcp"`, or `"kmip"`.

   - **uri** - Your MongoDB deployment connection URI. Set your connection URI in the `MONGODB_URI` environment variable or replace the value directly.

   - **keyVaultDatabaseName** - The MongoDB database where your data encryption keys (DEKs) will be stored. Set this to `"encryption"`.

   - **keyVaultCollectionName** - The collection in MongoDB where your DEKs will be stored. Set this to `"__keyVault"`.

   - **keyVaultNamespace** - The namespace in MongoDB where your DEKs will be stored. Set this to the values of the `keyVaultDatabaseName` and `keyVaultCollectionName` variables, separated by a period.

   - **encryptedDatabaseName** - The MongoDB database where your encrypted data will be stored. Set this to `"medicalRecords"`.

   - **encryptedCollectionName** - The collection in MongoDB where your encrypted data will be stored. Set this to `"patients"`.

   You can declare these variables by using the following code:

   ```java
   String kmsProviderName = "<KMS provider name>";
   String uri = QueryableEncryptionHelpers.getEnv("MONGODB_URI"); // Your connection URI
   String keyVaultDatabaseName = "encryption";
   String keyVaultCollectionName = "__keyVault";
   String keyVaultNamespace = keyVaultDatabaseName + "." + keyVaultCollectionName;
   String encryptedDatabaseName = "medicalRecords";
   String encryptedCollectionName = "patients";
   ```

   **Important: Key Vault Collection Namespace Permissions**

   The Key Vault collection is in the `encryption.__keyVault` namespace. Ensure that the database user your application uses to connect to MongoDB has [ReadWrite](/docs/manual/reference/built-in-roles#std-label-manual-reference-role-read-write) permissions on this namespace.

   **Tip: Environment Variables**

   The sample code in this tutorial references environment variables that you need to set. Alternatively, you can replace the values directly in the code.

   To learn how you can setup these environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/java/README.md) file included in the sample application on GitHub.

2. Add your KMS credentials

   Create a variable containing your KMS credentials with the following structure. Use the Azure Key Vault credentials you recorded when you [registered your application with Azure.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-register-cmk-azure)

   ```java
   Map<String, Object> kmsProviderDetails = new HashMap<>();
   kmsProviderDetails.put("tenantId", getEnv("AZURE_TENANT_ID")); // Your Azure tenant ID
   kmsProviderDetails.put("clientId", getEnv("AZURE_CLIENT_ID")); // Your Azure client ID
   kmsProviderDetails.put("clientSecret", getEnv("AZURE_CLIENT_SECRET")); // Your Azure client secret

   Map<String, Map<String, Object>> kmsProviderCredentials = new HashMap<String, Map<String, Object>>();
   kmsProviderCredentials.put("azure", kmsProviderDetails);
   ```

   You can also provide a custom name for your KMS provider by passing in a string that includes the name of the KMS provider, followed by a colon and the custom name. Providing a unique name for a KMS provider allows you to specify multiple KMS providers of the same type.

   For example, you can name your Azure KMS provider "my\_azure\_provider" in your KMS credentials variable as shown in the following code:

   ```java
   Map<String, Object> kmsProviderDetails = new HashMap<>();
   kmsProviderDetails.put("tenantId", getEnv("AZURE_TENANT_ID")); // Your Azure tenant ID
   kmsProviderDetails.put("clientId", getEnv("AZURE_CLIENT_ID")); // Your Azure client ID
   kmsProviderDetails.put("clientSecret", getEnv("AZURE_CLIENT_SECRET")); // Your Azure client secret

   Map<String, Map<String, Object>> kmsProviderCredentials = new HashMap<String, Map<String, Object>>();
   kmsProviderCredentials.put("azure:my_azure_provider", kmsProviderDetails);
   ```

   NOTE: The remaining steps in this tutorial use the default KMS provider string, `"azure"`.

3. Add your CMK credentials

   Create a variable containing your Customer Master Key credentials with the following structure. Use the CMK details you recorded when you [created a CMK.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-create-cmk-azure)

   ```java
   BsonDocument customerMasterKeyCredentials = new BsonDocument();
   customerMasterKeyCredentials.put("provider", new BsonString(kmsProviderName));
   customerMasterKeyCredentials.put("keyName", new BsonString(getEnv("AZURE_KEY_NAME"))); // Your Azure Key Vault Endpoint
   customerMasterKeyCredentials.put("keyVaultEndpoint", new BsonString(getEnv("AZURE_KEY_VAULT_ENDPOINT"))); // Your Azure Key Name
   ```

4. Create an encryption client

   To create a client for encrypting and decrypting data in encrypted collections, instantiate a new `MongoClient` using your connection URI and automatic encryption options.

   ```java
   MongoClientSettings clientSettings = MongoClientSettings.builder()
           .applyConnectionString(new ConnectionString(uri))
           .autoEncryptionSettings(autoEncryptionSettings)
           .build();

   try (MongoClient encryptedClient = MongoClients.create(clientSettings)) {
   ```

### Full Application Code

To see the complete code for the sample application, select your programming language in the language selector.

[Complete Go Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/go/)

Each sample application repository includes a `README.md` file that you can use to learn how to set up your environment and run the application.

1. Assign application variables

   The code samples in this tutorial use the following variables to perform the Queryable Encryption workflow:

   - **kmsProviderName** - The KMS you use to store your Customer Master Key. Set this to your key provider: `"aws"`, `"azure"`, `"gcp"`, or `"kmip"`.

   - **uri** - Your MongoDB deployment connection URI. Set your connection URI in the `MONGODB_URI` environment variable or replace the value directly.

   - **keyVaultDatabaseName** - The MongoDB database where your data encryption keys (DEKs) will be stored. Set this to `"encryption"`.

   - **keyVaultCollectionName** - The collection in MongoDB where your DEKs will be stored. Set this to `"__keyVault"`.

   - **keyVaultNamespace** - The namespace in MongoDB where your DEKs will be stored. Set this to the values of the `keyVaultDatabaseName` and `keyVaultCollectionName` variables, separated by a period.

   - **encryptedDatabaseName** - The MongoDB database where your encrypted data will be stored. Set this to `"medicalRecords"`.

   - **encryptedCollectionName** - The collection in MongoDB where your encrypted data will be stored. Set this to `"patients"`.

   You can declare these variables by using the following code:

   ```go
   kmsProviderName := "<KMS provider name>"
   uri := os.Getenv("MONGODB_URI") // Your connection URI
   keyVaultDatabaseName := "encryption"
   keyVaultCollectionName := "__keyVault"
   keyVaultNamespace := keyVaultDatabaseName + "." + keyVaultCollectionName
   encryptedDatabaseName := "medicalRecords"
   encryptedCollectionName := "patients"
   ```

   **Important: Key Vault Collection Namespace Permissions**

   The Key Vault collection is in the `encryption.__keyVault` namespace. Ensure that the database user your application uses to connect to MongoDB has [ReadWrite](/docs/manual/reference/built-in-roles#std-label-manual-reference-role-read-write) permissions on this namespace.

   **Tip: Environment Variables**

   The sample code in this tutorial references environment variables that you need to set. Alternatively, you can replace the values directly in the code.

   To learn how you can setup these environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/go/README.md) file included in the sample application on GitHub.

2. Add your KMS credentials

   Create a variable containing your KMS credentials with the following structure. Use the Azure Key Vault credentials you recorded when you [registered your application with Azure.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-register-cmk-azure)

   ```go
   kmsProviderCredentials := map[string]map[string]interface{}{
   	"azure": {
   		"tenantId":     os.Getenv("AZURE_TENANT_ID"),     // Azure tenant ID
   		"clientId":     os.Getenv("AZURE_CLIENT_ID"),     // Azure client ID
   		"clientSecret": os.Getenv("AZURE_CLIENT_SECRET"), // Azure client secret
   	},
   }
   ```

3. Add your CMK credentials

   Create a variable containing your Customer Master Key credentials with the following structure. Use the CMK details you recorded when you [created a CMK.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-create-cmk-azure)

   ```go
   customerMasterKeyCredentials := map[string]string{
   	"keyVaultEndpoint": os.Getenv("AZURE_KEY_VAULT_ENDPOINT"), // Your Azure Key Vault Endpoint
   	"keyName":          os.Getenv("AZURE_KEY_NAME"),           // Your Azure Key Name
   }
   ```

4. Create an encryption client

   To create a client for encrypting and decrypting data in encrypted collections, instantiate a new `MongoClient` using your connection URI and automatic encryption options.

   ```go
   opts := options.Client().
   	ApplyURI(uri).
   	SetAutoEncryptionOptions(autoEncryptionOptions)
   encryptedClient, err := mongo.Connect(opts)

   if err != nil {
   	panic(fmt.Sprintf("Unable to connect to MongoDB: %v\n", err))
   }
   defer func() {
   	_ = encryptedClient.Disconnect(context.TODO())
   }()
   ```

### Full Application Code

To see the complete code for the sample application, select your programming language in the language selector.

[Complete C# Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/csharp/)

Each sample application repository includes a `README.md` file that you can use to learn how to set up your environment and run the application.

1. Assign application variables

   The code samples in this tutorial use the following variables to perform the Queryable Encryption workflow:

   - **kmsProviderName** - The KMS you use to store your Customer Master Key. Set this to your key provider: `"aws"`, `"azure"`, `"gcp"`, or `"kmip"`.

   - **keyVaultDatabaseName** - The MongoDB database where your data encryption keys (DEKs) will be stored. Set `keyVaultDatabaseName` to `"encryption"`.

   - **keyVaultCollectionName** - The collection in MongoDB where your DEKs will be stored. Set `keyVaultCollectionName` to `"__keyVault"`.

   - **keyVaultNamespace** - The namespace in MongoDB where your DEKs will be stored. Set `keyVaultNamespace` to a new `CollectionNamespace` object whose name is the values of the `keyVaultDatabaseName` and `keyVaultCollectionName` variables, separated by a period.

   - **encryptedDatabaseName** - The MongoDB database where your encrypted data will be stored. Set `encryptedDatabaseName` to `"medicalRecords"`.

   - **encryptedCollectionName** - The collection in MongoDB where your encrypted data will be stored. Set `encryptedCollectionName` to `"patients"`.

   - **uri** - Your MongoDB deployment connection URI. Set your connection URI in the `appsettings.json` file or replace the value directly.

   You can declare these variables by using the following code:

   ```csharp
   const string kmsProviderName = "<your KMS provider name>";
   const string keyVaultDatabaseName = "encryption";
   const string keyVaultCollectionName = "__keyVault";
   var keyVaultNamespace =
       CollectionNamespace.FromFullName($"{keyVaultDatabaseName}.{keyVaultCollectionName}");
   const string encryptedDatabaseName = "medicalRecords";
   const string encryptedCollectionName = "patients";
   var appSettings = new ConfigurationBuilder().AddJsonFile("appsettings.json").Build();
   var uri = appSettings["MongoDbUri"];
   ```

   **Important: Key Vault Collection Namespace Permissions**

   The Key Vault collection is in the `encryption.__keyVault` namespace. Ensure that the database user your application uses to connect to MongoDB has [ReadWrite](/docs/manual/reference/built-in-roles#std-label-manual-reference-role-read-write) permissions on this namespace.

   **Tip: Environment Variables**

   The sample code in this tutorial references environment variables that you need to set. Alternatively, you can replace the values directly in the code.

   To learn how you can setup these environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/csharp/README.md) file included in the sample application on GitHub.

2. Add your KMS credentials

   Create a variable containing your KMS credentials with the following structure. Use the Azure Key Vault credentials you recorded when you [registered your application with Azure.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-register-cmk-azure)

   ```csharp
   var kmsProviderCredentials = new Dictionary<string, IReadOnlyDictionary<string, object>>();
   var kmsOptions = new Dictionary<string, object>
   {
       { "tenantId", _appSettings["Azure:TenantId"] }, // Your Azure tenant ID
       { "clientId", _appSettings["Azure:ClientId"] }, // Your Azure client ID
       { "clientSecret", _appSettings["Azure:ClientSecret"] } // Your Azure client secret
   };
   kmsProviderCredentials.Add("azure", kmsOptions);
   ```

   You can also provide a custom name for your KMS provider by passing in a string that includes the name of the KMS provider, followed by a colon and the custom name. Providing a unique name for a KMS provider allows you to specify multiple KMS providers of the same type.

   For example, you can name your Azure KMS provider "my\_azure\_provider" in your KMS credentials variable as shown in the following code:

   ```csharp
   var kmsProviderCredentials = new Dictionary<string, IReadOnlyDictionary<string, object>>();
   var kmsOptions = new Dictionary<string, object>
   {
       { "tenantId", _appSettings["Azure:TenantId"] }, // Your Azure tenant ID
       { "clientId", _appSettings["Azure:ClientId"] }, // Your Azure client ID
       { "clientSecret", _appSettings["Azure:ClientSecret"] } // Your Azure client secret
   };
   kmsProviderCredentials.Add("azure:my_azure_provider", kmsOptions);
   ```

   NOTE: The remaining steps in this tutorial use the default KMS provider string, `"azure"`.

3. Add your CMK credentials

   Create a variable containing your Customer Master Key credentials with the following structure. Use the CMK details you recorded when you [created a CMK.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-create-cmk-azure)

   ```csharp
   var customerMasterKeyCredentials = new BsonDocument
   {
       { "keyVaultEndpoint", _appSettings["Azure:KeyVaultEndpoint"] }, // Your Azure Key Vault Endpoint
       { "keyName", _appSettings["Azure:KeyName"] } // Your Azure Key Name
   };
   ```

4. Create an encryption client

   To create a client for encrypting and decrypting data in encrypted collections, instantiate a new `MongoClient` using your connection URI and automatic encryption options.

   IMPORTANT: If you are using the .NET/C# driver version 3.0 or later, you must add the following code to your application before instantiating a new `MongoClient`:

   ```csharp
   MongoClientSettings.Extensions.AddAutoEncryption(); // .NET/C# Driver v3.0 or later only
   ```

   Instantiate a new `MongoClient` by using your connection URI and automatic encryption options:

   ```csharp
   var clientSettings = MongoClientSettings.FromConnectionString(uri);
   clientSettings.AutoEncryptionOptions = qeHelpers.GetAutoEncryptionOptions(
       keyVaultNamespace,
       kmsProviderCredentials);

   var encryptedClient = new MongoClient(clientSettings);
   ```

### Full Application Code

To see the complete code for the sample application, select your programming language in the language selector.

[Complete Rust Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/rust/)

Each sample application repository includes a `README.md` file that you can use to learn how to set up your environment and run the application.

1. Assign application variables

   The code samples in this tutorial use the following variables to perform the Queryable Encryption workflow:

   - **kms\_provider\_name** - The KMS you're using to store your Customer Master Key. Set this variable to `"local"` for this tutorial.

   - **uri** - Your MongoDB deployment connection URI. Set your connection URI in the `MONGODB_URI` environment variable.

   - **key\_vault\_database\_name** - The database in MongoDB where your data encryption keys (DEKs) will be stored. Set this variable to `"encryption"`.

   - **key\_vault\_collection\_name** - The collection in MongoDB where your DEKs will be stored. Set this variable to `"__keyVault"`, which is the convention to help prevent mistaking it for a user collection.

   - **key\_vault\_namespace** - The namespace in MongoDB where your DEKs will be stored. Set this variable to a `Namespace` struct and pass the values of the `key_vault_database_name` and `key_vault_collection_name` variables.

   - **encrypted\_database\_name** - The database in MongoDB where your encrypted data will be stored. Set this variable to `"medicalRecords"`.

   - **encrypted\_collection\_name** - The collection in MongoDB where your encrypted data will be stored. Set this variable to `"patients"`.

   You can declare these variables by using the following code:

   ```rust
   let kms_provider_name = "<KMS provider name>";
   let uri = env::var("MONGODB_URI").expect("Set MONGODB_URI environment variable to your connection string");
   let key_vault_database_name = "encryption";
   let key_vault_collection_name = "__keyVault";
   let key_vault_namespace = Namespace::new(key_vault_database_name, key_vault_collection_name);
   let encrypted_database_name = "medicalRecords";
   let encrypted_collection_name = "patients";
   ```

   **Important: Key Vault Collection Namespace Permissions**

   The Key Vault collection is in the `encryption.__keyVault` namespace. Ensure that the database user your application uses to connect to MongoDB has [ReadWrite](/docs/manual/reference/built-in-roles#std-label-manual-reference-role-read-write) permissions on this namespace.

   **Tip: Environment Variables**

   The sample code in this tutorial references environment variables that you need to set. Alternatively, you can replace the values directly in the code.

   To learn how you can setup these environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/rust/README.md) file included in the sample application on GitHub.

2. Add your KMS credentials

   Create a variable containing your KMS credentials with the following structure. Use the Azure Key Vault credentials you recorded when you [registered your application with Azure.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-register-cmk-azure)

   ```rust
   kms_providers = vec![(
       KmsProvider::azure(),
       doc! {
           "tenantId": env::var("AZURE_TENANT_ID").expect("Set AZURE_TENANT_ID environment variable"),
           "clientId": env::var("AZURE_CLIENT_ID").expect("Set AZURE_CLIENT_ID environment variable"),
           "clientSecret": env::var("AZURE_CLIENT_SECRET").expect("AZURE_CLIENT_SECRET environment variable"),
       },
       None,
   )];
   ```

   You can also provide a custom name for your KMS provider by passing the name as a string to the `with_name()` function. Providing a unique name for a KMS provider allows you to specify multiple KMS providers of the same type.

   For example, you can name your Azure KMS provider "my\_azure\_provider" in your KMS credentials variable as shown in the following code:

   ```rust
   kms_providers = vec![(
       KmsProvider::azure().with_name("my_azure_provider"),
       doc! {
           "tenantId": env::var("AZURE_TENANT_ID").expect("Set AZURE_TENANT_ID environment variable"),
           "clientId": env::var("AZURE_CLIENT_ID").expect("Set AZURE_CLIENT_ID environment variable"),
           "clientSecret": env::var("AZURE_CLIENT_SECRET").expect("AZURE_CLIENT_SECRET environment variable"),
       },
       None,
   )];
   ```

   NOTE: The remaining steps in this tutorial use the default KMS provider string, `"azure"`.

3. Add your CMK credentials

   Create a variable containing your Customer Master Key credentials with the following structure. Use the CMK details you recorded when you [created a CMK.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-create-cmk-azure)

   ```rust
   let azure_master_key = AzureMasterKey::builder()
       .key_vault_endpoint(env::var("AZURE_KEY_VAULT_ENDPOINT").expect("Set the AZURE_KEY_VAULT_ENDPOINT environment variable"))
       .key_name(env::var("AZURE_KEY_NAME").expect("Set the AZURE_KEY_NAME environment variable"))
       .build();
   ```

4. Create an encryption client

   To create a client for encrypting and decrypting data in encrypted collections, instantiate a new `MongoClient` using your connection URI and automatic encryption options.

   ```rust
   let encrypted_client = encrypted_client_builder
       .extra_options(Some(doc!{
           "cryptSharedLibPath": env::var("SHARED_LIB_PATH").expect("Set SHARED_LIB_PATH environment variable to path to crypt_shared library")
       }))
       .key_vault_client(Client::with_uri_str(uri).await.unwrap())
       .build()
       .await
       .unwrap();
   ```

### Full Application Code

To see the complete code for the sample application, select your programming language in the language selector.

[Complete PHP Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/php/)

Each sample application repository includes a `README.md` file that you can use to learn how to set up your environment and run the application.

1. Assign application variables

   The code samples in this tutorial use the following variables to perform the Queryable Encryption workflow:

   - **$kmsProviderName** - The KMS you're using to store your Customer Master Key. Set the `KMS_PROVIDER` environment variable to your key provider: `'aws'`, `'azure'`, `'gcp'`, or `'kmip'`.

   - **$uri** - Your MongoDB deployment connection URI. Set your connection URI in the `MONGODB_URI` environment variable.

   - **$keyVaultDatabaseName** - The database in MongoDB where your data encryption keys (DEKs) will be stored. Set the value of `$keyVaultDatabaseName` to `'encryption'`.

   - **$keyVaultCollectionName** - The collection in MongoDB where your DEKs will be stored. Set this variable to `'__keyVault'`, which is the convention to help prevent mistaking it for a user collection.

   - **$keyVaultNamespace** - The namespace in MongoDB where your DEKs will be stored. Set this variable to the values of the `$keyVaultDatabaseName` and `$keyVaultCollectionName` variables, separated by a period.

   - **$encryptedDatabaseName** - The database in MongoDB where your encrypted data will be stored. Set this variable to `'medicalRecords'`.

   - **$encryptedCollectionName** - The collection in MongoDB where your encrypted data will be stored. Set this variable to `'patients'`.

   You can declare these variables by using the following code:

   ```php
   $kmsProviderName = getenv('KMS_PROVIDER');
   $uri = getenv('MONGODB_URI'); // Your connection URI
   $keyVaultDatabaseName = 'encryption';
   $keyVaultCollectionName = '__keyVault';
   $keyVaultNamespace = $keyVaultDatabaseName . '.' . $keyVaultCollectionName;
   $encryptedDatabaseName = 'medicalRecords';
   $encryptedCollectionName = 'patients';
   ```

   **Important: Key Vault Collection Namespace Permissions**

   The Key Vault collection is in the `encryption.__keyVault` namespace. Ensure that the database user your application uses to connect to MongoDB has [ReadWrite](/docs/manual/reference/built-in-roles#std-label-manual-reference-role-read-write) permissions on this namespace.

   **Tip: Environment Variables**

   The sample code in this tutorial references environment variables that you need to set. Alternatively, you can replace the values directly in the code.

   To learn how you can setup these environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/php/README.md) file included in the sample application on GitHub.

2. Add your KMS credentials

   Create a variable containing your KMS credentials with the following structure. Use the Azure Key Vault credentials you recorded when you [registered your application with Azure.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-register-cmk-azure)

   ```php
   $kmsProviders = [
       'azure' => [
           'tenantId' => getenv('AZURE_TENANT_ID'), // Your Azure tenant ID
           'clientId' => getenv('AZURE_CLIENT_ID'), // Your Azure client ID
           'clientSecret' => getenv('AZURE_CLIENT_SECRET'), // Your Azure client secret
       ],
   ];
   ```

   You can also provide a custom name for your KMS provider by passing in a string that includes the name of the KMS provider, followed by a colon and the custom name. Providing a unique name for a KMS provider allows you to specify multiple KMS providers of the same type.

   For example, you can name your Azure KMS provider 'my\_azure\_provider' in your KMS credentials variable as shown in the following code:

   ```php
   $kmsProviders = [
       'azure:my_azure_provider' => [
           'tenantId' => getenv('AZURE_TENANT_ID'), // Your Azure tenant ID
           'clientId' => getenv('AZURE_CLIENT_ID'), // Your Azure client ID
           'clientSecret' => getenv('AZURE_CLIENT_SECRET'), // Your Azure client secret
       ],
   ];
   ```

   NOTE: The remaining steps in this tutorial use the default KMS provider string, `'azure'`.

3. Add your CMK credentials

   Create a variable containing your Customer Master Key credentials with the following structure. Use the CMK details you recorded when you [created a CMK.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-create-cmk-azure)

   ```php
   $customerMasterKeyCredentials = [
       'keyVaultEndpoint' => getenv('AZURE_KEY_VAULT_ENDPOINT'), // Your Azure Key Vault Endpoint
       'keyName' => getenv('AZURE_KEY_NAME'), // Your Azure Key Name
   ];
   ```

4. Create an encryption client

   To create a client for encrypting and decrypting data in encrypted collections, instantiate a new `MongoClient` using your connection URI and automatic encryption options.

   ```php
   $encryptedClient = new \MongoDB\Client($uri, [], [
       'autoEncryption' => $autoEncryptionOptions,
   ]);
   ```

### Full Application Code

To see the complete code for the sample application, select your programming language in the language selector.

[Complete Ruby Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/ruby/)

Each sample application repository includes a `README.md` file that you can use to learn how to set up your environment and run the application.

1. Assign application variables

   The code samples in this tutorial use the following variables to perform the Queryable Encryption workflow:

   - **kms\_provider\_name** - The KMS you use to store your Customer Master Key. Set this to your key provider: `"aws"`, `"azure"`, `"gcp"`, or `"kmip"`.

   - **uri** - Your MongoDB deployment connection URI. Set your connection URI in the `MONGODB_URI` environment variable or replace the value directly.

   - **key\_vault\_database\_name** - The MongoDB database where your data encryption keys (DEKs) will be stored. Set this to `"encryption"`.

   - **key\_vault\_collection\_name** - The collection in MongoDB where your DEKs will be stored. Set this to `"__keyVault"`, which is the convention to help prevent mistaking it for a user collection.

   - **key\_vault\_namespace** - The namespace in MongoDB where your DEKs will be stored. Set this to the values of the `key_vault_database_name` and `key_vault_collection_name` variables separated by a period, in the format `"#{key_vault_database_name}.#{key_vault_collection_name}"`.

   - **encrypted\_database\_name** - The MongoDB database where your encrypted data will be stored. Set this to `"medicalRecords"`.

   - **encrypted\_collection\_name** - The collection in MongoDB where your encrypted data will be stored. Set this to `"patients"`.

   You can declare these variables by using the following code:

   ```ruby
   kms_provider_name = ENV["KMS_PROVIDER"]
   uri = ENV["MONGODB_URI"] # Your connection URI
   key_vault_database_name = "encryption"
   key_vault_collection_name = "__keyVault"
   key_vault_namespace = "#{key_vault_database_name}.#{key_vault_collection_name}"
   encrypted_database_name = "medicalRecords"
   encrypted_collection_name = "patients"
   ```

   **Important: Key Vault Collection Namespace Permissions**

   The Key Vault collection is in the `encryption.__keyVault` namespace. Ensure that the database user your application uses to connect to MongoDB has [ReadWrite](/docs/manual/reference/built-in-roles#std-label-manual-reference-role-read-write) permissions on this namespace.

   **Tip: Environment Variables**

   The sample code in this tutorial references environment variables that you need to set. Alternatively, you can replace the values directly in the code.

   To learn how you can setup these environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/ruby/README.md) file included in the sample application on GitHub.

2. Add your KMS credentials

   Create a variable containing your KMS credentials with the following structure. Use the Azure Key Vault credentials you recorded when you [registered your application with Azure.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-register-cmk-azure)

   ```ruby
   kms_providers = {
     azure: {
       tenantId: ENV["AZURE_TENANT_ID"], # Your Azure tenant ID
       clientId: ENV["AZURE_CLIENT_ID"], # Your Azure client ID
       clientSecret: ENV["AZURE_CLIENT_SECRET"] # Your Azure client secret
     }
   }
   ```

3. Add your CMK credentials

   Create a variable containing your Customer Master Key credentials with the following structure. Use the CMK details you recorded when you [created a CMK.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-create-cmk-azure)

   ```ruby
   customer_master_key_credentials = {
     keyVaultEndpoint: ENV["AZURE_KEY_VAULT_ENDPOINT"], # Your Azure Key Vault Endpoint
     keyName: ENV["AZURE_KEY_NAME"] # Your Azure Key Name
   }
   ```

4. Create an encryption client

   To create a client for encrypting and decrypting data in encrypted collections, instantiate a new `Mongo::Client` using your connection URI and automatic encryption options.

   ```ruby
   encrypted_client = Mongo::Client.new(uri, auto_encryption_options: auto_encryption_options)
   ```

### Full Application Code

To see the complete code for the sample application, select your programming language in the language selector.

[Complete mongosh Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/mongosh/)

Each sample application repository includes a `README.md` file that you can use to learn how to set up your environment and run the application.

1. Assign application variables

   The code samples in this tutorial use the following variables to perform the Queryable Encryption workflow:

   - **kmsProviderName** - The KMS you use to store your Customer Master Key. Set this to your key provider: `"aws"`, `"azure"`, `"gcp"`, or `"kmip"`.

   - **uri** - Your MongoDB deployment connection URI. Set your connection URI in the `MONGODB_URI` environment variable or replace the value directly.

   - **keyVaultDatabaseName** - The MongoDB database where your data encryption keys (DEKs) will be stored. Set this to `"encryption"`.

   - **keyVaultCollectionName** - The collection in MongoDB where your DEKs will be stored. Set this to `"__keyVault"`.

   - **keyVaultNamespace** - The namespace in MongoDB where your DEKs will be stored. Set this to the values of the `keyVaultDatabaseName` and `keyVaultCollectionName` variables, separated by a period.

   - **encryptedDatabaseName** - The MongoDB database where your encrypted data will be stored. Set this to `"medicalRecords"`.

   - **encryptedCollectionName** - The collection in MongoDB where your encrypted data will be stored. Set this to `"patients"`.

   You can declare these variables by using the following code:

   ```javascript
   const kmsProviderName = "<Your KMS Provider Name>";
   const uri = process.env.MONGODB_URI; // Your connection URI
   const keyVaultDatabaseName = "encryption";
   const keyVaultCollectionName = "__keyVault";
   const keyVaultNamespace = `${keyVaultDatabaseName}.${keyVaultCollectionName}`;
   const encryptedDatabaseName = "medicalRecords";
   const encryptedCollectionName = "patients";
   ```

   **Important: Key Vault Collection Namespace Permissions**

   The Key Vault collection is in the `encryption.__keyVault` namespace. Ensure that the database user your application uses to connect to MongoDB has [ReadWrite](/docs/manual/reference/built-in-roles#std-label-manual-reference-role-read-write) permissions on this namespace.

   **Tip: Environment Variables**

   The sample code in this tutorial references environment variables that you need to set. Alternatively, you can replace the values directly in the code.

   To learn how you can setup these environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/node/README.md) file included in the sample application on GitHub.

2. Add your KMS credentials

   Create a variable containing the endpoint of your KMIP-compliant key provider with the following structure:

   ```javascript
   kmsProviderCredentials = {
     kmip: {
       endpoint: process.env["KMIP_KMS_ENDPOINT"], // Your KMIP KMS endpoint
     },
   };
   ```

   You can also provide a custom name for your KMS provider by passing in a string that includes the name of the KMS provider, followed by a colon and the custom name. Providing a unique name for a KMS provider allows you to specify multiple KMS providers of the same type.

   For example, you can name your KMIP KMS provider "my\_kmip\_provider" in your KMS credentials variable as shown in the following code:

   ```javascript
   kmsProviderCredentials = {
     "kmip:my_kmip_provider": {
       endpoint: process.env["KMIP_KMS_ENDPOINT"], // Your KMIP KMS endpoint
     },
   };

   ```

   NOTE: The remaining steps in this tutorial use the default KMS provider string, `"kmip"`.

3. Add your CMK credentials

   Create an empty object as shown in the following code example. This prompts your KMIP (Key Management Interoperability Protocol)-compliant key provider to generate a new Customer Master Key.

   ```javascript
   customerMasterKeyCredentials = {};
   ```

4. Create an encryption client

   To create a client for encrypting and decrypting data in encrypted collections, instantiate a new `MongoClient` using your connection URI and automatic encryption options.

   ```javascript
   const encryptedClient = Mongo(uri, autoEncryptionOptions);
   ```

### Full Application Code

To see the complete code for the sample application, select your programming language in the language selector.

[Complete Node.js Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/node/)

Each sample application repository includes a `README.md` file that you can use to learn how to set up your environment and run the application.

1. Assign application variables

   The code samples in this tutorial use the following variables to perform the Queryable Encryption workflow:

   - **kmsProviderName** - The KMS you use to store your Customer Master Key. Set this to your key provider: `"aws"`, `"azure"`, `"gcp"`, or `"kmip"`.

   - **uri** - Your MongoDB deployment connection URI. Set your connection URI in the `MONGODB_URI` environment variable or replace the value directly.

   - **keyVaultDatabaseName** - The MongoDB database where your data encryption keys (DEKs) will be stored. Set this to `"encryption"`.

   - **keyVaultCollectionName** - The collection in MongoDB where your DEKs will be stored. Set this to `"__keyVault"`.

   - **keyVaultNamespace** - The namespace in MongoDB where your DEKs will be stored. Set this to the values of the `keyVaultDatabaseName` and `keyVaultCollectionName` variables, separated by a period.

   - **encryptedDatabaseName** - The MongoDB database where your encrypted data will be stored. Set this to `"medicalRecords"`.

   - **encryptedCollectionName** - The collection in MongoDB where your encrypted data will be stored. Set this to `"patients"`.

   You can declare these variables by using the following code:

   ```javascript
   const kmsProviderName = "<Your KMS Provider Name>";

   const uri = process.env.MONGODB_URI; // Your connection URI

   const keyVaultDatabaseName = "encryption";
   const keyVaultCollectionName = "__keyVault";
   const keyVaultNamespace = `${keyVaultDatabaseName}.${keyVaultCollectionName}`;
   const encryptedDatabaseName = "medicalRecords";
   const encryptedCollectionName = "patients";
   ```

   **Important: Key Vault Collection Namespace Permissions**

   The Key Vault collection is in the `encryption.__keyVault` namespace. Ensure that the database user your application uses to connect to MongoDB has [ReadWrite](/docs/manual/reference/built-in-roles#std-label-manual-reference-role-read-write) permissions on this namespace.

   **Tip: Environment Variables**

   The sample code in this tutorial references environment variables that you need to set. Alternatively, you can replace the values directly in the code.

   To learn how you can setup these environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/node/README.md) file included in the sample application on GitHub.

2. Add your KMS credentials

   Create a variable containing the endpoint of your KMIP-compliant key provider with the following structure:

   ```javascript
   kmsProviders = {
     kmip: {
       endpoint: process.env.KMIP_KMS_ENDPOINT, // Your KMIP KMS endpoint
     },
   };
   ```

   You can also provide a custom name for your KMS provider by passing in a string that includes the name of the KMS provider, followed by a colon and the custom name. Providing a unique name for a KMS provider allows you to specify multiple KMS providers of the same type.

   For example, you can name your KMIP KMS provider "my\_kmip\_provider" in your KMS credentials variable as shown in the following code:

   ```javascript
   kmsProviders = {
     "kmip:my_kmip_provider": {
       endpoint: process.env.KMIP_KMS_ENDPOINT, // Your KMIP KMS endpoint
     },
   };

   ```

   NOTE: The remaining steps in this tutorial use the default KMS provider string, `"kmip"`.

3. Add your CMK credentials

   Create an empty object as shown in the following code example. This prompts your KMIP (Key Management Interoperability Protocol)-compliant key provider to generate a new Customer Master Key.

   ```javascript
   customerMasterKeyCredentials = {};
   ```

4. Create an encryption client

   To create a client for encrypting and decrypting data in encrypted collections, instantiate a new `MongoClient` using your connection URI and automatic encryption options.

   ```javascript
   const encryptedClient = new MongoClient(uri, {
     autoEncryption: autoEncryptionOptions,
   });
   ```

### Full Application Code

To see the complete code for the sample application, select your programming language in the language selector.

[Complete Python Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/python/)

Each sample application repository includes a `README.md` file that you can use to learn how to set up your environment and run the application.

1. Assign application variables

   The code samples in this tutorial use the following variables to perform the Queryable Encryption workflow:

   - **kms\_provider\_name** - The KMS you use to store your Customer Master Key. Set this to your key provider: `"aws"`, `"azure"`, `"gcp"`, or `"kmip"`.

   - **uri** - Your MongoDB deployment connection URI. Set your connection URI in the `MONGODB_URI` environment variable or replace the value directly.

   - **key\_vault\_database\_name** - The MongoDB database where your data encryption keys (DEKs) will be stored. Set this to `"encryption"`.

   - **key\_vault\_collection\_name** - The collection in MongoDB where your DEKs will be stored. Set this to `"__keyVault"`.

   - **key\_vault\_namespace** - The namespace in MongoDB where your DEKs will be stored. Set this to the values of the `key_vault_database_name` and `key_vault_collection_name` variables, separated by a period.

   - **encrypted\_database\_name** - The MongoDB database where your encrypted data will be stored. Set this to `"medicalRecords"`.

   - **encrypted\_collection\_name** - The collection in MongoDB where your encrypted data will be stored. Set this to `"patients"`.

   You can declare these variables by using the following code:

   ```python
   kms_provider_name = "<KMS provider name>"
   uri = os.environ.get("MONGODB_URI", "mongodb://127.0.0.1:27017")  # Your connection URI
   key_vault_database_name = "encryption"
   key_vault_collection_name = "__keyVault"
   key_vault_namespace = f"{key_vault_database_name}.{key_vault_collection_name}"
   encrypted_database_name = "medicalRecords"
   encrypted_collection_name = "patients"
   ```

   **Important: Key Vault Collection Namespace Permissions**

   The Key Vault collection is in the `encryption.__keyVault` namespace. Ensure that the database user your application uses to connect to MongoDB has [ReadWrite](/docs/manual/reference/built-in-roles#std-label-manual-reference-role-read-write) permissions on this namespace.

   **Tip: Environment Variables**

   The sample code in this tutorial references environment variables that you need to set. Alternatively, you can replace the values directly in the code.

   To learn how you can setup these environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/python/README.md) file included in the sample application on GitHub.

2. Add your KMS credentials

   Create a variable containing the endpoint of your KMIP-compliant key provider with the following structure:

   ```python
   kms_provider_credentials = {
       "kmip": {
           "endpoint": os.environ['KMIP_KMS_ENDPOINT'] # Your KMIP KMS endpoint
       }
   }
   ```

   You can also provide a custom name for your KMS provider by passing in a string that includes the name of the KMS provider, followed by a colon and the custom name. Providing a unique name for a KMS provider allows you to specify multiple KMS providers of the same type.

   For example, you can name your KMIP KMS provider "my\_kmip\_provider" in your KMS credentials variable as shown in the following code:

   ```python
   kms_provider_credentials = {
       "kmip:my_kmip_provider": {
           "endpoint": os.environ['KMIP_KMS_ENDPOINT'] # Your KMIP KMS endpoint
       }
   }
   ```

   NOTE: The remaining steps in this tutorial use the default KMS provider string, `"kmip"`.

3. Add your CMK credentials

   Create an empty object as shown in the following code example. This prompts your KMIP (Key Management Interoperability Protocol)-compliant key provider to generate a new Customer Master Key.

   ```python
   customer_master_key_credentials = {}
   ```

4. Create an encryption client

   To create a client for encrypting and decrypting data in encrypted collections, instantiate a new `MongoClient` using your connection URI and automatic encryption options.

   ```python
   encrypted_client = MongoClient(
       uri, auto_encryption_opts=auto_encryption_options)
   ```

### Full Application Code

To see the complete code for the sample application, select your programming language in the language selector.

[Complete Java Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/java/)

Each sample application repository includes a `README.md` file that you can use to learn how to set up your environment and run the application.

1. Assign application variables

   The code samples in this tutorial use the following variables to perform the Queryable Encryption workflow:

   - **kmsProviderName** - The KMS you use to store your Customer Master Key. Set this to your key provider: `"aws"`, `"azure"`, `"gcp"`, or `"kmip"`.

   - **uri** - Your MongoDB deployment connection URI. Set your connection URI in the `MONGODB_URI` environment variable or replace the value directly.

   - **keyVaultDatabaseName** - The MongoDB database where your data encryption keys (DEKs) will be stored. Set this to `"encryption"`.

   - **keyVaultCollectionName** - The collection in MongoDB where your DEKs will be stored. Set this to `"__keyVault"`.

   - **keyVaultNamespace** - The namespace in MongoDB where your DEKs will be stored. Set this to the values of the `keyVaultDatabaseName` and `keyVaultCollectionName` variables, separated by a period.

   - **encryptedDatabaseName** - The MongoDB database where your encrypted data will be stored. Set this to `"medicalRecords"`.

   - **encryptedCollectionName** - The collection in MongoDB where your encrypted data will be stored. Set this to `"patients"`.

   You can declare these variables by using the following code:

   ```java
   String kmsProviderName = "<KMS provider name>";
   String uri = QueryableEncryptionHelpers.getEnv("MONGODB_URI"); // Your connection URI
   String keyVaultDatabaseName = "encryption";
   String keyVaultCollectionName = "__keyVault";
   String keyVaultNamespace = keyVaultDatabaseName + "." + keyVaultCollectionName;
   String encryptedDatabaseName = "medicalRecords";
   String encryptedCollectionName = "patients";
   ```

   **Important: Key Vault Collection Namespace Permissions**

   The Key Vault collection is in the `encryption.__keyVault` namespace. Ensure that the database user your application uses to connect to MongoDB has [ReadWrite](/docs/manual/reference/built-in-roles#std-label-manual-reference-role-read-write) permissions on this namespace.

   **Tip: Environment Variables**

   The sample code in this tutorial references environment variables that you need to set. Alternatively, you can replace the values directly in the code.

   To learn how you can setup these environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/java/README.md) file included in the sample application on GitHub.

2. Add your KMS credentials

   Create a variable containing the endpoint of your KMIP-compliant key provider with the following structure:

   ```java
   Map<String, Object> kmsProviderDetails = new HashMap<>();
   kmsProviderDetails.put("endpoint", getEnv("KMIP_KMS_ENDPOINT")); // Your KMIP KMS endpoint

   Map<String, Map<String, Object>> kmsProviderCredentials = new HashMap<String, Map<String, Object>>();
   kmsProviderCredentials.put("kmip", kmsProviderDetails);
   ```

   You can also provide a custom name for your KMS provider by passing in a string that includes the name of the KMS provider, followed by a colon and the custom name. Providing a unique name for a KMS provider allows you to specify multiple KMS providers of the same type.

   For example, you can name your KMIP KMS provider "my\_kmip\_provider" in your KMS credentials variable as shown in the following code:

   ```java
   Map<String, Object> kmsProviderDetails = new HashMap<>();
   kmsProviderDetails.put("endpoint", getEnv("KMIP_KMS_ENDPOINT")); // Your KMIP KMS endpoint

   Map<String, Map<String, Object>> kmsProviderCredentials = new HashMap<String, Map<String, Object>>();
   kmsProviderCredentials.put("kmip:my_kmip_provider", kmsProviderDetails);
   ```

   NOTE: The remaining steps in this tutorial use the default KMS provider string, `"kmip"`.

3. Add your CMK credentials

   Create an empty object as shown in the following code example. This prompts your KMIP (Key Management Interoperability Protocol)-compliant key provider to generate a new Customer Master Key.

   ```java
   BsonDocument customerMasterKeyCredentials = new BsonDocument();
   ```

4. Create an encryption client

   To create a client for encrypting and decrypting data in encrypted collections, instantiate a new `MongoClient` using your connection URI and automatic encryption options.

   ```java
   MongoClientSettings clientSettings = MongoClientSettings.builder()
           .applyConnectionString(new ConnectionString(uri))
           .autoEncryptionSettings(autoEncryptionSettings)
           .build();

   try (MongoClient encryptedClient = MongoClients.create(clientSettings)) {
   ```

### Full Application Code

To see the complete code for the sample application, select your programming language in the language selector.

[Complete Go Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/go/)

Each sample application repository includes a `README.md` file that you can use to learn how to set up your environment and run the application.

1. Assign application variables

   The code samples in this tutorial use the following variables to perform the Queryable Encryption workflow:

   - **kmsProviderName** - The KMS you use to store your Customer Master Key. Set this to your key provider: `"aws"`, `"azure"`, `"gcp"`, or `"kmip"`.

   - **uri** - Your MongoDB deployment connection URI. Set your connection URI in the `MONGODB_URI` environment variable or replace the value directly.

   - **keyVaultDatabaseName** - The MongoDB database where your data encryption keys (DEKs) will be stored. Set this to `"encryption"`.

   - **keyVaultCollectionName** - The collection in MongoDB where your DEKs will be stored. Set this to `"__keyVault"`.

   - **keyVaultNamespace** - The namespace in MongoDB where your DEKs will be stored. Set this to the values of the `keyVaultDatabaseName` and `keyVaultCollectionName` variables, separated by a period.

   - **encryptedDatabaseName** - The MongoDB database where your encrypted data will be stored. Set this to `"medicalRecords"`.

   - **encryptedCollectionName** - The collection in MongoDB where your encrypted data will be stored. Set this to `"patients"`.

   You can declare these variables by using the following code:

   ```go
   kmsProviderName := "<KMS provider name>"
   uri := os.Getenv("MONGODB_URI") // Your connection URI
   keyVaultDatabaseName := "encryption"
   keyVaultCollectionName := "__keyVault"
   keyVaultNamespace := keyVaultDatabaseName + "." + keyVaultCollectionName
   encryptedDatabaseName := "medicalRecords"
   encryptedCollectionName := "patients"
   ```

   **Important: Key Vault Collection Namespace Permissions**

   The Key Vault collection is in the `encryption.__keyVault` namespace. Ensure that the database user your application uses to connect to MongoDB has [ReadWrite](/docs/manual/reference/built-in-roles#std-label-manual-reference-role-read-write) permissions on this namespace.

   **Tip: Environment Variables**

   The sample code in this tutorial references environment variables that you need to set. Alternatively, you can replace the values directly in the code.

   To learn how you can setup these environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/go/README.md) file included in the sample application on GitHub.

2. Add your KMS credentials

   Create a variable containing the endpoint of your KMIP-compliant key provider with the following structure:

   ```go
   kmsProviderCredentials := map[string]map[string]interface{}{
   	"kmip": {
   		"endpoint": os.Getenv("KMIP_KMS_ENDPOINT"), // KMIP KMS endpoint
   	},
   }
   ```

3. Add your CMK credentials

   Create an empty object as shown in the following code example. This prompts your KMIP (Key Management Interoperability Protocol)-compliant key provider to generate a new Customer Master Key.

   ```go
   customerMasterKey := map[string]string{}
   ```

4. Create an encryption client

   To create a client for encrypting and decrypting data in encrypted collections, instantiate a new `MongoClient` using your connection URI and automatic encryption options.

   ```go
   opts := options.Client().
   	ApplyURI(uri).
   	SetAutoEncryptionOptions(autoEncryptionOptions)
   encryptedClient, err := mongo.Connect(opts)

   if err != nil {
   	panic(fmt.Sprintf("Unable to connect to MongoDB: %v\n", err))
   }
   defer func() {
   	_ = encryptedClient.Disconnect(context.TODO())
   }()
   ```

### Full Application Code

To see the complete code for the sample application, select your programming language in the language selector.

[Complete C# Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/csharp/)

Each sample application repository includes a `README.md` file that you can use to learn how to set up your environment and run the application.

1. Assign application variables

   The code samples in this tutorial use the following variables to perform the Queryable Encryption workflow:

   - **kmsProviderName** - The KMS you use to store your Customer Master Key. Set this to your key provider: `"aws"`, `"azure"`, `"gcp"`, or `"kmip"`.

   - **keyVaultDatabaseName** - The MongoDB database where your data encryption keys (DEKs) will be stored. Set `keyVaultDatabaseName` to `"encryption"`.

   - **keyVaultCollectionName** - The collection in MongoDB where your DEKs will be stored. Set `keyVaultCollectionName` to `"__keyVault"`.

   - **keyVaultNamespace** - The namespace in MongoDB where your DEKs will be stored. Set `keyVaultNamespace` to a new `CollectionNamespace` object whose name is the values of the `keyVaultDatabaseName` and `keyVaultCollectionName` variables, separated by a period.

   - **encryptedDatabaseName** - The MongoDB database where your encrypted data will be stored. Set `encryptedDatabaseName` to `"medicalRecords"`.

   - **encryptedCollectionName** - The collection in MongoDB where your encrypted data will be stored. Set `encryptedCollectionName` to `"patients"`.

   - **uri** - Your MongoDB deployment connection URI. Set your connection URI in the `appsettings.json` file or replace the value directly.

   You can declare these variables by using the following code:

   ```csharp
   const string kmsProviderName = "<your KMS provider name>";
   const string keyVaultDatabaseName = "encryption";
   const string keyVaultCollectionName = "__keyVault";
   var keyVaultNamespace =
       CollectionNamespace.FromFullName($"{keyVaultDatabaseName}.{keyVaultCollectionName}");
   const string encryptedDatabaseName = "medicalRecords";
   const string encryptedCollectionName = "patients";
   var appSettings = new ConfigurationBuilder().AddJsonFile("appsettings.json").Build();
   var uri = appSettings["MongoDbUri"];
   ```

   **Important: Key Vault Collection Namespace Permissions**

   The Key Vault collection is in the `encryption.__keyVault` namespace. Ensure that the database user your application uses to connect to MongoDB has [ReadWrite](/docs/manual/reference/built-in-roles#std-label-manual-reference-role-read-write) permissions on this namespace.

   **Tip: Environment Variables**

   The sample code in this tutorial references environment variables that you need to set. Alternatively, you can replace the values directly in the code.

   To learn how you can setup these environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/csharp/README.md) file included in the sample application on GitHub.

2. Add your KMS credentials

   Create a variable containing the endpoint of your KMIP-compliant key provider with the following structure:

   ```csharp
   var kmsProviderCredentials = new Dictionary<string, IReadOnlyDictionary<string, object>>();
   var kmsOptions = new Dictionary<string, object>
   {
       { "endpoint", _appSettings["Kmip:KmsEndpoint"] } // Your KMIP KMS endpoint
   };
   kmsProviderCredentials.Add("kmip", kmsOptions);
   ```

   You can also provide a custom name for your KMS provider by passing in a string that includes the name of the KMS provider, followed by a colon and the custom name. Providing a unique name for a KMS provider allows you to specify multiple KMS providers of the same type.

   For example, you can name your KMIP KMS provider "my\_kmip\_provider" in your KMS credentials variable as shown in the following code:

   ```csharp
   var kmsProviderCredentials = new Dictionary<string, IReadOnlyDictionary<string, object>>();
   var kmsOptions = new Dictionary<string, object>
   {
       { "endpoint", _appSettings["Kmip:KmsEndpoint"] } // Your KMIP KMS endpoint
   };
   kmsProviderCredentials.Add("kmip:my_kmip_provider", kmsOptions);
   ```

   NOTE: The remaining steps in this tutorial use the default KMS provider string, `"kmip"`.

3. Add your CMK credentials

   Create an empty object as shown in the following code example. This prompts your KMIP (Key Management Interoperability Protocol)-compliant key provider to generate a new Customer Master Key.

   ```csharp
   var customerMasterKeyCredentials = new BsonDocument();
   ```

4. Create an encryption client

   To create a client for encrypting and decrypting data in encrypted collections, instantiate a new `MongoClient` using your connection URI and automatic encryption options.

   IMPORTANT: If you are using the .NET/C# driver version 3.0 or later, you must add the following code to your application before instantiating a new `MongoClient`:

   ```csharp
   MongoClientSettings.Extensions.AddAutoEncryption(); // .NET/C# Driver v3.0 or later only
   ```

   Instantiate a new `MongoClient` by using your connection URI and automatic encryption options:

   ```csharp
   var clientSettings = MongoClientSettings.FromConnectionString(uri);
   clientSettings.AutoEncryptionOptions = qeHelpers.GetAutoEncryptionOptions(
       keyVaultNamespace,
       kmsProviderCredentials);

   var encryptedClient = new MongoClient(clientSettings);
   ```

### Full Application Code

To see the complete code for the sample application, select your programming language in the language selector.

[Complete Rust Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/rust/)

Each sample application repository includes a `README.md` file that you can use to learn how to set up your environment and run the application.

1. Assign application variables

   The code samples in this tutorial use the following variables to perform the Queryable Encryption workflow:

   - **kms\_provider\_name** - The KMS you're using to store your Customer Master Key. Set this variable to `"local"` for this tutorial.

   - **uri** - Your MongoDB deployment connection URI. Set your connection URI in the `MONGODB_URI` environment variable.

   - **key\_vault\_database\_name** - The database in MongoDB where your data encryption keys (DEKs) will be stored. Set this variable to `"encryption"`.

   - **key\_vault\_collection\_name** - The collection in MongoDB where your DEKs will be stored. Set this variable to `"__keyVault"`, which is the convention to help prevent mistaking it for a user collection.

   - **key\_vault\_namespace** - The namespace in MongoDB where your DEKs will be stored. Set this variable to a `Namespace` struct and pass the values of the `key_vault_database_name` and `key_vault_collection_name` variables.

   - **encrypted\_database\_name** - The database in MongoDB where your encrypted data will be stored. Set this variable to `"medicalRecords"`.

   - **encrypted\_collection\_name** - The collection in MongoDB where your encrypted data will be stored. Set this variable to `"patients"`.

   You can declare these variables by using the following code:

   ```rust
   let kms_provider_name = "<KMS provider name>";
   let uri = env::var("MONGODB_URI").expect("Set MONGODB_URI environment variable to your connection string");
   let key_vault_database_name = "encryption";
   let key_vault_collection_name = "__keyVault";
   let key_vault_namespace = Namespace::new(key_vault_database_name, key_vault_collection_name);
   let encrypted_database_name = "medicalRecords";
   let encrypted_collection_name = "patients";
   ```

   **Important: Key Vault Collection Namespace Permissions**

   The Key Vault collection is in the `encryption.__keyVault` namespace. Ensure that the database user your application uses to connect to MongoDB has [ReadWrite](/docs/manual/reference/built-in-roles#std-label-manual-reference-role-read-write) permissions on this namespace.

   **Tip: Environment Variables**

   The sample code in this tutorial references environment variables that you need to set. Alternatively, you can replace the values directly in the code.

   To learn how you can setup these environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/rust/README.md) file included in the sample application on GitHub.

2. Add your KMS credentials

   Create a variable containing the endpoint of your KMIP-compliant key provider with the following structure:

   ```rust
   kms_providers = vec![(
       KmsProvider::kmip(),
       doc! {
           "endpoint": env::var("KMIP_KMS_ENDPOINT").expect("Set KMIP_KMS_ENDPOINT environment variable")
       },
       Some(get_kmip_tls_options()),
   )];
   ```

   You can also provide a custom name for your KMS provider by passing the name as a string to the `with_name()` function. Providing a unique name for a KMS provider allows you to specify multiple KMS providers of the same type.

   For example, you can name your KMIP KMS provider "my\_kmip\_provider" in your KMS credentials variable as shown in the following code:

   ```rust
   kms_providers = vec![(
       KmsProvider::kmip().with_name("my_kmip_provider"),
       doc! {
           "endpoint": env::var("KMIP_KMS_ENDPOINT").expect("Set KMIP_KMS_ENDPOINT environment variable")
       },
       Some(get_kmip_tls_options()),
   )];
   ```

   NOTE: The remaining steps in this tutorial use the default KMS provider string, `"kmip"`.

3. Add your CMK credentials

   Create an empty object as shown in the following code example. This prompts your KMIP (Key Management Interoperability Protocol)-compliant key provider to generate a new Customer Master Key.

   ```rust
   let kmip_master_key = KmipMasterKey::builder().build();
   ```

4. Create an encryption client

   To create a client for encrypting and decrypting data in encrypted collections, instantiate a new `MongoClient` using your connection URI and automatic encryption options.

   ```rust
   let encrypted_client = encrypted_client_builder
       .extra_options(Some(doc!{
           "cryptSharedLibPath": env::var("SHARED_LIB_PATH").expect("Set SHARED_LIB_PATH environment variable to path to crypt_shared library")
       }))
       .key_vault_client(Client::with_uri_str(uri).await.unwrap())
       .build()
       .await
       .unwrap();
   ```

### Full Application Code

To see the complete code for the sample application, select your programming language in the language selector.

[Complete PHP Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/php/)

Each sample application repository includes a `README.md` file that you can use to learn how to set up your environment and run the application.

1. Assign application variables

   The code samples in this tutorial use the following variables to perform the Queryable Encryption workflow:

   - **$kmsProviderName** - The KMS you're using to store your Customer Master Key. Set the `KMS_PROVIDER` environment variable to your key provider: `'aws'`, `'azure'`, `'gcp'`, or `'kmip'`.

   - **$uri** - Your MongoDB deployment connection URI. Set your connection URI in the `MONGODB_URI` environment variable.

   - **$keyVaultDatabaseName** - The database in MongoDB where your data encryption keys (DEKs) will be stored. Set the value of `$keyVaultDatabaseName` to `'encryption'`.

   - **$keyVaultCollectionName** - The collection in MongoDB where your DEKs will be stored. Set this variable to `'__keyVault'`, which is the convention to help prevent mistaking it for a user collection.

   - **$keyVaultNamespace** - The namespace in MongoDB where your DEKs will be stored. Set this variable to the values of the `$keyVaultDatabaseName` and `$keyVaultCollectionName` variables, separated by a period.

   - **$encryptedDatabaseName** - The database in MongoDB where your encrypted data will be stored. Set this variable to `'medicalRecords'`.

   - **$encryptedCollectionName** - The collection in MongoDB where your encrypted data will be stored. Set this variable to `'patients'`.

   You can declare these variables by using the following code:

   ```php
   $kmsProviderName = getenv('KMS_PROVIDER');
   $uri = getenv('MONGODB_URI'); // Your connection URI
   $keyVaultDatabaseName = 'encryption';
   $keyVaultCollectionName = '__keyVault';
   $keyVaultNamespace = $keyVaultDatabaseName . '.' . $keyVaultCollectionName;
   $encryptedDatabaseName = 'medicalRecords';
   $encryptedCollectionName = 'patients';
   ```

   **Important: Key Vault Collection Namespace Permissions**

   The Key Vault collection is in the `encryption.__keyVault` namespace. Ensure that the database user your application uses to connect to MongoDB has [ReadWrite](/docs/manual/reference/built-in-roles#std-label-manual-reference-role-read-write) permissions on this namespace.

   **Tip: Environment Variables**

   The sample code in this tutorial references environment variables that you need to set. Alternatively, you can replace the values directly in the code.

   To learn how you can setup these environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/php/README.md) file included in the sample application on GitHub.

2. Add your KMS credentials

   Create a variable containing the endpoint of your KMIP-compliant key provider with the following structure:

   ```php
   $kmsProviders = [
       'kmip' => [
           'endpoint' => getenv('KMIP_ENDPOINT'), // Your KMIP endpoint
       ],
   ];
   ```

   You can also provide a custom name for your KMS provider by passing in a string that includes the name of the KMS provider, followed by a colon and the custom name. Providing a unique name for a KMS provider allows you to specify multiple KMS providers of the same type.

   For example, you can name your KMIP KMS provider 'my\_kmip\_provider' in your KMS credentials variable as shown in the following code:

   ```php
   $kmsProviders = [
       'kmip:my_kmip_provider' => [
           'endpoint' => getenv('KMIP_ENDPOINT'), // Your KMIP endpoint
       ],
   ];
   ```

   NOTE: The remaining steps in this tutorial use the default KMS provider string, `'kmip'`.

3. Add your CMK credentials

   Create an empty object as shown in the following code example. This prompts your KMIP (Key Management Interoperability Protocol)-compliant key provider to generate a new Customer Master Key.

   ```php
   $customerMasterKeyCredentials = [];
   ```

4. Create an encryption client

   To create a client for encrypting and decrypting data in encrypted collections, instantiate a new `MongoClient` using your connection URI and automatic encryption options.

   ```php
   $encryptedClient = new \MongoDB\Client($uri, [], [
       'autoEncryption' => $autoEncryptionOptions,
   ]);
   ```

### Full Application Code

To see the complete code for the sample application, select your programming language in the language selector.

[Complete Ruby Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/ruby/)

Each sample application repository includes a `README.md` file that you can use to learn how to set up your environment and run the application.

1. Assign application variables

   The code samples in this tutorial use the following variables to perform the Queryable Encryption workflow:

   - **kms\_provider\_name** - The KMS you use to store your Customer Master Key. Set this to your key provider: `"aws"`, `"azure"`, `"gcp"`, or `"kmip"`.

   - **uri** - Your MongoDB deployment connection URI. Set your connection URI in the `MONGODB_URI` environment variable or replace the value directly.

   - **key\_vault\_database\_name** - The MongoDB database where your data encryption keys (DEKs) will be stored. Set this to `"encryption"`.

   - **key\_vault\_collection\_name** - The collection in MongoDB where your DEKs will be stored. Set this to `"__keyVault"`, which is the convention to help prevent mistaking it for a user collection.

   - **key\_vault\_namespace** - The namespace in MongoDB where your DEKs will be stored. Set this to the values of the `key_vault_database_name` and `key_vault_collection_name` variables separated by a period, in the format `"#{key_vault_database_name}.#{key_vault_collection_name}"`.

   - **encrypted\_database\_name** - The MongoDB database where your encrypted data will be stored. Set this to `"medicalRecords"`.

   - **encrypted\_collection\_name** - The collection in MongoDB where your encrypted data will be stored. Set this to `"patients"`.

   You can declare these variables by using the following code:

   ```ruby
   kms_provider_name = ENV["KMS_PROVIDER"]
   uri = ENV["MONGODB_URI"] # Your connection URI
   key_vault_database_name = "encryption"
   key_vault_collection_name = "__keyVault"
   key_vault_namespace = "#{key_vault_database_name}.#{key_vault_collection_name}"
   encrypted_database_name = "medicalRecords"
   encrypted_collection_name = "patients"
   ```

   **Important: Key Vault Collection Namespace Permissions**

   The Key Vault collection is in the `encryption.__keyVault` namespace. Ensure that the database user your application uses to connect to MongoDB has [ReadWrite](/docs/manual/reference/built-in-roles#std-label-manual-reference-role-read-write) permissions on this namespace.

   **Tip: Environment Variables**

   The sample code in this tutorial references environment variables that you need to set. Alternatively, you can replace the values directly in the code.

   To learn how you can setup these environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/ruby/README.md) file included in the sample application on GitHub.

2. Add your KMS credentials

   Create a variable containing the endpoint of your KMIP-compliant key provider with the following structure:

   ```ruby
   kms_providers = {
     kmip: {
       endpoint: ENV["KMIP_KMS_ENDPOINT"] # Your KMIP KMS endpoint
     }
   }
   ```

3. Add your CMK credentials

   Create an empty object as shown in the following code example. This prompts your KMIP (Key Management Interoperability Protocol)-compliant key provider to generate a new Customer Master Key.

   ```ruby
   customer_master_key_credentials = {}
   ```

4. Create an encryption client

   To create a client for encrypting and decrypting data in encrypted collections, instantiate a new `Mongo::Client` using your connection URI and automatic encryption options.

   ```ruby
   encrypted_client = Mongo::Client.new(uri, auto_encryption_options: auto_encryption_options)
   ```

### Full Application Code

To see the complete code for the sample application, select your programming language in the language selector.

[Complete mongosh Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/mongosh/)

Each sample application repository includes a `README.md` file that you can use to learn how to set up your environment and run the application.

1. Assign application variables

   The code samples in this tutorial use the following variables to perform the Queryable Encryption workflow:

   - **kmsProviderName** - The KMS you use to store your Customer Master Key. Set this to your key provider: `"aws"`, `"azure"`, `"gcp"`, or `"kmip"`.

   - **uri** - Your MongoDB deployment connection URI. Set your connection URI in the `MONGODB_URI` environment variable or replace the value directly.

   - **keyVaultDatabaseName** - The MongoDB database where your data encryption keys (DEKs) will be stored. Set this to `"encryption"`.

   - **keyVaultCollectionName** - The collection in MongoDB where your DEKs will be stored. Set this to `"__keyVault"`.

   - **keyVaultNamespace** - The namespace in MongoDB where your DEKs will be stored. Set this to the values of the `keyVaultDatabaseName` and `keyVaultCollectionName` variables, separated by a period.

   - **encryptedDatabaseName** - The MongoDB database where your encrypted data will be stored. Set this to `"medicalRecords"`.

   - **encryptedCollectionName** - The collection in MongoDB where your encrypted data will be stored. Set this to `"patients"`.

   You can declare these variables by using the following code:

   ```javascript
   const kmsProviderName = "<Your KMS Provider Name>";
   const uri = process.env.MONGODB_URI; // Your connection URI
   const keyVaultDatabaseName = "encryption";
   const keyVaultCollectionName = "__keyVault";
   const keyVaultNamespace = `${keyVaultDatabaseName}.${keyVaultCollectionName}`;
   const encryptedDatabaseName = "medicalRecords";
   const encryptedCollectionName = "patients";
   ```

   **Important: Key Vault Collection Namespace Permissions**

   The Key Vault collection is in the `encryption.__keyVault` namespace. Ensure that the database user your application uses to connect to MongoDB has [ReadWrite](/docs/manual/reference/built-in-roles#std-label-manual-reference-role-read-write) permissions on this namespace.

   **Tip: Environment Variables**

   The sample code in this tutorial references environment variables that you need to set. Alternatively, you can replace the values directly in the code.

   To learn how you can setup these environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/node/README.md) file included in the sample application on GitHub.

2. Add your KMS credentials

   Create a variable containing your KMS credentials with the following structure.

   ```javascript
   kmsProviderCredentials = {
     gcp: {
       email: process.env["GCP_EMAIL"], // Your GCP email
       privateKey: process.env["GCP_PRIVATE_KEY"], // Your GCP private key
     },
   };
   ```

   You can also provide a custom name for your KMS provider by passing in a string that includes the name of the KMS provider, followed by a colon and the custom name. Providing a unique name for a KMS provider allows you to specify multiple KMS providers of the same type.

   For example, you can name your GCP KMS provider "my\_gcp\_provider" in your KMS credentials variable as shown in the following code:

   ```javascript
   kmsProviderCredentials = {
     "gcp:my_gcp_provider": {
       email: process.env["GCP_EMAIL"], // Your GCP email
       privateKey: process.env["GCP_PRIVATE_KEY"], // Your GCP private key
     },
   };

   ```

   NOTE: The remaining steps in this tutorial use the default KMS provider string, `"gcp"`.

3. Add your CMK credentials

   Create a variable containing your Customer Master Key credentials with the following structure. Use the credentials you recorded when you [created a CMK.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-create-cmk-gcp)

   ```javascript
   customerMasterKeyCredentials = {
     projectId: process.env["GCP_PROJECT_ID"], // Your GCP Project ID
     location: process.env["GCP_LOCATION"], // Your GCP Key Location
     keyRing: process.env["GCP_KEY_RING"], //  Your GCP Key Ring
     keyName: process.env["GCP_KEY_NAME"], // Your GCP Key Name
   };
   ```

4. Create an encryption client

   To create a client for encrypting and decrypting data in encrypted collections, instantiate a new `MongoClient` using your connection URI and automatic encryption options.

   ```javascript
   const encryptedClient = Mongo(uri, autoEncryptionOptions);
   ```

### Full Application Code

To see the complete code for the sample application, select your programming language in the language selector.

[Complete Node.js Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/node/)

Each sample application repository includes a `README.md` file that you can use to learn how to set up your environment and run the application.

1. Assign application variables

   The code samples in this tutorial use the following variables to perform the Queryable Encryption workflow:

   - **kmsProviderName** - The KMS you use to store your Customer Master Key. Set this to your key provider: `"aws"`, `"azure"`, `"gcp"`, or `"kmip"`.

   - **uri** - Your MongoDB deployment connection URI. Set your connection URI in the `MONGODB_URI` environment variable or replace the value directly.

   - **keyVaultDatabaseName** - The MongoDB database where your data encryption keys (DEKs) will be stored. Set this to `"encryption"`.

   - **keyVaultCollectionName** - The collection in MongoDB where your DEKs will be stored. Set this to `"__keyVault"`.

   - **keyVaultNamespace** - The namespace in MongoDB where your DEKs will be stored. Set this to the values of the `keyVaultDatabaseName` and `keyVaultCollectionName` variables, separated by a period.

   - **encryptedDatabaseName** - The MongoDB database where your encrypted data will be stored. Set this to `"medicalRecords"`.

   - **encryptedCollectionName** - The collection in MongoDB where your encrypted data will be stored. Set this to `"patients"`.

   You can declare these variables by using the following code:

   ```javascript
   const kmsProviderName = "<Your KMS Provider Name>";

   const uri = process.env.MONGODB_URI; // Your connection URI

   const keyVaultDatabaseName = "encryption";
   const keyVaultCollectionName = "__keyVault";
   const keyVaultNamespace = `${keyVaultDatabaseName}.${keyVaultCollectionName}`;
   const encryptedDatabaseName = "medicalRecords";
   const encryptedCollectionName = "patients";
   ```

   **Important: Key Vault Collection Namespace Permissions**

   The Key Vault collection is in the `encryption.__keyVault` namespace. Ensure that the database user your application uses to connect to MongoDB has [ReadWrite](/docs/manual/reference/built-in-roles#std-label-manual-reference-role-read-write) permissions on this namespace.

   **Tip: Environment Variables**

   The sample code in this tutorial references environment variables that you need to set. Alternatively, you can replace the values directly in the code.

   To learn how you can setup these environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/node/README.md) file included in the sample application on GitHub.

2. Add your KMS credentials

   Create a variable containing your KMS credentials with the following structure.

   ```javascript
   kmsProviders = {
     gcp: {
       email: process.env.GCP_EMAIL, // Your GCP email
       privateKey: process.env.GCP_PRIVATE_KEY, // Your GCP private key
     },
   };
   ```

   You can also provide a custom name for your KMS provider by passing in a string that includes the name of the KMS provider, followed by a colon and the custom name. Providing a unique name for a KMS provider allows you to specify multiple KMS providers of the same type.

   For example, you can name your GCP KMS provider "my\_gcp\_provider" in your KMS credentials variable as shown in the following code:

   ```javascript
   kmsProviders = {
     "gcp:my_gcp_provider": {
       email: process.env.GCP_EMAIL, // Your GCP email
       privateKey: process.env.GCP_PRIVATE_KEY, // Your GCP private key
     },
   };

   ```

   NOTE: The remaining steps in this tutorial use the default KMS provider string, `"gcp"`.

3. Add your CMK credentials

   Create a variable containing your Customer Master Key credentials with the following structure. Use the credentials you recorded when you [created a CMK.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-create-cmk-gcp)

   ```javascript
   customerMasterKeyCredentials = {
     projectId: process.env.GCP_PROJECT_ID, // Your GCP Project ID
     location: process.env.GCP_LOCATION, // Your GCP Key Location
     keyRing: process.env.GCP_KEY_RING, //  Your GCP Key Ring
     keyName: process.env.GCP_KEY_NAME, // Your GCP Key Name
   };
   ```

4. Create an encryption client

   To create a client for encrypting and decrypting data in encrypted collections, instantiate a new `MongoClient` using your connection URI and automatic encryption options.

   ```javascript
   const encryptedClient = new MongoClient(uri, {
     autoEncryption: autoEncryptionOptions,
   });
   ```

### Full Application Code

To see the complete code for the sample application, select your programming language in the language selector.

[Complete Python Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/python/)

Each sample application repository includes a `README.md` file that you can use to learn how to set up your environment and run the application.

1. Assign application variables

   The code samples in this tutorial use the following variables to perform the Queryable Encryption workflow:

   - **kms\_provider\_name** - The KMS you use to store your Customer Master Key. Set this to your key provider: `"aws"`, `"azure"`, `"gcp"`, or `"kmip"`.

   - **uri** - Your MongoDB deployment connection URI. Set your connection URI in the `MONGODB_URI` environment variable or replace the value directly.

   - **key\_vault\_database\_name** - The MongoDB database where your data encryption keys (DEKs) will be stored. Set this to `"encryption"`.

   - **key\_vault\_collection\_name** - The collection in MongoDB where your DEKs will be stored. Set this to `"__keyVault"`.

   - **key\_vault\_namespace** - The namespace in MongoDB where your DEKs will be stored. Set this to the values of the `key_vault_database_name` and `key_vault_collection_name` variables, separated by a period.

   - **encrypted\_database\_name** - The MongoDB database where your encrypted data will be stored. Set this to `"medicalRecords"`.

   - **encrypted\_collection\_name** - The collection in MongoDB where your encrypted data will be stored. Set this to `"patients"`.

   You can declare these variables by using the following code:

   ```python
   kms_provider_name = "<KMS provider name>"
   uri = os.environ.get("MONGODB_URI", "mongodb://127.0.0.1:27017")  # Your connection URI
   key_vault_database_name = "encryption"
   key_vault_collection_name = "__keyVault"
   key_vault_namespace = f"{key_vault_database_name}.{key_vault_collection_name}"
   encrypted_database_name = "medicalRecords"
   encrypted_collection_name = "patients"
   ```

   **Important: Key Vault Collection Namespace Permissions**

   The Key Vault collection is in the `encryption.__keyVault` namespace. Ensure that the database user your application uses to connect to MongoDB has [ReadWrite](/docs/manual/reference/built-in-roles#std-label-manual-reference-role-read-write) permissions on this namespace.

   **Tip: Environment Variables**

   The sample code in this tutorial references environment variables that you need to set. Alternatively, you can replace the values directly in the code.

   To learn how you can setup these environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/python/README.md) file included in the sample application on GitHub.

2. Add your KMS credentials

   Create a variable containing your KMS credentials with the following structure.

   ```python
   kms_provider_credentials = {
       "gcp": {
           "email": os.environ['GCP_EMAIL'], # Your GCP email
           "privateKey": os.environ['GCP_PRIVATE_KEY'] # Your GCP private key
       }
   }
   ```

   You can also provide a custom name for your KMS provider by passing in a string that includes the name of the KMS provider, followed by a colon and the custom name. Providing a unique name for a KMS provider allows you to specify multiple KMS providers of the same type.

   For example, you can name your GCP KMS provider "my\_gcp\_provider" in your KMS credentials variable as shown in the following code:

   ```python
   kms_provider_credentials = {
       "gcp:my_gcp_provider": {
           "email": os.environ['GCP_EMAIL'], # Your GCP email
           "privateKey": os.environ['GCP_PRIVATE_KEY'] # Your GCP private key
       }
   }
   ```

   NOTE: The remaining steps in this tutorial use the default KMS provider string, `"gcp"`.

3. Add your CMK credentials

   Create a variable containing your Customer Master Key credentials with the following structure. Use the credentials you recorded when you [created a CMK.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-create-cmk-gcp)

   ```python
   customer_master_key_credentials = {
       "projectId": os.environ['GCP_PROJECT_ID'], # Your GCP email
       "location": os.environ['GCP_LOCATION'],  # Your GCP private key
       "keyRing": os.environ['GCP_KEY_RING'],  # Your GCP private key
       "keyName": os.environ['GCP_KEY_NAME']  # Your GCP private key
   }
   ```

4. Create an encryption client

   To create a client for encrypting and decrypting data in encrypted collections, instantiate a new `MongoClient` using your connection URI and automatic encryption options.

   ```python
   encrypted_client = MongoClient(
       uri, auto_encryption_opts=auto_encryption_options)
   ```

### Full Application Code

To see the complete code for the sample application, select your programming language in the language selector.

[Complete Java Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/java/)

Each sample application repository includes a `README.md` file that you can use to learn how to set up your environment and run the application.

1. Assign application variables

   The code samples in this tutorial use the following variables to perform the Queryable Encryption workflow:

   - **kmsProviderName** - The KMS you use to store your Customer Master Key. Set this to your key provider: `"aws"`, `"azure"`, `"gcp"`, or `"kmip"`.

   - **uri** - Your MongoDB deployment connection URI. Set your connection URI in the `MONGODB_URI` environment variable or replace the value directly.

   - **keyVaultDatabaseName** - The MongoDB database where your data encryption keys (DEKs) will be stored. Set this to `"encryption"`.

   - **keyVaultCollectionName** - The collection in MongoDB where your DEKs will be stored. Set this to `"__keyVault"`.

   - **keyVaultNamespace** - The namespace in MongoDB where your DEKs will be stored. Set this to the values of the `keyVaultDatabaseName` and `keyVaultCollectionName` variables, separated by a period.

   - **encryptedDatabaseName** - The MongoDB database where your encrypted data will be stored. Set this to `"medicalRecords"`.

   - **encryptedCollectionName** - The collection in MongoDB where your encrypted data will be stored. Set this to `"patients"`.

   You can declare these variables by using the following code:

   ```java
   String kmsProviderName = "<KMS provider name>";
   String uri = QueryableEncryptionHelpers.getEnv("MONGODB_URI"); // Your connection URI
   String keyVaultDatabaseName = "encryption";
   String keyVaultCollectionName = "__keyVault";
   String keyVaultNamespace = keyVaultDatabaseName + "." + keyVaultCollectionName;
   String encryptedDatabaseName = "medicalRecords";
   String encryptedCollectionName = "patients";
   ```

   **Important: Key Vault Collection Namespace Permissions**

   The Key Vault collection is in the `encryption.__keyVault` namespace. Ensure that the database user your application uses to connect to MongoDB has [ReadWrite](/docs/manual/reference/built-in-roles#std-label-manual-reference-role-read-write) permissions on this namespace.

   **Tip: Environment Variables**

   The sample code in this tutorial references environment variables that you need to set. Alternatively, you can replace the values directly in the code.

   To learn how you can setup these environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/java/README.md) file included in the sample application on GitHub.

2. Add your KMS credentials

   Create a variable containing your KMS credentials with the following structure.

   ```java
   Map<String, Object> kmsProviderDetails = new HashMap<>();
   kmsProviderDetails.put("email", getEnv("GCP_EMAIL")); // Your GCP email
   kmsProviderDetails.put("privateKey", getEnv("GCP_PRIVATE_KEY")); // Your GCP private key

   Map<String, Map<String, Object>> kmsProviderCredentials = new HashMap<String, Map<String, Object>>();
   kmsProviderCredentials.put("gcp", kmsProviderDetails);
   ```

   You can also provide a custom name for your KMS provider by passing in a string that includes the name of the KMS provider, followed by a colon and the custom name. Providing a unique name for a KMS provider allows you to specify multiple KMS providers of the same type.

   For example, you can name your GCP KMS provider "my\_gcp\_provider" in your KMS credentials variable as shown in the following code:

   ```java
   Map<String, Object> kmsProviderDetails = new HashMap<>();
   kmsProviderDetails.put("email", getEnv("GCP_EMAIL")); // Your GCP email
   kmsProviderDetails.put("privateKey", getEnv("GCP_PRIVATE_KEY")); // Your GCP private key

   Map<String, Map<String, Object>> kmsProviderCredentials = new HashMap<String, Map<String, Object>>();
   kmsProviderCredentials.put("gcp:my_gcp_provider", kmsProviderDetails);
   ```

   NOTE: The remaining steps in this tutorial use the default KMS provider string, `"gcp"`.

3. Add your CMK credentials

   Create a variable containing your Customer Master Key credentials with the following structure. Use the credentials you recorded when you [created a CMK.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-create-cmk-gcp)

   ```java
   BsonDocument customerMasterKeyCredentials = new BsonDocument();
   customerMasterKeyCredentials.put("provider", new BsonString(kmsProviderName));
   customerMasterKeyCredentials.put("projectId", new BsonString(getEnv("GCP_PROJECT_ID"))); // Your GCP Project ID
   customerMasterKeyCredentials.put("location", new BsonString(getEnv("GCP_LOCATION"))); // Your GCP Key Location
   customerMasterKeyCredentials.put("keyRing", new BsonString(getEnv("GCP_KEY_RING"))); // Your GCP Key Ring
   customerMasterKeyCredentials.put("keyName", new BsonString(getEnv("GCP_KEY_NAME"))); // Your GCP Key Name
   ```

4. Create an encryption client

   To create a client for encrypting and decrypting data in encrypted collections, instantiate a new `MongoClient` using your connection URI and automatic encryption options.

   ```java
   MongoClientSettings clientSettings = MongoClientSettings.builder()
           .applyConnectionString(new ConnectionString(uri))
           .autoEncryptionSettings(autoEncryptionSettings)
           .build();

   try (MongoClient encryptedClient = MongoClients.create(clientSettings)) {
   ```

### Full Application Code

To see the complete code for the sample application, select your programming language in the language selector.

[Complete Go Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/go/)

Each sample application repository includes a `README.md` file that you can use to learn how to set up your environment and run the application.

1. Assign application variables

   The code samples in this tutorial use the following variables to perform the Queryable Encryption workflow:

   - **kmsProviderName** - The KMS you use to store your Customer Master Key. Set this to your key provider: `"aws"`, `"azure"`, `"gcp"`, or `"kmip"`.

   - **uri** - Your MongoDB deployment connection URI. Set your connection URI in the `MONGODB_URI` environment variable or replace the value directly.

   - **keyVaultDatabaseName** - The MongoDB database where your data encryption keys (DEKs) will be stored. Set this to `"encryption"`.

   - **keyVaultCollectionName** - The collection in MongoDB where your DEKs will be stored. Set this to `"__keyVault"`.

   - **keyVaultNamespace** - The namespace in MongoDB where your DEKs will be stored. Set this to the values of the `keyVaultDatabaseName` and `keyVaultCollectionName` variables, separated by a period.

   - **encryptedDatabaseName** - The MongoDB database where your encrypted data will be stored. Set this to `"medicalRecords"`.

   - **encryptedCollectionName** - The collection in MongoDB where your encrypted data will be stored. Set this to `"patients"`.

   You can declare these variables by using the following code:

   ```go
   kmsProviderName := "<KMS provider name>"
   uri := os.Getenv("MONGODB_URI") // Your connection URI
   keyVaultDatabaseName := "encryption"
   keyVaultCollectionName := "__keyVault"
   keyVaultNamespace := keyVaultDatabaseName + "." + keyVaultCollectionName
   encryptedDatabaseName := "medicalRecords"
   encryptedCollectionName := "patients"
   ```

   **Important: Key Vault Collection Namespace Permissions**

   The Key Vault collection is in the `encryption.__keyVault` namespace. Ensure that the database user your application uses to connect to MongoDB has [ReadWrite](/docs/manual/reference/built-in-roles#std-label-manual-reference-role-read-write) permissions on this namespace.

   **Tip: Environment Variables**

   The sample code in this tutorial references environment variables that you need to set. Alternatively, you can replace the values directly in the code.

   To learn how you can setup these environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/go/README.md) file included in the sample application on GitHub.

2. Add your KMS credentials

   Create a variable containing your KMS credentials with the following structure.

   ```go
   kmsProviderCredentials := map[string]map[string]interface{}{
   	"gcp": {
   		"email":      os.Getenv("GCP_EMAIL"),       // GCP email
   		"privateKey": os.Getenv("GCP_PRIVATE_KEY"), // GCP private key
   	},
   }
   ```

3. Add your CMK credentials

   Create a variable containing your Customer Master Key credentials with the following structure. Use the credentials you recorded when you [created a CMK.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-create-cmk-gcp)

   ```go
   customerMasterKeyCredentials := map[string]string{
   	"projectId": os.Getenv("GCP_PROJECT_ID"), // Your GCP Project ID
   	"location":  os.Getenv("GCP_LOCATION"),   // Your GCP Key Location
   	"keyRing":   os.Getenv("GCP_KEY_RING"),   // Your GCP Key Ring
   	"keyName":   os.Getenv("GCP_KEY_NAME"),   // Your GCP Key Name
   }
   ```

4. Create an encryption client

   To create a client for encrypting and decrypting data in encrypted collections, instantiate a new `MongoClient` using your connection URI and automatic encryption options.

   ```go
   opts := options.Client().
   	ApplyURI(uri).
   	SetAutoEncryptionOptions(autoEncryptionOptions)
   encryptedClient, err := mongo.Connect(opts)

   if err != nil {
   	panic(fmt.Sprintf("Unable to connect to MongoDB: %v\n", err))
   }
   defer func() {
   	_ = encryptedClient.Disconnect(context.TODO())
   }()
   ```

### Full Application Code

To see the complete code for the sample application, select your programming language in the language selector.

[Complete C# Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/csharp/)

Each sample application repository includes a `README.md` file that you can use to learn how to set up your environment and run the application.

1. Assign application variables

   The code samples in this tutorial use the following variables to perform the Queryable Encryption workflow:

   - **kmsProviderName** - The KMS you use to store your Customer Master Key. Set this to your key provider: `"aws"`, `"azure"`, `"gcp"`, or `"kmip"`.

   - **keyVaultDatabaseName** - The MongoDB database where your data encryption keys (DEKs) will be stored. Set `keyVaultDatabaseName` to `"encryption"`.

   - **keyVaultCollectionName** - The collection in MongoDB where your DEKs will be stored. Set `keyVaultCollectionName` to `"__keyVault"`.

   - **keyVaultNamespace** - The namespace in MongoDB where your DEKs will be stored. Set `keyVaultNamespace` to a new `CollectionNamespace` object whose name is the values of the `keyVaultDatabaseName` and `keyVaultCollectionName` variables, separated by a period.

   - **encryptedDatabaseName** - The MongoDB database where your encrypted data will be stored. Set `encryptedDatabaseName` to `"medicalRecords"`.

   - **encryptedCollectionName** - The collection in MongoDB where your encrypted data will be stored. Set `encryptedCollectionName` to `"patients"`.

   - **uri** - Your MongoDB deployment connection URI. Set your connection URI in the `appsettings.json` file or replace the value directly.

   You can declare these variables by using the following code:

   ```csharp
   const string kmsProviderName = "<your KMS provider name>";
   const string keyVaultDatabaseName = "encryption";
   const string keyVaultCollectionName = "__keyVault";
   var keyVaultNamespace =
       CollectionNamespace.FromFullName($"{keyVaultDatabaseName}.{keyVaultCollectionName}");
   const string encryptedDatabaseName = "medicalRecords";
   const string encryptedCollectionName = "patients";
   var appSettings = new ConfigurationBuilder().AddJsonFile("appsettings.json").Build();
   var uri = appSettings["MongoDbUri"];
   ```

   **Important: Key Vault Collection Namespace Permissions**

   The Key Vault collection is in the `encryption.__keyVault` namespace. Ensure that the database user your application uses to connect to MongoDB has [ReadWrite](/docs/manual/reference/built-in-roles#std-label-manual-reference-role-read-write) permissions on this namespace.

   **Tip: Environment Variables**

   The sample code in this tutorial references environment variables that you need to set. Alternatively, you can replace the values directly in the code.

   To learn how you can setup these environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/csharp/README.md) file included in the sample application on GitHub.

2. Add your KMS credentials

   Create a variable containing your KMS credentials with the following structure.

   ```csharp
   var kmsProviderCredentials = new Dictionary<string, IReadOnlyDictionary<string, object>>();
   var kmsOptions = new Dictionary<string, object>
   {
       { "email", _appSettings["Gcp:Email"] }, // Your GCP email
       { "privateKey", _appSettings["Gcp:PrivateKey"] } // Your GCP private key
   };
   kmsProviderCredentials.Add("gcp", kmsOptions);
   ```

   You can also provide a custom name for your KMS provider by passing in a string that includes the name of the KMS provider, followed by a colon and the custom name. Providing a unique name for a KMS provider allows you to specify multiple KMS providers of the same type.

   For example, you can name your GCP KMS provider "my\_gcp\_provider" in your KMS credentials variable as shown in the following code:

   ```csharp
   var kmsProviderCredentials = new Dictionary<string, IReadOnlyDictionary<string, object>>();
   var kmsOptions = new Dictionary<string, object>
   {
       { "email", _appSettings["Gcp:Email"] }, // Your GCP email
       { "privateKey", _appSettings["Gcp:PrivateKey"] } // Your GCP private key
   };
   kmsProviderCredentials.Add("gcp:my_gcp_provider", kmsOptions);
   ```

   NOTE: The remaining steps in this tutorial use the default KMS provider string, `"gcp"`.

3. Add your CMK credentials

   Create a variable containing your Customer Master Key credentials with the following structure. Use the credentials you recorded when you [created a CMK.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-create-cmk-gcp)

   ```csharp
   var customerMasterKeyCredentials = new BsonDocument
   {
       { "projectId", _appSettings["Gcp:ProjectId"] }, // Your GCP Project ID
       { "location", _appSettings["Gcp:Location"] }, // Your GCP Key Location
       { "keyRing", _appSettings["Gcp:KeyRing"] }, // Your GCP Key Ring
       { "keyName", _appSettings["Gcp:KeyName"] } // Your GCP Key Name
   };
   ```

4. Create an encryption client

   To create a client for encrypting and decrypting data in encrypted collections, instantiate a new `MongoClient` using your connection URI and automatic encryption options.

   IMPORTANT: If you are using the .NET/C# driver version 3.0 or later, you must add the following code to your application before instantiating a new `MongoClient`:

   ```csharp
   MongoClientSettings.Extensions.AddAutoEncryption(); // .NET/C# Driver v3.0 or later only
   ```

   Instantiate a new `MongoClient` by using your connection URI and automatic encryption options:

   ```csharp
   var clientSettings = MongoClientSettings.FromConnectionString(uri);
   clientSettings.AutoEncryptionOptions = qeHelpers.GetAutoEncryptionOptions(
       keyVaultNamespace,
       kmsProviderCredentials);

   var encryptedClient = new MongoClient(clientSettings);
   ```

### Full Application Code

To see the complete code for the sample application, select your programming language in the language selector.

[Complete Rust Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/rust/)

Each sample application repository includes a `README.md` file that you can use to learn how to set up your environment and run the application.

1. Assign application variables

   The code samples in this tutorial use the following variables to perform the Queryable Encryption workflow:

   - **kms\_provider\_name** - The KMS you're using to store your Customer Master Key. Set this variable to `"local"` for this tutorial.

   - **uri** - Your MongoDB deployment connection URI. Set your connection URI in the `MONGODB_URI` environment variable.

   - **key\_vault\_database\_name** - The database in MongoDB where your data encryption keys (DEKs) will be stored. Set this variable to `"encryption"`.

   - **key\_vault\_collection\_name** - The collection in MongoDB where your DEKs will be stored. Set this variable to `"__keyVault"`, which is the convention to help prevent mistaking it for a user collection.

   - **key\_vault\_namespace** - The namespace in MongoDB where your DEKs will be stored. Set this variable to a `Namespace` struct and pass the values of the `key_vault_database_name` and `key_vault_collection_name` variables.

   - **encrypted\_database\_name** - The database in MongoDB where your encrypted data will be stored. Set this variable to `"medicalRecords"`.

   - **encrypted\_collection\_name** - The collection in MongoDB where your encrypted data will be stored. Set this variable to `"patients"`.

   You can declare these variables by using the following code:

   ```rust
   let kms_provider_name = "<KMS provider name>";
   let uri = env::var("MONGODB_URI").expect("Set MONGODB_URI environment variable to your connection string");
   let key_vault_database_name = "encryption";
   let key_vault_collection_name = "__keyVault";
   let key_vault_namespace = Namespace::new(key_vault_database_name, key_vault_collection_name);
   let encrypted_database_name = "medicalRecords";
   let encrypted_collection_name = "patients";
   ```

   **Important: Key Vault Collection Namespace Permissions**

   The Key Vault collection is in the `encryption.__keyVault` namespace. Ensure that the database user your application uses to connect to MongoDB has [ReadWrite](/docs/manual/reference/built-in-roles#std-label-manual-reference-role-read-write) permissions on this namespace.

   **Tip: Environment Variables**

   The sample code in this tutorial references environment variables that you need to set. Alternatively, you can replace the values directly in the code.

   To learn how you can setup these environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/rust/README.md) file included in the sample application on GitHub.

2. Add your KMS credentials

   Create a variable containing your KMS credentials with the following structure.

   ```rust
   kms_providers = vec![(
       KmsProvider::gcp(),
       doc! {
           "email": env::var("GCP_EMAIL").expect("Set GCP_EMAIL environment variable"),
           "privateKey": env::var("GCP_PRIVATE_KEY").expect("Set GCP_PRIVATE_KEY environment variable"),
       },
       None,
   )];
   ```

   You can also provide a custom name for your KMS provider by passing the name as a string to the `with_name()` function. Providing a unique name for a KMS provider allows you to specify multiple KMS providers of the same type.

   For example, you can name your GCP KMS provider "my\_gcp\_provider" in your KMS credentials variable as shown in the following code:

   ```rust
   kms_providers = vec![(
       KmsProvider::gcp().with_name("my_gcp_provider"),
       doc! {
           "email": env::var("GCP_EMAIL").expect("Set GCP_EMAIL environment variable"),
           "privateKey": env::var("GCP_PRIVATE_KEY").expect("Set GCP_PRIVATE_KEY environment variable"),
       },
       None,
   )];
   ```

   NOTE: The remaining steps in this tutorial use the default KMS provider string, `"gcp"`.

3. Add your CMK credentials

   Create a variable containing your Customer Master Key credentials with the following structure. Use the credentials you recorded when you [created a CMK.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-create-cmk-gcp)

   ```rust
   let gcp_master_key = GcpMasterKey::builder()
       .project_id(env::var("GCP_PROJECT_ID").expect("Set the GCP_PROJECT_ID environment variable"))
       .location(env::var("GCP_LOCATION").expect("Set the GCP_LOCATION environment variable"))
       .key_ring(env::var("GCP_KEY_RING").expect("Set the GCP_KEY_RING environment variable"))
       .key_name(env::var("GCP_KEY_NAME").expect("Set the GCP_KEY_NAME environment variable"))
       .build();
   ```

4. Create an encryption client

   To create a client for encrypting and decrypting data in encrypted collections, instantiate a new `MongoClient` using your connection URI and automatic encryption options.

   ```rust
   let encrypted_client = encrypted_client_builder
       .extra_options(Some(doc!{
           "cryptSharedLibPath": env::var("SHARED_LIB_PATH").expect("Set SHARED_LIB_PATH environment variable to path to crypt_shared library")
       }))
       .key_vault_client(Client::with_uri_str(uri).await.unwrap())
       .build()
       .await
       .unwrap();
   ```

### Full Application Code

To see the complete code for the sample application, select your programming language in the language selector.

[Complete PHP Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/php/)

Each sample application repository includes a `README.md` file that you can use to learn how to set up your environment and run the application.

1. Assign application variables

   The code samples in this tutorial use the following variables to perform the Queryable Encryption workflow:

   - **$kmsProviderName** - The KMS you're using to store your Customer Master Key. Set the `KMS_PROVIDER` environment variable to your key provider: `'aws'`, `'azure'`, `'gcp'`, or `'kmip'`.

   - **$uri** - Your MongoDB deployment connection URI. Set your connection URI in the `MONGODB_URI` environment variable.

   - **$keyVaultDatabaseName** - The database in MongoDB where your data encryption keys (DEKs) will be stored. Set the value of `$keyVaultDatabaseName` to `'encryption'`.

   - **$keyVaultCollectionName** - The collection in MongoDB where your DEKs will be stored. Set this variable to `'__keyVault'`, which is the convention to help prevent mistaking it for a user collection.

   - **$keyVaultNamespace** - The namespace in MongoDB where your DEKs will be stored. Set this variable to the values of the `$keyVaultDatabaseName` and `$keyVaultCollectionName` variables, separated by a period.

   - **$encryptedDatabaseName** - The database in MongoDB where your encrypted data will be stored. Set this variable to `'medicalRecords'`.

   - **$encryptedCollectionName** - The collection in MongoDB where your encrypted data will be stored. Set this variable to `'patients'`.

   You can declare these variables by using the following code:

   ```php
   $kmsProviderName = getenv('KMS_PROVIDER');
   $uri = getenv('MONGODB_URI'); // Your connection URI
   $keyVaultDatabaseName = 'encryption';
   $keyVaultCollectionName = '__keyVault';
   $keyVaultNamespace = $keyVaultDatabaseName . '.' . $keyVaultCollectionName;
   $encryptedDatabaseName = 'medicalRecords';
   $encryptedCollectionName = 'patients';
   ```

   **Important: Key Vault Collection Namespace Permissions**

   The Key Vault collection is in the `encryption.__keyVault` namespace. Ensure that the database user your application uses to connect to MongoDB has [ReadWrite](/docs/manual/reference/built-in-roles#std-label-manual-reference-role-read-write) permissions on this namespace.

   **Tip: Environment Variables**

   The sample code in this tutorial references environment variables that you need to set. Alternatively, you can replace the values directly in the code.

   To learn how you can setup these environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/php/README.md) file included in the sample application on GitHub.

2. Add your KMS credentials

   Create a variable containing your KMS credentials with the following structure.

   ```php
   $kmsProviders = [
       'gcp' => [
           'email' => getenv('GCP_EMAIL'), // Your GCP email
           'privateKey' => getenv('GCP_PRIVATE_KEY'), // Your GCP private key
       ],
   ];
   ```

   You can also provide a custom name for your KMS provider by passing in a string that includes the name of the KMS provider, followed by a colon and the custom name. Providing a unique name for a KMS provider allows you to specify multiple KMS providers of the same type.

   For example, you can name your GCP KMS provider 'my\_gcp\_provider' in your KMS credentials variable as shown in the following code:

   ```php
   $kmsProviders = [
       'gcp:my_gcp_provider' => [
           'email' => getenv('GCP_EMAIL'), // Your GCP email
           'privateKey' => getenv('GCP_PRIVATE_KEY'), // Your GCP private key
       ],
   ];
   ```

   NOTE: The remaining steps in this tutorial use the default KMS provider string, `'gcp'`.

3. Add your CMK credentials

   Create a variable containing your Customer Master Key credentials with the following structure. Use the credentials you recorded when you [created a CMK.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-create-cmk-gcp)

   ```php
   $customerMasterKeyCredentials = [
       'projectId' => getenv('GCP_PROJECT_ID'), // Your GCP Project ID
       'location' => getenv('GCP_LOCATION'), // Your GCP Key Location
       'keyRing' => getenv('GCP_KEY_RING'), // Your GCP Key Ring
       'keyName' => getenv('GCP_KEY_NAME'), // Your GCP Key Name
   ];
   ```

4. Create an encryption client

   To create a client for encrypting and decrypting data in encrypted collections, instantiate a new `MongoClient` using your connection URI and automatic encryption options.

   ```php
   $encryptedClient = new \MongoDB\Client($uri, [], [
       'autoEncryption' => $autoEncryptionOptions,
   ]);
   ```

### Full Application Code

To see the complete code for the sample application, select your programming language in the language selector.

[Complete Ruby Application](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/ruby/)

Each sample application repository includes a `README.md` file that you can use to learn how to set up your environment and run the application.

1. Assign application variables

   The code samples in this tutorial use the following variables to perform the Queryable Encryption workflow:

   - **kms\_provider\_name** - The KMS you use to store your Customer Master Key. Set this to your key provider: `"aws"`, `"azure"`, `"gcp"`, or `"kmip"`.

   - **uri** - Your MongoDB deployment connection URI. Set your connection URI in the `MONGODB_URI` environment variable or replace the value directly.

   - **key\_vault\_database\_name** - The MongoDB database where your data encryption keys (DEKs) will be stored. Set this to `"encryption"`.

   - **key\_vault\_collection\_name** - The collection in MongoDB where your DEKs will be stored. Set this to `"__keyVault"`, which is the convention to help prevent mistaking it for a user collection.

   - **key\_vault\_namespace** - The namespace in MongoDB where your DEKs will be stored. Set this to the values of the `key_vault_database_name` and `key_vault_collection_name` variables separated by a period, in the format `"#{key_vault_database_name}.#{key_vault_collection_name}"`.

   - **encrypted\_database\_name** - The MongoDB database where your encrypted data will be stored. Set this to `"medicalRecords"`.

   - **encrypted\_collection\_name** - The collection in MongoDB where your encrypted data will be stored. Set this to `"patients"`.

   You can declare these variables by using the following code:

   ```ruby
   kms_provider_name = ENV["KMS_PROVIDER"]
   uri = ENV["MONGODB_URI"] # Your connection URI
   key_vault_database_name = "encryption"
   key_vault_collection_name = "__keyVault"
   key_vault_namespace = "#{key_vault_database_name}.#{key_vault_collection_name}"
   encrypted_database_name = "medicalRecords"
   encrypted_collection_name = "patients"
   ```

   **Important: Key Vault Collection Namespace Permissions**

   The Key Vault collection is in the `encryption.__keyVault` namespace. Ensure that the database user your application uses to connect to MongoDB has [ReadWrite](/docs/manual/reference/built-in-roles#std-label-manual-reference-role-read-write) permissions on this namespace.

   **Tip: Environment Variables**

   The sample code in this tutorial references environment variables that you need to set. Alternatively, you can replace the values directly in the code.

   To learn how you can setup these environment variables, see the [README.md](https://github.com/mongodb/docs/tree/main/content/manual/upcoming/source/includes/qe-tutorials/ruby/README.md) file included in the sample application on GitHub.

2. Add your KMS credentials

   Create a variable containing your KMS credentials with the following structure.

   ```ruby
   kms_providers = {
     gcp: {
       email: ENV["GCP_EMAIL"], # Your GCP email
       privateKey: ENV["GCP_PRIVATE_KEY"] # Your GCP private key
     }
   }
   ```

3. Add your CMK credentials

   Create a variable containing your Customer Master Key credentials with the following structure. Use the credentials you recorded when you [created a CMK.](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-create-cmk-gcp)

   ```ruby
   customer_master_key_credentials = {
     projectId: ENV["GCP_PROJECT_ID"], # Your GCP Project ID
     location: ENV["GCP_LOCATION"], # Your GCP Key Location
     keyRing: ENV["GCP_KEY_RING"], # Your GCP Key Ring
     keyName: ENV["GCP_KEY_NAME"] # Your GCP Key Name
   }
   ```

4. Create an encryption client

   To create a client for encrypting and decrypting data in encrypted collections, instantiate a new `Mongo::Client` using your connection URI and automatic encryption options.

   ```ruby
   encrypted_client = Mongo::Client.new(uri, auto_encryption_options: auto_encryption_options)
   ```

## Next Steps

After installing a driver and dependencies, creating a Customer Master Key, and creating your application, see [Overview: Use Queryable Encryption](/docs/manual/core/queryable-encryption/overview-use-qe#std-label-qe-overview-use-qe) to encrypt and query data.
