> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Time Series Compression

This page describes how MongoDB compresses data in time series collections, and how you can optimize compression.

## Default Compression Algorithm

Time series collections use [zstd](/docs/manual/reference/glossary#std-term-zstd) compression, which differs from the global default compression algorithm, [snappy.](/docs/manual/reference/glossary#std-term-snappy)

## Column Compression

Starting in MongoDB 5.2, time series collections use **column
compression**. Column compression adds a number of innovations that work together to significantly improve practical compression, reduce your data's overall storage on disk, and improve read performance.

These enhancements further reduce size of data on disk when compressed with `zstd`, and also significantly reduce space used in the WiredTiger cache.

The types of compression introduced are:

- Delta Encoding

- Object compression

- Array compression (starting in MongoDB 6.0)

- Run Length encoding (RLE)

### Delta Encoding (Delta Compression)

Delta Encoding takes advantage of the data in your time series collection having time-series characteristics. Instead of storing absolute values, Delta Encoding assumes that the measurements will not change rapidly between each other. This approach reduces the amount of information required by only storing the difference between measurements.

### Delta of Delta Encoding (Delta of Delta Compression)

With data that increases monotonically, Delta of Delta Encoding can further minimize the size of the number stored by calculating a delta of the delta itself.

### Object and Array Compression

Column compression ensures that if you are using objects and arrays in your documents, you receive the same compression benefits had those embedded fields existed at the root level of your document.

## Learn More

To learn how to optimize compression, see [Compression Best Practices.](/docs/manual/core/timeseries/timeseries-best-practices#std-label-tsc-best-practice-optimize-compression)
