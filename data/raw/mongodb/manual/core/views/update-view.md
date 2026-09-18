> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Modify or Remove a View

To remove a view, use the [`db.collection.drop()`](/docs/manual/reference/method/db.collection.drop#mongodb-method-db.collection.drop) method on the view.

To modify a view, you can either:

- Drop and recreate the view.

- Use the [`collMod`](/docs/manual/reference/command/collMod#mongodb-dbcommand-dbcmd.collMod) command.

## Example

Consider the following view named `lowStock`:

```javascript
db.createView(
   "lowStock",
   "products",
   [ { $match: { quantity: { $lte: 20 } } } ]
)
```

### Drop and Recreate the View

The following commands modify `lowStock` by dropping and recreating the view:

```javascript
db.lowStock.drop()

db.createView(
   "lowStock",
   "products",
   [ { $match: { quantity: { $lte: 10 } } } ]
)
```

### Use the `collMod` Command

Alternatively, you can use the `collMod` command to modify the view:

```javascript
db.runCommand( {
   collMod: "lowStock",
   viewOn: "products",
   "pipeline": [ { $match: { quantity: { $lte: 10 } } } ]
} )
```
