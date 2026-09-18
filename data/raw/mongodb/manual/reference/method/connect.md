> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# connect() (mongosh method)

## Description

Creates a connection to a MongoDB instance and returns the reference to the database. However, in most cases, use the [`Mongo()`](/docs/manual/reference/method/Mongo#mongodb-method-Mongo) object and its [`getDB()`](/docs/manual/reference/method/Mongo.getDB#mongodb-method-Mongo.getDB) method instead.

| Parameter | Type | Description |
| --- | --- | --- |
| `url` | string | Specifies the connection string. You can specify either: `<hostname>:<port>/<database>`; `<hostname>/<database>`; `<database>` |
| `user` | string | Optional. Specifies an existing username with access privileges for this database. If `user` is specified, you must include the `password` parameter as well. |
| `password` | string | Optional unless the `user` parameter is specified. Specifies the password for the `user`. |

## Compatibility

This method is available in deployments hosted in the following environments:

- [MongoDB Atlas](https://www.mongodb.com/docs/atlas): The fully managed service for MongoDB deployments in the cloud

* [MongoDB Enterprise](/docs/manual/administration/install-enterprise#std-label-install-mdb-enterprise): The subscription-based, self-managed version of MongoDB

* [MongoDB Community](/docs/manual/administration/install-community#std-label-install-mdb-community-edition): The source-available, free-to-use, and self-managed version of MongoDB

## Example

The following example instantiates a new connection to the MongoDB instance running on the localhost interface and returns a reference to `myDatabase`:

```javascript
db = connect("localhost:27017/myDatabase")
```

**See also:**

- [`Mongo()`](/docs/manual/reference/method/Mongo#mongodb-method-Mongo)

- [`Mongo.getDB()`](/docs/manual/reference/method/Mongo.getDB#mongodb-method-Mongo.getDB)

- [`db.auth()`](/docs/manual/reference/method/db.auth#mongodb-method-db.auth)
