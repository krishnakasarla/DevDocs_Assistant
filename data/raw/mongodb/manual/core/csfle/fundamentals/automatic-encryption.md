> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Automatic Encryption

MongoDB supports automatically encrypting fields in read and write operations when using Client-Side Field Level Encryption. You can perform automatic encryption using [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) and official MongoDB drivers. For a complete list of official compatible drivers with support for CSFLE, see Driver Compatibility [Compatibility.](/docs/manual/core/queryable-encryption/reference/compatibility#std-label-csfle-driver-compatibility)

## How Encrypted Writes and Reads Work

The following diagrams show how the client application and driver write and read field-level encrypted data.

### Encrypted Writes

For write operations, the driver encrypts field values *prior* to writing to the MongoDB database.

The following diagram shows the steps taken by the client application and driver to perform a write of field-level encrypted data:

![Diagram that shows the data flow for a write of field-level encrypted data](/images/CSFLE_Write_Encrypted_Data.png)

### Encrypted Reads

For read operations, the driver encrypts field values in the query *prior* to issuing the read operation.

For read operations that return encrypted fields, the driver automatically decrypts the encrypted values *only if* the driver was configured with access to the Customer Master Key (CMK) and Data Encryption Keys (DEK) used to encrypt those values.

The following diagram shows the steps taken by the client application and driver to query and decrypt field-level encrypted data:

![Diagram that shows the data flow for querying and reading field-level encrypted data](/images/CSFLE_Read_Encrypted_Data.png)

## Enabling Automatic Client-Side Field Level Encryption

To enable automatic encryption, specify automatic encryption settings in your client's `MongoClient` instance.

The following code snippets show how to create a client with automatic encryption enabled in `mongosh` and MongoDB drivers:

```java
MongoClientSettings clientSettings = MongoClientSettings.builder()
    .applyConnectionString(new ConnectionString("mongodb://localhost:27017"))
    .autoEncryptionSettings(AutoEncryptionSettings.builder()
        .keyVaultNamespace(keyVaultNamespace)
        .kmsProviders(kmsProviders)
        .schemaMap(schemaMap)
        .extraOptions(extraOptions)
        .build())
    .build();

MongoClient mongoClient = MongoClients.create(clientSettings);

```

```javascript
const secureClient = new MongoClient(connectionString, {
  monitorCommands: true,
  autoEncryption: {
    keyVaultNamespace,
    kmsProviders,
    schemaMap: patientSchema,
    extraOptions: extraOptions,
  },
});

```

```python
fle_opts = AutoEncryptionOpts(
  kms_providers,
  key_vault_namespace,
  schema_map=patient_schema,
  **extra_options
)
client = MongoClient(connection_string, auto_encryption_opts=fle_opts)

```

```csharp
var clientSettings = MongoClientSettings.FromConnectionString(_connectionString);
var autoEncryptionOptions = new AutoEncryptionOptions(
    keyVaultNamespace: keyVaultNamespace,
    kmsProviders: kmsProviders,
    schemaMap: schemaMap,
    extraOptions: extraOptions);
clientSettings.AutoEncryptionOptions = autoEncryptionOptions;
var client = new MongoClient(clientSettings);

```

```go
autoEncryptionOpts := options.AutoEncryption().
	SetKmsProviders(provider.Credentials()).
	SetKeyVaultNamespace(keyVaultNamespace).
	SetSchemaMap(schemaMap).
	SetExtraOptions(extraOptions)
client, err := mongo.Connect(context.TODO(), options.Client().ApplyURI(uri).SetAutoEncryptionOptions(autoEncryptionOpts))


```

```javascript
var autoEncryptionOpts =
{
   "keyVaultNamespace" : "<database>.<collection>",
   "kmsProviders" : { ... },
   "schemaMap" : { ... }
}

cluster = Mongo(
  "<Your Connection String>",
  autoEncryptionOpts
);

```

**Tip: Environment Variables**

If possible, consider defining the credentials provided in `kmsProviders` as environment variables, and then passing them to [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) using the [`--eval`](https://www.mongodb.com/docs/mongodb-shell/reference/options/#std-option-mongosh.--eval) option. This minimizes the chances of credentials leaking into logs.

For more information on CSFLE-specific `MongoClient` settings, see [MongoClient Options for CSFLE.](/docs/manual/core/csfle/reference/csfle-options-clients#std-label-csfle-reference-mongo-client)

## Server-Side Field Level Encryption Enforcement

MongoDB supports using [schema validation](/docs/manual/core/schema-validation#std-label-schema-validation-overview) to enforce encryption of specific fields in a collection. Clients performing automatic Client-Side Field Level Encryption have specific behavior depending on the database connection configuration:

- If the connection [autoEncryptionOpts](/docs/manual/core/csfle/reference/csfle-options-clients#std-label-csfle-enc-options-example) `schemaMap` object contains a key for the specified collection, the client uses that object to perform automatic field level encryption and ignores the remote schema. At minimum, the local rules **must** encrypt those fields that the remote schema marks as requiring encryption.

- If the connection [autoEncryptionOpts](/docs/manual/core/csfle/reference/csfle-options-clients#std-label-csfle-enc-options-example) `schemaMap` object does *not* contain a key for the specified collection, the client downloads the server-side remote schema for the collection and uses it to perform automatic field level encryption.

  **Important: Behavior Considerations**

  MongoDB uses [schema validation](/docs/manual/core/schema-validation#std-label-schema-validation-overview) to enforce encryption of specific fields in a collection. Without a client-side schema, the client downloads the server-side schema for the collection to determine which fields to encrypt. To avoid this issue, use client-side schema validation.

  Because CSFLE and Queryable Encryption do not provide a mechanism to verify the integrity of a schema, relying on a server-side schema means trusting that the server's schema has not been tampered with. If an adversary compromises the server, they can modify the schema so that a previously encrypted field is no longer labeled for encryption. This causes the client to send plaintext values for that field.

To learn how to set up server-side CSFLE enforcement, see [CSFLE Server-Side Schema Enforcement.](/docs/manual/core/csfle/reference/server-side-schema#std-label-csfle-reference-server-side-schema)
