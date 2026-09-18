> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Encryption Schemas

## Overview

On this page, you can learn how to create an encryption schema for automatic Client-Side Field Level Encryption (CSFLE) as well as see an example detailing how to create the encryption schema used in the CSFLE [Quick Start.](/docs/manual/core/csfle/quick-start#std-label-csfle-quick-start)

## Encryption Schemas

An encryption schema is a JSON object which uses a strict subset of [JSON Schema Draft 4 standard syntax](https://tools.ietf.org/html/draft-zyp-json-schema-04) along with the keywords `encrypt` and `encryptMetadata` to define the **encryption rules** that specify how your CSFLE-enabled client should encrypt your documents.

Encryption rules are JSON key-value pairs that define how your client application encrypts your fields. You must specify or inherit the following information in an encryption rule:

- The algorithm used to encrypt your field

- Which Data Encryption Key (DEK) your client uses to encrypt your field

- The [BSON](https://bsonspec.org/) type of your field

Encryption rules must contain either the `encrypt` or `encryptMetadata` keyword.

To learn more about the encryption algorithms you can define in your encryption schema, see [Fields and Encryption Types.](/docs/manual/core/csfle/fundamentals/encryption-algorithms#std-label-csfle-reference-encryption-algorithms)

To learn more about Data Encryption Keys, see [Encryption Keys and Key Vaults.](/docs/manual/core/queryable-encryption/fundamentals/keys-key-vaults#std-label-qe-reference-keys-key-vaults)

### encrypt Keyword

The `encrypt` keyword defines an encryption rule for a single field in a BSON document. Encryption rules containing the `encrypt` keyword have the following structure:

```json
"<field-name-to-encrypt>": {
  "encrypt": {
    "algorithm": "<encryption algorithm to use>",
    "bsonType": "<bson type of field>",
    "keyId": [UUID("<_id of your Data Encryption Key>" )]
  }
}

```

### encryptMetadata Keyword

The `encryptMetadata` keyword defines encryption rules which child elements of the sibling `properties` tag inherit. Encryption rules containing `encryptMetadata` have the following structure:

```json
"bsonType": "object",
"encryptMetadata": {
  "algorithm": "<encryption algorithm inherited by children of properties field>",
  "keyId": [UUID("<_id of your Data Encryption Key>" )]
},
"properties": { <object to inherit encryptMetadata values> }

```

### patternProperties Keyword

You can use the `patternProperties` keyword in your encryption schema to define encryption rules for all fields with names that match a regular expression. This allows you to specify multiple fields for encryption based on a single regular expression, or to specify them by only using a part of the field name. The `patternProperties` keyword replaces `properties` in your encryption schema.

Specify encryption rules with `patternProperties` using the following structure:

```json
"bsonType": "object",
"patternProperties": {
    "<regular expression to match>": {
    "encrypt": {
        "algorithm": "<encryption algorithm to use>",
        "bsonType": "<bson type of field>",
        "keyId": [UUID("<_id of your Data Encryption Key>" )]
    }
}

```

To see an example of how to use `patternProperties` see [Encryption Schema - Encrypt with Pattern Properties](/docs/manual/core/csfle/reference/encryption-schemas#std-label-field-level-encryption-auto-encrypt-with-pattern-properties)

## Example

This example explains how to generate the encryption schema used in the [Create an Encryption Schema For Your Documents](/docs/manual/core/csfle/quick-start#std-label-csfle-quickstart-encryption-schema) step of the CSFLE Quick Start.

In the Quick Start, you insert documents with the following structure into the `patients` collection of the `medicalRecords` database:

```json
{
  "_id": { "$oid": "<_id of your document>" },
  "name": "<name of patient>",
  "ssn": <integer>,
  "bloodType": "<blood type>",
  "medicalRecords": [
    { "weight": <integer>, "bloodPressure": "<blood pressure>" }
  ],
  "insurance": {
    "provider": "<provider name>",
    "policyNumber": <integer>
  }
}

```

### Specify the Namespace

At the root of your encryption schema, specify the namespace to which your encryption schema applies. Specify the following to encrypt and decrypt documents in the `patients` collection of the `medicalRecords` database:

```json
{
  "medicalRecords.patients": {
    <the schema created in the following steps of this example>
  }
}

```

### Specify the Data Encryption Key

In the Quick Start, you encrypt all fields of your document with a single Data Encryption Key (DEK). To configure all fields in your documents to use a single DEK for encryption and decryption, specify the `_id` of your DEK with the `encryptMetadata` keyword at the root of your encryption schema as follows:

```json
{
   "medicalRecords.patients": {
      "bsonType": "object",
      "encryptMetadata": {
         "keyId": [ UUID( "<_id of your Data Encryption Key>" ) ]
      },
      "properties": {
         <the schema created in the following steps of this example>
      }
   }
}

```

### Choose Encryption Rules

You decide to encrypt the following fields with the following encryption algorithms:

| Field Name | Encryption Algorithm | BSON Type |
| --- | --- | --- |
| `ssn` | Deterministic | Int |
| `bloodType` | Random | String |
| `medicalRecords` | Random | Array |
| `insurance.policyNumber` | Deterministic | Int |

You choose to encrypt the `ssn` and `insurance.policyNumber` fields with deterministic encryption for the following reasons:

- You want to be able to query on these fields.

- The values in these fields have a high cardinality, so this data is not susceptible to a frequency analysis attack.

You choose to encrypt the `bloodType` field with random encryption for the following reasons:

- You do not plan to query on this field.

- The values in this field have low cardinality, making them susceptible to a frequency analysis attack if you encrypted them deterministically.

You must encrypt the `medicalRecords` field with random encryption as CSFLE does not support deterministic encryption of fields of type `array`.

**Tip:**

To learn more about supported and unsupported automatic encryption operations, see [Supported Operations for Automatic Encryption.](/docs/manual/core/csfle/reference/supported-operations#std-label-csfle-reference-automatic-encryption-supported-operations)

### Specify Encryption Rules

To encrypt the `ssn` field with deterministic encryption, specify the following in your encryption schema:

```json
"ssn": {
    "encrypt": {
        "bsonType": "int",
        "algorithm": "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic"
    }
}

```

To encrypt the `bloodType` field with random encryption, specify the following in your encryption schema:

```json
"bloodType": {
    "encrypt": {
        "bsonType": "string",
        "algorithm": "AEAD_AES_256_CBC_HMAC_SHA_512-Random"
    }
}

```

To encrypt the `medicalRecords` field with random encryption, specify the following in your encryption schema:

```json
"medicalRecords": {
    "encrypt": {
        "bsonType": "array",
        "algorithm": "AEAD_AES_256_CBC_HMAC_SHA_512-Random"
    }
}

```

To encrypt the `insurance.policyNumber` field with deterministic encryption, specify the following in your encryption schema:

```json
"insurance": {
    "bsonType": "object",
    "properties": {
        "policyNumber": {
            "encrypt": {
                "bsonType": "int",
                "algorithm": "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic"
            }
        }
    }
}

```

### View the Complete Schema

The complete encryption schema for the Quick Start is as follows:

```json
{
  "medicalRecords.patients": {
    "bsonType": "object",
    "encryptMetadata": {
     "keyId": [UUID("<_id of your Data Encryption Key>" )]
   },
    "properties": {
      "insurance": {
        "bsonType": "object",
        "properties": {
          "policyNumber": {
            "encrypt": {
              "bsonType": "int",
              "algorithm": "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic"
            }
          }
        }
      },
      "medicalRecords": {
        "encrypt": {
          "bsonType": "array",
          "algorithm": "AEAD_AES_256_CBC_HMAC_SHA_512-Random"
        }
      },
      "bloodType": {
        "encrypt": {
          "bsonType": "string",
          "algorithm": "AEAD_AES_256_CBC_HMAC_SHA_512-Random"
        }
      },
      "ssn": {
        "encrypt": {
          "bsonType": "int",
          "algorithm": "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic"
        }
      }
    }
  }
}

```

## Learn More

To learn more about encryption schemas, see [CSFLE Encryption Schemas](/docs/manual/core/csfle/reference/encryption-schemas#std-label-csfle-reference-encryption-schemas)

To learn more about automatic encryption, see [Automatic Encryption.](/docs/manual/core/csfle/fundamentals/automatic-encryption#std-label-csfle-fundamentals-automatic-encryption)

To view the Quick Start, see [CSFLE Quick Start.](/docs/manual/core/csfle/quick-start#std-label-csfle-quick-start)
