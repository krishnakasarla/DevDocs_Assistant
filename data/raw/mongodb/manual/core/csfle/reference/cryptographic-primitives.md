> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Cryptographic Primitives

MongoDB encrypts all fields in Queryable Encryption and CSFLE with the [AEAD](https://en.wikipedia.org/wiki/Authenticated_encryption#Authenticated_encryption_with_associated_data) AES-256-CBC encryption algorithm.

- With Queryable Encryption, ciphertext is always non-deterministic.

- With CSFLE, if you specify deterministic encryption for a field, your application passes a deterministic initialization vector to AEAD.

- With CSFLE, if you specify random encryption for a field, your application passes a random initialization vector to AEAD.

**Note: Authenticated Encryption**

MongoDB uses the  [encrypt-then-MAC](https://en.wikipedia.org/wiki/Authenticated_encryption#Encrypt-then-MAC_\(EtM\)) approach to perform authenticated encryption. Both Queryable Encryption and CSFLE use the HMAC-SHA-256 algorithm to generate your MAC.
