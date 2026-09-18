> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Specify Language for Text Indexes on Self-Managed MongoDB

**Note:**

[MongoDB Search](https://www.mongodb.com/docs/atlas/atlas-search/) offers advanced full-text search capabilities, including support for [more language analyzers](https://www.mongodb.com/docs/search/indexes/analyzers/language/#std-label-ref-language-analyzers). We recommend using [MongoDB Search indexes](https://www.mongodb.com/docs/search/indexes/manage-indexes/#std-label-fts-manage-indexes) and the [`$search`](https://www.mongodb.com/docs/search/query/aggregation-stages/search/#mongodb-pipeline-pipe.-search) stage instead of text indexes and the `$text` operator.

By default, the `default_language` for text indexes is `english`. To improve the performance of non-English `$text` queries, you can specify a different default language associated with your text index.

The default language associated with the indexed data determines the suffix stemming rules. The default language also determines which language-specific stop words (for example, `the`, `an`, `a`, and `and` in English) are not indexed.

To specify a different language, use the `default_language` option when creating the text index. To see the languages available for text indexing, see [$text Query Languages on Self-Managed Deployments](/docs/manual/reference/text-search-languages#std-label-text-search-languages). Your operation should resemble this prototype:

```javascript
db.<collection>.createIndex(
   { <field>: "text" },
   { default_language: <language> }
)
```

If you specify a `default_language` value of `none`, the text index parses through each word in the field, including stop words, and ignores suffix stemming.

## Before You Begin

Create a `quotes` collection that contains the following documents with a Spanish text field:

```javascript
db.quotes.insertMany( [
   {
      _id: 1,
      quote : "La suerte protege a los audaces."
   },
   {
      _id: 2,
      quote: "Nada hay más surrealista que la realidad."
   },
   {
      _id: 3,
      quote: "Es este un puñal que veo delante de mí?"
   },
   {
      _id: 4,
      quote: "Nunca dejes que la realidad te estropee una buena historia."
   }
] )
```

## Procedure

The following operation creates a text index on the `quote` field and sets the `default_language` to `spanish`:

```javascript
db.quotes.createIndex(
   { quote: "text" },
   { default_language: "spanish" }
)
```

## Results

The resulting index supports `$text` queries on the `quote` field with Spanish-language suffix stemming rules. For example, the following query searches for the keyword `punal` in the `quote` field:

```javascript
db.quotes.find(
   {
      $text: { $search: "punal" }
   }
)
```

Output:

```javascript
[
   {
      _id: 3,
      quote: "Es este un puñal que veo delante de mí?"
   }
]
```

Although the `$search` value is set to `punal`, the query will return the document containing the word `puñal` because text indexes are [diacritic insensitive.](/docs/manual/core/indexes/index-types/index-text/text-index-properties#std-label-text-index-diacritic-insensitivity)

The index also ignores language-specific stop words. For example, although the document with `_id: 2` contains the word `hay`, the following query does not return any documents. `hay` is classified as a Spanish stop word, meaning it is not included in the text index.

```javascript
db.quotes.find(
   {
      $text: { $search: "hay" }
   }
)
```

## Learn More

- To create a text index for a collection containing text in multiple languages, see [Create a Multi-Language Text Index on Self-Managed Deployments.](/docs/manual/core/indexes/index-types/index-text/specify-language-text-index/create-text-index-multiple-languages#std-label-multiple-language-text-index)

- To learn about other text index properties, see [Text Index Properties on Self-Managed Deployments.](/docs/manual/core/indexes/index-types/index-text/text-index-properties#std-label-text-index-properties)
