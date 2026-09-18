> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Use a View to Join Two Collections

Use [`$lookup`](/docs/manual/reference/operator/aggregation/lookup#mongodb-pipeline-pipe.-lookup) to create a view over two collections. Applications can query the view without constructing or maintaining complex pipelines.

## Example

The examples on this page use data from the [sample\_mflix sample dataset](/docs/manual/sample-data/sample-mflix#std-label-sample-mflix). For details on how to load this dataset into your self-managed MongoDB deployment, see [Load the sample dataset](/docs/manual/sample-data/load-sample-data-local#std-label-sample-dataset-local). If you made any modifications to the sample databases, you may need to drop and recreate the databases to run the examples on this page.

### Create a Joined View

```javascript
db.createView( "movieComments", "movies", [
   { $match: { year: { $gte: 2014 } } },
   {
      $lookup:
         {
            from: "comments",
            localField: "_id",
            foreignField: "movie_id",
            as: "movieComments"
         }
   },
   {
      $project:
         {
            _id: 0,
            title: 1,
            year: 1,
            numComments: { $size: "$movieComments" }
         }
   }
] )

```

In the example:

- The [`$match`](/docs/manual/reference/operator/aggregation/match#mongodb-pipeline-pipe.-match) stage filters the `movies` collection to documents released in 2014 onward.

- The [`$lookup`](/docs/manual/reference/operator/aggregation/lookup#mongodb-pipeline-pipe.-lookup) stage uses the `_id` field in the `movies` collection to join documents in the `comments` collection that have a matching `movie_id` field.

- The matching documents are added as an array in the `movieComments` field.

- The [`$project`](/docs/manual/reference/operator/aggregation/project#mongodb-pipeline-pipe.-project) stage selects a subset of the available fields, including `numComments`, which is the count of comments for each movie.

### Query the View

Query the view for the five movies with the most comments:

```javascript
db.movieComments.aggregate( [
   {
      $group:
         {
            _id: "$title",
            totalComments: { $sum: "$numComments" }
         }
   },
   { $sort: { totalComments: -1 } },
   { $limit: 5 }
] )

```

```javascript
[
  { _id: '<title>', totalComments: <num> },
  { _id: '<title>', totalComments: <num> },
  { _id: '<title>', totalComments: <num> },
  { _id: '<title>', totalComments: <num> },
  { _id: '<title>', totalComments: <num> }
]
```
