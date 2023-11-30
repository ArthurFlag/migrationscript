
## Data flow architecture

When you enable CCR on your Aiven for Apache Cassandra service, you
connect to another service so that the two services (CCR pair) can
replicate data to each other. The CCR service pair constitutes a single
Apache Cassandra cluster that comprises nodes from the two services. The
services are located in different regions and the nodes of a single
service comprise a single datacenter.

:::mermaid

flowchart LR

:   subgraph Cluster_xy direction LR cluster_info\[\[\"User keyspace
    with replication:\<br\>NetworkTopologyStrategy {\'service_x\': 3,
    \'service_y\': 3}\"\]\] subgraph Service_x direction LR
    service_info_x\[\[cassandra.datacenter=service_x\]\] x1((node_x1))
    \-\-- x2((node_x2)) x2((node_x2)) \-\-- x3((node_x3)) x3((node_x3))
    \-\-- x1((node_x1)) end subgraph Service_y direction LR
    service_info_y\[\[cassandra.datacenter=service_y\]\] y1((node_y1))
    \-\-- y2((node_y2)) y2((node_y2)) \-\-- y3((node_y3)) y3((node_y3))
    \-\-- y1((node_y1)) end Service_x\<-. data_replication .-\>Service_y
    end
:::

## How it works

### Replication strategy

Apache Cassandra allows specifying the replication strategy when
creating a keyspace.

:::note What is the keyspace?
It is a namespace defining a replication strategy and particular options
for a group of tables.
:::