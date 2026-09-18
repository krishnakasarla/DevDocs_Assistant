> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Query for Locations that Intersect a GeoJSON Object

You can query for location data that intersects with a [GeoJSON object](/docs/manual/reference/geojson#std-label-geospatial-indexes-store-geojson). For example, consider an application that stores coordinates of gas stations. You can create a GeoJSON [LineString](/docs/manual/reference/geojson#std-label-geojson-linestring) that represents a road trip, and query for gas stations that intersect with the road trip route.

To query for location data that intersects with a GeoJSON object, use the [`$geoIntersects`](/docs/manual/reference/operator/query/geoIntersects#mongodb-query-op.-geoIntersects) operator:

```javascript
db.<collection>.find( {
   <location field> : {
      $geoIntersects : {
         $geometry : {
            type : "<GeoJSON object type>",
            coordinates : [ <coordinates> ]
         }
       }
    }
 } )
```

## About this Task

- When you specify longitude and latitude coordinates, list the **longitude** first, and then **latitude**.
  - Valid longitude values are between `-180` and `180`, both inclusive.

  - Valid latitude values are between `-90` and `90`, both inclusive.

- A location intersects with an object if it shares at least one point with the specified object. This includes objects that have a shared edge.

- `$geoIntersects` does not require a geospatial index. However, a geospatial index improves query performance. Only the [2dsphere](/docs/manual/core/indexes/index-types/geospatial/2dsphere#std-label-2dsphere-index) geospatial index supports `$geoIntersects`. For more information see [Create a 2dsphere Index.](/docs/manual/core/indexes/index-types/geospatial/2dsphere/create#std-label-create-2dsphere-index)

## Before You Begin

Create a `gasStations` collection that contains these documents:

```javascript
db.gasStations.insertMany( [
   {
      loc: { type: "Point", coordinates: [ -106.31, 35.65 ] },
      state: "New Mexico",
      country: "United States",
      name: "Horizons Gas Station"
   },
   {
      loc: { type: "Point", coordinates: [ -122.62, 40.75 ] },
      state: "California",
      country: "United States",
      name: "Car and Truck Rest Area"
   },
   {
      loc: { type: "Point", coordinates: [ -72.71, 44.15 ] },
      state: "Vermont",
      country: "United States",
      name: "Ready Gas and Snacks"
   }
] )
```

## Procedure

The following `$geoIntersects` query specifies a `LineString` containing four points and returns documents that intersect with the line:

```javascript
db.gasStations.find( {
   loc: {
      $geoIntersects: {
         $geometry: {
            type: "LineString",
            coordinates: [
               [ -105.82, 33.87 ],
               [ -106.01, 34.09 ],
               [ -106.31, 35.65 ],
               [ -107.39, 35.98 ]
            ]
          }
      }
   }
} )
```

Output:

```javascript
[
   {
     _id: ObjectId("63f658d45e5eefbdfef81ca4"),
     loc: { type: 'Point', coordinates: [ -106.31, 35.65 ] },
     state: 'New Mexico',
     country: 'United States',
     name: 'Horizons Gas Station'
   }
]
```

## Learn More

- [`$geoIntersects`](/docs/manual/reference/operator/query/geoIntersects#mongodb-query-op.-geoIntersects)

- [`LineString`](/docs/manual/reference/geojson#std-label-geojson-linestring)

- [Query for Locations Bound by a Polygon](/docs/manual/core/indexes/index-types/geospatial/2dsphere/query/geojson-bound-by-polygon#std-label-2dsphere-query-geojson-objects-polygon)

- [Geospatial Index Restrictions](/docs/manual/core/indexes/index-types/geospatial/restrictions#std-label-geospatial-restrictions)
