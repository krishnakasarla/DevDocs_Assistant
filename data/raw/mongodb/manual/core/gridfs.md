> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# GridFS for Self-Managed Deployments

[GridFS](/docs/manual/reference/glossary#std-term-GridFS) is a specification for storing and retrieving files that exceed the [BSON](/docs/manual/reference/glossary#std-term-BSON)-document [size limit](/docs/manual/reference/limits#std-label-limit-bson-document-size) of 16 MiB.

**Note:**

GridFS does not support [multi-document transactions.](/docs/manual/core/transactions#std-label-transactions)

Instead of storing a file in a single document, GridFS divides the file into parts, or chunks , and stores each chunk as a separate document. By default, GridFS uses a chunk size of 255 KiB; that is, GridFS divides a file into chunks of 255 KiB with the exception of the last chunk. The last chunk is only as large as necessary. Similarly, files that are no larger than the chunk size only have a final chunk, using only as much space as needed plus some additional metadata.

GridFS uses two collections to store files. One collection stores the file chunks, and the other stores file metadata.

When you query GridFS for a file, the driver reassembles the chunks as needed. You can perform range queries on files stored through GridFS. You can also access information from arbitrary sections of files, such as to "skip" to the middle of a video or audio file.

GridFS is useful not only for storing files that exceed 16 MiB but also for storing any files for which you want access without having to load the entire file into memory. See also [When to Use GridFS.](/docs/manual/core/gridfs#std-label-faq-developers-when-to-use-gridfs)

## When to Use GridFS

Use [GridFS](/docs/manual/reference/glossary#std-term-GridFS) for storing files larger than 16 MiB.

In some situations, storing large files may be more efficient in a MongoDB database than on a system-level filesystem.

- If your filesystem limits the number of files in a directory, you can use GridFS to store as many files as needed.

- When you want to access portions of large files without loading the entire file into memory, use GridFS.

- When you want to keep your files and metadata synced and deployed across a number of systems and facilities, use GridFS. With [geographically distributed replica sets](/docs/manual/core/replica-set-architecture-geographically-distributed#std-label-replica-set-geographical-distribution), MongoDB distributes files and their metadata to [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instances across multiple facilities.

Do not use GridFS if you need to update the content of the entire file atomically. As an alternative you can store multiple versions of each file and specify the current version of the file in the metadata. You can update the metadata field that indicates "latest" status in an atomic update after uploading the new version of the file, and later remove previous versions if needed.

If your files are all smaller than the 16 MiB [BSON Document Size](/docs/manual/reference/limits#mongodb-limit-BSON-Document-Size) limit, consider storing each file in a single document instead of using GridFS. Use the BinData data type to store the binary data. See your [drivers](https://www.mongodb.com/docs/drivers/) documentation for details on using BinData.

## Use GridFS

To store and retrieve files using [GridFS](/docs/manual/reference/glossary#std-term-GridFS), use either of the following:

- A MongoDB driver. See the [drivers](https://www.mongodb.com/docs/drivers/) documentation for information on using GridFS with your driver.

- The [`mongofiles`](https://www.mongodb.com/docs/database-tools/mongofiles/#mongodb-binary-bin.mongofiles) command-line tool. See the [`mongofiles`](https://www.mongodb.com/docs/database-tools/mongofiles/#mongodb-binary-bin.mongofiles) reference for documentation.

## GridFS Collections

[GridFS](/docs/manual/reference/glossary#std-term-GridFS) stores files in two collections:

- `chunks` stores the binary chunks. For details, see [The `chunks` Collection.](/docs/manual/core/gridfs#std-label-gridfs-chunks-collection)

- `files` stores the file's metadata. For details, see [The `files` Collection.](/docs/manual/core/gridfs#std-label-gridfs-files-collection)

GridFS places the collections in a common bucket by prefixing each with the bucket name. By default, GridFS uses two collections with a bucket named `fs`:

- `fs.files`

- `fs.chunks`

You can choose a different bucket name, as well as create multiple buckets in a single database. The full collection name, which includes the bucket name, is subject to the [namespace length limit.](/docs/manual/reference/limits#mongodb-limit-Namespace-Length)

### The `chunks` Collection

Each document in the `chunks`  collection represents a distinct chunk of a file as represented in [GridFS](/docs/manual/reference/glossary#std-term-GridFS). Documents in this collection have the following form:

```javascript
{
  "_id" : <ObjectId>,
  "files_id" : <ObjectId>,
  "n" : <num>,
  "data" : <binary>
}
```

A document from the `chunks` collection contains the following fields:

The unique [ObjectId](/docs/manual/reference/glossary#std-term-ObjectId) of the chunk.

The `_id` of the "parent" document, as specified in the `files` collection.

The sequence number of the chunk. GridFS numbers all chunks, starting with 0.

The chunk's payload as a [BSON](/docs/manual/reference/glossary#std-term-BSON) `Binary` type.

### The `files` Collection

Each document in the `files` collection represents a file in [GridFS.](/docs/manual/reference/glossary#std-term-GridFS)

```javascript
{
  "_id" : <ObjectId>,
  "length" : <num>,
  "chunkSize" : <num>,
  "uploadDate" : <timestamp>,
  "md5" : <hash>,
  "filename" : <string>,
  "contentType" : <string>,
  "aliases" : <string array>,
  "metadata" : <any>,
}
```

Documents in the `files` collection contain some or all of the following fields:

The unique identifier for this document. The `_id` is of the data type you chose for the original document. The default type for MongoDB documents is [BSON](/docs/manual/reference/glossary#std-term-BSON) [ObjectId.](/docs/manual/reference/glossary#std-term-ObjectId)

The size of the document in bytes.

The size of each chunk in **bytes**. GridFS divides the document into chunks of size `chunkSize`, except for the last, which is only as large as needed. The default size is 255 kibibytes (KiB).

The date the document was first stored by GridFS. This value has the `Date` type.

**Deprecated**

The MD5 algorithm is prohibited by FIPS 140-2. MongoDB drivers deprecate MD5 support and will remove MD5 generation in future releases.  Applications that require a file digest should implement it outside of GridFS and store in [`files.metadata`.](/docs/manual/core/gridfs#mongodb-data-files.metadata)

An MD5 hash of the complete file returned by the [`filemd5`](/docs/manual/reference/command/filemd5#mongodb-dbcommand-dbcmd.filemd5) command. This value has the `String` type.

Optional. A human-readable name for the GridFS file.

**Deprecated**

Optional. A valid MIME type for the GridFS file. For application use only.

Use [`files.metadata`](/docs/manual/core/gridfs#mongodb-data-files.metadata) for storing information related to the MIME type of the GridFS file.

**Deprecated**

Optional. An array of alias strings. For application use only.

Use [`files.metadata`](/docs/manual/core/gridfs#mongodb-data-files.metadata) for storing alias information.

Optional. The metadata field may be of any data type and can hold any additional information you want to store. To add arbitrary fields to documents in the `files` collection, add them to an object in the metadata field.

## GridFS Indexes

GridFS uses indexes on each of the `chunks` and `files` collections for efficiency. [Drivers](https://www.mongodb.com/docs/drivers/) that conform to the [GridFS specification](https://github.com/mongodb/specifications/blob/master/source/gridfs/gridfs-spec.rst) automatically create these indexes. You can also create additional indexes to suit your application.

### The `chunks` Index

[GridFS](/docs/manual/reference/glossary#std-term-GridFS) uses a [unique](/docs/manual/reference/glossary#std-term-unique-index), [compound](/docs/manual/reference/glossary#std-term-compound-index) index on the `chunks` collection using the `files_id` and `n` fields. This allows for efficient retrieval of chunks, as demonstrated in the following example:

```javascript
db.fs.chunks.find( { files_id: myFileID } ).sort( { n: 1 } )
```

[Drivers](https://www.mongodb.com/docs/drivers/) that conform to the [GridFS specification](https://github.com/mongodb/specifications/blob/master/source/gridfs/gridfs-spec.rst) automatically ensure that this index exists before read and write operations. See the relevant driver documentation for the specific behavior of your GridFS application.

If this index does not exist, you can issue the following operation to create it using [`mongosh`:](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh)

```javascript
db.fs.chunks.createIndex( { files_id: 1, n: 1 }, { unique: true } );
```

### The `files` Index

[GridFS](/docs/manual/reference/glossary#std-term-GridFS) uses an [index](/docs/manual/reference/command/collMod#mongodb-collflag-index) on the `files` collection using the `filename` and `uploadDate` fields. This index allows for efficient retrieval of files, as shown in this example:

```javascript
db.fs.files.find( { filename: myFileName } ).sort( { uploadDate: 1 } )
```

[Drivers](https://www.mongodb.com/docs/drivers/) that conform to the [GridFS specification](https://github.com/mongodb/specifications/blob/master/source/gridfs/gridfs-spec.rst) automatically ensure that this index exists before read and write operations. See the relevant driver documentation for the specific behavior of your GridFS application.

If this index does not exist, you can issue the following operation to create it using [`mongosh`:](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh)

```javascript
db.fs.files.createIndex( { filename: 1, uploadDate: 1 } );
```

The use of the term *chunks* in the context of GridFS is not related to the use of the term *chunks* in the context of sharding.

## Sharding GridFS

[GridFS](/docs/manual/reference/glossary#std-term-GridFS) has two collections to consider: `files` and `chunks`.

### `chunks` Collection

To shard the `chunks` collection, use either `{ files_id : 1, n : 1
}` or `{ files_id : 1 }` as the shard key index. `files_id` is an [ObjectId](/docs/manual/reference/glossary#std-term-ObjectId) and changes [monotonically.](/docs/manual/core/sharding-choose-a-shard-key#std-label-shard-key-monotonic)

For MongoDB drivers that do not run [`filemd5`](/docs/manual/reference/command/filemd5#mongodb-dbcommand-dbcmd.filemd5) to verify successful upload, you can use [hashed sharding](/docs/manual/core/hashed-sharding#std-label-sharding-hashed-sharding) for the `chunks` collection.

If the MongoDB driver runs [`filemd5`](/docs/manual/reference/command/filemd5#mongodb-dbcommand-dbcmd.filemd5), you cannot use [hashed sharding](/docs/manual/core/hashed-sharding#std-label-sharding-hashed-sharding). For details, see [SERVER-9888.](https://jira.mongodb.org/browse/SERVER-9888)

### `files` Collection

The `files` collection is small and only contains metadata. None of the required keys for GridFS lend themselves to an even distribution in a sharded environment. Leaving `files` unsharded allows all the file metadata documents to live on one shard.

If you *must* shard the `files` collection, use the `_id` field, possibly in combination with an application field.
