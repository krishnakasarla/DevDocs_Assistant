> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Build Materialized Views on Top of Time Series Data

Materialized views on time series data are useful for:

- archiving

- analytics

- facilitating data access for teams that cannot access the raw data

To create an [On-Demand Materialized view](/docs/manual/core/materialized-views), use the [`$merge`](/docs/manual/reference/operator/aggregation/merge#mongodb-pipeline-pipe.-merge) aggregation pipeline stage to transform and store your data:

```javascript
db.weather.aggregate([
  {
     $project: {
        date: {
           $dateToParts: { date: "$timestamp" }
        },
        temp: 1
     }
  },
  {
     $group: {
        _id: {
           date: {
              year: "$date.year",
              month: "$date.month",
              day: "$date.day"
           }
        },
        avgTmp: { $avg: "$temp" }
     }
  }, {
     $merge: { into: "dailytemperatureaverages", whenMatched: "replace" }
  }
])
```

The preceding pipeline, will create or update the `dailytemperatureaverages` collection with all daily temperature averages based on the `weather` collection.

**Note:**

It is not possible to natively schedule the refreshing of these materialized views.

For more information on materialized views, see [On-Demand Materialized Views.](/docs/manual/core/materialized-views)
