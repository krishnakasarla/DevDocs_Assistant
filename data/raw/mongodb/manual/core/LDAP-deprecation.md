> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# LDAP Deprecation

Starting in MongoDB 8.0, LDAP authentication and authorization is deprecated. LDAP is available and will continue to operate without changes throughout the lifetime of MongoDB 8. LDAP will be removed in a future major release.

You should plan to migrate from LDAP to an alternative authentication method.

Full LDAP migration information will be available in the future.

## Details

The following sections introduce alternative authentication methods for self-managed MongoDB Enterprise Advanced, MongoDB Atlas, and MongoDB Atlas for Government.

### Self-Managed MongoDB Enterprise Advanced

For human user access, MongoDB recommends migrating from LDAP to Workforce Identity Federation (OIDC authentication). Workforce Identity Federation allows single sign-on (SSO) access to your self-managed MongoDB databases using any IdP (Identity Provider) that supports OIDC, such as Microsoft Active Directory Federation Services (ADFS), Microsoft Entra ID, Okta, and Ping Identity.

For programmatic users, MongoDB recommends migrating from LDAP to Workload Identity Federation. With Workload Identity Federation, your applications can use databases with OAuth 2.0 access tokens provided by your authorization service.

You can also use cloud provider principals such as Microsoft Azure Managed Identities and Google Cloud Platform (GCP) service accounts. If you cannot use Workload Identity Federation, MongoDB recommends you use X.509 certificate authentication.

- To configure Workforce Identity Federation (OIDC authentication) with the MongoDB server, see [Configure MongoDB with Workforce Identity Federation.](/docs/manual/core/oidc/workforce/configure-oidc#std-label-configure-oidc)

- To configure Workload Identity Federation (OAuth2.0) with the MongoDB server, see [Configure MongoDB with Workload Identity Federation.](/docs/manual/core/oidc/workload/configure-mongodb-workload#std-label-configure-mongodb-workload)

- To configure Workforce and Workload Identity Federation with MongoDB Cloud Manager, see [Enable Authentication and Authorization with Cloud Manager.](https://www.mongodb.com/docs/cloud-manager/tutorial/enable-oidc-authentication-for-group/)

- To configure Workforce and Workload Identity Federation with MongoDB Ops Manager, see [Enable Authentication and Authorization with Ops Manager.](https://www.mongodb.com/docs/ops-manager/current/tutorial/enable-oidc-authentication-for-group/)

Some of the advantages of Workforce and Workload Identity Federation compared to LDAP for a self-managed MongoDB deployment are:

- **No credentials stored in MongoDB:** The LDAP bind user credentials are stored in MongoDB. With Workforce or Workload Identity Federation, MongoDB doesn't store credentials or secrets that grant access to user directories.

- **Reduced cross-application risk:** In an LDAP connection, the user's LDAP credentials are sent to MongoDB within the connection string, which is a risk for cross-application access. However, with Workforce and Workload Identity Federation, MongoDB never receives a secret. OIDC and OAuth 2.0 grant access tokens for specific resources using audience claims. If a token is compromised, the token cannot be used to access other applications.

- **Improved security with access tokens:** Identity Federation grants access through short term access tokens, which improves security when compared to LDAP. Access tokens are typically valid for one hour. The time period can usually be customized based on the IdP.

- **Authentication without passwords for application users:** If your applications are running in the cloud, Workload Identity Federation supports authentication without passwords for applications running on [specific cloud resources](https://www.mongodb.com/docs/atlas/workload-oidc/#built-in-authentication). This eliminates periodically renewing credentials.

### MongoDB Atlas and Atlas for Government

For human user access, MongoDB recommends migrating from LDAP to Workforce Identity Federation (OIDC authentication). Workforce Identity Federation allows single sign-on (SSO) access to your Atlas clusters with any IdP that supports OIDC, such as Microsoft Entra ID, Okta, and Ping Identity.

For programmatic users, MongoDB recommends migrating from LDAP to Amazon AWS-IAM authentication or Workload Identity Federation. If your applications are running on AWS resources, you can use AWS-IAM authentication to access your MongoDB Atlas clusters with AWS-IAM roles.

If your applications are running on Microsoft Azure or Google Cloud Platform systems, you can use Workload Identity Federation to access Atlas clusters with Microsoft Azure Managed Identities or Google Cloud Platform Service Accounts. If you cannot use AWS-IAM or Workload Identity Federation, MongoDB recommends using X.509 certificate authentication.

- To get started with Workforce and Workload Identity Federation, see [Authentication and Authorization with OIDC/OAuth 2.0 in Atlas.](https://www.mongodb.com/docs/atlas/security-oidc/)

- To get started with AWS-IAM authentication, see [Set Up Authentication with AWS-IAM.](https://www.mongodb.com/docs/atlas/security/aws-iam-authentication/)

Some of the advantages of Workforce and Workload Identity Federation compared to LDAP in Atlas are:

- **Improved network security:** LDAP requires a public Fully Qualified Domain Name (FQDN), which creates a potential firewall vulnerability. With Workforce Identity Federation, you can use an Internet connected IdP and synchronize part of the user directory to your IdP to improve security with Workforce Identity Federation.

- **Improved credentials handling:** Unlike LDAP, user credentials aren't sent to or stored in MongoDB when using Workforce or Workload Identity Federation.

- **Modern authentication policies for human users:** Workforce Identity Federation allows authentication through IdP, which enables the use of modern authentication policies.

- **Simple configuration:** LDAP users require a complex network configuration for Atlas. Identity Federation has a simpler configuration.

- **Improved security with access tokens:** Workforce and Workload Identity Federation and AWS-IAM authentication grant access through short term access tokens, which improves security when compared to LDAP. Access tokens are typically valid for one hour. The time period can usually be customized based on the IdP.

- **Authentication without passwords for application users:** Workload Identity Federation supports authentication without passwords for applications running on [specific cloud resources](https://www.mongodb.com/docs/atlas/workload-oidc/#built-in-authentication). This eliminates periodically renewing credentials.

- **Cost efficiency:** For Atlas Developer and Pro support, LDAP has a fee as part of the Advanced Security package. Workforce and Workload Identity Federation don't have an additional fee. For pricing, see:

  - [MongoDB Pricing](https://www.mongodb.com/pricing)

  - [MongoDB Atlas Additional Services](https://www.mongodb.com/docs/atlas/billing/additional-services/)

  - [Atlas Support Plans](https://www.mongodb.com/services/support/atlas-support-plans)
