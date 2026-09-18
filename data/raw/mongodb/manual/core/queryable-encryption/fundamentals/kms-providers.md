> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# KMS Providers

Queryable Encryption equality and range queries are fully supported in production. Prefix, suffix, and substring queries are only available in public preview in MongoDB 8.2. Do not enable these query types in production. GA functionality of prefix, suffix and substring query types will be incompatible with the preview feature. To learn more, see [Supported Query Types](https://www.mongodb.com/docs/manual/core/queryable-encryption/reference/supported-operations/).

## Overview

Learn about the Key Management System (KMS (Key Management System)) providers In-Use Encryption supports.

## Reasons to Use a Remote Key Management System

Using a remote Key Management System to manage your Customer Master Key has the following advantages over using your local filesystem to host it:

- Secure storage of the key with access auditing

- Reduced risk of access permission issues

- Availability and distribution of the key to remote clients

- Automated key backup and recovery

- Centralized encryption key lifecycle management

Additionally, for the following KMS (Key Management System) providers, your KMS (Key Management System) remotely encrypts and decrypts your Data Encryption Key, ensuring your Customer Master Key is never exposed to your Queryable Encryption or CSFLE enabled application:

- Amazon Web Services KMS

- Azure Key Vault

- Google Cloud KMS

## Key Management System Tasks

In In-Use Encryption, your Key Management System:

- Creates and encrypts the Customer Master Key

- Encrypts the Data Encryption Keys created by your application

- Decrypts Data Encryption Keys

To learn more about Customer Master Keys and Data Encryption Keys, see [Encryption Keys and Key Vaults.](/docs/manual/core/queryable-encryption/fundamentals/keys-key-vaults#std-label-qe-reference-keys-key-vaults)

### Create and Store your Customer Master Key

To create a Customer Master Key, configure your Key Management System to generate your Customer Master Key as follows:

![Diagram](/images/CSFLE_Master_Key_KMS.png)

To view a tutorial that demonstrates how to create and store a CMK (Customer Master Key) in your preferred KMS (Key Management System), see the [Queryable Encryption Automatic Encryption Tutorial](/docs/manual/core/queryable-encryption/tutorials#std-label-qe-tutorial-automatic-encryption) or [CSFLE Automatic Encryption Tutorial.](/docs/manual/core/csfle/tutorials#std-label-csfle-tutorial-automatic-encryption)

### Create and Encrypt a Data Encryption Key

To create a Data Encryption Key:

- Instantiate a `ClientEncryption` instance in your Queryable Encryption or CSFLE enabled application:

  - Provide a `kmsProviders` object that specifies the credentials your application uses to authenticate with your KMS (Key Management System) provider.

- Create a Data Encryption Key with the `CreateDataKey` method of the `ClientEncryption` object in your application.

  - Provide a `dataKeyOpts` object that specifies with which key your KMS (Key Management System) should encrypt your new Data Encryption Key.

To view a tutorial demonstrating how to create and encrypt a Data Encryption Key, see the following resources:

- [Queryable Encryption Quick Start](/docs/manual/core/queryable-encryption/quick-start#std-label-qe-quick-start)

- [Queryable Encryption Automatic Encryption Tutorial](/docs/manual/core/queryable-encryption/tutorials#std-label-qe-tutorial-automatic-encryption)

- [CSFLE Quick Start](/docs/manual/core/csfle/quick-start#std-label-csfle-quick-start)

- [CSFLE Automatic Encryption Tutorial](/docs/manual/core/csfle/tutorials#std-label-csfle-tutorial-automatic-encryption)

To view the structure of `kmsProviders` and `dataKeyOpts` objects for all supported KMS (Key Management System) providers, see [Supported Key Management Services.](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-fundamentals-kms-providers-supported-kms)

## Supported Key Management Services

The following sections of this page present the following information for all Key Management System providers:

- Architecture of In-Use Encryption enabled client

- Structure of `kmsProviders` objects

- Structure of `dataKeyOpts` objects

Both Queryable Encryption and CSFLE support the following Key Management System providers:

- [Amazon Web Services KMS](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-fundamentals-kms-providers-aws)

- [Azure Key Vault](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-fundamentals-kms-providers-azure)

- [Google Cloud Platform KMS](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-fundamentals-kms-providers-gcp)

- [KMIP](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-fundamentals-kms-providers-kmip)

- [Local Key Provider](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-fundamentals-kms-providers-local)

### Amazon Web Services KMS

This section provides information related to using [AWS Key Management Service](https://aws.amazon.com/kms/) in your Queryable Encryption or CSFLE enabled application.

To view a tutorial demonstrating how to use AWS KMS in your application, see [Overview: Enable Queryable Encryption](/docs/manual/core/queryable-encryption/overview-enable-qe#std-label-qe-overview-enable-qe) or [Use Automatic Client-Side Field Level Encryption with AWS.](/docs/manual/core/csfle/tutorials/aws/aws-automatic#std-label-csfle-tutorial-automatic-aws)

#### Architecture

The following diagram describes the architecture of a Queryable Encryption enabled application using AWS (Amazon Web Services) KMS.

![Diagram KMS](/images/CSFLE_Data_Key_KMS.png)

**Note: Client Can't Access Customer Master Key**

When using the preceding Key Management System, your Queryable Encryption enabled application does not have access to your Customer Master Key.

#### kmsProviders Object

The following table presents the structure of a `kmsProviders` object for AWS KMS:

| Field | Required for IAM User | Required for IAM Role | Description |
| --- | --- | --- | --- |
| Access Key ID | Yes | Yes | Identifies the account user. |
| Secret Access Key | Yes | Yes | Contains the authentication credentials of the account user. |
| Session Token | No | Yes | Contains a token obtained from AWS Security Token Service (STS). |

To use automatic credential fetching, specify an empty object for the `aws` credential. The driver then fetches credentials using its standard AWS credential lookup flow:

```json
{ "aws": {} }
```

#### dataKeyOpts Object

The following table presents the structure of a `dataKeyOpts` object for AWS KMS:

| Field | Required | Description |
| --- | --- | --- |
| key | Yes | [Amazon Resource Number (ARN)](https://docs.aws.amazon.com/kms/latest/developerguide/viewing-keys.html#find-cmk-id-arn) of the master key. |
| region | No | AWS region of your master key, e.g. "us-west-2"; required only if not specified in your ARN. |
| endpoint | No | Custom hostname for the AWS endpoint if configured for your account. |

### Azure Key Vault

This section provides information related to using [Azure Key Vault](https://azure.microsoft.com/en-us/services/key-vault/) in your Queryable Encryption or CSFLE enabled application.

To view a tutorial demonstrating how to use Azure Key Vault in your application, see [Overview: Enable Queryable Encryption](/docs/manual/core/queryable-encryption/overview-enable-qe#std-label-qe-overview-enable-qe) or [Use Automatic Client-Side Field Level Encryption with Azure.](/docs/manual/core/csfle/tutorials/azure/azure-automatic#std-label-csfle-tutorial-automatic-azure)

#### Architecture

The following diagram describes the architecture of a Queryable Encryption enabled application using Azure Key Vault.

![Diagram KMS](/images/CSFLE_Data_Key_KMS.png)

**Note: Client Can't Access Customer Master Key**

When using the preceding Key Management System, your Queryable Encryption enabled application does not have access to your Customer Master Key.

#### kmsProviders Object

The following table presents the structure of a `kmsProviders` object for Azure Key Vault:

| Field | Required | Description |
| --- | --- | --- |
| azure.tenantId | Yes | Identifies the organization of the account. |
| azure.clientId | Yes | Identifies the clientId to authenticate your registered application. |
| azure.clientSecret | Yes | Used to authenticate your registered application. |
| azure.identityPlatformEndpoint | No | Specifies a hostname and port number for the authentication server. Defaults to login.microsoftonline.com and is only needed for non-commercial Azure instances such as a government or China account. |

To use an access token instead of service principal credentials, specify the `azure.accessToken` field:

```json
{ "azure": { "accessToken": "<access token>"} }
```

To use automatic credential fetching, specify an empty object for the `azure` credential. The driver then retrieves credentials from the Azure Instance Metadata Service:

```json
{ "azure": {} }
```

#### dataKeyOpts Object

The following table presents the structure of a `dataKeyOpts` object for Azure Key Vault:

| Field | Required | Description |
| --- | --- | --- |
| keyName | Yes | Name of the master key |
| keyVersion | No, but strongly recommended | Version of the master key |
| keyVaultEndpoint | Yes | URL of the key vault. For example: `myVaultName.vault.azure.net` |

**Warning:**

If you do not include a `keyVersion` field, Azure Key Vault attempts to decrypt Data Encryption Keys using the latest Customer Master Key. If you rotate the CMK (Customer Master Key) but do not [rewrap the Data Encryption Keys](/docs/manual/core/queryable-encryption/fundamentals/manage-keys#std-label-qe-fundamentals-manage-keys) with the new master key, attempting to decrypt an existing DEK (Data Encryption Key) fails, since the DEK (Data Encryption Key) is encrypted with the previous version of the CMK (Customer Master Key).

### Google Cloud Platform KMS

This section provides information related to using [Google Cloud Key Management](https://cloud.google.com/security-key-management) in your Queryable Encryption or CSFLE enabled application.

To view a tutorial demonstrating how to use GCP KMS in your application, see [Overview: Enable Queryable Encryption](/docs/manual/core/queryable-encryption/overview-enable-qe#std-label-qe-overview-enable-qe) or [Use Automatic Client-Side Field Level Encryption with GCP.](/docs/manual/core/csfle/tutorials/gcp/gcp-automatic#std-label-csfle-tutorial-automatic-gcp)

#### Architecture

The following diagram describes the architecture of a Queryable Encryption enabled application using GCP KMS.

![Diagram KMS](/images/CSFLE_Data_Key_KMS.png)

**Note: Client Can't Access Customer Master Key**

When using the preceding Key Management System, your Queryable Encryption enabled application does not have access to your Customer Master Key.

#### kmsProviders Object

The following table presents the structure of a `kmsProviders` object for GCP KMS:

| Field | Required | Description |
| --- | --- | --- |
| email | Yes | Identifies your service account email address. |
| privateKey | Yes | Identifies your service account private key in either [base64 string](https://en.wikipedia.org/wiki/Base64) or [Binary subtype 0](https://www.mongodb.com/docs/manual/reference/mongodb-extended-json/#bson.Binary) format without the prefix and suffix markers.Suppose your service account private key value is as follows: `-----BEGIN PRIVATE KEY-----\nyour-private-key\n-----END PRIVATE KEY-----\n` The value you would specify for this field is: `your-private-key` If you have a `user-key.json` credential file, you can extract the string by executing the following command in a bash or similar shell. The following command requires that you install [OpenSSL](https://docs.openssl.org/master/) : `cat user-key.json | jq -r .private_key | openssl pkcs8 -topk8 -nocrypt -inform PEM -outform DER | base64 -w 0` |
| endpoint | No | Specifies a hostname and port number for the authentication server. Defaults to oauth2.googleapis.com. |

To use an access token instead of service account credentials, specify the `accessToken` field:

```json
{ "gcp": { "accessToken": "<access token>" } }
```

To use automatic credential fetching, specify an empty object for the `gcp` credential. The driver then retrieves credentials from the GCP metadata service:

```json
{ "gcp": {} }
```

#### dataKeyOpts Object

The following table presents the structure of a `dataKeyOpts` object for GCP KMS:

| Field | Required | Description |
| --- | --- | --- |
| projectId | Yes | Identifier for your project in which you created the key. |
| location | Yes | Region specified for your key. |
| keyRing | Yes | Identifier for the group of keys your key belongs to. |
| keyName | Yes | Identifier for the symmetric master key. |
| keyVersion | No | Specifies the version of the named key. If not specified, the default version of the key is used. |
| endpoint | No | Specifies the host and optional port of the Cloud KMS. The default is `cloudkms.googleapis.com`. |

### KMIP

This section provides information related to using a [KMIP](https://docs.oasis-open.org/kmip/spec/v1.0/os/kmip-spec-1.0-os.html) compliant Key Management System in your Queryable Encryption or CSFLE enabled application.

To learn how to set up KMIP with HashiCorp Vault, see [Manage client encryption keys with Vault as a KMIP server](https://developer.hashicorp.com/vault/tutorials/enterprise/kmip-engine) in the HashiCorp Vault documentation.

#### Architecture

The following diagram describes the architecture of a Queryable Encryption enabled application using a KMIP (Key Management Interoperability Protocol)-compliant key provider.

![Diagram](/images/CSFLE_Data_Key_KMIP.png)

**Important: Client Accesses Customer Master Key**

When your Queryable Encryption enabled application uses a KMIP (Key Management Interoperability Protocol)-compliant key provider without specifying the `delegated` option, your application directly accesses your Customer Master Key. To avoid directly accessing your CMK (Customer Master Key), you can set the `delegated` option to `true` in your [dataKeyOpts object.](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-fundamentals-kms-providers-kmip-datakeyopts)

#### kmsProviders Object

The following table presents the structure of a `kmsProviders` object for a KMIP compliant Key Management System:

**Note: Authenticate through TLS/SSL**

Your Queryable Encryption enabled application authenticates through TLS/SSL (Transport Layer Security/Secure Sockets Layer) when using KMIP.

| Field | Required | Description |
| --- | --- | --- |
| endpoint | Yes | Specifies a hostname and port number for the authentication server. |

#### dataKeyOpts Object

The following table presents the structure of a `dataKeyOpts` object for a KMIP compliant Key Management System:

| Field | Required | Description |
| --- | --- | --- |
| keyId | No | The `keyId` field of a 96 byte [Secret Data managed object](http://docs.oasis-open.org/kmip/spec/v1.4/os/kmip-spec-v1.4-os.html#_Toc490660780) stored in your KMIP (Key Management Interoperability Protocol)-compliant key provider. If you do not specify the `keyId` field in the `masterKey` document you send to your KMIP (Key Management Interoperability Protocol)-compliant key provider, the driver creates a new 96 Byte Secret Data managed object in your KMIP (Key Management Interoperability Protocol)-compliant key provider to act as your master key. |
| endpoint | Yes | The URI of your KMIP (Key Management Interoperability Protocol)-compliant key provider. |
| delegated | No | Set this option to `true` to delegate the encryption and decryption of your DEK (Data Encryption Key) to your KMIP (Key Management Interoperability Protocol)-compliant key provider. Delegating these to the KMIP (Key Management Interoperability Protocol)-compliant key provider ensures that you never have direct access to the CMK (Customer Master Key). If you do not set the `delegated` option to `true`, your application directly accesses and transports your Customer Master Key from the KMIP provider. IMPORTANT: The `delegated` option is not available in the Ruby or Go drivers. |

### Local Key Provider

This section provides information related to using a Local Key Provider in your Queryable Encryption or CSFLE enabled application.

**Warning: Secure your Local Key File in Production**

We recommend storing your Customer Master Keys in a remote [Key Management System](https://en.wikipedia.org/wiki/Key_management#Key_management_system) (KMS (Key Management System)). To learn how to use a remote KMS (Key Management System) in your Queryable Encryption implementation, see the [Queryable Encryption Tutorials](/docs/manual/core/queryable-encryption/tutorials#std-label-qe-tutorial-automatic-encryption) guide.

If you choose to use a local key provider in production, exercise great caution and do not store it on the file system. Consider injecting the key into your client application using a sidecar process, or use another approach that keeps the key secure.

To view a tutorial demonstrating how to use a Local Key Provider for testing Queryable Encryption, see the [Queryable Encryption Quick Start](/docs/manual/core/queryable-encryption/quick-start#std-label-qe-quick-start) or [CSFLE Quick Start.](/docs/manual/core/csfle/quick-start#std-label-csfle-quick-start)

#### Architecture

When you use a Local Key Provider for testing, your application retrieves your Customer Master Key from the computer it runs on. To use a Local Key Provider in production, use an approach that doesn't store the key on the file system. For example, you can inject the key into the client process via a sidecar.

The following diagram describes the architecture of a Queryable Encryption-enabled application using a Local Key Provider.

![Local Key Provider architecture diagram.](/images/CSFLE_Data_Key_Local.png)

#### kmsProviders Object

The following table presents the structure of a `kmsProviders` object for a Local Key Provider:

| Field | Required | Description |
| --- | --- | --- |
| key | Yes | The master key used to encrypt/decrypt data keys. The master key is passed as a base64 encoded string. |

#### dataKeyOpts Object

When you use a Local Key Provider, you specify your Customer Master Key through your `kmsProviders` object.
