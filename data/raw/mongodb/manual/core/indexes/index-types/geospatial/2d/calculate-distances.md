> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Convert Distance to Radians for Spherical Operators

2d indexes support certain query operators that calculate distances using spherical geometry. Spherical query operators use radians for distance. To use spherical query operators with a 2d index, you must convert distances to radians.

2d indexes support the following spherical query operators:

- [`$centerSphere`](/docs/manual/reference/operator/query/centerSphere#mongodb-query-op.-centerSphere)

- [`$geoNear`](/docs/manual/reference/operator/aggregation/geoNear#mongodb-pipeline-pipe.-geoNear) pipeline stage with the `spherical: true` option

- [`$near`](/docs/manual/reference/operator/query/near#mongodb-query-op.-near)

- [`$nearSphere`](/docs/manual/reference/operator/query/nearSphere#mongodb-query-op.-nearSphere)

## About this Task

Using a 2d index for queries on spherical data can return incorrect results or an error. For example, 2d indexes don't support spherical queries that wrap around the poles.

If your data is stored as longitude and latitude and you often run queries on spherical surfaces, use a [2dsphere index](/docs/manual/core/indexes/index-types/geospatial/2dsphere#std-label-2dsphere-index) instead of a 2d index.

When you specify longitude and latitude coordinates, list the **longitude** first, and then **latitude**.

- Valid longitude values are between `-180` and `180`, both inclusive.

- Valid latitude values are between `-90` and `90`, both inclusive.

## Procedure

To convert distance to radians, divide the distance by the radius of the sphere (for example, the Earth) in the same units as the distance measurement.

The equatorial radius of Earth is approximately 3,963.2 miles or 6,378.1 kilometers.

## Examples

The following examples use the [`$centerSphere`](/docs/manual/reference/operator/query/centerSphere#mongodb-query-op.-centerSphere) operator to perform queries. The `$centerSphere` operator uses radians to calculate distance.

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

### Convert Miles to Radians

The following query returns documents where the `address` field is within a circle with center point `[ -72, 44 ]` and a radius of 200 miles:

```javascript
db.contacts.find(
   {
      address:
         {
            $geoWithin:
               {
                  $centerSphere:
                     [
                        [ -72, 44 ] ,
                        200 / 3963.2
                     ]
               }
         }
   }
)
```

Output:

```javascript
[
  {
    _id: ObjectId("647e565c6cdaf4dc323ec92d"),
    name: 'Georgine Lestaw',
    phone: '714-555-0107',
    address: [ -74, 44.74 ]
  }
]
```

In the preceding query, to convert 200 miles to radians, the specified miles were divided by 3963.2.

### Convert Kilometers to Radians

The following query returns documents where the `address` field is within a circle with center point `[ 55, 42 ]` and a radius of 500 kilometers:

```javascript
db.contacts.find(
   {
      address:
         {
            $geoWithin:
               {
                  $centerSphere:
                     [
                        [ 55, 42 ] ,
                        500 / 6378.1
                     ]
               }
         }
   }
)
```

Output:

```javascript
[
  {
    _id: ObjectId("647e565c6cdaf4dc323ec92c"),
    name: 'Evander Otylia',
    phone: '202-555-0193',
    address: [ 55.5, 42.3 ]
  }
]
```

In the preceding query, to convert 500 kilometers to radians, the specified kilometers were divided by 6378.1.
