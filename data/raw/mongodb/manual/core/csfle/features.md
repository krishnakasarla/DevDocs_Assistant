> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# CSFLE Features

## Overview

On this page, you can learn about the security benefits of Client-Side Field Level Encryption (CSFLE), and how CSFLE compares to other security mechanisms supported by MongoDB. You can also view a fictional scenario that demonstrates the value of CSFLE in securing your data.

## Client-Side Field Level Encryption

Client-Side Field Level Encryption (CSFLE) is a feature of MongoDB that enables a client application to encrypt data before transporting it over the network. Sensitive data is transparently encrypted and decrypted by the client and only communicated to and from the server in encrypted form. CSFLE keeps encrypted fields secure in the following scenarios:

- Direct access to encrypted fields by a database superuser

- Access to encrypted fields by reading the server's memory

- Capture of encrypted fields over an insecure network

- Access to on-disk encrypted fields by reading database or backup files

While all clients have access to the non-sensitive data fields, only appropriately-configured CSFLE clients are able to read and write the encrypted data fields.

**Important: Remote Key Management System**

When you use CSFLE in production, you must use a remote Key Management System (KMS) to store your encryption key.

To view a step-by-step guide demonstrating how to use a remote KMS with CSFLE, see [CSFLE Tutorials.](/docs/manual/core/csfle/tutorials#std-label-csfle-tutorial-automatic-encryption)

To view a list of all supported KMS providers, see [KMS Providers.](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-fundamentals-kms-providers)

To learn more about why you should use a remote KMS, see [Reasons to Use a Remote Key Management System.](/docs/manual/core/queryable-encryption/fundamentals/kms-providers#std-label-qe-reasons-to-use-remote-kms)

## Other Security Mechanisms

This section describes the following security mechanisms supported by MongoDB and explains their use cases and limitations:

- [Role-Based Access Control](/docs/manual/core/csfle/features#std-label-csfle-features-role-based-access-control)

- [Encryption at Rest](/docs/manual/core/csfle/features#std-label-csfle-features-encryption-at-rest)

- [Transport Encryption (TLS/SSL)](/docs/manual/core/csfle/features#std-label-csfle-features-transport-encryption)

### Role-Based Access Control

Role-Based Access Control is a security mechanism that allows administrators to grant and restrict collection-level permissions for users. With the appropriate role definition and assignment, this solution prevents accidental disclosure of data and access.

Role-Based Access control cannot protect against the following scenarios:

- Capture of the data over an insecure network

- Access to on-disk data by reading database or backup files

- Access to data by reading the server's memory

- Direct access to data by a database superuser

To learn more, see [Role-Based Access Control.](https://www.mongodb.com/docs/manual/core/authorization/)

### Encryption at Rest

Encryption at Rest is a mechanism that encrypts database files on disk. This mechanism prevents a person who lacks database credentials, but has access to the computer hosting your database, from viewing your data.

This mechanism does not protect your data against the following scenarios:

- Capture of the data over an insecure network

- Access to data by reading the server's memory

- Direct access to data by a database superuser

To learn more, see [Encryption at Rest.](https://www.mongodb.com/docs/manual/core/security-encryption-at-rest/)

### Transport Encryption (TLS/SSL)

Transport Encryption using TLS/SSL encrypts your data over the network. TLS/SSL protects your data as it travels over an insecure network, but cannot protect your data from a privileged user or as it sits on disk.

To learn more, see [Transport Encryption using TLS/SSL](https://www.mongodb.com/docs/manual/core/security-transport-encryption/)

## Comparison of Features

To learn more about Queryable Encryption, see [Queryable Encryption Features.](/docs/manual/core/queryable-encryption/features#std-label-qe-features)

The following table describes potential security threats and how MongoDB encryption features address them. Use these mechanisms together: Role-Based Access Control, Encryption at Rest, Transport Encryption, and In-Use Encryption. Note that you can't use both Client-Side Field Level Encryption and Queryable Encryption in the same collection.

**Important:**

This is a high-level summary meant for general comparison. For detailed information, see the [Overview of Queryable Encryption](https://cdn.bfldr.com/2URK6TO/as/64kp46t53v34xw37gkngbrg/An_Overview_of_Queryable_Encryption) and [Design and Analysis of a Stateless Document Database Encryption Scheme](https://cdn.bfldr.com/2URK6TO/as/jkwp857q2zr8fj5vqs24f5/Design__Analysis_Stateless_Document_Database_Encryption_Scheme) whitepapers.

| Threat | TLS/SSL Transport Encryption | Encryption at Rest (EaR) | Queryable Encryption (Equality) + TLS/SSL + EaR | CSFLE + TLS/SSL + EaR |
| --- | --- | --- | --- | --- |
| Network Snooping (attacker has access to network traffic) | Reveals [operation metadata](/docs/manual/reference/glossary#std-term-operation-metadata) | Reveals operation metadata | Reveals operation metadata | Reveals operation metadata |
| Database Recoveries from Disk (attacker has physical disk access) | Reveals database | Reveals *size of database* and operation metadata | Reveals *size of database* and operation metadata | Reveals *size of database* and operation metadata |
| [Database exfiltration](/docs/manual/reference/glossary#std-term-database-exfiltration) from Disk and Memory (attacker has physical disk access and multiple database snapshots) | Reveals database | Reveals database | Reveals *size of database* and operation metadata | Reveals *frequency of values* and operation metadata |
| [Advanced Persistent Threat](/docs/manual/reference/glossary#std-term-Advanced-Persistent-Threat) (attacker has long-term, continuous access to network, disk, and memory while remaining undetected) | Reveals database | Reveals database | Queryable Encryption is not designed to protect against an ATP. See [whitepaper](https://cdn.bfldr.com/2URK6TO/as/64kp46t53v34xw37gkngbrg/An_Overview_of_Queryable_Encryption) for details. | CSFLE is not designed to protect against an ATP. See [whitepaper](https://cdn.bfldr.com/2URK6TO/as/64kp46t53v34xw37gkngbrg/An_Overview_of_Queryable_Encryption) for details. |

This assumes exfiltration occurs between completed operations. See [whitepaper](https://cdn.bfldr.com/2URK6TO/as/64kp46t53v34xw37gkngbrg/An_Overview_of_Queryable_Encryption) for details.

## Scenario

The following fictional scenario demonstrates the value of Client-Side Field Level Encryption (CSFLE) in securing your application's data, and how CSFLE interacts with the other security mechanism discussed in this guide.

In this scenario, we secure sensitive data on a medical care management system that stores patients' personal information, insurance information, and medical records for a fictional company, *MedcoMD*. None of the patient data is public, and specific data such as their social security number (SSN, a US government-issued ID number), insurance policy number, and vital sign measurements are particularly sensitive and subject to privacy compliance. It is important for the company and the patient that the data is kept private and secure.

MedcoMD needs this system to satisfy the following use cases:

- Doctors use the system to access patients' medical records, insurance information, and add new vital sign measurements.

- Receptionists use the system to verify patients' identities using their contact information.

- Receptionists can view a patient's insurance policy provider, but not their policy number.

- Receptionists cannot access a patient's medical records.

MedcoMD is also concerned with the disclosure of sensitive data through any of the following methods:

- Accidental disclosure of data on a receptionist's publicly-viewable screen.

- Direct access to the database by a superuser such as a database administrator.

- Capture of data over an insecure network.

- Access to data by reading the database server's memory.

- Access to data by reading database or backup files.

What can MedcoMD do to balance the functionality and access restrictions of their medical care management system?

### Solution

MedcoMD uses the following security mechanisms to satisfy their use cases and protect against the disclosure of sensitive medical data:

- [Transport Encryption (TLS/SSL)](/docs/manual/core/csfle/features#std-label-csfle-features-transport-encryption) to secure data as it travels over the network.

- [Encryption at Rest](/docs/manual/core/csfle/features#std-label-csfle-features-encryption-at-rest) to protect against disclosure of data by reading database or backup files.

- [Role-Based Access Control](/docs/manual/core/csfle/features#std-label-csfle-features-role-based-access-control) to limit the access of database users to the collections necessary for them to perform their tasks.

- Encrypting sensitive fields with CSFLE to satisfy the following use cases and constraints:

  - Prevent reading data from server memory as the CSFLE encrypted data is never on the database server in an unencrypted form.

  - Allow receptionists to verify patients' identities and prevent accidental disclosure of sensitive data on a receptionist's publicly viewable screen by providing receptionists with a client that is not CSFLE-enabled.

  - Allow doctors to view sensitive data privately in their offices by providing doctors with a CSFLE-enabled client.

## Learn More

To view a list of security measures you should implement to protect your MongoDB deployment, see the [Security Checklist.](https://www.mongodb.com/docs/manual/administration/security-checklist/)

To start using CSFLE, see the [CSFLE Quick Start.](/docs/manual/core/csfle/quick-start#std-label-csfle-quick-start)
