> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Tailable Cursors

By default, MongoDB automatically closes a cursor when the client exhausts all results in the cursor. However, for [capped collections](/docs/manual/core/capped-collections#std-label-manual-capped-collection) you can use a [tailable cursor](/docs/manual/reference/glossary#std-term-tailable-cursor) that remains open after the client exhausts the results in the initial cursor. Tailable cursors are conceptually equivalent to the `tail` Unix command with the `-f` option ("follow" mode). After clients insert additional documents into a capped collection, the tailable cursor continues to retrieve documents.

## Use Cases

Use tailable cursors on capped collections that have high write volumes where indexes aren't practical. For instance, MongoDB [replication](/docs/manual/replication#std-label-replication) uses tailable cursors to tail the primary's [oplog.](/docs/manual/reference/glossary#std-term-oplog)

**Note:**

If your query is on an indexed field, use a regular cursor instead of a tailable cursor. Keep track of the last value of the indexed field returned by the query. To retrieve the newly added documents, query the collection again using the last value of the indexed field in the query criteria. For example:

```javascript
db.<collection>.find( { indexedField: { $gt: <lastvalue> } } )
```

## Get Started

To create a tailable cursor in [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh), see [`cursor.tailable()`.](/docs/manual/reference/method/cursor.tailable#mongodb-method-cursor.tailable)

To see tailable cursor methods for your driver, see your [driver documentation.](https://www.mongodb.com/docs/drivers/)

## Behavior

Consider the following behaviors related to tailable cursors:

- Tailable cursors do not use indexes. They return documents in [natural order.](/docs/manual/reference/glossary#std-term-natural-order)

- Because tailable cursors do not use indexes, the initial scan for the query may be expensive. After initially exhausting the cursor, subsequent retrievals of the newly added documents are inexpensive.

- A tailable cursor can become invalid if the data at its current position is overwritten by new data. For example, this can happen if the speed of data insertion is faster than the speed of cursor iteration.

- By default, `mongosh` prints a warning when you use a blocking call on a tailable cursor, such as `.next()` or `.hasNext()`. To silence these warnings, use [`cursor.disableBlockWarnings()`.](/docs/manual/reference/method/cursor.disableBlockWarnings#mongodb-method-cursor.disableBlockWarnings)
