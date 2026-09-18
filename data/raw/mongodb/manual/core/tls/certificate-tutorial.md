> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Obtain TLS Server Certificates

Obtain server certificates to enable TLS (Transport Layer Security) encryption for your self-managed MongoDB replica set deployments.

**Important:**

These steps apply to self-managed MongoDB deployments. MongoDB Atlas clusters use TLS (Transport Layer Security) by default. If you use Cloud Manager or Ops Manager, configure TLS through your deployment management tool.

## Before you Begin

Before you start, ensure you have the following information and resources:

- You have a self-managed MongoDB replica set deployment that you want to secure with TLS.

- You have at least one admin user enabled on your deployment to verify TLS connections in later tutorials. If you want to enable X.509 client authentication, the admin user must have at least the [`userAdmin`](/docs/manual/reference/built-in-roles#mongodb-authrole-userAdmin) role to create and modify users in the `$external` database.

- You have a hostname for each node in your deployment, such as `mongo0.example.com`, `mongo1.example.com`, and `mongo2.example.com`. If you are using a public CA (Certificate Authority), you must have a registered domain name that corresponds to these hostnames.

- You have [OpenSSL](https://www.openssl.org/) installed on your machine.

- If you are planning on using a public CA, such as Let's Encrypt or DigiCert, you know which public CA you are using. If you are planning on using a private CA, you have access to your organization's PKI (Public Key Infrastructure) information. The process for obtaining certificates might be different based on the CA you use. However, you must end with the same `.pem` files described in the [final result](/docs/manual/core/tls/certificate-tutorial#std-label-tls-certificate-final-state) section of this tutorial.

- You have your preferred command line interface open.

- You know your deployment TLS configuration requirements and whether your certificates need `clientAuth` EKU (Extended Key Usage) based on the TLS Planning page.

## Steps

This tutorial creates one certificate called `mongo0.pem` for the first node in your deployment. When generating certificates for additional nodes, be specific in your file names. For example, name the certificate for your first secondary node `mongo1.pem`.

Follow this tutorial to obtain a server certificate from a public CA. **You must obtain a certificate for each node in your
deployment.**

1. Prepare your workspace

   Create and navigate to a directory to store your key and certificate files.

   On Linux or MacOS, run the following commands:

   ```bash
   mkdir -p ~/mongo-tls
   cd ~/mongo-tls
   ```

   In Windows Command Prompt or PowerShell:

   ```shell
   mkdir C:\mongo-tls
   cd C:\mongo-tls
   ```

2. Generate a private key

   **Note:**

   If you are using a CA that uses the ACME protocol like Let's Encrypt, the CA generates the certificate for you. In this case, follow your CA's instructions instead and resume this tutorial at the step where you create `.pem` files from your certificate and private key.

   Generate a private key with OpenSSL:

   ```bash
   openssl genrsa -out mongo0.key 4096
   ```

   This generates a 4096-bit RSA private key. If you need to use a different key size or algorithm, see the OpenSSL documentation.

   Restrict permissions on the generated `mongo0.key` file:

   ```bash
   chmod 600 mongo0.key
   ```

   Keep this file secret. The server uses this key to prove it owns the certificate.

3. Create a certificate signing request

   **Important:**

   Starting in April 2026, major public CAs stopped issuing TLS certificates that support client authentication. If you are using a public CA, do not include `extendedKeyUsage = clientAuth` in your CSR (Certificate Signing Request). If you need server certificates for client authentication, use a private CA. See the [Public Certificate Authority Policy Changes Affecting mTLS](https://www.mongodb.com/resources/products/alerts/public-certificate-authority-policy-changes-affecting-mtls/) Technical Advisory for more information.

   First, create a minimal OpenSSL configuration file called `csr.conf` that uses the following format:

   ```text
   [ req ]
   distinguished_name = dn
   prompt             = no
   req_extensions     = req_ext

   # Replace values in this section with your own information.

   [ dn ]
   C  = US                    # 2-letter country code
   ST = New-York              # State or province
   L  = New York City         # City or locality
   O  = Example Corp          # Organization name
   CN = mongo0.example.com    # Hostname of your MongoDB node

   [ req_ext ]
   subjectAltName = @alt_names
   keyUsage = digitalSignature
   extendedKeyUsage = serverAuth

   # Replace values in this section with any alternative
   # hostnames or IP addresses for your MongoDB node.

   [ alt_names ]
   DNS.1 = mongo0.example.com
   DNS.2 = localhost
   IP.1 = 127.0.0.1
   ```

   For more information about the fields in this file, see the OpenSSL [config file documentation](https://docs.openssl.org/3.6/man5/config/). Ensure that you fill out both the Common Name (`CN`) and Subject Alternative Name (`alt_names`) fields in the configuration file.

   Then, generate a CSR (Certificate Signing Request):

   ```bash
   openssl req -new -key mongo0.key -out mongo0.csr -config csr.conf
   ```

   This creates `mongo0.csr`. You will submit this file to the CA.

4. Submit the CSR to a public CA

   Sign in to your chosen public CA's portal and follow their instructions to submit your CSR. When prompted, upload or paste the contents of your `mongo0.csr` file. Choose the appropriate validation level:

   - **Domain Validation (DV)**: The CA verifies that you control the domain for which you're requesting a certificate. This is typically the quickest and least expensive option.

   - **Organization/Extended Validation (OV/EV)**: Choose this if your organization requires a higher level of trust.

   Follow the CA's instructions to complete the validation process. After successful completion, the CA issues your certificate.

5. Download and verify the certificate and chain

   After validation, download:

   - Your server certificate, stored as `mongo0.crt`

   - The `.pem` CA intermediate bundle, stored as `ca.pem`

   After you receive or create your certificate, verify that it matches the private key:

   ```bash
   # Compare the modulus of the key and certificate
   openssl rsa -noout -modulus -in  mongo0.key | openssl sha256
   openssl x509 -noout -modulus -in mongo0.crt | openssl sha256
   ```

   The output digests must match. If they do not, the certificate and key do not belong together, and MongoDB will not be able to use them.

   If your CA provided a separate chain file, you can also inspect it:

   ```bash
   openssl x509 -in mongo0.crt -text -noout
   openssl x509 -in ca.pem -text -noout
   ```

   Confirm that the certificate's `Issuer` and `Subject` fields, as well as validity dates, look correct.

6. Create `.pem` files

   You must combine your certificate and its private key to create a `.pem` file. For example, on Linux or MacOS:

   ```bash
   cat mongo0.crt mongo0.key > mongo0.pem
   ```

   In Windows PowerShell:

   ```shell
   type mongo0.crt mongo0.key > mongo0.pem
   ```

7. Organize the certificate and chain files

   Copy your `.pem` files to the directory where you plan to store TLS assets for MongoDB. You will reference these paths in your MongoDB configuration file in the next tutorial.

   You might need to copy the `.pem` files onto the remote server on which you host your node. Additionally, ensure you secure your files with appropriate permissions, such as read-only access for the owner.

   In Linux/MacOS:

   ```bash
   sudo mkdir -p /etc/ssl/mongodb
   sudo cp mongo0.pem ca.pem /etc/ssl/mongodb
   ```

   In Windows PowerShell:

   ```shell
   New-Item -ItemType Directory -Path C:\tls\mongodb -Force
   Copy-Item mongo0.pem,ca.pem `
     -Destination C:\tls\mongodb
   ```

8. Repeat for other nodes in deployment

   If you have multiple nodes or need multiple certificates for each node, obtain a certificate for each node following the same process.

   **Note:**

   In your MongoDB deployment, all certificates must be signed by the same CA. Therefore, you only need one CA certificate (`ca.pem`) and can skip downloading it again when obtaining your additional certificates.

If your organization operates its own internal PKI or private CA, obtain certificates from that CA. **You must obtain a certificate for each node in your
deployment.**

1. Prepare your workspace

   Create and navigate to a directory to store your key and certificate files.

   On Linux or MacOS, run the following commands:

   ```bash
   mkdir -p ~/mongo-tls
   cd ~/mongo-tls
   ```

   In Windows Command Prompt or PowerShell:

   ```shell
   mkdir C:\mongo-tls
   cd C:\mongo-tls
   ```

2. Review your organization's PKI requirements

   Check your internal PKI (Public Key Infrastructure) documentation, or contact your security team, for information like required key sizes, algorithms, or SANs (Subject Alternative Names).

3. Generate a private key

   **Note:**

   Your CA might use a different process for certificate generation, such as a web interface. In this case, follow your CA's instructions instead and resume this tutorial at the step where you create `.pem` files from your certificate and private key.

   Generate a private key with OpenSSL:

   ```bash
   openssl genrsa -out mongo0.key 4096
   ```

   This generates a 4096-bit RSA private key. If you need to use a different key size or algorithm, see the OpenSSL documentation.

   Restrict permissions on the generated `mongo0.key` file:

   ```bash
   chmod 600 mongo0.key
   ```

   Keep this file secret. The server uses this key to prove it owns the certificate.

4. Create a certificate signing request

   Ensure that your CSR (Certificate Signing Request) meets your organization's PKI policies.

   **Note:**

   If you want intra-cluster mTLS between nodes in your deployment, set `extendedKeyUsage = serverAuth, clientAuth` in your CSR configuration file so that your nodes can authenticate as both TLS servers and clients.

   First, create a minimal OpenSSL configuration file called `csr.conf` that uses the following format:

   ```text
   [ req ]
   distinguished_name = dn
   prompt             = no
   req_extensions     = req_ext

   # Replace values in this section with your own information.

   [ dn ]
   C  = US                    # 2-letter country code
   ST = New-York              # State or province
   L  = New York City         # City or locality
   O  = Example Corp          # Organization name
   CN = mongo0.example.com    # Hostname of your MongoDB node

   [ req_ext ]
   subjectAltName = @alt_names
   keyUsage = digitalSignature
   extendedKeyUsage = serverAuth

   # Replace values in this section with any alternative
   # hostnames or IP addresses for your MongoDB node.

   [ alt_names ]
   DNS.1 = mongo0.example.com
   DNS.2 = localhost
   IP.1 = 127.0.0.1
   ```

   For more information about the fields in this file, see the OpenSSL [config file documentation](https://docs.openssl.org/3.6/man5/config/). Ensure that you fill out both the Common Name (`CN`) and Subject Alternative Name (`alt_names`) fields in the configuration file.

   Then, generate a CSR (Certificate Signing Request):

   ```bash
   openssl req -new -key mongo0.key -out mongo0.csr -config csr.conf
   ```

   This creates `mongo0.csr`. You will submit this file to the CA.

5. Submit the CSR to your private CA

   Upload `mongo0.csr` to your internal PKI portal, or send it to your PKI administrators as instructed.

6. Download and verify the certificate and chain

   After validation, download:

   - Your server certificate, stored as `mongo0.crt`

   - The `.pem` CA intermediate bundle, stored as `ca.pem`

   After you receive or create your certificate, verify that it matches the private key:

   ```bash
   # Compare the modulus of the key and certificate
   openssl rsa -noout -modulus -in  mongo0.key | openssl sha256
   openssl x509 -noout -modulus -in mongo0.crt | openssl sha256
   ```

   The output digests must match. If they do not, the certificate and key do not belong together, and MongoDB will not be able to use them.

   If your CA provided a separate chain file, you can also inspect it:

   ```bash
   openssl x509 -in mongo0.crt -text -noout
   openssl x509 -in ca.pem -text -noout
   ```

   Confirm that the certificate's `Issuer` and `Subject` fields, as well as validity dates, look correct.

7. Create `.pem` files

   You must combine your certificate and its private key to create a `.pem` file. For example, on Linux or MacOS:

   ```bash
   cat mongo0.crt mongo0.key > mongo0.pem
   ```

   In Windows PowerShell:

   ```shell
   type mongo0.crt mongo0.key > mongo0.pem
   ```

8. Organize the certificate and chain files

   Copy your `.pem` files to the directory where you plan to store TLS assets for MongoDB. You will reference these paths in your MongoDB configuration file in the next tutorial.

   You might need to copy the `.pem` files onto the remote server on which you host your node. Additionally, ensure you secure your files with appropriate permissions, such as read-only access for the owner.

   In Linux/MacOS:

   ```bash
   sudo mkdir -p /etc/ssl/mongodb
   sudo cp mongo0.pem ca.pem /etc/ssl/mongodb
   ```

   In Windows PowerShell:

   ```shell
   New-Item -ItemType Directory -Path C:\tls\mongodb -Force
   Copy-Item mongo0.pem,ca.pem `
     -Destination C:\tls\mongodb
   ```

9. Repeat for other nodes in deployment

   If you have multiple nodes or need multiple certificates for each node, obtain a certificate for each node following the same process.

   **Note:**

   In your MongoDB deployment, all certificates must be signed by the same CA. Therefore, you only need one CA certificate (`ca.pem`) and can skip downloading it again when obtaining your additional certificates.

Use self-signed certificates for local development and testing. **Do not use self-signed certificates in production.**

1. Prepare your workspace

   Create and navigate to a directory to store your key and certificate files.

   On Linux or MacOS, run the following commands:

   ```bash
   mkdir -p ~/mongo-tls
   cd ~/mongo-tls
   ```

   In Windows Command Prompt or PowerShell:

   ```shell
   mkdir C:\mongo-tls
   cd C:\mongo-tls
   ```

2. Generate a private key

   Generate a private key with OpenSSL:

   ```bash
   openssl genrsa -out mongo0.key 4096
   ```

   This generates a 4096-bit RSA private key. If you need to use a different key size or algorithm, see the OpenSSL documentation.

   Restrict permissions on the generated `mongo0.key` file:

   ```bash
   chmod 600 mongo0.key
   ```

   Keep this file secret. The server uses this key to prove it owns the certificate.

3. Create a configuration file

   **Note:**

   If you want intra-cluster mTLS between nodes in your deployment, set `extendedKeyUsage = serverAuth, clientAuth` in your CSR configuration file so that your nodes can authenticate as both TLS servers and clients.

   Create a minimal OpenSSL configuration file called `csr.conf` that uses the following format:

   ```text
   [ req ]
   distinguished_name = dn
   prompt             = no
   req_extensions     = req_ext

   # Replace values in this section with your own information.

   [ dn ]
   C  = US                    # 2-letter country code
   ST = New-York              # State or province
   L  = New York City         # City or locality
   O  = Example Corp          # Organization name
   CN = mongo0.example.com    # Hostname of your MongoDB node

   [ req_ext ]
   subjectAltName = @alt_names
   keyUsage = digitalSignature
   extendedKeyUsage = serverAuth

   # Replace values in this section with any alternative
   # hostnames or IP addresses for your MongoDB node.

   [ alt_names ]
   DNS.1 = mongo0.example.com
   DNS.2 = localhost
   IP.1 = 127.0.0.1
   ```

   For more information about the fields in this file, see the OpenSSL [config file documentation](https://docs.openssl.org/3.6/man5/config/). Ensure that you fill out both the Common Name (`CN`) and Subject Alternative Name (`alt_names`) fields in the configuration file.

4. Generate a self-signed certificate

   Generate a certificate with the private key and configuration file that you created:

   ```bash
   openssl req -new \
      -x509 -days 365 \
      -key mongo0.key \
      -out mongo0.crt \
      -config csr.conf
   ```

   This command creates a self-signed certificate, `mongo0.crt`, that is valid for 365 days.

5. Verify the certificate

   After you receive or create your certificate, verify that it matches the private key:

   ```bash
   # Compare the modulus of the key and certificate
   openssl rsa -noout -modulus -in  mongo0.key | openssl sha256
   openssl x509 -noout -modulus -in mongo0.crt | openssl sha256
   ```

   The output digests must match. If they do not, the certificate and key do not belong together, and MongoDB will not be able to use them.

6. Create `.pem` files

   You must combine your certificate and its private key to create a `.pem` file. For example, on Linux or MacOS:

   ```bash
   cat mongo0.crt mongo0.key > mongo0.pem
   ```

   In Windows PowerShell:

   ```shell
   type mongo0.crt mongo0.key > mongo0.pem
   ```

   You can use your self-signed certificate as the CA file. For consistency with this tutorial, rename the certificate:

   ```bash
   cp mongo0.crt ca.pem
   ```

7. Organize the certificate and chain files

   Copy your `.pem` files to the directory where you plan to store TLS assets for MongoDB. You will reference these paths in your MongoDB configuration file in the next tutorial.

   You might need to copy the `.pem` files onto the remote server on which you host your node. Additionally, ensure you secure your files with appropriate permissions, such as read-only access for the owner.

   In Linux/MacOS:

   ```bash
   sudo mkdir -p /etc/ssl/mongodb
   sudo cp mongo0.pem ca.pem /etc/ssl/mongodb
   ```

   In Windows PowerShell:

   ```shell
   New-Item -ItemType Directory -Path C:\tls\mongodb -Force
   Copy-Item mongo0.pem,ca.pem `
     -Destination C:\tls\mongodb
   ```

8. Repeat for other nodes in deployment

   If you have multiple nodes or need multiple certificates for each node, obtain a certificate for each node following the same process.

## Final Result

At the end of this tutorial, you have the following `.pem` files in `/etc/ssl/mongodb`:

- For **each node**, you have a `.pem` file that contains the certificate and private key for that node, such as `mongo0.pem`, `mongo1.pem`, and `mongo2.pem`.

- For the deployment overall, you have the intermediate CA certificate that issued the certificates for each node, such as `ca.pem`.

## Next Steps

To learn how to configure TLS for your self-managed MongoDB deployment, continue to the next tutorial, [Configure TLS for a Self-Managed Deployment.](/docs/manual/core/tls/configure-server-tls-tutorial#std-label-configure-server-tls-tutorial)
