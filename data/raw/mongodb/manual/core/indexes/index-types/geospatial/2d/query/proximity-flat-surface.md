> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Query for Locations Near a Point on a Flat Surface

You can query for location data that appears near a specified point on a flat surface.

To query for location data near a specified point, use the [`$near`](/docs/manual/reference/operator/query/near#mongodb-query-op.-near) operator:

```javascript
db.<collection>.find( {
   <location field> : {
      $near : [ <longitude>, <latitude> ],
      $maxDistance : <distance in meters>
   }
} )
```

## About this Task

- When specifying coordinate pairs in the `$near` operator, list the **longitude** first, and then **latitude**.

  - Valid longitude values are between `-180` and `180`, both inclusive.

  - Valid latitude values are between `-90` and `90`, both inclusive.

- Specify distance in the `$maxDistance` field in **meters**.

## Before you Begin

1. Create the `contacts` collection:
   ```javascript
   db.contacts.insertMany( [
      {
         name: "Evander Otylia",
         phone: "202-555-0193",
         address: [ 55.5, 42.3 ]
      },
      {
         name: "Georgine Lestaw",
         phone: "714-555-0107",
         address: [ -74, 44.74 ]
      }
   ] )
   ```
   The `address` field contains [legacy coordinate pairs.](/docs/manual/geospatial-queries#std-label-geospatial-legacy)

2. To query for location data with the `$near` operator, you must create a [geospatial index](/docs/manual/core/indexes/index-types/index-geospatial#std-label-geospatial-index) on the field that contains the location data.

   Create a 2d index on the `address` field:

   ```javascript
   db.contacts.createIndex( { address: "2d" } )
   ```

## Procedure

Use `$near` to query the collection. The following `$near` query returns documents that have an `address` field within 50 meters of the coordinate pair `[ -73.92, 40.78 ]`:

```javascript
db.contacts.find( {
   address: {
      $near: [ -73.92, 40.78 ],
      $maxDistance : 50
   }
} )
```

Output:

```javascript
[
   {
     _id: ObjectId("640a3dd9c639b6f094b00e89"),
     name: 'Georgine Lestaw',
     phone: '714-555-0107',
     address: [ -74, 44.74 ]
   }
]
```

Results are sorted by distance from the queried point, from nearest to farthest.

## Learn More

- [`$near`](/docs/manual/reference/operator/query/near#mongodb-query-op.-near)

- [`$geoNear`](/docs/manual/reference/operator/aggregation/geoNear#mongodb-pipeline-pipe.-geoNear)

- [Geospatial Index Restrictions](/docs/manual/core/indexes/index-types/geospatial/restrictions#std-label-geospatial-restrictions)

- To perform proximity queries on a spherical surface, see [Query for Locations Near a Point on a Sphere.](/docs/manual/core/indexes/index-types/geospatial/2dsphere/query/proximity-to-geojson#std-label-2dsphere-query-geojson-proximity)
