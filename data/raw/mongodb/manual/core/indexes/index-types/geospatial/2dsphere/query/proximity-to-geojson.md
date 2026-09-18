> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Query for Locations Near a Point on a Sphere

You can query for location data that appears near a specified point on a sphere.

To query for location data near a specified point, use the [`$near`](/docs/manual/reference/operator/query/near#mongodb-query-op.-near) operator:

```javascript
db.<collection>.find( {
   <location field> : {
      $near : {
         $geometry : {
            type : "Point",
            coordinates : [ <longitude>, <latitude> ]
         },
         $maxDistance : <distance in meters>
      }
    }
 } )
```

## About this Task

- When you specify longitude and latitude coordinates, list the **longitude** first, and then **latitude**.
  - Valid longitude values are between `-180` and `180`, both inclusive.

  - Valid latitude values are between `-90` and `90`, both inclusive.

- Specify distance in the `$maxDistance` field in **meters**.

## Before You Begin

1. Create a `places` collection that contains these documents:

   ```javascript
   db.places.insertMany( [
      {
         loc: { type: "Point", coordinates: [ -73.97, 40.77 ] },
         name: "Central Park",
         category : "Park"
      },
      {
         loc: { type: "Point", coordinates: [ -73.88, 40.78 ] },
         name: "La Guardia Airport",
         category: "Airport"
      },
      {
         loc: { type: "Point", coordinates: [ -1.83, 51.18 ] },
         name: "Stonehenge",
         category : "Monument"
      }
   ] )
   ```

   The values in the `loc` field are [GeoJSON points.](/docs/manual/reference/geojson#std-label-geojson-point)

2. To query for location data with the `$near` operator, you must create a [geospatial index](/docs/manual/core/indexes/index-types/index-geospatial#std-label-geospatial-index) on the field that contains the location data.

   Create a 2dsphere index on the `loc` field:

   ```javascript
   db.places.createIndex( { "loc": "2dsphere" } )
   ```

## Procedure

Use `$near` to query the collection. The following `$near` query returns documents that have a `loc` field within 5000 meters of a GeoJSON point located at `[ -73.92, 40.78 ]`:

```javascript
db.places.find( {
   loc: {
      $near: {
         $geometry: {
            type: "Point",
            coordinates: [ -73.92, 40.78 ]
         },
         $maxDistance : 5000
      }
   }
} )
```

Output:

```javascript
[
  {
    _id: ObjectId("63f7c3b15e5eefbdfef81cab"),
    loc: { type: 'Point', coordinates: [ -73.88, 40.78 ] },
    name: 'La Guardia Airport',
    category: 'Airport'
  },
  {
    _id: ObjectId("63f7c3b15e5eefbdfef81caa"),
    loc: { type: 'Point', coordinates: [ -73.97, 40.77 ] },
    name: 'Central Park',
    category: 'Park'
  }
]
```

Results are sorted by distance from the queried point, from nearest to farthest.

## Learn More

- [`$near`](/docs/manual/reference/operator/query/near#mongodb-query-op.-near)

- [`$nearSphere`](/docs/manual/reference/operator/query/nearSphere#mongodb-query-op.-nearSphere)

- [`$geoNear`](/docs/manual/reference/operator/aggregation/geoNear#mongodb-pipeline-pipe.-geoNear)

- [`Point`](/docs/manual/reference/geojson#std-label-geojson-point)

- [Geospatial Index Restrictions](/docs/manual/core/indexes/index-types/geospatial/restrictions#std-label-geospatial-restrictions)
