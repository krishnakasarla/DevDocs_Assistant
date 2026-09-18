> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

<!--
Tab options on this page. Append to the .md URL to filter:
  ?tabs=<id,...>   select specific tabs (e.g. ?tabs=nodejs,shell)
  ?allTabs=true    include every tab
  (no param)       default: one tab per tabset

Available tabs:
  other tabs: aws, gcp, azure, kmip, local
-->

# How CSFLE Decrypts Documents

This page describes how CSFLE uses metadata from your Data Encryption Key and Customer Master Key to decrypt data.

## Metadata Used for Decryption

When you encrypt data using CSFLE, the data you encrypt is stored as a [`BinData`](/docs/manual/reference/mongodb-extended-json#mongodb-bsontype-Binary) subtype 6 object that includes the following metadata:

- The `_id` of the Data Encryption Key used to encrypt the data

- The encryption algorithm used to encrypt the data

Data Encryption Keys contain metadata that describes what Customer Master Key was used to encrypt them.

Drivers and [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) use this metadata to attempt to automatically decrypt your data.

## Automatic Decryption Process

To automatically decrypt your data, your CSFLE-enabled client performs the following procedure:

1. Check the `BinData` blob metadata of the field you intend to decrypt for the Data Encryption Key and encryption algorithm used to encrypt the value.

2. Check the Key Vault collection configured in the current database connection for the specified Data Encryption Key. If the Key Vault collection does not contain the specified key, automatic decryption fails and the driver returns an error.

3. Check the Data Encryption Key metadata for the Customer Master Key (CMK) used to encrypt the key material.

4. Decrypt the Data Encryption Key. This process varies by KMS provider:

   ### AWS

   For the Amazon Web Services (AWS) KMS, send the Data Encryption Key to your AWS KMS instance for decryption. If the CMK does not exist *or* if the connection configuration does not grant access to the CMK, decryption fails and the driver returns an error.

   **Tip:**

   To learn how to use the Amazon Web Services KMS for automatic encryption, see [Use Automatic Client-Side Field Level Encryption with AWS.](/docs/manual/core/csfle/tutorials/aws/aws-automatic#std-label-csfle-tutorial-automatic-aws)

5. Decrypt the `BinData` value using the decrypted Data Encryption Key and appropriate algorithm.

Applications with access to the MongoDB server that do not *also* have access to the required CMK and Data Encryption Keys cannot decrypt the `BinData` values.

## Automatically Encrypted Read Behavior

For read operations, the driver encrypts field values in the query document using your encryption schema *prior* to issuing the read operation.

Your client application then uses the `BinData` metadata to automatically decrypt the document you receive from MongoDB.

To learn more about encryption schemas, see [Encryption Schemas.](/docs/manual/core/csfle/fundamentals/create-schema#std-label-csfle-fundamentals-create-schema)

## Learn More

To learn how to configure the database connection for Client-Side Field Level Encryption, see [MongoClient Options for CSFLE.](/docs/manual/core/csfle/reference/csfle-options-clients#std-label-csfle-reference-mongo-client)

To learn more about the relationship between Data Encryption Keys and Customer Master Keys, see [Encryption Keys and Key Vaults.](/docs/manual/core/queryable-encryption/fundamentals/keys-key-vaults#std-label-qe-reference-keys-key-vaults)
