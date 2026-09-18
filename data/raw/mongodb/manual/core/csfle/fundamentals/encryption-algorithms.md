> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Fields and Encryption Types

This page describes the types of encryption used by MongoDB to perform Client-Side Field Level Encryption (CSFLE). To perform CSFLE, MongoDB uses the following types of encryption algorithms:

- [Deterministic Encryption](/docs/manual/core/csfle/fundamentals/encryption-algorithms#std-label-csfle-deterministic-encryption)

- [Randomized Encryption](/docs/manual/core/csfle/fundamentals/encryption-algorithms#std-label-csfle-random-encryption)

## Deterministic Encryption

The deterministic encryption algorithm ensures that a given input value always encrypts to the *same* output value each time the algorithm is executed. While deterministic encryption provides greater support for read operations, encrypted data with low cardinality is susceptible to frequency analysis recovery.

For sensitive fields that are *not* used in read operations, applications may use [randomized encryption](/docs/manual/core/csfle/fundamentals/encryption-algorithms#std-label-csfle-random-encryption) for improved protection from frequency analysis recovery.

**Important: Deterministically Encrypting Objects and Arrays not Supported**

Encrypting entire objects and arrays is not supported with deterministic encryption. To learn more and see an example, see [Support for Encrypting Objects and Arrays.](/docs/manual/core/csfle/fundamentals/encryption-algorithms#std-label-csfle-encrypting-objects-support)

### Query for Documents on a Deterministically Encrypted Field

You can query deterministically encrypted fields using standard MongoDB driver and [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) methods.

To view the complete list of all supported query operators on deterministically encrypted fields, see [Supported Operations for Automatic Encryption.](/docs/manual/core/csfle/reference/supported-operations#std-label-csfle-reference-automatic-encryption-supported-operations)

To learn more about reads on encrypted data, see [Encrypted Reads.](/docs/manual/core/csfle/fundamentals/automatic-encryption#std-label-encrypted-reads-diagram)

**Note: Querying from Clients without CSFLE Configured**

When you query on an encrypted field using a client that is not configured to use Client-Side Field Level Encryption (CSFLE), the query returns a null value. A client without CSFLE configured cannot query on an encrypted field.

## Randomized Encryption

The randomized encryption algorithm ensures that a given input value always encrypts to a *different* output value each time the algorithm is executed. While randomized encryption provides the strongest guarantees of data confidentiality, it also prevents support for any read operations which must operate on the encrypted field to evaluate the query.

For sensitive fields that *are* used in read operations, applications must use [deterministic encryption](/docs/manual/core/csfle/fundamentals/encryption-algorithms#std-label-csfle-deterministic-encryption) for improved read support on encrypted fields.

### Support for Encrypting Objects and Arrays

Encrypting entire objects or arrays is only supported with [randomized encryption.](/docs/manual/core/csfle/fundamentals/encryption-algorithms#std-label-csfle-random-encryption)

For example, consider the following document:

```json
{
   "personal_information" : {
      "ssn" : "123-45-6789",
      "credit_score" : 750,
      "credit_cards" : [ "1234-5678-9012-3456", "9876-5432-1098-7654"]
   },
   "phone_numbers" : [ "(212) 555-0153" ]
}
```

Encrypting the `personal_information` and `phone_numbers` fields using the randomized encryption algorithm encrypts the *entire* object. While this protects all fields nested under those fields, it also prevents querying against those nested fields.

To learn more about supported operations for encryption, see [Supported Operations for Automatic Encryption.](/docs/manual/core/csfle/reference/supported-operations#std-label-csfle-reference-automatic-encryption-supported-operations)

### Query for Documents on a Randomly Encrypted Field

You cannot directly query for documents on a randomly encrypted field. However, you can use another field to find the document that contains an approximation of the randomly encrypted field data.

For example, consider the following document where the `ssn` field is randomly encrypted:

```json
{
   "_id": "5d6ecdce70401f03b27448fc",
   "name": "Jon Doe",
   "ssn": 241014209,
   "bloodType": "AB+",
   "medicalRecords": [
       {
           "weight": 180,
           "bloodPressure": "120/80"
       }
   ],
   "insurance": {
       "provider": "MaestCare",
       "policyNumber": 123142
   }
}
```

Instead of querying the `ssn` field, you can add another plain-text field called `last4ssn` that contains the last 4 digits of the `ssn` field. You can then query on the `last4ssn` field as a proxy for `ssn`:

```json
{
   "_id": "5d6ecdce70401f03b27448fc",
   "name": "Jon Doe",
   "ssn": 241014209,
   "last4ssn": 4209,
   "bloodType": "AB+",
   "medicalRecords": [
      {
            "weight": 180,
            "bloodPressure": "120/80"
      }
   ],
   "insurance": {
      "provider": "MaestCare",
      "policyNumber": 123142
   }
}
```
