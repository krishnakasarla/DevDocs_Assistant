> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Create an Index on an Embedded Field in an Array

You can create indexes on embedded document fields within arrays. These indexes improve performance for queries on specific embedded fields that appear in arrays. When you create an index on a field inside an array, MongoDB stores that index as a multikey index.

To create an index, use the [`db.collection.createIndex()`](/docs/manual/reference/method/db.collection.createIndex#mongodb-method-db.collection.createIndex) method. Your operation should resemble this prototype:

```javascript
db.<collection>.createIndex( { <field>: <sortOrder> } )
```

## About this Task

The example on this page uses an `inventory` collection that contains these documents:

```javascript
db.inventory.insertMany( [
   {
      "item": "t-shirt",
      "stock": [
         {
            "size": "small",
            "quantity": 8
         },
         {
            "size": "large",
            "quantity": 10
         },
       ]
   },
   {
      "item": "sweater",
      "stock": [
         {
            "size": "small",
            "quantity": 4
         },
         {
            "size": "large",
            "quantity": 7
         },
       ]
   },
   {
      "item": "vest",
      "stock": [
         {
            "size": "small",
            "quantity": 6
         },
         {
            "size": "large",
            "quantity": 1
         }
       ]
   }
] )
```

You need to order more inventory any time you have less than five of an item in stock. To find which items to reorder, you query for documents where an element in the `stock` array has a `quantity` less than `5`. To improve performance for this query, you can create an index on the `stock.quantity` field.

## Procedure

The following operation creates an ascending multikey index on the `stock.quantity` field of the `inventory` collection:

```javascript
db.inventory.createIndex( { "stock.quantity": 1 } )
```

Because `stock` contains an array value, MongoDB stores this index as a multikey index.

## Results

The index contains a key for each individual value that appears in the `stock.quantity` field. The index is ascending, meaning the keys are stored in this order: `[ 1, 4, 6, 7, 8, 10 ]`.

The index supports queries that select on the `stock.quantity` field. For example, the following query returns documents where at least one element in the `stock` array has a `quantity` less than `5`:

```javascript
db.inventory.find(
   {
      "stock.quantity": { $lt: 5 }
   }
)
```

Output:

```javascript
[
  {
    _id: ObjectId("63449793b1fac2ee2e957ef3"),
    item: 'vest',
    stock: [ { size: 'small', quantity: 6 }, { size: 'large', quantity: 1 } ]
  },
  {
    _id: ObjectId("63449793b1fac2ee2e957ef2"),
    item: 'sweater',
    stock: [ { size: 'small', quantity: 4 }, { size: 'large', quantity: 7 } ]
  }
]
```

### Sort Results

The index also supports sort operations on the `stock.quantity` field, such as this query:

```javascript
db.inventory.find().sort( { "stock.quantity": -1 } )
```

Output:

```javascript
[
  {
    _id: ObjectId("63449793b1fac2ee2e957ef1"),
    item: 't-shirt',
    stock: [ { size: 'small', quantity: 8 }, { size: 'large', quantity: 10 } ]
  },
  {
    _id: ObjectId("63449793b1fac2ee2e957ef2"),
    item: 'sweater',
    stock: [ { size: 'small', quantity: 4 }, { size: 'large', quantity: 7 } ]
  },
  {
    _id: ObjectId("63449793b1fac2ee2e957ef3"),
    item: 'vest',
    stock: [ { size: 'small', quantity: 6 }, { size: 'large', quantity: 1 } ]
  }
]
```

When sorting an array of objects, in a descending sort, MongoDB sorts based on the field with the highest-valued element first.

## Learn More

- [Create a multikey index on an array of scalar values.](/docs/manual/core/indexes/index-types/index-multikey/create-multikey-index-basic#std-label-index-create-multikey-basic)

- [Learn about multikey index bounds.](/docs/manual/core/indexes/index-types/index-multikey/multikey-index-bounds#std-label-indexes-multikey-bounds)
