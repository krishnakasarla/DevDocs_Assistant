> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# In-Use Encryption

MongoDB provides two approaches to [In-Use Encryption:](/docs/manual/reference/glossary#std-term-In-Use-Encryption)

- [Queryable Encryption](/docs/manual/core/queryable-encryption#std-label-qe-manual-feature-qe)

- [Client-Side Field Level Encryption.](/docs/manual/core/csfle#std-label-manual-csfle-feature)

## Choosing an In-Use Encryption Approach

You can use both Queryable Encryption and Client-Side Field Level Encryption in the same deployment, but they are incompatible with each other in the same collection. For a comparison of the two, including compatibility with MongoDB versions and points to consider when choosing one or the other, see [Choosing an In-Use Encryption Approach.](/docs/manual/core/queryable-encryption/about-qe-csfle#std-label-about-qe-csfle)

## Encryption Keys and Key Vaults

Both Queryable Encryption and Client-Side Field Level Encryption use an [envelope encryption](/docs/manual/reference/glossary#std-term-envelope-encryption) approach to encrypt data, where an encrypted field in a document uses a unique [Data Encryption Key](/docs/manual/reference/glossary#std-term-Data-Encryption-Key), and those keys are encrypted using a [Customer Master Key.](/docs/manual/reference/glossary#std-term-Customer-Master-Key)

For details, see [Encryption Keys and Key Vaults.](/docs/manual/core/queryable-encryption/fundamentals/keys-key-vaults#std-label-qe-reference-keys-key-vaults)

## Queryable Encryption

To learn how Queryable Encryption and its components work and how to implement it in your application, see [Queryable Encryption.](/docs/manual/core/queryable-encryption#std-label-qe-manual-feature-qe)

## Client-Side Field Level Encryption

To learn how Client-Side Field Level Encryption and its components work and how to implement it in your application, see [Client-Side Field Level Encryption.](/docs/manual/core/csfle#std-label-manual-csfle-feature)
