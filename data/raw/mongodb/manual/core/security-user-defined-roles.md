> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# User-Defined Roles on Self-Managed Deployments

MongoDB provides a number of [built-in roles](/docs/manual/reference/built-in-roles). However, if these roles cannot describe the desired set of privileges, you can create new roles.

**Note:**

You can configure custom database roles in the UI for deployments hosted in MongoDB Atlas. To learn more, see [Configure Custom Database Roles.](https://www.mongodb.com/docs/atlas/security-add-mongodb-roles/)

## Role Management Interface

To add a role, MongoDB provides the [`db.createRole()`](/docs/manual/reference/method/db.createRole#mongodb-method-db.createRole) method. MongoDB also provides methods to update existing user-defined roles. For a full list of role management methods, see [Role Management.](/docs/manual/reference/method#std-label-role-management-methods)

## Scope

When adding a role, you create the role in a specific database. MongoDB uses the combination of the database and the role name to uniquely define a role.

Except for roles created in the `admin` database, a role can only include privileges that apply to its database and can only inherit from other roles in its database.

A role created in the `admin` database can include privileges that apply to the `admin` database, other databases or to the [cluster](/docs/manual/reference/resource-document#std-label-resource-cluster) resource, and can inherit from roles in other databases as well as the `admin` database.

## Centralized Role Data

MongoDB stores all role information in the [system.roles](/docs/manual/reference/system-roles-collection) collection in the `admin` database

Do not access this collection directly but instead use the [role management commands](/docs/manual/reference/command#std-label-role-management-commands) to view and edit custom roles.
