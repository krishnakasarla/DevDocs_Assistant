> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Set up Automatic Removal for Time Series Collections (TTL)

When you create a [time series collection](/docs/manual/core/timeseries-collections#std-label-manual-timeseries-collection), you can set up automatic removal of documents older than a specified number of seconds by using the `expireAfterSeconds` property:

```csharp
var createCommand = new BsonDocument
{
    { "create", "weather24h" },
    { "timeseries", new BsonDocument
        {
            { "timeField", "timestamp" },
            { "metaField", "sensorId" },
            { "granularity", "seconds" }
        }
    },
    { "expireAfterSeconds", 86400 }
};

// Execute the command to create the collection
await database.RunCommandAsync<BsonDocument>(createCommand);

```

The expiration threshold is the `timeField` field value plus the specified number of seconds. Consider the following document in the `weather24h` collection:

```json
{
  "time": {
    "$date": "2045-11-19T18:00:00Z"
  },
  "sensor": {
    "sensorId": 5578,
    "type": "temperature"
  },
  "temp": 48.2
}

```

The document has a timestamp of `"2021-11-19T18:00:00Z"` and the `expireAfterSeconds` value is set to 86400 seconds (one day), so the document will expire from the database at `"2021-11-20T18:00:00Z"`.

**Note:**

Once all documents in a bucket are expired, the background task that removes expired buckets removes the bucket during the next run. See [Timing of Delete Operations](/docs/manual/core/timeseries/timeseries-automatic-removal#std-label-timeseries-collection-delete-operations-timing) for more information.

## Create or Change Expiration Time

To enable automatic removal of documents on a [time series collection](/docs/manual/core/timeseries-collections#std-label-manual-timeseries-collection) that doesn't have an expiration, or to modify the expiration time on an existing collection, change the `expireAfterSeconds` parameter value, using the [`collMod`](/docs/manual/reference/command/collMod#mongodb-dbcommand-dbcmd.collMod) command:

```csharp
var command = new BsonDocument
{
    { "collMod", "weather24h" },
    { "expireAfterSeconds", 7200 } // Set expiration to 2 hours (7200 seconds)
};

var result = await database.RunCommandAsync<BsonDocument>(command);

```

## Retrieve the Current Value of `expireAfterSeconds`

To retrieve the current value of `expireAfterSeconds`, use the `ListCollectionsAsync` method. The result document contains the `options.expireAfterSeconds` field for the timeseries collection.

```csharp
var collectionInfoCursor = await
    database.ListCollectionsAsync(
        new ListCollectionsOptions { Filter = new BsonDocument("name", "weather24h") });
var collectionInfo = await collectionInfoCursor.FirstOrDefaultAsync();
if (collectionInfo != null)
{
    return collectionInfo["options"]["expireAfterSeconds"];
}

```

**Output:**

```json
{
    "cursor": {
       "id": ...,
       "firstBatch": [
         {
            "name": ...,
            "type": "timeseries",
            "options": {
               "expireAfterSeconds": ...,
               "timeseries": { 
                    ... 
               }
            },
            ...
         },
         ...
       ]
    }
 }
```

## Disable Automatic Removal

To disable automatic removal, use the [`collMod`](/docs/manual/reference/command/collMod#mongodb-dbcommand-dbcmd.collMod) command to set `expireAfterSeconds` to `off`:

```csharp
var command = new BsonDocument
{
    { "collMod", "weather24h" },
    { "expireAfterSeconds", "off" }
};

await database.RunCommandAsync<BsonDocument>(command);

```

When you create a [time series collection](/docs/manual/core/timeseries-collections#std-label-manual-timeseries-collection), you can set up automatic removal of documents older than a specified number of seconds by using the `expireAfterSeconds` property:

```java
Document createCommand = new Document("create", "weather24h")
        .append("timeseries", new Document()
                .append("timeField", "timestamp")
                .append("metaField", "sensorId")
                .append("granularity", "seconds"))
        .append("expireAfterSeconds", 86400);

// Execute the command to create the collection
database.runCommand(createCommand);

```

The expiration threshold is the `timeField` field value plus the specified number of seconds. Consider the following document in the `weather24h` collection:

```json
{
  "time": {
    "$date": "2021-11-19T18:00:00Z"
  },
  "sensor": {
    "sensorId": 5578,
    "type": "temperature"
  },
  "temp": 48.2
}

```

The document has a timestamp of `"2021-11-19T18:00:00Z"` and the `expireAfterSeconds` value is set to 86400 seconds (one day), so the document will expire from the database at `"2021-11-20T18:00:00Z"`.

**Note:**

Once all documents in a bucket are expired, the background task that removes expired buckets removes the bucket during the next run. See [Timing of Delete Operations](/docs/manual/core/timeseries/timeseries-automatic-removal#std-label-timeseries-collection-delete-operations-timing) for more information.

## Create or Change Expiration Time

To enable automatic removal of documents on a [time series collection](/docs/manual/core/timeseries-collections#std-label-manual-timeseries-collection) that doesn't have an expiration, or to modify the expiration time on an existing collection, change the `expireAfterSeconds` parameter value, using the [`collMod`](/docs/manual/reference/command/collMod#mongodb-dbcommand-dbcmd.collMod) command:

```java
Document command = new Document("collMod", "weather24h")
        .append("expireAfterSeconds", 7200); // Set expiration to 2 hours (7200 seconds)

Document result = database.runCommand(command);

```

## Retrieve the Current Value of `expireAfterSeconds`

To retrieve the current value of `expireAfterSeconds`, use the `listCollections` method. The result document contains the `options.expireAfterSeconds` field for the timeseries collection.

```java
Document filter = new Document("name", "weather24h");
Document collectionInfo = database.listCollections().filter(filter).first();
if (collectionInfo != null) {
    Document options = collectionInfo.get("options", Document.class);
    if (options != null) {
        return options.getLong("expireAfterSeconds");
    }
}

```

**Output:**

```json
{
    "cursor": {
       "id": ...,
       "firstBatch": [
         {
            "name": ...,
            "type": "timeseries",
            "options": {
               "expireAfterSeconds": ...,
               "timeseries": {
                    ...
               }
            },
            ...
         },
         ...
       ]
    }
 }

```

## Disable Automatic Removal

To disable automatic removal, use the [`collMod`](/docs/manual/reference/command/collMod#mongodb-dbcommand-dbcmd.collMod) command to set `expireAfterSeconds` to `off`:

```java
Document command = new Document("collMod", "weather24h")
        .append("expireAfterSeconds", "off");

database.runCommand(command);

```

When you create a [time series collection](/docs/manual/core/timeseries-collections#std-label-manual-timeseries-collection), you can set up automatic removal of documents older than a specified number of seconds by using the `expireAfterSeconds` parameter:

```javascript
db.createCollection(
    "weather24h",
    {
       timeseries: {
          timeField: "timestamp",
          metaField: "metadata",
          granularity: "hours"
       },
       expireAfterSeconds: 86400
    }
)
```

The expiration threshold is the `timeField` field value plus the specified number of seconds. Consider the following document in the `weather24h` collection:

```text
{
   "metadata": {"sensorId": 5578, "type": "temperature"},
   "timestamp": ISODate("2021-05-18T10:00:00.000Z"),
   "temp": 12
}
```

The document would expire from the database at `"2021-05-19T10:00:00.000Z"`. Once all documents in a bucket are expired, the background task that removes expired buckets removes the bucket during the next run. See [Timing of Delete Operations](/docs/manual/core/timeseries/timeseries-automatic-removal#std-label-timeseries-collection-delete-operations-timing) for more information.

## Enable Automatic Removal on a Collection

To enable automatic removal of documents for an existing [time series collection](/docs/manual/core/timeseries-collections#std-label-manual-timeseries-collection), issue the following [`collMod`](/docs/manual/reference/command/collMod#mongodb-dbcommand-dbcmd.collMod) command:

```javascript
db.runCommand({
   collMod: "weather24h",
   expireAfterSeconds: 604801
})
```

## Change the `expireAfterSeconds` Parameter

To change the `expireAfterSeconds` parameter value, issue the following [`collMod`](/docs/manual/reference/command/collMod#mongodb-dbcommand-dbcmd.collMod) command:

```javascript
db.runCommand({
   collMod: "weather24h",
   expireAfterSeconds: 604801
})
```

## Retrieve the Current Value of `expireAfterSeconds`

To retrieve the current value of `expireAfterSeconds`, use the [`listCollections`](/docs/manual/reference/command/listCollections#mongodb-dbcommand-dbcmd.listCollections) command:

```javascript
db.runCommand( { listCollections: 1 } )
```

The result document contains a document for the time series collection which contains the `options.expireAfterSeconds` field.

```javascript
{
    cursor: {
       id: <number>,
       ns: 'test.$cmd.listCollections',
       firstBatch: [
         {
            name: <string>,
            type: 'timeseries',
            options: {
               expireAfterSeconds: <number>,
               timeseries: { ... }
            },
            ...
         },
         ...
       ]
    }
 }
```

## Disable Automatic Removal

To disable automatic removal, use the [`collMod`](/docs/manual/reference/command/collMod#mongodb-dbcommand-dbcmd.collMod) command to set `expireAfterSeconds` to `off`:

```javascript
db.runCommand({
    collMod: "weather24h",
    expireAfterSeconds: "off"
})
```

When you create a [time series collection](/docs/manual/core/timeseries-collections#std-label-manual-timeseries-collection), you can set up automatic removal of documents older than a specified number of seconds by using the `expireAfterSeconds` property:

```javascript
const createCommand = {
  create: 'weather24h',
  timeseries: {
    timeField: 'timestamp',
    metaField: 'sensorId',
    granularity: 'seconds',
  },
  expireAfterSeconds: 86400,
};

// Execute the command to create the collection
await database.command(createCommand);

```

The expiration threshold is the `timeField` field value plus the specified number of seconds. Consider the following document in the `weather24h` collection:

```json
{
  "time": {
    "$date": "2021-11-19T18:00:00Z"
  },
  "sensor": {
    "sensorId": 5578,
    "type": "temperature"
  },
  "temp": 48.2
}

```

The document has a timestamp of `"2021-11-19T18:00:00Z"` and the `expireAfterSeconds` value is set to 86400 seconds (one day). The document will expire from the database at `"2021-11-2   0T18:00:00Z"`.

**Note:**

Once all documents in a bucket are expired, the background task that removes expired buckets removes the bucket during the next run. See [Timing of Delete Operations](/docs/manual/core/timeseries/timeseries-automatic-removal#std-label-timeseries-collection-delete-operations-timing) for more information.

## Create or Change Expiration Time

To enable automatic removal of documents on a [time series collection](/docs/manual/core/timeseries-collections#std-label-manual-timeseries-collection) that doesn't have an expiration, or to modify the expiration time on an existing collection, change the `expireAfterSeconds` parameter value, using the [`collMod`](/docs/manual/reference/command/collMod#mongodb-dbcommand-dbcmd.collMod) command:

```javascript
const command = {
  collMod: 'weather24h',
  expireAfterSeconds: 7200, // Set expiration to 2 hours (7200 seconds)
};

const result = await database.command(command);

```

## Retrieve the Current Value of `expireAfterSeconds`

To retrieve the current value of `expireAfterSeconds`, use the `ListCollectionsAsync` method. The result document contains the `options.expireAfterSeconds` field for the timeseries collection.

```javascript
const collections = await database
  .listCollections({ name: 'weather24h' })
  .toArray();
if (collections.length > 0) {
  const collectionInfo = collections[0];
  return collectionInfo.options?.expireAfterSeconds;
}

```

**Output:**

```json
{
    "cursor": {
       "id": ...,
       "firstBatch": [
         {
            "name": ...,
            "type": "timeseries",
            "options": {
               "expireAfterSeconds": ...,
               "timeseries": { 
                    ... 
               }
            },
            ...
         },
         ...
       ]
    }
 }
```

## Disable Automatic Removal

To disable automatic removal, use the [`collMod`](/docs/manual/reference/command/collMod#mongodb-dbcommand-dbcmd.collMod) command to set `expireAfterSeconds` to `off`:

```javascript
const command = {
  collMod: 'weather24h',
  expireAfterSeconds: 'off',
};

await database.command(command);

```

When you create a [time series collection](/docs/manual/core/timeseries-collections#std-label-manual-timeseries-collection), you can set up automatic removal of documents older than a specified number of seconds by using the `expireAfterSeconds` property:

```python
create_command = {
    "create": "weather24h",
    "timeseries": {
        "timeField": "timestamp",
        "metaField": "sensorId",
        "granularity": "seconds"
    },
    "expireAfterSeconds": 86400
}

# Execute the command to create the collection
database.command(create_command)

```

The expiration threshold is the `timeField` field value plus the specified number of seconds. Consider the following document in the `weather24h` collection:

```json
{
  "time": {
    "$date": "2021-11-19T18:00:00Z"
  },
  "sensor": {
    "sensorId": 5578,
    "type": "temperature"
  },
  "temp": 48.2
}

```

The document has a timestamp of `"2021-11-19T18:00:00Z"` and the `expireAfterSeconds` value is set to 86400 seconds (one day). The document will expire from the database at `"2021-11-20T18:00:00Z"`.

**Note:**

Once all documents in a bucket are expired, the background task that removes expired buckets removes the bucket during the next run. See [Timing of Delete Operations](/docs/manual/core/timeseries/timeseries-automatic-removal#std-label-timeseries-collection-delete-operations-timing) for more information.

## Create or Change Expiration Time

To enable automatic removal of documents on a [time series collection](/docs/manual/core/timeseries-collections#std-label-manual-timeseries-collection) that doesn't have an expiration, or to modify the expiration time on an existing collection, change the `expireAfterSeconds` parameter value, using the [`collMod`](/docs/manual/reference/command/collMod#mongodb-dbcommand-dbcmd.collMod) command:

```python
command = {
    "collMod": "weather24h",
    "expireAfterSeconds": 7200  # Set expiration to 2 hours (7200 seconds)
}

result = database.command(command)

```

## Retrieve the Current Value of `expireAfterSeconds`

To retrieve the current value of `expireAfterSeconds`, use the `list_collections` method. The result document contains the `options.expireAfterSeconds` field for the timeseries collection.

```python
collections = list(database.list_collections(filter={"name": "weather24h"}))
if collections:
    collection_info = collections[0]
    options = collection_info.get("options", {})
    return options.get("expireAfterSeconds")

```

**Output:**

```json
{
    "cursor": {
       "id": ...,
       "firstBatch": [
         {
            "name": ...,
            "type": "timeseries",
            "options": {
               "expireAfterSeconds": ...,
               "timeseries": { 
                    ... 
               }
            },
            ...
         },
         ...
       ]
    }
 }
```

## Disable Automatic Removal

To disable automatic removal, use the [`collMod`](/docs/manual/reference/command/collMod#mongodb-dbcommand-dbcmd.collMod) command to set `expireAfterSeconds` to `off`:

```python
command = {
    "collMod": "weather24h",
    "expireAfterSeconds": "off"
}

database.command(command)

```

## Behavior

### Timing of Delete Operations

MongoDB doesn't guarantee that expired data will be deleted immediately upon expiration. Once all documents in a bucket are expired, the background task that removes expired buckets removes the bucket during the next run. The maximum span of time that a single bucket is allowed to cover is controlled by the `granularity` of the time series collection:

| `granularity` | Covered Time Span |
| --- | --- |
| `"seconds"` (default) | one hour |
| `"minutes"` | 24 hours |
| `"hours"` | 30 days |

The background task that removes expired buckets runs every 60 seconds. Therefore, documents may remain in a collection during the period between the expiration of the document, the expiration of all other documents in the bucket and the running of the background task.

Because the duration of the removal operation depends on the workload of your mongod instance, expired data may exist for some time beyond the 60 second period between runs of the background task.
