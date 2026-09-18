> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

<!--
Tab options on this page. Append to the .md URL to filter:
  ?tabs=<id,...>   select specific tabs (e.g. ?tabs=nodejs,shell)
  ?allTabs=true    include every tab
  (no param)       default: one tab per tabset

Available tabs:
  other tabs: client-tls-no-cert, client-tls-with-cert
-->

# Connect to a TLS-Enabled Replica Set

This tutorial shows you how to connect [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) to a TLS (Transport Layer Security)-enabled self-managed replica set.

## Before You Begin

Before you start, verify that you have the following:

- A replica set that you configured to use TLS using the steps in [Configure TLS on Self-Managed Deployments.](/docs/manual/core/tls/configure-server-tls-tutorial#std-label-configure-server-tls-tutorial)

- MongoDB access control enabled on your deployment and at least one admin user created. To set up access control, see [Enable Access Control on Self-Managed Deployments](/docs/manual/tutorial/enable-authentication#std-label-enable-access-control). This user must have `clusterMonitor` privileges.

- If you want to connect to your deployment using X.509 authentication, ensure that you have OpenSSL installed to generate a client certificate.

- Access to [`mongosh`.](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh)

## Steps

### Without X.509 Client Authentication

If you do not want to use mutual TLS or X.509 client authentication, follow this procedure. If you set [`allowConnectionsWithoutCertificates`](/docs/manual/reference/configuration-options#mongodb-setting-net.tls.allowConnectionsWithoutCertificates) to `true` in your server configuration, clients can connect without presenting a certificate and authenticate with SCRAM instead.

1. Connect to your deployment with `mongosh`

   Connect `mongosh` to your replica set using the following options:

   ```bash
   mongosh "mongodb://mongo0.example.com:27017,mongo1.example.com:27017,mongo2.example.com:27017" \
       --tls --tlsCAFile /etc/ssl/mongodb/ca.pem
   ```

   - [`--tls`](https://www.mongodb.com/docs/mongodb-shell/reference/options/#std-option-mongosh.--tls) enables TLS encryption for the connection.

   - [`--tlsCAFile`](https://www.mongodb.com/docs/mongodb-shell/reference/options/#std-option-mongosh.--tlsCAFile) is set to the CA certificate that signed the server certificates so that `mongosh` can verify the server's certificates.

   Connecting without a client certificate establishes a TLS-encrypted session but does not authenticate you. To run most commands, you must authenticate with a mechanism such as [SCRAM.](/docs/manual/core/security-scram#std-label-authentication-scram)

2. Authenticate user

   Use the [`db.auth()`](/docs/manual/reference/method/db.auth#mongodb-method-db.auth) method to authenticate with your admin username and password.

3. Verify your connection

   Run the following to confirm your authentication state:

   ```javascript
   db.adminCommand({ connectionStatus: 1 })
   ```

   Confirm that `authInfo.authenticatedUsers` includes the expected user.

## Final Result

After completing this tutorial, `mongosh` is connected to your replica set over an encrypted TLS connection, authenticated with either SCRAM or X.509.
