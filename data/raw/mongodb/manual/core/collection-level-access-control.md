> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Collection-Level Access Control in Self-Managed Deployments

Collection-level access control allows administrators to grant users privileges that are scoped to specific collections.

Administrators can implement collection-level access control through [user-defined roles](/docs/manual/core/security-user-defined-roles#std-label-user-defined-roles). By creating a role with [privileges](/docs/manual/core/authorization#std-label-privileges) that are scoped to a specific collection in a particular database, administrators can provision users with roles that grant privileges on a collection level.

## Privileges and Scope

A privilege consists of [actions](/docs/manual/reference/privilege-actions#std-label-security-user-actions) and the [resources](/docs/manual/reference/resource-document#std-label-resource-document) upon which the actions are permissible; i.e. the resources define the scope of the actions for that privilege.

By specifying both the database and the collection in the [resource document](/docs/manual/reference/resource-document#std-label-resource-specific-db-collection) for a privilege, administrator can limit the privilege actions just to a specific collection in a specific database. Each privilege action in a role can be scoped to a different collection.

For example, a user defined role can contain the following privileges:

```javascript
privileges: [
  { resource: { db: "products", collection: "inventory" }, actions: [ "find", "update", "insert" ] },
  { resource: { db: "products", collection: "orders" },  actions: [ "find" ] }
]
```

The first privilege scopes its actions to the `inventory` collection of the `products` database. The second privilege scopes its actions to the `orders` collection of the `products` database.

As a best practice, avoid assigning `createCollection` privileges to users who don't have read privileges on the collection.

## Additional Information

For more information on user-defined roles and MongoDB authorization model, see [Role-Based Access Control in Self-Managed Deployments](/docs/manual/core/authorization). For a tutorial on creating user-defined roles, see [Manage Users and Roles on Self-Managed Deployments.](/docs/manual/tutorial/manage-users-and-roles)
