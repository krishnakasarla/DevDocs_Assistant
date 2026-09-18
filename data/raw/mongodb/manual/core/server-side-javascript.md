> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Server-side JavaScript

**Important: Server-side JavaScript Deprecated**

Starting in MongoDB 8.0, server-side JavaScript functions ([`$accumulator`](/docs/manual/reference/operator/aggregation/accumulator#mongodb-group-grp.-accumulator), [`$function`](/docs/manual/reference/operator/aggregation/function#mongodb-expression-exp.-function), [`$where`](/docs/manual/reference/operator/query/where#mongodb-query-op.-where)) are deprecated. MongoDB logs a warning when you run these functions.

[Map-reduce](/docs/manual/core/map-reduce#std-label-map-reduce) is deprecated starting in MongoDB 5.0.

MongoDB provides the following commands, methods, and operator that perform server-side execution of JavaScript code:

- [`mapReduce`](/docs/manual/reference/command/mapReduce#mongodb-dbcommand-dbcmd.mapReduce) and the corresponding [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) method [`db.collection.mapReduce()`](/docs/manual/reference/method/db.collection.mapReduce#mongodb-method-db.collection.mapReduce).  For more information, see [Map-Reduce.](/docs/manual/core/map-reduce)

- [`$where`](/docs/manual/reference/operator/query/where#mongodb-query-op.-where) operator that evaluates a JavaScript expression or a function in order to query for documents.

- [`$accumulator`](/docs/manual/reference/operator/aggregation/accumulator#mongodb-group-grp.-accumulator) and [`$function`](/docs/manual/reference/operator/aggregation/function#mongodb-expression-exp.-function) aggregation operations that allows users to define custom aggregation expressions.

You can also specify a JavaScript file to [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) to run on the server. For more information, see [Running `.js` files via a `mongosh` Instance on the Server](/docs/manual/core/server-side-javascript#std-label-running-js-scripts-in-mongo-on-mongod-host)

**Note: JavaScript in MongoDB**

Although these methods use JavaScript, most interactions with MongoDB do not use JavaScript but use an [idiomatic driver](https://www.mongodb.com/docs/drivers/) in the language of the interacting application.

If you do not need to perform server-side execution of JavaScript code, see [Disable Server-Side Execution of JavaScript.](/docs/manual/core/server-side-javascript#std-label-disable-server-side-js)

**Note:**

If you are using SELinux, any MongoDB operation that requires [server-side JavaScript](/docs/manual/core/server-side-javascript#std-label-server-side-javascript) will result in segfault errors. [Disable Server-Side Execution of JavaScript](/docs/manual/core/server-side-javascript#std-label-disable-server-side-js) describes how to disable execution of server-side JavaScript.

## Running `.js` files via a `mongosh` Instance on the Server

You can specify a JavaScript (`.js`) file to [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) to execute the file on the server. This is a good technique for performing batch administrative work. When you run [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) on the server, connecting via the localhost interface, the connection is fast with low latency.

## Disable Server-Side Execution of JavaScript

You can disable all server-side execution of JavaScript:

- For a [`mongod`](/docs/manual/reference/program/mongod#mongodb-binary-bin.mongod) instance by passing the [`--noscripting`](/docs/manual/reference/program/mongod#std-option-mongod.--noscripting) option on the command line or setting [`security.javascriptEnabled`](/docs/manual/reference/configuration-options#mongodb-setting-security.javascriptEnabled) to false in the configuration file.

- For a [`mongos`](/docs/manual/reference/program/mongos#mongodb-binary-bin.mongos) instance by passing the [`--noscripting`](/docs/manual/reference/program/mongos#std-option-mongos.--noscripting) option on the command line or setting [`security.javascriptEnabled`](/docs/manual/reference/configuration-options#mongodb-setting-security.javascriptEnabled) to false in the configuration file.

## Behavior

### Concurrency

Refer to the individual method or operator documentation for any concurrency information. See also the [concurrency table.](/docs/manual/faq/concurrency#std-label-faq-concurrency-operations-locks)

### Unsupported Array and String Functions

MongoDB 6.0 upgrades the internal JavaScript engine used for [server-side JavaScript](/docs/manual/core/server-side-javascript#std-label-server-side-javascript), [`$accumulator`](/docs/manual/reference/operator/aggregation/accumulator#mongodb-group-grp.-accumulator), [`$function`](/docs/manual/reference/operator/aggregation/function#mongodb-expression-exp.-function), and [`$where`](/docs/manual/reference/operator/query/where#mongodb-query-op.-where) expressions and from MozJS-60 to MozJS-91. Several deprecated, non-standard array and string functions that existed in MozJS-60 are removed in MozJS-91.
