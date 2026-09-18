> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Read Preference Tag Set Lists

If a replica set member or members are associated with [`tags`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.members-n-.tags), you can specify a tag set list (array of tag sets) in the read preference to target those members.

To [configure](/docs/manual/reference/replica-configuration#std-label-replica-set-configuration-document) a member with tags, set [`members[n].tags`](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.members-n-.tags) to a document that contains the tag name and value pairs. The value of the tags must be a string.

```javascript
{ "<tag1>": "<string1>", "<tag2>": "<string2>",... }
```

Then, you can include a tag set list in the read preference to target tagged members. A tag set list is an array of tag sets, where each tag set contains one or more tag/value pairs.

```javascript
[ { "<tag1>": "<string1>", "<tag2>": "<string2>",... }, ... ]
```

To find replica set members, MongoDB tries each document in succession until a match is found.  See [Order of Tag Matching](/docs/manual/core/read-preference-tags#std-label-read-pref-order-matching) for details.

For example, if a secondary member has the following [`members[n].tags`:](/docs/manual/reference/replica-configuration#mongodb-rsconf-rsconf.members-n-.tags)

```javascript
{ "region": "South", "datacenter": "A" }
```

Then, the following tag set lists can direct read operations to the aforementioned secondary (or other members with the same tags):

```javascript
[ { "region": "South", "datacenter": "A" }, { } ]     // Find members with both tag values. If none are found, read from any eligible member.
[ { "region": "South" }, { "datacenter": "A" }, { } ] // Find members with the specified region tag. Only if not found, then find members with the specified datacenter tag. If none are found, read from any eligible member.
[ { "datacenter": "A" }, { "region": "South" }, { } ] // Find members with the specified datacenter tag. Only if not found, then find members with the specified region tag. If none are found, read from any eligible member.
[ { "region": "South" }, { } ]                        // Find members with the specified region tag value. If none are found, read from any eligible member.
[ { "datacenter": "A" }, { } ]                        // Find members with the specified datacenter tag value. If none are found, read from any eligible member.
[ { } ]                                               // Find any eligible member.
```

## Order of Tag Matching

If the tag set list contains multiple documents, MongoDB tries each document in succession until a match is found. Once a match is found, that tag set is used to find all eligible matching members, and the remaining tag sets are ignored. If no members match any of the tag sets, the read operation returns with an error.

**Tip:**

To avoid an error if no members match any of the tag specifications, you can add an empty document `{ }` as the last element of the tag set list to read from any eligible member.

For example, consider the following tag set list with three tag sets:

```javascript
[ { "region": "South", "datacenter": "A" },  { "rack": "rack-1" }, { } ]
```

First, MongoDB tries to find members tagged with both `"region":
"South"` and `"datacenter": "A"`.

```none
{ "region": "South", "datacenter": "A" }
```

- If a member is found, the remaining tag sets are not considered. Instead, MongoDB uses this tag set to find all eligible members.

- Else, MongoDB tries to find members with the tags specified in the second document

  ```none
  { "rack": "rack-1" }
  ```

  - If a member is found tagged, the remaining tag set is not considered. Instead, MongoDB uses this tag set to find all eligible members.

  - Else, the third document is considered.

    ```none
    { }
    ```

    The empty document matches any eligible member.

## Tag Set List and Read Preference Modes

Tags are not compatible with mode [`primary`](/docs/manual/reference/glossary#std-term-primary), and in general, only apply when [selecting](/docs/manual/core/read-preference-mechanics#std-label-replica-set-read-preference-behavior-member-selection) a [secondary](/docs/manual/reference/glossary#std-term-secondary) member of a set for a read operation. However, the [`nearest`](/docs/manual/core/read-preference#mongodb-readmode-nearest) read mode, when combined with a tag set list, selects the matching member with the lowest network latency. This member may be a primary or secondary.

| Mode | Notes |
| --- | --- |
| [`primaryPreferred`](/docs/manual/core/read-preference#mongodb-readmode-primaryPreferred) | Specified tag set list only applies if selecting eligible secondaries. |
| [`secondary`](/docs/manual/reference/glossary#std-term-secondary) | Specified tag set list always applies. |
| [`secondaryPreferred`](/docs/manual/core/read-preference#mongodb-readmode-secondaryPreferred) | Specified tag set list only applies if selecting eligible secondaries. |
| [`nearest`](/docs/manual/core/read-preference#mongodb-readmode-nearest) | Specified tag set list applies whether selecting either primary or eligible secondaries. |

For information on the interaction between the [modes](/docs/manual/core/read-preference#std-label-replica-set-read-preference-modes) and tag set lists, refer to the [specific read preference mode documentation.](/docs/manual/core/read-preference#std-label-replica-set-read-preference-modes)

For information on configuring tag set lists, see the [Configure Replica Set Tag Sets](/docs/manual/tutorial/configure-replica-set-tag-sets) tutorial.
