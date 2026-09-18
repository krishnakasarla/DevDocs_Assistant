> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Rotate and Rewrap Encryption Keys

Queryable Encryption equality and range queries are fully supported in production. Prefix, suffix, and substring queries are only available in public preview in MongoDB 8.2. Do not enable these query types in production. GA functionality of prefix, suffix and substring query types will be incompatible with the preview feature. To learn more, see [Supported Query Types](https://www.mongodb.com/docs/manual/core/queryable-encryption/reference/supported-operations/).

In this guide, you can learn how to manage your encryption keys with a Key Management System (KMS (Key Management System)) in your application.

## Overview

This procedure shows you how to rotate encryption keys for Queryable Encryption using [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh). Rotating DEKs consists of rewrapping them with a new Customer Master Key, so the terms "rotate" and "rewrap" are sometimes used interchangeably.

After completing this guide, you should be able to rotate your Customer Master Key (CMK (Customer Master Key)) on your Key Management System, and then rewrap existing DEKs in your Key Vault collection with your new CMK (Customer Master Key).

**Warning:**

As you rotate keys, confirm that they aren't used to encrypt any keys or data before deleting them. If you delete a DEK (Data Encryption Key), all fields encrypted with that DEK (Data Encryption Key) become permanently unreadable. If you delete a CMK (Customer Master Key), all fields encrypted with a DEK (Data Encryption Key) using that CMK (Customer Master Key) become permanently unreadable.

### Related Information

For a detailed explanation of the concepts included in this procedure, refer to the topics below.

To learn more about keys and key vaults, see [Encryption Keys and Key Vaults](/docs/manual/core/queryable-encryption/fundamentals/keys-key-vaults#std-label-qe-reference-keys-key-vaults). To view a list of supported KMS (Key Management System) providers, see the [KMS Providers](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-fundamentals-kms-providers) page.

For tutorials detailing how to set up a Queryable Encryption enabled application with each of the supported KMS (Key Management System) providers, see [Overview: Enable Queryable Encryption.](/docs/manual/core/queryable-encryption/overview-enable-qe#std-label-qe-overview-enable-qe)

## Procedure

1. Rotate your Customer Master Key on your Key Management System

   The process for rotating your CMK (Customer Master Key) depends on your KMS (Key Management System) provider. For details, refer to your key provider's documentation:

   - AWS: [Rotating AWS KMS Keys](https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html)

   - Azure: [Configure cryptographic key auto-rotation in Azure Key Vault](https://learn.microsoft.com/en-us/azure/key-vault/keys/how-to-configure-key-rotation)

   - GCP: [Rotate a key](https://cloud.google.com/kms/docs/rotate-key)

   Once you rotate the CMK (Customer Master Key), MongoDB uses it to wrap all new DEKs. To re-wrap existing DEKs, continue to the following steps.

2. Rotate your Data Encryption Keys using `KeyVault.rewrapManyDataKey()`

   The [`KeyVault.rewrapManyDataKey()`](/docs/manual/reference/method/KeyVault.rewrapManyDataKey#mongodb-method-KeyVault.rewrapManyDataKey) method automatically decrypts multiple Data Encryption Keys and re-encrypts them using the specified CMK (Customer Master Key). It then updates the keys in the Key Vault collection.

   The method has the following syntax:

   ```javascript
   let keyVault = db.getMongo().getKeyVault()

   keyVault.rewrapManyDataKey(
      {
         "<Query filter document>"
      },
      {
         provider: "<KMS provider>",
         masterKey: {
            "<dataKeyOpts Key>" : "<dataKeyOpts Value>"
         }
      }
   )
   ```

   1. Specify a query filter document to select the keys to rotate, or omit the argument to rotate all keys in the Key Vault collection

      If you specify a [query filter document](/docs/manual/core/documents-other-uses#std-label-document-query-filter), but no keys match, then no keys rotate.

   2. Specify the KMS (Key Management System) provider

   3. Specify the `masterKey` using the new CMK (Customer Master Key), or omit the argument to rotate keys using their existing CMK (Customer Master Key)

Your DEKs themselves are left unchanged after re-wrapping them with the new CMK (Customer Master Key). The key rotation process is seamless, and does not interrupt your application.
