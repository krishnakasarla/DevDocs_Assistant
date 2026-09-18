> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Create a Wildcard Index on a Single Field

Wildcard indexes on a single field support queries on any subfield of the indexed field. Use wildcard indexes to support queries on field names that you don't know in advance or vary between documents.

To create a wildcard index on a single field, use the [`db.collection.createIndex()`](/docs/manual/reference/method/db.collection.createIndex#mongodb-method-db.collection.createIndex) method and include the wildcard specifier (`$**`) in the index key:

```javascript
db.collection.createIndex( { "<field>.$**": <sortOrder> } )
```

## About this Task

Only use wildcard indexes when the fields you want to index are unknown or may change. Wildcard indexes don't perform as well as targeted indexes on specific fields. If your collection contains arbitrary field names that prevent targeted indexes, consider remodeling your schema to have consistent field names. To learn more about targeted indexes, see [Create Indexes to Support Your Queries.](/docs/manual/data-modeling/schema-design-process/create-indexes#std-label-create-indexes-to-support-queries)

## Before You Begin

Create a `products` collection that contains the following documents:

```javascript
db.products.insertMany( [
   {
      "product_name" : "Spy Coat",
      "attributes" : {
         "material" : [ "Tweed", "Wool", "Leather" ],
         "size" : {
            "length" : 72,
            "units" : "inches"
         }
      }
   },
   {
      "product_name" : "Spy Pen",
      "attributes" : {
         "colors" : [ "Blue", "Black" ],
         "secret_feature" : {
            "name" : "laser",
            "power" : "1000",
            "units" : "watts",
         }
      }
   }
] )
```

## Procedure

The following operation creates a wildcard index on the `attributes` field:

```javascript
db.products.createIndex( { "attributes.$**" : 1 } )
```

## Results

The wildcard index supports single-field queries on `attributes` or its embedded fields. For example, the index supports the following queries:

- Query:

  ```javascript
  db.products.find( { "attributes.size.length" : { $gt : 60 } } )
  ```

  Output:

  ```javascript
  [
    {
      _id: ObjectId("63472196b1fac2ee2e957ef6"),
      product_name: 'Spy Coat',
      attributes: {
        material: [ 'Tweed', 'Wool', 'Leather' ],
        size: { length: 72, units: 'inches' }
      }
    }
  ]
  ```

- Query:

  ```javascript
  db.products.find( { "attributes.material" : "Leather" } )
  ```

  Output:

  ```javascript
  [
    {
      _id: ObjectId("63472196b1fac2ee2e957ef6"),
      product_name: 'Spy Coat',
      attributes: {
        material: [ 'Tweed', 'Wool', 'Leather' ],
        size: { length: 72, units: 'inches' }
      }
    }
  ]
  ```

- Query:

  ```javascript
  db.products.find(
     { "attributes.secret_feature.name" : "laser" },
     { "_id": 0, "product_name": 1, "attributes.colors": 1 }
  )
  ```

  Output:

  ```javascript
  [
    {
      product_name: 'Spy Pen',
      attributes: { colors: [ 'Blue', 'Black' ] }
    }
  ]
  ```

Wildcard indexes have specific behavior when the indexed field contains an embedded object (for example, `attributes.secret_feature`). For more information, see [Wildcard Indexes on Embedded Objects and Arrays.](/docs/manual/core/indexes/index-types/index-wildcard/reference/embedded-object-behavior#std-label-wildcard-index-embedded-object-behavior)

## Learn More

To learn more about behaviors and use cases for wildcard indexes, see:

- [Create a Wildcard Index on All Fields](/docs/manual/core/indexes/index-types/index-wildcard/create-wildcard-index-all-fields#std-label-create-wildcard-index-all-fields)

- [Include or Exclude Fields in a Wildcard Index](/docs/manual/core/indexes/index-types/index-wildcard/create-wildcard-index-multiple-fields#std-label-create-wildcard-index-multiple-fields)

- [Compound Wildcard Indexes](/docs/manual/core/indexes/index-types/index-wildcard/index-wildcard-compound#std-label-wildcard-index-compound)

- [Wildcard Index Restrictions](/docs/manual/core/indexes/index-types/index-wildcard/reference/restrictions#std-label-wildcard-index-restrictions)
