> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

<!--
Tab options on this page. Append to the .md URL to filter:
  ?tabs=<id,...>   select specific tabs (e.g. ?tabs=nodejs,shell)
  ?allTabs=true    include every tab
  (no param)       default: one tab per tabset

Available tabs:
  other tabs: single-key, multiple-key-sequence
-->

# Self-Managed Internal/Membership Authentication

You can require that members of [replica sets](/docs/manual/reference/glossary#std-term-replica-set) and [sharded clusters](/docs/manual/reference/glossary#std-term-sharded-cluster) authenticate to each other. For the internal authentication of the members, MongoDB can use either [keyfiles](/docs/manual/core/security-internal-authentication#std-label-internal-auth-keyfile) or [X.509](/docs/manual/core/security-internal-authentication#std-label-internal-auth-x509) certificates.

The selected method is used for all internal communication. For example, when a client authenticates to a [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) using one of the supported [authentication mechanisms](/docs/manual/core/authentication#std-label-security-authentication-mechanisms), the `mongos` then uses the configured internal authentication method to connect to the required [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) processes.

**Note:**

Enabling internal authentication also enables [client authorization.](/docs/manual/core/authorization)

## Keyfiles

Keyfiles use [SCRAM](/docs/manual/core/security-scram) challenge and response authentication mechanism where the keyfiles contain the shared password for the members.

### Key Requirements

A key's length must be between 6 and 1024 characters and may only contain characters in the base64 set. MongoDB strips whitespace characters (e.g. `x0d`, `x09`, and `x20`) for cross-platform convenience. As a result, the following operations produce identical keys:

```bash
echo -e "mysecretkey" > key1
echo -e "my secret key" > key1
echo -e "my secret key\n" > key2
echo -e "my    secret    key" > key3
echo -e "my\r\nsecret\r\nkey\r\n" > key4
```

### Keyfile Format

[Keyfiles for internal membership authentication](/docs/manual/core/security-internal-authentication#std-label-internal-auth-keyfile) use YAML format to allow for multiple keys in a keyfile. The YAML format accepts either:

- A single key string (same as in earlier versions)

- A sequence of key strings

The YAML format is compatible with the existing single-key keyfiles that use the text file format.

For example,

### Single key

If the keyfile contains a single key, you can specify the key string with or without quotes:

```yaml
my old secret key1
```

The ability to specify multiple keys in a file allows for the rolling upgrade of the keys without downtime. See [Rotate Keys for Self-Managed Replica Sets](/docs/manual/tutorial/rotate-key-replica-set) and [Rotate Keys for Self-Managed Sharded Clusters.](/docs/manual/tutorial/rotate-key-sharded-cluster)

All [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) and [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instances of a deployment must share at least one common key.

On UNIX systems, the keyfile must not have group or world permissions. On Windows systems, keyfile permissions are not checked.

You must store the keyfile on each server hosting the member of the replica set or sharded clusters.

For [MongoDB's encrypted storage engine](/docs/manual/core/security-encryption-at-rest), the [keyfile](/docs/manual/tutorial/configure-encryption#std-label-encrypt-local-key-mgmt) used for local key management can only contain a single key .

### MongoDB Configuration for Keyfile

To specify the keyfile, use the [`security.keyFile`](/docs/manual/reference/configuration-options#mongodb-setting-security.keyFile) setting or `--keyFile` command line option.

For an example of keyfile internal authentication, see [Update Self-Managed Replica Set to Keyfile Authentication.](/docs/manual/tutorial/enforce-keyfile-access-control-in-existing-replica-set)

## X.509

Members of a replica set or sharded cluster can use X.509 certificates for internal authentication instead of using keyfiles. This is also known as Mutual TLS or mTLS. MongoDB supports X.509 certificate authentication for use with a secure TLS/SSL connection.

**Note:**

MongoDB disables support for TLS 1.0 and TLS 1.1 encryption on systems where TLS 1.2+ is available.

### Member Certificate Requirements

When TLS is enabled, use member certificates to verify membership to internal connections in a sharded cluster or a replica set. You can configure member certificate file paths with the [`net.tls.clusterFile`](/docs/manual/reference/configuration-options#mongodb-setting-net.tls.clusterFile) and [`net.tls.certificateKeyFile`](/docs/manual/reference/configuration-options#mongodb-setting-net.tls.certificateKeyFile) options. Members have the following configuration requirements:

- Cluster member configuration must specify a non-empty value for at least one of the attributes used for authentication. By default, MongoDB accepts:

  - the Organization (`O`)

  - the Organizational Unit (`OU`)

  - the Domain Component (`DC`)

  MongoDB verifies that entries match exactly across all member certificates. If you list multiple `OU` values, all certificates must use an identical list.

  You can specify alternative attributes to use for authentication by setting [`net.tls.clusterAuthX509.extensionValue`.](/docs/manual/reference/configuration-options#mongodb-setting-net.tls.clusterAuthX509.extensionValue)

- Cluster member configuration must include the same [`net.tls.clusterAuthX509.attributes`](/docs/manual/reference/configuration-options#mongodb-setting-net.tls.clusterAuthX509.attributes) and use matching values. Attribute order doesn't matter. The following example sets `O` and `OU`, but not `DC`:

  ```yaml
  net:
    tls:
      clusterAuthX509:
        attributes: O=MongoDB, OU=MongoDB Server
  ```

**Note:**

If you set the `enforceUserClusterSeparation` parameter to `false`, the following behaviors apply:

- You cannot set `clusterAuthMode` to an option that allows X.509 or the server will not start. The server will only start if `clusterAuthMode` is `keyFile`.

- A client can create a user in the `$external` database whose `O/OU/DC` attributes match the server's configured attributes for cluster membership.

- A client presenting a member certificate can now attempt [MONGODB-X509](/docs/manual/core/security-x.509#std-label-security-auth-x509) authentication as a user in the `$external` database.

To set the `enforceUserClusterSeparation` parameter to `false`, run the following command during startup:

```javascript
mongod --setParameter enforceUserClusterSeparation=false
```

The certificates have the following requirements:

- A single Certificate Authority (CA) must issue all X.509 certificates for the members of a sharded cluster or a replica set.

- At least one of the Subject Alternative Name (`SAN`) entries must match the server hostname used by other cluster members. When comparing `SAN`s, MongoDB can compare either DNS names or IP addresses.

  If you don't specify `subjectAltName`, MongoDB compares the Common Name (CN) instead. However, this usage of CN is deprecated per [RFC2818](https://datatracker.ietf.org/doc/html/rfc2818)

Key Usage and Extended Key Usage are X.509 extensions that strictly define and restrict the use of the key associated with a certificate. Both of these extensions are optional. If `tlsCertificateKeyFile` or `tlsClusterFile` point to certificates that omit these extensions, no restrictions apply to using the certificate.

If X.509 certificates used for `tlsCertificateKeyFile` or `tlsClusterFile` include the Extended Key Usage (EKU) extension, they must comply with the following rules:

- `tlsCertificateKeyFile` must include `serverAuth` in EKU.

  ```none
  extendedKeyUsage = serverAuth
  ```

- `tlsClusterFile` must include `clientAuth` in EKU:

  ```none
  extendedKeyUsage = clientAuth
  ```

- If `tlsClusterFile` is omitted and only `tlsCertificateKeyFile` is configured, then `tlsCertificateKeyFile` must include both `serverAuth` and `clientAuth` in EKU:

  ```none
  extendedKeyUsage = clientAuth, serverAuth
  ```

If X.509 certificates used for `tlsCertificateKeyFile` or `tlsClusterFile` include the Key Usage (KU) extension, set it as follows:

- `tlsCertificateKeyFile` should contain `digitalSignature`, `keyEncipherment`, and `keyAgreement` in its KU extension:

  ```none
  keyUsage = digitalSignature, keyEncipherment, keyAgreement
  ```

- `tlsClusterFile` should contain `digitalSignature` in its KU extension:

  ```none
  keyUsage = digitalSignature
  ```

### MongoDB Configuration

You can use TLS for internal authentication between each member of your replica set (each [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instance) or sharded cluster (each [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) and [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instance).

To use TLS for internal authentication, use the following settings:

- [`security.clusterAuthMode`](/docs/manual/reference/configuration-options#mongodb-setting-security.clusterAuthMode) or [`--clusterAuthMode`](/docs/manual/reference/program/mongod#std-option-mongod.--clusterAuthMode) set to `x509`

- [`net.tls.clusterFile`](/docs/manual/reference/configuration-options#mongodb-setting-net.tls.clusterFile) or [`--tlsClusterFile`](/docs/manual/reference/program/mongod#std-option-mongod.--clusterAuthMode)

**Important:**

If you set [`--tlsMode`](/docs/manual/reference/program/mongod#std-option-mongod.--tlsMode)  to any value other than `disabled`, MongoDB uses the certificate specified in [`net.tls.certificateKeyFile`](/docs/manual/reference/configuration-options#mongodb-setting-net.tls.certificateKeyFile) for both server and client authentication in internal replica set connections. This certificate setting applies regardless of whether you set [`security.clusterAuthMode`](/docs/manual/reference/configuration-options#mongodb-setting-security.clusterAuthMode) to `X.509`.

[`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) and [`mongos`](/docs/manual/reference/program/mongos#std-option-mongos.--tlsCertificateKeyFile) instances use their certificate key files to prove their identity to clients, but certificate key files can also be used for membership authentication. If you do not specify a cluster file, members use their certificate key files for membership authentication. Specify the certificate key file with [`net.tls.certificateKeyFile`](/docs/manual/reference/configuration-options#mongodb-setting-net.tls.certificateKeyFile) or [`--tlsCertificateKeyFile`.](/docs/manual/reference/program/mongod#std-option-mongod.--tlsCertificateKeyFile)

To use the certificate key file for both client authentication and membership authentication, the certificate must either:

- Omit `extendedKeyUsage` or

- Specify `extendedKeyUsage = serverAuth, clientAuth`

## Next Steps

For an example of X.509 internal authentication, see [Verify Cluster Membership with X.509 on Self-Managed MongoDB.](/docs/manual/tutorial/configure-x509-member-authentication#std-label-x509-internal-authentication)

To upgrade from keyfile internal authentication to X.509 internal authentication, see [Upgrade from Keyfile Authentication to X.509 Authentication.](/docs/manual/tutorial/upgrade-keyfile-to-x509#std-label-upgrade-to-x509-internal-authentication)
