> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Causal Consistency and Read and Write Concerns

With MongoDB's [causally consistent client sessions](/docs/manual/core/read-isolation-consistency-recency#std-label-sessions), different combinations of read and write concerns provide different [causal consistency guarantees.](/docs/manual/core/read-isolation-consistency-recency#std-label-causal-consistency-guarantees)

The following table lists the specific guarantees that various combinations provide:

| Read Concern | Write Concern | Read own writes | Monotonic reads | Monotonic writes | Writes follow reads |
| --- | --- | --- | --- | --- | --- |
| [`"majority"`](/docs/manual/reference/read-concern-majority#mongodb-readconcern-readconcern.-majority-) | [`"majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) | ✅ | ✅ | ✅ | ✅ |
| [`"majority"`](/docs/manual/reference/read-concern-majority#mongodb-readconcern-readconcern.-majority-) | [`{ w: 1 }`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-number-) |  | ✅ |  | ✅ |
| [`"local"`](/docs/manual/reference/read-concern-local#mongodb-readconcern-readconcern.-local-) | [`{ w: 1 }`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-number-) |  |  |  | |
| [`"local"`](/docs/manual/reference/read-concern-local#mongodb-readconcern-readconcern.-local-) | [`"majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) |  |  | ✅ | |

If you want causal consistency with data durability, then, as seen from the table, only read operations with [`"majority"`](/docs/manual/reference/read-concern-majority#mongodb-readconcern-readconcern.-majority-) read concern and write operations with [`"majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) write concern can guarantee all four causal consistency guarantees. That is, [causally consistent client sessions](/docs/manual/core/read-isolation-consistency-recency#std-label-sessions) can only guarantee causal consistency for:

- Read operations with [`"majority"`](/docs/manual/reference/read-concern-majority#mongodb-readconcern-readconcern.-majority-) read concern; in other words, the read operations that return data that has been acknowledged by a majority of the replica set members and is durable.

- Write operations with [`"majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) write concern; in other words, the write operations that request acknowledgment that the operation has been applied to a majority of the replica set's voting members.

If you want causal consistency without data durability (meaning that writes may be rolled back), then write operations with [`{ w: 1 }`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-number-) write concern can also provide causal consistency.

**Note:**

The other combinations of read and write concerns may also satisfy all four causal consistency guarantees in some situations, but not necessarily in all situations.

The read concern [`"majority"`](/docs/manual/reference/read-concern-majority#mongodb-readconcern-readconcern.-majority-) and write concern [`"majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) ensure that the four causal consistency guarantees hold even in [circumstances (such as with a network partition)](/docs/manual/core/read-preference-use-cases#std-label-edge-cases) where two members in a replica set *transiently* believe that they are the primary. And while both primaries can complete writes with [`{ w: 1 }`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-number-) write concern, only one primary will be able to complete writes with [`"majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) write concern.

For example, consider a situation where a network partition divides a five member replica set:

![Network partition: new primary elected on one side but old primary has not stepped down yet.](/images/network-partition-two-primaries.svg)

**Example: With the above partition**

- Writes with [`"majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) write concern can complete on `P` new but cannot complete on `P` old.

- Writes with [`{ w: 1 }`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-number-) write concern can complete on either `P` old or `P` new. However, the writes to `P` old (as well as the writes replicated to `S` 1) roll back once these members regain communication with the rest of the replica set.

- After a successful write with [`"majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) write concern on `P` new, causally consistent reads with [`"majority"`](/docs/manual/reference/read-concern-majority#mongodb-readconcern-readconcern.-majority-) read concern can observe the write on `P` new, `S` 2,and `S` 3. The reads can also observe the write on `P` old and `S` 1 once they can communicate with the rest of the replica set and sync from the other members of the replica set. Any writes made to `P` old and/or replicated to `S` 1 during the partition are rolled back.

## Scenarios

To illustrate the read and write concern requirements, the following scenarios have a client issue a sequence of operations with various combination of read and write concerns to the replica set:

- [Read Concern `"majority"` and Write concern `"majority"`](/docs/manual/core/causal-consistency-read-write-concerns#std-label-causal-rc-majority-wc-majority)

- [Read Concern `"majority"` and Write concern `{w: 1}`](/docs/manual/core/causal-consistency-read-write-concerns#std-label-causal-rc-majority-wc-1)

- [Read Concern `"local"` and Write concern `"majority"`](/docs/manual/core/causal-consistency-read-write-concerns#std-label-causal-rc-local-wc-majority)

- [Read Concern `"local"` and Write concern `{w: 1}`](/docs/manual/core/causal-consistency-read-write-concerns#std-label-causal-rc-local-wc-1)

### Read Concern `"majority"` and Write concern `"majority"`

The use of read concern [`"majority"`](/docs/manual/reference/read-concern-majority#mongodb-readconcern-readconcern.-majority-) and write concern [`"majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) in a causally consistent session provides the following causal consistency guarantees:

✅ Read own writes  ✅ Monotonic reads  ✅ Monotonic writes  ✅ Writes follow reads

**Note: Scenario 1 (Read Concern "majority" and Write Concern "majority")**

During the transient period with two primaries, because only `P` new can fulfill writes with [`{ w: "majority" }`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) write concern, a client session can issue the following sequence of operations successfully:

| Sequence | Example |
| --- | --- |
| 1. Write 1 with write concern [`"majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-)  to  `P` new2. Read 1 with read concern [`"majority"`](/docs/manual/reference/read-concern-majority#mongodb-readconcern-readconcern.-majority-) to `S` 23. Write 2 with write concern [`"majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) to `P` new4. Read 2 with read concern [`"majority"`](/docs/manual/reference/read-concern-majority#mongodb-readconcern-readconcern.-majority-) to `S` 3 | For item `A`, update `qty` to `50`.Read item `A`.For items with `qty` less than or equal to `50`,update `restock` to `true`.Read item `A`. |

![State of data with two primaries using read concern majority and write concern majority](/images/causal-rc-majority-wc-majority.svg)

| ✅ **Read own writes** | Read 1 reads data from `S` 2 that reflects a state after Write 1.Read 2 reads data from `S` 3 that reflects a state after Write 1 followed by Write 2. |
| --- | --- |
| ✅ **Monotonic reads** | Read 2 reads data from `S` 3 that reflects a state after Read 1. |
| ✅ **Monotonic writes** | Write 2 updates data on `P` new that reflects a state after Write 1. |
| ✅ **Writes follow reads** | Write 2 updates data on `P` new that reflects a state of the data after Read 1 (meaning that an earlier state reflects the data read by Read 1). |

**Note: Scenario 2 (Read Concern "majority" and Write Concern "majority")**

Consider an alternative sequence where Read 1 with read concern [`"majority"`](/docs/manual/reference/read-concern-majority#mongodb-readconcern-readconcern.-majority-) routes to `S` 1:

| Sequence | Example |
| --- | --- |
| 1. Write 1 with write concern [`"majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-)  to  `P` new2. Read 1 with read concern [`"majority"`](/docs/manual/reference/read-concern-majority#mongodb-readconcern-readconcern.-majority-) to `S` 13. Write 2 with write concern [`"majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) to `P` new4. Read 2 with with read concern [`"majority"`](/docs/manual/reference/read-concern-majority#mongodb-readconcern-readconcern.-majority-) to `S` 3 | For item `A`, update `qty` to `50`.Read item `A`.For items with `qty` less than or equal to `50`,update `restock` to `true`.Read item `A`. |

In this sequence, Read 1 cannot return until the majority commit point has advanced on `P` old. This cannot occur until `P` old and `S` 1 can communicate with the rest of the replica set; at which time, `P` old has stepped down (if not already), and the two members sync (including Write 1) from the other members of the replica set.

| ✅ **Read own writes** | Read 1 reflects a state of data after Write 1, albeit after the network partition has healed and the member has sync'ed from the other members of the replica set. Read 2 reads data from `S` 3 that reflects a state after Write 1 followed by Write 2. |
| --- | --- |
| ✅ **Monotonic reads** | Read 2 reads data from `S` 3 that reflects a state after Read 1 (meaning that an earlier state is reflected in the data read by Read 1). |
| ✅ **Monotonic writes** | Write 2 updates data on `P` new that reflects a state after Write 1. |
| ✅ **Writes follow reads** | Write 2 updates data on `P` new that reflects a state of the data after Read 1 (meaning that an earlier state reflects the data read by Read 1). |

### Read Concern `"majority"` and Write concern `{w: 1}`

The use of read concern [`"majority"`](/docs/manual/reference/read-concern-majority#mongodb-readconcern-readconcern.-majority-) and write concern [`{ w: 1 }`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-number-) in a causally consistent session provides the following causal consistency guarantees *if you want
causal consistency with data durability*:

❌ Read own writes  ✅ Monotonic reads  ❌ Monotonic writes  ✅ Writes follow reads

*If you want causal consistency without data durability*:

✅ Read own writes  ✅ Monotonic reads  ✅ Monotonic writes  ✅ Writes follow reads

**Note: Scenario 3 (Read Concern "majority" and Write Concern \{w: 1})**

During the transient period with two primaries, because both `P` old and `P` new can fulfill writes with [`{ w: 1 }`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-number-) write concern, a client session could issue the following sequence of operations successfully but not be causally consistent **if you want causal
consistency with data durability**:

| Sequence | Example |
| --- | --- |
| 1. Write 1 with write concern [`{ w: 1 }`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-number-)  to  `P` old2. Read 1 with read concern [`"majority"`](/docs/manual/reference/read-concern-majority#mongodb-readconcern-readconcern.-majority-) to `S` 23. Write 2 with write concern [`{ w: 1 }`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-number-) to `P` new4. Read 2 with with read concern [`"majority"`](/docs/manual/reference/read-concern-majority#mongodb-readconcern-readconcern.-majority-) to `S` 3 | For item `A`, update `qty` to `50`.Read item `A`.For items with `qty` less than or equal to `50`,update `restock` to `true`.Read item `A`. |

![State of data with two primaries using read concern majority and write concern 1](/images/causal-rc-majority-wc-1.svg)

In this sequence,

- Read 1 cannot return until the majority commit point has advanced on `P` new past the time of Write 1.

- Read 2 cannot return until the majority commit point has advanced on `P` new past the time of Write 2.

- Write 1 will roll back when the network partition is healed.

➤ *If you want causal consistency with data durability*

| ❌ **Read own writes** | Read 1 reads data from `S` 2 that doesn't reflect a state after Write 1. |
| --- | --- |
| ✅ **Monotonic reads** | Read 2 reads data from `S` 3 that reflects a state after Read 1 (meaning that an earlier state is reflected in the data read by Read 1). |
| ❌ **Monotonic writes** | Write 2 updates data on `P` new that does not reflect a state after Write 1. |
| ✅ **Writes follow reads** | Write 2 updates data on `P` new that reflects a state after Read 1 (meaning that an earlier state reflects the data read by Read 1). |

➤ *If you want causal consistency without data durability*

| ✅ **Read own writes** | Read 1 reads data from `S` 2 that reflects a state equivalent to Write 1 followed by rollback of Write 1. |
| --- | --- |
| ✅ **Monotonic reads** | Read 2 reads data from `S` 3 that reflects a state after Read 1 (meaning that an earlier state is reflected in the data read by Read 1). |
| ✅ **Monotonic writes** | Write 2 updates data on `P` new that is equivalent to after Write 1 followed by rollback of Write 1. |
| ✅ **Writes follow reads** | Write 2 updates data on `P` new that reflects a state after Read 1 (meaning whose earlier state reflects the data read by Read 1). |

**Note: Scenario 4 (Read Concern "majority" and Write Concern \{w: 1})**

Consider an alternative sequence where Read 1 with read concern [`"majority"`](/docs/manual/reference/read-concern-majority#mongodb-readconcern-readconcern.-majority-) routes to `S` 1:

| Sequence | Example |
| --- | --- |
| 1. Write 1 with write concern [`{ w: 1 }`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-number-)  to  `P` old2. Read 1 with read concern [`"majority"`](/docs/manual/reference/read-concern-majority#mongodb-readconcern-readconcern.-majority-) to `S` 13. Write 2 with write concern [`{ w: 1 }`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-number-) to `P` new4. Read 2 with with read concern [`"majority"`](/docs/manual/reference/read-concern-majority#mongodb-readconcern-readconcern.-majority-) to `S` 3 | For item `A`, update `qty` to `50`.Read item `A`.For items with `qty` less than or equal to `50`,update `restock` to `true`.Read item `A`. |

In this sequence:

- Read 1 cannot return until the majority commit point has advanced on `S` 1. This cannot occur until `P` old and `S` 1 can communicate with the rest of the replica set. At which time, `P` old has stepped down (if not already), Write 1 is rolled back from `P` old and `S` 1, and the two members sync from the other members of the replica set.

➤ *If you want causal consistency with data durability*

| ❌ **Read own writes** | The data read by Read 1 doesn't reflect the results of Write 1, which has rolled back. |
| --- | --- |
| ✅ **Monotonic reads** | Read 2 reads data from `S` 3 that reflects a state after Read 1 (meaning whose earlier state reflects the data read by Read 1). |
| ❌ **Monotonic writes** | Write 2 updates data on `P` new that does not reflect a state after Write 1, which had preceded Write 2 but has rolled back. |
| ✅ **Writes follow reads** | Write 2 updates data on `P` new that reflects a state after Read 1 (meaning whose earlier state reflects the data read by Read 1). |

➤ *If you want causal consistency without data durability*

| ✅ **Read own writes** | Read 1 returns data that reflects the final result of Write 1 since Write 1 ultimately rolls back. |
| --- | --- |
| ✅ **Monotonic reads** | Read 2 reads data from `S` 3 that reflects a state after Read 1 (meaning that an earlier state reflects the data read by Read 1). |
| ✅ **Monotonic writes** | Write 2 updates data on `P` new that is equivalent to after Write 1 followed by rollback of Write 1. |
| ✅ **Writes follow reads** | Write 2 updates data on `P` new that reflects a state after Read 1 (meaning that an earlier state reflects the data read by Read 1). |

### Read Concern `"local"` and Write concern `{w: 1}`

The use of read concern [`"local"`](/docs/manual/reference/read-concern-local#mongodb-readconcern-readconcern.-local-) and write concern [`{ w: 1 }`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-number-) in a causally consistent session cannot guarantee causal consistency.

❌ Read own writes  ❌ Monotonic reads  ❌ Monotonic writes  ❌ Writes follow reads

This combination may satisfy all four causal consistency guarantees in some situations, but not necessarily in all situations.

**Note: Scenario 5 (Read Concern "local" and Write Concern \{w: 1})**

During this transient period, because both `P` old and `P` new can fulfill writes with [`{ w: 1 }`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-number-) write concern, a client session could issue the following sequence of operations successfully but not be causally consistent:

| Sequence | Example |
| --- | --- |
| 1. Write 1 with write concern [`{ w: 1 }`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-number-)  to  `P` old2. Read 1 with read concern [`"local"`](/docs/manual/reference/read-concern-local#mongodb-readconcern-readconcern.-local-) to `S` 13. Write 2 with write concern [`{ w: 1 }`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-number-) to `P` new4. Read 2 with read concern [`"local"`](/docs/manual/reference/read-concern-local#mongodb-readconcern-readconcern.-local-) to `S` 3 | For item `A`, update `qty` to `50`.Read item `A`.For items with `qty` less than or equal to `50`,update `restock` to `true`.Read item `A`. |

![State of data with two primaries using read concern local and write concern 1](/images/causal-rc-local-wc-1.svg)

| ❌ Read own writes | Read 2 reads data from `S` 3 that only reflects a state after Write 2 and not Write 1 followed by Write 2. |
| --- | --- |
| ❌ Monotonic reads | Read 2 reads data from `S` 3 that doesn't reflect a state after Read 1 (meaning that an earlier state doesn't reflect the data read by Read 1). |
| ❌ Monotonic writes | Write 2 updates data on `P` new that does not reflect a state after Write 1. |
| ❌ Write follow read | Write 2 updates data on `P` new that does not reflect a state after Read 1 (meaning that an earlier state doesn't reflect the data read by Read 1). |

### Read Concern `"local"` and Write concern `"majority"`

The use of read concern [`"local"`](/docs/manual/reference/read-concern-local#mongodb-readconcern-readconcern.-local-) and write concern [`"majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) in a causally consistent session provides the following causal consistency guarantees:

❌ Read own writes  ❌ Monotonic reads  ✅ Monotonic writes  ❌ Writes follow reads

This combination may satisfy all four causal consistency guarantees in some situations, but not necessarily in all situations.

**Note: Scenario 6 (Read Concern "local" and Write Concern "majority")**

During this transient period, because only `P` new can fulfill writes with  [`{ w: "majority" }`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-) write concern, a client session could issue the following sequence of operations successfully but not be causally consistent:

| Sequence | Example |
| --- | --- |
| 1. Write 1 with write concern [`"majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-)  to  `P` new2. Read 1 with read concern [`"local"`](/docs/manual/reference/read-concern-local#mongodb-readconcern-readconcern.-local-) to `S` 13. Write 2 with write concern [`"majority"`](/docs/manual/reference/write-concern#mongodb-writeconcern-writeconcern.-majority-)  to `P` new4. Read 2 with read concern [`"local"`](/docs/manual/reference/read-concern-local#mongodb-readconcern-readconcern.-local-) to `S` 3 | For item `A`, update `qty` to `50`.Read item `A`.For items with `qty` less than or equal to `50`,update `restock` to `true`.Read item `A`. |

![State of data with two primaries using read concern local and write concern majority](/images/causal-rc-local-wc-majority.svg)

| ❌ Read own writes. | Read 1 reads data from `S` 1 that doesn't reflect a state after Write 1. |
| --- | --- |
| ❌ Monotonic reads. | Read 2 reads data from `S` 3 that doesn't reflect a state after Read 1 (meaning that an earlier state doesn't reflect the data read by Read 1). |
| ✅ Monotonic writes | Write 2 updates data on `P` new that reflects a state after Write 1. |
| ❌ Write follow read. | Write 2 updates data on `P` new that does not reflect a state after Read 1 (meaning that an earlier state doesn't reflect the data read by Read 1). |
