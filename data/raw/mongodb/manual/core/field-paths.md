> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Field Paths

Use [field path](/docs/manual/reference/glossary#std-term-field-path) expressions to access fields in input documents. Prefix the field name or the [dotted field path](/docs/manual/core/document#std-label-document-dot-notation) (for embedded documents) with a dollar sign `$`.

## Nested Fields

The following examples use the [planets](https://www.mongodb.com/docs/atlas/sample-data/sample-guides/#collections) collection from the [Atlas Sample Databases](https://www.mongodb.com/docs/atlas/sample-data/). Each document in this collection has the following structure:

```javascript
{
   _id: new ObjectId("6220f6b78a733c51b416c80e"),
   name: "Uranus",
   orderFromSun: 7,
   hasRings: true,
   mainAtmosphere: [ "H2", "He", "CH4" ],
   surfaceTemperatureC: { min: null, max: null, mean: -197.2 }
}
```

To specify the nested `mean` field within `surfaceTemperatureC`, use [dot notation](/docs/manual/reference/glossary#std-term-dot-notation) (`"field.nestedField"`) with a dollar sign `$`. This aggregation pipeline projects only the `mean` nested field value for each document:

```javascript
db.planets.aggregate( [
   {
      $project: {
         nested_field: "$surfaceTemperatureC.mean"
      }
   }
] )
```

An example returned document:

```javascript
{ _id: ObjectId('6220f6b78a733c51b416c80e'), nested_field: -197.2 }
```

## Array of Nested Fields

Use [dot notation](/docs/manual/reference/glossary#std-term-dot-notation) in a field path to access a field nested within an array. For example, consider a `products` collection whose `instock` field holds an array of nested `warehouse` fields:

```javascript
db.products.insertMany( [
   { item: "journal", instock: [ { warehouse: "A"}, { warehouse: "C" } ] },
   { item: "notebook", instock: [ { warehouse: "C" } ] },
   { item: "paper", instock: [ { warehouse: "A" }, { warehouse: "B" } ] },
   { item: "planner", instock: [ { warehouse: "A" }, { warehouse: "B" } ] },
   { item: "postcard", instock: [ { warehouse: "B" }, { warehouse: "C" } ] }
] )
```

The following aggregation pipeline uses `$instock.warehouse` to access the nested `warehouse` fields.

```javascript
db.products.aggregate( [
   {
      $project: {
         item: 1,
         warehouses: "$instock.warehouse"
      }
   }
] )
```

In this example, `$instock.warehouse` outputs an array of values that are in the nested `warehouse` field for each document. The pipeline returns the following documents:

```javascript
[
   {
      _id: ObjectId('6740b55e33b29cf6b1d884f7'),
      item: "journal",
      warehouses: [ "A", "C" ]
   },
   {
      _id: ObjectId('6740b55e33b29cf6b1d884f8'),
      item: "notebook",
      warehouses: [ "C" ]
   },
   {
      _id: ObjectId('6740b55e33b29cf6b1d884f9'),
      item: "paper",
      warehouses: [ "A", "B" ]
   },
   {
      _id: ObjectId('6740b55e33b29cf6b1d884fa'),
      item: "planner",
      warehouses: [ "A", "B" ]
   },
   {
      _id: ObjectId('6740b55e33b29cf6b1d884fb'),
      item: "postcard",
      warehouses: [ "B", "C" ]
   }
]
```

## Array of Nested Arrays

You can also use [dot notation](/docs/manual/reference/glossary#std-term-dot-notation) with a dollar sign `$` in a field path to access an array within a nested array. The following example uses a `fruits` collection with this document:

```javascript
db.fruits.insertOne(
   {
      _id: ObjectId("5ba53172ce6fa2fcfc58e0ac"),
      inventory: [
         {
            apples: [
               "macintosh",
               "golden delicious",
            ]
         },
         {
            oranges: [
               "mandarin",
            ]
         },
         {
            apples: [
               "braeburn",
               "honeycrisp",
            ]
         }
      ]
   }
)
```

The following aggregation pipeline accesses the nested `apples` arrays inside `inventory`:

```javascript
db.fruits.aggregate( [
   { $project:
      { all_apples: "$inventory.apples" } }
] )
```

In this pipeline, `$inventory.apples` resolves to an array of nested arrays. The pipeline returns the following document:

```javascript
{
   _id: ObjectId('5ba53172ce6fa2fcfc58e0ac'),
   all_apples: [
      [ "macintosh", "golden delicious" ],
      [ "braeburn", "honeycrisp" ]
   ]
}
```

## Learn More

For more information on accessing and interacting with nested elements, see [Dot Notation](/docs/manual/core/document#std-label-document-dot-notation) and [Query an Array of Embedded Documents.](/docs/manual/tutorial/query-array-of-documents#std-label-array-match-embedded-documents)
