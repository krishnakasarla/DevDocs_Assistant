> For the complete MongoDB documentation index, see www.mongodb.com/docs/llms.txt

# Start with Sharded Clusters

We recommend starting with a single sharded cluster when you are building a new application regardless of your immediate need for multiple shards.

The following scenarios benefit from sharded cluster architecture:

| Use Case | Description |
| --- | --- |
| Cost Optimization | Vertical scaling becomes increasingly expensive and less effective as hardware requirements grow. Horizontal scaling offers more predictable and cost-effective scaling as resource demands increase. |
| High Concurrent Collection Access | Applications with multiple active collections where resource contention results in performance bottlenecks. Sharding distributes collections across dedicated hardware, preventing resource contention. |
| High-Throughput Workloads | Applications with high read/write volumes benefit from distributing traffic across multiple machines, improving performance and reducing bottlenecks. |
| Large Data Sets | If your data volumes grow rapidly or working sets exceed single-server memory capacity, horizontal scaling ensures sustainable performance by distributing data across multiple nodes. |
| Multi-Tenant Environments | Applications serving multiple customers benefit from having dedicated shards per tenant, providing performance isolation and customized resource allocation. MongoDB's sharding features enable efficient multi-tenant architectures. |
| Global Deployments | When your users are spread across different regions, distributing data across geographically positioned shards reduces latency and enhances the user experience. |

## Details

Starting with a sharded cluster is a proactive approach that offers:

- Effortless Horizontal Scaling – You can easily add shards as your application grows, without the complexity of migrating from a replica set.

- Cost-Effective Infrastructure – MongoDB 8.0 introduces [config shards](/docs/manual/core/config-shard#std-label-config-shard-concept), allowing you to set up a sharded cluster on a single replica set infrastructure without dedicated config servers. In MongoDB Atlas, sharded clusters with up to 3 shards in version 8.0 use config shards by default.

Consider adding shards when your database reaches 60-70% of resource utilization (RAM, vCPUs, or storage) of a sizable machine. For example, in Atlas, consistent 60-70% resource utilization of an M60 machine with a 4 TB disk indicates an additional shard should be added.

## Learn More

- [Manage Unsharded Collections](/docs/manual/core/sharding-manage-unsharded-collections#std-label-sharding-manage-unsharded-collections)

- [Distribute Collection Data](/docs/manual/core/sharding-distribute-collection-data#std-label-sharding-distribute-collection-data)
