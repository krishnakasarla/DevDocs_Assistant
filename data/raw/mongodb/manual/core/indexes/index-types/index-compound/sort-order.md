> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Compound Index Sort Order

Indexes store entries in either ascending (`1`) or descending (`-1`) order. For [compound indexes](/docs/manual/core/indexes/index-types/index-compound#std-label-index-type-compound), sort order can determine whether the index can support a sort operation. The direction of a field in a compound index is relevant only if there is a sort on multiple fields in opposite directions.

Compound indexes support sort operations that match either the sort order of the index, or the reverse sort order of the index.

For information on sort order and indexes, see [Use Indexes to Sort Query Results.](/docs/manual/tutorial/sort-results-with-indexes#std-label-sorting-with-indexes)

## Use Case

A mobile game has a leaderboard that shows the following information:

- Highest game scores

- The user who achieved each score

- The date each score was achieved

The application sorts the leaderboard first by `score` in descending order. Then, the `username` associated with each `score` is sorted in ascending order (alphabetically).

A compound index can improve performance for the leaderboard if the sort order in the index matches the sort order in the query.

## Example

Consider a `leaderboard` collection with these documents:

```javascript
db.leaderboard.insertMany( [
   {
      "score": 50,
      "username": "Alex Martin",
      "date": ISODate("2022-03-01T00:00:00Z")
   },
   {
      "score": 55,
      "username": "Laura Garcia",
      "date": ISODate("2022-03-02T00:00:00Z")
   },
   {
      "score": 60,
      "username": "Alex Martin",
      "date": ISODate("2022-03-03T00:00:00Z")
   },
   {
      "score": 60,
      "username": "Riya Patel",
      "date": ISODate("2022-03-04T00:00:00Z")
   },
   {
      "score": 50,
      "username": "Laura Garcia",
      "date": ISODate("2022-03-05T00:00:00Z")
   }
] )
```

This query returns leaderboard results:

```javascript
db.leaderboard.find().sort( { score: -1, username: 1 } )
```

Output:

```javascript
[
   {
      _id: ObjectId("632235700646eaee87a56a74"),
      score: 60,
      username: 'Alex Martin',
      date: ISODate("2022-03-03T00:00:00.000Z")
   },
   {
      _id: ObjectId("632235700646eaee87a56a75"),
      score: 60,
      username: 'Riya Patel',
      date: ISODate("2022-03-04T00:00:00.000Z")
   },
   {
      _id: ObjectId("632235700646eaee87a56a73"),
      score: 55,
      username: 'Laura Garcia',
      date: ISODate("2022-03-02T00:00:00.000Z")
   },
   {
      _id: ObjectId("632235700646eaee87a56a72"),
      score: 50,
      username: 'Alex Martin',
      date: ISODate("2022-03-01T00:00:00.000Z")
   },
   {
      _id: ObjectId("632235700646eaee87a56a76"),
      score: 50,
      username: 'Laura Garcia',
      date: ISODate("2022-03-05T00:00:00.000Z")
   }
]
```

The results are sorted first by score in descending order, then by username in ascending order (alphabetically).

### Supporting Index for the Leaderboard

The following index improves performance for the leaderboard results because the sort order of the index matches the sort order used in the query:

```javascript
db.leaderboard.createIndex( { score: -1, username: 1 } )
```

This compound index stores:

- `score` values in descending order.

- `username` values in ascending order (alphabetically).

### Reverse Results

MongoDB can traverse a compound index in either direction. If the application allows users to view the leaderboard in reverse order, the index supports that query as well.

The following query returns the leaderboard in reverse order, where results are sorted first by ascending `score` values and then by descending `username` values (reverse alphabetically):

```javascript
db.leaderboard.find().sort( { score: 1, username: -1 } )
```

Output:

```javascript
[
   {
      _id: ObjectId("632235700646eaee87a56a76"),
      score: 50,
      username: 'Laura Garcia',
      date: ISODate("2022-03-05T00:00:00.000Z")
   },
   {
      _id: ObjectId("632235700646eaee87a56a72"),
      score: 50,
      username: 'Alex Martin',
      date: ISODate("2022-03-01T00:00:00.000Z")
   },
   {
      _id: ObjectId("632235700646eaee87a56a73"),
      score: 55,
      username: 'Laura Garcia',
      date: ISODate("2022-03-02T00:00:00.000Z")
   },
   {
      _id: ObjectId("632235700646eaee87a56a75"),
      score: 60,
      username: 'Riya Patel',
      date: ISODate("2022-03-04T00:00:00.000Z")
   },
   {
      _id: ObjectId("632235700646eaee87a56a74"),
      score: 60,
      username: 'Alex Martin',
      date: ISODate("2022-03-03T00:00:00.000Z")
   }
]
```

The `{ score: -1, username: 1 }` index supports this query.

### Unsupported Queries

Compound indexes cannot support queries where the sort order does not match the index or the reverse of the index. As a result, the `{ score:
-1, username: 1 }` index **cannot** support sorting by ascending `score` values and then by ascending `username` values, such as this query:

```javascript
db.leaderboard.find().sort( { score: 1, username: 1 } )
```

Additionally, for a sort operation to use an index, the fields specified in the sort must appear in the same order that they appear in an index. As a result, the above index cannot support this query:

```javascript
db.leaderboard.find().sort( { username: 1, score: -1, } )
```

## Learn More

- For more information on sort order and indexes, see [Use Indexes to Sort Query Results.](/docs/manual/tutorial/sort-results-with-indexes#std-label-sorting-with-indexes)

- For more information on sorting query results, see [`sort()`.](/docs/manual/reference/method/cursor.sort#mongodb-method-cursor.sort)
