> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

<!--
Tab options on this page. Append to the .md URL to filter:
  ?tabs=<id,...>   select specific tabs (e.g. ?tabs=nodejs,shell)
  ?allTabs=true    include every tab
  (no param)       default: one tab per tabset

Available tabs:
  drivers: shell, csharp, go, java-sync, nodejs, python
-->

# Create a Customer Master Key

Queryable Encryption equality and range queries are fully supported in production. Prefix, suffix, and substring queries are only available in public preview in MongoDB 8.2. Do not enable these query types in production. GA functionality of prefix, suffix and substring query types will be incompatible with the preview feature. To learn more, see [Supported Query Types](https://www.mongodb.com/docs/manual/core/queryable-encryption/reference/supported-operations/).

## Overview

In this guide, you will learn how to generate a Customer Master Key in your Key Management System of choice. Generate a Customer Master Key before creating your Queryable Encryption-enabled application.

**Tip: Customer Master Keys**

To learn more about the Customer Master Key, see [Encryption Keys and Key Vaults](/docs/manual/core/queryable-encryption/fundamentals/keys-key-vaults#std-label-qe-reference-keys-key-vaults)

## Before You Start

Complete the preceding tasks before continuing:

1. [Install a Queryable Encryption compatible driver and dependencies](/docs/manual/core/queryable-encryption/install#std-label-qe-install)

2. [Install and configure a Queryable Encryption library](/docs/manual/core/queryable-encryption/install-library#std-label-qe-csfle-install-library)

## Procedure

Select your key provider below.

1. Create the Customer Master Key

   Log in to your [AWS Management Console.](https://aws.amazon.com/console/)

   Navigate to the [AWS KMS Console.](https://aws.amazon.com/kms/)

   Create your Customer Master Key

   Create a new symmetric key by following the official AWS documentation on [Creating symmetric KMS keys](https://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html#create-symmetric-cmk). The key you create is your Customer Master Key. Choose a name and description that helps you identify it; these fields do not affect the functionality or configuration of your CMK (Customer Master Key).

   In the Usage Permissions step of the key generation process, apply the following default key policy that enables Identity and Access Management (IAM (Identity and Access Management)) policies to grant access to your Customer Master Key:

   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Sid": "Enable IAM User Permissions",
         "Effect": "Allow",
         "Principal": {
           "AWS": "<ARN of your AWS account principal>"
         },
         "Action": "kms:*",
         "Resource": "*"
       }
     ]
   }

   ```

   **Important:**

   Record the Amazon Resource Name (ARN (Amazon Resource Name)) and Region of your Customer Master Key. You will use these in later steps of this guide.

   **Tip: Key Policies**

   To learn more about key policies, see [Key Policies in AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html) in the official AWS documentation.

2. Create an AWS IAM User

   Navigate to the [AWS IAM Console.](https://aws.amazon.com/iam/)

   Create an IAM User

   Create a new programmatic IAM (Identity and Access Management) user in the AWS management console by following the official AWS documentation on [Adding a User](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html). You will use this IAM (Identity and Access Management) user as a service account for your Queryable Encryption-enabled application. Your application authenticates with AWS KMS using the IAM (Identity and Access Management) user to encrypt and decrypt your Data Encryption Keys (DEKs) with your Customer Master Key (CMK).

   **Important: Record your Credentials**

   Ensure you record the following IAM (Identity and Access Management) credentials in the final step of creating your IAM (Identity and Access Management) user:

   - **access key ID**

   - **secret access key**

   You have one opportunity to record these credentials. If you do not record these credentials during this step, you must create another IAM (Identity and Access Management) user.

   Grant Permissions

   Grant your IAM (Identity and Access Management) user `kms:Encrypt` and `kms:Decrypt` permissions for your remote master key.

   **Important:**

   The new client IAM (Identity and Access Management) user *should not* have administrative permissions for the master key. To keep your data secure, follow the [principle of least privilege.](https://en.wikipedia.org/w/index.php?title=Principle_of_least_privilege\&oldid=1080333157)

   The following inline policy allows an IAM (Identity and Access Management) user to encrypt and decrypt with the Customer Master Key with the least privileges possible:

   **Note: Remote Master Key ARN**

   The following policy requires the ARN (Amazon Resource Name) of the key you generate in the [Create the Master Key](/docs/manual/core/queryable-encryption/qe-create-cmk#std-label-qe-aws-create-master-key) step of this guide.

   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": ["kms:Decrypt", "kms:Encrypt"],
         "Resource": "<the Amazon Resource Name (ARN) of your remote master key>"
       }
     ]
   }

   ```

   To apply the preceding policy to your IAM (Identity and Access Management) user, follow the [Adding IAM identity permissions](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage-attach-detach.html#add-policies-console) guide in the AWS documentation.

   **Important: Authenticate with IAM Roles in Production**

   When deploying your Queryable Encryption-enabled application to a production environment, authenticate your application by using an IAM (Identity and Access Management) role instead of an IAM (Identity and Access Management) user.

   To learn more about IAM (Identity and Access Management) roles, see the following pages in the official AWS documentation:

   - [IAM roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)

   - [When to create an IAM role (instead of a user)](https://docs.aws.amazon.com/IAM/latest/UserGuide/id.html#id_which-to-choose_role)

1) Register your Application with Azure

   Log in to [Azure.](https://azure.microsoft.com/en-us/features/azure-portal/)

   Register your Application with Azure Active Directory

   To register an application on Azure Active Directory, follow Microsoft's official [Register an application with the Microsoft identity platform](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app) Quick Start.

   ### MongoDB Shell

   **Important: Record your Credentials**

   Ensure you record the following credentials:

   - **Tenant ID**

   - **Client ID**

   - **Client secret**

   You need these credentials to construct your `kmsProviders` object later in this tutorial. You can also authenticate by using an access token or automatic credential fetching. To learn about all available credential forms for Azure, see [kmsProviders Object.](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-kms-provider-object-azure)

2) Create the Customer Master Key

   Create your Azure Key Vault and Customer Master Key

   To create a new Azure Key Vault instance and Customer Master Key, follow Microsoft's official [Set and retrieve a key from Azure Key Vault using the Azure portal](https://docs.microsoft.com/en-us/azure/key-vault/keys/quick-create-portal) Quick Start.

   **Important: Record your Credentials**

   Ensure you record the following credentials:

   - **Key Name**

   - **Key Identifier** (referred to as `keyVaultEndpoint` later in this guide)

   - **Key Version**

   You will need them to construct your `dataKeyOpts` object later in this tutorial.

   Grant Permissions

   Grant your client application `wrap` and `unwrap` permissions to the key.

1. Register a GCP (Google Cloud Platform) Service Account

   Register or log in to your existing account on [Google Cloud.](https://cloud.google.com)

   Create a service account for your project

   To create a service account on Google Cloud, follow the [Creating a service account](https://cloud.google.com/iam/docs/creating-managing-service-accounts#creating) guide in Google's official documentation.

   Add a service account key

   To add a service account key on Google Cloud, follow the [Managing service account keys](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) guide in Google's official documentation.

   ### MongoDB Shell

   **Important:**

   When creating your service account key, you receive a one-time download of the private key information. Make sure to download this file in either the PKCS12 or JSON format for use later in this tutorial.

2. Create a GCP (Google Cloud Platform) Customer Master Key

   Create a new Customer Master Key

   Create a key ring and a symmetric key by following the [Create a key](https://cloud.google.com/kms/docs/creating-keys) guide from Google's official documentation.

   This key is your Customer Master Key (CMK (Customer Master Key)).

   Record the following details of your CMK (Customer Master Key) for use in a future step of this tutorial.

   | Field | Required | Description |
   | --- | --- | --- |
   | key_name | Yes | Identifier for the CMK (Customer Master Key). |
   | key_ring | Yes | Identifier for the group of keys your key belongs to. |
   | key_version | No | The version of the named key. |
   | location | Yes | Region specified for your key. |
   | endpoint | No | The host and optional port of the Google Cloud KMS. The default value is `cloudkms.googleapis.com`. |

1) Configure your KMIP-Compliant Key Provider

   To connect a MongoDB driver client to your KMIP (Key Management Interoperability Protocol)-compliant key provider, you must configure your KMIP (Key Management Interoperability Protocol)-compliant key provider such that it accepts your client's TLS certificate.

   Consult the documentation for your KMIP (Key Management Interoperability Protocol)-compliant key provider for information on how to accept your client certificate.

2) Specify your Certificates

   Your client must connect to your KMIP (Key Management Interoperability Protocol)-compliant key provider through TLS and present a client certificate that your KMIP (Key Management Interoperability Protocol)-compliant key provider accepts:

   ### MongoDB Shell

   ```javascript
   const tlsOptions = {
     kmip: {
       tlsCAFile: process.env["KMIP_TLS_CA_FILE"], // Path to your TLS CA file
       tlsCertificateKeyFile: process.env["KMIP_TLS_CERT_FILE"], // Path to your TLS certificate key file
     },
   };
   ```

## Next Steps

After installing drivers and dependencies and creating a Customer Master Key, you can [create your Queryable Encryption enabled application.](/docs/manual/core/queryable-encryption/qe-create-application#std-label-qe-create-application)
