> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Create a View with Default Collation

[Collation](/docs/manual/reference/collation#std-label-manual-collation) allows you to specify language-specific rules for string comparison, such as rules for letter-case and accent marks.

This page explains how to specify a default collation for a view.

## Example

Create a `places` collection with the following documents:

```javascript
db.places.insertMany([
   { _id: 1, category: "café" },
   { _id: 2, category: "cafe" },
   { _id: 3, category: "cafE" }
])
```

The following operation creates a view, specifying collation at the view level:

```javascript
db.createView(
   "placesView",
   "places",
   [ { $project: { category: 1 } } ],
   { collation: { locale: "fr", strength: 1 } }
)
```

The following operation uses the view's collation:

```javascript
db.placesView.countDocuments( { category: "cafe" } )
```

The operation returns `3`.

**Note: Collation Behavior**

- You can specify a default [collation](/docs/manual/reference/collation#std-label-collation) for a view at creation time. If no collation is specified, the view's default collation is the "simple" binary comparison collator. That is, the view does not inherit the collection's default collation.

- String comparisons on the view use the view's default collation. An operation that attempts to change or override a view's default collation will fail with an error.

- If creating a view from another view, you cannot specify a collation that differs from the source view's collation.

- If performing an aggregation that involves multiple views, such as with [`$lookup`](/docs/manual/reference/operator/aggregation/lookup#mongodb-pipeline-pipe.-lookup) or [`$graphLookup`](/docs/manual/reference/operator/aggregation/graphLookup#mongodb-pipeline-pipe.-graphLookup), the views must have the same [collation.](/docs/manual/reference/collation#std-label-collation)
