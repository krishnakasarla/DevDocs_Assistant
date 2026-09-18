> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Cursors

A [cursor](/docs/manual/reference/glossary#std-term-cursor) points to the results of a [query](/docs/manual/tutorial/query-documents#std-label-read-operations-queries). Cursors let you iterate over database results one batch at a time.

## Use Cases

The `find()` and `aggregate()` methods return a cursor with a batch of results. Iterate the cursor manually or use [`toArray()`](/docs/manual/reference/method/cursor.toArray#mongodb-method-cursor.toArray) to access documents. For more information, see [Iterate a Cursor in `mongosh`.](/docs/manual/tutorial/iterate-a-cursor#std-label-read-operations-cursors)

For [capped collections](/docs/manual/core/capped-collections#std-label-manual-capped-collection), use a tailable cursor to retrieve documents as they are inserted. For more information, see [Tailable Cursors.](/docs/manual/core/tailable-cursors#std-label-tailable-cursors-landing-page)

## Behavior

MongoDB closes cursors created within a [client session](/docs/manual/core/read-isolation-consistency-recency#std-label-read-isolation-consistency-recency) when:

- The client exhausts the cursor.

- You manually close the cursor.

- You manually terminate the session.

- The [session](/docs/manual/reference/server-sessions#std-label-server-sessions) times out.

[`cursorTimeoutMillis`](/docs/manual/reference/parameters#mongodb-parameter-param.cursorTimeoutMillis) sets the timeout for idle cursors (default: 10 minutes). MongoDB closes idle cursors outside sessions after this time. Returning a batch extends the timeout. Use [`killCursors`](/docs/manual/reference/command/killCursors#mongodb-dbcommand-dbcmd.killCursors) to close cursors manually.

[`localLogicalSessionTimeoutMinutes`](/docs/manual/reference/parameters#mongodb-parameter-param.localLogicalSessionTimeoutMinutes) sets the session timeout (default: 30 minutes). Use [`refreshSessions`](/docs/manual/reference/command/refreshSessions#mongodb-dbcommand-dbcmd.refreshSessions) to extend a session and [`killSessions`](/docs/manual/reference/command/killSessions#mongodb-dbcommand-dbcmd.killSessions) to end it.

Drivers and [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) create implicit sessions for cursors opened outside explicit sessions.

### Concurrent Updates While Using a Cursor

As a cursor returns documents, other operations may run in the background and affect the results, depending on the read concern level. For details, see [Read Isolation, Consistency, and Recency.](/docs/manual/core/read-isolation-consistency-recency#std-label-read-isolation-consistency-recency)

### Cursor Results for Non-Existent `mongos` Databases

Starting in MongoDB 7.2, aggregation pipeline queries that attempt to use non-existent databases on [mongos](/docs/manual/reference/program/mongos#std-program-mongos) deployments return validation errors.

In previous versions, these aggregation queries return empty cursors.

## Get Started

- [Iterate a Cursor in `mongosh`](/docs/manual/tutorial/iterate-a-cursor#std-label-read-operations-cursors)

- [Tailable Cursors](/docs/manual/core/tailable-cursors#std-label-tailable-cursors-landing-page)

- [MongoDB Drivers](https://www.mongodb.com/docs/drivers/)

## Details

[`find`](/docs/manual/reference/command/find#mongodb-dbcommand-dbcmd.find) and [`aggregate`](/docs/manual/reference/command/aggregate#mongodb-dbcommand-dbcmd.aggregate) operations execute until they fill a [batch](/docs/manual/core/cursors#std-label-cursor-batches). The query then pauses. This paused query is a *cursor*, identified by a *cursor ID*.

The database returns the batch and cursor ID. Drivers and `mongosh` store this in a client-side cursor. If more documents exist, the cursor retrieves the next batch via [`getMore`](/docs/manual/reference/command/getMore#mongodb-dbcommand-dbcmd.getMore). Use [`cursor.objsLeftInBatch()`](/docs/manual/reference/method/cursor.objsLeftInBatch#mongodb-method-cursor.objsLeftInBatch) to check remaining batch results and [`cursor.hasNext()`](/docs/manual/reference/method/cursor.hasNext#mongodb-method-cursor.hasNext) to check for more results.

### Cursor Batches

Cursors return results in batches, limited by the 16 MiB [maximum BSON document size](/docs/manual/reference/limits#std-label-limit-bson-document-size). Use [`cursor.batchSize()`](/docs/manual/reference/method/cursor.batchSize#mongodb-method-cursor.batchSize) to set the document limit. `find()` and `aggregate()` default to a batch size of `101`. Subsequent [`getMore`](/docs/manual/reference/command/getMore#mongodb-dbcommand-dbcmd.getMore) operations have no default limit, only the 16 MiB message size.

### Sorting

Queries with a sort operation *without* an index must load all documents into memory before returning results.

### Cursor Information

[`db.serverStatus()`](/docs/manual/reference/method/db.serverStatus#mongodb-method-db.serverStatus) returns cursor metrics in the `metrics.cursor` field. See [`metrics.cursor`.](/docs/manual/reference/command/serverStatus#mongodb-serverstatus-serverstatus.metrics.cursor)

## Learn More

- [MongoDB Drivers](https://www.mongodb.com/docs/drivers/)

- [Cursors](/docs/manual/reference/method#std-label-doc-cursor-methods)
