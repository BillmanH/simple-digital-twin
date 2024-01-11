# %%

import ssl
import asyncio
import os, sys
import json
import pandas as pd
import numpy as np
import yaml

sys.path.append("..")
from connections import cmdbgraph


# TODO: Read these config vars from a config file
# Length of characters of the UUID
DTDL_ID_LENGTH = 13
MODELS_PATH = os.path.join('.','infra','demo','dtdl')

class TemplateNotFoundError(Exception):
    print("no template was found with the correct name in the infra folder")
    pass


# %%

class dtdl:
    def __init__(self, j):
        # Template stuff
        self.DTDL_ID_LENGTH = DTDL_ID_LENGTH

        print(f"creating model object for {j.get('name')}, from template {j.get('class')}")
        self.input_dict = j
        # Loading the template files
        self.template = self.read_json(self.input_dict['class'])
        if self.template.get('extends'):
            print(f"     * Template {self.template.get('@id','MissingID')} is extended from template: {self.template.get('extends')}")
            # TODO: extended templates will need a more robust process that can recursively collect from multiple extensions
            #       the current model just allows one extension. Createing a looping `get_extensions` function that returns an array of extention templates should do it.
            self.extensions = [self.read_json(self.template['extends'].replace('dtmi:com:adt:dtsample:','').replace(';1',''))]
        else:
            self.extensions = []
        if 'class' in j.keys():
            self.label = j['class']
        else:
            print('No class name found in input dictionary')

        # Building the model object to be uploaded
        self.model = {'name':'model not extablished'}
        self.build_model()
        self.name = j['name'] 

    def uuid(self):
        return self.input_dict.get('name','noName') + "".join([str(i) for i in np.random.choice(range(10), self.DTDL_ID_LENGTH)])
    
    def read_json(self,filename):
        # get load the template, and let the user know if the file is not found.
        path = os.path.join(MODELS_PATH,filename + '.json')
        try:
            template = json.load(open(path))
        except:
            print(f'ERROR: no file found at : {path}')
            TemplateNotFoundError()
        return template
   
    def build_model(self):
        model = {}
        for ext in self.extensions:
            # TODO: Process is not truly recursive. This will need to be updated to allow recursively building extensions
            for k in ext.keys():
                model[k.lower()] = ext[k]
        # Finally, load the template for the object
        for t in self.template.keys():
            if self.template[t]:
                model[t.lower()] = self.template[t]

        for t in self.input_dict.keys():
            if self.input_dict[t] != None:
                model[t] = self.input_dict[t]

        self.model = model
        # Attach a GUID for the object as dtdlid
        self.model['dtid'] = self.uuid()
        self.model['label'] = self.label

        # CosmosDB doesnt support nested objects very well, so we flattening the structure for the graph. 
        for item in self.model['contents']:
            if item['@type'] == "Property":
                self.model[item['name']] = self.input_dict[t]
        self.model.pop('contents')

    def get_node(self):
        return self.model
        
    def __repr__(self):
        return(f"<dtdl object - {self.label}:{self.name}>")
    


# %%

eq = pd.read_excel('infra/demo/equipment.xlsx', sheet_name='Equipment').dropna(axis=0, subset='id').replace(np.nan, None, regex=True)
rel = pd.read_excel('infra/demo/equipment.xlsx', sheet_name='Relationships')
dtdls = [dtdl(i) for i in eq.to_dict('records')]

# %%
pd.DataFrame([d.get_node() for d in dtdls])
# %%
d = dtdl(eq.to_dict('records')[6])
d.get_node()
# %%
dtdls[6].input_dict
# %%
# Uploading the models to the graph

PARAMS = yaml.safe_load(open('infra/demo/cmdbkeys.yml'))
# %%

# ssl._create_default_https_context = ssl._create_unverified_context
# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# import nest_asyncio
# # this is required for running in a Jupyter Notebook. 
# nest_asyncio.apply()


# %%
c = cmdbgraph.CosmosdbClient(PARAMS['cosmosdb'])

# c.run_query()
# %%

# %%
rel['node1'] = rel['from'].apply(lambda x: [d for d in dtdls if d.get_node()['id']==x][0].get_node()['dtid'])
rel['node2'] = rel['to'].apply(lambda x: [d for d in dtdls if d.get_node()['id']==x][0].get_node()['dtid'])
rel['label'] = rel['name']
rel
# %%
vertecies = [c.create_vertex(node) for node in [d.get_node() for d in dtdls]]
# %%
edges = [c.create_edge(edge) for edge in rel.to_dict('records')]
# %%
