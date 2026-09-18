> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Create a Multi-Language Text Index on Self-Managed Deployments

**Note:**

[MongoDB Search](https://www.mongodb.com/docs/atlas/atlas-search/) offers advanced full-text search capabilities, including [multi analyzers](https://www.mongodb.com/docs/search/indexes/analyzers/multi/#std-label-ref-multi-analyzers). We recommend using [MongoDB Search indexes](https://www.mongodb.com/docs/search/indexes/manage-indexes/#std-label-fts-manage-indexes) instead of text indexes.

You can create a text index to improve the performance of text queries run on a collection containing documents or embedded documents with text in multiple languages.

If a collection contains documents or embedded documents that are in multiple different languages, include a field named `language` and specify the language for those documents as the field value. To see the languages available for text indexing, see [$text Query Languages on Self-Managed Deployments.](/docs/manual/reference/text-search-languages#std-label-text-search-languages)

Your insert operation should resemble this example to support text indexing for multiple languages:

```javascript
db.<collection>.insertOne(
   {
      <field>: <value>,
      language: <language>
   }
)
```

## Before You Begin

Create a `quotes` collection that contains multi-language documents that include the `language` field:

```javascript
db.quotes.insertMany( [
   {
      _id: 1,
      language: "portuguese",
      original: "A sorte protege os audazes.",
      translation:
        [
           {
              language: "english",
              quote: "Fortune favors the bold."
           },
           {
              language: "spanish",
              quote: "La suerte protege a los audaces."
           }
       ]
   },
   {
      _id: 2,
      language: "spanish",
      original: "Nada hay más surrealista que la realidad.",
      translation:
         [
           {
             language: "english",
             quote: "There is nothing more surreal than reality."
           },
           {
             language: "french",
             quote: "Il n'y a rien de plus surréaliste que la réalité."
           }
         ]
   },
   {
      _id: 3,
      original: "Is this a dagger which I see before me?",
      translation:
      {
         language: "spanish",
         quote: "Es este un puñal que veo delante de mí."
      }
   }
] )
```

## Procedure

The following operation creates a text index on the `original` and `translation.quote` fields:

```javascript
db.quotes.createIndex({ original: "text", "translation.quote": "text", "default_language" : "fr" })
```

**Note:**

English is the default language for indexes. If you do not specify the [default\_language](/docs/manual/reference/command/createIndexes#std-label-createIndexes-default-language), your query must specify the language with the [$language](/docs/manual/reference/operator/query/text#std-label-language-field) parameter. For more information, refer to [Specify Language for Text Indexes on Self-Managed MongoDB.](/docs/manual/core/indexes/index-types/index-text/specify-text-index-language#std-label-specify-default-text-index-language)

## Results

The resulting index supports `$text` queries for the documents and embedded documents containing the `original` and `translation.quote` fields. The text index follows different suffix stemming rules, and ignores stop words specific to each language, based on the value in the `language` field.

For example, the following query searches for the `french` word `réalité`.

```javascript
db.quotes.find(
   { $text:
      { $search: "réalité" }
   }
)
```

Output:

```javascript
[
   {
      _id: 2,
      language: 'spanish',
      original: 'Nada hay más surrealista que la realidad.',
      translation: [
         {
            language: 'english',
            quote: 'There is nothing more surreal than reality.'
         },
         {
            language: 'french',
            quote: "Il n'y a rien de plus surréaliste que la réalité."
         }
      ]
   }
]
```

For embedded documents that do not contain the `language` field,

- If the enclosing document contains the `language` field, then the index uses the document's language for the embedded documents.

- Otherwise, the index uses the default language for the embedded documents.

For documents that do not contain the `language` field, the index uses the default language, which is English.

## Learn More

- To specify the text index language in a field other than `language`, see [Specify Text Index Language on Self-Managed Deployments.](/docs/manual/core/indexes/index-types/index-text/specify-language-text-index/use-any-field-to-specify-language#std-label-text-index-specify-language-in-field)

- To learn how to specify the default language for a text index, see [Specify Language for Text Indexes on Self-Managed MongoDB.](/docs/manual/core/indexes/index-types/index-text/specify-text-index-language#std-label-specify-default-text-index-language)

- To learn about other text index properties, see [Text Index Properties on Self-Managed Deployments.](/docs/manual/core/indexes/index-types/index-text/text-index-properties#std-label-text-index-properties)
