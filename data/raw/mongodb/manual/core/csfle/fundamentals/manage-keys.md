> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Encryption Key Management

In this guide, you can learn how to manage your encryption keys with a Key Management System (KMS (Key Management System)) in your Client-Side Field Level Encryption (CSFLE)-enabled application.

## Encryption Components

MongoDB uses the following components to perform Client-Side Field Level Encryption:

- Data Encryption Keys (DEK (Data Encryption Key))s

- Customer Master Keys (CMK (Customer Master Key))s

- Key Vault collections

- Key Management System (KMS (Key Management System))

To learn more about keys and key vaults, see [Encryption Keys and Key Vaults.](/docs/manual/core/queryable-encryption/fundamentals/keys-key-vaults#std-label-qe-reference-keys-key-vaults)

## Supported Key Management Services

Client-Side Field Level Encryption supports the following Key Management System providers:

- Amazon Web Services KMS

- Azure Key Vault

- Google Cloud KMS

- Any KMIP Compliant Key Management System

- Local Key Provider

The default KMIP protocol version is 1.2. You can configure MongoDB to use KMIP version 1.0 or 1.1 in the MongoDB server [configuration file.](/docs/manual/reference/configuration-options#std-label-configuration-options)

To learn more about these providers, including diagrams that show how your application uses them to perform Client-Side Field Level Encryption, see [KMS Providers.](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-fundamentals-kms-providers)

## Manage a Data Encryption Key's Alternate Name

You can assign a Data Encryption Key alternate names to make the key easier to reference. Assigning alternate names allows you to perform the following actions:

- Reference a DEK (Data Encryption Key) by different means than the `_id` field.

- Dynamically assign DEKs at runtime.

### Create a Data Encryption Key with an Alternate Name

**Important: Prerequisite**

Prior to adding a new key alternate name, you must create a partial unique index on the `keyAltNames` field. This index should have a `partialFilterExpression` for documents where `keyAltNames` exists.

Client-Side Field Level Encryption depends on server-enforced uniqueness of key alternate names.

To learn how to create a partial index, refer to [Partial Indexes.](/docs/manual/core/index-partial#std-label-index-type-partial)

The following example creates a Data Encryption Key with an alternate name. Select the tab that corresponds to your driver language:

```python
client = MongoClient(connection_string)
client_encryption = ClientEncryption(
    kms_providers,
    key_vault_namespace,
    client,
    CodecOptions(uuid_representation=STANDARD),
)
master_key={ "<Your dataKeyOpts Key>" : "<Your dataKeyOpts Value>"}
data_key_id = client_encryption.create_data_key(provider, master_key, key_alt_names=["<Your Key Alt Name>"])

```

```java
ClientEncryptionSettings clientEncryptionSettings = ClientEncryptionSettings.builder()
.keyVaultMongoClientSettings(MongoClientSettings.builder()
    .applyConnectionString(new ConnectionString(connectionString))
    .build())
.keyVaultNamespace(keyVaultNamespace)
.kmsProviders(kmsProviders)
.build();
ClientEncryption clientEncryption = ClientEncryptions.create(clientEncryptionSettings);

BsonDocument masterKeyProperties = new BsonDocument();
masterKeyProperties.put("provider", new BsonString("<Your KMS Provider>"));
masterKeyProperties.put("<Your dataKeyOpts Key>", new BsonString("<Your dataKeyOpts Value>"));
List keyAltNames = new ArrayList<String>();
keyAltNames.add("<Your Key Alt Name>");

BsonBinary dataKeyId = clientEncryption.createDataKey(kmsProvider, new DataKeyOptions().masterKey(masterKeyProperties).keyAltNames(keyAltNames));

```

```javascript
const encryption = new ClientEncryption(client, {
  keyVaultNamespace,
  kmsProviders,
});
const masterKey = {
  "<Your dataKeyOpts Key>": "<Your dataKeyOpts Value>",
};
const key = await encryption.createDataKey(provider, {
  masterKey: masterKey,
  keyAltNames: ["<Your Key Alt Name>"],
});

```

```csharp
var keyVaultClient = new MongoClient(connectionString);
var clientEncryptionOptions = new ClientEncryptionOptions(
    keyVaultClient: keyVaultClient,
    keyVaultNamespace: keyVaultNamespace,
    kmsProviders: kmsProviders);
var clientEncryption = new ClientEncryption(clientEncryptionOptions);

var dataKeyOptions = new DataKeyOptions(
    alternateKeyNames: new[] { "<Your Key Alt Name>" },
    masterKey: new BsonDocument
    {
        { "<Your dataKeyOpts Keys>", "<Your dataKeyOpts Values>" },
    });

var dataKeyId = clientEncryption.CreateDataKey("<Your KMS Provider>", dataKeyOptions, CancellationToken.None);

```

```go
clientEncryptionOpts := options.ClientEncryption().SetKeyVaultNamespace(KeyVaultNamespace).SetKmsProviders(kmsProviders)
keyVaultClient, err := mongo.Connect(context.TODO(), options.Client().ApplyURI(URI))
if err != nil {
	return fmt.Errorf("Client connect error %v", err)
}
clientEnc, err := mongo.NewClientEncryption(keyVaultClient, clientEncryptionOpts)
if err != nil {
	return fmt.Errorf("NewClientEncryption error %v", err)
}
defer func() {
	_ = clientEnc.Close(context.TODO())
}()
masterKey := map[string]interface{}{
	"<Your dataKeyOpts Key>": "<Your dataKeyOpts Value>",
}
dataKeyOpts := options.DataKey().
	SetMasterKey(masterKey).
	SetKeyAltNames([]string{"<Your Key Alt Name>"})
dataKeyID, err := clientEnc.CreateDataKey(context.TODO(), provider, dataKeyOpts)
if err != nil {
	return fmt.Errorf("create data key error %v", err)
}

```

```javascript
var autoEncryptionOpts = {
  keyVaultNamespace: keyVaultNamespace,
  kmsProviders: kmsProviders,
};
var encryptedClient = Mongo(
  connectionString,
  autoEncryptionOpts
);
var clientEncryption = encryptedClient.getClientEncryption();
var masterKey = {
  "<Your dataKeyOpts Key>": "<Your dataKeyOpts Value>",
};
var keyVault = encryptedClient.getKeyVault();
var keyId = keyVault.createKey("aws", masterKey, ["<Your Key Alt Name>"]);

```

To learn more about `dataKeyOpts` and `kmsProviders` objects, see [KMS Providers.](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-fundamentals-kms-providers)

### Use Key Alternate Names in an Automatic Encryption Schema

Encryption schemas contain user-specified rules that identify which fields must be encrypted and how to encrypt those fields. In your encryption rules, you can specify alternate key names name for the Data Encryption Key which encrypts your field.

You must refer to a key alternate name with a [JSON pointer](/docs/manual/reference/glossary#std-term-JSON-pointer). Use JSON pointers to reference a field in your query or update document which contains the value of your key alternate name.

**Important: Cannot Use Alternate Name for Deterministically Encrypted Field**

You cannot reference a DEK (Data Encryption Key) by it's alternate name when encrypting a field with the [deterministic encryption algorithm](/docs/manual/core/csfle/fundamentals/encryption-algorithms#std-label-csfle-deterministic-encryption). To encrypt your field deterministically, you must specify the `_id` of the key you would like to use to encrypt your field.

#### Reference Key Alternate Name in an Encryption Schema

Consider the following encryption schema which encrypts the `salary` field:

```json
{
  "<database>.<collection>": {
    "bsonType": "object",
    "properties": {
      "salary": {
        "encrypt": {
          "bsonType": "int",
          "keyId": "/fieldWithAltName",
          "algorithm": "AEAD_AES_256_CBC_HMAC_SHA_512-Random"
        }
      }
    }
  }
}
```

The schema's `keyId` field contains a JSON pointer to reference the `fieldWithAltName` field within the documents being encrypted.

The following document's `fieldWithAltName` value is `my-alt-name`:

```json
{
  "name": "Jon Doe",
  "salary": 45000,
  "fieldWithAltName": "my-alt-name"
}
```

The `salary` field is encrypted by the DEK (Data Encryption Key) that has the alternate name `my-alt-name`.

#### Dynamically Assign Keys at Runtime

You can use alternate key names to dynamically set the Data Encryption Key for a field at runtime. Use this functionality to encrypt individual documents with different DEKs using the same encryption schema.

For example, consider the following documents:

```json
{
    "name": "Jon Doe",
    "salary": 45000,
    "fieldWithAltName": "my-alt-name"
},
{
    "name": "Jane Smith",
    "salary": 70000,
    "fieldWithAltName": "my-other-alt-name"
}
```

You insert the preceding documents using a CSFLE-enabled client configured with the encryption schema from the [previous example.](/docs/manual/core/csfle/fundamentals/manage-keys#std-label-csfle-reference-key-alt-name-in-schema)

In the encryption schema, the `salary.encrypt.keyId` field contains a JSON pointer to the `fieldWithAltName` field of the inserted document. As a result, the `salary` fields in the two example documents are each encrypted using a DEK (Data Encryption Key) specific to the individual document. The keys are assigned dynamically at runtime.

## Procedure: Rotate Encryption Keys Using Mongo Shell

With version 1.5 and later of the Mongo Shell, you can rotate encryption keys using the `rewrapManyDataKey` method. The `rewrapManyDataKey` method automatically decrypts multiple data keys and re-encrypts them using a specified Customer Master Key. It then updates the rotated keys in the key vault collection. This method allows you to rotate encryption keys based on two optional arguments:

- A filter used to specify which keys to rotate. If no data key matches the given filter, no keys are rotated. Omit the filter to rotate all keys in your key vault collection.

- An object that represents a new CMK (Customer Master Key). Omit this object to rotate the data keys using their current CMKs.

The `rewrapManyDataKey` uses the following syntax:

```json
keyVault = db.getKeyVault()

keyVault.rewrapManyDataKey(
   {
      "<Your custom filter>"
   },
   {
      provider: "<KMS provider>",
      masterKey: {
         "<dataKeyOpts Key>" : "<dataKeyOpts Value>"
      }
   }
)
```

To learn more about the `dataKeyOpts` object for your KMS provider, see [Supported Key Management Services.](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-fundamentals-kms-providers-supported-kms)

## Delete a Data Encryption Key

You can delete a Data Encryption Key from your Key Vault collection using standard CRUD [delete operations](/docs/manual/tutorial/remove-documents#std-label-write-op-delete). If you delete a DEK (Data Encryption Key), all fields encrypted with that DEK (Data Encryption Key) become permanently unreadable.

**Tip: MongoDB Shell Specific Feature**

The MongoDB shell allows you to delete a DEK (Data Encryption Key) by `UUID` using the `keyVault.deleteKey()` method as follows:

```none
keyVault = db.getKeyVault()
keyVault.deleteKey(UUID("<UUID String>"))
```

To learn more about Key Vault collections see [Encryption Keys and Key Vaults.](/docs/manual/core/queryable-encryption/fundamentals/keys-key-vaults#std-label-qe-reference-keys-key-vaults)

## Learn More

For tutorials detailing how to set up a CSFLE-enabled application with each of the supported KMS (Key Management System) providers, see the following pages:

- [Use Automatic Client-Side Field Level Encryption with AWS](/docs/manual/core/csfle/tutorials/aws/aws-automatic#std-label-csfle-tutorial-automatic-aws)

- [Use Automatic Client-Side Field Level Encryption with Azure](/docs/manual/core/csfle/tutorials/azure/azure-automatic#std-label-csfle-tutorial-automatic-azure)

- [Use Automatic Client-Side Field Level Encryption with GCP](/docs/manual/core/csfle/tutorials/gcp/gcp-automatic#std-label-csfle-tutorial-automatic-gcp)

- [Use Automatic Client-Side Field Level Encryption with KMIP](/docs/manual/core/csfle/tutorials/kmip/kmip-automatic#std-label-csfle-tutorial-automatic-kmip)

To view additional examples of encryption schemas, see [CSFLE Encryption Schemas.](/docs/manual/core/csfle/reference/encryption-schemas#std-label-csfle-reference-encryption-schemas)
