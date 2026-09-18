> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# CSFLE Encryption Schemas

## Overview

**Note: Enterprise Feature**

The automatic feature of field level encryption is only supported in MongoDB Enterprise 6.0 or later, and MongoDB Atlas 6.0 or later clusters.

Encryption schemas contain user-specified rules that identify which fields must be encrypted and how to encrypt those fields. Applications must specify the automatic encryption rules using a strict subset of the [JSON Schema Draft 4 standard syntax](https://tools.ietf.org/html/draft-zyp-json-schema-04) and the following encryption-specific keywords:

- [Encrypt](/docs/manual/core/csfle/reference/encryption-schemas#std-label-csfle-reference-encryption-schemas-encrypt-keyword) specifies the encryption options to use when encrypting the current field.

- [Encrypt Metadata](/docs/manual/core/csfle/reference/encryption-schemas#std-label-field-level-encryption-encryptMetadata-keyword) specifies inheritable encryption options.

For the MongoDB shell, use the [`Mongo()`](/docs/manual/reference/method/Mongo#mongodb-method-Mongo) constructor to create the database connection with the automatic encryption rules included as part of the Client-Side Field Level Encryption [configuration object](/docs/manual/reference/method/Mongo#std-label-autoEncryptionOpts). See [Connect to a Cluster with Automatic Client-Side Encryption Enabled](/docs/manual/reference/method/Mongo#std-label-mongo-connection-automatic-client-side-encryption-enabled) for an example.

For the official MongoDB drivers, use the driver-specific database connection constructor (`MongoClient`) to create the database connection with the automatic encryption rules included as part of the Client-Side Field Level Encryption configuration object. To learn more about CSFLE-specific `MongoClient` options, see the [mongo client](/docs/manual/core/csfle/reference/csfle-options-clients#std-label-csfle-reference-mongo-client) page.

**Important: Don't Specify Schema Validation Keywords In Your Encryption Schema**

Do  **not** specify schema validation keywords in the automatic encryption rules. To define schema validation rules, configure [schema validation.](/docs/manual/core/schema-validation#std-label-schema-validation-overview)

## Definition

*Object*

```json
"bsonType" : "object",
"properties" : {
  "<fieldName>" : {
    "encrypt" : {
      "algorithm" : "<string>",
      "bsonType" : "<string>" | [ "<string>" ],
      "keyId" : [ <UUID> ]
    }
  }
}
```

Indicates that `<fieldName>` must be encrypted. The `encrypt` object has the following requirements:

- `encrypt` cannot have any sibling fields in the `<fieldName>` object. `encrypt` must be the only child of the `<fieldName>` object.

- `encrypt` cannot be specified within any subschema of the `items` or `additionalItems` keywords. Specifically, automatic Client-Side Field Level Encryption does not support encrypting individual elements of an array.

The `encrypt` object can contain **only** the following fields:

- [`algorithm`](/docs/manual/core/csfle/reference/encryption-schemas#mongodb-autoencryptkeyword-autoencryptkeyword.encrypt.algorithm)

- [`bsonType`](/docs/manual/core/csfle/reference/encryption-schemas#mongodb-autoencryptkeyword-autoencryptkeyword.encrypt.bsonType)

- [`keyId`](/docs/manual/core/csfle/reference/encryption-schemas#mongodb-autoencryptkeyword-autoencryptkeyword.encrypt.keyId)

Including any other field to the `encrypt` object results in errors when issuing automatically encrypted read or write operations

If [`keyId`](/docs/manual/core/csfle/reference/encryption-schemas#mongodb-autoencryptkeyword-autoencryptkeyword.encrypt.keyId) or [`algorithm`](/docs/manual/core/csfle/reference/encryption-schemas#mongodb-autoencryptkeyword-autoencryptkeyword.encrypt.algorithm) are omitted, the [Automatic Encryption Shared Library](/docs/manual/core/csfle/reference/install-library#std-label-csfle-reference-shared-library) checks all parent fields and attempts to construct those options from the nearest [`encryptMetadata`](/docs/manual/core/csfle/reference/encryption-schemas#mongodb-autoencryptkeyword-autoencryptkeyword.encryptMetadata) object that specifies the option. [`bsonType`](/docs/manual/core/csfle/reference/encryption-schemas#mongodb-autoencryptkeyword-autoencryptkeyword.encrypt.bsonType) cannot be inherited and *may* be required depending on the value of [`algorithm`.](/docs/manual/core/csfle/reference/encryption-schemas#mongodb-autoencryptkeyword-autoencryptkeyword.encrypt.algorithm)

If the Automatic Encryption Shared Library cannot construct the full `encrypt` object using the fields specified to the object and any required `encryptMetadata`-inherited keys, automatic encryption fails and returns an error.

*String*

Indicates which encryption algorithm to use when encrypting values of `<fieldName>`. Supports the following algorithms *only*:

- `AEAD_AES_256_CBC_HMAC_SHA_512-Random`

- `AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic`

For complete documentation on the encryption algorithms, see [Fields and Encryption Types.](/docs/manual/core/csfle/fundamentals/encryption-algorithms#std-label-csfle-reference-encryption-algorithms)

If omitted, the [Automatic Encryption Shared Library](/docs/manual/core/csfle/reference/install-library#std-label-csfle-reference-shared-library) checks all parent fields for the closest ancestor containing an [`encryptMetadata.algorithm`](/docs/manual/core/csfle/reference/encryption-schemas#mongodb-autoencryptkeyword-autoencryptkeyword.encryptMetadata.algorithm) key and inherits that value. If no parent [`algorithm`](/docs/manual/core/csfle/reference/encryption-schemas#mongodb-autoencryptkeyword-autoencryptkeyword.encryptMetadata.algorithm) exists, automatic field level encryption fails and returns an error.

- If `encrypt.algorithm` or its inherited value is `AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic`, the `encrypt` object *requires* the [`encrypt.bsonType`](/docs/manual/core/csfle/reference/encryption-schemas#mongodb-autoencryptkeyword-autoencryptkeyword.encrypt.bsonType) field.

- If `encrypt.algorithm` or its inherited value is `AEAD_AES_256_CBC_HMAC_SHA_512-Random`, the `encrypt` object *may* include the [`encrypt.bsonType`](/docs/manual/core/csfle/reference/encryption-schemas#mongodb-autoencryptkeyword-autoencryptkeyword.encrypt.bsonType) field.

*String | Array of Strings*

The [BSON type](/docs/manual/reference/bson-types#std-label-bson-types) of the field being encrypted. Required if [`encrypt.algorithm`](/docs/manual/core/csfle/reference/encryption-schemas#mongodb-autoencryptkeyword-autoencryptkeyword.encrypt.algorithm) is `AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic`.

If [`encrypt.algorithm`](/docs/manual/core/csfle/reference/encryption-schemas#mongodb-autoencryptkeyword-autoencryptkeyword.encrypt.algorithm) or its inherited value is `AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic`, `bsonType` *must* specify a *single* type.  `bsonType` does **not** support any of the following BSON types with the deterministic encryption algorithm:

- `double`

- `decimal128`

- `bool`

- `object`

- `array`

If [`encrypt.algorithm`](/docs/manual/core/csfle/reference/encryption-schemas#mongodb-autoencryptkeyword-autoencryptkeyword.encrypt.algorithm) or its inherited value is `AED_AES_256_CBC_HMAC_SHA_512-Random`, `bsonType` is optional and may specify an array of supported bson types. For fields with `bsonType` of `array` or `object`, the client encrypts the *entire* array or object and not their individual elements.

`encrypt.bsonType` does **not** support the following types regardless of [`encrypt.algorithm`](/docs/manual/core/csfle/reference/encryption-schemas#mongodb-autoencryptkeyword-autoencryptkeyword.encrypt.algorithm) or its inherited value:

- `minKey`

- `maxKey`

- `null`

- `undefined`

*String (JSON pointer) | Array of single UUID*

- If you use a UUID, specify *one* UUID inside an array. This is the UUID of the Data Encryption Key to use for encrypting field values. The UUID is a BSON [binary data](http://bsonspec.org/spec.html) element of subtype `4`.

- If you use a string, use a [JSON pointer](/docs/manual/reference/glossary#std-term-JSON-pointer) that references a [key alternate name.](/docs/manual/core/csfle/fundamentals/manage-keys#std-label-key_alt_names)

If omitted, the [Automatic Encryption Shared Library](/docs/manual/core/csfle/reference/install-library#std-label-csfle-reference-shared-library) checks all parent fields for the closest ancestor containing an [`encryptMetadata.keyId`](/docs/manual/core/csfle/reference/encryption-schemas#mongodb-autoencryptkeyword-autoencryptkeyword.encryptMetadata.keyId) key and inherits that value. If no parent [`keyId`](/docs/manual/core/csfle/reference/encryption-schemas#mongodb-autoencryptkeyword-autoencryptkeyword.encryptMetadata.keyId) exists, automatic field level encryption fails and returns an error.

The [`keyId`](/docs/manual/core/csfle/reference/encryption-schemas#mongodb-autoencryptkeyword-autoencryptkeyword.encrypt.keyId) or its inherited value *must* exist in the Key Vault collection specified as  part of the automatic encryption [configuration options](/docs/manual/reference/method/Mongo#std-label-autoEncryptionOpts). If the specified Data Encryption Key does not exist, automatic encryption fails.

Official MongoDB drivers have language-specific requirements for specifying the UUID. Defer to the [driver documentation](/docs/manual/core/csfle/tutorials#std-label-csfle-driver-tutorials) for complete documentation on implementing client-side field level encryption.

*Object*

```json
{
  "bsonType" : "object",
  "encryptMetadata" : {
    "algorithm" : "<string>",
    "keyId" : [ <UUID> ]
  },
  "properties" : {
    "encrypt" : {}
  }
}
```

Defines encryption options which an [`encrypt`](/docs/manual/core/csfle/reference/encryption-schemas#mongodb-autoencryptkeyword-autoencryptkeyword.encrypt) object nested in the sibling `properties` may inherit. If an [`encrypt`](/docs/manual/core/csfle/reference/encryption-schemas#mongodb-autoencryptkeyword-autoencryptkeyword.encrypt) is missing an option required to support encryption, the Automatic Encryption Shared Library searches all parent objects to locate an [`encryptMetadata`](/docs/manual/core/csfle/reference/encryption-schemas#mongodb-autoencryptkeyword-autoencryptkeyword.encryptMetadata) object that specifies the missing option.

`encryptMetadata` must be specified in subschemas with `bsonType:
    "object"`. `encryptMetadata` cannot be specified to any subschema of the `items` or `additionalItems` keywords. Specifically, automatic Client-Side Field Level Encryption does not support encrypting individual elements of an array.

The `encryptMetadata` object can contain *only* the following fields. Including any other field to the `encrypt` object results in errors when issuing automatically encrypted read or write operations:

- [`algorithm`](/docs/manual/core/csfle/reference/encryption-schemas#mongodb-autoencryptkeyword-autoencryptkeyword.encryptMetadata.algorithm)

- [`keyId`](/docs/manual/core/csfle/reference/encryption-schemas#mongodb-autoencryptkeyword-autoencryptkeyword.encryptMetadata.keyId)

*String*

The encryption algorithm to use to encrypt a given field. If an [`encrypt`](/docs/manual/core/csfle/reference/encryption-schemas#mongodb-autoencryptkeyword-autoencryptkeyword.encrypt) object is missing the [`algorithm`](/docs/manual/core/csfle/reference/encryption-schemas#mongodb-autoencryptkeyword-autoencryptkeyword.encrypt.algorithm) field, the Automatic Encryption Shared Library searches all parent objects to locate an [`encryptMetadata`](/docs/manual/core/csfle/reference/encryption-schemas#mongodb-autoencryptkeyword-autoencryptkeyword.encryptMetadata) object that specifies [`encryptMetadata.algorithm`.](/docs/manual/core/csfle/reference/encryption-schemas#mongodb-autoencryptkeyword-autoencryptkeyword.encryptMetadata.algorithm)

Supports the following algorithms *only*:

- `AEAD_AES_256_CBC_HMAC_SHA_512-Random`

- `AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic`

For complete documentation on the encryption algorithms, see [Fields and Encryption Types.](/docs/manual/core/csfle/fundamentals/encryption-algorithms#std-label-field-level-encryption-algorithms)

If specifying `AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic`, any `encrypt` object inheriting that value *must* specify [`encrypt.bsonType`.](/docs/manual/core/csfle/reference/encryption-schemas#mongodb-autoencryptkeyword-autoencryptkeyword.encrypt.bsonType)

*Array of single UUID*

The UUID of a Data Encryption Key. The UUID is a BSON [binary data](http://bsonspec.org/spec.html) element of subtype `4`.

Specify *one* string inside the array.

If an [`encrypt`](/docs/manual/core/csfle/reference/encryption-schemas#mongodb-autoencryptkeyword-autoencryptkeyword.encrypt) object is missing the [`keyId`](/docs/manual/core/csfle/reference/encryption-schemas#mongodb-autoencryptkeyword-autoencryptkeyword.encrypt.keyId) field, the Automatic Encryption Shared Library searches all parent objects to locate an [`encryptMetadata`](/docs/manual/core/csfle/reference/encryption-schemas#mongodb-autoencryptkeyword-autoencryptkeyword.encryptMetadata) object that specifies [`encryptMetadata.keyId`.](/docs/manual/core/csfle/reference/encryption-schemas#mongodb-autoencryptkeyword-autoencryptkeyword.encryptMetadata.keyId)

The Data Encryption Key *must* exist in the Key Vault collection specified as part of the automatic encryption [configuration options](/docs/manual/core/csfle/reference/csfle-options-clients#std-label-csfle-reference-mongo-client). The specified configuration options must *also* include appropriate access to the [Key Management Service (KMS)](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-fundamentals-kms-providers) and Customer Master Key (CMK) used to create the data key. Automatic encryption fails if the Data Encryption Key does not exist *or* if the client cannot decrypt the key with the specified KMS and CMK.

Official MongoDB drivers have language-specific requirements for specifying the UUID. Defer to the [driver documentation](/docs/manual/core/csfle/tutorials#std-label-csfle-driver-tutorials) for complete documentation on implementing client-side field level encryption.

## Examples

### Encryption Schema -  Multiple Fields

Consider a collection `MedCo.patients` where each document has the following structure:

```none
{
  "fname" : "<String>",
  "lname" : "<String>",
  "passportId" : "<String>",
  "bloodType" : "<String>",
  "medicalRecords" : [
    {<object>}
  ],
  "insurance" : {
    "policyNumber" : "<string>",
    "provider" : "<string>"
  }
}
```

The following fields contains personally identifiable information (PII) that may be queried:

- `passportId`

- `bloodType`

- `insurance.policyNumber`

- `insurance.provider`

The [deterministic](/docs/manual/core/csfle/fundamentals/encryption-algorithms#std-label-field-level-encryption-deterministic) encryption algorithm guarantees that the encrypted output of a value remains static. This allows queries for a specific value to return meaningful results at the cost of increased susceptibility to frequency analysis recovery. The deterministic encryption algorithm therefore meets both the encryption and queryability requirements of the data.

The following fields contain legally protected personally identifiable information (PII) that may never be queried:

- `medicalRecords`

The [randomized](/docs/manual/core/csfle/fundamentals/encryption-algorithms#std-label-field-level-encryption-random) encryption algorithm guarantees that the encrypted output of a value is always unique. This prevents queries for a specific field value from returning meaningful results while supporting the highest possible protection of the field contents. The randomized encryption algorithm therefore meets both the encryption and queryability requirements of the data.

The following schema specifies automatic encryption rules which meet the above requirements for the `MedCo.patients` collection:

```json
{
  "MedCo.patients" : {
    "bsonType" : "object",
    "properties" : {
      "passportId" : {
        "encrypt" : {
          "keyId" : [UUID("bffb361b-30d3-42c0-b7a4-d24a272b72e3")],
          "algorithm" : "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic",
          "bsonType" : "string"
        }
      },
      "bloodType" : {
        "encrypt" : {
          "keyId" : [UUID("bffb361b-30d3-42c0-b7a4-d24a272b72e3")],
          "algorithm" : "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic",
          "bsonType" : "string"
        }
      },
      "medicalRecords" : {
        "encrypt" : {
          "keyId" : [UUID("f3821212-e697-4d65-b740-4a6791697c6d")],
          "algorithm" : "AEAD_AES_256_CBC_HMAC_SHA_512-Random",
          "bsonType" : "array"
        }
      },
      "insurance" : {
        "bsonType" : "object",
        "properties" : {
          "policyNumber" : {
            "encrypt" : {
              "keyId" : [UUID("bffb361b-30d3-42c0-b7a4-d24a272b72e3")],
              "algorithm" : "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic",
              "bsonType" : "string"
            }
          },
          "provider" : {
            "encrypt" : {
              "keyId" : [UUID("bffb361b-30d3-42c0-b7a4-d24a272b72e3")],
              "algorithm" : "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic",
              "bsonType" : "string"
            }
          }
        }
      }
    }
  }
}
```

The above automatic encryption rules mark the `passportId`, `bloodType`, `insurance.policyNumber`, `insurance.provider`, and `medicalRecords` fields for encryption.

- The `passportId`, `bloodType`, `insurance.policyNumber`, and `provider` fields require deterministic encryption using the specified key.

- The `medicalRecords` field requires randomized encryption using the specified key.

While Queryable Encryption does not support encrypting individual array elements, randomized encryption supports encrypting the *entire* array field rather than individual elements in the field. The example automatic encryption rules specify randomized encryption for the `medicalRecords` field to encrypt the entire array. If the automatic encryption rules specified [`encrypt`](/docs/manual/core/csfle/reference/encryption-schemas#mongodb-autoencryptkeyword-autoencryptkeyword.encrypt) or [`encryptMetadata`](/docs/manual/core/csfle/reference/encryption-schemas#mongodb-autoencryptkeyword-autoencryptkeyword.encryptMetadata) within `medicalRecords.items` or `medicalRecords.additionalItems`, automatic field level encryption fails and returns an errors.

The official MongoDB drivers, [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh), and the legacy `mongo` shell require specifying the automatic encryption rules as part of creating the database connection object:

- For `mongosh`, use the [`Mongo()`](/docs/manual/reference/method/Mongo#mongodb-method-Mongo) constructor to create a database connection. Specify the automatic encryption rules to the `schemaMap` key of the [`AutoEncryptionOpts`](/docs/manual/reference/method/Mongo#std-label-autoEncryptionOpts) parameter. See [Connect to a Cluster with Automatic Client-Side Encryption Enabled](/docs/manual/reference/method/Mongo#std-label-mongo-connection-automatic-client-side-encryption-enabled) for a complete example.

- For the official MongoDB drivers, use the driver-specific database connection constructor (`MongoClient`) to create the database connection with the automatic encryption rules included as part of the Queryable Encryption configuration object. Defer to the [driver API reference](/docs/manual/core/csfle/tutorials#std-label-csfle-driver-tutorials) for more complete documentation and tutorials.

For all clients, the `keyVault` and `kmsProviders` specified to the Queryable Encryption parameter *must* grant access to both the Data Encryption Keys specified in the automatic encryption rules *and* the Customer Master Key used to encrypt the Data Encryption Keys.

### Encryption Schema -  Multiple Fields With Inheritance

Consider a collection `MedCo.patients` where each document has the following structure:

```none
{
  "fname" : "<String>",
  "lname" : "<String>",
  "passportId" : "<String>",
  "bloodType" : "<String>",
  "medicalRecords" : [
    {<object>}
  ],
  "insurance" : {
    "policyNumber" : "<string>",
    "provider" : "<string>"
  }
}
```

The following fields contain private data that may be queried:

- `passportId`

- `bloodType`

- `insurance.policyNumber`

- `insurance.provider`

The [deterministic](/docs/manual/core/csfle/fundamentals/encryption-algorithms#std-label-field-level-encryption-deterministic) encryption algorithm guarantees that the encrypted output of a value remains static. This allows queries for a specific value to return meaningful results at the cost of increased susceptibility to frequency analysis recovery. The deterministic encryption algorithm therefore meets both the encryption and queryability requirements of the data.

The following fields contain private data that may never be queried:

- `medicalRecords`

The [randomized](/docs/manual/core/csfle/fundamentals/encryption-algorithms#std-label-field-level-encryption-random) encryption algorithm guarantees that the encrypted output of a value is always unique. This prevents queries for a specific field value from returning meaningful results while supporting the highest possible protection of the field contents. The randomized encryption algorithm therefore meets both the encryption and queryability requirements of the data.

The following schema specifies automatic encryption rules which meet the encryption requirements for the `MedCo.patients` collection:

```json
{
  "MedCo.patients" : {
    "bsonType" : "object",
    "encryptMetadata" : {
      "keyId" : [UUID("6c512f5e-09bc-434f-b6db-c42eee30c6b1")],
      "algorithm" : "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic"
    },
    "properties" : {
      "passportId" : {
        "encrypt" : {
          "bsonType" : "string"
        }
      },
      "bloodType" : {
        "encrypt" : {
          "bsonType" : "string"
        }
      },
      "medicalRecords" : {
        "encrypt" : {
          "keyId" : [UUID("6c512f5e-09bc-434f-b6db-c42eee30c6b1")],
          "algorithm" : "AEAD_AES_256_CBC_HMAC_SHA_512-Random",
          "bsonType" : "array"
        }
      },
      "insurance" : {
        "bsonType" : "object",
        "properties" : {
          "policyNumber" : {
            "encrypt" : {
              "bsonType" : "string"
            }
          },
          "provider" : {
            "encrypt" : {
              "bsonType" : "string"
            }
          }
        }
      }
    }
  }
}
```

The above automatic encryption rules mark the `passportId`, `bloodType`, `insurance.policyNumber`, `insurance.provider`, and `medicalRecords` fields for encryption.

- The `passportId`, `bloodType`, `insurance.policyNumber`, and `provider` fields inherit their encryption settings from the parent `encryptMetadata` field. Specifically, these fields inherit the [`algorithm`](/docs/manual/core/csfle/reference/encryption-schemas#mongodb-autoencryptkeyword-autoencryptkeyword.encryptMetadata.algorithm) and [`keyId`](/docs/manual/core/csfle/reference/encryption-schemas#mongodb-autoencryptkeyword-autoencryptkeyword.encryptMetadata.keyId) values specifying deterministic encryption with the specified Data Encryption Key.

- The `medicalRecords` field requires randomized encryption using the specified key. The `encrypt` options override those specified in the parent `encryptMetadata` field.

While Queryable Encryption does not support encrypting individual array elements, randomized encryption supports encrypting the *entire* array field rather than individual elements in the field. The example automatic encryption rules specify randomized encryption for the `medicalRecords` field to encrypt the entire array. If the automatic encryption rules specified [`encrypt`](/docs/manual/core/csfle/reference/encryption-schemas#mongodb-autoencryptkeyword-autoencryptkeyword.encrypt) or [`encryptMetadata`](/docs/manual/core/csfle/reference/encryption-schemas#mongodb-autoencryptkeyword-autoencryptkeyword.encryptMetadata) within `medicalRecords.items` or `medicalRecords.additionalItems`, automatic field level encryption fails and returns an errors.

The official MongoDB drivers, [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh), and the legacy `mongo` shell require specifying the automatic encryption rules as part of creating the database connection object:

- For `mongosh`, use the [`Mongo()`](/docs/manual/reference/method/Mongo#mongodb-method-Mongo) constructor to create a database connection. Specify the automatic encryption rules to the `schemaMap` key of the [`AutoEncryptionOpts`](/docs/manual/reference/method/Mongo#std-label-autoEncryptionOpts) parameter. See [Connect to a Cluster with Automatic Client-Side Encryption Enabled](/docs/manual/reference/method/Mongo#std-label-mongo-connection-automatic-client-side-encryption-enabled) for a complete example.

- For the official MongoDB drivers, use the driver-specific database connection constructor (`MongoClient`) to create the database connection with the automatic encryption rules included as part of the Queryable Encryption configuration object. Defer to the [driver API reference](/docs/manual/core/csfle/tutorials#std-label-csfle-driver-tutorials) for more complete documentation and tutorials.

For all clients, the `keyVault` and `kmsProviders` specified to the Queryable Encryption parameter *must* grant access to both the Data Encryption Keys specified in the automatic encryption rules *and* the Customer Master Key used to encrypt the Data Encryption Keys.

To learn more about your CMK and Key Vault collection, see the [key vaults](/docs/manual/core/queryable-encryption/fundamentals/keys-key-vaults#std-label-qe-reference-keys-key-vaults) page.

To learn more about encryption algorithms, see the [Encryption algorithms](/docs/manual/core/csfle/fundamentals/encryption-algorithms#std-label-csfle-reference-encryption-algorithms) page.

To learn more about CSFLE-specific `MongoClient` options, see the [mongo client](/docs/manual/core/csfle/reference/csfle-options-clients#std-label-csfle-reference-mongo-client) page.

### Encryption Schema -  Encrypt with Pattern Properties

You can use the `patternProperties` keyword in your encryption schema to define encryption rules for all fields with names that match a regular expression.

Consider a collection `MedCo.patients` where each document has the following structure:

```none
{
  "fname" : "<string>",
  "lname" : "<string>",
  "passportId_PIIString" : "<string>",
  "bloodType_PIIString" : "<string>",
  "medicalRecords_PIIArray" : [
    {<object>}
  ],
  "insurance" : {
    "policyNumber_PIINumber" : "<number>",
    "provider_PIIString" : "<string>"
  }
}
```

The fields that contain private data are identified by a "\_PII\<type>" tag appended the end of the field name.

- `passportId_PIIString`

- `bloodType_PIIString`

- `medicalRecords_PIIArray`

- `insurance.policyNumber_PIINumber`

- `insurance.provider_PIIString`

You can use the `patternProperties` keyword to configure these fields for encryption, without identifying each field individually, and without using the full field name. Do this by using regular expressions that match all fields that end with the "\_PII\<type>" tag.

The following JSON schema uses `patternProperties` and regular expressions to specify which fields to encrypt.

```json
{
  "MedCo.patients": {
  "bsonType": "object",
  "patternProperties": {
    "_PIIString$": {
      "encrypt": {
        "keyId": [UUID("6c512f5e-09bc-434f-b6db-c42eee30c6b1")],
        "bsonType": "string",
        "algorithm": "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic",
      },
    },
    "_PIIArray$": {
      "encrypt": {
        "keyId": [UUID("6c512f5e-09bc-434f-b6db-c42eee30c6b1")],
        "bsonType": "array",
        "algorithm": "AEAD_AES_256_CBC_HMAC_SHA_512-Random",
      },
    },
    "insurance": {
      "bsonType": "object",
      "patternProperties": {
        "_PIINumber$": {
          "encrypt": {
            "keyId": [UUID("6c512f5e-09bc-434f-b6db-c42eee30c6b1")],
            "bsonType": "int",
            "algorithm": "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic",
          },
        },
        "_PIIString$": {
          "encrypt": {
            "keyId": [UUID("6c512f5e-09bc-434f-b6db-c42eee30c6b1")],
            "bsonType": "string",
            "algorithm": "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic",
          },
        },
      },
    },
  },
  },
}
```

The above automatic encryption rules mark the `passportId_PIIString`, `bloodType_PIIString`, `medicalRecords_PIIArray`, `insurance.policyNumber_PIINumber`, `insurance.provider_PIIString` fields for encryption.

To Learn more about the `patternProperties` keyword, see [patternProperties Keyword.](/docs/manual/core/csfle/fundamentals/create-schema#std-label-csfle-fundamentals-pattern-properties)
