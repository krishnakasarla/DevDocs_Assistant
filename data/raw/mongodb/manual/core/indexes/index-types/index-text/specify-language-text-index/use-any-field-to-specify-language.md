> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Specify Text Index Language on Self-Managed Deployments

**Note:**

[MongoDB Search](https://www.mongodb.com/docs/atlas/atlas-search/) offers advanced full-text search capabilities, including [custom analyzers](https://www.mongodb.com/docs/search/indexes/analyzers/custom/#std-label-custom-analyzers) with [token filters](https://www.mongodb.com/docs/search/indexes/analyzers/token-filters/#std-label-token-filters-ref). We recommend using [MongoDB Search indexes](https://www.mongodb.com/docs/search/indexes/manage-indexes/#std-label-fts-manage-indexes) instead of text indexes.

A text index's language determines the rules used to parse stem words and ignore stop words when you run queries with the `$text` operator.

By default, if a text index does not have a [default language](/docs/manual/core/indexes/index-types/index-text/specify-text-index-language#std-label-specify-text-index-language), the index uses the `language` document field to determine the language it uses. As a result, text indexes are not limited to a single language because the value of the `language` field can change between documents.

You can change the field that the index uses to determine its language. This is useful if your field names are not in English, and your documents do not have a field called `language`.

To specify the text index language in a field other than `language`, include the `language_override` option when you create the index:

```javascript
db.<collection>.createIndex(
   { <field> : "text" },
   { language_override: "<field>" }
)
```

The text index uses the field specified in the `language_override` option to determine the language to use for the corresponding document.

For documents that don't contain the field specified in `language_override`, the index uses English as its language.

## Before You Begin

Create the `quotes` collection:

```javascript
db.quotes.insertMany(
   [
      {
         _id: 1,
         idioma: "portuguese",
         quote: "A sorte protege os audazes"
      },
      {
         _id: 2,
         idioma: "spanish",
         quote: "Nada hay más surrealista que la realidad."
      },
      {
         _id: 3,
         idioma: "english",
         quote: "is this a dagger which I see before me"
      }
   ]
)
```

The language for each quote is specified in the `idioma` field.

## Procedure

Create a text index on the `quote` field. Specify the `language_override` option to cause the text index to use the `idioma` field for the language:

```javascript
db.quotes.createIndex(
   { quote : "text" },
   { language_override: "idioma" }
)
```

## Results

The index supports `$text` queries on the `quote` field and uses language rules based on the language specified in the `idioma` field. Each document specifies a different value in the `idioma` field, which means that each document is searched with different language rules.

Consider the following examples:

### Search for a Valid Term

The following query searches for the string `audazes`:

```javascript
db.quotes.find(
   {
      $text: { $search: "audazes" }
   }
)
```

Output:

```javascript
[
  { _id: 1, idioma: 'portuguese', quote: 'A sorte protege os audazes' }
]
```

The preceding query uses Portuguese as the language to fulfill the query.

### Search for a Stop Word

The following query searches for the string `hay`:

```javascript
db.quotes.find(
   {
      $text: { $search: "hay" }
   }
)
```

The preceding query returns no results, even though the string `hay` appears in the `quote` field of document `_id: 2`.

Document `_id: 2` specifies a language of Spanish. `hay` is considered a stop word in Spanish, and is therefore not incldued in the text index.

## Learn More

- To see the languages available for text indexes, see [$text Query Languages on Self-Managed Deployments.](/docs/manual/reference/text-search-languages#std-label-text-search-languages)

- To learn how to specify a default language for an entire text index, see [Specify Language for Text Indexes on Self-Managed MongoDB.](/docs/manual/core/indexes/index-types/index-text/specify-text-index-language#std-label-specify-text-index-language)

- To see text index restrictions, see [Text Index Restrictions on Self-Managed Deployments.](/docs/manual/core/indexes/index-types/index-text/text-index-restrictions#std-label-text-index-restrictions)
