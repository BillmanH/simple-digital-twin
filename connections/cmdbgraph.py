import os,sys, ssl

from functools import reduce

import numpy as np


from gremlin_python.driver import client, protocol, serializer
from gremlin_python.driver.protocol import GremlinServerError


import asyncio

# # NOTE: If you are running this in REPL (Like a jupyter notebook or IPython), then you need to add this code:
# ssl._create_default_https_context = ssl._create_unverified_context
# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# import nest_asyncio
# # this is required for running in a Jupyter Notebook. 
# nest_asyncio.apply()


if sys.platform == 'win32':
    print("executing local windows deployment")


# ASSERTIONS: 
# Nodes must have expected values
expectedProperties = ['label','dtdlid','name']
notFloats = ['dtdlid','id','dtid','objid']

class GraphFormatError(Exception):
    """data structure error graph error message for cosmos/gremlin checks"""
    pass


# class ConnectionIssue(Exception):
#     print("Exodest cmdb connetion issue: ")
#     pass

#%%
class CosmosdbClient():
    # TODO: build capability to 'upsert' nodes instead of drop and replace. 
    """s
    cb = CosmosdbClient()
    cb.add_query()
    cb.run_queries()

    data format = `{"nodes":nodes_list,"edges":edges_list}`

    node format = {
        'label':'foo',
        'dtdlid':'00001',
        'name':'myname'
    }
    

    edge format = `{'node1':0000,'node2':0001,'label':'hasRelationship',...other properties}`
        it's always the dtdlid of the nodes, connecting to the dtdlid of the ohter node. 

    """
    def __init__(self, localConfig=None) -> None:
        if localConfig:
            self.endpoint = localConfig['CMDB_URL']
            self.username = localConfig['CMDB_DATABASE']
            self.password = localConfig['CMDB_KEY']
        else:
            self.endpoint = os.getenv("CMDB_URL","env vars not set")
            self.username = os.getenv("CMDB_DATABASE","env vars not set")
            # TODO: Conda commands don't work with the `==` keys, so I'm arbitrarily adding them here. This should be fixed later.
            #       Meantime, you can just enter the key without the equal signs at the end. 
            self.password = os.getenv("CMDB_KEY","env vars not set")+"=="
        self.c = None
        self.res = "no query"
        self.stack = []
        self.stacklimit = 15
        self.res_stack = {}

    ## Managing the client
    def open_client(self):
            self.c = client.Client(
                self.endpoint,
                "g",
                username=self.username,
                password=self.password,
                message_serializer=serializer.GraphSONSerializersV2d0()
            )
            
    def close_client(self):
        self.c.close()


    ## cleaning results
    def cs(self, s):
        # Clean String
        s = (str(s).replace("'", "")
                .replace("\\","-")
            )
        return s
    
    ## Managing the queries 
    def run_query(self, query="g.V().count()"):
        self.open_client()
        callback = self.c.submitAsync(query)
        res = callback.result().all().result()
        self.close_client()
        self.res = res

    def run_query_from_list(self, query="g.V().count()"):
        callback = self.c.submitAsync(query)
        # res = callback.result().all().result()
        res = callback
        self.res = res

    def collect_anchors(self, scene_id):
        query = f"""g.V().has('dtid','{scene_id}').as('boundary')
                .in().has('label','area').as('area')
                .in('isin').as('elements')
                .in('has').as('anchor')
                    .path()
                        .by(values('dtid','name','local_x','local_y','local_z').fold())
                        .by(values('dtid','name','displayname').fold())
                        .by(values('dtid','name','displayname','description','manufacturer','model_no','volume').fold())
                        .by(values('dtid','local_x','local_y','local_z','volume').fold())
                """.strip()
        self.open_client()
        callback = self.c.submitAsync(query)
        res = callback.result().all().result()
        self.close_client()
        self.res = res
        return res


    def add_query(self, query="g.V().count()"):
        self.stack.append(query)

    def run_queries(self):
        self.open_client()
        res = {}
        for q in self.stack:
            self.run_query_from_list(q)
            res[q] = self.res
        self.res = res
        self.stack = []
        self.close_client()

    
    def parse_properties(self,node):
        """
        used in actions and other places where json is nested in properties. 
        example:
                'properties': {'type': [{'id': 'de09040b-2c60-4a8a-b640-d78a248688f9',
                        'value': 'healthcare_initiatives'}],
                    'applies_to': [{'id': 'd753c296-7b62-4eb4-8e18-df39a67977ea',
                        'value': 'pop'}],
        returns nicely formated dict
        """
        n = {}
        for k in node["properties"].keys():
            if len(node["properties"][k]) == 1:
                n[k] = node["properties"][k][0]["value"]
        return n

    def parse_all_properties(self,res):
        """
        meant to pas in one response item at a time:
            `self.actions = [self.c.parse_all_properties(i) for i in self.c.res]`
        """
        r = {}
        for part in self.res[0].keys():
            if res[part]['type']=='edge':
                r[part] = res[part]['properties']
            else:
                r[part] = self.parse_properties(res[part])
        return r



    def create_custom_edge(self,n1,n2,label):
        edge = f"""
        g.V().has('dtdlid','{n1['dtdlid']}')
            .addE('{label}')
            .to(g.V().has('dtdlid','{n2['dtdlid']}'))
        """
        return edge
    
    # creating strings for uploading data
    def create_vertex(self,node):
        node['dtid'] = str(node['dtid'])
        # TODO: objid here for backwards compatability. remove in next graphdb updeate.
        node['objid'] = str(node['dtid'])
        if (len(
            [i for i in expectedProperties 
                if i in list(node.keys())]
                )>len(expectedProperties)
            ):
            raise GraphFormatError
        gaddv = f"g.addV('{node['label']}')"
        properties = [k for k in node.keys()]
        for k in properties:
            # converting boolian values to gremlin bools
            if type(node[k])==bool:
                node[k]=str(node[k]).lower()
            # try to convert objects that aren't ids
            if k not in notFloats:
                #first try to upload it as a float.
                try:
                    rounded = np.round_(node[k],4)
                    substr = f".property('{k}',{rounded})"
                except:
                    substr = f".property('{k}','{self.cs(node[k])}')"
            else:
                substr = f".property('{k}','{self.cs(node[k])}')"
            gaddv += substr

        gaddv += f".property('objtype','{node['label']}')"
        return gaddv

    def create_edge(self, edge):
        gadde = f"g.V().has('dtid','{edge['node1']}').addE('{self.cs(edge['label'])}')"
        for i in [j for j in edge.keys() if j not in ['label','node1','node2']]:
            gadde += f".property('{i}','{edge[i]}')"
        gadde_fin = f".to(g.V().has('dtid','{self.cs(edge['node2'])}'))"
        return gadde + gadde_fin


    def upload_data(self, data, verbose=True):
        """
        uploads nodes and edges in a format `{"nodes":nodes,"edges":edges}`.
        edge format:
            `{'node1':0000,'node2':0001,'label':'hasRelationship',...other properties}`
        Each value is a list of dicts with all properties. 
        Extra items are piped in as properties of the edge.
        Note that edge lables don't show in a valuemap. So you need to add a 'name' to the properties if you want that info. 
        """
        # TODO: I removed the field tests because it wasn't relefant. I'll add it back in at some point. 
        # data = self.test_fields(data)
        for node in data["nodes"]:
            if verbose:
                print(f'loading {node}')
            n = self.create_vertex(node)
            self.add_query(n)
            if len(self.stack)>self.stacklimit:
                self.run_queries()
        if verbose:
            print(" sending -> ",end=' ')
        self.run_queries()
        if verbose:
            print(' sent.')    
        for edge in data["edges"]:
            e = self.create_edge(edge)
            self.add_query(e)
            if len(self.stack)>self.stacklimit:
                self.run_queries()
        self.run_queries()

    def patch_property(self, dtdlid, property, value):
        """
        updates a specific property on a specific object
        """
        query = f"""
        g.V().has('dtdlid','{dtdlid}').property('{property}','{value}')
        """ 
        res = self.run_query(query)
        self.res = res 

    def __repr__(self) -> str:
        return f"<CBDB Graph Connector: >"
    

# g.V().has('dtid','boundary17529430240082').as('boundary')
# .in().has('label','area').as('area')
# .in('isin').as('elements')
# .in('has').as('anchor')
#     .path()
#         .by(values('dtid','name','local_x','local_y','local_z').fold())
#         .by(values('dtid','name','displayname').fold())
#         .by(values('dtid','name','displayname','description','manufacturer','model_no','volume').fold())
#         .by(values('dtid','local_x','local_y','local_z','volume').fold())