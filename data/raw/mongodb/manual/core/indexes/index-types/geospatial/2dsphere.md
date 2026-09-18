> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# 2dsphere Indexes

2dsphere indexes support geospatial queries on an earth-like sphere. For example, 2dsphere indexes can:

- Determine points within a specified area.

- Calculate proximity to a specified point.

- Return exact matches on coordinate queries.

The values of the indexed field must be either:

- [GeoJSON objects](/docs/manual/geospatial-queries#std-label-geospatial-geojson)

- [Legacy coordinate pairs](/docs/manual/geospatial-queries#std-label-geospatial-legacy)

  For legacy coordinate pairs, the 2dsphere index converts the data to [GeoJSON points.](/docs/manual/reference/geojson#std-label-geojson-point)

To create a 2dsphere index, specify the string `2dsphere` as the index type:

```javascript
db.<collection>.createIndex( { <location field> : "2dsphere" } )
```

**Note:**

When [creating a a 2dsphere index](/docs/manual/core/indexes/index-types/geospatial/2dsphere/create#std-label-2dsphere-index-create), the first value, or longitude, must be between -180 and 180, inclusive. The second value, or latitude, must be between -90 and 90, inclusive. These coordinates "wrap" around the sphere. For example, -179.9 and +179.9 are near neighbors.

## Use Cases

Use 2dsphere indexes to query and perform calculations on location data where the data points appear on Earth, or another spherical surface. For example:

- A food delivery application uses 2dsphere indexes to support searches for nearby restaurants.

- A route planning application uses 2dsphere indexes to calculate the shortest distance between rest stops.

- A city planner uses 2dsphere indexes to find parks that exist within city limits.

## Get Started

To learn how to create and query 2dsphere indexes, see:

- [Create a 2dsphere Index](/docs/manual/core/indexes/index-types/geospatial/2dsphere/create#std-label-2dsphere-index-create)

- [Query for Locations Bound by a Polygon](/docs/manual/core/indexes/index-types/geospatial/2dsphere/query/geojson-bound-by-polygon#std-label-2dsphere-query-geojson-objects-polygon)

- [Query for Locations Near a Point on a Sphere](/docs/manual/core/indexes/index-types/geospatial/2dsphere/query/proximity-to-geojson#std-label-2dsphere-query-geojson-proximity)

- [Query for Locations that Intersect a GeoJSON Object](/docs/manual/core/indexes/index-types/geospatial/2dsphere/query/intersections-of-geojson-objects#std-label-2dsphere-query-intersection)

- [Query for Locations within a Circle on a Sphere](/docs/manual/core/indexes/index-types/geospatial/2dsphere/query/points-within-circle-on-sphere#std-label-2dsphere-query-points-within-circle-on-sphere)

## Details

2dsphere indexes are always [sparse](/docs/manual/core/index-sparse#std-label-index-type-sparse) and have special behaviors when created as part of a [compound index.](/docs/manual/core/indexes/index-types/index-compound#std-label-index-type-compound)

### `sparse` Property

2dsphere indexes are always [sparse](/docs/manual/core/index-sparse#std-label-index-type-sparse). When you create a 2dsphere index, MongoDB ignores the `sparse` option.

If an existing or newly inserted document does not contain a 2dsphere index field (or the field is `null` or an empty array), MongoDB does not add an entry for the document to the index.

### Compound 2dsphere Indexes

- For a compound index that includes a 2dsphere index key along with keys of other types, only the 2dsphere index field determines whether the index references a document.

- A compound 2dsphere index can reference multiple location and non-location fields. In contrast, a compound [2d](/docs/manual/core/indexes/index-types/geospatial/2d#std-label-2d-index) index can only reference one location field and one other field.

### 2dsphereIndexVersion

Starting in MongoDB 8.3, [2dsphereIndexVersion](/docs/manual/core/indexes/index-types/geospatial/2dsphere/2dsphere-index-versions#std-label-2dsphere-index-versions) is set to version `4` by default.

If you need to downgrade the [FCV](/docs/manual/reference/command/setFeatureCompatibilityVersion#std-label-view-fcv) to anything below 8.3, you must first drop the `2dsphere` version `4` indexes.

## Learn More

- [Geospatial Queries](/docs/manual/geospatial-queries)

- [Geospatial Query Predicate Operators](/docs/manual/reference/mql/query-predicates/geospatial#std-label-geospatial-query-operators)

- [Find Restaurants with Geospatial Queries](/docs/manual/tutorial/geospatial-tutorial#std-label-geospatial-tutorial-restaurants)

- [Geospatial Index Restrictions](/docs/manual/core/indexes/index-types/geospatial/restrictions#std-label-geospatial-restrictions)
