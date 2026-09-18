> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Text Index Versions on Self-Managed Deployments

**Note:**

MongoDB offers an improved full-text search solution, [MongoDB Search](https://www.mongodb.com/docs/atlas/atlas-search/), and vector search solution, [MongoDB Vector Search](https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-overview/). We recommend using [MongoDB Search indexes](https://www.mongodb.com/docs/search/indexes/manage-indexes/#std-label-fts-manage-indexes) or [MongoDB Vector Search indexes](https://www.mongodb.com/docs/vector-search/indexes/vector-search-type/#std-label-avs-types-vector-search)  instead of text indexes.

Text indexes are available in the following versions:

| Text Index Version | Description |
| --- | --- |
| Version 3 | MongoDB 3.2 introduces version 3 of text indexes. Version 3 is the default version for text indexes created in MongoDB 3.2 and later. |
| Version 2 | MongoDB 2.6 introduces version 2 of text indexes. Version 2 is the default version for text indexes created in MongoDB 2.6 to 3.0. |
| Version 1 | MongoDB 2.4 introduces version 1 of text indexes. MongoDB 2.4 only supports version 1. |

## Change Index Version

**Important:**

Always use the default index version when possible. Only override the default version if required for compatibility reasons.

To override the default version and specify a different version for your text index, set the `textIndexVersion` option when you create an index:

```javascript
db.<collection>.createIndex(
   { <field>: "text" },
   { "textIndexVersion": <version> }
)
```

### Example

The following command creates a version 2 text index on the `content` field:

```javascript
db.test.createIndex(
   { "content": "text" },
   { "textIndexVersion": 2 }
 )
```
