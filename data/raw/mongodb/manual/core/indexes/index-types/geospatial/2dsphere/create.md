> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Create a 2dsphere Index

2dsphere indexes support geospatial queries on an earth-like sphere. For example, 2dsphere indexes can:

- Determine points within a specified area.

- Calculate proximity to a specified point.

- Return exact matches on coordinate queries.

To create a 2dsphere index, use the [`db.collection.createIndex()`](/docs/manual/reference/method/db.collection.createIndex#mongodb-method-db.collection.createIndex) method and specify the string `"2dsphere"` as the index type:

```javascript
db.<collection>.createIndex( { <location field> : "2dsphere" } )
```

The values in the `<location field>` must be either:

- [GeoJSON objects](/docs/manual/geospatial-queries#std-label-geospatial-geojson)

- [Legacy coordinate pairs](/docs/manual/geospatial-queries#std-label-geospatial-legacy)

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

The values in the `loc` field are [GeoJSON points.](/docs/manual/reference/geojson#std-label-geojson-point)

## Procedure

The following operation creates a 2dsphere index on the location field `loc`:

```javascript
db.places.createIndex( { loc : "2dsphere" } )
```

## Next Steps

After you create a 2dsphere index, you can use the index for geospatial queries. To learn more, see [Query a 2dsphere Index.](/docs/manual/core/indexes/index-types/geospatial/2dsphere/query#std-label-2dsphere-index-query)

## Learn More

- [2dsphere Indexes](/docs/manual/core/indexes/index-types/geospatial/2dsphere#std-label-2dsphere-index)

- [Geospatial Queries](/docs/manual/geospatial-queries)

- [Geospatial Index Restrictions](/docs/manual/core/indexes/index-types/geospatial/restrictions#std-label-geospatial-restrictions)
