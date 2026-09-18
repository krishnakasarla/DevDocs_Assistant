> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Create an Index on a Single Field

You can create an index on a single field to improve performance for queries on that field.

To create a single-field index, use the [`db.collection.createIndex()`](/docs/manual/reference/method/db.collection.createIndex#mongodb-method-db.collection.createIndex) method:

```javascript
db.<collection>.createIndex( { <field>: <sort-order> } )
```

## Before You Begin

Create a `students` collection that contains the following documents:

```javascript
db.students.insertMany( [
   {
      "name": "Alice",
      "gpa": 3.6,
      "location": { city: "Sacramento", state: "California" }
   },
   {
      "name": "Bob",
      "gpa": 3.2,
      "location": { city: "Albany", state: "New York" }
   }
] )
```

## Procedures

The following examples show you how to:

- [Create an Index on a Single Field](/docs/manual/core/indexes/index-types/index-single/create-single-field-index#std-label-index-create-ascending-single-field)

- [Create an Index on an Embedded Field](/docs/manual/core/indexes/index-types/index-single/create-single-field-index#std-label-index-embedded-fields)

### Create an Index on a Single Field

Consider a school administrator who frequently looks up students by their GPA (Grade Point Average). You can create an index on the `gpa` field to improve performance for those queries:

```javascript
db.students.createIndex( { gpa: 1 } )
```

#### Results

The index supports queries that select on the field `gpa`, such as the following:

```javascript
db.students.find( { gpa: 3.6 } )

db.students.find( { gpa: { $lt: 3.4 } } )
```

### Create an Index on an Embedded Field

You can create indexes on fields within embedded documents. Indexes on embedded fields can fulfill queries that use [dot notation.](/docs/manual/reference/glossary#std-term-dot-notation)

The `location` field is an embedded document that contains the embedded fields `city` and `state`. Create an index on the `location.state` field:

```javascript
db.students.createIndex( { "location.state": 1 } )
```

#### Results

The index supports queries on the field `location.state`, such as the following:

```javascript
db.students.find( { "location.state": "California" } )

db.students.find( { "location.city": "Albany", "location.state": "New York" } )
```

## Learn More

- [Create an Index on an Embedded Document](/docs/manual/core/indexes/index-types/index-single/create-embedded-object-index#std-label-index-embedded-documents)

- [Create an Index on an Embedded Field in an Array](/docs/manual/core/indexes/index-types/index-multikey/create-multikey-index-embedded#std-label-index-create-multikey-embedded)

- [Check if a query uses an index](/docs/manual/tutorial/measure-index-use#std-label-index-measure-index-use)

- [Learn about other types of index types](/docs/manual/core/indexes/index-types#std-label-index-types)
