> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Query for Locations within a Circle on a Sphere

You can query for location data within a circle on the surface of a sphere. Use these queries to return data within a [spherical cap.](https://en.wikipedia.org/w/index.php?title=Spherical_cap\&oldid=1107980309)

To query for location data within a circle on a sphere, use [`$geoWithin`](/docs/manual/reference/operator/query/geoWithin#mongodb-query-op.-geoWithin) with the [`$centerSphere`](/docs/manual/reference/operator/query/centerSphere#mongodb-query-op.-centerSphere) operator. In the `$centerSphere` operator, specify the coordinates and radius of the circle to query within:

```javascript
db.<collection>.find( {
   <location field> : {
      $geoWithin : {
         $centerSphere: [
            [ <longitude>, <latitude> ],
            <radius>
         ]
       }
    }
 } )
```

## About this Task

- When you specify longitude and latitude coordinates, list the **longitude** first, and then **latitude**.
  - Valid longitude values are between `-180` and `180`, both inclusive.

  - Valid latitude values are between `-90` and `90`, both inclusive.

- In the `$centerSphere` operator, specify the circle's radius in **radians**. To convert other units to and from radians, see [Convert Distance to Radians for Spherical Operators.](/docs/manual/core/indexes/index-types/geospatial/2d/calculate-distances#std-label-calculate-distance-spherical-geometry)

  - This example calculates distance in kilometers. To convert kilometers to radians, divide the kilometer value by `6378.1`.

- `$geoWithin` does not require a geospatial index. However, a geospatial index improves query performance. Only the [2dsphere](/docs/manual/core/indexes/index-types/geospatial/2dsphere#std-label-2dsphere-index) geospatial index supports `$geoWithin`. For more information see [Create a 2dsphere Index.](/docs/manual/core/indexes/index-types/geospatial/2dsphere/create#std-label-create-2dsphere-index)

## Before You Begin

Create a `places` collection that contains these documents:

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

## Procedure

To query the collection, use `$geoWithin` with the `$centerSphere` operator:

```javascript
db.places.find( {
   loc: {
      $geoWithin: {
         $centerSphere: [
            [ -1.76, 51.16 ],
            10 / 6378.1
         ]
      }
   }
} )
```

The query returns documents where the `loc` field is within a 10 kilometer radius of a point at longitude `-1.76`, latitude `51.16`.

Output:

```javascript
[
   {
     _id: ObjectId("63fd205e4a08b5e248c03e32"),
     loc: { type: 'Point', coordinates: [ -1.83, 51.18 ] },
     name: 'Stonehenge',
     category: 'Monument'
   }
]
```

## Learn More

- [`$geoWithin`](/docs/manual/reference/operator/query/geoWithin#mongodb-query-op.-geoWithin)

- [`$centerSphere`](/docs/manual/reference/operator/query/centerSphere#mongodb-query-op.-centerSphere)

- [Query for Locations Bound by a Polygon](/docs/manual/core/indexes/index-types/geospatial/2dsphere/query/geojson-bound-by-polygon#std-label-2dsphere-query-geojson-objects-polygon)

- [Query for Locations that Intersect a GeoJSON Object](/docs/manual/core/indexes/index-types/geospatial/2dsphere/query/intersections-of-geojson-objects#std-label-2dsphere-query-intersection)

- [Query for Locations Near a Point on a Sphere](/docs/manual/core/indexes/index-types/geospatial/2dsphere/query/proximity-to-geojson#std-label-2dsphere-query-geojson-proximity)

- [Geospatial Index Restrictions](/docs/manual/core/indexes/index-types/geospatial/restrictions#std-label-geospatial-restrictions)
