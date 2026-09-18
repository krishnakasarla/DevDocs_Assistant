> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# List Time Series Collections in a Database

You can output a list of collections in a database and filter the results by a variety of properties, including collection type. You can use this functionality to list all time series collections in a database.

## Procedure

To list all time series collections in a database, use the [`listCollections`](/docs/manual/reference/command/listCollections#mongodb-dbcommand-dbcmd.listCollections) command with a filter for `{ type: "timeseries" }`:

```javascript
db.runCommand( {
   listCollections: 1,
   filter: { type: "timeseries" }
} )
```

## Output

For time series collections, the output includes:

- `type: 'timeseries'`

- `options: { timeseries: { ... } }`

For example:

```javascript
{
  cursor: {
    id: Long("0"),
    ns: 'test.$cmd.listCollections',
    firstBatch: [
      {
        name: 'weather',
        type: 'timeseries',
        options: {
          timeseries: {
            timeField: 'timestamp',
            metaField: 'metadata',
            granularity: 'hours',
            bucketMaxSpanSeconds: 2592000
          }
        },
        info: { readOnly: false }
      }
    ]
  },
  ok: 1
}
```
