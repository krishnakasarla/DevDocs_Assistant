> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Define Location Precision for a 2d Index

In a 2d index, location precision is defined by the size in bits of the [geohash](/docs/manual/reference/glossary#std-term-geohash) values used to store the indexed data. By default, 2d indexes use 26 bits of precision, which is equivalent to approximately two feet (60 centimeters).

Location precision affects performance for insert and read operations.

To change the default precision, specify a `bits` value when you create the 2d index. You can specify a `bits` value between 1 and 32, inclusive.

```javascript
db.<collection>.createIndex(
   { <location field>: "2d" },
   { bits: <bit precision> }
)
```

## About this Task

Location precision affects query performance:

- Lower precision improves performance for insert and update operations, and uses less storage.

- Higher precision improves performance for read operations because queries scan smaller portions of the index to return results.

Location precision does not affect query accuracy. Grid coordinates are always used in the final query processing.

## Before You Begin

Create the `contacts` collection:

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

## Procedure

Create a 2d index on the `address` field. Specify a location precision of `32` bits:

```javascript
db.contacts.createIndex(
   { address: "2d" },
   { bits: 32 }
)
```

## Next Steps

You can use the 2d index to perform calculations on location data, such as [proximity queries.](/docs/manual/core/indexes/index-types/geospatial/2d/query/proximity-flat-surface#std-label-2d-index-proximity-query)

## Learn More

- [Geohash Values](/docs/manual/core/indexes/index-types/geospatial/2d/internals#std-label-geospatial-indexes-geohash)

- [Geospatial Models](/docs/manual/geospatial-queries#std-label-geospatial-geometry)

- [Legacy Coordinate Pairs](/docs/manual/geospatial-queries#std-label-geospatial-legacy)
