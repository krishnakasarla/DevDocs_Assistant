> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Text Index Restrictions on Self-Managed Deployments

**Note:**

MongoDB offers an improved full-text search solution, [MongoDB Search](https://www.mongodb.com/docs/atlas/atlas-search/), and vector search solution, [MongoDB Vector Search](https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-overview/). We recommend using [MongoDB Search indexes](https://www.mongodb.com/docs/search/indexes/manage-indexes/#std-label-fts-manage-indexes) or [MongoDB Vector Search indexes](https://www.mongodb.com/docs/vector-search/indexes/vector-search-type/#std-label-avs-types-vector-search)  instead of text indexes.

Text indexes have these restrictions:

## One Text Index per Collection

A collection can have at most one text index.

MongoDB Search (available in [MongoDB](https://www.mongodb.com/atlas/database)) supports multiple full-text search indexes on a single collection. To learn more, see the [MongoDB Search documentation.](https://www.mongodb.com/docs/atlas/atlas-search/)

## $text Queries and Hints

If a query includes a `$text` expression, you cannot use [`hint()`](/docs/manual/reference/method/cursor.hint#mongodb-method-cursor.hint) to specify which index to use for the query.

## $text Queries and Multi-Word Strings

If the `$search` string of a `$text` operation includes a multi-word string and individual terms, `$text` only matches the documents that include the multi-word string.

For examples of `$text` queries with multi-word strings, see [Exact Strings.](/docs/manual/reference/operator/query/text#std-label-text-operator-exact-string)

## Text Index and Sort

Text indexes cannot improve performance for sort operations. This restriction applies to both single-field and compound text indexes.

## Compound Text Index

A [compound index](/docs/manual/core/indexes/index-types/index-compound#std-label-index-type-compound) can include a text index key in combination with ascending and descending index keys. However, compound text indexes have these restrictions:

- A compound text index cannot include any other special index types, such as [multikey](/docs/manual/core/indexes/index-types/index-multikey#std-label-index-type-multi-key) or [geospatial](/docs/manual/core/indexes/index-types/index-geospatial#std-label-geospatial-index) index fields.

- If the compound text index includes keys **preceding** the text index key, to use [`$text`](/docs/manual/reference/operator/query/text#mongodb-query-op.-text), the query predicate must include **equality match conditions** on the preceding keys.

- When you create a compound text index, all text index keys must be listed adjacently in the index specification document.

For examples of compound text indexes, see these pages:

- [Create a Compound Text Index](/docs/manual/core/indexes/index-types/index-text/create-text-index#std-label-compound-text-index-example)

- [Limit Text Index Entries Scanned on Self-Managed Deployments](/docs/manual/core/indexes/index-types/index-text/limit-number-of-items-scanned-for-text-search#std-label-limit-entries-scanned)

## Collation Option

Text indexes only support binary comparison, and do not support the [collation](/docs/manual/reference/collation#std-label-collation) option. Binary comparison compares the numeric Unicode value of each character in each string, and does not account for letter case or accent marks.

To create a text index on a collection that has a non-simple collation, you must explicitly specify `{ collation: { locale: "simple"
} }` when you create the index.

For example, consider a collection named `collationTest` with a collation of `{ locale: "en" }`:

```javascript
db.createCollection(
   "collationTest",
   {
      collation: { locale: "en" }
   }
)
```

To create a text index on the `collationTest` collection, you must specify `{ collation: { locale: "simple" } }`. The following command creates a text index on the `quotes` field:

```javascript
db.collationTest.createIndex(
   {
      quotes: "text"
   },
   {
      collation: { locale: "simple" }
   }
)
```
