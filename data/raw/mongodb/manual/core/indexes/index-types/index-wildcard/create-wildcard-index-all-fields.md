> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Create a Wildcard Index on All Fields

You can create a wildcard index that supports queries on all possible document fields. Wildcard indexes support queries on arbitrary or unknown field names.

To create a wildcard index on all fields (excluding `_id`), use the wildcard specifier (`$**`) as the index key:

```javascript
db.<collection>.createIndex( { "$**": <sortOrder> } )
```

## About this Task

Only use wildcard indexes when the fields you want to index are unknown or may change. Wildcard indexes don't perform as well as targeted indexes on specific fields. If your collection contains arbitrary field names that prevent targeted indexes, consider remodeling your schema to have consistent field names. To learn more about targeted indexes, see [Create Indexes to Support Your Queries.](/docs/manual/data-modeling/schema-design-process/create-indexes#std-label-create-indexes-to-support-queries)

## Before You Begin

Create an `artwork` collection that contains the following documents:

```javascript
db.artwork.insertMany( [
   {
      "name": "The Scream",
      "artist": "Edvard Munch",
      "style": "modern",
      "themes": [ "humanity", "horror" ]
   },
   {
      "name": "Acrobats",
      "artist": {
         "name": "Raoul Dufy",
         "nationality": "French",
         "yearBorn": 1877
      },
      "originalTitle": "Les acrobates",
      "dimensions": [ 65, 49 ]
   },
   {
      "name": "The Thinker",
      "type": "sculpture",
      "materials": [ "bronze" ],
      "year": 1904
   }
] )
```

Each document contains details about the artwork. The field names vary between documents depending on the information available about the piece.

## Procedure

The following operation creates a wildcard index on all document fields in the `artwork` collection (excluding `_id`):

```javascript
db.artwork.createIndex( { "$**" : 1 } )
```

## Results

This index supports single-field queries on any field in the collection. If a document contains an embedded document or array, the wildcard index traverses the document or array and stores the value for all fields in the document or array.

For example, the index supports the following queries:

- Query:

  ```javascript
  db.artwork.find( { "style": "modern" } )
  ```

  Output:

  ```javascript
  [
     {
        _id: ObjectId("6352c401b1fac2ee2e957f09"),
        name: 'The Scream',
        artist: 'Edvard Munch',
        style: 'modern',
        themes: [ 'humanity', 'horror' ]
     }
  ]
  ```

- Query:

  ```javascript
  db.artwork.find( { "artist.nationality": "French" } )
  ```

  Output:

  ```javascript
  [
     {
        _id: ObjectId("6352c525b1fac2ee2e957f0d"),
        name: 'Acrobats',
        artist: { name: 'Raoul Dufy', nationality: 'French', yearBorn: 1877 },
        originalTitle: 'Les acrobates',
        dimensions: [ 65, 49 ]
     }
  ]
  ```

- Query:

  ```javascript
  db.artwork.find( { "materials": "bronze" } )
  ```

  Output:

  ```javascript
  [
     {
        _id: ObjectId("6352c387b1fac2ee2e957f08"),
        name: 'The Thinker',
        type: 'sculpture',
        materials: [ 'bronze' ],
        year: 1904
     }
  ]
  ```

## Learn More

To learn how to create a wildcard index that projects specific fields to cover, see the following pages:

- [Filter Fields with a `wildcardProjection`](/docs/manual/core/indexes/index-types/index-wildcard/index-wildcard-compound#std-label-wc-compound-index-wcProject)

- [Include or Exclude Fields in a Wildcard Index](/docs/manual/core/indexes/index-types/index-wildcard/create-wildcard-index-multiple-fields#std-label-create-wildcard-index-multiple-fields)

To learn more about behaviors for wildcard indexes, see:

- [Wildcard Indexes on Embedded Objects and Arrays](/docs/manual/core/indexes/index-types/index-wildcard/reference/embedded-object-behavior#std-label-wildcard-index-embedded-object-behavior)

- [Wildcard Index Restrictions](/docs/manual/core/indexes/index-types/index-wildcard/reference/restrictions#std-label-wildcard-index-restrictions)
