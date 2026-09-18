> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Connect to a Cluster

Learn how to connect to MongoDB clusters whether they are hosted on MongoDB Atlas or self-managed.

## Connection String Formats

To connect to your deployment, you need a connection string. The connection string format depends on whether you connect to a replica set, sharded cluster, or standalone deployment.

**Replica Set:**

```bash
mongodb+srv://myDatabaseUser:D1fficultP%40ssw0rd@mongodb0.example.com/?authSource=admin&replicaSet=myRepl
```

**Sharded Cluster:**

```bash
mongodb+srv://myDatabaseUser:D1fficultP%40ssw0rd@mongos0.example.com/?authSource=admin
```

**Standalone:**

```bash
mongodb+srv://myDatabaseUser:D1fficultP%40ssw0rd@mongodb0.example.com/?authSource=admin
```

If the username or password includes the following characters, those characters must be converted using [percent encoding:](https://tools.ietf.org/html/rfc3986#section-2.1)

```none
$ : / ? # [ ] @
```

For detailed information about connection string formats and options, see [Connection Strings.](/docs/manual/reference/connection-string#std-label-find-connection-string)

## Get Your Connection String

How you obtain your connection string depends on whether your deployment is hosted on MongoDB Atlas or self-managed.

### MongoDB Atlas Deployments

To connect to a cluster hosted on MongoDB Atlas, see [Connect to an Atlas Cluster](https://www.mongodb.com/docs/atlas/connect-to-database-deployment/#std-label-atlas-connect-to-deployment), which covers how to:

- Get your connection string via the Atlas CLI or Atlas UI.

- Configure your IP access list.

- Create database users.

- Use various connection methods including drivers, Compass, `mongosh`, and more.

### Self-Managed Deployments

Before you connect to a self-managed deployment:

- Ensure your MongoDB deployment is running and accessible.

- Create a database user with the appropriate privileges.

- Verify network connectivity between your client and the MongoDB deployment.

To construct your connection string, use the appropriate [connection string format](/docs/manual/connect-to-cluster#std-label-connection-string-formats) for your deployment topology.

### Connection Methods

After you have your connection string, you can connect using the following methods:

- [Connect to a Deployment Using a MongoDB Client Library](https://www.mongodb.com/docs/ops-manager/current/tutorial/connect-to-mongodb/#std-label-connect-via-driver) - MongoDB drivers for various programming languages

- [Connect to a Cluster via Compass](https://www.mongodb.com/docs/atlas/compass-connection/#std-label-atlas-connect-via-compass) - MongoDB Compass GUI

- [Connect to a Cluster via mongosh](https://www.mongodb.com/docs/atlas/mongo-shell-connection/#std-label-connect-mongo-shell) - `mongosh`

- [Connect to a Cluster via VS Code](https://www.mongodb.com/docs/atlas/mongodb-for-vscode/#std-label-mongodb-for-vscode) - MongoDB for VS Code

- [Connect to a Cluster via the BI Connector](https://www.mongodb.com/docs/atlas/bi-connection/#std-label-bi-connection) - MongoDB BI Connector

- [Command Line Tools](https://www.mongodb.com/docs/atlas/command-line-tools/#std-label-command-line-tools) - mongodump, mongorestore, and other tools

## Learn More

- [Connection String Formats](/docs/manual/reference/connection-string#std-label-find-connection-string)

- [Connection String Options](/docs/manual/reference/connection-string-options#std-label-connections-connection-options)

- [Test Primary Failover](https://www.mongodb.com/docs/atlas/tutorial/test-resilience/test-primary-failover/#std-label-test-failover)

- [Connection Limits and Cluster Tier](https://www.mongodb.com/docs/atlas/reference/atlas-limits/#std-label-connection-limits)
