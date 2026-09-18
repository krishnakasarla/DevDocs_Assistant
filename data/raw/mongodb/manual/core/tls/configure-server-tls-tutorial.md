> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

<!--
Tab options on this page. Append to the .md URL to filter:
  ?tabs=<id,...>   select specific tabs (e.g. ?tabs=nodejs,shell)
  ?allTabs=true    include every tab
  (no param)       default: one tab per tabset

Available tabs:
  other tabs: server-tls-without-mtls, server-tls-with-mtls
-->

# Configure TLS on Self-Managed Deployments

This tutorial shows you how to configure TLS (Transport Layer Security) on a self-managed replica set. Select an approach based on whether you want to use intra-cluster mTLS (Mutual TLS), which is required to enable X.509 authentication between nodes.

**Important:**

These steps apply to self-managed MongoDB deployments. MongoDB Atlas clusters use TLS (Transport Layer Security) by default. If you use Cloud Manager or Ops Manager, configure TLS through your deployment management tool.

## Before You Begin

Before you start, verify that you have the following:

- A self-managed replica set in which each node has a hostname, such as `localhost` or `mongo0.example.com`. TLS is not currently configured on any node in the replica set.

- TLS server certificates for each node that you obtained by following the [Obtain Server Certificates](/docs/manual/core/tls/certificate-tutorial#std-label-tls-certificate-tutorial) tutorial, such as `mongo0.pem`.

- A CA certificate to sign the server certificates, such as `ca.pem`.

- Access to the [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) configuration file on each node.

- Access to [`mongosh`.](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh)

## Steps

### Intra-Cluster TLS with Keyfile Auth

Follow this procedure if you do not need intra-cluster mTLS or X.509 authentication between server nodes.

1. Create a keyfile

   Each node uses the contents of a keyfile to authenticate other members of the deployment. Create a keyfile using the following command:

   ```shell
   openssl rand -base64 756 > /etc/ssl/mongodb/keyfile
   chmod 400 /etc/ssl/mongodb/keyfile
   ```

   Copy the keyfile to each node in your deployment. Ensure that you restrict permissions on the keyfile so that only the `mongod` process can read the file.

2. Edit the configuration file on each node

   On **each node,** locate and open your `mongod` configuration file. If the file does not exist, create it. Add the following [TLS options](/docs/manual/reference/configuration-options#std-label-net-tls-conf-options). Use absolute paths to the certificate files.

   For example, the configuration file for your primary node looks like the following:

   ```yaml
   net:
     tls:
       mode: allowTLS
       certificateKeyFile: /etc/ssl/mongodb/mongo0.pem
       CAFile: /etc/ssl/mongodb/ca.pem
       allowConnectionsWithoutCertificates: true

   security:
     clusterAuthMode: keyFile
     keyFile: /etc/ssl/mongodb/keyfile

   setParameter:
     tlsWithholdClientCertificate: true
   ```

   - [`mode`](/docs/manual/reference/configuration-options#mongodb-setting-net.tls.mode) set to `allowTLS` accepts TLS connections but does not require them, so nodes can complete a rolling restart without interrupting replication.

   - [`certificateKeyFile`](/docs/manual/reference/configuration-options#mongodb-setting-net.tls.certificateKeyFile) specifies the node's certificate. Replace the filename with the certificate key file for the specific node you are configuring. [`CAFile`](/docs/manual/reference/configuration-options#mongodb-setting-net.tls.CAFile) specifies the CA certificate that signed the node's certificate.

   - [`allowConnectionsWithoutCertificates`](/docs/manual/reference/configuration-options#mongodb-setting-net.tls.allowConnectionsWithoutCertificates) allows clients to connect without providing a TLS certificate.

   - [`clusterAuthMode`](/docs/manual/reference/configuration-options#mongodb-setting-security.clusterAuthMode) set to `keyFile` enables nodes to authenticate using a keyfile. [`keyFile`](/docs/manual/reference/configuration-options#mongodb-setting-security.keyFile) specifies the keyfile that nodes use to authenticate to each other.

   - [`tlsWithholdClientCertificate`](/docs/manual/reference/parameters#mongodb-parameter-param.tlsWithholdClientCertificate) prevents the node from presenting its server certificate when making outbound connections to other nodes in the cluster. This is necessary because it prevents nodes from using server-authentication certificates for client authentication, especially if your certificates do not include the `clientAuth` EKU.

3. Restart the replica set members

   Restart the `mongod` process to apply the new TLS configuration. To apply the configuration without downtime, restart nodes in a rolling fashion.

   On each host for your deployment, starting with the secondary nodes and finishing with the primary node, run the following:

   ```sh
   sudo systemctl restart mongod
   ```

   To verify that the rolling restart completed successfully, run the following command on each host:

   ```sh
   sudo systemctl status mongod
   ```

4. Update the configuration to enforce TLS

   After all nodes restart successfully with TLS enabled, update the configuration file on each node. Change `net.tls.mode` from `allowTLS` to `requireTLS` to enforce encrypted connections for all clients and members:

   ```yaml
   net:
     tls:
       mode: requireTLS
   ```

5. Restart the replica set members

   Restart the `mongod` process to apply the new TLS configuration. To apply the configuration without downtime, restart nodes in a rolling fashion.

   On each host for your deployment, starting with the secondary nodes and finishing with the primary node, run the following:

   ```sh
   sudo systemctl restart mongod
   ```

   To verify that the rolling restart completed successfully, run the following command on each host:

   ```sh
   sudo systemctl status mongod
   ```

## Next Steps

To learn how to connect to your deployment with a client application, continue to [Connect to a TLS-Enabled Replica Set.](/docs/manual/core/tls/configure-client-tls-tutorial#std-label-configure-client-tls-tutorial)
