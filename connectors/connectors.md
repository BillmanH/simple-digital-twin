# Data Connectors

The components of the application are meant to be interchangable. So you should be able to quickly add your connector here if the version included isn't a match for your system. Do consider contributing if you add a new open source connector. 

## CosmosDB Gremlin Graph
[About CosmosDB and Gremlin](https://learn.microsoft.com/en-us/azure/cosmos-db/gremlin/support)

Connection requires the following environment variables. 
* `CMDB_KEY` - The access key provided by Azure. 
    - **Note** the key naturally comes with `==` characters, which causes issues in the local testing environment. So the `cmdbgraph` connector automatically reads it as "`<secret>==`". You need to delete the `==` from your env variable. 
* `CMDB_URL` - Web socket connection for gremlin. e.g. `wss://<your instance>.gremlin.cosmos.azure.com:443/`
* `CMDB_DATABASE` - the path of your graph databse. e.g. `/dbs/graphdb/colls/systems` which is created automatically in the ARM template. 

